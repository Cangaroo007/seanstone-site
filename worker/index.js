/**
 * id.seanstone.com — the site's server side.
 *
 *   GET  /          visitor identity: city, network and, where it resolves, company.
 *   POST /enquiry   the enquiry the page composed, forwarded to Sean's inbox.
 *
 * Account level only. Never a person, unless a person types their own address
 * into the compose panel and presses send. See TIER1-INTELLIGENCE.md.
 *
 * Two identity sources, both cheap on purpose:
 *
 *   1. Cloudflare's own `request.cf` — city, region, country and the AS organisation.
 *      Free, no vendor, no key, always present.
 *   2. IPLocate — adds a clean company name, domain and TYPE. Free tier is 1,000
 *      requests a day, forever, and its licence explicitly permits displaying the
 *      returned data to the end user, which most competitors' terms do not.
 *      Set the key with:  wrangler secret put IPLOCATE_KEY
 *
 * Email goes out through Cloudflare Email Service's `send_email` binding. Sending
 * to a VERIFIED DESTINATION ADDRESS on your own account is free on every plan,
 * including the free one — and the only recipient here is Sean, so no Workers Paid
 * plan, no third-party mail vendor and no API key are involved.
 *   wrangler.toml:  [[send_email]]
 *                   name = "EMAIL"
 *                   destination_address = "sean@cangaroo.ai"
 * The destination_address attribute pins the binding: this Worker cannot email
 * anybody else even if it is compromised or misused.
 */

const ALLOWED = ['https://seanstone.com', 'https://www.seanstone.com'];

// A residential ISP, a data centre or a mobile carrier is not an employer. Showing
// "You're visiting from Telstra Corporation" is worse than showing nothing at all,
// so these types are resolved but never surfaced as a company.
const NOT_A_COMPANY = ['isp', 'hosting', 'mobile', 'education_and_research'];

const TO   = 'sean@cangaroo.ai';
const FROM = 'site@seanstone.com';

// A public POST endpoint is a public POST endpoint. Cheap in-memory throttle per
// isolate, plus hard caps on size, so nobody can turn this into a mail relay.
const MAX_BODY = 12000;
const RATE = { max: 5, windowMs: 15 * 60 * 1000 };
const seen = new Map();

function cors(origin) {
  const allow = ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8',
  };
}

function throttled(ip) {
  const now = Date.now();
  const hits = (seen.get(ip) || []).filter((t) => now - t < RATE.windowMs);
  hits.push(now);
  seen.set(ip, hits);
  if (seen.size > 5000) { seen.clear(); }        // isolates are cheap; leaks are not
  return hits.length > RATE.max;
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function identity(request, env) {
  const cf = request.cf || {};
  const out = {
    city: cf.city || null,
    region: cf.region || null,
    country: cf.country || null,
    timezone: cf.timezone || null,
    network: cf.asOrganization || null,
    asn: cf.asn || null,
    company: null,
  };

  if (env.IPLOCATE_KEY) {
    try {
      const ip = request.headers.get('CF-Connecting-IP');
      // Cached at Cloudflare's edge for a day: the same handful of ISP ranges
      // account for most traffic, so this keeps us far inside the free tier.
      const r = await fetch(
        `https://iplocate.io/api/lookup/${ip}?apikey=${env.IPLOCATE_KEY}`,
        { cf: { cacheTtl: 86400, cacheEverything: true } }
      );
      if (r.ok) {
        const d = await r.json();
        const c = d.company;
        if (c && c.name && !NOT_A_COMPANY.includes(String(c.type || '').toLowerCase())) {
          out.company = { name: c.name, domain: c.domain || null, type: c.type || null };
        }
        // IPLocate's city data is generally finer-grained than Cloudflare's.
        if (d.city) { out.city = d.city; }
      }
    } catch (e) {
      // Enrichment is a bonus, never a dependency. Fall through with what we have.
    }
  }
  return out;
}

async function enquiry(request, env, headers) {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (throttled(ip)) {
    return new Response(JSON.stringify({ ok: false, error: 'rate_limited' }), { status: 429, headers });
  }

  const raw = await request.text();
  if (!raw || raw.length > MAX_BODY) {
    return new Response(JSON.stringify({ ok: false, error: 'bad_size' }), { status: 400, headers });
  }

  let d;
  try { d = JSON.parse(raw); } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: 'bad_json' }), { status: 400, headers });
  }

  const body    = String(d.body || '').slice(0, 8000).trim();
  const subject = String(d.subject || 'Enquiry from seanstone.com').slice(0, 160).trim();
  const email   = String(d.email || '').slice(0, 200).trim();
  if (!body) {
    return new Response(JSON.stringify({ ok: false, error: 'empty' }), { status: 400, headers });
  }
  // Loose on purpose: a wrong-looking address is still worth delivering, it just
  // does not get used as Reply-To.
  const replyTo = /^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(email) ? email : '';

  const cf = request.cf || {};
  const meta = [
    replyTo ? `reply to: ${replyTo}` : 'no reply address given',
    d.company ? `company: ${d.company}` : '',
    d.city || cf.city ? `city: ${d.city || cf.city}${cf.country ? ', ' + cf.country : ''}` : '',
    cf.asOrganization ? `network: ${cf.asOrganization}` : '',
    `score: ${Number(d.score) || 0} · ${Number(d.depth) || 0}% read`,
    `page: ${String(d.page || '/').slice(0, 120)}`,
  ].filter(Boolean).join('\n');

  const text = `${body}\n\n---\n${meta}\n`;
  const html = `<div style="font:15px/1.6 -apple-system,Segoe UI,sans-serif;color:#101513">
<pre style="font:13px/1.65 ui-monospace,Menlo,monospace;white-space:pre-wrap;margin:0 0 20px">${esc(body)}</pre>
<hr style="border:0;border-top:1px solid #ddd;margin:20px 0">
<pre style="font:12px/1.6 ui-monospace,Menlo,monospace;white-space:pre-wrap;color:#5D665F;margin:0">${esc(meta)}</pre>
</div>`;

  try {
    const sent = await env.EMAIL.send({
      to: TO,
      from: FROM,
      subject: `[seanstone.com] ${subject}`,
      ...(replyTo ? { replyTo: replyTo } : {}),
      text,
      html,
    });
    return new Response(JSON.stringify({ ok: true, id: sent && sent.messageId }), { headers });
  } catch (e) {
    // The page falls back to copy-to-clipboard and mailto, so a failure here is
    // recoverable for the visitor. Report it honestly rather than pretending.
    return new Response(
      JSON.stringify({ ok: false, error: (e && e.code) || 'send_failed' }),
      { status: 502, headers }
    );
  }
}

export default {
  async fetch(request, env) {
    const headers = { ...cors(request.headers.get('Origin') || '') };
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: { ...headers, 'Access-Control-Max-Age': '86400' } });
    }

    if (url.pathname === '/enquiry') {
      if (request.method !== 'POST') {
        return new Response(JSON.stringify({ ok: false, error: 'post_only' }), { status: 405, headers });
      }
      return enquiry(request, env, headers);
    }

    const out = await identity(request, env);
    return new Response(JSON.stringify(out), {
      headers: { ...headers, 'Cache-Control': 'private, max-age=3600' },
    });
  },
};

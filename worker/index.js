/**
 * id.seanstone.com — visitor identity lookup for seanstone.com
 *
 * Account level only. Returns the city, the network and (where it resolves) the
 * company. Never a person. See TIER1-INTELLIGENCE.md for why that line matters.
 *
 * Cloudflare gives city, country and network for free in `request.cf` — no vendor,
 * no key, no cost. The IPinfo call is optional enrichment; without a token the
 * Worker still returns something useful.
 */

const ALLOWED = ['https://seanstone.com', 'https://www.seanstone.com'];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allow = ALLOWED.includes(origin) ? origin : ALLOWED[0];

    const headers = {
      'Access-Control-Allow-Origin': allow,
      'Content-Type': 'application/json; charset=utf-8',
      // Cache per-visitor for an hour at the edge; keeps the free tier comfortable.
      'Cache-Control': 'private, max-age=3600',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: { ...headers, 'Access-Control-Allow-Methods': 'GET, OPTIONS' } });
    }

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

    // Optional: resolve the network to an actual company.
    // wrangler secret put IPINFO_TOKEN
    if (env.IPINFO_TOKEN) {
      try {
        const ip = request.headers.get('CF-Connecting-IP');
        const r = await fetch(`https://ipinfo.io/${ip}?token=${env.IPINFO_TOKEN}`, {
          cf: { cacheTtl: 3600, cacheEverything: true },
        });
        if (r.ok) {
          const d = await r.json();
          if (d.company && d.company.type === 'business' && d.company.domain) {
            out.company = { name: d.company.name, domain: d.company.domain };
          }
        }
      } catch (e) {
        // Enrichment is a bonus, never a dependency. Fall through with what we have.
      }
    }

    return new Response(JSON.stringify(out), { headers });
  },
};

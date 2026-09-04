/**
 * id.seanstone.com — visitor identity lookup for seanstone.com
 *
 * Account level only. Returns the city, the network and — where it resolves — the
 * company. Never a person. See TIER1-INTELLIGENCE.md for why that line matters.
 *
 * Two sources, both cheap on purpose:
 *
 *   1. Cloudflare's own `request.cf` — city, region, country and the AS organisation.
 *      Free, no vendor, no key, always present.
 *   2. IPLocate — adds a clean company name, domain and TYPE. Free tier is 1,000
 *      requests a day, forever, and its licence explicitly permits displaying the
 *      returned data to the end user, which most competitors' terms do not.
 *      Set the key with:  wrangler secret put IPLOCATE_KEY
 *
 * Without the key the Worker still returns everything in (1) and the panel degrades
 * to naming the network rather than the company.
 */

const ALLOWED = ['https://seanstone.com', 'https://www.seanstone.com'];

// A residential ISP, a data centre or a mobile carrier is not an employer. Showing
// "You're visiting from Telstra Corporation" is worse than showing nothing at all,
// so these types are resolved but never surfaced as a company.
const NOT_A_COMPANY = ['isp', 'hosting', 'mobile', 'education_and_research'];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allow = ALLOWED.includes(origin) ? origin : ALLOWED[0];

    const headers = {
      'Access-Control-Allow-Origin': allow,
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'private, max-age=3600',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: { ...headers, 'Access-Control-Allow-Methods': 'GET, OPTIONS' },
      });
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

    return new Response(JSON.stringify(out), { headers });
  },
};

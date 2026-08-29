# Tier 1 — company identification

*Design spec, not built. Tier 0 (everything the browser gives away, all client-side) shipped
in v0.8. This is the next step if and when it's worth it.*

The goal: the panel says **"You're visiting from Salesforce's network"** instead of
"Anonymous visitor". For a revenue audience that is the single most impressive thing a
website can do, because it's the thing they all wish theirs did.

---

## 1 · What's actually achievable

Set expectations before building anything. Independent analysis, as at 2026:

| | Realistic match rate | Coverage |
|---|---|---|
| **Account-level** (which company) | **30–50%** of total traffic | Global, better on direct/organic than paid social |
| **Person-level** (which human) | **10–30%** | Primarily US |

Vendors advertise 60–90%. That is not what independent measurement finds. Assume **one
visitor in three** resolves to a company, that a good share of those are an ISP or a VPN
rather than an employer, and design the panel so a miss looks deliberate rather than broken.

**Design consequence:** the company line must degrade gracefully. "Visiting from Telstra in
Brisbane" is honest and still interesting. "Unknown network" is fine. Never guess.

---

## 2 · Architecture

GitHub Pages is static, so identification needs one server call. Cloudflare Workers is the
obvious host — seanstone.com is already on Cloudflare, and the free tier is 100k requests a
day, roughly a thousand times more than this site will need.

```
browser ──fetch──▶ id.seanstone.com (Cloudflare Worker)
                     │  reads request.cf and the client IP
                     │  calls an IP-intelligence API
                     ◀──┘ returns { company, domain, industry, size, city, country, isIsp }
```

The Worker, not the browser, holds the API key. The browser never sees it, and the IP never
reaches a third party from the visitor's own machine.

### Worker sketch

```js
export default {
  async fetch(req, env) {
    const ip = req.headers.get('CF-Connecting-IP');
    const cf = req.cf || {};                    // Cloudflare gives geo + ASN free
    const cors = {
      'Access-Control-Allow-Origin': 'https://seanstone.com',
      'Cache-Control': 'public, max-age=3600',
      'Content-Type': 'application/json',
    };

    // Cloudflare alone gives you city, country, ASN and the network name —
    // enough for a useful answer with no third party at all.
    const base = {
      city: cf.city, country: cf.country,
      network: cf.asOrganization, asn: cf.asn,
    };

    // Optional enrichment. Skip it and the panel still has something to say.
    let company = null;
    if (env.IPINFO_TOKEN) {
      const r = await fetch(`https://ipinfo.io/${ip}?token=${env.IPINFO_TOKEN}`);
      if (r.ok) {
        const d = await r.json();
        if (d.company && d.company.type === 'business') {
          company = { name: d.company.name, domain: d.company.domain };
        }
      }
    }
    return new Response(JSON.stringify({ ...base, company }), { headers: cors });
  }
};
```

**Worth noting:** `request.cf.asOrganization` is free, needs no vendor, and already
distinguishes "Amazon Technologies" from "Telstra" from "Deloitte Touche Tohmatsu". Build
that first and see whether the paid layer adds anything before paying for it.

### Deployment

1. `npm create cloudflare@latest id-worker`
2. Paste the Worker above, `npx wrangler secret put IPINFO_TOKEN` if using enrichment
3. `npx wrangler deploy`, then add a route for `id.seanstone.com` in the Cloudflare dashboard
4. In `template.html`, one `fetch()` on load, feeding the same `logEvent`/`paint` pipeline
   Tier 0 already uses

---

## 3 · Vendor options, if the free layer isn't enough

| Vendor | Level | Match rate | From |
|---|---|---|---|
| **Cloudflare `request.cf`** | Network / ASN | ~100% (network, not company) | **free** |
| **IPinfo / ipapi** | Account | modest | free tier, then ~$50/mo |
| **Factors** | Account + analytics | up to 75% on ICP traffic | $99/mo |
| **Leadfeeder / Dealfront** | Account | 30–40% | €99/mo |
| **RB2B** | Person, US only | 15–30% | free tier |
| **Warmly** | Account + chat | 40–50% | ~$700/mo |
| **6sense, Clearbit** | Account + intent | 50–60% | enterprise |

Start at the top of that table. The gap between "free" and "$99/mo" is much smaller than the
vendors would like you to believe for a site with this traffic volume.

---

## 4 · Privacy — the line to hold

- **Account-level is defensible.** Resolving an IP to a company is generally outside GDPR
  because it isn't personal data, is not classed as personal information under CCPA/CPRA,
  and is PECR-compliant when the matching happens server-side. That is the line.
- **Person-level is a different thing entirely.** It needs a lawful basis, carries real
  obligations, and — for a site whose entire argument is that you build revenue systems
  *honestly* — it costs more in credibility than it returns. Don't.
- Sean is in California. CPRA applies to the site regardless of where it's hosted.

**"We identify the company, never the person"** is a good sentence to be able to say to a
prospect. It's a differentiator, not a limitation.

---

## 5 · The copy that has to change

The panel currently says:

> Nothing leaves your browser — a small note is kept there so the page recognises you next
> time.

That is true today and it is load-bearing: the site's whole argument is that it does
honestly what it claims. The moment a `fetch()` goes out, that sentence is a lie and the
argument collapses with it. Replace it with something like:

> Your browser tells us the rest. We look up the *network* you're on — the company, never
> the person — and nothing here is stored on a server.

Say it plainly, in the panel, before showing the company name. Being visibly straight about
the mechanism is more impressive to this audience than the mechanism itself.

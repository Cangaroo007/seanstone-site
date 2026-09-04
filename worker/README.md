# The identity Worker

Turns *"Pacific time"* into *"San Francisco"*, names the network the visitor is on, and —
where it resolves — their company and logo. Account level only, never person level.

## Deploy it

```bash
cd worker
npm install -g wrangler          # once
wrangler login                   # opens a browser
wrangler deploy
```

Wrangler will offer to create the `id.seanstone.com` custom domain when it sees the route
in `wrangler.toml`. Say yes — it adds the DNS record for you.

**Test it:**

```bash
curl -s https://id.seanstone.com | python3 -m json.tool
```

You should get your real city, your ISP or company as `network`, and `company: null` unless
you've added the optional token below.

## Then switch it on in the site

In `src/site.json`:

```json
"identity": { "endpoint": "https://id.seanstone.com" }
```

Then `python3 build.py`, commit, push. An empty `endpoint` disables the whole thing and the
panel falls back to the browser-only version — so it degrades cleanly if the Worker is ever
down or removed.

## Optional: company resolution

Cloudflare alone already distinguishes "Deloitte Touche Tohmatsu" from "Comcast Cable" in
the `network` field, which is most of the value. To also get a clean company name and domain
(and therefore a logo), add an [ipinfo.io](https://ipinfo.io) token:

```bash
wrangler secret put IPINFO_TOKEN
```

Expect **30–50%** of traffic to resolve to a company, not the 60–90% vendors advertise. The
panel is built to degrade gracefully — an ISP name is honest and still interesting.

## Cost

Cloudflare Workers free tier is 100,000 requests a day. This site will use a few hundred a
month. The `request.cf` data costs nothing. IPinfo has a free tier and paid plans from
roughly $50/month if you outgrow it.

## What it deliberately does not do

- No person-level identification. It needs a lawful basis under GDPR, and it would cost more
  in credibility than it returns on a site whose argument is that Sean builds these systems
  honestly.
- No storage. Nothing is written down; the response is computed per request and cached at
  the edge for an hour.

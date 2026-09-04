# Build log

## 4 Sep 2026 — v1.5: three ways in, and an honest ceiling

Sean: *"We need to move an enquiry form near the top... I don't want a typical form, what can we
do that is more dynamic and engaging."* And separately: *"emphasise that what the website is
doing is our base level engagement package... I don't want people thinking this type of
tracking is all we do."*

Both notes point at the same weakness. The page was very good at being impressive and
comparatively bad at converting or at telling anyone what it was a sample of.

**The trap.** A Name / Email / Message box near the top would contradict the argument the page
spends 4,000 words making. *"Most websites collect leads. This one queries your business"* —
followed by a contact form — is a page arguing against itself. So none of the three hooks is a
form. Each delivers something before it asks for anything, and each composes an enquiry that
arrives already carrying what the page worked out on its own.

### 1. The sentence that fills itself in — under the hero

Two inline dropdowns in the display face:

> I want to fix **the enquiries we never call back** and I'd know it worked if **every enquiry
> got an answer inside the hour**.

Beneath it, a monospace strip headed **"Already known, without asking"** — company, city, local
time, weather there, visit number, device, referrer, declared segment — followed by *"I worked
all of that out before you typed anything. That is the entire pitch."*

That strip is the enquiry hook and the product demo in the same six inches of page. The
sentence is the opening two minutes of a discovery call, and the page has already done its half.

The tokens are **inline `<span role="button">`, not `<button>`**: a real button is an inline
block, so when the phrase wrapped the dashed underline ruled the entire line instead of
following the words. With `display:inline` and `box-decoration-break:clone` the rule breaks
correctly. Keyboard handlers restore Enter and Space.

### 2. One question that answers first — above the diagnostic

*"What is the number you want moved?"* Six chips. Picking one returns, immediately and without
an email: what the problem usually turns out to be, an hours range, and what I would need to
start. Framed as **"Before the seven questions, one"** so it reads as a deliberate on-ramp to
the diagnostic rather than a duplicate of it. Every answer ends with two doors — send it now,
or answer the seven.

### 3. Ask it something — before the CTA

Ten written answers, matched client-side on keyword overlap with a threshold. Cost, agencies,
speed, what happens if it fails, who writes the code, company size, changing CRM, and *"what
are you not good at"*, which is the one that earns the rest.

**A miss is the best outcome in the whole feature.** No answer in the bank means the page says
so — *"I have not written an answer to that one, which is a decent sign it is worth asking
properly"* — and hands them a mail draft with their own question already in it. Meanwhile the
log fires **"Asked something with no written answer — that is the one to reply to"** at weight
20. An unanswerable question is the highest-quality signal on the site and now the strongest
capture path.

### One composer behind all three

`contextBlock()` appends to every enquiry: company, city, local time, weather, visit history,
device, referrer, declared segment, time on page, scroll depth, score, the diagnostic's weakest
zone, the scope and its hours, and every question they typed. It signs off *"Sean — none of the
above was typed in. Reply to whatever is wrong about it."*

**Delivery is pre-composed `mailto:`, with copy-to-clipboard beside it.** Sean did not pick a
delivery option, so this is the assumption: it ships today, needs no key, stores nothing, and
keeps the privacy page true. The upgrade — POST to the existing Worker with mailto as a silent
fallback — is about an hour plus a free Resend key, and belongs with Sprint 4's CRM wiring
anyway. It would recover the people whose mail client swallows a mailto, which is not a small
number on mobile.

Note the honest consequence of mailto: **there is no email field**, because their mail client
supplies the address. A field that collects something the transport already knows is theatre.

### The tiers — the ceiling, said out loud

New section directly after the live dashboard, at exactly the moment a reader is thinking
*"nice tracking widget"*:

- **01 The instrumented front door** — *"You are inside this one."* Marked as the base
  engagement, 20–40 hours.
- **02 Into Road Runner** — the same event stream pointed at the platform instead of a panel.
  The connective layer between the front door and the systems that hold the business; answers
  the visitor from live data, writes the record, routes the account, tells the owner what to
  say. *"The difference between a page that watches and a system that acts."* Where most of the
  value is.
- **03 Built to your requirement** — configured quoting, brokered pricing, capacity, portals.
  Kervio is one of these, end to end.

Closing line: *"The tracking on this page is the demonstration, not the offer. Nobody has ever
bought analytics from me; they buy the layer above it."* A matching two-sentence version sits in
the rail itself, linking down to the section, because the rail is where the misreading happens.

### Also

- `.gitignore` for `worker/.wrangler/` — the v1.4 commit picked up wrangler's local account
  cache. Nothing secret (the account ID is already public in `wrangler.toml`) but it is not
  repo content.
- Privacy page gains a row for the enquiry hooks: composed in the browser, no endpoint,
  nothing posted.
- Verified in Playwright, both themes: token wrap, popover dismissal, mailto subject and body,
  the number answers, a keyword hit and a deliberate miss, and the tier ladder.

## 4 Sep 2026 — v1.4: the page writes them a note, and looks up their weather

Sprint 3, items 1 and 2. Neither needed a Worker change.

**Why the live site looked *less* specific than it should.** Sean noticed the panel saying
"Pacific time" with no company row, and asked whether we had actually shipped anything. The
Worker was fine — a direct call to `id.seanstone.com` returns the city, the network, and now
a real company object from IPLocate. The problem was that the `index.html` sitting on
seanstone.com still carried `"identity": {"endpoint": ""}`; it was built before the endpoint
was switched on, so `identify()` returned immediately and the panel fell back to the
browser-only time-zone proxy. v1.4 carries the endpoint. Nothing was broken, and nothing was
missing — a stale build was pretending the Worker did not exist.

**The note.** At genuine engagement — the diagnostic finished, two or more scope items
picked, contact details copied, or score 45+ *with* a third of the page read — a section
unhides and the page writes four or five paragraphs of prose addressed to the reader.
Composed at read time from facts it already holds: the company if it resolved, the city, the
local hour, whether that hour is outside working hours, the visit number, minutes on page,
scroll depth, leave-and-return count, the declared segment, whether they used the enquiry
engine, the weakest diagnostic zone with the fix I'd start on, and the scope they costed with
the hours and the months.

Three rules kept it honest:

- **No sentence exists without its fact.** There is no template with blanks. If the company
  didn't resolve, the sentence that would have named it is never written.
- **It shows its working.** A monospace receipt at the foot lists every fact it used, counted.
  The trick is only impressive if you can see it isn't a trick.
- **It is deliberately hard to trigger.** A note written to someone who has read two
  paragraphs is a parlour trick. `noteReady()` is the gate.

Re-composed only when a fact it uses actually changes — a stamp on the card compares the
inputs, so `paint()` can call it every second for nothing.

**The weather.** Once the Worker returns a real city, the browser asks open-meteo for the
current temperature and conditions there — geocode the city name, then one forecast call.
No key, no cookie, no account, and a *city name* goes over the wire, never an IP. Fahrenheit
for US visitors, Celsius everywhere else. It only runs when there is a real city: guessing
the weather from a time-zone proxy would be exactly the fakery the rest of the page argues
against, so with the Worker down the row simply never appears.

The line reads as prose in the note ("It is 57°F and foggy in San Francisco — the page went
and asked, a minute ago. It knows your city. It does not know your street"), which is the
point: it is the cheapest possible proof that the page is pulling live external data *about
the reader*, and the sentence immediately draws the boundary.

**Privacy page** gained a row for the open-meteo lookup and a paragraph about the note under
Automated assessment — generated from the same config, so it cannot drift.

**Verified** in Playwright across four states: Worker up with a company match, Worker down
(no geo, no weather, note still composes from browser facts), no declared segment with a
scope built, and an out-of-hours Sydney visitor. Two prose bugs found and fixed — outcome
names that contain "and" turned the scope list into a run-on, and "Somewhere on Sydney or
Melbourne" needed "in".

## 4 Sep 2026 — company resolution: don't pay for it

Sean offered to pay for the best IP-to-company service, strongest in the US and secondly
Australia. Two agents researched it. The answer is that he should not pay, and two things I
had told him earlier were wrong.

**Corrections.** IPinfo's Business API is **closed to new customers**; company data is now
Enterprise-tier only at a 1M+ requests/month minimum, so the plan I suggested does not exist
for a site with a few hundred lookups. And I quoted Warmly at "~$700/month" from a secondary
source — its AI web-deanonymisation product starts at **$10,000/year**.

**MaxMind would have been a trap.** Its EULA bans "displaying geolocation pairing
information" and displaying the services to others; standard pricing is internal-business-use
only. A public "you're visiting from Acme" panel needs a redistribution licence.

**Chosen: IPLocate free tier.** 1,000 requests/day forever, returns
`company{name, domain, type}`, and the API licence *explicitly* grants the right to
"receive, store, process, and display the data returned by the API" — which most competitors'
terms do not. Runner-up if a second source is ever wanted: **ipregistry**, $10 for 15,000
credits that never expire, attribution optional.

**Australia is structurally hard, and nobody has a number.** APNIC allocations sit largely
with Telstra, Optus and TPG/Vocus, so a mid-market Australian business on ordinary business
broadband resolves to the *carrier*, not the employer — no vendor fixes this. The only
published AU figure anywhere is a vendor's own (35–55% company-level vs 40–65% US, no sample
size). The genuinely strong international graphs are 6sense and Demandbase at a $63–69k/year
median. Live tests confirmed the pattern: organisations with their own ASN resolve cleanly
(University of Melbourne → unimelb.edu.au), ordinary businesses do not.

Also dead and removed from consideration: **Koala** (shut down 30 Sep 2025) and **Clearbit
Reveal** as a standalone (absorbed into HubSpot Breeze, HubSpot-only, no external API).

**Worker updated** to call IPLocate when `IPLOCATE_KEY` is set, cached at the edge for a day
so the free tier is never troubled, and to suppress `isp`, `hosting`, `mobile` and
`education_and_research` types — "You're visiting from Telstra Corporation" is worse than
showing nothing. Without the key it behaves exactly as before.

**The measurement that matters:** run it for a month and log what fraction of Australian
visitors resolve to a real company rather than a carrier. That single number is worth more
than every published benchmark in this category.

## 4 Sep 2026 — v1.3 — the Worker is live

`id.seanstone.com` deployed (version `2d25d1ec`) and switched on. Returns real data:

```json
{"city":"San Francisco","region":"California","country":"US",
 "network":"Webpass Inc.","asn":19165,"company":null}
```

**Deploy notes worth keeping.** Sean's `CLOUDFLARE_API_TOKEN` had DNS scope but not Workers,
and belonged to a *different account* (`1dba4525…`) than the zone (`16fbf46a…`). Fix was
`unset CLOUDFLARE_API_TOKEN` plus OAuth login. The Worker must live in the same account as
the zone or the custom domain will not attach.

**Consent now decides on the real country code, not the time zone.** This is the material
improvement: a visitor in Germany whose browser reports an American time zone previously got
no banner and had tags loaded. The gate now holds the tags until the lookup answers — capped
at 1.5 seconds, after which it falls back to the time-zone heuristic rather than blocking
analytics indefinitely. `identify()` takes a callback; `settleConsent()` is idempotent so
whichever fires first wins.

**Verified across three payloads** with the endpoint stubbed:

| Scenario | Banner | Loaded |
|---|---|---|
| US, real Worker payload | no | Cloudflare, GA4, ContentSquare |
| DE country with a US time zone | **yes** | Cloudflare only |
| US, company resolves to Salesforce | no | all three |

The panel now reads "1:02 PM · San Francisco, US" with a Network row, and the zone-proxy
explanation hides itself. With a company match the next action becomes "Someone from
Salesforce is on the page. You know the account before they have said a word."

`company` is null on residential connections — Webpass is an ISP, not an employer — which is
the expected 30–50% miss rate behaving correctly. An `IPINFO_TOKEN` secret would add
company resolution for corporate networks.

## 4 Sep 2026 — v1.2 — the screens

**DEPLOYED — commit `95f4d51`, verified live.** All seven images serving from
`seanstone.com/img/` with correct byte counts (326KB, 394KB, 171KB spot-checked). 2.00 MiB
pushed. First commit in this repo to carry binaries.

Seven product screenshots in, with captions, on both the work accordion and the case pages.
Sprint 1's biggest item closed: the work section is no longer text-only.

**Road Runner — four shots**, produced by a separate Cowork session and accompanied by an
unusually good build record. They were rebuilt as clean HTML from the real repos rather than
captured from production, so no customer data was handled; design tokens, nav structure and
form copy come from the source files, listed shot by shot. Fictional dataset documented and
fixed so any future shot stays consistent (Meridian Stone Co., Halberd Kitchens, Dana
Whitlock et al; ACMA fiction phone range).

**Kervio — three shots**, reconstructed here from Sean's production screenshots after
sampling the real palette (`#BDFE2C` lime, `#0B1118` ink). His originals could not be used:
all three were in an empty state, the pricing screen was showing `rate not available for
this fabrication` with two `RATE REQUIRED` rows, and the placeholder address said Buderim QLD
against a Newcastle NSW cover identity. Numbers are internally consistent across all three
frames — $17,218 subtotal, $1,721.80 GST, $18,939.80 total.

**Verified metrics replaced the qualitative claims** in two case studies, taking only what
the build record could evidence with a command:

- 170 per-client landing pages live, up from 150 three weeks earlier (`ls public/partners/*.html | wc -l`)
- 229 stonemasons mapped; only 20 had any recorded relationship before the reach view
- 3,025 organisations behind the enquiry form's company lookup
- 109 hours of build across May–June 2026

**Deliberately not used:** enquiry volume, segmentation split by role, and time-to-launch for
a landing page — no instrumented figure exists for any of them. The "40 minutes" visible in
the landing-page shot is set dressing and is not repeated as a claim anywhere in the copy.
The session that produced the shots flagged this itself, which is the right instinct.

**Layout:** one screenshot per row, not two. These are dense product UIs and halving the
width makes the detail — the thing that proves the claim — unreadable. Lazy-loaded, async
decoding, explicit alt text. `shotsHtml()` in the template and `render_case()` in `build.py`
produce the same markup and must be changed together.

**Still missing:** `roadrunner-03-form.png`, the self-segmenting enquiry form mid-branch.
It is in the build record but was not among the files supplied. That shot carries the
front-door thesis better than any of the other four.

## 4 Sep 2026 — v1.1 — region-aware consent, privacy page

Sean pushed back on an over-cautious read of ContentSquare, and was right: the CIPA §631
session-replay cases turn on interception of the *contents* of a communication — form
fields, chat, checkout — on high-traffic commercial sites where a class and a damages theory
exist. This site submits nothing anywhere; the enquiry engine is entirely client-side.
ContentSquare stays. It is also, for someone selling RevOps, evidence he runs the tooling he
talks about.

He also asked for Australia to be checked properly. Two agents researched OAIC primary
sources and reform status. Findings that changed the design:

- **No cookie banner is legally required in Australia.** There is no ePrivacy equivalent.
  APP 3.2's test for non-sensitive collection is "reasonably necessary", not consent;
  consent bites only for *sensitive* information under APP 3.3. APP Guidelines Ch B, fn 14:
  "Analytical information collected from cookies … will not be personal information under
  the Privacy Act unless an individual is reasonably identifiable." The OAIC itself runs
  Google Analytics behind a notice-only banner.
- **But APP 5 notification does apply**, and it is the obligation people fail. The OAIC's
  June 2026 pixel determinations (Medmate, Monash IVF) were about *sensitive* health data
  collected without consent — but the accompanying sweep found 77% of pixel users never
  mentioned them in a privacy policy. That is the gap worth closing here.
- Small business exemption (s 6D, under A$3M turnover) **still in force**, not scheduled for
  removal. Tranche 2 exposure draft (31 Aug 2026, consultation closes 18 Sep 2026) proposes a
  "fair and reasonable" test applying *regardless of consent* — worth tracking, not law.
- ADM transparency (APP 1.7–1.8) commences **10 December 2026** for APP entities.

### What was built

- **Region-aware consent gate.** Europe/EEA/UK get a banner and nothing loads until they
  choose; everywhere else the tags load immediately, which is what US and Australian law
  actually require — notice, not opt-in. Region by time zone now, by the Worker's country
  code once that is deployed.
- **Global Privacy Control honoured everywhere.** GPC signal present → no analytics at all,
  no banner. Twelve US states including California require this to be respected automatically.
- **Cloudflare Web Analytics is never gated** — it is cookieless and sets nothing on the
  device, so consent does not attach to it. It runs for every visitor.
- **`/privacy/` generated by `build.py` from the same config that emits the tags**, so the
  page cannot claim something the site does not do. Add or remove a tag and the table
  changes with it. Includes a voluntary automated-decision-making disclosure — the thing APP
  1.8 will require of larger entities from December 2026 — because a site about being
  straight with people should not wait to be asked.
- Footer links to the privacy page and a "Cookie choice" button to reopen the banner.

**Bug found and fixed in the same pass:** the `__ANALYTICS__` build placeholder was being
replaced *everywhere*, including inside `window.__ANALYTICS__` in the page's own JavaScript,
which produced `window.<script …>` and killed the entire script block. Placeholder is now an
HTML comment (`<!--ANALYTICS-->`) that cannot collide with JS identifiers.

Tested across regions with external requests stubbed: US and Australia load all three tags
with no banner; Germany and the UK show the banner and load only Cloudflare; GPC blocks
everything; accepting in the EU loads GA4 and ContentSquare and is remembered on reload.

## 29 Aug 2026 — v1.0 — analytics tags and the identity Worker

**Analytics are now build-time injected from `src/site.json`**, so IDs are data, not code.
An empty value means the tag simply is not emitted.

```json
"analytics": { "cloudflareToken": "", "ga4": "", "contentsquare": "597912112e565" }
```

ContentSquare is live (Sean's existing tag). Cloudflare Web Analytics and GA4 need their IDs
pasting in. `build.py` now prints which tags are on and whether the identity endpoint is set.

**The panel's disclosure was rewritten**, because "nothing leaves your browser" stops being
true the moment a tag loads:

> This panel runs in your browser; a small note is kept there so the page recognises you next
> time. The site also runs ordinary analytics — which is rather the point: you can measure
> everything and still know nothing about who is on your site.

Better than the original: it names the problem the site exists to solve.

**The identity Worker is written and tested** (`worker/`), but not deployed — it needs
`wrangler deploy`. Account level only: city, region, country and network/ASN from
`request.cf` (free, no vendor), plus optional company resolution via an IPinfo token.

Client side, with `identity.endpoint` set:

- **Local time becomes a real place** — "10:17 AM · San Francisco, US" replaces "Pacific
  time", and the zone-proxy explanation hides itself once a real city is known.
- **Network row** — "Salesforce.com Inc".
- **Company row with logo** via `logo.clearbit.com/<domain>`, free and keyless, with an
  `onerror` that removes the image rather than showing a broken one.
- **A company match rewrites the next action**: "Someone from Salesforce is on the page. You
  know the account before they have said a word."

Tested end to end against a mock endpoint: city, network, company and logo all render, the
next action changes, no console errors. With the endpoint empty the site is browser-only and
degrades silently — a dead or removed Worker cannot break the page, and the lookup has a
4-second timeout for the same reason.

## 29 Aug 2026 — v0.9 — prioritisation, work accordion, honest geography

Three things Sean called out, all fair.

**1 · Selecting a capability greyed things out instead of doing something.** It now
*re-ranks*. Capabilities are multi-select — pick what you actually need — and both the
evidence list and the work list reorder with a FLIP animation so you watch the page
rearrange itself. A bar states what happened: "Reordered around AI-directed product build.
2 of 4 projects evidence that — they are now first, and the top one is open." Unmatched
items are muted rather than buried, and still readable. The rail logs "You said you need
ai-directed product build — page re-ranked around it." This is the clearest demonstration
of dynamic content prioritisation on the site, and it is the Road Runner claim applied to
Sean's own page.

**2 · The work section was disjointed and linked to nothing.** It is now an accordion —
collapsed by default with name, kicker, thesis and *clickable capability chips* in each
header. The chips are the missing link: clicking one from a project re-ranks the whole page
around that capability, so the two sections are one mechanism instead of two lists. First
project opens by default; "Open all" toggles the lot.

**3 · "Los Angeles" when he is in San Francisco.** Not a bug — IANA zone names are region
proxies, and everyone from Vancouver to Tijuana is `America/Los_Angeles`. Naming the proxy
city is simply wrong, so the panel now names the region ("Pacific time") and explains the
gap underneath: *a browser gives a time zone, not a city; naming your actual city needs a
server-side lookup.* That is honest, it teaches the visitor something about their own data,
and it makes the case for Phase 2 far better than a marketing line would.

Also: no analytics of any kind are installed — see `ROADMAP.md`, Phase 1.

## 29 Aug 2026 — v0.8 — Tier 0 visitor intelligence

**DEPLOYED — commit `df15659`, verified live.** Local time, visits, attention and the
verdict header all confirmed serving from seanstone.com. Includes the v0.7 alignment and
alert fixes.

Everything the browser gives away, read client-side. No backend, no cost, no third party,
and the panel's "nothing leaves your browser" claim stays true.

- **Local time and timezone** — "10:05 am · Brisbane". Reading outside working hours is
  itself scored as a signal: personal interest, not a work errand.
- **Return-visitor memory** via localStorage — "3rd visit · first 4 days ago", with its own
  stage ("Returning visitor — came back") and a next action for the third visit with no
  enquiry. Wrapped in try/catch so a private window degrades to a first visit.
- **Device, browser and connection** — "Mac · Chrome · 4g".
- **Attention** — scroll depth, leaving and coming back (with the time away), and a signal at
  75% read ("that is not a bounce").
- **Copy detection** — copying anything containing an @ or a URL fires the strongest signal
  on the page and moves the stage to "Hand-raiser — took your details". Copying a passage
  logs separately: they are quoting you to someone.
- **Print detection** — printing or saving to PDF usually means showing someone else.

The rail's blurb now discloses the localStorage note, because the honesty of that panel is
the argument.

Tier 1 (company identification via a Cloudflare Worker) is specified but not built:
`TIER1-INTELLIGENCE.md`.

## 28 Aug 2026 — v0.7 — panel alignment and two bugs

- **The rail was floating at an arbitrary height.** It is sticky, so it can never line up
  with the scrolling column beside it — but it was offset 32px below its sticky point, which
  made the top edge land at a random place mid-section and read as a misalignment. It now
  docks at a constant 64px from the viewport top, which is exactly the hero's own top
  padding: aligned with the first screen at rest, and a deliberate constant gutter under the
  header thereafter.
- **Empty alert box showed on load.** `.alertbox{display:flex}` overrode the browser's
  `[hidden]{display:none}` (equal specificity, author sheet wins), so the box rendered with
  a heading and no content. Added `.alertbox[hidden]{display:none}`.
- **Alert appeared up to a second late.** `signal()` now repaints immediately rather than
  waiting for the next one-second tick.

## 28 Aug 2026 — v0.6 — the live panel, rebuilt as a verdict

**DEPLOYED — commit `7d910ee`, verified live.** Both fixes confirmed from outside:
the homepage serves the verdict panel, and `/case/kervio/` serves pre-rendered case copy
in the static HTML. `.nojekyll` is in the repo. Nothing outstanding on the deployment.

Sean has a working clone at `~/Downloads/ss-deploy/repo`, so future updates are:
`git pull`, drop in new files, `git add -A && git commit -m "..." && git push`.


Sean's note, and he was right: the telemetry panel was dynamic but didn't prove anything a
revenue person cares about. Event counters and a sparkline say "I can track things", which
is table stakes and impresses nobody. Rebuilt to answer the question a revenue buyer is
actually asking — *so what would you do about this visitor?*

- **Stage and next action promoted to the top**, in plain English: "Qualified — has costed
  the work", "Send the scope they built, priced, within the hour."
- **The alert card is the payoff.** Once someone completes the diagnostic, resolves an
  account in the enquiry engine, or builds a scope, the panel shows the actual message
  their sales team would receive — naming the weakest zone, the hours costed, the items
  chosen. That is the moment the argument lands.
- **Event log rewritten in plain English.** Was `crm.record.create → contact, tagged build`;
  now "Created a contact in the CRM, tagged build" and "Pulled their trading history from
  finance — $184,200 this year". Same events, readable by the buyer.
- **Sparkline and raw event counter deleted.** Decoration that made the panel look like
  analytics, which was the problem.
- **The duplicate account card removed** from the dashboard section — the rail already
  shows it. That section now leads with the alert message and the argument: *anyone can log
  page views; the value is the decision.* Retitled "You never filled in a form", which is
  the pain a revenue leader recognises.
- Rail scrolls internally now that it holds more, so the log stays reachable.

## 28 Aug 2026 — v0.5 — case studies pre-rendered

The case-study body was injected by JavaScript, so `/case/<id>/` served the homepage copy to
anything that doesn't execute JS — LinkedIn's card scraper, most SEO tools, any preview
unfurler. `build.py` now pre-renders each case's problem / built / changed into the static
HTML (`render_case()`, a server-side twin of `openCase()` in the template), ships the page
with `<body class="case-open">` so it displays without JS at all, and lets the JavaScript
re-render the identical markup and take over the interactions on load.

Also in this pass:

- **Per-page meta and OG descriptions** on each case page — previously all four inherited
  the homepage's description, which is worth nothing in a search result. The description is
  now the case's own opening line, and `og:description` is the project's thesis.
- **The back link is a real `<a href="/">`** in the static HTML, so it works with JS off.
- Verified both ways: JavaScript on (one visible section, listeners attached, no console
  errors) and JavaScript off (full case copy rendered, working back link).

*Note for future edits: `render_case()` in `build.py` and `openCase()` in `template.html`
produce the same markup and must be changed together.*

Files changed: `build.py`, `case/*/index.html` (all four). `index.html` is byte-identical.

## 28 Aug 2026 — v0.4 (current) — deployment ready

- **Restructured for GitHub Pages.** Deployables moved from `dist/` to the repo root, so
  Pages serves `/` with no build step of its own. `.build/` (gitignored) holds the Artifact
  variant. `CNAME` and `.nojekyll` are now generated by `build.py` rather than kept by hand.
- **Standalone case-study pages** at `/case/<id>/`, each with its own title, description,
  canonical and OG URL. Previously the case studies were hash-routed only, which Google
  ignores — these are four genuinely indexable pages targeting "Road Runner", "Kervio",
  the Alpha Surfaces work and Sales Hunters. The hash routes still work.
- **robots.txt and sitemap.xml**, both generated and both consistent with `flags.noindex`.
- **`flags.noindex`** added — live and linkable but out of search results, in one flag.
- **`GO-LIVE.md`** — the deployment runbook, written against the actual Cloudflare state
  from the 27 Aug cutover.

**Launch decision (28 Aug):** fully live and indexed, public repo. `engagementOffer: true`,
`showRates: true`, `noindex: false`. The flags remain if that needs to change.

**LIVE — 28 Aug 2026.** Pushed to `github.com/Cangaroo007/seanstone-site` (commit
`3832584`, "Instrumented site v0.4") and serving at https://seanstone.com over HTTPS.
Verified from outside: homepage, `/case/kervio/`, `/case/roadrunner/`, `/robots.txt` and
`/sitemap.xml` all return correctly, with the right per-page titles.

Two follow-ups noted at go-live:

1. **`.nojekyll` was never added.** GitHub is running Jekyll over the repo. Nothing breaks —
   no underscore-prefixed files exist — but add it when convenient, since a future file
   named `_something` would silently vanish.
2. ~~Case-study body copy is injected by JavaScript.~~ **Fixed in v0.5, below.**

## 28 Aug 2026 — v0.3

- **The Road Runner walkthrough is in.** A working replica of the Alpha Surfaces enquiry
  engine: four personas, each swapping the form to different fields; live company lookup
  against a sample CRM that returns account tier, trading YTD, owner and last activity;
  stock queries answered on the page from sample inventory; and a "what the business sees"
  panel showing the record, the routing, the priority and the next action as it is built.
  All of it feeds the same event log — `crm.match`, `finance.lookup`, `inventory.query`.
  Sample data is fictional and labelled on the page.
- **Case-study pages.** Problem → what was built → what changed, for all four projects.
  Hash-routed (`#case/roadrunner`) so they are shareable and linkable from LinkedIn, while
  the site stays one file.
- **Launch polish.** Open Graph tags and a generated share card (`tools/make_og.py`),
  canonical URL, inline SVG favicon, print stylesheet that produces a clean PDF, `CNAME`.
- **Rate set to $200/hr**, top of the fractional GTM-engineer band.
- **Domain set to seanstone.com** — Sean is the brand; contact stays sean@cangaroo.ai
  until a seanstone.com mailbox exists.

## 28 Aug 2026 — v0.2

Restructured into a real repo with a build step, and closed the gaps left in v0.1.

- **Split content from code.** `src/site.json` + `src/template.html` → `build.py` →
  `dist/index.html`. Copy and numbers are now editable without touching a line of code.
- **Wired the flags.** `engagementOffer: false` now actually removes the scope builder,
  drops the client router path and rewrites the CTA; `showRates: false` hides pricing.
  Both states tested clean, no console errors.
- **"Send it to me" on the scope builder** — a mailto with the full scope pre-filled in
  the body, including the diagnostic's weakest zone if they completed it. Previously it
  was copy-to-clipboard only, which asked the visitor to do the work of sending.
- **Retuned engagement scoring.** It saturated at 100 within about thirty seconds, which
  made the live record meaningless. A full read-and-engage pass now lands around 70.
- **Router grid** to a 2×2 instead of leaving the fourth option orphaned on its own row.

## 28 Aug 2026 — v0.1

First draft. Hero, router, capability graph, four projects, diagnostic, scope builder,
method, live session record, career timeline. Light and dark themes, telemetry rail with
mobile drawer.

---

# Open items

## Needs Sean

1. **Screenshots or a live link for Road Runner and Kervio.** Every claim on the page is
   currently text. One real screen roughly doubles the credibility of the work section.
   This is the single highest-value thing outstanding.
2. **Two or three named client outcomes**, with permission. "50+ companies, $200M+" is a
   strong number but it isn't a story, and stories are what get quoted back to you.
3. ~~The real hourly rate.~~ Set to $200/hr. Change it in `site.json` any time.
4. **Alpha Surfaces' real numbers** — enquiry volume before and after, segmentation split,
   anything measurable. It's the clearest proof of the front-door thesis and currently
   has no evidence attached.
5. ~~Domain decision.~~ seanstone.com. Still worth deciding whether to set up
   sean@seanstone.com as the contact address rather than sean@cangaroo.ai.
6. **The `engagementOffer` decision**, alongside counsel. See README.

## Next build candidates

- **Real CRM wiring** — point the event stream, diagnostic results and submitted scopes at
  an actual HubSpot or Pipedrive endpoint. Needs an API key and a sandbox to aim at. This is
  the step that turns the site from a demonstration into a working part of the pipeline.
- **Aggregate diagnostic stats**, once there's real traffic to aggregate.
- **Regenerate og.png with the real Instrument Serif face** — currently DejaVu, since the
  build container has no access to the Google font file.
- **A second demo persona set** for a different vertical, if the stone-industry framing
  is too narrow for the clients Sean actually wants.

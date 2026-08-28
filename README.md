# seanstone.com — instrumented portfolio

A personal site that argues by working, not by describing. Four interactive pieces:

| Piece | What it proves |
|---|---|
| **Visitor router** + live event log | The multi-audience front door (the Alpha Surfaces pattern), applied to Sean |
| **Revenue-leak diagnostic** | Domain judgement, made playable and kept by the visitor |
| **Enquiry engine** | The Alpha Surfaces pattern, rebuilt live: pick an audience, watch the form branch, resolve a company against a mock CRM, query stock |
| **Scope builder** | Turns the "outsource me by the hour" offer into a costed artefact they send back |
| **Running verdict** | Stage, score, next action and the alert your sales team would receive — computed from real behaviour, in the language a revenue person uses |

Plus hash-routed case-study pages (`#case/roadrunner`) — shareable URLs, still one file.

Positioning and the reasoning behind all of it: `claude/personal-site-positioning.md`.

---

## Repo shape

```
/
├── build.py              ← run this after any change
├── README.md
├── GO-LIVE.md            ← deployment runbook
├── BUILD-LOG.md          ← what changed, and what's still open
├── src/
│   ├── site.json         ← every word and number on the page  (content)
│   └── template.html     ← markup, CSS, JS                    (code)
├── tools/
│   └── make_og.py        ← regenerates the social share image
│
│   generated — never edit by hand, they are overwritten on every build:
├── index.html            ← the deployable single file, served at /
├── case/<id>/index.html  ← a standalone indexable page per case study
├── og.png                ← LinkedIn / social card
├── robots.txt            ← follows flags.noindex
├── sitemap.xml
├── CNAME                 ← seanstone.com
└── .nojekyll             ← stops GitHub running Jekyll over the files
```

Deployables live at the repo root rather than in `dist/`, so GitHub Pages serves `/`
with no build step of its own. `.build/` holds the Artifact variant and is gitignored.

**The rule: content lives in `src/site.json`, code lives in `src/template.html`.**
If you're editing copy inside template.html, that string belongs in site.json instead.

```bash
python3 build.py
```

No dependencies, no npm, no build toolchain. It reads two files and writes three.

### What's in site.json

| Key | Controls |
|---|---|
| `profile` | Name, email, links |
| `flags` | `engagementOffer`, `showRates`, `noindex` — see below |
| `rate` | Hourly rate and the full-time comparison bands |
| `metrics` | The four numbers under the hero |
| `capabilities` | The capability graph, and which projects evidence each |
| `projects` | Road Runner, Kervio, Alpha Surfaces, Sales Hunters |
| `paths` | Router options and the audience each section is tagged to |
| `demo` | The enquiry engine: personas and their fields, the sample CRM accounts, the sample stock |
| `diagnostic` | Questions, scoring zones, zone commentary, recommended fixes |
| `scope` | Outcomes and hour estimates in the scope builder |
| `timeline` | Career history |

Add a project by appending to `projects` and listing its id under the relevant
capability's `evidence` array — the capability graph and filtering wire themselves up.
Give it a `case` object (`problem`, `built[]`, `changed[]`) and a "Read the case study"
button appears automatically, with its own shareable `#case/<id>` URL.

**The enquiry engine's data is fictional and labelled as such on the page.** The accounts,
trading figures and stock levels are illustrative samples, not Alpha Surfaces' real records.
Keep it that way unless you have written permission to publish the real ones.

---

## The flags

```json
"flags": { "engagementOffer": true, "showRates": true }
```

- **`engagementOffer: false`** removes the scope builder entirely, drops the
  "I need revenue systems built" router path, and rewrites the closing CTA to a
  neutral "have a look, then get in touch." The site becomes a portfolio and
  credentials piece rather than an open offer to sell hours.
- **`showRates: false`** keeps the scope builder but hides all pricing.
- **`noindex: true`** adds a noindex tag and flips `robots.txt` to disallow everything —
  the site stays live and linkable, but stays out of search results.

Both are tested and switch cleanly. This exists because a public, dated, indexed page
soliciting US engagements is exactly the evidence the work-authorisation question turns
on — so the offer can be switched on the day it should be, without rebuilding anything.

---

## Deploying

Full runbook, including the Cloudflare records and the certificate gotchas:
**`GO-LIVE.md`**. Short version: public repo, Pages from `main` / root, five grey-clouded
DNS records, custom domain, wait for the certificate.

**Anywhere else:** it's static files with no dependencies beyond Google Fonts.

---

## Working with Lovable

Lovable will want to rebuild this as React + Tailwind. Fine — but two rules, or it
loses its point:

1. **The data stays one object.** *"All copy and data come from a single `siteData`
   object; components read from it and never hardcode strings."*
2. **The telemetry stays real.** The event log, engagement score, stage and next-best-
   action must stay wired to actual interactions. If it becomes a decorative animation,
   the site is lying and the whole argument collapses.

Starting prompt:

> Rebuild this static page as a React + Tailwind app. Preserve exactly: the visitor
> router that shows/hides sections by audience, the live event log and engagement
> scoring, the 7-question diagnostic with zone scoring, and the scope builder. All
> content comes from a single `siteData` object. Match the existing palette and
> typography tokens.

---

## Wiring it up for real

Everything currently runs in the browser and nothing is sent anywhere — which the page
states honestly. To make it live:

- **Event stream → CRM.** POST the event objects the log already produces to HubSpot or
  Pipedrive. The log lines are shaped like CRM events on purpose.
- **Diagnostic → contact record.** Six zone scores plus the weakest zone as properties.
  A genuinely useful lead-scoring input.
- **Scope → deal.** A submitted scope is a qualified opportunity with the line items
  already chosen. Create the deal, notify, reply within the hour.
- **Aggregate view.** Once real traffic exists, show anonymised roll-ups. Only ever
  publish real numbers.

---

## Behaviour notes

- Light and dark themes defined at token level; respects `prefers-color-scheme` and an
  explicit `data-theme` attribute.
- `prefers-reduced-motion` disables all animation.
- Telemetry rail collapses to a bottom drawer under 1080px.
- No dependencies except Google Fonts. No tracking, no cookies, no storage.

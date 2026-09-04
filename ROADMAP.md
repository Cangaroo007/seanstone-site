# seanstone.com — roadmap

*29 Aug 2026. Ordered by impact per hour, not by ambition.*

---

## Where it stands

Live, indexed, five interactive pieces, four case-study pages, Tier 0 visitor intelligence.
The argument works: the site doesn't claim Sean builds interactive commercial systems, it
*is* one.

**No analytics of any kind are installed.** Not GA4, not Cloudflare, not ContentSquare —
nothing. Every number in the panel is computed in the visitor's browser and discarded when
they close the tab. Sean currently has no idea how many people have visited.

---

## Phase 1 — measurement (do this first, ~1 hour)

Everything below this line is guesswork until there is traffic data. The site is live and
being shared; that data is being lost every day it isn't there.

| Option | Cost | What it gives | Cost to the site |
|---|---|---|---|
| **Cloudflare Web Analytics** | free | Pageviews, referrers, countries, core web vitals. Cookieless, no consent banner needed. | One script tag. Doesn't identify anyone. |
| **GA4** | free | The full acquisition/behaviour model, Search Console integration, audiences. Expected of anyone selling RevOps. | Needs Consent Mode for EU traffic; cookies; the panel's disclosure must change. |
| **Microsoft Clarity** | free | Heatmaps and session replay — you watch people use the diagnostic and scope builder. | Same consent considerations. |
| **ContentSquare** | trial | Zone-based experience analytics, deeper replay. Sean already has a tag: `t.contentsquare.net/uxa/597912112e565.js` | Heavyweight for a one-page site; strongest privacy footprint. |

**Recommendation: Cloudflare Web Analytics + Microsoft Clarity.** Both free, both instant.
Cloudflare answers "is anyone coming"; Clarity answers "where do they stall" — and for this
site the second question is the interesting one, because you want to know whether people
actually finish the diagnostic. Add GA4 as well if the ecosystem matters to you commercially.
Hold ContentSquare until there is enough traffic for zone analysis to say anything.

**Whatever goes in, one line of copy has to change.** The panel says *"nothing leaves your
browser"*. That stops being true the moment a tag loads. New wording, roughly:

> The panel runs entirely in your browser. The site itself uses [X] for analytics, like most
> sites — which is the whole point: you can measure everything and still know nothing about
> who is on your site.

That reframing is better than the original, because it names the problem the site solves.

---

## Phase 2 — identity: from "Pacific time" to "San Francisco" (~3 hours)

The panel currently says *Pacific time* rather than *San Francisco*, and now explains why:
a browser gives a time zone, not a city. Everyone from Vancouver to Tijuana reads the same.

One Cloudflare Worker fixes it and unlocks the rest. Full design in `TIER1-INTELLIGENCE.md`.

1. **Real city and country** — `request.cf.city` is free, needs no vendor, and is accurate.
   *"9:48 AM · San Francisco"* is a much better line than the honest apology it replaces.
2. **The network they're on** — `request.cf.asOrganization`, also free, already distinguishes
   "Deloitte Touche Tohmatsu" from "Comcast Cable".
3. **The company, where it resolves** — expect 30–50% of traffic, not the 60–90% vendors
   claim. Degrade gracefully: an ISP name is honest and still interesting.
4. **Their logo.** If the company resolves, `logo.clearbit.com/<domain>` returns it, free, no
   key. *A visitor seeing their own employer's logo appear in the panel is the single highest
   wow-per-line-of-code on this entire list.*

**Rule that doesn't bend: account level only, never person level.** Resolving an IP to a
company sits outside GDPR and isn't personal information under CPRA. Person-level ID needs a
lawful basis and would cost more in credibility than it returns — "we identify the company,
never the person" is a sentence worth being able to say to a prospect.

---

## Phase 3 — the funky tier

Ranked by impact per hour of build.

**1 · The page writes them a note.** At high engagement, generate a short paragraph naming
their segment, their weakest diagnostic zone and what Sean would do first — in prose, not
bullets. Feels like being spoken to rather than scored. *Pure client-side, ~2 hours.*

**2 · Live weather at their location.** Worker + open-meteo (free, no key): *"It's 14°C and
foggy in San Francisco."* Trivial, but it proves the page is pulling live external data about
*them*, which is exactly the Road Runner claim. *~1 hour on top of Phase 2.*

**3 · "Four other people are reading this right now."** A Cloudflare Durable Object holding a
live count. Real shared state, and the only thing on the site that can't be faked with
client-side JavaScript. *~3 hours.*

**4 · Replay your own session.** A scrubber that plays back what the visitor did on the page —
their own thirty seconds, as a timeline. The site showing you your own behaviour is unsettling
in a way that lands. *~4 hours.*

**5 · "Show me what you'd do for a company like mine."** Pick industry, size and stack; the
diagnostic and scope builder pre-fill with defaults for that shape of business. Turns two
generic tools into one specific answer. *~4 hours, and it needs Sean's judgement encoded as
data — the valuable part.*

**6 · Ask it anything.** A question box answering from Sean's own content via an LLM call
through a Worker. High wow, real cost, real risk of saying something wrong in his voice.
*Last, if at all.*

**7 · Email me this session record.** One button, sends the visitor their own record and
copies Sean. Closes the loop the whole site is arguing for. *~2 hours, needs an email API.*

---

## Phase 4 — the content gaps (unchanged, and still the biggest)

No amount of the above compensates for these:

1. **A screenshot of Road Runner and one of Kervio.** Every claim in the work section is
   currently words. One real screen roughly doubles its credibility. Twenty minutes.
2. **Two or three named client outcomes**, with permission.
3. **Alpha Surfaces' real numbers.** The enquiry engine makes a strong claim with no
   measurement attached.

---

## Suggested order

```
Week 1   Analytics (1h) → screenshots and outcomes (1h) → Cloudflare Worker: city + network (3h)
Week 2   Company + logo resolution (2h) → the personal note (2h)
Later    Live visitor count, session replay, "a company like mine"
```

Phase 1 and Phase 4 together are about two hours and are worth more than everything in
Phase 3 combined. Do them first.

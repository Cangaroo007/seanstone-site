# Rollout sprints — seanstone.com

*Written 4 September 2026. Two-day sprints. Each one ships something live.*

**The honest framing before we start:** the build is ahead of the content. Nothing in Sprint
2 onwards makes the site more persuasive than one screenshot of Road Runner would. So
Sprint 1 is yours, it's about ninety minutes of your time, and it's worth more than the rest
of this document combined. Everything after it is me.

---

## ✅ Sprint 0 — shipped today

Live and verified from outside:

- Region-aware consent gate — banner in Europe/UK only, GPC honoured everywhere
- `/privacy/` generated from the tag config, so it can't drift out of date
- Cloudflare Web Analytics, GA4 (`G-60G7VKJ4ZN`), ContentSquare all firing
- Capability re-ranking, work accordion, Tier 0 visitor intelligence
- Four case-study pages, pre-rendered, indexable

---

## Sprint 1 — Fri 4 – Sat 5 Sep · **make it true** · mostly done

✅ Road Runner screenshots (4 of 5) · ✅ Kervio screenshots (3) · ✅ verified production
metrics in the case studies. Outstanding: `roadrunner-03-form.png`, named client outcomes,
Search Console, LinkedIn Post Inspector.

The site currently asserts things it doesn't evidence. This closes that.

| # | Task | Time |
|---|---|---|
| 1 | **Screenshot Road Runner** — the dashboard, a report, a client landing page. Any two. | 10 min |
| 2 | **Screenshot Kervio** — the quote screen and one manufacturing view | 10 min |
| 3 | **Two or three client outcomes**, named, with permission. "We took X from A to B in C months." | 30 min |
| 4 | **Alpha Surfaces numbers** — enquiry volume before/after, or the segmentation split. Anything measurable. | 20 min |
| 5 | **Search Console** — add seanstone.com, verify by TXT in Cloudflare, submit `sitemap.xml` | 10 min |
| 6 | **LinkedIn Post Inspector** — run the URL through to warm the share card | 2 min |
| 7 | **ContentSquare** — confirm text-input masking is on in project settings | 5 min |

**Send me 1–4 and I ship them the same day.** Screenshots go into the work accordion and the
case pages; outcomes become a proof strip; the Alpha Surfaces numbers go under the enquiry
engine, which currently makes a strong claim with nothing behind it.

**Done when:** the work section contains at least one real image and one named outcome.

---

## Sprint 2 — Sun 6 – Mon 7 Sep · **the identity Worker** · ~3h, mine + 20 min yours

Turns *"Pacific time"* into *"San Francisco"* and puts visitors' company logos in the panel.

**Yours:**
```bash
cd ~/Downloads/ss-deploy/repo/worker
npm install -g wrangler && wrangler login && wrangler deploy
curl -s https://id.seanstone.com | python3 -m json.tool
```
Then optionally `wrangler secret put IPINFO_TOKEN` with a free ipinfo.io key for company
resolution. Send me the JSON output.

**Mine:** switch `identity.endpoint` on, move the consent region check from the time-zone
heuristic to the Worker's real country code (more accurate and legally cleaner), verify the
degradation path still holds if the Worker is down.

**Done when:** the panel names your city, and a visitor from a corporate network sees their
employer's logo.

---

## Sprint 3 — Tue 8 – Wed 9 Sep · **the funky tier** · ~5h, mine · **1 and 2 shipped in v1.4**

Ranked by impact per hour. We can cut from the bottom.

1. ✅ **The page writes them a note.** At high engagement it produces a short paragraph in
   prose — their segment, their weakest zone, what you'd do first. Being spoken to rather
   than scored. *~2h*
2. ✅ **Live weather at their real location.** "It's 14°C and foggy in San Francisco." Trivial,
   but it proves the page is pulling live external data *about them*. *~1h*
3. **"Four other people are reading this right now."** A Durable Object holding a live count.
   The only thing on the site that can't be faked client-side. *~3h*

**Done when:** a visitor who finishes the diagnostic gets a paragraph written to them, not a
score card.

---

## Sprint 4 — Thu 10 – Fri 11 Sep · **close the loop** · ~4h, mine + your API key

This is the sprint that stops the site being a demonstration and makes it part of your
pipeline. It's also the strongest sales asset: *"this is running on my own site, here's the
deal it created."*

- Event stream → HubSpot or Pipedrive (the log lines are already shaped as CRM events)
- Diagnostic results → contact properties, six zone scores plus the weakest
- Submitted scope → a deal with the line items already chosen, and an alert to you
- "Email me this session record" button

**Yours:** a HubSpot or Pipedrive sandbox and a private app token.

**Done when:** you complete the diagnostic on your own site and a real record appears in your
CRM within seconds.

---

## Sprint 5 — following week · **depth** · ~5h, mine

- A second enquiry-engine persona set for a non-stone vertical, if stone framing is too
  narrow for the clients you actually want
- Case-study numbers wired in once Sprint 1 delivers them
- Regenerate `og.png` with the real Instrument Serif face
- Aggregate diagnostic stats, once there's traffic to aggregate honestly

---

## Standing decisions to revisit

- **`engagementOffer`** — currently `true`, so the site is an open offer to sell hours. One
  flag flips it to portfolio-only. Worth a conversation with Alcorn.
- **Tranche 2 privacy reform** — Australian exposure draft, consultation closed 18 Sep 2026.
  If the "fair and reasonable" test passes, consent stops being the fix and data minimisation
  becomes it. Re-read the privacy page when it lands.
- **ContentSquare** — keep it while it's earning its place. If after a month of traffic the
  replays aren't telling you anything the funnel doesn't, drop it and remove a dependency.

---

## How each sprint ships

```bash
cd ~/Downloads/ss-deploy/repo && git pull --quiet && \
unzip -o -q ~/Downloads/seanstonev<NN>.zip -d /tmp/v<NN> && cp -R /tmp/v<NN>/*/. . && \
git add -A && git commit -m "<sprint>" && git push origin HEAD:main
```

About a minute to go live. Everything is verified from outside before I call it done.

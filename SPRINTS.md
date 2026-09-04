# Where seanstone.com stands — 4 September 2026

*Rewritten at the end of the build day. The previous version is in git history.*

**The honest headline: the build is now a long way ahead of both the content and the
traffic.** Everything below the line marked "Yours" is worth more than everything above it,
and none of it is code.

---

## Shipped and live

| | |
|---|---|
| **The page** | Router, capability graph, four case studies with real screenshots, revenue-leak diagnostic, scope builder, live session panel, career history |
| **Tier 0–1 intelligence** | City, network and company resolved server-side via Cloudflare + IPLocate; live weather at the visitor's real location |
| **The note** | At genuine engagement the page writes four or five paragraphs of prose to the reader, assembled from what they actually did, with a receipt listing every fact used |
| **Three enquiry hooks** | The self-completing sentence under the hero; "what number do you want moved" above the diagnostic; the ask box before the CTA |
| **The tier ladder** | Front door → Road Runner → built to requirement, so nobody mistakes the instrumentation for the offer |
| **The compose panel** | Every enquiry pre-written and editable, posted to a real endpoint, with copy-to-clipboard as the floor |
| **The answer engine** | Eleven written answers, then Claude assembling from `kb.md` for anything else — badged so the reader knows which is which |
| **The record** | D1 storing every enquiry and every hot session; `/admin` behind a password |
| **The alert** | Score crosses 80 → the session is emailed to Sean, and the page tells the visitor it happened |
| **Compliance** | Region-aware consent gate, GPC honoured, `/privacy/` generated from config so it cannot drift |

---

## Yours — and this is the whole list that matters

Ranked. The first two are worth more than the rest of this document.

1. **Two or three named client outcomes, with permission.** *"We took X from A to B in C
   months."* The site now has an answer engine, an alert system and a database, and still not
   one named customer. Every number on it is about volume, not about a person who was helped.
   **~30 minutes. Highest-value thing outstanding by a distance.**
2. **The Alpha Surfaces numbers** — enquiry volume before and after, or the segmentation split.
   The enquiry engine makes a strong claim with nothing behind it. **~20 minutes.**
3. **Put the URL to work.** LinkedIn headline and featured section, email signature, outreach.
   The instrumentation only pays off with traffic, and there is currently almost none. The
   alert has never fired for a stranger.
4. **Google Search Console** — add seanstone.com, verify by TXT in Cloudflare, submit
   `sitemap.xml`. **~10 minutes.**
5. **Rotate the Cloudflare API token.** It was pasted into a chat transcript. My Profile → API
   Tokens → Roll, then update `~/.zshrc`. **~5 minutes, still outstanding.**
6. **`roadrunner-03-form.png`** — the one screenshot still missing from the set.
7. **LinkedIn Post Inspector** on the URL, to warm the share card. **2 minutes.**
8. **ContentSquare** — confirm text-input masking is on in project settings. **5 minutes.**

---

## Mine, when you want it

Ranked by what I think it is actually worth, not by how interesting it is to build.

1. **Read the first real sessions and tune the thresholds.** 80 is a guess. Once a dozen
   strangers have been through, the score curve will say whether it is the right number, and
   whether `nextAction()` is saying useful things about real people. *~2h, needs traffic first.*
2. **Grow `kb.md` as the work grows**, and tighten one thing: when it declines an invented
   client it currently recites the full list of named engagements, which reads like it is
   reading off a card. *~1h.*
3. **"Four other people are reading this right now."** A Durable Object holding a live count —
   the only thing on the site that cannot be faked client-side. Unlocked by the Workers Paid
   upgrade. *~3h.*
4. **Company visit log.** The Worker already resolves company for every visitor; logging those
   to D1 gives you *"these fourteen companies looked at your site this week"* without anybody
   filling anything in. This is the Warmly product at $0 rather than $10,000/year, and it is
   the strongest thing you could put in front of a prospect. *~3h.*
5. **CRM wiring** — push contacts and deals into HubSpot or Pipedrive. Genuinely lower priority
   than it was: `/admin` and the email alerts already do the job at your volume. Worth it when
   there is enough flow to justify a pipeline. *~4h, needs a sandbox and a token.*
6. **A second enquiry-engine persona set** for a non-stone vertical, if the stone framing is
   too narrow for the clients you actually want. *~3h.*
7. **Regenerate `og.png`** with the real Instrument Serif face. Cosmetic. *~30m.*

---

## Standing decisions to revisit

- **`engagementOffer`** is `true`, so the site is an open offer to sell hours. One flag turns it
  into a portfolio. Worth a conversation with Alcorn.
- **DMARC.** Back at `p=none` deliberately. Read a few weeks of the `rua` reports, confirm every
  legitimate sender aligns, then step to `p=quarantine` and eventually `p=reject`. Do not jump.
- **Tranche 2 privacy reform** — Australian exposure draft, consultation closed 18 Sep 2026. If
  the "fair and reasonable" test passes, data minimisation replaces consent as the fix, and the
  privacy page needs re-reading.
- **ContentSquare** — keep it while it earns its place. If after a month the replays are not
  telling you anything the funnel does not, drop it and remove a dependency.
- **Anthropic spend** — the rate limit bounds it, but check the console after the first week of
  real traffic to see what a question actually costs.

---

## How anything ships

```bash
cd ~/Downloads/ss-deploy/repo && git pull --quiet && \
unzip -o -q ~/Downloads/seanstonev<NN>.zip -d /tmp/v<NN> && cp -R /tmp/v<NN>/*/. . && \
git add -A && git commit -m "<what>" && git push origin HEAD:main
```

Worker changes additionally need `cd worker && cfw deploy`.

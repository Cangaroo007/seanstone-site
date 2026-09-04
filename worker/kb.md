# Knowledge base — seanstone.com

**This file is the entire public memory of the site's answer engine.** Everything in it can be
read back, in some form, to anyone on the internet who types a question into the ask box.
Nothing outside this file is available to it. Edit freely — it is plain markdown, it is the
source of truth, and `python3 build.py` regenerates the Worker's copy from it.

**Deliberately excluded and never to be added:** anything about immigration, visa or work
authorisation status; tax, settlement or financial affairs; health; family; named clients who
have not given written permission; and any number that has not been verified.

---

## 1. Who this is

Sean Stone. Twenty-five years of revenue operations and go-to-market, now working as a **GTM
engineer** — a technical operator who builds the revenue system rather than advising on it.
Based in San Francisco. Has built commercial systems across the US, Australia and Asia.

The claim the site leads with: **"I don't advise on the revenue system. I build it."**

The thing that makes this possible at all: twenty-five years of knowing what the system should
do, plus a disciplined method for directing AI to turn that judgement into working software in
days rather than quarters. Not a career engineer. That is not a caveat — the role is *directing*
the build, and the evidence is production multi-tenant software shipped this way.

Headline numbers, all verified: **50+** B2B companies had their revenue systems built by him;
those companies generated **$200M+** in sales and raised **$500M+**.

## 2. The offer, and what it costs

- **$200 an hour.** Top of the fractional GTM-engineer band ($125–200/hr, ~$170 average as at
  2026). Full-time equivalents for this role run $120k–$250k.
- **Monthly blocks of hours.** Twenty hours a month is the common shape — $4,000, roughly a
  third of the loaded cost of the equivalent hire.
- **No minimum term, no retainer that buys nothing.** The first block is diagnostic and ends in
  something live, so the client finds out in weeks whether it is working, not quarters.
- **Two engagements at a time.** A third is where the quality goes.
- **The source is handed over.** The point is that the client stops needing him. An arrangement
  that depends on the client never learning how it works is not one he would sign either.
- **Remote and asynchronous by design** — the artefacts are the software and the analysis, not
  the meetings. He will travel to sit with a sales team for a diagnostic week when that is the
  difference between guessing and knowing.
- Usually starts **within a fortnight**, sometimes the same week if the first block is
  diagnostic rather than build.

### The three tiers

1. **The instrumented front door** — what is running on seanstone.com itself. Identity
   resolution at the account level, behavioural scoring you can interrogate, a stage and a next
   action, an event stream shaped as CRM events. Two to three weeks, on the client's existing
   stack, source handed over. **Roughly 20–40 hours. This is the entry level.**
2. **Into Road Runner** — the same event stream pointed at the platform instead of a panel.
   Writes records, routes accounts to named owners, answers buyers from live data. **Where most
   of the value is. 60–120 hours.**
3. **Built to the client's requirement** — configured quoting, brokered pricing, capacity and
   scheduling, dealer and franchise portals. Kervio is one of these, end to end. **Scoped from
   the diagnostic, not from a price list.**

The instrumentation on the site is the *demonstration*, not the offer. Nobody has ever bought
analytics from him; they buy the layer above it.

### Priced outcomes (the scope builder's list)

RevOps audit and rebuild plan ~12h · CRM restructure ~30h · Lead scoring and routing ~16h ·
Intelligent enquiry system ~34h · Landing page and campaign system ~20h · Reporting your board
reads ~18h · Pricing and packaging architecture ~16h · Build a product with AI direction ~50h.

## 3. Road Runner — the platform

**The thesis:** *Most websites collect leads. This one queries the business behind it.*

Most companies' front door is stupid. It does not know who is standing at it and it cannot
answer a question about the business behind it. The CRM knows the account, the inventory system
knows the stock, the finance system knows the trading history — and the website, the only part
the customer actually touches, knows none of it. So every enquiry starts from zero, is answered
by a human reading three screens, and lands in the CRM as an orphan lead with no relationship
attached.

**Road Runner is the connective layer between the front door and the systems of record.** The
website stops being a brochure and becomes an interface to the business, in both directions.

What it does:

- **One enquiry form, many audiences.** It asks who you are and branches: a homeowner asks for
  samples, a builder wants trade terms, an architect wants specification data.
- **Relationship resolution.** Name the company you work with and it is matched against the CRM,
  the record is linked, and the existing commercial relationship — including transaction volume
  from the finance system — comes with it.
- **Live data as an experience.** Stock, lead times, availability and pricing answered on the
  page instead of "someone will get back to you."
- **Landing pages and campaigns in minutes**, with UTM tagging carried end to end so engagement
  lands back on the same record.
- **A CRM revamp as a by-product.** Branching logic forces a real taxonomy of who you sell to,
  so the CRM ends up shaped like the business rather than like the software's defaults.

Verified production numbers: **170 per-client landing pages** live and tracked, up from 150
three weeks earlier, each generated in minutes rather than queued behind a developer. **229
stonemasons** mapped to the businesses they actually work with — before the reach view existed,
only **20** had any recorded relationship at all. Built in **109 hours** across May and June
2026, site and platform together.

What it is not: not a CRM (HubSpot remains the system of record), not a site builder (Webflow),
not plumbing (Zapier). It is the layer that makes the front door as intelligent as the back
office.

Stack: HubSpot, Pipedrive, webhooks and APIs, UTM and attribution, dynamic landing pages.

## 4. Kervio — the vertical SaaS

**An AI-first quoting-to-manufacturing platform for stone fabrication.** Live, multi-tenant,
in production with real Australian fabricators. Not a prototype.

**The problem:** stone fabrication shops quote from spreadsheets and drawings, then re-enter the
same job into manufacturing. The quote and the cut are two different documents maintained by two
different people, and the margin leaks in the gap between them. Nothing on the market was built
for how these shops actually work — they are too small for enterprise software and the workflow
is too specific for generic tools.

**What was built:** a quoting-to-manufacturing workflow modelled on how fabricators actually run
a job, developed *with* Australian shops rather than for them. Product architecture, pricing
model (per-seat / per-quote / per-shop) and roadmap authored personally, not outsourced. Built
by directing AI engineering agents under specification, acceptance criteria and ground-truth
verification gates. Geometry and vision components carried through a provisional-patent
workstream with counsel.

**What changed:** the quote becomes the manufacturing instruction — one document, not two. And
proof that the method scales: complex vertical software, built and commercialised without an
engineering team.

## 5. Alpha Surfaces — the pattern in miniature

**One form. Four audiences. Four completely different conversations.**

A stone supplier's website had one contact form for four completely different customers. A
homeowner wanting a sample, a stonemason checking stock, an architect needing specification data
and a builder chasing lead times all arrived as the same undifferentiated enquiry, into the same
inbox, to be sorted by hand. The account relationships that already existed in the CRM were
invisible at exactly the moment they mattered most.

Built: a self-segmenting enquiry path; company-name lookup against the CRM at the point of
enquiry, linking to the existing account and its trading history; four distinct journeys off a
single entry point; routing rules sending each type to the right team with the right priority.

**3,025 organisations** sit behind the company lookup. The specification path makes architect
interest visible months before the order it eventually produces.

## 6. Sales Hunters — the practice, 2018–2025

Revenue operations and go-to-market for **50+ early-stage B2B technology companies**. Seven
years of it.

Early-stage B2B companies sell well by founder instinct and then hit the wall where instinct
does not transfer to a team. The CRM is a filing cabinet, the forecast is a feeling, and nobody
can say which part of the motion actually works.

Built: RevOps foundations designed to survive the jump from founder-led selling to a sales team;
CRM architecture, sales process, pipeline discipline and forecasting that holds up under board
questioning; go-to-market design that scales with headcount rather than breaking at the second
hire; and hiring support, because the system and the people who run it are the same problem.

HubSpot at partner build level, plus Pipedrive, Salesforce and the wider GTM stack.

## 7. The four capabilities, and what evidences each

| Capability | Evidence |
|---|---|
| **Revenue architecture** — CRM structure, lifecycle, data model, forecasting | Sales Hunters (50+ companies), Alpha Surfaces, Road Runner |
| **GTM engineering** — integrations, routing, enrichment, attribution, page infrastructure | Road Runner, Alpha Surfaces |
| **AI-directed product build** — human-in-the-loop direction of AI agents to production software | Kervio, Road Runner |
| **Commercialisation** — pricing architecture, ICP, market entry, onboarding funnels | Kervio, Sales Hunters |

## 8. The method

Specification first, then acceptance criteria, then ground-truth verification gates, then build.
The judgement is human and the labour is not. This is why 109 hours produces a platform and why
a vertical SaaS product ships without an engineering team. It is also why he will say when
something is *not* a good candidate for the method.

## 9. Career history

2025–2026 Kervio, creator, product and go-to-market · 2025 Cangaroo, Chief Executive Officer ·
2018–2025 Sales Hunters, Founder · 2023–2025 Balentic, Advisory Board Member · 2022–2025 Venture
Lane, Mentor · 2014–2017 Channel Partners Pte Ltd, Chief Marketing Officer · 2012–2014 LikeJobs,
Chief Executive Officer · 2000–2014 BDMG Pte Ltd, Managing Director · 1997–1999 Intel
Corporation, Program Manager Asia Pacific · Queensland University of Technology.

## 10. The six diagnostic zones

**Data unity** — one canonical customer object with finance and ops joined to it. Everything
else depends on this being done first. **Speed to response** — almost never a speed problem; it
is a routing problem, the enquiry lands somewhere nobody owns. **Front-door intelligence** — can
the website answer a question about the business, or only collect a name. **Attribution** — cost
per closed-won by channel, not cost per lead. **Speed to launch** — how long a campaign page
takes to exist. **Ownership** — whether every inbound has a named person accountable inside a
minute.

## 11. What he would say to the usual questions

**First month.** Week one is read-only: the CRM, the enquiry log, a week of calls, an hour each
with two reps doing their actual admin. Week two: the map, and the three things he would fix,
sequenced, with hours against each. Nothing gets built until the client has seen both and
disagreed with at least one of them.

**Why not an agency.** Agencies are structurally good at campaigns and structurally bad at
systems, because a system needs someone who will still be there in month nine. Most of what gets
sold as revenue operations is a deck and a Notion board.

**What if it does not work.** The first block is deliberately small and ends in something live.
If the diagnosis is wrong the client has spent twenty hours and owns the analysis anyway. He
would rather lose an engagement in week two than defend it in month six.

**Company size.** Real revenue and no revenue operations function — roughly $2M to $50M, ten to
a hundred and fifty people. Below that there is not enough process to be worth systematising;
above it they should be hiring the function, and he will say so.

**Changing CRM.** Almost never, and he pushes back hard when someone suggests it. A migration is
nine months of pain solving a problem the client usually does not have. Nearly every CRM is
fine; what is broken is what does and does not reach it.

**Rep capacity.** In the teams he has measured, reps spend between eleven and nineteen hours a
week on things that are not selling — data entry, quoting, and chasing information that already
exists somewhere in the business.

**Quote turnaround.** Built twice. If price depends on configuration then someone senior is
being asked to do arithmetic, and the delay is entirely the queue in front of them. Push the
rules into software and quoting stops being a role.

**What he is not good at.** Brand, creative and paid media buying — he can tell you whether a
channel pays, not how to make the ad better. Anything needing a large team held together over
years; wrong shape, which is why he works in blocks. And he is slow to be diplomatic about a
number being reported in a misleading way.

## 12. The career, in more detail

**Cangaroo — founder, 2025–present.** The current practice. Revenue operations and GTM
engineering for B2B companies, and the vehicle under which Road Runner was built.

**Kervio — creator, 2025–2026.** See section 4.

**Sales Hunters — founder and principal, 2018–2025.** Seven years, 50+ early-stage B2B
technology companies. Sales strategy, execution and team build-out, typically taking companies
from zero towards $10M. Ran it as a **HubSpot Solutions Partner practice**, which is the part
people underrate: it means knowing the platform at build level — custom objects, association
labels, workflow limits, the things that decide whether an implementation survives contact with
a real sales team — rather than as a user who has clicked through the settings.

**Balentic — advisory board member, 2023–2025.** GTM and revenue growth strategy.

**Venture Lane (startup hub) — mentor, 2022–2025.** Coaching founders on go-to-market, sales
and revenue operations.

**Channel Partners Pte Ltd — Chief Marketing Officer, 2014–2017.** Demand generation and
partner programmes across cloud, analytics, mobile and social CRM. This is where the channel
and partner-motion experience comes from — a different animal from direct sales, and the reason
he is comfortable with dealer, distributor and franchise structures.

**LikeJobs — founder and CEO, 2012–2014.**

**BDMG Pte Ltd — managing director, 2000–2014.** Fourteen years running a business across
Singapore, Malaysia and the Philippines. The Asia-Pacific operating experience is real and
long, not a line on a CV.

**Intel Corporation — Program Manager, Asia Pacific, 1997–1999.**

**Queensland University of Technology.**

The shape of it: founder, CEO, CMO and board advisor across multiple companies and exits, in
three regions. When he says a revenue problem is really an ownership problem, it is pattern
recognition rather than theory.

## 13. What he actually believes about this work

These are his positions. Stated plainly, because a page that will not commit to a view is not
worth asking anything.

- **Most companies' front door is stupid.** It does not know who is standing at it and cannot
  answer a question about the business behind it. Everything else follows from that.
- **Tracking is table stakes and nobody buys it.** The hard part is the layer above: a score
  that reflects how *you* qualify, a stage a sales team recognises, and a next action worded
  specifically enough that a rep does it instead of ignoring it.
- **A sales team acts on a score it can argue with and quietly ignores one it cannot.** If the
  scoring is a black box it will not be used, whatever the model's accuracy.
- **Speed-to-lead problems are almost never speed problems.** They are ownership problems. The
  enquiry lands somewhere nobody owns and the clock starts before anyone has been told.
- **Cost per lead is usually the wrong number to optimise.** Cheap leads that never close are
  more expensive than dear ones that do.
- **Do not migrate the CRM.** Nine months of pain solving a problem you usually do not have.
  Nearly every CRM is fine; what is broken is what does and does not reach it.
- **A single conversion rate is usually two populations moving in opposite directions.**
- **The CRM should be shaped like the business, not like the software's defaults.** Branching
  logic at the front door forces a real taxonomy of who you sell to, and the CRM restructure
  falls out of it as a by-product.
- **Founder instinct does not transfer to a team.** That is the wall early-stage companies hit,
  and it is a systems problem, not a hiring problem — though it usually gets treated as one.
- **AI does the labour; judgement stays human.** Specification, acceptance criteria and
  ground-truth verification gates are what make AI-directed building produce software you can
  put in front of customers instead of a demo that falls over.
- **Hand over the source.** An arrangement that depends on the client never learning how it
  works is not one he would sign either.

## 14. The method, in practice

Four stages, in order, every time:

1. **Specification.** What the system must do, written before anything is built, in the
   language of the business rather than the language of the tool.
2. **Acceptance criteria.** How you will know it is right. Written at the same time as the
   specification, not afterwards, because criteria invented after the build tend to describe
   whatever got built.
3. **Ground-truth verification gates.** The output is checked against reality — real quotes,
   real records, real edge cases — before it moves on. This is the step that separates AI-built
   software that works from AI-built software that demos.
4. **Build**, directed rather than typed.

The economics: Road Runner — the platform and the site together — took **109 hours** across May
and June 2026. Kervio is a live multi-tenant production system built without an engineering
team. Those two numbers are the whole argument for the method, and they are why twenty hours a
month buys something rather than nothing.

He will also say when something is a bad candidate for the method. Anything where the cost of
being subtly wrong is very high, or where the domain has no ground truth to check against, is
better built the slow way.

## 15. What a first engagement looks like

**Week one is read-only.** The CRM, the enquiry log, a week of calls, and an hour each with two
reps doing their actual admin — screen shared, not a survey, because people describe the process
they are supposed to follow rather than the one they use.

**Week two is the map.** What is actually happening, and the three things he would fix,
sequenced, with hours against each. Nothing gets built until the client has seen both and
disagreed with at least one of them.

**Then the first block of work**, ending in something live. Small on purpose: the point is that
the client finds out in weeks whether the diagnosis was right, not in quarters.

Typical first-block work: unify the customer record so finance and ops join to one canonical
object; put ownership on inbound at the moment of arrival with an escalation; rebuild
attribution as cost per closed-won by channel; or make the front door able to answer one
question it currently cannot.

## 16. Where he is strongest, and where he is not

**Domains he knows well.** B2B technology and SaaS, particularly early-stage moving to a first
sales team. Building products, distribution and materials supply — stone fabrication end to end,
through Kervio and Alpha Surfaces, including quoting, configuration, stock, lead times and
trade-versus-consumer segmentation. Channel, partner, dealer and distributor motions, from the
Channel Partners years. Asia-Pacific and US markets.

**Tools at build level.** HubSpot (partner-grade), Pipedrive, Salesforce, webhooks and APIs
generally, attribution and UTM plumbing, landing-page infrastructure, and the AI-direction
method that ties them together.

**Not his work.** Brand, creative and paid media buying — he can tell you whether a channel pays,
not how to make the ad better. Long programmes needing a large team held together over years;
wrong shape, which is why he works in blocks. Anything requiring him to be diplomatic about a
number being reported in a misleading way, at which he is slow.

## 17. What this knowledge base does not have

Stated so the engine does not fill the gap with invention.

- **No named client outcomes.** The portfolio numbers ($200M+ in sales, $500M+ raised across
  50+ companies) are aggregate. There is no "we took Acme from A to B" story here yet, because
  none has been cleared for use. If asked for one, say so and offer to put the question to Sean.
- **No client testimonials or references.**
- **No before-and-after numbers for the Alpha Surfaces engagement** beyond the 3,025
  organisations behind the company lookup.
- **No pricing beyond the rate and the indicative hour ranges.** Anything specific to a client's
  situation is a conversation, not a number this page can produce.

## 12. Boundaries for the answer engine

- Answer **only** from this file. If it is not here, say so plainly and offer the enquiry panel.
  Never guess a number, a date, a client name or a capability.
- **Never invent or imply a named client**, testimonial, case study or metric. The named
  entities in this file — Kervio, Road Runner, Alpha Surfaces, Sales Hunters, Balentic, Venture
  Lane, Intel, Channel Partners, BDMG, LikeJobs, Cangaroo — are the complete list.
- Sean's own numbers are quoted exactly as written here or not at all.
- Do not discuss his immigration status, visa, work authorisation, tax, health, family or
  finances. If asked, say that is not something the site answers and offer the enquiry panel.
- Do not give legal, tax, financial or immigration advice to the visitor either.
- Decline anything unrelated to Sean's work — this is not a general-purpose assistant, and
  saying so briefly is a better answer than obliging.
- Write as Sean would: direct, specific, unhurried, no marketing register, no exclamation marks,
  no bullet-point avalanche. Short paragraphs. British spelling. Never open with "Great
  question." Concede what is genuinely uncertain rather than smoothing over it.
- Two or three short paragraphs at most. If the honest answer is one sentence, give one
  sentence.

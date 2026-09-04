#!/usr/bin/env python3
"""
Build seanstone.com.

    python3 build.py

Reads   src/template.html   (markup, CSS, JS — the code)
        src/site.json       (every word and number on the page — the content)

Writes  index.html          the deployable, self-contained single file (repo root,
                            so GitHub Pages can serve "/" with no build step)
        CNAME, .nojekyll    Pages configuration
        robots.txt, sitemap.xml  indexing, driven by flags.noindex
        case/<id>/index.html  a standalone indexable page per case study
        .build/artifact.html  the same page with the wrapper stripped, for
                            publishing as an Artifact (not deployed)

Editing rule: content changes go in site.json, code changes go in
template.html. If you find yourself editing copy inside template.html,
the string belongs in site.json instead.
"""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT           # deployable files sit at the repo root, so GitHub Pages
BUILD = ROOT / ".build"  # serves from "/" with no build step of its own
TOKEN = "__SITE_DATA__"
ROBOTS = "__ROBOTS__"
ANALYTICS = "<!--ANALYTICS-->"  # a comment, so it cannot collide with window.__ANALYTICS__ in the page JS


def esc(s):
    """Mirror of the esc() in template.html, so pre-rendered markup matches
    exactly what the JavaScript produces on load."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def render_case(project, projects):
    """Server-side twin of openCase() in template.html.

    The case-study body is otherwise injected by JavaScript, which means any
    crawler or link-preview scraper that does not execute JS sees the homepage
    content on a /case/<id>/ URL. Pre-rendering it here puts the real copy in
    the static HTML; the JS re-renders the identical markup on load and takes
    over the interactions. If you change the markup in openCase(), change it
    here too.
    """
    c = project["case"]
    others = [p for p in projects if p["id"] != project["id"] and p.get("case")]
    built = "".join(f"<li>{esc(x)}</li>" for x in c["built"])
    changed = "".join(f"<li>{esc(x)}</li>" for x in c["changed"])
    stack = "".join(f'<span class="pill">{esc(s)}</span>' for s in project["stack"])
    imgs = project.get("images") or []
    shots = ""
    if imgs:
        figs = "".join(
            f'<figure><img src="/{esc(im["src"])}" alt="{esc(im["alt"])}" loading="lazy" decoding="async">'
            f'<figcaption><span class="src">{esc(project["name"])} \u00b7 {i+1:02d}</span> '
            f'{esc(im["caption"])}</figcaption></figure>'
            for i, im in enumerate(imgs))
        shots = ('<div class="case-block"><h3>The screens</h3>'
                 f'<div class="shots{" multi" if len(imgs) > 1 else ""}">{figs}</div></div>')
    nav = "".join(
        f'<button class="caselink" type="button" data-case="{o["id"]}">{esc(o["name"])} \u2192</button>'
        for o in others)
    return (
        '<a class="backlink" href="/">\u2190 Back to everything else</a>'
        f'<div class="case-hero"><div class="label" style="margin-top:var(--s5)">'
        f'{esc(project["kicker"])} \u00b7 {esc(project["year"])}</div>'
        f'<h2 class="display">{esc(project["name"])}</h2>'
        f'<p class="lede">{esc(project["thesis"])}</p></div>'
        '<div class="case-body">'
        f'<div class="case-block"><h3>The problem</h3><p>{esc(c["problem"])}</p></div>'
        f'<div class="case-block"><h3>What was built</h3><ul class="klist">{built}</ul></div>'
        f'<div class="case-block"><h3>What changed</h3><ul class="klist">{changed}</ul></div>'
        + shots +
        f'<div class="case-block"><h3>Built with</h3><div class="stack">{stack}</div></div>'
        '</div>'
        f'<div class="casenav">{nav}'
        '<button class="caselink" type="button" id="case-back2">All work</button></div>'
    )


def render_privacy(data, html):
    """Generate /privacy/ from the same config that drives the tags, so the page
    can never claim something the site does not actually do. Reuses the built
    page's <head> for fonts and CSS."""
    a = data.get("analytics", {})
    ident = data.get("identity", {}).get("endpoint", "")
    p = data.get("privacy", {})
    prof = data.get("profile", {})
    head = html[html.index("<title>"):html.index("</head>")]
    head = head.replace(
        "<title>Sean Stone — Revenue Systems</title>",
        "<title>Privacy — Sean Stone</title>", 1)
    head = head.replace('<meta name="robots" content="index, follow">',
                        '<meta name="robots" content="noindex, follow">')

    rows = []
    rows.append((
        "The panel on the site",
        "Your time zone, device and browser, how far you scroll, whether you leave and come back, "
        "and whether you copy something. A small note is kept in your own browser so the page "
        "recognises you on a return visit.",
        "Stays in your browser. Never sent to a server, never stored by me, gone when you clear site data."))
    rows.append((
        "The enquiry hooks",
        "The sentence you complete, the number you pick and anything you type into the ask box.",
        "Composed entirely in your browser as you use the page. Nothing is transmitted at this "
        "stage \u2014 it becomes an enquiry only if you open the panel and press send, and you "
        "can read and edit every word first."))
    if data.get("alert", {}).get("endpoint"):
        rows.append((
            "The engagement alert",
            "If your engagement score passes 80 \u2014 which takes sustained, deliberate use of "
            "the tools on this page \u2014 the contents of the live panel are emailed to Sean and "
            "stored: the resolved company, city and network, your score, what you read, the "
            "diagnostic result and any scope you built. No name, no email address, nothing "
            "you did not do on this page.",
            "The page tells you in the log at the moment this happens, rather than after the "
            "fact in a policy. This is the one thing on the site that reaches Sean without you "
            "choosing to contact him, which is why it announces itself."))
        rows.append((
            "What is kept, and where",
            "Enquiries you send, and the sessions described above.",
            "A Cloudflare D1 database on Sean's own account, readable only by him behind a "
            "password. No third-party CRM, no data broker, no advertising platform. Ask at the "
            "address below and it will be deleted."))
    if data.get("ask", {}).get("endpoint"):
        rows.append((
            "Asking the page a question",
            "The question you type, and nothing else \u2014 no identifier, no location, no session "
            "history travels with it.",
            "Sent to a Cloudflare Worker on this domain, which passes the question and Sean's "
            "own knowledge base to Anthropic's Claude API to compose an answer. Anthropic does "
            "not train on it. Nothing is stored here, and the written answers are served "
            "without leaving your browser at all."))
    if data.get("enquiry", {}).get("endpoint"):
        rows.append((
            "Sending an enquiry",
            "Only what you choose to send: the message shown in the panel, which you can edit "
            "or delete before sending, and your email address if you fill that field in.",
            "Posted to a Cloudflare Worker on this domain, which forwards it to my inbox and "
            "keeps no copy. Nothing is sent until you press the button, the email field is "
            "optional, and there is no third-party form service involved."))
    if a.get("cloudflareToken"):
        rows.append((
            "Cloudflare Web Analytics",
            "Page views, referrer, country, and page performance.",
            "Cookieless. Sets nothing on your device and does not fingerprint you, which is why it "
            "is not covered by the cookie choice."))
    if a.get("ga4"):
        rows.append((
            "Google Analytics 4",
            "Standard web analytics — pages viewed, how you arrived, approximate location, device.",
            "Sets cookies. Processed by Google in the United States. In Europe and the UK it does not "
            "load at all unless you accept."))
    if a.get("contentsquare"):
        rows.append((
            "ContentSquare",
            "How the page is used — clicks, scrolling and interaction with the tools on it. Text you "
            "type is masked.",
            "Sets cookies. In Europe and the UK it does not load at all unless you accept."))
    if ident:
        rows.append((
            "Network lookup",
            "The city and the network your connection belongs to, and where it resolves, the company "
            "that network belongs to.",
            "Account level only — the organisation, never you as an individual. Computed per request "
            "and not stored."))
        rows.append((
            "Weather (open-meteo.com)",
            "Once the network lookup has returned a city, the site asks open-meteo for the current "
            "temperature and conditions in that city.",
            "A city name is sent, never your IP address or anything identifying. No key, no cookie, "
            "no account. Used only to write the line on the page."))

    table = "".join(
        f"<tr><td><b>{r[0]}</b></td><td>{r[1]}</td><td>{r[2]}</td></tr>" for r in rows)

    body = f"""<div class="shell"><main>
<section class="hero" style="padding-bottom:var(--s6)">
  <a class="backlink" href="/">← Back to the site</a>
  <h1 class="display" style="font-size:clamp(38px,6vw,64px);margin-top:var(--s5)">Privacy</h1>
  <p class="lede">What this site collects, who gets it, and how to say no. Last updated {p.get('updated','')}.</p>
</section>
<section>
  <div class="sec-head"><div class="label"><span class="tick"></span> What is collected</div></div>
  <div style="overflow-x:auto">
  <table style="width:100%;border-collapse:collapse;font-size:14.5px">
    <thead><tr>
      <th style="text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule)" class="label">Source</th>
      <th style="text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule)" class="label">What</th>
      <th style="text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule)" class="label">Notes</th>
    </tr></thead>
    <tbody>{table}</tbody>
  </table></div>
  <style>tbody td{{padding:12px;border-bottom:1px solid var(--rule-soft);vertical-align:top;color:var(--ink-soft)}}
  tbody td b{{color:var(--ink)}}</style>
</section>
<section>
  <div class="sec-head"><div class="label"><span class="tick"></span> Your choices</div>
    <h2 class="display" style="font-size:clamp(24px,3vw,34px)">Three ways to say no</h2></div>
  <ul class="klist" style="max-width:66ch">
    <li><b>Global Privacy Control.</b> If your browser sends a GPC signal, no analytics load at all,
        wherever you are. Nothing to click.</li>
    <li><b>The cookie choice.</b> Shown automatically in Europe and the UK, where opt-in is required
        before non-essential cookies. Reopen it any time from the footer link on the main page.</li>
    <li><b>Your browser.</b> Blocking cookies or using a private window works, and the site is built
        to degrade quietly when you do.</li>
  </ul>
  <p class="note" style="margin-top:var(--s4);max-width:66ch">Outside Europe and the UK the tags load
    without a banner, which is what the law in the United States and Australia actually requires —
    notice rather than opt-in. This page is that notice.</p>
</section>
<section>
  <div class="sec-head"><div class="label"><span class="tick"></span> Automated assessment</div>
    <h2 class="display" style="font-size:clamp(24px,3vw,34px)">The page scores you. Here is how.</h2></div>
  <p class="prose">The live panel assigns you an engagement score, a stage and a suggested next action,
    computed from what you do on the page — sections read, tools used, time spent. It is arithmetic
    running in your browser, it is shown to you as it happens, and it makes no decision that affects
    your rights or your access to anything. Nothing about it is stored on a server or used to decide
    anything about you.</p>
  <p class="prose" style="margin-top:var(--s3)">If you spend long enough on the page, or complete the
    diagnostic, it also writes you a short note in prose. That note is assembled in your browser from
    the same facts listed above, it lists at the bottom exactly which ones it used, and no copy of it
    exists anywhere else.</p>
  <p class="prose" style="margin-top:var(--s3)">This disclosure is voluntary. It is the kind of thing
    Australian privacy law will require of larger organisations from December 2026, and it seems
    contrary to the spirit of a site about being straight with people to wait to be asked.</p>
</section>
<section>
  <div class="sec-head"><div class="label"><span class="tick"></span> Contact</div></div>
  <p class="prose">Questions, or want anything removed: <a href="mailto:{p.get('contact', prof.get('email',''))}">{p.get('contact', prof.get('email',''))}</a>.
    There is no account to delete and no mailing list to leave.</p>
</section>
<footer><div>Sean Stone · <a href="/">seanstone.com</a></div></footer>
</main></div>"""
    return "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n" \
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" \
           + head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n"


def main() -> int:
    template = (SRC / "template.html").read_text(encoding="utf-8")
    raw = (SRC / "site.json").read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"site.json is not valid JSON — line {e.lineno}, column {e.colno}: {e.msg}")
        return 1

    # Guard against breaking out of the <script> block.
    payload = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")

    if TOKEN not in template:
        print(f"template.html is missing the {TOKEN} placeholder.")
        return 1

    html = template.replace(TOKEN, payload)

    noindex = bool(data.get("flags", {}).get("noindex"))
    domain = data.get("profile", {}).get("site", "seanstone.com")
    robots = ('<meta name="robots" content="noindex, nofollow">' if noindex
              else '<meta name="robots" content="index, follow">')
    html = html.replace(ROBOTS, robots)

    # Analytics. Cloudflare's beacon is cookieless so it loads unconditionally;
    # GA4 and ContentSquare set cookies, so they are handed to the page as config
    # and loaded by the consent gate in template.html — blocked until accepted
    # where consent is legally required, immediate elsewhere.
    a = data.get("analytics", {})
    tags = []
    if a.get("cloudflareToken"):
        tags.append(
            '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
            f'data-cf-beacon=\'{{"token": "{a["cloudflareToken"]}"}}\'></script>')
    gated = {k: a.get(k, "") for k in ("ga4", "contentsquare") if a.get(k)}
    if gated:
        tags.append("<script>window.__ANALYTICS__=" + json.dumps(gated) + ";</script>")
    html = html.replace(ANALYTICS, "\n".join(tags))

    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "CNAME").write_text(f"{domain}\n", encoding="utf-8")

    # robots.txt + sitemap.xml, consistent with the noindex flag
    if noindex:
        (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    else:
        (OUT / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\n\nSitemap: https://{domain}/sitemap.xml\n",
            encoding="utf-8")
        today = datetime.date.today().isoformat()
        urls = [f"https://{domain}/"] + [
            f"https://{domain}/case/{p['id']}/" for p in data.get("projects", []) if p.get("case")
        ]
        entries = "\n".join(
            f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{entries}\n</urlset>\n", encoding="utf-8")

    priv = OUT / "privacy"
    priv.mkdir(exist_ok=True)
    (priv / "index.html").write_text(render_privacy(data, html), encoding="utf-8")

    # Standalone, indexable page per case study at /case/<id>/ — same single file,
    # opened straight onto that case, with its own title, description and canonical.
    for p in data.get("projects", []):
        if not p.get("case"):
            continue
        page = html.replace(
            "<title>Sean Stone — Revenue Systems</title>",
            f"<title>{p['name']} — Sean Stone</title>")
        page = page.replace(
            f'<link rel="canonical" href="https://{domain}/">',
            f'<link rel="canonical" href="https://{domain}/case/{p["id"]}/">')
        page = page.replace(
            f'<meta property="og:url" content="https://{domain}/">',
            f'<meta property="og:url" content="https://{domain}/case/{p["id"]}/">')
        page = page.replace(
            '<meta property="og:title" content="Sean Stone — I don\'t advise on the revenue system. I build it.">',
            f'<meta property="og:title" content="{p["name"]} — {p["thesis"]}">')
        page = page.replace(
            '<meta name="description" content="Sean Stone builds revenue systems \u2014 CRM architecture, GTM engineering and AI-directed product builds. Twenty-five years, 50+ B2B companies, production software shipped.">',
            f'<meta name="description" content="{esc(p["case"]["problem"][:180].rsplit(" ", 1)[0])}\u2026">')
        page = page.replace(
            f'<meta property="og:description" content="An instrumented portfolio: a working enquiry engine, a revenue-leak diagnostic, and a scope builder. Every claim is one click from its evidence.">',
            f'<meta property="og:description" content="{esc(p["thesis"])}">')
        # Pre-render the case body into the static HTML, and open it without JS.
        page = page.replace(
            '<section class="caseview" id="case-sec" aria-live="polite"></section>',
            f'<section class="caseview" id="case-sec" aria-live="polite">'
            f'{render_case(p, data["projects"])}</section>', 1)
        page = page.replace(
            "<body>",
            f'<body class="case-open">\n<script>window.__OPEN_CASE__={json.dumps(p["id"])};</script>',
            1)
        case_dir = OUT / "case" / p["id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "index.html").write_text(page, encoding="utf-8")

    # Artifact variant: no doctype/html/head/body wrapper.
    head = html[html.index("<title>"):html.index("</head>")].strip()
    body = html[html.index("<body>") + len("<body>"):html.index("</body>")].strip()
    BUILD.mkdir(exist_ok=True)
    (BUILD / "artifact.html").write_text(head + "\n\n" + body + "\n", encoding="utf-8")

    counts = {
        "projects": len(data.get("projects", [])),
        "capabilities": len(data.get("capabilities", [])),
        "questions": len(data.get("diagnostic", {}).get("questions", [])),
        "outcomes": len(data.get("scope", {}).get("outcomes", [])),
        "timeline": len(data.get("timeline", [])),
    }
    flags = data.get("flags", {})
    print(f"built index.html — {len(html):,} bytes")
    print("  content: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
    print(f"  flags:   engagementOffer={flags.get('engagementOffer')}, showRates={flags.get('showRates')}")
    print(f"  rate:    ${data.get('rate', {}).get('hourly')}/hr")
    print(f"  robots:  {'noindex' if noindex else 'index'}")
    on = [k for k, v in data.get("analytics", {}).items() if v]
    print(f"  tags:    {', '.join(on) if on else 'none — see ROADMAP.md Phase 1'}")
    print(f"  identity:{' ' + data.get('identity', {}).get('endpoint', '') if data.get('identity', {}).get('endpoint') else ' browser-only (no Worker endpoint set)'}")
    print(f"  pages:   / plus {sum(1 for p in data.get('projects', []) if p.get('case'))} case pages, /privacy/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

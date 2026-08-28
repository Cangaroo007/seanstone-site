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
        page = page.replace("<body>", f"<body>\n<script>window.__OPEN_CASE__={json.dumps(p['id'])};</script>", 1)
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
    print(f"  pages:   / plus {sum(1 for p in data.get('projects', []) if p.get('case'))} case pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())

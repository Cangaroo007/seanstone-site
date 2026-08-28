#!/usr/bin/env python3
"""Generate dist/og.png — the LinkedIn / social share card. Run from the repo root:

    python3 tools/make_og.py

Not part of build.py; the image only needs regenerating when the headline,
the metrics or the domain change. Uses DejaVu Serif as a stand-in for
Instrument Serif — swap the font paths if you install the real face.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER, INK, ACC, MUT, GRID = (232,235,231), (16,21,19), (14,110,99), (93,102,95), (222,226,221)
LINES = ["I don't advise on", "the revenue system."]
ITALIC_LINE = "I build it."
STATS = "25 years  ·  50+ B2B companies  ·  $200M+ in portfolio sales"
DOMAIN = "seanstone.com"
TAGS = "RevOps · GTM engineering · AI-directed build"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRID)

    base = "/usr/share/fonts/truetype/dejavu/"
    serif = font(base + "DejaVuSerif.ttf", 64)
    serif_i = font(base + "DejaVuSerif-Italic.ttf", 64)
    mono = font(base + "DejaVuSansMono.ttf", 20)
    sans = font(base + "DejaVuSans.ttf", 24)

    d.text((72, 64), "SEAN STONE  ·  REVENUE SYSTEMS", font=mono, fill=MUT)
    y = 150
    for line in LINES:
        d.text((72, y), line, font=serif, fill=INK)
        y += 78
    d.text((72, y), ITALIC_LINE, font=serif_i, fill=ACC)
    d.text((72, 430), STATS, font=sans, fill=MUT)
    d.line([(72, 490), (1128, 490)], fill=(200, 205, 199), width=1)
    d.text((72, 516), DOMAIN, font=mono, fill=INK)
    d.text((640, 516), TAGS, font=mono, fill=MUT)

    img.save("og.png")
    print("wrote og.png")


if __name__ == "__main__":
    main()

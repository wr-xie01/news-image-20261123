#!/usr/bin/env python3
"""Draw the 23 November 2026 news front page (1024x1024 PNG).

One file, no network, no inputs: run `python3 generate_image.py` and it
writes entry.png next to itself. All six stories happened or were first
reported on Monday 23 November 2026.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 32, 44)
NAVY = (24, 48, 92)
RED = (178, 44, 38)
GREY = (90, 92, 96)
CARD = (255, 255, 255)
LINE = (200, 196, 184)
ACCENT = (24, 48, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, box):
    """Small pictogram for one story, drawn with plain PIL shapes.

    box is (x0, y0, x1, y1); the drawing uses only lines, arcs and
    polygons, so it stays crisp at any size.
    """
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0
    col = NAVY
    if kind == "chart":  # falling market chart
        draw.line([(x0 + 4, y1 - 8), (x0 + 4, y0 + 4)], fill=col, width=3)
        draw.line([(x0 + 4, y1 - 8), (x1 - 4, y1 - 8)], fill=col, width=3)
        pts = [(x0 + 8, y0 + 12), (x0 + 18, y0 + 18), (x0 + 26, y0 + 14),
               (x0 + 36, y0 + 28), (x0 + 44, y0 + 34)]
        draw.line(pts, fill=RED, width=4, joint="curve")
        draw.line([(x0 + 44, y0 + 34), (x0 + 44, y0 + 26),
                   (x0 + 36, y0 + 34)], fill=RED, width=3)
    elif kind == "cricket":  # bat and ball
        draw.line([(x0 + 12, y1 - 6), (x0 + 30, y0 + 10)], fill=col, width=7)
        draw.ellipse([x0 + 26, y0 + 6, x0 + 40, y0 + 20], fill=col)
        draw.ellipse([x1 - 18, y1 - 18, x1 - 4, y1 - 4], fill=RED)
        draw.arc([x1 - 18, y1 - 18, x1 - 4, y1 - 4], 200, 340, fill=(255, 255, 255), width=2)
    elif kind == "screen":  # magnifier over a ribbon cross
        draw.ellipse([x0 + 6, y0 + 4, x0 + 34, y0 + 32], outline=col, width=4)
        draw.line([(x0 + 30, y0 + 28), (x0 + 44, y0 + 42)], fill=col, width=5)
        draw.line([(x0 + 20, y0 + 13), (x0 + 20, y0 + 23)], fill=RED, width=4)
        draw.line([(x0 + 15, y0 + 18), (x0 + 25, y0 + 18)], fill=RED, width=4)
    elif kind == "flags":  # two meeting flags
        draw.line([(x0 + 12, y0 + 4), (x0 + 12, y1 - 4)], fill=col, width=3)
        draw.polygon([(x0 + 12, y0 + 4), (x0 + 30, y0 + 10), (x0 + 12, y0 + 16)],
                     fill=RED)
        draw.line([(x1 - 12, y0 + 4), (x1 - 12, y1 - 4)], fill=col, width=3)
        draw.polygon([(x1 - 12, y0 + 4), (x1 - 30, y0 + 10), (x1 - 12, y0 + 16)],
                     fill=(34, 120, 60))
    elif kind == "ball":  # football
        draw.ellipse([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=col, width=4)
        r = w // 5
        px = [cx + r * 0.95, cx + r * 0.29, cx - r * 0.77, cx - r * 0.77,
              cx + r * 0.29]
        py = [cy, cy + r * 0.95, cy + r * 0.59, cy - r * 0.59, cy - r * 0.95]
        draw.polygon(list(zip(px, py)), fill=col)
        for px_, py_ in zip(px, py):
            draw.line([(cx + (px_ - cx) * 2.1, cy + (py_ - cy) * 2.1),
                       (px_, py_)], fill=col, width=2)
    elif kind == "quake":  # seismic wave
        pts = []
        for i in range(9):
            px = x0 + 4 + i * (w - 8) // 8
            py = cy + (-1 if i % 2 else 1) * (h // 3) * (1 if i in (2, 6) else 0.35)
            if i in (0, 8):
                py = cy
            pts.append((px, py))
        draw.line(pts, fill=RED, width=4, joint="curve")
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)


STORIES = [
    ("SEOUL", "chart",
     "KOSPI slides 5.8% as AI sell-off deepens",
     "Seoul readies a 10 trillion won stabilisation fund after the "
     "Nasdaq's worst week since 2020; US futures rebound."),
    ("WELLINGTON", "cricket",
     "India denied as New Zealand bat out a draw",
     "Mitchell and Phillips hold firm on day five; New Zealand finish "
     "239 for 5 after India's record 720 for 9."),
    ("LONDON", "screen",
     "NHS launches world's biggest AI cancer trial",
     "The EDITH trial will test AI reading of mammograms for nearly "
     "700,000 women at 30 sites across the UK."),
    ("NEW DELHI", "flags",
     "Nepal's PM meets Modi in Delhi",
     "Balen Shah's first visit as PM brings talks, a joint vision, "
     "and a new Ayodhya-Janakpur train service."),
    ("ZURICH", "ball",
     "FIFA confirms UK as 2035 World Cup host",
     "The first World Cup in Britain since 1966: 48 teams, 104 "
     "matches and 19 venues across four nations."),
    ("VANUATU", "quake",
     "Deep M6.5 quake shakes the Pacific",
     "The tremor struck 600 km down at 02:40 UTC; no damage was "
     "reported and there was no tsunami threat."),
]


def draw_card(draw, x, y, cw, ch, city, icon, headline, body):
    draw.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                           fill=CARD, outline=LINE, width=2)
    pad = 18
    ix, iy = x + pad, y + pad
    draw_icon(draw, icon, (ix, iy, ix + 48, iy + 48))
    kicker = font(SANS_B, 16)
    draw.text((ix + 60, iy + 14), city, font=kicker, fill=RED)
    ty = y + pad + 62
    hl = font(SANS_B, 22)
    for line in wrap(draw, headline, hl, cw - 2 * pad)[:3]:
        draw.text((x + pad, ty), line, font=hl, fill=INK)
        ty += 27
    ty += 6
    bf = font(SANS, 17)
    for line in wrap(draw, body, bf, cw - 2 * pad)[:4]:
        draw.text((x + pad, ty), line, font=bf, fill=(52, 56, 64))
        ty += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    mast = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 34), title, font=mast, fill=NAVY)
    draw.line([(36, 118), (W - 36, 118)], fill=NAVY, width=3)

    # Date band
    draw.rectangle([36, 132, W - 36, 178], fill=NAVY)
    band = font(SANS_B, 26)
    date = "MONDAY  •  23 NOVEMBER 2026"
    dw = draw.textlength(date, font=band)
    draw.text(((W - dw) / 2, 142), date, font=band, fill=(255, 255, 255))

    # Subhead
    sub = font(SANS, 18)
    subline = "Six stories from six corners of the world — one day, one page."
    sw = draw.textlength(subline, font=sub)
    draw.text(((W - sw) / 2, 192), subline, font=sub, fill=GREY)

    # Story grid: 3 columns x 2 rows
    gx, gy = 36, 232
    cw, ch = 296, 336
    gap = 20
    for i, (city, icon, headline, body) in enumerate(STORIES):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        draw_card(draw, cx, cy, cw, ch, city, icon, headline, body)

    # Footer
    foot = font(SANS, 15)
    line = ("All six stories above happened or were first reported "
            "on 23 November 2026.")
    fw = draw.textlength(line, font=foot)
    draw.text(((W - fw) / 2, 946), line, font=foot, fill=GREY)
    draw.line([(36, 932), (W - 36, 932)], fill=LINE, width=2)

    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

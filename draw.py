#!/usr/bin/env python3
"""Draw 'The World Today - Wednesday 25 November 2026' as a 1024x1024 PNG.

Every story was checked against live news on 25 Nov 2026: each one either
happened or was first reported that day. Nothing is invented. The picture is
a newspaper front page: masthead, three illustrated leads, nine minis, a
briefs index and a pinned world map. Output is fully deterministic.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
TEAL = (14, 110, 105)
GOLD = (176, 124, 18)
GREY = (110, 104, 90)
LIGHT = (216, 210, 192)
PURPLE = (96, 56, 140)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 56)
F_DATE = font(SANS_B, 25)
F_TAG = font(SANS, 15)
F_KICK = font(SANS_B, 14)
F_HEAD = font(SANS_B, 21)
F_BODY = font(SANS, 14)
F_MINI_H = font(SANS_B, 15)
F_MINI_B = font(SANS, 12)
F_BRIEF_H = font(SANS_B, 14)
F_BRIEF = font(SANS, 13)
F_SEC = font(SANS_B, 16)
F_KEY = font(SANS, 12)
F_PIN = font(SANS_B, 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real pixel widths."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=4, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def rule(draw, x, y, w, fill=INK, thick=2):
    draw.rectangle([x, y, x + w, y + thick - 1], fill=fill)


# ---------------------------------------------------------------- leads art

def art_cpi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 240, 245), outline=GREY)
    bx, by = x + 16, y + 14
    bw, bh = w - 32, h - 40
    draw.line([bx, by + bh, bx + bw, by + bh], fill=INK, width=2)
    draw.line([bx, by, bx, by + bh], fill=INK, width=2)
    vals = [3.6, 4.1, 4.3, 4.9]
    labels = ["JUL", "AUG", "SEP", "OCT"]
    step = bw // 4
    for i, v in enumerate(vals):
        bar_h = int((v / 5.5) * (bh - 8))
        x0 = bx + 8 + i * step
        col = RED if i == 3 else BLUE
        draw.rectangle([x0, by + bh - bar_h, x0 + step - 14, by + bh], fill=col)
        draw.text((x0 + 2, by + bh - bar_h - 18), f"{v}%", font=F_BRIEF, fill=INK)
        draw.text((x0 + 2, by + bh + 4), labels[i], font=F_KEY, fill=GREY)
    draw.text((x + 8, y + 6), "CPI y/y", font=F_KEY, fill=GREY)


def art_treaty(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 226), outline=GREY)
    # two flag poles with waving flags
    for fx, col_main, col_star in ((x + 26, (0, 47, 108), (255, 255, 255)),
                                   (x + w - 96, (0, 90, 60), (255, 215, 0))):
        draw.line([fx, y + 12, fx, y + h - 14], fill=INK, width=3)
        draw.polygon([(fx, y + 12), (fx + 62, y + 20), (fx + 62, y + 48),
                      (fx, y + 42)], fill=col_main)
        for sx, sy in ((fx + 16, y + 26), (fx + 34, y + 22), (fx + 48, y + 30)):
            draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=col_star)
    # document with seal between the flags
    dx, dy = x + w // 2 - 34, y + h - 52
    draw.rectangle([dx, dy, dx + 68, dy + 40], fill=(255, 255, 255), outline=INK)
    for i in range(3):
        draw.line([dx + 8, dy + 9 + i * 9, dx + 60, dy + 9 + i * 9], fill=GREY)
    draw.ellipse([dx + 48, dy + 26, dx + 64, dy + 42], fill=RED, outline=(120, 10, 20))


def art_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 233, 232), outline=GREY)
    pts = [(x + 14, y + 22), (x + 60, y + 30), (x + 106, y + 26),
           (x + 152, y + 44), (x + 198, y + 52), (x + 244, y + 74),
           (x + 290, y + 88)]
    draw.line(pts, fill=RED, width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.text((x + 16, y + h - 26), "NIKKEI -2.8%   KOSPI -5.3%", font=F_BRIEF, fill=INK)
    draw.text((x + w - 62, y + 8), "-5.1%", font=F_BRIEF, fill=RED)


# ---------------------------------------------------------------- mini icons

def icon_ball(draw, x, y, s):
    draw.ellipse([x, y, x + s, y + s], fill=(255, 255, 255), outline=INK, width=2)
    draw.polygon([(x + s * .42, y + s * .38), (x + s * .58, y + s * .38),
                  (x + s * .62, y + s * .55), (x + s * .5, y + s * .66),
                  (x + s * .38, y + s * .55)], fill=INK)


def icon_quake(draw, x, y, s):
    draw.line([(x + 4, y + s * .7), (x + s * .3, y + s * .3),
               (x + s * .5, y + s * .62), (x + s * .7, y + s * .25),
               (x + s - 4, y + s * .55)], fill=INK, width=3)
    draw.line([(x + 4, y + s - 6), (x + s - 4, y + s - 6)], fill=INK, width=2)


def icon_gold(draw, x, y, s):
    draw.polygon([(x + 8, y + s * .62), (x + 14, y + s * .3),
                  (x + s - 14, y + s * .3), (x + s - 8, y + s * .62)],
                 fill=GOLD, outline=(120, 80, 0))
    draw.line([(x + 8, y + s * .62), (x + s - 8, y + s * .62)], fill=(120, 80, 0), width=2)


def icon_doc(draw, x, y, s):
    draw.rectangle([x + 10, y + 6, x + s - 10, y + s - 6], fill=(255, 255, 255), outline=INK, width=2)
    for i in range(3):
        draw.line([x + 16, y + 16 + i * 10, x + s - 16, y + 16 + i * 10], fill=GREY)


def icon_ribbon(draw, x, y, s):
    draw.ellipse([x + 8, y + 8, x + s * .55, y + s * .55], outline=PURPLE, width=3)
    draw.ellipse([x + s * .45, y + 8, x + s - 8, y + s * .55], outline=PURPLE, width=3)
    draw.polygon([(x + s * .42, y + s * .5), (x + s * .58, y + s * .5),
                  (x + s * .68, y + s - 8), (x + s * .5, y + s * .68),
                  (x + s * .32, y + s - 8)], fill=PURPLE)


def icon_chart(draw, x, y, s):
    for i, bh in enumerate((14, 24, 10, 30)):
        x0 = x + 8 + i * 12
        draw.rectangle([x0, y + s - 8 - bh, x0 + 8, y + s - 8], fill=BLUE)


def icon_bank(draw, x, y, s):
    draw.polygon([(x + 6, y + 14), (x + s // 2, y + 4), (x + s - 6, y + 14)], fill=BLUE)
    for i in range(3):
        x0 = x + 10 + i * 14
        draw.rectangle([x0, y + 18, x0 + 7, y + s - 10], fill=BLUE)
    draw.rectangle([x + 6, y + s - 10, x + s - 6, y + s - 6], fill=BLUE)


ICONS = {"ball": icon_ball, "quake": icon_quake, "gold": icon_gold,
         "doc": icon_doc, "ribbon": icon_ribbon, "chart": icon_chart,
         "bank": icon_bank}
ICON_BG = {"ball": (220, 235, 220), "quake": (240, 228, 210),
           "gold": (248, 236, 190), "doc": (226, 232, 240),
           "ribbon": (238, 226, 244), "chart": (232, 238, 245),
           "bank": (226, 232, 240)}

# ---------------------------------------------------------------- content

LEADS = [
    ("INFLATION  •  CANBERRA", "Australia's inflation jumps to 4.9%",
     "Prices rose 4.9% in the year to October, up from 4.3% — a three-year "
     "high. Housing drove it, up 6.4%; core inflation hit 3.8%.", art_cpi),
    ("PACIFIC  •  CANBERRA", "Solomons signs Australia security pact",
     "Australia and Solomon Islands signed a treaty making Canberra the "
     "islands' top security partner, as the 2022 China pact lapses.", art_treaty),
    ("MARKETS  •  ASIA", "Asian stocks tumble as AI rally fizzles",
     "Chip shares led a Wednesday sell-off: Tokyo's Nikkei fell 2.8%, Seoul's "
     "Kospi 5.3% and Taiwan 5.1% after Wall Street's AI slide.", art_markets),
]

MINIS = [
    ("ball", "Champions League: Real hit five",
     "Real Madrid 5-1 PSV; Arsenal 1-1 Dortmund; Man City 2-2 Napoli. "
     "Tuesday night in Europe, results into Wednesday in Asia."),
    ("quake", "M5.9 quake in the Southern Ocean",
     "A shallow magnitude 5.9 quake struck the Balleny Islands region at "
     "01:38 UTC. No damage expected; green alert issued."),
    ("quake", "M5.1 quake jolts Antique, Philippines",
     "A magnitude 5.1 quake hit near Valderrama at 07:29 local time. "
     "Aftershocks expected, officials said."),
    ("gold", "Gold slumps on Fed and tariff fears",
     "Bullion slid on Wednesday, wiping out Monday's rebound, as traders "
     "priced more US rate hikes and tariff-driven selling."),
    ("doc", "US tariff decision due today",
     "Washington is expected to unveil new duties on 16 trading partners "
     "after its excess-capacity probe. Rates still unclear."),
    ("ribbon", "A day against violence on women",
     "25 November is the International Day for the Elimination of Violence "
     "against Women, marked worldwide today."),
    ("quake", "M4.3 quake near Shihezi, China",
     "A magnitude 4.3 earthquake struck 69 km south-west of Shihezi at "
     "01:19 UTC, at a depth of 10 km."),
    ("chart", "Perth inflation leaps to 5.5%",
     "Perth prices rose 0.8% in October alone — the biggest jump of any "
     "Australian capital. Hobart hit 6.0%, Adelaide 5.7%."),
    ("bank", "SoftBank extends its slide",
     "SoftBank fell about 13% in Wednesday trade, extending a drop of "
     "nearly 70% since June as debt worries grow."),
]

BRIEFS = [
    ("TSMC -5%, Samsung -8%", "chipmakers lead Asia's sell-off."),
    ("Advantest -12%, Tokyo Electron -11%", "Nikkei's chip drag."),
    ("MSCI Asia ex-Japan -2.3%", "broad regional slide."),
    ("S&P 500 futures -0.3%", "Wall Street's weak lead."),
    ("Aussie dollar jumps", "after the hot CPI print."),
    ("Electricity +25.2%", "as energy rebates ended."),
    ("Transport +10.6%", "on dearer fuel."),
    ("Core inflation 3.8%", "well above the RBA's 2-3% band."),
    ("UCL: Galatasaray 1-0 Villa", "Bodo/Glimt 1-0 LASK."),
    ("UCL: Como 1-0 AEK", "Feyenoord 0-1 Porto."),
    ("UCL: Leipzig 3-1 Lens", "Slovan 0-2 Real Betis."),
    ("M4.4 quake off Liloy", "Zamboanga del Norte, 01:01 local."),
]

# lon/lat of each numbered pin, plus a small badge offset (dx, dy) so
# clustered pins do not cover each other; a hairline joins badge to spot.
PINS = [
    ("1", -35.3, 149.1, "Canberra", (0, 0)),
    ("2", -33.9, 151.2, "Sydney", (14, 10)),
    ("3", 35.7, 139.7, "Tokyo", (12, -12)),
    ("4", 37.6, 127.0, "Seoul", (-14, -10)),
    ("5", 25.0, 121.6, "Taipei", (-2, 14)),
    ("6", -63.2, 171.0, "Balleny Is.", (0, 0)),
    ("7", 10.9, 122.2, "Antique", (12, 8)),
    ("8", 40.4, -3.7, "Madrid", (-14, 8)),
    ("9", 51.5, -0.1, "London", (12, -12)),
]

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-75, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 42),
     (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-97, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-158, 58)],
    # South America
    [(-80, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -54),
     (-73, -50), (-73, -37), (-80, -20), (-81, -6)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (26, -34), (18, -35), (12, -18), (9, 4), (-8, 4)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 58), (10, 57), (18, 56),
     (21, 55), (24, 60), (30, 70), (40, 68), (55, 69), (70, 73), (90, 75),
     (110, 76), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60),
     (162, 56), (156, 51), (142, 45), (140, 40), (135, 35), (130, 33),
     (127, 35), (122, 38), (120, 32), (110, 20), (105, 10), (100, 8),
     (97, 16), (92, 21), (88, 22), (80, 15), (76, 8), (73, 20), (66, 25),
     (60, 25), (57, 27), (52, 28), (48, 30), (44, 29), (40, 36), (36, 36),
     (30, 36), (26, 38), (22, 37), (18, 40), (12, 44), (8, 44), (3, 43),
     (-2, 37), (-9, 37)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    rule(d, 0, 0, W, INK, 6)
    d.text((16, 14), "THE WORLD TODAY", font=F_TITLE, fill=INK)
    d.text((16, 72), "One day's world news — every story checked for this date",
           font=F_TAG, fill=GREY)
    date_txt = "WEDNESDAY"
    d.text((W - 16 - d.textlength(date_txt, font=F_DATE), 12), date_txt,
           font=F_DATE, fill=RED)
    d.text((W - 16 - d.textlength("25 NOVEMBER 2026", font=F_DATE), 42),
           "25 NOVEMBER 2026", font=F_DATE, fill=INK)
    rule(d, 16, 92, W - 32, INK, 3)

    # ---- three illustrated leads
    lead_y, lead_h = 100, 236
    col_w, gap = 322, 9
    for i, (kick, head, body, art) in enumerate(LEADS):
        x = 16 + i * (col_w + gap)
        d.text((x, lead_y), kick, font=F_KICK, fill=RED)
        art(d, x, lead_y + 20, col_w, 112)
        hy = lead_y + 140
        hy = para(d, x, hy, head, F_HEAD, col_w, leading=1, max_lines=2)
        para(d, x, hy + 2, body, F_BODY, col_w, leading=2, max_lines=3)
        if i < 2:
            d.line([x + col_w + 4, lead_y, x + col_w + 4, lead_y + lead_h],
                   fill=LIGHT, width=2)
    rule(d, 16, 344, W - 32, INK, 2)

    # ---- nine minis, 3 x 3
    d.text((16, 354), "MORE OF THE DAY", font=F_SEC, fill=INK)
    mini_y0, mini_h, mini_w = 378, 96, 322
    for i, (icon, head, body) in enumerate(MINIS):
        r, c = divmod(i, 3)
        x = 16 + c * (mini_w + gap)
        y = mini_y0 + r * (mini_h + 8)
        d.rectangle([x, y, x + mini_w, y + mini_h], outline=LIGHT, width=1)
        ix, iy, s = x + 8, y + 8, 52
        d.rectangle([ix, iy, ix + s, iy + s], fill=ICON_BG[icon], outline=GREY)
        ICONS[icon](d, ix + 2, iy + 2, s - 4)
        tx = x + 70
        ty = para(d, tx, y + 7, head, F_MINI_H, mini_w - 78, leading=1, max_lines=1)
        para(d, tx, ty + 1, body, F_MINI_B, mini_w - 78, leading=1, max_lines=3)
    rule(d, 16, 682, W - 32, INK, 2)

    # ---- briefs index
    d.text((16, 692), "THE DAY IN BRIEF", font=F_SEC, fill=INK)
    by = 716
    for i, (bold, rest) in enumerate(BRIEFS):
        c, r = divmod(i, 6)
        x = 16 + c * 500
        y = by + r * 20
        d.text((x, y), "•", font=F_BRIEF, fill=RED)
        d.text((x + 14, y), bold, font=F_BRIEF_H, fill=INK)
        bw = d.textlength(bold, font=F_BRIEF_H)
        d.text((x + 14 + bw + 4, y), rest, font=F_BRIEF, fill=INK)
    rule(d, 16, 844, W - 32, INK, 2)

    # ---- pinned world map
    d.text((16, 854), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
    mx, my, mw, mh = 16, 878, W - 32, 104
    d.rectangle([mx, my, mx + mw, my + mh], fill=(226, 234, 240), outline=GREY)

    def project(lon, lat):
        px = mx + (lon + 180) / 360 * mw
        py = my + (85 - lat) / 155 * mh
        return px, py

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LIGHT, outline=GREY)
    # Antarctica sliver
    d.polygon([project(-180, -70), project(180, -70), project(180, -78),
               project(-180, -78)], fill=LIGHT, outline=GREY)
    for num, lat, lon, _label, (odx, ody) in PINS:
        px, py = project(lon, lat)
        bx, by = px + odx, py + ody
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        if odx or ody:
            d.line([px, py, bx, by], fill=RED, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED,
                  outline=(255, 255, 255))
        tw = d.textlength(num, font=F_PIN)
        d.text((bx - tw / 2, by - 6), num, font=F_PIN, fill=(255, 255, 255))
    key = "  •  ".join(f"{n} {lab}" for n, _la, _lo, lab, _o in PINS)
    d.text((16, 988), key, font=F_KEY, fill=INK)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    build()

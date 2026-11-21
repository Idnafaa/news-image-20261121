"""Render the news-image-20261121 front page into entry.png.

"THE WORLD IN ONE DAY - SATURDAY, 21 NOVEMBER 2026": a broadsheet poster,
1024x1024, drawn with PIL primitives (no photos, no network). 31 stories:
1 hero, 6 illustrated cards, 24 briefs, plus masthead, dateline, figures
strip and sources footer. Stories happened or were first reported on
21 Nov 2026 (any time zone) and were cross-checked across two or more
sources (Reuters, AP, BBC, IMD, USGS, IANS and others).

Deterministic: fixed layout, no randomness; re-running reproduces the
identical PNG bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 22
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (28, 28, 30)
NAVY = (27, 42, 74)
NAVY_DEEP = (18, 30, 56)
RED = (178, 34, 34)
RED_BRIGHT = (205, 48, 48)
GOLD = (201, 150, 39)
GREY = (96, 96, 100)
LIGHT_LINE = (205, 198, 184)
CARD_BG = (255, 253, 248)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_MASTHEAD = font(SERIF_B, 54)
F_DATELINE = font(SANS_B, 14)
F_FIG_NUM = font(SERIF_B, 24)
F_FIG_CAP = font(SANS, 9)
F_KICKER = font(SANS_B, 10)
F_HERO_HEAD = font(SERIF_B, 27)
F_HERO_BODY = font(SANS, 11.5)
F_CARD_HEAD = font(SERIF_B, 13.5)
F_CARD_BODY = font(SANS, 9.5)
F_SECTION = font(SERIF_B, 16)
F_BRIEF = font(SANS, 9.5)
F_BRIEF_B = font(SANS_B, 9.5)
F_FOOT = font(SANS, 9)
F_BADGE = font(SANS_B, 11)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(draw, cx, cy, num, r=11):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED_BRIGHT,
                 outline=(255, 255, 255), width=2)
    t = str(num)
    tw = draw.textlength(t, font=F_BADGE)
    draw.text((cx - tw / 2, cy - 8), t, font=F_BADGE, fill=(255, 255, 255))


def draw_text(draw, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes

def scene_missiles(d, box):
    """Missiles streaking over a night skyline."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(20, 28, 52))
    for i in range(14):
        sx = x0 + (i * 53) % w
        sy = y0 + (i * 31) % (h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 235))
    heights = [0.3, 0.45, 0.36, 0.55, 0.4, 0.5, 0.34, 0.44]
    bw = w / len(heights)
    for i, hf in enumerate(heights):
        bx = x0 + i * bw
        d.rectangle([bx + 2, y1 - h * hf, bx + bw - 2, y1], fill=(10, 14, 28))
        for wy in range(3):
            d.rectangle([bx + 6, y1 - h * hf + 6 + wy * 10, bx + 10,
                         y1 - h * hf + 10 + wy * 10], fill=(240, 200, 90))
    for i in range(3):
        sx = x0 + w * (0.15 + 0.3 * i)
        sy = y0 + 10 + i * 8
        ex, ey = sx + w * 0.28, sy + h * 0.45
        d.line([(sx, sy), (ex, ey)], fill=(255, 170, 60), width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 90, 40))
        d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], outline=(255, 140, 60), width=2)


def scene_handshake(d, box):
    """Two flags and a handshake bar."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(225, 232, 245))
    # EU flag
    d.rectangle([x0 + 10, y0 + 8, x0 + 62, y0 + 42], fill=(30, 60, 160))
    for i in range(8):
        import math
        a = i * math.pi / 4
        cx = x0 + 36 + 11 * math.cos(a)
        cy = y0 + 25 + 11 * math.sin(a)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(250, 210, 60))
    # UK-ish flag
    fx = x1 - 62
    d.rectangle([fx, y0 + 8, fx + 52, y0 + 42], fill=(30, 50, 140))
    d.line([(fx, y0 + 8), (fx + 52, y0 + 42)], fill=(255, 255, 255), width=5)
    d.line([(fx + 52, y0 + 8), (fx, y0 + 42)], fill=(255, 255, 255), width=5)
    d.line([(fx + 26, y0 + 8), (fx + 26, y0 + 42)], fill=(220, 40, 50), width=6)
    d.line([(fx, y0 + 25), (fx + 52, y0 + 25)], fill=(220, 40, 50), width=6)
    d.rectangle([x0 + 20, y1 - 22, x1 - 20, y1 - 10], fill=NAVY)
    d.text((x0 + w / 2 - 32, y1 - 21), "DEAL DONE", font=font(SANS_B, 9),
           fill=(255, 255, 255))


def scene_quake(d, box):
    """Cracked ground and shaking buildings."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(238, 226, 205))
    for i, hf in enumerate([0.55, 0.7, 0.5, 0.62]):
        bx = x0 + 12 + i * (w // 4)
        tilt = 4 if i % 2 else -4
        d.polygon([(bx, y1 - 18), (bx + tilt, y1 - 18 - h * hf),
                   (bx + 26 + tilt, y1 - 18 - h * hf), (bx + 26, y1 - 18)],
                  fill=(120, 110, 100))
    d.line([(x0 + 6, y1 - 12), (x0 + w * 0.35, y1 - 20), (x0 + w * 0.55, y1 - 8),
            (x0 + w * 0.8, y1 - 16), (x1 - 8, y1 - 10)], fill=INK, width=3)
    d.text((x0 + 8, y0 + 4), "M 6.8", font=font(SERIF_B, 16), fill=RED)


def scene_chart(d, box):
    """Falling market chart."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(250, 248, 242))
    d.line([(x0 + 10, y1 - 12), (x1 - 8, y1 - 12)], fill=GREY, width=2)
    d.line([(x0 + 10, y0 + 6), (x0 + 10, y1 - 12)], fill=GREY, width=2)
    pts = [(0.08, 0.2), (0.25, 0.3), (0.4, 0.25), (0.55, 0.5), (0.7, 0.6),
           (0.85, 0.85), (0.95, 0.92)]
    xy = [(x0 + w * px, y0 + h * py) for px, py in pts]
    d.line(xy, fill=RED_BRIGHT, width=4)
    for px, py in xy:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x0 + w - 52, y0 + 6), "-3.7%", font=font(SERIF_B, 15), fill=RED)


def scene_mic(d, box):
    """Stage microphone with a warning sign."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(40, 36, 60))
    cx = x0 + w / 2
    d.rounded_rectangle([cx - 12, y0 + 10, cx + 12, y0 + 48], radius=11,
                        fill=(200, 200, 210))
    d.line([(cx, y0 + 48), (cx, y1 - 14)], fill=(160, 160, 170), width=4)
    d.line([(cx - 18, y1 - 12), (cx + 18, y1 - 12)], fill=(160, 160, 170), width=4)
    d.ellipse([x0 + 8, y0 + 8, x0 + 30, y0 + 30], fill=(250, 200, 40),
              outline=INK, width=2)
    d.text((x0 + 15, y0 + 11), "!", font=font(SANS_B, 14), fill=INK)


def scene_cyclone(d, box):
    """Spiral cyclone over coast."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(190, 215, 235))
    cx, cy = x0 + w / 2, y0 + h / 2 - 6
    for r in (30, 22, 14):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=320,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(90, 140, 190))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(110, 150, 90))
    d.text((x0 + 8, y1 - 30), "AKVAN", font=font(SANS_B, 10), fill=NAVY_DEEP)


def scene_scales(d, box):
    """Scales of justice."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(240, 236, 224))
    cx = x0 + w / 2
    d.line([(cx, y0 + 10), (cx, y1 - 16)], fill=GOLD, width=4)
    d.line([(x0 + 14, y0 + 16), (x1 - 14, y0 + 16)], fill=GOLD, width=4)
    for sx in (x0 + 14, x1 - 14):
        d.line([(sx, y0 + 16), (sx - 12, y0 + 36)], fill=GOLD, width=2)
        d.line([(sx, y0 + 16), (sx + 12, y0 + 36)], fill=GOLD, width=2)
        d.arc([sx - 13, y0 + 28, sx + 13, y0 + 44], start=0, end=180,
              fill=GOLD, width=3)
    d.rectangle([cx - 16, y1 - 14, cx + 16, y1 - 8], fill=GOLD)


SCENES = {
    "handshake": scene_handshake,
    "quake": scene_quake,
    "chart": scene_chart,
    "mic": scene_mic,
    "cyclone": scene_cyclone,
    "scales": scene_scales,
}

# ---------------------------------------------------------------- stories

HERO = {
    "num": 1, "kicker": "EUROPE - WAR",
    "head": "Russian missiles fall in Poland as Ukraine is pounded",
    "body": "Two Russian missiles and a suspected drone came down in "
            "south-eastern Poland during one of the largest overnight "
            "attacks on Ukraine. PM Donald Tusk called it an "
            "\"intentional provocation\"; NATO's Mark Rutte called it a "
            "\"grave violation\" of Polish airspace. Russia fired 400+ "
            "drones and 110+ missiles at Ukraine, killing at least 8 "
            "people and wounding two dozen more. No one was hurt in Poland.",
}

CARDS = [
    {"num": 2, "scene": "handshake", "kicker": "BRUSSELS - DIPLOMACY",
     "head": "UK and EU strike biggest post-Brexit deal",
     "body": "PM Andy Burnham and EU leaders agreed 100,000 youth visas "
             "each way for stays up to 3 years, scrapped most food checks "
             "from 2028, linked carbon markets and brought Britain back "
             "into Erasmus+."},
    {"num": 3, "scene": "quake", "kicker": "PERU - EARTHQUAKE",
     "head": "6.8 quake shakes Peru, Lima empties",
     "body": "A magnitude 6.8 earthquake struck Junin in the central "
             "Andes at 129 km deep. Tremors sent Lima residents and "
             "lawmakers into the streets. No casualties or major damage "
             "were reported."},
    {"num": 4, "scene": "chart", "kicker": "WALL STREET - MARKETS",
     "head": "AI sell-off pushes US stocks into correction",
     "body": "The S&P 500 fell 3.7% and the Nasdaq 5.3% as AI shares "
             "tumbled. Anthropic slid 9.1% in its second day of trading; "
             "Nvidia dropped about 14%. The Nasdaq erased all its 2026 "
             "gains."},
    {"num": 5, "scene": "mic", "kicker": "DENMARK - ESPIONAGE",
     "head": "Denmark: Russia plotted to kill rapper",
     "body": "Danish intelligence says Russian services planned to kill "
             "Ukrainian-American rapper Kyivstoner at a concert near "
             "Copenhagen. Armed men were stopped minutes before the show. "
             "Denmark is expelling Russia's defence attache; Moscow "
             "denies it."},
    {"num": 6, "scene": "cyclone", "kicker": "INDIA - WEATHER",
     "head": "Cyclone Akvan batters Odisha coast",
     "body": "Akvan crossed near Gopalpur with winds of 70-80 km/h "
             "gusting to 90, dumping heavy rain across Odisha and Andhra "
             "Pradesh. More than 300,000 people were moved to shelters; "
             "no deaths were reported."},
    {"num": 7, "scene": "scales", "kicker": "THE HAGUE - JUSTICE",
     "head": "World Court: Myanmar committed genocide",
     "body": "The ICJ ruled Myanmar committed genocide against the "
             "Rohingya - the first time it has found a state responsible "
             "for genocide. Myanmar must allow safe returns, pay "
             "reparations and report back within two years."},
]

BRIEFS = [
    ("NEW YORK", "Mayor Mamdani sets 2032 to close the Rikers Island jail."),
    ("DELHI", "Nepal PM Balendra Shah arrives on his first foreign visit."),
    ("WELLINGTON", "KL Rahul: first Indian opener with Test tons in all SENA lands."),
    ("RAJASTHAN", "Congress sweeps polls: 33 of 37 districts, 3,701 seats."),
    ("GAZA", "EU urges Israel to let aid reach flooded Gaza camps."),
    ("LOS ANGELES", "Jury convicts man of starting the 2025 Palisades Fire."),
    ("SHENZHEN", "Trump, Xi and Putin summit ends with little of substance."),
    ("WASHINGTON", "Trump: no rush on Iran, may not decide until 2027."),
    ("HORMUZ", "Tanker strike and fire reported off Khasab."),
    ("WASHINGTON", "US sanctions four Iranians over oil revenues."),
    ("KRYVYI RIH", "Strike leaves two dead, 42 injured, officials say."),
    ("BRUSSELS", "EU adopts 1bn euros in military aid for Ukraine."),
    ("PARIS", "Fourth weekend of cost-of-living protests across France."),
    ("JERUSALEM", "Herzog taps Eisenkot to form a government, not Netanyahu."),
    ("WASHINGTON", "US details handling of $12bn in Venezuelan oil revenue."),
    ("MUMBAI", "Record foreign inflow into Indian shares; Sensex rallies."),
    ("MUNICH", "Bayern lose Harry Kane for months to an ankle tear."),
    ("ABU DHABI", "UAE Bulls win the T10 title for a second straight year."),
    ("BHOPAL", "India women beat Malaysia 4-1 in Asian hockey opener."),
    ("LOS ANGELES", "Hyundai unveils new Elantra at the LA Auto Show."),
    ("NEW YORK", "Banks report vendor cyberattacks; networks unaffected."),
    ("VIENNA", "Austria confirms Foreign Ministry website was hacked."),
    ("CINCINNATI", "Fiona, the famous premature baby hippo, has died."),
    ("ANTALYA", "COP31 talks enter final stage; finance still unresolved."),
]

FIGURES = [
    ("400+", "drones fired at Ukraine overnight"),
    ("6.8", "magnitude of the Peru quake"),
    ("100,000", "youth visas each way, UK-EU deal"),
    ("-3.7%", "S&P 500 fall into correction"),
    ("300,000+", "people sheltered from Akvan"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, 14), title, font=F_MASTHEAD, fill=NAVY_DEEP)
    d.rectangle([MARGIN, 82, W - MARGIN, 85], fill=INK)
    d.rectangle([MARGIN, 88, W - MARGIN, 89], fill=INK)
    dateline = "SATURDAY, 21 NOVEMBER 2026  -  THE WORLD'S NEWS IN ONE IMAGE  -  31 STORIES"
    dw = d.textlength(dateline, font=F_DATELINE)
    d.text(((W - dw) / 2, 94), dateline, font=F_DATELINE, fill=RED)
    d.rectangle([MARGIN, 116, W - MARGIN, 117], fill=LIGHT_LINE)

    # hero
    hy = 124
    hero_box = [MARGIN, hy, W - MARGIN, hy + 172]
    d.rounded_rectangle(hero_box, radius=8, fill=NAVY_DEEP)
    scene_missiles(d, [MARGIN + 14, hy + 14, MARGIN + 430, hy + 158])
    badge(d, MARGIN + 30, hy + 30, HERO["num"])
    tx = MARGIN + 452
    tw2 = W - MARGIN - tx - 14
    d.text((tx, hy + 16), HERO["kicker"], font=F_KICKER, fill=GOLD)
    y = draw_text(d, tx, hy + 32, HERO["head"], F_HERO_HEAD,
                  (255, 255, 255), tw2, 32)
    draw_text(d, tx, y + 4, HERO["body"], F_HERO_BODY,
              (225, 230, 242), tw2, 15)

    # cards 3 x 2
    cy = hy + 184
    card_w = (CONTENT_W - 2 * 12) // 3
    card_h = 170
    for i, card in enumerate(CARDS):
        cx = MARGIN + (i % 3) * (card_w + 12)
        cyy = cy + (i // 3) * (card_h + 12)
        d.rounded_rectangle([cx, cyy, cx + card_w, cyy + card_h], radius=8,
                            fill=CARD_BG, outline=LIGHT_LINE, width=1)
        SCENES[card["scene"]](d, [cx + 8, cyy + 8, cx + card_w - 8, cyy + 66])
        badge(d, cx + 22, cyy + 22, card["num"])
        d.text((cx + 10, cyy + 72), card["kicker"], font=F_KICKER, fill=RED)
        y = draw_text(d, cx + 10, cyy + 86, card["head"], F_CARD_HEAD, INK,
                      card_w - 20, 16)
        draw_text(d, cx + 10, y + 2, card["body"], F_CARD_BODY, GREY,
                  card_w - 20, 12.5)

    # figures strip
    fy = cy + 2 * card_h + 24
    d.rectangle([MARGIN, fy, W - MARGIN, fy + 52], fill=NAVY)
    fw = CONTENT_W / len(FIGURES)
    for i, (num, cap) in enumerate(FIGURES):
        cx = MARGIN + i * fw
        nw = d.textlength(num, font=F_FIG_NUM)
        d.text((cx + (fw - nw) / 2, fy + 5), num, font=F_FIG_NUM,
               fill=(255, 255, 255))
        lines = wrap(d, cap, F_FIG_CAP, fw - 14)
        ly = fy + 34
        for line in lines[:2]:
            lw = d.textlength(line, font=F_FIG_CAP)
            d.text((cx + (fw - lw) / 2, ly), line, font=F_FIG_CAP,
                   fill=(200, 212, 235))
            ly += 11

    # briefs
    by = fy + 64
    d.text((MARGIN, by), "AROUND THE WORLD IN BRIEF", font=F_SECTION, fill=NAVY_DEEP)
    d.rectangle([MARGIN, by + 24, W - MARGIN, by + 25], fill=INK)
    cols = 3
    col_w = (CONTENT_W - (cols - 1) * 16) // cols
    per_col = (len(BRIEFS) + cols - 1) // cols
    for c in range(cols):
        x = MARGIN + c * (col_w + 16)
        y = by + 34
        for j in range(per_col):
            idx = c * per_col + j
            if idx >= len(BRIEFS):
                break
            place, text = BRIEFS[idx]
            num = 8 + idx
            badge(d, x + 10, y + 8, num, r=9)
            d.text((x + 26, y), place, font=F_BRIEF_B, fill=RED)
            y = draw_text(d, x + 26, y + 12, text, F_BRIEF, INK, col_w - 26, 11)
            y += 2

    # footer
    foot_y = H - 30
    d.rectangle([MARGIN, foot_y - 6, W - MARGIN, foot_y - 5], fill=LIGHT_LINE)
    foot = ("Every story happened or was first reported on 21 November 2026 and was checked "
            "against two or more sources: Reuters, AP, BBC, IMD, USGS, IANS. Drawn with PIL - no photographs.")
    draw_text(d, MARGIN, foot_y, foot, F_FOOT, GREY, CONTENT_W, 12)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

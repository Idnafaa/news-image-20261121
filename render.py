#!/usr/bin/env python3
"""Draw 'The World in One Day - 21 November 2026' as a broadsheet front page.

Everything is drawn with PIL primitives and DejaVu text. The output is a
1024x1024 PNG written next to this file as entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 243, 233)
INK = (28, 26, 24)
FAINT = (105, 100, 92)
RULE = (60, 56, 50)
RED = (168, 32, 28)
NAVY = (27, 48, 84)
TEAL = (18, 96, 96)
GOLD = (176, 124, 22)
SKY = (196, 216, 228)
FIELD = (206, 214, 176)
SEA = (140, 176, 196)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrap(draw, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def jet(draw, x, y, s, fill):
    draw.polygon([(x, y), (x + 3 * s, y + s), (x + s, y + s),
                  (x + s, y + 2 * s), (x - s, y + 2 * s), (x - s, y + s),
                  (x - 3 * s, y + s)], fill=fill)


def hero_scene(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY, outline=INK, width=2)
    # ground
    gy = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, gy, x1, y1], fill=FIELD)
    # border line (Poland west, Ukraine east)
    bx = x0 + int((x1 - x0) * 0.52)
    for yy in range(y0 + 6, y1 - 6, 12):
        draw.line([bx, yy, bx, yy + 7], fill=INK, width=2)
    draw.text((x0 + 10, y0 + 8), "POLAND", font=font(SANS_B, 15), fill=NAVY)
    draw.text((bx + 10, y0 + 8), "UKRAINE", font=font(SANS_B, 15), fill=RED)
    draw.text((x0 + 10, y1 - 24), "Nowy Lipowiec  ~50 km from border",
              font=font(SANS, 12), fill=INK)
    # missile arcs coming from the east
    for k, (sx, sy, ex, ey) in enumerate([
            (x1 - 30, y0 + 40, bx - 90, gy + 30),
            (x1 - 20, y0 + 90, bx - 40, gy + 55)]):
        pts = []
        for t in range(0, 21):
            f = t / 20
            px = sx + (ex - sx) * f
            py = sy + (ey - sy) * f - 70 * 4 * f * (1 - f)
            pts.append((px, py))
        draw.line(pts, fill=RED, width=3)
        draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=RED)
        star(draw, ex, ey - 14, 10, GOLD)
    # drone dot
    dx, dy = bx - 150, y0 + 60
    draw.ellipse([dx - 6, dy - 4, dx + 6, dy + 4], fill=INK)
    draw.line([dx - 14, dy, dx + 14, dy], fill=INK, width=2)
    draw.text((dx - 26, dy + 8), "drone", font=font(SANS, 11), fill=INK)
    # jets scrambled
    jet(draw, x0 + 90, y0 + 55, 7, NAVY)
    jet(draw, x0 + 150, y0 + 80, 6, NAVY)
    draw.text((x0 + 60, y0 + 95), "NATO jets up", font=font(SANS, 11), fill=NAVY)
    # village houses
    for hx in (x0 + 40, x0 + 95, x0 + 150):
        draw.rectangle([hx, gy + 28, hx + 34, gy + 52], fill=(255, 255, 255),
                       outline=INK, width=1)
        draw.polygon([(hx - 3, gy + 28), (hx + 17, gy + 12), (hx + 37, gy + 28)],
                     fill=RED)


def icon_quake(draw, cx, cy):
    draw.line([cx - 26, cy + 10, cx - 10, cy - 14, cx + 2, cy + 16,
               cx + 12, cy - 8, cx + 26, cy + 10], fill=RED, width=4)


def icon_chart(draw, cx, cy):
    draw.line([cx - 28, cy - 18, cx - 10, cy - 2, cx + 4, cy - 10,
               cx + 28, cy + 18], fill=RED, width=4)
    draw.polygon([(cx + 28, cy + 18), (cx + 14, cy + 16), (cx + 26, cy + 6)],
                 fill=RED)


def icon_globe(draw, cx, cy):
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=TEAL, width=3)
    draw.arc([cx - 10, cy - 22, cx + 10, cy + 22], 90, 270, fill=TEAL, width=2)
    draw.arc([cx - 10, cy - 22, cx + 10, cy + 22], 270, 90, fill=TEAL, width=2)
    draw.line([cx - 22, cy, cx + 22, cy], fill=TEAL, width=2)


def icon_handshake(draw, cx, cy):
    draw.rectangle([cx - 28, cy - 8, cx - 4, cy + 8], fill=NAVY)
    draw.rectangle([cx + 4, cy - 8, cx + 28, cy + 8], fill=GOLD)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=INK)


def icon_shield(draw, cx, cy):
    draw.polygon([(cx - 20, cy - 20), (cx + 20, cy - 20), (cx + 20, cy + 2),
                  (cx, cy + 24), (cx - 20, cy + 2)], outline=NAVY, width=3)
    star(draw, cx, cy - 4, 9, RED)


def icon_crowd(draw, cx, cy):
    for dx in (-20, 0, 20):
        draw.ellipse([cx + dx - 7, cy - 16, cx + dx + 7, cy - 2], fill=INK)
        draw.rectangle([cx + dx - 8, cy, cx + dx + 8, cy + 18], fill=INK)


CARDS = [
    ("ANTALYA, TURKIYE", "Climate talks run into overtime",
     "COP31 missed its Friday close. A France-Panama bloc demands fossil-fuel "
     "words and fair finance; the draft dropped them.", icon_globe, TEAL),
    ("NEW YORK", "Wall Street slides into correction",
     "S&P 500 -3.7% Friday, 7th loss in a row. Nvidia -14%, Anthropic fizzled "
     "after its record IPO. Nasdaq negative for 2026.", icon_chart, RED),
    ("JUNIN, PERU", "6.8 quake sends Lima outdoors",
     "Deep tremor at 01:09 UTC Saturday, felt 320 km away in the capital. "
     "No casualties reported; no tsunami threat.", icon_quake, RED),
    ("BRUSSELS", "UK and EU seal post-Brexit reset",
     "100,000 youth visas each way for up to 3 years, most food checks "
     "scrapped, UK rejoins Erasmus+ from 2027.", icon_handshake, NAVY),
    ("COPENHAGEN", "Denmark expels Russian attache",
     "PET says Moscow plotted to kill rapper Kyivstoner; gunmen stopped "
     "5 minutes before the show. Russia denies it.", icon_shield, NAVY),
    ("PARIS", "France marches again over living costs",
     "Acte VI Saturday: unions, students and Gilets jaunes, 8 years on. "
     "70,000 police deployed nationwide.", icon_crowd, INK),
]

BRIEFS_LEFT = [
    ("KRYVYI RIH", "Double-tap kills boy, 7, and paramedic; 42 hurt"),
    ("KYIV / LVIV", "80+ missiles, 400+ drones; bridges hit, power cut"),
    ("HORMUZ", "Tanker ablaze 8 nm north of Khasab; crew safe"),
    ("WASHINGTON", "Trump threatens 'tremendous tax' on data centres abroad"),
    ("NEW YORK", "Mamdani: Rikers Island to close by 2032, 4 borough jails"),
    ("LOS ANGELES", "Palisades arsonist guilty at retrial; 12 died in 2025 fire"),
    ("VIRGINIA", "Child 0-4 is state's first measles death of 2026; 220 cases"),
    ("FLORIDA", "Space Coast floods again; St Johns breaks 1953 record"),
    ("ODISHA", "Cyclone Akvan ashore at Gopalpur; 300,000 evacuated"),
    ("MUMBAI", "Foreign buying hits record Rs 1.22 lakh crore in November"),
    ("JAIPUR", "Congress routs BJP 3,701 to 2,181 in panchayat polls"),
    ("KATHMANDU", "PM Balen heads to Delhi Sunday, first foreign visit"),
    ("WELLINGTON", "KL Rahul 100: first Indian opener with tons in all SENA lands"),
]

BRIEFS_RIGHT = [
    ("MUNICH", "Kane out for months; Bayern held 1-1 by Koln"),
    ("RAWALPINDI", "Pakistan beat Sri Lanka by 8 wickets, take series 1-0"),
    ("ABU DHABI", "UAE Bulls lift T10 trophy, beat Yas Lions by 24 runs"),
    ("TURIN", "Medvedev downs Tiafoe 6-3 6-4 at ATP Finals"),
    ("BRUSSELS", "EU adopts EUR 1bn military aid package for Ukraine"),
    ("VIENNA", "Foreign ministry website hacked; staff details viewed"),
    ("LONDON", "Banks flag vendor cyberattack; card networks unaffected"),
    ("LOS ANGELES", "Hyundai unveils 8th-generation Elantra hybrid"),
    ("KUALA LUMPUR", "India U17s draw 0-0, qualify for AFC Asian Cup 2027"),
    ("BHOPAL", "India women beat Malaysia 4-1 in hockey opener"),
    ("CINCINNATI", "Fiona the hippo mourned; Senate honours her memory"),
    ("WASHINGTON", "US sanctions 4 Iranians over oil revenues (OFAC)"),
    ("FRANKFURT", "Boone, Brunnermeier in frame for ECB board seat"),
]

NUMBERS = [
    ("6.8", "Peru quake"),
    ("-3.7%", "S&P 500 Friday"),
    ("100,000", "youth visas"),
    ("42", "hurt, Kryvyi Rih"),
    ("70,000", "police, France"),
    ("Rs1.22L cr", "India inflows"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    centered(d, W // 2, 14, "The World in One Day", font(SERIF_B, 44), INK)
    centered(d, W // 2, 64, "Saturday 21 November 2026  -  the day's news on one page",
             font(SANS_B, 17), RED)
    d.line([24, 92, W - 24, 92], fill=RULE, width=3)
    d.line([24, 97, W - 24, 97], fill=RULE, width=1)

    # hero
    d.text((24, 104), "WARSAW  -  NATO'S EASTERN EDGE",
           font=font(SANS_B, 15), fill=FAINT)
    y = draw_wrap(d, 24, 124, "Russian missiles fall inside Poland; NATO scrambles",
                  font(SERIF_B, 30), INK, 600, 34)
    y = draw_wrap(d, 24, y + 2,
                  "Two Kh-101 cruise missiles and a jet drone came down 30-50 km "
                  "inside Poland during a huge overnight barrage on Ukraine. "
                  "PM Tusk calls it an 'intentional provocation'; nobody was hurt. "
                  "Poland asks NATO for AWACS and F-35s; Rutte due in Warsaw today.",
                  font(SANS, 14), INK, 600, 18)
    hero_scene(d, (644, 104, W - 24, 316))

    # cards 3 x 2
    top = 322
    cw = (W - 48 - 16) // 3
    ch = 140
    for i, (place, head, body, icon, accent) in enumerate(CARDS):
        cx = 24 + (i % 3) * (cw + 8)
        cy = top + (i // 3) * (ch + 8)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255),
                    outline=RULE, width=1)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=accent)
        icon(d, cx + 34, cy + 40)
        d.text((cx + 68, cy + 14), place, font=font(SANS_B, 12), fill=FAINT)
        hy = draw_wrap(d, cx + 68, cy + 30, head, font(SERIF_B, 16), INK,
                       cw - 78, 19)
        draw_wrap(d, cx + 12, max(hy + 2, cy + 78), body, font(SANS, 12),
                  INK, cw - 24, 15)

    # numbers strip
    ny = top + 2 * ch + 20
    d.rectangle([24, ny, W - 24, ny + 58], fill=NAVY)
    seg = (W - 48) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = 24 + i * seg + seg // 2
        centered(d, cx, ny + 6, num, font(SANS_B, 20), (255, 255, 255))
        centered(d, cx, ny + 32, lab, font(SANS, 11), (200, 214, 232))
        if i:
            d.line([24 + i * seg, ny + 8, 24 + i * seg, ny + 50],
                   fill=(90, 115, 155), width=1)

    # briefs
    by = ny + 70
    d.text((24, by), "AROUND THE WORLD IN BRIEF", font=font(SANS_B, 15), fill=RED)
    by += 24
    col_w = (W - 48 - 20) // 2
    for col, briefs in enumerate((BRIEFS_LEFT, BRIEFS_RIGHT)):
        x = 24 + col * (col_w + 20)
        yy = by
        for place, text in briefs:
            d.ellipse([x, yy + 5, x + 7, yy + 12], fill=RED)
            d.text((x + 14, yy), place, font=font(SANS_B, 11), fill=NAVY)
            pw = d.textlength(place + "  ", font=font(SANS_B, 11))
            lines = wrap(d, text, font(SANS, 12), col_w - 14 - pw)
            d.text((x + 14 + pw, yy - 1), lines[0], font=font(SANS, 12), fill=INK)
            yy += 14
            for extra in lines[1:]:
                d.text((x + 14, yy - 1), extra, font=font(SANS, 12), fill=INK)
                yy += 14
            yy += 2

    # footer
    fy = H - 44
    d.line([24, fy, W - 24, fy], fill=RULE, width=2)
    centered(d, W // 2, fy + 8,
             "All events above happened or were first reported on Saturday "
             "21 November 2026 (some late Friday UTC).  Sources: Reuters, AP, "
             "AFP, BBC, UN News, IMD, UKMTO, VDH.",
             font(SANS, 11), FAINT)
    centered(d, W // 2, fy + 24, "World Television Day  -  21 November",
             font(SANS, 11), FAINT)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

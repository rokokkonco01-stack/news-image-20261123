#!/usr/bin/env python3
"""Sum up Monday 23 November 2026's world news in one image.

Deterministic newspaper front-page generator. Writes /output/entry.png.
No network, no randomness, no wall-clock — two runs produce identical bytes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REG = os.path.join(HERE, "fonts", "Carlito-Regular.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "Carlito-Bold.ttf")
FONT_MAST = os.path.join(HERE, "fonts", "Poppins-Bold.ttf")

W, H = 1024, 1024
PAPER = (246, 241, 232)
INK = (18, 18, 20)
RULE = (18, 18, 20)
GRAY = (92, 90, 86)
RED = (178, 34, 34)
NAVY = (30, 46, 84)
GREEN = (40, 94, 62)
GOLD = (170, 120, 20)
PURPLE = (84, 46, 116)
TEAL = (20, 100, 110)


def font(size, path=FONT_REG):
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


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def hline(draw, y, x0, x1, color=RULE, width=2):
    draw.rectangle([x0, y, x1, y + width], fill=color)


# ---- icons (all drawn deterministically) ----------------------------------
def draw_drone(d, x, y, s):
    for i in range(3):
        yy = y + s * 0.62 + i * s * 0.10
        d.line([x + s * 0.05, yy, x + s * 0.95, yy], fill=(70, 100, 120), width=2)
    d.polygon([(x, y + s * 0.25), (x + s * 0.85, y + s * 0.15),
               (x + s, y + s * 0.55), (x + s * 0.15, y + s * 0.65)], fill=(30, 34, 40))
    d.line([x + s * 0.55, y + s * 0.15, x + s * 0.55, y], fill=(30, 34, 40), width=3)
    d.line([x + s * 0.40, y + s * 0.05, x + s * 0.70, y + s * 0.05], fill=(30, 34, 40), width=2)


def draw_ship(d, x, y, s, fill=(22, 26, 32)):
    d.polygon([(x, y + s), (x + s * 0.18, y + s * 0.62), (x + s * 0.5, y + s * 0.66),
               (x + s * 0.9, y + s * 0.70), (x + s, y + s)], fill=fill)
    d.polygon([(x + s * 0.30, y + s * 0.62), (x + s * 0.45, y + s * 0.20),
               (x + s * 0.58, y + s * 0.62)], fill=fill)


def draw_explosion(d, cx, cy, r, color=(200, 60, 40)):
    pts = []
    for i in range(16):
        ang = math.pi * 2 * i / 16
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def draw_satellite(d, x, y, s):
    body = (40, 44, 52)
    d.rectangle([x + s * 0.35, y + s * 0.2, x + s * 0.65, y + s * 0.6], fill=body)
    d.rectangle([x, y + s * 0.28, x + s * 0.35, y + s * 0.52], fill=(40, 80, 150))
    d.rectangle([x + s * 0.65, y + s * 0.28, x + s, y + s * 0.52], fill=(40, 80, 150))
    for px in (x + s * 0.06, x + s * 0.14, x + s * 0.22):
        d.line([px, y + s * 0.28, px, y + s * 0.52], fill=(20, 40, 80), width=2)
    for px in (x + s * 0.78, x + s * 0.86, x + s * 0.94):
        d.line([px, y + s * 0.28, px, y + s * 0.52], fill=(20, 40, 80), width=2)
    d.ellipse([x + s * 0.38, y, x + s * 0.62, y + s * 0.24], outline=body, width=3)
    cx, cy = x + s * 0.5, y + s * 0.78
    d.circle((cx, cy), int(s * 0.14), outline=(150, 60, 30), width=3)
    for i in range(3):
        ang = -math.pi / 2 + i * math.pi * 2 / 3
        d.line([cx, cy, cx + math.cos(ang) * s * 0.13, cy + math.sin(ang) * s * 0.13],
               fill=(150, 60, 30), width=2)


def draw_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=(30, 80, 50), width=4)
    d.ellipse([x + s * 0.25, y, x + s * 0.75, y + s], outline=(30, 80, 50), width=2)
    d.ellipse([x, y + s * 0.25, x + s, y + s * 0.75], outline=(30, 80, 50), width=2)
    d.line([x + s * 0.1, y + s * 0.5, x + s * 0.9, y + s * 0.5], fill=(30, 80, 50), width=2)
    tx = x + s * 0.72
    d.rectangle([tx - 4, y + s * 0.15, tx + 4, y + s * 0.65], fill=(180, 50, 50))
    d.circle((tx, y + s * 0.72), 8, fill=(180, 50, 50))


def draw_chart(d, x, y, s, color=GOLD):
    pts = [(x + s * 0.05, y + s * 0.3), (x + s * 0.25, y + s * 0.45),
           (x + s * 0.45, y + s * 0.35), (x + s * 0.65, y + s * 0.68),
           (x + s * 0.95, y + s * 0.92)]
    d.line(pts, fill=color, width=5, joint="curve")
    d.line([x, y + s, x + s, y + s], fill=(120, 120, 120), width=2)
    d.line([x, y, x, y + s], fill=(120, 120, 120), width=2)


def draw_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], outline=(30, 30, 30), width=3)
    d.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8],
                outline=(30, 30, 30), width=2)
    cx, cy = x + s / 2, y + s / 2
    d.line([cx, y + s * 0.2, cx, y + s * 0.8], fill=(30, 30, 30), width=2)
    d.line([x + s * 0.2, cy, x + s * 0.8, cy], fill=(30, 30, 30), width=2)
    for i in range(4):
        px = x + s * 0.3 + i * s * 0.13
        d.line([px, y, px, y + s * 0.2], fill=(30, 30, 30), width=2)
        d.line([px, y + s * 0.8, px, y + s], fill=(30, 30, 30), width=2)


def draw_rocket(d, x, y, s):
    d.polygon([(x + s * 0.5, y), (x + s * 0.68, y + s * 0.35),
               (x + s * 0.32, y + s * 0.35)], fill=(80, 80, 90))
    d.rectangle([x + s * 0.32, y + s * 0.35, x + s * 0.68, y + s * 0.7], fill=(90, 90, 100))
    d.polygon([(x + s * 0.32, y + s * 0.7), (x + s * 0.42, y + s * 0.9),
               (x + s * 0.5, y + s * 0.7)], fill=(150, 50, 40))
    d.polygon([(x + s * 0.68, y + s * 0.7), (x + s * 0.58, y + s * 0.9),
               (x + s * 0.5, y + s * 0.7)], fill=(150, 50, 40))
    d.polygon([(x + s * 0.44, y + s * 0.9), (x + s * 0.56, y + s * 0.9),
               (x + s * 0.5, y + s * 1.0)], fill=(230, 150, 40))


def draw_capitol(d, x, y, s):
    d.rectangle([x + s * 0.15, y + s * 0.7, x + s * 0.85, y + s * 0.85], fill=(60, 60, 66))
    d.rectangle([x + s * 0.3, y + s * 0.55, x + s * 0.7, y + s * 0.7], fill=(70, 70, 76))
    d.arc([x + s * 0.28, y + s * 0.25, x + s * 0.72, y + s * 0.75], 180, 360,
          fill=(70, 70, 76), width=8)
    d.line([x + s * 0.5, y + s * 0.05, x + s * 0.5, y + s * 0.15], fill=(70, 70, 76), width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(80, FONT_MAST)
    f_head = font(60, FONT_BOLD)
    f_kicker = font(22, FONT_BOLD)
    f_sub = font(24, FONT_REG)
    f_colhead = font(30, FONT_BOLD)
    f_dek = font(19, FONT_REG)
    f_cap = font(16, FONT_REG)
    f_date = font(19, FONT_BOLD)
    f_small = font(17, FONT_REG)

    # ---- masthead ---------------------------------------------------------
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    text(d, ((W - tw) / 2, 22), title, f_mast, INK)
    daterow = "MONDAY 23 NOVEMBER 2026"
    dw = d.textlength(daterow, font=f_date)
    text(d, ((W - dw) / 2, 112), daterow, f_date, GRAY)
    ed = "DAILY WORLD EDITION \u00b7 FINAL"
    ew = d.textlength(ed, font=f_small)
    text(d, ((W - ew) / 2, 138), ed, f_small, GRAY)
    hline(d, 170, 32, W - 32, RULE, 4)
    hline(d, 178, 32, W - 32, RULE, 1)

    # ---- lead banner ------------------------------------------------------
    y = 194
    text(d, (32, y), "WAR IN EUROPE", f_kicker, RED)
    y += 30
    text(d, (32, y), "UKRAINE STRIKES", f_head, INK)
    text(d, (32, y + 70), "RUSSIAN WARSHIPS", f_head, INK)
    y += 70 + 48
    sub = ("Naval drones hit two vessels off Libya; the Kremlin accuses Kyiv of "
           "\u201cterrorist activity\u201d after a Baltic cargo-ship strike")
    for ln in wrap(d, sub, f_sub, W - 200):
        text(d, (32, y), ln, f_sub, GRAY)
        y += 30

    # ---- illustration -----------------------------------------------------
    iy = y + 8
    ih = 118
    d.rectangle([32, iy, W - 32, iy + ih], fill=(24, 42, 60))
    for i in range(4):
        yy = iy + ih - 16 - i * 22
        d.line([32, yy, W - 32, yy], fill=(16, 30, 46), width=3)
    draw_ship(d, 680, iy + 8, 190)
    draw_explosion(d, 775, iy + 40, 26)
    draw_drone(d, 100, iy + 30, 90)
    d.line([190, iy + 62, 290, iy + 62], fill=(120, 160, 190), width=3)
    text(d, (32, iy + ih + 10), "Illustration: Ukrainian naval drones closing on a Russian vessel", f_cap, GRAY)
    y = iy + ih + 40
    hline(d, y, 32, W - 32, RULE, 2)
    y += 14

    # ---- three columns ----------------------------------------------------
    col_w = (W - 64 - 2 * 24) // 3
    x0, x1, x2 = 32, 32 + col_w + 24, 32 + 2 * (col_w + 24)

    def story(x, ystart, kicker, kcolor, headline, dek, icon_fn):
        yy = ystart
        text(d, (x, yy), kicker, f_kicker, kcolor)
        yy += 28
        for ln in wrap(d, headline, f_colhead, col_w - 8):
            text(d, (x, yy), ln, f_colhead, INK)
            yy += 38
        icon_fn(d, x + 2, yy + 2, 40)
        yy += 48
        for ln in wrap(d, dek, f_dek, col_w - 8):
            text(d, (x, yy), ln, f_dek, GRAY)
            yy += 23
        return yy + 6

    cy1 = story(x0, y, "NUCLEAR THREAT", NAVY,
                "Russia readies nuclear satellite",
                "NATO warns of a weapon in orbit.", draw_satellite)
    cy1 = story(x0, cy1, "CLIMATE", GREEN,
                "COP31 ends with no deal",
                "Fourth failed summit in a row.", draw_globe)

    cy2 = story(x1, y, "MARKETS", GOLD,
                "Stocks tumble on AI bubble fears",
                "$44bn cyber deal rattles investors.", draw_chart)
    cy2 = story(x1, cy2, "TECHNOLOGY", TEAL,
                "Nvidia's Huang reinstated",
                "Board ends a week of turmoil.", draw_chip)

    cy3 = story(x2, y, "UNITED STATES", RED,
                "Democrats sweep the House",
                "Largest margin in 50 years.", draw_capitol)
    cy3 = story(x2, cy3, "SPACE", PURPLE,
                "Probe enters Mercury orbit",
                "First arrival in a decade.", draw_rocket)

    bottom = max(cy1, cy2, cy3)
    d.line([x0 + col_w + 12, y - 6, x0 + col_w + 12, bottom], fill=(140, 134, 124), width=1)
    d.line([x1 + col_w + 12, y - 6, x1 + col_w + 12, bottom], fill=(140, 134, 124), width=1)

    foot_y = bottom + 12
    hline(d, foot_y, 32, W - 32, RULE, 2)
    text(d, (32, foot_y + 10), "Compiled for make.fun \u2014 one image, the day\u2019s world news.", f_small, GRAY)

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    os.chmod(out_dir, 0o755)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    os.chmod(path, 0o644)
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()

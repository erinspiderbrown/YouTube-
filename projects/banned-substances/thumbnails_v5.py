"""Thumbnails v5: the actual drugs only (user, 9 Nov 2026: no Gatlin, no Marion Jones; drugs like the original, but original).
Real photos (Wikimedia Commons, credits in thumbnail_credits.md). Every photo is only downscaled.
E: white circle grid ("every X explained" 5.5M layout).  F: dark neon tiles (the channel's own neon look).
python3 -I thumbnails_v5.py SCRATCH_DIR OUT_DIR
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
S = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
RED = (235, 30, 40); WHITE = (255, 255, 255); BLACK = (0, 0, 0)

DRUGS = [  # (file, crop box, label, colour)
    ("src/Winstrol tablets.JPG", (40, 120, 1090, 1170), "STANOZOLOL", (0, 170, 255)),
    ("drugs/d0.jpg", (190, 40, 1110, 960), "EPO", (170, 60, 255)),
    ("src/Depo-testosterone crop.jpg", (0, 350, 1642, 1992), "TESTOSTERONE", (240, 40, 50)),
    ("drugs/d2.jpg", (0, 210, 1280, 1490), "HGH", (255, 170, 0)),
    ("leaf/leaf_1.jpg", (93, 0, 1234, 1141), "WEED", (40, 200, 70)),
    ("drugs/d8.jpg", (160, 0, 1120, 960), "MELDONIUM", (255, 80, 170)),
    ("drugs/d3.jpg", (213, 0, 1066, 853), "CAPTAGON", (0, 200, 200)),
    ("drugs/d7.jpg", (40, 0, 1000, 960), "DIURETICS", (255, 120, 0)),
    ("drugs/d5.jpg", (0, 99, 1280, 1379), "ASTHMA PUMP", (30, 90, 255)),
    ("drugs/d4.jpg", (340, 560, 970, 1190), "RAT POISON", (150, 150, 150)),
]


def tile(f, box, D):
    im = Image.open(f"{S}/{f}").convert("RGB").crop(box)
    im = ImageOps.fit(im, (D, D), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 35, 3))
    im = ImageEnhance.Contrast(im).enhance(1.06); im = ImageEnhance.Color(im).enhance(1.1)
    return im


def mask(D, kind, ss=4):
    m = Image.new("L", (D * ss, D * ss), 0); d = ImageDraw.Draw(m)
    if kind == "circle": d.ellipse([0, 0, D * ss - 1, D * ss - 1], fill=255)
    else: d.rounded_rectangle([0, 0, D * ss - 1, D * ss - 1], radius=int(D * 0.14) * ss, fill=255)
    return m.resize((D, D), Image.LANCZOS)


def title(im, y, size, colour_rest, font=INTER, parts=None):
    d = ImageDraw.Draw(im); ft = ImageFont.truetype(font, size)
    parts = parts or [("EVERY ", colour_rest), ("BANNED", RED), (" DRUG IN TRACK", colour_rest)]
    tw = sum(d.textlength(t, font=ft) for t, _ in parts); x = (W - tw) / 2
    for t, c in parts: d.text((x, y), t, font=ft, fill=c + (255,)); x += d.textlength(t, font=ft)


def layout(im, kind, D, ring, label_col, font, fsize, y1, dy, glow=False):
    d = ImageDraw.Draw(im); fl = ImageFont.truetype(font, fsize)
    xs = [W * (i + 0.5) / 5 for i in range(5)]
    for i, (f, box, lab, col) in enumerate(DRUGS):
        cx, cy = int(xs[i % 5]), y1 + (i // 5) * dy
        R = D // 2 + ring; om = mask(2 * R, kind)
        if glow:
            g = Image.new("RGBA", (2 * R + 120, 2 * R + 120), (0, 0, 0, 0)); g.paste(col + (255,), (60, 60), om)
            g = g.filter(ImageFilter.GaussianBlur(26)); im.alpha_composite(g, (cx - R - 60, cy - R - 60))
        else:
            sh = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 80), (20, 20), om)
            im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (cx - R - 20 + 4, cy - R - 20 + 8))
        rr = Image.new("RGBA", (2 * R, 2 * R), col + (255,)); rr.putalpha(om); im.alpha_composite(rr, (cx - R, cy - R))
        t = tile(f, box, D).convert("RGBA"); t.putalpha(mask(D, kind)); im.alpha_composite(t, (cx - D // 2, cy - D // 2))
        d.text((cx, cy + R + fsize * 0.85), lab, font=fl, fill=label_col + (255,), anchor="mm")


def save(im, name):
    rgb = im.convert("RGB")
    rgb.save(f"{OUT}/{name}_HD.jpg", quality=95, subsampling=0)
    rgb.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95, subsampling=0, optimize=True)


def e_white():
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    title(im, 34, 112, BLACK)
    layout(im, "circle", 285, 12, BLACK, INTER, 42, 360, 425)
    save(im, "E_drugs_circle_grid")


def f_dark():
    im = Image.new("RGBA", (W, H), (10, 10, 14, 255))
    bg = Image.new("L", (W, H), 0); ImageDraw.Draw(bg).ellipse([W * 0.1, -H * 0.3, W * 0.9, H * 0.9], fill=110)
    red = Image.new("RGBA", (W, H), (120, 0, 10, 255)); red.putalpha(bg.filter(ImageFilter.GaussianBlur(200)))
    im.alpha_composite(red)
    title(im, 26, 118, WHITE, font=ANTON, parts=[("EVERY ", WHITE), ("BANNED", RED), (" DRUG IN TRACK", WHITE)])
    layout(im, "rounded", 280, 8, WHITE, ANTON, 50, 370, 420, glow=True)
    save(im, "F_drugs_neon_tiles")


e_white(); f_dark(); print("ok")

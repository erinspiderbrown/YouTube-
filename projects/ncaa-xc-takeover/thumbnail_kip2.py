"""Kipchoge thumbnails v3, built from what the niche's breakout thumbnails do:
one big sharp face on a blurred natural background, 1-3 huge words, news-style bottom banner, a red circle or strike for contrast.
Face: 1080p frame from youthrunnermag's 2024 Mountain Regional interview (https://youtu.be/gHvSTQ1nQ0A).
Race background: Makosh Official's 2024 Mountain Regional race video (https://youtu.be/_nQhvRsfULo), heavily blurred.
Run: python3 -I projects/ncaa-xc-takeover/thumbnail_kip2.py OUTDIR"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
FI = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"
YEL, RED, WHITE, BLACK = (255, 214, 0), (230, 28, 36), (255, 255, 255), (0, 0, 0)

def clean(im):
    import cv2
    a = np.array(im.split()[-1]); m = (a > 110).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8); keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    m = cv2.morphologyEx((lab == keep).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    out = im.copy(); out.putalpha(Image.fromarray(np.where(m > 0, a, 0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))); return out

def person(height):
    cut = clean(Image.open(f"{SCR}/photos/cut_kip.png").convert("RGBA"))
    rgb = cut.convert("RGB"); a = cut.split()[-1]
    rgb = ImageEnhance.Contrast(rgb).enhance(1.15); rgb = ImageEnhance.Color(rgb).enhance(1.15)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.08).filter(ImageFilter.UnsharpMask(3, 150, 2)); rgb.putalpha(a)
    rgb = rgb.crop(rgb.split()[-1].getbbox()); s = height / rgb.height
    return rgb.resize((int(rgb.width * s), height), Image.LANCZOS)

def blurred(path, zoom=1.0, cx=0.5, cy=0.5, blur=16, bright=0.7):
    im = Image.open(path).convert("RGB"); w, h = im.size
    tw, th = w / zoom, h / zoom; x0 = (w - tw) * cx; y0 = (h - th) * cy
    im = im.crop((int(x0), int(y0), int(x0 + tw), int(y0 + th)))
    im = ImageOps.fit(im, (W, H)).filter(ImageFilter.GaussianBlur(blur))
    im = ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(bright)).enhance(1.2)
    return im.convert("RGBA")

def side_shade(im, strength=210, width=1150, side="left"):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for i in range(W):
        f = i if side == "left" else W - i
        d.line([(i, 0), (i, H)], fill=(0, 0, 0, int(strength * max(0, 1 - f / width) ** 1.3)))
    im.alpha_composite(sh)

def place(im, cut, x, y, glow=(255, 255, 255)):
    a = cut.split()[-1]
    for col, grow, blur, n in ((glow, 9, 5, 2), (BLACK, 31, 30, 1)):
        g = Image.new("RGBA", cut.size, col + (0,)); g.putalpha(a.filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(blur)))
        for _ in range(n): im.alpha_composite(g, (x, y))
    im.alpha_composite(cut, (x, y))

def words(im, xy, s, font, fill, stroke=0, anchor="la", shadow=18, rot=0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,), anchor=anchor)
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, center=xy)
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.7))))
        im.alpha_composite(sh, (6, 12))
    im.alpha_composite(lay)

def save(im, name):
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95)

cut = person(1110)
cx, cy = W - cut.width + 120, H - cut.height + 8

# K1 · news banner over his real race (the breakout format: face + bottom banner + red tag)
im = blurred(f"{SCR}/kipf/race_128.png", zoom=1.35, cx=0.2, cy=0.6, blur=14, bright=0.75); side_shade(im, 170, 1100)
place(im, cut, cx, cy)
d = ImageDraw.Draw(im)
d.rectangle([0, 805, W, 1015], fill=WHITE + (255,))
words(im, (W // 2, 910), "HE'S 28… AND A FRESHMAN.", ImageFont.truetype(ANTON, 160), BLACK, anchor="mm", shadow=0)
d.rectangle([60, 725, 540, 805], fill=RED + (255,))
words(im, (300, 765), "TEXAS TECH · 2024", ImageFont.truetype(ANTON, 54), WHITE, anchor="mm", shadow=0)
words(im, (60, 40), "LEGAL?", ImageFont.truetype(FI, 230), YEL, stroke=10)
save(im, "K1_news-banner")

# K2 · 18 vs 28 (instant age contrast)
im = blurred(f"{SCR}/kipf/f_13.2.png", zoom=1.0, blur=18, bright=0.6); side_shade(im, 220, 1150)
place(im, cut, cx, cy)
A = ImageFont.truetype(ANTON, 330)
words(im, (70, 10), "18", A, (200, 200, 200), stroke=6)
d = ImageDraw.Draw(im); d.line([(55, 330), (420, 70)], fill=RED + (255,), width=34)
words(im, (420, 10), "28", A, YEL, stroke=8)
d.ellipse([395, 20, 805, 420], outline=RED + (255,), width=18)
words(im, (70, 470), "COLLEGE", ImageFont.truetype(ANTON, 200), WHITE, stroke=6)
words(im, (70, 700), "FRESHMAN", ImageFont.truetype(ANTON, 200), WHITE, stroke=6)
save(im, "K2_18-vs-28")

# K3 · one huge word + age pill (Coach Rob / "TERRIBLE!" style)
im = blurred(f"{SCR}/kipf/race_130.png", zoom=1.5, cx=0.15, cy=0.6, blur=16, bright=0.8); side_shade(im, 190, 1150)
place(im, cut, cx, cy)
words(im, (60, 150), "FRESHMAN?!", ImageFont.truetype(FI, 168), WHITE, stroke=9, rot=4)
d = ImageDraw.Draw(im)
d.rounded_rectangle([80, 430, 640, 600], 30, fill=YEL + (255,), outline=BLACK + (255,), width=8)
words(im, (360, 515), "AGE: 28", ImageFont.truetype(ANTON, 120), BLACK, anchor="mm", shadow=0)
save(im, "K3_freshman-age-28")
print("done")

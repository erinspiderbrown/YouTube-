"""Thumbnail D v2: "28-YEAR-OLD FRESHMAN" redesign.
Photo: 1080p frame of Solomon Kipchoge (Texas Tech beanie) from youthrunnermag's 2024 Mountain Regional interview
(https://youtu.be/gHvSTQ1nQ0A, Nov 2024, his 28-year-old freshman season), cut out with rembg.
Run: python3 -I projects/ncaa-xc-takeover/thumbnail_kip.py OUTDIR"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FI = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
YEL, RED, WHITE = (255, 214, 0), (226, 24, 36), (255, 255, 255)

def cutout(path):
    cache = f"{SCR}/photos/cut_kip.png"
    if not os.path.exists(cache):
        from rembg import remove, new_session
        im = Image.open(path).convert("RGB")
        remove(im, session=new_session("u2net_human_seg")).save(cache)
    return Image.open(cache).convert("RGBA")

def clean(im):
    """keep only the person: threshold the matte and keep its largest connected piece"""
    import cv2
    a = np.array(im.split()[-1])
    m = (a > 110).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    m = (lab == keep).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    a = np.where(m > 0, a, 0).astype(np.uint8)
    out = im.copy(); out.putalpha(Image.fromarray(a).filter(ImageFilter.GaussianBlur(1.2))); return out

def pop(im):
    rgb = im.convert("RGB"); a = im.split()[-1]
    rgb = ImageEnhance.Contrast(rgb).enhance(1.18); rgb = ImageEnhance.Color(rgb).enhance(1.2)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06).filter(ImageFilter.UnsharpMask(3, 140, 2))
    rgb.putalpha(a); return rgb

def radial_bg(c_in, c_out, cx=0.68, cy=0.45):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x / W - cx) * 1.6) ** 2 + (y / H - cy) ** 2); k = np.clip(r / 0.85, 0, 1)[..., None]
    a = np.array(c_in, np.float32) * (1 - k) + np.array(c_out, np.float32) * k
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")

def stroke_text(im, xy, s, font, fill, stroke=10, shadow=True, anchor="la"):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255), anchor=anchor)
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(18)).point(lambda v: min(255, int(v * 1.6))))
        im.alpha_composite(sh, (8, 14))
    im.alpha_composite(lay)

def rim(im, cut, x, y, col, blur, times=1, grow=11):
    a = cut.split()[-1].filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(blur))
    g = Image.new("RGBA", cut.size, col + (0,)); g.putalpha(a)
    for _ in range(times): im.alpha_composite(g, (x, y))

def arrow(im, p0, p1, col=RED, w=26):
    d = ImageDraw.Draw(im); d.line([p0, p1], fill=col + (255,), width=w)
    import math
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); L = 70
    pts = [p1, (p1[0] - L * math.cos(ang - 0.5), p1[1] - L * math.sin(ang - 0.5)), (p1[0] - L * math.cos(ang + 0.5), p1[1] - L * math.sin(ang + 0.5))]
    d.polygon(pts, fill=col + (255,))

cut = pop(clean(cutout(f"{SCR}/kipf/f_13.2.png")))
bb = cut.split()[-1].getbbox(); cut = cut.crop(bb)
s = 1115 / cut.height; cut = cut.resize((int(cut.width * s), 1115), Image.LANCZOS)

# --- D2a: Texas Tech red/black, giant "28"
im = radial_bg((150, 18, 28), (12, 6, 8))
for i in range(0, W, 60):  # subtle diagonal speed lines
    ImageDraw.Draw(im).line([(i, H), (i + 500, 0)], fill=(255, 255, 255, 10), width=3)
x, y = W - cut.width + 90, H - cut.height + 5
rim(im, cut, x, y, WHITE, 6, 2, 9); rim(im, cut, x, y, YEL, 26, 1, 21)
im.alpha_composite(cut, (x, y))
stroke_text(im, (60, -40), "28", ImageFont.truetype(FI, 560), YEL, 14)
stroke_text(im, (640, 120), "YEAR", ImageFont.truetype(FI, 150), WHITE, 9)
stroke_text(im, (640, 270), "OLD", ImageFont.truetype(FI, 150), WHITE, 9)
d = ImageDraw.Draw(im)
box = [70, 560, 1000, 760]; d.rectangle(box, fill=WHITE + (255,)); d.rectangle([box[0] + 10, box[1] + 10, box[2] - 10, box[3] - 10], fill=RED + (255,))
stroke_text(im, (535, 660), "FRESHMAN?", ImageFont.truetype(FI, 150), WHITE, 6, shadow=False, anchor="mm")
tag = ImageFont.truetype(FB, 40)
d.rounded_rectangle([80, 820, 640, 890], 10, fill=(0, 0, 0, 200)); d.text((105, 834), "TEXAS TECH · FALL 2024", font=tag, fill=WHITE)
im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/D2a_28-year-old-freshman.jpg", quality=95)

# --- D2b: blurred real background (his own interview frame), yellow + black, label style
bg = Image.open(f"{SCR}/kipf/f_13.2.png").convert("RGB")
bg = ImageOps.fit(bg, (W, H)).filter(ImageFilter.GaussianBlur(14)); bg = ImageEnhance.Brightness(bg).enhance(0.45)
im = bg.convert("RGBA")
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(shade)
for i in range(W): ds.line([(i, 0), (i, H)], fill=(0, 0, 0, int(200 * max(0, 1 - i / 1100))))
im.alpha_composite(shade)
x, y = W - cut.width + 90, H - cut.height + 5
rim(im, cut, x, y, WHITE, 5, 2, 9); rim(im, cut, x, y, RED, 30, 1, 25)
im.alpha_composite(cut, (x, y))
stroke_text(im, (60, 60), "AGE 28.", ImageFont.truetype(FI, 220), YEL, 12)
stroke_text(im, (60, 300), "COLLEGE", ImageFont.truetype(FI, 170), WHITE, 10)
stroke_text(im, (60, 490), "FRESHMAN.", ImageFont.truetype(FI, 170), WHITE, 10)
d = ImageDraw.Draw(im)
d.ellipse([60, 770, 330, 1040], fill=RED + (255,), outline=WHITE + (255,), width=10)
stroke_text(im, (195, 905), "LEGAL?", ImageFont.truetype(FI, 62), WHITE, 4, shadow=False, anchor="mm")
im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/D2b_age-28-college-freshman.jpg", quality=95)
print("done")

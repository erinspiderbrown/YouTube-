"""Thumbnails v3 for The Downfall of Matthew Boling: the "pro" pass (user, 10 Nov 2026: v2 "look amateur").
What changed vs v2: clean subject cutouts (rembg isnet / birefnet-portrait) instead of rectangular photo panels,
one cinematic background (Budapest stadium at night, blurred), rim light + colour-matched grading on every cutout,
depth (giant ghosted Bolt behind, sharp Boling in front), clean heavy type with soft shadow (no grunge), one accent colour.
Real photos only, never upscaled beyond the source frame.
python3 -I thumbnail_v3.py ASSET_DIR OUT_DIR    (ASSET_DIR has bg_bud_342.png, cut/*.png)
"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"; INTBL = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
A, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
GOLD, WHITE, BLACK, RED, CYAN = (255, 196, 40), (255, 255, 255), (0, 0, 0), (235, 32, 40), (120, 210, 255)
F = lambda p, s: ImageFont.truetype(p, s)


def bg_stadium(tint=(10, 18, 40), blur=14, dark=0.5):
    im = Image.open(f"{A}/bg_bud_342.png").convert("RGB").resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))  # blurred backdrop only
    im = ImageEnhance.Brightness(im).enhance(dark); im = Image.blend(im, Image.new("RGB", im.size, tint), 0.35)
    # vignette
    y, x = np.mgrid[0:H, 0:W].astype(np.float32); v = 1 - 0.75 * (((x - W / 2) / (W / 1.6)) ** 2 + ((y - H / 2) / (H / 1.3)) ** 2)
    a = np.asarray(im).astype(np.float32) * np.clip(v, 0.15, 1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def beams(im, x, col=(255, 220, 150), a=60):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(x - 60, -50), (x + 60, -50), (x + 420, H), (x - 420, H)], fill=col + (a,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(60)))


def cut(name, box=None):
    c = Image.open(f"{A}/cut/{name}").convert("RGBA")
    if box: c = c.crop(box)
    return c.crop(c.getbbox())


def grade(c, con=1.1, col=1.1, bri=1.0, temp=0.0):
    rgb, a = c.convert("RGB"), c.split()[-1]
    rgb = ImageEnhance.Contrast(rgb).enhance(con); rgb = ImageEnhance.Color(rgb).enhance(col); rgb = ImageEnhance.Brightness(rgb).enhance(bri)
    if temp:
        r, g, b = rgb.split(); r = r.point(lambda v: min(255, v * (1 + temp))); b = b.point(lambda v: min(255, v * (1 - temp))); rgb = Image.merge("RGB", (r, g, b))
    rgb = rgb.filter(ImageFilter.UnsharpMask(1.4, 50, 2)); rgb.putalpha(a); return rgb


def place(im, c, x, y, h, rim=WHITE, rim_a=1.0, glow=None, glow_a=0.6, shadow=True, alpha=1.0):
    """paste cutout c with its height scaled to h (downscale only), add rim light + back glow."""
    s = min(1.0, h / c.height); c = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
    a = c.split()[-1]
    if alpha < 1: a = a.point(lambda v: int(v * alpha)); c.putalpha(a)
    if glow:
        g = Image.new("RGBA", c.size, glow + (0,)); g.putalpha(a.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(min(255, v * 1.6) * glow_a)))
        big = Image.new("RGBA", (W, H), (0, 0, 0, 0)); big.alpha_composite(g, (x, y)); im.alpha_composite(big.filter(ImageFilter.GaussianBlur(30)))
    if shadow:
        sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.7)))
        im.alpha_composite(sh, (x + 14, y + 18))
    im.alpha_composite(c, (x, y))
    if rim:
        er = a.filter(ImageFilter.MinFilter(9)); edge = ImageChops.subtract(a, er).filter(ImageFilter.GaussianBlur(3))
        r = Image.new("RGBA", c.size, rim + (0,)); r.putalpha(edge.point(lambda v: int(min(255, v * 1.4) * rim_a))); im.alpha_composite(r, (x, y))
    return c.size


def text(im, xy, s, size, fill, anchor="la", stroke=0, shadow=0.85, grad=None):
    f = F(ANTON, size); l, t, r, b = f.getbbox(s, stroke_width=stroke); pad = 50
    lay = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((pad - l, pad - t), s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,))
    if grad:  # vertical gradient fill
        g = Image.new("RGBA", lay.size); gd = ImageDraw.Draw(g)
        for yy in range(lay.height):
            k = yy / lay.height; gd.line([(0, yy), (lay.width, yy)], fill=tuple(int(grad[0][i] * (1 - k) + grad[1][i] * k) for i in range(3)) + (255,))
        a = lay.split()[-1]; g.putalpha(a); lay = g
    x, y = xy
    if anchor == "ma": x -= lay.width // 2
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * shadow)))
    im.alpha_composite(sh, (x + 6, y + 14)); im.alpha_composite(lay, (x, y)); return lay.size


def grain(im, k=6):
    n = np.random.default_rng(3).normal(0, k, (H, W, 1)).astype(np.float32)
    a = np.asarray(im.convert("RGB")).astype(np.float32) + n
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def save(im, name):
    im = grain(im)
    im.save(f"{OUT}/{name}_HD.jpg", quality=95, subsampling=0)
    im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95, subsampling=0, optimize=True)


def fade_bottom(c, start=0.62):
    a = c.split()[-1]; g = Image.new("L", c.size, 255); d = ImageDraw.Draw(g); y0 = int(c.height * start)
    for y in range(y0, c.height): d.line([(0, y), (c.width, y)], fill=int(255 * (1 - (y - y0) / (c.height - y0)) ** 1.6))
    c = c.copy(); c.putalpha(ImageChops.multiply(a, g)); return c


def solid(c, lo=60, hi=200):
    a = c.split()[-1].point(lambda v: 0 if v < lo else (255 if v > hi else int((v - lo) * 255 / (hi - lo)))); c = c.copy(); c.putalpha(a); return c


def largest(c):
    import cv2
    a = np.asarray(c.split()[-1]); n, lab, st, _ = cv2.connectedComponentsWithStats((a > 30).astype(np.uint8))
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = Image.fromarray(((lab == k) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    c = c.copy(); c.putalpha(ImageChops.multiply(c.split()[-1], m)); return c.crop(c.getbbox())


bolt = largest(cut("bolt_rio.png"))
head = fade_bottom(solid(cut("d_362.png", (540, 40, 1012, 820))), 0.7)       # Boling profile, facing right (HD, 1080p doc frame)
smile = fade_bottom(cut("d_363.png", (975, 0, 1920, 1080)), 0.72)               # Boling close-up, smiling

def gold(c):
    g = ImageOps.colorize(ImageOps.grayscale(c.convert("RGB")), (50, 25, 0), (255, 210, 100)); g.putalpha(c.split()[-1]); return g

# ---- P1: Boling (big, right) looks up at the giant gold ghost of Usain Bolt (left) ----
im = bg_stadium((14, 16, 34)); beams(im, 420, (255, 200, 90), 85)
place(im, gold(bolt), -40, 20, 1060, rim=GOLD, glow=GOLD, glow_a=0.65, shadow=False, alpha=0.88)
place(im, grade(smile, 1.1, 0.9, 1.08, -0.02), 975, 0, 1080, rim=(150, 200, 255), rim_a=0.75, glow=(60, 120, 220), glow_a=0.3)
text(im, (40, 610), "THE NEXT", 150, WHITE)
text(im, (40, 760), "BOLT?", 280, GOLD, grad=((255, 232, 130), (255, 150, 10)))
save(im, "P1_next_bolt")

# ---- P2: the number that made him + "WIND-AIDED" stamp, big smiling Boling ----
im = bg_stadium((30, 10, 6), 16, 0.4); beams(im, 1450, (255, 150, 70), 55)
f = F(ANTON, 470); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
d.text((80, 170), "9.98", font=f, fill=(255, 180, 35, 255))
g = lay.filter(ImageFilter.GaussianBlur(28)); im.alpha_composite(g); im.alpha_composite(g); im.alpha_composite(lay)
st = Image.new("RGBA", (900, 230), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rounded_rectangle([10, 10, 890, 220], 18, outline=RED + (255,), width=16); sd.text((450, 115), "WIND-AIDED", font=F(ANTON, 150), fill=RED + (255,), anchor="mm")
st = st.rotate(-9, expand=True, resample=Image.BICUBIC); sh = Image.new("RGBA", st.size, (0, 0, 0, 0)); sh.putalpha(st.split()[-1].filter(ImageFilter.GaussianBlur(10)))
im.alpha_composite(sh, (95, 690)); im.alpha_composite(st, (80, 670))
place(im, grade(smile, 1.1, 1.05, 1.1, 0.04), 975, 0, 1080, rim=(255, 170, 90), rim_a=0.7, glow=(220, 90, 30), glow_a=0.3)
save(im, "P2_998_wind")
# ---- P3: THEN (sprinting, gold) vs NOW (dark sunset profile), WHAT HAPPENED? ----
im = bg_stadium((12, 14, 30), 16, 0.42)
sun = Image.open(f"{A}/d_411.png").convert("RGB").crop((520, 0, 1600, 1080))          # 1080x1080, Boling silhouette vs sunset
sun = ImageEnhance.Contrast(sun).enhance(1.15).convert("RGBA")
m = Image.new("L", sun.size, 0); md = ImageDraw.Draw(m)
for x in range(sun.width): md.line([(x, 0), (x, sun.height)], fill=int(255 * min(1, x / 360) ** 1.4))
sun.putalpha(m); im.alpha_composite(sun, (W - 1080, 0))
beams(im, 420, (255, 200, 90), 70)
run = largest(cut("ark1_boling.png"))
place(im, grade(run, 1.12, 1.15, 1.06, 0.06), 60, 30, 1050, rim=GOLD, rim_a=0.9, glow=GOLD, glow_a=0.22, shadow=False)
text(im, (560, 60), "THEN", 120, GOLD)
text(im, (1640, 60), "NOW", 120, (255, 140, 110))
text(im, (W // 2 + 120, 780), "WHAT HAPPENED?", 200, WHITE, anchor="ma")
save(im, "P3_then_now")
print("ok")

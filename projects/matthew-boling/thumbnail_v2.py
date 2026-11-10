"""Thumbnails v2 for The Downfall of Matthew Boling, built from the viral-thumbnail study (thumbnail_research.md).
Real photos only, never upscaled:
  - Usain Bolt lightning pose, Rio 2016 (Wikimedia Commons, "Usain Bolt Rio 100m final 2016.jpg")
  - Boling racing, Arkansas Invite 2020 (Wikimedia Commons, "Arkansas Invite 2020 MatthewBoling.jpg")
  - Boling, hands on head at dusk / smiling close-up (University of Georgia documentary frames, 1080p)
python3 -I thumbnail_v2.py ASSET_DIR OUT_DIR
"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"; INTBL = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
A, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
YEL, RED, WHITE, BLACK = (255, 222, 0), (232, 22, 30), (255, 255, 255), (0, 0, 0)
F = lambda p, s: ImageFont.truetype(p, s)


def load(name): return Image.open(f"{A}/{name}").convert("RGB")


def fit_crop(im, box, size):
    """crop box then scale to size; asserts we only ever downscale."""
    c = im.crop(box); s = size[0] / c.width
    assert s <= 1.001 and size[1] / c.height <= 1.001, (box, size, s)
    return c.resize(size, Image.LANCZOS)


def grade(im, con=1.12, col=1.15, bri=1.03, sharp=True):
    im = ImageEnhance.Contrast(im).enhance(con); im = ImageEnhance.Color(im).enhance(col); im = ImageEnhance.Brightness(im).enhance(bri)
    return im.filter(ImageFilter.UnsharpMask(1.2, 40, 3)) if sharp else im


def sad(im):
    g = ImageOps.grayscale(im).convert("RGB"); g = ImageEnhance.Contrast(g).enhance(1.25)
    blue = Image.new("RGB", im.size, (20, 40, 70)); return Image.blend(g, blue, 0.18)


def grunge_text(im, xy, text, size, fill, stroke=16, anchor="la", rough=True, rot=0, outline=BLACK):
    """Heavy condensed text, thick outline, slightly distressed edges (the Korzemba/Nonstop look)."""
    f = F(ANTON, size); l, t, r, b = f.getbbox(text, stroke_width=stroke); pad = 60
    lay = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((pad - l, pad - t), text, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=outline + (255,))
    if rough:
        rnd = random.Random(len(text) * 7); n = Image.new("L", lay.size, 255); nd = ImageDraw.Draw(n)
        for _ in range(int(lay.width * lay.height / 900)):
            x, y = rnd.randrange(lay.width), rnd.randrange(lay.height); rr = rnd.choice((1, 2, 2, 3))
            nd.ellipse([x, y, x + rr, y + rr], fill=0)
        a = ImageChops.multiply(lay.split()[-1], n); lay.putalpha(a)
    if rot: lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.8)))
    x, y = xy
    if anchor == "ma": x -= lay.width // 2
    if anchor == "ra": x -= lay.width
    im.paste(sh, (x + 10, y + 14), sh); im.paste(lay, (x, y), lay)
    return lay.size


def arrow(im, pts, col=RED, w=26):
    """hand-drawn style curved arrow through 3 points."""
    d = ImageDraw.Draw(im); (x0, y0), (mx, my), (x1, y1) = pts
    P = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in [i / 50 for i in range(51)]]
    ang = math.atan2(y1 - P[-5][1], x1 - P[-5][0]); L = 90
    head = [(x1 + 10 * math.cos(ang), y1 + 10 * math.sin(ang)), (x1 - L * math.cos(ang - 0.55), y1 - L * math.sin(ang - 0.55)), (x1 - L * math.cos(ang + 0.55), y1 - L * math.sin(ang + 0.55))]
    for c, ww in ((BLACK, w + 14), (col, w)):
        for p, q in zip(P, P[1:]): d.line([p, q], fill=c, width=ww)
        d.polygon(head, fill=c, outline=BLACK if c == col else c)
    d.line([P[-2], (x1, y1)], fill=col, width=w)


def circle(im, box, col=RED, w=14):
    d = ImageDraw.Draw(im)
    for c, ww in ((BLACK, w + 10), (col, w)): d.ellipse(box, outline=c, width=ww)


def bolt_split(im, left, right, x=960, col=YEL):
    """two panels separated by a jagged lightning seam."""
    pts = [(x + 40, 0), (x - 30, 330), (x + 50, 350), (x - 40, 720), (x + 30, 740), (x - 50, H)]
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0)] + pts + [(0, H)], fill=255)
    im.paste(right, (0, 0)); im.paste(left, (0, 0), m)
    d = ImageDraw.Draw(im)
    for c, ww in ((BLACK, 30), (col, 16)): d.line(pts, fill=c, width=ww, joint="curve")


def save(im, name):
    im = im.convert("RGB"); im.save(f"{OUT}/{name}_HD.jpg", quality=95, subsampling=0)
    im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95, subsampling=0, optimize=True)


bolt = load("bolt_rio.jpg")            # 1920x1280, Bolt at x~250-960, y~430-1250
ark = load("ark1.jpg")                 # 1920x1280, Boling (centre) x~900-1350
hands = load("d_416.png")              # 1920x1080, Boling hands on head x~480-1440
smile = load("d_363.png")              # 1920x1080, close-up smile

# ---- T1: THE NEXT BOLT?  Bolt (bright) | Boling hands on head (cold), lightning seam ----
L = Image.new("RGB", (W, H)); R = Image.new("RGB", (W, H))
L.paste(grade(bolt.crop((60, 200, 1170, 1280)), 1.1, 1.25, 1.05), (-40, 0))
r = sad(fit_crop(hands, (300, 0, 1500, 1080), (1200, 1080))); R.paste(grade(r, 1.08, 1.0, 1.0), (840, 0))
im = Image.new("RGB", (W, H)); bolt_split(im, L, R, 1000)
grunge_text(im, (W // 2, 770), "THE NEXT BOLT?", 235, YEL, 18, anchor="ma")
t = Image.new("RGBA", (W, H)); grunge_text(t, (1090, 20), "9.98 AT 18", 120, WHITE, 12, rot=4); im.paste(t, (0, 0), t)
save(im, "T1_next_bolt")

# ---- T2: THEN / NOW banners + WHAT WENT WRONG? ----
im = Image.new("RGB", (W, H), (10, 10, 12))
lt = grade(fit_crop(ark, (720, 40, 1640, 1120), (940, 1080)) if False else fit_crop(ark, (700, 60, 1600, 1094), (900, 1034)), 1.12, 1.2, 1.05)
im.paste(lt, (0, 46))
rt = sad(fit_crop(hands, (420, 0, 1440, 1080), (1000, 1059)))
im.paste(rt, (920, 21))
d = ImageDraw.Draw(im); d.rectangle([900, 0, 920, H], fill=BLACK)
for x0, x1, lab in ((0, 900, "THEN"), (920, W, "NOW")):
    d.rectangle([x0, 0, x1, 150], fill=RED); d.text(((x0 + x1) / 2, 75), lab, font=F(INTBL, 120), fill=WHITE, anchor="mm")
grunge_text(im, (W // 2, 760), "WHAT WENT WRONG?", 210, RED, 18, anchor="ma", outline=WHITE)
t = Image.new("RGBA", (W, H)); grunge_text(t, (60, 600), "9.98", 150, YEL, 12, rot=6); im.paste(t, (0, 0), t)
save(im, "T2_then_now")

# ---- T3: quote style, smiling close-up | hands on head, red circle ----
im = Image.new("RGB", (W, H), (0, 0, 0))
im.paste(grade(fit_crop(smile, (760, 0, 1720, 1080), (960, 1080)), 1.1, 1.15, 1.08), (0, 0))
im.paste(sad(fit_crop(hands, (480, 0, 1440, 1080), (960, 1080))), (960, 0))
d = ImageDraw.Draw(im); d.rectangle([950, 0, 970, H], fill=BLACK)
grunge_text(im, (W // 2, 700), "“HE WAS SUPPOSED TO BE", 118, WHITE, 14, anchor="ma")
grunge_text(im, (W // 2, 840), "THE NEXT USAIN BOLT”", 150, RED, 16, anchor="ma", outline=WHITE)
circle(im, (1230, 270, 1610, 660))
save(im, "T3_quote")
print("ok")

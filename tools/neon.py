"""Neon look for graphics: dark synthwave background, bloom, neon-framed photos, archival frames.

Used by the Jon Drummond documentary (user asked for "neon and it should pop").
- background(t): near-black navy, drifting orange/cyan glows, faint top grid,
  perspective floor grid scrolling toward camera, HUD corner brackets.
- finish(im, t): bloom (bright parts glow), faint scanlines, film grain.
- neon_photo(...): a photo card with a glowing border, pop-in and a name tag.
- archive_frame(...): RGBA overlay used on top of real archival footage.
"""
import math, os
from functools import lru_cache
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import gfx

W, H, FPS = 1920, 1080, 24
BG = (6, 7, 13)
ORANGE = (255, 122, 26)
CYAN = (0, 229, 255)
PINK = (255, 46, 99)
WHITE = (248, 248, 252)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def eo(t):
    t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def eback(t, s=1.7):
    t = min(max(t, 0), 1) - 1; return t * t * ((s + 1) * t + s) + 1
def seg(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)

def mono(size):
    return ImageFont.truetype(MONO, size)

# ------------------------------------------------------------------ background
_yy, _xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)

TAG = "JD//ARCHIVE"  # corner label on the neon background; projects override it

NOBLOOM = []  # photo rects this frame: kept out of the bloom so photos don't wash out

def background(t):
    NOBLOOM.clear()
    x, y = _xx, _yy
    g1 = np.exp(-(((x - (W / 8 + 140 * math.sin(t * 0.35))) / 230) ** 2 + ((y - (H / 10 + 25 * math.cos(t * 0.3))) / 120) ** 2))
    g2 = np.exp(-(((x - (W / 4 - 90 - 60 * math.cos(t * 0.27))) / 200) ** 2 + ((y - H / 6) / 140) ** 2))
    vig = 1 - 0.6 * (((x - W / 8) / (W / 8)) ** 2 * 0.5 + ((y - H / 8) / (H / 8)) ** 2 * 0.5)
    img = np.zeros((H // 4, W // 4, 3), np.float32)
    for c in range(3):
        img[..., c] = BG[c] * vig + g1 * ORANGE[c] * 0.13 + g2 * CYAN[c] * 0.08
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im, "RGBA")
    # faint top grid
    off = int((t * 10) % 80)
    for gx in range(-80 + off, W, 80): d.line([(gx, 0), (gx, 640)], fill=(40, 60, 90, 22))
    for gy in range(0, 640, 80): d.line([(0, gy), (W, gy)], fill=(40, 60, 90, 22))
    # perspective floor
    hz, vx = 700, W / 2
    d.line([(0, hz), (W, hz)], fill=ORANGE + (70,), width=2)
    for i in range(-14, 15):
        xb = vx + i * 230
        d.line([(vx + i * 18, hz), (xb, H)], fill=CYAN + (34,), width=2)
    ph = (t * 0.6) % 1
    for j in range(9):
        z = (j + ph) / 9
        yy = hz + (H - hz) * z ** 2.2
        d.line([(0, yy), (W, yy)], fill=CYAN + (int(10 + 45 * z),), width=2)
    # HUD corners
    L = 46
    for sx, sy in ((40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)):
        dx = 1 if sx < W / 2 else -1; dy = 1 if sy < H / 2 else -1
        d.line([(sx, sy), (sx + dx * L, sy)], fill=CYAN + (150,), width=3)
        d.line([(sx, sy), (sx, sy + dy * L)], fill=CYAN + (150,), width=3)
    d.text((W - 60, H - 72), f"{TAG}  {int(t * 24) % 10000:04d}", font=mono(18), fill=CYAN + (110,), anchor="ra")
    return im

# ------------------------------------------------------------------ finish (bloom)
_grain = [np.random.default_rng(i).normal(0, 5, (H // 2, W // 2)).astype(np.float32) for i in range(6)]
_scan = ((np.arange(H) % 3 == 0).astype(np.float32) * -6)[:, None, None]

def bloom(a, strength=1.0, thr=120):
    a = a.astype(np.float32)
    lum = a.max(axis=2, keepdims=True)
    bright = a * np.clip((lum - thr) / (255 - thr), 0, 1)
    for x0, y0, x1, y1 in NOBLOOM:
        bright[max(0, y0):max(0, y1), max(0, x0):max(0, x1)] *= 0.08
    small = cv2.resize(bright, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    g1 = cv2.GaussianBlur(small, (0, 0), 3)
    g2 = cv2.GaussianBlur(small, (0, 0), 12)
    glow = cv2.resize(g1 * 0.9 + g2 * 1.1, (W, H), interpolation=cv2.INTER_LINEAR)
    return a + glow * strength

def finish(im, t):
    a = bloom(np.asarray(im.convert("RGB")))
    gr = _grain[int(t * FPS) % len(_grain)]
    gr = np.kron(gr, np.ones((2, 2), np.float32))[:H, :W]
    a = a + gr[..., None] + _scan
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ------------------------------------------------------------------ photos
PHOTOS = None  # set by caller: directory with p_*.jpg / l_*.jpg

@lru_cache(maxsize=64)
def load_crop(path, cx=0.5, cy=0.5, hfrac=1.0, aspect=0.78):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    ch = h * hfrac; cw = ch * aspect
    if cw > w: cw = w; ch = cw / aspect
    x0 = min(max(0, cx * w - cw / 2), w - cw); y0 = min(max(0, cy * h - ch / 2), h - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))

def glow_rect(size, box, color, width=4, blur=18, inner=True):
    """RGBA layer with a glowing neon rectangle outline."""
    lay = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle(box, outline=color + (255,), width=width + 6)
    g = lay.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.alpha_composite(g); out.alpha_composite(g)
    d2 = ImageDraw.Draw(out)
    d2.rectangle(box, outline=color + (255,), width=width)
    x0, y0, x1, y1 = box
    d2.rectangle([x0 + width, y0 + width, x1 - width, y1 - width], outline=(255, 255, 255, 140), width=1)
    return out

def neon_photo(im, src, cx, cy, h, t, t0, color=ORANGE, label=None, sub=None, crop=(0.5, 0.5, 1.0), aspect=0.78, zoom=0.05):
    """Paste a neon-framed photo centred at (cx, cy) with height h, popping in at t0."""
    k = eback(seg(t, t0, t0 + 0.45))
    if k <= 0: return
    ph = load_crop(src, *crop, aspect=aspect)
    hh = int(h * min(1.08, k)); ww = int(hh * aspect)
    if hh < 8: return
    z = 1 + zoom * seg(t, t0, t0 + 6)
    big = ph.resize((int(ww * z), int(hh * z)), Image.LANCZOS)
    ox, oy = (big.width - ww) // 2, (big.height - hh) // 2
    pic = big.crop((ox, oy, ox + ww, oy + hh))
    x0, y0 = int(cx - ww / 2), int(cy - hh / 2)
    pad = 60
    fr = glow_rect((ww + 2 * pad, hh + 2 * pad), [pad - 3, pad - 3, pad + ww + 2, pad + hh + 2], color, width=4, blur=16)
    im.paste(pic, (x0, y0))
    NOBLOOM.append((x0 + 4, y0 + 4, x0 + ww - 4, y0 + hh - 4))
    im.paste(fr, (x0 - pad, y0 - pad), fr)
    if label:
        ka = eo(seg(t, t0 + 0.25, t0 + 0.6))
        if ka > 0:
            d = ImageDraw.Draw(im, "RGBA")
            f = gfx.font("Black", 34); fs = mono(18)
            tw = d.textlength(label.upper(), font=f) + 40
            bx, by = cx - tw / 2, y0 + hh + 22
            d.rectangle([bx, by, bx + tw * ka, by + 52], fill=(8, 9, 16, 230), outline=color + (255,), width=2)
            if ka > 0.7: d.text((cx, by + 26), label.upper(), font=f, fill=WHITE, anchor="mm")
            if sub and ka > 0.9:
                d.text((cx, by + 72), sub.upper(), font=fs, fill=color + (255,), anchor="mm")

# ------------------------------------------------------------------ archival overlay
def archive_frame(tag, box=None, color=ORANGE, accent=CYAN, kind="ARCHIVE"):
    """Full-frame RGBA overlay: neon border around `box` (or screen edge), REC dot, tag text."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if box:
        im.alpha_composite(glow_rect((W, H), box, color, width=4, blur=22))
        x0, y0, x1, y1 = box
    else:
        x0, y0, x1, y1 = 34, 34, W - 34, H - 34
    d = ImageDraw.Draw(im)
    L = 54
    for sx, sy, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(sx, sy), (sx + dx * L, sy)], fill=accent + (255,), width=5)
        d.line([(sx, sy), (sx, sy + dy * L)], fill=accent + (255,), width=5)
    f = mono(24)
    tx, ty = x0 + 30, y0 + 26
    kw = d.textlength(kind + " ", font=f); tw = d.textlength("// " + tag.upper(), font=f)
    d.rectangle([tx - 12, ty - 8, tx + 30 + kw + tw + 14, ty + 34], fill=(4, 6, 14, 170))
    d.ellipse([tx, ty + 4, tx + 18, ty + 22], fill=PINK + (255,))
    d.text((tx + 30, ty), kind, font=f, fill=WHITE + (235,))
    d.text((tx + 30 + kw, ty), "// " + tag.upper(), font=f, fill=color + (255,))
    glow = im.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); out.alpha_composite(glow); out.alpha_composite(im)
    return out

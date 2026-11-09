"""Thumbnails for "Every Banned Substance in Track (and who got caught)" (The Erin Brown).

Built from thumbnail_research.md: the 32x original is a 2x4 grid of drug photos with captions. The top "every X" outliers
(BTS scandals 59x, 13 Track Stars Banned 26x) are grids of faces captioned with the offence. So: faces + the drug that got them.
Look: the documentary neon (cyan + orange glow on dark) from tools/neon.py / projects/jon-drummond, plus red BANNED stamps.
Real photos only: Wikimedia Commons (see thumbnail_credits.md).

Run: python3 -I projects/banned-substances/thumbnails.py SRC_DIR OUT_DIR   (renders 1920x1080, saves 1280x720 JPGs)
"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops, ImageOps

SRC_DIR = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/banned/src"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/banned/thumbs"
W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
CYAN, ORANGE, RED = (0, 229, 255), (255, 122, 26), (235, 28, 36)
NAVY, INK = (6, 10, 20), (12, 16, 28)

# name: (file, face centre x, face centre y (fractions of the image), head height (crown to chin) as fraction of image height)
SRC = {
    "johnson88":  ("Elgrafico 3599 ben johnson.jpg",          0.63, 0.165, 0.11),   # El Grafico 3599, Sept 1988 (Seoul)
    "johnson":    ("Ben Johnson 2017 (cropped).jpg",          0.475, 0.255, 0.36),
    "jones":      ("Marion Jones Sydney 2000.JPEG",           0.415, 0.185, 0.15),   # Sydney 2000
    "gatlin":     ("Justin Gatlin Rio 2016b-cr.jpg",          0.54, 0.135, 0.125),   # Rio 2016 100m final
    "shacarri":   ("ShaCarri sq.jpg",                         0.56, 0.225, 0.16),    # 2021 US Olympic Trials (the THC meet)
    "shacarri23": ("ShaCarri Budapest 2023.jpg",              0.497, 0.170, 0.16),
    "krabbe":     ("Krabbe Berlin 1988.jpg",                  0.28, 0.27, 0.19),     # Bundesarchiv, Berlin 1988
    "lashmanova": ("Elena Lashmanova London 2012.jpg",        0.46, 0.145, 0.17),
    "chambers":   ("Dwain Chambers 2008.jpg",                 0.46, 0.37, 0.55),
    "powell":     ("Asafa Powell Paris 2006.jpg",             0.42, 0.235, 0.06),
    "merritt":    ("LaShawn Merritt 2012.JPG",                0.48, 0.32, 0.50),
    "gay":        ("Tyson Gay 2012.jpg",                      0.49, 0.235, 0.17),
}
# drug photos: (file, crop box as fractions l, t, r, b)
DRUG = {
    "stanozolol": ("Wp stanozolol.jpg",        (0.30, 0.20, 0.98, 0.98)),   # Strombafort = stanozolol 10 mg tablets
    "steroids":   ("Port Huron steroids.jpg",  (0.05, 0.28, 0.95, 0.80)),   # seized anabolic steroid vials (CBP)
    "cannabis":   ("Cannabis Closeup 01.jpg",  (0.05, 0.00, 0.95, 0.95)),
    "testosterone": ("Depo-testosterone crop.jpg", (0.0, 0.0, 1.0, 1.0)),
    "winstrol":   ("Winstrol tablets.JPG",     (0.0, 0.0, 1.0, 1.0)),   # Winstrol = stanozolol 50 mg tablets
}

def have(name):
    return os.path.exists(f"{SRC_DIR}/{SRC[name][0]}")

def load(f):
    return ImageOps.exif_transpose(Image.open(f"{SRC_DIR}/{f}")).convert("RGB")

def cover(im, size, cx=0.5, cy=0.5):
    """Scale `im` to cover `size`, keeping point (cx, cy) as central as possible."""
    tw, th = size; iw, ih = im.size; s = max(tw / iw, th / ih)
    sw, sh = iw * s, ih * s
    x0 = min(max(cx * sw - tw / 2, 0), sw - tw); y0 = min(max(cy * sh - th / 2, 0), sh - th)
    return im.resize((max(tw, int(round(sw))), max(th, int(round(sh)))), Image.LANCZOS).crop((int(x0), int(y0), int(x0) + tw, int(y0) + th))

def face_tile(name, size, face_px, fy=0.42, fx=0.5):
    """Tile of `size` with the head about face_px tall, placed at (fx, fy) of the tile; the photo always covers the tile."""
    f, cx, cy, fh = SRC[name]
    im = load(f); iw, ih = im.size
    tw, th = size
    s = max(face_px / (fh * ih), tw / iw, th / ih)
    sw, sh = iw * s, ih * s
    x0 = min(max(cx * sw - fx * tw, 0), sw - tw); y0 = min(max(cy * sh - fy * th, 0), sh - th)
    out = im.resize((int(round(sw)), int(round(sh))), Image.LANCZOS).crop((int(x0), int(y0), int(x0) + tw, int(y0) + th))
    out = ImageEnhance.Contrast(out).enhance(1.10); out = ImageEnhance.Color(out).enhance(1.05)
    return out.filter(ImageFilter.UnsharpMask(2, 110 if s > 1.5 else 60, 2))

def drug_tile(name, size):
    f, (l, t, r, b) = DRUG[name]
    im = load(f); iw, ih = im.size
    im = im.crop((int(l * iw), int(t * ih), int(r * iw), int(b * ih)))
    out = cover(im, size)
    out = ImageEnhance.Contrast(out).enhance(1.12); out = ImageEnhance.Color(out).enhance(1.1)
    return out.filter(ImageFilter.UnsharpMask(2, 70, 2))

def font(size): return ImageFont.truetype(ANTON, size)

def fit_size(s, maxw, size):
    while font(size).getlength(s) > maxw and size > 20: size -= 2
    return size

def glow_layer(mask, col, radius, gain=1.6):
    g = Image.new("RGBA", mask.size, col + (0,))
    g.putalpha(mask.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, int(v * gain))))
    return g

def neon_text(im, xy, s, size, col, anchor="mm", core=WHITE, glow=(26, 10), stroke=0):
    """Neon tube lettering: coloured outer glow, coloured edge, near-white core."""
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).text(xy, s, font=font(size), fill=255, anchor=anchor, stroke_width=stroke, stroke_fill=255)
    for r in glow: im.alpha_composite(glow_layer(m, col, r, 1.5))
    edge = Image.new("RGBA", im.size, col + (0,)); edge.putalpha(m); im.alpha_composite(edge)
    inner = Image.new("L", im.size, 0); ImageDraw.Draw(inner).text(xy, s, font=font(size), fill=255, anchor=anchor)
    inner = inner.filter(ImageFilter.MinFilter(5)) if size > 90 else inner.filter(ImageFilter.MinFilter(3))
    c = Image.new("RGBA", im.size, tuple(int(core[i] * 0.8 + col[i] * 0.2) for i in range(3)) + (0,)); c.putalpha(inner); im.alpha_composite(c)

def text(im, xy, s, size, fill, stroke=0, anchor="mm", shadow=12, stroke_fill=BLACK):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=font(size), fill=fill + (255,), stroke_width=stroke, stroke_fill=stroke_fill + (255,), anchor=anchor)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.5))))
        im.alpha_composite(sh, (4, 8))
    im.alpha_composite(lay)

def neon_frame(im, box, col, width=6, radius=14, glow=(18, 7)):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle(box, radius, outline=255, width=width)
    for r in glow: im.alpha_composite(glow_layer(m, col, r, 1.7))
    e = Image.new("RGBA", im.size, col + (0,)); e.putalpha(m); im.alpha_composite(e)
    core = Image.new("RGBA", im.size, (255, 255, 255, 0)); core.putalpha(m.filter(ImageFilter.MinFilter(3)).point(lambda v: int(v * 0.7))); im.alpha_composite(core)

def paste_rounded(im, tile, xy, radius=14):
    m = Image.new("L", tile.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, tile.width - 1, tile.height - 1], radius, fill=255)
    im.paste(tile, xy, m)

def stamp(im, cx, cy, s, size, rot=-14, col=RED, pad=(26, 8)):
    """Rubber-stamp: double red border + distressed red letters, rotated."""
    f = font(size); l, t, r, b = f.getbbox(s, anchor="mm")
    w, h = int(r - l + 2 * pad[0]), int(b - t + 2 * pad[1])
    lay = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bw = max(5, size // 12)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], 10, outline=col + (255,), width=bw)
    d.rounded_rectangle([20 + bw + 5, 20 + bw + 5, 20 + w - bw - 5, 20 + h - bw - 5], 6, outline=col + (255,), width=max(2, bw // 3))
    d.text((20 + w / 2, 20 + h / 2 + 2), s, font=f, fill=col + (255,), anchor="mm")
    rnd = random.Random(hash(s) & 0xffff)
    noise = Image.new("L", lay.size, 255); nd = ImageDraw.Draw(noise)
    for _ in range(int(lay.width * lay.height / 260)):
        x, y = rnd.randrange(lay.width), rnd.randrange(lay.height); rr = rnd.choice((1, 1, 2, 3))
        nd.ellipse([x, y, x + rr, y + rr], fill=rnd.choice((0, 60, 120)))
    a = ImageChops.multiply(lay.split()[-1], noise); lay.putalpha(a)
    lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.6)))
    im.alpha_composite(sh, (int(cx - lay.width / 2 + 3), int(cy - lay.height / 2 + 5)))
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def bg_dark(col_a=CYAN, col_b=ORANGE):
    """Deep navy with a faint HUD grid and two soft colour blooms."""
    im = Image.new("RGBA", (W, H), NAVY + (255,)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(20, 40, 60, 255), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(20, 40, 60, 255), width=1)
    for (cx, cy, col) in ((0.15, 0.1, col_a), (0.85, 0.95, col_b)):
        b = Image.new("L", (W // 8, H // 8), 0); ImageDraw.Draw(b).ellipse([cx * W / 8 - 70, cy * H / 8 - 50, cx * W / 8 + 70, cy * H / 8 + 50], fill=80)
        b = b.filter(ImageFilter.GaussianBlur(25)).resize((W, H), Image.BICUBIC)
        g = Image.new("RGBA", (W, H), col + (0,)); g.putalpha(b); im.alpha_composite(g)
    return im

def vignette(im, strength=170):
    m = Image.new("L", (W // 8, H // 8), 0); d = ImageDraw.Draw(m)
    d.ellipse([-W // 16, -H // 14, W // 8 + W // 16, H // 8 + H // 14], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(18)).resize((W, H), Image.BICUBIC)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 255)); sh.putalpha(m.point(lambda v: int(strength * (1 - v / 255))))
    im.alpha_composite(sh)

def scan_lines(im, alpha=22):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for y in range(0, H, 4): d.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    im.alpha_composite(lay)

def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    p = f"{OUT}/{name}.jpg"
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(p, quality=92, optimize=True)
    assert os.path.getsize(p) < 2_000_000, p
    print(p, os.path.getsize(p))
    return p

# ---------------------------------------------------------------- A: neon face grid
GRID = [  # (photo, drug caption, name)
    ("johnson88", "STANOZOLOL", "BEN JOHNSON '88", 0.30),
    ("jones", "“THE CLEAR”", "MARION JONES"),
    ("gatlin", "TESTOSTERONE", "JUSTIN GATLIN"),
    ("shacarri", "THC", "SHA'CARRI"),
    ("krabbe", "CLENBUTEROL", "KATRIN KRABBE"),
    ("lashmanova", "GW1516", "LASHMANOVA"),
    ("merritt", "DHEA", "LASHAWN MERRITT"),
    ("chambers", "THG", "DWAIN CHAMBERS", 0.30),
]

def thumb_grid(name="A_neon_grid", items=None, stamp_word="BANNED"):
    items = items or [g for g in GRID if have(g[0])][:8]
    im = bg_dark()
    cols, rows = 4, 2
    mx, my, gx, gy = 46, 40, 30, 30
    tw = (W - 2 * mx - (cols - 1) * gx) // cols
    th = (H - 2 * my - (rows - 1) * gy) // rows
    cap_h = 118
    ph = th - cap_h
    for i, it in enumerate(items):
        who, drug, nm = it[:3]; fscale = it[3] if len(it) > 3 else 0.42
        c, r = i % cols, i // cols
        x, y = mx + c * (tw + gx), my + r * (th + gy)
        col = CYAN if (c + r) % 2 == 0 else ORANGE
        tile = face_tile(who, (tw, ph), face_px=int(ph * fscale), fy=0.40)
        # dark caption panel under the photo
        card = Image.new("RGBA", (tw, th), INK + (255,)); card.paste(tile, (0, 0))
        g = Image.new("RGBA", (tw, 60), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for yy in range(60): gd.line([(0, yy), (tw, yy)], fill=INK + (int(255 * yy / 60),))
        card.alpha_composite(g, (0, ph - 60))
        paste_rounded(im, card.convert("RGB"), (x, y), 16)
        neon_frame(im, [x, y, x + tw, y + th], col, width=5, radius=16)
        sz = fit_size(drug, tw - 40, 84)
        neon_text(im, (x + tw / 2, y + ph + cap_h / 2 - 2), drug, sz, col, glow=(16, 6))
        # name tag top-left (HUD style)
        tag = font(30); nw = tag.getlength(nm)
        d = ImageDraw.Draw(im)
        d.rectangle([x + 12, y + 12, x + 32 + nw, y + 56], fill=(0, 0, 0, 200))
        d.rectangle([x + 12, y + 12, x + 17, y + 56], fill=col + (255,))
        d.text((x + 25, y + 34), nm, font=tag, fill=WHITE + (255,), anchor="lm")
        stamp(im, x + tw - 92, y + ph - 34, stamp_word, 42, rot=-12 + (i % 3) * 5)
    scan_lines(im, 14)
    return save(im, name)

# ---------------------------------------------------------------- B: Ben Johnson 9.79 hero
def thumb_johnson(name="B_johnson_979"):
    im = bg_dark(ORANGE, RED)
    # the real 1988 El Grafico cover as a tilted, neon-framed card
    cov = load(SRC["johnson88"][0])
    ch = 900; cw = int(cov.width * ch / cov.height)
    cov = cov.resize((cw, ch), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    card = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0))
    card.paste(cov, (60, 60))
    fm = Image.new("L", card.size, 0); ImageDraw.Draw(fm).rectangle([56, 56, 64 + cw, 64 + ch], outline=255, width=8)
    for r in (30, 10): card.alpha_composite(glow_layer(fm, ORANGE, r, 1.8))
    e = Image.new("RGBA", card.size, ORANGE + (0,)); e.putalpha(fm); card.alpha_composite(e)
    card = card.rotate(4, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(card, (40, (H - card.height) // 2 + 10))
    # the real drug: stanozolol tablets
    dt = drug_tile("winstrol", (560, 380))
    dx, dy = 1270, 600
    paste_rounded(im, dt, (dx, dy), 18)
    neon_frame(im, [dx, dy, dx + 560, dy + 380], CYAN, width=6, radius=18)
    # copy
    neon_text(im, (1300, 300), "9.79", 330, CYAN, glow=(40, 14))
    d = ImageDraw.Draw(im)
    d.line([(990, 330), (1640, 250)], fill=RED + (255,), width=26)
    stamp(im, 1240, 560, "STANOZOLOL", 92, rot=-6)
    text(im, (1300, 90), "SEOUL 1988 • GOLD STRIPPED", 50, WHITE, shadow=10)
    vignette(im, 120); scan_lines(im, 14)
    return save(im, name)

# ---------------------------------------------------------------- C: who used what? lineup
def thumb_lineup(name="C_who_used_what"):
    im = bg_dark()
    people = [p for p in ("johnson88", "jones", "shacarri", "gatlin") if have(p)]
    FS = {"johnson88": 0.30}
    drugs = [d for d in ("cannabis", "winstrol", "testosterone", "steroids") if os.path.exists(f"{SRC_DIR}/{DRUG[d][0]}")]  # scrambled on purpose
    neon_text(im, (W / 2, 112), "WHO USED WHAT?", 150, ORANGE, glow=(34, 12))
    n = len(people); mx, gx = 60, 34
    tw = (W - 2 * mx - (n - 1) * gx) // n
    fh = 470
    for i, p in enumerate(people):
        x, y = mx + i * (tw + gx), 230
        paste_rounded(im, face_tile(p, (tw, fh), face_px=int(fh * FS.get(p, 0.40)), fy=0.40), (x, y), 16)
        neon_frame(im, [x, y, x + tw, y + fh], CYAN, width=5)
    labels = {"winstrol": "STANOZOLOL", "stanozolol": "STANOZOLOL", "steroids": "STEROIDS", "cannabis": "THC", "testosterone": "TESTOSTERONE"}
    m = len(drugs); dw = (W - 2 * mx - (m - 1) * gx) // m; dh = 280
    for i, dname in enumerate(drugs):
        x, y = mx + i * (dw + gx), 760
        paste_rounded(im, drug_tile(dname, (dw, dh)), (x, y), 16)
        neon_frame(im, [x, y, x + dw, y + dh], ORANGE, width=5)
        lab = labels[dname]; sz = fit_size(lab, dw - 50, 64)
        d = ImageDraw.Draw(im); bw = font(sz).getlength(lab)
        d.rounded_rectangle([x + dw / 2 - bw / 2 - 18, y + dh - sz - 34, x + dw / 2 + bw / 2 + 18, y + dh - 14], 10, fill=(0, 0, 0, 215))
        d.text((x + dw / 2, y + dh - 24 - sz / 2), lab, font=font(sz), fill=WHITE + (255,), anchor="mm")
    # question marks linking the rows
    for i in range(n):
        cx = mx + i * (tw + gx) + tw / 2
        neon_text(im, (cx, 718), "?", 120, ORANGE, glow=(22, 8))
    scan_lines(im, 14)
    return save(im, name)

# ---------------------------------------------------------------- D: original-format white grid, drug over face
def thumb_pairs(name="D_drug_over_face"):
    im = Image.new("RGBA", (W, H), WHITE + (255,))
    pairs = [("winstrol", "STANOZOLOL", "johnson88", "BEN JOHNSON '88"),
             ("testosterone", "TESTOSTERONE", "gatlin", "GATLIN '06"),
             ("cannabis", "THC", "shacarri", "SHA'CARRI '21"),
             ("steroids", "STEROIDS", "jones", "MARION JONES")]
    pairs = [p for p in pairs if have(p[2]) and os.path.exists(f"{SRC_DIR}/{DRUG[p[0]][0]}")]
    n = len(pairs); mx, gx = 40, 34
    tw = (W - 2 * mx - (n - 1) * gx) // n
    th, cap = 400, 104
    for i, (dn, dl, who, nl) in enumerate(pairs):
        x = mx + i * (tw + gx)
        im.paste(drug_tile(dn, (tw, th)), (x, 20))
        sz = fit_size(dl, tw - 10, 80)
        text(im, (x + tw / 2, 20 + th + cap / 2), dl, sz, BLACK, shadow=0)
        im.paste(face_tile(who, (tw, th), face_px=int(th * (0.30 if who == 'johnson88' else 0.42)), fy=0.40), (x, 20 + th + cap))
        sz2 = fit_size(nl, tw - 10, 70)
        text(im, (x + tw / 2, 20 + 2 * th + cap + 58), nl, sz2, BLACK, shadow=0)
        stamp(im, x + tw - 104, 20 + th + cap + th - 44, "CAUGHT", 44, rot=-12)
    return save(im, name)

if __name__ == "__main__":
    which = sys.argv[3:] or ["A", "B", "C", "D"]
    if "A" in which: thumb_grid()
    if "B" in which: thumb_johnson()
    if "C" in which: thumb_lineup()
    if "D" in which: thumb_pairs()

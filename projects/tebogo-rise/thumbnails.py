"""Thumbnails for "The Rise of Letsile Tebogo" (The Erin Brown).
African look: Botswana flag colours (light blue #75AADB, black, white) + gold, warm golden grade, basket-weave triangle accents.
Built from the niche's breakout thumbnails (see thumbnail_research.md): one big sharp face on a soft natural background,
1-3 huge words, year/age panels with huge numbers (the user's pick last time), versus split.
Real photos only: Wikimedia Commons + frames from YouTube race videos (see thumbnail_credits.md).
Helpers adapted from projects/ncaa-100m-champs/thumbnails.py and projects/ncaa-xc-takeover/thumbnail_kip2.py.
Run: python3 -I projects/tebogo-rise/thumbnails.py OUTDIR   (renders 1920x1080, saves 1280x720 JPGs)"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/tebogo"
SRC_DIR = f"{SCR}/src"
GEO = f"{SCR}/geo/countries-50m.json"   # world-atlas@2.0.2 (Natural Earth 1:50m, public domain) via jsDelivr
W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
BLUE, BLACK, WHITE = (117, 170, 219), (0, 0, 0), (255, 255, 255)
GOLD, GOLD_D, CREAM = (255, 196, 30), (196, 128, 10), (255, 240, 205)
NAVY = (14, 18, 26)

# name: (file, face centre x, face centre y (0-1 of image), head height (crown to chin) as fraction of image height)
SRC = {
    "hero":    ("douala_crop.jpg",   0.484, 0.225, 0.24),   # 2024 African Champs, Douala (CC0)
    "smile":   ("bislett_smile.jpg", 0.512, 0.165, 0.22),   # Bislett Games 2026, Oslo (CC BY-SA 4.0)
    "u20":     ("nai_22.0.png",      0.498, 0.350, 0.16),   # 2021 World U20 Nairobi, age 18 (World Athletics)
    "worlds":  ("bud_up.png",        0.420, 0.330, 0.48),   # 2023 Worlds Budapest, after 100m silver, 9:13.9 (World Athletics)
    "paris":   ("paris_face.png",    0.510, 0.134, 0.20),   # Paris 2024 200m final intro (Olympics)
    "lyles":   ("lyles_bud.png",     0.575, 0.410, 0.27),   # Noah Lyles, Budapest 2023 (World Athletics)
}
CROP = {}

def load(name):
    f = SRC[name][0]
    return Image.open(f"{SRC_DIR}/{f}").convert("RGB")

def face_tile(name, size, face_px, fy=0.4, fx=0.5, enhance=True):
    """Tile of `size` with the head about face_px tall, centred near (fx, fy) of the tile; the photo always covers the tile."""
    f, cx, cy, fh = SRC[name]
    im = load(name); iw, ih = im.size
    l, t, r, b = CROP.get(name, (0, 0, 1, 1))
    im = im.crop((int(l * iw), int(t * ih), int(r * iw), int(b * ih)))
    fpx = fh * ih
    cx = (cx - l) / (r - l); cy = (cy - t) / (b - t); iw, ih = im.size
    tw, th = size
    s = max(face_px / fpx, tw / iw, th / ih)
    sw, sh_ = iw * s, ih * s
    x0 = min(max(cx * sw - fx * tw, 0), sw - tw); y0 = min(max(cy * sh_ - fy * th, 0), sh_ - th)
    out = im.resize((int(round(sw)), int(round(sh_))), Image.LANCZOS).crop((int(x0), int(y0), int(x0) + tw, int(y0) + th))
    if enhance:
        out = ImageEnhance.Contrast(out).enhance(1.08); out = ImageEnhance.Color(out).enhance(1.08)
        out = out.filter(ImageFilter.UnsharpMask(2, 90 if s > 1.2 else 50, 2))
    return out

def golden(im, amt=0.30, warm=(1.10, 1.0, 0.80)):
    """Warm golden grade: warm channel gains blended in, slight lift of contrast."""
    rgb = im.convert("RGB")
    r, g, b = rgb.split()
    r = r.point(lambda v: min(255, int(v * warm[0]))); g = g.point(lambda v: min(255, int(v * warm[1]))); b = b.point(lambda v: int(v * warm[2]))
    out = Image.blend(rgb, Image.merge("RGB", (r, g, b)), amt / 0.3 * 0.6 if amt < 0.3 else 0.6)
    gold = Image.new("RGB", out.size, (255, 170, 40))
    out = Image.blend(out, ImageChops.soft_light(out, gold), amt)
    return out.convert("RGBA") if im.mode == "RGBA" else out

def vignette(im, strength=170):
    m = Image.new("L", (W // 8, H // 8), 0); d = ImageDraw.Draw(m)
    d.ellipse([-W // 16, -H // 14, W // 8 + W // 16, H // 8 + H // 14], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(18)).resize((W, H), Image.BICUBIC)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 255)); sh.putalpha(m.point(lambda v: int(strength * (1 - v / 255))))
    im.alpha_composite(sh)

def text(im, xy, s, size, fill, stroke=0, anchor="mm", shadow=14, stroke_fill=BLACK):
    fnt = ImageFont.truetype(ANTON, size)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=fnt, fill=fill + (255,), stroke_width=stroke, stroke_fill=stroke_fill + (255,), anchor=anchor)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.6))))
        im.alpha_composite(sh, (5, 9))
    im.alpha_composite(lay)

def gold_text(im, xy, s, size, stroke=8, anchor="mm", shadow=16):
    """Gold gradient lettering with a dark outline (medal look)."""
    fnt = ImageFont.truetype(ANTON, size)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).text(xy, s, font=fnt, fill=255, anchor=anchor)
    so = Image.new("L", im.size, 0); ImageDraw.Draw(so).text(xy, s, font=fnt, fill=255, anchor=anchor, stroke_width=stroke, stroke_fill=255)
    bb = m.getbbox() or (0, 0, W, H)
    grad = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(grad)
    top, bot = bb[1], bb[3]
    stops = [(0.0, (255, 236, 150)), (0.45, (255, 196, 30)), (0.55, (232, 150, 10)), (1.0, (255, 210, 70))]
    for y in range(top, bot + 1):
        t = (y - top) / max(1, bot - top)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0); c = tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)); break
        d.line([(0, y), (W, y)], fill=c + (255,))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(so.filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.7))))
        im.alpha_composite(sh, (6, 11))
    edge = Image.new("RGBA", im.size, NAVY + (0,)); edge.putalpha(so); im.alpha_composite(edge)
    grad.putalpha(m); im.alpha_composite(grad)

def fit_size(s, maxw, size):
    fnt = ImageFont.truetype(ANTON, size)
    while fnt.getlength(s) > maxw and size > 20:
        size -= 4; fnt = ImageFont.truetype(ANTON, size)
    return size

def pill(im, cx, cy, s, size, bg, fg, padx=34, pady=14, radius=18, maxw=None, rot=0, outline=BLACK):
    if maxw: size = fit_size(s, maxw - 2 * padx, size)
    fnt = ImageFont.truetype(ANTON, size)
    l, t, r, b = fnt.getbbox(s, anchor="mm")
    w, h = (r - l) + 2 * padx, (b - t) + 2 * pady
    lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], radius, fill=bg + (255,), outline=outline + (255,), width=6)
    d.text((30 + w / 2, 30 + h / 2), s, font=fnt, fill=fg + (255,), anchor="mm")
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(sh, (int(cx - lay.width / 2 + 4), int(cy - lay.height / 2 + 8)))
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def vgrad(im, y0, y1, a0, a1, col=BLACK):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(y0, y1):
        a = a0 + (a1 - a0) * (y - y0) / max(1, y1 - y0); d.line([(0, y), (W, y)], fill=col + (int(a),))
    im.alpha_composite(g)

def hgrad(im, x0, x1, a0, a1, col=BLACK):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for x in range(x0, x1):
        a = a0 + (a1 - a0) * (x - x0) / max(1, x1 - x0); d.line([(x, 0), (x, H)], fill=col + (int(max(0, a)),))
    im.alpha_composite(g)

def weave_band(im, y, h=46, x0=0, x1=W, cols=(GOLD, BLACK, BLUE, BLACK)):
    """Basket-weave style band: alternating up/down triangles (Botswana basketry 'Ngwao' style accent)."""
    d = ImageDraw.Draw(im); step = h
    d.rectangle([x0, y, x1, y + h], fill=NAVY + (255,))
    for i, x in enumerate(range(x0 - step, x1 + step, step)):
        c = cols[i % len(cols)]
        d.polygon([(x, y + h), (x + step / 2, y + 4), (x + step, y + h)], fill=c + (255,))
        d.polygon([(x + step / 2, y + 4), (x + step, y + h - 2), (x + step * 1.5, y + 4)], fill=WHITE + (255,) if i % 2 else BLUE + (255,))
    d.line([(x0, y), (x1, y)], fill=GOLD + (255,), width=5); d.line([(x0, y + h), (x1, y + h)], fill=GOLD + (255,), width=5)

def flag_stripe_v(im, x, w=26):
    """Vertical Botswana flag stripe used as a panel divider: blue | white | black | white | blue."""
    d = ImageDraw.Draw(im); parts = [(BLUE, 0.28), (WHITE, 0.10), (BLACK, 0.24), (WHITE, 0.10), (BLUE, 0.28)]
    cx = x - w / 2
    for col, f in parts:
        d.rectangle([cx, 0, cx + w * f, H], fill=col + (255,)); cx += w * f

# ---------- Africa silhouette from world-atlas topojson (Natural Earth, public domain) ----------
AFRICA_IDS = {"012", "024", "072", "108", "120", "132", "140", "148", "174", "178", "180", "204", "226", "231", "232", "262", "266",
              "270", "288", "324", "384", "404", "426", "430", "434", "450", "454", "466", "478", "480", "504", "508", "516", "562",
              "566", "624", "646", "678", "686", "690", "694", "706", "710", "716", "728", "729", "732", "748", "768", "788", "800",
              "818", "834", "854", "894"}

def _topo():
    tj = json.load(open(GEO)); sc, tr = tj["transform"]["scale"], tj["transform"]["translate"]
    arcs = []
    for a in tj["arcs"]:
        x = y = 0; pts = []
        for dx, dy in a:
            x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    def ring(idx):
        out = []
        for i in idx:
            p = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(p[1:] if out else p)
        return out
    geoms = {}
    for g in tj["objects"]["countries"]["geometries"]:
        polys = [g["arcs"]] if g["type"] == "Polygon" else g.get("arcs", []) if g["type"] == "MultiPolygon" else []
        geoms[str(g.get("id"))] = [[ring(r) for r in poly] for poly in polys]
    return geoms

def africa_layer(box_h, fill=GOLD, botswana=BLUE, outline=NAVY, glow=GOLD):
    """RGBA image of Africa (equirectangular, lat-scaled) filled `fill`, Botswana in `botswana`, with soft glow."""
    geoms = _topo(); lon0, lon1, lat0, lat1 = -18.5, 52.5, -35.5, 38.0
    s = box_h / (lat1 - lat0); bw = int((lon1 - lon0) * s * 0.97); pad = 40
    P = lambda lo, la: (pad + (lo - lon0) * s * 0.97, pad + (lat1 - la) * s)
    big = Image.new("L", (bw + 2 * pad, box_h + 2 * pad), 0); bots = Image.new("L", big.size, 0)
    da, db = ImageDraw.Draw(big), ImageDraw.Draw(bots)
    for cid in AFRICA_IDS:
        for poly in geoms.get(cid, []):
            for k, r in enumerate(poly):
                if len(r) < 3: continue
                pts = [P(lo, la) for lo, la in r]
                if max(p[0] for p in pts) < 0 or min(p[0] for p in pts) > big.width: continue
                da.polygon(pts, fill=0 if k else 255)
                if cid == "072": db.polygon(pts, fill=0 if k else 255)
    lay = Image.new("RGBA", big.size, (0, 0, 0, 0))
    g = Image.new("RGBA", big.size, glow + (0,)); g.putalpha(big.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.9)))
    lay.alpha_composite(g)
    o = Image.new("RGBA", big.size, outline + (0,)); o.putalpha(big.filter(ImageFilter.MaxFilter(7))); lay.alpha_composite(o)
    f = Image.new("RGBA", big.size, fill + (0,)); f.putalpha(big); lay.alpha_composite(f)
    b = Image.new("RGBA", big.size, botswana + (0,)); b.putalpha(bots); lay.alpha_composite(b)
    bo = Image.new("RGBA", big.size, NAVY + (0,)); bo.putalpha(ImageChops.subtract(bots.filter(ImageFilter.MaxFilter(5)), bots)); lay.alpha_composite(bo)
    return lay

def save(im, out, name):
    p = f"{out}/{name}.jpg"
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(p, quality=92, optimize=True)
    assert os.path.getsize(p) < 2 * 1024 * 1024, p

# ---------------- thumbnails ----------------
def A_age_panels(OUT):
    """User's pick last time (huge yellow years under faces) + age contrast: 18 (U20 champ, Nairobi Aug 2021; born 7 Jun 2003) / 20 (2 world medals) / 21 (Olympic gold)."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    panels = [("u20", "18", "WORLD U20 CHAMP", 0.36), ("worlds", "20", "2 WORLD MEDALS", 0.38), ("paris", "21", "OLYMPIC GOLD", 0.36)]
    for i, (n, *_ , fy) in enumerate(panels):
        t = face_tile(n, (640, H), face_px=330, fy=fy)
        im.paste(golden(t, 0.22), (i * 640, 0))
    vgrad(im, 0, 200, 120, 0); vgrad(im, 600, H, 0, 240, NAVY)
    for x in (640, 1280): flag_stripe_v(im, x, 28)
    for i, (n, age, tag, _) in enumerate(panels):
        cx = i * 640 + 320
        pill(im, cx, 690, tag, 58, GOLD if i == 2 else BLUE, BLACK, padx=22, pady=10, radius=14, maxw=600)
        gold_text(im, (cx, 905), age, 300, stroke=10)
    save(im, OUT, "A_18-20-21_age-panels")

def B_first_ever(OUT):
    """One big sharp face on the soft stadium background + 2 huge words + Africa silhouette with Botswana marked."""
    base = face_tile("hero", (W, H), face_px=760, fx=0.70, fy=0.40)
    im = golden(base, 0.32).convert("RGBA")
    hgrad(im, 0, 1150, 235, 0, NAVY)
    vignette(im, 120)
    af = africa_layer(520)
    im.alpha_composite(af, (40, 430))
    gold_text(im, (70, 30), "FIRST", 250, stroke=10, anchor="la")
    text(im, (78, 300), "EVER", 150, WHITE, stroke=6, anchor="la")
    pill(im, 860, 975, "OLYMPIC 200M CHAMP", 64, GOLD, BLACK, padx=26, pady=12, radius=16)
    weave_band(im, H - 46, 46)
    save(im, OUT, "B_first-ever-africa")

def C_1946(OUT):
    """Big time number (the 'record' format) + smiling face; Botswana blue panel with gold weave accent."""
    base = face_tile("smile", (W, H), face_px=720, fx=0.68, fy=0.40)
    blur = base.filter(ImageFilter.GaussianBlur(14))
    m = Image.new("L", (W, H)); d = ImageDraw.Draw(m)
    for x in range(W): d.line([(x, 0), (x, H)], fill=int(255 * min(1, max(0, (1000 - x) / 320))))
    comp = Image.composite(blur, base, m)
    patch = comp.crop((1700, 820, W, H)).filter(ImageFilter.GaussianBlur(18)); comp.paste(patch, (1700, 820))  # illegible arm tattoo text: softened
    im = golden(comp, 0.30).convert("RGBA")
    hgrad(im, 0, 1100, 225, 0, NAVY)
    gold_text(im, (60, 60), "19.46", 330, stroke=12, anchor="la")
    text(im, (70, 520), "AFRICA'S FIRST", 118, WHITE, stroke=6, anchor="la")
    text(im, (70, 680), "OLYMPIC 200M CHAMP", 96, BLUE, stroke=6, anchor="la")
    weave_band(im, 0, 40)
    weave_band(im, H - 40, 40)
    save(im, OUT, "C_19-46")

def D_lyles_vs(OUT):
    """Versus split (Noah Lyles vs Tebogo) with the Paris 200m final times: 19.70 vs 19.46."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    L = face_tile("lyles", (960, H), face_px=430, fy=0.40)
    L = ImageEnhance.Color(L).enhance(0.55); L = ImageEnhance.Brightness(L).enhance(0.8)
    R = golden(face_tile("hero", (960, H), face_px=470, fx=0.48, fy=0.40), 0.32)
    im.paste(L, (0, 0)); im.paste(R, (960, 0))
    vgrad(im, 640, H, 0, 235, NAVY)
    d = ImageDraw.Draw(im)
    d.polygon([(930, 0), (1000, 0), (990, H), (920, H)], fill=BLACK + (255,))
    d.polygon([(944, 0), (986, 0), (976, H), (934, H)], fill=GOLD + (255,))
    text(im, (480, 760), "LYLES", 130, WHITE, stroke=6)
    text(im, (480, 925), "19.70", 170, (200, 200, 200), stroke=7)
    text(im, (1440, 760), "TEBOGO", 130, WHITE, stroke=6)
    gold_text(im, (1400, 925), "19.46", 190, stroke=9)
    pill(im, 960, 90, "OLYMPIC 200M FINAL", 62, GOLD, BLACK, padx=26, pady=10, radius=14)
    save(im, OUT, "D_lyles-vs-tebogo")

def E_age17_flag(OUT):
    """Age 18 with the Botswana flag (Nairobi 2021 U20 title) -> 'OLYMPIC CHAMP' at 21: the whole rise in one image."""
    base = face_tile("u20", (W, H), face_px=300, fx=0.68, fy=0.36)
    im = golden(base, 0.22).convert("RGBA")
    hgrad(im, 0, 1050, 230, 0, NAVY)
    vignette(im, 90)
    gold_text(im, (70, 10), "18", 420, stroke=12, anchor="la")
    text(im, (400, 150), "YEARS OLD", 110, WHITE, stroke=6, anchor="la")
    d = ImageDraw.Draw(im)
    d.polygon([(110, 560), (250, 560), (250, 520), (340, 610), (250, 700), (250, 660), (110, 660)], fill=GOLD + (255,), outline=BLACK + (255,))
    text(im, (380, 610), "OLYMPIC", 150, WHITE, stroke=7, anchor="lm")
    gold_text(im, (380, 800), "CHAMP", 190, stroke=10, anchor="lm")
    weave_band(im, H - 44, 44)
    save(im, OUT, "E_18-to-olympic-champ")

if __name__ == "__main__":
    OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
    only = sys.argv[2:] or None
    for fn in (A_age_panels, B_first_ever, C_1946, D_lyles_vs, E_age17_flag):
        if not only or fn.__name__[0] in only: fn(OUT)
    print("done")

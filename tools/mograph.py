"""Full-screen animated motion graphics (maps, timelines, data, explainers).

Each graphic is a function frame(t, dur) -> PIL RGB image, rendered at 24 fps to mp4.
Shared look: dark charcoal background, faint grid, drifting orange glow, film grain.
"""
import json, math, os, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfx

W, H, FPS = 1920, 1080, 24
BG = (13, 14, 18)
ORANGE = (255, 122, 26)
RED = (229, 57, 53)
WHITE = (245, 245, 245)
GREY = (110, 114, 124)
DIM = (52, 55, 63)
GEO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "geo")

def eo(t):  # ease out cubic
    t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def eio(t):
    t = min(max(t, 0), 1); return 3 * t * t - 2 * t * t * t
def eback(t, s=1.7):
    t = min(max(t, 0), 1) - 1; return t * t * ((s + 1) * t + s) + 1
def seg(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)

_grain = [np.random.default_rng(i).normal(0, 6, (H // 2, W // 2)).astype(np.float32) for i in range(6)]

def background(t):
    y, x = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
    cx = W // 8 + 60 * math.sin(t * 0.4); cy = H // 8 + 30 * math.cos(t * 0.3)
    g = np.exp(-(((x - cx) / 260) ** 2 + ((y - cy) / 170) ** 2))
    v = 1 - 0.55 * (((x - W / 8) / (W / 8)) ** 2 + ((y - H / 8) / (H / 8)) ** 2) * 0.5
    img = np.zeros((H // 4, W // 4, 3), np.float32)
    for c in range(3):
        img[..., c] = BG[c] * v + g * (ORANGE[c] * 0.10)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im)
    off = int((t * 12) % 80)
    for gx in range(-80 + off, W, 80): d.line([(gx, 0), (gx, H)], fill=(22, 23, 28))
    for gy in range(0, H, 80): d.line([(0, gy), (W, gy)], fill=(22, 23, 28))
    return im

def finish(im, t):
    a = np.asarray(im).astype(np.float32)
    gr = _grain[int(t * FPS) % len(_grain)]
    gr = np.kron(gr, np.ones((2, 2), np.float32))[:H, :W]
    return Image.fromarray(np.clip(a + gr[..., None], 0, 255).astype(np.uint8))

def text(d, xy, s, size, fill=WHITE, weight="Black", anchor="la", alpha=1.0):
    f = gfx.font(weight, size)
    if alpha < 1:
        fill = tuple(int(c * alpha + b * (1 - alpha)) for c, b in zip(fill, BG))
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    return d.textlength(s, font=f)

def header(d, t, kicker, title, x=110, y=90):
    k = eo(t / 0.4)
    if k <= 0: return
    w = text(d, (x, y), kicker.upper(), 28, ORANGE, "Bold", alpha=k)
    d.rectangle([x, y + 44, x + int(120 * eo((t - 0.1) / 0.4)), y + 50], fill=ORANGE)
    f = gfx.font("Black", 76)
    shown = title.upper()[: int(len(title) * eo((t - 0.15) / 0.5))]
    d.text((x, y + 70), shown, font=f, fill=WHITE)

def render(frame_fn, dur, out):
    n = round(dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        p.stdin.write(finish(frame_fn(t, dur), t).tobytes())
    p.stdin.close(); p.wait()
    return out

# ------------------------------------------------------------------ maps
def _load(name):
    return json.load(open(os.path.join(GEO, name)))["features"]

def _polys(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"][0]]
    return [p[0] for p in geom["coordinates"]]

class Proj:
    def __init__(self, lon0, lon1, lat0, lat1, box=(0, 0, W, H)):
        self.set(lon0, lon1, lat0, lat1, box)
    def set(self, lon0, lon1, lat0, lat1, box=(0, 0, W, H)):
        self.lon0, self.lat1 = lon0, lat1
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        bw, bh = box[2] - box[0], box[3] - box[1]
        self.s = min(bw / ((lon1 - lon0) * self.k), bh / (lat1 - lat0))
        self.ox = box[0] + (bw - (lon1 - lon0) * self.k * self.s) / 2
        self.oy = box[1] + (bh - (lat1 - lat0) * self.s) / 2
    def __call__(self, lon, lat):
        return (self.ox + (lon - self.lon0) * self.k * self.s, self.oy + (self.lat1 - lat) * self.s)

def lerp_view(a, b, k):
    return tuple(x + (y - x) * k for x, y in zip(a, b))

def draw_map(d, feats, proj, hi=None, hi_fill=ORANGE, base_fill=(30, 32, 38), edge=(70, 74, 84), hi_k=1.0):
    hi = hi or {}
    for f in feats:
        nm = f["properties"].get("name")
        for poly in _polys(f["geometry"]):
            pts = [proj(x, y) for x, y in poly]
            if len(pts) < 3: continue
            fill = base_fill
            if nm in hi:
                k = hi[nm] * hi_k
                fill = tuple(int(b + (c - b) * k) for b, c in zip(base_fill, hi_fill))
            d.polygon(pts, fill=fill, outline=edge)

def pin(d, xy, t0, t, label=None, sub=None, color=ORANGE, side="right"):
    k = eback(seg(t, t0, t0 + 0.45))
    if k <= 0: return
    x, y = xy; drop = (1 - k) * -60
    for r in range(3):  # pulse rings
        ph = ((t - t0) * 0.8 + r / 3) % 1
        rr = 10 + 50 * ph; a = int(255 * (1 - ph) * 0.6)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=color + (a,) if len(color) == 3 else color, width=3)
    d.ellipse([x - 13, y - 13 + drop, x + 13, y + 13 + drop], fill=color, outline=WHITE, width=4)
    if label:
        ka = eo(seg(t, t0 + 0.3, t0 + 0.7))
        if ka > 0:
            f = gfx.font("Black", 40); fs = gfx.font("SemiBold", 24)
            tw = max(d.textlength(label.upper(), font=f), d.textlength((sub or "").upper(), font=fs))
            bx = x + 34 if side == "right" else x - 34 - tw - 40
            by = y - 46
            d.rectangle([bx, by, bx + (tw + 40) * ka, by + 58], fill=(14, 14, 16))
            d.rectangle([bx, by, bx + 8, by + 58], fill=color)
            if ka > 0.6: d.text((bx + 22, by + 29), label.upper(), font=f, fill=WHITE, anchor="lm")
            if sub and ka > 0.8:
                d.rectangle([bx, by + 58, bx + tw + 40, by + 96], fill=color)
                d.text((bx + 22, by + 77), sub.upper(), font=fs, fill=(18, 18, 18), anchor="lm")

def arc(d, a, b, k, color=ORANGE, width=5, bend=0.25):
    if k <= 0: return
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = []
    for i in range(int(60 * k) + 1):
        s = i / 60
        pts.append(((1 - s) ** 2 * x0 + 2 * (1 - s) * s * cx + s * s * x1,
                    (1 - s) ** 2 * y0 + 2 * (1 - s) * s * cy + s * s * y1))
    if len(pts) > 1:
        for i in range(0, len(pts) - 1, 2):  # dashed
            d.line([pts[i], pts[i + 1]], fill=color, width=width)
        hx, hy = pts[-1]; d.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], fill=color)

MONTVERDE = (-81.674, 28.600)
ORLANDO = (-81.379, 28.538)

def florida_map(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    us = _load("us_states.json")
    k = eio(seg(t, 0.0, 1.6))
    v = lerp_view((-125, -66, 24, 50), (-88.5, -79.5, 24.3, 31.2), k)
    proj = Proj(*v, box=(560, 60, 1860, 1040))
    draw_map(d, us, proj, hi={"Florida": 1.0}, hi_k=eo(seg(t, 0.6, 1.4)), hi_fill=(70, 46, 30))
    pin(d, proj(*ORLANDO), 1.9, t, None, color=GREY)
    if t > 2.0:
        ox, oy = proj(*ORLANDO)
        text(d, (ox + 20, oy + 6), "Orlando", 24, GREY, "SemiBold", alpha=eo(seg(t, 2.0, 2.4)))
    pin(d, proj(*MONTVERDE), 1.5, t, "Montverde Academy", "Montverde, Florida", side="left")
    header(d, t, "Where it happened", "Central Florida")
    return im

def world_routes(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    world = _load("world.json")
    proj = Proj(-100, -45, 0, 34, box=(80, 230, 1840, 1040))
    dests = [("Suriname", (-55.2, 5.85)), ("British Virgin Islands", (-64.62, 18.43)), ("Jamaica", (-76.8, 18.0))]
    hi = {"Suriname": eo(seg(t, 1.0, 1.6)), "Jamaica": eo(seg(t, 2.6, 3.2))}
    draw_map(d, world, proj, hi=hi, hi_fill=(90, 52, 26))
    draw_map(d, _load("us_states.json"), proj, base_fill=(30, 32, 38))
    src = proj(*MONTVERDE)
    for i, (nm, ll) in enumerate(dests):
        t0 = 0.6 + i * 0.8
        arc(d, src, proj(*ll), eo(seg(t, t0, t0 + 0.7)), bend=-0.18)
        pin(d, proj(*ll), t0 + 0.6, t, nm, f"Positive test #{i + 1}", color=RED, side="right" if i == 0 else "left" if i == 2 else "right")
    pin(d, src, 0.2, t, "Montverde", None)
    header(d, t, "Different countries · different agencies", "One school")
    return im

def converge(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    pts0 = [(330, 330), (330, 620), (330, 910)]
    names = ["Suriname", "British Virgin Islands", "Jamaica"]
    school = (1350, 610)
    for i, (p, nm) in enumerate(zip(pts0, names)):
        k = eo(seg(t, 0.2 + i * 0.25, 0.7 + i * 0.25))
        d.ellipse([p[0] - 34, p[1] - 34, p[0] + 34, p[1] + 34], fill=RED if k > 0 else DIM)
        text(d, (p[0], p[1]), "+", 50, WHITE, "Black", anchor="mm")
        text(d, (p[0] + 60, p[1] - 22), nm.upper(), 34, WHITE, "Black", alpha=k)
        text(d, (p[0] + 60, p[1] + 20), "POSITIVE TEST", 24, RED, "Bold", alpha=k)
        kk = eo(seg(t, 1.2 + i * 0.15, 2.0 + i * 0.15))
        if kk > 0:
            sx, sy = p[0] + 380, p[1]
            ex, ey = sx + (school[0] - 150 - sx) * kk, sy + (school[1] - sy) * kk
            d.line([(sx, sy), (ex, ey)], fill=ORANGE, width=6)
    ks = eback(seg(t, 1.9, 2.5))
    if ks > 0:
        x, y = school; s = 150 * ks
        d.polygon([(x - s, y - s * 0.2), (x, y - s * 0.9), (x + s, y - s * 0.2)], fill=ORANGE)
        d.rectangle([x - s * 0.85, y - s * 0.2, x + s * 0.85, y + s * 0.8], fill=ORANGE)
        for c in (-0.5, 0, 0.5):
            d.rectangle([x + s * c - s * 0.12, y + s * 0.05, x + s * c + s * 0.12, y + s * 0.8], fill=BG)
        text(d, (x, y + s * 1.1), "1 SCHOOL", int(70 * ks), WHITE, "Black", anchor="mt")
    header(d, t, "Three kids · three countries", "Same team")
    return im

def africa_target(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    world = _load("world.json")
    proj = Proj(-20, 60, -15, 40, box=(500, 140, 1880, 1060))
    pulse = 0.6 + 0.4 * math.sin(t * 5)
    hi = {"Kenya": eo(seg(t, 0.8, 1.3)) * pulse, "Ethiopia": eo(seg(t, 1.3, 1.8)) * pulse}
    draw_map(d, world, proj, hi=hi, hi_fill=RED)
    for nm, ll, t0 in (("Kenya", (37.9, 0.2), 0.8), ("Ethiopia", (39.5, 8.6), 1.3)):
        x, y = proj(*ll); k = eback(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        r = 70 * k
        d.ellipse([x - r, y - r, x + r, y + r], outline=RED, width=4)
        d.line([(x - r - 30, y), (x - r + 20, y)], fill=RED, width=4); d.line([(x + r - 20, y), (x + r + 30, y)], fill=RED, width=4)
        d.line([(x, y - r - 30), (x, y - r + 20)], fill=RED, width=4); d.line([(x, y + r - 20), (x, y + r + 30)], fill=RED, width=4)
        text(d, (x + r + 40, y - 20), nm.upper(), 40, WHITE, "Black", alpha=k)
    header(d, t, "His point", "Target testing")
    k = eo(seg(t, 2.2, 2.7))
    if k > 0:
        text(d, (110, 330), "“They over-police", 44, WHITE, "Bold", alpha=k)
        text(d, (110, 390), "the African countries.”", 44, WHITE, "Bold", alpha=k)
    return im

def stepper(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Gerald Phiri · case status", "Still pending")
    steps = ["Athletes test positive", "Provisional suspension", "Hearing", "Final decision"]
    x0, x1, y = 360, 1560, 620
    gap = (x1 - x0) / (len(steps) - 1)
    k = eo(seg(t, 0.4, 1.4))
    d.line([(x0, y), (x0 + (x1 - x0) * k, y)], fill=DIM, width=8)
    d.line([(x0, y), (x0 + gap * eo(seg(t, 0.6, 1.4)), y)], fill=ORANGE, width=8)
    for i, s in enumerate(steps):
        x = x0 + gap * i; ks = eback(seg(t, 0.5 + i * 0.2, 0.9 + i * 0.2))
        if ks <= 0: continue
        done, active = i == 0, i == 1
        col = ORANGE if done else (RED if active else DIM)
        r = 30 * ks * (1 + (0.15 * math.sin(t * 6) if active else 0))
        if active:
            for j in range(2):
                ph = (t * 0.9 + j / 2) % 1; rr = 30 + 50 * ph
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=RED + (int(220 * (1 - ph)),), width=3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=WHITE if (done or active) else GREY, width=4)
        text(d, (x, y + 70), s.upper(), 30, WHITE if (done or active) else GREY, "Black", anchor="mt", alpha=ks)
        if i >= 2: text(d, (x, y), "?", 34, GREY, "Black", anchor="mm", alpha=ks)
    if t > 1.6:
        k = eo(seg(t, 1.6, 2.0))
        text(d, (x0 + gap, y - 110), "HE IS HERE", 30, RED, "Black", anchor="mm", alpha=k)
    return im

def definition(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    x, y = 180, 250
    word = "provisional suspension"
    n = int(len(word) * seg(t, 0.2, 1.3))
    w = text(d, (x, y), word[:n], 104, WHITE, "Black")
    if int(t * 2.5) % 2 == 0 and n < len(word):
        d.rectangle([x + w + 10, y + 10, x + w + 18, y + 110], fill=ORANGE)
    text(d, (x, y + 140), "/ prə-ˈvi-zhə-nəl  sə-ˈspen-shən /   noun", 34, GREY, "Medium", alpha=eo(seg(t, 1.3, 1.7)))
    defs = [("1.", "Taken off the track while the case is investigated."),
            ("2.", "His words: “administrative leave, for real.”"),
            ("3.", "No ban. No sanction. Not yet.")]
    for i, (num, s) in enumerate(defs):
        k = eo(seg(t, 2.0 + i * 0.9, 2.5 + i * 0.9))
        if k <= 0: continue
        yy = y + 260 + i * 100
        text(d, (x + int((1 - k) * 60), yy), num, 44, ORANGE, "Black", alpha=k)
        text(d, (x + 80 + int((1 - k) * 60), yy), s, 44, WHITE if i < 2 else ORANGE, "Bold", alpha=k)
    return im

def relationship(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Who was in charge", "Montverde track & field")
    a, b = (560, 640), (1360, 640)
    for (x, y), lab, sub, t0 in ((a, "Head track coach", "Gerald Phiri", 0.4), (b, "Athletic director", "The coach’s wife", 0.8)):
        k = eback(seg(t, t0, t0 + 0.5))
        if k <= 0: continue
        r = 110 * k
        d.ellipse([x - r, y - r, x + r, y + r], fill=(26, 27, 33), outline=ORANGE, width=6)
        d.ellipse([x - 32 * k, y - 62 * k, x + 32 * k, y + 2 * k], fill=GREY)
        d.pieslice([x - 62 * k, y + 8 * k, x + 62 * k, y + 120 * k], 180, 360, fill=GREY)
        text(d, (x, y + 140), lab.upper(), 40, WHITE, "Black", anchor="mt", alpha=min(1, k))
        text(d, (x, y + 192), sub.upper(), 28, ORANGE, "Bold", anchor="mt", alpha=min(1, k))
    k = eo(seg(t, 1.3, 2.0))
    if k > 0:
        mid = (a[0] + b[0]) / 2
        d.line([(a[0] + 120, a[1]), (a[0] + 120 + (b[0] - a[0] - 240) * k, a[1])], fill=ORANGE, width=6)
        if k > 0.9:
            for dx in (-22, 22):
                d.ellipse([mid + dx - 34, a[1] - 34, mid + dx + 34, a[1] + 34], outline=ORANGE, width=8)
            text(d, (mid, a[1] - 70), "MARRIED", 34, WHITE, "Black", anchor="mb")
    return im

def deal_timeline(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Issam Asinga · 2023", "What he lost")
    pts = [("South American Games", 360), ("Pro deal", 960), ("World Championships", 1560)]
    y = 620
    k = eo(seg(t, 0.4, 1.6))
    d.line([(360, y), (360 + 1200 * k, y)], fill=WHITE, width=6)
    for i, (lab, x) in enumerate(pts):
        ks = eback(seg(t, 0.5 + i * 0.4, 0.9 + i * 0.4))
        if ks <= 0: continue
        r = 22 * ks
        d.ellipse([x - r, y - r, x + r, y + r], fill=ORANGE if i == 0 else WHITE)
        text(d, (x, y + 60), lab.upper(), 34, WHITE, "Black", anchor="mt", alpha=min(1, ks))
        if i == 1: text(d, (x, y - 60), "EXPECTED RIGHT AFTER", 24, GREY, "Bold", anchor="mb", alpha=min(1, ks))
    kb = seg(t, 2.4, 2.6)
    if kb > 0:  # suspension breaks the line
        x = 700
        d.rectangle([x - 14, y - 160, x + 14, y + 40], fill=RED)
        sc = 1.8 - 0.8 * eo(seg(t, 2.4, 2.6))
        f = gfx.font("Black", int(64 * sc))
        tw = d.textlength("SUSPENDED", font=f)
        d.rectangle([x - tw / 2 - 24, y - 270, x + tw / 2 + 24, y - 270 + 90 * sc], fill=RED)
        d.text((x, y - 270 + 45 * sc), "SUSPENDED", font=f, fill=WHITE, anchor="mm")
    for i, x in enumerate((960, 1560)):
        kx = eo(seg(t, 3.0 + i * 0.3, 3.3 + i * 0.3))
        if kx > 0:
            s = 46
            d.line([(x - s, y - s), (x - s + 2 * s * kx, y - s + 2 * s * kx)], fill=RED, width=12)
            d.line([(x + s, y - s), (x + s - 2 * s * kx, y - s + 2 * s * kx)], fill=RED, width=12)
    return im

def jadco_vs_aiu(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Same situation · different judges", "Who decides your fate")
    for i, (title, sub, quote, col, t0) in enumerate((
            ("JADCO", "Jamaica’s anti-doping commission", "“Willing to take the time and\ncomprehend the situation.”", ORANGE, 0.5),
            ("AIU / WADA", "International anti-doping", "“They’re nailing it\nto the cross.”", RED, 1.1))):
        k = eo(seg(t, t0, t0 + 0.5))
        if k <= 0: continue
        x = 140 + i * 860 + int((1 - k) * (-80 if i == 0 else 80)); y = 340
        d.rectangle([x, y, x + 780, y + 560], fill=(22, 23, 28), outline=col, width=4)
        d.rectangle([x, y, x + 780, y + 14], fill=col)
        text(d, (x + 50, y + 60), title, 84, WHITE, "Black")
        text(d, (x + 50, y + 170), sub.upper(), 26, col, "Bold")
        kq = eo(seg(t, t0 + 0.5, t0 + 1.0))
        for j, line in enumerate(quote.split("\n")):
            text(d, (x + 50, y + 260 + j * 64), line, 46, WHITE, "Bold", alpha=kq)
        text(d, (x + 50, y + 470), "MORE LENIENT" if i == 0 else "HARSHEST PENALTIES", 32, col, "Black", alpha=kq)
    return im

def gw1516(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    cx, cy = 1420, 560
    for i in range(6):  # rotating molecule
        a = t * 0.6 + i * math.pi / 3
        k = eo(seg(t, 0.1 + i * 0.08, 0.5 + i * 0.08))
        r = 190 * k
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        a2 = t * 0.6 + (i + 1) * math.pi / 3
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        d.line([(x, y), (x2, y2)], fill=ORANGE, width=6)
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=WHITE if i % 2 else ORANGE)
        ox, oy = cx + (r + 120) * math.cos(a), cy + (r + 120) * math.sin(a)
        if i % 2 == 0:
            d.line([(x, y), (ox, oy)], fill=GREY, width=4); d.ellipse([ox - 14, oy - 14, ox + 14, oy + 14], fill=GREY)
    header(d, t, "The substance", "GW1516")
    text(d, (110, 330), "a.k.a. Cardarine", 40, GREY, "Bold", alpha=eo(seg(t, 0.6, 1.0)))
    facts = ["Boosts endurance", "Never approved for human use", "Banned by WADA"]
    for i, f in enumerate(facts):
        k = eo(seg(t, 1.2 + i * 0.6, 1.6 + i * 0.6))
        if k <= 0: continue
        y = 470 + i * 110
        d.rectangle([110, y, 110 + 16, y + 60], fill=ORANGE)
        text(d, (150 + int((1 - k) * 40), y + 30), f.upper(), 50, WHITE, "Black", anchor="lm", alpha=k)
    return im

def _runner(d, x, y, s, col):
    d.ellipse([x - 9 * s, y - 40 * s, x + 9 * s, y - 22 * s], fill=col)
    d.line([(x, y - 22 * s), (x - 4 * s, y + 6 * s)], fill=col, width=int(7 * s))
    d.line([(x - 4 * s, y + 6 * s), (x + 12 * s, y + 30 * s)], fill=col, width=int(6 * s))
    d.line([(x - 4 * s, y + 6 * s), (x - 18 * s, y + 26 * s)], fill=col, width=int(6 * s))
    d.line([(x - 1 * s, y - 14 * s), (x + 16 * s, y - 2 * s)], fill=col, width=int(5 * s))
    d.line([(x - 1 * s, y - 14 * s), (x - 16 * s, y - 20 * s)], fill=col, width=int(5 * s))

def tracker(stage):
    def fn(t, dur):
        im = background(t); d = ImageDraw.Draw(im, "RGBA")
        header(d, t, "Same team · same substance", "Positive tests")
        labels = ["Athlete 1", "Athlete 2", "Athlete 3", "Athlete 4"]
        subs = ["International meet", "International meet", "International meet", "Tested by her mom"]
        for i in range(4):
            x = 330 + i * 420; y = 640
            lit_t = 0.5 + i * 0.7 if stage == 3 else (0.2 if i < 3 else 1.0)
            lit = i < stage and t >= lit_t
            k = eback(seg(t, lit_t, lit_t + 0.35)) if lit else 0
            col = (RED if i < 3 else ORANGE) if lit else DIM
            d.ellipse([x - 120, y - 150, x + 120, y + 90], fill=(24, 25, 30), outline=col, width=5)
            _runner(d, x, y - 20, 2.6, col if lit else (70, 74, 84))
            text(d, (x, y + 130), labels[i].upper(), 36, WHITE if lit else GREY, "Black", anchor="mt")
            if lit:
                text(d, (x, y + 180), subs[i].upper(), 24, col, "Bold", anchor="mt", alpha=min(1, k))
                f = gfx.font("Black", int(40 * (2 - min(1, k))))
                d.text((x, y - 190), "POSITIVE", font=f, fill=col, anchor="mm")
        cnt = sum(1 for i in range(stage) if t >= (0.5 + i * 0.7 if stage == 3 else (0.2 if i < 3 else 1.0)))
        text(d, (1810, 100), str(cnt), 150, ORANGE, "Black", anchor="ra")
        text(d, (1810, 270), "AND COUNTING" if stage == 4 else "AND NOBODY ASKED WHY", 26, GREY, "Bold", anchor="ra")
        return im
    return fn

def team_grid(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "His theory", "Who got caught?")
    cols, rows = 8, 3
    caught, private = {2, 9, 19}, {13}
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            x = 170 + c * 140; y = 420 + r * 190
            k = eo(seg(t, 0.2 + i * 0.03, 0.5 + i * 0.03))
            if k <= 0: continue
            col = (80, 84, 94)
            if t > 1.8 and i in caught: col = RED
            if t > 2.4 and i in private: col = ORANGE
            _runner(d, x, y + int((1 - k) * 30), 2.0, col)
    leg = [(RED, "Tested at international meets", "CAUGHT", 1.8), (ORANGE, "Tested privately by a parent", "CAUGHT", 2.4),
           (GREY, "Rest of the team", "NEVER TESTED", 3.0)]
    for i, (col, s, tag, t0) in enumerate(leg):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 440 + i * 150
        d.rectangle([1380, y, 1400, y + 90], fill=col)
        text(d, (1425, y + 4), tag, 40, col, "Black", alpha=k)
        text(d, (1425, y + 56), s.upper(), 22, WHITE, "Bold", alpha=k)
    return im

GRAPHICS = {
    "florida_map": florida_map, "world_routes": world_routes, "converge": converge,
    "africa_target": africa_target, "stepper": stepper, "definition": definition,
    "relationship": relationship, "deal_timeline": deal_timeline, "jadco_vs_aiu": jadco_vs_aiu,
    "gw1516": gw1516, "tracker3": tracker(3), "tracker4": tracker(4), "team_grid": team_grid,
}

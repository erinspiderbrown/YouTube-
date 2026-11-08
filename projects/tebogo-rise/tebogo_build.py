"""The Rise of Letsile Tebogo: full documentary edit, African look.

Look: warm golden grade, Botswana flag palette (light blue / black / white) with gold, basket-weave triangle bands
on cards and lower thirds, animated Africa map (Kanye pin, Namibia, the continent lighting up), real race footage.
Sound: kalimba origins bed -> amapiano rise bed -> kalimba grief bed -> drums + choir triumph bed, ducked under the
voice; djembe/talking drum/kalimba/shaker/drum boom SFX and crowd ululation under the homecoming.

EDL times are written in VO v1 seconds (vo_v1_words.json) and mapped through T() onto VO v2, which has
"seventeen years old" and "at seventeen" cut out (he was 18 at the 2021 World U20s).

Run:  python3 projects/tebogo-rise/tebogo_build.py [stage ...]   stages: shots concat audio mux (default all)
"""
import os, sys, json, math, subprocess, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/tebogo-rise"
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
TB = f"{SCR}/tebogo"; REAL = f"{TB}/real"; R = f"{TB}/render"; SFXD = f"{TB}/sfx"
for d in ("ov", "shots", "cards", "maps"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO_VER = int(os.environ.get("VO_VER", "3"))
VO = f"{P}/tebogo_voiceover_v{VO_VER}.wav"
OUT = f"{SCR}/output/Tebogo_Rise_v{VO_VER}.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"; INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GOLD, BLUE, DEEP, RED = (242, 179, 61), (117, 170, 219), (14, 10, 6), (220, 60, 40)

# EDL times are VO v1 seconds. v2 = v1 with two cuts; v3 = full street/chill re-record (script_v3.md), mapped by
# aligning the two whisper transcripts word by word (difflib), plus manual anchors around the new "Botswana before him".
CUTS = [(78.30, 79.95), (390.20, 391.45)]
def _w(v): return json.load(open(f"{P}/vo_v{v}_words.json"))[0]["words"]
def _tok(w): return "".join(ch for ch in w.lower() if ch.isalnum())
def _anchors():
    import difflib
    a, b = _w(1), _w(VO_VER); ta, tb = [_tok(x["w"]) for x in a], [_tok(x["w"]) for x in b]
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False); P_ = [(0.0, 0.0)]
    for blk in sm.get_matching_blocks():
        if blk.size < 2: continue
        for k in range(blk.size):
            y = b[blk.b + k]["s"]
            if not (B0 - 0.5 <= y <= B1 + 0.5): P_.append((a[blk.a + k]["s"], y))
    P_ += EXTRA_ANCHORS; P_.sort(); out = [P_[0]]
    for x, y in P_[1:]:
        if x > out[-1][0] + 1e-3 and y > out[-1][1] + 1e-3: out.append((x, y))
    out.append((a[-1]["e"] + 10, b[-1]["e"] + 10)); return out
def _find(words, phrase, after=0.0):
    p = [_tok(x) for x in phrase.split()]; t = [_tok(x["w"]) for x in words]
    for i in range(len(t) - len(p) + 1):
        if t[i:i + len(p)] == p and words[i]["s"] >= after: return words[i]["s"]
    raise KeyError(phrase)
if VO_VER >= 3:
    W3 = _w(VO_VER)
    B0 = _find(W3, "now peep where") - 0.25          # start of "Botswana before him" (raw v3 time)
    B1 = _find(W3, "nairobi", B0) - 1.6              # "Twenty twenty-one. Nairobi" -> back to the mapped edit
    EXTRA_ANCHORS = [(71.95, B0 - 0.05), (74.10, B1)]
    _A = _anchors(); _AX = np.array([p[0] for p in _A]); _AY = np.array([p[1] for p in _A])
    def T(x): return float(np.interp(x, _AX, _AY))
    END = W3[-1]["e"] + 3.4
else:
    def T(x):
        s = 0.0
        for a, b in CUTS:
            if x >= b: s += b - a
            elif x > a: s += x - a
        return x - s
    END = T(421.2) + 3.4

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: print(" ".join(map(str, cmd))[:800]); print(r.stderr[-2500:]); raise SystemExit(1)
    return r

def F(path, size): return ImageFont.truetype(path, size)
def ease(u): return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, u)))

# ------------------------------------------------------------------ African graphic language
def weave(w, h=30, alpha=255):
    """Botswana-basket style band: alternating up/down triangles in black, gold and blue."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = h
    cols = [GOLD, BLACK, BLUE, BLACK]
    for k, x in enumerate(range(-s, w + s, s)):
        d.polygon([(x, h), (x + s / 2, 0), (x + s, h)], fill=cols[k % 4] + (alpha,))
        d.polygon([(x + s / 2, 0), (x + s, h), (x + 1.5 * s, 0)], fill=(DEEP if k % 2 else (250, 240, 220)) + (alpha,))
    d.line([(0, 0), (w, 0)], fill=GOLD + (alpha,), width=3); d.line([(0, h - 2), (w, h - 2)], fill=GOLD + (alpha,), width=3)
    return im

def flag_bar(w, h):
    """Botswana flag stripes laid horizontally: blue / white / black / white / blue."""
    im = Image.new("RGBA", (w, h), BLUE + (255,)); d = ImageDraw.Draw(im)
    d.rectangle([0, int(h * 0.36), w, int(h * 0.64)], fill=WHITE); d.rectangle([0, int(h * 0.42), w, int(h * 0.58)], fill=BLACK)
    return im

def stroke_text(d, xy, s, font, fill, stroke=8, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))

def shadowed(layer):
    a = layer.split()[-1]; sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.6))))
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0)); out.alpha_composite(sh, (6, 10)); out.alpha_composite(layer); return out

def fit_font(text, path, size, maxw):
    while F(path, size).getlength(text) > maxw and size > 30: size -= 4
    return F(path, size)

def make_overlay(spec):
    kind = spec[0]; im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "pop":  # ("pop", text, colour, pos, size)
        _, text, col, pos, size = spec; f = fit_font(text, ANTON, size, W - 200)
        xy, anc = {"c": ((W // 2, Hh // 2), "mm"), "b": ((W // 2, Hh - 170), "mm"), "t": ((W // 2, 150), "mm"),
                   "l": ((100, Hh // 2), "lm"), "bl": ((100, Hh - 190), "lm"), "tl": ((100, 160), "lm")}[pos]
        stroke_text(d, xy, text, f, tuple(col), max(6, size // 14), anc)
        bb = d.textbbox(xy, text, font=f, anchor=anc)
        im.alpha_composite(flag_bar(bb[2] - bb[0], 16), (bb[0], bb[3] + 18))
        return shadowed(im)
    if kind == "stat":  # ("stat", big, label)
        _, big, label = spec
        stroke_text(d, (100, 560), big, fit_font(big, ANTON, 250, 1300), GOLD, 12, "ls")
        f = fit_font(label, ANTON, 76, 1300); lw = int(f.getlength(label))
        d.rectangle([80, 590, 140 + lw, 690], fill=(0, 0, 0, 215)); d.text((110, 640), label, font=f, fill=WHITE, anchor="lm")
        im.alpha_composite(weave(lw + 60, 22), (80, 690)); return shadowed(im)
    if kind == "list":  # ("list", [lines])
        _, lines = spec
        for j, l in enumerate(lines):
            f = fit_font(l, ANTON, 110, 1600); y = 330 + j * 150
            stroke_text(d, (100, y), l, f, GOLD if j == len(lines) - 1 else WHITE, 8, "lm")
        return shadowed(im)
    if kind == "year":  # ("year", text)
        _, yr = spec; f = fit_font(yr, ANTON, 220, 1500); stroke_text(d, (W // 2, 180), yr, f, GOLD, 12, "mm")
        tw = int(f.getlength(yr)) + 120; im.alpha_composite(weave(tw, 30), ((W - tw) // 2, 320)); return shadowed(im)
    if kind == "name":  # ("name", name, sub)
        _, name, sub = spec; f = fit_font(name, ANTON, 120, 1300); nw = int(f.getlength(name))
        bw = max(nw, int(F(ANTON, 52).getlength(sub))) + 170
        d.rectangle([0, Hh - 310, bw, Hh - 130], fill=(0, 0, 0, 215))
        im.alpha_composite(flag_bar(26, 260).rotate(0, expand=True), (0, Hh - 310))
        d.text((70, Hh - 230), name, font=f, fill=WHITE, anchor="lm")
        d.rectangle([0, Hh - 130, bw, Hh - 60], fill=GOLD + (240,))
        d.text((70, Hh - 95), sub, font=F(ANTON, 52), fill=BLACK, anchor="lm")
        im.alpha_composite(weave(bw, 24), (0, Hh - 334)); return shadowed(im)
    if kind == "quote":  # ("quote", [lines], source)
        _, lines, source = spec; f = F(INTER, 64); lh = 96
        bw = max(int(f.getlength(l)) for l in lines) + 240; bh = len(lines) * lh + 250
        x0, y0 = (W - bw) // 2, (Hh - bh) // 2
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(12, 9, 6, 238))
        im.alpha_composite(weave(bw, 30), (x0, y0 - 30)); im.alpha_composite(weave(bw, 30), (x0, y0 + bh))
        d.text((x0 + 26, y0 - 20), "“", font=F(ANTON, 220), fill=GOLD)
        for j, l in enumerate(lines): d.text((x0 + 130, y0 + 95 + j * lh), l, font=f, fill=WHITE)
        d.text((x0 + 130, y0 + bh - 80), source, font=F(INTB, 40), fill=BLUE); return im
    if kind == "tribute":  # ("tribute", text) quiet white serif-free line on black, small
        _, text = spec; f = F(INTB, 64); stroke_text(d, (W // 2, Hh // 2), text, f, WHITE, 0, "mm"); return im
    if kind == "endq":
        _, l1, l2 = spec
        stroke_text(d, (W // 2, 360), l1, fit_font(l1, ANTON, 130, 1700), WHITE, 10, "mm")
        stroke_text(d, (W // 2, 530), l2, fit_font(l2, ANTON, 130, 1700), GOLD, 10, "mm")
        im.alpha_composite(weave(1100, 30), ((W - 1100) // 2, 640))
        stroke_text(d, (W // 2, 760), "LET ME KNOW DOWN BELOW", F(ANTON, 76), WHITE, 6, "mm"); return shadowed(im)
    raise ValueError(kind)

def overlay_png(spec):
    p = f"{R}/ov/{hashlib.md5(json.dumps(spec).encode()).hexdigest()[:12]}.png"
    if not os.path.exists(p): make_overlay(spec).save(p)
    return p

# ------------------------------------------------------------------ Africa map
AFRICA = set("012 024 072 108 120 132 140 148 174 178 180 204 226 231 232 262 266 270 288 324 384 404 426 430 434 450 454 466 "
              "478 480 504 508 516 562 566 624 646 686 694 706 710 716 728 729 732 748 768 788 800 818 834 854 894".split())
_GEO = None
def geo():
    global _GEO
    if _GEO: return _GEO
    t = json.load(open(f"{TB}/geo/countries-50m.json")); sc, tr = t["transform"]["scale"], t["transform"]["translate"]
    arcs = []
    for arc in t["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc: x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        arcs.append(pts)
    def ring(idx):
        out = []
        for i in idx:
            p = arcs[i] if i >= 0 else arcs[~i][::-1]
            out += p[1:] if out else p
        return out
    C = {}
    for g in t["objects"]["countries"]["geometries"]:
        cid = g.get("id"); name = g.get("properties", {}).get("name", "")
        if cid not in AFRICA and name != "Somaliland": continue
        polys = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"] if g["type"] == "MultiPolygon" else []
        rings = [ring(p[0]) for p in polys]
        big = max(rings, key=len); cx = sum(p[0] for p in big) / len(big); cy = sum(p[1] for p in big) / len(big)
        C[cid or name] = dict(name=name, rings=rings, c=(cx, cy))
    _GEO = C; return C

KANYE, GABS, LAGOS = (25.35, -24.98), (25.91, -24.65), (3.38, 6.52)
def map_frame(mode, u, dur):
    """u = seconds into the shot."""
    C = geo(); q = u / dur
    views = {  # (lon, lat, px per degree) start -> end
        "intro": ((17, 3, 9.0), (17, 3, 13.0)), "kanye": ((17, 3, 13.0), (24.3, -22.4, 82.0)),
        "namibia": ((10, -10, 16.0), (6, -21, 38.0)), "light": ((19, 2, 12.5), (19, 2, 14.0)),
        "nigeria": ((18, 0, 13.0), (8, 6, 34.0)), "lit": ((19, 2, 15.0), (19, 2, 12.0))}[mode]
    zq = ease((u - 0.6) / 4.2) if mode == "kanye" else ease(q)
    lon0, lat0, k = [a + (b - a) * zq for a, b in zip(*views)]
    if mode == "kanye": k = views[0][2] * (views[1][2] / views[0][2]) ** zq;
    def P(lon, lat): return (W / 2 + (lon - lon0) * k, Hh / 2 - (lat - lat0) * k)
    im = Image.new("RGB", (W, Hh), DEEP); d = ImageDraw.Draw(im, "RGBA")
    # warm radial background + weave borders
    bg = Image.new("L", (W, Hh), 0); ImageDraw.Draw(bg).ellipse([W * 0.15, -200, W * 0.85, Hh + 200], fill=70)
    im.paste((60, 36, 12), (0, 0), bg.filter(ImageFilter.GaussianBlur(160)))
    lit = {}
    if mode in ("light", "lit", "nigeria"):
        bx, by = C["072"]["c"]; dist = {cid: math.hypot(v["c"][0] - bx, v["c"][1] - by) for cid, v in C.items()}; dmax = max(dist.values())
        for cid in C:
            if mode == "light": lit[cid] = min(1, max(0, (q * 1.15 * dmax - dist[cid]) / 6))
            else: lit[cid] = 0.2 if mode == "nigeria" else 1.0
    draw_in = min(1, u / 1.4) if mode == "intro" else 1
    glow = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for cid, v in C.items():
        hl = None
        if cid == "072" and mode != "intro": hl = BLUE
        if cid == "516" and mode == "namibia": hl = GOLD
        if cid == "566" and mode == "nigeria": hl = GOLD
        for rg in v["rings"]:
            pts = [P(*p) for p in rg]
            if len(pts) < 3: continue
            if hl: fill = hl + (255,)
            elif lit.get(cid): a = lit[cid]; fill = tuple(int(30 + (c - 30) * a * 0.85) for c in GOLD) + (255,)
            else: fill = (34, 26, 18, int(255 * draw_in))
            d.polygon(pts, fill=fill, outline=GOLD + (int(200 * draw_in),))
            if hl or lit.get(cid, 0) > 0.5: gd.polygon(pts, fill=(hl or GOLD) + (150,))
    im = Image.alpha_composite(im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(22))).convert("RGB"); d = ImageDraw.Draw(im, "RGBA")
    # re-stroke borders crisp on top
    for cid, v in C.items():
        for rg in v["rings"]:
            pts = [P(*p) for p in rg]
            if len(pts) >= 3: d.line(pts + [pts[0]], fill=GOLD + (int(170 * draw_in),), width=2 if k < 40 else 3)
    def label(lon, lat, text, col, size=64, dy=0):
        x, y = P(lon, lat); stroke_text(d, (x, y + dy), text, F(ANTON, size), col, 6, "mm")
    def pin(lon, lat, text, a):
        if a <= 0: return
        x, y = P(lon, lat); r = 14 + 10 * math.sin(u * 6) ** 2
        d.ellipse([x - r - 12, y - r - 12, x + r + 12, y + r + 12], outline=GOLD + (int(160 * a),), width=4)
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=WHITE + (int(255 * a),), outline=BLACK, width=3)
        stroke_text(d, (x + 34, y - 6), text, F(ANTON, 70), WHITE, 6, "lm")
    if mode == "kanye":
        if zq > 0.35: label(*C["072"]["c"], "BOTSWANA", WHITE, 78, dy=-120 * min(1, k / 82))
        pin(*GABS, "GABORONE", min(1, (u - 5.0) / 0.4) * 0.0)  # capital kept unlabelled to keep focus on Kanye
        pin(*KANYE, "KANYE", min(1, (u - 5.2) / 0.4))
    if mode == "namibia":
        nx, ny = C["516"]["c"]; bx, by = C["072"]["c"]
        label(nx - 1.0, ny - 4.5, "NAMIBIA", WHITE, 64); label(bx + 0.8, by + 0.2, "BOTSWANA", WHITE, 40)
    if mode == "nigeria":
        label(*C["566"]["c"], "NIGERIA", WHITE, 60); label(*C["072"]["c"], "BOTSWANA", WHITE, 30)
    if mode in ("light", "lit"): label(*C["072"]["c"], "BOTSWANA", WHITE, 30)
    im = im.convert("RGBA")
    im.alpha_composite(weave(W, 34), (0, 0)); im.alpha_composite(weave(W, 34).rotate(180), (0, Hh - 34))
    return im.convert("RGB")

def map_clip(mode, dur):
    n = int(round(dur * FPS)); out = f"{R}/maps/{mode}_{n}.mp4"
    if os.path.exists(out): return out
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{Hh}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(map_frame(mode, i / FPS, dur).tobytes())
    p.stdin.close(); p.wait(); return out

# ------------------------------------------------------------------ edit decision list (VO v1 seconds)
PH = {"douala": f"{TB}/photos/c00.jpg", "gabs": f"{TB}/photos/c01.jpg", "kanye_road": f"{TB}/photos/c02.jpg",
      "paris_jo": f"{TB}/photos/c06.jpg", "laus1": f"{TB}/photos/c08.jpg", "laus2": f"{TB}/photos/c09.jpg",
      "laus3": f"{TB}/commons/c20.jpg", "bislett": f"{TB}/src/bislett_smile.jpg",
      "bud_flag": f"{TB}/src/bud_flag.png", "bud_face": f"{TB}/src/bud_face.png", "bud_face2": f"{TB}/src/bud_face2.png",
      "u20_board": f"{TB}/src/u20_board.png"}
def c(t, src, ss=0, **o): return dict(t=t, src=src, ss=ss, **o)
SHOTS = [
    # 01 cold open
    c(0.0, "paris100", 24, amb=1), c(4.74, "paris100", 0.5), c(5.28, "paris100", 4.9), c(6.28, "paris100", 13), c(7.24, "paris100", 19),
    c(8.64, "MAP", mode="intro"),
    c(18.16, "paris200", 5, amb=1), c(21.12, "paris200", 28, amb=1), c(23.62, "paris200", 41.5, amb=1),
    c(28.36, "paris200", 119, amb=1), c(33.46, "nairobi2021", 21.2, sp=0.6), c(35.6, "budapest100", 393),
    c(37.8, "paris200", 156), c(39.8, "homecoming", 103, amb=1),
    # 02 who he is
    c(42.34, "MAP", mode="kanye"), c(49.84, "PHOTO", photo="kanye_road"), c(53.2, "PHOTO", photo="douala"),
    c(59.28, "PHOTO", photo="gabs"), c(65.22, "PHOTO", photo="bud_flag"),
    # 03 World U20s
    c(74.18, "nairobi2021", 0, amb=1), c(78.3, "nairobi2021", 7.5, amb=1), c(81.32, "nairobi2021", 20.6, sp=0.55),
    c(86.46, "CARD", base=("cali2022", 34)), c(90.84, "PHOTO", photo="bud_face2"), c(96.42, "CARD", base=("nairobi2021", 16)),
    c(105.22, "cali2022", 0.5, amb=1), c(109.88, "cali2022", 4.5, amb=1), c(112.64, "cali2022", 9.2, amb=1),
    c(115.04, "cali2022", 13, amb=1), c(118.68, "cali2022", 32.5, amb=1), c(121.24, "cali2022", 22, amb=1),
    c(125.64, "PHOTO", photo="u20_board"), c(126.78, "nairobi2021", 21.0, sp=0.5), c(130.46, "MAPSTILL", mode="kanye"),
    # 04 Budapest 2023
    c(135.18, "budapest100", 65, amb=1), c(139.84, "budapest100", 230, amb=1), c(143.68, "budapest100", 240, amb=1),
    c(148.64, "budapest100", 252, amb=1), c(152.96, "budapest100", 393, amb=1), c(158.4, "budapest200", 0, vert=1, amb=1),
    c(162.36, "CARD", base=("budapest200", 4), red=1), c(166.54, "budapest200", 8, vert=1, amb=1),
    c(169.36, "PHOTO", photo="bud_face"), c(172.44, "budapest100", 442, amb=1),
    # 05 road to Paris + his mother
    c(179.74, "teb300", 15, amb=1), c(184.52, "teb300", 87, amb=1), c(188.9, "CARD", base=("teb300", 45)),
    c(191.34, "PHOTO", photo="douala"),
    c(196.56, "BLACK"), c(199.58, "PHOTO", photo="bud_face2", bw=1), c(204.54, "BLACK"), c(210.46, "CARD", base=("paris200", 124), bw=1),
    c(215.96, "PHOTO", photo="bud_face", bw=1), c(217.84, "PHOTO", photo="paris_jo"),
    c(222.66, "paris200", 123.2, sp=0.6), c(224.78, "paris200", 119, sp=0.7),
    # 06 Paris
    c(228.46, "paris100", 12, amb=1), c(230.2, "paris100", 47, amb=1), c(234.34, "paris200", 5, amb=1),
    c(237.86, "paris200", 14, amb=1), c(239.16, "paris200", 29, amb=1), c(242.52, "MAP", mode="namibia"), c(249.96, "paris200", 45, amb=1),
    c(253.44, "paris200", 50.5, amb=1), c(257.8, "paris200", 80, amb=1), c(260.9, "paris200", 119, amb=1),
    c(264.52, "paris200", 147, amb=1), c(267.98, "paris200", 156, amb=1),
    # 07 Africa
    c(274.04, "homecoming", 21, amb=1), c(279.46, "homecoming", 103, amb=1), c(284.06, "MAP", mode="light"),
    c(289.14, "CARD", base=("homecoming", 60)), c(296.34, "homecoming", 76, amb=1), c(301.5, "homecoming", 45, amb=1),
    c(307.38, "PHOTO", photo="laus1"),
    # 08 the generation
    c(312.4, "tokyo4x4", 34, amb=1), c(314.94, "tokyo4x4", 0, amb=1), c(318.44, "CARD", base=("tokyo4x4", 500)),
    c(322.18, "keb400", 0, amb=1), c(328.98, "keb400", 29, amb=1), c(331.74, "keb400", 18, amb=1),
    c(335.46, "tokyo4x4s", 30, amb=1), c(338.72, "tokyo4x4s", 47, amb=1),
    c(341.36, "gaborone4x4", 2917, amb=1), c(347.98, "gaborone4x4", 2700, amb=1), c(351.96, "gaborone4x4", 3040, amb=1),
    c(355.06, "gaborone4x4", 3222, amb=1), c(357.04, "MAP", mode="nigeria"), c(365.14, "gaborone4x4", 3200, amb=1),
    # 09 the weight
    c(369.3, "PHOTO", photo="laus2"), c(373.64, "PHOTO", photo="laus3"), c(378.02, "CARD", base=("budapest100", 556)),
    # 10 close
    c(386.28, "paris200", 156), c(388.62, "nairobi2021", 20.8, sp=0.55), c(391.98, "budapest100", 393), c(394.14, "paris200", 119),
    c(396.58, "paris200", 90), c(400.34, "paris200", 124), c(402.32, "homecoming", 21), c(404.12, "MAP", mode="lit"),
    c(407.42, "gaborone4x4", 2720), c(412.5, "PHOTO", photo="bislett"), c(414.68, "CARD", base=("paris200", 156)),
]
for s in SHOTS: s["t"] = round(T(s["t"]), 3)
if VO_VER >= 3:  # "Botswana before him" (only in v3): placed at raw v3 times found in the transcript
    f = lambda p: _find(W3, p, B0 - 1)
    SHOTS += [dict(t=B0, src="PHOTO", photo="gabs"), dict(t=f("country under") - 0.2, src="PHOTO", photo="kanye_road"),
              dict(t=f("before paris") - 0.2, src="CARD", base=("gaborone4x4", 2930)),
              dict(t=f("amos") - 0.5, src="CARD", base=("gaborone4x4", 3200)),
              dict(t=f("one world") - 0.2, src="CARD", base=("homecoming", 103)),
              dict(t=f("but a real") - 0.2, src="MAPSTILL", mode="kanye"),
              dict(t=f("thats where he") - 0.2, src="PHOTO", photo="douala")]
    SHOTS.sort(key=lambda s: s["t"])

def pop(t0, t1, text, col=WHITE, pos="c", size=150): return (t0, t1, ("pop", text, list(col), pos, size))
OVER = [
    pop(4.74, 5.25, "USA", pos="b"), pop(5.3, 6.2, "JAMAICA", pos="b"),
    pop(6.28, 7.2, "CANADA", pos="b"), pop(7.24, 8.6, "GREAT BRITAIN", pos="b"),
    pop(9.4, 11.0, "DISTANCE", GOLD, "b", 170), pop(11.08, 12.8, "MARATHONS", GOLD, "b", 170),
    (12.84, 18.1, ("stat", "1908", "LAST AFRICAN MAN TO WIN AN OLYMPIC SPRINT")),
    (18.16, 21.0, ("year", "AUG 8, 2024")), pop(21.12, 23.5, "OLYMPIC 200M FINAL", pos="b", size=120),
    (25.6, 28.3, ("stat", "19.46", "OLYMPIC 200M")), pop(28.36, 33.3, "FIRST AFRICAN EVER", GOLD, "b", 150),
    (42.4, 49.7, ("name", "LETSILE TEBOGO", "BORN JUNE 7, 2003 · KANYE, BOTSWANA")),
    pop(49.84, 53.1, "SOCCER FIRST", WHITE, "b", 140), pop(53.4, 59.1, "HIS MOM, SERATIWA", WHITE, "b", 110),
    pop(59.28, 61.4, "2019", GOLD, "t", 170), (61.6, 65.1, ("name", "KEBONYEMODISA MOSIMANYANE", "HIS COACH THEN · HIS COACH NOW")),
    pop(68.0, 70.4, "NO U.S. COLLEGE", WHITE, "b", 130), pop(70.54, 71.85, "STAYED IN BOTSWANA", GOLD, "b", 130),
    (74.18, 77.9, ("year", "2021")), pop(75.0, 77.9, "NAIROBI, KENYA · WORLD U20s", WHITE, "b", 90),
    pop(79.95, 81.3, "AGE 18", GOLD, "tl", 130), pop(80.1, 86.4, "WORLD U20 100M CHAMPION", GOLD, "b", 110),
    (86.46, 90.7, ("year", "2022")), (88.2, 90.7, ("stat", "9.96", "GABORONE · APRIL 2022")),
    pop(90.84, 93.6, "FIRST BOTSWANA MAN UNDER 10", GOLD, "b", 110), pop(93.8, 96.3, "WORLD U20 RECORD", WHITE, "b", 120),
    pop(96.42, 99.1, "EUGENE · SENIOR WORLDS", WHITE, "t", 110), (99.22, 105.1, ("stat", "9.94", "HEAT · AGAINST GROWN MEN")),
    pop(105.22, 109.8, "CALI, COLOMBIA · WORLD U20s", WHITE, "b", 100),
    (118.68, 121.2, ("stat", "9.91", "WORLD U20 RECORD")), pop(121.24, 122.8, "SHOWBOATING?", WHITE, "b", 140),
    pop(125.64, 126.7, "YOUNG BOLT", GOLD, "c", 230), pop(130.46, 135.0, "A COUNTRY THAT NEVER HAD ONE", GOLD, "b", 110),
    (139.84, 143.6, ("year", "2023")), pop(140.4, 143.6, "WORLD CHAMPIONSHIPS · BUDAPEST", WHITE, "b", 90),
    pop(144.54, 148.5, "NOAH LYLES", WHITE, "bl", 110), (148.64, 152.9, ("stat", "9.88", "SILVER · NATIONAL RECORD")),
    pop(152.96, 158.3, "FIRST AFRICAN MAN · WORLD 100M MEDAL", GOLD, "b", 90),
    pop(158.4, 162.3, "5 DAYS LATER · 200M", WHITE, "t", 100), pop(164.96, 166.5, "GRADE 1 TEAR", (255, 90, 70), "c", 200),
    pop(168.4, 169.3, "BRONZE", GOLD, "c", 220), (169.36, 172.4, ("list", ["20 YEARS OLD", "HURT", "2 WORLD MEDALS"])),
    (184.52, 188.8, ("stat", "30.69", "300M · WORLD BEST")), (189.4, 191.3, ("stat", "44.29", "400M")),
    pop(192.32, 196.4, "AFRICA'S SPRINT FAVORITE", GOLD, "b", 110),
    (196.6, 199.5, ("tribute", "MAY 19, 2024")),
    (204.6, 210.4, ("tribute", "He found out on social media.")),
    (210.6, 215.9, ("quote", ["When my mother passed away,", "I thought it was the end of my career."], "LETSILE TEBOGO")),
    pop(222.66, 224.7, "HER BIRTHDAY ON HIS SPIKES", WHITE, "b", 100), pop(224.78, 228.3, "HER INITIALS ON HIS NAILS", WHITE, "b", 100),
    (228.46, 230.1, ("year", "PARIS 2024")), (230.4, 234.2, ("stat", "9.86", "100M · 6TH · NATIONAL RECORD")),
    (234.34, 237.7, ("year", "AUG 8 · 200M FINAL")), pop(237.86, 239.1, "KENNY BEDNAREK", WHITE, "bl", 110),
    pop(239.16, 242.4, "NOAH LYLES", WHITE, "bl", 110),
    (244.54, 248.6, ("stat", "4× SILVER", "FRANKIE FREDERICKS · NAMIBIA · 1992 & 1996")),
    pop(248.76, 249.9, "NEVER GOLD", GOLD, "c", 200),
    (253.44, 257.7, ("stat", "19.46", "AFRICAN RECORD · 5TH FASTEST EVER")),
    pop(260.9, 264.4, "FIRST AFRICAN OLYMPIC 200M CHAMPION", GOLD, "b", 90),
    pop(264.52, 267.9, "BOTSWANA'S FIRST OLYMPIC GOLD", GOLD, "b", 100),
    (268.1, 274.0, ("quote", ["It means a lot to the African continent,", "'cause now they see Africa as a sprinting home."], "LETSILE TEBOGO · PARIS 2024")),
    pop(276.08, 279.4, "WHOLE COUNTRY GETS THE AFTERNOON OFF", WHITE, "b", 90),
    (279.6, 284.0, ("stat", "30,000+", "NATIONAL STADIUM · GABORONE")),
    pop(286.08, 289.0, "ALL OF AFRICA", GOLD, "b", 150),
    pop(293.04, 294.2, "MARATHON", WHITE, "c", 200), pop(294.28, 296.2, "400M AT MOST", WHITE, "c", 200),
    (299.0, 301.4, ("quote", ["Africans can be sprinters too."], "LETSILE TEBOGO")),
    pop(303.04, 304.5, "NOT AMERICA", WHITE, "b", 130), pop(304.62, 306.0, "NOT JAMAICA", WHITE, "b", 130),
    pop(306.04, 307.3, "FROM HOME", GOLD, "b", 150), (308.0, 312.3, ("stat", "2024", "WORLD ATHLETICS MALE ATHLETE OF THE YEAR")),
    (314.94, 318.3, ("year", "2025 · TOKYO")), (318.44, 322.1, ("list", ["100M: FALSE START", "200M: 4TH"])),
    (322.4, 327.4, ("name", "COLLEN KEBINATSHIPI", "BOTSWANA · AGE 21")), (327.46, 331.6, ("stat", "43.53", "WORLD 400M CHAMPION")),
    (331.8, 335.3, ("name", "BAYAPO NDORI", "BOTSWANA · 400M BRONZE")),
    pop(336.92, 338.6, "TEBOGO · 2ND LEG", WHITE, "b", 110), pop(338.72, 341.3, "WORLD CHAMPIONS", GOLD, "b", 150),
    (341.36, 345.9, ("year", "2026")), pop(342.6, 345.9, "WORLD RELAYS · FIRST TIME IN AFRICA", WHITE, "b", 90),
    pop(346.12, 347.9, "GABORONE, BOTSWANA", GOLD, "b", 120),
    pop(355.06, 356.0, "GOLD", GOLD, "c", 220), pop(356.14, 357.0, "AFRICAN RECORD", WHITE, "b", 130),
    (360.44, 365.0, ("name", "KANYINSOLA AJAYI", "NIGERIA · 2026")),
    pop(365.14, 369.2, "AFRICA: A SPRINTING HOME", GOLD, "b", 120),
    (378.1, 386.1, ("quote", ["I carry so many hopes and lives behind my back,", "so it is just too much.", "But we will go through it."], "LETSILE TEBOGO · SEPT 2026")),
    (388.62, 391.9, ("list", ["WORLD U20 CHAMP AT 18"])), (391.98, 394.1, ("list", ["WORLD U20 CHAMP AT 18", "2 WORLD MEDALS AT 20"])),
    (394.14, 396.5, ("list", ["WORLD U20 CHAMP AT 18", "2 WORLD MEDALS AT 20", "OLYMPIC CHAMPION AT 21"])),
    pop(396.58, 400.2, "FIRST AFRICAN OLYMPIC 200M CHAMPION", GOLD, "b", 90),
    pop(400.34, 402.2, "FOR HIS MOM", WHITE, "b", 130), pop(402.32, 404.0, "FOR BOTSWANA", BLUE, "b", 130),
    pop(404.12, 407.3, "FOR ALL OF AFRICA", GOLD, "b", 140), pop(407.6, 412.4, "FROM KANYE TO LAGOS", WHITE, "b", 120),
    (414.68, 999, ("endq", "IS TEBOGO THE BIGGEST THING", "TO HAPPEN TO AFRICAN SPRINTING?")),
]
OVER = [(round(T(a), 3), round(min(T(b), END), 3), s) for a, b, s in OVER]
if VO_VER >= 3:
    f = lambda p: _find(W3, p, B0 - 1)
    OVER += [(B0, f("country under") - 0.3, ("pop", "BOTSWANA BEFORE HIM", list(GOLD), "b", 130)),
             (f("country under"), f("before paris") - 0.3, ("list", ["UNDER 3 MILLION PEOPLE", "MOSTLY DESERT"])),
             (f("before paris"), f("amos") - 0.6, ("stat", "2", "OLYMPIC MEDALS BEFORE PARIS")),
             (f("amos") - 0.3, f("and a") - 0.1, ("name", "NIJEL AMOS", "800M SILVER \u00b7 LONDON 2012")),
             (f("and a"), f("one world") - 0.3, ("pop", "4\u00d7400 BRONZE \u00b7 TOKYO 2020", list(WHITE), "b", 110)),
             (f("one world"), f("but a real") - 0.3, ("name", "AMANTLE MONTSHO", "WORLD 400M CHAMPION \u00b7 2011")),
             (f("but a real") + 0.3, f("thats where he") - 0.3, ("pop", "A REAL SPRINTER? NEVER.", list(GOLD), "b", 130))]
    OVER.sort(key=lambda o: o[0])

GRADE = "colorbalance=rs=0.06:gs=0.015:bs=-0.07:rm=0.04:bm=-0.04,eq=contrast=1.07:saturation=1.14:gamma=0.98,vignette=PI/5"
def card_base(src, ss, out, bw=False, red=False):
    if not os.path.exists(out):
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", f"{REAL}/{src}.mp4", "-frames:v", "1", out])
    im = Image.open(out).convert("RGB")
    im = ImageOps.fit(im, (W, Hh)).filter(ImageFilter.GaussianBlur(12))
    if bw: im = ImageOps.grayscale(im).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.38)
    tint = Image.new("RGB", (W, Hh), (120, 20, 10) if red else (70, 40, 10)); im = Image.blend(im, tint, 0.22)
    im = im.convert("RGBA")
    if not bw: im.alpha_composite(weave(W, 34), (0, 0)); im.alpha_composite(weave(W, 34).rotate(180), (0, Hh - 34))
    return im.convert("RGB")

def photo_card(name, out, bw=False):
    im = Image.open(PH[name]).convert("RGB"); im = ImageOps.exif_transpose(im)
    if bw: im = ImageOps.grayscale(im).convert("RGB")
    bg = ImageOps.fit(im, (W, Hh)).filter(ImageFilter.GaussianBlur(30)); bg = ImageEnhance.Brightness(bg).enhance(0.45).convert("RGBA")
    fg = im.copy(); fg.thumbnail((1600, 900))
    if fg.height < 900: fg = fg.resize((int(fg.width * 900 / fg.height), 900))
    if fg.width > 1700: fg = fg.resize((1700, int(fg.height * 1700 / fg.width)))
    x, y = (W - fg.width) // 2, (Hh - fg.height) // 2 - 10
    d = ImageDraw.Draw(bg); d.rectangle([x - 10, y - 10, x + fg.width + 10, y + fg.height + 10], fill=(GOLD if not bw else (200, 200, 200)) + (255,))
    bg.alpha_composite(fg.convert("RGBA"), (x, y))
    if not bw: bg.alpha_composite(weave(fg.width + 20, 26), (x - 10, y + fg.height + 10))
    bg.convert("RGB").save(out)

def render_shot(i, sh, t1):
    out = f"{R}/shots/{i:03d}.mp4"
    dur = (round(t1 * FPS) - round(sh["t"] * FPS)) / FPS
    key = json.dumps([sh, dur, GRADE, [o for o in OVER if o[0] < t1 and o[1] > sh["t"]]], sort_keys=True, default=str)
    stamp = f"{out}.key"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == key: return out
    src = sh["src"]; amb = False
    if src in ("MAP", "MAPSTILL"):
        if src == "MAP": f = map_clip(sh["mode"], dur)
        else:
            f = f"{R}/maps/still_{sh['mode']}.png"; map_frame(sh["mode"], 7.5, 7.5).save(f)
        ins = ["-i", f] if src == "MAP" else ["-loop", "1", "-t", str(dur), "-i", f]
        base = f"[0:v]scale='trunc(1920*(1+0.03*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1" if src == "MAPSTILL" else "[0:v]scale=1920:1080,setsar=1"
    elif src == "BLACK":
        ins = ["-f", "lavfi", "-t", str(dur), "-i", f"color=c=black:s=1920x1080:r=24"]; base = "[0:v]setsar=1"
    elif src == "CARD":
        cb = f"{R}/cards/{i:03d}.png"; card_base(*sh["base"], f"{R}/cards/{sh['base'][0]}_{sh['base'][1]}.png", sh.get("bw"), sh.get("red")).save(cb)
        ins = ["-loop", "1", "-t", str(dur), "-i", cb]; base = f"[0:v]scale='trunc(1920*(1+0.05*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1"
    elif src == "PHOTO":
        pc = f"{R}/cards/ph_{sh['photo']}{'_bw' if sh.get('bw') else ''}.png"
        if not os.path.exists(pc): photo_card(sh["photo"], pc, sh.get("bw"))
        ins = ["-loop", "1", "-t", str(dur), "-i", pc]
        base = f"[0:v]scale='trunc(1920*(1+0.045*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1"
        if not sh.get("bw"): base += ",colorbalance=rs=0.03:bs=-0.03"
    else:
        sp = sh.get("sp", 1.0); sdur = dur * sp + 0.1
        ins = ["-ss", str(sh["ss"]), "-t", f"{sdur:.3f}", "-i", f"{REAL}/{src}.mp4"]
        if sh.get("vert"):
            base = (f"[0:v]setpts=(PTS-STARTPTS)/{sp},split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=28,eq=brightness=-0.22[bg];"
                    "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1")
        else:
            z = 0.05
            base = (f"[0:v]setpts=(PTS-STARTPTS)/{sp},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                    f"scale='trunc(1920*(1+{z}*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1")
        base += ",hue=s=0,eq=contrast=1.2" if sh.get("bw") else "," + GRADE
        amb = bool(sh.get("amb")) and sp == 1.0
    vf = [base + ",fps=24,format=yuva420p[b0]"]; k = 0
    for (o0, o1, spec) in OVER:
        if o0 >= t1 or o1 <= sh["t"]: continue
        a, b = max(0, o0 - sh["t"]), min(dur, o1 - sh["t"]); png = overlay_png(spec); k += 1
        ins += ["-loop", "1", "-t", f"{b:.3f}", "-i", png]
        fin = 0.18 if o0 >= sh["t"] else 0; fout = 0.18 if o1 <= t1 else 0
        chain = f"[{k}:v]format=rgba"
        if fin: chain += f",fade=in:st={a:.3f}:d={fin}:alpha=1"
        if fout: chain += f",fade=out:st={b - fout:.3f}:d={fout}:alpha=1"
        slide = f"if(lt(t-{a:.3f},0.24),40*(1-(t-{a:.3f})/0.24),0)" if fin and spec[0] not in ("tribute", "quote") else "0"
        vf.append(chain + f"[o{k}];[b{k - 1}][o{k}]overlay=x=0:y='{slide}':enable='between(t,{a:.3f},{b:.3f})'[b{k}]")
    vf.append(f"[b{k}]format=yuv420p[v]")
    aud = ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    amap = f"{k + 1}:a"
    if amb: vf.append(f"[0:a]aresample=48000,volume=0.2,highpass=f=120,apad=whole_dur={dur}[a]"); amap = "[a]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + ins + aud + ["-filter_complex", ";".join(vf), "-map", "[v]", "-map", amap,
           "-t", str(dur), "-r", "24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-ar", "48000", "-ac", "2", out]
    run(cmd); open(stamp, "w").write(key); return out

def shot_list():
    return [(i, sh, SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END) for i, sh in enumerate(SHOTS)]

def stage_shots():
    from concurrent.futures import ThreadPoolExecutor
    only = os.environ.get("ONLY")  # e.g. ONLY=0-20 for a preview
    todo = shot_list()
    if only: a, b = map(int, only.split("-")); todo = [x for x in todo if a <= x[0] <= b]
    for i, sh, t1 in todo:  # maps first (PIL heavy, sequential)
        if sh["src"] == "MAP": map_clip(sh["mode"], (round(t1 * FPS) - round(sh["t"] * FPS)) / FPS)
    with ThreadPoolExecutor(6) as ex: list(ex.map(lambda a: render_shot(*a), todo))
    print("shots", len(todo))

def stage_concat():
    lst = f"{R}/concat.txt"
    open(lst, "w").write("".join(f"file '{R}/shots/{i:03d}.mp4'\n" for i, _, _ in shot_list()))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/picture.mp4"])
    print("concat", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/picture.mp4"]).stdout.strip(), "END", END)

# ------------------------------------------------------------------ audio
def sfx_list():
    S = []
    for (o0, o1, spec) in OVER:
        k = spec[0]
        if k == "year": S.append((o0 - 0.05, "djembe", 0.55))
        elif k == "stat": S.append((o0 - 0.05, "drumboom", 0.5))
        elif k == "name": S.append((o0 - 0.05, "kalimba", 0.35))
        elif k in ("pop", "list"): S.append((o0 - 0.06, "shaker", 0.22))
        elif k == "quote" and o0 > T(230): S.append((o0 - 0.05, "kalimba", 0.3))
    for sh in SHOTS:
        if sh["src"] == "MAP": S.append((sh["t"], "talkingdrum", 0.45))
    S = [s for s in S if not (T(196.4) < s[0] < T(217.8))]  # silence the grief passage except music
    return S

def bed(path, t0, t1, vol, fin=1.5, fout=2.0, offset=0.0):
    out = f"{R}/bed_{os.path.basename(path)}_{t0:.1f}.wav"; L = t1 - t0; dl = int(t0 * 1000)
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "3", "-ss", str(offset), "-i", path, "-t", f"{L:.2f}", "-af",
         f"volume={vol},afade=t=in:st=0:d={fin},afade=t=out:st={L - fout:.2f}:d={fout},adelay={dl}|{dl},apad=whole_dur={END}",
         "-ar", "48000", "-ac", "2", out]); return out

def stage_audio():
    M = f"{P}/music"
    beds = [bed(f"{M}/origins_kalimba.wav", 0.0, T(75.0), 0.5, fin=0.8, fout=2.5),
            bed(f"{M}/rise_amapiano.wav", T(73.6), T(197.4), 0.42, fin=2.0, fout=2.0),
            bed(f"{M}/grief_kalimba.mp3", T(196.0), T(229.4), 0.55, fin=1.5, fout=2.5),
            bed(f"{M}/triumph_drums_choir.mp3", T(227.6), END, 0.5, fin=2.0, fout=4.0)]
    amb = [bed(f"{SFXD}/savanna_dusk.mp3", T(42.3), T(74.0), 0.35, fin=1.5, fout=2.0),
           bed(f"{SFXD}/crowd_ululation.mp3", T(274.0), T(284.0), 0.32, fin=0.6, fout=1.5),
           bed(f"{SFXD}/crowd_ululation.mp3", T(260.9), T(268.0), 0.26, fin=0.4, fout=1.5),
           bed(f"{SFXD}/crowd_ululation.mp3", T(355.0), T(358.5), 0.26, fin=0.3, fout=1.2)]
    S = sfx_list(); ins = []; fl = []
    nb = len(beds); na = len(amb); base_idx = 2 + nb + na
    for j, (t, n, g) in enumerate(S):
        ins += ["-i", f"{SFXD}/{n}.mp3"]; d = int(max(0, t) * 1000)
        fl.append(f"[{j + base_idx}:a]volume={g},afade=t=out:st=1.6:d=0.6,adelay={d}|{d},aformat=sample_rates=48000:channel_layouts=stereo[s{j}]")
    bed_in = "".join(f"[{2 + j}:a]" for j in range(nb))
    amb_in = "".join(f"[{2 + nb + j}:a]" for j in range(na))
    mix_in = "".join(f"[s{j}]" for j in range(len(S)))
    fc = ";".join(fl) + (";" if fl else "") + \
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];{bed_in}amix=inputs={nb}:normalize=0[music];" \
        f"[vo]asplit=2[vo1][vo2];[music][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=25:release=450[duck];" \
        f"[vo1][duck][1:a]{amb_in}{mix_in}amix=inputs={3 + na + len(S)}:normalize=0:duration=first,alimiter=limit=0.95[out]"
    run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", f"apad=whole_dur={END}", "-ar", "48000", "-ac", "2", f"{R}/vo_pad.wav"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", f"{R}/vo_pad.wav", "-i", f"{R}/picture.mp4"] + sum((["-i", b] for b in beds + amb), []) + ins + \
          ["-filter_complex", fc, "-map", "[out]", "-t", str(END), "-ar", "48000", f"{R}/mix.wav"]
    run(cmd); print("audio", len(S), "sfx")

def stage_mux():
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", str(END), "-movflags", "+faststart", OUT])
    print("wrote", OUT)

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")

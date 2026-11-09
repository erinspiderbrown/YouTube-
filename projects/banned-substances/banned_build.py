"""Every Banned Drug in Track & The Star Who Got Caught Using It: full countdown edit.

Look: the channel's documentary neon (dark navy, cyan + orange glow, red for BANNED), HUD tags on archival footage,
neon countdown cards with the real drug photo for every substance, neon-framed photos for athletes without footage.
Real news / interview soundbites play with their own audio at the [SOUNDBITE] markers in script_v2.md: the voiceover
is split there and the clip is inserted, so every time below is written in raw voiceover seconds (vo_v1_words.json)
and mapped onto the final timeline by FT().

Run:  python3 projects/banned-substances/banned_build.py [stage ...]   stages: shots concat audio mux (default all)
      ONLY=0-30 limits the shots stage to a range (preview).
"""
import os, sys, json, math, subprocess, hashlib, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/banned-substances"
sys.path.insert(0, f"{ROOT}/tools")
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
BS = f"{SCR}/banned"; REAL = f"{BS}/real"; R = f"{BS}/render"
for d in ("ov", "shots", "cards", "sfx", "sb"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/banned_voiceover_v1.wav"
OUT = f"{SCR}/output/Every_Banned_Drug_In_Track_v1.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"; INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
INTB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"; MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
WHITE, BLACK = (248, 248, 252), (0, 0, 0)
ORANGE, CYAN, RED, PINK, YEL = (255, 122, 26), (0, 229, 255), (235, 30, 40), (255, 46, 99), (255, 214, 0)
NAVY = (6, 7, 13)

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/vo_v1_words.json"))[0]["words"]
_NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def _tok(w):
    t = "".join(ch for ch in w.lower() if ch.isalnum())
    return _NUMW[int(t)] if t.isdigit() and int(t) <= 20 else t
TOK = [_tok(x["w"]) for x in WORDS]
def at(phrase, after=0.0, end=False):
    """Start (or end) time of the first occurrence of `phrase` starting at/after `after` (raw VO seconds)."""
    p = [_tok(x) for x in phrase.split() if _tok(x)]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i:i + len(p)] == p and WORDS[i]["s"] >= after - 1e-6:
            return WORDS[i + len(p) - 1]["e"] if end else WORDS[i]["s"]
    raise KeyError(f"phrase not found after {after:.1f}: {phrase!r}")
NUMBERS = [WORDS[i]["s"] for i, t in enumerate(TOK) if t == "number"]   # "Number one" ... "Number nineteen"
VO_END = WORDS[-1]["e"]

# ------------------------------------------------------------------ soundbites (inserted into the timeline)
PAD = 0.35   # breath before/after each soundbite
PRE = 5.0    # cold open: Seoul race finish plays before anything else
def SBX(before_phrase, src, a, b, tag, after=0.0):
    """Soundbite inserted just before `before_phrase` (searched from `after`, raw VO seconds)."""
    if before_phrase is None: t = 0.0
    else:
        keep = _CUR[0]; t = A(before_phrase, after) - 0.2; _CUR[0] = keep
    return dict(t=round(t, 3), src=src, ss=a, dur=round(b - a, 3), tag=tag)
SOUNDBITES = []
def _sb():
    S_ = SOUNDBITES; c = CARD
    S_.append(SBX(None, "benjohnson_bbc", 85.6, 100.0, "BBC · SEOUL 1988"))
    S_.append(SBX("then he goes in front", "benjohnson_bbc", 115.2, 122.8, "BBC · SEOUL 1988", c[1]))
    S_.append(SBX("then you got antonio", "montgomery_ap09", 29.67, 34.17, "AP · 2009", c[3]))
    S_.append(SBX("three golds", "marionjones_court07", 1.2, 5.3, "AP · WHITE PLAINS 2007", c[4]))
    S_.append(SBX("and she did six months", "marionjones_ioc_ap", 27.0, 37.5, "AP · IOC 2007", c[4]))
    S_.append(SBX("a pork burrito", "houlihan_kgw", 26.5, 38.1, "KGW NEWS · 2021", c[5]))
    S_.append(SBX("that s heidi krieger", "krieger_tws", 109.8, 123.8, "TRANS WORLD SPORT", c[6]))
    S_.append(SBX("that s maria sharapova", "sharapova_ap", 6.0, 17.0, "AP · LOS ANGELES 2016", c[9]))
    S_.append(SBX("tyson gay one of", "tysongay_ch4", 2.0, 16.0, "CHANNEL 4 NEWS · 2013", c[11]))
    S_.append(SBX("ruth", "chepngetich_cbs", 54.0, 63.0, "CBS NEWS CHICAGO · 2025", c[14]))
    S_.append(SBX("today it s a street drug", "captagon_ch4", 90.0, 101.0, "CHANNEL 4 NEWS · SYRIA 2024", c[15]))
    S_.append(SBX("sarm cj", "ujah_sky_suspended", 0.0, 10.0, "SKY NEWS · 2021", c[19]))
    S_.append(SBX("one month ban", "shacarri_today", 569.7, 576.0, "NBC TODAY · 2021", c[19]))
    S_.sort(key=lambda s: s["t"])
def FT(t):
    """raw VO seconds -> final timeline seconds."""
    sh = PRE
    for s in SOUNDBITES:
        if s["t"] <= t + 1e-6: sh += s["dur"] + 2 * PAD
    return t + sh
def SB_START(s):  # final-timeline start of a soundbite clip
    sh = PRE
    for o in SOUNDBITES:
        if o is s: break
        sh += o["dur"] + 2 * PAD
    return s["t"] + sh + PAD - 0.15

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: print(" ".join(map(str, cmd))[:900]); print(r.stderr[-2500:]); raise SystemExit(1)
    return r
def F(path, size): return ImageFont.truetype(path, size)
def fit(text, path, size, maxw):
    while F(path, size).getlength(text) > maxw and size > 26: size -= 4
    return F(path, size)

# ------------------------------------------------------------------ neon graphic language
def glow(layer, blur=14, k=2):
    g = layer.filter(ImageFilter.GaussianBlur(blur)); out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    for _ in range(k): out.alpha_composite(g)
    out.alpha_composite(layer); return out

def neon_text(im, xy, s, font, col, anchor="mm", stroke=0, blur=16):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=font, fill=col + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=BLACK + (255,))
    g = lay.filter(ImageFilter.GaussianBlur(blur)); im.alpha_composite(g); im.alpha_composite(lay)

def shadow_text(im, xy, s, font, col, anchor="mm", stroke=8):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=font, fill=col + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=BLACK + (255,))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(12)))
    im.alpha_composite(sh, (5, 8)); im.alpha_composite(lay)

def neon_rect(size, box, col, width=4, blur=16):
    lay = Image.new("RGBA", size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle(box, outline=col + (255,), width=width)
    return glow(lay, blur, 2)

_BG = None
def neon_bg():
    """Static neon backdrop (cards): navy, red/orange/cyan glows, floor grid, HUD corners."""
    global _BG
    if _BG: return _BG.copy()
    yy, xx = np.mgrid[0:Hh // 4, 0:W // 4].astype(np.float32)
    g1 = np.exp(-(((xx - W / 8) / 260) ** 2 + ((yy - Hh / 12) / 140) ** 2))
    g2 = np.exp(-(((xx - W / 4 + 60) / 180) ** 2 + ((yy - Hh / 6) / 120) ** 2))
    g3 = np.exp(-(((xx - 50) / 180) ** 2 + ((yy - Hh / 5) / 120) ** 2))
    a = np.zeros((Hh // 4, W // 4, 3), np.float32)
    for c in range(3): a[..., c] = NAVY[c] + g1 * (150, 10, 20)[c] * 0.55 + g2 * CYAN[c] * 0.08 + g3 * ORANGE[c] * 0.10
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, Hh), Image.BILINEAR).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA"); hz = 760
    d.line([(0, hz), (W, hz)], fill=RED + (90,), width=2)
    for i in range(-14, 15): d.line([(W / 2 + i * 18, hz), (W / 2 + i * 230, Hh)], fill=CYAN + (30,), width=2)
    for j in range(9):
        z = (j + 0.5) / 9; y = hz + (Hh - hz) * z ** 2.2; d.line([(0, y), (W, y)], fill=CYAN + (int(10 + 40 * z),), width=2)
    for gx in range(0, W, 80): d.line([(gx, 0), (gx, hz)], fill=(40, 60, 90, 18))
    for gy in range(0, hz, 80): d.line([(0, gy), (W, gy)], fill=(40, 60, 90, 18))
    L = 46
    for sx, sy in ((40, 40), (W - 40, 40), (40, Hh - 40), (W - 40, Hh - 40)):
        dx = 1 if sx < W / 2 else -1; dy = 1 if sy < Hh / 2 else -1
        d.line([(sx, sy), (sx + dx * L, sy)], fill=CYAN + (150,), width=3); d.line([(sx, sy), (sx, sy + dy * L)], fill=CYAN + (150,), width=3)
    _BG = im; return im.copy()

def archive_tag(tag, col=ORANGE, kind="ARCHIVE"):
    """Full-frame HUD overlay for archival footage: corner brackets + REC dot + tag."""
    im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im); L = 54; x0, y0, x1, y1 = 34, 34, W - 34, Hh - 34
    for sx, sy, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(sx, sy), (sx + dx * L, sy)], fill=CYAN + (230,), width=5); d.line([(sx, sy), (sx, sy + dy * L)], fill=CYAN + (230,), width=5)
    f = F(MONO, 24); tx, ty = x0 + 30, y0 + 26; kw = d.textlength(kind + " ", font=f); tw = d.textlength("// " + tag.upper(), font=f)
    d.rectangle([tx - 12, ty - 8, tx + 30 + kw + tw + 14, ty + 34], fill=(4, 6, 14, 180))
    d.ellipse([tx, ty + 4, tx + 18, ty + 22], fill=PINK + (255,))
    d.text((tx + 30, ty), kind, font=f, fill=WHITE + (235,)); d.text((tx + 30 + kw, ty), "// " + tag.upper(), font=f, fill=col + (255,))
    return glow(im, 6, 1)

# ------------------------------------------------------------------ cards
DRUG_PH = {
    "winstrol": (f"{BS}/src/Winstrol tablets.JPG", (40, 120, 1090, 1170)), "epo": (f"{BS}/drugs/d0.jpg", (190, 40, 1110, 960)),
    "hgh": (f"{BS}/drugs/d2.jpg", (0, 210, 1280, 1490)), "testo": (f"{BS}/src/Depo-testosterone crop.jpg", (0, 350, 1642, 1992)),
    "weed": (f"{BS}/leaf/leaf_1.jpg", (93, 0, 1234, 1141)), "meld": (f"{BS}/drugs/d8.jpg", (160, 0, 1120, 960)),
    "captagon": (f"{BS}/drugs/d3.jpg", (213, 0, 1066, 853)), "diur": (f"{BS}/drugs/d7.jpg", (40, 0, 1000, 960)),
    "inhaler": (f"{BS}/drugs/d5.jpg", (0, 99, 1280, 1379)), "strych": (f"{BS}/drugs/d4.jpg", (340, 560, 970, 1190)),
    "amph": (f"{BS}/drugs/d6.jpg", (300, 0, 718, 418)), "vials": (f"{BS}/src/Port Huron steroids.jpg", (0, 700, 1920, 2620)),
    "syringe": (f"{BS}/syr/Syringe_with_insulin_for_a_cat.jpg", (900, 0, 2092, 1192)),
}
def count_card(n, name, cat, ph=None, col=ORANGE, sub=None):
    im = neon_bg()
    num = f"#{n}" if isinstance(n, int) else n
    if ph:
        path, box = DRUG_PH[ph]; D = 600
        t = ImageOps.fit(Image.open(path).convert("RGB").crop(box), (D, D), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 30, 3))
        m = Image.new("L", (D * 4, D * 4), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, D * 4 - 1, D * 4 - 1], radius=80 * 4, fill=255)
        m = m.resize((D, D), Image.LANCZOS); x0, y0 = W - D - 170, (Hh - D) // 2 - 30
        ring = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); rr = Image.new("RGBA", (D + 24, D + 24), col + (255,))
        mm = Image.new("L", ((D + 24) * 4, (D + 24) * 4), 0); ImageDraw.Draw(mm).rounded_rectangle([0, 0, (D + 24) * 4 - 1, (D + 24) * 4 - 1], radius=92 * 4, fill=255)
        rr.putalpha(mm.resize((D + 24, D + 24), Image.LANCZOS)); ring.alpha_composite(rr, (x0 - 12, y0 - 12))
        im.alpha_composite(glow(ring, 30, 2)); tt = t.convert("RGBA"); tt.putalpha(m); im.alpha_composite(tt, (x0, y0))
        tx, maxw = 150, W - D - 170 - 150 - 80
    else:
        tx, maxw = 150, W - 300
    neon_text(im, (tx, 300), num, F(ANTON, 230), col, "ls", blur=22)
    fn = fit(name, ANTON, 170, maxw); shadow_text(im, (tx, 500), name, fn, WHITE, "ls", 0)
    d = ImageDraw.Draw(im); fc = F(MONO, 40); cw = d.textlength(cat, font=fc)
    d.rectangle([tx, 560, tx + cw + 40, 620], fill=(4, 6, 14, 220), outline=CYAN + (255,), width=3)
    d.text((tx + 20, 590), cat, font=fc, fill=CYAN + (255,), anchor="lm")
    if sub: d.text((tx, 680), sub, font=F(INTB, 44), fill=WHITE + (230,), anchor="lm")
    return im.convert("RGB")

PEOPLE = f"{BS}/ppl"
def photo_card(path, label=None, sub=None, col=CYAN, crop=None, bw=False):
    im = neon_bg(); ph = Image.open(path).convert("RGB"); ph = ImageOps.exif_transpose(ph)
    if crop: ph = ph.crop(crop)
    if bw: ph = ImageOps.grayscale(ph).convert("RGB")
    ph.thumbnail((1500, 780), Image.LANCZOS)
    x0, y0 = (W - ph.width) // 2, (Hh - ph.height) // 2 - (40 if label else 0)
    im.alpha_composite(neon_rect((W, Hh), [x0 - 6, y0 - 6, x0 + ph.width + 5, y0 + ph.height + 5], col, 5, 18))
    im.paste(ph, (x0, y0))
    if label:
        d = ImageDraw.Draw(im); f = fit(label, ANTON, 64, 1300); tw = d.textlength(label, font=f) + 60
        bx, by = (W - tw) / 2, y0 + ph.height + 26
        d.rectangle([bx, by, bx + tw, by + 84], fill=(8, 9, 16, 235), outline=col + (255,), width=3)
        d.text((W / 2, by + 42), label, font=f, fill=WHITE, anchor="mm")
        if sub: d.text((W / 2, by + 118), sub, font=F(MONO, 30), fill=col + (255,), anchor="mm")
    return im.convert("RGB")

def text_card(lines, col=ORANGE, sub=None):
    im = neon_bg(); n = len(lines); y0 = Hh // 2 - (n - 1) * 80 - (40 if sub else 0)
    for j, l in enumerate(lines):
        neon_text(im, (W // 2, y0 + j * 160), l, fit(l, ANTON, 150, 1700), col if j == n - 1 else WHITE, "mm", blur=18)
    if sub: ImageDraw.Draw(im).text((W // 2, y0 + n * 160 + 10), sub, font=F(MONO, 36), fill=CYAN + (255,), anchor="mm")
    return im.convert("RGB")

# ------------------------------------------------------------------ overlays (drawn over any shot)
def make_overlay(spec):
    kind = spec[0]; im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "name":   # ("name", NAME, sub)
        _, name, sub = spec; f = fit(name, ANTON, 110, 1250); nw = int(f.getlength(name)); sw = int(F(MONO, 36).getlength(sub))
        bw = max(nw, sw) + 120; y = Hh - 300
        d.rectangle([0, y, bw, y + 150], fill=(6, 7, 13, 230)); d.rectangle([0, y + 150, bw, y + 210], fill=(6, 7, 13, 200))
        im.alpha_composite(neon_rect((W, Hh), [0, y, bw, y + 210], CYAN, 3, 12))
        d.rectangle([0, y, 14, y + 210], fill=ORANGE + (255,))
        d.text((50, y + 78), name, font=f, fill=WHITE, anchor="lm"); d.text((50, y + 182), sub, font=F(MONO, 36), fill=ORANGE + (255,), anchor="lm")
        return im
    if kind == "stat":   # ("stat", BIG, label, colour)
        _, big, label, col = spec; f = fit(big, ANTON, 260, 1500)
        neon_text(im, (110, 560), big, f, tuple(col), "ls", stroke=6, blur=20)
        fl = fit(label, ANTON, 72, 1500); lw = int(fl.getlength(label))
        d = ImageDraw.Draw(im); d.rectangle([90, 590, 150 + lw, 690], fill=(6, 7, 13, 225)); d.text((120, 640), label, font=fl, fill=WHITE, anchor="lm")
        im.alpha_composite(neon_rect((W, Hh), [90, 590, 150 + lw, 690], tuple(col), 3, 12)); return im
    if kind == "ban":    # ("ban", text) red stamp
        _, text = spec; f = fit(text, ANTON, 150, 1500); tw = f.getlength(text) + 80
        lay = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        bx, by = (W - tw) / 2, Hh / 2 - 105
        dl.rectangle([bx, by, bx + tw, by + 210], outline=RED + (255,), width=12); dl.text((W / 2, Hh / 2), text, font=f, fill=RED + (255,), anchor="mm")
        lay = lay.rotate(-6, center=(W / 2, Hh / 2), resample=Image.BICUBIC)
        dark = Image.new("RGBA", (W, Hh), (0, 0, 0, 70)); im.alpha_composite(dark); im.alpha_composite(glow(lay, 10, 1)); return im
    if kind == "pop":    # ("pop", text, colour, pos)
        _, text, col, pos = spec; f = fit(text, ANTON, 130, W - 220)
        xy, anc = {"c": ((W // 2, Hh // 2), "mm"), "b": ((W // 2, Hh - 180), "mm"), "t": ((W // 2, 170), "mm")}[pos]
        shadow_text(im, xy, text, f, tuple(col), anc, 9); return im
    if kind == "quote":  # ("quote", [lines], source)
        _, lines, source = spec; f = F(INTER, 60); lh = 92
        bw = max(int(f.getlength(l)) for l in lines) + 220; bh = len(lines) * lh + 200; x0, y0 = (W - bw) // 2, (Hh - bh) // 2
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(6, 7, 13, 235)); im.alpha_composite(neon_rect((W, Hh), [x0, y0, x0 + bw, y0 + bh], ORANGE, 4, 16))
        d = ImageDraw.Draw(im); d.text((x0 + 30, y0 - 10), "“", font=F(ANTON, 200), fill=ORANGE + (255,))
        for j, l in enumerate(lines): d.text((x0 + 120, y0 + 80 + j * lh), l, font=f, fill=WHITE)
        d.text((x0 + 120, y0 + bh - 70), source, font=F(MONO, 32), fill=CYAN + (255,)); return im
    if kind == "list":   # ("list", [lines], colour of last)
        _, lines, col = spec
        for j, l in enumerate(lines): shadow_text(im, (110, 330 + j * 145), l, fit(l, ANTON, 104, 1650), tuple(col) if j == len(lines) - 1 else WHITE, "lm", 8)
        return im
    if kind == "sbtag":  # soundbite source tag
        return archive_tag(spec[1], ORANGE, "SOURCE")
    if kind == "endq":
        _, l1, l2 = spec
        neon_text(im, (W // 2, 380), l1, fit(l1, ANTON, 130, 1700), WHITE, "mm", 8)
        neon_text(im, (W // 2, 550), l2, fit(l2, ANTON, 130, 1700), ORANGE, "mm", 8)
        shadow_text(im, (W // 2, 760), "LET ME KNOW DOWN BELOW", F(ANTON, 76), CYAN, "mm", 6); return im
    raise ValueError(kind)

def overlay_png(spec):
    p = f"{R}/ov/{hashlib.md5(json.dumps(spec).encode()).hexdigest()[:12]}.png"
    if not os.path.exists(p): make_overlay(spec).save(p)
    return p

# ------------------------------------------------------------------ fuzzy sequential phrase finder
import difflib
_CUR = [0.0]
def A(phrase, after=None, end=False):
    """Like at(), but searches forward from the running cursor and tolerates whisper misspellings."""
    t0 = _CUR[0] if after is None else after
    try: t = at(phrase, t0, end)
    except KeyError:
        p = [_tok(x) for x in phrase.split() if _tok(x)]; tgt = " ".join(p); best = (0, None)
        for i in range(len(TOK) - len(p) + 1):
            if WORDS[i]["s"] < t0 - 1e-6: continue
            if WORDS[i]["s"] > t0 + 45: break
            r = difflib.SequenceMatcher(None, tgt, " ".join(TOK[i:i + len(p)])).ratio()
            if r >= 0.78: best = (r, i); break
            if r > best[0] + 0.02: best = (r, i)
        if best[0] < 0.6: raise KeyError(f"no match for {phrase!r} after {t0:.1f} (best {best[0]:.2f})")
        i = best[1]; t = WORDS[i + len(p) - 1]["e"] if end else WORDS[i]["s"]
    if not end: _CUR[0] = t
    return t

def _cards():
    import re as _re
    nw = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    out, cur = {}, 0
    for k in range(1, 20):
        for i in range(cur, len(WORDS)):
            t = TOK[i]
            if t in (str(k), nw[k - 1]) and WORDS[i]["s"] > (max(out.values()) + 20 if out else 30) and \
               (TOK[i - 1] == "number" or WORDS[i]["s"] - WORDS[i - 1]["e"] > 0.35 or WORDS[i - 1]["w"][-1:] in ".?!") and \
               (WORDS[i]["w"][-1:] in ".," or TOK[i - 1] == "number"):
                out[k] = WORDS[i - 1]["s"] if TOK[i - 1] == "number" else WORDS[i]["s"] - 0.45; cur = i + 1; break
        else: raise KeyError(f"card {k}")
    return out
CARD = _cards()

# ------------------------------------------------------------------ edit decision list (raw VO seconds)
SHOTS, OVER = [], []
def S(t, src, ss=0.0, **o): SHOTS.append(dict(t=round(t, 3), src=src, ss=ss, **o))
def O(t, dur, spec): OVER.append((round(t, 3), round(t + dur, 3), spec))
def pop(t, dur, text, col=WHITE, pos="b"): O(t, dur, ("pop", text, list(col), pos))
def name(t, dur, n, sub): O(t, dur, ("name", n, sub))
def stat(t, dur, big, label, col=ORANGE): O(t, dur, ("stat", big, label, list(col)))
def ban(t, dur, text): O(t, dur, ("ban", text))
def lst(t, dur, lines, col=ORANGE): O(t, dur, ("list", lines, list(col)))
PPL = lambda n: f"{BS}/ppl/{n}.jpg"
SRC = lambda n: f"{BS}/src/{n}"
HK = lambda n: f"{BS}/hicks/hicks_{n}.jpg"
CARDS = {}
def card(k, name_, cat, ph=None, col=ORANGE, sub=None):
    t = CARD[k] if isinstance(k, int) else k[1]
    S(t, "COUNT", n=k if isinstance(k, int) else k[0], name=name_, cat=cat, ph=ph, col=list(col), sub=sub); _CUR[0] = t + 0.5
    return t

def build_edl():
    _sb(); a = A
    # 00 cold open ------------------------------------------------------------------
    S(a("y all that s ben johnson"), "benjohnson88", 40.0, tag="SEOUL 1988"); stat(a("y all that s ben johnson"), 3.0, "9.79", "WORLD RECORD · SEOUL 1988")
    S(a("fastest man"), "benjohnson88", 42.0, tag="SEOUL 1988")
    S(a("and two days later"), "benjohnson_cbc25", 106.0, tag="CBC · 1988"); pop(a("gone"), 1.6, "GONE", RED, "c")
    S(a("gold medal world record"), "benjohnson_bbc", 132.0, tag="SEOUL 1988"); lst(a("gold medal world record"), 2.6, ["GOLD MEDAL", "WORLD RECORD", "ALL OF IT"], RED)
    S(a("and that was one drug"), "PHOTO", path=f"{P}/thumbs/v5/F_drugs_neon_tiles_HD.jpg", full=1)
    S(a("so today"), "kenya_citizen_ban", 5.0, tag="CITIZEN TV KENYA")
    S(a("what it do"), "captagon_ch4", 70.0, tag="CHANNEL 4 NEWS")
    S(a("and the real names"), "marionjones_court07", 9.0, tag="AP · 2007")
    S(a("mind you some of these"), "marionjones_ioc_ap", 2.0, tag="AP · IOC")
    S(a("some lost world records"), "montgomery02", 138.0, tag="PARIS 2002")
    S(a("one man damn near died"), "PHOTO", path=HK(5), bw=1, label="ST. LOUIS · 1904")
    S(a("and some of this stuff"), "jepchirchir_ktn", 2.0, tag="KTN NEWS · 2026")
    S(a("20 substances"), "TEXT", lines=["20 BANNED SUBSTANCES", "LET'S GET INTO IT"])
    # 01 stanozolol -------------------------------------------------------------------
    card(1, "STANOZOLOL", "ANABOLIC STEROID", "winstrol", sub="AKA WINSTROL")
    S(a("this is steroid"), "benjohnson88", 10.0, tag="SEOUL 1988"); lst(a("more muscle"), 3.6, ["MORE MUSCLE", "MORE STRENGTH", "FASTER RECOVERY"])
    S(a("so you already know"), "benjohnson_bbc", 16.0, tag="BBC · 1988")
    S(a("1988 100 meter final"), "benjohnson_bbc", 28.0, tag="SEOUL 1988 · 100M FINAL", amb=1)
    name(a("ben johnson versus carl lewis"), 2.6, "JOHNSON vs LEWIS", "CANADA vs USA")
    S(a("johnson run"), "benjohnson88", 39.0, tag="SEOUL 1988", amb=1); stat(a("johnson run") + 0.8, 2.4, "9.79", "WORLD RECORD")
    S(a("and the test come back"), "benjohnson_cbc25", 114.0, tag="CBC · 1988"); pop(a("stenosalol", None), 1.8, "STANOZOLOL", RED, "c")
    S(a("then he goes in front"), "benjohnson_cbc25", 165.0, tag="DUBIN INQUIRY · 1989")
    S(a("so they took his"), "benjohnson_cbc25", 91.0, tag="CBC"); stat(a("from the year before"), 2.6, "9.83", "1987 WORLD RECORD · ERASED", RED)
    S(a("and here go the crazy part"), "benjohnson_bbc", 56.0, tag="SEOUL 1988 · THE LINEUP")
    S(a("carl lewis linford christie"), "benjohnson_bbc", 100.0, tag="SEOUL 1988 · THE LINEUP")
    lst(a("carl lewis linford christie"), 3.4, ["CARL LEWIS", "LINFORD CHRISTIE", "DENNIS MITCHELL", "DESAI WILLIAMS"], CYAN)
    S(a("six of the eight"), "benjohnson_cbc25", 129.0, tag="CBC"); stat(a("six of the eight"), 2.0, "6 OF 8", "TIED TO DOPING LATER", RED)
    pop(a("that s why they call it"), 3.0, "THE DIRTIEST RACE IN HISTORY", ORANGE, "b")
    S(a("and you think that s old news"), "TEXT", lines=["PARIS 2024", "OPENING CEREMONY"])
    S(a("dominique"), "TEXT", lines=["DOMINIQUE MULAMBA", "POSITIVE · STANOZOLOL"], col=list(RED))
    ban(a("four years"), 1.6, "BANNED 4 YEARS"); S(a("same drug"), "benjohnson88", 42.0, tag="SEOUL 1988"); pop(a("same drug"), 2.6, "SAME DRUG · 36 YEARS LATER", ORANGE, "b")
    # 02 EPO --------------------------------------------------------------------------
    card(2, "EPO", "BLOOD BOOSTER", "epo", CYAN, sub="ERYTHROPOIETIN")
    S(a("your kidneys"), "jeptoo_citizen", 40.0, tag="CITIZEN TV KENYA"); lst(a("more red blood cells"), 3.2, ["MORE RED BLOOD CELLS", "MORE OXYGEN"], CYAN)
    S(a("this one ain t for the sprinters"), "kenya_citizen_ban", 50.0, tag="KENYA"); pop(a("distance guys"), 1.8, "DISTANCE RUNNERS", CYAN, "b")
    S(a("beijing 2008"), "ramzi_beijing08", 0.0, tag="BEIJING 2008 · 1500M", amb=1)
    S(a("rashid"), "ramzi_beijing08", 24.0, tag="BEIJING 2008 · 1500M"); name(a("rashid"), 3.0, "RASHID RAMZI", "BAHRAIN · 1500M GOLD")
    S(a("then they retested"), "ramzi_beijing08", 58.0, tag="BEIJING 2008"); pop(a("called sarah"), 2.2, "RETEST: CERA (NEW EPO)", RED, "b")
    S(a("gold medal gone"), "PHOTO", path=PPL("ramzi"), label="RASHID RAMZI", sub="GOLD STRIPPED"); ban(a("gold medal gone"), 1.5, "STRIPPED")
    S(a("asbel kiprop"), "kiprop_africanews", 4.0, tag="AFRICANEWS"); name(a("asbel kiprop"), 3.4, "ASBEL KIPROP", "KENYA · 3× WORLD CHAMPION")
    S(a("years later he get caught"), "kiprop_africanews", 40.0, tag="AFRICANEWS · 2019"); ban(a("four years"), 1.6, "BANNED 4 YEARS")
    S(a("rita jep"), "jeptoo_citizen", 44.0, tag="BOSTON 2014"); name(a("rita jep"), 3.0, "RITA JEPTOO", "BOSTON & CHICAGO 2014")
    ban(a("lost both"), 1.6, "BOTH TITLES STRIPPED")
    S(a("and it s not slowing down"), "kenya_citizen_ban", 162.0, tag="CITIZEN TV KENYA"); stat(a("over 140"), 3.0, "140+", "KENYANS SANCTIONED SINCE 2017", RED)
    S(a("this year albert"), "PHOTO", path=PPL("korir"), label="ALBERT KORIR", sub="FORMER NYC MARATHON CHAMP"); ban(a("got five years"), 1.6, "5 YEARS · CERA")
    S(a("and just last month"), "jepchirchir_tv47", 12.0, tag="TV47 KENYA · OCT 2026"); name(a("olympic marathon champ"), 3.0, "PERES JEPCHIRCHIR", "OLYMPIC MARATHON CHAMPION")
    S(a("got provisionally suspended"), "jepchirchir_ktn", 2.0, tag="KTN NEWS · OCT 2026"); pop(a("got provisionally suspended"), 2.4, "PROVISIONALLY SUSPENDED · EPO", RED, "b")
    pop(a("that case still open"), 2.4, "CASE STILL OPEN", CYAN, "b")
    # 03 HGH --------------------------------------------------------------------------
    card(3, "HGH", "HUMAN GROWTH HORMONE", "hgh", ORANGE)
    S(a("now this one don t"), "montgomery02", 36.0, tag="ESPN2 · PARIS 2002"); lst(a("your muscles"), 3.4, ["MUSCLES", "TENDONS", "LIGAMENTS", "HEAL FASTER"])
    S(a("tim montgomery"), "montgomery02", 48.0, tag="PARIS 2002", amb=1); stat(a("tim montgomery"), 3.4, "9.78", "WORLD RECORD · 2002")
    S(a("and mind you this man"), "montgomery02", 162.0, tag="ESPN2 · 2002"); pop(a("never failed a drug test"), 2.4, "NEVER FAILED A TEST", ORANGE, "b")
    S(a("they got him off paperwork"), "montgomery_ap09", 0.0, tag="AP"); pop(a("balco"), 1.6, "BALCO INVESTIGATION", CYAN, "t"); ban(a("record white"), 1.4, "RECORD WIPED")
    S(a("then you got antonio"), "TEXT", lines=["ANTONIO PETTIGREW", "ADMITTED HGH + EPO UNDER OATH"])
    ban(a("the whole usa"), 2.4, "SYDNEY 4×400 GOLD · STRIPPED")
    S(a("and the most recent big one"), "okagbare_cgtn", 48.0, tag="CGTN AFRICA"); name(a("blessing"), 3.0, "BLESSING OKAGBARE", "NIGERIA · OLYMPIC MEDALIST")
    S(a("tokyo 2021"), "okagbare_cgtn", 28.0, tag="TOKYO 2020"); pop(a("she went 100 heat"), 1.8, "WON HER HEAT", WHITE, "b")
    S(a("and then they pull her"), "okagbare_cgtn", 4.0, tag="CGTN AFRICA"); pop(a("before the semis"), 1.8, "PULLED BEFORE THE SEMIS", RED, "b")
    ban(a("11 years"), 2.0, "BANNED 11 YEARS")
    # 04 THG --------------------------------------------------------------------------
    card(4, 'THG · "THE CLEAR"', "DESIGNER STEROID", "syringe", PINK)
    S(a("this was a designer steroid"), "TEXT", lines=["BALCO LAB", "BUILT TO BEAT THE TEST"])
    S(a("so how you catch"), "PHOTO", path=f"{BS}/syr/Syringe_with_insulin_for_a_cat.jpg", crop=(300, 0, 2784, 1192)); pop(a("2003 somebody mailed"), 2.6, "2003 · AN ANONYMOUS SYRINGE", ORANGE, "b")
    S(a("and who was it"), "TEXT", lines=["TREVOR GRAHAM", "COACH OF JONES · MONTGOMERY · GATLIN"])
    S(a("the lab cracked it"), "benjohnson_cbc25", 120.0, tag="ANTI-DOPING LAB")
    S(a("dwayne chambers"), "montgomery02", 30.0, tag="PARIS 2002"); name(a("dwayne chambers"), 2.4, "DWAIN CHAMBERS", "GREAT BRITAIN · EUROPEAN CHAMP")
    S(a("regina jacobs"), "TEXT", lines=["REGINA JACOBS", "POSITIVE"])
    S(a("and marion jones never"), "marionjones00", 2.0, tag="SYDNEY 2000", amb=1); name(a("and marion jones never"), 3.0, "MARION JONES", "5 MEDALS · SYDNEY 2000")
    S(a("three golds"), "marionjones00", 18.0, tag="SYDNEY 2000"); ban(a("all five gone"), 1.8, "ALL 5 MEDALS STRIPPED")
    S(a("and she did six months"), "marionjones_court07", 9.0, tag="AP · WHITE PLAINS 2007"); pop(a("six months in federal prison"), 2.6, "6 MONTHS · FEDERAL PRISON", RED, "b")
    # 05 nandrolone ---------------------------------------------------------------------
    card(5, "NANDROLONE", "ANABOLIC STEROID", "vials", ORANGE)
    S(a("classic steroid"), "benjohnson_cbc25", 240.0, tag="LAB")
    pop(a("the excuses get wild"), 2.0, "THE EXCUSES GET WILD", ORANGE, "b")
    S(a("linford christie"), "christie_bbc", 3.0, tag="BBC"); name(a("linford christie"), 3.0, "LINFORD CHRISTIE", "OLYMPIC 100M CHAMPION · 1992"); ban(a("two years"), 1.4, "BANNED 2 YEARS")
    S(a("dieter"), "PHOTO", path=PPL("baumann"), label="DIETER BAUMANN", sub="OLYMPIC 5000M CHAMPION"); pop(a("spiked his toothpaste"), 2.4, '"SOMEBODY SPIKED MY TOOTHPASTE"', ORANGE, "t")
    S(a("and then shelby"), "PHOTO", path=PPL("houlihan"), label="SHELBY HOULIHAN", sub="AMERICAN RECORD HOLDER")
    S(a("a pork burrito"), "houlihan_kgw", 48.0, tag="KGW NEWS"); pop(a("a pork burrito"), 1.8, "A PORK BURRITO", ORANGE, "c")
    S(a("four years"), "houlihan_kgw", 78.0, tag="KGW NEWS"); ban(a("four years"), 1.5, "BANNED 4 YEARS"); pop(a("she missed tokyo"), 1.8, "MISSED TOKYO & PARIS", RED, "b")
    # 06 dianabol / oral-turinabol -------------------------------------------------------
    card(6, "DIANABOL vs ORAL-TURINABOL", "STEROID PILLS", None, RED, sub="THE ONE MOST VIDEOS GET WRONG")
    S(a("diana ball is the old school"), "TEXT", lines=["DIANABOL", "MADE IN AMERICA · 1950s"])
    pop(a("two throwers from belarus"), 2.6, "ATHENS 2004 · 2 MEDALS LOST", RED, "b")
    S(a("but east germany"), "krieger_tws", 5.0, tag="EAST GERMANY"); pop(a("but east germany"), 1.6, "EAST GERMANY", WHITE, "b")
    S(a("oral torena ball"), "krieger_tws", 157.0, tag="TRANS WORLD SPORT"); pop(a("oral torena ball"), 2.4, "ORAL-TURINABOL", CYAN, "b")
    S(a("1974"), "krieger_tws", 20.0, tag="EAST GERMANY"); stat(a("1974"), 2.6, "STATE PLAN 14.25", "EAST GERMANY · 1974")
    stat(a("up to 10"), 3.0, "10,000", "ATHLETES · SOME OF THEM KIDS", RED)
    S(a("that s heidi krieger"), "krieger_tws", 50.0, tag="ARCHIVE 1980s"); name(a("that s heidi krieger"), 3.0, "HEIDI KRIEGER", "SHOT PUT · EAST GERMANY")
    S(a("later in life"), "krieger_tws", 300.0, tag="TRANS WORLD SPORT"); name(a("later in life"), 3.0, "ANDREAS KRIEGER", "TODAY")
    S(a("and a lot of them athletes"), "krieger_tws", 330.0, tag="BERLIN · 2000 TRIAL")
    # 07 clenbuterol -----------------------------------------------------------------------
    card(7, "CLENBUTEROL", "FAT BURNER", None, CYAN, sub="ASTHMA DRUG · CATTLE DRUG")
    S(a("it s an asthma drug"), "TEXT", lines=["ASTHMA DRUG", "...AND FOR COWS"]); lst(a("it burns fat"), 3.0, ["BURNS FAT", "KEEPS MUSCLE"], CYAN)
    S(a("katrin"), "krabbe91", 48.0, tag="TOKYO 1991", amb=1); name(a("katrin"), 3.0, "KATRIN KRABBE", "DOUBLE WORLD CHAMPION · 1991")
    S(a("biggest star in germany"), "krabbe91", 222.0, tag="TOKYO 1991")
    S(a("then 1992"), "krabbe91", 54.0, tag="TOKYO 1991"); ban(a("then 1992"), 1.8, "CLENBUTEROL · 1992")
    pop(a("unsporting"), 2.2, '"UNSPORTING BEHAVIOR"', ORANGE, "b"); ban(a("three years career over"), 1.8, "CAREER OVER")
    S(a("and the meat thing is real"), "TEXT", lines=["MEXICO · CHINA", "CONTAMINATED BEEF"])
    S(a("south africa s record holder"), "PHOTO", path=PPL("horn"), label="CARINA HORN", sub="SOUTH AFRICA · RECORD HOLDER"); ban(a("six years"), 1.5, "BANNED 6 YEARS")
    # 08 GHRP-6 --------------------------------------------------------------------------
    card(8, "GHRP-6", "PEPTIDE", None, PINK, sub="GROWTH HORMONE RELEASING PEPTIDE")
    S(a("this a peptide"), "TEXT", lines=["TRICKS YOUR BODY", "INTO MAKING GROWTH HORMONE"]); pop(a("out your system"), 2.2, "GONE IN 1–2 DAYS", CYAN, "b")
    S(a("side effect"), "TEXT", lines=["SIDE EFFECT", "HUNGRY"])
    S(a("and i m gonna keep it real"), "TEXT", lines=["NO FAMOUS", "TRACK CASE"])
    S(a("the closest is"), "TEXT", lines=["MARIN PREMERU", "CROATIA · GHRP-2 · 4 YEARS"])
    S(a("so you could take that two ways"), "TEXT", lines=["NOBODY USING IT?", "OR JUST HARD TO CATCH?"])
    # 09 meldonium ----------------------------------------------------------------------
    card(9, "MELDONIUM", "HEART DRUG", "meld", ORANGE, sub="FROM LATVIA")
    S(a("it s supposed to make your body"), "sharapova_ap", 52.0, tag="AP · 2016"); pop(a("probably not much"), 2.0, "PROBABLY NOT MUCH", CYAN, "b")
    S(a("so january 1st"), "TEXT", lines=["JANUARY 1, 2016", "MELDONIUM BANNED"])
    pop(a("positives everywhere"), 1.6, "POSITIVES EVERYWHERE", RED, "c")
    S(a("that s maria sharapova"), "PHOTO", path=PPL("sharapova"), label="MARIA SHARAPOVA", sub="TENNIS · 15 MONTHS")
    S(a("abeba"), "PHOTO", path=PPL("aregawi"), label="ABEBA AREGAWI", sub="2013 WORLD 1500M CHAMPION")
    S(a("tokyo marathon winner"), "aregawi_ap", 30.0, tag="AP · 2016"); name(a("tokyo marathon winner"), 3.0, "ENDESHAW NEGESSE", "TOKYO MARATHON WINNER")
    # 10 amphetamine -------------------------------------------------------------------
    card(10, "AMPHETAMINE", "STIMULANT", "amph", CYAN)
    S(a("straight stimulant"), "captagon_ch4", 75.0, tag="CHANNEL 4 NEWS"); lst(a("you locked in"), 3.0, ["LOCKED IN", "AGGRESSIVE", "NO PAIN"], RED)
    S(a("justin gatlin s first strike"), "PHOTO", path=SRC("Justin Gatlin Doha 2015.jpg"), label="JUSTIN GATLIN", sub="STRIKE 1 · 2001 · ADHD MEDICINE")
    S(a("luvo"), "manyonga_wa17", 4.0, tag="LONDON 2017"); name(a("luvo"), 3.0, "LUVO MANYONGA", "SOUTH AFRICA · LONG JUMP"); ban(a("18 months"), 1.5, "18 MONTHS · METH")
    S(a("and this a guy who came back"), "manyonga_wa17", 8.0, tag="LONDON 2017", amb=1); pop(a("2017 world title"), 2.0, "2017 WORLD CHAMPION", ORANGE, "b")
    S(a("then got banned again"), "manyonga_wa17", 42.0, tag="LONDON 2017"); pop(a("then got banned again"), 2.4, "BANNED AGAIN · MISSED TESTS", RED, "b")
    # 11 testosterone ------------------------------------------------------------------
    card(11, "TESTOSTERONE", "THE ORIGINAL", "testo", RED)
    S(a("they test it with a ratio"), "TEXT", lines=["T/E RATIO", "OVER 4 : 1 = FLAGGED"])
    S(a("dennis mitchell"), "benjohnson_bbc", 56.0, tag="SEOUL 1988"); name(a("dennis mitchell"), 3.0, "DENNIS MITCHELL", "OLYMPIC MEDALIST · USA")
    lst(a("he had five beers"), 3.0, ["5 BEERS", "+ HIS WIFE, 4 TIMES"], ORANGE)
    S(a("the us federation"), "benjohnson_bbc", 100.0, tag="SEOUL 1988"); ban(a("still gave him two years"), 1.5, "BANNED 2 YEARS")
    S(a("justin gatlin strike two"), "PHOTO", path=SRC("Justin Gatlin Rio 2016b-cr.jpg"), label="JUSTIN GATLIN", sub="STRIKE 2 · 2006")
    stat(a("just tired the world record"), 2.4, "9.77", "TIED WORLD RECORD"); ban(a("four years"), 1.4, "BANNED 4 YEARS")
    S(a("tyson gay one of"), "tysongay_ch4", 28.0, tag="CHANNEL 4 NEWS", amb=1); name(a("tyson gay one of"), 3.0, "TYSON GAY", "2ND FASTEST MAN EVER")
    S(a("he said it was from a cream"), "tysongay_ch4", 60.0, tag="CHANNEL 4 NEWS"); pop(a("from a cream"), 1.8, '"IT WAS A CREAM"', ORANGE, "b")
    S(a("and the us team lost"), "tysongay_ch4", 136.0, tag="CHANNEL 4 NEWS"); ban(a("silver because of it"), 1.8, "2012 4×100 SILVER · STRIPPED")
    # 12 ephedrine ----------------------------------------------------------------------
    card(12, "EPHEDRINE", "STIMULANT", None, ORANGE, sub="COLD MEDICINE · DIET PILLS")
    S(a("this in regular cold medicine"), "TEXT", lines=["COLD MEDICINE", "DIET PILLS"]); pop(a("only banned on race day"), 2.4, "BANNED ON RACE DAY ONLY", CYAN, "b")
    S(a("and y all ain t ready"), "PHOTO", path=PPL("lewis"), label="CARL LEWIS", sub="9× OLYMPIC CHAMPION")
    pop(a("1988 olympic trials"), 2.6, "1988 OLYMPIC TRIALS · POSITIVE", RED, "b")
    S(a("the us olympic committee"), "benjohnson_bbc", 68.0, tag="SEOUL 1988"); pop(a("and cleared him"), 1.8, "CLEARED", CYAN, "c")
    stat(a("nobody found out"), 2.6, "2003", "WHEN IT CAME OUT")
    S(a("so think about it"), "benjohnson_bbc", 33.0, tag="SEOUL 1988")
    stat(a("and it stayed quiet"), 2.6, "15 YEARS", "KEPT QUIET", RED)
    # 13 GW1516 -------------------------------------------------------------------------
    card(13, "GW1516", "CARDARINE", None, CYAN, sub='"EXERCISE IN A PILL"')
    S(a("in mice"), "TEXT", lines=["IN MICE:", "BURN FAT · RUN LONGER"])
    S(a("then the mice and rats"), "TEXT", lines=["MICE & RATS", "GOT CANCER"], col=list(RED))
    pop(a("the anti doping agency"), 2.4, "WADA: DO NOT TAKE THIS", RED, "b")
    pop(a("people took it anyway"), 1.8, "PEOPLE TOOK IT ANYWAY", ORANGE, "c")
    S(a("elena"), "lashmanova_oly12", 160.0, tag="LONDON 2012", amb=1); name(a("elena"), 3.0, "ELENA LASHMANOVA", "2012 OLYMPIC 20K WALK CHAMPION")
    ban(a("later they took her gold"), 1.6, "GOLD STRIPPED")
    S(a("nigel amos"), "PHOTO", path=PPL("amos"), label="NIJEL AMOS", sub="BOTSWANA · OLYMPIC 800M SILVER"); ban(a("three years"), 1.4, "BANNED 3 YEARS")
    S(a("and isam asinga"), "asinga_fos", 0.0, tag="FRONT OFFICE SPORTS"); name(a("and isam asinga"), 3.0, "ISSAM ASINGA", "AGE 18 · USA / SURINAME")
    S(a("run 989"), "asinga_fos", 106.0, tag="FRONT OFFICE SPORTS"); stat(a("run 989"), 2.4, "9.89", "WORLD U20 RECORD")
    S(a("then gw1516"), "asinga_fos", 140.0, tag="FRONT OFFICE SPORTS")
    S(a("he said it came from"), "asinga_fos", 90.0, tag="FRONT OFFICE SPORTS"); pop(a("recovery gummies"), 1.8, '"RECOVERY GUMMIES"', ORANGE, "b")
    S(a("record erased"), "asinga_fos", 240.0, tag="FRONT OFFICE SPORTS"); ban(a("record erased"), 1.8, "RECORD ERASED · 4 YEARS")
    # 14 diuretics ----------------------------------------------------------------------
    card(14, "DIURETICS", "MASKING AGENT", "diur", ORANGE)
    S(a("these ain t for speed"), "TEXT", lines=["THEY MAKE YOU PEE", "A LOT"]); pop(a("that waters down"), 2.6, "HIDES OTHER DRUGS", CYAN, "b")
    pop(a("that s why they banned all year"), 2.0, "BANNED ALL YEAR", RED, "b")
    S(a("the biggest one right now"), "chepngetich_cbs", 28.0, tag="CBS NEWS CHICAGO")
    S(a("ruth"), "chepngetich_cbs", 32.0, tag="CHICAGO 2024", amb=1); name(a("ruth"), 3.4, "RUTH CHEPNGETICH", "MARATHON WORLD RECORD · 2:09:56")
    S(a("she tests positive"), "chepngetich_cbs", 104.0, tag="CBS NEWS CHICAGO"); pop(a("housemaids pills"), 2.0, '"MY HOUSEMAID\'S PILLS"', ORANGE, "b")
    ban(a("three years"), 1.4, "BANNED 3 YEARS")
    S(a("the record still stand"), "chepngetich_cbs", 48.0, tag="CHICAGO 2024"); pop(a("the record still stand"), 2.6, "THE RECORD STILL STANDS", CYAN, "b")
    S(a("and remember ben johnson"), "benjohnson_ap95", 6.0, tag="AP · ROME 1995"); stat(a("strike three"), 2.4, "1999", "STRIKE 3 · A DIURETIC", RED)
    ban(a("banned for life"), 1.6, "BANNED FOR LIFE")
    S(a("jamaican sprinter"), "PHOTO", path=PPL("mullings"), label="STEVE MULLINGS", sub="JAMAICA · 2ND OFFENSE"); ban(a("second offense life"), 1.6, "BANNED FOR LIFE")
    # 15 captagon -----------------------------------------------------------------------
    card(15, "CAPTAGON", "STIMULANT PILL", "captagon", PINK)
    S(a("it s a pill your body"), "captagon_ch4", 68.0, tag="CHANNEL 4 NEWS · SYRIA"); lst(a("amphetamine and one called"), 3.0, ["AMPHETAMINE", "+ THEOPHYLLINE"], CYAN)
    stat(a("it was made in"), 2.6, "1961", "MADE AS A MEDICINE")
    S(a("and i m gonna keep it real ain t no track"), "TEXT", lines=["NO TRACK ATHLETE", "ON RECORD"])
    S(a("the famous story is soccer"), "TEXT", lines=["BUNDESLIGA · 1980s", "TEAM DOCTORS ADMITTED IT"])
    S(a("today it s a street drug"), "captagon_ch4", 150.0, tag="CHANNEL 4 NEWS · SYRIA")
    # 16 IGF-1 --------------------------------------------------------------------------
    card(16, "IGF-1", "GROWTH FACTOR", None, CYAN, sub="INSULIN-LIKE GROWTH FACTOR 1")
    S(a("when you take growth hormone"), "TEXT", lines=["GROWS TISSUE", "BUILDS PROTEIN"])
    S(a("ain t no track athlete ever"), "TEXT", lines=["NO TRACK BAN", "YOUR BODY MAKES IT"])
    S(a("the most famous case was golf"), "PHOTO", path=PPL("singh"), label="VIJAY SINGH", sub="GOLF · DEER ANTLER SPRAY"); pop(a("he got cleared"), 1.6, "CLEARED", CYAN, "c")
    S(a("so when you hear nobody"), "TEXT", lines=["NOBODY CAUGHT", "≠ NOBODY USING"])
    # 17 salbutamol ---------------------------------------------------------------------
    card(17, "SALBUTAMOL", "ASTHMA INHALER", "inhaler", CYAN)
    S(a("you re allowed to use it"), "TEXT", lines=["ALLOWED", "UP TO A LIMIT"])
    S(a("kim collins"), "PHOTO", path=PPL("collins"), label="KIM COLLINS", sub="ST KITTS & NEVIS"); pop(a("forgot to declare"), 2.2, "FORGOT TO DECLARE IT", ORANGE, "b")
    S(a("next year world champ"), "montgomery02", 6.0, tag="PARIS 2002"); stat(a("next year world champ"), 2.2, "2003", "WORLD 100M CHAMPION")
    S(a("so that s the gray area"), "TEXT", lines=["REAL MEDICINE", "REAL LIMIT", "REAL FIGHTS"])
    # 18 strychnine ---------------------------------------------------------------------
    card(18, "STRYCHNINE", "RAT POISON", "strych", RED)
    lst(a("tiny dose"), 4.0, ["TINY DOSE: WAKES YOU UP", "MORE: SEIZURES", "MORE: DEAD"], RED)
    S(a("1904 olympic marathon"), "PHOTO", path=HK(7), bw=1, label="ST. LOUIS · 1904 MARATHON")
    S(a("thomas hicks"), "PHOTO", path=HK(5), bw=1, label="THOMAS HICKS", sub="USA")
    lst(a("strychnine mixed with raw egg"), 3.4, ["STRYCHNINE + RAW EGG WHITES", "+ MORE STRYCHNINE & BRANDY"], RED)
    S(a("and he won"), "PHOTO", path=HK(0), bw=1, label="OLYMPIC CHAMPION")
    S(a("and it wasn t even against"), "TEXT", lines=["1904", "THERE WERE NO RULES"])
    # 19 oxandrolone --------------------------------------------------------------------
    card(19, "OXANDROLONE", "ANAVAR · MILD STEROID", None, ORANGE)
    S(a("doctors use it"), "TEXT", lines=["FOR BURNS", "& SURGERY RECOVERY"])
    S(a("athens 2004"), "TEXT", lines=["ATHENS 2004", "SHOT PUT"]); name(a("yuri"), 2.8, "YURIY BILONOH", "UKRAINE · GOLD")
    stat(a("eight years later"), 2.6, "2012", "RETEST: OXANDROLONE", RED)
    S(a("handed to adam nelson"), "PHOTO", path=PPL("nelson"), label="ADAM NELSON", sub="USA · OLYMPIC CHAMPION, 8 YEARS LATE")
    S(a("russia s svetlana"), "TEXT", lines=["SVETLANA KRIVELYOVA", "BRONZE STRIPPED"])
    S(a("they keep your samples"), "benjohnson_cbc25", 240.0, tag="LAB"); stat(a("they keep your samples"), 2.8, "10 YEARS", "SAMPLES KEPT", CYAN)
    # 20 bonus: the new wave ------------------------------------------------------------
    card(("BONUS", A("before we get to the last one")), "THE NEW WAVE", "WHAT'S CATCHING PEOPLE NOW", None, PINK)
    S(a("trem bologne"), "knighton_cgtn", 13.0, tag="CGTN"); pop(a("trem bologne"), 1.6, "TRENBOLONE", RED, "t"); name(a("arianne knighton"), 3.0, "ERRIYON KNIGHTON", "USA · PARIS 200M FINALIST")
    S(a("he said it was contaminated"), "knighton_cgtn", 0.0, tag="CGTN"); pop(a("contaminated oxtail"), 1.8, '"CONTAMINATED OXTAIL"', ORANGE, "b")
    S(a("then they appealed"), "knighton_cgtn", 24.0, tag="CGTN · 2025"); ban(a("gave him four years"), 1.6, "BANNED 4 YEARS")
    S(a("he out the 2028"), "paris200_final", 180.0, tag="PARIS 2024"); pop(a("he out the 2028"), 2.0, "OUT OF LA 2028", RED, "b")
    S(a("sarm cj"), "tokyo_4x100_final", 51.0, tag="TOKYO 2020", amb=1); pop(a("sarm cj"), 1.2, "SARMs", RED, "t"); name(a("cj uja"), 3.0, "CJ UJAH", "GREAT BRITAIN · 4×100")
    pop(a("osterring"), 1.8, "OSTARINE", RED, "t")
    S(a("the whole team lost"), "ujah_sky_stripped", 24.0, tag="SKY SPORTS NEWS"); ban(a("the whole team lost"), 1.8, "SILVER STRIPPED")
    S(a("tramitazidine"), "trimetazidine_reuters", 6.0, tag="REUTERS"); pop(a("tramitazidine"), 1.4, "TRIMETAZIDINE", RED, "t")
    S(a("lawrence"), "PHOTO", path=PPL("cherono"), label="LAWRENCE CHERONO", sub="BOSTON & CHICAGO WINNER"); pop(a("wrong pills"), 1.8, '"MY WIFE GAVE ME THE WRONG PILLS"', ORANGE, "t"); ban(a("seven years"), 1.6, "BANNED 7 YEARS")
    # 21 cannabis -----------------------------------------------------------------------
    card(("THE LAST ONE", A("and the last one the one")), "WEED", "CANNABIS · THC", "weed", (40, 200, 70))
    S(a("it don t make you faster"), "TEXT", lines=["DOESN'T MAKE YOU FASTER", "DOESN'T MAKE YOU STRONGER"])
    S(a("why it s banned"), "TEXT", lines=["THE RULE: 2 OF 3"]); lst(a("it helps you"), 4.6, ["HELPS YOU?", "DANGEROUS?", "AGAINST THE SPIRIT OF SPORT?"], (40, 200, 70))
    S(a("and you already know the name"), "shacarri21", 2.0, tag="NBC · 2021 OLYMPIC TRIALS"); name(a("sha carri"), 3.0, "SHA'CARRI RICHARDSON", "USA")
    S(a("2021 olympic trials"), "shacarri21", 30.0, tag="EUGENE · 2021", amb=1); stat(a("1086"), 2.4, "10.86", "2021 OLYMPIC TRIALS")
    S(a("fastest woman in america"), "shacarri21", 44.0, tag="EUGENE · 2021", amb=1)
    S(a("then it come out"), "shacarri_today", 2.0, tag="NBC TODAY · 2021"); pop(a("thc"), 1.6, "THC", RED, "c")
    S(a("she said she found out"), "shacarri_today", 60.0, tag="NBC TODAY · 2021")
    S(a("one month ban"), "shacarri_today", 40.0, tag="NBC TODAY · 2021"); ban(a("one month ban"), 1.6, "1-MONTH BAN")
    pop(a("but that month was the olympics"), 2.4, "THAT MONTH WAS THE OLYMPICS", RED, "b")
    S(a("and the whole country"), "shacarri21", 64.0, tag="EUGENE · 2021")
    # 22 close --------------------------------------------------------------------------
    S(a("so that s every banned"), "PHOTO", path=f"{P}/thumbs/v5/F_drugs_neon_tiles_HD.jpg", full=1)
    S(a("some of these got people"), "marionjones_ioc_ap", 2.0, tag="AP · IOC")
    S(a("one man got banned for life"), "benjohnson_ap95", 66.0, tag="AP · 1995"); pop(a("twice"), 1.4, "TWICE", RED, "c")
    S(a("one damn near killed"), "PHOTO", path=HK(5), bw=1, label="ST. LOUIS · 1904")
    S(a("and some of this stuff"), "jepchirchir_ktn", 12.0, tag="KTN NEWS · 2026")
    S(a("and here go what get me"), "montgomery02", 162.0, tag="ESPN2 · 2002"); pop(a("never failed"), 2.4, "NEVER FAILED A TEST", ORANGE, "b")
    O(a("retests"), 4.6, ("list", ["RETESTS", "PAPERWORK", "A SYRINGE IN THE MAIL"], list(ORANGE)))
    S(a("so when y all watch"), "paris200_final", 440.0, tag="PARIS 2024", amb=1)
    S(a("them samples"), "benjohnson_cbc25", 240.0, tag="LAB"); stat(a("them samples"), 3.0, "10 YEARS", "IN THE FREEZER", CYAN)
    S(a("which one shocked"), "TEXT", lines=[" "]); O(a("which one shocked"), 30.0, ("endq", "WHICH ONE SHOCKED", "YOU THE MOST?"))

# ------------------------------------------------------------------ final timeline
def timeline():
    """Shots and overlays in final-timeline seconds, soundbites and the pre-roll included."""
    build_edl()
    sb_raw = [s["t"] for s in SOUNDBITES]
    vo_shots = sorted(SHOTS, key=lambda s: s["t"])
    # after each soundbite, make sure a shot starts exactly where the VO resumes (continue the previous shot)
    for s in SOUNDBITES:
        if s["t"] <= 0: continue
        if any(abs(v["t"] - s["t"]) < 0.25 or (s["t"] < v["t"] < s["t"] + 0.6) for v in vo_shots): continue
        prev = max((v for v in vo_shots if v["t"] < s["t"]), key=lambda v: v["t"])
        cont = dict(prev); cont["t"] = s["t"] + 0.001
        if prev["src"] not in ("COUNT", "PHOTO", "TEXT"): cont["ss"] = prev["ss"] + (s["t"] - prev["t"])
        vo_shots.append(cont)
    vo_shots.sort(key=lambda s: s["t"])
    seq = [dict(T=0.0, src="benjohnson88", ss=36.0, tag="SEOUL 1988 · 100M FINAL", amb=1, full_amb=1)]
    for v in vo_shots:
        d = dict(v); d["T"] = round(FT(v["t"]), 3); seq.append(d)
    for s in SOUNDBITES:
        st = SB_START(s) - (PAD - 0.15)  # soundbite shot covers the pads too
        seq.append(dict(T=round(st, 3), src=s["src"], ss=round(s["ss"] - PAD, 3), tag=s["tag"], sb=1))
    seq.sort(key=lambda x: x["T"])
    end = FT(VO_END) + 5.0
    out = []
    for i, x in enumerate(seq):
        t1 = seq[i + 1]["T"] if i + 1 < len(seq) else end
        if t1 - x["T"] < 0.3: continue
        out.append((x, t1))
    # overlays: map to final time; clip at any soundbite start inside them
    ov = []
    for a0, a1, spec in OVER:
        f0, f1 = FT(a0), FT(a1)
        for s in SOUNDBITES:
            if a0 < s["t"] < a1: f1 = min(f1, s["t"] + (FT(s["t"] - 1e-3) - (s["t"] - 1e-3)))
        ov.append((round(f0, 3), round(min(f1, end), 3), spec))
    for s in SOUNDBITES:
        st = SB_START(s) - (PAD - 0.15); ov.append((round(st + 0.1, 3), round(st + s["dur"] + 2 * PAD - 0.1, 3), ("sbtag", s["tag"])))
    return out, ov, end

GRADE = "eq=contrast=1.08:saturation=1.12:gamma=0.97,colorbalance=rs=-0.03:bs=0.05:rh=0.04:bh=-0.02,vignette=PI/5"
def card_png(sh, key):
    out = f"{R}/cards/{hashlib.md5(json.dumps(key, sort_keys=True, default=str).encode()).hexdigest()[:12]}.png"
    if os.path.exists(out): return out
    if sh["src"] == "COUNT": im = count_card(sh["n"], sh["name"], sh["cat"], sh.get("ph"), tuple(sh["col"]), sh.get("sub"))
    elif sh["src"] == "TEXT": im = text_card(sh["lines"], tuple(sh.get("col", ORANGE)))
    elif sh.get("full"): im = ImageOps.fit(Image.open(sh["path"]).convert("RGB"), (W, Hh), Image.LANCZOS)
    else:
        crop = tuple(sh["crop"]) if sh.get("crop") else None
        im = photo_card(sh["path"], sh.get("label"), sh.get("sub"), CYAN if not sh.get("bw") else ORANGE, crop, sh.get("bw"))
    im.save(out); return out

def tag_png(tag):
    p = f"{R}/ov/tag_{hashlib.md5(tag.encode()).hexdigest()[:10]}.png"
    if not os.path.exists(p): archive_tag(tag).save(p)
    return p

def render_shot(i, sh, T1, OV):
    out = f"{R}/shots/{i:04d}.mp4"; T0 = sh["T"]
    dur = (round(T1 * FPS) - round(T0 * FPS)) / FPS
    mine = [o for o in OV if o[0] < T1 and o[1] > T0]
    key = json.dumps([sh, dur, GRADE, mine], sort_keys=True, default=str); stamp = f"{out}.key"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == key: return out
    src = sh["src"]; amb_vol = 0.0
    if src in ("COUNT", "TEXT", "PHOTO"):
        png = card_png(sh, [sh.get(k) for k in ("src", "n", "name", "cat", "ph", "col", "sub", "lines", "path", "label", "bw", "crop", "full")])
        ins = ["-loop", "1", "-t", f"{dur:.3f}", "-i", png]
        z = 0.06 if src == "COUNT" else 0.045
        base = f"[0:v]scale='trunc(1920*(1+{z}*t/{dur:.3f})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1"
        if src == "COUNT": base += ",eq=brightness='if(lt(t,0.12),0.35*(1-t/0.12),0)':eval=frame"
    else:
        ins = ["-ss", f"{max(0, sh['ss']):.3f}", "-t", f"{dur + 0.1:.3f}", "-i", f"{REAL}/{src}.mp4"]
        base = (f"[0:v]setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                f"scale='trunc(1920*(1+0.04*t/{dur:.3f})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1,{GRADE}")
        if sh.get("sb"): base = (f"[0:v]setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                                 f"eq=contrast=1.05:saturation=1.05")
        amb_vol = 1.0 if sh.get("sb") else (0.9 if sh.get("full_amb") else (0.18 if sh.get("amb") else 0.0))
        if not sh.get("sb"):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", tag_png(sh.get("tag", "ARCHIVE"))]
    vf = [base + ",fps=24,format=yuva420p[b0]"]; k = 0
    if src not in ("COUNT", "TEXT", "PHOTO") and not sh.get("sb"):
        k = 1; vf.append("[1:v]format=rgba[o1];[b0][o1]overlay=0:0[b1]")
    for (o0, o1, spec) in mine:
        a_, b_ = max(0, o0 - T0), min(dur, o1 - T0); png = overlay_png(spec); k += 1
        ins += ["-loop", "1", "-t", f"{b_:.3f}", "-i", png]
        fin = 0.15 if o0 >= T0 else 0; fout = 0.15 if o1 <= T1 else 0
        chain = f"[{k}:v]format=rgba"
        if fin: chain += f",fade=in:st={a_:.3f}:d={fin}:alpha=1"
        if fout: chain += f",fade=out:st={b_ - fout:.3f}:d={fout}:alpha=1"
        slide = f"if(lt(t-{a_:.3f},0.22),36*(1-(t-{a_:.3f})/0.22),0)" if fin and spec[0] in ("name", "stat", "pop", "list") else "0"
        vf.append(chain + f"[o{k}];[b{k - 1}][o{k}]overlay=x=0:y='{slide}':enable='between(t,{a_:.3f},{b_:.3f})'[b{k}]")
    vf.append(f"[b{k}]format=yuv420p[v]")
    ins += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]; amap = f"{k + 1}:a"
    if amb_vol > 0:
        hp = "" if sh.get("sb") else ",highpass=f=120"
        vf.append(f"[0:a]aresample=48000,volume={amb_vol}{hp},apad=whole_dur={dur:.3f}[a]"); amap = "[a]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(vf), "-map", "[v]", "-map", amap,
           "-t", f"{dur:.3f}", "-r", "24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-ar", "48000", "-ac", "2", out]
    run(cmd); open(stamp, "w").write(key); return out

_TL = None
def TL():
    global _TL
    if _TL is None: _TL = timeline()
    return _TL

def stage_shots():
    from concurrent.futures import ThreadPoolExecutor
    shots, ov, end = TL(); todo = list(enumerate(shots))
    only = os.environ.get("ONLY")
    if only: a, b = map(int, only.split("-")); todo = [x for x in todo if a <= x[0] <= b]
    for i, (sh, t1) in todo:   # PIL cards first (sequential, cached)
        if sh["src"] in ("COUNT", "TEXT", "PHOTO"): card_png(sh, [sh.get(k) for k in ("src", "n", "name", "cat", "ph", "col", "sub", "lines", "path", "label", "bw", "crop", "full")])
    for o in ov: overlay_png(o[2])
    with ThreadPoolExecutor(6) as ex: list(ex.map(lambda a: render_shot(a[0], a[1][0], a[1][1], ov), todo))
    print("shots", len(todo), "of", len(shots), "end", round(end, 1))

def stage_concat():
    shots, ov, end = TL(); lst = f"{R}/concat.txt"
    open(lst, "w").write("".join(f"file '{R}/shots/{i:04d}.mp4'\n" for i in range(len(shots))))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/picture.mp4"])
    print("concat", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/picture.mp4"]).stdout.strip(), "END", round(end, 2))

# ------------------------------------------------------------------ audio
def vo_track(end):
    """Voiceover with silence opened up for the pre-roll and every soundbite."""
    x = np.frombuffer(run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"]).stdout, np.float32).reshape(-1, 2) \
        if False else np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    SR = 48000; parts = [np.zeros((int(PRE * SR), 2), np.float32)]; last = 0
    for s in SOUNDBITES:
        if s["t"] <= 0:
            parts.append(np.zeros((int((s["dur"] + 2 * PAD) * SR), 2), np.float32)); continue
        cut = int(s["t"] * SR); parts.append(x[last:cut]); parts.append(np.zeros((int((s["dur"] + 2 * PAD) * SR), 2), np.float32)); last = cut
    parts.append(x[last:]); y = np.concatenate(parts)
    y = np.concatenate([y, np.zeros((max(0, int(end * SR) - len(y)), 2), np.float32)])[:int(end * SR)]
    p = f"{R}/vo_full.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", p], input=y.tobytes(), check=True)
    return p

def make_sfx(kind, seed):
    import sounds
    p = f"{R}/sfx/{kind}_{seed}.wav"
    if not os.path.exists(p):
        if kind == "decode": sounds.ui_sound("decode", p, seed)
        else: sounds.trans_sound(kind, p, seed)
    return p

def bed(path, t0, t1, vol, end, fin=1.5, fout=2.5, offset=0.0):
    out = f"{R}/bed_{os.path.basename(path)}_{t0:.1f}.wav"; L = t1 - t0; dl = int(t0 * 1000)
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", str(offset), "-i", path, "-t", f"{L:.2f}", "-af",
         f"volume={vol},afade=t=in:st=0:d={fin},afade=t=out:st={max(0, L - fout):.2f}:d={fout},adelay={dl}|{dl},apad=whole_dur={end:.2f}",
         "-ar", "48000", "-ac", "2", out]); return out

def stage_audio():
    shots, ov, end = TL(); vo = vo_track(end)
    M1 = f"{ROOT}/projects/jon-drummond/music"; M2 = f"{ROOT}/projects/ncaa-100m-champs/music"
    C = {k: FT(v) for k, v in CARD.items()}
    bonus = FT(at("before we get to the last one", CARD[19])); weed = FT(at("and the last one", CARD[19] + 30)); close = FT(at("so that s every banned", CARD[19] + 60))
    beds = [bed(f"{M1}/M1_cold-open-background.mp3", 0, C[1] + 0.5, 0.55, end, 0.5, 1.5),
            bed(f"{M2}/trap_bed.mp3", C[1] - 0.2, C[6] + 0.4, 0.38, end, 0.3, 1.5),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", C[6] - 0.2, C[10] + 0.4, 0.45, end, 0.6, 1.5),
            bed(f"{M2}/trap_bed.mp3", C[10] - 0.2, C[14] + 0.4, 0.38, end, 0.3, 1.5, offset=120),
            bed(f"{M1}/M4_coaching-ban.mp3", C[14] - 0.2, bonus + 0.4, 0.45, end, 0.6, 1.5),
            bed(f"{M2}/trap_bed.mp3", bonus - 0.2, weed + 0.4, 0.38, end, 0.3, 1.5, offset=200),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", weed - 0.2, close + 0.4, 0.45, end, 0.6, 1.5, offset=40),
            bed(f"{M1}/M5_verdict-ending.mp3", close - 0.2, end, 0.5, end, 0.8, 3.5)]
    S_ = []
    for j, (sh, t1) in enumerate(shots):
        if sh["src"] == "COUNT": S_.append((sh["T"] - 0.05, make_sfx("glitch", 100 + j), 0.55))
        elif sh.get("sb"): S_.append((sh["T"] - 0.05, make_sfx("scan", 300 + j), 0.35))
    for j, (o0, o1, spec) in enumerate(ov):
        k = spec[0]
        if k == "ban": S_.append((o0 - 0.04, make_sfx("zoom", 500 + j), 0.5))
        elif k in ("name", "stat"): S_.append((o0 - 0.05, make_sfx("streak", 700 + j), 0.3))
        elif k in ("pop", "list"): S_.append((o0 - 0.05, make_sfx("decode", 900 + j), 0.22))
    ins, fl = [], []; nb = len(beds); base = 2 + nb
    for j, (t, path, g) in enumerate(S_):
        ins += ["-i", path]; d = int(max(0, t) * 1000)
        fl.append(f"[{j + base}:a]volume={g},afade=t=out:st=1.4:d=0.5,adelay={d}|{d},aformat=sample_rates=48000:channel_layouts=stereo[s{j}]")
    bed_in = "".join(f"[{2 + j}:a]" for j in range(nb)); mix_in = "".join(f"[s{j}]" for j in range(len(S_)))
    fc = ";".join(fl) + (";" if fl else "") + \
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[pic];" \
        f"{bed_in}amix=inputs={nb}:normalize=0[music];[vo][pic]amix=inputs=2:normalize=0[key0];[key0]asplit=2[key][keyout];" \
        f"[music][key]sidechaincompress=threshold=0.025:ratio=6:attack=20:release=500[duck];" \
        f"[keyout][duck]{mix_in}amix=inputs={2 + len(S_)}:normalize=0:duration=first,alimiter=limit=0.95[out]"
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", f"{R}/picture.mp4"] + sum((["-i", b] for b in beds), []) + ins + \
          ["-filter_complex", fc, "-map", "[out]", "-t", f"{end:.2f}", "-ar", "48000", f"{R}/mix.wav"]
    run(cmd); print("audio", len(S_), "sfx")

def stage_mux():
    shots, ov, end = TL()
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", f"{end:.2f}", "-movflags", "+faststart", OUT])
    print("wrote", OUT)

def stage_check():
    shots, ov, end = TL()
    print("shots", len(shots), "overlays", len(ov), "end", round(end, 1), "soundbites", len(SOUNDBITES))
    for s in SOUNDBITES: print(" SB", round(s["t"], 1), "->", round(SB_START(s), 1), s["src"], s["dur"])
    print(" cards", {k: round(FT(v), 1) for k, v in CARD.items()})

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")

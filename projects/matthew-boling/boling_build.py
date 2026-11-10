"""The Downfall of Matthew Boling: documentary neon edit on the user's own voiceover (no tempo change).

Look: the channel's documentary neon (dark navy, cyan + orange glow, red for setbacks), HUD tags on real footage,
stat graphics for every time/place. Every time in the EDL is raw voiceover seconds (vo_user_v1_words.json);
FT() adds the short natural-sound pre-roll.

Run:  python3 projects/matthew-boling/boling_build.py [stage ...]   stages: shots concat audio mux (default all)
      ONLY=0-30 limits the shots stage to a range (preview).
"""
import os, sys, json, math, subprocess, hashlib, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/matthew-boling"
sys.path.insert(0, f"{ROOT}/tools")
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
BS = f"{SCR}/boling"; REAL = f"{BS}/real"; R = f"{BS}/render"
for d in ("ov", "shots", "cards", "sfx"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/boling_voiceover_user_v1.wav"
OUT = f"{SCR}/output/Downfall_of_Matthew_Boling_v1.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"; INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
INTB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"; MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
WHITE, BLACK = (248, 248, 252), (0, 0, 0)
ORANGE, CYAN, RED, PINK, YEL = (255, 122, 26), (0, 229, 255), (235, 30, 40), (255, 46, 99), (255, 214, 0)
NAVY = (6, 7, 13)

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/vo_user_v1_words.json"))[0]["words"]
_NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def _tok(w):
    t = "".join(ch for ch in w.lower() if ch.isalnum())
    return _NUMW[int(t)] if t.isdigit() and int(t) <= 20 else t
TOK = [_tok(x["w"]) for x in WORDS]
def at(phrase, after=0.0, end=False):
    p = [_tok(x) for x in phrase.split() if _tok(x)]
    for i in range(len(TOK) - len(p) + 1):
        if TOK[i:i + len(p)] == p and WORDS[i]["s"] >= after - 1e-6:
            return WORDS[i + len(p) - 1]["e"] if end else WORDS[i]["s"]
    raise KeyError(f"phrase not found after {after:.1f}: {phrase!r}")
VO_END = WORDS[-1]["e"]
PART = {k: min(w["s"] for w in WORDS if w["part"] == k) for k in range(1, 9)}

PRE = 2.0          # natural sound of the 2019 meet before the first word
SOUNDBITES = []
def FT(t): return t + PRE
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
# ------------------------------------------------------------------ edit decision list (raw VO seconds)
SHOTS, OVER = [], []
def S(t, src, ss=0.0, **o): SHOTS.append(dict(t=round(t, 3), src=src, ss=ss, **o))
def O(t, dur, spec): OVER.append((round(t, 3), round(t + dur, 3), spec))
def pop(t, dur, text, col=WHITE, pos="b"): O(t, dur, ("pop", text, list(col), pos))
def name(t, dur, n, sub): O(t, dur, ("name", n, sub))
def stat(t, dur, big, label, col=ORANGE): O(t, dur, ("stat", big, label, list(col)))
def ban(t, dur, text): O(t, dur, ("ban", text))
def lst(t, dur, lines, col=ORANGE): O(t, dur, ("list", lines, list(col)))

def build_edl():
    a = A
    T19, TST, TPA, TGA = "REGION MEET · APRIL 27, 2019", "TEXAS 6A STATE · MAY 2019", "PAN AM U20 · SAN JOSÉ 2019", "UNIVERSITY OF GEORGIA"
    # 1 cold open --------------------------------------------------------------------
    S(a("april"), "b998_dctf", 1.0, tag="HOUSTON · " + T19, amb=1); pop(a("april"), 3.0, "APRIL 27, 2019", WHITE, "t")
    S(a("a scene from"), "b998_flo", 0.0, tag=T19, amb=1); pop(a("straight jesuit"), 2.2, "STRAKE JESUIT · SENIOR", WHITE, "t")
    S(a("and runs") + 0.2, "b998_flo", 2.6, tag=T19, amb=1)
    S(a("998 in high school"), "b998_dctf", 23.3, tag=T19); stat(a("998 in high school"), 2.4, "9.98", "100M · IN HIGH SCHOOL")
    S(a("now the win"), "b998_flo", 15.0, tag=T19, amb=1); stat(a("way over"), 3.8, "+4.2 m/s", "WIND · LEGAL LIMIT IS +2.0", RED)
    pop(a("ain t matter"), 1.4, "DIDN'T MATTER", ORANGE, "c")
    S(a("by the next morning"), "b998_cbs", 1.5, tag="CBS MORNING NEWS · 2019")
    S(a("espn"), "b998_cbs", 5.8, tag="CBS MORNING NEWS · 2019"); lst(a("espn"), 3.6, ["ESPN", "CBS · FOX", "SPORTS ILLUSTRATED"], CYAN)
    S(a("everybody calling"), "b998_cbs", 10.0, tag="CBS MORNING NEWS · 2019"); pop(a("white lightning"), 1.7, "“WHITE LIGHTNING”", WHITE, "c")
    S(a("people saying"), "b998_cbs", 13.5, tag="CBS MORNING NEWS · 2019"); pop(a("usain bolt"), 2.0, "THE NEXT USAIN BOLT?", ORANGE, "b")
    S(a("his name was"), "b998_cbs", 18.6, tag="TEAM USA · 2019"); name(a("matthew") , 1.5, "MATTHEW BOLING", "STRAKE JESUIT · HOUSTON, TX")
    S(a("and seven years later"), "bdocshort", 360.5, tag=TGA); pop(a("seven years later"), 2.6, "7 YEARS LATER", WHITE, "t")
    S(a("what happened"), "bdocshort", 418.5, tag=TGA); pop(a("what happened"), 2.6, "WHAT HAPPENED?", ORANGE, "c")
    # 2 the hype was real --------------------------------------------------------------
    S(a("now first"), "bdocshort", 115.5, tag="STRAKE JESUIT"); pop(a("not a flute"), 2.0, "NOT A FLUKE", CYAN, "c")
    S(a("that same season"), "b1013", 40.0, tag=TST, amb=1)
    S(a("he ran 10") - 0.4, "b1013", 132.5, tag=TST, amb=1); stat(a("he ran 10") + 0.3, 5.0, "10.13", "LEGAL WIND · US HIGH SCHOOL RECORD")
    S(a("he won a long jump"), "bdocshort", 173.5, tag="STRAKE JESUIT"); stat(a("jumping 26"), 2.6, "26 FT", "LONG JUMP · STATE CHAMP", CYAN)
    S(a("and then he anchored"), "b4474", 140.0, tag=TST + " · 4X400", amb=1)
    S(a("he got the stick"), "b4474", 157.0, tag=TST + " · 4X400", amb=1); stat(a("20 meters"), 1.9, "20+ M", "BEHIND AT THE HANDOFF", RED)
    S(a("and ran a 44") - 0.3, "b4474", 170.0, tag=TST + " · 4X400", amb=1); stat(a("and ran a 44") + 0.4, 3.4, "44.74", "ANCHOR SPLIT")
    S(a("whole thing"), "b4474", 188.5, tag=TST + " · 4X400", amb=1)
    S(a("he won gatorade"), "bdocshort", 346.5, tag="STRAKE JESUIT"); pop(a("he won gatorade"), 2.8, "GATORADE NATIONAL ATHLETE OF THE YEAR", WHITE, "b")
    S(a("pan am"), "bpanam", 2.0, tag=TPA); stat(a("four gold"), 1.8, "4 GOLD", "PAN AM U20 CHAMPIONSHIPS", YEL)
    S(a("100 200"), "bpanam", 60.0, tag=TPA); lst(a("100 200"), 5.0, ["100M · 200M", "4X100 · 4X400", "BOTH RELAYS: U20 WORLD RECORDS"], YEL)
    S(a("oh and a nickname"), "bpanam", 100.0, tag=TPA); pop(a("oh and a nickname"), 2.6, "“WHITE LIGHTNING”", WHITE, "t")
    S(a("he didn t want"), "bpanam", 118.0, tag=TPA); pop(a("he didn t want"), 3.4, "HE DIDN'T LIKE IT", ORANGE, "b")
    S(a("he just wanted to run"), "bdocshort", 158.0, tag="HOUSTON")
    S(a("committed to georgia"), "bdocshort", 230.0, tag=TGA); pop(a("committed to georgia"), 2.6, "COMMITTED: GEORGIA", RED, "t")
    S(a("something crazy") - 1.0, "bdocshort", 303.0, tag=TGA)
    # 3 georgia ----------------------------------------------------------------------------
    S(a("his first year"), "bdocshort", 202.0, tag=TGA); pop(a("covid"), 2.6, "2020 · SEASON CANCELLED", RED, "b")
    S(a("2021 he came back"), "bncaa21", 2.0, tag="NCAA INDOOR · FAYETTEVILLE 2021", amb=1)
    stat(a("20 19") - 0.2, 3.6, "20.19", "NCAA INDOOR 200M CHAMPION", YEL)
    S(a("and for a minute"), "bncaa21", 84.0, tag="NCAA INDOOR · FAYETTEVILLE 2021")
    S(a("then the olympic trials"), "btrials21", 28.0, tag="OLYMPIC TRIALS · EUGENE 2021", amb=1)
    S(a("he goes out"), "btrials21", 98.0, tag="OLYMPIC TRIALS · 100M SEMIS", amb=1); stat(a("14th"), 2.6, "14TH", "100M SEMIS · OUT", RED)
    S(a("and then the 200"), "btrials21", 248.0, tag="OLYMPIC TRIALS · 200M SEMIS", amb=1); stat(a("ninth"), 2.2, "9TH", "200M SEMIS", RED)
    pop(a("one spot"), 2.4, "1 SPOT FROM THE FINAL", ORANGE, "b")
    S(a("that was the first time"), "btrials21", 290.0, tag="OLYMPIC TRIALS · EUGENE 2021")
    S(a("this ain t high school"), "bdocshort", 362.0, tag=TGA); pop(a("this ain t high school"), 2.8, "THIS AIN'T HIGH SCHOOL NO MORE", WHITE, "b")
    # 4 he actually got faster ---------------------------------------------------------------
    S(a("and here go the part"), "bdocshort", 389.0, tag=TGA); pop(a("people forget"), 1.8, "THE PART PEOPLE FORGET", CYAN, "t")
    S(a("2022 he runs"), "bdocshort", 305.0, tag="GEORGIA · 2022"); stat(a("2022 he runs") + 0.4, 4.0, "9.98", "AGAIN · GAINESVILLE 2022")
    pop(a("legal win"), 2.2, "+1.6 WIND · LEGAL", CYAN, "b")
    S(a("and a couple weeks later"), "b1992", 0.5, tag="GEORGIA TECH INVITATIONAL · 2022", amb=1); stat(a("1992"), 3.0, "19.92", "200M · APRIL 23, 2022", YEL)
    S(a("he won the sec"), "bsec22", 10.0, tag="SEC CHAMPIONSHIPS · 2022", amb=1); pop(a("he won the sec"), 2.0, "SEC CHAMPION · 200M", YEL, "t")
    S(a("took second"), "bsec22", 35.5, tag="SEC CHAMPIONSHIPS · 2022"); pop(a("took second"), 2.0, "2ND AT NCAAs", WHITE, "t")
    S(a("so he ain t slow"), "b1992", 42.5, tag="WORLD RANKINGS · 2022")
    lst(a("he a sub 10"), 3.2, ["SUB-10", "SUB-20"], CYAN)
    S(a("but at usa"), "bdocshort", 375.0, tag=TGA); stat(a("but at usa") + 0.3, 2.6, "6TH", "USATF 200M · 2022", RED)
    S(a("and in america"), "btrials21", 57.0, tag="HAYWARD FIELD · EUGENE"); pop(a("top ten in the world"), 3.6, "TOP 10 IN THE WORLD... STILL HOME", WHITE, "b")
    S(a("because the us"), "btrials21", 230.0, tag="HAYWARD FIELD · EUGENE"); pop(a("that deep"), 1.6, "THAT DEEP", ORANGE, "c")
    # 5 the switch ---------------------------------------------------------------------------
    S(a("2023 he wins"), "bncaa23", 52.0, tag="NCAA INDOOR · ALBUQUERQUE 2023", amb=1); stat(a("the indoor ncaa"), 3.2, "20.12", "NCAA INDOOR 200M CHAMPION · AGAIN", YEL)
    S(a("but outdoors"), "bdocshort", 404.0, tag=TGA); pop(a("make the finals"), 2.0, "NO FINAL", RED, "c")
    S(a("so he tried something"), "bdocshort", 389.0, tag=TGA); pop(a("the 400"), 1.8, "THE 400", ORANGE, "c")
    S(a("at usa s he finished"), "bdocshort", 317.0, tag=TGA); stat(a("6th again"), 2.6, "6TH", "USATF 400M · 45.17", ORANGE)
    S(a("got him on"), "bbudapest", 86.0, tag="WORLD CHAMPIONSHIPS · BUDAPEST 2023", amb=1); pop(a("budapest"), 2.0, "BUDAPEST WORLDS", CYAN, "t")
    S(a("and man he ran"), "bbudapest", 452.0, tag="BUDAPEST 2023 · MIXED 4X400 FINAL", amb=1); stat(a("3rd leg"), 2.6, "3RD LEG", "MIXED 4X400 · USA", CYAN)
    S(a("gold medal world"), "bbudapest", 655.0, tag="BUDAPEST 2023 · MIXED 4X400 FINAL", amb=1); stat(a("gold medal world"), 3.0, "3:08.80", "GOLD · WORLD RECORD", YEL)
    S(a("he ran in heats"), "bbudapest", 600.0, tag="BUDAPEST 2023", amb=1); pop(a("they won that too"), 1.8, "GOLD AGAIN", YEL, "b")
    S(a("so on paper"), "bbudapest", 826.0, tag="BUDAPEST 2023 · RESULTS"); pop(a("two time world"), 2.8, "2-TIME WORLD CHAMPION", YEL, "c")
    S(a("that september"), "bprobts", 117.0, tag="PRO · 2024"); pop(a("skips his last year"), 2.6, "TURNS PRO · SEPT 2023", ORANGE, "t")
    S(a("moved to south carolina"), "bprobts", 150.0, tag="PRO · SOUTH CAROLINA"); name(a("coach") , 2.8, "ALLEYNE FRANCIQUE", "NEW COACH · SOUTH CAROLINA")
    S(a("saying he wanted"), "bprobts", 255.0, tag="PRO · SOUTH CAROLINA"); pop(a("world stage"), 1.8, "THE WORLD STAGE", CYAN, "b")
    # 6 paris -------------------------------------------------------------------------------
    S(PART[6] - 0.3, "bprobts", 186.0, tag="2024 SEASON"); pop(PART[6] + 0.1, 2.6, "2024 · OLYMPIC YEAR", ORANGE, "t")
    S(a("this the one everybody"), "b998_flo", 3.0, tag="FLASHBACK · 2019", bw=1)
    S(a("he runs") , "bprobts", 208.0, tag="2024 SEASON", amb=1); stat(a("44") , 3.2, "44.84", "400M PR · JULY 2024", YEL)
    S(a("he gets the world indoor"), "bprobts", 296.0, tag="2024 SEASON", amb=1); lst(a("he gets the world indoor"), 3.6, ["WORLD INDOORS · SILVER", "WORLD RELAYS · GOLD"], YEL)
    S(a("then the trials"), "TEXT", lines=["2024 OLYMPIC TRIALS"], sub="EUGENE · JUNE 2024")
    S(a("in the 400 he makes") , "btrials21", 40.0, tag="HAYWARD FIELD · EUGENE"); stat(a("finishes eighth"), 3.4, "8TH", "400M FINAL · LAST", RED)
    S(a("in the 200 ninth"), "btrials21", 280.0, tag="HAYWARD FIELD · EUGENE"); stat(a("ninth again"), 2.6, "9TH", "200M · NO FINAL", RED)
    S(a("and they don t pick"), "bdocshort", 362.0, tag=TGA); ban(a("no pairs"), 2.2, "NO PARIS")
    # 7 now ---------------------------------------------------------------------------------
    S(PART[7] - 0.2, "bgst", 120.0, tag="GRAND SLAM TRACK · PHILADELPHIA 2025", amb=1); stat(a("seventh"), 3.0, "7TH", "200M · 20.87", RED)
    S(a("fifth") - 0.3, "bgst", 190.0, tag="GRAND SLAM TRACK · PHILADELPHIA 2025", amb=1); stat(a("fifth"), 2.4, "5TH", "400M", ORANGE)
    S(a("that year he ran"), "bdocshort", 303.0, tag="2026"); pop(a("that year he ran"), 4.2, "2026", CYAN, "t")
    stat(a("45") , 3.4, "45.51", "400M · JULY 10, 2026", WHITE)
    S(a("the kid that ran"), "b998_flo", 5.0, tag="FLASHBACK · 2019", bw=1); stat(a("at 18"), 2.0, "9.98", "AT 18", ORANGE)
    S(a("his best 100"), "b998_dctf", 24.0, tag="FLASHBACK · 2019"); stat(a("is still"), 3.0, "9.98", "STILL HIS BEST 100", CYAN)
    # 8 so is it really a downfall ----------------------------------------------------------
    S(PART[8] - 0.2, "bdocshort", 420.0, tag=TGA)
    S(a("is a two time"), "bbudapest", 655.0, tag="BUDAPEST 2023"); pop(a("is a two time"), 2.6, "2-TIME WORLD CHAMPION", YEL, "b")
    S(a("he ran sub 10"), "b1992", 25.0, tag="ATLANTA · 2022"); lst(a("he ran sub 10"), 3.2, ["SUB-10", "SUB-20"], CYAN)
    S(a("most people"), "bprobts", 318.0, tag="PRO · 2024")
    S(a("but that ain t"), "b998_cbs", 2.0, tag="CBS MORNING NEWS · 2019")
    S(a("promised the next"), "b998_cbs", 18.6, tag="TEAM USA · 2019"); pop(a("usain bolt"), 2.2, "“THE NEXT USAIN BOLT”", ORANGE, "c")
    S(a("he went viral"), "b998_cbs", 6.0, tag="CBS MORNING NEWS · 2019"); stat(a("wasn t even legal"), 2.6, "+4.2", "TAILWIND · NOT LEGAL", RED)
    S(a("before he ever ran"), "bdocshort", 230.0, tag=TGA)
    S(a("measured against"), "b998_flo", 2.6, tag="REGION MEET · 2019", bw=1); pop(a("one clip"), 3.0, "1 CLIP", ORANGE, "c")
    S(a("it s the hardest team"), "btrials21", 57.0, tag="HAYWARD FIELD · EUGENE"); pop(a("it s the hardest team"), 3.0, "THE HARDEST TEAM IN THE WORLD TO MAKE", WHITE, "b")
    S(a("sixth in america"), "btrials21", 232.0, tag="HAYWARD FIELD · EUGENE"); stat(a("sixth in america"), 3.6, "6TH IN THE US", "= TOP 10 IN THE WORLD", ORANGE)
    S(a("so was this a downfall"), "bdocshort", 404.0, tag=TGA); O(a("so was this a downfall"), 8.0, ("endq", "A DOWNFALL?", "OR TOO MUCH HYPE?"))
    S(a("let me know") - 0.3, "bdocshort", 418.5, tag=TGA)
    S(a("and if you was"), "b998_cbs", 19.0, tag="2019"); pop(a("hype train"), 3.4, "WERE YOU ON THE HYPE TRAIN?", ORANGE, "b")

# ------------------------------------------------------------------ final timeline
def timeline():
    build_edl()
    seq = [dict(T=0.0, src="b998_dctf", ss=0.0, tag="HOUSTON · APRIL 27, 2019", amb=1, full_amb=1)]
    for v in sorted(SHOTS, key=lambda s: s["t"]):
        d = dict(v); d["T"] = round(FT(v["t"]), 3); seq.append(d)
    seq.sort(key=lambda x: x["T"]); end = FT(VO_END) + 4.0; out = []
    for i, x in enumerate(seq):
        t1 = seq[i + 1]["T"] if i + 1 < len(seq) else end
        if t1 - x["T"] < 0.3: continue
        out.append((x, t1))
    ov = [(round(FT(a0), 3), round(min(FT(a1), end), 3), spec) for a0, a1, spec in OVER]
    return out, ov, end
GRADE = "eq=contrast=1.08:saturation=1.12:gamma=0.97,colorbalance=rs=-0.03:bs=0.05:rh=0.04:bh=-0.02,vignette=PI/5,tpad=stop_mode=clone:stop_duration=60"
def card_png(sh, key):
    out = f"{R}/cards/{hashlib.md5(json.dumps(key, sort_keys=True, default=str).encode()).hexdigest()[:12]}.png"
    if os.path.exists(out): return out
    if sh["src"] == "TEXT": im = text_card(sh["lines"], tuple(sh.get("col", ORANGE)), sh.get("sub"))
    elif sh.get("full"): im = ImageOps.fit(Image.open(sh["path"]).convert("RGB"), (W, Hh), Image.LANCZOS)
    else:
        crop = tuple(sh["crop"]) if sh.get("crop") else None
        im = photo_card(sh["path"], sh.get("label"), sh.get("sub"), CYAN if not sh.get("bw") else ORANGE, crop, sh.get("bw"))
    im.save(out); return out

def tag_png(tag):
    p = f"{R}/ov/tag_{hashlib.md5(tag.encode()).hexdigest()[:10]}.png"
    if not os.path.exists(p): archive_tag(tag).save(p + ".tmp.png"); os.replace(p + ".tmp.png", p)
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
        if sh.get("bw"): base += ",hue=s=0.12,eq=contrast=1.12"
        if sh.get("sb"): base = (f"[0:v]setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                                 f"eq=contrast=1.05:saturation=1.05,tpad=stop_mode=clone:stop_duration=30")
        amb_vol = 1.0 if sh.get("sb") else (0.9 if sh.get("full_amb") else (0.18 if sh.get("amb") else 0.0))
        if not sh.get("sb"):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", tag_png(sh.get("tag", "ARCHIVE"))]
    vf = [base + ",fps=24,format=yuva420p[b0]"]; k = 0
    if src not in ("COUNT", "TEXT", "PHOTO") and not sh.get("sb"):
        k = 1; vf.append("[1:v]format=rgba[o1];[b0][o1]overlay=0:0[b1]")
    for (o0, o1, spec) in mine:
        a_, b_ = max(0, o0 - T0), min(dur, o1 - T0)
        if b_ - a_ < 0.25: continue
        png = overlay_png(spec); k += 1
        ins += ["-loop", "1", "-t", f"{b_:.3f}", "-i", png]
        fd = min(0.15, (b_ - a_) / 3)
        fin = fd if o0 >= T0 else 0; fout = fd if o1 <= T1 else 0
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
    for _, (sh, t1) in todo:
        if sh["src"] not in ("COUNT", "TEXT", "PHOTO") and not sh.get("sb"): tag_png(sh.get("tag", "ARCHIVE"))
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

def vo_track(end):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    SR = 48000; y = np.concatenate([np.zeros((int(PRE * SR), 2), np.float32), x])
    y = np.concatenate([y, np.zeros((max(0, int(end * SR) - len(y)), 2), np.float32)])[:int(end * SR)]
    p = f"{R}/vo_full.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", p], input=y.tobytes(), check=True)
    return p

def stage_audio():
    shots, ov, end = TL(); vo = vo_track(end)
    M1 = f"{ROOT}/projects/jon-drummond/music"; Pt = {k: FT(v) for k, v in PART.items()}
    beds = [bed(f"{M1}/M1_cold-open-background.mp3", 0, Pt[2] + 0.4, 0.5, end, 1.0, 1.5),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", Pt[2] - 0.2, Pt[4] + 0.4, 0.42, end, 0.6, 1.5),
            bed(f"{M1}/M4_coaching-ban.mp3", Pt[4] - 0.2, Pt[6] + 0.4, 0.42, end, 0.6, 1.5),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", Pt[6] - 0.2, Pt[8] + 0.4, 0.42, end, 0.6, 1.5, offset=60),
            bed(f"{M1}/M5_verdict-ending.mp3", Pt[8] - 0.2, end, 0.48, end, 0.8, 3.5)]
    S_ = []
    for j, (sh, t1) in enumerate(shots):
        if sh["src"] == "TEXT": S_.append((sh["T"] - 0.05, make_sfx("glitch", 100 + j), 0.5))
        elif j and shots[j - 1][0]["src"] != sh["src"] and j % 3 == 0: S_.append((sh["T"] - 0.08, make_sfx(("scan", "pixel", "streak")[j % 3], 300 + j), 0.16))
    for j, (o0, o1, spec) in enumerate(ov):
        k = spec[0]
        if k == "ban": S_.append((o0 - 0.04, make_sfx("zoom", 500 + j), 0.5))
        elif k in ("name", "stat"): S_.append((o0 - 0.05, make_sfx("streak", 700 + j), 0.28))
        elif k in ("pop", "list"): S_.append((o0 - 0.05, make_sfx("decode", 900 + j), 0.2))
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
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-vn", "-af", f"aresample=48000:async=1:first_pts=0,apad=whole_dur={end:.2f}",
         "-t", f"{end:.2f}", "-ac", "2", "-c:a", "pcm_s16le", f"{R}/pic_audio.wav"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", f"{R}/pic_audio.wav"] + sum((["-i", b] for b in beds), []) + ins + \
          ["-filter_complex", fc, "-map", "[out]", "-t", f"{end:.2f}", "-ar", "48000", f"{R}/mix.wav"]
    run(cmd); print("audio", len(S_), "sfx")

def stage_mux():
    shots, ov, end = TL()
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", f"{end:.2f}", "-movflags", "+faststart", OUT])
    print("wrote", OUT)

def stage_check():
    shots, ov, end = TL()
    print("shots", len(shots), "overlays", len(ov), "end", round(end, 1))
    for sh, t1 in shots: print(f"{sh['T']:7.2f}-{t1:7.2f} {sh['src']:10s} {sh.get('ss',0):7.1f} {sh.get('tag','')}")
    for o in ov: print(f"  OV {o[0]:7.2f}-{o[1]:7.2f} {o[2][:3]}")

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")

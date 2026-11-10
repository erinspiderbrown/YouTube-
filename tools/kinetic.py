"""Animated kinetic graphics (overlays with alpha) for documentary edits.

Replaces the static neon stat boxes the user didn't like on the Boling cut (10 Nov 2026).
Style: bold condensed type (Anton) in white with a thick black stroke and a soft shadow, one accent
colour per graphic, things land with a slam (scale overshoot + 2-frame shake), labels wipe/type on,
numbers roll before they settle. Each graphic is frame(t, dur) -> RGBA 1920x1080; render() writes a
.mov (png codec, alpha) that ffmpeg can overlay.
"""
import math, os, random, subprocess
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 24
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"
INTB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INTBL = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
WHITE, BLACK = (250, 250, 250), (0, 0, 0)
ACC = {"orange": (255, 122, 26), "red": (232, 36, 44), "gold": (255, 196, 0), "cyan": (0, 214, 255),
       "white": (250, 250, 250), "green": (40, 210, 110)}


def eo(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def eback(t, s=2.2): t = min(max(t, 0), 1) - 1; return t * t * ((s + 1) * t + s) + 1
def seg(t, a, b): return min(max((t - a) / (b - a), 0), 1) if b > a else float(t >= a)


@lru_cache(64)
def F(path, size): return ImageFont.truetype(path, int(size))


def fit(text, path, size, maxw):
    while F(path, size).getlength(text) > maxw and size > 24: size -= 4
    return F(path, size)


def _txt_layer(text, font, fill, stroke=10):
    """Text on its own tight RGBA tile, black stroke + drop shadow."""
    l, t, r, b = font.getbbox(text, stroke_width=stroke)
    pad = 40; w, h = r - l + 2 * pad, b - t + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((pad - l, pad - t), text, font=font, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,))
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.75)))
    out = Image.new("RGBA", (w + 10, h + 14), (0, 0, 0, 0)); out.alpha_composite(sh, (8, 12)); out.alpha_composite(lay, (0, 0))
    return out, pad


def _paste_scaled(im, tile, cx, cy, s, alpha=1.0, anchor="c"):
    if s <= 0.01 or alpha <= 0.01: return
    tw, th = max(1, int(tile.width * s)), max(1, int(tile.height * s))
    t = tile.resize((tw, th), Image.BICUBIC)
    if alpha < 1: a = t.split()[-1].point(lambda v: int(v * alpha)); t.putalpha(a)
    x = int(cx - tw / 2) if anchor == "c" else int(cx)
    im.alpha_composite(t, (x, int(cy - th / 2)))


def _slam(t, t0, dur=0.26):
    """scale + shake for a slam-in starting at t0."""
    k = seg(t, t0, t0 + dur); s = 1.55 - 0.55 * eback(k, 1.4)
    sh = 0
    if t0 + dur <= t < t0 + dur + 0.12: sh = 7 * math.sin((t - t0) * 140)
    return s, sh


def _exit(t, dur, d=0.18):
    return 1 - seg(t, dur - d, dur)


def _roll(final, k, seed):
    """digits scramble until k reaches 1."""
    if k >= 1: return final
    rnd = random.Random(seed + int(k * 30)); n = int(len(final) * k)
    return "".join(c if (i < n or not c.isdigit()) else str(rnd.randint(0, 9)) for i, c in enumerate(final))


# ------------------------------------------------------------------ graphics
def stat(t, dur, big, label, col="orange", pos="l"):
    """Big number that rolls then slams, accent bar wipes, label types on. pos l (lower-left) or c."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c = ACC[col]; ex = _exit(t, dur)
    if ex <= 0: return im
    roll_k = seg(t, 0.0, 0.35)
    s, sh = _slam(t, 0.0)
    txt = _roll(big, roll_k, hash(big) & 999)
    f = fit(big, ANTON, 250, 1300); tile, pad = _txt_layer(txt, f, WHITE, 11)
    x0 = 120 if pos == "l" else W / 2 - F(ANTON, f.size).getlength(big) / 2 - pad
    cy = 560 if pos == "l" else 470
    # accent bar behind the label
    fl = fit(label, ANTON, 64, 1500); lw = fl.getlength(label) + 60
    bk = eo(seg(t, 0.18, 0.42)); by = cy + tile.height / 2 - 30
    d = ImageDraw.Draw(im)
    if bk > 0:
        d.rectangle([x0 + pad - 6, by, x0 + pad - 6 + lw * bk, by + 92], fill=c + (int(240 * ex),))
    # label typing
    lk = seg(t, 0.3, 0.6); n = int(round(len(label) * lk))
    if n:
        lt, lp = _txt_layer(label[:n], fl, BLACK if col in ("gold", "white", "cyan") else WHITE, 0)
        im.alpha_composite(lt if ex >= 1 else _fade(lt, ex), (int(x0 + pad - 6 + 30 - lp), int(by + 46 - lt.height / 2 + 4)))
    _paste_scaled(im, tile, x0 + sh, cy - 40, s, ex, anchor="l")
    return im


def _fade(tile, a):
    t = tile.copy(); t.putalpha(t.split()[-1].point(lambda v: int(v * a))); return t


def words(t, dur, text, col="white", pos="b", hi=None, size=130):
    """Kinetic line: words slam in one after another. hi = words (upper) drawn in the accent colour."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ex = _exit(t, dur)
    if ex <= 0: return im
    ws = text.split(); hi = set(x.strip(".,?!\"\u201c\u201d") for x in (hi or "").upper().split())
    f = fit(text, ANTON, size, W - 240); space = f.getlength(" ")
    widths = [f.getlength(w) for w in ws]; total = sum(widths) + space * (len(ws) - 1)
    y = {"b": H - 190, "c": H / 2, "t": 175}[pos]; x = W / 2 - total / 2
    for i, w in enumerate(ws):
        t0 = 0.07 * i; s, sh = _slam(t, t0, 0.22)
        if t >= t0:
            colr = ACC[col] if (w.upper().strip(".,?!\"“”") in hi or (col != "white" and not hi)) else WHITE
            tile, pad = _txt_layer(w, f, colr, 9)
            _paste_scaled(im, tile, x + widths[i] / 2 + sh, y, s, ex)
        x += widths[i] + space
    return im


def stack(t, dur, lines, col="orange"):
    """Lines stack in from the left, last one in the accent colour."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ex = _exit(t, dur); n = len(lines)
    if ex <= 0: return im
    y0 = H / 2 - (n - 1) * 72
    for j, l in enumerate(lines):
        k = eo(seg(t, 0.16 * j, 0.16 * j + 0.28))
        if k <= 0: continue
        f = fit(l, ANTON, 120, 1500); tile, pad = _txt_layer(l, f, ACC[col] if j == n - 1 else WHITE, 9)
        im.alpha_composite(_fade(tile, k * ex), (int(110 - pad - 160 * (1 - k)), int(y0 + j * 144 - tile.height / 2)))
    return im


def name(t, dur, nm, sub, col="orange"):
    """Lower third: accent line draws, name wipes up, sub types."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ex = _exit(t, dur); c = ACC[col]
    if ex <= 0: return im
    d = ImageDraw.Draw(im); x, y = 110, H - 250
    lk = eo(seg(t, 0, 0.3)); fn = fit(nm, ANTON, 120, 1300); nw = fn.getlength(nm)
    d.rectangle([x, y + 92, x + (nw + 40) * lk, y + 100], fill=c + (int(255 * ex),))
    k = eo(seg(t, 0.12, 0.4))
    if k > 0:
        tile, pad = _txt_layer(nm, fn, WHITE, 8)
        crop = tile.crop((0, 0, tile.width, int(tile.height * 1.0)))
        im.alpha_composite(_fade(crop, ex), (x - pad, int(y - 45 + 40 * (1 - k) - pad + 10)))
    n = int(len(sub) * seg(t, 0.35, 0.7))
    if n:
        fs = F(INTBL, 40); tile, pad = _txt_layer(sub[:n], fs, c, 5)
        im.alpha_composite(_fade(tile, ex), (x - pad, y + 112 - pad + 10))
    return im


def stamp(t, dur, text, col="red"):
    """Rubber stamp slam (bans, verdicts)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ex = _exit(t, dur); c = ACC[col]
    if ex <= 0: return im
    k = seg(t, 0, 0.18); s = 2.2 - 1.2 * eo(k)
    f = fit(text, ANTON, 190, 1500); tw = f.getlength(text)
    lay = Image.new("RGBA", (int(tw + 160), 330), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([12, 12, lay.width - 12, lay.height - 12], outline=c + (255,), width=16)
    d.text((lay.width / 2, lay.height / 2), text, font=f, fill=c + (255,), anchor="mm")
    lay = lay.rotate(7, expand=True, resample=Image.BICUBIC)
    dark = Image.new("RGBA", (W, H), (0, 0, 0, int(90 * min(1, t / 0.15) * ex))); im.alpha_composite(dark)
    sh = 10 * math.sin(t * 150) if 0.18 <= t < 0.32 else 0
    _paste_scaled(im, lay, W / 2 + sh, H / 2, s, ex * min(1, k * 3))
    return im


def chapter(t, dur, num, title, col="orange"):
    """Chapter slate over the picture: darkens, number slams, title wipes in."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, int(150 * _exit(t, dur, 0.3) * eo(seg(t, 0, 0.2)))))
    ex = _exit(t, dur, 0.3); c = ACC[col]
    if ex <= 0: return im
    s, sh = _slam(t, 0.05)
    fN = F(ANTON, 300); tile, pad = _txt_layer(num, fN, c, 12)
    _paste_scaled(im, tile, W / 2 + sh, 400, s, ex)
    k = eo(seg(t, 0.3, 0.6))
    if k > 0:
        ft = fit(title, ANTON, 120, 1600); tt, tp = _txt_layer(title, ft, WHITE, 9)
        cw = int(tt.width * k); tt = tt.crop((0, 0, max(1, cw), tt.height))
        im.alpha_composite(_fade(tt, ex), (int(W / 2 - (tt.width / k if k else 0) / 2), 620 - tt.height // 2))
    return im


def endq(t, dur, l1, l2):
    im = Image.new("RGBA", (W, H), (0, 0, 0, int(140 * eo(seg(t, 0, 0.3)))))
    a = words(t, dur, l1, "white", "c", size=150); im.alpha_composite(a, (0, -110))
    if t > 0.5: b = words(t - 0.5, dur - 0.5, l2, "orange", "c", size=150); im.alpha_composite(b, (0, 70))
    if t > 1.2: cq = words(t - 1.2, dur - 1.2, "LET ME KNOW IN THE COMMENTS", "cyan", "c", hi="COMMENTS", size=70); im.alpha_composite(cq, (0, 260))
    return im


def source(t, dur, text):
    """Small source credit, bottom-right (replaces the neon HUD corner tag)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); a = min(1, t / 0.25) * _exit(t, dur, 0.25)
    if a <= 0: return im
    f = F(INTB, 26); tw = f.getlength(text); d = ImageDraw.Draw(im)
    d.rectangle([W - 70 - tw - 24, H - 84, W - 70, H - 46], fill=(0, 0, 0, int(140 * a)))
    d.rectangle([W - 70 - tw - 24, H - 84, W - 70 - tw - 18, H - 46], fill=ACC["orange"] + (int(255 * a),))
    d.text((W - 70 - tw - 6, H - 65), text, font=f, fill=WHITE + (int(235 * a),), anchor="lm")
    return im


KINDS = dict(stat=stat, words=words, stack=stack, name=name, stamp=stamp, chapter=chapter, endq=endq, source=source)


def render(spec, dur, out):
    """spec = (kind, *args). Writes a png-in-mov with alpha, dur seconds."""
    fn = KINDS[spec[0]]; n = max(1, round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out + ".tmp.mov"], stdin=subprocess.PIPE)
    blank = None
    for i in range(n):
        im = fn(i / FPS, dur, *spec[1:])
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); os.replace(out + ".tmp.mov", out)
    return out


if __name__ == "__main__":   # quick look: python3 tools/kinetic.py OUTDIR
    import sys
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    bg = Image.new("RGBA", (W, H), (60, 90, 70, 255))
    tests = [("stat", 2.5, ("stat", "9.98", "100M · IN HIGH SCHOOL", "orange")), ("words", 2.0, ("words", "THE NEXT USAIN BOLT?", "orange", "b", "BOLT?")),
             ("stack", 2.0, ("stack", ["ESPN", "CBS · FOX", "SPORTS ILLUSTRATED"], "cyan")), ("name", 2.5, ("name", "MATTHEW BOLING", "STRAKE JESUIT · HOUSTON, TX")),
             ("stamp", 2.0, ("stamp", "NO PARIS")), ("chapter", 2.5, ("chapter", "02", "THE HYPE WAS REAL")), ("source", 2.0, ("source", "CBS MORNING NEWS · 2019"))]
    for nm, dur, spec in tests:
        for tt in (0.1, 0.3, 1.0):
            fr = bg.copy(); fr.alpha_composite(KINDS[spec[0]](tt, dur, *spec[1:])); fr.convert("RGB").resize((640, 360)).save(f"{o}/{nm}_{tt}.jpg")
    print("ok")

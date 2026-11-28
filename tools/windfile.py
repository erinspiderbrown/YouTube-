"""WIND FILE: the Gout Gout v3 visual identity (28 Nov 2026).

The user: the usual graphics "look like regular Claude graphics... the same colors and fonts and shapes and graphs
that I see in every other video made by Claude. Do something unique." So nothing here uses Inter/Anton/Bebas, pills,
glass boxes, yellow numbers or bar tables. The motif comes from the story (it's all about wind):
  - type: Instrument Serif (italic for statements, quotes, titles) + JetBrains Mono (instrument readouts, labels)
    + Space Grotesk (subtitles only, for legibility)
  - palette: ink navy, ice cyan (instrument light), warm paper white, coral for illegal / over-the-limit wind
  - motifs: drifting wind streamlines behind titles, an anemometer dial for every wind reading, survey crosshair
    ticks instead of boxes, a "drift chart" (dumbbell on a time axis) for the finalists' next races
Interface: same frame(t, dur, *args) -> RGBA 1920x1080 kinds, registered into modern.KINDS (import last).
Kinds: subs, iname, name, title, number, chapter, date, wipe, quote, board, nextrace, drift, stamp, dial
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from functools import lru_cache
import modern as K
from modern import W, H, ease, inout, seg, life, layer

FD = "/home/user/YouTube-/tools/fonts"
SERIF, SERIF_I = f"{FD}/InstrumentSerif-Regular.ttf", f"{FD}/InstrumentSerif-Italic.ttf"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-{}.ttf"
GROT = f"{FD}/SpaceGrotesk[wght].ttf"
INK = (6, 18, 28); CYAN = (155, 232, 255); PAPER = (243, 238, 228); CORAL = (255, 92, 120); MUTE = (150, 170, 182)


@lru_cache(256)
def F(path, size, wght=None):
    import glob
    if "{}" in path:
        cands = glob.glob(path.format(wght or "Medium")) or glob.glob("/usr/share/fonts/**/JetBrainsMono-Medium.ttf", recursive=True)
        path = cands[0]
    f = ImageFont.truetype(path, int(size))
    if wght and path.endswith("].ttf"):
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f


def tracked_w(txt, f, tr): return sum(f.getlength(c) for c in txt) + tr * max(0, len(txt) - 1)


def draw_tr(d, x, y, txt, f, fill, tr=0, anchor="l"):
    w = tracked_w(txt, f, tr)
    if anchor == "c": x -= w / 2
    elif anchor == "r": x -= w
    for c in txt: d.text((x, y), c, font=f, fill=fill, anchor="ls"); x += f.getlength(c) + tr
    return w


def glow(im, r=14, a=0.55, col=None):
    """Soft halo under the drawing (instrument light), plus a faint dark drop for legibility."""
    al = im.split()[3]
    out = layer()
    dark = Image.new("RGBA", im.size, (0, 0, 0, 0)); dark.putalpha(al.filter(ImageFilter.GaussianBlur(r * 1.4)).point(lambda v: int(v * 0.6)))
    out.alpha_composite(dark, (0, 4))
    if col:
        g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(al.filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * a))); out.alpha_composite(g)
    out.alpha_composite(im); return out


def fade(im, k):
    if k >= 1: return im
    o = im.copy(); o.putalpha(im.split()[3].point(lambda v: int(v * max(0, k)))); return o


def wind_in(im, k, dist=140):
    """Letters blow in from the left: horizontal motion smear that resolves as k -> 1."""
    if k >= 1: return im
    if k <= 0: return layer()
    arr = np.asarray(im, np.float32); n = int(2 + 14 * (1 - k)); dx = dist * (1 - k)
    acc = np.zeros_like(arr)
    for i in range(n):
        s = int(-dx * i / max(1, n - 1)); acc += np.roll(arr, s, axis=1)
    acc /= n; out = Image.fromarray(acc.astype(np.uint8), "RGBA"); return fade(out, k)


def scrim(a, where="full"):
    im = layer()
    if a <= 0: return im
    g = np.zeros((H, W, 4), np.uint8); g[..., :3] = INK
    if where == "full": g[..., 3] = int(255 * a)
    else:
        y = np.arange(H, dtype=np.float32); ramp = np.clip((y - H * 0.42) / (H * 0.58), 0, 1) ** 1.3
        g[..., 3] = (255 * a * ramp)[:, None].astype(np.uint8)
    return Image.fromarray(g, "RGBA")


def streamlines(t, k, seed=7, n=46, region=(0, 0, W, H), col=CYAN, alpha=0.35, speed=520):
    """Signature motif: thin wind streaks drifting left->right with fading tails, gently curving."""
    im = layer(); d = ImageDraw.Draw(im); rng = np.random.default_rng(seed); x0, y0, x1, y1 = region
    for i in range(n):
        y = rng.uniform(y0, y1); ph = rng.uniform(0, 1); L = rng.uniform(120, 420); amp = rng.uniform(6, 22); fr = rng.uniform(0.002, 0.006)
        sp = speed * rng.uniform(0.6, 1.4); head = x0 + ((ph * (x1 - x0 + L) + sp * t) % (x1 - x0 + L)) - L * 0.2
        pts = []
        for j in range(14):
            xx = head - L * j / 13; pts.append((xx, y + amp * math.sin(fr * xx + i)))
        a = alpha * k * rng.uniform(0.4, 1.0)
        for j in range(13):
            aa = int(255 * a * (1 - j / 13) ** 1.6)
            if aa > 2: d.line([pts[j], pts[j + 1]], fill=col + (aa,), width=2 if j < 3 else 1)
    return im


def ticks(d, x0, y0, x1, y1, a, L=22, col=PAPER):
    """Survey crosshair corners instead of a box."""
    c = col + (int(200 * a),)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x, y), (x + sx * L, y)], fill=c, width=2); d.line([(x, y), (x, y + sy * L)], fill=c, width=2)


def _roll(final, k):
    digs = [c for c in final if c.isdigit()]
    if not digs or k >= 1: return final
    val = int("".join(digs)); cur = str(int(val * k)).zfill(len(digs)); it = iter(cur)
    return "".join(next(it) if c.isdigit() else c for c in final)


def wind_val(s):
    """'+3.4 wind' / '+2.3' / '-2.1' -> float or None."""
    import re
    m = re.match(r"^\s*([+\-]\d+(?:\.\d+)?)", s or "")
    return float(m.group(1)) if m else None


def dial(t, dur, val, label="", x=W - 250, y=230, r=92, k_override=None):
    """Anemometer: arc from -3 to +4 m/s, legal zone cyan, over +2.0 coral; needle swings to val."""
    k = life(t, dur, 0.4, 0.4) if k_override is None else k_override
    im = layer(); d = ImageDraw.Draw(im)
    a0, a1 = 150, 390   # degrees (PIL: 0 = 3 o'clock, clockwise)
    ang = lambda v: a0 + (a1 - a0) * (min(4, max(-3, v)) + 3) / 7
    d.arc([x - r, y - r, x + r, y + r], a0, ang(2.0), fill=CYAN + (int(170 * k),), width=3)
    d.arc([x - r, y - r, x + r, y + r], ang(2.0), a1, fill=CORAL + (int(230 * k),), width=5)
    for v in range(-3, 5):
        A = math.radians(ang(v)); d.line([(x + (r - 12) * math.cos(A), y + (r - 12) * math.sin(A)), (x + r * math.cos(A), y + r * math.sin(A))], fill=PAPER + (int(200 * k),), width=2)
    sw = ease(seg(t, 0.15, 1.0)); cur = -3 + (val + 3) * sw + 0.25 * math.sin(t * 9) * (1 - sw)
    A = math.radians(ang(cur)); col = CORAL if cur > 2.0 else PAPER
    d.line([(x, y), (x + (r - 18) * math.cos(A), y + (r - 18) * math.sin(A))], fill=col + (int(255 * k),), width=4)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col + (int(255 * k),))
    f = F(MONO, 30, "Bold"); txt = f"{val:+.1f}"; d.text((x, y + 48), txt, font=f, fill=(CORAL if val > 2.0 else PAPER) + (int(255 * k),), anchor="ms")
    draw_tr(d, x, y + 74, "M/S" + (" · " + label.upper() if label else ""), F(MONO, 15), MUTE + (int(230 * k),), 3, "c")
    return glow(im, 10, 0.35, CYAN)


# ------------------------------------------------------------------ kinds
def subs(t, dur, words, size=48):
    """Clean subtitles, no box: Space Grotesk, spoken word full white with a cyan underline sweep, rest dimmed."""
    f = F(GROT, size, 560); maxw = W - 520; lines, cur = [], []
    for w in words:
        if cur and f.getlength(" ".join(x[0] for x in cur + [w])) > maxw: lines.append(cur); cur = []
        cur.append(w)
    if cur: lines.append(cur)
    pages = [lines[i:i + 2] for i in range(0, len(lines), 2)]; curp = None
    for pg in pages:
        if t >= pg[0][0][1] - 0.15: curp = pg
    if not curp: return layer()
    a = curp[0][0][1]; b = curp[-1][-1][2]; nxt = [p for p in pages if p[0][0][1] > a]; end = (nxt[0][0][0][1] - 0.05) if nxt else b + 0.7
    k = ease(seg(t, a - 0.15, a + 0.12)) * (1 - ease(seg(t, end - 0.15, end + 0.1)))
    if k <= 0: return layer()
    im = layer(); d = ImageDraw.Draw(im); lh = size * 1.34; y0 = H - 110 - (len(curp) - 1) * lh
    for li, ln in enumerate(curp):
        x = W / 2 - f.getlength(" ".join(w[0] for w in ln)) / 2
        for w, w0, w1 in ln:
            on = ease(seg(t, w0 - 0.04, w0 + 0.1)); ww = f.getlength(w)
            c = tuple(int(MUTE[i] * 0.85 + (PAPER[i] - MUTE[i] * 0.85) * on) for i in range(3))
            d.text((x, y0 + li * lh), w, font=f, fill=c + (int(255 * k),), anchor="ls")
            u = ease(seg(t, w0, w1 + 0.05)) * (1 - ease(seg(t, w1 + 0.05, w1 + 0.35)))
            if u > 0: d.line([(x, y0 + li * lh + 10), (x + ww * u, y0 + li * lh + 10)], fill=CYAN + (int(230 * k),), width=3)
            x += f.getlength(w + " ")
    return glow(im, 8, 0.0)


def iname(t, dur, nm, role, where=""):
    """Name blows in (serif), role and source as mono readout lines, cyan hairline + crosshair ticks."""
    L = min(dur, 4.8); k = ease(seg(t, 0.0, 0.5)) * (1 - inout(seg(t, L - 0.45, L)))
    if k <= 0: return layer()
    x, y = 120, H - 250; im = layer(); d = ImageDraw.Draw(im)
    fN = F(SERIF, 76); nw = fN.getlength(nm)
    n = layer(); ImageDraw.Draw(n).text((x, y), nm, font=fN, fill=PAPER + (255,), anchor="ls"); im.alpha_composite(wind_in(n, ease(seg(t, 0.05, 0.75))))
    g = ease(seg(t, 0.2, 0.9)); d.line([(x, y + 18), (x + (nw + 40) * g, y + 18)], fill=CYAN + (220,), width=2)
    yy = y + 52
    if role: draw_tr(d, x, yy, role.upper(), F(MONO, 22, "Medium"), PAPER + (int(235 * ease(seg(t, 0.35, 0.9))),), 2); yy += 32
    if where: draw_tr(d, x, yy, "SRC / " + where.upper(), F(MONO, 16, "Regular"), MUTE + (int(220 * ease(seg(t, 0.5, 1.0))),), 3)
    ticks(d, x - 34, y - 86, x + max(nw, 520) + 50, yy + 22, ease(seg(t, 0.3, 0.9)), 18)
    out = scrim(0.5 * k, "bottom"); out.alpha_composite(fade(glow(im, 12, 0.25, CYAN), k)); return out


def name(t, dur, nm, sub, side="l"): return iname(t, dur, nm, sub, "")


def title(t, dur, kicker, headline, pos="bl"):
    """Kicker as an instrument line ('// KICKER'), headline in big serif italic, wind streaks drift behind it."""
    k = life(t, dur, 0.5, 0.45); out = scrim(0.62 * k, "bottom")
    out.alpha_composite(streamlines(t, k, seed=len(headline), n=26, region=(0, H - 420, W, H - 120), alpha=0.28))
    im = layer(); d = ImageDraw.Draw(im); x, y = 120, H - 170
    draw_tr(d, x, y - 150, "// " + kicker.upper(), F(MONO, 22, "Medium"), CYAN + (int(255 * ease(seg(t, 0, 0.5))),), 3)
    f = F(SERIF_I, 160)
    while f.getlength(headline) > W - 260: f = F(SERIF_I, f.size - 6)
    h = layer(); ImageDraw.Draw(h).text((x - 6, y), headline, font=f, fill=PAPER + (255,), anchor="ls")
    im.alpha_composite(wind_in(h, ease(seg(t, 0.1, 0.85)), 220))
    out.alpha_composite(fade(glow(im, 16, 0.2, CYAN), 1 - inout(seg(t, dur - 0.45, dur)))); return out


def number(t, dur, value, label, sub=""):
    """Big serif numerals roll and settle; label as a mono readout; if the value is a wind reading, add the dial."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.6 * k)
    wv = wind_val(value); f = F(SERIF, 300)
    while f.getlength(value) > W - 400: f = F(SERIF, f.size - 10)
    im = layer(); d = ImageDraw.Draw(im); cx = W / 2 - (160 if wv is not None else 0)
    txt = _roll(value, ease(seg(t, 0.05, 0.9))); col = CORAL if (wv is not None and wv > 2.0) else PAPER
    d.text((cx, H / 2 + 70), txt, font=f, fill=col + (255,), anchor="ms")
    draw_tr(d, cx, H / 2 + 140, label.upper(), F(MONO, 24, "Medium"), PAPER + (int(240 * ease(seg(t, 0.35, 0.9))),), 4, "c")
    if sub: draw_tr(d, cx, H / 2 + 180, sub.upper(), F(MONO, 18), MUTE + (int(220 * ease(seg(t, 0.5, 1.0))),), 4, "c")
    out.alpha_composite(fade(glow(im, 18, 0.3, CYAN), k))
    if wv is not None: out.alpha_composite(dial(t, dur, wv, "", x=W / 2 + 470, y=H / 2 - 10, r=120))
    return out


def chapter(t, dur, num, ttl):
    """Full-frame wind field, 'FILE 05' mono, title in huge serif italic blowing in, a cyan horizon line."""
    k = life(t, dur, 0.55, 0.5); out = scrim(0.78 * k)
    out.alpha_composite(streamlines(t, k, seed=int(num) * 13, n=70, alpha=0.4, speed=700))
    im = layer(); d = ImageDraw.Draw(im)
    draw_tr(d, W / 2, H / 2 - 140, f"FILE {num}", F(MONO, 26, "Bold"), CYAN + (int(255 * ease(seg(t, 0, 0.5))),), 10, "c")
    f = F(SERIF_I, 220)
    while f.getlength(ttl) > W - 260: f = F(SERIF_I, f.size - 8)
    h = layer(); ImageDraw.Draw(h).text((W / 2, H / 2 + 70), ttl, font=f, fill=PAPER + (255,), anchor="ms"); im.alpha_composite(wind_in(h, ease(seg(t, 0.15, 1.0)), 300))
    g = ease(seg(t, 0.4, 1.3)); L = 380 * g; d.line([(W / 2 - L, H / 2 + 120), (W / 2 + L, H / 2 + 120)], fill=CYAN + (180,), width=2)
    out.alpha_composite(fade(glow(im, 18, 0.3, CYAN), 1 - inout(seg(t, dur - 0.5, dur)))); return out


def date(t, dur, text, sub=""):
    k = life(t, dur, 0.5, 0.5); out = scrim(0.5 * k); im = layer(); d = ImageDraw.Draw(im)
    h = layer(); ImageDraw.Draw(h).text((W / 2, H / 2 + 40), text, font=F(SERIF_I, 140), fill=PAPER + (255,), anchor="ms"); im.alpha_composite(wind_in(h, ease(seg(t, 0.1, 0.85))))
    if sub: draw_tr(d, W / 2, H / 2 + 110, sub.upper(), F(MONO, 24, "Medium"), CYAN + (int(240 * ease(seg(t, 0.4, 1.0))),), 6, "c")
    out.alpha_composite(fade(glow(im, 14, 0.25, CYAN), 1 - inout(seg(t, dur - 0.5, dur)))); return out


def wipe(t, dur, lines, kicker="", pos="c", size=128):
    """Statement in serif italic, line by line blowing in; the last line in cyan; kicker as mono."""
    k = life(t, dur, 0.4, 0.45); out = scrim(0.64 * k)
    out.alpha_composite(streamlines(t, k, seed=len(lines[0]), n=40, alpha=0.25))
    f = F(SERIF_I, size)
    for ln in lines:
        while f.getlength(ln) > W - 240: f = F(SERIF_I, f.size - 6)
    im = layer(); d = ImageDraw.Draw(im); lh = f.size * 1.02; y = H / 2 - (len(lines) - 1) * lh / 2 + f.size * 0.3
    if kicker: draw_tr(d, W / 2, y - f.size - 10, "// " + kicker.upper(), F(MONO, 22, "Medium"), CYAN + (230,), 4, "c")
    for i, ln in enumerate(lines):
        h = layer(); col = CYAN if (i == len(lines) - 1 and len(lines) > 1) else PAPER
        ImageDraw.Draw(h).text((W / 2, y + i * lh), ln, font=f, fill=col + (255,), anchor="ms")
        im.alpha_composite(wind_in(h, ease(seg(t, 0.1 + 0.3 * i, 0.85 + 0.3 * i)), 260))
    out.alpha_composite(fade(glow(im, 16, 0.25, CYAN), 1 - inout(seg(t, dur - 0.45, dur)))); return out


def quote(t, dur, text, who=""):
    """The user likes on-screen quotes: big serif italic, words settle in one by one, cyan rule, mono attribution."""
    out = scrim(0.66 * life(t, dur, 0.5, 0.45)); fo = 1 - inout(seg(t, dur - 0.45, dur))
    f = F(SERIF_I, 76); words = text.split(); lines, cur = [], []
    for wd in words:
        if cur and f.getlength(" ".join(cur + [wd])) > W - 640: lines.append(cur); cur = []
        cur.append(wd)
    if cur: lines.append(cur)
    n = len(words); per = min(0.2, max(0.07, dur * 0.4 / max(1, n))); im = layer(); d = ImageDraw.Draw(im); lh = 92
    y0 = H / 2 - (len(lines) - 1) * lh / 2 + 24; x0 = 330
    d.line([(x0 - 50, y0 - 70), (x0 - 50, y0 - 70 + (len(lines) * lh + 30) * ease(seg(t, 0, 0.8)))], fill=CYAN + (int(220 * fo),), width=3)
    i = 0
    for li, ln in enumerate(lines):
        x = x0
        for wd in ln:
            a = ease(seg(t, 0.2 + i * per, 0.2 + i * per + 0.35)) * fo
            d.text((x, y0 + li * lh), wd, font=f, fill=PAPER + (int(255 * a),), anchor="ls"); x += f.getlength(wd + " "); i += 1
    if who:
        a = ease(seg(t, 0.2 + n * per, 0.8 + n * per)) * fo
        draw_tr(d, x0, y0 + len(lines) * lh + 20, "— " + who.upper(), F(MONO, 22, "Medium"), CYAN + (int(240 * a),), 3)
    out.alpha_composite(glow(im, 14, 0.15, CYAN)); return out


def board(t, dur, kicker, rows, note=""):
    """Readout list (not a table): each row is a mono label, a serif time, and the wind as a small vector arrow
    whose length is the wind speed (coral when over +2.0). Rows print in like an instrument log."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.74 * k); fo = 1 - inout(seg(t, dur - 0.45, dur))
    out.alpha_composite(streamlines(t, k * 0.6, seed=len(rows) * 5, n=30, alpha=0.18))
    n = len(rows); rh = min(92, int(640 / max(1, n))); top = H / 2 - n * rh / 2 + 40; x0 = 300; x1 = 820; x2 = 1150
    im = layer(); d = ImageDraw.Draw(im)
    draw_tr(d, x0, top - 70, "// " + kicker.upper(), F(MONO, 24, "Medium"), CYAN + (int(255 * k),), 3)
    ticks(d, x0 - 50, top - 120, W - 250, top + n * rh + (60 if note else 20), k, 20)
    fl = F(MONO, int(rh * 0.3), "Medium"); fv = F(SERIF, int(rh * 0.72)); fn = F(MONO, int(rh * 0.27))
    for i, (a, b, c, hi) in enumerate(rows):
        kr = ease(seg(t, 0.3 + i * 0.16, 0.7 + i * 0.16)) * fo
        if kr <= 0: continue
        y = top + i * rh + rh * 0.7; col = PAPER if hi else MUTE
        draw_tr(d, x0, y - 6, a.upper(), fl, col + (int(255 * kr),), 2)
        d.text((x1, y + 6), b, font=fv, fill=PAPER + (int(255 * kr),), anchor="ls")
        wv = wind_val(c)
        if wv is not None:
            L = 40 * abs(wv) * ease(seg(t, 0.45 + i * 0.16, 0.95 + i * 0.16)); cc = CORAL if wv > 2.0 else CYAN; sx = x2 + 10
            dirn = 1 if wv >= 0 else -1; ex = sx + dirn * L
            d.line([(sx, y - 14), (ex, y - 14)], fill=cc + (int(255 * kr),), width=4)
            if L > 6: d.polygon([(ex, y - 24), (ex + dirn * 16, y - 14), (ex, y - 4)], fill=cc + (int(255 * kr),))
            draw_tr(d, W - 300, y - 6, c.upper(), fn, cc + (int(255 * kr),), 2, "r")
        else: draw_tr(d, W - 300, y - 6, c.upper(), fn, col + (int(255 * kr),), 2, "r")
        d.line([(x0, top + (i + 1) * rh + 2), (W - 300, top + (i + 1) * rh + 2)], fill=PAPER + (int(30 * kr),), width=1)
    if note: draw_tr(d, x0, top + n * rh + 44, note.upper(), F(MONO, 18), MUTE + (int(230 * ease(seg(t, 0.4 + n * 0.16, 1.0 + n * 0.16)) * fo),), 3)
    out.alpha_composite(glow(im, 10, 0.12, CYAN)); return out


def _tx(v, lo, hi, x0, x1): return x0 + (x1 - x0) * (v - lo) / (hi - lo)


def drift(t, dur, title_, rows, upto=None):
    """Drift chart for the finalists: one line per runner on a time axis (19.6 -> 21.5 s). A cyan dot lands on the
    Sydney time, then the line drifts right to the next race (coral dot) - everybody's line blows the same way.
    rows = [(name, sydney, next_or_None, next_label)]; upto = number of rows revealed (for syncing to the VO)."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.8 * k); fo = 1 - inout(seg(t, dur - 0.45, dur))
    out.alpha_composite(streamlines(t, k * 0.5, seed=91, n=34, alpha=0.16))
    im = layer(); d = ImageDraw.Draw(im); lo, hi = 19.5, 21.6; X0, X1 = 640, W - 380
    n = len(rows); rh = min(86, int(700 / n)); top = 230
    draw_tr(d, 150, top - 90, "// " + title_.upper(), F(MONO, 24, "Medium"), CYAN + (int(255 * k),), 3)
    for v in (19.5, 20.0, 20.5, 21.0, 21.5):
        x = _tx(v, lo, hi, X0, X1); d.line([(x, top - 40), (x, top + n * rh)], fill=PAPER + (int(34 * k),), width=1)
        draw_tr(d, x, top + n * rh + 34, f"{v:.1f}", F(MONO, 18), MUTE + (int(220 * k),), 1, "c")
    draw_tr(d, X1, top - 50, "SLOWER →", F(MONO, 16), MUTE + (int(200 * k),), 3, "r")
    lim = len(rows) if upto is None else upto
    for i, row in enumerate(rows):
        nm, a, b, lab = row[:4]
        t0 = (rows[i][4] if len(rows[i]) > 4 else 0.35 + i * (dur - 1.2) / max(1, n)) if upto is None else 0.3 + i * 0.12
        if i >= lim: continue
        kr = ease(seg(t, t0, t0 + 0.4)) * fo
        if kr <= 0: continue
        y = top + i * rh + rh / 2
        draw_tr(d, 150, y + 9, nm.upper(), F(MONO, 24, "Medium"), PAPER + (int(255 * kr),), 2)
        xa = _tx(a, lo, hi, X0, X1)
        d.ellipse([xa - 9, y - 9, xa + 9, y + 9], fill=CYAN + (int(255 * kr),))
        d.text((xa - 18, y - 16), f"{a:.2f}", font=F(SERIF, 34), fill=CYAN + (int(255 * kr),), anchor="rs")
        if b is not None:
            g = ease(seg(t, t0 + 0.35, t0 + 1.1)); xb = xa + (_tx(b, lo, hi, X0, X1) - xa) * g
            d.line([(xa, y), (xb, y)], fill=PAPER + (int(150 * kr),), width=3)
            d.ellipse([xb - 9, y - 9, xb + 9, y + 9], fill=CORAL + (int(255 * kr),))
            if g > 0.95:
                d.text((xb + 18, y - 16), f"{b:.2f}", font=F(SERIF, 34), fill=CORAL + (int(255 * kr),), anchor="ls")
                draw_tr(d, xb + 20, y + 22, lab.upper(), F(MONO, 14), MUTE + (int(230 * kr),), 2)
        else:
            draw_tr(d, xa + 26, y + 8, lab.upper(), F(MONO, 18), MUTE + (int(230 * kr),), 2)
    out.alpha_composite(glow(im, 8, 0.15, CYAN)); return out


def nextrace(t, dur, nm, final_t, next_t, next_meet, delta, place=""):
    return drift(t, dur, nm, [(nm, float(final_t), float(next_t), next_meet + " · " + delta)])


def stamp(t, dur, text, sub=""):
    """Recording readout top-left: blinking coral dot + 'REC' style mono line + date. No pill."""
    k = life(t, dur, 0.35, 0.4); im = layer(); d = ImageDraw.Draw(im)
    if int(t * 2) % 2 == 0: d.ellipse([110, 92, 132, 114], fill=CORAL + (int(255 * k),))
    draw_tr(d, 150, 112, text.upper(), F(MONO, 30, "Bold"), PAPER + (int(255 * k),), 6)
    if sub: draw_tr(d, 150, 150, sub.upper(), F(MONO, 20, "Medium"), CYAN + (int(240 * k),), 4)
    ticks(d, 84, 66, 620, 172, k, 16); return glow(im, 8, 0.2, CYAN)


def dialk(t, dur, val, label=""): return dial(t, dur, float(val), label)


K.KINDS.update(subs=subs, iname=iname, name=name, title=title, number=number, chapter=chapter, date=date, wipe=wipe,
               quote=quote, board=board, nextrace=nextrace, drift=drift, stamp=stamp, dial=dialk)


if __name__ == "__main__":
    import sys, os
    o = sys.argv[1]; os.makedirs(o, exist_ok=True); bg = Image.open(sys.argv[2]).convert("RGBA").resize((W, H))
    ws = [(w, 0.28 * i, 0.28 * i + 0.24) for i, w in enumerate("He's coming with the hype of running 19.67, which he has to prove is a real time.".split())]
    FIN = [("Gout Gout", 19.67, 20.60, "Oslo DL"), ("Aidan Murphy", 19.88, 20.28, "Oceania heat"), ("Calab Law", 20.21, 20.85, "Tokyo"),
           ("Christopher Ius", 20.26, 21.02, "Oceania heat"), ("Archer McHugh", 20.37, None, "no 200m rest of 2026"), ("Rory Easton", 20.37, 21.42, "Oceania heat · DNF final"),
           ("Sebastian Milverton", 20.83, None, "no 200m rest of 2026")]
    tests = [("subs", 6, ("subs", ws), 3.0), ("iname", 6, ("iname", "Donovan Bailey", "1996 Olympic 100m champion", "CBC Sports"), 2.0),
             ("title", 4, ("title", "Australian Championships · April 12, 2026", "19.67"), 2.2),
             ("number", 4, ("number", "+2.3", "Women's 200m final, minutes before", "Sydney · April 12, 2026"), 2.4),
             ("chapter", 3, ("chapter", "05", "Sydney"), 2.0), ("wipe", 4, ("wipe", ["Outside Sydney,", "never under 20 legal."], "The pattern"), 2.6),
             ("board", 6, ("board", "Every sub-10 / sub-20 before 2026", [("100m · Dec 2024", "10.04", "+3.4 wind", 1), ("200m · Mar 2025", "19.98", "+3.4 wind", 1), ("100m · Apr 2025", "9.99", "+2.6 wind", 1), ("Ostrava 2025", "20.02", "0.0 wind", 0)], "Legal limit +2.0"), 4.5),
             ("drift", 9, ("drift", "Sydney final → very next 200m", FIN), 8.5),
             ("stamp", 4, ("stamp", "Rec · TikTok", "Posted June 29, 2026"), 2.0), ("quote", 5, ("quote", "I can guarantee you, if Tate Taylor runs 19.85 or faster, Gout Gout will pull out.", "Erin Brown, June 29"), 4.5)]
    for nm, dur, spec, at in tests:
        fr = bg.copy(); fr.alpha_composite(K.KINDS[spec[0]](at, dur, *spec[1:])); fr.convert("RGB").save(f"{o}/{nm}.jpg", quality=86)
    print("ok")


def source(t, dur, text):
    """Tiny source credit bottom-right as an instrument line: 'SRC / ...' in mono, cyan slash."""
    im = layer(); a = life(t, dur, 0.4, 0.3)
    if a <= 0: return im
    d = ImageDraw.Draw(im); f = F(MONO, 16, "Medium"); txt = text.upper(); w = tracked_w(txt, f, 2)
    draw_tr(d, W - 64 - w - tracked_w("SRC / ", f, 2), H - 50, "SRC / ", f, CYAN + (int(200 * a),), 2)
    draw_tr(d, W - 64 - w, H - 50, txt, f, PAPER + (int(185 * a),), 2)
    return glow(im, 5, 0.0)


K.source = source


def clock(t, dur, t0, label="", rate=1.0, stop=None):
    """Race clock as an instrument readout top-right: mono digits, cyan tick bar sweeping like a stopwatch hand."""
    k = life(t, dur, 0.4, 0.4); v = t0 + t * rate
    if stop is not None: v = min(v, stop)
    im = layer(); d = ImageDraw.Draw(im); x = W - 110
    d.text((x, 130), f"{v:05.2f}", font=F(MONO, 64, "Bold"), fill=PAPER + (255,), anchor="rs")
    frac = (v % 1.0); d.line([(x - 300, 150), (x - 300 + 300 * frac, 150)], fill=CYAN + (230,), width=3)
    if label: draw_tr(d, x, 182, label.upper(), F(MONO, 17, "Medium"), MUTE + (235,), 3, "r")
    ticks(d, x - 330, 52, x + 20, 200, 1.0, 14)
    return fade(glow(im, 8, 0.2, CYAN), k)


def gap(t, dur, a_name, a_secs, b_name, b_secs, gap_text, kicker=""):
    """Two runs on one time axis (the drift-chart language): dots land, the gap between them is measured."""
    k = life(t, dur, 0.5, 0.45); out = scrim(0.66 * k); fo = 1 - inout(seg(t, dur - 0.45, dur))
    out.alpha_composite(streamlines(t, k * 0.6, seed=3, n=30, alpha=0.2))
    im = layer(); d = ImageDraw.Draw(im); lo, hi = min(a_secs, b_secs) - 0.35, max(a_secs, b_secs) + 0.35; X0, X1 = 360, W - 360
    if kicker: draw_tr(d, X0, 330, "// " + kicker.upper(), F(MONO, 22, "Medium"), CYAN + (int(240 * k),), 3)
    for i, (nm, v, col) in enumerate(((a_name, a_secs, CYAN), (b_name, b_secs, PAPER))):
        y = 470 + i * 150; kr = ease(seg(t, 0.2 + i * 0.4, 0.7 + i * 0.4)) * fo
        d.line([(X0, y), (X1, y)], fill=PAPER + (int(40 * kr),), width=1)
        x = _tx(v, lo, hi, X0, X1) if kr > 0 else X0; xx = X0 + (x - X0) * ease(seg(t, 0.2 + i * 0.4, 1.0 + i * 0.4))
        d.line([(X0, y), (xx, y)], fill=col + (int(200 * kr),), width=3); d.ellipse([xx - 10, y - 10, xx + 10, y + 10], fill=col + (int(255 * kr),))
        draw_tr(d, X0, y - 26, nm.upper(), F(MONO, 22, "Medium"), col + (int(255 * kr),), 2)
        d.text((xx + 22, y + 16), f"{v:.2f}", font=F(SERIF, 64), fill=col + (int(255 * kr),), anchor="ls")
    kg = ease(seg(t, 1.3, 1.8)) * fo
    if kg > 0:
        xa, xb = _tx(a_secs, lo, hi, X0, X1), _tx(b_secs, lo, hi, X0, X1)
        d.line([(xa, 690), (xa, 710), (xb, 710), (xb, 690)], fill=CORAL + (int(255 * kg),), width=2)
        d.text(((xa + xb) / 2, 790), gap_text, font=F(SERIF_I, 72), fill=CORAL + (int(255 * kg),), anchor="ms")
    out.alpha_composite(glow(im, 10, 0.15, CYAN)); return out


K.KINDS.update(clock=clock, gap=gap)

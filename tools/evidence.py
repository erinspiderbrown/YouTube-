"""Evidence look (Gout Gout v3, 28 Nov 2026): the user said the on-screen words "could be better and more visually
appealing". The modern.py set (thin Inter, small, low contrast) read as plain. This set keeps it modern and clean but
gives it weight: big condensed display type (Anton), frosted dark glass panels with a hairline border, one red accent,
a yellow highlight for numbers, mask reveals with a light sweep, rows that slide in with a stagger. Nothing slams.

Import after modern/premium/cinema: it overrides these kinds in modern.KINDS:
  subs, iname, title, number, name, chapter, board, wipe, date, quote
and adds:
  nextrace (name, final_time, next_time, next_meet, delta)  runner card: Sydney final -> very next race
  stamp    (text, sub)                                        "RECEIPT"/"CALLED IT" tag, top-left, with a date line
"""
import math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import modern as K
from modern import W, H, F, ease, inout, seg, life, layer, soft_shadow, draw_tracked, tracked, MED, SEMI, REG, DISP_SEMI, DISP_BOLD, BOLD

ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
WHITE = (248, 248, 246); SOFT = (196, 200, 208); DIM = (128, 132, 140)
RED = (238, 52, 52); YEL = (255, 204, 51); GLASS = (14, 16, 22)
NUMRE = re.compile(r"^[+\-]?\d[\d.:,]*\w?[.,!?]*$")


# ------------------------------------------------------------------ helpers
def glass(w, h, r=18, a=178, border=46):
    """Frosted dark panel: vertical gradient fill, hairline border, soft top sheen."""
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    g = np.linspace(1.0, 0.82, int(h))[:, None] * np.ones((1, int(w)))
    fill = np.zeros((int(h), int(w), 4), np.uint8)
    for i, c in enumerate(GLASS): fill[..., i] = c
    fill[..., 3] = (a * g).astype(np.uint8)
    im = Image.fromarray(fill, "RGBA"); im.putalpha(Image.fromarray((np.asarray(m) / 255 * fill[..., 3]).astype(np.uint8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], r, outline=(255, 255, 255, border), width=1)
    d.line([(r, 1), (w - r, 1)], fill=(255, 255, 255, border + 30), width=1)
    return im


def put(dst, im, x, y, k=1.0, dx=0, dy=0):
    if k <= 0: return
    if k < 1:
        im = im.copy(); a = im.split()[3].point(lambda v: int(v * k)); im.putalpha(a)
    dst.alpha_composite(im, (int(x + dx), int(y + dy)))


def shadow(im, r=22, o=0.6):
    pad = r * 2; big = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    a = Image.new("L", big.size, 0); a.paste(im.split()[3], (pad, pad)); a = a.filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * o))
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); sh.putalpha(a); big.alpha_composite(sh, (0, 8)); big.alpha_composite(im, (pad, pad))
    return big, pad


def mask_reveal(im, k, direction="lr", soft=60):
    """Reveal an RGBA image left->right through a soft-edged mask; k in 0..1."""
    if k >= 1: return im
    if k <= 0: return Image.new("RGBA", im.size, (0, 0, 0, 0))
    w, h = im.size; x = np.arange(w, dtype=np.float32)
    edge = (w + soft) * k
    m = np.clip((edge - x) / soft, 0, 1)[None, :] * np.ones((h, 1), np.float32)
    out = im.copy(); a = np.asarray(im.split()[3], np.float32) * m; out.putalpha(Image.fromarray(a.astype(np.uint8))); return out


def sweep(im, k, width=160, strength=120):
    """A light streak passes across the opaque parts of im once (k 0..1)."""
    if k <= 0 or k >= 1: return im
    w, h = im.size; x = np.arange(w, dtype=np.float32); cx = -width + (w + 2 * width) * k
    g = np.exp(-((x - cx) / width) ** 2)[None, :] * np.ones((h, 1), np.float32)
    arr = np.asarray(im, np.float32).copy(); a = arr[..., 3:4] / 255
    arr[..., :3] = np.clip(arr[..., :3] + strength * g[..., None] * a, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def text_img(txt, font, fill, track=0):
    w = int(tracked(txt, font, track) + 8) if track else int(font.getlength(txt) + 8)
    asc, desc = font.getmetrics(); im = Image.new("RGBA", (w, asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if track: draw_tracked(d, (2, asc + 2), txt, font, fill, track)
    else: d.text((2, asc + 2), txt, font=font, fill=fill, anchor="ls")
    return im


def pill(txt, fg=WHITE, bg=RED, size=24, track=5):
    f = F(BOLD, size); t = text_img(txt.upper(), f, fg + (255,), track)
    im = Image.new("RGBA", (t.width + 30, int(size * 1.75)), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 6, fill=bg + (255,))
    im.alpha_composite(t, (15, int((im.height - t.height) / 2) + 2)); return im


def scrim(a, where="full"):
    im = layer()
    if a <= 0: return im
    if where == "full": im.paste((0, 0, 0, int(255 * a)), [0, 0, W, H]); return im
    g = np.zeros((H, W, 4), np.uint8); y = np.arange(H, dtype=np.float32)
    ramp = np.clip((y - H * 0.45) / (H * 0.55), 0, 1) ** 1.4 if where == "bottom" else np.clip((H * 0.5 - y) / (H * 0.5), 0, 1)
    g[..., 3] = (255 * a * ramp)[:, None]; return Image.fromarray(g, "RGBA")


def isnum(w): return bool(NUMRE.match(w.strip()))


# ------------------------------------------------------------------ kinds
def subs(t, dur, words, size=50):
    """Karaoke subtitles on a soft dark band: spoken word white, upcoming dim, numbers in yellow. Max 2 lines."""
    f = F(SEMI, size); maxw = W - 520
    lines, cur = [], []
    for w in words:
        if cur and f.getlength(" ".join(x[0] for x in cur + [w])) > maxw: lines.append(cur); cur = []
        cur.append(w)
    if cur: lines.append(cur)
    pages = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    curp = None
    for pg in pages:
        if t >= pg[0][0][1] - 0.15: curp = pg
    if not curp: return layer()
    a = curp[0][0][1]; b = curp[-1][-1][2]
    nxt = [p for p in pages if p[0][0][1] > a]; end = (nxt[0][0][0][1] - 0.05) if nxt else b + 0.7
    k = ease(seg(t, a - 0.15, a + 0.12)) * (1 - ease(seg(t, end - 0.15, end + 0.1)))
    if k <= 0: return layer()
    lh = size * 1.36; y0 = H - 112 - (len(curp) - 1) * lh
    out = layer()
    bw = max(f.getlength(" ".join(x[0] for x in ln)) for ln in curp) + 70; bh = len(curp) * lh + 34
    band = glass(bw, bh, 14, 150, 0); put(out, band, W / 2 - bw / 2, y0 - size - 14, k)
    im = layer(); d = ImageDraw.Draw(im)
    for li, ln in enumerate(curp):
        x = W / 2 - f.getlength(" ".join(w[0] for w in ln)) / 2
        for w, w0, w1 in ln:
            on = ease(seg(t, w0 - 0.04, w0 + 0.1))
            hi = YEL if isnum(w) else WHITE
            c = tuple(int(DIM[i] + (hi[i] - DIM[i]) * on) for i in range(3))
            d.text((x, y0 + li * lh), w, font=f, fill=c + (int(255 * k),), anchor="ls"); x += f.getlength(w + " ")
    out.alpha_composite(im); return out


def iname(t, dur, nm, role, where=""):
    """Interview ID: glass card slides in from the left with a red bar; NAME in condensed caps; leaves by ~4.6 s."""
    L = min(dur, 4.8); k = ease(seg(t, 0.05, 0.6)) * (1 - inout(seg(t, L - 0.45, L)))
    if k <= 0: return layer()
    fN = F(ANTON, 62); fR = F(SEMI, 26); fW = F(MED, 19)
    tn = text_img(nm.upper(), fN, WHITE + (255,), 2); tr = text_img(role, fR, SOFT + (255,)) if role else None
    tw = text_img(where.upper(), fW, (170, 174, 182, 255), 4) if where else None
    w = max(tn.width, tr.width if tr else 0, tw.width if tw else 0) + 64; h = 30 + tn.height + (tr.height + 4 if tr else 0) + (tw.height + 6 if tw else 0) + 12
    card = glass(w, h); d = ImageDraw.Draw(card)
    grow = ease(seg(t, 0.2, 0.75)); d.rectangle([0, 0, 7, int(h * grow)], fill=RED + (255,))
    y = 16; card.alpha_composite(mask_reveal(tn, ease(seg(t, 0.15, 0.8))), (30, y)); y += tn.height - 6
    if tr: card.alpha_composite(mask_reveal(tr, ease(seg(t, 0.3, 0.95))), (32, y)); y += tr.height + 4
    if tw: card.alpha_composite(mask_reveal(tw, ease(seg(t, 0.45, 1.1))), (32, y))
    card = sweep(card, seg(t, 0.6, 1.5), 140, 45)
    sh, pad = shadow(card); out = layer(); put(out, sh, 110 - pad, H - 330 - pad, k, dx=-60 * (1 - k)); return out


def name(t, dur, nm, sub, side="l"): return iname(t, dur, nm, sub, "")


def title(t, dur, kicker, headline, pos="bl"):
    """Red kicker pill + huge condensed headline revealed by a mask with a light sweep, lower-left."""
    k = life(t, dur, 0.5, 0.45); out = scrim(0.7 * k, "bottom")
    p = pill(kicker, size=22); put(out, p, 130, H - 300, ease(seg(t, 0, 0.4)) * (1 - inout(seg(t, dur - 0.45, dur))), dx=-30 * (1 - ease(seg(t, 0, 0.4))))
    f = F(ANTON, 150)
    while f.getlength(headline.upper()) > W - 300: f = F(ANTON, f.size - 6)
    hd = text_img(headline.upper(), f, WHITE + (255,), 2)
    hd = sweep(mask_reveal(hd, ease(seg(t, 0.15, 0.85))), seg(t, 0.7, 1.6))
    sh, pad = shadow(hd, 26, 0.7); put(out, sh, 126 - pad, H - 262 - pad, 1 - inout(seg(t, dur - 0.45, dur))); return out


def _roll(final, k):
    digs = [c for c in final if c.isdigit()]
    if not digs or k >= 1: return final
    val = int("".join(digs)); cur = str(int(val * k)).zfill(len(digs)); it = iter(cur)
    return "".join(next(it) if c.isdigit() else c for c in final)


def number(t, dur, value, label, sub=""):
    """Giant condensed number rolls up and lands with a soft glow; red label pill; optional sub line."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.6 * k)
    cnt = ease(seg(t, 0.05, 0.95)); f = F(ANTON, 330)
    while f.getlength(value) > W - 260: f = F(ANTON, f.size - 10)
    num = text_img(_roll(value, cnt), f, WHITE + (255,), 4)
    glow = num.filter(ImageFilter.GaussianBlur(28)); ga = glow.split()[3].point(lambda v: int(v * 0.5 * ease(seg(t, 0.9, 1.3))))
    glow = Image.new("RGBA", num.size, YEL + (0,)); glow.putalpha(ga)
    full = text_img(value, f, WHITE + (255,), 4); x = W / 2 - full.width / 2; y = H / 2 - full.height / 2 - 40
    put(out, glow, x, y, k); sh, pad = shadow(num, 30, 0.7); put(out, sh, x - pad, y - pad, k, dy=20 * (1 - ease(seg(t, 0, 0.6))))
    pl = pill(label, size=26); kl = life(max(0, t - 0.4), dur - 0.4, 0.45, 0.45)
    put(out, pl, W / 2 - pl.width / 2, y + full.height + 10, kl, dy=12 * (1 - kl))
    if sub:
        ts = text_img(sub.upper(), F(MED, 24), SOFT + (255,), 6); put(out, ts, W / 2 - ts.width / 2, y + full.height + 70, kl)
    return out


def chapter(t, dur, num, ttl):
    """Letterbox bars slide in, 'PART 05' in red, giant title wipes on with a light streak; thin rules either side."""
    k = life(t, dur, 0.55, 0.5); out = scrim(0.72 * k)
    bars = layer(); d = ImageDraw.Draw(bars); bh = int(110 * ease(seg(t, 0, 0.5)) * (1 - inout(seg(t, dur - 0.5, dur))))
    d.rectangle([0, 0, W, bh], fill=(0, 0, 0, 255)); d.rectangle([0, H - bh, W, H], fill=(0, 0, 0, 255)); out.alpha_composite(bars)
    pt = text_img(f"PART {num}", F(BOLD, 28), RED + (255,), 12); put(out, pt, W / 2 - pt.width / 2, H / 2 - 150, k)
    f = F(ANTON, 190)
    while f.getlength(ttl.upper()) > W - 260: f = F(ANTON, f.size - 8)
    tt = text_img(ttl.upper(), f, WHITE + (255,), 6)
    tt = sweep(mask_reveal(tt, ease(seg(t, 0.2, 1.0))), seg(t, 0.9, 1.9), 200, 140)
    x = W / 2 - tt.width / 2; y = H / 2 - tt.height / 2 + 20
    sh, pad = shadow(tt, 30, 0.6); put(out, sh, x - pad, y - pad, 1 - inout(seg(t, dur - 0.5, dur)))
    g = ease(seg(t, 0.3, 1.2)) * (1 - inout(seg(t, dur - 0.5, dur))); ln = layer(); dl = ImageDraw.Draw(ln); yy = y + tt.height + 18; L = 260 * g
    dl.line([(W / 2 - L, yy), (W / 2 + L, yy)], fill=(255, 255, 255, 120), width=2); out.alpha_composite(ln); return out


def date(t, dur, text, sub=""):
    k = life(t, dur, 0.5, 0.5); out = scrim(0.5 * k)
    f = F(ANTON, 140); tt = text_img(text.upper(), f, WHITE + (255,), 4)
    tt = sweep(mask_reveal(tt, ease(seg(t, 0.1, 0.8))), seg(t, 0.7, 1.6))
    x = W / 2 - tt.width / 2; y = H / 2 - tt.height / 2 - 20; sh, pad = shadow(tt); put(out, sh, x - pad, y - pad, 1 - inout(seg(t, dur - 0.5, dur)))
    if sub:
        p = pill(sub, size=24); put(out, p, W / 2 - p.width / 2, y + tt.height + 12, life(max(0, t - 0.35), dur - 0.35, 0.4, 0.45))
    return out


def wipe(t, dur, lines, kicker="", pos="c", size=120):
    """Statement: each line wipes on (last line yellow), optional red kicker pill above."""
    k = life(t, dur, 0.4, 0.45); out = scrim(0.62 * k)
    f = F(ANTON, size); imgs = []
    for i, ln in enumerate(lines):
        while f.getlength(ln.upper()) > W - 240: f = F(ANTON, f.size - 6)
    for i, ln in enumerate(lines):
        col = YEL if (i == len(lines) - 1 and len(lines) > 1) else WHITE
        imgs.append(text_img(ln.upper(), f, col + (255,), 3))
    tot = sum(i.height for i in imgs) - 18 * (len(imgs) - 1); y = H / 2 - tot / 2 + 10
    if kicker:
        p = pill(kicker, size=24); put(out, p, W / 2 - p.width / 2, y - 70, k)
    fo = 1 - inout(seg(t, dur - 0.45, dur))
    for i, im in enumerate(imgs):
        r = sweep(mask_reveal(im, ease(seg(t, 0.12 + 0.28 * i, 0.75 + 0.28 * i))), seg(t, 0.8 + 0.28 * i, 1.7 + 0.28 * i))
        sh, pad = shadow(r, 26, 0.65); put(out, sh, W / 2 - im.width / 2 - pad, y - pad, fo); y += im.height - 18
    return out


def quote(t, dur, text, who=""):
    out = scrim(0.66 * life(t, dur, 0.5, 0.45)); fo = 1 - inout(seg(t, dur - 0.45, dur))
    q = text_img("“", F(ANTON, 220), RED + (255,)); put(out, q, 230, 170, ease(seg(t, 0, 0.5)) * fo)
    f = F(DISP_SEMI, 66); words = text.split(); lines, cur = [], []
    for wd in words:
        if cur and f.getlength(" ".join(cur + [wd])) > W - 600: lines.append(cur); cur = []
        cur.append(wd)
    if cur: lines.append(cur)
    n = len(words); per = min(0.2, max(0.07, dur * 0.4 / max(1, n))); im = layer(); d = ImageDraw.Draw(im); i = 0; lh = 88
    y0 = H / 2 - (len(lines) - 1) * lh / 2 + 20
    for li, ln in enumerate(lines):
        x = 330
        for wd in ln:
            a = ease(seg(t, 0.2 + i * per, 0.2 + i * per + 0.35)) * fo
            d.text((x, y0 + li * lh), wd, font=f, fill=(YEL if isnum(wd) else WHITE) + (int(255 * a),), anchor="ls"); x += f.getlength(wd + " "); i += 1
    if who:
        a = ease(seg(t, 0.2 + n * per, 0.8 + n * per)) * fo
        draw_tracked(d, (332, y0 + len(lines) * lh + 24), "— " + who.upper(), F(BOLD, 26), (255, 255, 255, int(220 * a)), 7)
    out.alpha_composite(soft_shadow(im, 18)); return out


def board(t, dur, kicker, rows, note=""):
    """Glass table: red kicker pill, rows slide in from the right with a stagger; hi rows get a red bar + white,
    a third column starting with '+' (slower) is drawn red, '-' green-ish white."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.7 * k); fo = 1 - inout(seg(t, dur - 0.45, dur))
    n = len(rows); rh = min(78, int(620 / max(1, n))); sz = int(rh * 0.5)
    fa = F(SEMI, sz); fb = F(ANTON, int(sz * 1.18)); fc = F(BOLD, int(sz * 0.86))
    wa = max(fa.getlength(r[0]) for r in rows); wb = max(fb.getlength(r[1]) for r in rows); wc = max(fc.getlength(r[2]) for r in rows)
    pw = max(1100, wa + wb + wc + 220); ph = n * rh + 150
    x0 = W / 2 - pw / 2; y0 = H / 2 - ph / 2 + 20
    pan = glass(pw, ph, 20, 190); put(out, pan, x0, y0, k, dy=20 * (1 - k))
    p = pill(kicker, size=24); put(out, p, x0 + 40, y0 - p.height / 2, k)
    for i, (a, b, c, hi) in enumerate(rows):
        kr = ease(seg(t, 0.3 + i * 0.14, 0.75 + i * 0.14)) * fo
        if kr <= 0: continue
        r = Image.new("RGBA", (int(pw), rh), (0, 0, 0, 0)); d = ImageDraw.Draw(r); yb = rh * 0.68
        if hi: d.rectangle([0, 6, int(pw) - 1, rh - 6], fill=(255, 255, 255, 18)); d.rectangle([0, 6, 6, rh - 6], fill=RED + (255,))
        col = WHITE if hi else SOFT
        d.text((44, yb), a, font=fa, fill=col + (255,), anchor="ls")
        d.text((44 + wa + 70, yb + 2), b, font=fb, fill=(YEL if hi else WHITE) + (255,), anchor="ls")
        cc = RED if c.strip().startswith("+") else (col if not c.strip().startswith("-") else (120, 220, 150))
        d.text((pw - 44, yb), c, font=fc, fill=cc + (255,), anchor="rs")
        d.line([(44, rh - 1), (pw - 44, rh - 1)], fill=(255, 255, 255, 28), width=1)
        put(out, r, x0, y0 + 60 + i * rh, kr, dx=80 * (1 - kr))
    if note:
        tn = text_img(note.upper(), F(MED, 22), SOFT + (255,), 6); put(out, tn, W / 2 - tn.width / 2, y0 + ph - 54, ease(seg(t, 0.4 + n * 0.14, 1.0 + n * 0.14)) * fo)
    return out


def nextrace(t, dur, nm, final_t, next_t, next_meet, delta, place=""):
    """One finalist: SYDNEY FINAL time (dim) -> arrow draws -> NEXT RACE time (white) -> delta in red, on a glass card."""
    k = life(t, dur, 0.45, 0.45); out = scrim(0.55 * k)
    pw, ph = 1260, 470; x0 = W / 2 - pw / 2; y0 = H / 2 - ph / 2
    card = glass(pw, ph, 22, 196); d = ImageDraw.Draw(card)
    d.rectangle([0, 0, 8, ph], fill=RED + (255,))
    tn = text_img(nm.upper(), F(ANTON, 76), WHITE + (255,), 2); card.alpha_composite(mask_reveal(tn, ease(seg(t, 0.1, 0.7))), (50, 26))
    if place: tp = text_img(place.upper(), F(BOLD, 22), SOFT + (255,), 6); card.alpha_composite(tp, (54, 26 + tn.height - 4))
    lab = lambda s: text_img(s.upper(), F(BOLD, 22), (170, 174, 182, 255), 6)
    card.alpha_composite(lab("Sydney final · Apr 12"), (54, 190))
    card.alpha_composite(lab(next_meet), (700, 190))
    fbig = F(ANTON, 150)
    ta = text_img(final_t, fbig, (205, 208, 214, 255), 3); card.alpha_composite(mask_reveal(ta, ease(seg(t, 0.25, 0.8))), (50, 222))
    tb = text_img(_roll(next_t, ease(seg(t, 1.0, 1.7))), fbig, WHITE + (255,), 3)
    if t >= 0.95: card.alpha_composite(tb, (696, 222))
    g = ease(seg(t, 0.75, 1.1)); ax0, ax1, ay = 50 + ta.width + 20, 50 + ta.width + 20 + (640 - ta.width - 60) * g, 222 + ta.height / 2 + 6
    if g > 0:
        d.line([(ax0, ay), (ax1, ay)], fill=(255, 255, 255, 150), width=3)
        if g > 0.95: d.polygon([(ax1, ay - 11), (ax1 + 18, ay), (ax1, ay + 11)], fill=(255, 255, 255, 180))
    if t >= 1.7:
        kd = ease(seg(t, 1.7, 2.1)); dp = pill(delta, bg=RED if delta.startswith("+") else (40, 140, 90), size=30)
        tmp = Image.new("RGBA", dp.size, (0, 0, 0, 0)); tmp.alpha_composite(dp); a = tmp.split()[3].point(lambda v: int(v * kd)); tmp.putalpha(a)
        card.alpha_composite(tmp, (pw - dp.width - 50, 36))
    sh, pad = shadow(card, 30, 0.6); put(out, sh, x0 - pad, y0 - pad, k, dy=24 * (1 - k)); return out


def stamp(t, dur, text, sub=""):
    """Red tag top-left ("RECEIPT") with a date line; enters with a small scale settle, no slam."""
    k = life(t, dur, 0.35, 0.4); out = layer()
    p = pill(text, size=34, track=8); s = 1.15 - 0.15 * ease(seg(t, 0, 0.35))
    p = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS); sh, pad = shadow(p, 16, 0.6); put(out, sh, 110 - pad, 96 - pad, k)
    if sub:
        ts = text_img(sub.upper(), F(BOLD, 26), WHITE + (255,), 6); sh, pad = shadow(ts, 10, 0.8); put(out, sh, 114 - pad, 96 + p.height + 14 - pad, life(max(0, t - 0.25), dur - 0.25, 0.35, 0.4))
    return out


K.KINDS.update(subs=subs, iname=iname, name=name, title=title, number=number, chapter=chapter, date=date, wipe=wipe,
               quote=quote, board=board, nextrace=nextrace, stamp=stamp)


if __name__ == "__main__":   # stills: python3 tools/evidence.py OUTDIR BG.jpg
    import sys, os
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    bg = Image.open(sys.argv[2]).convert("RGBA").resize((W, H))
    ws = [(w, 0.28 * i, 0.28 * i + 0.24) for i, w in enumerate("He's coming with the hype of running 19.67, which he has to prove is a real time.".split())]
    tests = [("subs", 6, ("subs", ws), 3.0), ("iname", 6, ("iname", "Donovan Bailey", "1996 Olympic 100m champion", "CBC Sports"), 2.0),
             ("title", 4, ("title", "Australian Championships · April 12, 2026", "19.67"), 2.2),
             ("number", 4, ("number", "+2.3", "Women's 200m final, minutes before", "Sydney · April 12, 2026"), 2.4),
             ("chapter", 3, ("chapter", "05", "Sydney"), 2.0), ("wipe", 4, ("wipe", ["Outside Sydney", "never under 20 legal"], "The pattern"), 2.6),
             ("board", 6, ("board", "Men's 200m final · next race", [("Gout Gout", "19.67", "+0.93", 1), ("Aidan Murphy", "19.88", "+0.17", 0), ("Calab Law", "20.21", "+0.39", 0)], "every finalist slower"), 4.0),
             ("nextrace", 4, ("nextrace", "Calab Law", "20.21", "20.60", "Commonwealth Games · Jul", "+0.39", "3rd in Sydney"), 3.0),
             ("stamp", 4, ("stamp", "Receipt", "Posted June 29, 2026"), 2.0), ("quote", 5, ("quote", "I can guarantee you, if Tate Taylor runs 19.85 or faster, Gout Gout will pull out.", "Erin Brown, June 29"), 4.5)]
    for nm, dur, spec, at in tests:
        fr = bg.copy(); fr.alpha_composite(K.KINDS[spec[0]](at, dur, *spec[1:])); fr.convert("RGB").save(f"{o}/{nm}.jpg", quality=86)
    print("ok")

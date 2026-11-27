"""Premium doc layer (Kejelcha, 27 Nov 2026): the step-up for interviews, transitions and on-screen wording.

Overlays (register into modern.KINDS, same frame(t, dur, *args) -> RGBA interface):
  subs      word-synced interview subtitles: clean two-line captions, the spoken word lights up, the rest sits dim
  iname     interview ID: name + role + small source/location line, hairline draws, settles in, leaves early
  clock     a clean race clock (top-right) that runs from t0 at real speed, optional label ("LONDON · KM 41")
  gap       finish comparison: two lanes, both clocks roll to their times, then the gap bracket ("11 SECONDS")
  wipe      headline revealed line by line through a rising mask (Apple-style), optional kicker; no slam
  timeline  career near-misses on a horizontal rail; each dot lands with year, event, place and margin
Transitions (apply to a finished video in one pass, see apply_transitions):
  whip  directional motion-blur pan across the cut       blur  defocus + slight zoom dissolve
  leak  clean warm light bloom across the cut            push  slide with motion blur
  dip   quick dip to black (for a beat / chapter)        luma  bright areas of B burn in first
The incoming side of a transition is real; the outgoing side holds its last frame after the cut (hidden by blur).
"""
import math, subprocess, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import modern as K
from modern import W, H, FPS, F, ease, inout, seg, life, layer, soft_shadow, reveal, scrim, draw_tracked, tracked
from modern import WHITE, SOFT, ACCENT, MED, SEMI, REG, LIGHT, DISP_SEMI, DISP_MED, DISP_BOLD, THIN, XL

DIM = (150, 152, 158)


def _lines(words, font, maxw):
    lines, cur = [], []
    for w in words:
        if cur and font.getlength(" ".join(x[0] for x in cur + [w])) > maxw: lines.append(cur); cur = []
        cur.append(w)
    if cur: lines.append(cur)
    return lines


def subs(t, dur, words, size=46):
    """words = [(text, t0, t1)] relative to the overlay start. Pages of max 2 lines; spoken words go white."""
    f = F(SEMI, size); maxw = W - 560; lines = _lines(words, f, maxw)
    pages = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    cur = None
    for pg in pages:
        a, b = pg[0][0][1], pg[-1][-1][2]
        if t >= a - 0.15: cur = (pg, a, b)
    if not cur: return layer()
    pg, a, b = cur
    nxt = [p for p in pages if p[0][0][1] > a]
    end = (nxt[0][0][0][1] - 0.05) if nxt else b + 0.6
    k = ease(seg(t, a - 0.15, a + 0.1)) * (1 - ease(seg(t, end - 0.12, end + 0.12)))
    if k <= 0: return layer()
    im = layer(); d = ImageDraw.Draw(im); lh = size * 1.32; y0 = H - 120 - (len(pg) - 1) * lh
    for li, ln in enumerate(pg):
        x = W / 2 - f.getlength(" ".join(w[0] for w in ln)) / 2
        for w, w0, w1 in ln:
            on = ease(seg(t, w0 - 0.04, w0 + 0.12))
            c = tuple(int(DIM[i] + (WHITE[i] - DIM[i]) * on) for i in range(3))
            d.text((x, y0 + li * lh), w, font=f, fill=c + (int(255 * k),), anchor="ls"); x += f.getlength(w + " ")
    return soft_shadow(im, 10, 0.85)


def iname(t, dur, nm, role, where=""):
    """Interview ID, lower-left; leaves after ~4.5 s even if the bite runs on."""
    d_ = min(dur, 4.8); k = life(t, d_, 0.7, 0.5); g = ease(seg(t, 0.05, 0.9))
    if k <= 0: return layer()
    x, y = 132, H - 330
    im = layer(); d = ImageDraw.Draw(im)
    d.line([(x - 26, y - 52), (x - 26, y - 52 + 120 * g)], fill=ACCENT + (255,), width=3)
    d.text((x, y), nm, font=F(DISP_SEMI, 54), fill=WHITE + (255,), anchor="ls")
    draw_tracked(d, (x, y + 44), role.upper(), F(MED, 24), SOFT + (240,), 6)
    if where: draw_tracked(d, (x, y + 80), where.upper(), F(REG, 20), DIM + (230,), 6)
    out = scrim(0.35 * k, "bottom"); out.alpha_composite(reveal(soft_shadow(im, 14), k, 10)); return out


def _fmt(s, hund=False):
    h, r = divmod(s, 3600); m, r = divmod(r, 60)
    base = f"{int(h)}:{int(m):02d}:{int(r):02d}" if h >= 1 else f"{int(m)}:{int(r):02d}"
    return base + (f".{int((r % 1) * 100):02d}" if hund else "")


def clock(t, dur, t0, label="", rate=1.0, stop=None):
    """Race clock top-right; t0 = seconds shown at overlay start."""
    k = life(t, dur, 0.5, 0.4); v = t0 + t * rate
    if stop is not None: v = min(v, stop)
    im = layer(); d = ImageDraw.Draw(im); x = W - 120
    f = F(DISP_MED, 50); s = _fmt(v)
    d.text((x, 118), s, font=f, fill=WHITE + (255,), anchor="rs")
    if label: draw_tracked(d, (x, 152), label.upper(), F(MED, 20), SOFT + (230,), 6, "r")
    d.line([(x - 250, 72), (x, 72)], fill=WHITE + (90,), width=1); d.line([(x - 36, 72), (x, 72)], fill=ACCENT + (255,), width=3)
    return reveal(soft_shadow(im, 10, 0.7), k, 6)


def gap(t, dur, a_name, a_secs, b_name, b_secs, gap_text, kicker=""):
    """Two lanes; clocks roll up to their finish times; the second lane's bar runs past; gap bracket lands."""
    k = life(t, dur, 0.6, 0.5); out = scrim(0.62 * k)
    im = layer(); d = ImageDraw.Draw(im)
    x0, x1 = 300, W - 300; lane_y = [H / 2 - 90, H / 2 + 110]
    tmax = max(a_secs, b_secs); base = tmax - 40          # show the last 40 s of the race on the rail
    roll = ease(seg(t, 0.5, 3.6))
    def X(s): return x0 + (x1 - x0) * (s - base) / (tmax + 4 - base)
    if kicker: draw_tracked(d, (W / 2, 190), kicker.upper(), F(MED, 26), SOFT + (240,), 10, "c")
    for (nm, secs), y, col in zip(((a_name, a_secs), (b_name, b_secs)), lane_y, (WHITE, SOFT)):
        cur = base + (secs - base) * min(1, roll * tmax / secs if secs else 1)
        cur = min(secs, base + (tmax - base) * roll)
        d.line([(x0, y), (x1, y)], fill=WHITE + (60,), width=2)
        d.line([(x0, y), (X(cur), y)], fill=col + (255,), width=6)
        d.ellipse([X(cur) - 9, y - 9, X(cur) + 9, y + 9], fill=col + (255,))
        d.text((x0, y - 34), nm, font=F(DISP_SEMI, 40), fill=WHITE + (255,), anchor="ls")
        d.text((x1, y - 30), _fmt(cur, False), font=F(DISP_MED, 48), fill=col + (255,), anchor="rs")
    bk = ease(seg(t, 3.7, 4.4))
    if bk > 0:
        xa, xb = X(a_secs), X(b_secs); yb = lane_y[1] + 70
        a = int(255 * bk)
        d.line([(xa, yb - 14), (xa, yb), (xa + (xb - xa) * bk, yb)], fill=ACCENT + (a,), width=3)
        if bk > 0.95: d.line([(xb, yb), (xb, yb - 14)], fill=ACCENT + (a,), width=3)
        draw_tracked(d, ((xa + xb) / 2, yb + 62), gap_text.upper(), F(DISP_SEMI, 44), WHITE + (a,), 8, "c")
    out.alpha_composite(reveal(soft_shadow(im, 16), k, 10)); return out


def wipe(t, dur, lines, kicker="", pos="c", size=96):
    """Headline lines rise into view through a mask, one after another; kicker fades above."""
    k = life(t, dur, 0.4, 0.5); f = F(DISP_SEMI, size); lh = size * 1.12
    out = scrim(0.5 * k, "full" if pos == "c" else "bottom")
    n = len(lines); y_top = (H / 2 - n * lh / 2) if pos == "c" else (H - 180 - n * lh)
    fade = 1 - inout(seg(t, dur - 0.5, dur))
    for i, ln in enumerate(lines):
        p = ease(seg(t, 0.15 + i * 0.22, 0.95 + i * 0.22))
        if p <= 0: continue
        strip = Image.new("RGBA", (W, int(lh) + 30), (0, 0, 0, 0)); ds = ImageDraw.Draw(strip)
        xx = W / 2 if pos == "c" else 140
        ds.text((xx, lh * 0.82 + (1 - p) * lh), ln, font=f, fill=WHITE + (int(255 * fade),), anchor="ms" if pos == "c" else "ls")
        out.alpha_composite(soft_shadow_small(strip), (0, int(y_top + i * lh)))
    if kicker:
        a = ease(seg(t, 0.0, 0.7)) * fade; im = layer(); d = ImageDraw.Draw(im)
        if pos == "c": draw_tracked(d, (W / 2, y_top - 30), kicker.upper(), F(MED, 26), SOFT + (int(240 * a),), 10, "c")
        else: draw_tracked(d, (140, y_top - 30), kicker.upper(), F(MED, 26), SOFT + (int(240 * a),), 10)
        out.alpha_composite(im)
    return out


def soft_shadow_small(im):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a); o = Image.new("RGBA", im.size, (0, 0, 0, 0))
    o.alpha_composite(sh, (0, 5)); o.alpha_composite(im); return o


def timeline(t, dur, title_, events, upto=None):
    """events = [(year, event, result, note)]; result like '2nd'. Dots land one by one along a rail."""
    k = life(t, dur, 0.6, 0.5); out = scrim(0.7 * k)
    im = layer(); d = ImageDraw.Draw(im); n = len(events); upto = n if upto is None else upto
    x0, x1, y = 200, W - 200, H / 2 + 10
    rail = ease(seg(t, 0.2, 1.2)); d.line([(x0, y), (x0 + (x1 - x0) * rail, y)], fill=WHITE + (110,), width=2)
    draw_tracked(d, (W / 2, 210), title_.upper(), F(MED, 28), SOFT + (240,), 10, "c")
    for i, (yr, ev, res, note) in enumerate(events[:upto]):
        x = x0 + (x1 - x0) * (i + 0.5) / n; p = ease(seg(t, 0.9 + i * 0.45, 1.5 + i * 0.45))
        if p <= 0: continue
        a = int(255 * p); up = i % 2 == 0; col = ACCENT if res.lower().startswith(("2", "silver")) else WHITE
        r = 9 * p; d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))
        rows = [("res", res), ("yr", str(yr)), ("ev", ev)] + ([("note", note)] if note else [])
        hgt = {"res": 54, "yr": 32, "ev": 26, "note": 28}
        yy = y - 36 - sum(hgt[r] for r, _ in rows) if up else y + 34
        for r, v in rows:
            yy += hgt[r]
            if r == "res": d.text((x, yy), v, font=F(DISP_SEMI, 50), fill=col + (a,), anchor="ms")
            elif r == "yr": d.text((x, yy), v, font=F(MED, 25), fill=WHITE + (a,), anchor="ms")
            elif r == "ev": draw_tracked(d, (x, yy), v.upper(), F(REG, 18), SOFT + (a,), 4, "c")
            else: d.text((x, yy), v, font=F(REG, 22), fill=DIM + (a,), anchor="ms")
    out.alpha_composite(reveal(soft_shadow(im, 14), k, 8)); return out


K.KINDS.update(subs=subs, iname=iname, clock=clock, gap=gap, wipe=wipe, timeline=timeline)


# ------------------------------------------------------------------ transitions
def _mblur(f, dx, dy=0):
    n = int(max(abs(dx), abs(dy)))
    if n < 2: return f
    k = np.zeros((2 * n + 1, 2 * n + 1), np.float32)
    if abs(dx) >= abs(dy): k[n, :] = 1
    else: k[:, n] = 1
    return cv2.filter2D(f, -1, k / k.sum())


def _shift(f, dx, dy=0):
    M = np.float32([[1, 0, dx], [0, 1, dy]]); return cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def _zoom(f, z):
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z); return cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT)


def tframe(kind, A, B, p):
    """A, B float32 HxWx3 frames; p in [0,1], cut at 0.5."""
    s = p * p * (3 - 2 * p)
    if kind == "whip":
        e = 0.5 * (1 + math.tanh(9 * (p - 0.5))) ; sp = math.exp(-((p - 0.5) / 0.16) ** 2)
        off = W * e; a = _shift(A, -off); b = _shift(B, W - off)
        out = a.copy(); xb = int(round(W - off)); out[:, max(0, xb):] = b[:, max(0, xb):]
        return _mblur(out, 160 * sp)
    if kind == "push":
        off = W * s; sp = math.sin(math.pi * p)
        a = _mblur(_shift(A, -off), 50 * sp); b = _mblur(_shift(B, W - off), 50 * sp)
        out = a.copy(); xb = int(W - off); out[:, max(0, xb):] = b[:, max(0, xb):]; return out
    if kind == "blur":
        sp = math.sin(math.pi * p); r = 1 + 2 * int(18 * sp)
        a = cv2.GaussianBlur(_zoom(A, 1 + 0.05 * s), (r, r), 0); b = cv2.GaussianBlur(_zoom(B, 1.05 - 0.05 * s), (r, r), 0)
        return a * (1 - s) + b * s
    if kind == "leak":
        sp = math.sin(math.pi * p); base = A * (1 - s) + B * s
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        cx = W * (0.15 + 0.7 * p); g = np.exp(-(((xx - cx) / (W * 0.35)) ** 2 + ((yy - H * 0.4) / (H * 0.7)) ** 2))
        glow = g[..., None] * np.array([255, 196, 140], np.float32) * 0.9 * sp
        return np.clip(base + glow * (1 - base / 255.0) * 1.2, 0, 255)
    if kind == "dip":
        k = 1 - math.sin(math.pi * p); return (A if p < 0.5 else B) * k
    if kind == "luma":
        lum = cv2.cvtColor(B.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        m = np.clip((s * 1.6 - (1 - lum) * 0.6), 0, 1)[..., None]; m = cv2.GaussianBlur(m, (31, 31), 0)[..., None] if m.ndim == 3 else m
        return A * (1 - m) + B * m
    raise ValueError(kind)


def apply_transitions(src, out, cuts, dur=0.5, crf=17):
    """cuts = [(time_s, kind)]. One decode/encode pass; audio copied. Outgoing side freezes its last pre-cut frame."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    a_, b_ = probe.split("/"); fps = float(a_) / float(b_)
    half = int(round(dur * fps / 2)); jobs = {}
    for c, kind in cuts:
        fc = int(round(c * fps))
        for i in range(fc - half, fc + half): jobs[i] = (fc, kind)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{fps}",
                            "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
                            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    sz = W * H * 3; i = 0; buf = []          # buffer frames of the current transition window
    last_pre = None
    while True:
        raw = dec.stdout.read(sz)
        if len(raw) < sz: break
        if i in jobs:
            fc, kind = jobs[i]; buf.append(np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32))
            if i == fc + half - 1:
                pre = [b for j, b in zip(range(fc - half, fc + half), buf) if j < fc]; post = [b for j, b in zip(range(fc - half, fc + half), buf) if j >= fc]
                A_last, B_first = pre[-1], post[0]
                for n, j in enumerate(range(fc - half, fc + half)):
                    p = (n + 0.5) / (2 * half)
                    A = pre[n] if j < fc else A_last
                    B = post[j - fc] if j >= fc else B_first
                    enc.stdin.write(np.clip(tframe(kind, A, B, p), 0, 255).astype(np.uint8).tobytes())
                buf = []
        else:
            if buf:   # window cut short at file end
                for b in buf: enc.stdin.write(b.astype(np.uint8).tobytes())
                buf = []
            enc.stdin.write(raw)
        i += 1
    for b in buf: enc.stdin.write(b.astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait(); os.replace(out + ".tmp.mp4", out); return out


if __name__ == "__main__":   # preview stills: python3 tools/premium.py OUTDIR [BG.jpg] [BG2.jpg]
    import sys
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    bg = Image.open(sys.argv[2]).convert("RGBA").resize((W, H)) if len(sys.argv) > 2 else Image.new("RGBA", (W, H), (60, 70, 80, 255))
    ws = [(w, 0.3 * i, 0.3 * i + 0.25) for i, w in enumerate("I was very happy because I broke two hours. Next marathon, 1:58, I hope.".split())]
    tests = [("subs", 6, ("subs", ws), 2.0), ("iname", 6, ("iname", "Yomif Kejelcha", "1:59:41 · 2nd, London 2026", "Interview · London"), 2.5),
             ("clock", 5, ("clock", 7150, "London · finish straight"), 2.0),
             ("gap", 6, ("gap", "Sabastian Sawe", 7170, "Yomif Kejelcha", 7181, "11 seconds", "London Marathon · April 26, 2026"), 5.0),
             ("wipe", 4, ("wipe", ["The fastest marathon", "ever run to lose."], "1:59:41"), 2.0),
             ("timeline", 7, ("timeline", "So close, so many times", [(2016, "World Indoors 3000m", "Gold", ""), (2019, "Worlds 10,000m", "2nd", "0.?? s"), (2019, "Indoor mile", "WR", "3:47.01"), (2024, "Valencia Half", "WR", "57:30"), (2025, "Worlds 10,000m", "2nd", ""), (2026, "London Marathon", "2nd", "11 s")]), 6.5)]
    for nm, dur, spec, at in tests:
        fr = bg.copy(); fr.alpha_composite(K.KINDS[spec[0]](at, dur, *spec[1:])); fr.convert("RGB").save(f"{o}/{nm}.jpg", quality=85)
    if len(sys.argv) > 3:
        A = np.asarray(Image.open(sys.argv[2]).convert("RGB").resize((W, H))).astype(np.float32); B = np.asarray(Image.open(sys.argv[3]).convert("RGB").resize((W, H))).astype(np.float32)
        for kind in ("whip", "blur", "leak", "push", "luma"):
            strip = [Image.fromarray(np.clip(tframe(kind, A, B, p), 0, 255).astype(np.uint8)).resize((480, 270)) for p in (0.2, 0.4, 0.5, 0.6, 0.8)]
            s = Image.new("RGB", (2400, 270)); [s.paste(x, (480 * i, 0)) for i, x in enumerate(strip)]; s.save(f"{o}/tr_{kind}.jpg", quality=80)
    print("ok")

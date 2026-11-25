"""Cinematic layer (added 25 Nov 2026 for the Michael Norman video; user asked for a step up from the modern look).
Extends tools/modern.py (same type, colours and easing) with:
  letterbox  2.39:1 bars that slide in and out (cold open, low points, chapter turns)
  tracker    a row of global-championship results that fills in as the story goes (big meets only)
  counter    a live-ticking counter ("days since his PB") with a thin progress rule
  versus     two-column split comparison (e.g. Lyles vs Norman) whose rows ease in
  scope      a slow rotating ring + crosshair "lock-on" around a point (motion-tracked label feel)
All return RGBA 1920x1080 frames; import this module to register them in modern.KINDS.
"""
import math
from PIL import Image, ImageDraw
import modern as M
from modern import W, H, F, WHITE, SOFT, ACCENT, ease, inout, seg, life, layer, reveal, soft_shadow, scrim, draw_tracked, tracked

BAR = int((H - W / 2.39) / 2)   # 138 px for 2.39:1


def letterbox(t, dur, fin=0.6, fout=0.6):
    k = ease(seg(t, 0, fin)) * (1 - inout(seg(t, dur - fout, dur)))
    im = layer(); d = ImageDraw.Draw(im); h = int(BAR * k)
    if h > 0:
        d.rectangle([0, 0, W, h], fill=(0, 0, 0, 255)); d.rectangle([0, H - h, W, H], fill=(0, 0, 0, 255))
    return im


def tracker(t, dur, kicker, items, upto, hi=None):
    """items = [(meet, year, result, tone)], tone: 'good'|'bad'|'none'. Items with index < upto are filled; item `upto`
    (if any) animates in now. Bottom-centre strip over a soft gradient; reads like a scoreboard, nothing slams."""
    k = life(t, dur, 0.6, 0.5); out = scrim(0.55 * k, "bottom")
    n = len(items); cw = 250; x0 = W / 2 - n * cw / 2; y = H - 190
    hd = layer(); dh = ImageDraw.Draw(hd)
    draw_tracked(dh, (W / 2, y - 92), kicker.upper(), F(M.SEMI, 22), SOFT + (230,), 9, "c")
    out.alpha_composite(reveal(hd, k))
    for i, (meet, year, res, tone) in enumerate(items):
        if i > upto: kk = 0.25
        elif i == upto: kk = ease(seg(t, 0.5, 1.3))
        else: kk = 1.0
        c = layer(); d = ImageDraw.Draw(c); cx = x0 + i * cw + cw / 2
        col = (WHITE if tone == "good" else (232, 92, 80) if tone == "bad" else SOFT)
        a = int(255 * kk * k)
        d.line([(x0 + i * cw + 14, y - 50), (x0 + (i + 1) * cw - 14, y - 50)], fill=SOFT + (int(70 * k),), width=2)
        if kk > 0.3:
            d.line([(cx - 40 * kk, y - 50), (cx + 40 * kk, y - 50)], fill=col + (a,), width=4)
        draw_tracked(d, (cx, y - 14), f"{meet} {year}".upper(), F(M.MED, 20), SOFT + (int(220 * k),), 4, "c")
        fr = F(M.DISP_SEMI if i == hi else M.DISP_MED, 44)
        d.text((cx, y + 42), res if i <= upto else "·", font=fr, fill=col + (a if i <= upto else int(120 * k),), anchor="ms")
        out.alpha_composite(soft_shadow(c, 10, 0.5))
    return out


def counter(t, dur, start, end, label, sub=""):
    """Counts from start to end (ints) with commas, ticking like a clock; label in tracked caps; thin rule fills."""
    k = life(t, dur, 0.6, 0.6); out = scrim(0.6 * k)
    p = inout(seg(t, 0.3, max(0.4, dur - 1.0))); v = int(round(start + (end - start) * p))
    im = layer(); d = ImageDraw.Draw(im); f = F(M.XL, 240); s = f"{v:,}"
    d.text((W / 2, H / 2 + 50), s, font=f, fill=WHITE + (255,), anchor="ms")
    lw = 520; d.line([(W / 2 - lw / 2, H / 2 + 100), (W / 2 + lw / 2, H / 2 + 100)], fill=SOFT + (60,), width=2)
    d.line([(W / 2 - lw / 2, H / 2 + 100), (W / 2 - lw / 2 + lw * p, H / 2 + 100)], fill=ACCENT + (255,), width=3)
    draw_tracked(d, (W / 2, H / 2 + 160), label.upper(), F(M.SEMI, 30), WHITE + (235,), 10, "c")
    if sub: draw_tracked(d, (W / 2, H / 2 + 208), sub.upper(), F(M.REG, 22), SOFT + (210,), 7, "c")
    out.alpha_composite(reveal(soft_shadow(im, 24), k, 10)); return out


def versus(t, dur, left, right, rows, note=""):
    """Split comparison. left/right = (name, sub). rows = [(label, lval, rval)]; a thin centre divider grows."""
    k = life(t, dur, 0.6, 0.5); out = scrim(0.78 * k)
    g = ease(seg(t, 0.1, 0.9)); top = 290; n = len(rows); rh = 92
    dv = layer(); d = ImageDraw.Draw(dv)
    d.line([(W / 2, top - 40), (W / 2, top - 40 + 120 * g)], fill=SOFT + (90,), width=2)
    for side, (nm, sb), x in (("l", left, W / 2 - 360), ("r", right, W / 2 + 360)):
        d.text((x, top + 10), nm, font=F(M.DISP_SEMI, 60), fill=WHITE + (255,), anchor="ms")
        draw_tracked(d, (x, top + 56), sb.upper(), F(M.MED, 22), SOFT + (230,), 6, "c")
    out.alpha_composite(reveal(soft_shadow(dv), k))
    for i, (lab, lv, rv) in enumerate(rows):
        kr = life(max(0, t - 0.5 - i * 0.25), dur - 0.5 - i * 0.25, 0.5, 0.4)
        if kr <= 0: continue
        r = layer(); dr = ImageDraw.Draw(r); y = top + 150 + i * rh
        draw_tracked(dr, (W / 2, y - 34), lab.upper(), F(M.MED, 20), SOFT + (210,), 6, "c")
        dr.text((W / 2 - 360, y + 14), lv, font=F(M.DISP_MED, 50), fill=WHITE + (255,), anchor="ms")
        dr.text((W / 2 + 360, y + 14), rv, font=F(M.DISP_MED, 50), fill=WHITE + (255,), anchor="ms")
        out.alpha_composite(reveal(soft_shadow(r, 10), kr, 8))
    if note:
        nl = layer(); draw_tracked(ImageDraw.Draw(nl), (W / 2, top + 150 + n * rh + 20), note.upper(), F(M.REG, 22), SOFT + (220,), 7, "c")
        out.alpha_composite(reveal(nl, life(max(0, t - 1.0), dur - 1.0, 0.6, 0.5)))
    return out


def scope(t, dur, x, y, text, sub=""):
    """Lock-on ring around (x, y): ring shrinks onto the point, rotates slowly, tick marks; label to the right."""
    k = life(t, dur, 0.5, 0.4); s = ease(seg(t, 0, 0.7)); r = 150 - 70 * s; rot = t * 25
    im = layer(); d = ImageDraw.Draw(im); a = int(240 * k)
    d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE + (a,), width=2)
    for j in range(4):
        ang = math.radians(rot + j * 90); c, sn = math.cos(ang), math.sin(ang)
        d.line([(x + c * (r - 14), y + sn * (r - 14)), (x + c * (r + 14), y + sn * (r + 14))], fill=WHITE + (a,), width=3)
    if s > 0.9:
        lx = x + r + 40; d.line([(x + r + 6, y), (lx, y)], fill=WHITE + (a,), width=2)
        draw_tracked(d, (lx + 14, y + 10), text.upper(), F(M.SEMI, 28), WHITE + (a,), 5)
        if sub: draw_tracked(d, (lx + 14, y + 46), sub.upper(), F(M.REG, 20), SOFT + (int(220 * k),), 5)
    return soft_shadow(im, 8, 0.5)


M.KINDS.update(letterbox=letterbox, tracker=tracker, counter=counter, versus=versus, scope=scope)
render = M.render

"""Modern documentary graphics (user, 17 Nov 2026): replaces the kinetic.py "slap stickers".

Look: current Netflix/Apple sports doc. Clean Inter type, mostly white with soft shadows, small tracked-caps
kickers, big light-weight numerals, thin rules. Things ease in (fade + small drift + blur-to-sharp) and ease out;
nothing slams, shakes or flashes. No grain, no vintage textures, no orange boxes.

Same interface as kinetic.py: each graphic is frame(t, dur, *args) -> RGBA 1920x1080 and render(spec, dur, out)
writes a .mov (png codec, alpha) for ffmpeg to overlay. Kinds: date, title, number, name, quote, chapter, source, label.
"""
import os, subprocess
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 24
FD = "/usr/share/fonts/opentype/inter"
THIN, XL, LIGHT, REG, MED, SEMI, BOLD = (f"{FD}/Inter-{w}.otf" for w in ("Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold"))
DISP_MED, DISP_SEMI, DISP_BOLD = (f"{FD}/InterDisplay-{w}.otf" for w in ("Medium", "SemiBold", "Bold"))
WHITE = (246, 246, 244)
SOFT = (210, 212, 216)
ACCENT = (226, 72, 58)      # used sparingly: one thin rule or one word, never a box


def ease(t): t = min(max(t, 0.0), 1.0); return 1 - (1 - t) ** 3            # ease-out cubic
def inout(t): t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)
def seg(t, a, b): return min(max((t - a) / (b - a), 0.0), 1.0) if b > a else float(t >= a)
def life(t, dur, fin=0.6, fout=0.45): return ease(seg(t, 0, fin)) * (1 - inout(seg(t, dur - fout, dur)))


@lru_cache(128)
def F(path, size): return ImageFont.truetype(path, int(size))


def tracked(text, font, track):
    """Width of text drawn with extra letter spacing (track in px)."""
    return sum(font.getlength(c) for c in text) + track * max(0, len(text) - 1)


def draw_tracked(d, xy, text, font, fill, track, anchor="l"):
    x, y = xy; w = tracked(text, font, track)
    if anchor == "c": x -= w / 2
    elif anchor == "r": x -= w
    for c in text:
        d.text((x, y), c, font=font, fill=fill, anchor="ls"); x += font.getlength(c) + track
    return w


def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def soft_shadow(im, radius=18, opacity=0.55):
    a = im.split()[3].filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * opacity))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a)
    out = layer(); out.alpha_composite(sh, (0, 6)); out.alpha_composite(im); return out


def reveal(im, k, drift=18):
    """Blur-to-sharp + small upward drift + fade, k in 0..1 (1 = settled)."""
    if k <= 0: return layer()
    if k < 1:
        b = (1 - k) * 10
        if b > 0.4: im = im.filter(ImageFilter.GaussianBlur(b))
        im = im.transform(im.size, Image.AFFINE, (1, 0, 0, 0, 1, -drift * (1 - k)), Image.BICUBIC)
    a = im.split()[3].point(lambda v: int(v * k)); im = im.copy(); im.putalpha(a); return im


def scrim(alpha, where="full"):
    """Darkening behind type so it reads on any footage."""
    im = layer()
    if alpha <= 0: return im
    if where == "full":
        im.paste((0, 0, 0, int(255 * alpha)), (0, 0, W, H)); return im
    g = Image.linear_gradient("L").resize((W, H))      # 0 top -> 255 bottom
    if where == "left": g = Image.linear_gradient("L").rotate(90, expand=True).resize((W, H)).transpose(Image.FLIP_LEFT_RIGHT)
    blk = Image.new("RGBA", (W, H), (0, 0, 0, 255)); blk.putalpha(g.point(lambda v: int(v * alpha))); return blk


# ---------------------------------------------------------------- graphics
def date(t, dur, text, sub=""):
    """Centred date card: tracked caps between two hairlines, darkened frame."""
    k = life(t, dur, 0.9, 0.6); out = scrim(0.45 * k)
    im = layer(); d = ImageDraw.Draw(im); f = F(MED, 40); tr = 14
    w = draw_tracked(d, (W / 2, H / 2 + 14), text.upper(), f, WHITE + (255,), tr, "c")
    grow = ease(seg(t, 0.15, 1.1)); L = 140 * grow
    d.line([(W / 2 - w / 2 - 40 - L, H / 2), (W / 2 - w / 2 - 40, H / 2)], fill=WHITE + (200,), width=2)
    d.line([(W / 2 + w / 2 + 40, H / 2), (W / 2 + w / 2 + 40 + L, H / 2)], fill=WHITE + (200,), width=2)
    if sub: draw_tracked(d, (W / 2, H / 2 + 74), sub.upper(), F(REG, 24), SOFT + (220,), 8, "c")
    out.alpha_composite(reveal(soft_shadow(im), k)); return out


def title(t, dur, kicker, headline, pos="bl"):
    """Kicker (small tracked caps) over a headline, lower-left, with a bottom gradient for legibility."""
    k1 = life(t, dur, 0.7, 0.5); k2 = life(max(0, t - 0.18), dur - 0.18, 0.8, 0.5)
    out = scrim(0.6 * k1, "bottom")
    x, y = 140, H - 210
    a = layer(); d = ImageDraw.Draw(a)
    d.line([(x, y - 70), (x + 56 * ease(seg(t, 0, 0.8)), y - 70)], fill=ACCENT + (255,), width=3)
    draw_tracked(d, (x, y - 30), kicker.upper(), F(SEMI, 26), SOFT + (255,), 7)
    b = layer(); ImageDraw.Draw(b).text((x - 4, y + 64), headline, font=F(DISP_SEMI, 92), fill=WHITE + (255,), anchor="ls")
    out.alpha_composite(reveal(soft_shadow(a), k1)); out.alpha_composite(reveal(soft_shadow(b, 22), k2, 24)); return out


def _num_at(final, k):
    """Count up the digits of a time/number string; non-digits stay put."""
    digs = [c for c in final if c.isdigit()]
    if not digs or k >= 1: return final
    val = int("".join(digs)); cur = str(int(val * inout(k))).zfill(len(digs)); it = iter(cur)
    return "".join(next(it) if c.isdigit() else c for c in final)


def number(t, dur, value, label, sub=""):
    """Big light numerals centred on a darkened frame; digits count up and settle; label in tracked caps."""
    k = life(t, dur, 0.5, 0.5); out = scrim(0.55 * k)
    cnt = ease(seg(t, 0.1, 1.0)); txt = _num_at(value, cnt)
    im = layer(); d = ImageDraw.Draw(im)
    f = F(XL, 250)
    while f.getlength(value) > W - 300: f = F(XL, f.size - 10)
    vw = f.getlength(value)
    d.text((W / 2 - vw / 2, H / 2 + 60), txt, font=f, fill=WHITE + (255,), anchor="ls")
    lab = layer(); dl = ImageDraw.Draw(lab)
    lw = draw_tracked(dl, (W / 2, H / 2 + 150), label.upper(), F(SEMI, 30), WHITE + (235,), 10, "c")
    dl.line([(W / 2 - 30, H / 2 + 100), (W / 2 + 30, H / 2 + 100)], fill=ACCENT + (255,), width=3)
    if sub: draw_tracked(dl, (W / 2, H / 2 + 200), sub.upper(), F(REG, 24), SOFT + (210,), 7, "c")
    out.alpha_composite(reveal(soft_shadow(im, 26), k, 10))
    out.alpha_composite(reveal(soft_shadow(lab), life(max(0, t - 0.35), dur - 0.35, 0.6, 0.5)))
    return out


def name(t, dur, nm, sub, side="l"):
    """Minimal lower third: a hairline grows, the name eases in above it, the role below."""
    k = life(t, dur, 0.6, 0.45); g = ease(seg(t, 0, 0.7))
    x = 140 if side == "l" else W - 140; y = H - 190
    out = scrim(0.45 * k, "bottom")
    im = layer(); d = ImageDraw.Draw(im)
    fN = F(DISP_SEMI, 58); fS = F(MED, 26)
    wN = fN.getlength(nm); wS = tracked(sub.upper(), fS, 6); L = max(wN, wS) + 20
    x0 = x if side == "l" else x - L
    d.line([(x0, y + 14), (x0 + L * g, y + 14)], fill=WHITE + (210,), width=2)
    d.line([(x0, y + 14), (x0 + 40 * g, y + 14)], fill=ACCENT + (255,), width=4)
    d.text((x0, y - 8), nm, font=fN, fill=WHITE + (255,), anchor="ls")
    draw_tracked(d, (x0, y + 58), sub.upper(), fS, SOFT + (240,), 6)
    out.alpha_composite(reveal(soft_shadow(im), k, 14)); return out


def quote(t, dur, text, who=""):
    """Centred quote; words fade in one after another; attribution in tracked caps."""
    out = scrim(0.6 * life(t, dur, 0.6, 0.5))
    words = text.split(); f = F(DISP_MED, 64); maxw = W - 520
    lines, cur = [], []
    for wd in words:
        if cur and f.getlength(" ".join(cur + [wd])) > maxw: lines.append(cur); cur = []
        cur.append(wd)
    if cur: lines.append(cur)
    n = len(words); per = min(0.22, max(0.08, (dur * 0.45) / max(1, n)))
    im = layer(); d = ImageDraw.Draw(im); i = 0; lh = 86; y0 = H / 2 - (len(lines) - 1) * lh / 2 + 20
    fade_out = 1 - inout(seg(t, dur - 0.45, dur))
    for li, ln in enumerate(lines):
        x = W / 2 - f.getlength(" ".join(ln)) / 2
        for wd in ln:
            a = ease(seg(t, 0.25 + i * per, 0.25 + i * per + 0.45)) * fade_out
            d.text((x, y0 + li * lh), wd, font=f, fill=WHITE + (int(255 * a),), anchor="ls"); x += f.getlength(wd + " "); i += 1
    if who:
        a = ease(seg(t, 0.25 + n * per, 0.25 + n * per + 0.6)) * fade_out
        draw_tracked(d, (W / 2, y0 + len(lines) * lh + 30), "— " + who.upper(), F(MED, 26), SOFT + (int(240 * a),), 8, "c")
    out.alpha_composite(soft_shadow(im, 20)); return out


def chapter(t, dur, num, ttl):
    """Chapter card: 'PART 02' small, title large and light, centred, over a dark frame."""
    k = life(t, dur, 0.7, 0.6); out = scrim(0.7 * k)
    a = layer(); d = ImageDraw.Draw(a)
    draw_tracked(d, (W / 2, H / 2 - 70), f"PART {num}", F(SEMI, 26), SOFT + (255,), 12, "c")
    d.line([(W / 2 - 24, H / 2 - 46), (W / 2 + 24, H / 2 - 46)], fill=ACCENT + (255,), width=3)
    b = layer(); f = F(LIGHT, 110)
    while f.getlength(ttl) > W - 240: f = F(LIGHT, f.size - 6)
    ImageDraw.Draw(b).text((W / 2, H / 2 + 60), ttl, font=f, fill=WHITE + (255,), anchor="ms")
    out.alpha_composite(reveal(soft_shadow(a), k)); out.alpha_composite(reveal(soft_shadow(b, 24), life(max(0, t - 0.2), dur - 0.2, 0.8, 0.6), 26))
    return out


def label(t, dur, text, x, y, sub=""):
    """Pin label for a point in frame (x, y in px): dot, leader line, small text. Static anchor."""
    k = life(t, dur, 0.5, 0.4); g = ease(seg(t, 0.05, 0.6))
    im = layer(); d = ImageDraw.Draw(im)
    r = 7; d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE + (255,), width=2); d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=WHITE + (255,))
    lx, ly = x + 70 * g, y - 70 * g; d.line([(x + 5, y - 5), (lx, ly)], fill=WHITE + (230,), width=2)
    if g > 0.95:
        d.line([(lx, ly), (lx + 30, ly)], fill=WHITE + (230,), width=2)
        draw_tracked(d, (lx + 40, ly + 9), text.upper(), F(SEMI, 26), WHITE + (255,), 5)
        if sub: draw_tracked(d, (lx + 40, ly + 44), sub.upper(), F(REG, 20), SOFT + (230,), 5)
    out = layer(); out.alpha_composite(reveal(soft_shadow(im, 10), k, 6)); return out


def source(t, dur, text):
    """Tiny credit bottom-right: tracked caps, no box."""
    im = layer(); a = life(t, dur, 0.4, 0.3)
    if a <= 0: return im
    d = ImageDraw.Draw(im); draw_tracked(d, (W - 70, H - 56), text.upper(), F(MED, 18), WHITE + (int(170 * a),), 4, "r")
    return soft_shadow(im, 6, 0.6)


KINDS = dict(date=date, title=title, number=number, name=name, quote=quote, chapter=chapter, label=label, source=source)


def render(spec, dur, out):
    """spec = (kind, *args). Writes a png-in-mov with alpha, dur seconds."""
    fn = KINDS[spec[0]]; n = max(1, round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out + ".tmp.mov"], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(fn(i / FPS, dur, *spec[1:]).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + ".tmp.mov", out)
    return out


if __name__ == "__main__":   # quick look: python3 tools/modern.py OUTDIR [BG.jpg]
    import sys
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    bg = Image.open(sys.argv[2]).convert("RGBA").resize((W, H)) if len(sys.argv) > 2 else Image.new("RGBA", (W, H), (70, 80, 90, 255))
    tests = [("date", 3, ("date", "November 7, 2019", "New York Times")), ("title", 3, ("title", "Bronxville, New York", "The fastest girl in America")),
             ("number", 3, ("number", "4:04.62", "American junior record", "1500m · May 2013")), ("name", 3, ("name", "Alberto Salazar", "Head coach · Nike Oregon Project")),
             ("quote", 4, ("quote", "They wanted me thinner, and thinner, and thinner.", "Mary Cain")), ("chapter", 3, ("chapter", "02", "The Deal")),
             ("label", 3, ("label", "Mary Cain", 900, 600, "Age 17")), ("source", 3, ("source", "New York Times Opinion · 2019"))]
    for nm, dur, spec in tests:
        fr = bg.copy(); fr.alpha_composite(KINDS[spec[0]](dur * 0.6, dur, *spec[1:])); fr.convert("RGB").save(f"{o}/{nm}.jpg", quality=88)
    print("ok")

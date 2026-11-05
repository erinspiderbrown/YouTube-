"""Jon Drummond thumbnails v2: high-res, layered.

Sources: real broadcast frames upscaled 3x with Topaz "Recover 3" (ElevenLabs flow "Jon Drummond thumbnails"),
subject cut-outs with BiRefNet, Wikimedia Commons Stade de France (Paris 2003) and the USADA logo.
Rendered at 2560x1440, saved as 1280x720 (YouTube size) and a full-size PNG.

T1  PROTEST vs BAN: Paris stadium backdrop, cut-out Drummond hands up ("I didn't move"), a tilted USADA case
    file with a BANNED 8 YEARS stamp, a circular inset of him lying on the track, 2003/2014 tags, neon rim light.
T2  HE WOULDN'T LEAVE: sharp full-bleed shot of him on the track with officials standing over him, big glowing
    3-line text, an inset of him arguing with officials, red arrow, PARIS 2003 tag.
T3  Jimmy-style: overhead shot of him alone on the track, red ring + arrow, face close-up inset, one-line caption.
"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
SRC = f"{SCR}/thumb_jd"
PH = f"{SCR}/photos"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SCR}/output"
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
INTER = "/usr/share/fonts/opentype/inter/"
W, H = 2560, 1440
RED = (236, 28, 36); WHITE = (255, 255, 255); ORANGE = (255, 122, 26); CYAN = (0, 229, 255); YEL = (255, 214, 0)

def F(size): return ImageFont.truetype(ANTON, size)
def FI(w, size): return ImageFont.truetype(f"{INTER}Inter-{w}.otf", size)

def load(name):
    return Image.open(f"{SRC}/{name}.png")

def grade(im, contrast=1.1, color=1.15, sharp=True):
    im = im.convert("RGB")
    if sharp: im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(contrast)).enhance(color)

def cover(im, size, cx=0.5, cy=0.5):
    w, h = im.size; tw, th = size
    s = max(tw / w, th / h); im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    x = int((im.width - tw) * cx); y = int((im.height - th) * cy)
    return im.crop((x, y, x + tw, y + th))

def outline(cut, px=10, color=WHITE, glow=None, glow_r=30):
    """White sticker outline (+ optional colored glow) around an RGBA cut-out."""
    a = cut.split()[-1]
    pad = px + glow_r * 2
    big = Image.new("RGBA", (cut.width + 2 * pad, cut.height + 2 * pad), (0, 0, 0, 0))
    am = Image.new("L", big.size, 0); am.paste(a, (pad, pad))
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    if glow:
        g = am.filter(ImageFilter.MaxFilter(px * 2 + 1)).filter(ImageFilter.GaussianBlur(glow_r))
        gl = Image.new("RGBA", big.size, glow + (0,)); gl.putalpha(g.point(lambda v: min(255, int(v * 1.6))))
        out.alpha_composite(gl)
    st = am.filter(ImageFilter.MaxFilter(px * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    sl = Image.new("RGBA", big.size, color + (0,)); sl.putalpha(st)
    out.alpha_composite(sl)
    out.alpha_composite(cut, (pad, pad))
    return out, pad

def shadow(base, layer, xy, off=(18, 26), blur=28, alpha=170):
    a = layer.split()[-1].point(lambda v: v * alpha // 255).filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(a)
    base.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1]))
    base.alpha_composite(layer, xy)

def text(base, xy, s, size, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0), glow=None, glow_r=26, glow_a=1.0, anchor="la", shadow_px=10):
    f = F(size)
    if shadow_px:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        sd.text((xy[0] + shadow_px, xy[1] + shadow_px), s, font=f, fill=(0, 0, 0, 200), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    if glow:
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.text(xy, s, font=f, fill=glow + (255,), anchor=anchor, stroke_width=stroke + 8, stroke_fill=glow + (255,))
        g = lay.filter(ImageFilter.GaussianBlur(glow_r)); g.putalpha(g.split()[-1].point(lambda v: min(255, int(v * glow_a))))
        base.alpha_composite(g)
    d = ImageDraw.Draw(base)
    d.text(xy, s, font=f, fill=fill + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill + (255,))
    return d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke)

def circle_inset(base, im, center, r, ring=RED, ring_w=16):
    im = cover(im, (2 * r, 2 * r))
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    lay = Image.new("RGBA", (2 * r + 80, 2 * r + 80), (0, 0, 0, 0))
    sh = Image.new("L", lay.size, 0); ImageDraw.Draw(sh).ellipse([40, 52, 40 + 2 * r, 52 + 2 * r], fill=190)
    shl = Image.new("RGBA", lay.size, (0, 0, 0, 0)); shl.putalpha(sh.filter(ImageFilter.GaussianBlur(22)))
    lay.alpha_composite(shl)
    lay.paste(im, (40, 40), m)
    d = ImageDraw.Draw(lay)
    d.ellipse([40 - 10, 40 - 10, 40 + 2 * r + 10, 40 + 2 * r + 10], outline=WHITE + (255,), width=ring_w + 10)
    d.ellipse([40 - 4, 40 - 4, 40 + 2 * r + 4, 40 + 2 * r + 4], outline=ring + (255,), width=ring_w)
    base.alpha_composite(lay, (center[0] - r - 40, center[1] - r - 40))

def arrow(base, p0, p1, bend=0.25, color=RED, width=26):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 60)]
    ang = math.atan2(pts[-1][1] - pts[-5][1], pts[-1][0] - pts[-5][0])
    L = width * 3.0
    def head(scale):
        tip = (x1 + math.cos(ang) * width * 0.6 * scale, y1 + math.sin(ang) * width * 0.6 * scale)
        return [tip, (x1 - L * scale * math.cos(ang - 0.55), y1 - L * scale * math.sin(ang - 0.55)),
                (x1 - L * scale * math.cos(ang + 0.55), y1 - L * scale * math.sin(ang + 0.55))]
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(pts[:-3], fill=WHITE + (255,), width=width + 14, joint="curve"); d.polygon(head(1.22), fill=WHITE + (255,))
    d.line(pts[:-3], fill=color + (255,), width=width, joint="curve"); d.polygon(head(1.0), fill=color + (255,))
    sh = lay.split()[-1].filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 150 // 255)
    s = Image.new("RGBA", base.size, (0, 0, 0, 0)); s.putalpha(sh)
    base.alpha_composite(s, (8, 12)); base.alpha_composite(lay)

def tag(base, xy, s, color, size=92):
    d = ImageDraw.Draw(base); f = F(size); tw = d.textlength(s, font=f)
    x, y = xy; h = int(size * 1.32)
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([x - 8, y - 8, x + tw + 68, y + h + 8], radius=26, outline=color + (255,), width=16)
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(16)))
    d.rounded_rectangle([x, y, x + tw + 60, y + h], radius=22, fill=(8, 10, 18, 240), outline=color + (255,), width=7)
    d.text((x + 30, y + h // 2 + 2), s, font=f, fill=WHITE + (255,), anchor="lm")

def stamp(t1, t2, w=880, h=470, rot=-8):
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rounded_rectangle([14, 14, w - 14, h - 14], radius=34, outline=RED + (255,), width=24)
    d.rounded_rectangle([40, 40, w - 40, h - 40], radius=24, outline=RED + (255,), width=7)
    d.text((w // 2, h * 0.40), t1, font=F(int(h * 0.42)), fill=RED + (255,), anchor="mm")
    d.text((w // 2, h * 0.76), t2, font=F(int(h * 0.20)), fill=RED + (255,), anchor="mm")
    a = np.asarray(st).copy()
    rng = np.random.default_rng(7)
    noise = Image.fromarray((rng.random(a.shape[:2]) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
    nz = np.asarray(noise)
    a[..., 3] = (a[..., 3] * np.where(nz < 70, 0.25, 1.0)).astype(np.uint8)
    return Image.fromarray(a).rotate(rot, expand=True, resample=Image.BICUBIC)

def case_file(w=980, h=1180):
    """A USADA decision document (paper) with redacted-style lines; the real USADA logo at the top."""
    doc = Image.new("RGBA", (w, h), (246, 243, 236, 255)); d = ImageDraw.Draw(doc)
    logo = Image.open(f"{PH}/l_usada.jpg").convert("RGB")
    lg = logo.crop((0, 0, logo.width, logo.height)); lg.thumbnail((420, 260), Image.LANCZOS)
    doc.paste(lg, (60, 60))
    d.text((60, 60 + lg.height + 40), "ANTI-DOPING DECISION", font=FI("Black", 64), fill=(25, 25, 30, 255))
    d.text((60, 60 + lg.height + 120), "Respondent: JON DRUMMOND", font=FI("Bold", 40), fill=(60, 60, 66, 255))
    d.text((60, 60 + lg.height + 172), "December 17, 2014", font=FI("Medium", 36), fill=(90, 90, 96, 255))
    y = 60 + lg.height + 250
    rng = np.random.default_rng(3)
    for i in range(11):
        ln = int(w - 120 - rng.integers(0, 260)) if i % 4 else int(w * 0.55)
        col = (40, 40, 44, 255) if i in (4, 5) else (175, 172, 165, 255)
        d.rounded_rectangle([60, y, 60 + ln, y + 22], radius=6, fill=col)
        y += 48
    d.rectangle([0, h - 18, w, h], fill=RED + (255,))
    return doc

# ------------------------------------------------------------------ T1
def t1():
    bg = Image.open(f"{PH}/l_paris_stadium.jpg").convert("RGB")
    bg = cover(bg, (W, H), 0.5, 0.35).filter(ImageFilter.GaussianBlur(5))
    bg = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(0.8)).enhance(0.42)
    can = bg.convert("RGBA")
    # red/orange atmosphere from the right, cool from the left
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    warm = np.clip((x - W * 0.45) / (W * 0.55), 0, 1) ** 1.3 * 0.55
    cool = np.clip((W * 0.45 - x) / (W * 0.45), 0, 1) ** 1.5 * 0.35
    tint = np.zeros((H, W, 4), np.uint8)
    tint[..., 0] = 200; tint[..., 1] = 20; tint[..., 2] = 20; tint[..., 3] = (warm * 255).astype(np.uint8)
    can.alpha_composite(Image.fromarray(tint))
    tint2 = np.zeros((H, W, 4), np.uint8); tint2[..., 0] = 0; tint2[..., 1] = 120; tint2[..., 2] = 200; tint2[..., 3] = (cool * 255).astype(np.uint8)
    can.alpha_composite(Image.fromarray(tint2))
    # case file (right), tilted, with the BANNED stamp on it
    doc = case_file().rotate(5, expand=True, resample=Image.BICUBIC)
    doc = doc.resize((int(doc.width * 0.95), int(doc.height * 0.95)), Image.LANCZOS)
    dx, dy = W - doc.width - 40, 175
    shadow(can, doc, (dx, dy), off=(24, 34), blur=34, alpha=200)
    st = stamp("BANNED", "8 YEARS", w=900, h=480, rot=-11)
    shadow(can, st, (dx + doc.width // 2 - st.width // 2 - 20, dy + 470), off=(10, 14), blur=14, alpha=120)
    # Drummond cut-out (left), hands up: "I didn't move"
    src = Image.open(f"{SRC}/cut_handsup.png").convert("RGBA")
    src = src.crop(src.split()[-1].getbbox())
    s_ = 1180 / src.height
    cut = src.resize((int(src.width * s_), int(src.height * s_)), Image.LANCZOS)
    rgb = grade(cut.convert("RGB"), 1.08, 1.1); rgb.putalpha(cut.split()[-1]); cut = rgb
    st_cut, pad = outline(cut, 12, WHITE, glow=CYAN, glow_r=40)
    shadow(can, st_cut, (-60 - pad, H - cut.height - pad + 8), off=(20, 20), blur=30, alpha=150)
    # inset: him lying on the track, between the two halves
    circle_inset(can, grade(load("up_overhead")).crop((700, 0, 1800, 1100)), (1490, 1080), 250)
    text(can, (1490, 1418), "HE WOULDN'T LEAVE", 96, WHITE, stroke=8, anchor="mb", shadow_px=8)
    tag(can, (70, 64), "2003", CYAN)
    tag(can, (W - 330, 64), "2014", ORANGE)
    return can.convert("RGB")

# ------------------------------------------------------------------ T2
def t2():
    ph = grade(load("up_lying_officials"), 1.12, 1.15)
    ph = cover(ph, (int(W * 0.70), H), 0.62, 0.5)
    can = Image.new("RGBA", (W, H), (34, 36, 42, 255))
    noise = np.random.default_rng(2).normal(0, 14, (H, W)).astype(np.float32)
    g = np.clip(np.full((H, W), 52, np.float32) + noise, 0, 255).astype(np.uint8)
    can = Image.merge("RGBA", (Image.fromarray(g),) * 3 + (Image.new("L", (W, H), 255),))
    ramp = np.clip((np.arange(ph.width) - 20) / 520, 0, 1)[None, :] * np.ones((H, 1))
    can.paste(ph, (W - ph.width, 0), Image.fromarray((ramp * 255).astype(np.uint8)))
    vg = Image.new("L", (W, H), 0); ImageDraw.Draw(vg).ellipse([-500, -400, W + 500, H + 400], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(200))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dark.putalpha(Image.eval(vg, lambda v: (255 - v) * 150 // 255))
    can.alpha_composite(dark)
    lines = [("HE", 300, WHITE, WHITE, 0), ("WOULDN'T", 340, WHITE, WHITE, 0), ("LEAVE", 470, RED, (255, 50, 50), 10)]
    hs = [F(sz).getbbox(t)[3] - F(sz).getbbox(t)[1] for t, sz, *_ in lines]
    gap = 40; y = (H - sum(hs) - 2 * gap) // 2
    for (t, sz, col, gl, st), h in zip(lines, hs):
        top = F(sz).getbbox(t)[1]
        text(can, (90, y - top), t, sz, col, stroke=st, glow=gl, glow_r=34, glow_a=0.75, shadow_px=12)
        y += h + gap
    circle_inset(can, grade(load("up_arguing")).crop((0, 0, 1900, 1878)), (W - 300, 300), 255, ring=ORANGE)
    arrow(can, (W - 520, 520), (W - 1000, 900), bend=0.3)
    tag(can, (W - 560, H - 200), "PARIS 2003", CYAN, size=80)
    return can.convert("RGB")

# ------------------------------------------------------------------ T3
def t3():
    ph = grade(load("up_overhead"), 1.12, 1.2)
    can = cover(ph, (W, H), 0.5, 0.4).convert("RGBA")
    vg = Image.new("L", (W, H), 0); ImageDraw.Draw(vg).ellipse([-300, -300, W + 300, H + 300], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dark.putalpha(Image.eval(vg, lambda v: (255 - v) * 170 // 255))
    can.alpha_composite(dark)
    d = ImageDraw.Draw(can)
    cx, cy, rx, ry = 1015, 640, 300, 560
    d.ellipse([cx - rx - 10, cy - ry - 10, cx + rx + 10, cy + ry + 10], outline=WHITE + (255,), width=34)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=RED + (255,), width=22)
    arrow(can, (1850, 1010), (1350, 560), bend=0.28, width=34)
    circle_inset(can, grade(load("up_face_closeup")).crop((300, 100, 2511, 1878)), (W - 255, 255), 225, ring=ORANGE)   # also hides the TV logo
    text(can, (W - 70, H - 60), "HE WOULDN'T MOVE", 230, WHITE, stroke=14, anchor="rb", shadow_px=14)
    return can.convert("RGB")

if __name__ == "__main__":
    for k, fn in (("1", t1), ("2", t2), ("3", t3)):
        im = fn()
        im.save(f"{OUT}/drummond_thumb_v2_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/drummond_thumb_v2_{k}.jpg", quality=94)
        print(k, im.size)

"""Jon Drummond thumbnails: three variants for YouTube's Test & Compare.

A  "HE WOULDN'T LEAVE"  - the channel's proven format (big glowing words + emotional real frame)
B  2003 vs 2014 split    - protest (hands up) vs 8-year ban stamp, neon divider
C  Jimmy-style moment    - full-bleed overhead shot of him alone on the track, red circle + arrow, short caption
Frames come from the real footage in the scratchpad (see credits.md). Output 1280x720 JPGs.
"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
SRC = f"{SCR}/thumb_jd"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SCR}/output"
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
W, H = 1280, 720
RED = (235, 30, 35); WHITE = (255, 255, 255); ORANGE = (255, 122, 26); CYAN = (0, 229, 255)

def F(size): return ImageFont.truetype(ANTON, size)

def frame(name, box=None):
    im = Image.open(f"{SRC}/{name}.png").convert("RGB")
    bb = im.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()   # drop black letterbox
    if bb: im = im.crop(bb)
    if box: im = im.crop(box)
    return im

def enhance(im, size):
    im = im.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2.2, percent=140, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(1.12)
    return ImageEnhance.Color(im).enhance(1.18)

def grit(im, amt=9, seed=1):
    a = np.asarray(im).astype(np.float32)
    a += np.random.default_rng(seed).normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def glow_text(base, xy, text, size, fill=WHITE, glow=WHITE, glow_r=16, glow_a=200, stroke=0, anchor="la"):
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, text, font=F(size), fill=glow + (255,), anchor=anchor, stroke_width=stroke + 6, stroke_fill=glow + (255,))
    g = lay.filter(ImageFilter.GaussianBlur(glow_r)); g.putalpha(g.split()[-1].point(lambda v: min(255, v * glow_a // 255)))
    base.alpha_composite(g)
    d2 = ImageDraw.Draw(base)
    d2.text(xy, text, font=F(size), fill=fill + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return d2.textbbox(xy, text, font=F(size), anchor=anchor, stroke_width=stroke)

def arrow(base, pts, color=RED, width=16):
    """Hand-drawn style curved arrow through 3 points (quadratic bezier), white outline, arrowhead at the end."""
    (x0, y0), (cx, cy), (x1, y1) = pts
    path = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 40)]
    ang = math.atan2(path[-1][1] - path[-4][1], path[-1][0] - path[-4][0])
    L = width * 3.2
    head = [(x1 + L * 0.25 * math.cos(ang), y1 + L * 0.25 * math.sin(ang)),
            (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)),
            (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))]
    d = ImageDraw.Draw(base)
    for col, w, grow in ((WHITE, width + 10, 6), (color, width, 0)):
        d.line(path[:-2], fill=col + (255,), width=w, joint="curve")
        hh = [(x + (x - x1) * 0 , y) for x, y in head]
        if grow:
            cxh = sum(p[0] for p in head) / 3; cyh = sum(p[1] for p in head) / 3
            hh = [(cxh + (x - cxh) * 1.25, cyh + (y - cyh) * 1.25) for x, y in head]
        d.polygon(hh, fill=col + (255,))

def ring(base, box, color=RED, width=12):
    d = ImageDraw.Draw(base)
    d.ellipse(box, outline=WHITE + (255,), width=width + 8)
    d.ellipse([box[0] + 4, box[1] + 4, box[2] - 4, box[3] - 4], outline=color + (255,), width=width)

# ------------------------------------------------------------------ A: HE WOULDN'T LEAVE
def thumb_a():
    bg = Image.new("RGB", (W, H), (70, 72, 76)); bg = grit(bg, 12, 3)
    ph = frame("ds335", (215, 8, 790, 620))                                      # officials' feet + his face (TV logo cropped out)
    ph = enhance(ph, (int(ph.width * H / ph.height), H))
    can = bg.convert("RGBA")
    x0 = W - ph.width + 40
    ramp = np.clip((np.arange(ph.width) - 10) / 230, 0, 1)[None, :] * np.ones((ph.height, 1))
    can.paste(ph, (x0, 0), Image.fromarray((ramp * 255).astype(np.uint8)))
    lines = [("HE", 150, WHITE, WHITE, 0), ("WOULDN'T", 172, WHITE, WHITE, 0), ("LEAVE", 226, RED, (255, 60, 60), 4)]
    hs = [F(sz).getbbox(t)[3] - F(sz).getbbox(t)[1] for t, sz, *_ in lines]
    gap = 22; y = (H - sum(hs) - gap * 2) // 2
    for (t, sz, col, gl, st), h in zip(lines, hs):
        top = F(sz).getbbox(t)[1]
        glow_text(can, (46, y - top), t, sz, col, gl, 18, 190, stroke=st)
        y += h + gap
    return can.convert("RGB")

# ------------------------------------------------------------------ B: 2003 vs 2014
def stamp(text1, text2, w=600, h=330):
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rounded_rectangle([12, 12, w - 12, h - 12], radius=26, outline=RED + (255,), width=18)
    d.text((w // 2, 128), text1, font=F(150), fill=RED + (255,), anchor="mm")
    d.text((w // 2, 255), text2, font=F(86), fill=RED + (255,), anchor="mm")
    a = np.asarray(st).copy()                                                    # rubber-stamp wear
    holes = np.random.default_rng(4).random(a.shape[:2]) < 0.10
    a[..., 3][holes] = (a[..., 3][holes] * 0.25).astype(np.uint8)
    return Image.fromarray(a).rotate(-9, expand=True, resample=Image.BICUBIC)

def pill(base, xy, text, color):
    d = ImageDraw.Draw(base); f = F(64)
    tw = d.textlength(text, font=f)
    x, y = xy
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([x - 6, y - 6, x + tw + 46, y + 94], radius=18, outline=color + (255,), width=10)
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle([x, y, x + tw + 40, y + 88], radius=16, fill=(8, 10, 18, 235), outline=color + (255,), width=5)
    d.text((x + 20, y + 44), text, font=f, fill=WHITE + (255,), anchor="lm")

def thumb_b():
    can = Image.new("RGBA", (W, H), (10, 8, 12, 255))
    LW = 740
    left = enhance(frame("ds575", (110, 0, 110 + LW, 720)), (LW, H))              # both hands in frame
    can.paste(left, (0, 0))
    right = enhance(frame("ds323", (220, 60, 640, 600)), (W - LW, H))             # overhead: lying on the track
    right = ImageEnhance.Brightness(right).enhance(0.42).convert("RGBA")
    right.alpha_composite(Image.new("RGBA", right.size, (120, 0, 0, 90)))
    can.paste(right, (LW, 0))
    st = stamp("BANNED", "8 YEARS"); st = st.resize((int(st.width * 0.82), int(st.height * 0.82)), Image.LANCZOS)
    can.alpha_composite(st, (LW + (W - LW) // 2 - st.width // 2, 380 - st.height // 2))
    lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.line([(LW, 0), (LW, H)], fill=ORANGE + (255,), width=16)
    can.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(can).line([(LW, 0), (LW, H)], fill=(255, 220, 180, 255), width=5)
    pill(can, (28, 26), "2003", CYAN)
    pill(can, (W - 180, 26), "2014", ORANGE)
    return can.convert("RGB")

# ------------------------------------------------------------------ C: Jimmy-style real moment
def thumb_c():
    ph = enhance(frame("ds323", (0, 120, 836, 590)), (W, H))
    can = ph.convert("RGBA")
    vig = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vig)
    vd.ellipse([-200, -260, W + 200, H + 260], fill=255); vig = vig.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 170)); dark.putalpha(Image.eval(vig, lambda v: 170 - v * 170 // 255))
    can.alpha_composite(dark)
    ring(can, (330, 50, 650, 520))
    arrow(can, [(990, 470), (900, 260), (680, 250)])
    glow_text(can, (1240, 690), "HE WOULDN'T MOVE", 118, WHITE, (0, 0, 0), 10, 200, stroke=7, anchor="rd")
    return can.convert("RGB")

if __name__ == "__main__":
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        im = fn(); p = f"{OUT}/drummond_thumbnail_{k}.jpg"; im.save(p, quality=93); print(p, im.size)

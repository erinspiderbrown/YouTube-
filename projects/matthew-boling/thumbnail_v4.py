"""Thumbnails v4: real photos only (user, 10 Nov 2026), one full photo per thumbnail, no cutout layering.
Method (the FloTrack "Matt Boling 44.74" 7.4M-view look + pro sports grading): the whole frame is one real 6720px photo
(Wikimedia Commons, jenaragon94, CC BY 2.0), everything but Boling goes black-and-white and darker, Boling stays in full
colour with a red outline, one huge line of text with a single yellow keyword.
python3 -I thumbnail_v4.py FULL_DIR OUT_DIR   (FULL_DIR: ark1_full.jpg, ark2_full.jpg + *_mask.png from rembg at 2400x1600)
"""
import sys, os, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
D, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
YEL, RED, WHITE, BLACK = (255, 220, 0), (240, 30, 30), (255, 255, 255), (0, 0, 0)


def subject_mask(name, pick_x):
    """mask of the one person whose component covers x = pick_x (fraction of width)."""
    m = np.asarray(Image.open(f"{D}/{name}_mask.png").convert("L"))
    n, lab, st, _ = cv2.connectedComponentsWithStats((m > 100).astype(np.uint8))
    best = max(range(1, n), key=lambda k: (st[k, cv2.CC_STAT_AREA] if st[k, 0] <= pick_x * m.shape[1] <= st[k, 0] + st[k, 2] else 0))
    sel = np.where(lab == best, m, 0).astype(np.uint8)
    return Image.fromarray(sel)


def build(name, pick_x, crop, text_lines, out, arrow=None):
    im = Image.open(f"{D}/{name}.jpg").convert("RGB")
    m = subject_mask(name, pick_x).resize(im.size, Image.BICUBIC)
    im, m = im.crop(crop), m.crop(crop)
    im, m = im.resize((W, H), Image.LANCZOS), m.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    # background: black-and-white, darker, cool
    bg = ImageOps.grayscale(im).convert("RGB"); bg = ImageEnhance.Contrast(bg).enhance(1.25); bg = ImageEnhance.Brightness(bg).enhance(0.55)
    bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 20, 40)), 0.15)
    # subject: full colour, punchy
    fg = ImageEnhance.Contrast(im).enhance(1.18); fg = ImageEnhance.Color(fg).enhance(1.25); fg = ImageEnhance.Brightness(fg).enhance(1.08)
    fg = fg.filter(ImageFilter.UnsharpMask(1.5, 60, 2))
    out_im = bg.copy()
    # red outline + glow (dilated mask ring)
    a = np.asarray(m).astype(np.uint8)
    ring = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27)))
    glow = Image.fromarray(cv2.GaussianBlur(ring, (0, 0), 18))
    red = Image.new("RGB", (W, H), RED)
    out_im = Image.composite(red, out_im, glow.point(lambda v: int(v * 0.55)))
    out_im = Image.composite(red, out_im, Image.fromarray(ring))
    out_im = Image.composite(fg, out_im, m)
    # vignette
    y, x = np.mgrid[0:H, 0:W].astype(np.float32); v = 1 - 0.55 * (((x - W / 2) / (W / 1.7)) ** 2 + ((y - H / 2) / (H / 1.4)) ** 2)
    o = (np.asarray(out_im).astype(np.float32) * np.clip(v, 0.35, 1)[..., None]).clip(0, 255).astype(np.uint8)
    out_im = Image.fromarray(o).convert("RGBA")
    for (txt, col, size, xy, anchor) in text_lines:
        f = ImageFont.truetype(ANTON, size); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text(xy, txt, font=f, fill=col + (255,), anchor=anchor, stroke_width=max(8, size // 18), stroke_fill=BLACK + (255,))
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(14)))
        out_im.alpha_composite(sh, (6, 12)); out_im.alpha_composite(lay)
    if arrow:
        d = ImageDraw.Draw(out_im); (x0, y0), (mx, my), (x1, y1) = arrow
        P = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in [i / 40 for i in range(41)]]
        ang = math.atan2(y1 - P[-4][1], x1 - P[-4][0]); L = 80
        head = [(x1, y1), (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)), (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))]
        for c, w in ((BLACK, 36), (YEL, 22)):
            for p, q in zip(P, P[1:]): d.line([p, q], fill=c, width=w)
            d.polygon(head, fill=c)
    rgb = out_im.convert("RGB")
    rgb.save(f"{OUT}/{out}_HD.jpg", quality=95, subsampling=0)
    rgb.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{out}.jpg", quality=95, subsampling=0, optimize=True)


# A: mid-sprint, Boling (middle runner) in colour.  full width, 16:9 band
build("ark1_full", 0.62, (0, 220, 6720, 4000),
      [("THE NEXT", WHITE, 150, (60, 560), "la"), ("BOLT?", YEL, 270, (60, 715), "la")], "Q1_next_bolt_sprint")
# B: the start line, Boling the only one standing
build("ark2_full", 0.51, (840, 560, 5996, 3460),
      [("WHAT", WHITE, 190, (60, 300), "la"), ("HAPPENED?", YEL, 190, (W - 60, 300), "ra")], "Q2_only_one_standing")
print("ok")

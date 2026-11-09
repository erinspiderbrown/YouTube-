"""Thumbnails v4 (HD): same proven layouts as v3, rebuilt from full-resolution originals.
Rules from studying the 5M-34M view thumbnails at maxres: the photo is only ever DOWNscaled (never stretched),
light grading only (no heavy sharpening or saturation), tight crop with the face ~1/3 of the frame height.
python3 -I thumbnails_v4.py SCRATCH_DIR OUT_DIR
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
S = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
GREEN = (46, 230, 70); RED = (235, 30, 40); YEL = (255, 220, 0); WHITE = (255, 255, 255); BLACK = (0, 0, 0)


def grade(im, con=1.06, sat=1.08, bri=1.0):
    im = ImageEnhance.Contrast(im).enhance(con); im = ImageEnhance.Color(im).enhance(sat)
    return ImageEnhance.Brightness(im).enhance(bri)


def hd_crop(path, face_c, face_h, face_px, fx, fy):
    """Crop so the face (centre face_c, height face_h in source px) is face_px tall at (fx*W, fy*H). Downscale only."""
    im = Image.open(path).convert("RGB"); k = face_px / face_h
    assert k <= 1.0, f"{path}: would upscale x{k:.2f}"
    cw, ch = W / k, H / k; x0 = face_c[0] - fx * cw; y0 = face_c[1] - fy * ch
    x0 = max(0, min(im.width - cw, x0)); y0 = max(0, min(im.height - ch, y0))
    out = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    out = out.filter(ImageFilter.UnsharpMask(1.2, 40, 3))
    return grade(out), (x0, y0, k)


def vignette(im, strength=0.35):
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse([-W * 0.15, -H * 0.25, W * 1.15, H * 1.25], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * strength)))
    inv = m.point(lambda v: 255 - v); dark.putalpha(inv.point(lambda v: int(v * strength)))
    im.alpha_composite(dark)


def circ_mask(d, ss=4):
    m = Image.new("L", (d * ss, d * ss), 0); ImageDraw.Draw(m).ellipse([0, 0, d * ss - 1, d * ss - 1], fill=255)
    return m.resize((d, d), Image.LANCZOS)


def magnifier(im, target, tr, bubble, br, content, col=GREEN, width=14):
    ss = 3; lay = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    (x1, y1), (x2, y2) = target, bubble
    ang = math.atan2(y2 - y1, x2 - x1); dist = math.hypot(x2 - x1, y2 - y1)
    a = math.acos(max(-1, min(1, (tr - br) / dist)))
    for s in (1, -1):
        p1 = (x1 + tr * math.cos(ang + s * a), y1 + tr * math.sin(ang + s * a))
        p2 = (x2 + br * math.cos(ang + s * a), y2 + br * math.sin(ang + s * a))
        d.line([(p1[0] * ss, p1[1] * ss), (p2[0] * ss, p2[1] * ss)], fill=col + (255,), width=width * ss)
    d.ellipse([(x1 - tr) * ss, (y1 - tr) * ss, (x1 + tr) * ss, (y1 + tr) * ss], outline=col + (255,), width=width * ss)
    lay = lay.resize((W, H), Image.LANCZOS)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(8)).point(lambda v: v * 0.55))
    im.alpha_composite(sh, (3, 5)); im.alpha_composite(lay)
    D = 2 * br; m = circ_mask(D)
    shb = Image.new("RGBA", (D + 80, D + 80), (0, 0, 0, 0)); shb.paste((0, 0, 0, 160), (40, 40), m)
    im.alpha_composite(shb.filter(ImageFilter.GaussianBlur(20)), (x2 - br - 40 + 6, y2 - br - 40 + 12))
    c = ImageOps.fit(content.convert("RGB"), (D, D), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 30, 3))
    c = grade(c).convert("RGBA"); c.putalpha(m); im.alpha_composite(c, (x2 - br, y2 - br))
    ring = Image.new("RGBA", (D * ss, D * ss), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([0, 0, D * ss - 1, D * ss - 1], outline=col + (255,), width=int(width * 1.3) * ss)
    im.alpha_composite(ring.resize((D, D), Image.LANCZOS), (x2 - br, y2 - br))


def text(im, xy, s, size, fill, stroke=12, anchor="mm", font=ANTON):
    f = ImageFont.truetype(font, size); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,), anchor=anchor)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(12)))
    im.alpha_composite(sh, (5, 8)); im.alpha_composite(lay)


def save(im, name):
    rgb = im.convert("RGB")
    rgb.save(f"{OUT}/{name}_HD.jpg", quality=95, subsampling=0)
    rgb.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95, subsampling=0, optimize=True)


def src(p): return f"{S}/{p}"


# A: Sha'Carri, 2021 Olympic Trials win (jenaragon94, CC BY 2.0) + cannabis leaf
def sha():
    face = (3993, 525)
    im, (x0, y0, k) = hd_crop(src("hd/sha32.jpg"), face, 544, 390, 0.67, 0.34)
    im = im.convert("RGBA"); vignette(im, 0.3)
    mouth = (int((3993 - x0) * k), int((525 + 0.27 * 544 - y0) * k))
    magnifier(im, mouth, 62, (430, 400), 310, Image.open(src("leaf/leaf_1.jpg")))
    text(im, (430, 900), "BANNED", 200, YEL, 13)
    save(im, "A_shacarri_weed")


# B: Justin Gatlin, London 2012 100m final (Kent Capture, CC BY 2.0) + Depo-Testosterone vial
def gatlin():
    face = (2577, 765)
    im, (x0, y0, k) = hd_crop(src("hd/gat20.jpg"), face, 675, 360, 0.66, 0.34)
    im = im.convert("RGBA"); vignette(im, 0.3)
    arm = (int((2060 - x0) * k), int((1560 - y0) * k))
    vial = Image.open(src("src/Depo-testosterone crop.jpg")).convert("RGB").crop((0, 250, 1642, 1892))
    magnifier(im, arm, 62, (480, 400), 320, vial)
    text(im, (480, 905), "CAUGHT TWICE", 150, YEL, 12)
    save(im, "B_gatlin_testosterone")


# C: Marion Jones, Sydney 2000 podium (TSgt Rick Sforza, USAF, public domain) + syringe. Shown at 1:1, no upscaling.
def jones():
    p = Image.open(src("src/Marion Jones Sydney 2000.JPEG")).convert("RGB").filter(ImageFilter.UnsharpMask(1.0, 30, 3))
    p = grade(p, 1.05, 1.06)
    bg = p.crop((10, 10, 120, 300)).resize((1, 1), Image.BOX).getpixel((0, 0))
    im = Image.new("RGBA", (W, H), bg + (255,))
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    for x in range(W): gd.line([(x, 0), (x, H)], fill=int(110 * (1 - x / W)))
    im = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, g)
    px, py = W - p.width - 20, -30
    m = Image.new("L", p.size, 255); md = ImageDraw.Draw(m)
    for x in range(180): md.line([(x, 0), (x, p.height)], fill=int(255 * x / 180))
    im.paste(p, (px, py), m); vignette(im, 0.25)
    syr = Image.open(src("syr/Syringe_with_insulin_for_a_cat.jpg")).convert("RGB").crop((250, 230, 2600, 1010))
    syr = syr.rotate(28, expand=True, resample=Image.BICUBIC, fillcolor=(200, 140, 70))
    syr = syr.crop((int(syr.width * 0.24), int(syr.height * 0.2), int(syr.width * 0.8), int(syr.height * 0.8)))
    magnifier(im, (px + 390, py + 868), 70, (560, 430), 350, syr)
    text(im, (560, 930), "STRIPPED", 170, RED, 13)
    save(im, "C_jones_syringe")


# D: "every X explained" circle grid (EverythingProfessor 5.5M layout), real faces, light grading only
GRID = [  # (file, face box x,y,w,h or None for a pre-cropped square, label, ring colour)
    ("thumbs_v3/bj_16.jpg", (549, 133, 245, 324), "STANOZOLOL", (0, 170, 255)),
    ("src/Marion Jones Sydney 2000.JPEG", (303, 121, 189, 250), "THE CLEAR", (255, 200, 0)),
    ("hd/sha32.jpg", (3802, 253, 382, 544), "WEED", (40, 200, 70)),
    ("hd/gat20.jpg", (2335, 427, 484, 675), "TESTOSTERONE", (240, 40, 50)),
    ("faces/kiprop_africanews.jpg", None, "EPO", (160, 70, 255)),
    ("src/Krabbe Berlin 1988.jpg", (113, 183, 109, 137), "CLENBUTEROL", (255, 120, 0)),
    ("src/Elena Lashmanova London 2012.jpg", (582, 188, 270, 347), "GW1516", (0, 200, 200)),
    ("faces/chep_raw.jpg", (861, 96, 160, 174), "DIURETICS", (255, 80, 170)),
    ("faces/knighton_cgtn.jpg", None, "TRENBOLONE", (30, 90, 255)),
    ("hicks/hicks_9.jpg", (486, 210, 376, 552), "RAT POISON", (120, 120, 120)),
]


def face_circle(f, box, D, zoom=1.7):
    im = Image.open(src(f)).convert("RGB")
    if box:
        x, y, w, h = box; s = int(max(w, h) * zoom); cx, cy = x + w / 2, y + h / 2 + h * 0.12
        im = im.crop((int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2)))
    im = ImageOps.fit(im, (D, D), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 30, 3))
    im = grade(im, 1.05, 1.06).convert("RGBA"); im.putalpha(circ_mask(D)); return im


def grid():
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    ft = ImageFont.truetype(INTER, 112)
    parts = [("EVERY ", BLACK), ("BANNED", RED), (" DRUG IN TRACK", BLACK)]
    tw = sum(d.textlength(t, font=ft) for t, _ in parts); x = (W - tw) / 2
    for t, c in parts: d.text((x, 34), t, font=ft, fill=c + (255,)); x += d.textlength(t, font=ft)
    D = 285; ring = 12; fl = ImageFont.truetype(INTER, 42)
    xs = [W * (i + 0.5) / 5 for i in range(5)]
    for i, (f, box, lab, col) in enumerate(GRID):
        cx, cy = int(xs[i % 5]), 360 + (i // 5) * 425
        R = D // 2 + ring; dm = circ_mask(2 * R)
        cr = Image.new("RGBA", (2 * R, 2 * R), col + (255,)); cr.putalpha(dm)
        sh = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 80), (20, 20), dm)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (cx - R - 20 + 4, cy - R - 20 + 8))
        im.alpha_composite(cr, (cx - R, cy - R)); im.alpha_composite(face_circle(f, box, D), (cx - D // 2, cy - D // 2))
        d.text((cx, cy + R + 38), lab, font=fl, fill=BLACK + (255,), anchor="mm")
    save(im, "D_every_banned_grid")


if __name__ == "__main__":
    sha(); gatlin(); jones(); grid(); print("ok")

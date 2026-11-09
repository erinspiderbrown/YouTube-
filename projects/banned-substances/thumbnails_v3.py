"""Thumbnails v3: modelled on the niche's million-view thumbnails (studied 9 Nov 2026, see thumbnail_research.md, section 7).
H1/H2: one bright real photo + a green magnifier bubble on the evidence (BE AMAZED "Athletes Caught Cheating", 13M).
G1: white "every X explained" circle grid (EverythingProfessor 5.4M / 2.3M, catlover12 5.0M) with real faces.
python3 -I thumbnails_v3.py SCRATCH_DIR OUT_DIR
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1920, 1080
FONTS = "/home/user/YouTube-/tools/fonts"
ANTON = f"{FONTS}/Anton-Regular.ttf"
S = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
GREEN = (40, 255, 60); RED = (235, 30, 40); YEL = (255, 222, 0); WHITE = (255, 255, 255); BLACK = (0, 0, 0)


def pop(im, sharp=120, con=1.12, sat=1.18, bri=1.04):
    im = im.filter(ImageFilter.UnsharpMask(2, sharp, 2))
    im = ImageEnhance.Contrast(im).enhance(con); im = ImageEnhance.Color(im).enhance(sat)
    return ImageEnhance.Brightness(im).enhance(bri)


def circ_mask(d, ss=4):
    m = Image.new("L", (d * ss, d * ss), 0); ImageDraw.Draw(m).ellipse([0, 0, d * ss - 1, d * ss - 1], fill=255)
    return m.resize((d, d), Image.LANCZOS)


def magnifier(im, target, tr, bubble, br, content, col=GREEN, width=16):
    """Small ring on target, big bubble with content, joined by the two outer tangent lines."""
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
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 0.6))
    im.alpha_composite(sh, (4, 6)); im.alpha_composite(lay)
    # bubble: drop shadow, content, ring
    D = 2 * br; m = circ_mask(D)
    shb = Image.new("RGBA", (D + 80, D + 80), (0, 0, 0, 0)); shb.paste((0, 0, 0, 170), (40, 40), m)
    im.alpha_composite(shb.filter(ImageFilter.GaussianBlur(22)), (x2 - br - 40 + 8, y2 - br - 40 + 14))
    c = ImageOps.fit(content.convert("RGBA"), (D, D), Image.LANCZOS); c.putalpha(m)
    im.alpha_composite(c, (x2 - br, y2 - br))
    ring = Image.new("RGBA", (D * ss, D * ss), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([0, 0, D * ss - 1, D * ss - 1], outline=col + (255,), width=int(width * 1.4) * ss)
    im.alpha_composite(ring.resize((D, D), Image.LANCZOS), (x2 - br, y2 - br))


def text(im, xy, s, size, fill, stroke=14, anchor="mm", font=ANTON, rot=0):
    f = ImageFont.truetype(font, size); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,), anchor=anchor)
    if rot: lay = lay.rotate(rot, center=xy, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(14)))
    im.alpha_composite(sh, (6, 10)); im.alpha_composite(lay)


def save(im, name):
    im.convert("RGB").save(f"{OUT}/{name}_HD.jpg", quality=93)
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=92, optimize=True)


# ---------- H1: Ben Johnson in the blocks, Seoul 1988 + Winstrol zoom ----------
def h1():
    f = Image.open(f"{S}/thumbs_v3/bj_16.jpg").convert("RGB")       # 1280x720 with pillarbox 125..1165
    crop = f.crop((125, 0, 1165, 585))                               # 1040x585 = 16:9
    im = pop(crop.resize((W, H), Image.LANCZOS), sharp=170, con=1.18, sat=1.28, bri=1.12).convert("RGBA")
    pills = Image.open(f"{S}/src/Winstrol tablets.JPG").convert("RGB").crop((0, 330, 880, 1110))
    pills = pop(pills, 80, 1.1, 1.15)
    # ring on his upper arm (left of frame), bubble top-right
    magnifier(im, (1440, 810), 95, (1540, 330), 290, pills)
    text(im, (360, 900), "9.79", 300, YEL, 16)
    save(im, "H1_johnson_winstrol")


# ---------- H2: Marion Jones, Sydney 2000 gold + syringe zoom ----------
def h2():
    p = Image.open(f"{S}/src/Marion Jones Sydney 2000.JPEG").convert("RGB")
    k = 1.12; p = pop(p.resize((int(p.width * k), int(p.height * k)), Image.LANCZOS), 110, 1.1, 1.2, 1.05)
    bg_col = p.crop((10, 10, 120, 300)).resize((1, 1), Image.BOX).getpixel((0, 0))
    im = Image.new("RGBA", (W, H), bg_col + (255,))
    # soft stadium-dark gradient so the left side is not flat
    g = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(g)
    for x in range(W): gd.line([(x, 0), (x, H)], fill=int(90 * (1 - x / W)))
    im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), (0, 0)) if False else None
    im = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, g)
    px = W - p.width - 10
    m = Image.new("L", p.size, 255); md = ImageDraw.Draw(m)
    for x in range(160): md.line([(x, 0), (x, p.height)], fill=int(255 * x / 160))
    im.paste(p, (px, -40), m)
    syr = Image.open(f"{S}/syr/Syringe_with_insulin_for_a_cat.jpg").convert("RGB")
    syr = syr.crop((250, 230, 2600, 1010)).rotate(28, expand=True, resample=Image.BICUBIC, fillcolor=(200, 140, 70)); syr = syr.crop((int(syr.width*0.24), int(syr.height*0.2), int(syr.width*0.8), int(syr.height*0.8))); syr = pop(syr, 90, 1.15, 1.25, 1.1)
    medal = (px + int(390 * k), -40 + int(868 * k))
    magnifier(im, medal, 75, (500, 440), 360, syr)
    text(im, (500, 950), "STRIPPED", 170, RED, 14)
    save(im, "H2_jones_syringe")


# ---------- G1: "every X explained" circle grid, real faces + drug ----------
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
GRID = [  # (file, face box x,y,w,h, label, ring colour)
    ("thumbs_v3/bj_16.jpg", (549, 133, 245, 324), "STANOZOLOL", (0, 170, 255)),
    ("src/Marion Jones Sydney 2000.JPEG", (303, 121, 189, 250), "THE CLEAR", (255, 200, 0)),
    ("src/ShaCarri sq.jpg", (516, 174, 200, 278), "WEED", (40, 200, 70)),
    ("src/Justin Gatlin Rio 2016b-cr.jpg", (632, 171, 245, 331), "TESTOSTERONE", (240, 40, 50)),
    ("faces/kiprop_africanews.jpg", None, "EPO", (160, 70, 255)),
    ("src/Krabbe Berlin 1988.jpg", (113, 183, 109, 137), "CLENBUTEROL", (255, 120, 0)),
    ("src/Elena Lashmanova London 2012.jpg", (582, 188, 270, 347), "GW1516", (0, 200, 200)),
    ("faces/chep_raw.jpg", (861, 96, 160, 174), "DIURETICS", (255, 80, 170)),
    ("faces/knighton_cgtn.jpg", None, "TRENBOLONE", (30, 90, 255)),
    ("hicks/hicks_9.jpg", (486, 210, 376, 552), "RAT POISON", (120, 120, 120)),
]


def face_circle(f, box, D, zoom=1.75):
    im = Image.open(f"{S}/{f}").convert("RGB")
    if box:
        x, y, w, h = box; s = int(max(w, h) * zoom); cx, cy = x + w / 2, y + h / 2 + h * 0.12
        im = im.crop((int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2)))
    im = pop(ImageOps.fit(im, (D, D), Image.LANCZOS), 90, 1.08, 1.15, 1.05).convert("RGBA")
    im.putalpha(circ_mask(D)); return im


def g1():
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    ft = ImageFont.truetype(INTER, 112)
    parts = [("EVERY ", BLACK), ("BANNED", RED), (" DRUG IN TRACK", BLACK)]
    tw = sum(d.textlength(t, font=ft) for t, _ in parts); x = (W - tw) / 2
    for t, c in parts: d.text((x, 28), t, font=ft, fill=c + (255,)); x += d.textlength(t, font=ft)
    D = 270; ring = 12; fl = ImageFont.truetype(INTER, 40)
    xs = [W * (i + 0.5) / 5 for i in range(5)]
    for i, (f, box, lab, col) in enumerate(GRID):
        cx, cy = int(xs[i % 5]), 345 + (i // 5) * 415
        R = D // 2 + ring
        dm = circ_mask(2 * R); cr = Image.new("RGBA", (2 * R, 2 * R), col + (255,)); cr.putalpha(dm)
        sh = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (20, 20), dm)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (cx - R - 20 + 4, cy - R - 20 + 8))
        im.alpha_composite(cr, (cx - R, cy - R))
        im.alpha_composite(face_circle(f, box, D), (cx - D // 2, cy - D // 2))
        d.text((cx, cy + R + 36), lab, font=fl, fill=BLACK + (255,), anchor="mm")
    save(im, "G1_every_banned_grid")


# ---------- H3: Sha'Carri with the flag + weed leaf zoom ----------
def h3():
    p = Image.open(f"{S}/src/ShaCarri Budapest 2023.jpg").convert("RGB").crop((0, 0, 909, 511))
    im = pop(p.resize((W, H), Image.LANCZOS), 120, 1.1, 1.2, 1.05).convert("RGBA")
    leaf = Image.open(f"{S}/leaf/leaf_1.jpg").convert("RGB"); leaf = pop(leaf, 80, 1.12, 1.25, 1.05)
    k = W / 909; mouth = (int(545 * k), int(178 * k))
    magnifier(im, mouth, 62, (470, 420), 340, leaf)
    text(im, (470, 930), "BANNED", 190, YEL, 15)
    save(im, "H3_shacarri_weed")


h1(); h2(); h3(); g1(); print("ok")

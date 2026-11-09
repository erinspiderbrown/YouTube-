"""Split thumbnails (user's pick, 9 Nov 2026): athlete face on the left, the real drug in red light on the right,
one huge word. Real photos only (Wikimedia Commons; credits in thumbnail_credits.md).
python3 -I thumbnails_split.py SRC_DIR OUT_DIR
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
RED, WHITE, BLACK, YEL = (230, 25, 35), (255, 255, 255), (0, 0, 0), (255, 214, 0)
SRC = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)

def face_panel(f, box, head_px, cx_frac=0.36, cy=470):
    """Scale photo so the face box (x,y,w,h) is head_px tall, place face centre at (cx_frac*W, cy)."""
    im = Image.open(f"{SRC}/{f}").convert("RGB"); x, y, w, h = box
    k = head_px / h; im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(2, 80, 2)); im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.1)
    can = ImageOps.fit(im, (W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    can = ImageEnhance.Brightness(can).enhance(0.45)
    can.paste(im, (int(cx_frac * W - (x + w / 2) * k), int(cy - (y + h / 2) * k)))
    return can

def drug_panel(f, crop=None, scale=1.0):
    im = Image.open(f"{SRC}/{f}").convert("RGB")
    if crop: im = im.crop(crop)
    im = ImageOps.fit(im, (int(W * 0.55), H), Image.LANCZOS, centering=(0.5, 0.5))
    g = ImageOps.grayscale(im); g = ImageOps.autocontrast(g, cutoff=1)
    red = ImageOps.colorize(g, black=(8, 0, 0), mid=(170, 10, 15), white=(255, 210, 200))
    red = ImageEnhance.Contrast(red).enhance(1.25)
    return red

def huge(im, xy, s, size, fill, stroke=14, anchor="mm", rot=0):
    f = ImageFont.truetype(ANTON, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,), anchor=anchor)
    if rot: lay = lay.rotate(rot, center=xy, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(sh, (8, 12)); im.alpha_composite(lay)

def pill(im, cx, cy, s, size, bg, fg):
    f = ImageFont.truetype(ANTON, size); l, t, r, b = f.getbbox(s, anchor="mm")
    d = ImageDraw.Draw(im); pad = 26
    d.rectangle([cx + l - pad, cy + t - pad // 2 - 4, cx + r + pad, cy + b + pad // 2 + 4], fill=bg + (255,))
    d.text((cx, cy), s, font=f, fill=fg + (255,), anchor="mm")

def compose(face, drug, word, drug_label, tag, name):
    im = face.convert("RGBA")
    dx = int(W * 0.47)
    # diagonal split: drug panel on the right with a slanted edge
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon([(dx + 120, 0), (W, 0), (W, H), (dx - 60, H)], fill=255)
    right = Image.new("RGBA", (W, H)); right.paste(drug.convert("RGBA"), (W - drug.width, 0)); right.putalpha(mask)
    im.alpha_composite(right)
    d = ImageDraw.Draw(im); d.line([(dx + 120, 0), (dx - 60, H)], fill=RED + (255,), width=16)
    # dark vignette for type
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(v)
    for y in range(700, H): vd.line([(0, y), (W, y)], fill=(0, 0, 0, int(200 * (y - 700) / (H - 700))))
    im.alpha_composite(v)
    huge(im, (W // 2 + 40, H - 190), word, 330, YEL if word != "CAUGHT" else WHITE, 16)
    pill(im, int(W * 0.77), 110, drug_label, 70, RED, WHITE)
    pill(im, int(W * 0.17), 110, tag, 62, BLACK, WHITE)
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=92, optimize=True)

compose(face_panel("Justin Gatlin Rio 2016b-cr.jpg", (642, 177, 244, 313), 560),
        drug_panel("Depo-testosterone crop.jpg"), "CAUGHT", "TESTOSTERONE", "GATLIN '06", "S1_gatlin_testosterone")
compose(face_panel("ShaCarri sq.jpg", (516, 174, 200, 278), 560),
        drug_panel("Cannabis Closeup 01.jpg"), "BANNED", "THC", "SHA'CARRI '21", "S2_shacarri_thc")
compose(face_panel("Dwain Chambers 2008.jpg", (330, 180, 1200, 1500), 900, cx_frac=0.27, cy=520),
        drug_panel("Port Huron steroids.jpg", crop=(0, 600, 1920, 2900)), "CAUGHT", "\"THE CLEAR\"", "CHAMBERS '03", "S3_chambers_clear")
compose(face_panel("Ben Johnson 2017 (cropped).jpg", (163, 117, 272, 358), 560),
        drug_panel("Winstrol tablets.JPG"), "9.79", "STANOZOLOL", "BEN JOHNSON '88", "S4_johnson_winstrol")
print("ok")

"""House thumbnail template, copied from the user's own Boling thumbnail (10 Nov 2026):
examples/thumbnails/user_boling_what_happened.png. See examples/thumbnails/README.md for the rules.

Layout (1920x1080):
  - background: a real crowd/stadium photo, blurred (depth of field), bright, warm, light vignette
  - ACTION: the athlete's peak moment (cutout), upper-left/centre, ~70% frame height
  - FACE: big close-up of the same athlete (cutout), right side, head cropped at the top, ~55% of the width
  - TEXT: bottom-left, two lines of heavy italic sans: line 1 white, line 2 yellow->orange gradient, dark outline +
    drop shadow, red brush swoosh under line 2
Usage:
  python3 tools/thumb_template.py --bg BG.jpg --action ACTION.png --face FACE.png --l1 WHAT --l2 HAPPENED? --out OUT.jpg
  ACTION/FACE: RGBA cutouts (rembg isnet-general-use / birefnet-portrait). Real photos only; scale <= 1 where possible.
  Optional: --face-x 0.53 --face-h 1.08 --action-x 0.08 --action-y 0.0 --action-h 0.72 --bg-blur 7
"""
import argparse, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

W, H = 1920, 1080
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT = f"{FONTS}/Montserrat-BlackItalic.ttf"


def grade(c, con=1.1, col=1.15, bri=1.04, warm=0.04, sharp=True):
    a = c.split()[-1] if c.mode == "RGBA" else None; rgb = c.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(con); rgb = ImageEnhance.Color(rgb).enhance(col); rgb = ImageEnhance.Brightness(rgb).enhance(bri)
    if warm:
        r, g, b = rgb.split(); r = r.point(lambda v: min(255, int(v * (1 + warm)))); b = b.point(lambda v: int(v * (1 - warm))); rgb = Image.merge("RGB", (r, g, b))
    if sharp: rgb = rgb.filter(ImageFilter.UnsharpMask(1.6, 70, 2))
    if a: rgb.putalpha(a)
    return rgb


def background(path, blur):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    im = grade(im.filter(ImageFilter.GaussianBlur(blur)), 1.05, 1.1, 0.95, 0.03, False)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32); v = 1 - 0.45 * (((x - W * 0.55) / W) ** 2 + ((y - H / 2) / (H * 0.8)) ** 2)
    return Image.fromarray((np.asarray(im).astype(np.float32) * np.clip(v, 0.5, 1)[..., None]).clip(0, 255).astype(np.uint8)).convert("RGBA")


def place(im, c, cx, top, h, feather=2, shadow=0.45):
    c = c.crop(c.getbbox()); s = h / c.height; c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    a = c.split()[-1].filter(ImageFilter.GaussianBlur(feather)); c.putalpha(a)
    x = int(cx - c.width / 2)
    if shadow:
        sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(25)).point(lambda v: int(v * shadow)))
        im.alpha_composite(sh, (x + 18, int(top) + 16))
    im.alpha_composite(c, (x, int(top)))
    return x, int(top), c.size


def gradient_text(text, size, top_col, bot_col, outline=6):
    f = ImageFont.truetype(FONT, size); l, t, r, b = f.getbbox(text, stroke_width=outline); pad = 40
    w, h = r - l + 2 * pad, b - t + 2 * pad
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).text((pad - l, pad - t), text, font=f, fill=255)
    stroke = Image.new("L", (w, h), 0); ImageDraw.Draw(stroke).text((pad - l, pad - t), text, font=f, fill=255, stroke_width=outline, stroke_fill=255)
    g = Image.new("RGB", (w, h)); gd = ImageDraw.Draw(g)
    for yy in range(h):
        k = min(1, max(0, (yy - pad) / max(1, h - 2 * pad)))
        gd.line([(0, yy), (w, yy)], fill=tuple(int(top_col[i] * (1 - k) + bot_col[i] * k) for i in range(3)))
    out = Image.new("RGBA", (w, h), (20, 12, 8, 0)); out.putalpha(stroke)                       # dark outline
    fill = g.convert("RGBA"); fill.putalpha(mask); out.alpha_composite(fill)
    return out


def text_block(im, l1, l2, x=70, y_bottom=None):
    y_bottom = y_bottom or H - 90
    t2 = gradient_text(l2, 190, (255, 236, 90), (255, 150, 10))
    t1 = gradient_text(l1, 165, (255, 255, 255), (205, 205, 210))
    y2 = y_bottom - t2.height + 30; y1 = y2 - t1.height + 55
    for t, (xx, yy) in ((t1, (x, y1)), (t2, (x, y2))):
        sh = Image.new("RGBA", t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[-1].filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.85)))
        im.alpha_composite(sh, (xx + 8, yy + 14)); im.alpha_composite(t, (xx, yy))
    # red brush swoosh under line 2 (tapered)
    sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sw)
    x0, x1, yb = x + 40, x + t2.width - 30, y2 + t2.height - 32
    pts_top = [(x0 + (x1 - x0) * k, yb - 16 * math.sin(math.pi * k ** 0.8) - 6 * k) for k in [i / 30 for i in range(31)]]
    pts_bot = [(x0 + (x1 - x0) * k, yb + 4 + 14 * math.sin(math.pi * k ** 0.8) * (1 - 0.5 * k)) for k in [i / 30 for i in range(31)]][::-1]
    d.polygon(pts_top + pts_bot, fill=(226, 28, 34, 255))
    im.alpha_composite(sw.filter(ImageFilter.GaussianBlur(1.2)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True); ap.add_argument("--action", required=True); ap.add_argument("--face", required=True)
    ap.add_argument("--l1", default="WHAT"); ap.add_argument("--l2", default="HAPPENED?"); ap.add_argument("--out", required=True)
    ap.add_argument("--face-x", type=float, default=0.76); ap.add_argument("--face-h", type=float, default=1.0)
    ap.add_argument("--face-top", type=float, default=0.02)
    ap.add_argument("--action-x", type=float, default=0.30); ap.add_argument("--action-y", type=float, default=0.0); ap.add_argument("--action-h", type=float, default=0.72)
    ap.add_argument("--bg-blur", type=float, default=7)
    a = ap.parse_args()
    im = background(a.bg, a.bg_blur)
    place(im, grade(Image.open(a.action).convert("RGBA")), W * a.action_x, H * a.action_y, H * a.action_h)
    place(im, grade(Image.open(a.face).convert("RGBA"), 1.08, 1.12, 1.06), W * a.face_x, H * a.face_top, H * a.face_h)
    text_block(im, a.l1, a.l2)
    rgb = im.convert("RGB"); rgb.save(a.out.replace(".jpg", "_HD.jpg"), quality=95, subsampling=0)
    rgb.resize((1280, 720), Image.LANCZOS).save(a.out, quality=95, subsampling=0, optimize=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()

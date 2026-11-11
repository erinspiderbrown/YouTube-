"""Downfall thumbnail template (the user liked this format on 11 Nov 2026).
Copied from InternetJanitor's "The Satisfying Downfall of Ben Shapiro" (1.7M views in 2 days):
examples/satisfying_downfall_study.md.

Layout (1920x1080):
  - background: plain textured colour (default deep blue), darker at the edges
  - FACE: one huge front-on close-up of the subject, centred, head cropped at the top, chin/shoulders at the bottom
  - TEXT: 3 parts. A small white italic word left (HE), a giant red block word over the forehead (LOST),
    and a small white italic word right (EVERYTHING.) with a yellow marker underline.
Rules: a REAL photo or video frame of the subject with a sad, shocked or defeated face. Never paint on tears
or change the expression (that's a fabricated image of a real person).
Usage:
  python3 tools/thumb_downfall.py --face FACE.png --left HE --big LOST --right EVERYTHING. --out OUT.jpg
  FACE: an RGBA cutout (rembg birefnet-portrait) or a plain photo (then it's used as the full frame, no cutout).
  Optional: --bg-color 22,48,110  --face-h 1.25  --face-top -0.18  --face-x 0.5  --crop 0.2,0,0.85,0.8  --fade sides|bottom
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1920, 1080
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
BLOCK = f"{FONTS}/Anton-Regular.ttf"
ITAL = f"{FONTS}/Montserrat-BlackItalic.ttf"


def textured_bg(col):
    rng = np.random.default_rng(7)
    n = np.zeros((H, W), np.float32)
    for k, amp in ((96, 0.5), (24, 0.3), (6, 0.2)):  # mottled, painted-canvas look
        m = rng.normal(0, 1, (H // k + 1, W // k + 1)).astype(np.float32)
        m = np.asarray(Image.fromarray(((m * 40) + 128).clip(0, 255).astype(np.uint8)).resize((W + k, H + k), Image.BICUBIC)).astype(np.float32)[:H, :W]
        n += amp * (m / 128 - 1)
    fine = rng.normal(0, 1, (H, W)).astype(np.float32) * 0.04
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.55 * (((x - W / 2) / W) ** 2 * 2 + ((y - H / 2) / H) ** 2 * 1.5)
    base = np.array(col, np.float32)[None, None, :] * (1 + 0.22 * n[..., None] + fine[..., None]) * vig[..., None]
    return Image.fromarray(base.clip(0, 255).astype(np.uint8)).convert("RGBA")


def grade_face(c):
    a = c.split()[-1]; rgb = c.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.12); rgb = ImageEnhance.Color(rgb).enhance(1.08)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.05); rgb = rgb.filter(ImageFilter.UnsharpMask(2, 90, 2))
    rgb.putalpha(a); return rgb


def text_img(text, font, size, fill, stroke=0, stroke_col=(0, 0, 0)):
    f = ImageFont.truetype(font, size); l, t, r, b = f.getbbox(text, stroke_width=stroke); pad = 30
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_col)
    return im


def paste_shadow(im, t, xy, blur=14, op=0.75, off=(6, 10)):
    sh = Image.new("RGBA", t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[-1].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op)))
    im.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1])); im.alpha_composite(t, xy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--face", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--left", default="HE"); ap.add_argument("--big", default="LOST"); ap.add_argument("--right", default="EVERYTHING.")
    ap.add_argument("--bg-color", default="22,48,110"); ap.add_argument("--face-h", type=float, default=1.25)
    ap.add_argument("--face-top", type=float, default=-0.18); ap.add_argument("--face-x", type=float, default=0.5)
    ap.add_argument("--big-y", type=float, default=0.06)
    ap.add_argument("--crop", default="", help="x0,y0,x1,y1 in 0-1 of the cutout, to frame head+shoulders")
    ap.add_argument("--fade", default="sides", choices=["sides", "bottom", ""])
    a = ap.parse_args()
    im = textured_bg(tuple(int(v) for v in a.bg_color.split(",")))
    face = Image.open(a.face)
    if face.mode == "RGBA" and face.split()[-1].getextrema()[0] < 250:
        face = face.crop(face.getbbox())
        if a.crop:
            c = [float(v) for v in a.crop.split(",")]
            face = face.crop((int(c[0] * face.width), int(c[1] * face.height), int(c[2] * face.width), int(c[3] * face.height)))
        face = grade_face(face)
        s = H * a.face_h / face.height; face = face.resize((int(face.width * s), int(face.height * s)), Image.LANCZOS)
        al = face.split()[-1].filter(ImageFilter.GaussianBlur(2))
        x, y = int(W * a.face_x - face.width / 2), int(H * a.face_top)
        if a.fade:  # fade the cut edges of the body into the background (a line about 82% down the frame)
            yy = np.arange(face.height)[:, None] + y
            f = np.clip((H * 0.98 - yy) / (H * 0.16), 0, 1) if a.fade == "bottom" else 1
            xx = np.arange(face.width)[None, :]
            side = np.clip(np.minimum(xx, face.width - 1 - xx) / (face.width * 0.12), 0, 1)
            lower = np.clip((yy - (y + face.height * 0.55)) / (face.height * 0.2), 0, 1)
            g = np.minimum(f, 1 - lower * (1 - side))
            al = Image.fromarray((np.asarray(al).astype(np.float32) * g).astype(np.uint8))
        face.putalpha(al)
        glow = Image.new("RGBA", face.size, (0, 0, 0, 0)); glow.putalpha(al.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.6)))
        im.alpha_composite(glow, (x, y + 10)); im.alpha_composite(face, (x, y))
    else:  # a plain photo fills the frame
        face = face.convert("RGB"); s = max(W / face.width, H / face.height)
        face = face.resize((int(face.width * s) + 1, int(face.height * s) + 1), Image.LANCZOS)
        im = grade_face(face.crop((0, 0, W, H)).convert("RGBA"))
    big = text_img(a.big, BLOCK, 300, (235, 16, 22), 3, (120, 0, 0))
    bx, by = (W - big.width) // 2, int(H * a.big_y)
    paste_shadow(im, big, (bx, by), 18, 0.8, (8, 12))
    left = text_img(a.left, ITAL, 150, (255, 255, 255))
    paste_shadow(im, left, (max(30, bx - left.width - 30), by + int(big.height * 0.28)))
    right = text_img(a.right, ITAL, 82 if len(a.right) > 6 else 130, (255, 255, 255))
    rx = min(W - right.width - 10, bx + big.width + 10); ry = by + int(big.height * 0.38)
    paste_shadow(im, right, (rx, ry))
    # yellow marker underline, slightly uneven
    ul = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ul)
    x0, x1, yb = rx + 30, rx + right.width - 25, ry + right.height - 14
    d.polygon([(x0, yb - 7), (x1, yb - 10), (x1 + 4, yb + 6), (x0 - 2, yb + 9)], fill=(250, 222, 30, 255))
    im.alpha_composite(ul.filter(ImageFilter.GaussianBlur(1)))
    rgb = im.convert("RGB"); rgb.save(a.out.replace(".jpg", "_HD.jpg"), quality=95, subsampling=0)
    rgb.resize((1280, 720), Image.LANCZOS).save(a.out, quality=95, subsampling=0, optimize=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()

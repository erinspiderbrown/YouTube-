"""'One brutal number' before/after thumbnail (studied 11 Nov 2026: "TOTAL PLAYS IN NFL: 4", 1.25M views).
Left: the athlete at the peak (colour). Right: later (black-and-white, darker). A label + one giant number.
Real photos/frames only.
Usage:
  python3 tools/thumb_number.py --before B.png --after A.png --label "PRs SINCE AGE 16:" --num 0 \
      --btag "AGE 16 · 10.98" --out OUT.jpg [--bx 0.5 --by 0.4 --bz 1.6 --ax 0.6 --ay 0.4 --az 1.5]
  bx/by = centre of the crop in the before frame (0-1), bz = zoom; same for after.
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W, H = 1920, 1080
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
ITAL = f"{FONTS}/Montserrat-BlackItalic.ttf"; BLOCK = f"{FONTS}/Anton-Regular.ttf"


def panel(path, cx, cy, z, w, h, bw=False):
    im = Image.open(path).convert("RGB"); s = max(w / im.width, h / im.height) * z
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x0 = int(min(max(0, cx * im.width - w / 2), im.width - w)); y0 = int(min(max(0, cy * im.height - h / 2), im.height - h))
    p = im.crop((x0, y0, x0 + w, y0 + h)).filter(ImageFilter.UnsharpMask(2, 80, 2))
    if bw:
        p = ImageEnhance.Contrast(ImageOps.grayscale(p).convert("RGB")).enhance(1.25); p = ImageEnhance.Brightness(p).enhance(0.85)
    else:
        p = ImageEnhance.Color(ImageEnhance.Contrast(p).enhance(1.12)).enhance(1.2)
    return p


def text(t, font, size, fill, stroke=10, sc=(0, 0, 0)):
    f = ImageFont.truetype(font, int(size)); l, tp, r, b = f.getbbox(t, stroke_width=stroke); pad = 30
    im = Image.new("RGBA", (r - l + 2 * pad, b - tp + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - tp), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc)
    return im


def shadow(im, t, xy, blur=16, op=0.8):
    sh = Image.new("RGBA", t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[-1].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op)))
    im.alpha_composite(sh, (xy[0] + 8, xy[1] + 12)); im.alpha_composite(t, xy)


def main():
    ap = argparse.ArgumentParser()
    for k in ("before", "after", "label", "num", "out"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--btag", default=""); ap.add_argument("--atag", default="")
    for k, d in (("bx", .5), ("by", .4), ("bz", 1.0), ("ax", .5), ("ay", .4), ("az", 1.0)): ap.add_argument("--" + k, type=float, default=d)
    a = ap.parse_args()
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    L = panel(a.before, a.bx, a.by, a.bz, 1010, H); R = panel(a.after, a.ax, a.ay, a.az, 1010, H, bw=True)
    im.paste(L, (0, 0))
    m = Image.new("L", (1010, H), 0); ImageDraw.Draw(m).polygon([(90, 0), (1010, 0), (1010, H), (0, H)], fill=255)
    im.paste(R, (910, 0), m)
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sl)
    d.polygon([(990, 0), (1012, 0), (922, H), (900, H)], fill=(255, 255, 255, 255))
    im.alpha_composite(sl)
    # bottom gradient so the text reads
    g = np.zeros((H, W), np.uint8); g[int(H * .55):] = np.linspace(0, 200, H - int(H * .55)).astype(np.uint8)[:, None]
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 255)); dark.putalpha(Image.fromarray(g)); im.alpha_composite(dark)
    lab = text(a.label, ITAL, 112, (255, 255, 255), 9)
    num = text(a.num, BLOCK, 620, (255, 214, 0), 16)
    shadow(im, lab, (60, H - lab.height - 40))
    shadow(im, num, (W - num.width - 40, H - num.height + 70), 24, 0.9)
    for tag, x in ((a.btag, 60), (a.atag, 1010)):
        if not tag: continue
        t = text(tag, ITAL, 60, (20, 20, 20), 0); bx = Image.new("RGBA", (t.width - 20, t.height - 30), (255, 255, 255, 240))
        bx.alpha_composite(t, (-10, -15)); shadow(im, bx, (x, 50), 10, 0.5)
    rgb = im.convert("RGB"); rgb.save(a.out.replace(".jpg", "_HD.jpg"), quality=95)
    rgb.resize((1280, 720), Image.LANCZOS).save(a.out, quality=95, optimize=True); print("wrote", a.out)


if __name__ == "__main__":
    main()

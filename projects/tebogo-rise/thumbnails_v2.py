"""HD thumbnails, round 2, modelled on the million-view thumbnails in the niche (see thumbnail_research.md, round 2):
- F "hero": Olympics' "BOLT / THE FASTEST MAN ALIVE" (8.4M): one big real photo on dark, giant one-word name,
  gold rule, one short subtitle. Face = 4K Commons portrait (Douala 2024, CC0).
- G "collage": "The Rise and Fall of Sha'Carri Richardson" (464K, 32x) and Olympics' "Letsile Tebogo wins gold" (1.2M):
  big sharp centre face, flag moments either side, name across the bottom.
Run: python3 -I projects/tebogo-rise/thumbnails_v2.py OUTDIR
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import thumbnails as T

W, H = T.W, T.H
SRC = T.SRC_DIR

def hd_face(scale_head_px, cx, cy):
    """Douala portrait (3840 px) scaled so the head is scale_head_px tall, face centre at canvas (cx, cy)."""
    im = Image.open(f"{SRC}/douala_crop.jpg").convert("RGB")
    fx, fy, fh = 0.484 * im.width, 0.225 * im.height, 0.24 * im.height
    k = scale_head_px / fh
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(1.08); im = T.golden(im, 0.18)
    return im, (int(cx - fx * k), int(cy - fy * k))

def F_hero(OUT):
    im = Image.new("RGBA", (W, H), (10, 8, 6, 255))
    face, xy = hd_face(560, 1360, 400)
    im.paste(face, xy)
    T.hgrad(im, 0, 1180, 250, 0)          # dark left for type
    T.vgrad(im, 760, H, 0, 200)           # dark bottom
    T.vignette(im, 120)
    T.text(im, (90, 170), "THE RISE OF", 92, T.WHITE, stroke=0, anchor="lm", shadow=10)
    T.text(im, (78, 410), "TEBOGO", 330, T.WHITE, stroke=0, anchor="lm", shadow=18)
    d = ImageDraw.Draw(im); d.rectangle([90, 600, 900, 618], fill=T.GOLD + (255,))
    T.gold_text(im, (88, 715), "AFRICA'S FIRST", 150, stroke=8, anchor="lm")
    T.text(im, (92, 860), "OLYMPIC 200M CHAMPION", 92, T.WHITE, stroke=0, anchor="lm", shadow=10)
    T.flag_stripe_v(im, 40, 22)
    T.save(im, OUT, "F_hero_HD")

def side_panel(name, w, fx, fy, head_px):
    im = Image.open(f"{SRC}/{name}").convert("RGB")
    k = head_px / (0.16 * im.height) if name.startswith("nai") else head_px / (0.2 * im.height)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    cx, cy = fx * im.width, fy * im.height
    top = max(0, min(im.height - H, int(cy - H * 0.38))); left = max(0, min(im.width - w, int(cx - w / 2)))
    box = (left, top, left + w, top + H)
    p = im.crop(box); p = T.golden(p, 0.22); p = ImageEnhance.Brightness(p).enhance(0.85)
    return p

def G_collage(OUT):
    im = Image.new("RGBA", (W, H), (10, 8, 6, 255))
    L = side_panel("nai_22.0.png", 760, 0.498, 0.35, 230)      # Nairobi 2021, age 18, with the flag
    R = side_panel("paris_flag.png", 760, 0.50, 0.30, 230)     # Paris 2024 gold, with the flag
    im.paste(L, (0, 0)); im.paste(R, (W - 760, 0))
    face, xy = hd_face(600, W // 2, 360)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle([560, 0, W - 560, H], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(90))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layer.paste(face, xy); layer.putalpha(mask)
    im.alpha_composite(layer)
    T.vgrad(im, 640, H, 0, 235)
    T.vignette(im, 110)
    T.pill(im, 330, 120, "18 · WORLD U20 CHAMP", 54, T.BLUE, T.BLACK)
    T.pill(im, W - 330, 120, "21 · OLYMPIC GOLD", 54, T.GOLD, T.BLACK)
    T.text(im, (W // 2, 790), "THE RISE OF", 96, T.WHITE, stroke=0, shadow=12)
    T.gold_text(im, (W // 2, 935), "LETSILE TEBOGO", 200, stroke=9)
    T.weave_band(im, H - 40, 40)
    T.save(im, OUT, "G_collage_HD")

if __name__ == "__main__":
    OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
    F_hero(OUT); G_collage(OUT); print("done")

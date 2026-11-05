"""Oscar Pistorius thumbnail v1, in the style the user approved for Drummond (thumbnail_v4.py):
HD real frames, subject cut out on a dark background, one proof element, 2-4 huge words.

Sources (all real, imported via vidIQ, see credits.md):
- Hero: 1080p Eyewitness News courtroom frame of Pistorius in a suit (ewn_due_release @ 74 s).
  Cropped above the burned-in subtitles, cut out with BiRefNet-portrait (rembg) -> thumb/src/cut_hero.png.
- Proof: London 2012 Olympic stadium frame, Pistorius on the track with his name bib and blades
  (itn_400semi_qual @ 26 s), as a white-bordered photo card labelled "LONDON 2012".
- Respectful of Reeva Steenkamp: she is not used as thumbnail bait, no weapon, door or crime-scene imagery.
Rendered at 2560x1440, saved at 1280x720.
Run: python3 -I projects/oscar-pistorius/thumbnail_v1.py
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
sys.path.insert(0, "/home/user/YouTube-/projects/jon-drummond")
from thumbnail_v4 import F, cover, grade, glow_layer, drop_shadow, photo_card, arrow, headline, RED, YEL, WHITE, W, H

SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad"
SRC = f"{SCR}/thumb/src"
OUT = f"{SCR}/thumb"

def backdrop():
    st = Image.open(f"{SRC}/c6.png").convert("RGB")     # the Olympic stadium itself, blurred to mood
    bg = cover(st, (W, H), 0.5, 0.3).filter(ImageFilter.GaussianBlur(16))
    a = np.asarray(ImageEnhance.Color(bg).enhance(0.35), np.float32) * 0.22
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a += np.exp(-(((xx - 1850) / 760) ** 2 + ((yy - 700) / 620) ** 2))[..., None] * np.array([170, 18, 22])   # red behind him
    a += np.exp(-(((xx - 350) / 900) ** 2 + ((yy - 250) / 700) ** 2))[..., None] * np.array([8, 34, 105])     # cold blue left
    ang = np.arctan2(yy + 260, xx - 1900)
    rays = (0.5 + 0.5 * np.sin(ang * 24)) ** 6 * np.clip(1 - np.hypot(xx - 1900, yy + 260) / 2300, 0, 1)
    a += rays[..., None] * np.array([70, 22, 20])
    vig = 1 - 0.55 * np.clip(((xx - W * 0.6) / (W * 0.7)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2, 0, 1)
    a *= vig[..., None]
    a += np.random.default_rng(3).normal(0, 5, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def hero(scale):
    cut = Image.open(f"{SRC}/cut_hero.png").convert("RGBA").crop((700, 0, 1920, 880))
    rgb = grade(cut, 1.12, 1.08, 120)
    A = np.asarray(cut.split()[-1].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8)), np.float32)
    ys = np.arange(cut.height, dtype=np.float32)[:, None]
    A *= np.clip((cut.height - 1 - ys) / 140, 0, 1)            # fade the cropped chest into the dark
    im = rgb.convert("RGBA"); im.putalpha(Image.fromarray(A.astype(np.uint8)))
    er = im.split()[-1].filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(4))
    edge = np.clip((np.asarray(im.split()[-1], np.float32) - np.asarray(er, np.float32)) / 255, 0, 1)[..., None]
    px = np.asarray(im.convert("RGB"), np.float32)
    px = px * (1 - edge * 0.5) + np.array([255, 110, 90]) * edge * 0.5     # warm red rim light
    out = Image.fromarray(np.clip(px, 0, 255).astype(np.uint8)).convert("RGBA"); out.putalpha(im.split()[-1])
    return out.resize((round(out.width * scale), round(out.height * scale)), Image.LANCZOS)

def build(lines):
    can = backdrop()
    S = 1.22
    hr = hero(S)
    hx, hy = W - hr.width + 40, H - hr.height + 10
    drop_shadow(can, hr, (hx, hy), off=(-30, 20), blur=40, a=210)
    can.alpha_composite(hr, (hx, hy))
    # proof: Pistorius on the Olympic track, London 2012
    ol = Image.open(f"{SRC}/c6.png").convert("RGB").crop((300, 0, 1060, 700))
    pc = photo_card(ol, 640, 590, -4, label="LONDON 2012")
    px_, py_ = 120, H - pc.height - 50
    drop_shadow(can, pc, (px_, py_), off=(12, 26), blur=30, a=220)
    can.alpha_composite(pc, (px_, py_))
    tr, tm = headline(can, lines, 90, 60)
    arrow(can, (px_ + pc.width - 30, py_ + 230), (hx + 175, hy + 640), bend=-0.22)
    out = ImageEnhance.Contrast(can.convert("RGB")).enhance(1.04)
    g = np.random.default_rng(9).normal(0, 3.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))

VARIANTS = {
    "A": [("OLYMPIAN", 300, WHITE), ("TO MURDERER", 250, RED)],
    "B": [("HERO TO", 300, WHITE), ("PRISONER", 330, YEL)],
}

if __name__ == "__main__":
    for k, lines in VARIANTS.items():
        im = build(lines)
        im.save(f"{OUT}/pistorius_thumb_v1_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/pistorius_thumb_v1_{k}.jpg", quality=94)
        print(k)

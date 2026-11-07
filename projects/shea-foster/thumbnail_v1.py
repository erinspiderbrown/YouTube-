"""Shea Foster thumbnails in the published Drummond style (see CLAUDE.md): one real frame full-bleed,
a short white black-italic statement with a period top-left, one real photo inset in a white border bottom-left.

Sources (real):
- Main: Foster sit-down interview, NGTF "By The Grace of God" ep. 1 (2024) @ 35 s, pushed down so the text clears his face.
- Inset A/C: the 2021 Oklahoma State NCAA XC podium photo (user's Dropbox 20.jpg), every face except Foster's blurred.
- Inset B: the hospital photo after the June 2021 crash (user's Dropbox 13.webp).
Run: python3 -I projects/shea-foster/thumbnail_v1.py
"""
import importlib.util
import numpy as np
from PIL import Image

T = importlib.util.spec_from_file_location("t2", "/home/user/YouTube-/projects/oscar-pistorius/thumbnail_v2.py")
t2 = importlib.util.module_from_spec(T); T.loader.exec_module(t2)
SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad/shea"
t2.SRC = f"{SCR}/thumb"
W, H = t2.W, t2.H


def build(main, box, lines, inset_path, inset_crop, inset_w, size=270, maxw=1250, pad=250):
    can = t2.main_image(main, box, pad)
    t2.headline(can, lines, 110, 80, size, maxw)
    ins = t2.inset(inset_path, inset_crop, inset_w)
    x, y = 120, H - ins.height - 80
    t2.shadow(can, ins, (x, y))
    can.alpha_composite(ins, (x, y))
    out = can.convert("RGB")
    g = np.random.default_rng(9).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))


def spotlight_inset(width, label="OKLAHOMA STATE \u00b7 3RD AT 2021 NCAA XC", border=10):
    """The 2021 OSU podium photo (Dropbox 21.jpg), faces unblurred, Foster the bright spot, school name on the frame."""
    from PIL import ImageDraw, ImageFont, ImageFilter, ImageEnhance
    ph = Image.open(f"{SCR}/dropbox/21.jpg").convert("RGB").crop((330, 170, 1190, 690))
    ph = t2.grade(ph, 1.08, 1.12, 70)
    dim = ImageEnhance.Brightness(ImageEnhance.Color(ph).enhance(0.55)).enhance(0.55)
    m = Image.new("L", ph.size, 0)
    ImageDraw.Draw(m).ellipse([350 - 20, -10, 490 + 20, 530], fill=255)   # Foster: x 680-800 incl. raised trophy
    m = m.filter(ImageFilter.GaussianBlur(14))
    ph = Image.composite(ph, dim, m)
    h = round(width * ph.height / ph.width)
    ph = ph.resize((width, h), Image.LANCZOS)
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", max(28, width // 22))
    band = int(f.size * 1.7)
    card = Image.new("RGBA", (width + 2 * border, h + border + band), (255, 255, 255, 255))
    card.paste(ph, (border, border))
    d = ImageDraw.Draw(card)
    d.text(((card.width - f.getlength(label)) / 2, h + border + (band - f.size) / 2 - 4), label, font=f, fill=(20, 20, 24, 255))
    return card


def build_spot(main, box, lines, inset_w, size=270, maxw=1250, pad=250):
    can = t2.main_image(main, box, pad)
    t2.headline(can, lines, 110, 80, size, maxw)
    ins = spotlight_inset(inset_w)
    x, y = 110, H - ins.height - 70
    t2.shadow(can, ins, (x, y))
    can.alpha_composite(ins, (x, y))
    out = can.convert("RGB")
    g = np.random.default_rng(9).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))


TEAM = (f"{SCR}/assets/team20_foster.png", (560, 230, 1060, 560), 820)
HOSP = (f"{SCR}/dropbox/13.webp", (200, 250, 1247, 1100), 640)
VARIANTS = {
    "A": ("n35", (0, 0, 1920, 1080), ["HIS TEAMMATES", "KNEW."], TEAM),
    "B": ("n35", (0, 0, 1920, 1080), ["BANNED", "4 YEARS."], HOSP),
    "C": ("n35", (0, 0, 1920, 1080), ["NOBODY", "SAID A WORD."], TEAM),
}

if __name__ == "__main__":
    for k, (main, box, lines, (ip, ic, iw)) in VARIANTS.items():
        im = build(main, box, lines, ip, ic, iw)
        im.save(f"{SCR}/thumb/shea_thumb_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{SCR}/thumb/shea_thumb_{k}.jpg", quality=94)
        print(k)
    im = build_spot("n35", (0, 0, 1920, 1080), ["HIS TEAMMATES", "KNEW."], 1000)
    im.save(f"{SCR}/thumb/shea_thumb_A2_full.png")
    im.resize((1280, 720), Image.LANCZOS).save(f"{SCR}/thumb/shea_thumb_A2.jpg", quality=94)
    print("A2")

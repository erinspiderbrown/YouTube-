"""Shea Foster thumbnails v3: built from a study of million-view thumbnails in the niche (7 Nov 2026).

What the top performers share:
- JxmyHighroller (19.8M / 7.8M views): one real moment, full frame, and a red arrow singling out one person in a group.
- Nicki Swift "Marion Jones" (2.2M): a real photo with a circled detail that makes you look.
- Cycling-scandal hits: 2-4 word all-caps statements with one coloured keyword.
- One focal point, high contrast, readable on a phone at 160 px wide.

Variants (2560x1440):
  T1 "WHO'S DOPING?"   full-frame OSU podium photo, every face visible: the cold-open guessing game. Pairs with the title
                       "Who's Doping In This Photo? (You Picked Wrong)".
  T2 "IT WAS HIM."     the same photo, Foster circled in red with a red arrow (Jxmy-style call-out).
  T3 "HIS TEAMMATES KNEW."  upgraded A2: bigger face, yellow keyword, the inset circles Foster.
  T4 "PARALYZED → BANNED."  hospital bed vs. his OSU photo, the story arc in one look.
Run: python3 -I projects/shea-foster/thumbnail_v3.py
"""
import importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

T = importlib.util.spec_from_file_location("t2", "/home/user/YouTube-/projects/oscar-pistorius/thumbnail_v2.py")
t2 = importlib.util.module_from_spec(T); T.loader.exec_module(t2)
SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad/shea"
OUT = "/home/user/YouTube-/projects/shea-foster/out"
W, H = 2560, 1440
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"
YELLOW, RED, WHITE = (255, 214, 0, 255), (235, 30, 35, 255), (255, 255, 255, 255)
TEAM = f"{SCR}/dropbox/21.jpg"
TEAM_CROP = (0, 110, 1206, 788)          # 16:9 out of the 1206x796 photo
FOSTER_FACE = (746, 353)                 # in the original photo (SFace match 0.69)


def team_full(spot=False):
    im = Image.open(TEAM).convert("RGB").crop(TEAM_CROP)
    s = W / im.width
    im = im.resize((W, H), Image.LANCZOS)
    im = t2.grade(im, 1.12, 1.15, 110)
    fx, fy = FOSTER_FACE[0] * s, (FOSTER_FACE[1] - TEAM_CROP[1]) * s
    if spot:   # everyone else a touch darker, Foster stays bright
        dim = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.7)).enhance(0.62)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse([fx - 210, fy - 420, fx + 210, fy + 900], fill=255)
        im = Image.composite(im, dim, m.filter(ImageFilter.GaussianBlur(40)))
    a = np.asarray(im, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    a *= 1 - 0.55 * np.clip(1 - yy / 420, 0, 1)          # darker ceiling band for the words
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA"), (fx, fy)


def words(can, parts, x, y, size, center=False):
    """parts: list of (text, colour) on one line."""
    f = ImageFont.truetype(FONT, size)
    total = sum(f.getlength(t) for t, _ in parts)
    if center:
        x = (W - total) / 2
    lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bb = f.getbbox(parts[0][0])
    for t, c in parts:
        d.text((x, y - bb[1]), t, font=f, fill=c, stroke_width=max(4, size // 40), stroke_fill=(0, 0, 0, 255))
        x += f.getlength(t)
    t2.shadow(can, lay, (0, 0), off=(0, 12), blur=22, a=200)
    can.alpha_composite(lay)


def ring(can, cx, cy, rx, ry, width=18):
    lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=RED, width=width)
    t2.shadow(can, lay, (0, 0), off=(0, 6), blur=10, a=170)
    can.alpha_composite(lay)


def arrow(can, x0, y0, x1, y1, width=26):
    lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line([(x0, y0), (x1, y1)], fill=RED, width=width)
    ang = np.arctan2(y1 - y0, x1 - x0); L = 90
    for s in (-1, 1):
        a2 = ang + np.pi + s * 0.5
        d.line([(x1, y1), (x1 + L * np.cos(a2), y1 + L * np.sin(a2))], fill=RED, width=width)
    d.ellipse([x1 - width / 2, y1 - width / 2, x1 + width / 2, y1 + width / 2], fill=RED)
    t2.shadow(can, lay, (0, 0), off=(0, 6), blur=10, a=170)
    can.alpha_composite(lay)


def finish(can, name):
    im = can.convert("RGB")
    g = np.random.default_rng(9).normal(0, 2.2, (H, W, 1))
    im = Image.fromarray(np.clip(np.asarray(im, np.float32) + g, 0, 255).astype(np.uint8))
    im.save(f"{SCR}/thumb/{name}_full.png")
    im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=93)
    return name


def t1():
    can, _ = team_full()
    words(can, [("WHO'S ", WHITE), ("DOPING?", YELLOW)], 0, 70, 250, center=True)
    return finish(can, "shea_thumb_v3_T1_whos_doping")


def t2_him():
    can, (fx, fy) = team_full(spot=True)
    words(can, [("IT WAS ", WHITE), ("HIM.", YELLOW)], 0, 70, 250, center=True)
    ring(can, fx, fy + 20, 165, 205)
    arrow(can, fx + 430, fy - 250, fx + 175, fy - 95)   # from under "HIM." down to the ring, clear of the teammates
    return finish(can, "shea_thumb_v3_T2_it_was_him")


def t3():
    t2.SRC = f"{SCR}/thumb"
    can = t2.main_image("n35", (240, 0, 1920, 945), 0)     # tighter on his face
    lay_parts = [("HIS TEAMMATES", [("HIS TEAMMATES", WHITE)]), ("KNEW.", [("KNEW.", YELLOW)])]
    y = 80
    for _, parts in lay_parts:
        words(can, parts, 110, y, 260)
        y += 255
    ph = Image.open(TEAM).convert("RGB").crop((330, 170, 1190, 690))
    ph = t2.grade(ph, 1.10, 1.15, 70)
    dim = ImageEnhance.Brightness(ImageEnhance.Color(ph).enhance(0.6)).enhance(0.6)
    m = Image.new("L", ph.size, 0)
    ImageDraw.Draw(m).ellipse([330, -10, 510, 530], fill=255)
    ph = Image.composite(ph, dim, m.filter(ImageFilter.GaussianBlur(14)))
    wpx = 1060
    ph = ph.resize((wpx, round(wpx * ph.height / ph.width)), Image.LANCZOS)
    dd = ImageDraw.Draw(ph)
    sx = wpx / 860
    cx, cy = (746 - 330) * sx, (353 - 170) * sx
    dd.ellipse([cx - 62, cy - 74, cx + 62, cy + 80], outline=RED[:3], width=9)
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 46)
    band = 80
    card = Image.new("RGBA", (wpx + 20, ph.height + 10 + band), (255, 255, 255, 255))
    card.paste(ph, (10, 10))
    lab = "OKLAHOMA STATE · 3RD AT 2021 NCAA XC"
    ImageDraw.Draw(card).text(((card.width - f.getlength(lab)) / 2, ph.height + 10 + 14), lab, font=f, fill=(20, 20, 24))
    x, y = 100, H - card.height - 60
    t2.shadow(can, card, (x, y))
    can.alpha_composite(card, (x, y))
    return finish(can, "shea_thumb_v3_T3_teammates_knew")


def t4():
    can = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    left = Image.open(f"{SCR}/dropbox/13.webp").convert("RGB")
    lw = W // 2
    s = max(lw / left.width, H / left.height)
    left = left.resize((int(left.width * s), int(left.height * s)), Image.LANCZOS)
    left = left.crop(((left.width - lw) // 2, int(left.height * 0.12), (left.width - lw) // 2 + lw, int(left.height * 0.12) + H))
    right = Image.open(f"{SCR}/assets/ng_osu.png").convert("RGB").crop((420, 0, 1500, 1080))
    right = right.resize((lw, int(lw * right.height / right.width)), Image.LANCZOS)
    right = right.crop((0, (right.height - H) // 2, lw, (right.height - H) // 2 + H))
    right = ImageEnhance.Color(right).enhance(0.0)                    # banned side in black & white
    can.paste(t2.grade(left, 1.08, 1.0, 80), (0, 0)); can.paste(t2.grade(right, 1.15, 1.0, 80), (lw, 0))
    a = np.asarray(can.convert("RGB"), np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    a *= 1 - 0.6 * np.clip((yy - 950) / 490, 0, 1)
    can = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    ImageDraw.Draw(can).rectangle([lw - 6, 0, lw + 6, H], fill=WHITE)
    f = ImageFont.truetype(FONT, 210)
    for txt, col, cx in (("PARALYZED", WHITE, lw / 2), ("BANNED.", RED, lw + lw / 2)):
        lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((cx - f.getlength(txt) / 2, 1160), txt, font=f, fill=col, stroke_width=6, stroke_fill=(0, 0, 0, 255))
        t2.shadow(can, lay, (0, 0), off=(0, 10), blur=18, a=200)
        can.alpha_composite(lay)
    return finish(can, "shea_thumb_v3_T4_paralyzed_banned")


if __name__ == "__main__":
    for fn in (t1, t2_him, t3, t4):
        print(fn())

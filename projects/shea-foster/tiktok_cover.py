"""TikTok cover (1080x1920) for the Shea Foster video, in the same style as the YouTube thumbnail A.

Layout:
- Foster's 2024 interview frame, sharp and full height, pushed down so the face sits mid-frame.
- The strip above it is a blurred, darkened extension of the same frame, so there's no black anywhere (user rule).
- White black-italic headline with a period at the top.
- One real inset photo in a white border at the bottom left: the 2021 OSU podium, every face but Foster's blurred.
- Everything important sits inside the centre 3:4 area that TikTok's profile grid shows.
Run: python3 -I projects/shea-foster/tiktok_cover.py
"""
import importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

T = importlib.util.spec_from_file_location("t2", "/home/user/YouTube-/projects/oscar-pistorius/thumbnail_v2.py")
t2 = importlib.util.module_from_spec(T); T.loader.exec_module(t2)
SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad/shea"
W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"
SHIFT = 300          # push the sharp frame down by this much


def base():
    fr = Image.open(f"{SCR}/thumb/n35.png").convert("RGB")
    cw = round(1080 * 9 / 16)                      # 9:16 crop around the face (face centre x ≈ 960)
    crop = fr.crop((960 - cw // 2, 0, 960 + cw // 2, 1080)).resize((W, H), Image.LANCZOS)
    crop = t2.grade(crop, 1.10, 1.08, 120)
    bg = crop.resize((W // 10, H // 10)).filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR)
    bg = ImageEnhance.Brightness(bg).enhance(0.5)
    can = bg.copy()
    sharp = crop.crop((0, 0, W, H - SHIFT))
    mask = Image.new("L", sharp.size, 255)
    grad = np.clip(np.arange(sharp.height) / 160.0, 0, 1)[:, None] * 255
    mask = Image.fromarray(np.repeat(grad, W, 1).astype(np.uint8))
    can.paste(sharp, (0, SHIFT), mask)
    a = np.asarray(can, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    top = np.clip(1 - yy / 760, 0, 1) ** 1.4            # darker top for the headline
    bot = np.clip((yy - 1300) / 620, 0, 1) ** 1.6        # a little darker at the bottom for the inset
    a *= (1 - 0.70 * top) * (1 - 0.45 * bot)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def headline(can, lines, y, size, maxw=980):
    f = ImageFont.truetype(FONT, size)
    while max(f.getlength(l) for l in lines) > maxw:
        size -= 4; f = ImageFont.truetype(FONT, size)
    for ln in lines:
        lay = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        bb = f.getbbox(ln)
        d.text(((W - f.getlength(ln)) / 2, y - bb[1]), ln, font=f, fill=(255, 255, 255, 255))
        t2.shadow(can, lay, (0, 0), off=(0, 8), blur=16, a=180)
        can.alpha_composite(lay)
        y += int(size * 0.98)
    return y


def build(lines, size, out):
    can = base()
    headline(can, lines, 250, size)
    ins = t2.inset(f"{SCR}/assets/team20_foster.png", (560, 230, 1060, 560), 540, border=9)
    x, y = 56, 1700 - ins.height
    t2.shadow(can, ins, (x, y))
    can.alpha_composite(ins, (x, y))
    im = can.convert("RGB")
    g = np.random.default_rng(9).normal(0, 2.2, (H, W, 1))
    im = Image.fromarray(np.clip(np.asarray(im, np.float32) + g, 0, 255).astype(np.uint8))
    im.save(out, quality=95)
    return out


if __name__ == "__main__":
    for k, (lines, size) in {"A": (["HIS TEAMMATES", "KNEW."], 170),
                             "B": (["EVERYONE WAS", "WATCHING THE", "WRONG RUNNER."], 140)}.items():
        print(build(lines, size, f"/home/user/YouTube-/projects/shea-foster/out/shea_tiktok_cover_{k}.jpg"))

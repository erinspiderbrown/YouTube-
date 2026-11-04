"""On-screen graphics renderer (transparent 1920x1080 PNGs)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1920, 1080
ORANGE = (255, 122, 26, 255)
WHITE = (255, 255, 255, 255)
DARK = (14, 14, 16, 215)
FD = "/usr/share/fonts/opentype/inter/"
def font(weight, size):
    for n in (f"InterDisplay-{weight}.otf", f"Inter-{weight}.otf"):
        try: return ImageFont.truetype(FD + n, size)
        except OSError: pass
    return ImageFont.truetype(FD + "Inter-Bold.otf", size)

def _shadow(img, radius=14, alpha=150):
    a = img.split()[-1].filter(ImageFilter.GaussianBlur(radius))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: min(alpha, v)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 6)); out.alpha_composite(img)
    return out

def lower_third(name, sub, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    fn, fs = font("Black", 64), font("SemiBold", 32)
    nw = d.textlength(name.upper(), font=fn); sw = d.textlength(sub.upper(), font=fs)
    x, y = 110, 800
    bw = int(max(nw, sw) + 70)
    d.rectangle([x, y, x + 12, y + 150], fill=ORANGE)
    d.rectangle([x + 12, y, x + 12 + bw, y + 92], fill=DARK)
    d.text((x + 44, y + 10), name.upper(), font=fn, fill=WHITE)
    d.rectangle([x + 12, y + 92, x + 12 + int(sw + 70), y + 150], fill=ORANGE)
    d.text((x + 44, y + 101), sub.upper(), font=fs, fill=(20, 20, 20, 255))
    _shadow(img).save(path)

def keyword(text, path, pos="left", size=96):
    """Bold word(s) on an orange bar, kinetic-bar style."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("Black", size)
    lines = text.upper().split("\n")
    lh = int(size * 1.22)
    widths = [d.textlength(l, font=f) for l in lines]
    if pos == "left": x0, y0 = 110, 150
    elif pos == "right": x0, y0 = W - 110 - max(widths) - 60, 150
    else: x0, y0 = (W - max(widths) - 60) / 2, H - 140 - lh * len(lines)
    for i, (l, w) in enumerate(zip(lines, widths)):
        y = y0 + i * (lh + 10)
        bx = x0 if pos != "center" else (W - w - 60) / 2
        fill = ORANGE if i == len(lines) - 1 else DARK
        col = (20, 20, 20, 255) if fill == ORANGE else WHITE
        d.rectangle([bx, y, bx + w + 60, y + lh], fill=fill)
        d.text((bx + 30, y + lh / 2), l, font=f, fill=col, anchor="lm")
    _shadow(img).save(path)

def title_card(top, big, path, note=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    fb, ft = font("Black", 150), font("Bold", 44)
    d.text((W / 2, H / 2 - 110), top.upper(), font=ft, fill=ORANGE, anchor="mm")
    for i, l in enumerate(big.upper().split("\n")):
        d.text((W / 2, H / 2 + i * 160), l, font=fb, fill=WHITE, anchor="mm")
    if note:
        d.text((W / 2, H - 70), note.upper(), font=font("Medium", 24), fill=(220, 220, 220, 255), anchor="mm")
    _shadow(img, 20, 200).save(path)

def caption_tag(text, path):
    """Small source/credit tag bottom-right."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("SemiBold", 24); w = d.textlength(text, font=f)
    d.rectangle([W - 70 - w - 30, H - 90, W - 70, H - 50], fill=(0, 0, 0, 150))
    d.text((W - 70 - w - 15, H - 70), text, font=f, fill=(230, 230, 230, 255), anchor="lm")
    img.save(path)

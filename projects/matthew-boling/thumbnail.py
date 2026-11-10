"""Thumbnails for The Downfall of Matthew Boling, Ev Hand style (examples/thumbnails/README.md).
One scene: real HD Boling (Georgia documentary frame, 1080p, only downscaled), a physical prop
(a stadium LED board frozen at 9.98 with a red "WIND-AIDED" hang tag), 1-3 huge words, one curved arrow.
python3 -I thumbnail.py SRC_FRAME OUT_DIR
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1920, 1080
ROOT = "/home/user/YouTube-"
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"; INTBL = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
YEL, RED, WHITE, BLACK = (255, 214, 0), (226, 30, 38), (255, 255, 255), (0, 0, 0)
F = lambda p, s: ImageFont.truetype(p, s)


def base():
    src = Image.open(SRC).convert("RGB")                      # 1920x1080 doc frame, face at x~600-990
    ph = src.crop((380, 0, 1380, 1080))                       # 1000x1080, no scaling
    ph = ImageEnhance.Contrast(ph).enhance(1.12); ph = ImageEnhance.Color(ph).enhance(1.08)
    ph = ImageEnhance.Brightness(ph).enhance(1.04)
    im = Image.new("RGB", (W, H), (12, 13, 18))
    # right side: dark stadium night glow
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse([1050, 150, 2100, 1150], fill=150)
    glow = Image.new("RGB", (W, H), (120, 20, 20)); im.paste(glow, (0, 0), g.filter(ImageFilter.GaussianBlur(160)))
    m = Image.new("L", ph.size, 255); md = ImageDraw.Draw(m)
    for i in range(220): md.line([(ph.width - 220 + i, 0), (ph.width - 220 + i, H)], fill=int(255 * (1 - i / 220)))
    im.paste(ph, (0, 0), m)
    return im


def led_board(im, x, y, text="9.98"):
    """Stadium LED timing board as a physical prop."""
    d = ImageDraw.Draw(im); bw, bh = 700, 330
    sh = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 40, bw + 40, bh + 40], 26, fill=(0, 0, 0, 200))
    im.paste(sh.filter(ImageFilter.GaussianBlur(22)), (x - 30, y - 10), sh.filter(ImageFilter.GaussianBlur(22)))
    d.rounded_rectangle([x, y, x + bw, y + bh], 22, fill=(18, 18, 20), outline=(70, 70, 76), width=8)
    d.rounded_rectangle([x + 26, y + 26, x + bw - 26, y + bh - 26], 10, fill=(6, 6, 6))
    f = F(ANTON, 250); tw = d.textlength(text, font=f)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text((x + bw / 2, y + bh / 2 + 6), text, font=f, fill=(255, 168, 20, 255), anchor="mm")
    gl = lay.filter(ImageFilter.GaussianBlur(14))
    im.paste(gl, (0, 0), gl); im.paste(lay, (0, 0), lay)
    # LED dot grid
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dots)
    for yy in range(y + 30, y + bh - 30, 9): dd.line([(x + 30, yy), (x + bw - 30, yy)], fill=(0, 0, 0, 90), width=3)
    im.paste(dots, (0, 0), dots)
    d.text((x + 40, y + 34), "100M", font=F(INTBL, 34), fill=(200, 200, 205))
    d.text((x + bw - 40, y + 34), "WIND +4.2", font=F(INTBL, 34), fill=(255, 80, 80), anchor="ra")
    return (x, y, bw, bh)


def hang_tag(im, x, y, text, rot=-12):
    tw, th = 420, 150
    t = Image.new("RGBA", (tw + 60, th + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.polygon([(30, 30 + th / 2), (80, 30), (30 + tw, 30), (30 + tw, 30 + th), (80, 30 + th)], fill=RED + (255,))
    d.ellipse([58, 30 + th / 2 - 14, 86, 30 + th / 2 + 14], fill=(250, 240, 230, 255))
    d.text((30 + tw / 2 + 30, 30 + th / 2), text, font=F(ANTON, 86), fill=WHITE + (255,), anchor="mm")
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", t.size, (0, 0, 0, 0)); sh.putalpha(t.split()[-1].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
    im.paste(sh, (x + 8, y + 12), sh); im.paste(t, (x, y), t)


def big_text(im, lines, x, y, size=190):
    d = ImageDraw.Draw(im)
    for i, parts in enumerate(lines):
        cx = x
        for s, c in parts:
            f = F(ANTON, size)
            d.text((cx, y + i * (size + 8)), s, font=f, fill=c, stroke_width=14, stroke_fill=BLACK)
            cx += d.textlength(s, font=f)


def arrow(im, p0, p1, bend=0.35, col=YEL, w=22):
    d = ImageDraw.Draw(im); (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1) for t in [i / 40 for i in range(41)]]
    for a, b in zip(pts, pts[1:]): d.line([a, b], fill=BLACK, width=w + 12)
    ang = math.atan2(y1 - pts[-4][1], x1 - pts[-4][0]); L = 70
    head = [(x1, y1), (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)), (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))]
    d.polygon(head, fill=BLACK, outline=BLACK, width=12)
    for a, b in zip(pts, pts[1:]): d.line([a, b], fill=col, width=w)
    d.polygon(head, fill=col)


def save(im, name):
    im.save(f"{OUT}/{name}_HD.jpg", quality=95, subsampling=0)
    im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=95, subsampling=0, optimize=True)


# A: WHAT HAPPENED?  board + wind tag, arrow from the tag to the wind reading
im = base(); bx, by, bw, bh = led_board(im, 1150, 600)
hang_tag(im, 1050, 860, "WIND-AIDED", 6)
big_text(im, [[("WHAT", WHITE)], [("HAPPENED?", YEL)]], 1040, 40, 200)
arrow(im, (1560, 905), (1830, 700), 0.25)
save(im, "A_what_happened")

# B: NEXT BOLT?  same scene, different words
im = base(); led_board(im, 1150, 600); hang_tag(im, 1050, 860, "WIND-AIDED", 6)
big_text(im, [[("THE NEXT", WHITE)], [("BOLT?", YEL)]], 1100, 40, 200)
arrow(im, (1560, 905), (1830, 700), 0.25)
save(im, "B_next_bolt")
print("ok")

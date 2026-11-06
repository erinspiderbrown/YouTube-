"""Thumbnail options v2, in the style of the user's Drummond / Pistorius thumbnails:
full-bleed real HD photo, 2-3 huge white italic words with a shadow, white-bordered inset photo (proof).
Run: python3 -I projects/ncaa-xc-takeover/thumbnails_v2.py OUTDIR"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
PH, FR = f"{SCR}/photos", f"{SCR}/tframes"
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"
FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

def grade(im, c=1.12, s=1.15, b=1.0):
    im = ImageEnhance.Contrast(im).enhance(c); im = ImageEnhance.Color(im).enhance(s)
    return ImageEnhance.Brightness(im).enhance(b)

def bg(path, cx=0.5, cy=0.4, zoom=1.0, sharpen=False):
    im = Image.open(path).convert("RGB")
    w, h = im.size; tw = w / zoom; th = tw * H / W
    if th > h / zoom: th = h / zoom; tw = th * W / H
    x0 = min(max(0, cx * w - tw / 2), w - tw); y0 = min(max(0, cy * h - th / 2), h - th)
    im = im.crop((int(x0), int(y0), int(x0 + tw), int(y0 + th))).resize((W, H), Image.LANCZOS)
    if sharpen: im = im.filter(ImageFilter.UnsharpMask(3, 120, 2))
    return grade(im).convert("RGBA")

def shade(im, side="left", strength=0.75, width=0.6):
    """dark gradient behind the words, like a vignette from that side"""
    g = Image.new("L", (W, 1))
    for x in range(W):
        f = x / W if side == "left" else 1 - x / W
        g.putpixel((x, 0), int(255 * strength * max(0, 1 - f / width) ** 1.4))
    g = g.resize((W, H))
    top = Image.new("L", (1, H))
    for y in range(H): top.putpixel((0, y), int(140 * max(0, 1 - y / (H * 0.55)) ** 2))
    g = Image.fromarray(__import__("numpy").maximum(__import__("numpy").array(g), __import__("numpy").array(top.resize((W, H)))))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 255)); dark.putalpha(g)
    im.alpha_composite(dark)

def words(im, lines, x=70, y=40, size=210, color=(255, 255, 255), accent=None):
    f = ImageFont.truetype(FONT, size)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, l in enumerate(lines):
        col = accent if (accent and i == len(lines) - 1) else color
        d.text((x, y + i * int(size * 1.02)), l, font=f, fill=col + (255,))
    a = lay.split()[-1]
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(16)).point(lambda v: min(255, v * 2)))
    im.alpha_composite(sh, (6, 10)); im.alpha_composite(lay)

def inset(im, src, box, crop=None, border=10, rot=0):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    p = src if isinstance(src, Image.Image) else Image.open(src).convert("RGB")
    if crop: pw, ph = p.size; p = p.crop((int(crop[0] * pw), int(crop[1] * ph), int(crop[2] * pw), int(crop[3] * ph)))
    p = grade(ImageOps.fit(p.convert("RGB"), (w, h), Image.LANCZOS), 1.08, 1.1).filter(ImageFilter.UnsharpMask(2, 80, 2))
    card = Image.new("RGBA", (w + 2 * border, h + 2 * border), (255, 255, 255, 255)); card.paste(p, (border, border))
    if rot: card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.putalpha(card.split()[-1].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.7))
    im.alpha_composite(sh, (x0 - border + 8, y0 - border + 14)); im.alpha_composite(card, (x0 - border, y0 - border))

def comment(text_lines, likes=None, w=900, size=54):
    h = 140 + len(text_lines) * int(size * 1.25) + (60 if likes else 0)
    c = Image.new("RGB", (w, h), (255, 255, 255)); d = ImageDraw.Draw(c)
    d.ellipse([34, 34, 104, 104], fill=(205, 208, 214)); d.rounded_rectangle([130, 46, 400, 76], 8, fill=(220, 222, 228))
    f = ImageFont.truetype(FB, size)
    for i, l in enumerate(text_lines): d.text((130, 100 + i * int(size * 1.25)), l, font=f, fill=(15, 15, 15))
    if likes: d.text((130, h - 70), f"Likes: {likes}", font=ImageFont.truetype(FB, 38), fill=(90, 90, 90))
    return c

def circle(im, box, width=14):
    d = ImageDraw.Draw(im); d.ellipse(box, outline=(240, 30, 30, 255), width=width)

def save(im, name):
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{OUT}/{name}.jpg", quality=94)

# 1 THEY BROKE NO RULES. · stone-faced Lemngole + the 2025 champion as proof
im = bg(f"{PH}/t_lem01.jpg", cx=0.62, cy=0.22, zoom=1.0); shade(im, "left", 0.8, 0.7)
words(im, ["THEY BROKE", "NO RULES."], size=190)
inset(im, f"{FR}/men1940.jpg", (80, 560, 760, 960), crop=(0.08, 0.05, 0.92, 0.9))
save(im, "A_they-broke-no-rules")

# 2 WHAT RULE? · celebrating Lemngole + real comment, circled
im = bg(f"{PH}/p_lemngole.jpg", cx=0.5, cy=0.2, zoom=1.15); shade(im, "left", 0.8, 0.7)
words(im, ["WHAT", "RULE?"], size=230)
c = comment(["Should only be open to", "Americans. Not guests."])
inset(im, c, (70, 640, 70 + 760, 640 + int(760 * c.height / c.width)), border=6, rot=2)
circle(im, (30, 600, 900, 1040))
save(im, "B_what-rule")

# 3 IMPORTED? · Kenyans finishing 1-2 + the "imported" comment
im = bg(f"{PH}/t_cherotich.jpg", cx=0.42, cy=0.3, zoom=1.25); shade(im, "right", 0.85, 0.65)
words(im, ["IMPORTED?"], x=930, y=40, size=150)
c = comment(["Almost all the athletes are", "imported from Africa…"], size=50)
inset(im, c, (1060, 700, 1060 + 780, 700 + int(780 * c.height / c.width)), border=6, rot=-2)
circle(im, (1010, 660, 1890, 1020))
save(im, "C_imported")

# 4 28-YEAR-OLD FRESHMAN? · Kipchoge close up (WSU) + NCAA trophy start line
im = bg(f"{FR}/kip1383.jpg", cx=0.36, cy=0.45, zoom=1.2, sharpen=True); shade(im, "left", 0.8, 0.65)
words(im, ["28 YEARS OLD.", "FRESHMAN."], size=150, accent=(255, 214, 0))
inset(im, f"{FR}/men6.jpg", (70, 680, 610, 980), crop=(0.2, 0.15, 0.95, 0.82))
save(im, "D_28-year-old-freshman")

# 5 NO AGE LIMIT. · Kipchoge + Samuel champion inset (pairs with the 95 title)
im = bg(f"{FR}/kip1380.jpg", cx=0.36, cy=0.45, zoom=1.2, sharpen=True); shade(im, "left", 0.8, 0.65)
words(im, ["NO AGE", "LIMIT."], size=220)
inset(im, f"{FR}/men1940.jpg", (70, 640, 690, 990), crop=(0.08, 0.05, 0.92, 0.9))
save(im, "E_no-age-limit")

# 6 no words, Pistorius-style collage · celebration + champion + real comment in the middle
im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
left = bg(f"{PH}/p_lemngole.jpg", cx=0.45, cy=0.22, zoom=1.0)
im.alpha_composite(ImageOps.fit(left, (952, H), Image.LANCZOS, centering=(0.5, 0.3)), (0, 0))
right = grade(Image.open(f"{FR}/men1940.jpg").convert("RGB").crop((80, 20, 480, 440))).filter(ImageFilter.UnsharpMask(3, 120, 2))
im.alpha_composite(ImageOps.fit(right, (960, H), Image.LANCZOS, centering=(0.55, 0.4)).convert("RGBA"), (960, 0))
c = comment(["Should only be open to", "Americans. Not guests."])
inset(im, c, (560, 730, 560 + 800, 730 + int(800 * c.height / c.width)), border=6)
circle(im, (520, 690, 1400, 1060))
save(im, "F_collage-no-text")
print("done")

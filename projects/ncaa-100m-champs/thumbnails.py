"""Thumbnails for "What happened to the last 10 NCAA men's 100m champions".
Built from the format's breakout thumbnails (see thumbnail_research.md): a row of champions with one-word fate tags,
boom-vs-bust split, year-stamped panels, a lineup + WHAT HAPPENED?
Real photos only: Wikimedia Commons + frames from YouTube race/interview videos (see thumbnail_credits.md).
Run: python3 -I projects/ncaa-100m-champs/thumbnails.py OUTDIR   (renders 1920x1080, saves 1280x720 JPGs)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/hundo/src"
W, H = 1920, 1080
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
YEL, RED, GREEN, WHITE, BLACK = (255, 214, 0), (228, 30, 38), (40, 200, 90), (255, 255, 255), (0, 0, 0)

# name: (file, face centre x, face centre y (0-1 of image), face height as fraction of image height)
SRC = {
    "coleman":    ("coleman_c54.jpg",         0.57, 0.253, 0.30),
    "coleman2":   ("coleman_c26.jpg",         0.552, 0.134, 0.124),
    "oduduru":    ("oduduru_lr88.jpg",        0.46, 0.29, 0.37),
    "oduduru2":   ("oduduru_lr16.jpg",        0.51, 0.25, 0.36),
    "laird":      ("laird_flo132.jpg",        0.46, 0.42, 0.38),
    "laird_close":("laird_flo233.jpg",        0.50, 0.52, 0.71),
    "lawson":     ("lawson_c29.jpg",          0.557, 0.132, 0.104),
    "burrell":    ("burrell_c46.jpg",         0.50, 0.29, 0.466),
    "lindsey":    ("lindsey_c52.jpg",         0.50, 0.254, 0.33),
    "fahnbulleh": ("fahnbulleh_c62.jpg",      0.50, 0.127, 0.13),
    "hinchliffe": ("hinchliffe_ncaa240.jpg",  0.434, 0.38, 0.68),
    "anthony":    ("anthony_ncaa260.jpg",     0.453, 0.33, 0.34),
    "ajayi":      ("ajayi_ldn8.jpg",          0.624, 0.317, 0.14),
    "ajayi2":     ("ajayi_ncaa300.jpg",       0.465, 0.36, 0.66),
}

# usable part of each source (l, t, r, b as fractions): cuts TV tickers, lower-thirds and corner bugs
CROP = {"hinchliffe": (0, 0.09, 1, 0.885), "anthony": (0, 0.09, 1, 0.70), "ajayi2": (0, 0.08, 1, 0.885),
        "laird_close": (0, 0.07, 1, 1), "laird": (0, 0.07, 1, 1), "ajayi": (0, 0, 1, 0.80)}

def face_tile(name, size, face_px, fy=0.4, fx=0.5, enhance=True):
    """Crop a tile of `size` with the face about face_px tall, centred near (fx, fy) of the tile.
    The photo always covers the whole tile (face is enlarged / shifted if needed), so no fill or cut-out edges."""
    f, cx, cy, fh = SRC[name]
    im = Image.open(f"{SCR}/{f}").convert("RGB"); iw, ih = im.size
    l, t, r, b = CROP.get(name, (0, 0, 1, 1))
    im = im.crop((int(l * iw), int(t * ih), int(r * iw), int(b * ih)))
    fpx = fh * ih  # face height in source pixels
    cx = (cx - l) / (r - l); cy = (cy - t) / (b - t); iw, ih = im.size
    tw, th = size
    s = max(face_px / fpx, tw / iw, th / ih)
    sw, sh_ = iw * s, ih * s
    x0 = min(max(cx * sw - fx * tw, 0), sw - tw); y0 = min(max(cy * sh_ - fy * th, 0), sh_ - th)
    out = im.resize((int(round(sw)), int(round(sh_))), Image.LANCZOS).crop((int(x0), int(y0), int(x0) + tw, int(y0) + th))
    if enhance:
        out = ImageEnhance.Contrast(out).enhance(1.1); out = ImageEnhance.Color(out).enhance(1.1)
        out = out.filter(ImageFilter.UnsharpMask(2, 80 if s > 1.2 else 50, 2))
    return out

def text(im, xy, s, size, fill, stroke=0, anchor="mm", shadow=14, font=ANTON):
    fnt = ImageFont.truetype(font, size)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(xy, s, font=fnt, fill=fill + (255,), stroke_width=stroke, stroke_fill=BLACK + (255,), anchor=anchor)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: min(255, int(v * 1.6))))
        im.alpha_composite(sh, (5, 9))
    im.alpha_composite(lay)

def fit_size(s, maxw, size):
    fnt = ImageFont.truetype(ANTON, size)
    while fnt.getlength(s) > maxw and size > 20:
        size -= 4; fnt = ImageFont.truetype(ANTON, size)
    return size

def pill(im, cx, cy, s, size, bg, fg, padx=34, pady=14, radius=18, maxw=None, rot=0):
    if maxw: size = fit_size(s, maxw - 2 * padx, size)
    fnt = ImageFont.truetype(ANTON, size)
    l, t, r, b = fnt.getbbox(s, anchor="mm")
    w, h = (r - l) + 2 * padx, (b - t) + 2 * pady
    lay = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], radius, fill=bg + (255,), outline=BLACK + (255,), width=6)
    d.text((30 + w / 2, 30 + h / 2), s, font=fnt, fill=fg + (255,), anchor="mm")
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[-1].filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(sh, (int(cx - lay.width / 2 + 4), int(cy - lay.height / 2 + 8)))
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def vgrad(im, y0, y1, a0, a1, col=BLACK):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for y in range(y0, y1):
        a = a0 + (a1 - a0) * (y - y0) / max(1, y1 - y0); d.line([(0, y), (W, y)], fill=col + (int(a),))
    im.alpha_composite(g)

def save(im, out, name):
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{out}/{name}.jpg", quality=92)

def check(im, cx, cy, r, col=GREEN):
    """round badge with a tick"""
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=BLACK + (255,))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,))
    d.line([(cx - r * .45, cy + r * .02), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], fill=WHITE + (255,), width=int(r * .28), joint="curve")

def cross(im, cx, cy, r, col=RED):
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=BLACK + (255,))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,))
    k = r * .42; w = int(r * .26)
    d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=WHITE + (255,), width=w); d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=WHITE + (255,), width=w)

def gutters(im, xs, w=10):
    d = ImageDraw.Draw(im)
    for x in xs: d.rectangle([x - w // 2, 0, x + w // 2, H], fill=BLACK + (255,))

def A_fate_row(OUT):
    """Heisman-21 format (1.5M views, 16x): three champions, one-word fate above each."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    cols = [("coleman", "WORLD CHAMP", YEL, BLACK, "2017"), ("oduduru", "BANNED", RED, WHITE, "2019"), ("laird", "INJURED", YEL, BLACK, "2021")]
    for i, (n, tag, bg, fg, yr) in enumerate(cols):
        t = face_tile(n, (640, H), face_px=360, fy=0.50)
        im.paste(t, (i * 640, 0))
    vgrad(im, 0, 260, 150, 0); vgrad(im, 760, H, 0, 220)
    gutters(im, [640, 1280])
    for i, (n, tag, bg, fg, yr) in enumerate(cols):
        pill(im, i * 640 + 320, 125, tag, 118, bg, fg, maxw=600)
        text(im, (i * 640 + 320, 985), f"NCAA CHAMP {yr}", 74, WHITE, stroke=4)
    save(im, OUT, "A_fate-row")

def B_boom_bust(OUT):
    """#1-QB format (1.0M views, 12x): success vs failure split, coloured header tags, years in the corner."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    im.paste(face_tile("coleman", (960, H - 170), face_px=470, fy=0.47), (0, 170))
    im.paste(face_tile("oduduru2", (960, H - 170), face_px=470, fy=0.47), (960, 170))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, W, 170], fill=(12, 12, 12, 255))
    text(im, (480, 88), "WORLD CHAMPION", 120, GREEN, shadow=0)
    text(im, (1440, 88), "BANNED", 132, RED, shadow=0)
    gutters(im, [960], 12)
    for x, yr in ((40, "'17"), (1000, "'19")):
        text(im, (x, 205), yr, 110, WHITE, stroke=6, anchor="la")
    vgrad(im, 860, H, 0, 210)
    text(im, (480, 990), "NCAA CHAMP", 92, YEL, stroke=5)
    text(im, (1440, 990), "NCAA CHAMP", 92, YEL, stroke=5)
    save(im, OUT, "B_boom-vs-bust")

def C_grid10(OUT):
    """Every-champion grid (NFL #1 picks 2.75M, FCS Heisman 28x): all ten, years stamped, the clear fates marked.
    Burrell's tile gets his year and name only: no fate mark."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    champs = [("lawson", "2016"), ("coleman", "2017"), ("burrell", "2018"), ("oduduru", "2019"), ("laird", "2021"),
              ("fahnbulleh", "2022"), ("lindsey", "2023"), ("hinchliffe", "2024"), ("anthony", "2025"), ("ajayi", "2026")]
    top = 250; tw, th = 384, (H - top) // 2
    for i, (n, yr) in enumerate(champs):
        x, y = (i % 5) * tw, top + (i // 5) * th
        im.paste(face_tile(n, (tw, th), face_px=190, fy=0.40), (x, y))
    vgrad(im, top, top + 40, 120, 0)
    d = ImageDraw.Draw(im)
    for i in range(1, 5): d.rectangle([i * tw - 4, top, i * tw + 4, H], fill=BLACK + (255,))
    d.rectangle([0, top + th - 4, W, top + th + 4], fill=BLACK + (255,))
    for i, (n, yr) in enumerate(champs):
        x, y = (i % 5) * tw, top + (i // 5) * th
        text(im, (x + 18, y + th - 16), yr, 82, YEL, stroke=5, anchor="ld", shadow=8)
    marks = {1: ("WORLD CHAMP", GREEN, WHITE), 3: ("BANNED", RED, WHITE), 4: ("INJURED", YEL, BLACK), 9: ("NEXT?", WHITE, BLACK)}
    for i, (tag, bg, fg) in marks.items():
        x, y = (i % 5) * tw, top + (i // 5) * th
        pill(im, x + tw / 2, y + 48, tag, 52, bg, fg, padx=18, pady=8, radius=12, maxw=tw - 20)
    text(im, (W // 2, 128), "WHAT HAPPENED?", 200, WHITE, stroke=0, shadow=0)
    save(im, OUT, "C_all-ten-grid")

def D_year_panels(OUT):
    """NCAA's own 100m compilation (8.6x) + women's 100m (13x): vertical panels with huge years."""
    im = Image.new("RGBA", (W, H), BLACK + (255,))
    panels = [("coleman", "2017", "WORLD CHAMP", GREEN, WHITE), ("oduduru", "2019", "BANNED", RED, WHITE),
              ("laird", "2021", "INJURED", YEL, BLACK), ("ajayi", "2026", "NEXT?", WHITE, BLACK)]
    for i, (n, yr, *_ ) in enumerate(panels):
        im.paste(face_tile(n, (480, H), face_px=280, fy=0.40), (i * 480, 0))
    vgrad(im, 700, H, 0, 235)
    gutters(im, [480, 960, 1440])
    for i, (n, yr, tag, bg, fg) in enumerate(panels):
        cx = i * 480 + 240
        pill(im, cx, 760, tag, 62, bg, fg, padx=22, pady=10, radius=14, maxw=440)
        text(im, (cx, 930), yr, 230, YEL, stroke=8)
    save(im, OUT, "D_year-panels")

def E_next_one(OUT):
    """User's proven style: one big sharp face, soft background, 1-3 huge words, red for contrast.
    Ajayi (2026 champ) + three small 'receipts' of earlier champions."""
    # right: Ajayi, London DL (sharp); left: his NCAA-final crowd, blurred; blended with a soft gradient (no cut-out)
    im = face_tile("ajayi2", (W, H), face_px=900, fx=0.5, fy=0.5, enhance=False).filter(ImageFilter.GaussianBlur(22))
    im = ImageEnhance.Brightness(im).enhance(0.55).convert("RGBA")
    face = face_tile("ajayi", (1080, H), face_px=430, fx=0.52, fy=0.40).convert("RGBA")
    m = Image.new("L", face.size, 255); d = ImageDraw.Draw(m)
    for x in range(260): d.line([(x, 0), (x, H)], fill=int(255 * (x / 260) ** 1.5))
    face.putalpha(m); im.alpha_composite(face, (W - 1080, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for x in range(W): d.line([(x, 0), (x, H)], fill=(0, 0, 0, int(170 * max(0, 1 - x / 1000) ** 1.2)))
    im.alpha_composite(sh)
    text(im, (70, 40), "THE NEXT", 200, WHITE, stroke=8, anchor="la")
    text(im, (70, 250), "ONE?", 300, YEL, stroke=10, anchor="la")
    minis = [("coleman", "WORLD CHAMP", GREEN, WHITE), ("oduduru", "BANNED", RED, WHITE), ("laird", "INJURED", YEL, BLACK)]
    for i, (n, tag, bg, fg) in enumerate(minis):
        x, y = 70 + i * 300, 690
        t = face_tile(n, (270, 300), face_px=150, fy=0.42)
        ImageDraw.Draw(im).rectangle([x - 6, y - 6, x + 276, y + 306], fill=WHITE + (255,))
        im.paste(t, (x, y))
        pill(im, x + 135, y + 300, tag, 40, bg, fg, padx=12, pady=6, radius=10, maxw=290)
    save(im, OUT, "E_next-one")

def F_banned_face(OUT):
    """Single big face, NCAA CHAMP -> BANNED (true: AIU ban to Feb 2029; his 2019 NCAA title is not struck, so no strike-through)."""
    base = face_tile("oduduru", (W, H), face_px=640, fx=0.70, fy=0.44)
    blur = base.filter(ImageFilter.GaussianBlur(12))
    mask = Image.new("L", (W, H)); d = ImageDraw.Draw(mask)
    for x in range(W): d.line([(x, 0), (x, H)], fill=int(255 * min(1, max(0, (1000 - x) / 300))))
    im = Image.composite(blur, base, mask).convert("RGBA")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for x in range(W): d.line([(x, 0), (x, H)], fill=(0, 0, 0, int(215 * max(0, 1 - x / 1150) ** 1.2)))
    im.alpha_composite(sh)
    text(im, (70, 110), "NCAA CHAMP", 170, WHITE, stroke=8, anchor="la")
    d = ImageDraw.Draw(im)
    d.polygon([(330, 360), (470, 360), (470, 320), (560, 410), (470, 500), (470, 460), (330, 460)], fill=RED + (255,), outline=BLACK + (255,))
    pill(im, 420, 680, "BANNED", 230, RED, WHITE, padx=40, pady=18, radius=22, rot=4)
    text(im, (420, 905), "UNTIL 2029", 100, WHITE, stroke=5)
    save(im, OUT, "F_champ-to-banned")

if __name__ == "__main__":
    OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
    for fn in (A_fate_row, B_boom_bust, C_grid10, D_year_panels, E_next_one, F_banned_face):
        fn(OUT)
    print("done")

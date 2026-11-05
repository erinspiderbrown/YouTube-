"""Jon Drummond thumbnail v3: built from what's winning in the athlete-scandal niche (vidIQ outliers, 5 Nov 2026).

The pattern the top performers share ("RayGun and the Story of the 'Worst Olympian Ever'" 7.1x, David King
"HE DIDN'T WANT THIS" 11x, CATASTROPHIYA "SHE STILL HANGS" 20x, "FRAMED" 188x):
  one real subject, big, cut out on a dark stadium; ONE proof element (RayGun's 0-18 scoreboard);
  2-4 huge condensed words that add a question the title doesn't answer; one red accent. Nothing else.

Here: the real Paris 2003 frame of Drummond, hands up and eyes closed ("I didn't move"), cut out over a dark
Stade de France, an LED results board reading FALSE START behind him, and a 3-line headline on the right.
Variants for YouTube Test & Compare: A "WORST PROTEST EVER?", B "HE WOULDN'T LEAVE".
Rendered at 2560x1440, saved at 1280x720.
"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, "/home/user/YouTube-/projects/jon-drummond")
from thumbnail_v2 import SRC, PH, ANTON, W, H, cover, shadow  # noqa: E402

SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SCR}/output"
RED = (232, 24, 34); WHITE = (250, 248, 242); AMBER = (255, 170, 40)

def F(size): return ImageFont.truetype(ANTON, size)

def noise(shape, scale, seed):
    """Smooth value noise in [0,1]."""
    rng = np.random.default_rng(seed)
    h, w = shape
    small = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def grunge(shape, seed=1, amount=0.05):
    """Worn-print mask (1 = ink, 0 = chipped), like the distressed type on the top doc thumbnails."""
    h, w = shape
    n = 0.6 * noise(shape, 2, seed) + 0.4 * noise(shape, 7, seed + 1)
    chip = (n > np.quantile(n, 1 - amount)).astype(np.float32)
    rng = np.random.default_rng(seed + 9)
    sc = Image.new("L", (w, h), 0); d = ImageDraw.Draw(sc)
    for _ in range(int(w * h / 260000)):      # a few thin scratches
        x, y = rng.integers(0, w), rng.integers(0, h); L = rng.integers(20, 140); a = rng.uniform(-0.5, 0.5)
        d.line([x, y, x + L * math.cos(a), y + L * math.sin(a)], fill=255, width=int(rng.integers(2, 5)))
    chip = np.maximum(chip, np.asarray(sc, np.float32) / 255 * 0.9)
    m = 1 - chip * 0.92
    return Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))

def headline(lines, width, gap=34):
    """Stack lines and size each one to the same width (like the RayGun thumbnail). lines: [(text, color)]."""
    rows = []
    for t, col in lines:
        sz = 400
        for _ in range(30):
            bb = F(sz).getbbox(t); tw = bb[2] - bb[0]
            if abs(tw - width) < 4: break
            sz = int(sz * width / tw)
        bb = F(sz).getbbox(t)
        rows.append((t, col, sz, bb))
    hsum = sum(bb[3] - bb[1] for *_, bb in rows) + gap * (len(rows) - 1)
    lay = Image.new("RGBA", (width + 40, hsum + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    y = 20
    for t, col, sz, bb in rows:
        d.text((20 - bb[0], y - bb[1]), t, font=F(sz), fill=col + (255,))
        y += bb[3] - bb[1] + gap
    a = np.asarray(lay.split()[-1], np.float32) * np.asarray(grunge((lay.height, lay.width), 4), np.float32) / 255
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    return lay

def brush(w, h, color=RED, seed=5):
    """A dry red brush swipe (underline)."""
    rng = np.random.default_rng(seed)
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    xs = np.linspace(0, w, 80)
    top = h * 0.30 + np.sin(xs / w * math.pi) * -h * 0.10 + rng.normal(0, h * 0.02, 80)
    thick = h * 0.42 * (np.sin(np.clip(xs / w, 0, 1) * math.pi) ** 0.35)
    thick[:6] *= np.linspace(0.3, 1, 6)
    pts = list(zip(xs, top)) + list(zip(xs[::-1], (top + thick)[::-1]))
    d.polygon(pts, fill=255)
    a = np.asarray(m, np.float32) / 255
    streak = noise((h, w), 2, seed)[:, :1] * np.ones((1, w))          # horizontal bristle streaks
    fade = np.clip((np.arange(w) - w * 0.72) / (w * 0.28), 0, 1)[None, :]  # dry tail on the right
    a = a * (1 - (streak < 0.30 + fade * 0.45) * (0.25 + 0.75 * fade))
    a *= np.asarray(grunge((h, w), seed, 0.08), np.float32) / 255
    lay = Image.new("RGBA", (w, h), color + (0,)); lay.putalpha(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)))
    return lay

def led_board(lines, cols=74, pitch=15, pad=26):
    """Stadium results board in dot-matrix LEDs. lines: [(text, color, rows)]."""
    rows_total = sum(r for _, _, r in lines) + 2 * (len(lines) - 1)
    bw, bh = cols * pitch + 2 * pad, rows_total * pitch + 2 * pad
    board = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(board)
    d.rounded_rectangle([0, 0, bw + 39, bh + 39], radius=18, fill=(26, 28, 34, 255), outline=(70, 74, 84, 255), width=6)
    d.rectangle([20, 20, bw + 19, bh + 19], fill=(6, 6, 9, 255))
    glow = Image.new("RGBA", board.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    y0 = 0
    for t, col, rows in lines:
        # rasterise the text at LED resolution
        fnt = F(100); bb = fnt.getbbox(t)
        tmp = Image.new("L", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), 0)
        ImageDraw.Draw(tmp).text((2 - bb[0], 2 - bb[1]), t, font=fnt, fill=255)
        tw = max(1, round(tmp.width * rows / tmp.height)); tw = min(tw, cols)
        dots = np.asarray(tmp.resize((tw, rows), Image.BOX), np.float32) / 255
        x0 = (cols - tw) // 2
        for r in range(cols):
            for q in range(rows):
                cx = 20 + pad + r * pitch + pitch // 2; cy = 20 + pad + (y0 + q) * pitch + pitch // 2
                on = r - x0 in range(tw) and dots[q, r - x0] > 0.42
                rad = pitch * 0.36
                if on:
                    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col + (255,))
                    gd.ellipse([cx - rad * 1.6, cy - rad * 1.6, cx + rad * 1.6, cy + rad * 1.6], fill=col + (255,))
                else:
                    d.ellipse([cx - rad * 0.8, cy - rad * 0.8, cx + rad * 0.8, cy + rad * 0.8], fill=(24, 22, 26, 255))
        y0 += rows + 2
    g = glow.filter(ImageFilter.GaussianBlur(14)); g.putalpha(g.split()[-1].point(lambda v: v * 150 // 255))
    out = Image.new("RGBA", board.size, (0, 0, 0, 0)); out.alpha_composite(board); out.alpha_composite(g)
    return out

def backdrop():
    st = Image.open(f"{PH}/l_paris_stadium.jpg").convert("RGB").crop((0, 140, 1600, 760))
    bg = cover(st, (W, H), 0.5, 0.5).filter(ImageFilter.GaussianBlur(9))
    bg = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(0.35)).enhance(0.30)
    a = np.asarray(bg, np.float32)
    a = a * np.array([0.82, 0.9, 1.12])                           # cool night grade
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # red backlight behind the subject's head, dark falloff to the edges
    red = np.exp(-(((xx - 820) / 900) ** 2 + ((yy - 560) / 700) ** 2))[..., None] * np.array([150, 18, 22])
    a = a + red
    vig = 1 - 0.65 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.75)) ** 2, 0, 1)
    a = a * vig[..., None]
    # stadium floodlights (top left), soft bloom + star streaks
    fl = np.zeros((H, W), np.float32)
    for cx, cy, s in ((240, 120, 1.0), (520, 70, 0.8), (90, 260, 0.6)):
        fl += s * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * 26 ** 2)))
        fl += s * 0.35 * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * 140 ** 2)))
        fl += s * 0.25 * np.exp(-(((yy - cy) / 5) ** 2)) * np.exp(-((xx - cx) / 420) ** 2)
    a = a + fl[..., None] * np.array([235, 240, 255])
    n = np.random.default_rng(3).normal(0, 6, (H, W, 1))
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).convert("RGBA")

def subject(height):
    cut = Image.open(f"{SRC}/cut_handsup.png").convert("RGBA")
    cut = cut.crop(cut.split()[-1].getbbox())
    s = height / cut.height
    cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
    rgb = cut.convert("RGB").filter(ImageFilter.UnsharpMask(radius=3, percent=110, threshold=2))
    rgb = ImageEnhance.Color(ImageEnhance.Contrast(rgb).enhance(1.16)).enhance(1.12)
    a = np.asarray(rgb, np.float32)
    al = cut.split()[-1].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    # rim light: warm on the right edge, red on the left, like the backlight in the scene
    er = al.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(3))
    edge = np.clip((np.asarray(al, np.float32) - np.asarray(er, np.float32)) / 255, 0, 1)[..., None]
    xs = np.linspace(0, 1, cut.width)[None, :, None]
    rim = (1 - xs) * np.array([255, 60, 50]) + xs * np.array([255, 225, 190])
    a = a * (1 - edge * 0.35) + rim * edge * 0.35
    # sink the bottom (bib) into shadow so the eye goes to the face and hands
    yy = np.linspace(0, 1, cut.height)[:, None, None]
    a = a * (1 - np.clip((yy - 0.72) / 0.28, 0, 1) * 0.55)
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); out.putalpha(al)
    return out

def build(words, red_idx, board_lines):
    can = backdrop()
    # proof element: the results board, behind him
    bd = led_board(board_lines)
    bd = bd.resize((int(bd.width * 1.0), int(bd.height * 1.0)), Image.LANCZOS)
    bx, by = (W - 1240) // 2 - 520, 40
    shadow(can, bd.filter(ImageFilter.GaussianBlur(1.2)), (bx, by), off=(0, 18), blur=30, alpha=170)
    # subject
    sub = subject(1220)
    sx, sy = -150, H - sub.height + 40
    shadow(can, sub, (sx, sy), off=(26, 10), blur=40, alpha=230)
    # headline, right
    tw = 860
    hl = headline([(w, RED if i == red_idx else WHITE) for i, w in enumerate(words)], tw)
    hx, hy = W - tw - 90, (H - hl.height) // 2 - 70
    # dark halo behind the type so it reads on any background
    halo = Image.new("RGBA", hl.size, (0, 0, 0, 0)); halo.putalpha(hl.split()[-1].filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(30)).point(lambda v: v * 200 // 255))
    can.alpha_composite(halo, (hx - 20, hy - 20))
    if red_idx is not None:
        # red glow under the red word only
        r = Image.new("RGBA", hl.size, (0, 0, 0, 0)); ra = np.asarray(hl, np.float32)
        mask = ((ra[..., 0] > 180) & (ra[..., 1] < 90)).astype(np.float32) * ra[..., 3] / 255
        r = Image.new("RGBA", hl.size, RED + (0,)); r.putalpha(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28)))
        can.alpha_composite(r, (hx - 20, hy - 20))
    sh = Image.new("RGBA", hl.size, (0, 0, 0, 0)); sh.putalpha(hl.split()[-1].filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * 220 // 255))
    can.alpha_composite(sh, (hx - 20 + 10, hy - 20 + 14))
    can.alpha_composite(hl, (hx - 20, hy - 20))
    br = brush(tw + 80, 150)
    can.alpha_composite(br, (hx - 50, hy - 20 + hl.height - 10))
    # film grain + slight overall contrast
    out = can.convert("RGB")
    out = ImageEnhance.Contrast(out).enhance(1.05)
    g = np.random.default_rng(11).normal(0, 4.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))

BOARD = [("FALSE START", RED, 15)]
VARIANTS = {
    "A": (["WORST", "PROTEST", "EVER?"], None),
    "B": (["HE WOULDN'T", "LEAVE"], 1),
}

if __name__ == "__main__":
    for k, (words, red) in VARIANTS.items():
        im = build(words, red, BOARD)
        im.save(f"{OUT}/drummond_thumb_v3_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/drummond_thumb_v3_{k}.jpg", quality=94)
        print(k, im.size)

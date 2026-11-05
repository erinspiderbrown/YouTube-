"""Jon Drummond thumbnail v4: HD real frames, layered.

Sources (all real, Paris 2003 World Championships):
- HD broadcast frame of the official raising the red card over Drummond as he protests, hands up
  (from a clean re-upload of the race coverage, imported via vidIQ). Burned-in subtitles were removed by
  aligning an AI clean-up of the frame and pasting back ONLY the subtitle patch; the rest is original pixels.
  Cut out with BiRefNet.
- HD frame of him lying on the track, hands behind his head, officials' shoes beside him (same treatment).
- The start-sensor printout shown in that coverage: "Lane4 0.052 Sec Fault".
- Wikimedia Commons Stade de France (Paris 2003) for the backdrop.
Rendered at 2560x1440, saved at 1280x720.
"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
SRC = f"{SCR}/thumb4/src"
PH = f"{SCR}/photos"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{SCR}/thumb4"
ANTON = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
W, H = 2560, 1440
RED = (235, 30, 38); YEL = (255, 214, 0); WHITE = (255, 255, 255); BLACK = (0, 0, 0)

def F(s): return ImageFont.truetype(ANTON, s)

def cover(im, size, cx=0.5, cy=0.5):
    w, h = im.size; tw, th = size
    s = max(tw / w, th / h); im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    x = int((im.width - tw) * cx); y = int((im.height - th) * cy)
    return im.crop((x, y, x + tw, y + th))

def grade(im, c=1.12, s=1.18, sharp=110):
    rgb = im.convert("RGB").filter(ImageFilter.UnsharpMask(radius=2.2, percent=sharp, threshold=2))
    return ImageEnhance.Color(ImageEnhance.Contrast(rgb).enhance(c)).enhance(s)

def glow_layer(alpha, color, blur, gain=1.0):
    g = alpha.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, int(v * gain)))
    lay = Image.new("RGBA", alpha.size, color + (0,)); lay.putalpha(g)
    return lay

def drop_shadow(base, layer, xy, off=(0, 24), blur=34, a=200):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.split()[-1].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * a // 255))
    base.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1]))

def backdrop():
    st = Image.open(f"{PH}/l_paris_2003_b.jpg").convert("RGB")
    bg = cover(st, (W, H), 0.5, 0.35).filter(ImageFilter.GaussianBlur(14))
    a = np.asarray(ImageEnhance.Color(bg).enhance(0.5), np.float32) * 0.28
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # hot red light behind the hero (right), cold blue on the left
    a += np.exp(-(((xx - 2050) / 700) ** 2 + ((yy - 950) / 560) ** 2))[..., None] * np.array([185, 20, 24])
    # keep it dark around the red card so the card itself pops
    a *= (1 - 0.6 * np.exp(-(((xx - 1720) / 420) ** 2 + ((yy - 220) / 300) ** 2)))[..., None]
    a += np.exp(-(((xx - 300) / 900) ** 2 + ((yy - 300) / 700) ** 2))[..., None] * np.array([10, 40, 110])
    # light rays from the top right
    ang = np.arctan2(yy + 200, xx - 2100)
    rays = (0.5 + 0.5 * np.sin(ang * 26)) ** 6 * np.clip(1 - np.hypot(xx - 2100, yy + 200) / 2200, 0, 1)
    a += rays[..., None] * np.array([80, 26, 22])
    vig = 1 - 0.55 * np.clip(((xx - W * 0.6) / (W * 0.7)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2, 0, 1)
    a *= vig[..., None]
    a += np.random.default_rng(3).normal(0, 5, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def hero(scale):
    cut = Image.open(f"{SRC}/cut_hero.png").convert("RGBA")
    rgb = grade(cut, 1.14, 1.15, 120)
    al = cut.split()[-1].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    A = np.asarray(al, np.float32)
    # the frame edges cut the official's arm (left) and a hand (right): fade those edges into the dark
    xs = np.arange(cut.width, dtype=np.float32)[None, :]
    A *= np.clip(xs / 150, 0, 1) ** 1.2
    A *= np.clip((cut.width - 1 - xs) / 60, 0, 1)
    im = rgb.convert("RGBA"); im.putalpha(Image.fromarray(A.astype(np.uint8)))
    # warm rim light from the red glow behind
    er = im.split()[-1].filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(4))
    edge = np.clip((np.asarray(im.split()[-1], np.float32) - np.asarray(er, np.float32)) / 255, 0, 1)[..., None]
    px = np.asarray(im.convert("RGB"), np.float32)
    px = px * (1 - edge * 0.45) + np.array([255, 120, 90]) * edge * 0.45
    card = np.zeros(px.shape[:2], np.float32); card[78:392, 168:402] = 1
    redness = np.clip((px[..., 0] - np.maximum(px[..., 1], px[..., 2]) - 40) / 60, 0, 1) * card
    tgt = px * np.array([1.0, 0.62, 0.62]) * 1.02
    px = px * (1 - redness[..., None]) + tgt * redness[..., None]
    out = Image.fromarray(np.clip(px, 0, 255).astype(np.uint8)).convert("RGBA"); out.putalpha(im.split()[-1])
    out = out.crop((0, 40, cut.width, cut.height))
    return out.resize((round(out.width * scale), round(out.height * scale)), Image.LANCZOS)

def photo_card(im, w, h, rot, border=16, label=None):
    ph = grade(cover(im, (w, h)), 1.1, 1.15, 90)
    card = Image.new("RGBA", (w + 2 * border, h + 2 * border), WHITE + (255,))
    card.paste(ph, (border, border))
    if label:
        d = ImageDraw.Draw(card); f = F(64)
        tw = d.textlength(label, font=f)
        d.rectangle([border, h + border - 104, border + tw + 56, h + border - 18], fill=RED + (255,))
        d.text((border + 28, h + border - 61), label, font=f, fill=WHITE + (255,), anchor="lm")
    return card.rotate(rot, expand=True, resample=Image.BICUBIC)

def sensor_chip():
    g = Image.open(f"{SRC}/graph_lane4.png").convert("RGB").crop((0, 110, 470, 590))
    g = ImageEnhance.Contrast(g).enhance(1.15)
    card = Image.new("RGBA", (g.width + 24, g.height + 24), WHITE + (255,)); card.paste(g, (12, 12))
    d = ImageDraw.Draw(card)
    # red ring around "0.052 Sec / Fault"
    d.ellipse([-6, 92, 300, 300], outline=RED + (255,), width=12)
    return card.rotate(6, expand=True, resample=Image.BICUBIC)

def arrow(base, p0, p1, bend=0.25, color=YEL, width=30):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * bend, my + ny * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 60)]
    ang = math.atan2(pts[-1][1] - pts[-5][1], pts[-1][0] - pts[-5][0])
    L = width * 3.0
    def head(k):
        tip = (x1 + math.cos(ang) * width * 0.6 * k, y1 + math.sin(ang) * width * 0.6 * k)
        return [tip, (x1 - L * k * math.cos(ang - 0.55), y1 - L * k * math.sin(ang - 0.55)), (x1 - L * k * math.cos(ang + 0.55), y1 - L * k * math.sin(ang + 0.55))]
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(pts[:-3], fill=BLACK + (255,), width=width + 16, joint="curve"); d.polygon(head(1.25), fill=BLACK + (255,))
    d.line(pts[:-3], fill=color + (255,), width=width, joint="curve"); d.polygon(head(1.0), fill=color + (255,))
    drop_shadow(base, lay, (0, 0), off=(6, 12), blur=10, a=150)
    base.alpha_composite(lay)

def headline(base, lines, x, y, gap=10):
    right = 0
    """lines: [(text, size, fill)]. Thick black stroke + hard drop shadow + soft glow on coloured words."""
    for t, sz, col in lines:
        f = F(sz); bb = f.getbbox(t)
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((x, y - bb[1]), t, font=f, fill=col + (255,), stroke_width=int(sz * 0.045), stroke_fill=BLACK + (255,))
        a = lay.split()[-1]
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(3)).point(lambda v: v * 230 // 255))
        base.alpha_composite(sh, (14, 18))
        if col != WHITE:
            base.alpha_composite(glow_layer(a, col, 40, 0.9))
        base.alpha_composite(lay)
        right, mid = x + bb[2], y + (bb[3] - bb[1]) // 2   # ends on the last line
        y += (bb[3] - bb[1]) + gap
    return right, mid

def build(lines):
    can = backdrop()
    # hero: official raising the red card over Drummond (right)
    S = 1.22
    hr = hero(S)
    hx, hy = W - hr.width + 100, -20
    def P(x, y): return hx + int(x * S), hy + int((y - 40) * S)   # source-frame coords -> canvas
    # red card: white edge glow + red bloom so it separates from the background
    card = Image.new("L", can.size, 0)
    ImageDraw.Draw(card).rounded_rectangle([*P(168, 78), *P(402, 392)], radius=14, fill=255)
    can.alpha_composite(glow_layer(card, (255, 50, 40), 60, 1.3))
    can.alpha_composite(glow_layer(card.filter(ImageFilter.MaxFilter(17)), WHITE, 10, 1.6))
    drop_shadow(can, hr, (hx, hy), off=(-30, 20), blur=40, a=210)
    can.alpha_composite(hr, (hx, hy))
    # inset: him lying on the track (bottom left)
    ly = Image.open(f"{SRC}/lying_clean.png").convert("RGB").crop((0, 520, 1080, 1360))
    pc = photo_card(ly, 760, 560, 4, label="50 MINUTES")
    px_, py_ = 110, H - pc.height - 40
    drop_shadow(can, pc, (px_, py_), off=(12, 26), blur=30, a=220)
    can.alpha_composite(pc, (px_, py_))
    # proof: start-sensor printout
    sc = sensor_chip().resize((int(470 * 0.62 + 30), int(480 * 0.62 + 40)), Image.LANCZOS)
    sx, sy = px_ + pc.width - 120, py_ + 40
    drop_shadow(can, sc, (sx, sy), off=(10, 20), blur=24, a=200)
    can.alpha_composite(sc, (sx, sy))
    # headline (top left)
    tr, tm = headline(can, lines, 90, 60)
    # arrow from the headline to the red card
    cx_, cy_ = P(160, 230)
    arrow(can, (tr + 60, tm - 20), (cx_ - 20, cy_ + 40), bend=-0.2)
    out = can.convert("RGB")
    out = ImageEnhance.Contrast(out).enhance(1.04)
    g = np.random.default_rng(9).normal(0, 3.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))

VARIANTS = {
    "A": [("“I DIDN'T", 300, WHITE), ("MOVE!”", 360, YEL)],
    "B": [("HE WOULDN'T", 250, WHITE), ("LEAVE", 380, YEL)],
}

if __name__ == "__main__":
    for k, lines in VARIANTS.items():
        im = build(lines)
        im.save(f"{OUT}/drummond_thumb_v4_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{OUT}/drummond_thumb_v4_{k}.jpg", quality=94)
        print(k)

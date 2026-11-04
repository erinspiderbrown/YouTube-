"""Futuristic HUD keyword pop-ups (replaces the flat orange bars).

Per frame:
- corner brackets snap open from the centre of the box
- a dark glass panel with a faint border and moving scanlines
- characters 'decode' (random glyphs resolving left to right) with chromatic aberration
- a mono index label ("// 07  SIGNAL") with a blinking cursor
- an orange underline sweeps across, then a light pulse travels along it
- exit: horizontal glitch slices + RGB split, then gone
Rendered to a 1920x1080 RGBA .mov (PNG codec).
"""
import random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfx

W, H, FPS = 1920, 1080, 24
ORANGE = (255, 122, 26)
WHITE = (250, 250, 250)
GLYPHS = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&/<>=+"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def eo(t):
    t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def seg(t, a, b):
    return min(max((t - a) / (b - a), 0), 1)

def render(text, idx, dur, pos, out, label="SIGNAL", seed=0):
    from PIL import ImageFont
    rnd = random.Random(seed)
    lines = text.upper().split("\n")
    f = gfx.font("Black", 92)
    fm = ImageFont.truetype(MONO, 22)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lw = [tmp.textlength(l, font=f) for l in lines]
    lh = 104
    bw = int(max(lw) + 90); bh = int(lh * len(lines) + 70)
    x0 = 100 if pos == "left" else W - 100 - bw
    y0 = 150
    n = round(dur * FPS)
    total_chars = sum(len(l) for l in lines)
    # per-char resolve time (staggered)
    resolve = []
    k = 0
    for l in lines:
        resolve.append([0.12 + 0.42 * ((k + i) / max(1, total_chars - 1)) + rnd.uniform(0, 0.06) for i in range(len(l))])
        k += len(l)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out], stdin=subprocess.PIPE)
    for fi in range(n):
        t = fi / FPS; te = dur - t
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        ko = eo(t / 0.22)
        cx, cy = x0 + bw / 2, y0 + bh / 2
        hw, hh = bw / 2 * (0.2 + 0.8 * ko), bh / 2 * (0.3 + 0.7 * ko)
        # glass panel
        if ko > 0.3:
            a = int(150 * seg(t, 0.06, 0.25))
            d.rectangle([cx - hw, cy - hh, cx + hw, cy + hh], fill=(8, 9, 12, int(a * 1.3)), outline=(255, 255, 255, int(a * 0.25)))
            for yy in range(int(cy - hh) + ((fi * 3) % 6), int(cy + hh), 6):  # moving scanlines
                d.line([(cx - hw, yy), (cx + hw, yy)], fill=(255, 255, 255, 10))
        # corner brackets
        L = 34; wdt = 4
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = cx + sx * hw, cy + sy * hh
                d.line([(px, py), (px - sx * L, py)], fill=ORANGE + (255,), width=wdt)
                d.line([(px, py), (px, py - sy * L)], fill=ORANGE + (255,), width=wdt)
        # mono label
        if t > 0.15:
            blink = "_" if int(t * 4) % 2 == 0 else " "
            d.text((x0 + 4, y0 - 34), f"// {idx:02d}  {label}{blink}", font=fm, fill=ORANGE + (230,))
        # text layer (decode)
        tl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tl)
        for li, l in enumerate(lines):
            x = x0 + 45; y = y0 + 35 + li * lh
            col = ORANGE if (li == len(lines) - 1 and len(lines) > 1) else WHITE
            for ci, ch in enumerate(l):
                rt = resolve[li][ci]
                if t < rt - 0.18: shown = None
                elif t < rt: shown = rnd.choice(GLYPHS) if ch != " " else " "
                else: shown = ch
                cw = td.textlength(ch, font=f)
                if shown:
                    c = col if shown == ch else (col[0], col[1], col[2])
                    alpha = 255 if shown == ch else 170
                    td.text((x, y), shown, font=f, fill=c + (alpha,))
                x += cw
        # chromatic aberration while decoding / on exit
        ab = 6 * (1 - seg(t, 0.35, 0.7)) + (10 * seg(-te, -0.3, 0) if te < 0.3 else 0)
        if ab > 0.5:
            arr = np.array(tl)
            r = np.roll(arr, int(ab), axis=1); b = np.roll(arr, -int(ab), axis=1)
            out_arr = arr.copy()
            out_arr[..., 0] = np.maximum(arr[..., 0], r[..., 0]); out_arr[..., 2] = np.maximum(arr[..., 2], b[..., 2])
            out_arr[..., 3] = np.maximum(arr[..., 3], np.maximum(r[..., 3], b[..., 3]) // 2)
            tl = Image.fromarray(out_arr)
        glow = tl.filter(ImageFilter.GaussianBlur(10))
        im.alpha_composite(glow.point(lambda v: v // 3) if False else glow)
        im.alpha_composite(tl)
        # underline sweep + travelling light pulse
        ku = eo(seg(t, 0.35, 0.75))
        if ku > 0:
            uy = cy + hh - 14
            d2 = ImageDraw.Draw(im)
            d2.rectangle([cx - hw + 20, uy, cx - hw + 20 + (bw - 40) * ku, uy + 4], fill=ORANGE + (255,))
            pp = ((t - 0.75) * 0.9) % 1.4
            if t > 0.75 and pp < 1:
                px = cx - hw + 20 + (bw - 40) * pp
                d2.ellipse([px - 26, uy - 6, px + 26, uy + 10], fill=(255, 220, 180, 160))
        # exit glitch
        if te < 0.3:
            arr = np.array(im); g = seg(-te, -0.3, 0)
            for _ in range(int(14 * g) + 1):
                y = rnd.randint(int(y0 - 40), int(y0 + bh)); hgt = rnd.randint(4, 30)
                arr[y:y + hgt] = np.roll(arr[y:y + hgt], rnd.randint(-120, 120), axis=1)
            arr[..., 3] = (arr[..., 3] * (1 - g ** 2)).astype(np.uint8)
            im = Image.fromarray(arr)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    return out

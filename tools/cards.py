"""Animated name cards: photo panel pops in on screen-right, name + role bars wipe in,
optional stamp (e.g. SUSPENDED) slams on, everything slides out at the end.

Rendered to a 1920x1080 RGBA .mov (PNG codec) that gets overlaid on the edit.
"""
import math, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import gfx

W, H, FPS = 1920, 1080, 24
ORANGE, DARK, WHITE = (255, 122, 26, 255), (14, 14, 16, 235), (255, 255, 255, 255)
RED = (229, 57, 53, 255)
PW, PH = 500, 620            # photo panel size
PX, PY = 1290, 120           # panel top-left (final)

# crop focus per photo: (centre x, top y, crop height), as fractions of the image
CROPS = {
    "coach_mouth.jpg": (0.51, 0.0, 1.0),
    "coach_head.jpg": (0.52, 0.0, 1.0),
    "issam_270.jpg": (0.5, 0.0, 1.0),
    "issam_race.jpg": (0.53, 0.0, 0.74),
    "hodge_flag.jpg": (0.51, 0.0, 1.0),
    "athlete_walk.jpg": (0.5, 0.0, 1.0),
}

def ease_out_back(t, s=1.70158):
    t = min(max(t, 0), 1) - 1; return t * t * ((s + 1) * t + s) + 1
def ease_out(t):
    t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def ease_in(t):
    t = min(max(t, 0), 1); return t ** 3

def crop_photo(path, name):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    cx, ty, hf = CROPS.get(name, (0.5, 0, 1))
    ch = int(im.height * hf); cw = int(ch * PW / PH)
    if cw > im.width: cw = im.width; ch = int(cw * PH / PW)
    x = int(min(max(0, cx * im.width - cw / 2), im.width - cw)); y = int(ty * im.height)
    return im.crop((x, y, x + cw, y + ch))

def panel(photo, zoom):
    """Photo panel with white border at a given ken-burns zoom."""
    w, h = photo.size; z = 1 + 0.06 * zoom
    cw, ch = int(w / z), int(h / z)
    p = photo.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch)).resize((PW, PH), Image.LANCZOS)
    out = Image.new("RGBA", (PW + 16, PH + 16), WHITE); out.paste(p, (8, 8))
    return out

def bar(text, fnt, fill, color, pad=28, h=None):
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = int(tmp.textlength(text, font=fnt)); bh = h or int(fnt.size * 1.45)
    b = Image.new("RGBA", (tw + pad * 2, bh), fill)
    ImageDraw.Draw(b).text((pad, bh / 2), text, font=fnt, fill=color, anchor="lm")
    return b

def stamp_img(text, small=None, color=RED):
    f = gfx.font("Black", 70); fs = gfx.font("Bold", 26)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    tw = int(tmp.textlength(text, font=f)); w = tw + 70; h = 120 if not small else 150
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10 + w, 10 + h], radius=14, outline=color, width=8, fill=(255, 255, 255, 190))
    if small: d.text((10 + w / 2, 42), small, font=fs, fill=color, anchor="mm")
    d.text((10 + w / 2, 10 + h - 55 if small else 10 + h / 2), text, font=f, fill=color, anchor="mm")
    return im.rotate(12, expand=True, resample=Image.BICUBIC)

def shadow_of(img, r=18, a=160):
    al = img.split()[-1].filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(a, v))
    s = Image.new("RGBA", img.size, (0, 0, 0, 0)); s.putalpha(al); return s

def render(card, out_path):
    """card: dict(photo, path, name, sub, dur, stamp=(text, small, t, color) | None, credit=None)"""
    photo = crop_photo(card["path"], card["photo"])
    n = round(card["dur"] * FPS)
    name_bar = bar(card["name"].upper(), gfx.font("Black", 60), ORANGE, (18, 18, 18, 255))
    sub_bar = bar(card["sub"].upper(), gfx.font("SemiBold", 28), DARK, WHITE)
    st = card.get("stamp")
    st_img = stamp_img(st[0], st[1], st[3] if len(st) > 3 else RED) if st else None
    credit = bar(card["credit"], gfx.font("Medium", 20), (0, 0, 0, 160), (230, 230, 230, 255), pad=12) if card.get("credit") else None
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", out_path], stdin=subprocess.PIPE)
    exit_d = 0.35
    for i in range(n):
        t = i / FPS; te = card["dur"] - t
        ex = ease_in(1 - te / exit_d) if te < exit_d else 0     # exit progress
        dx = int(760 * ex)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # orange accent block behind panel
        a1 = ease_out((t - 0.08) / 0.35)
        if a1 > 0:
            blk = Image.new("RGBA", (PW + 16, PH + 16), ORANGE)
            ox = PX + 22 + int((1 - a1) * 300) + dx
            frame.alpha_composite(blk, (ox, PY + 22))
        # photo panel: pop with overshoot + small rotation settle
        p = ease_out_back(t / 0.45)
        if t > 0:
            pan = panel(photo, t / card["dur"])
            sc = 0.6 + 0.4 * p; rot = -8 + 6 * ease_out(t / 0.45)
            pw, ph = int(pan.width * sc), int(pan.height * sc)
            pr = pan.resize((max(1, pw), max(1, ph)), Image.BILINEAR).rotate(rot, expand=True, resample=Image.BICUBIC)
            alpha = min(1, t / 0.15)
            if alpha < 1: pr.putalpha(pr.split()[-1].point(lambda v: int(v * alpha)))
            cx, cy = PX + (PW + 16) // 2 + dx, PY + (PH + 16) // 2 + int((1 - ease_out(t / 0.45)) * 60)
            frame.alpha_composite(shadow_of(pr), (cx - pr.width // 2, cy - pr.height // 2 + 10))
            frame.alpha_composite(pr, (cx - pr.width // 2, cy - pr.height // 2))
            if credit and t > 0.45:
                frame.alpha_composite(credit, (PX + 8 + dx, PY + PH - credit.height))
        # name + role bars wipe in from the left edge of the panel
        for b, t0, y in ((name_bar, 0.30, PY + PH - 40), (sub_bar, 0.46, PY + PH - 40 + name_bar.height)):
            k = ease_out((t - t0) / 0.30)
            if k <= 0: continue
            vis = b.crop((0, 0, max(1, int(b.width * k)), b.height))
            x = PX - 40 + dx
            frame.alpha_composite(shadow_of(vis, 10, 120), (x, y + 6)); frame.alpha_composite(vis, (x, y))
        # stamp slam
        if st_img is not None and t >= st[2]:
            k = min(1, (t - st[2]) / 0.16); sc = 2.0 - 1.0 * ease_out(k)
            si = st_img.resize((int(st_img.width * sc), int(st_img.height * sc)), Image.BILINEAR)
            if k < 1: si.putalpha(si.split()[-1].point(lambda v: int(v * k)))
            sx = PX + (PW + 16) // 2 - si.width // 2 + dx; sy = PY + int(PH * 0.55) - si.height // 2
            frame.alpha_composite(si, (sx, sy))
        if ex > 0:
            frame.putalpha(frame.split()[-1].point(lambda v: int(v * (1 - ex * 0.6))))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close(); proc.wait()
    return out_path

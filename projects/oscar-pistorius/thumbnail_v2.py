"""Oscar Pistorius thumbnail v2: same layout as the Drummond thumbnail the user actually published
("HE WOULDN'T LEAVE."): one real moment full-bleed, a short white black-italic statement top-left on a dark
corner, one real inset photo in a white border bottom-left. No cut-outs, glows, rays or arrows.

Sources (real):
- A/C main: The New York Times 1080p courtroom footage, 12 Sep 2014: Pistorius standing in the dock as
  Judge Masipa reads the verdict, police officer in hi-vis behind him (nyt_verdict @ 39 s).
- B main: Eyewitness News 1080p, Pistorius walking out through police and cameras (ewn_due_release @ 18.5 s),
  cropped above the burned-in subtitles.
- Inset: Wikimedia Commons, "Oscar Pistorius, the first round of the 400m at the London 2012 Olympic Games"
  (Jim Thurston, CC BY-SA 2.0): him sprinting on blades, PISTORIUS bib.
Reeva Steenkamp is not used. No weapon, door or crime-scene imagery.
Run: python3 -I projects/oscar-pistorius/thumbnail_v2.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad"
SRC = f"{SCR}/thumb2"
PH = f"{SCR}/pistorius/photos"
W, H = 2560, 1440
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf"

def grade(im, c=1.10, s=1.10, sharp=90):
    im = im.filter(ImageFilter.UnsharpMask(radius=2.0, percent=sharp, threshold=2))
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(c)).enhance(s)

def main_image(name, box, pad=0):
    """pad: push the frame down by this many px; the band above is a dark extension of the frame's top rows."""
    im = Image.open(f"{SRC}/{name}.png").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
    im = grade(im)
    if pad:
        top = im.crop((0, 0, W, 60)).resize((W, pad + 60)).filter(ImageFilter.GaussianBlur(30))
        top = ImageEnhance.Brightness(top).enhance(0.45)
        can = Image.new("RGB", (W, H)); can.paste(top, (0, 0))
        band = Image.new("L", (W, 120)); band.putdata([int(255 * y / 119) for y in range(120) for _ in range(W)])
        can.paste(im.crop((0, 0, W, H - pad)), (0, pad))
        can.paste(top.crop((0, pad - 60, W, pad + 60)), (0, pad - 60), Image.eval(band, lambda v: 255 - v))
        im = can
    a = np.asarray(im, np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # dark corner top-left for the text (like the reference), light vignette elsewhere
    dark = np.clip(1 - np.hypot(xx / (W * 0.62), yy / (H * 0.62)), 0, 1) ** 1.3
    a *= (1 - 0.78 * dark)[..., None]
    vig = 1 - 0.28 * np.clip(((xx - W * 0.6) / (W * 0.75)) ** 2 + ((yy - H * 0.5) / (H * 0.85)) ** 2, 0, 1)
    a *= vig[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def inset(path, crop, w, border=10):
    ph = Image.open(path).convert("RGB")
    ph = grade(ph.crop(crop), 1.08, 1.12, 70)
    h = round(w * ph.height / ph.width)
    ph = ph.resize((w, h), Image.LANCZOS)
    card = Image.new("RGBA", (w + 2 * border, h + 2 * border), (255, 255, 255, 255))
    card.paste(ph, (border, border))
    return card

def shadow(base, layer, xy, off=(0, 18), blur=26, a=190):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.split()[-1].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * a // 255))
    base.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1]))

def headline(base, lines, x, y, size, maxw=1500):
    f = ImageFont.truetype(FONT, size)
    while max(f.getlength(l) for l in lines) > maxw: size -= 4; f = ImageFont.truetype(FONT, size)
    for ln in lines:
        lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        bb = f.getbbox(ln)
        d.text((x, y - bb[1]), ln, font=f, fill=(255, 255, 255, 255))
        shadow(base, lay, (0, 0), off=(0, 10), blur=18, a=170)
        base.alpha_composite(lay)
        y += int(size * 0.98)

def build(main, box, lines, size, pad=0, maxw=1500):
    can = main_image(main, box, pad)
    headline(can, lines, 110, 80, size, maxw)
    ins = inset(f"{PH}/Oscar_Pistorius_the_first_round_of_the_400m_at_the_London_20.jpg", (250, 40, 1210, 740), 860)
    x, y = 120, H - ins.height - 80
    shadow(can, ins, (x, y))
    can.alpha_composite(ins, (x, y))
    out = can.convert("RGB")
    g = np.random.default_rng(9).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(np.asarray(out, np.float32) + g, 0, 255).astype(np.uint8))

DOCK = ("n2", (0, 0, 1440, 810))      # Pistorius in the dock, officer behind; NYT logo cropped out
CROWD = ("e2", (0, 40, 1400, 828))     # walking out through police and cameras; subtitles cropped out
VARIANTS = {
    "A": (DOCK, ["HE SAID IT WAS", "AN ACCIDENT."], 300, 300, 1500),
    "B": (CROWD, ["HE SAID IT WAS", "AN ACCIDENT."], 300, 0, 1230),
    "C": (DOCK, ["HE THOUGHT SHE", "WAS AN INTRUDER."], 300, 300, 1500),
}

if __name__ == "__main__":
    for k, ((name, box), lines, size, pad, maxw) in VARIANTS.items():
        im = build(name, box, lines, size, pad, maxw)
        im.save(f"{SCR}/thumb2/pistorius_thumb_v2_{k}_full.png")
        im.resize((1280, 720), Image.LANCZOS).save(f"{SCR}/thumb2/pistorius_thumb_v2_{k}.jpg", quality=94)
        print(k)

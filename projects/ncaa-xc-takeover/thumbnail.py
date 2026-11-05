"""Thumbnail v1 (1280x720): Lemngole cut-out (Commons, CC BY-SA 4.0), a real comment as the proof element, 2 huge words.
Run: python3 -I projects/ncaa-xc-takeover/thumbnail.py OUT.jpg"""
import sys
sys.path.insert(0, "/home/user/YouTube-/tools")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import gfx, neon as N

SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
W, H = 1920, 1080
N.TAG = "XC//FILE"
im = N.background(3.0).convert("RGB")
a = np.asarray(im).astype(np.float32) * 0.8
im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")

# subject cut-out with neon rim
cut = Image.open(f"{SCR}/photos/cut_lemngole.png").convert("RGBA")
s = 1180 / cut.height; cut = cut.resize((int(cut.width * s), 1180), Image.LANCZOS)
x0, y0 = W - cut.width + 120, H - cut.height + 160
alpha = cut.split()[-1]
for col, blur, k in ((N.CYAN, 26, 2), (N.ORANGE, 8, 1)):
    g = Image.new("RGBA", cut.size, col + (0,)); g.putalpha(alpha.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(blur)))
    for _ in range(k): im.alpha_composite(g, (x0, y0))
im.alpha_composite(cut, (x0, y0))

d = ImageDraw.Draw(im)
# proof: real comment card
cx, cy, cw, ch = 70, 610, 900, 250
card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); dc = ImageDraw.Draw(card)
dc.rounded_rectangle([0, 0, cw - 1, ch - 1], 22, fill=(20, 20, 24, 245), outline=N.PINK + (255,), width=5)
dc.ellipse([30, 34, 100, 104], fill=(70, 72, 84)); dc.rounded_rectangle([125, 46, 360, 76], 8, fill=(60, 62, 72))
f = gfx.font("Bold", 50)
dc.text((125, 100), "Should only be open to", font=f, fill=(255, 255, 255))
dc.text((125, 160), "Americans. Not guests.", font=f, fill=(255, 255, 255))
card = card.rotate(3, expand=True, resample=Image.BICUBIC)
im.alpha_composite(card, (cx, cy))

# 2 huge words with glow
txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(txt)
F = gfx.font("Black", 230)
dt.text((70, 40), "WHAT", font=F, fill=(255, 255, 255, 255))
dt.text((70, 290), "RULE?", font=F, fill=N.ORANGE + (255,))
glow = txt.filter(ImageFilter.GaussianBlur(18))
im.alpha_composite(glow); im.alpha_composite(txt)

# red circle around the comment + arrow from the words
d = ImageDraw.Draw(im)
d.ellipse([40, 585, 1010, 905], outline=(255, 40, 40), width=12)
d.line([(820, 540), (900, 600)], fill=(255, 40, 40), width=14)
d.polygon([(915, 615), (870, 600), (900, 570)], fill=(255, 40, 40))
im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(sys.argv[1], quality=93)
print("wrote", sys.argv[1])

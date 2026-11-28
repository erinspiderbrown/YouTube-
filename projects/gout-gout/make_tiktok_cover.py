"""TikTok cover (1080x1920) from the user's magnifier thumbnail: crop on the magnifier + Gout, scaled big in the middle,
the photo's own sky/track blurred to fill, title in the top third (cream heavy italic like the house style)."""
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
import numpy as np
T = Image.open("thumbnail_user_magnifier.png").convert("RGB"); W, H = T.size
# crop: from the magnifier's left edge to the right edge (magnifier + Gout), full height
cx1 = int(W * 0.33); crop = T.crop((cx1, 0, W, H))
s = 1080 / crop.width; crop = crop.resize((1080, int(crop.height * s)), Image.LANCZOS)
bg = T.resize((int(W * 1920 / H), 1920), Image.LANCZOS); bx = (bg.width - 1080) // 2
bg = bg.crop((bx, 0, bx + 1080, 1920)).filter(ImageFilter.GaussianBlur(34)); bg = ImageEnhance.Brightness(bg).enhance(0.62)
C = bg.copy(); y0 = 820
m = Image.new("L", crop.size, 255); d = ImageDraw.Draw(m)
for i in range(120): d.line([(0, i), (crop.width, i)], fill=int(255 * i / 120)); d.line([(0, crop.height - 1 - i), (crop.width, crop.height - 1 - i)], fill=int(255 * i / 120))
C.paste(crop, (0, y0), m)
F = ImageFont.truetype("/home/user/YouTube-/tools/fonts/Montserrat-ExtraBoldItalic.ttf", 108)
F2 = ImageFont.truetype("/home/user/YouTube-/tools/fonts/Montserrat-ExtraBoldItalic.ttf", 64)
dr = ImageDraw.Draw(C)
lines = [("INVESTIGATING", F2, (255, 255, 255)), ("AUSTRALIA'S", F, (250, 240, 214)), ("FASTEST MAN", F, (250, 240, 214)), ("EVER", F, (255, 196, 40))]
y = 260
sh = Image.new("L", C.size, 0); ds = ImageDraw.Draw(sh)
pos = []
for t, f, col in lines:
    bb = dr.textbbox((0, 0), t, font=f); w = bb[2] - bb[0]; x = (1080 - w) // 2 - bb[0]
    pos.append((x, y, t, f, col)); ds.text((x + 5, y + 9), t, font=f, fill=210); y += (bb[3] - bb[1]) + 34
C.paste(Image.new("RGB", C.size, (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
for x, y, t, f, col in pos: dr.text((x, y), t, font=f, fill=col)
nz = np.random.default_rng(1).normal(0, 2.0, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + nz, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(crop.size)

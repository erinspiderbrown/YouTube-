"""TikTok cover (1080x1920) from the user's own 'this is BAD' thumbnail: same photo, face cropped tall,
its dark background extended upward, and the thumbnail's own 'this is BAD' type moved into the top third."""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
T = Image.open("thumbnail_user_this_is_bad.png").convert("RGB"); W, H = T.size
body = T.crop((int(W * 0.475), 0, W, H)); s = 1080 / body.width; body = body.resize((1080, int(body.height * s)), Image.LANCZOS)
bg = T.crop((0, 0, int(W * 0.04), int(H * 0.12))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
C = bg.copy(); y0 = 1920 - body.height
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(260): d.line([(0, i), (body.width, i)], fill=int(255 * i / 260))
C.paste(body, (0, y0), m)
txt = T.crop((int(W * 0.025), int(H * 0.19), int(W * 0.452), int(H * 0.75))); k = 900 / txt.width
txt = txt.resize((900, int(txt.height * k)), Image.LANCZOS)
hsv = txt.convert("HSV"); sat = hsv.split()[1]; val = txt.convert("L")
tm = Image.eval(Image.merge("RGB", (val, sat, sat)).convert("L"), lambda v: 0)
import numpy as np
a = np.asarray(txt).astype(int); white = (a.min(2) > 150); red = (a[..., 0] > 150) & (a[..., 1] < 90)
mk = Image.fromarray(((white | red) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
sh = Image.new("RGB", txt.size, (0, 0, 0)); C.paste(sh, (98, 212), mk.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.7)))
C.paste(txt, (90, 200), mk)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(60 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
C.save("tiktok_cover.jpg", quality=93); print(y0, body.size, txt.size)

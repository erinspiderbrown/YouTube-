"""TikTok cover (1080x1920) from the user's 'youngest ever' thumbnail: same photo cropped to Sam, its own dark crowd
background extended upward, the thumbnail's own 'youngest ever' type moved into the top third."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, cv2
T0 = Image.open("thumbnail_user_youngest_ever.png").convert("RGB"); W, H = T0.size
a0 = np.asarray(T0); mm = np.zeros(a0.shape[:2], np.uint8)
x1, x2, y1, y2 = int(W * 0.03), int(W * 0.49), int(H * 0.26), int(H * 0.40)
reg = a0[y1:y2, x1:x2].astype(int); mm[y1:y2, x1:x2] = (reg.min(2) > 150) * 255
mm = cv2.dilate(mm, np.ones((11, 11), np.uint8))
T = Image.fromarray(cv2.inpaint(a0, mm, 9, cv2.INPAINT_TELEA))
body = T.crop((int(W * 0.30), 0, int(W * 0.93), H)); body = body.resize((1080, int(body.height * 1080 / body.width)), Image.LANCZOS)
y0 = 1920 - body.height
bg = T.crop((0, 0, int(W * 0.25), int(H * 0.2))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(45))
C = bg.copy(); m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(300): d.line([(0, i), (body.width, i)], fill=int(255 * i / 300))
C.paste(body, (0, y0), m)
txt = T0.crop((x1, y1, x2, y2)); k = 980 / txt.width; txt = txt.resize((980, int(txt.height * k)), Image.LANCZOS)
a = np.asarray(txt).astype(int); mk = Image.fromarray(((a.min(2) > 160) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.0))
tx, ty = 50, 300
C.paste(Image.new("RGB", txt.size, (0, 0, 0)), (tx + 8, ty + 12), mk.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.75)))
C.paste(txt, (tx, ty), mk)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(70 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
n = np.random.default_rng(1).normal(0, 4, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + n, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(y0, txt.size)

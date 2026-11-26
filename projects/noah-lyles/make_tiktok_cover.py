"""TikTok cover (1080x1920) from the user's 'This is really bad' thumbnail: the same photo cropped tight on Noah's face,
its own dark track background extended above and below, the thumbnail's own text + red underline moved into the top third."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, cv2
T0 = Image.open("thumbnail_user_really_bad.png").convert("RGB"); W, H = T0.size
a0 = np.asarray(T0).astype(int)
x1, x2, y1, y2 = int(W * 0.60), int(W * 0.985), int(H * 0.585), int(H * 0.715)
reg = a0[y1:y2, x1:x2]
white = reg.min(2) > 150
red = (reg[..., 0] > 140) & (reg[..., 1] < 90) & (reg[..., 2] < 100)
tm = ((white | red) * 255).astype("uint8")
mm = np.zeros(a0.shape[:2], np.uint8); mm[y1:y2, x1:x2] = cv2.dilate(tm, np.ones((13, 13), np.uint8))
T = Image.fromarray(cv2.inpaint(a0.astype("uint8"), mm, 9, cv2.INPAINT_TELEA))
cx1, cx2 = int(W * 0.16), int(W * 0.72)
body = T.crop((cx1, 0, cx2, H)); body = body.resize((1080, int(body.height * 1080 / body.width)), Image.LANCZOS)
y0 = 470
bg = T.crop((int(W * 0.70), int(H * 0.05), int(W * 0.98), int(H * 0.45))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
bot = T.crop((cx1, int(H * 0.80), cx2, H)).resize((1080, 1920 - y0 - body.height + 200), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
C = bg.copy(); C.paste(bot, (0, y0 + body.height - 200))
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(260): d.line([(0, i), (body.width, i)], fill=int(255 * i / 260))
for i in range(200): d.line([(0, body.height - 1 - i), (body.width, body.height - 1 - i)], fill=int(255 * i / 200))
C.paste(body, (0, y0), m)
txt = T0.crop((x1, y1, x2, y2)); k = 1000 / txt.width; txt = txt.resize((1000, int(txt.height * k)), Image.LANCZOS)
mk = Image.fromarray(tm).resize(txt.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
tx, ty = 40, 230
C.paste(Image.new("RGB", txt.size, (0, 0, 0)), (tx + 6, ty + 10), mk.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.8)))
C.paste(txt, (tx, ty), mk)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(70 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
n = np.random.default_rng(1).normal(0, 3.5, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + n, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(body.size, txt.size)

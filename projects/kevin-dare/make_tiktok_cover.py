"""TikTok cover (1080x1920) from the user's 'dead at 19' thumbnail: same photo cropped on Kevin, its own dark background
extended above and below, the thumbnail's own 'dead at 19' + red line moved into the top third."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, cv2
T0 = Image.open("thumbnail_user_dead_at_19.png").convert("RGB"); W, H = T0.size
a0 = np.asarray(T0).astype(int)
x1, x2, y1, y2 = int(W * 0.43), int(W * 0.97), int(H * 0.26), int(H * 0.52)
reg = a0[y1:y2, x1:x2]
white = reg.min(2) > 150
red = (reg[..., 0] > 70) & (reg[..., 0] > reg[..., 1] * 1.6) & (reg[..., 0] > reg[..., 2] * 1.6)
tm = ((white | red) * 255).astype("uint8")
mm = np.zeros(a0.shape[:2], np.uint8); mm[y1:y2, x1:x2] = cv2.dilate(tm, np.ones((13, 13), np.uint8))
xr = int(W * 0.38); rr = a0[y1:y2, xr:x1]; mm[y1:y2, xr:x1] |= ((rr[..., 0] > 60) & (rr[..., 0] > rr[..., 1] * 1.4)).astype("uint8") * 255
mm = cv2.dilate(mm, np.ones((9, 9), np.uint8))
T = Image.fromarray(cv2.inpaint(a0.astype("uint8"), mm, 9, cv2.INPAINT_TELEA))
cx1, cx2 = int(W * 0.04), int(W * 0.68)
body = T.crop((cx1, 0, cx2, H)); body = body.resize((1080, int(body.height * 1080 / body.width)), Image.LANCZOS)
y0 = 560
bg = T.crop((int(W * 0.70), int(H * 0.05), int(W * 0.98), int(H * 0.40))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
C = bg.copy()
bot = T.crop((cx1, int(H * 0.82), cx2, H)).resize((1080, 1920 - y0 - body.height + 220), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
C.paste(bot, (0, y0 + body.height - 220))
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(240): d.line([(0, i), (body.width, i)], fill=int(255 * i / 240))
for i in range(220): d.line([(0, body.height - 1 - i), (body.width, body.height - 1 - i)], fill=int(255 * i / 220))
C.paste(body, (0, y0), m)
txt = T0.crop((x1, y1, x2, y2)); k = 980 / txt.width; txt = txt.resize((980, int(txt.height * k)), Image.LANCZOS)
mk = Image.fromarray(tm).resize(txt.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
tx, ty = 50, 260
C.paste(Image.new("RGB", txt.size, (0, 0, 0)), (tx + 6, ty + 10), mk.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.8)))
C.paste(txt, (tx, ty), mk)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(70 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
n = np.random.default_rng(1).normal(0, 3.0, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + n, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(body.size, txt.size)
# clean the last sliver of the thumbnail's red line that sits beside his neck
Cf = np.asarray(Image.open("tiktok_cover.jpg")).copy(); b = Cf[990:1070, 620:860].astype(int)
mk2 = np.zeros(Cf.shape[:2], np.uint8)
mk2[990:1070, 620:860] = (((b[..., 0] - np.maximum(b[..., 1], b[..., 2])) > 10) * 255).astype("uint8")
mk2 = cv2.dilate(mk2, np.ones((9, 9), np.uint8))
Image.fromarray(cv2.inpaint(Cf, mk2, 9, cv2.INPAINT_TELEA)).save("tiktok_cover.jpg", quality=93)

"""TikTok cover (1080x1920) from the user's 'How Is This Possible?' thumbnail: same photo cropped to Cooper,
its own dark stadium background extended upward, and the thumbnail's own title + red swoosh in the top third."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
T0 = Image.open("thumbnail_user_how_is_this_possible.png").convert("RGB"); W, H = T0.size
# remove the old title from the photo (it would show beside Cooper): inpaint the text + swoosh pixels
import cv2
a0 = np.asarray(T0); mm = np.zeros(a0.shape[:2], np.uint8)
x1, x2, y1, y2 = int(W * 0.02), int(W * 0.47), int(H * 0.15), int(H * 0.53)
reg = a0[y1:y2, x1:x2].astype(int)
mm[y1:y2, x1:x2] = ((reg.min(2) > 110) | ((reg[..., 0] > 120) & (reg[..., 1] < 90))) * 255
mm[:, int(W * 0.465):] = 0; mm[int(H * 0.435):, int(W * 0.41):] = 0
mm = cv2.dilate(mm, np.ones((9, 9), np.uint8))
T = Image.fromarray(cv2.inpaint(a0, mm, 9, cv2.INPAINT_TELEA)).filter(ImageFilter.GaussianBlur(0))
body = T.crop((int(W * 0.31), 0, int(W * 0.955), H)); s = 1080 / body.width
body = body.resize((1080, int(body.height * s)), Image.LANCZOS)
y0 = 1920 - body.height
# background: the photo's own top band, stretched and blurred
band = T.crop((0, 0, int(W * 0.28), int(H * 0.12)))
bg = band.resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(45))
C = bg.copy()
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(300): d.line([(0, i), (body.width, i)], fill=int(255 * i / 300))
C.paste(body, (0, y0), m)
# title + swoosh lifted from the thumbnail
txt = T0.crop((int(W * 0.035), int(H * 0.17), int(W * 0.452), int(H * 0.51))); k = 960 / txt.width
txt = txt.resize((960, int(txt.height * k)), Image.LANCZOS)
a = np.asarray(txt).astype(int)
white = a.min(2) > 170; red = (a[..., 0] > 150) & (a[..., 1] < 80) & (a[..., 2] < 80)
sel = white | red; yy, xx = np.mgrid[0:sel.shape[0], 0:sel.shape[1]]
sel &= ~((yy / k + H * 0.17 > H * 0.435) & (xx / k + W * 0.035 > W * 0.41))
mk = Image.fromarray((sel * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.0))
tx, ty = 60, 230
C.paste(Image.new("RGB", txt.size, (0, 0, 0)), (tx + 8, ty + 12), mk.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.75)))
C.paste(txt, (tx, ty), mk)
# grade: vignette + light grain
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(70 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
n = (np.random.default_rng(1).normal(0, 4, (1920, 1080, 1))).astype(int)
C = Image.fromarray(np.clip(np.asarray(C).astype(int) + n, 0, 255).astype("uint8"))
C.save("tiktok_cover.jpg", quality=93); print(y0, body.size, txt.size)

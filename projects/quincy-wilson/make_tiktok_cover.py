"""TikTok cover (1080x1920) from the user's '16 years old' thumbnail: same photo cropped on Quincy, its own purple track
extended above and below, the thumbnail's own '16 years old' + arrow moved into the top third."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np, cv2
T0 = Image.open("thumbnail_user_16_years_old.png").convert("RGB"); W, H = T0.size
a0 = np.asarray(T0).astype(int)
x1, x2, y1, y2 = int(W * 0.645), int(W * 0.975), int(H * 0.14), int(H * 0.30)
reg = a0[y1:y2, x1:x2]
tm = ((reg.min(2) > 200) * 255).astype("uint8")
mm = np.zeros(a0.shape[:2], np.uint8); mm[y1:y2, x1:x2] = cv2.dilate(tm, np.ones((11, 11), np.uint8))
T = Image.fromarray(cv2.inpaint(a0.astype("uint8"), mm, 9, cv2.INPAINT_TELEA))
cx1, cx2 = int(W * 0.30), int(W * 0.88)
body = T.crop((cx1, 0, cx2, H)); body = body.resize((1080, int(body.height * 1080 / body.width)), Image.LANCZOS)
y0 = 560
bg = T.crop((int(W * 0.05), int(H * 0.0), int(W * 0.30), int(H * 0.25))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
C = bg.copy()
bot = T.crop((cx1, int(H * 0.82), cx2, H)).resize((1080, max(10, 1920 - y0 - body.height + 220)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
C.paste(bot, (0, y0 + body.height - 220))
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(240): d.line([(0, i), (body.width, i)], fill=int(255 * i / 240))
for i in range(220): d.line([(0, body.height - 1 - i), (body.width, body.height - 1 - i)], fill=int(255 * i / 220))
C.paste(body, (0, y0), m)
# the thumbnail's own words, redrawn crisp in a matching rounded bold sans, plus its white arrow (curving to his head)
from PIL import ImageFont
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 150)
txt = "16 years old"; bb = ImageDraw.Draw(C).textbbox((0, 0), txt, font=F); tw = bb[2] - bb[0]
tx, ty = (1080 - tw) // 2 - bb[0], 250
sh = Image.new("L", C.size, 0); ImageDraw.Draw(sh).text((tx + 4, ty + 10), txt, font=F, fill=180)
C.paste(Image.new("RGB", C.size, (25, 15, 60)), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
ImageDraw.Draw(C).text((tx, ty), txt, font=F, fill=(255, 255, 255))
S = 4; L = Image.new("L", (1080 * S, 1920 * S), 0); dl = ImageDraw.Draw(L)
p0, p1, p2 = np.array([800, 455]), np.array([850, 560]), np.array([668, 618])
pts = [tuple(((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2) * S) for t in np.linspace(0, 0.9, 40)]
dl.line(pts, fill=255, width=9 * S, joint="curve")
d = p2 - (0.81 * p0 + 0.18 * p1 + 0.01 * p2 + 0 * p2); d = (p2 - np.array(pts[-1]) / S); d = d / np.linalg.norm(d); n = np.array([-d[1], d[0]])
tip = p2 + d * 6; base = p2 - d * 34
dl.polygon([tuple(tip * S), tuple((base + n * 22) * S), tuple((base - n * 22) * S)], fill=255)
L = L.resize((1080, 1920), Image.LANCZOS)
C.paste(Image.new("RGB", C.size, (25, 15, 60)), (3, 6), L.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.6)))
C.paste(Image.new("RGB", C.size, (255, 255, 255)), (0, 0), L)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(60 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
n = np.random.default_rng(1).normal(0, 2.5, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + n, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(body.size)

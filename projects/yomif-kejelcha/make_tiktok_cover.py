"""TikTok cover (1080x1920) from the user's 'STILL LOST.' thumbnail: the same photo cropped on Kejelcha (Sawe still
behind him), its own blurred crowd extended above, 'STILL LOST.' redrawn crisp in the top third + the white arrow."""
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import numpy as np, cv2
T0 = Image.open("thumbnail_user_still_lost.png").convert("RGB"); W, H = T0.size
a0 = np.asarray(T0).astype(int)
# remove the thumbnail's own text + arrow (top-right) by inpainting the bright cream/white pixels there
x1, x2, y1, y2 = int(W * 0.43), int(W * 0.86), int(H * 0.08), int(H * 0.28)
reg = a0[y1:y2, x1:x2]; tm = ((reg.min(2) > 190) * 255).astype("uint8")
mm = np.zeros(a0.shape[:2], np.uint8); mm[y1:y2, x1:x2] = cv2.dilate(tm, np.ones((13, 13), np.uint8))
T = Image.fromarray(cv2.inpaint(a0.astype("uint8"), mm, 11, cv2.INPAINT_TELEA))
cx1, cx2 = int(W * 0.12), int(W * 0.76)          # Kejelcha + Sawe behind
body = T.crop((cx1, 0, cx2, H)); body = body.resize((1080, int(body.height * 1080 / body.width)), Image.LANCZOS)
y0 = 1920 - body.height
bg = T.crop((cx1, 0, cx2, int(H * 0.30))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
C = bg.copy()
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(300): d.line([(0, i), (body.width, i)], fill=int(255 * i / 300))
C.paste(body, (0, y0), m)
# title, same look: cream heavy italic, soft shadow
F = ImageFont.truetype("/home/user/YouTube-/tools/fonts/Montserrat-ExtraBoldItalic.ttf", 150)
txt = "STILL LOST."; bb = ImageDraw.Draw(C).textbbox((0, 0), txt, font=F); tw = bb[2] - bb[0]
tx, ty = (1080 - tw) // 2 - bb[0], 520
sh = Image.new("L", C.size, 0); ImageDraw.Draw(sh).text((tx + 5, ty + 10), txt, font=F, fill=200)
C.paste(Image.new("RGB", C.size, (10, 10, 10)), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
ImageDraw.Draw(C).text((tx, ty), txt, font=F, fill=(250, 240, 214))
# white arrow from the title down toward his head
S = 4; L = Image.new("L", (1080 * S, 1920 * S), 0); dl = ImageDraw.Draw(L)
fy = y0 + int(0.12 * body.height)        # around his hair line
p0, p1, p2 = np.array([760, ty + 200]), np.array([740, ty + 300]), np.array([600, fy + 30])
pts = [tuple(((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2) * S) for t in np.linspace(0, 0.9, 40)]
dl.line(pts, fill=255, width=10 * S, joint="curve")
dv = p2 - np.array(pts[-1]) / S; dv = dv / np.linalg.norm(dv); n = np.array([-dv[1], dv[0]])
tip = p2 + dv * 8; base = p2 - dv * 40
dl.polygon([tuple(tip * S), tuple((base + n * 26) * S), tuple((base - n * 26) * S)], fill=255)
L = L.resize((1080, 1920), Image.LANCZOS)
C.paste(Image.new("RGB", C.size, (10, 10, 10)), (3, 6), L.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.5)))
C.paste(Image.new("RGB", C.size, (255, 255, 255)), (0, 0), L)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(55 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
nz = np.random.default_rng(1).normal(0, 2.5, (1920, 1080, 1)).astype(int)
Image.fromarray(np.clip(np.asarray(C).astype(int) + nz, 0, 255).astype("uint8")).save("tiktok_cover.jpg", quality=93); print(body.size, y0)

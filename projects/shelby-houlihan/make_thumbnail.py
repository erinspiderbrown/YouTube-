"""Shelby thumbnail (downfall style): user's photo (Topaz-upscaled, face unchanged), subject lowered so the
shocked eyes stay clear; text "THE BURRITO BAN." above her head (white italic / giant red block / white underlined)."""
import sys, numpy as np
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import thumb_downfall as T
W, H = 1920, 1080
ph = Image.open("shelby_face_up.png").convert("RGB")           # 2396x1596
s = 1620 / ph.height; ph = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)  # ~1981x1320
y0 = 250                                                            # push the photo down so text sits above the head
bg = ph.crop((0, 0, ph.width, 60)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
bg = ImageEnhance.Brightness(bg).enhance(0.55)
cv = bg.copy()
x0 = (W - ph.width) // 2
m = Image.new("L", ph.size, 255); m.paste(Image.linear_gradient("L").resize((ph.width, 140)), (0, 0))
cv.paste(ph, (x0, y0), m)
cv = T.grade_face(cv.convert("RGBA")).convert("RGB")
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
vig = 1 - 0.35 * (((x - W / 2) / W) ** 2 * 2 + ((y - H / 2) / H) ** 2 * 1.2)
cv = Image.fromarray((np.asarray(cv).astype(np.float32) * vig[..., None]).clip(0, 255).astype(np.uint8)).convert("RGBA")
big = T.text_img("BURRITO", T.BLOCK, 290, (235, 16, 22), 3, (120, 0, 0))
left = T.text_img("THE", T.ITAL, 140, (255, 255, 255)); right = T.text_img("BAN.", T.ITAL, 130, (255, 255, 255))
bx = (W - big.width) // 2 + (left.width - right.width) // 6; by = -18
T.paste_shadow(cv, big, (bx, by), 18, 0.85, (8, 12))
T.paste_shadow(cv, left, (bx - left.width + 20, by + int(big.height * 0.30)))
rx = bx + big.width - 20; ry = by + int(big.height * 0.36); T.paste_shadow(cv, right, (rx, ry))
d = ImageDraw.Draw(cv); x1, x2, yb = rx + 30, rx + right.width - 25, ry + right.height - 14
d.polygon([(x1, yb - 7), (x2, yb - 10), (x2 + 4, yb + 6), (x1 - 2, yb + 9)], fill=(250, 222, 30, 255))
out = cv.convert("RGB"); out.save("thumbnail_HD.jpg", quality=95)
out.resize((1280, 720), Image.LANCZOS).save("thumbnail.jpg", quality=93); print("ok")

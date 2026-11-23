"""TikTok cover 1080x1920 from the Shelby thumbnail photo (Topaz upscale, face unchanged): face mid-frame, top extended with the photo's dark stadium background, THE BURRITO BAN. in the top third."""
import sys, numpy as np
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import thumb_downfall as T
W, H = 1080, 1920
ph = Image.open("shelby_face_up.png").convert("RGB")      # 2396x1596
s = 2000 / ph.height; ph = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)   # ~3003x2000
x0 = -(ph.width - W) // 2; y0 = 640
bg = ph.crop((0, 0, ph.width, 80)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
cv = ImageEnhance.Brightness(bg).enhance(0.5)
m = Image.new("L", ph.size, 255); m.paste(Image.linear_gradient("L").resize((ph.width, 200)), (0, 0))
cv.paste(ph, (x0, y0), m)
cv = T.grade_face(cv.convert("RGBA")).convert("RGB")
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
vig = 1 - 0.4 * (((x - W / 2) / W) ** 2 * 2 + ((y - H / 2) / H) ** 2 * 1.2)
cv = Image.fromarray((np.asarray(cv).astype(np.float32) * vig[..., None]).clip(0, 255).astype(np.uint8)).convert("RGBA")
def center(t, y): T.paste_shadow(cv, t, ((W - t.width) // 2, y))
center(T.text_img("THE", T.ITAL, 150, (255, 255, 255)), 170)
center(T.text_img("BURRITO", T.BLOCK, 250, (235, 16, 22), 3, (120, 0, 0)), 320)
ban = T.text_img("BAN.", T.ITAL, 170, (255, 255, 255)); bx, byy = (W - ban.width) // 2, 610; T.paste_shadow(cv, ban, (bx, byy))
d = ImageDraw.Draw(cv); a, b, yb = bx + 30, bx + ban.width - 25, byy + ban.height - 14
d.polygon([(a, yb - 7), (b, yb - 10), (b + 4, yb + 6), (a - 2, yb + 9)], fill=(250, 222, 30, 255))
cv.convert("RGB").save("tiktok_cover.jpg", quality=95); print("ok")

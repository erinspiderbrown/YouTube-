"""Shelby thumbnail v2, modelled on the channel's best (Tuohy 'WHERE DID SHE GO?', Boling 'WHAT HAPPENED?'):
full real photo, subject right with USA flag + HOULIHAN bib visible, brighter grade, short cream condensed question left."""
import sys, numpy as np
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import thumb_downfall as T
W, H = 1920, 1080
ph = Image.open("shelby_face_up.png").convert("RGB")        # 2396x1596
s = 1140 / ph.height; ph = ph.resize((int(ph.width * s), int(ph.height * s)), Image.LANCZOS)   # ~1711x1140
x0 = W - ph.width + 170; y0 = -70
# background: the photo's own dark stadium, stretched from its left edge and blurred
left = ph.crop((0, 0, 160, ph.height)).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
cv = ImageEnhance.Brightness(left).enhance(0.9)
m = Image.new("L", ph.size, 255); m.paste(Image.linear_gradient("L").rotate(90, expand=True).resize((520, ph.height)), (0, 0))
cv.paste(ph, (x0, y0), m)
cv = ImageEnhance.Brightness(cv).enhance(1.12); cv = ImageEnhance.Contrast(cv).enhance(1.12); cv = ImageEnhance.Color(cv).enhance(1.12)
cv = cv.filter(ImageFilter.UnsharpMask(2, 70, 2))
# soft dark gradient on the left for text legibility
x = np.arange(W, dtype=np.float32); g1 = np.clip(0.6 + 0.4 * (x / 1000) ** 1.5, 0, 1)
g = np.repeat(g1[None, :, None], H, axis=0)
cv = Image.fromarray((np.asarray(cv).astype(np.float32) * g).clip(0, 255).astype(np.uint8)).convert("RGBA")
F = "/home/user/YouTube-/tools/fonts/BebasNeue-Regular.ttf"
cream = (246, 238, 222, 255)
def line(t, size, y, fill=cream):
    im = T.text_img(t, F, size, fill); T.paste_shadow(cv, im, (70, y), 16, 0.8, (5, 8)); return im
line("BANNED FOR", 200, 270)
line("A BURRITO?", 200, 470)
cv.convert("RGB").save("thumbnail_v2_HD.jpg", quality=95)
cv.convert("RGB").resize((1280, 720), Image.LANCZOS).save("thumbnail_v2.jpg", quality=93); print("ok")

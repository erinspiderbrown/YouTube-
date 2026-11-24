"""Speed thumbnail v2 (24 Nov 2026): the user's own Speed photo with its old text inpainted away and a debate hook
(the top videos on this topic are 'is it real / he lied' doubt videos). Variants: A '10.35 / FAKE?', B 'THEY SAID / FAKE'."""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/home/user/YouTube-/tools/fonts/Anton-Regular.ttf"
src = cv2.imread("thumbnail_user.png"); H, W = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
white = cv2.inRange(src, (225, 225, 225), (255, 255, 255)); red = cv2.inRange(hsv, (0, 170, 150), (8, 255, 255)) | cv2.inRange(hsv, (172, 170, 150), (180, 255, 255))
m = (white | red); m[:, int(W * 0.56):] = 0; m[:int(H * 0.08)] = 0
m = cv2.dilate(m, np.ones((9, 9), np.uint8), 2)
clean = cv2.inpaint(src, m, 9, cv2.INPAINT_TELEA)
base = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
blur = base.filter(ImageFilter.GaussianBlur(22)); bm = Image.new("L", (W, H)); db = ImageDraw.Draw(bm)
for x in range(W): db.line([(x, 0), (x, H)], fill=int(255 * min(1, max(0, (W * 0.44 - x) / (W * 0.06)))))
base = Image.composite(blur, base, bm)
# darken the left so type reads cleanly
g = Image.new("L", (W, H)); d = ImageDraw.Draw(g)
for x in range(W): d.line([(x, 0), (x, H)], fill=int(170 * max(0, 1 - x / (W * 0.62))))
base = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), base, g)
def text(img, xy, s, size, fill, rot=0):
    f = ImageFont.truetype(F, size); bb = f.getbbox(s); w, h = bb[2] + 20, bb[3] + 30
    L = Image.new("RGBA", (w, h)); ImageDraw.Draw(L).text((10, 0), s, font=f, fill=fill)
    sh = Image.new("RGBA", (w, h)); ImageDraw.Draw(sh).text((10, 0), s, font=f, fill=(0, 0, 0, 230)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    if rot: L = L.rotate(rot, expand=True, resample=Image.BICUBIC); sh = sh.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(sh, (xy[0] + 8, xy[1] + 10)); img.alpha_composite(L, xy)
for name, l1, l2, c2 in [("A", "10.35", "FAKE?", (232, 36, 36, 255)), ("B", "THEY SAID", "FAKE", (232, 36, 36, 255))]:
    im = base.convert("RGBA")
    if name == "A":
        text(im, (70, 150), l1, 330, (255, 255, 255, 255)); text(im, (90, 560), l2, 230, c2, rot=4)
    else:
        text(im, (70, 210), l1, 190, (255, 255, 255, 255)); text(im, (70, 470), l2, 300, c2, rot=4)
    out = im.convert("RGB").resize((1280, 720), Image.LANCZOS); out.save(f"thumbnail_v2{name}.jpg", quality=92)
print("ok")

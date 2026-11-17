"""Jakob TikTok cover (1080x1920) from the user's "AT WHAT COST?" thumbnail photo, per the CLAUDE.md recipe:
one photo with its own background, tight crop with the face mid-frame, top extended with the photo's own dark
stadium, the thumbnail's old title inpainted out and redrawn big in the top third, graded with vignette + grain."""
import os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
P = os.path.dirname(os.path.abspath(__file__))
src = cv2.imread(f"{P}/thumbnail_user_at_what_cost.png")
# 1. remove the old white title (bright pixels in its box) by inpainting
box = np.zeros(src.shape[:2], np.uint8); box[270:400, 90:690] = 255
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
txt = ((hsv[..., 2] > 150) & (hsv[..., 1] < 70)).astype(np.uint8) * 255
mask = cv2.dilate(cv2.bitwise_and(txt, box), np.ones((9, 9), np.uint8))
clean = cv2.inpaint(src, mask, 9, cv2.INPAINT_TELEA)
im = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
W, H = 1080, 1920
x0, x1 = 520, 1400                       # pointing hand + face + NORWAY vest
crop = im.crop((x0, 0, x1, im.height)); s = W / crop.width
ph = crop.resize((W, int(crop.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 50, 2)); py = H - ph.height
# 2. extend the top with the photo's own dark stadium background
top = im.crop((0, 0, 470, 260)).resize((W, py + 260), Image.BICUBIC).filter(ImageFilter.GaussianBlur(24))   # empty dark stadium, left of the subject
canvas = Image.new("RGB", (W, H)); canvas.paste(top, (0, 0))
a = Image.new("L", ph.size, 255); a.paste(Image.linear_gradient("L").resize((W, 260)), (0, 0))
# keep the subject (hair) solid over the blend: rembg isnet mask of the thumbnail
from PIL import ImageChops
msk = Image.open("/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/jakob/jk_mask.png").convert("L").crop((x0, 0, x1, im.height)).resize(ph.size, Image.LANCZOS)
a = ImageChops.lighter(a, msk)
canvas.paste(ph, (0, py), a)
# 3. grade: contrast, darker edges
rgb = ImageEnhance.Contrast(canvas).enhance(1.08)
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-380, -200, W + 380, H + 260], fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
out = Image.composite(rgb, ImageEnhance.Brightness(rgb).enhance(0.5), v).convert("RGBA")
# 4. title, same look as the thumbnail: plain white condensed caps with a soft shadow
F = ImageFont.truetype("/home/user/YouTube-/tools/fonts/BebasNeue-Regular.ttf", 230)
def title(t, y):
    lay = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((W // 2, 150), t, font=F, fill=(255, 255, 255), anchor="mm")
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[3].point(lambda q: int(q * 0.75))); sh = sh.filter(ImageFilter.GaussianBlur(14))
    out.alpha_composite(sh, (6, y - 140)); out.alpha_composite(lay, (0, y - 150))
title("AT WHAT", 330); title("COST?", 560)
g = np.random.default_rng(3).normal(0, 4, (H, W, 1))
res = np.clip(np.array(out.convert("RGB")).astype(float) + g, 0, 255).astype("uint8")
Image.fromarray(res).save(f"{P}/tiktok_cover.jpg", quality=95)
print("py", py, "scale", round(s, 3))

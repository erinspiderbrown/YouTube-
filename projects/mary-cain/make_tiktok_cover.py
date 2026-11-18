"""Mary Cain TikTok cover (1080x1920) from the user's "NIKE / WHAT HAPPENED?" thumbnail, per the CLAUDE.md recipe:
one photo with its own background, tight crop with the face mid-frame, top extended with the photo's own dark wall
and Nike swoosh (old title inpainted out), the thumbnail's title redrawn big in the top third, graded.
Run: python3 projects/mary-cain/make_tiktok_cover.py"""
import os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
P = os.path.dirname(os.path.abspath(__file__))
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/mary"
src = cv2.imread(f"{P}/thumbnail_user_nike_what_happened.png")
# 1. remove the old title + red rule (right side) by inpainting
box = np.zeros(src.shape[:2], np.uint8); box[280:580, 900:1660] = 255
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
txt = ((hsv[..., 2] > 140) & (hsv[..., 1] < 80)) | ((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 120)
mask = cv2.dilate(cv2.bitwise_and(txt.astype(np.uint8) * 255, box), np.ones((11, 11), np.uint8))
clean = cv2.inpaint(src, mask, 11, cv2.INPAINT_TELEA)
im = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
W, H = 1080, 1920
# 2. subject: Mary, fists and bib
x0, x1 = 110, 950
crop = im.crop((x0, 0, x1, im.height)); s = W / crop.width
ph = crop.resize((W, int(crop.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 50, 2)); py = H - ph.height
# 3. top: the photo's own dark wall with the swoosh (old title removed), softened so it reads as depth
wall = im.crop((975, 0, 1672, 620)); ws = W / wall.width
top = wall.resize((W, int(wall.height * ws)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
top = ImageEnhance.Brightness(top).enhance(0.85)
canvas = Image.new("RGB", (W, H), (12, 12, 14)); canvas.paste(top, (0, 0))
blend = 300
a = Image.new("L", ph.size, 255); a.paste(Image.linear_gradient("L").resize((W, blend)), (0, 0))
msk = Image.open(f"{SCR}/mc_mask.png").convert("L").crop((x0, 0, x1, im.height)).resize(ph.size, Image.LANCZOS)
a = ImageChops.lighter(a, msk)
canvas.paste(ph, (0, py), a)
# 4. grade: contrast, darker edges
rgb = ImageEnhance.Contrast(canvas).enhance(1.06)
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-380, -260, W + 380, H + 260], fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
out = Image.composite(rgb, ImageEnhance.Brightness(rgb).enhance(0.55), v).convert("RGBA")
# 5. title in the thumbnail's style: small spaced NIKE, big condensed italic WHAT HAPPENED?, red rule
def layer_text(t, font, size_box, spacing=0):
    lay = Image.new("RGBA", size_box, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if spacing:
        widths = [d.textlength(c, font=font) for c in t]; tw = sum(widths) + spacing * (len(t) - 1); x = (size_box[0] - tw) / 2
        for c, w in zip(t, widths): d.text((x, size_box[1] / 2), c, font=font, fill=(255, 255, 255), anchor="lm"); x += w + spacing
    else:
        d.text((size_box[0] / 2, size_box[1] / 2), t, font=font, fill=(255, 255, 255), anchor="mm")
    return lay
def italic(lay, k=0.16):
    w, h = lay.size; return lay.transform((w, h), Image.AFFINE, (1, k, -k * h / 2, 0, 1, 0), Image.BICUBIC)
def put(lay, y, blur=14, op=0.8):
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[3].point(lambda q: int(q * op))); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh, (5, y + 6)); out.alpha_composite(lay, (0, y))
B = "/home/user/YouTube-/tools/fonts/BebasNeue-Regular.ttf"
put(layer_text("NIKE", ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 64), (W, 110), spacing=30), 170, 8, 0.7)
put(italic(layer_text("WHAT", ImageFont.truetype(B, 250), (W, 260))), 270)
put(italic(layer_text("HAPPENED?", ImageFont.truetype(B, 250), (W, 260))), 490)
ImageDraw.Draw(out).rectangle([W // 2 - 190, 744, W // 2 + 190, 751], fill=(196, 30, 46))
g = np.random.default_rng(5).normal(0, 3, (H, W, 1))
res = np.clip(np.array(out.convert("RGB")).astype(float) + g, 0, 255).astype("uint8")
Image.fromarray(res).save(f"{P}/tiktok_cover.jpg", quality=95)
print("py", py, "scale", round(s, 3), "top", top.size)

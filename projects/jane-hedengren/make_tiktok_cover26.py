"""TikTok cover (1080x1920) from the user's NCAA 2026 thumbnail: one photo, crop centred on Jane Hedengren, top extended
with the photo's own stormy sky (blurred, blended), title big in the top third, light grade."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
P = os.path.dirname(os.path.abspath(__file__))
src = Image.open(f"{P}/thumbnail_user_ncaa2026.png").convert("RGB")   # 1672x941
W, H = 1080, 1920
x0 = 880 - 330; crop = src.crop((x0, 0, x0 + 660, 941)); s = W / crop.width
ph = crop.resize((W, int(crop.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2)); py = H - ph.height
sky = src.crop((x0 - 200, 0, x0 + 860, 260)).resize((W, py + 220), Image.LANCZOS).filter(ImageFilter.GaussianBlur(10))
sky = ImageEnhance.Brightness(sky).enhance(0.7)
cv = Image.new("RGB", (W, H)); cv.paste(sky, (0, 0))
m = Image.new("L", ph.size, 255); m.paste(Image.linear_gradient("L").resize((W, 220)), (0, 0))
cv.paste(ph, (0, py), m)
cv = ImageEnhance.Contrast(cv).enhance(1.06)
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-400, -300, W + 400, H + 300], fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
out = Image.composite(cv, ImageEnhance.Brightness(cv).enhance(0.55), v).convert("RGBA")
B = "/home/user/YouTube-/tools/fonts/BebasNeue-Regular.ttf"
def put(text, size, y, fill, blur=14):
    f = ImageFont.truetype(B, size); lay = Image.new("RGBA", (W, size + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, (size + 60) / 2), text, font=f, fill=fill, anchor="mm")
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(lay.split()[3].point(lambda q: int(q * 0.85))); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh, (6, y + 8)); out.alpha_composite(lay, (0, y))
put("IS JANE HEDENGREN", 130, 120, (244, 236, 220, 255))
put("ABOUT TO", 130, 250, (244, 236, 220, 255))
put("CHOKE?", 270, 360, (226, 46, 40, 255), 18)
out.convert("RGB").save(f"{P}/tiktok_cover_ncaa2026.jpg", quality=95); print("py", py)

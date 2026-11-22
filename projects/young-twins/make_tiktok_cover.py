"""TikTok cover 1080x1920 from the user's twins thumbnail: crop on both faces, extend top with the photo's own dusk sky (blurred), "THEY FELL OFF" big in the top third (white/red heavy italic)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
P = os.path.dirname(os.path.abspath(__file__))
src = Image.open(f"{P}/thumbnail_user.png").convert("RGB"); sw, sh = src.size
W, H = 1080, 1920
x0, x1 = int(sw * 0.0), int(sw * 0.70)
crop = src.crop((x0, 0, x1, sh)); s = W / crop.width
ph = crop.resize((W, int(crop.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4, 50, 2)); py = H - ph.height
bg = src.crop((int(sw*0.62), 0, int(sw*0.72), int(sh*0.12))).resize((W, py + 260), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))
bg = ImageEnhance.Brightness(bg).enhance(0.6)
cv = Image.new("RGB", (W, H)); cv.paste(bg, (0, 0))
m = Image.new("L", ph.size, 255); m.paste(Image.linear_gradient("L").resize((W, 260)), (0, 0))
cv.paste(ph, (0, py), m)
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-400, -300, W + 400, H + 300], fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
out = Image.composite(cv, ImageEnhance.Brightness(cv).enhance(0.6), v).convert("RGBA")
F = "/home/user/YouTube-/tools/fonts/Montserrat-BlackItalic.ttf"
def put(text, size, y, fill, blur=16):
    f = ImageFont.truetype(F, size); lay = Image.new("RGBA", (W, size + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, (size + 80) / 2), text, font=f, fill=fill, anchor="mm")
    sh_ = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh_.putalpha(lay.split()[3].point(lambda q: int(q * 0.9))); sh_ = sh_.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh_, (6, y + 10)); out.alpha_composite(lay, (0, y))
put("THEY", 170, 120, (255, 255, 255, 255))
put("FELL", 250, 270, (232, 18, 18, 255), 20)
put("OFF", 210, 500, (255, 255, 255, 255))
out.convert("RGB").save(f"{P}/tiktok_cover.jpg", quality=95); print("py", py)

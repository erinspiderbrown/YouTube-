"""TikTok cover (1080x1920) from the user's own thumbnail: same photo, subject cropped tall, its dark arena background
extended upward, and the thumbnail's own 'drew hunter' type moved into the top third."""
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
T = Image.open("thumbnail_user.png").convert("RGB"); W, H = T.size
body = T.crop((int(W * 0.50), 0, W, H)); s = 1080 / body.width; body = body.resize((1080, int(body.height * s)), Image.LANCZOS)
bg = T.crop((int(W * 0.50), 0, W, int(H * 0.35))).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
bg = ImageEnhance.Brightness(bg).enhance(0.55)
C = bg.copy(); y0 = 1920 - body.height - 40
m = Image.new("L", body.size, 255); d = ImageDraw.Draw(m)
for i in range(220): d.line([(0, i), (body.width, i)], fill=int(255 * i / 220))
C.paste(body, (0, y0), m)
txt = T.crop((int(W * 0.04), int(H * 0.12), int(W * 0.5), int(H * 0.52))); k = 980 / txt.width
txt = txt.resize((980, int(txt.height * k)), Image.LANCZOS)
tm = txt.convert("L").point(lambda v: 255 if v > 150 else int(v * 1.2) if v > 90 else 0).filter(ImageFilter.GaussianBlur(1))
sh = Image.new("RGB", txt.size, (0, 0, 0)); C.paste(sh, (58, 232), tm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.6)))
C.paste(txt, (50, 220), tm)
g = Image.new("L", (1080, 1920), 0); dg = ImageDraw.Draw(g)
for r in range(0, 400, 4): dg.rectangle([r // 2, r, 1080 - r // 2, 1920 - r], outline=int(70 * (1 - r / 400)), width=4)
C = Image.composite(Image.new("RGB", C.size, (0, 0, 0)), C, g.filter(ImageFilter.GaussianBlur(30)))
C = ImageEnhance.Contrast(C).enhance(1.05); C.save("tiktok_cover.jpg", quality=93); print(y0, body.size, txt.size)

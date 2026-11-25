"""Depth-pull still (cinematic step-up, 25 Nov 2026): turns a photo into a 1920x1080 clip with a 2.5D feel.
Background plate = the photo filled and blurred, slowly pulling back; foreground = the sharp photo (fit for
portrait, soft-edged for landscape) slowly pushing in. Different speeds read as depth. No grain.
usage: python3 depth_still.py IN.jpg OUT.mp4 [seconds=10] [focus_x=0.5] [focus_y=0.45]"""
import sys, subprocess
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
W, H, FPS = 1920, 1080, 24
src, out = sys.argv[1], sys.argv[2]; dur = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
fx = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.45
im = Image.open(src).convert("RGB"); iw, ih = im.size
def fill(img, w, h):
    s = max(w / img.width, h / img.height); r = img.resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    x = int((r.width - w) * fx); y = int((r.height - h) * fy); return r.crop((x, y, x + w, y + h))
bg0 = ImageEnhance.Brightness(fill(im, int(W * 1.12), int(H * 1.12)).filter(ImageFilter.GaussianBlur(28))).enhance(0.55)
portrait = ih > iw * 0.9
if portrait:
    s = (H * 0.98) / ih; fg0 = im.resize((int(iw * s), int(ih * s)), Image.LANCZOS)
    mask0 = Image.new("L", fg0.size, 255)
else:
    fg0 = fill(im, W, H); mask0 = Image.new("L", fg0.size, 0); d = ImageDraw.Draw(mask0)
    d.rounded_rectangle([60, 40, W - 60, H - 40], 80, fill=255); mask0 = mask0.filter(ImageFilter.GaussianBlur(70))
n = int(dur * FPS)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(n):
    k = i / max(1, n - 1); e = k * k * (3 - 2 * k)
    sb = 1.0 + 0.06 * (1 - e)                         # background pulls back
    b = bg0.resize((int(bg0.width * sb / 1.12 * 1.12), int(bg0.height * sb / 1.12 * 1.12)))
    frame = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    sf = 1.0 + 0.10 * e                               # foreground pushes in
    f = fg0.resize((int(fg0.width * sf), int(fg0.height * sf)), Image.BICUBIC); m = mask0.resize(f.size, Image.BICUBIC)
    x = int(W / 2 - f.width * (0.5 if portrait else fx) + (0 if portrait else (fx - 0.5) * 0)); y = int(H / 2 - f.height * (0.5 if portrait else fy))
    if not portrait: x = (W - f.width) // 2; y = (H - f.height) // 2
    frame.paste(f, (x, y), m); p.stdin.write(frame.tobytes())
p.stdin.close(); p.wait(); print("ok", out)

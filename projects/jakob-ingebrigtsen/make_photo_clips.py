"""Turn the Commons photos (independent photographers) into 8 s 1080p Ken Burns clips (clips/p_<name>.mp4).
Portrait or narrow photos sit on a blurred, darkened copy of themselves. args: PHOTODIR CLIPDIR name=file [focus x,y] ..."""
import sys, os, subprocess
from PIL import Image, ImageFilter, ImageEnhance
src, dst = sys.argv[1], sys.argv[2]
for spec in sys.argv[3:]:
    name, f = spec.split("=", 1)
    zin = True
    if f.endswith("@out"): f, zin = f[:-4], False
    out = f"{dst}/p_{name}.mp4"
    if os.path.exists(out): continue
    im = Image.open(f"{src}/{f}").convert("RGB")
    CW, CH = 2400, 1350
    bg = im.copy(); s = max(CW / bg.width, CH / bg.height); bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
    bg = bg.crop(((bg.width - CW) // 2, (bg.height - CH) // 2, (bg.width - CW) // 2 + CW, (bg.height - CH) // 2 + CH))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
    r = im.width / im.height
    if r >= 1.6:   # wide: fill the frame
        s = max(CW / im.width, CH / im.height); fg = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
        bg.paste(fg.crop(((fg.width - CW) // 2, (fg.height - CH) // 2, (fg.width - CW) // 2 + CW, (fg.height - CH) // 2 + CH)), (0, 0))
    else:
        s = min(CW / im.width, CH / im.height); fg = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        bg.paste(fg, ((CW - fg.width) // 2, (CH - fg.height) // 2))
    tmp = f"{dst}/p_{name}.png"; bg.save(tmp)
    z = "1+0.12*on/192" if zin else "1.12-0.12*on/192"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", tmp, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-vf", f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24,format=yuv420p",
                    "-t", "8", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-shortest", out], check=True)
    os.remove(tmp); print("made", out)

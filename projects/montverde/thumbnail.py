import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T = Image.open("thumb_orig.png").convert("RGB")
R = Image.open("release.png").convert("RGB")

# ---------- 1. real press release document
hdr = R.crop((30, 1862, 1180, 2048))
body = R.crop((80, 393, 1180, 1245))
b = np.asarray(body).astype(np.float32)
bg = cv2.dilate(b, np.ones((25, 25), np.uint8)); bg = cv2.GaussianBlur(bg, (0, 0), 15)
b = np.clip(b / np.maximum(bg, 1) * 255, 0, 255)          # flatten the grey page shading to white
body = Image.fromarray(b.astype(np.uint8))
# highlighter marks (body-crop coords)
hl = Image.new("RGBA", body.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
Y = (255, 214, 0, 120)
for box in [(842, 170, 925, 198), (86, 197, 364, 225),            # "by three / athletes - all coached by Phiri"
            (246, 408, 817, 437)]:                                 # "Possession of GW1516 when he was an Athlete in 2018 and 2019"
    hd.rounded_rectangle(box, radius=6, fill=Y)
body = Image.alpha_composite(body.convert("RGBA"), hl)
W = 1100
hdr = hdr.resize((W, int(hdr.height * W / hdr.width)), Image.LANCZOS)
doc = Image.new("RGBA", (W, hdr.height + body.height + 8), (255, 255, 255, 255))
doc.paste(hdr, (0, 0)); doc.paste(body, (0, hdr.height + 8))
d = ImageDraw.Draw(doc); d.rectangle([0, doc.height - 10, W, doc.height], fill=(232, 98, 42))
# scale + tilt + shadow
s = 600 / W
doc = doc.resize((int(W * s), int(doc.height * s)), Image.LANCZOS)
doc = doc.rotate(3, expand=True, resample=Image.BICUBIC)
sh = Image.new("RGBA", doc.size, (0, 0, 0, 0)); sh.putalpha(doc.split()[-1].point(lambda v: 170 if v else 0))
sh = sh.filter(ImageFilter.GaussianBlur(18))
out = T.convert("RGBA")
px, py = 1092, 22
out.alpha_composite(sh, (px + 10, py + 16)); out.alpha_composite(doc, (px, py))

# keep the athletes in FRONT of the document (as in the original design):
o = np.asarray(T).astype(np.int16)
lum = o.min(2); sat = o.max(2) - o.min(2)
olddoc = ((lum > 165) & (sat < 40)).astype(np.uint8)
olddoc = cv2.morphologyEx(olddoc, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
yy, xx = np.mgrid[0:T.height, 0:T.width]
cand = ((olddoc == 0) & (xx > 900) & (xx < 1300) & (yy > 230) & (yy < 640)).astype(np.uint8)
cand = cv2.morphologyEx(cand, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab = cv2.connectedComponents(cand)
keep = np.zeros_like(cand)
for i in range(1, n):          # athletes are the blobs that continue out to the left of the document
    comp = lab == i
    if comp[:, 900:1095].any() and comp.sum() > 2000: keep[comp] = 1
keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
ff = keep.copy(); h_, w_ = ff.shape; msk = np.zeros((h_ + 2, w_ + 2), np.uint8)
cv2.floodFill(ff, msk, (1660, 5), 1)               # fill holes (e.g. white jersey letters)
holes = (ff == 0); keep[holes] = 1
athlete = keep.astype(bool) & (yy > 230)
fa = np.asarray(out).copy(); fa[athlete, :3] = o[athlete].astype(np.uint8); out = Image.fromarray(fa)

# ---------- 2. "4 ATHLETES" -> "3 ATHLETES"
a = np.asarray(out.convert("RGB")).copy()
x0, y0, x1, y1 = 482, 772, 566, 866
reg = a[y0:y1, x0:x1].astype(int)
m = np.zeros(a.shape[:2], np.uint8)
m[y0:y1, x0:x1] = ((reg.min(2) > 150)).astype(np.uint8) * 255
m = cv2.dilate(m, np.ones((5, 5), np.uint8))
a = cv2.inpaint(a, m, 6, cv2.INPAINT_TELEA)
out = Image.fromarray(a).convert("RGBA")
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Black.otf", 108)
g = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
gd.text((40, 20), "3", font=f, fill=(255, 255, 255, 255))
g = g.transform(g.size, Image.AFFINE, (1, 0.21, -20, 0, 1, 0), resample=Image.BICUBIC)   # italic shear
bb = g.getbbox(); g = g.crop(bb)
gs = Image.new("RGBA", g.size, (0, 0, 0, 0)); gs.putalpha(g.split()[-1].point(lambda v: v // 2))
gs = gs.filter(ImageFilter.GaussianBlur(3))
gx, gy = 489, 783
out.alpha_composite(gs, (gx + 3, gy + 4)); out.alpha_composite(g, (gx, gy))
out.convert("RGB").save("thumbnail_v2.png")
out.convert("RGB").save("thumbnail_v2.jpg", quality=92)
print("ok", out.size, "glyph", g.size)

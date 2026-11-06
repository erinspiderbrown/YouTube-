"""JxmyHighroller-style graphics for the Shea Foster video: plain, clean, white.

Every function returns a full-frame 1920x1080 RGBA PIL image (cached by the caller).
- big(): a big white number/word with a small label, for use over darkened footage.
- doc(): a white "document" card with real quoted text and yellow highlights.
- lower(): a small plain lower third.
- comment(): a plain white comment bubble (no usernames).
- center(): centred white text.
- tag(): small corner label (e.g. ILLUSTRATION).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FD = "/usr/share/fonts/opentype/inter/"


def font(weight, size):
    for n in (f"InterDisplay-{weight}.otf", f"Inter-{weight}.otf"):
        try:
            return ImageFont.truetype(FD + n, size)
        except OSError:
            pass
    return ImageFont.truetype(FD + "Inter-Bold.otf", size)


def _shadow(img, r=16, a=170):
    al = img.split()[-1].filter(ImageFilter.GaussianBlur(r))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(al.point(lambda v: min(a, v)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 5))
    out.alpha_composite(img)
    return out


def _fit(text, weight, size, maxw):
    f = font(weight, size)
    while f.getlength(text) > maxw and size > 40:
        size -= 6
        f = font(weight, size)
    return f


def big(text, label=None, size=230, label_above=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = _fit(text, "Black", size, W - 200)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    y = (H - th) // 2 - bb[1] - (30 if label else 0)
    d.text(((W - tw) // 2 - bb[0], y), text, font=f, fill=(255, 255, 255, 255))
    if label:
        lf = _fit(label, "Bold", 46, W - 260)
        lw = lf.getlength(label)
        ly = y + bb[1] - 80 if label_above else y + bb[3] + 40
        d.text(((W - lw) // 2, ly), label, font=lf, fill=(255, 255, 255, 235))
    return _shadow(im)


def center(text, size=110, y=None, weight="Black", color=(255, 255, 255, 255)):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = _fit(text, weight, size, W - 220)
    bb = d.textbbox((0, 0), text, font=f)
    x = (W - (bb[2] - bb[0])) // 2 - bb[0]
    yy = ((H - (bb[3] - bb[1])) // 2 - bb[1]) if y is None else y
    d.text((x, yy), text, font=f, fill=color)
    return _shadow(im, 12, 150)


def tag(text):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font("SemiBold", 26)
    w = f.getlength(text)
    d.rectangle([W - w - 74, 40, W - 40, 84], fill=(0, 0, 0, 150))
    d.text((W - w - 57, 46), text, font=f, fill=(255, 255, 255, 220))
    return im


def lower(name, sub=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    nf, sf = font("Black", 56), font("Medium", 32)
    nw = nf.getlength(name)
    sw = sf.getlength(sub) if sub else 0
    bw = max(nw, sw) + 64
    y0 = 860 if sub else 900
    d.rectangle([90, y0, 90 + bw, 1010], fill=(0, 0, 0, 175))
    d.rectangle([90, y0, 98, 1010], fill=(255, 255, 255, 255))
    d.text((122, y0 + 14), name, font=nf, fill=(255, 255, 255, 255))
    if sub:
        d.text((124, y0 + 92), sub, font=sf, fill=(225, 225, 225, 255))
    return im


def comment(text, x, y):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    f = font("SemiBold", 46)
    tw = f.getlength(text)
    w = int(tw + 200)
    d.rounded_rectangle([0, 0, w, 150], 26, fill=(255, 255, 255, 250))
    d.ellipse([28, 37, 104, 113], fill=(190, 193, 200, 255))
    d.rounded_rectangle([130, 34, 260, 52], 9, fill=(205, 208, 214, 255))
    d.text((130, 64), text, font=f, fill=(20, 20, 24, 255))
    card = _shadow(card.crop((0, 0, w + 10, 170)), 14, 120)
    im.alpha_composite(card, (x, y))
    return im


def doc(source, text, highlights=(), width=1360, size=50, title=None):
    """White document card. `highlights` are exact substrings of `text` to mark yellow."""
    f = font("Medium", size)
    hf = font("SemiBold", size)
    sf = font("Bold", 28)
    tf = font("Black", 64)
    marks = [False] * len(text)
    for h in highlights:
        i = text.find(h)
        assert i >= 0, h
        for k in range(i, i + len(h)):
            marks[k] = True
    # tokens with highlight flag
    toks, pos = [], 0
    for wd in text.split(" "):
        hl = any(marks[pos:pos + len(wd)])
        toks.append((wd, hl))
        pos += len(wd) + 1
    pad = 70
    inner = width - 2 * pad
    lines, cur, cw = [], [], 0
    sp = f.getlength(" ")
    for wd, hl in toks:
        ww = (hf if hl else f).getlength(wd)
        if cur and cw + sp + ww > inner:
            lines.append(cur)
            cur, cw = [], 0
        cur.append((wd, hl, ww))
        cw += (sp if len(cur) > 1 else 0) + ww
    if cur:
        lines.append(cur)
    lh = int(size * 1.5)
    ttl_h = 0
    if title:
        tlines, cur2 = [], ""
        for wd in title.split(" "):
            t2 = (cur2 + " " + wd).strip()
            if tf.getlength(t2) > inner and cur2:
                tlines.append(cur2)
                cur2 = wd
            else:
                cur2 = t2
        tlines.append(cur2)
        ttl_h = len(tlines) * 80 + 30
    hgt = pad + 50 + ttl_h + len(lines) * lh + pad - 10
    card = Image.new("RGBA", (width, hgt), (255, 255, 255, 255))
    d = ImageDraw.Draw(card)
    d.text((pad, pad - 10), source.upper(), font=sf, fill=(150, 30, 30, 255))
    y = pad + 50
    if title:
        for tl in tlines:
            d.text((pad, y), tl, font=tf, fill=(15, 15, 18, 255))
            y += 80
        y += 30
    for ln in lines:
        x = pad
        for i, (wd, hl, ww) in enumerate(ln):
            if hl:
                nxt = ln[i + 1][1] if i + 1 < len(ln) else False
                d.rectangle([x - 6, y + 2, x + ww + (sp if nxt else 0) + 6, y + lh - 10], fill=(255, 226, 60, 255))
            x += ww + sp
        x = pad
        for wd, hl, ww in ln:
            d.text((x, y), wd, font=hf if hl else f, fill=(15, 15, 18, 255))
            x += ww + sp
        y += lh
    card = _shadow(card, 22, 160)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.alpha_composite(card, ((W - card.width) // 2, (H - card.height) // 2))
    return im

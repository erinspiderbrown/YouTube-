"""What happened to the last 10 NCAA men's 100m champions: full edit.

Style copied from the breakout "What happened to the last X winners" videos (see edit_style.md): a 10-tile champion
grid that fills with fate stamps between segments, year + name splash cards, stacked stat pop-ups, black-and-white
with red text for low points, quote cards for documents, dark trap bed ducked under the voice, whooshes/sub-booms/stamps.

Run:  python3 projects/ncaa-100m-champs/hundo_build.py [stage ...]   stages: overlays grid shots concat audio mux (default all)
"""
import os, sys, json, math, subprocess, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/ncaa-100m-champs"
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
H = f"{SCR}/hundo"; REAL = f"{H}/real"; R = f"{H}/render"; FACES = f"{H}/faces"
for d in ("ov", "shots", "grid", "cards"): os.makedirs(f"{R}/{d}", exist_ok=True)
SFXD = f"{ROOT}/projects/jon-drummond/sfx"
VO = f"{P}/hundo_voiceover_v1.wav"; END = 522.0
OUT = f"{SCR}/output/hundo_v1_master.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24
ANTON = f"{ROOT}/tools/fonts/Anton-Regular.ttf"; INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
WHITE, BLACK, RED, GREEN, AMBER, BLUE, YEL = (255, 255, 255), (0, 0, 0), (235, 35, 45), (40, 210, 90), (255, 176, 0), (40, 140, 255), (255, 214, 0)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: print(" ".join(map(str, cmd))[:800]); print(r.stderr[-2500:]); raise SystemExit(1)
    return r

def F(path, size): return ImageFont.truetype(path, size)

# ------------------------------------------------------------------ champions + grid states
CH = [  # key, year, name, school, accent, fate, fate colour
    ("lawson", 2016, "JARRION LAWSON", "ARKANSAS", (157, 34, 53), "LOST 2 YEARS", AMBER),
    ("coleman", 2017, "CHRISTIAN COLEMAN", "TENNESSEE", (255, 130, 0), "WORLD CHAMP", GREEN),
    ("burrell", 2018, "CAMERON BURRELL", "HOUSTON", (200, 16, 46), "REST EASY", WHITE),
    ("oduduru", 2019, "DIVINE ODUDURU", "TEXAS TECH · NIGERIA", (204, 0, 0), "BANNED", RED),
    ("laird", 2021, "TERRANCE LAIRD", "LSU", (253, 208, 35), "INJURED", RED),
    ("fahnbulleh", 2022, "JOSEPH FAHNBULLEH", "FLORIDA · LIBERIA", (0, 33, 165), "STILL GRINDING", AMBER),
    ("lindsey", 2023, "COURTNEY LINDSEY", "TEXAS TECH", (204, 0, 0), "STILL GRINDING", AMBER),
    ("hinchliffe", 2024, "LOUIE HINCHLIFFE", "HOUSTON · GREAT BRITAIN", (200, 16, 46), "BACK TO COLLEGE", BLUE),
    ("anthony", 2025, "JORDAN ANTHONY", "ARKANSAS", (157, 34, 53), "WORLD CHAMP", GREEN),
    ("ajayi", 2026, "KANYINSOLA AJAYI", "AUBURN · NIGERIA", (232, 119, 34), "???", WHITE),
]
TW = 330; GAP = 34; GX0 = (W - (5 * TW + 4 * GAP)) // 2; GY0 = 210

def tile_xy(i): return GX0 + (i % 5) * (TW + GAP), GY0 + (i // 5) * (TW + 120)

_BG = None
def grid_bg():
    global _BG
    if _BG is None:
        f = f"{R}/grid/bg.png"
        if not os.path.exists(f):
            run(["ffmpeg", "-v", "error", "-y", "-ss", "100", "-i", f"{REAL}/ncaa2024_100.mp4", "-frames:v", "1", f])
        im = Image.open(f).convert("RGB").resize((W, Hh)).filter(ImageFilter.GaussianBlur(22))
        _BG = ImageEnhance.Brightness(im).enhance(0.32).convert("RGBA")
    return _BG.copy()

def stroke_text(d, xy, s, font, fill, stroke=8, anchor="la"):
    d.text(xy, s, font=font, fill=fill, stroke_width=stroke, stroke_fill=BLACK, anchor=anchor)

def stamp_img(text, col, scale=1.0, rot=-8):
    f = F(ANTON, int(64 * scale)); tw = int(f.getlength(text)) + int(40 * scale); th = int(100 * scale)
    im = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, tw + 10, th + 10], int(10 * scale), outline=col + (255,), width=max(3, int(8 * scale)), fill=(0, 0, 0, 150))
    d.text((tw / 2 + 10, th / 2 + 12), text, font=f, fill=col + (255,), anchor="mm")
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)

def grid_frame(done, active=None, reveal=10, grey_all=False, stamp_scale=None, highlight=None):
    """done = number of finished champions (their tiles show fate stamps)."""
    im = grid_bg(); d = ImageDraw.Draw(im)
    stroke_text(d, (W // 2, 105), "THE LAST 10 NCAA 100M CHAMPIONS", F(ANTON, 88), WHITE, 6, "mm")
    for i, (k, yr, name, school, acc, fate, fcol) in enumerate(CH[:reveal]):
        x, y = tile_xy(i)
        face = Image.open(f"{FACES}/{k}.png").convert("RGB").resize((TW, TW), Image.LANCZOS)
        if grey_all or (i >= done and i != active): face = ImageEnhance.Brightness(ImageOps.grayscale(face).convert("RGB")).enhance(0.55)
        if k == "burrell" and i < done: face = ImageEnhance.Color(face).enhance(0.35)
        border = YEL if (i == active or i == highlight) else (acc if i < done else (90, 90, 90))
        d.rectangle([x - 7, y - 7, x + TW + 6, y + TW + 6], fill=border + (255,))
        im.paste(face, (x, y))
        d.rectangle([x, y + TW - 70, x + TW, y + TW], fill=(0, 0, 0, 215))
        d.text((x + TW // 2, y + TW - 36), str(yr), font=F(ANTON, 52), fill=WHITE, anchor="mm")
        d.text((x + TW // 2, y + TW + 34), name.split()[-1], font=F(ANTON, 46), fill=WHITE, anchor="mm")
        if i < done or (stamp_scale is not None and i == done):
            s = 1.0 if i < done else stamp_scale
            st = stamp_img(fate, fcol, 0.62 * s)
            im.alpha_composite(st, (int(x + TW / 2 - st.width / 2), int(y + TW * 0.42 - st.height / 2)))
        if i == highlight:
            d.rectangle([x - 12, y - 12, x + TW + 11, y + TW + 11], outline=YEL + (255,), width=6)
    return im

def ease(u): return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, u)))

def write_frames(frames_fn, n, out):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{Hh}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frames_fn(i).convert("RGB").tobytes())
    p.stdin.close(); p.wait()

def zoom_to(im, cx, cy, z):
    """crop around (cx, cy) by zoom factor z (1 = full frame)."""
    w, h = W / z, Hh / z; x0 = min(max(0, cx - w / 2), W - w); y0 = min(max(0, cy - h / 2), Hh - h)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, Hh), Image.BILINEAR)

def grid_step(i, dur):
    """stamp champion i-1, then push into tile i."""
    out = f"{R}/grid/step_{i}.mp4"
    if os.path.exists(out): return out
    n = int(round(dur * FPS)); ns = int(0.75 * FPS)
    base_done = grid_frame(i, active=None if i >= 10 else i)
    def fr(f):
        if i > 0 and f < ns:
            sc = 2.2 - 1.2 * min(1, f / (0.25 * FPS))
            return grid_frame(i - 1, active=i - 1, stamp_scale=sc) if f < ns - 1 else base_done
        if i >= 10: return base_done
        u = ease((f - ns) / max(1, n - ns - 1)); x, y = tile_xy(i)
        return zoom_to(base_done, x + TW / 2, y + TW / 2, 1 + 2.2 * u)
    write_frames(fr, n, out); return out

def grid_intro(dur):
    out = f"{R}/grid/intro.mp4"
    if os.path.exists(out): return out
    n = int(round(dur * FPS))
    def fr(f):
        k = min(10, 1 + int(f / (0.45 * FPS)))
        im = grid_frame(0, reveal=k, grey_all=True); return zoom_to(im, W / 2, Hh / 2, 1.0 + 0.04 * f / n)
    write_frames(fr, n, out); return out

def grid_verdict(seq, dur, name):
    """static full grid with a moving highlight. seq = [(t_rel, idx or None)]"""
    out = f"{R}/grid/{name}.mp4"
    if os.path.exists(out): return out
    n = int(round(dur * FPS)); cache = {}
    def fr(f):
        t = f / FPS; idx = None
        for tt, ii in seq:
            if t >= tt: idx = ii
        if idx not in cache: cache[idx] = grid_frame(10, highlight=idx)
        im = cache[idx]
        if idx is None: return zoom_to(im, W / 2, Hh / 2, 1 + 0.03 * f / n)
        x, y = tile_xy(idx); return zoom_to(im, (W / 2) * 0.65 + (x + TW / 2) * 0.35, (Hh / 2) * 0.65 + (y + TW / 2) * 0.35, 1.18)
    write_frames(fr, n, out); return out

# ------------------------------------------------------------------ overlay PNGs
def ov_path(spec):
    return f"{R}/ov/{hashlib.md5(json.dumps(spec).encode()).hexdigest()[:12]}.png"

def shadowed(layer):
    a = layer.split()[-1]; sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 1.6))))
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0)); out.alpha_composite(sh, (6, 10)); out.alpha_composite(layer); return out

def fit_font(text, path, size, maxw):
    while F(path, size).getlength(text) > maxw and size > 30: size -= 4
    return F(path, size)

def make_overlay(spec):
    kind = spec[0]; im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "pop":  # ("pop", text, colour, pos, size)
        _, text, col, pos, size = spec; f = fit_font(text, ANTON, size, W - 160)
        xy, anc = {"c": ((W // 2, Hh // 2), "mm"), "b": ((W // 2, Hh - 150), "mm"), "t": ((W // 2, 140), "mm"),
                   "l": ((90, Hh // 2), "lm"), "bl": ((90, Hh - 170), "lm"), "tl": ((90, 150), "lm")}[pos]
        stroke_text(d, xy, text, f, tuple(col), max(6, size // 14), anc); return shadowed(im)
    if kind == "stat":  # ("stat", big, label, colour)
        _, big, label, col = spec
        stroke_text(d, (90, 520), big, fit_font(big, ANTON, 230, 1100), tuple(col), 12, "ls")
        stroke_text(d, (98, 610), label, fit_font(label, ANTON, 78, 1200), WHITE, 7, "ls"); return shadowed(im)
    if kind == "list":  # ("list", [lines], colour) stacked checklist on the left
        _, lines, col = spec
        for j, l in enumerate(lines):
            chk = l.endswith("✓"); l = l.replace("✓", "").strip(); f = fit_font(l, ANTON, 104, 1500); y = 300 + j * 135
            stroke_text(d, (90, y), l, f, tuple(col), 8, "lm")
            if chk: stroke_text(d, (90 + int(f.getlength(l)) + 40, y + 6), "✓", F(INTER, 100), GREEN, 8, "lm")
        return shadowed(im)
    if kind == "year":  # ("year", 2016)
        _, yr = spec; stroke_text(d, (W // 2, 170), str(yr), F(ANTON, 230), WHITE, 12, "mm"); return shadowed(im)
    if kind == "name":  # ("name", name, school, accent)
        _, name, school, acc = spec; f = fit_font(name, ANTON, 128, 1300); nw = int(f.getlength(name))
        d.rectangle([0, Hh - 300, nw + 170, Hh - 120], fill=(0, 0, 0, 205)); d.rectangle([0, Hh - 300, 22, Hh - 120], fill=tuple(acc) + (255,))
        d.text((70, Hh - 222), name, font=f, fill=WHITE, anchor="lm")
        d.rectangle([0, Hh - 120, int(F(ANTON, 54).getlength(school)) + 130, Hh - 50], fill=tuple(acc) + (240,))
        d.text((70, Hh - 86), school, font=F(ANTON, 54), fill=WHITE, anchor="lm"); return shadowed(im)
    if kind == "quote":  # ("quote", [lines], source, highlight_line_idx) — real quote / real document wording
        _, lines, source, hl = spec; f = F(INTER, 62); lh = 92
        bw = max(int(f.getlength(l)) for l in lines) + 160; bh = len(lines) * lh + 210
        x0, y0 = (W - bw) // 2, (Hh - bh) // 2
        d.rounded_rectangle([x0 + 10, y0 + 14, x0 + bw + 10, y0 + bh + 14], 26, fill=(0, 0, 0, 140))
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 26, fill=(250, 250, 248, 255))
        for j, l in enumerate(lines):
            yy = y0 + 80 + j * lh
            if j == hl: d.rectangle([x0 + 70, yy - 6, x0 + 90 + int(f.getlength(l)), yy + 74], fill=(255, 226, 60, 255))
            d.text((x0 + 80, yy), l, font=f, fill=(15, 15, 15))
        d.text((x0 + 80, y0 + bh - 70), source, font=F(INTB, 38), fill=(110, 110, 110)); return im
    if kind == "sub":  # mid-video subscribe button (state 0 red, 1 subscribed)
        _, state = spec; x0, y0 = W - 620, Hh - 230
        d.rounded_rectangle([x0, y0, x0 + 520, y0 + 120], 60, fill=((204, 0, 0, 255) if state == 0 else (60, 60, 60, 255)))
        d.text((x0 + 260, y0 + 62), "SUBSCRIBE" if state == 0 else "SUBSCRIBED", font=F(ANTON, 64), fill=WHITE, anchor="mm")
        if state == 1:  # cursor
            cx, cy = x0 + 380, y0 + 80; d.polygon([(cx, cy), (cx, cy + 80), (cx + 22, cy + 60), (cx + 42, cy + 96), (cx + 56, cy + 88), (cx + 36, cy + 54), (cx + 64, cy + 52)], fill=WHITE, outline=BLACK)
        return shadowed(im)
    if kind == "small":  # ("small", text) bottom caption, e.g. support line
        _, text = spec; f = F(INTB, 40); tw = int(f.getlength(text))
        d.rounded_rectangle([(W - tw) // 2 - 30, Hh - 120, (W + tw) // 2 + 30, Hh - 50], 14, fill=(0, 0, 0, 190))
        d.text((W // 2, Hh - 85), text, font=f, fill=WHITE, anchor="mm"); return im
    if kind == "endq":
        stroke_text(d, (W // 2, 330), "WHICH STORY HIT YOU", F(ANTON, 150), WHITE, 10, "mm")
        stroke_text(d, (W // 2, 500), "THE HARDEST?", F(ANTON, 150), YEL, 10, "mm")
        stroke_text(d, (W // 2, 680), "TELL ME IN THE COMMENTS 👇".replace(" 👇", ""), F(ANTON, 80), WHITE, 6, "mm"); return shadowed(im)
    raise ValueError(kind)

def overlay_png(spec):
    p = ov_path(spec)
    if not os.path.exists(p): make_overlay(spec).save(p)
    return p

# ------------------------------------------------------------------ edit decision list (VO time, seconds)
E = "espn"
def c(t, src, ss, **o): return dict(t=t, src=src, ss=ss, **o)
SHOTS = [
    # cold open
    c(0.0, "ncaa2026_100", 176), c(1.7, "ncaa2016_100", 185), c(3.8, "ncaa2024_100", 101, cr=E),
    c(7.1, "coleman_doha2019", 23.5, sp=0.6), c(9.0, "ncaa2019_oduduru", 22, cr=E, bw=1), c(12.0, "ncaa2016_100", 290, bw=1),
    c(15.5, "ncaa2018_100", 165, sp=0.5, bw=1), c(18.2, "ncaa2025_100", 160, cr=E), c(21.0, "ncaa2023_100", 95),
    c(24.2, "ncaa2026_100", 246, cr=E, sp=0.6), c(26.2, "GRID_INTRO", 0), c(32.4, "ncaa2026_100", 225, cr=E, amb=1),
    c(37.9, "GRID", 0),
    # 2016 Lawson
    c(39.8, "ncaa2016_100", 220), c(43.0, "ncaa2016_100", 181, amb=1), c(45.7, "ncaa2016_100", 240, amb=1),
    c(51.8, "lawson_2017_interview", 15), c(55.7, "lawson_2017_interview", 62),
    c(59.2, "ncaa2016_100", 300, bw=1), c(61.1, "lawson_2017_interview", 95, bw=1), c(65.2, "lawson_2017_interview", 125, bw=1),
    c(70.8, "ncaa2016_100", 292, bw=1), c(73.9, "lawson_2017_interview", 150), c(76.3, "CARD", 0, base=("lawson_2017_interview", 160)),
    c(85.4, "ncaa2016_100", 305), c(86.8, "lawson_2017_interview", 180, bw=1), c(93.2, "lawson_2017_interview", 200, bw=1),
    c(95.1, "lawson_2017_interview", 212), c(99.7, "ncaa2016_100", 245, sp=0.5), c(102.0, "ncaa2016_100", 314, sp=0.6),
    c(104.6, "GRID", 1),
    # 2017 Coleman
    c(106.6, "coleman_982", 5), c(108.0, "coleman_982", 127, amb=1), c(112.9, "coleman_982", 170),
    c(115.3, "coleman_doha2019", 9, amb=1), c(121.3, "coleman_doha2019", 24),
    c(123.6, "coleman_ban_news", 21, bw=1), c(129.9, "coleman_ban_news", 0, bw=1), c(131.3, "coleman_982", 40, bw=1),
    c(135.2, "coleman_ban_news", 33), c(136.7, "coleman_doha2019", 28), c(139.5, "coleman_982", 186, amb=1),
    c(142.5, "coleman_ban_news", 10.5), c(147.2, "coleman_ban_news", 23), c(149.0, "coleman_doha2019", 27, sp=0.6),
    c(151.1, "coleman_982", 139, amb=1), c(154.7, "coleman_982", 180, bw=1),
    c(156.3, "GRID", 2),
    # 2018 Burrell (tribute)
    c(158.3, "ncaa2018_100", 27), c(159.7, "ncaa2018_100", 141, amb=1), c(161.8, "ncaa2018_100", 161, sp=0.6),
    c(164.9, "ncaa2018_100", 244), c(170.0, "ncaa2018_100", 270), c(174.1, "PHOTO", 0, photo="p_lewis.jpg"),
    c(176.7, "burrell_4x100_2017", 2), c(181.6, "ncaa2018_100", 309, sp=0.6), c(183.6, "ncaa2018_100", 283, soft=1),
    c(189.6, "ncaa2018_100", 167, sp=0.5, soft=1), c(193.6, "ncaa2018_100", 29, sp=0.5, soft=1),
    c(198.4, "GRID", 3),
    # 2019 Oduduru
    c(200.4, "ncaa2019_oduduru", 22, cr=E), c(203.2, "ncaa2019_oduduru", 0, cr=E, amb=1), c(205.3, "ncaa2019_oduduru", 92, cr=E, amb=1),
    c(209.7, "ncaa2019_oduduru", 113, cr=E), c(213.3, "ncaa2019_oduduru", 131, cr=E, bw=1),
    c(214.8, "CARD", 0, base=("ncaa2019_oduduru", 35)), c(224.6, "CARD", 0, base=("ncaa2019_oduduru", 120)),
    c(230.6, "ncaa2019_oduduru", 26, cr=E, bw=1, sp=0.5), c(233.2, "ncaa2019_oduduru", 34, cr=E, bw=1),
    c(236.5, "ncaa2019_oduduru", 150, cr=E, bw=1), c(240.3, "ncaa2019_oduduru", 37, cr=E), c(242.7, "ncaa2019_oduduru", 160, cr=E, bw=1, sp=0.5),
    c(244.8, "GRID", 4), c(246.8, "ncaa2021_100", 2, cr=E, bw=1), c(248.6, "GRIDZ", 4),
    # 2021 Laird
    c(249.6, "ncaa2021_100", 17, cr=E), c(252.9, "ncaa2021_100", 158, cr=E, amb=1), c(255.2, "ncaa2021_100", 180, cr=E),
    c(258.2, "ncaa2021_100", 189, cr=E), c(260.4, "ncaa2021_100", 217, cr=E, amb=1),
    c(262.4, "ncaa2021_100", 37, cr=E, bw=1), c(266.8, "ncaa2021_100", 200, cr=E, bw=1), c(270.4, "ncaa2021_100", 26, cr=E, bw=1, sp=0.6),
    c(275.5, "laird_la2023", 6), c(279.7, "laird_la2023", 40), c(281.2, "laird_la2023", 100, bw=1, sp=0.6),
    c(285.7, "CARD", 0, base=("ncaa2021_100", 30)), c(290.0, "ncaa2021_100", 205, cr=E, bw=1, sp=0.5),
    c(292.4, "GRID", 5),
    # 2022 Fahnbulleh
    c(294.4, "ncaa2022_100", 33, cr=E), c(296.5, "ncaa2022_100", 1, cr=E, amb=1), c(299.2, "ncaa2022_100", 56, cr=E, amb=1),
    c(301.4, "fahn_200_2022", 8, cr=E, amb=1), c(305.3, "fahn_200_2022", 24, cr=E), c(308.1, "fahn_200_2022", 46, cr=E),
    c(311.3, "fahn_200_2022", 126, cr=E), c(313.7, "ncaa2022_100", 136, cr=E), c(316.3, "ncaa2022_100", 62, cr=E, amb=1),
    c(318.2, "fahn_200_2022", 140, cr=E), c(322.9, "GRID", 6),
    # 2023 Lindsey
    c(324.9, "ncaa2023_100", 94), c(327.0, "ncaa2023_100", 70, amb=1), c(332.2, "ncaa2023_100", 126, amb=1),
    c(336.5, "ncaa2023_100", 105), c(338.6, "ncaa2023_100", 110, bw=1), c(340.1, "ncaa2023_100", 118, bw=1),
    c(347.0, "ncaa2023_100", 140, bw=1, sp=0.6), c(352.9, "GRID", 7),
    # 2024 Hinchliffe
    c(355.0, "ncaa2024_100", 43, cr=E), c(357.4, "PHOTO", 0, photo="p_lewis.jpg"), c(359.4, "ncaa2024_100", 97, cr=E, amb=1),
    c(362.0, "ncaa2024_100", 113, cr=E), c(364.9, "paris2024_100final", 26, amb=1), c(368.6, "paris2024_100final", 84, sp=0.6),
    c(370.3, "ncaa2024_100", 128, cr=E), c(374.1, "ncaa2024_100", 205, cr=E, bw=1), c(378.5, "ncaa2024_100", 230, cr=E, bw=1),
    c(381.6, "hinch_return2026", 0, vert=1), c(384.0, "hinch_return2026", 5, vert=1, amb=1), c(389.0, "hinch_return2026", 1, vert=1),
    c(393.6, "ncaa2024_100", 214, cr=E), c(398.6, "GRID", 8),
    # 2025 Anthony
    c(400.6, "ncaa2025_100", 66, cr=E), c(402.8, "ncaa2025_100", 126, cr=E, amb=1), c(405.9, "ncaa2025_100", 160, cr=E),
    c(410.2, "ncaa2025_100", 186, cr=E, amb=1), c(413.0, "ncaa2025_100", 172, cr=E), c(415.7, "ncaa2025_100", 266, cr=E),
    c(421.5, "anthony_60_worlds2026", 0, amb=1), c(424.5, "anthony_60_worlds2026", 20), c(427.0, "anthony_60_worlds2026", 47),
    c(430.6, "GRID", 9),
    # 2026 Ajayi
    c(432.6, "ncaa2026_100", 40, cr=E), c(435.3, "ncaa2026_100", 47, cr=E), c(439.9, "ncaa2026_100", 108, cr=E),
    c(442.6, "ncaa2026_100", 162, cr=E, amb=1), c(446.5, "ncaa2026_100", 238, cr=E, amb=1), c(449.6, "ncaa2026_100", 246, cr=E, sp=0.6),
    c(454.0, "ncaa2026_100", 194, cr=E), c(457.4, "ncaa2026_100", 278, cr=E), c(461.7, "ncaa2026_100", 300, cr=E, bw=1),
    # verdict
    c(463.0, "GRID", 10), c(464.4, "VERDICT", 0),
    c(489.9, "ncaa2016_100", 190, amb=1), c(492.4, "ncaa2024_100", 104, cr=E, amb=1), c(494.5, "ncaa2026_100", 178, cr=E, amb=1),
    c(496.6, "ncaa2021_100", 37, cr=E, bw=1), c(498.2, "ncaa2021_100", 200, cr=E, bw=1), c(499.0, "coleman_ban_news", 21, bw=1),
    c(499.8, "lawson_2017_interview", 95, bw=1), c(500.6, "ncaa2024_100", 230, cr=E, bw=1), c(502.2, "ncaa2026_100", 226, cr=E, amb=1),
    c(504.0, "ncaa2026_100", 240, cr=E, sp=0.6), c(509.4, "ncaa2016_100", 182, amb=1), c(511.3, "VERDICT2", 0),
    c(514.3, "ncaa2025_100", 190, cr=E, bw=1, sp=0.5),
]
VERDICT_SEQ = [(0, None), (467.0 - 464.4, 1), (469.8 - 464.4, 8), (474.0 - 464.4, 7), (476.6 - 464.4, 3), (480.2 - 464.4, 0),
               (483.7 - 464.4, 4), (485.3 - 464.4, 7), (487.2 - 464.4, 2)]
VERDICT2_SEQ = [(0, None), (512.8 - 511.3, 2)]
GRID_DUR = {i: (2.0 if i else 1.9) for i in range(11)}

def pop(t0, t1, text, col=WHITE, pos="c", size=150): return (t0, t1, ("pop", text, list(col), pos, size))
OVER = [
    pop(0.2, 1.7, "10 MEN."), pop(1.8, 3.8, "10 NATIONAL TITLES"), pop(3.9, 7.0, "10 \"FASTEST MAN IN COLLEGE\" CROWNS", size=110),
    pop(7.3, 9.0, "WORLD CHAMPION", GREEN), pop(9.2, 12.0, "BANNED UNTIL 2029", RED), pop(12.3, 15.4, "A STEAK?", AMBER),
    pop(24.3, 26.2, "\"THE NEXT ONE\"", YEL), pop(27.0, 32.4, "WHERE ARE THEY NOW?", YEL, "b", 120),
    pop(32.6, 37.8, "WHAT'S AN NCAA TITLE REALLY WORTH?", WHITE, "b", 100),
    # Lawson
    (39.9, 43.0, ("year", 2016)), (40.1, 45.6, ("name", "JARRION LAWSON", "ARKANSAS", [157, 34, 53])),
    (46.2, 51.7, ("list", ["100M  ✓", "200M  ✓", "LONG JUMP  ✓"], list(WHITE))), pop(44.2, 45.6, "FIRST SINCE JESSE OWENS · 1936", YEL, "t", 90),
    (52.0, 57.1, ("stat", "SILVER", "2017 WORLDS · LONG JUMP", list(WHITE))), pop(55.8, 59.0, "AGE: 23", YEL, "bl", 120),
    pop(59.3, 61.0, "JUNE 2018", RED, "t", 120), pop(61.3, 65.0, "POSITIVE TEST: TRENBOLONE", RED), pop(65.4, 69.3, "\"CONTAMINATED BEEF\"", AMBER),
    pop(69.5, 70.7, "NOBODY BELIEVES HIM", WHITE, "b", 100), pop(71.0, 73.8, "4-YEAR BAN", RED, "c", 200),
    (76.5, 85.3, ("quote", ["The origin of the substance was more likely", "than not contaminated beef.", "He bore no fault or negligence."],
                  "Summary of the Court of Arbitration for Sport ruling · March 2020", 2)),
    pop(85.5, 86.7, "BAN GONE.", GREEN, "c", 200), pop(87.0, 90.7, "2 YEARS GONE", RED), pop(90.9, 93.1, "MISSED 2019 WORLDS", RED, "b", 110),
    pop(93.3, 95.0, "KNEE INJURY", RED), (95.2, 99.6, ("stat", "8.14M", "ZAGREB · JUNE 2026", list(YEL))),
    # Coleman
    (106.7, 109.0, ("year", 2017)), (106.9, 112.0, ("name", "CHRISTIAN COLEMAN", "TENNESSEE", [255, 130, 0])),
    (109.2, 115.2, ("stat", "9.82", "COLLEGIATE RECORD · STILL #1", list(YEL))),
    (119.4, 123.5, ("stat", "9.76", "WORLD CHAMPION · DOHA 2019", list(GREEN))),
    pop(126.5, 127.6, "MISSED TESTS", RED), pop(127.7, 128.8, "NOT FAILED.", WHITE), pop(128.9, 129.8, "MISSED.", RED, "c", 220),
    pop(130.0, 131.2, "WHEREABOUTS VIOLATIONS", RED), pop(131.4, 135.1, "BANNED · MISSED TOKYO 2020", RED),
    (136.8, 142.4, ("list", ["2024 WORLD INDOOR 60M  ✓", "WORLD RELAY GOLD  ✓", "DIAMOND LEAGUE TITLES  ✓"], list(GREEN))),
    pop(142.6, 147.1, "FEB 2026: ARRESTED", RED, "t", 120), pop(147.3, 148.9, "PLEADED NOT GUILTY", WHITE, "b", 110),
    pop(154.8, 156.2, "A BAN + AN ARREST", AMBER),
    # Burrell
    (158.4, 161.6, ("year", 2018)), (158.6, 163.8, ("name", "CAMERON BURRELL", "HOUSTON", [200, 16, 46])),
    pop(165.1, 169.9, "DAD: LEROY BURRELL · 100M WORLD RECORD", WHITE, "t", 90),
    pop(170.1, 174.0, "MOM: MICHELLE FINN-BURRELL · OLYMPIC GOLD", WHITE, "t", 90),
    pop(174.2, 176.6, "GODFATHER: CARL LEWIS", YEL, "b", 110), pop(176.8, 181.5, "HOUSTON 4X100 · NCAA CHAMPIONS", WHITE, "b", 100),
    pop(197.4, 198.3, "REST EASY, CAM.", WHITE, "c", 150),
    (189.6, 198.3, ("small", "If you're struggling, you're not alone. In the US, call or text 988.")),
    # Oduduru
    (200.5, 203.1, ("year", 2019)), (200.7, 205.2, ("name", "DIVINE ODUDURU", "TEXAS TECH · NIGERIA", [204, 0, 0])),
    (205.4, 209.6, ("stat", "9.86 + 19.73", "SAME MEET · NCAA 2019", list(YEL))), pop(213.4, 214.7, "THEN THE FEDS GOT INVOLVED", RED),
    (215.0, 224.4, ("quote", ["Eric Lira: the first person charged under", "the Rodchenkov Anti-Doping Act,", "the U.S. law that makes doping fraud a crime."],
                    "Summary · U.S. Department of Justice, 2022 · Lira pleaded guilty", 0)),
    (224.7, 230.4, ("quote", ["\"Athlete 1\"  =  Blessing Okagbare", "\"Athlete 2\"  =  ?"], "Criminal complaint, U.S. v. Eric Lira", 1)),
    pop(230.8, 233.1, "ATHLETE 2 = DIVINE ODUDURU", RED), pop(233.3, 236.4, "BANNED UNTIL FEB 2029", RED, "c", 170),
    pop(236.6, 240.2, "RESULTS SINCE JULY 2021: ERASED", RED), pop(240.4, 242.6, "HE SAYS HE WAS SET UP", WHITE, "b", 110),
    pop(246.9, 248.5, "2020: CANCELED · COVID-19", WHITE, "c", 130),
    (249.0, 256.0, ("sub", 0)), (254.0, 256.5, ("sub", 1)),
    # Laird
    (249.7, 252.8, ("year", 2021)), (249.9, 254.8, ("name", "TERRANCE LAIRD", "LSU", [253, 208, 35])),
    (255.3, 258.1, ("list", ["100M CHAMP  ✓", "200M CHAMP  ✓"], list(WHITE))), pop(258.3, 260.3, "TURNS PRO · ADIDAS", WHITE, "b", 110),
    pop(262.5, 266.7, "RACING ON A BROKEN BACK", RED), pop(266.9, 270.3, "SPINAL DECOMPRESSION · 2X A WEEK", RED, "b", 100),
    pop(271.8, 273.1, "HERNIATED DISCS", RED, "c", 170), pop(273.3, 275.4, "MISSED ALL OF 2022", RED, "b", 110),
    (275.6, 281.1, ("stat", "20.06", "2023 · LA GRAND PRIX · 200M", list(GREEN))), pop(281.4, 285.5, "...AND THEN, QUIET.", WHITE),
    (285.8, 289.9, ("quote", ["\"Terrance Laird - Anyone know what", "happened to him this year?\"", "\"What happened to Terrance Laird\""],
                    "LetsRun.com message board threads", 2)),
    # Fahnbulleh
    (294.5, 296.4, ("year", 2022)), (294.7, 299.1, ("name", "JOSEPH FAHNBULLEH", "FLORIDA · LIBERIA", [0, 33, 165])),
    pop(301.5, 305.2, "OLYMPIC 200M FINALS: TOKYO + PARIS", WHITE, "t", 96), pop(305.4, 308.0, "2024 AFRICAN CHAMPION · 100 + 200", WHITE, "t", 96),
    (308.2, 311.2, ("stat", "19.83", "LIBERIAN RECORD · 200M", list(YEL))), pop(311.4, 313.6, "STILL ON THE DIAMOND LEAGUE", WHITE, "b", 100),
    (313.8, 316.2, ("stat", "0", "GLOBAL MEDALS", list(RED))), pop(318.3, 322.8, "GRINDING. ONE PAYCHECK AT A TIME.", AMBER, "b", 100),
    # Lindsey
    (325.0, 327.0, ("year", 2023)), (325.2, 329.5, ("name", "COURTNEY LINDSEY", "TEXAS TECH", [204, 0, 0])),
    pop(327.2, 332.0, "TURNS PRO · NIKE", WHITE, "t", 110), (332.3, 334.2, ("stat", "19.71", "200M · 2024", list(YEL))),
    (334.2, 336.4, ("stat", "9.82", "100M · 2025", list(YEL))), pop(336.6, 338.5, "WORLD-CLASS FAST", GREEN),
    (340.2, 346.1, ("stat", "5TH", "2026 USA CHAMPIONSHIPS · 9.97", list(RED))), pop(346.3, 346.9, "FIFTH.", RED, "c", 220),
    pop(347.2, 352.8, "9.8 = A PLANE TICKET HOME", WHITE, "b", 110),
    # Hinchliffe
    (355.1, 357.3, ("year", 2024)), (355.3, 359.3, ("name", "LOUIE HINCHLIFFE", "HOUSTON · GREAT BRITAIN", [200, 16, 46])),
    pop(357.5, 359.3, "COACH: CARL LEWIS", YEL, "b", 110), (359.5, 364.8, ("stat", "9.95", "NCAA CHAMPION · 2024", list(YEL))),
    pop(365.0, 368.5, "WEEKS LATER: THE OLYMPIC 100M FINAL", WHITE, "t", 96), pop(370.4, 374.0, "TURNS PRO · ASICS", WHITE, "b", 110),
    pop(374.2, 376.7, "2025", RED, "t", 150), (376.9, 381.5, ("list", ["STRESS FRACTURE", "HAMSTRING", "LOSES HIS FATHER"], list(RED))),
    pop(384.1, 389.0, "GIVES UP THE PRO DEAL", YEL, "t", 110), pop(389.1, 393.5, "BACK TO HOUSTON. BACK TO CARL LEWIS.", WHITE, "b", 96),
    # Anthony
    (400.7, 402.7, ("year", 2025)), (400.9, 405.8, ("name", "JORDAN ANTHONY", "ARKANSAS", [157, 34, 53])),
    pop(404.6, 405.8, "FOOTBALL PLAYER", AMBER, "t", 120), pop(406.0, 410.1, "WR: KENTUCKY → TEXAS A&M → ARKANSAS", WHITE, "t", 96),
    pop(410.3, 412.9, "NCAA 100M CHAMP · 10.07", YEL, "b", 110), pop(413.1, 415.6, "TURNS PRO · ADIDAS", WHITE, "b", 110),
    pop(415.8, 419.0, "THE BOWERMAN AWARD", YEL), pop(419.2, 421.4, "FIRST FOOTBALL PLAYER EVER", GREEN, "b", 110),
    (421.6, 425.2, ("stat", "6.41", "WORLD INDOOR 60M CHAMPION · 2026", list(GREEN))),
    # Ajayi
    (432.7, 435.2, ("year", 2026)), (432.9, 439.8, ("name", "KANYINSOLA AJAYI", "AUBURN · NIGERIA", [232, 119, 34])),
    (442.7, 446.4, ("stat", "9.72w", "NCAA CHAMPION · 2026", list(YEL))),
    (449.7, 457.3, ("list", ["PRE CLASSIC WIN  ✓", "LONDON DIAMOND LEAGUE WIN  ✓", "COMMONWEALTH BRONZE  ✓"], list(GREEN))),
    pop(457.5, 461.6, "AGE 22", YEL, "bl", 130), pop(461.8, 463.0, "SO DID EVERY NAME IN THIS VIDEO", WHITE, "b", 100),
    # verdict
    pop(464.5, 466.9, "LET'S ADD IT UP", YEL, "b", 110),
    pop(490.0, 496.5, "ONE DAY IN JUNE", YEL, "b", 120), pop(498.3, 502.1, "INJURIES · TESTERS · AGENTS · MONEY · LUCK", RED, "c", 104),
    pop(502.3, 503.9, "NONE OF IT'S ON THE RESULTS SHEET", WHITE, "b", 100), pop(504.2, 509.3, "\"HE'S THE NEXT ONE\"", YEL),
    pop(509.5, 511.2, "RUN IT BACK.", WHITE, "c", 170), pop(511.4, 512.7, "ASK THESE NINE.", WHITE, "b", 120),
    pop(512.8, 514.2, "REMEMBER THE TENTH.", YEL, "b", 120), (514.4, END, ("endq",)),
]

# ------------------------------------------------------------------ shot rendering
CROPS = {"espn": "crop=iw*0.9:ih*0.9:iw*0.05:0,"}

def card_base(src, ss, out):
    if not os.path.exists(out):
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", f"{REAL}/{src}.mp4", "-frames:v", "1", out])
    im = Image.open(out).convert("RGB").resize((W, Hh)).filter(ImageFilter.GaussianBlur(10))
    return ImageEnhance.Brightness(ImageOps.grayscale(im).convert("RGB")).enhance(0.4)

def render_shot(i, sh, t1):
    out = f"{R}/shots/{i:03d}.mp4"
    dur = (round(t1 * FPS) - round(sh["t"] * FPS)) / FPS  # frame-exact so the picture never drifts from the voice
    key = json.dumps([sh, dur, [o for o in OVER if o[0] < t1 and o[1] > sh["t"]]], sort_keys=True, default=str)
    stamp = f"{out}.key"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == key: return out
    src = sh["src"]; ins = []; vf = []
    if src in ("GRID", "GRIDZ", "GRID_INTRO", "VERDICT", "VERDICT2"):
        if src == "GRID_INTRO": f = grid_intro(dur)
        elif src == "VERDICT": f = grid_verdict(VERDICT_SEQ, dur, "verdict")
        elif src == "VERDICT2": f = grid_verdict(VERDICT2_SEQ, dur, "verdict2")
        elif src == "GRIDZ":  # zoom only (no stamp) into tile ss+1
            f = f"{R}/grid/zoom_{sh['ss'] + 1}.mp4"
            if not os.path.exists(f):
                base = grid_frame(sh["ss"] + 1, active=sh["ss"] + 1); x, y = tile_xy(sh["ss"] + 1); n = int(round(dur * FPS))
                write_frames(lambda q: zoom_to(base, x + TW / 2, y + TW / 2, 1 + 2.2 * ease(q / max(1, n - 1))), n, f)
        else: f = grid_step(sh["ss"], dur)
        ins = ["-i", f]; base = "[0:v]scale=1920:1080,setsar=1"; amb = False
    elif src == "CARD":
        cb = f"{R}/cards/{i:03d}.png"; card_base(*sh["base"], f"{R}/cards/{i:03d}_src.png").save(cb)
        ins = ["-loop", "1", "-t", str(dur), "-i", cb]; base = f"[0:v]scale='trunc(1920*(1+0.05*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1"; amb = False
    elif src == "PHOTO":
        ins = ["-loop", "1", "-t", str(dur), "-i", f"{SCR}/photos/{sh['photo']}"]
        base = ("[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30,eq=brightness=-0.18[bg];"
                f"[b]scale=-2:'trunc(980*(1+0.04*t/{dur})/2)*2':eval=frame[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"); amb = False
    else:
        sp = sh.get("sp", 1.0); sdur = dur * sp
        ins = ["-ss", str(sh["ss"]), "-t", f"{sdur:.3f}", "-i", f"{REAL}/{src}.mp4"]
        cr = CROPS.get(sh.get("cr"), "")
        if sh.get("vert"):
            base = (f"[0:v]setpts=PTS/{sp},split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=28,eq=brightness=-0.2[bg];"
                    "[b]scale=-2:1000[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
        else:
            z = 0.06
            base = (f"[0:v]{cr}setpts=(PTS-STARTPTS)/{sp},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                    f"scale='trunc(1920*(1+{z}*t/{dur})/2)*2':-2:eval=frame,crop=1920:1080,setsar=1")
        if sh.get("bw"): base += ",hue=s=0,eq=contrast=1.28:brightness=-0.04"
        elif sh.get("soft"): base += ",eq=saturation=0.55:brightness=-0.02"
        else: base += ",eq=contrast=1.08:saturation=1.12"
        amb = bool(sh.get("amb")) and sp == 1.0
    vf.append(base + ",fps=24,format=yuva420p[b0]")
    k = 0
    for (o0, o1, spec) in OVER:
        if o0 >= t1 or o1 <= sh["t"]: continue
        a, b = max(0, o0 - sh["t"]), min(dur, o1 - sh["t"]); png = overlay_png(spec); k += 1
        ins += ["-loop", "1", "-t", f"{b:.3f}", "-i", png]
        fin = 0.16 if o0 >= sh["t"] else 0; fout = 0.16 if o1 <= t1 else 0
        chain = f"[{k}:v]format=rgba"
        if fin: chain += f",fade=in:st={a:.3f}:d={fin}:alpha=1"
        if fout: chain += f",fade=out:st={b - fout:.3f}:d={fout}:alpha=1"
        slide = f"if(lt(t-{a:.3f},0.22),46*(1-(t-{a:.3f})/0.22),0)" if fin else "0"
        vf.append(chain + f"[o{k}];[b{k - 1}][o{k}]overlay=x=0:y='{slide}':enable='between(t,{a:.3f},{b:.3f})'[b{k}]")
    vf.append(f"[b{k}]format=yuv420p[v]")
    aud = ["-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo"]
    amap = f"{k + 1}:a"
    if amb: vf.append("[0:a]aresample=48000,volume=0.22,highpass=f=120[a]"); amap = "[a]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + ins + aud + ["-filter_complex", ";".join(vf), "-map", "[v]", "-map", amap,
           "-t", str(dur), "-r", "24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-ar", "48000", "-ac", "2", out]
    run(cmd); open(stamp, "w").write(key); return out

def shot_list():
    out = []
    for i, sh in enumerate(SHOTS):
        t1 = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END
        out.append((i, sh, t1))
    return out

def stage_shots():
    from concurrent.futures import ThreadPoolExecutor
    # grids first (sequential, PIL heavy) so the parallel ffmpeg pass never races on them
    for i, sh, t1 in shot_list():
        if sh["src"] == "GRID": grid_step(sh["ss"], (round(t1 * FPS) - round(sh["t"] * FPS)) / FPS)
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda a: render_shot(*a), shot_list()))
    print("shots", len(SHOTS))

def stage_concat():
    lst = f"{R}/concat.txt"
    open(lst, "w").write("".join(f"file '{R}/shots/{i:03d}.mp4'\n" for i, _, _ in shot_list()))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/picture.mp4"])
    print("concat", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/picture.mp4"]).stdout.strip())

# ------------------------------------------------------------------ audio
def sfx_list():
    S = []
    for (o0, o1, spec) in OVER:
        if spec[0] == "year": S.append((o0 - 0.05, "sub-boom", 0.55))
        elif spec[0] in ("pop", "stat", "list", "name"): S.append((o0 - 0.08, "whoosh", 0.22))
        elif spec[0] == "quote": S.append((o0 - 0.05, "newspaper-rip", 0.3))
    for sh in SHOTS:
        if sh["src"] == "GRID" and 0 < sh["ss"] and sh["ss"] != 3: S.append((sh["t"] + 0.12, "rubber-stamp", 0.6))
        if sh["src"] in ("GRID", "GRIDZ") and sh["ss"] < 10: S.append((sh["t"] + 0.8, "whoosh", 0.4))
    S += [(59.2, "record-scratch", 0.45), (213.2, "record-scratch", 0.45), (0.0, "sub-boom", 0.6), (26.2, "sub-boom", 0.5)]
    return S

def stage_audio():
    M = f"{P}/music"
    # trap bed: loop to cover the whole film, dip out for the Burrell tribute (156.5-200), tribute piano underneath
    vol = ("volume='0.17*(1-0.94*between(t,157.6,199.6))"
           "*if(between(t,156.4,157.6),1-(t-156.4)/1.2*0.94,1)*if(between(t,199.6,201.0),0.06+(t-199.6)/1.4*0.94,1)':eval=frame")
    trap = f"{R}/trap_full.wav"
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "2", "-i", f"{M}/trap_bed.mp3", "-t", str(END), "-af", vol + f",afade=t=out:st={END - 4}:d=4", "-ar", "48000", "-ac", "2", trap])
    trib = f"{R}/tribute.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{M}/tribute.mp3", "-t", "44", "-af",
         "volume=0.3,afade=t=in:st=0:d=1.5,afade=t=out:st=40.5:d=3.5,adelay=156800|156800", "-ar", "48000", "-ac", "2", trib])
    S = sfx_list(); ins = []; fl = []
    for j, (t, n, g) in enumerate(S):
        ins += ["-i", f"{SFXD}/{n}.mp3"]; d = int(max(0, t) * 1000)
        fl.append(f"[{j + 4}:a]volume={g},adelay={d}|{d},aformat=sample_rates=48000:channel_layouts=stereo[s{j}]")
    mix_in = "".join(f"[s{j}]" for j in range(len(S)))
    fc = ";".join(fl) + (";" if fl else "") + \
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0[vo];[1:a]volume=1.0[amb];" \
        f"[vo]asplit=2[vo1][vo2];[2:a][vo2]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400[duck];" \
        f"[vo1][duck][3:a][amb]{mix_in}amix=inputs={4 + len(S)}:normalize=0:duration=first,alimiter=limit=0.95[out]"
    run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", f"apad=whole_dur={END}", "-ar", "48000", "-ac", "2", f"{R}/vo_pad.wav"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", f"{R}/vo_pad.wav", "-i", f"{R}/picture.mp4", "-i", trap, "-i", trib] + ins + \
          ["-filter_complex", fc, "-map", "[out]", "-t", str(END), "-ar", "48000", f"{R}/mix.wav"]
    run(cmd); print("audio", len(S), "sfx")

def stage_mux():
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", str(END), "-movflags", "+faststart", OUT])
    print("wrote", OUT)

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")

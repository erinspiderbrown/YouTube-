"""NCAA cross country "takeover" documentary build: voiceover-driven, real footage + Commons photos,
neon motion graphics (ncaa_mograph.py). Same pipeline as projects/jon-drummond/jd_build.py.

Shot kinds:
  g  motion graphic (ncaa_mograph, neon look)
  a  real footage, full-bleed + ARCHIVE tag      f  real footage, framed in neon over a blurred backdrop
  opts: e = source end, yb = vertical crop bias, tag = label, cr = (x0, y0, x1, y1) fractional crop after cropdetect
Stages: shots -> transitions -> compose (HUD keywords, grain) -> audio -> mux
Run:  python3 -I projects/ncaa-xc-takeover/ncaa_build.py [stage ...]
"""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"
P = f"{ROOT}/projects/ncaa-xc-takeover"
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
R = f"{SCR}/render_ncaa"; os.makedirs(f"{R}/frames", exist_ok=True)
REAL = f"{SCR}/real"      # YouTube imports via vidIQ (see credits.md)
PHOTOS = f"{SCR}/photos"  # Wikimedia Commons photos (credits.json)
MUSIC_DIR = f"{ROOT}/projects/jon-drummond/music"; SFX_DIR = f"{ROOT}/projects/jon-drummond/sfx"
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, P)
import mograph as M
import neon as N
N.PHOTOS = PHOTOS
M.finish = N.finish
import ncaa_mograph as J, hud, sounds, transitions as TR
import gfx

FPS = 24
VO = f"{P}/ncaa-xc_voiceover_v4.mp3"  # v4: Kenya/Kenyan respelled "Kinya/Kinyan" (user: Texas pronunciation), else as v3
END_V1 = 596.2
OUT = f"{SCR}/output/ncaa-xc_v4_master.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:800]); print(r.stderr[-2000:]); raise SystemExit(1)

def rl(n): return f"{REAL}/{n}.mp4"
M25, W25, PRS, ITN, WCC, PAC = rl("ncaa2025_men"), rl("ncaa2025_women"), rl("presser_men_2025"), rl("iten_vice"), rl("wsu_wcc2025"), rl("wsu_pac12_2026")
KNT, SEO, RAP, RST, MJ, HED = rl("knighton"), rl("seoul1988_100m"), rl("rono_1978_ap"), rl("rono_1978_steeple"), rl("montgomery_jones_ap"), rl("hedengren_big12_2026")
TAGS = {M25: "NCAA XC · Columbia MO · 2025", W25: "NCAA XC Women · 2025", PRS: "NCAA XC press conf · 2025", ITN: "Iten, Kenya",
        WCC: "WCC XC · 2025 · Kipchoge", PAC: "Pac-12 XC · 2026", KNT: "Knighton case · 2024–25", SEO: "Seoul Olympics · 1988",
        RAP: "Oslo · 1978 · Rono WR", RST: "Commonwealth Games · 1978", MJ: "AP Archive", HED: "Big 12 XC · 2026"}
SRC_CR = {M25: (0.19, 0.0, 1.0, 0.87), W25: (0.19, 0.0, 1.0, 0.87), ITN: (0.0, 0.07, 0.9, 1.0), RAP: (0.0, 0.0, 0.86, 1.0),
          MJ: (0.0, 0.0, 0.86, 1.0), SEO: (0.0, 0.0, 1.0, 0.8)}

SHOTS = [
    # ---- 01 cold open
    (0.0, "a", M25, 8.0), (1.7, "g", "title_card", 0), (5.0, "a", M25, 63.0), (8.8, "a", M25, 61.0, {"e": 75.0}),
    (11.1, "g", "results", 0), (22.8, "a", W25, 1095.0), (26.1, "a", M25, 1211.0), (31.0, "f", M25, 1938.0, {"cr": (0, 0, 1, 1)}),
    (32.3, "g", "c_guests", 0), (39.2, "g", "c_30plus", 0), (44.1, "a", M25, 1817.0), (46.8, "g", "c_congrats", 0),
    (51.2, "a", M25, 1272.0), (54.5, "g", "legal", 0), (62.9, "a", M25, 424.0), (67.1, "a", M25, 2120.0),
    # ---- 02 this ain't new
    (69.7, "a", RST, 15.0), (72.7, "g", "cover1977", 0), (79.2, "f", RAP, 2.0), (84.0, "a", RST, 121.0),
    (87.8, "g", "rono_stats", 0), (96.0, "f", RAP, 28.0), (99.6, "g", "fifty_years", 0),
    # ---- 03 college is for adults
    (108.1, "a", WCC, 1378.0, {"yb": 0.2}), (111.5, "g", "kipchoge_file", 0), (120.9, "a", WCC, 240.0), (124.0, "g", "age_limit", 0),
    (135.2, "a", M25, 545.0), (138.1, "g", "eligibility", 0), (145.8, "g", "same_rule", 0), (159.5, "g", "dunkley", 0),
    (168.5, "f", WCC, 480.0), (172.2, "a", PAC, 1209.0), (174.3, "g", "third_place", 0),
    # ---- 04 a better situation
    (180.3, "a", ITN, 38.0, {"e": 41.9}), (182.9, "a", ITN, 62.0, {"e": 64.6}), (186.2, "a", ITN, 162.0, {"e": 170.5}), (190.0, "a", ITN, 80.0, {"e": 83.5}),
    (192.6, "g", "offer", 0), (202.4, "a", ITN, 497.5, {"e": 505.5}), (206.2, "g", "pipeline", 0), (220.0, "g", "share", 0), (227.1, "g", "went_got", 0),
    # ---- 05 the hate
    (233.5, "g", "two_groups", 0), (238.2, "a", M25, 485.0), (240.8, "g", "eyestone", 0), (250.7, "a", W25, 365.0),
    (254.7, "g", "smith", 0), (260.6, "a", M25, 1211.0), (264.0, "a", M25, 1878.0), (268.0, "a", M25, 61.0),
    (275.1, "f", M25, 2120.0, {"tag": "NCAA Championships · YouTube"}), (282.9, "g", "c_guests", 0), (286.0, "g", "c_corrupt", 0),
    (293.8, "g", "c_imported", 0), (297.1, "g", "imported", 0), (299.6, "g", "no_rule", 0), (313.2, "g", "sports_grid", 0),
    (328.4, "a", M25, 1696.0),
    # ---- 06a doping: testing
    (332.7, "a", W25, 203.0), (338.7, "g", "cases", 0), (353.1, "g", "category_a", 0), (372.4, "a", ITN, 434.0, {"e": 470.0}),
    (377.7, "g", "usa_not", 0), (380.9, "g", "tests_compare", 0),
    # ---- 06b America
    (393.2, "f", SEO, 0.5), (396.1, "g", "exum", 0), (414.6, "a", SEO, 69.0), (416.5, "g", "lewis", 0),
    (434.3, "f", MJ, 54.0), (437.5, "f", MJ, 34.0), (442.6, "g", "informants", 0), (455.9, "a", KNT, 324.0),
    (459.0, "g", "knighton", 0), (465.5, "f", KNT, 170.0), (471.6, "g", "double_standard", 0), (481.9, "g", "cheaters", 0),
    # ---- 07 the rule change
    (490.9, "a", M25, 1757.0), (495.4, "g", "five_in_five", 0), (509.0, "g", "old_rules", 0), (515.3, "g", "clock", 0),
    # ---- 08 nov 21
    (527.0, "f", HED, 0.0), (531.7, "a", W25, 1136.0), (535.8, "g", "matchup", 0), (542.0, "g", "nov21", 0),
    (552.7, "a", M25, 8.0), (557.3, "a", RST, 152.0), (560.6, "a", WCC, 1378.0, {"yb": 0.2}), (563.8, "a", M25, 1817.0),
    (567.0, "g", "what_rule", 0), (577.3, "a", M25, 121.0), (584.2, "g", "end_card", 0),
]

KEYWORDS = [  # (vo_time, text, dur, pos)
    (0.3, "NATIONALS\n2025", 1.4, "left"), (22.9, "COURSE\nRECORD", 2.4, "right"), (26.3, "KENYA +\nMOROCCO", 2.6, "right"),
    (62.9, "SO WHY\nTHE OUTRAGE?", 3.0, "left"), (69.8, "THIS AIN'T\nNEW", 2.6, "left"), (84.1, "HENRY\nRONO", 2.6, "right"),
    (108.2, "28-YEAR-OLD\nFRESHMAN", 3.0, "left"), (121.0, "IS IT\nTHOUGH?", 2.6, "left"), (172.3, "WASHINGTON\nSTATE", 1.9, "right"),
    (180.4, "THEIR\nSIDE", 2.4, "left"), (202.5, "WHO'S TURNING\nTHAT DOWN?", 3.0, "left"), (260.7, "SHUT UP\n& COACH", 3.0, "right"),
    (264.1, "THE\nCOMMENTS", 3.4, "left"), (328.5, "ABOUT\nTHE RULES?", 3.0, "left"), (332.8, "DOPING", 2.4, "left"),
    (414.7, "CARL\nLEWIS", 1.8, "right"), (434.4, "BALCO", 2.4, "right"), (455.9, "ERRIYON\nKNIGHTON", 2.6, "right"),
    (490.9, "THE\nPROOF", 2.4, "left"), (531.8, "2ND TO\nA KENYAN", 3.0, "right"), (552.8, "LINE UP.\nRUN.", 3.0, "left"),
    (563.9, "THE RUNNERS\nJUST RAN", 3.0, "left"),
]
SFX = [  # (vo_time, file, gain)
    (0.05, "sub-boom", 0.9), (8.85, "starting-gun", 0.5), (11.1, "whoosh", 0.5), (57.9, "rubber-stamp", 0.9), (69.7, "whoosh", 0.6),
    (72.8, "newspaper-rip", 0.6), (108.1, "whoosh", 0.6), (180.3, "whoosh", 0.6), (233.5, "whoosh", 0.6), (297.1, "sub-boom", 0.9),
    (301.8, "sub-boom", 0.6), (332.7, "whoosh", 0.6), (393.2, "whoosh", 0.6), (471.6, "sub-boom", 0.8), (490.9, "whoosh", 0.6),
    (495.7, "sub-boom", 0.8), (527.0, "whoosh", 0.6), (552.7, "crowd-roar", 0.5), (574.2, "sub-boom", 0.9), (584.2, "sub-boom", 0.8),
]
MUSIC = [  # (file, start, gain, fade_out_at)
    ("M1_cold-open-background", 0.0, 0.55, 96.0), ("M2_sydney", 104.0, 0.5, 170.0), ("M3_rule-paris-fallout", 178.0, 0.55, 316.0),
    ("M4_coaching-ban", 330.0, 0.5, 422.0), ("M5_verdict-ending", 428.0, 0.55, 490.0), ("M3_rule-paris-fallout", 494.0, 0.5, 592.0),
]

# ---- v2 retime: every time above was set against the v1 voiceover; T() maps v1 time -> v2 time (word-aligned)
_TM = np.array(json.load(open(f"{P}/vo_timemap_v1_to_v4.json")))
def T(x):
    if x <= _TM[-1, 0]: return float(np.interp(x, _TM[:, 0], _TM[:, 1]))
    return float(_TM[-1, 1] + (x - _TM[-1, 0]))
END = T(584.2) + (END_V1 - 584.2)
KEYWORDS = [(T(t), txt, d, pos) for t, txt, d, pos in KEYWORDS]
SFX = [(T(t), n, g) for t, n, g in SFX]
MUSIC = [(n, T(s), g, T(fo)) for n, s, g, fo in MUSIC]

def shots():
    out = []
    for i, x in enumerate(SHOTS):
        s0, k, src, off = x[:4]; opt = x[4] if len(x) > 4 else {}
        e0 = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END_V1
        s, e = T(s0), (T(e0) if i + 1 < len(SHOTS) else END)
        f0, f1 = round(s * FPS), round(e * FPS)
        out.append(dict(i=i, start=f0 / FPS, frames=f1 - f0, kind=k, src=src, off=off, opt=opt, scale=(e - s) / (e0 - s0)))
    return out

def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)

_crop = {}
def cropdetect(path, at=1.0, overscan=0.0):
    key = (path, round(at, 1), overscan)
    if key not in _crop:
        r = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{at:.2f}", "-i", path, "-vf", "cropdetect=30:2:0", "-frames:v", "14", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        c = [l.split("crop=")[-1].strip() for l in r.splitlines() if "crop=" in l]
        if not c: _crop[key] = None
        else:
            w, h, x, y = map(int, Counter(c[2:] or c).most_common(1)[0][0].split(":"))
            ox, oy = int(w * overscan) // 2 * 2, int(h * overscan) // 2 * 2
            _crop[key] = (w - 2 * ox, h - 2 * oy, x + ox, y + oy)
    return _crop[key]

GRADE = "eq=contrast=1.12:saturation=1.08:brightness=-0.02,colorbalance=rs=-0.04:bs=0.06:rh=0.05:bh=-0.04"
GRADE_A = "eq=contrast=1.08:saturation=1.14:gamma=0.97,unsharp=5:5:0.55:5:5:0.0"
NEON_COLS = [N.ORANGE, N.CYAN]

def enc(out):
    return ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), out]

def frame_png(tag, box, color, kind="ARCHIVE"):
    key = f"{kind}_{tag}_{box}_{color}".encode().hex()[:120]
    f = f"{R}/frames/{key}.png"
    if not os.path.exists(f):
        N.archive_frame(tag, box=box, color=color, accent=N.CYAN if color == N.ORANGE else N.ORANGE, kind=kind).save(f)
    return f

def render_archive(sh, out):
    n = sh["frames"]; d = n / FPS; o = sh["opt"]; src = sh["src"]
    cw, ch, cx, cy = cropdetect(src, sh["off"] + 0.3, overscan=0.03)
    fx0, fy0, fx1, fy1 = o.get("cr", SRC_CR.get(src, (0, 0, 1, 1)))
    cx, cy = cx + int(cw * fx0) // 2 * 2, cy + int(ch * fy0) // 2 * 2
    cw, ch = int(cw * (fx1 - fx0)) // 2 * 2, int(ch * (fy1 - fy0)) // 2 * 2
    avail = max(0.4, o.get("e", dur(src)) - sh["off"])
    slow = min(2.0, max(1.0, d / avail))
    tag = o.get("tag", TAGS.get(src, "Archive"))
    col = NEON_COLS[sh["i"] % 2]
    pre = (f"crop={cw}:{ch}:{cx}:{cy},setpts=PTS*{slow:.4f},fps={FPS},tpad=stop_mode=clone:stop_duration=30,{GRADE_A}")
    if sh["kind"] == "a":
        yb = o.get("yb", 0.4)
        fc = (f"[0:v]{pre},scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080:(iw-1920)/2:(ih-1080)*{yb},"
              f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS},vignette=angle=PI/5[v];"
              f"[1:v]format=rgba[o];[v][o]overlay=0:0,format=yuv420p[out]")
        png = frame_png(tag, None, col)
    else:
        fh = 900; fw = round(fh * cw / ch / 2) * 2
        if fw > 1640: fw = 1640; fh = round(fw * ch / cw / 2) * 2
        x0, y0 = (1920 - fw) // 2, (1080 - fh) // 2
        fc = (f"[0:v]{pre},split[a][b];"
              f"[a]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,boxblur=10:2,scale=1920:1080,"
              f"eq=brightness=-0.24:saturation=1.5[bg];"
              f"[b]scale={fw}:{fh}:flags=lanczos,zoompan=z='1+0.05*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={fw}x{fh}:fps={FPS}[fg];"
              f"[bg][fg]overlay={x0}:{y0},vignette=angle=PI/4[v];[1:v]format=rgba[o];[v][o]overlay=0:0,format=yuv420p[out]")
        png = frame_png(tag, (x0 - 3, y0 - 3, x0 + fw + 2, y0 + fh + 2), col)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sh['off']:.3f}", "-i", src, "-loop", "1", "-i", png,
         "-filter_complex", fc, "-map", "[out]", "-frames:v", str(n)] + enc(out))

def render_photo(sh, out):
    n = sh["frames"]; o = sh["opt"]
    im0 = Image.open(f"{PHOTOS}/{sh['src']}.jpg").convert("RGB")
    w, h = im0.size
    col = NEON_COLS[sh["i"] % 2]
    bg = ImageOps.fit(im0, (480, 270)).filter(ImageFilter.GaussianBlur(9)).resize((1920, 1080), Image.BILINEAR)
    bg = ImageEnhance.Color(ImageEnhance.Brightness(bg).enhance(0.32)).enhance(1.4)
    sc = min(1480 / w, 800 / h); pw, ph = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
    x0, y0 = (1920 - pw) // 2, (1080 - ph) // 2 - 30
    big = im0.resize((int(pw * 1.08), int(ph * 1.08)), Image.LANCZOS)
    frame = N.glow_rect((1920, 1080), [x0 - 3, y0 - 3, x0 + pw + 2, y0 + ph + 2], col, width=4, blur=20)
    tagl = N.archive_frame(o.get("tag", "Photo"), box=None, color=col, kind="IMG")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-"] + enc(out),
                            stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        z = 1.0 + 0.07 * i / max(1, n - 1)
        ww, hh = big.width / z / 1.08 * 1.0, big.height / z / 1.08
        cx, cy = big.width / 2, big.height / 2
        pic = big.crop((int(cx - ww / 2), int(cy - hh / 2), int(cx + ww / 2), int(cy + hh / 2))).resize((pw, ph), Image.BILINEAR)
        k = N.eback(N.seg(t, 0, 0.4))
        s = 0.9 + 0.1 * k
        im = bg.copy()
        if s < 0.999:
            pp = pic.resize((int(pw * s), int(ph * s)), Image.BILINEAR)
            im.paste(pp, (x0 + (pw - pp.width) // 2, y0 + (ph - pp.height) // 2))
        else:
            im.paste(pic, (x0, y0))
        im.paste(frame, (0, 0), frame)
        im.paste(tagl, (0, 0), tagl)
        ka = N.eo(N.seg(t, 0.25, 0.6))
        if o.get("label") and ka > 0:
            d = ImageDraw.Draw(im, "RGBA")
            f = gfx.font("Black", 46); fs = N.mono(22)
            lab = o["label"].upper(); sub = o.get("sub", "").upper()
            tw = max(d.textlength(lab, font=f), d.textlength(sub, font=fs)) + 60
            bx, by = x0 + 30, y0 + ph - 40
            d.rectangle([bx, by, bx + tw * ka, by + 104], fill=(6, 8, 18, 225), outline=col + (255,), width=3)
            d.rectangle([bx, by, bx + 10, by + 104], fill=col + (255,))
            if ka > 0.6:
                d.text((bx + 34, by + 14), lab, font=f, fill=N.WHITE)
                d.text((bx + 36, by + 70), sub, font=fs, fill=col + (255,))
        proc.stdin.write(im.tobytes())
    proc.stdin.close(); proc.wait()

def render_shot(sh):
    out = f"{R}/shot_{sh['i']:03d}.mp4"
    if os.path.exists(out): return out
    n = sh["frames"]; d = n / FPS
    if sh["kind"] == "g":
        fn, sc = J.GRAPHICS[sh["src"]], sh["scale"]  # graphics were timed to v1: stretch their clock to the slower read
        M.render(lambda t, dd: fn(t / sc, dd / sc), d, out); return out
    if sh["kind"] in ("a", "f"):
        render_archive(sh, out); return out
    if sh["kind"] == "p":
        render_photo(sh, out); return out
    avail = max(0.5, dur(sh["src"]) - sh["off"])
    slow = min(1.6, max(1.0, d / avail))
    crop = cropdetect(sh["src"]) if "/ai_broll/" in sh["src"] else None
    pre = "crop={}:{}:{}:{},".format(*crop) if crop else ""
    vf = (f"{pre}scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setpts=PTS*{slow:.4f},"
          f"fps={FPS},tpad=stop_mode=clone:stop_duration=30,{GRADE},"
          f"zoompan=z='1+0.07*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS},"
          f"vignette=angle=PI/5,format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(sh["off"]), "-i", sh["src"], "-vf", vf, "-frames:v", str(n)] + enc(out))
    return out

def stage_shots():
    sh = shots()
    with ThreadPoolExecutor(4) as ex: files = list(ex.map(render_shot, sh))
    with open(f"{R}/concat.txt", "w") as f:
        for x in files: f.write(f"file '{x}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{R}/concat.txt", "-c", "copy", f"{R}/base.mp4"])
    print("base", dur(f"{R}/base.mp4"))

def _grab(path, times):
    t0 = max(0, min(times)); n = round((max(times) - t0) * FPS) + 2
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", path, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, 1080, 1920, 3)
    return [fr[min(len(fr) - 1, max(0, round((t - t0) * FPS)))] for t in times]

SECTION_STARTS = {round(T(x), 3) for x in (69.7, 108.1, 180.3, 233.5, 332.7, 393.2, 490.9, 527.0, 584.2)}

def cut_list():
    sh = shots(); cuts = []
    for j, x in enumerate(sh[1:], 1):
        if x["kind"] == "g" or sh[j - 1]["kind"] == "g" or any(abs(x["start"] - s) < 0.05 for s in SECTION_STARTS) or j % 3 == 0:
            cuts.append(x["start"])
    return cuts

def stage_transitions():
    base = f"{R}/base.mp4"; ev = []
    for j, T in enumerate(cut_list()):
        kind = TR.KINDS[j % len(TR.KINDS)]
        out = f"{R}/tr_{j:03d}.mp4"
        if not os.path.exists(out):
            TR.ORANGE = np.array(NEON_COLS[(j // len(TR.KINDS)) % 2], np.float32)  # alternate orange / cyan glow
            times = [T + (i - 6) / FPS for i in range(12)]
            fa = _grab(base, [min(t, T - 1 / FPS) for t in times]); fb = _grab(base, [max(t, T) for t in times])
            rng = np.random.default_rng(j)
            p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-"] + enc(out), stdin=subprocess.PIPE)
            for i in range(12): p.stdin.write(np.ascontiguousarray(TR.frame(kind, fa[i], fb[i], (i + 0.5) / 12, rng)).tobytes())
            p.stdin.close(); p.wait()
        ev.append(dict(start=T - 6 / FPS, cut=T, kind=kind, file=out))
    json.dump(ev, open(f"{R}/trans.json", "w"))
    print("transitions", len(ev))

def stage_compose():
    tev = json.load(open(f"{R}/trans.json"))
    kws = []
    for i, (t, txt, d, pos) in enumerate(KEYWORDS):
        f = f"{R}/hud_{i:02d}.mov"
        if not os.path.exists(f): hud.render(txt, i + 1, d, pos, f, seed=100 + i, neon=True)
        kws.append(dict(start=round(t * FPS) / FPS, dur=d, file=f))
    json.dump(kws, open(f"{R}/kws.json", "w"))
    inputs = ["-i", f"{R}/base.mp4"]; fc = []; last = "[0:v]"; k = 1
    for tr in tev:
        inputs += ["-i", tr["file"]]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{tr['start']:.4f}/TB[t{k}]")
        fc.append(f"{last}[t{k}]overlay=eof_action=pass:enable='between(t,{tr['start']:.4f},{tr['start'] + 0.499:.4f})'[v{k}]"); last = f"[v{k}]"; k += 1
    for g in kws:
        inputs += ["-i", g["file"]]
        fc.append(f"[{k}:v]format=rgba,setpts=PTS-STARTPTS+{g['start']:.4f}/TB[g{k}]")
        fc.append(f"{last}[g{k}]overlay=eof_action=pass:format=auto:enable='between(t,{g['start']:.4f},{g['start'] + g['dur']:.4f})'[v{k}]"); last = f"[v{k}]"; k += 1
    fc.append(f"{last}noise=alls=5:allf=t,fade=in:st=0:d=0.6,format=yuv420p[out]")
    open(f"{R}/compose.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/compose.txt", "-map", "[out]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), f"{R}/video.mp4"])
    print("video", dur(f"{R}/video.mp4"))

def stage_audio():
    tev = json.load(open(f"{R}/trans.json")); kws = json.load(open(f"{R}/kws.json"))
    sdir = f"{R}/sfx"; os.makedirs(sdir, exist_ok=True)
    inputs = ["-i", VO]; fc = ["[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=%.3f,asplit=2[vo][sc]" % END]
    k = 1; mus = []
    for name, s, g, fo in MUSIC:
        inputs += ["-stream_loop", "-1", "-i", f"{MUSIC_DIR}/{name}.mp3"]  # loop: beds are longer after the v2 retime
        ms = int(s * 1000); fl = fo - s
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{fl + 3:.2f},afade=t=in:d=1.5,afade=t=out:st={fl:.2f}:d=3,volume={g},adelay={ms}|{ms}[m{k}]")
        mus.append(f"[m{k}]"); k += 1
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,equalizer=f=220:t=q:w=1.1:g=-3.5[mbus]")  # leave room for the voice's low end
    fc.append("[mbus][sc]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=450:makeup=1[mduck]")
    fx = []
    for t, name, g in SFX:
        inputs += ["-i", f"{SFX_DIR}/{name}.mp3"]; ms = int(t * 1000)
        lim = ",atrim=0:2.5,afade=t=out:st=1.8:d=0.7" if name == "starting-gun" else ""
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo{lim},volume={g},adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, tr in enumerate(tev):
        f = f"{sdir}/tr_{j:03d}.wav"; sounds.trans_sound(tr["kind"], f, 2000 + j)
        inputs += ["-i", f]; ms = int(max(0, tr["cut"] - 0.30) * 1000)
        fc.append(f"[{k}:a]volume=0.22,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, g in enumerate(kws):
        f = f"{sdir}/kw_{j:02d}.wav"; sounds.ui_sound("decode", f, 3000 + j)
        inputs += ["-i", f]; ms = int(g["start"] * 1000)
        fc.append(f"[{k}:a]volume=0.18,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, sh in enumerate(x for x in shots() if x["kind"] == "p"):  # soft UI blip as each photo pops in
        f = f"{sdir}/ph_{j:02d}.wav"; sounds.ui_sound("decode", f, 4000 + j)
        inputs += ["-i", f]; ms = int(sh["start"] * 1000)
        fc.append(f"[{k}:a]volume=0.12,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    fc.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    fc.append(f"[vo][mduck][fx]amix=inputs=3:normalize=0,atrim=0:{END:.3f},afade=t=out:st={END - 2.5:.2f}:d=2.5,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000[out]")
    open(f"{R}/audio.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/audio.txt", "-map", "[out]", "-c:a", "pcm_s16le", f"{R}/mix.wav"])
    print("mix", dur(f"{R}/mix.wav"))

def stage_mux():
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/video.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", OUT])
    print("wrote", OUT, dur(OUT))

if __name__ == "__main__":
    for s in sys.argv[1:] or ["shots", "transitions", "compose", "audio", "mux"]:
        print("==", s, flush=True); globals()["stage_" + s]()

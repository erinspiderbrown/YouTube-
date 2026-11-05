"""Jon Drummond documentary build (v2): voiceover-driven, real archival footage + real photos,
neon motion graphics.

Shot kinds:
  g  motion graphic (jd_mograph, neon look)
  v  stock / AI clip, full frame
  a  real archival footage, full-bleed (4:3 cropped to fill) + ARCHIVE tag
  f  real archival footage, framed: blurred backdrop + neon border + ARCHIVE tag
  p  real photo card (Wikimedia Commons), neon frame + name tag

Stages: shots -> transitions -> compose (HUD keywords, grain) -> audio -> mux
Run:  python3 -I projects/jon-drummond/jd_build.py [stage ...]
"""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"
P = f"{ROOT}/projects/jon-drummond"
SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
R = f"{SCR}/render_jd2"; os.makedirs(f"{R}/frames", exist_ok=True)
STOCK = f"{SCR}/broll"
REAL = f"{SCR}/real"      # user's Dropbox clips + YouTube imports (see README for sources)
PHOTOS = f"{SCR}/photos"  # Wikimedia Commons photos (credits.json)
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, P)
import mograph as M
M.GEO = f"{SCR}/geo"
import neon as N
N.PHOTOS = PHOTOS
M.finish = N.finish
import jd_mograph as J, hud, sounds, transitions as TR
import gfx

FPS = 24
VO = f"{P}/jon-drummond_voiceover_v3b.mp3"  # v3b: natural-speed phrases on the v3 timeline + warmer EQ (tools/rephrase_voiceover.py)
END = 517.5
OUT = f"{SCR}/output/jon-drummond_v2_master.mp4"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:800]); print(r.stderr[-2000:]); raise SystemExit(1)

def ai(n): return f"{P}/ai_broll/{n}.mp4"
def st(n): return f"{STOCK}/{n}.mp4"
def rl(n): return f"{REAL}/{n}.mp4"

PAR = rl("paris2003_protest")      # user's Dropbox: fan footage, Paris 2003 100m quarterfinal
T96 = rl("trials1996_semi")        # user's Dropbox: 1996 US Trials 100m semi (NBC)
DST = rl("drummond_story")         # YouTube: compilation with France 2 broadcast of Paris 2003 + NBC Sydney 2000
SYD = rl("sydney2000_4x100_fr")    # YouTube: Sydney 2000 men's 4x100 final (France TV)
STU = rl("stuttgart1993_wr")       # YouTube: Stuttgart 1993 4x100 WR (IAAF)
ATL = rl("atlanta1996_4x100")      # YouTube: Atlanta 1996 4x100 final
BOL = rl("bolt_daegu2011")         # YouTube: Daegu 2011 100m final, Bolt false start (Universal Sports)
LON = rl("london2012_women_wr")    # YouTube: London 2012 women's 4x100 WR (Olympics)
TYG = rl("tyson_gay_news")         # YouTube: PBS NewsHour on Tyson Gay's positive tests
TAGS = {PAR: "Paris · Worlds 2003", DST: "Paris · Worlds 2003", T96: "US Trials · 1996", SYD: "Sydney · Olympics 2000",
        STU: "Stuttgart · Worlds 1993", ATL: "Atlanta · Olympics 1996", BOL: "Daegu · Worlds 2011",
        LON: "London · Olympics 2012", TYG: "News · 2013"}
SYDNEY = {"tag": "Sydney · Olympics 2000"}

# (start_sec, kind, source, offset, opts)   each shot runs until the next one starts
# opts: e = where the source shot ends (cut in the source), yb = vertical crop bias for 'a',
#       tag = archive label, label/sub = photo name tag
SHOTS = [
    # ---- cold open: Paris 2003
    (0.0, "a", PAR, 45.0, {"e": 50.5}),                 # "All right, check it out" - start replay on the big screen
    (1.76, "a", PAR, 61.0, {"e": 64.0, "yb": 0.3}),     # "You see this man right here?"
    (3.3, "a", DST, 313.0, {"e": 316.0}),               # "Lay it out flat on his back"
    (6.9, "g", "profile", 0),
    (12.9, "a", DST, 321.0, {"e": 327.8, "yb": 0.3}),   # "bruh is not leaving this track"
    (16.0, "a", DST, 316.0, {"e": 320.8}),              # "Not today, not for nobody"
    (18.8, "a", PAR, 156.0, {"e": 162.5}),              # "officials standing over him"
    (21.5, "a", PAR, 219.0, {"e": 223.0}),              # "thousands of folks in the stands"
    (24.6, "a", PAR, 90.0, {"e": 105.5, "yb": 0.6}),    # "The whole meet just stopped"
    (27.0, "a", PAR, 171.5, {"e": 176.5}),              # "I ain't move"
    (30.0, "g", "delay_clock", 0),
    (33.7, "f", DST, 42.3, {"e": 49.0}),                # arguing with officials (France 2)
    (39.0, "a", PAR, 215.2, {"e": 218.8}),              # "Meltdown, embarrassing, career over"
    (42.2, "v", st("lightning"), 4.4),
    (45.3, "p", "p_drummond_1994", 0, {"label": "Jon Drummond", "sub": "11 years later", "tag": "Photo · 1994"}),
    (48.3, "g", "case_stamp", 0),
    (54.9, "f", DST, 57.6, {"e": 59.9, "tag": "Jon Drummond"}),  # "the biggest showman in track"
    (57.6, "a", PAR, 126.0, {"e": 139.5}),              # "refusing to leave the track"
    (61.1, "g", "title", 0),
    # ---- background
    (65.5, "f", T96, 0.3, {"e": 8.4}),                  # NBC intro: Jon Drummond
    (69.0, "p", "l_rowhouses", 0, {"label": "Philadelphia", "sub": "born 1968", "tag": "West Philly"}),
    (71.6, "p", "l_overbrook", 0, {"label": "Overbrook High School", "sub": "West Philadelphia", "tag": "Overbrook"}),
    (73.4, "p", "p_wilt", 0, {"label": "Wilt Chamberlain", "sub": "Overbrook alum", "tag": "Photo · 1960"}),
    (75.1, "p", "l_odessa", 0, {"label": "Odessa College", "sub": "JUCO · Odessa, Texas", "tag": "Odessa, TX"}),
    (78.1, "p", "l_tcu", 0, {"label": "TCU", "sub": "Fort Worth, Texas", "tag": "Fort Worth, TX"}),
    (79.6, "f", STU, 56.5, {"e": 62.6}),                # USA relay intro with Drummond on the lower third
    (82.7, "a", STU, 130.0, {"e": 144.6}),              # '93 world gold, tied the WR
    (85.9, "f", STU, 161.0, {"e": 205.0}),              # WINNER 37.40 WR
    (88.1, "a", ATL, 38.0, {"e": 60.4}),                # silver in Atlanta '96
    (91.2, "g", "medals", 0),
    (93.7, "f", T96, 9.0, {"e": 19.9}),                 # "a whole personality"
    (97.4, "f", T96, 123.0, {"e": 126.8}),              # "He was the talker" - shh
    (100.3, "a", STU, 186.0, {"e": 189.0}),             # "Some folks loved that"
    (102.5, "a", PAR, 304.5, {"e": 310.8}),             # "...could not stand it"
    (106.0, "g", "ch_sydney", 0),
    # ---- Sydney 2000
    (111.1, "f", DST, 104.0, {"e": 110.9, **SYDNEY}),   # NBC: 1st exchange Williams - Drummond
    (115.0, "f", SYD, 38.0, {"e": 47.8}),               # USA lineup: Drummond, Williams, Lewis, Greene
    (117.9, "g", "team", 0),                            # real photos pop on each name
    (122.7, "f", SYD, 192.8, {"e": 196.0}),             # Greene crosses: gold
    (125.3, "p", "p_greene_sydney", 0, {"label": "Maurice Greene", "sub": "Sydney 2000", "tag": "Photo · Sydney 2000"}),
    (128.1, "a", SYD, 196.5, {"e": 205.0}),             # party starts on the track
    (131.6, "g", "medal_stand", 0),                     # Kissinger photo
    (135.2, "f", SYD, 105.0, {"e": 109.9}),             # Greene, tongue out
    (138.0, "v", st("newspaper"), 4),
    (141.1, "g", "q_regret", 0),
    (148.0, "f", DST, 98.0, {"e": 103.5, **SYDNEY}),    # NBC: Jon Drummond, 1st leg
    (151.0, "f", SYD, 48.0, {"e": 50.8}),
    (154.2, "g", "emails", 0),
    (161.2, "f", SYD, 267.5, {"e": 277.8}),             # "Was it a lil' much?"
    (165.3, "p", "p_lewis_1996", 0, {"label": "Brian Lewis", "sub": "USA 4x100 · leg 3", "tag": "US Trials · 1996"}),
    (168.3, "f", SYD, 276.0, {"e": 281.0}),
    (172.8, "f", SYD, 101.0, {"e": 104.9}),             # "or 'bout who was celebratin', and how"
    (175.5, "v", st("blocks3"), 2),
    (177.8, "g", "rep", 0),
    (184.3, "g", "ch_paris", 0),
    # ---- rule change & Paris 2003
    (187.6, "g", "rule", 0),
    (206.5, "a", PAR, 5.0, {"e": 13.9, "yb": 0.55}),
    (210.4, "p", "l_paris_2003", 0, {"label": "Paris · Saint-Denis", "sub": "World Championships 2003", "tag": "Photo · 2003"}),
    (214.1, "g", "paris", 0),
    (217.6, "f", PAR, 35.8, {"e": 38.4}),               # start list: JON DRUMMOND USA
    (219.9, "a", PAR, 207.0, {"e": 213.4, "yb": 0.3}),  # "34 years old"
    (225.5, "f", DST, 37.0, {"e": 39.1}),               # "down in the blocks... set"
    (228.6, "g", "false_start", 0),
    (232.5, "a", PAR, 51.0, {"e": 53.9, "yb": 0.3}),    # "Say he never left the blocks"
    (235.9, "a", PAR, 14.5, {"e": 18.9}),               # "what'd he do next?"
    (240.9, "a", PAR, 70.0, {"e": 89.0, "yb": 0.6}),    # "He won't leave."
    (242.2, "a", PAR, 202.0, {"e": 206.8, "yb": 0.3}),  # "arguin' with the officials"
    (244.2, "f", DST, 568.6, {"e": 570.6}),             # "lay down on the track"
    (245.7, "a", PAR, 127.0, {"e": 131.5}),             # "cryin', beatin' on his chest"
    (248.0, "f", DST, 344.0, {"e": 347.8}),             # "hands up to the crowd"
    (249.3, "f", DST, 328.0, {"e": 332.6}),             # team manager talks to him
    (254.2, "g", "delay_clock", 0),
    (257.3, "a", PAR, 253.0, {"e": 262.5, "yb": 0.4}),  # "when he finally walk off"
    (263.1, "g", "q_mj", 0),                            # Michael Johnson photo
    (271.5, "f", DST, 427.2, {"e": 431.7}),             # "tried to explain hisself"
    (275.4, "v", st("blocks1"), 6),
    (279.7, "a", PAR, 247.0, {"e": 253.0, "yb": 0.4}),  # "how he make his livin'"
    (283.0, "g", "fallout", 0),
    (295.4, "g", "q_spirit", 0),
    (305.8, "a", PAR, 76.0, {"e": 89.0, "yb": 0.6}),    # "My take: bad look"
    (309.3, "a", PAR, 320.0, {"e": 327.5}),             # "hold up a whole world championship"
    (313.2, "v", st("blocks2"), 4),
    (316.8, "f", PAR, 178.0, {"e": 187.5}),             # "a flinch ain't the same as shootin' out the blocks"
    (320.2, "g", "bolt", 0),
    (332.2, "a", BOL, 66.5, {"e": 72.0}),               # Bolt's false start
    (335.2, "a", BOL, 34.0, {"e": 45.9, "yb": 0.3}),
    (337.7, "a", BOL, 90.0, {"e": 101.3}),              # "Drummond lost the argument"
    (343.9, "a", PAR, 312.5, {"e": 318.5, "yb": 0.5}),  # "should've been the end of his story"
    (346.5, "g", "ch_fall", 0),
    # ---- coaching & the ban
    (349.7, "v", st("coachtalk"), 2),
    (354.6, "a", TYG, 8.3, {"e": 11.9}),                # "one of the dudes he coached"
    (356.4, "p", "p_gay_2012", 0, {"label": "Tyson Gay", "sub": "coached by Drummond", "tag": "Photo · London 2012"}),
    (359.7, "p", "l_london_view", 0, {"label": "London 2012", "sub": "Olympic Stadium", "tag": "Photo · 2012"}),
    (363.7, "g", "london", 0),
    (367.4, "a", SYD, 199.5, {"e": 205.0}),             # "same dude they called a disgrace in Sydney"
    (369.8, "p", "l_usa_4x100_2012", 0, {"label": "Team USA 4x100", "sub": "London 2012", "tag": "Photo · 2012"}),
    (372.3, "a", LON, 404.5, {"e": 412.0}),             # women's 4x100 world record
    (374.3, "a", LON, 424.5, {"e": 432.0}),             # NEW WR 40.82
    (376.3, "a", LON, 350.0, {"e": 358.0}),             # "redemption arc"
    (380.3, "v", st("lightning"), 40),
    (383.2, "a", TYG, 12.5, {"e": 22.6}),               # "Tyson Gay failed drug tests"
    (387.2, "v", st("lab_tubes"), 1),
    (391.8, "g", "gay_case", 0),
    (403.0, "a", TYG, 53.9, {"e": 57.3}),               # "Basically... he talked": Gay in USADA's video
    (404.8, "a", PAR, 58.6, {"e": 60.9, "yb": 0.3}),    # "led straight to his coach"
    (407.7, "p", "l_usada", 0, {"label": "USADA", "sub": "U.S. Anti-Doping Agency", "tag": "USADA"}),
    (410.9, "v", st("suit_laptop"), 2),
    (414.2, "v", st("gavel"), 1),
    (418.8, "g", "ruling", 0), (427.4, "g", "sanction", 0), (437.1, "g", "q_ceo", 0),
    # ---- Hall of Fame & ending
    (444.7, "f", T96, 23.6, {"e": 31.0}),               # "feel like a movie"
    (449.0, "g", "same_year", 0),
    (463.1, "f", DST, 564.0, {"e": 566.6}),             # "So what we make of Jon Drummond?"
    (465.2, "f", T96, 77.3, {"e": 79.7}),
    (468.3, "f", DST, 111.2, {"e": 116.3, **SYDNEY}),   # "Sydney was a celebration that went too far"
    (473.2, "a", PAR, 133.0, {"e": 139.5}),             # "Paris was a protest that went too far"
    (478.6, "v", st("gavel"), 5),
    (483.9, "v", st("judge_doc"), 2),
    (491.9, "g", "now", 0),
    (498.9, "a", PAR, 223.0, {"e": 226.5}),
    (502.1, "a", PAR, 65.0, {"e": 68.9}),               # "In Paris, Jon Drummond laid on that track"
    (504.9, "a", DST, 322.0, {"e": 327.8, "yb": 0.3}),  # "...and wouldn't leave"
    (509.8, "g", "end", 0),
]

KEYWORDS = [  # (vo_time, text, dur, pos)
    (39.0, "Meltdown.\nCareer over.", 2.8, "left"), (97.4, "The talker.", 2.4, "right"),
    (163.1, "Was it a\nlil' much?", 2.6, "left"), (169.9, "Or 'bout WHO\nwas celebratin'?", 3.2, "right"),
    (232.5, "Just a\nflinch?", 2.6, "left"), (240.9, "He won't\nleave.", 2.6, "left"), (305.8, "My take:\nbad look.", 2.8, "left"),
    (313.2, "But he\nwasn't trippin'.", 2.8, "right"), (337.7, "Lost the\nargument.", 2.6, "left"),
    (376.3, "Redemption\narc?", 2.6, "left"), (403.0, "Basically…\nhe talked.", 2.8, "left"), (465.2, "Keep it\na buck.", 2.6, "left"),
    (478.6, "But 2014?\nDifferent.", 2.8, "right"),
]
SFX = [  # (vo_time, file, gain)
    (0.05, "sub-boom", 0.9), (39.0, "newspaper-rip", 0.7), (42.1, "record-scratch", 0.8), (53.2, "rubber-stamp", 1.0),
    (61.2, "sub-boom", 0.9), (106.0, "whoosh", 0.6), (122.9, "crowd-roar", 0.8), (138.1, "newspaper-rip", 0.6),
    (184.3, "whoosh", 0.6), (226.9, "starting-gun", 0.9), (228.6, "sub-boom", 0.9), (240.9, "sub-boom", 0.6),
    (257.4, "newspaper-rip", 0.6), (327.0, "rubber-stamp", 0.8), (346.5, "whoosh", 0.6), (380.3, "sub-boom", 0.9),
    (418.9, "rubber-stamp", 0.8), (427.5, "rubber-stamp", 1.0), (457.3, "sub-boom", 0.8), (509.8, "sub-boom", 0.8),
]
MUSIC = [  # (file, start, gain, fade_out_at)
    ("M1_cold-open-background", 0.0, 0.55, 97.0), ("M2_sydney", 106.0, 0.5, 173.0), ("M3_rule-paris-fallout", 184.0, 0.55, 321.0),
    ("M4_coaching-ban", 346.0, 0.5, 438.0), ("M5_verdict-ending", 446.0, 0.55, 512.0),
]

def shots():
    out = []
    for i, x in enumerate(SHOTS):
        s, k, src, off = x[:4]; opt = x[4] if len(x) > 4 else {}
        e = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END
        f0, f1 = round(s * FPS), round(e * FPS)
        out.append(dict(i=i, start=f0 / FPS, frames=f1 - f0, kind=k, src=src, off=off, opt=opt))
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
        M.render(J.GRAPHICS[sh["src"]], d, out); return out
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

SECTION_STARTS = {61.1, 106.0, 111.1, 184.3, 187.6, 346.5, 349.7, 444.7, 509.8}

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
        inputs += ["-i", f"{P}/music/{name}.mp3"]
        ms = int(s * 1000); fl = fo - s
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{fl + 3:.2f},afade=t=in:d=1.5,afade=t=out:st={fl:.2f}:d=3,volume={g},adelay={ms}|{ms}[m{k}]")
        mus.append(f"[m{k}]"); k += 1
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,equalizer=f=220:t=q:w=1.1:g=-3.5[mbus]")  # leave room for the voice's low end
    fc.append("[mbus][sc]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=450:makeup=1[mduck]")
    fx = []
    for t, name, g in SFX:
        inputs += ["-i", f"{P}/sfx/{name}.mp3"]; ms = int(t * 1000)
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

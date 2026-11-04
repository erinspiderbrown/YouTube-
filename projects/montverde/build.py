"""Podcast-style edit pipeline: Montverde video.

Stages (each cached in render/):
  1. plan     - keep-ranges from word timestamps, shots + framing, timeline
  2. aroll    - render each A-roll shot (crop/punch-in + grade) and inserts
  3. broll    - render B-roll inserts (stock clips / photo Ken Burns) + graphics PNGs
  4. compose  - concat base, overlay B-roll + graphics
  5. audio    - voice edit + cleanup, music bed w/ ducking, SFX, loudness
  6. mux      - final.mp4
"""
import json, os, subprocess, sys, wave, math
from concurrent.futures import ThreadPoolExecutor
import numpy as np

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(S, "scripts"))
import gfx, cards
import cv2
from deshadow import deshadow

F, B, A, R = (os.path.join(S, d) for d in ("dropbox1/files", "broll", "assets", "render"))
os.makedirs(R, exist_ok=True)
FPS = 24
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:600]); print(r.stderr[-2000:]); raise SystemExit(1)

def fr(t):  # snap to frame grid
    return round(t * FPS) / FPS

# ---------------------------------------------------------------- 1. plan
CUT_END = 599.95   # user: cut everything after "this doping shit is a joke"
ALL_WORDS = [w for seg in json.load(open(os.path.join(S, "work/main.json"))) for w in seg["words"]]
words = [w for w in ALL_WORDS if w["s"] < CUT_END]
import re as _re
SWEAR = _re.compile(r"\b(shit|fuck\w*|motherfuck\w*|nigga\w*|bitch\w*)\b", _re.I)
SWEARS = [(w["s"], w["e"]) for w in words if SWEAR.search(w["w"])]
GAP, PRE, POST = 0.45, 0.10, 0.16
ranges = []
cur = [words[0]["s"], words[0]["e"]]
for w in words[1:]:
    if w["s"] - cur[1] > GAP:
        ranges.append(cur); cur = [w["s"], w["e"]]
    else:
        cur[1] = w["e"]
ranges.append(cur)
ranges = [[max(0, s - PRE), e + POST] for s, e in ranges]
for i in range(1, len(ranges)):  # no overlaps
    if ranges[i][0] < ranges[i - 1][1]:
        mid = (ranges[i][0] + ranges[i - 1][1]) / 2
        ranges[i - 1][1] = mid; ranges[i][0] = mid

# split long ranges into shots (angle change on continuous audio) at word gaps
MAXSHOT = 8.0
shots = []
for s, e in ranges:
    inner = [w for w in words if s <= w["s"] and w["e"] <= e]
    start = s
    while e - start > MAXSHOT + 3:
        target = start + MAXSHOT
        cands = [(abs(a["e"] - target), (a["e"] + b["s"]) / 2) for a, b in zip(inner, inner[1:])
                 if start + 3 < a["e"] < e - 3 and b["s"] - a["e"] > 0.12]
        if not cands: break
        cut = min(cands)[1]
        shots.append([start, cut, False]); start = cut
    shots.append([start, e, True])   # True = ends at a real time-cut

# framing: (crop_w, cx, cy) in 4K coords; cycle changes on every shot
FRAMES = {"W": (3840, 1920, 1080), "M": (3072, 1650, 1130), "C": (2560, 1478, 1080)}
CYCLE = ["C", "M", "C", "W"]
shot_items = []
for i, (s, e, tc) in enumerate(shots):
    shot_items.append({"type": "aroll", "src": [s, e], "frame": CYCLE[i % len(CYCLE)]})

TITLE_AFTER, INTERVIEW_AFTER = 30.56, 236.99
TITLE_DUR = 3.0
timeline = []
for it in shot_items:
    timeline.append(it)
    if abs(it["src"][1] - POST - TITLE_AFTER) < 0.3:
        timeline.append({"type": "title", "dur": TITLE_DUR})
    if abs(it["src"][1] - POST - INTERVIEW_AFTER) < 0.3:
        timeline.append({"type": "interview", "src": [0.30, 14.0]})
timeline.append({"type": "end", "dur": 4.0})
assert sum(t["type"] == "title" for t in timeline) == 1, "title anchor not found"
assert sum(t["type"] == "interview" for t in timeline) == 1, "interview anchor not found"

t = 0.0
for it in timeline:
    d = it["dur"] if "dur" in it else it["src"][1] - it["src"][0]
    it["frames"] = max(1, round(d * FPS)); it["out"] = t; t += it["frames"] / FPS
TOTAL = t

def O(src):
    """Map a source time to output time."""
    best = None
    for it in timeline:
        if it["type"] != "aroll": continue
        s, e = it["src"]
        if s <= src <= e: return it["out"] + (src - s)
        if src < s and best is None: best = it["out"]
    return best if best is not None else TOTAL

# ---------------------------------------------------------------- creative spec (source times)
BROLL = [  # (src_start, src_end, kind, file, offset)
    (3.38, 5.16, "stock", "sweep", 3),
    (10.66, 13.6, "stock", "fl_palms", 2),
    (20.5, 23.68, "stock", "pour_bottle", 2),
    (26.82, 30.56, "stock", "lab_tubes", 1),
    (65.94, 71.78, "stock", "pour_glass", 0),
    (71.78, 77.04, "stock", "warmup", 1),
    (94.38, 99.78, "stock", "lab_gloves", 1),
    (128.26, 134.6, "stock", "campus2", 3),
    (150.07, 153.91, "stock", "judge_doc", 1),
    (195.53, 201.31, "stock", "campus1", 3),
    (205.11, 209.69, "stock", "gavel", 1),
    (332.2, 337.26, "stock", "lab_drops", 2),
    (390.08, 397.8, "stock", "campus2", 14),
    (415.18, 419.62, "stock", "lab_tubes", 7),
    (464.19, 468.99, "stock", "women_track", 1),
    (494.87, 499.13, "stock", "male_track", 1),
    (499.29, 503.75, "stock", "women_track", 6),
    (549.57, 556.89, "stock", "pour_bottle", 9),
    (556.89, 561.15, "stock", "blocks1", 2),
]
GERALD = dict(name="Gerald Phiri", sub="Former Montverde track coach")
ISSAM = dict(name="Issam Asinga", sub="Sprinter · Suriname")
ADAEJAH = dict(name="Adaejah Hodge", sub="Sprinter · British Virgin Islands")
CARDS = [  # (src_start, src_end, person, photo, stamp, credit)
    (14.3, 18.9, GERALD, "coach_mouth.jpg", None, None),
    (41.9, 46.3, GERALD, "coach_head.jpg", ("SUSPENDED", "PROVISIONALLY", 1.0), None),
    (56.4, 62.2, ISSAM, "issam_270.jpg", ("SUSPENDED", None, 1.6), "Photo: Oscar Muñoz Badilla"),
    (103.3, 105.6, ADAEJAH, "hodge_flag.jpg", None, None),
    (105.9, 108.6, ISSAM, "issam_race.jpg", None, None),
    (178.4, 181.2, ISSAM, "athlete_walk.jpg", None, None),
    (218.3, 222.6, ISSAM, "issam_race.jpg", ("SUSPENDED", None, 1.2), None),
    (245.3, 250.0, ADAEJAH, "hodge_flag.jpg", ("NIL DEAL", "SIGNED", 1.6, (255, 122, 26, 255)), None),
]
KEYWORDS = [  # (src_time, text, dur, pos)
    (1.9, "Swept under\nthe rug", 2.6, "left"),
    (8.3, "Almost\n2 years", 2.2, "left"),
    (16.5, "Allegedly", 2.0, "left"),
    (34.2, "Everybody\non the team", 2.4, "left"),
    (47.9, "New company", 2.2, "left"),
    (68.4, "Clear. Tasteless.\nOdorless.", 3.2, "left"),
    (117.2, "These kids\nare cooked", 2.2, "left"),
    (138.8, "Nobody's\ntalking about it", 2.4, "left"),
    (152.0, "Administrative\nleave", 2.4, "right"),
    (205.2, "Sue the\nschool", 2.4, "left"),
    (197.5, "Well-funded\nboarding school", 3.0, "left"),
    (226.3, "All the money\nhe lost", 2.6, "left"),
    (250.2, "Same substance.\nSame coach.", 3.2, "right"),
    (329.9, "Target\ntesting", 2.4, "left"),
    (387.7, "3 athletes.\n1 school.", 3.0, "left"),
    (415.2, "GW1516", 2.6, "right"),
    (437.6, "Lightning\nstriking twice", 2.6, "left"),
    (488.0, "Athlete\n#4", 2.2, "left"),
    (551.0, "Water bottles\nat practice", 3.0, "left"),
]
LOWER_THIRDS = [  # (src_time, name, sub, dur)
    (10.9, "Montverde Academy", "Montverde, Florida", 2.6),
]
DISCLAIMER = "Commentary & opinion · Claims about the coach and school are allegations"

def stage_plan():
    plan = {"total": TOTAL, "timeline": timeline}
    json.dump(plan, open(os.path.join(R, "plan.json"), "w"), indent=1)
    n_cuts = sum(1 for s in shots if s[2]) - 1
    print(f"shots={len(shots)} time-cuts={n_cuts} total={TOTAL:.1f}s (source 699.3s)")

# ---------------------------------------------------------------- 2. aroll
GRADE = ("curves=master='0/0.02 0.18/0.21 0.42/0.5 0.7/0.72 0.85/0.8 1/0.9',"
         "eq=saturation=1.12,colorbalance=rm=0.015:bm=-0.015:rs=0.01:bs=-0.01")
STOCK_GRADE = "eq=contrast=1.06:saturation=1.08,colorbalance=rm=0.02:bm=-0.02"

SOFA_Y = 0.72 * 2160  # top of the sofa back, 4K coords
FACES = np.array(json.load(open(os.path.join(S, "work/faces.json"))))
FACE_MED = np.median(FACES[:, 1:3], axis=0)

def face_at(s, e):
    m = FACES[(FACES[:, 0] >= s) & (FACES[:, 0] <= e)]
    fx, fy = (np.median(m[:, 1:3], axis=0) if len(m) else FACE_MED)
    return fx * 3840, fy * 2160

def crop_rect(code, src=None):
    w = FRAMES[code][0]; h = w * 9 // 16
    if code == "W": return w, h, 0, 0
    fx, fy = face_at(*src) if src else (FACE_MED[0] * 3840, FACE_MED[1] * 2160)
    lead = 0.08 * w  # a little look-room to his left side of frame
    cx = fx + lead
    x = int(min(max(0, cx - w / 2), 3840 - w)); y = int(min(max(0, fy - 0.55 * h), 2160 - h))
    return w, h, x & ~1, y & ~1

def enc(out):
    return ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-video_track_timescale", "12288", out]

def render_item(i):
    it = timeline[i]; out = os.path.join(R, f"item_{i:03d}.mp4")
    if os.path.exists(out): return
    d = it["frames"] / FPS
    if it["type"] == "aroll":
        w, h, x, y = crop_rect(it["frame"], it["src"])
        fx, _ = face_at(*it["src"])
        face_x = (fx - x) / w * 1920
        sofa_y = (SOFA_Y - y) / h * 1080
        mask = cv2.resize(cv2.imread(os.path.join(A, "lightmask.png"))[y:y + h, x:x + w], (1920, 1080),
                          interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{it['src'][0]:.3f}", "-t", f"{d + 0.5:.3f}",
                                "-i", os.path.join(F, "main.mov"), "-vf",
                                f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,fps={FPS},{GRADE}",
                                "-frames:v", str(it["frames"]), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                               stdout=subprocess.PIPE)
        encp = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", "1920x1080", "-r", str(FPS), "-i", "-", "-vf", "unsharp=5:5:0.3"] + enc(out),
                                stdin=subprocess.PIPE)
        fsz = 1920 * 1080 * 3; nfr = 0; last = None; dstate = {}
        while nfr < it["frames"]:
            buf = dec.stdout.read(fsz)
            if len(buf) < fsz:
                buf = last  # source ran short: hold last frame
                if buf is None: break
            last = buf
            fr_ = np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3)
            fixed, _ = deshadow(fr_, sofa_y, face_x, state=dstate)
            fixed = (fixed.astype(np.float32) * mask[..., ::-1]).astype(np.uint8)
            encp.stdin.write(fixed.tobytes()); nfr += 1
        dec.stdout.close(); dec.wait(); encp.stdin.close(); encp.wait()
    elif it["type"] == "interview":
        tag = os.path.join(R, "g_interview_tag.png")
        gfx.caption_tag("Issam Asinga · post-race interview", tag)
        fc = (f"[0:v]scale=1920:1080:flags=lanczos,fps={FPS},{STOCK_GRADE},unsharp=5:5:0.5[v];"
              f"[v][1:v]overlay,format=yuv420p,trim=end_frame={it['frames']}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{it['src'][0]:.3f}", "-i", os.path.join(F, "interview.mp4"),
             "-loop", "1", "-i", tag, "-filter_complex", fc, "-map", "[o]", "-frames:v", str(it["frames"])] + enc(out))
    elif it["type"] in ("title", "end"):
        png = os.path.join(R, f"g_{it['type']}.png")
        if it["type"] == "title":
            gfx.title_card("The Montverde Academy doping scandal", "Swept under\nthe rug", png, DISCLAIMER)
            bg, off = os.path.join(B, "blocks3.mp4"), 1
        else:
            gfx.title_card("What do you think?", "Let me know\nin the comments", png)
            bg, off = os.path.join(B, "fl_city.mp4"), 2
        fc = (f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps={FPS},"
              f"eq=brightness=-0.28:saturation=0.75,boxblur=10:1,vignette=angle=PI/3,setpts=PTS*1.4[bg];"
              f"[1:v]format=rgba,fade=in:st=0.1:d=0.35:alpha=1[t];[bg][t]overlay,"
              f"fade=in:st=0:d=0.2,format=yuv420p,trim=end_frame={it['frames']}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(off), "-i", bg, "-loop", "1", "-i", png,
             "-filter_complex", fc, "-map", "[o]", "-frames:v", str(it["frames"])] + enc(out))

def stage_aroll():
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(render_item, range(len(timeline))))
    lst = os.path.join(R, "concat.txt")
    with open(lst, "w") as f:
        for i in range(len(timeline)): f.write(f"file 'item_{i:03d}.mp4'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
         os.path.join(R, "base.mp4")])

# ---------------------------------------------------------------- 3. broll + graphics
def broll_events():
    ev = []
    for s, e, kind, src, opt in BROLL:
        o0, o1 = fr(O(s)), fr(O(e))
        if o1 - o0 < 0.8: print("skip short broll", src, s); continue
        ev.append({"start": o0, "dur": o1 - o0, "kind": kind, "src": src, "opt": opt})
    return ev

def render_broll(i, b):
    out = os.path.join(R, f"broll_{i:02d}.mp4")
    if os.path.exists(out): return out
    n = round(b["dur"] * FPS)
    if b["kind"] == "stock":
        src = os.path.join(B, b["src"] + ".mp4")
        fc = (f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,"
              f"fps={FPS},{STOCK_GRADE},tpad=stop_mode=clone:stop_duration=10,"
              f"vignette=angle=PI/6,format=yuv420p,trim=end_frame={n}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(b["opt"]), "-i", src, "-filter_complex", fc,
             "-map", "[o]", "-frames:v", str(n)] + enc(out))
    else:
        src = os.path.join(F, b["src"])
        # blurred cover background + framed photo, slow push-in
        fc = (f"[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,boxblur=40:2,"
              f"eq=brightness=-0.18:saturation=0.9[bg];"
              f"[0:v]scale=-2:1860:flags=lanczos,pad=iw+24:ih+24:12:12:color=0xFF7A1A[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,"
              f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={FPS}")
        if b["opt"]:
            tag = os.path.join(R, f"g_credit_{i:02d}.png"); gfx.caption_tag(b["opt"], tag)
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tag, "-filter_complex",
                 fc + "[p];[p][1:v]overlay,format=yuv420p[o]", "-map", "[o]", "-frames:v", str(n)] + enc(out))
        else:
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc + ",format=yuv420p[o]",
                 "-map", "[o]", "-frames:v", str(n)] + enc(out))
    return out

def gfx_events():
    ev = []
    for i, (s, text, d, pos) in enumerate(KEYWORDS):
        p = os.path.join(R, f"g_kw_{i:02d}.png"); gfx.keyword(text, p, pos)
        ev.append({"start": fr(O(s)), "dur": d, "png": p, "kind": "kw"})
    for i, (s, name, sub, d) in enumerate(LOWER_THIRDS):
        p = os.path.join(R, f"g_lt_{i:02d}.png"); gfx.lower_third(name, sub, p)
        ev.append({"start": fr(O(s)), "dur": d, "png": p, "kind": "lt"})
    return ev

def card_events():
    ev = []
    for i, (s0, s1, person, photo, stamp, credit) in enumerate(CARDS):
        o0, o1 = fr(O(s0)), fr(O(s1))
        out = os.path.join(R, f"card_{i:02d}.mov")
        if not os.path.exists(out):
            cards.render(dict(person, photo=photo, path=os.path.join(F, photo), dur=o1 - o0,
                              stamp=stamp, credit=credit), out)
        ev.append({"start": o0, "dur": o1 - o0, "file": out, "stamp_t": stamp[2] if stamp else None})
    return ev

def stage_compose():
    bev = broll_events()
    with ThreadPoolExecutor(4) as ex:
        files = list(ex.map(lambda ib: render_broll(*ib), enumerate(bev)))
    gev = gfx_events()
    cev = card_events()
    json.dump({"broll": bev, "gfx": gev, "cards": cev}, open(os.path.join(R, "events.json"), "w"), indent=1)
    inputs = ["-i", os.path.join(R, "base.mp4")]
    fc, last, k = [], "[0:v]", 1
    for b, f in zip(bev, files):
        inputs += ["-i", f]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{b['start']:.4f}/TB[b{k}]")
        fc.append(f"{last}[b{k}]overlay=eof_action=pass:enable='between(t,{b['start']:.4f},{b['start'] + b['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    for g in gev:
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{g['dur']:.3f}", "-i", g["png"]]
        fc.append(f"[{k}:v]format=rgba,fade=in:st=0:d=0.15:alpha=1,fade=out:st={g['dur'] - 0.2:.3f}:d=0.2:alpha=1,"
                  f"setpts=PTS-STARTPTS+{g['start']:.4f}/TB[g{k}]")
        fc.append(f"{last}[g{k}]overlay=eof_action=pass:enable='between(t,{g['start']:.4f},{g['start'] + g['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    for c in cev:
        inputs += ["-i", c["file"]]
        fc.append(f"[{k}:v]format=rgba,setpts=PTS-STARTPTS+{c['start']:.4f}/TB[c{k}]")
        fc.append(f"{last}[c{k}]overlay=eof_action=pass:format=auto:enable='between(t,{c['start']:.4f},{c['start'] + c['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    fc.append(f"{last}format=yuv420p[out]")
    script = os.path.join(R, "compose.txt"); open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", script, "-map", "[out]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-movflags", "+faststart", os.path.join(R, "video.mp4")])

# ---------------------------------------------------------------- 5. audio
SR = 48000
def load(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    assert w.getframerate() == SR; return a

def save(p, a):
    a = np.clip(a, -1, 1); w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()

def stage_audio():
    voice, inter = load(os.path.join(S, "work/voice48.wav")), load(os.path.join(S, "work/interview48.wav"))
    total_n = round(TOTAL * SR)
    v_track = np.zeros(total_n, np.float32); i_track = np.zeros(total_n, np.float32)
    fade = int(0.006 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    for it in timeline:
        if it["type"] not in ("aroll", "interview"): continue
        n = round(it["frames"] / FPS * SR); o = round(it["out"] * SR)
        srcarr = voice if it["type"] == "aroll" else inter
        s = round(it["src"][0] * SR); seg = srcarr[s:s + n].copy()
        seg[:fade] *= ramp; seg[-fade:] *= ramp[::-1]
        (v_track if it["type"] == "aroll" else i_track)[o:o + len(seg)] += seg
    # mute swear words (user request): silence each word with short fades
    fd = int(0.012 * SR); muted = 0
    for ws, we in SWEARS:
        o0, o1 = O(ws), O(we)
        if o1 <= o0 or o1 - o0 > 2: continue
        a, b = round((o0 - 0.04) * SR), round((o1 + 0.05) * SR)
        lo, hi = max(0, a - fd), min(len(v_track), b + fd)
        env = np.ones(hi - lo, np.float32)
        env[a - lo:b - lo] = 0
        env[:a - lo] = np.linspace(1, 0, a - lo); env[b - lo:] = np.linspace(0, 1, hi - b)
        v_track[lo:hi] *= env; muted += 1
    print("muted", muted, "swear words")
    save(os.path.join(R, "voice_raw.wav"), v_track); save(os.path.join(R, "interview_raw.wav"), i_track)

    title = next(it for it in timeline if it["type"] == "title")
    end = next(it for it in timeline if it["type"] == "end")
    t_title_end = title["out"] + title["frames"] / FPS
    bev = json.load(open(os.path.join(R, "events.json")))
    sfx = []  # (file, time, gain)
    for b in bev["broll"]: sfx.append(("whoosh", max(0, b["start"] - 0.3), 0.22))
    for g in bev["gfx"]: sfx.append(("pop" if g["kind"] == "kw" else "whoosh", g["start"], 0.30 if g["kind"] == "kw" else 0.15))
    sfx += [("hit", title["out"], 0.9), ("whoosh", title["out"] - 0.35, 0.4), ("hit", end["out"], 0.6)]
    for c in bev.get("cards", []):
        sfx += [("whoosh", max(0, c["start"] - 0.15), 0.3), ("pop", c["start"] + 0.32, 0.35),
                ("pop", c["start"] + 0.48, 0.25), ("whoosh", c["start"] + c["dur"] - 0.35, 0.18)]
        if c["stamp_t"] is not None: sfx.append(("hit", c["start"] + c["stamp_t"], 0.7))
    inter_item = next(it for it in timeline if it["type"] == "interview")
    sfx.append(("whoosh", inter_item["out"] - 0.3, 0.3))

    inputs = ["-i", os.path.join(R, "voice_raw.wav"), "-i", os.path.join(R, "interview_raw.wav"),
              "-stream_loop", "-1", "-i", os.path.join(A, "music.wav")]
    fc = [
        # voice cleanup: rumble cut, gentle denoise, presence, compression
        "[0:a]highpass=f=80,afftdn=nf=-28,equalizer=f=3500:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-2,"
        "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,aformat=sample_rates=48000:channel_layouts=stereo[vo]",
        "[1:a]highpass=f=100,afftdn=nf=-25,acompressor=threshold=-22dB:ratio=3:makeup=5,volume=1.6,"
        "aformat=sample_rates=48000:channel_layouts=stereo[io]",
        "[vo][io]amix=inputs=2:normalize=0,asplit=3[voice][sc][sc2]",
        # music: louder in cold open/title/end card, low bed elsewhere, ducked under voice
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},"
        f"volume='if(lt(t,{t_title_end:.2f}),0.32,if(gt(t,{end['out']:.2f}),0.45,0.085))':eval=frame,"
        f"afade=t=out:st={TOTAL - 2.5:.2f}:d=2.5[mus]",
        "[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck]",
    ]
    k = 3; labels = []
    for name, t0, g in sfx:
        inputs += ["-i", os.path.join(A, name + ".wav")]
        ms = int(t0 * 1000)
        fc.append(f"[{k}:a]volume={g},adelay={ms}|{ms}[s{k}]"); labels.append(f"[s{k}]"); k += 1
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0[sfx]")
    fc.append("[sc2]anullsink")
    fc.append(f"[voice][duck][sfx]amix=inputs=3:normalize=0,atrim=0:{TOTAL:.3f},"
              "loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    script = os.path.join(R, "audio.txt"); open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", script, "-map", "[out]",
         "-c:a", "pcm_s16le", os.path.join(R, "mix.wav")])

def stage_mux():
    out = os.path.join(S, "output", "montverde_edit_v1.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(R, "video.mp4"), "-i", os.path.join(R, "mix.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
         "-movflags", "+faststart", out])
    print("wrote", out)

if __name__ == "__main__":
    stages = sys.argv[1:] or ["plan", "aroll", "compose", "audio", "mux"]
    for st in stages:
        print("==", st, flush=True); globals()["stage_" + st]()

"""Jon Drummond documentary build: voiceover-driven, full-screen B-roll + motion graphics.

Stages: shots -> base -> transitions -> compose (HUD keywords, grain) -> audio -> mux
Run:  python3 -I projects/jon-drummond/jd_build.py [stage ...]
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np

ROOT = "/home/user/YouTube-"
P = f"{ROOT}/projects/jon-drummond"
SCR = "/tmp/claude-0/-home-user-YouTube-/7a45229e-6af3-5cf7-9b94-045288e3239e/scratchpad"
R = f"{SCR}/render_jd"; os.makedirs(R, exist_ok=True)
STOCK = f"{SCR}/broll"
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, P)
import mograph as M
M.GEO = f"{SCR}/geo"
import jd_mograph as J, hud, sounds, transitions as TR

FPS = 24
VO = f"{P}/jon-drummond_voiceover_v3.mp3"
END = 517.5

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:500]); print(r.stderr[-1500:]); raise SystemExit(1)

def ai(n): return f"{P}/ai_broll/{n}.mp4"
def st(n): return f"{STOCK}/{n}.mp4"

# (start_sec, kind, source, offset)   each shot runs until the next one starts
SHOTS = [
    (0.0, "v", ai("S01_empty-blocks"), 0), (6.9, "g", "profile", 0), (12.9, "v", ai("S04_waiting-empty-lanes"), 0),
    (18.8, "v", ai("S03_confused-crowd"), 0), (24.6, "v", st("watch"), 1), (30.0, "g", "delay_clock", 0),
    (33.7, "v", st("newspaper"), 1), (42.2, "v", st("lightning"), 4.4), (48.3, "g", "case_stamp", 0),
    (54.9, "v", st("blocks1"), 2), (61.1, "g", "title", 0),
    (65.5, "v", ai("S05_philly-rowhouses"), 0), (71.6, "g", "route_map", 0), (79.6, "v", ai("S07_baton-handoff"), 0),
    (86.4, "g", "medals", 0), (93.7, "v", st("male_track"), 1), (100.3, "v", st("start_line"), 2), (106.0, "g", "ch_sydney", 0),
    (111.1, "v", ai("S08_sydney-harbour"), 0), (117.9, "g", "team", 0), (122.7, "v", ai("S03_confused-crowd"), 1.5),
    (128.1, "v", st("women_track"), 1), (131.6, "g", "medal_stand", 0), (138.0, "v", st("newspaper"), 4),
    (141.1, "g", "q_regret", 0), (148.0, "v", st("coachtalk"), 1), (154.2, "g", "emails", 0), (161.2, "v", st("warmup"), 1),
    (168.3, "v", st("blocks2"), 1), (175.5, "v", st("blocks3"), 2), (177.8, "g", "rep", 0), (184.3, "g", "ch_paris", 0),
    (187.6, "g", "rule", 0), (206.5, "v", st("start_line"), 7), (214.1, "g", "paris", 0), (219.9, "v", st("warmup"), 6),
    (225.5, "v", st("blocks3"), 6), (228.6, "g", "false_start", 0), (232.5, "v", ai("S01_empty-blocks"), 0),
    (240.9, "v", ai("S04_waiting-empty-lanes"), 0), (249.3, "v", ai("S03_confused-crowd"), 0), (254.2, "g", "delay_clock", 0),
    (257.3, "v", st("newspaper"), 2), (263.1, "g", "q_mj", 0), (271.5, "v", st("judge_doc"), 1), (277.5, "v", st("blocks1"), 6),
    (283.0, "g", "fallout", 0), (295.4, "g", "q_spirit", 0), (305.8, "v", st("start_line"), 11), (313.2, "v", st("blocks2"), 4),
    (320.2, "g", "bolt", 0), (332.2, "v", st("male_track"), 3), (337.7, "v", st("lightning"), 20), (346.5, "g", "ch_fall", 0),
    (349.7, "v", st("coachtalk"), 2), (354.6, "v", st("watch"), 4), (359.7, "g", "london", 0), (372.3, "v", st("women_track"), 5),
    (380.3, "v", st("lightning"), 40), (383.2, "v", st("lab_tubes"), 1), (391.8, "g", "gay_case", 0), (403.0, "v", st("lab_gloves"), 1),
    (407.7, "v", st("suit_laptop"), 2), (414.2, "v", st("gavel"), 1), (418.8, "g", "ruling", 0), (427.4, "g", "sanction", 0),
    (437.1, "g", "q_ceo", 0), (444.7, "v", st("blocks1"), 4), (449.0, "g", "same_year", 0), (463.1, "v", st("start_line"), 13),
    (468.3, "v", ai("S08_sydney-harbour"), 0), (473.2, "v", ai("S04_waiting-empty-lanes"), 0.5), (478.6, "v", st("gavel"), 5),
    (483.9, "v", st("judge_doc"), 2), (491.9, "g", "now", 0), (498.9, "v", ai("S01_empty-blocks"), 0),
    (504.9, "v", ai("S04_waiting-empty-lanes"), 1), (509.8, "g", "end", 0),
]

KEYWORDS = [  # (vo_time, text, dur, pos)
    (39.0, "Meltdown.\nCareer over.", 2.8, "left"), (97.4, "The talker.", 2.4, "left"),
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
    for i, (s, k, src, off) in enumerate(SHOTS):
        e = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END
        f0, f1 = round(s * FPS), round(e * FPS)
        out.append(dict(i=i, start=f0 / FPS, frames=f1 - f0, kind=k, src=src, off=off))
    return out

def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)

_crop = {}
def cropdetect(path):
    if path not in _crop:
        r = subprocess.run(["ffmpeg", "-v", "info", "-ss", "1", "-i", path, "-vf", "cropdetect=24:2:0", "-frames:v", "30", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        c = [l.split("crop=")[-1].strip() for l in r.splitlines() if "crop=" in l]
        _crop[path] = c[-1] if c else None
    return _crop[path]

GRADE = "eq=contrast=1.07:saturation=0.82:brightness=-0.015,colorbalance=rs=0.035:bs=-0.035:rm=0.02:bm=-0.02"

def enc(out):
    return ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), out]

def render_shot(sh):
    out = f"{R}/shot_{sh['i']:03d}.mp4"
    if os.path.exists(out): return out
    n = sh["frames"]; d = n / FPS
    if sh["kind"] == "g":
        M.render(J.GRAPHICS[sh["src"]], d, out); return out
    avail = max(0.5, dur(sh["src"]) - sh["off"])
    slow = min(1.6, max(1.0, d / avail))
    crop = cropdetect(sh["src"]) if "/ai_broll/" in sh["src"] else None
    pre = f"crop={crop}," if crop else ""
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

def cut_list():
    sh = shots(); cuts = []
    section_starts = {61.1, 106.0, 111.1, 184.3, 187.6, 346.5, 349.7, 444.7, 509.8}
    for j, x in enumerate(sh[1:], 1):
        if x["kind"] == "g" or sh[j - 1]["kind"] == "g" or any(abs(x["start"] - s) < 0.05 for s in section_starts) or j % 3 == 0:
            cuts.append(x["start"])
    return cuts

def stage_transitions():
    base = f"{R}/base.mp4"; ev = []
    for j, T in enumerate(cut_list()):
        kind = TR.KINDS[j % len(TR.KINDS)]
        out = f"{R}/tr_{j:03d}.mp4"
        if not os.path.exists(out):
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
        if not os.path.exists(f): hud.render(txt, i + 1, d, pos, f, seed=100 + i)
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
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0[mbus]")
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
    fc.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    fc.append(f"[vo][mduck][fx]amix=inputs=3:normalize=0,atrim=0:{END:.3f},afade=t=out:st={END - 2.5:.2f}:d=2.5,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000[out]")
    open(f"{R}/audio.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/audio.txt", "-map", "[out]", "-c:a", "pcm_s16le", f"{R}/mix.wav"])
    print("mix", dur(f"{R}/mix.wav"))

def stage_mux():
    out = f"{SCR}/output/jon-drummond_v1_master.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/video.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out])
    print("wrote", out, dur(out))

if __name__ == "__main__":
    for s in sys.argv[1:] or ["shots", "transitions", "compose", "audio", "mux"]:
        print("==", s, flush=True); globals()["stage_" + s]()

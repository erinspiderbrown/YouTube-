"""IShowSpeed 10.35: clean the user's own read (Dropbox '2220 W Mission Ln 6.m4a', 5:47).
Cuts: the false start 'Otto Bolton been training him since -' (restarted), the two profanities
('goddamn', 'ass') removed whole at energy dips, long pauses trimmed inside measured silence
(tools/safe_cuts.py). No tempo change. Output vo_clean.wav (-16 LUFS)."""
import json, os, subprocess, sys, numpy as np
P = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{P}/../../tools")
from safe_cuts import pause_cuts, safe_point
SR = 48000
RAW = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/speed/in2/2220 W Mission Ln 6.m4a"
W = json.load(open("/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/speed/in2/vo_words_raw.json"))
CHAIN = ("highpass=f=75,afftdn=nr=10:nf=-50:tn=1,deesser=i=0.4,"
         "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
         "equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5")
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", RAW, "-af", CHAIN, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).copy()
def onset(t0, t1, thr=-40):
    h = int(0.01 * SR)
    for t in np.arange(t0, t1, 0.01):
        s = x[int(t * SR):int(t * SR) + h]
        if 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9) > thr: return t
    return t1
o2 = onset(53.4, 55.0)
MIST = [(51.02, o2 - 0.04),          # false start, keep the restart
        (14.38, 14.88),              # "goddamn" removed -> "lost their mind"
        (328.95, 329.31)]            # "ass" removed -> "pathetic sport"
mist = MIST
w = [q for q in W if not any(a <= (q["s"] + q["e"]) / 2 <= b for a, b in mist)]
cuts = [c for c in pause_cuts(x, SR, w, min_gap=1.0, keep=0.4) if all(c[1] <= a or c[0] >= b for a, b in mist)] + mist
a0 = max(0, safe_point(x, SR, w[0]["s"] - 0.35, 0.3)); b0 = min(len(x) / SR, w[-1]["e"] + 0.8)
cuts = sorted(cuts); segs = []; s0 = a0
for c0, c1 in cuts:
    if c0 > s0: segs.append((s0, c0))
    s0 = max(s0, c1)
segs.append((s0, b0))
y = []
for u, v in segs:
    seg = x[int(u * SR):int(v * SR)].copy(); n = int(0.012 * SR)
    if len(seg) > 2 * n: seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
    y.append(seg)
y = np.concatenate(y)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", str(SR), "-c:a", "pcm_s16le", f"{P}/vo_clean.wav"],
               input=y.tobytes(), check=True)
json.dump({"cuts": cuts, "start": a0, "end": b0, "segs": segs}, open(f"{P}/vo_cuts.json", "w"))
print("onset2", round(o2, 2), "cuts", len(cuts), "raw", round(len(x) / SR, 1), "->", round(len(y) / SR, 1), "s")

"""Match a TTS take to the user's natural rhythm WITHOUT slowing the words (user, 22 Nov 2026: slowed takes sound
"too slow and chill"). Keeps every word at its generated speed; only lengthens existing pauses toward the user's
measured pause length (their reads: ~19 pauses per 100 words, median ~0.70 s). Optional pitch shift in semitones
(the user's voice sits ~140-158 Hz; the clone came out ~170-190 Hz).
usage: python3 match_rhythm.py IN.mp3 OUT.mp3 [--pause 0.70] [--semitones 0] [--min-gap 0.22]"""
import sys, subprocess, re, argparse, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--pause", type=float, default=0.70); ap.add_argument("--semitones", type=float, default=0.0)
ap.add_argument("--min-gap", type=float, default=0.22); a = ap.parse_args()
SR = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.inp, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.float32)
log = subprocess.run(["ffmpeg", "-i", a.inp, "-af", f"silencedetect=n=-38dB:d={a.min_gap}", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", log)]; en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
out, cur, added = [], 0, 0.0
rng = np.random.default_rng(7)
for s, e in zip(st, en):
    if s < 0.3 or e > len(x) / SR - 0.2: continue
    g = e - s; tgt = max(g, rng.normal(a.pause, 0.12))      # only lengthen, never shorten
    mid = int((s + e) / 2 * SR)
    out.append(x[cur:mid]); out.append(np.zeros(int((tgt - g) * SR), np.float32)); cur = mid; added += tgt - g
out.append(x[cur:]); y = np.concatenate(out)
af = []
if a.semitones: r = 2 ** (a.semitones / 12); af = [f"asetrate={int(SR*r)},aresample={SR},atempo={1/r:.6f}"]
p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-"] + (["-af", af[0]] if af else []) + ["-b:a", "192k", a.out], input=y.tobytes())
print(f"{a.out}: {len(x)/SR:.1f}s -> {len(y)/SR:.1f}s, +{added:.1f}s over {len(st)} pauses")

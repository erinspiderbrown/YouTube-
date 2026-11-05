"""Pace a voiceover to a target words-per-minute WITHOUT making it sound robotic, then warm-EQ, level and stitch it.

Why: stretching a cloned voice (rubberband at 0.85-0.92) smears it and sounds robotic, more so the harder it is
pushed. Here every section is split into phrases at its natural pauses. Each phrase gets at most a light WSOLA
slow-down (atempo, never below --min-tempo, default 0.96), and the rest of the time is added as extra pause
between phrases. Sentence ends get twice the extra pause of commas and breaths. The voice itself stays untouched.

Usage:
  python3 tools/space_voiceover.py --target-wpm 166 --out FULL.mp3 [--gap 0.7] [--words-json words.json] SEC1.mp3 SEC2.mp3 ...
Writes FULL.mp3 (and FULL.wav), plus optional word timings of the result for the edit.
"""
import argparse, json, subprocess
import numpy as np
from faster_whisper import WhisperModel

SR = 44100
EQ = ("highpass=f=55,equalizer=f=130:t=q:w=0.9:g=1.2,equalizer=f=320:t=q:w=1.4:g=-1.0,highshelf=f=2600:g=-5.5,"
      "equalizer=f=6800:t=q:w=1.6:g=-1.5,deesser=i=0.35:m=0.5:f=0.5,acompressor=threshold=-22dB:ratio=2.2:attack=12:release=220:makeup=2")

def load(path, sr=SR):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()

def atempo(x, tempo):
    if abs(tempo - 1) < 1e-3: return x
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.4f}",
                        "-f", "f32le", "-"], input=x.tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()

def words_of(model, x16):
    segs, _ = model.transcribe(x16, word_timestamps=True)
    return [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in s.words]

def artic(ws):
    """Speaking speed without the pauses: words per minute of talking time (gaps over 0.25 s left out)."""
    talk = sum(w["e"] - w["s"] for w in ws) + sum(max(0, b["s"] - a["e"]) for a, b in zip(ws, ws[1:]) if b["s"] - a["e"] < 0.25)
    return len(ws) / talk * 60

def pace_section(model, path, target_wpm, min_tempo, max_extra, split_gap, ref_artic=None, tempo_scale=1.0):
    x = load(path); x16 = load(path, 16000)
    ws = words_of(model, x16)
    n, dur = len(ws), len(x) / SR
    if ref_artic:   # match the reference take's speaking speed first, so every section sounds like the same read
        tempo = max(min_tempo, min(1.0, ref_artic / artic(ws)) * tempo_scale)
        target = max(n / target_wpm * 60, dur / tempo)
    else:
        target = n / target_wpm * 60
        tempo = max(min_tempo, min(1.0, dur / target) * tempo_scale)
    # cut points at the middle of every pause >= split_gap
    cuts, kinds = [], []
    for a, b in zip(ws, ws[1:]):
        g = b["s"] - a["e"]
        if g >= split_gap:
            cuts.append((a["e"] + b["s"]) / 2)
            kinds.append(2.0 if a["w"][-1:] in ".?!…" else 1.0)
    after = dur / tempo
    extra = max(0.0, target - after)
    wsum = sum(kinds) or 1
    adds = [min(max_extra, extra * k / wsum) for k in kinds]
    bounds = [0.0] + cuts + [dur]
    out = []
    for i in range(len(bounds) - 1):
        seg = x[int(bounds[i] * SR):int(bounds[i + 1] * SR)]
        out.append(atempo(seg, tempo))
        if i < len(adds): out.append(np.zeros(int(adds[i] * SR), np.float32))
    y = np.concatenate(out)
    return y, dict(file=path, words=n, raw_s=round(dur, 1), raw_wpm=round(n / dur * 60), artic=round(artic(ws)), tempo=round(tempo, 3),
                   pauses=len(cuts), added_s=round(sum(adds), 1), out_s=round(len(y) / SR, 1), out_wpm=round(n / (len(y) / SR) * 60))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--target-wpm", type=float, default=166)
    ap.add_argument("--min-tempo", type=float, default=0.96)
    ap.add_argument("--max-extra", type=float, default=0.9, help="most extra pause added at one break (s)")
    ap.add_argument("--split-gap", type=float, default=0.12, help="pause length (s) that counts as a phrase break")
    ap.add_argument("--gap", type=float, default=0.7, help="silence between sections (s)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--words-json")
    ap.add_argument("--tempo-scale", type=float, default=1.0, help="slow every section's speaking speed by this factor (keep >= 0.92 or it sounds robotic)")
    ap.add_argument("--ref", help="reference take whose speaking speed every section is matched to")
    a = ap.parse_args()
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    ref = artic(words_of(model, load(a.ref, 16000))) if a.ref else None
    if ref: print(f"reference speaking speed {ref:.0f} wpm ({a.ref})")
    parts = []
    for p in a.inputs:
        y, info = pace_section(model, p, a.target_wpm, a.min_tempo, a.max_extra, a.split_gap, ref, a.tempo_scale)
        print(json.dumps(info))
        parts += [y, np.zeros(int(a.gap * SR), np.float32)]
    full = np.concatenate(parts[:-1])
    wav = a.out.rsplit(".", 1)[0] + ".wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-af", EQ + ",loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", str(SR), "-c:a", "pcm_s16le", wav],
                   input=np.clip(full, -1, 1).tobytes(), check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", a.out], check=True)
    ws = words_of(model, load(wav, 16000))
    d = len(full) / SR
    print(f"FULL {a.out}: {int(d // 60)}:{d % 60:04.1f}  {len(ws)} words  {len(ws) / d * 60:.0f} wpm")
    if a.words_json:
        json.dump([{"words": ws}], open(a.words_json, "w"))

if __name__ == "__main__":
    main()

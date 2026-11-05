"""Time-fit voiceover sections to a target speaking pace, normalise loudness, and stitch.

Usage:
  python3 tools/pace_voiceover.py --target-wpm 166 --gap 0.6 --out FULL.mp3 SEC1_raw.mp3 SEC2_raw.mp3 ...

For each section:
- measure words-per-minute (word count over the section's full duration) with faster-whisper
- tempo = target / measured, clamped to 0.85–1.05, applied with rubberband (pitch- and formant-preserving)
- loudness normalised to -16 LUFS
Each processed section is written next to its input as *_paced.mp3; then all are joined with a short gap.
"""
import argparse, os, subprocess, tempfile, wave
import numpy as np
from faster_whisper import WhisperModel

def wav16(src, dst):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", dst], check=True)

def load(p):
    w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def wpm(model, path, tmp):
    wav16(path, tmp); a = load(tmp)
    segs = list(model.transcribe(a, word_timestamps=True)[0])
    n = sum(len(s.words) for s in segs)
    return n / (len(a) / 16000) * 60, n, len(a) / 16000

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--target-wpm", type=float, default=166)
    ap.add_argument("--gap", type=float, default=0.6)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    tmp = os.path.join(tempfile.mkdtemp(), "t.wav")
    outs = []
    for p in a.inputs:
        raw_wpm, n, dur = wpm(model, p, tmp)
        tempo = min(1.05, max(0.85, a.target_wpm / raw_wpm))
        o = p.replace("_raw.mp3", "").replace(".mp3", "") + "_paced.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-af",
                        f"rubberband=tempo={tempo:.4f}:pitchq=quality:formant=preserved:window=standard,"
                        "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", o], check=True)
        new_wpm, _, new_dur = wpm(model, o, tmp)
        print(f"{os.path.basename(p):40s} raw {raw_wpm:5.0f} wpm ({dur:5.1f}s) -> tempo {tempo:.3f} -> {new_wpm:5.0f} wpm ({new_dur:5.1f}s)")
        outs.append(o)
    ins = []; fc = ""
    for i, o in enumerate(outs):
        ins += ["-i", o]; fc += f"[{i}:a]aresample=44100,apad=pad_dur={a.gap}[a{i}];"
    fc += "".join(f"[a{i}]" for i in range(len(outs))) + f"concat=n={len(outs)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", fc, "-map", "[out]", "-ar", "44100",
                    "-c:a", "libmp3lame", "-b:a", "192k", a.out], check=True)
    tot_wpm, n, dur = wpm(model, a.out, tmp)
    print(f"FULL {a.out}: {dur/60:.0f}:{dur%60:04.1f}  {n} words  {tot_wpm:.0f} wpm overall")

if __name__ == "__main__":
    main()

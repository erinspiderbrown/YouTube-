"""Re-time vo_user_v{V}_words.json part by part with faster-whisper on the cleaned voiceover (after clean_voiceover.py)."""
import json, os, subprocess, numpy as np
from faster_whisper import WhisperModel
V = os.environ.get("V", "2"); P = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{P}/vo_user_v{V}_words.json"))[0]["words"]
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=8)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{P}/boling_voiceover_user_v{V}.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
out = []
for k in range(1, 9):
    ws = [w for w in W if w["part"] == k]; a = max(0, ws[0]["s"] - 0.4); b = ws[-1]["e"] + 0.6
    segs, _ = m.transcribe(x[int(a * 16000):int(b * 16000)], word_timestamps=True, condition_on_previous_text=False, beam_size=5)
    for s in segs:
        for w in s.words: out.append(dict(w=w.word.strip(), s=round(w.start + a, 3), e=round(w.end + a, 3), part=k))
json.dump([{"words": out}], open(f"{P}/vo_user_v{V}_words.json", "w")); print("words", len(out), "end", out[-1]["e"])

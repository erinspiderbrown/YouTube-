import sys, json, wave, numpy as np
def load(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0; return a
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for wav, out in zip(sys.argv[1::2], sys.argv[2::2]):
    segs, _ = m.transcribe(load(wav), word_timestamps=True, vad_filter=True)
    data = []
    with open(out + ".txt", "w") as t:
        for s in segs:
            t.write(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}\n")
            data.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                         "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]})
    json.dump(data, open(out + ".json", "w"))
    print("done", out)

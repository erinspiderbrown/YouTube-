import json, subprocess, sys, numpy as np
S = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
SR = 44100; TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
d = json.load(open(f"{S}/vo/take_scores4.json"))
def load(p): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout,np.float32).copy()
def atempo(x,t): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={t}","-f","f32le","-"],input=x.tobytes(),capture_output=True,check=True).stdout,np.float32).copy()
XF = int(0.012 * SR)
def join(a, b):
    if len(a) < XF or len(b) < XF: return np.concatenate([a, b])
    r = np.linspace(0, 1, XF, dtype=np.float32)
    return np.concatenate([a[:-XF], a[-XF:] * (1 - r) + b[:XF] * r, b[XF:]])
for sid, v in d.items():
    x = load(f"{S}/vo/raw4/{sid}.mp3")
    spans = [(w["s"] - 0.04, w["e"] + 0.04) for w in v["words"] if w["w"].lower().strip(" .,?!'\"").startswith(("kenya", "kinya", "kenyan"))]
    out = np.zeros(0, np.float32); pos = 0
    for s, e in spans:
        a, b = int(max(pos, s * SR)), int(min(len(x), e * SR))
        out = join(out, x[pos:a]) if len(out) else x[pos:a]
        out = join(out, atempo(x[a:b], TEMPO)); pos = b
    out = join(out, x[pos:]) if len(out) else x
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-c:a","libmp3lame","-b:a","192k",f"{S}/vo/raw5/{sid}.mp3"],input=np.clip(out,-1,1).tobytes(),check=True)
    print(sid, len(spans), round(len(x)/SR,2), "->", round(len(out)/SR,2))

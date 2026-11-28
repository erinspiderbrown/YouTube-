"""Similarity of TTS windows to the user's REAL voice (ECAPA speaker embeddings, speechbrain).
Reference = mean embedding of 4 s windows from the user's own recorded voiceovers."""
import sys, glob, subprocess, numpy as np, torch, json, os
from speechbrain.inference.speaker import EncoderClassifier
enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="sb_spk")
P = "/home/user/YouTube-/projects"
REFS = [f"{P}/matthew-boling/boling_voiceover_user_v2.wav", f"{P}/katelyn-tuohy/tuohy_voiceover.wav", f"{P}/alan-webb/webb_voiceover.wav",
        f"{P}/drew-hunter/vo_clean.wav", f"{P}/michael-norman/vo_clean.wav"]
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout,np.float32)
def emb(x):
    with torch.no_grad(): e = enc.encode_batch(torch.tensor(x).unsqueeze(0))[0, 0].numpy()
    return e / np.linalg.norm(e)
def windows(x, w=4.0, hop=4.0):
    n = int(w*16000); h = int(hop*16000)
    for i in range(0, max(1, len(x) - n + 1), h):
        seg = x[i:i+n]
        if np.sqrt((seg**2).mean()) > 0.01: yield i/16000, seg
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref_user_emb.npy")
if not os.path.exists(REF):
    es = []
    for f in REFS:
        x = load(f)[: 16000*240]
        es += [emb(s) for _, s in windows(x)]
    r = np.mean(es, 0); np.save(REF, r / np.linalg.norm(r)); print("ref windows", len(es))
ref = np.load(REF)
for f in sys.argv[1:]:
    x = load(f); sims = [(t, float(emb(s) @ ref)) for t, s in windows(x, 4.0, 2.0)]
    v = [s for _, s in sims]
    print(f"{os.path.basename(f):28s} mean={np.mean(v):.3f} min={np.min(v):.3f} " + " ".join(f"{t:.0f}:{s:.2f}" for t, s in sims))

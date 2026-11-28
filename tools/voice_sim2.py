"""Similarity to the APPROVED clone voice (the user's accepted videos), per 4 s window."""
import sys, subprocess, numpy as np, torch, os
from speechbrain.inference.speaker import EncoderClassifier
enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="sb_spk")
P = "/home/user/YouTube-/projects"
REFS = [f"{P}/yomif-kejelcha/vo_kejelcha.mp3", f"{P}/noah-lyles/vo_lyles.mp3", f"{P}/kevin-dare/vo_dare.mp3", f"{P}/cooper-lutkenhaus/vo_cooper.mp3"]
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout,np.float32)
def emb(x):
    with torch.no_grad(): e = enc.encode_batch(torch.tensor(x).unsqueeze(0))[0, 0].numpy()
    return e / np.linalg.norm(e)
def windows(x, w=4.0, hop=4.0):
    n = int(w*16000); h = int(hop*16000)
    for i in range(0, max(1, len(x) - n + 1), h):
        seg = x[i:i+n]
        if np.sqrt((seg**2).mean()) > 0.01: yield i/16000, seg
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref_approved_emb.npy")
if not os.path.exists(REF):
    es = []
    for f in REFS: es += [emb(s) for _, s in windows(load(f)[:16000*200])]
    r = np.mean(es, 0); np.save(REF, r/np.linalg.norm(r)); print("ref windows", len(es))
ref = np.load(REF)
for f in sys.argv[1:]:
    x = load(f); sims = [(t, float(emb(s) @ ref)) for t, s in windows(x, 4.0, 2.0)]
    v = [s for _, s in sims]
    print(f"{f[-34:]:34s} mean={np.mean(v):.3f} min={np.min(v):.3f} | " + " ".join(f"{t:.0f}:{s:.2f}" for t, s in sims))

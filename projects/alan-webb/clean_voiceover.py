"""Alan Webb: clean the user's one-take voiceover (Dropbox Alan-webb.m4a, 5:59).
Every cut sits inside measured silence (tools/safe_cuts.py), never at whisper word ends,
so years and numbers are never clipped. After cleaning, the output is re-transcribed and
every number in the script is checked (check_vo.py)."""
import json, os, subprocess, sys, numpy as np
P=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(P, "..", "..", "tools"))
from safe_cuts import pause_cuts, safe_point
SR=48000
RAW=sys.argv[1]
CHAIN="highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5"
W=json.load(open(f"{P}/vo_words_raw.json"))
# flubs (raw seconds)
MIST=[(83.3,85.95)]   # "America wasn't winning nothing. | The American athletes weren't winning anything."
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",RAW,"-af",CHAIN,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout,np.float32).copy()
mist=[(safe_point(x,SR,a,0.25),safe_point(x,SR,b,0.25)) for a,b in MIST]
w=[q for q in W if not any(a<=(q["s"]+q["e"])/2<=b for a,b in mist)]
cuts=[c for c in pause_cuts(x,SR,w,min_gap=1.0,keep=0.35) if all(c[1]<=a or c[0]>=b for a,b in mist)]+mist
a0=max(0,safe_point(x,SR,w[0]["s"]-0.4,0.3)); b0=min(len(x)/SR,w[-1]["e"]+0.8)
cuts=sorted(cuts); segs=[]; s0=a0
for c0,c1 in cuts: segs.append((s0,c0)); s0=c1
segs.append((s0,b0))
y=[]
for u,v in segs:
    seg=x[int(u*SR):int(v*SR)].copy(); n=int(0.015*SR)
    if len(seg)>2*n: seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    y.append(seg)
y=np.concatenate(y)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89","-ar",str(SR),"-c:a","pcm_s16le",f"{P}/webb_voiceover.wav"],input=y.tobytes(),check=True)
json.dump({"cuts":cuts,"start":a0,"end":b0},open(f"{P}/vo_cuts.json","w"))
print("cuts",len(cuts),"raw",round(len(x)/SR,1),"->",round(len(y)/SR,1),"s")

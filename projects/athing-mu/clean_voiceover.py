"""Athing Mu: clean the user's one-take voiceover (Dropbox 2220-W-Mission-Ln-6.m4a).
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
MIST=[(83.3,86.4),(141.85,143.52),(190.9,195.6),(198.12,200.5),(382.9,384.12)]
# restart "He says she had more th-" ; "June 21st," (wrong date: Trials final was June 27) ; first "She holds Keely Hodgkinson off by one." ;
# "by eight thousandths of a second" (wrong: it was 0.08 s, shown as a graphic) ; "14"/"4:10" (shown as a graphic)
MUTE=[(90.9,91.3),(149.1,149.45)]   # stray noises in the pauses (user, 19 Nov 2026: mic/grunt noises between takes)
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",RAW,"-af",CHAIN,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout,np.float32).copy()
for a,b in MUTE: x[int(a*SR):int(b*SR)]=0.0
mist=[(safe_point(x,SR,m[0],m[2] if len(m)>2 else 0.25),safe_point(x,SR,m[1],m[2] if len(m)>2 else 0.25)) for m in MIST]
w=[q for q in W if not any(a<=(q["s"]+q["e"])/2<=b for a,b in mist)]
cuts=[c for c in pause_cuts(x,SR,w,min_gap=0.8,keep=0.35) if all(c[1]<=a or c[0]>=b for a,b in mist)]+mist
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
# second pass (user, 19 Nov 2026: "remove the long pauses"): every measured silence longer than 0.6 s is shortened to 0.5 s,
# cutting only inside the silence (0.25 s kept on each side), so no word is touched.
fr=int(0.01*SR); e=np.sqrt(np.convolve(y**2,np.ones(fr)/fr,'same'))[::fr]; db=20*np.log10(e+1e-9); fl=np.percentile(db,8); q=db<fl+14
keep=np.ones(len(y),bool); i=0; nsil=0
while i<len(q):
    if q[i]:
        j=i
        while j<len(q) and q[j]: j+=1
        if (j-i)*0.01>0.6 and i>0 and j<len(q): keep[(i+25)*fr:(j-25)*fr]=False; nsil+=1
        i=j
    else: i+=1
# rebuild from the kept stretches with 10 ms fades at every join, so no cut can click
idx=np.flatnonzero(np.diff(np.concatenate([[0],keep.astype(np.int8),[0]])))
segs2=[]; n=int(0.01*SR)
for u,v in zip(idx[::2],idx[1::2]):
    s=y[u:v].copy()
    if len(s)>2*n: s[:n]*=np.linspace(0,1,n); s[-n:]*=np.linspace(1,0,n)
    segs2.append(s)
y=np.concatenate(segs2); print("long pauses shortened:",nsil)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89","-ar",str(SR),"-c:a","pcm_s16le",f"{P}/athing_voiceover.wav"],input=y.tobytes(),check=True)
json.dump({"cuts":cuts,"start":a0,"end":b0},open(f"{P}/vo_cuts.json","w"))
print("cuts",len(cuts),"raw",round(len(x)/SR,1),"->",round(len(y)/SR,1),"s")

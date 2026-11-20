"""Mondo Duplantis: clean the user's one-take voiceover (Dropbox Mondo.m4a, 20 Nov 2026).
User: cut errors, long pauses, background noises and every repeated line.
- MIST: restarts/wrong lines, cut at measured-silence points (checked on the waveform).
- Gap gating: between words, everything after the true end of one word and before the onset of the next
  is muted (with fades), so grunts/mic bumps/breath noise in the pauses go away; the word edges are found
  by energy with a 0.15 s hold, never by whisper end times (they run early on numbers).
- Long pauses: any silence over 0.6 s is shortened to 0.5 s.
Then check_vo.py re-transcribes and checks every number."""
import json, os, subprocess, sys, numpy as np
P=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(P, "..", "..", "tools"))
from safe_cuts import rms_db, noise_floor, pause_cuts
SR=48000; HOP=0.01
RAW=sys.argv[1]
CHAIN="highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5"
W=json.load(open(f"{P}/vo_words_raw.json"))
MIST=[(238.9,240.7),    # "The tro-" restart before "The trophy"
      (261.1,268.3),    # "Everybody calls him..." restart
      (342.9,347.9),    # "February? He clears 6.19 indoors." (wrong number: it was 6.17; shown as a graphic instead)
      (371.5,374.9),    # "Higher than everybody." (he is 2nd all-time, not higher than Mondo)
      (458.8,463.9)]    # "He said he had too much going on and not enough time to..." restart
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",RAW,"-af",CHAIN,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout,np.float32).copy()
db=rms_db(x,SR); thr=noise_floor(db)+14
def onset_back(t,lim):   # walk back from whisper start until 0.10 s of silence
    i=int(t/HOP); q=0; first=t
    while i>int(lim/HOP):
        if db[i]>thr: first=i*HOP; q=0
        else:
            q+=1
            if q*HOP>=0.10: break
        i-=1
    return first
def offset_fwd(t,lim):   # walk forward from whisper end until 0.15 s of silence
    i=int(t/HOP); q=0; last=t
    while i<min(len(db),int(lim/HOP)):
        if db[i]>thr: last=(i+1)*HOP; q=0
        else:
            q+=1
            if q*HOP>=0.15: break
        i+=1
    return last
w=[q for q in W if not any(a<=(q["s"]+q["e"])/2<=b for a,b in MIST)]
nm=0
for p,q in zip(w,w[1:]):
    if q["s"]-p["e"]<0.2: continue
    a=offset_fwd(p["e"],q["s"])+0.06; b=onset_back(q["s"],a)-0.05
    if b-a>=0.15:
        i,j=int(a*SR),int(b*SR); n=int(0.01*SR)
        x[i:i+n]*=np.linspace(1,0,n); x[j-n:j]*=np.linspace(0,1,n); x[i+n:j-n]=0.0; nm+=1
a0=max(0,w[0]["s"]-0.4); b0=min(len(x)/SR,offset_fwd(w[-1]["e"],len(x)/SR)+0.6)
cuts=sorted(MIST); segs=[]; s0=a0
for c0,c1 in cuts: segs.append((s0,c0)); s0=c1
segs.append((s0,b0)); y=[]
for u,v in segs:
    seg=x[int(u*SR):int(v*SR)].copy(); n=int(0.015*SR)
    if len(seg)>2*n: seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    y.append(seg)
y=np.concatenate(y)
fr=int(0.01*SR); e=np.sqrt(np.convolve(y**2,np.ones(fr)/fr,'same'))[::fr]; d=20*np.log10(e+1e-9); qq=d<noise_floor(d)+14
keep=np.ones(len(y),bool); i=0; nsil=0
while i<len(qq):
    if qq[i]:
        j=i
        while j<len(qq) and qq[j]: j+=1
        if (j-i)*0.01>0.6 and i>0 and j<len(qq): keep[(i+25)*fr:(j-25)*fr]=False; nsil+=1
        i=j
    else: i+=1
idx=np.flatnonzero(np.diff(np.concatenate([[0],keep.astype(np.int8),[0]])))
out=[]; n=int(0.01*SR)
for u,v in zip(idx[::2],idx[1::2]):
    s=y[u:v].copy()
    if len(s)>2*n: s[:n]*=np.linspace(0,1,n); s[-n:]*=np.linspace(1,0,n)
    out.append(s)
y=np.concatenate(out)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89","-ar",str(SR),"-c:a","pcm_s16le",f"{P}/mondo_voiceover.wav"],input=y.tobytes(),check=True)
json.dump({"mist":MIST,"start":a0,"end":b0},open(f"{P}/vo_cuts.json","w"))
print("gaps muted",nm,"long pauses shortened",nsil,"raw",round(len(x)/SR,1),"->",round(len(y)/SR,1),"s")

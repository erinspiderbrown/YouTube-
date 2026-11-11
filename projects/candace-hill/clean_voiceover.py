"""Candace Hill: clean the user's own voiceover (copied from projects/matthew-boling/clean_voiceover.py).
raw/ = the user's 8 Dropbox takes. Words from a per-chunk faster-whisper pass (vo_words_raw.json);
the whole-file pass skipped a full sentence in part 8, so chunked words are the source of truth."""
import json, os, subprocess, numpy as np, sys
SR=48000
RAW=sys.argv[1] if len(sys.argv)>1 else "raw"
order=['Candace 1.m4a','Candace 2.m4a','Candace pt 3.m4a','Candace 4.m4a','Candace 5.m4a','Candace 6.m4a','Candace 7.m4a','Candace 8.m4a']
P=os.path.dirname(os.path.abspath(__file__))
W=json.load(open(f"{P}/vo_words_raw.json"))
# usable span per take (start, end)
SPAN={'Candace 1.m4a':(5.15,47.75),'Candace 7.m4a':(1.6,None)}
# flubbed takes / restarts, snapped to silences
MIST={'Candace pt 3.m4a':[(13.55,17.62)],    # "ASICS ain't never signed the number" -> keep the re-read "ain't never say the number"
      'Candace 6.m4a':[(29.25,33.85)]}        # "8." (she was 9th of 9 in the 2021 final, per NBC's results board) + "Then she moved to the..." restart
# whisper hallucinations on breaths/tails (drop the words, keep the audio)
JUNK={"We'll","be","right","back.","Peace!","See","you","next","time.","Yes.","it."}
CHAIN="highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5"
def load(f):
    r=subprocess.run(["ffmpeg","-v","error","-i",f"{RAW}/{f}","-af",CHAIN,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True)
    return np.frombuffer(r.stdout,np.float32).copy()
parts=[]; log=[]; tl=[]; t=0.0; GAP=0.9
for k,f in enumerate(order):
    x=load(f); w=[q for q in W[f] if q["w"] not in JUNK]
    sa,sb=SPAN.get(f,(None,None))
    a=sa if sa is not None else max(0,w[0]["s"]-0.25)
    b=min(len(x)/SR, sb if sb is not None else w[-1]["e"]+0.45)
    w=[q for q in w if a<=q["s"]<=b and not any(m0<=(q["s"]+q["e"])/2<=m1 for m0,m1 in MIST.get(f,[]))]
    cuts=[]
    for p,q in zip(w,w[1:]):
        g=q["s"]-p["e"]
        if g>1.0: cuts.append((p["e"]+0.3,q["s"]-0.35))
    for m0,m1 in MIST.get(f,[]):
        cuts=[c for c in cuts if c[1]<=m0 or c[0]>=m1]+[(m0,m1)]
    cuts.sort()
    segs=[]; s0=a
    for c0,c1 in cuts: segs.append((s0,c0)); s0=c1
    segs.append((s0,b))
    y=[]
    for u,v in segs:
        seg=x[int(u*SR):int(v*SR)].copy(); n=int(0.012*SR)
        if len(seg)>2*n: seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
        y.append(seg)
    y=np.concatenate(y)
    def mp(tt):
        o=tt-a
        for c0,c1 in cuts:
            if tt>=c1: o-=(c1-c0)
            elif tt>c0: o-=(tt-c0)
        return o
    for ww in w: tl.append(dict(w=ww["w"],s=round(t+mp(ww["s"]),3),e=round(t+mp(min(ww["e"],b)),3),part=k+1))
    log.append((k+1,f,round(len(x)/SR,1),round(len(y)/SR,1),len(cuts)))
    parts.append(y); t+=len(y)/SR
    if k<len(order)-1: parts.append(np.zeros(int(GAP*SR),np.float32)); t+=GAP
full=np.concatenate(parts)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89","-ar",str(SR),"-c:a","pcm_s16le",f"{P}/candace_voiceover.wav"],input=full.tobytes(),check=True)
json.dump([{"words":tl}],open(f"{P}/vo_words.json","w"))
for l in log: print(l)
print("total",round(len(full)/SR,1),"s")

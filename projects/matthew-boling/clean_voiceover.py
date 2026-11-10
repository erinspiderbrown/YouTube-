import json, subprocess, numpy as np
SR=48000
order=["Boling vid pt 1.m4a","Boling part 2.m4a","Matt pt 3.m4a","Matt pt 4.m4a","Matt pt 5.m4a","Matt pt 6.m4a","Matt pt 7.m4a","Matt pt 7 (1).m4a"]
W=json.load(open("words_raw.json"))
endfix={"Matt pt 5.m4a":51.65}
CHAIN="highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5"
def load(f):
    r=subprocess.run(["ffmpeg","-v","error","-i","raw/"+f,"-af",CHAIN,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True)
    return np.frombuffer(r.stdout,np.float32).copy()
parts=[]; log=[]; tl=[]; t=0.0; GAP=0.9
for k,f in enumerate(order):
    x=load(f); w=W[f]
    a=max(0,w[0]["s"]-0.25); b=min(len(x)/SR, endfix.get(f, w[-1]["e"]+0.45))
    # shorten long pauses between words (>1.0s -> 0.65s), keep everything else as read
    cuts=[]
    for p,q in zip(w,w[1:]):
        g=q["s"]-p["e"]
        if g>1.0 and p["e"]>a and q["s"]<b: cuts.append((p["e"]+0.3,q["s"]-0.35))
    segs=[]; s0=a
    for c0,c1 in cuts: segs.append((s0,c0)); s0=c1
    segs.append((s0,b))
    y=[]
    for i,(u,v) in enumerate(segs):
        seg=x[int(u*SR):int(v*SR)].copy(); n=int(0.012*SR)
        if len(seg)>2*n: seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
        y.append(seg)
    y=np.concatenate(y)
    removed=sum(c1-c0 for c0,c1 in cuts)
    log.append((k+1,f,round(len(x)/SR,1),round(len(y)/SR,1),len(cuts),round(removed,1)))
    # word map: original time -> new time
    def mp(tt):
        o=tt-a
        for c0,c1 in cuts:
            if tt>=c1: o-=(c1-c0)
            elif tt>c0: o-=(tt-c0)
        return o
    for ww in w:
        if a<=ww["s"]<=b: tl.append(dict(w=ww["w"],s=round(t+mp(ww["s"]),3),e=round(t+mp(min(ww["e"],b)),3),part=k+1))
    parts.append(y); t+=len(y)/SR
    if k<len(order)-1: parts.append(np.zeros(int(GAP*SR),np.float32)); t+=GAP
full=np.concatenate(parts)
P="/home/user/YouTube-/projects/matthew-boling"
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-af","loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89","-ar",str(SR),"-c:a","pcm_s16le",f"{P}/boling_voiceover_user_v1.wav"],input=full.tobytes(),check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{P}/boling_voiceover_user_v1.wav","-c:a","libmp3lame","-b:a","192k",f"{P}/boling_voiceover_user_v1.mp3"],check=True)
json.dump([{"words":tl}],open(f"{P}/vo_user_v1_words.json","w"))
for l in log: print(l)
print("total",round(len(full)/SR,1),"s")

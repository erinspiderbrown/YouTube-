"""Transcribe windows of clips (small.en). args: CLIPDIR spec... where spec = name[:a-b[,a-b]]"""
import sys,json,subprocess,numpy as np,os
from faster_whisper import WhisperModel
C=sys.argv[1]; m=WhisperModel("small.en",compute_type="int8",cpu_threads=2)
for spec in sys.argv[2:]:
    name,_,w=spec.partition(":"); out=f"{C}/tx_{name}.json"
    if os.path.exists(out): continue
    wins=[tuple(map(float,x.split("-"))) for x in w.split(",")] if w else [(0,None)]
    segs=[]
    for a,b in wins:
        cmd=["ffmpeg","-v","error","-ss",str(a)]+(["-t",str(b-a)] if b else [])+["-i",f"{C}/clips/{name}.mp4","-ac","1","-ar","16000","-f","f32le","-"]
        x=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32)
        s,_=m.transcribe(x,word_timestamps=True,beam_size=3,vad_filter=True,condition_on_previous_text=False)
        segs+=[{"s":round(g.start+a,2),"e":round(g.end+a,2),"t":g.text.strip(),"words":[{"w":q.word.strip(),"s":round(q.start+a,2),"e":round(q.end+a,2)} for q in g.words]} for g in s]
    json.dump(segs,open(out,"w")); print("done",name,flush=True)

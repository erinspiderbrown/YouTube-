import sys,json,subprocess,numpy as np,os
from faster_whisper import WhisperModel
C=sys.argv[1]; m=WhisperModel("small.en",compute_type="int8")
for f in sys.argv[2:]:
    out=f"{C}/tx_{f}.json"
    if os.path.exists(out): continue
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"{C}/clips/{f}.mp4","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    s,_=m.transcribe(x,word_timestamps=True,beam_size=5,vad_filter=True,condition_on_previous_text=False)
    segs=[{"s":round(g.start,2),"e":round(g.end,2),"t":g.text.strip(),"words":[{"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)} for w in g.words]} for g in s]
    json.dump(segs,open(out,"w")); print("done",f,flush=True)

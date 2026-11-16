"""Verbatim word transcript of the user's raw take (no VAD, so flubs and restarts stay in)."""
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
raw,out=sys.argv[1],sys.argv[2]
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",raw,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
m=WhisperModel("medium.en",compute_type="int8")
s,_=m.transcribe(x,word_timestamps=True,beam_size=5,condition_on_previous_text=False)
W=[{"w":w.word.strip(),"s":round(w.start,3),"e":round(w.end,3)} for sg in s for w in sg.words]
json.dump(W,open(out,"w"))
print(len(W))

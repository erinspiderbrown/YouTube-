"""Re-transcribe the cleaned VO; every number the user said in the raw take must come back whole."""
import json, subprocess, sys, os, re, numpy as np
from faster_whisper import WhisperModel
P=os.path.dirname(os.path.abspath(__file__))
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"{P}/tuohy_voiceover.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
m=WhisperModel("medium.en",compute_type="int8")
s,_=m.transcribe(x,word_timestamps=True,beam_size=5,condition_on_previous_text=False,vad_filter=True,vad_parameters={"min_silence_duration_ms":400})
W=[{"w":w.word.strip(),"s":round(w.start,3),"e":round(w.end,3)} for sg in s for w in sg.words]
json.dump(W,open(f"{P}/vo_words.json","w"))
num=lambda ws:[re.sub(r"[^\d.]","",w["w"]).strip(".") for w in ws if re.search(r"\d",w["w"])]
raw=num(json.load(open(f"{P}/vo_words_raw.json"))); new=num(W)
print("raw:",raw); print("new:",new); print("MATCH" if raw==new else "MISMATCH")

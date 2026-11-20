"""Re-transcribe short chunks of the raw take (medium.en, no VAD) to check flubs. args: RAW a-b a-b ..."""
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
raw=sys.argv[1]; m=WhisperModel("medium.en",compute_type="int8")
for spec in sys.argv[2:]:
    a,b=map(float,spec.split("-"))
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(b-a),"-i",raw,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    s,_=m.transcribe(x,word_timestamps=True,beam_size=5,condition_on_previous_text=False,initial_prompt="Mondo Duplantis, Emmanouil Karalis, Manolo, Kurtis Marschall, Sam Kendricks, Desiré Inglander, Lausanne, Zurich, Brussels, Stockholm, 6.21, 6.32, Lavillenie, Bubka.")
    print(f"== {spec}: "+" ".join(f"{w.word.strip()}[{w.start+a:.1f}]" for g in s for w in g.words),flush=True)

"""Description for the final cut: chapters from the build timeline + clip credits."""
import sys
sys.argv = ["x"]
exec(open("/home/user/YouTube-/projects/ishowspeed-10-35/speed_build.py").read().split("if __name__")[0])
shots, ov, end = TL()
def ts(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
ch = [("0:00", "IShowSpeed ran 10.35")] + [(ts(o0), spec[2]) for o0, o1, spec in ov if spec[0] == "chapter"] + [(ts(FT(PART[8]) - 0.5), "So is it real?")]
D = """IShowSpeed ran 10.35 in the 100 on Speed Goes Pro with Ato Boldon coaching him and Usain Bolt watching, and half the track world lost their mind. I've run 10.3 multiple times, so let me break down what actually happened: the 10.50 and the 10.35, why the timing gates matter (no gun, no reaction time), why "run it at a real meet" ain't the argument y'all think it is, and why track people should be giving Speed his flowers.

""" + "\n".join(f"{a} {b}" for a, b in ch) + """

So y'all tell me: is Speed's 10.35 real to you? Let me know in the comments.

Facts: Speed Goes Pro season 2, "I RACED USAIN BOLT!" (IShowSpeed, November 2026): run 1 10.50, run 2 10.352 on SmartSpeed timing gates, gate start, no wind reading. Gout Gout 19.67 (+1.7) at the Australian Championships, April 12, 2026, then 20.60 on June 10, 2026. Speed vs Noah Lyles 50 m, November 2024.

CLIPS (used for commentary and criticism)
- IShowSpeed, Speed Goes Pro: I RACED USAIN BOLT! https://youtu.be/PHSsdHu2Er0
- The Photo Finish https://youtu.be/ug4FBPWJpp4
- Coach Rob Track and Field https://youtu.be/jNoinOA1Yws
- Dylan Terryberry https://youtu.be/9TjSvZd31h8
- VALD Performance (SmartSpeed) https://youtu.be/PX3Cp4BMAYU
- Vic Pascoe, Gout Gout 19.67 from the stands https://youtu.be/9ksy5Sl1r2Q
- ABC News (Australia) https://youtu.be/DOXywv3QjFc
- Justin Gatlin, Ready Set Go https://youtu.be/jw65e1_0JBw
- Speedy Boykins: Speed vs Noah Lyles https://youtu.be/XnQho9Lj53w · Speed in Botswana https://youtu.be/buqm6z_aQqo
- IShowSpeed, Speed Goes Pro season 2 trailer https://youtu.be/uhMzbucFP88

#IShowSpeed #UsainBolt #TrackAndField #SpeedGoesPro #100m
"""
open("/home/user/YouTube-/projects/ishowspeed-10-35/description.txt", "w").write(D)
print("\n".join(f"{a} {b}" for a, b in ch)); print("end", ts(end))

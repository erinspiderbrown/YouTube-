"""Description for the final cut: chapters from the build timeline + clip credits."""
import sys
sys.argv = ["x"]
exec(open("/home/user/YouTube-/projects/shelby-houlihan/shelby_build.py").read().split("if __name__")[0])
shots, ov, end = TL()
def ts(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
ch = [("0:00", "In her own words")] + [(ts(o0), spec[2]) for o0, o1, spec in ov if spec[0] == "chapter"]
D = """Shelby Houlihan was the fastest American woman ever in the 1500 and the 5000. Then in June 2021 she was banned for 4 years after testing positive for nandrolone, and she said it came from a pork burrito bought at a food truck. The Court of Arbitration for Sport said her explanation was possible but unlikely and upheld the ban. She has always said she never doped. She came back in 2025 with a World Indoor silver, a US title and 4th at the World Championships. So do y'all believe the burrito?

""" + "\n".join(f"{a} {b}" for a, b in ch) + """

Do you believe the burrito, or nah? Let me know in the comments.

Her account vs the ruling: this video presents Shelby Houlihan's own explanation and the CAS decision. It does not claim she knowingly doped.

Facts: the 2021 CAS ruling as reported by Sports Illustrated, NPR, CBC and LetsRun; ESPN (Trials start list); World Athletics results (Nanjing, Tokyo); USATF; LetsRun; Skechers; Canadian Running; Wikipedia. Times and results as of November 2026.

CLIPS (used for commentary and criticism)
- KGW News https://youtu.be/TZZsF-Nmd5Q · https://youtu.be/m56PYZKQ30U · https://youtu.be/tC7caEJTM-w
- KREM 2 News https://youtu.be/iCBTON-3uJ8 · KOIN 6 https://youtu.be/h0jXhk30gCM · WHO 13 https://youtu.be/xxCfYiiBnys
- LetsRun https://youtu.be/wL40pPoy3T4 · https://youtu.be/yknzgioo1hU · https://youtu.be/3zQ9LwX-JV0 · https://youtu.be/KfRB8ty2C2U · https://youtu.be/2dtQnx9pFic · https://youtu.be/ozNT2nTyhEM
- Des Moines Register https://youtu.be/KvBX8fzHd_Y
- Alec Eagon, The Extra Year https://youtu.be/fRF_lh36Be4
- TRACK: All-Access https://youtu.be/ubHDGLJGK_s · Erik Boal Sports https://youtu.be/W66Uvo4LbhU
- Cameron Hanes, Lift. Run. Shoot. https://youtu.be/tCsvjrXIon8 · Troy Lynch https://youtu.be/yqXtUaLJbuA

#ShelbyHoulihan #BurritoBan #Doping #TrackAndField #Running #BowermanTrackClub
"""
open("/home/user/YouTube-/projects/shelby-houlihan/shelby_build.py").read().split("if __name__")[0])
shots, ov, end = TL()
def ts(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
ch = [("0:00", "In her own words")] + [(ts(o0), spec[2]) for o0, o1, spec in ov if spec[0] == "chapter"]
D = """Leo and Lex Young were the faces of Newbury Park, the team people called the greatest high school cross country team in American history. Leo ran 13:38 for 3 miles, Lex broke the national high school 5000 record in 13:34.96, and both went to Stanford with NIL deals. Yesterday at NCAA Cross Country nationals, Leo finished 117th and Lex 154th. So what happened to the Young twins?

""" + "\n".join(f"{a} {b}" for a, b in ch) + """

Did the Young twins fall off, or were they overhyped from day one? Let me know in the comments.

Facts: Stanford Athletics (gostanford.com), TFRRS, World Athletics, Track & Field News (Feb 2022), LetsRun, CITIUS MAG, Stanford Daily, KSL (Daniel Simmons record). NCAA XC places 2023-2026 from Stanford's own recaps.

CLIPS (used for commentary and criticism)
- L&L (Leo & Lex Young) https://youtu.be/RkPKK1KibMI · https://youtu.be/eXmdqlpJifY · https://youtu.be/7buSOhnvniQ · https://youtu.be/x3eviAm4RYQ · https://youtu.be/PJ3B-v_og3A · https://youtu.be/jJy-_WFhtrU · https://youtu.be/jPc0MjcfGH8 · https://youtu.be/HmZxHQU0LU8 · https://youtu.be/B65Tl-CW_qs
- PrepCalTrack / Rich Gonzalez https://youtu.be/-mq8eHgoujQ · https://youtu.be/jKmHHWDoU9c · https://youtu.be/6YmjdCKF8tc · https://youtu.be/TzsR5LPAfb0 · https://youtu.be/oLZZInqm4ts
- hdRunners https://youtu.be/xpMZ_dT8dME · https://youtu.be/5Gbw9NpX1Gg · https://youtu.be/p-rtS4PDQsc · https://youtu.be/MZMy1j3s7cY
- CITIUS MAG https://youtu.be/pT6lT65nEv0 · https://youtu.be/bUOJPE0CMjs · https://youtu.be/DzmiIRicoLk
- LetsRun https://youtu.be/c2-CaGPGzkk · RUNNING REPORT https://youtu.be/PbgA_h_TbuI · COFFEECLUB podcast https://youtu.be/IZuGJAQKe94
- Pali Project https://youtu.be/CRbNanOq8Dg · Trials of Miles Racing https://youtu.be/eGKhtk3XrWA

#LeoYoung #LexYoung #NicoYoung #NewburyPark #Stanford #NCAAXC #CrossCountry
"""
open("/home/user/YouTube-/projects/shelby-houlihan/description.txt", "w").write(D)
print("\n".join(f"{a} {b}" for a, b in ch)); print("end", ts(end))

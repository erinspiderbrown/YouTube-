"""IShowSpeed 10.35: soundbites + EDL (modern style, tools/modern.py). Voiceover = the user's own read (vo_clean.wav).
Footage: Speed's own channels (Speed Goes Pro S2 "I RACED USAIN BOLT!", Speedy Boykins), The Photo Finish, Coach Rob,
Dylan Terryberry, VALD Performance, Vic Pascoe (fan, from the stands), ABC News (AU), Ready Set Go (Gatlin), the user's own prediction clip.
No NBC/Peacock, Olympic, Diamond League, FloTrack/MileSplit, RunnerSpace, NCAA/ESPN broadcasts.
Avoid: speed_bolt_main Getty archive (50-60, 165-175, 288-310, 418-424, 838-866, 928-934) and the F-word at 1283.6 (soundbite audio ends 1283.3;
1283+ only as a muted shot); photofinish_lie 20-37, 75-120, 138-163 (broadcasts), so its gate explainer plays over Speed's own blocks footage;
coachrob_legit 300 s screenshot."""

TAGS = {
    "speed_bolt_main": "IShowSpeed · Speed Goes Pro · November 2026",
    "photofinish_lie": "The Photo Finish · November 2026",
    "coachrob_legit": "Coach Rob Track and Field · November 2026",
    "terryberry_legit": "Dylan Terryberry · November 2026",
    "vald_smartspeed": "VALD Performance · SmartSpeed gates",
    "gout_1967_fan": "Vic Pascoe (from the stands) · Australian Championships · April 2026",
    "gout_abc_news": "ABC News (Australia) · April 2026",
    "gatlin_rsg_gout": "Justin Gatlin · Ready Set Go · April 2026",
    "lyles_50m_speedy": "Speedy Boykins · Speed vs Noah Lyles · November 2024",
    "tebogo_race_speedy": "Speedy Boykins · Speed in Botswana · January 2026",
    "sgp_s2_trailer": "IShowSpeed · Speed Goes Pro season 2",
    "erin_prediction": "Erin Brown · my prediction",
}

# cold open: Speed's own words before the run
PRE_SB = ("speed_bolt_main", 0.6, 7.35, "IShowSpeed · Speed Goes Pro · November 2026")
R = {"raw": 1}
M = "speed_bolt_main"; PF = "photofinish_lie"; CR = "coachrob_legit"; TB = "terryberry_legit"; VA = "vald_smartspeed"
GF = "gout_1967_fan"; GA = "gout_abc_news"; GT = "gatlin_rsg_gout"; LY = "lyles_50m_speedy"; TE = "tebogo_race_speedy"
SG = "sgp_s2_trailer"; EB = "erin_prediction"

SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])  times word-checked against tx/*.json
    (("so let me explain", 2), EB, 57.85, 77.25, "Erin Brown · my prediction, before the race", R),
    (("this was on his", 2), M, 184.95, 191.0, "IShowSpeed · Speed Goes Pro · November 2026", R),
    (("so his first run", 2), M, 956.6, 964.7, "Usain Bolt to Speed · Speed Goes Pro · November 2026", R),
    (("he had a break", 2), M, 1189.6, 1201.5, "IShowSpeed after run 1 · Speed Goes Pro · November 2026", R),
    (("and you saying both if", 2), M, 1263.5, 1283.3, "Run 2 · Speed Goes Pro · November 2026", R),
    (("and listen to what", 2), M, 1406.4, 1418.3, "Usain Bolt · Speed Goes Pro · November 2026", R),
    (("he said speed really", 2), M, 565.75, 570.4, "Ato Boldon · Speed Goes Pro · November 2026", R),
    (("im gonna be fair", 3), TB, 19.95, 24.25, "Dylan Terryberry, pro miler · November 2026", R),
    (("people been saying", 3), PF, 150.6, 157.5, "The Photo Finish · November 2026",
     dict(raw=1, vsrc=M, vss=1131.0)),
    (("but i aint gonna hold", 3), PF, 265.0, 271.2, "The Photo Finish · November 2026", R),
    (("and thats what bothers", 4), CR, 573.9, 578.95, "Coach Rob Track and Field · November 2026", R),
    (("name the last time", 4), LY, 33.4, 37.0, "IShowSpeed after racing Noah Lyles · November 2024", R),
    (("and instead of saying", 4), CR, 628.3, 637.4, "Coach Rob Track and Field · November 2026", R),
    (("and honestly i feel", 4), M, 1213.4, 1216.0, "Usain Bolt · Speed Goes Pro · November 2026", R),
    (("official meet legal", 5), GF, 79.3, 88.8, "Stadium announcer · Vic Pascoe (from the stands) · April 2026", R),
    (("and it was fake", 5), GA, 26.45, 36.35, "Gout Gout · ABC News (Australia) · April 2026", R),
    (("so my point is", 5), GT, 76.7, 82.45, "Justin Gatlin · Ready Set Go · April 2026", R),
    (("now i think hes", 7), M, 1378.0, 1392.6, "IShowSpeed and Usain Bolt · Speed Goes Pro · November 2026",
     dict(raw=1, at=270.95)),   # silence 270.87-271.02, before "Now"
    (("both said he need", 7), M, 1434.4, 1438.7, "Usain Bolt · Speed Goes Pro · November 2026", R),
    (("im not gonna say", 7), CR, 664.0, 676.75, "Coach Rob Track and Field · November 2026", R),
    (("and i respect that", 7), EB, 91.4, 96.95, "Erin Brown · my prediction", R),
    (("so y all tell", 8), M, 1290.9, 1297.6, "IShowSpeed after run 2 · Speed Goes Pro · November 2026", R),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 open ---------------------------------------------------------------------------------------
    S(PART[1] - 0.05, M, 1275.0, flash=1)
    number(a("ran 10 35") + 0.1, 3.2, "10.35", "100 metres", "IShowSpeed · November 2026")
    S(a("and half the track"), PF, 182.0)
    S(a("everybody in the comments"), TB, 3.0)
    S(a("he aint really run"), PF, 197.0, bw=1)
    S(a("and ill be a thousand"), M, 1068.0)
    S(a("speak on it"), M, 762.0, slow=0.7)
    S(a("and i know what 10 3"), M, 1356.0)
    S(a("and from what i saw"), M, 1286.0, punch=0.5)
    S(a("something else"), M, 1365.0)
    # 2 the run -------------------------------------------------------------------------------------
    S(PART[2] - 0.05, M, 890.0, flash=1); chapter(PART[2] + 0.2, "01", "The Run")
    S(a("a lot of people talking"), M, 942.0)
    S(a("this was on his"), SG, 4.0); title(a("this was on his") + 0.2, 3.0, "Speed Goes Pro · Season 2", "The 100 metres")
    S(a("been training him since"), M, 332.0); name(a("been training him since"), 3.0, "Ato Boldon", "4-time Olympic medallist · Speed's coach")
    S(a("was right there watching"), M, 912.0); name(a("was right there watching"), 2.8, "Usain Bolt", "100m world record holder")
    S(a("so his first run"), M, 1131.5)
    S(a("he went out there"), M, 1138.6)
    S(a("speed ran 10 5"), M, 1155.3, punch=0.4)
    S(a("he had a break"), M, 1062.0)
    S(a("and for his second run"), M, 1257.0)
    S(a("went out and he ran"), M, 1243.5)
    S(a("and you saying both if"), M, 1283.0)
    S(a("fastest man of all"), M, 1000.0); number(a("fastest man of all"), 2.8, "9.58", "100m world record", "Usain Bolt · 2009")
    S(a("and he said he was"), M, 1400.0)
    S(a("and said man to run"), M, 1385.0)
    O(a("by yourself is no") - 0.6, 4.2, ("board", "Speed Goes Pro · SmartSpeed gates", [("Run 1", "10.50", "", 0), ("Run 2", "10.35", "10.352", 1)], "Timed by gates · no gun · no wind reading"))
    S(a("and listen to what"), M, 312.0)
    S(a("he said speed really"), M, 240.0); number(a("70") - 0.2, 2.8, "70%", "Natural speed", "Ato Boldon's estimate")
    S(a("the technique"), M, 500.0)
    S(a("and thats exactly what"), M, 552.0)
    # 3 the gates -----------------------------------------------------------------------------------
    S(PART[3] - 0.05, PF, 183.0, flash=1); chapter(PART[3] + 0.2, "02", "The Gates")
    S(a("im gonna be fair"), VA, 4.0)
    S(a("it wasnt a gun start"), VA, 14.0); title(a("it wasnt a gun start") + 0.2, 3.4, "Timing gates", "The clock starts when he breaks the beam")
    S(a("not when the gun"), M, 1139.0)
    S(a("there is no reaction"), VA, 22.0)
    S(a("people been saying"), PF, 197.0); number(a("10 7 10 8") - 0.2, 3.0, "10.7", "With a gun?", "What the doubters say: 10.7–10.8")
    S(a("but i aint gonna hold"), M, 253.0, punch=0.6)
    S(a("understand what that"), M, 782.0)
    S(a("im a guy who"), M, 722.0)
    S(a("the fastest i probably"), M, 682.0)
    S(a("so for him to be"), M, 1140.0)
    S(a("this guy can literally"), M, 1357.0, punch=0.5)
    # 4 the attention -------------------------------------------------------------------------------
    S(PART[4] - 0.05, M, 1428.0, flash=1); chapter(PART[4] + 0.2, "03", "The Attention")
    S(a("speed is bringing"), TE, 1.0)
    S(a("about this sport that"), TE, 6.0)
    S(a("he got over"), LY, 9.0); number(a("he got over"), 3.0, "50 m", "Speed vs Noah Lyles", "November 2024")
    S(a("millions of people watch"), LY, 11.5)
    S(a("name the last time"), GF, 26.0)
    S(a("and instead of saying"), PF, 182.0, bw=1)
    S(a("these internet coaches"), PF, 200.0, bw=1)
    S(a("in the comments talking"), PF, 166.0, bw=1)
    S(a("and honestly i feel"), M, 1287.0, slow=0.6)
    S(a("is he got people"), TE, 12.0)
    # 5 real meets ----------------------------------------------------------------------------------
    S(PART[5] - 0.05, TB, 20.0, flash=1); chapter(PART[5] + 0.2, "04", "Real Meets")
    S(a("this was the dumbest"), M, 1368.0)
    S(a("about real meets"), GF, 2.0)
    S(a("gout gout from"), GF, 8.0); name(a("gout gout from") + 0.2, 2.8, "Gout Gout", "Australian sprinter")
    date(a("championships last year") , 2.8, "April 12, 2026", "Australian Championships · Sydney")
    S(a("and ran 1967"), GF, 14.0); number(a("and ran 1967") + 0.2, 3.2, "19.67", "200 metres", "Wind +1.7 · legal")
    S(a("official meet legal"), GF, 110.0)
    S(a("and it was fake"), GF, 97.0, bw=1)
    S(a("and then his very"), GF, 60.0, bw=1, slow=0.7)
    number(a("whole second slower") + 0.2, 3.0, "20.60", "His next 200", "June 10, 2026")
    S(a("so my point is"), GA, 60.0)
    S(a("so stop acting"), M, 1360.0)
    S(a("want to doubt it"), PF, 201.0, bw=1)
    # 6 crabs in a bucket ---------------------------------------------------------------------------
    S(PART[6] - 0.05, M, 1430.0, flash=1); chapter(PART[6] + 0.2, "05", "Crabs In A Bucket")
    S(a("nobody care about"), M, 906.0)
    S(a("the meats be empty"), M, 900.0, slow=0.7)
    S(a("then somebody come"), TE, 2.0)
    S(a("and then the first thing"), PF, 184.0, bw=1)
    S(a("he aint fast"), TB, 22.0, bw=1)
    S(a("crabs in a bucket"), M, 1153.0, bw=1)
    S(a("full of crabs"), M, 1198.0, bw=1)
    S(a("reason the sport"), M, 1432.0, slow=0.6)
    # 7 his flowers ---------------------------------------------------------------------------------
    S(PART[7] - 0.05, M, 1376.0, flash=1); chapter(PART[7] + 0.2, "06", "His Flowers")
    S(a("now i think hes"), M, 1394.0)
    S(a("both said he need"), M, 742.0); number(a("five more years") - 0.3, 2.8, "5", "More years", "Usain Bolt's timeline")
    S(a("im not gonna say"), M, 1064.0)
    S(a("i think he could make"), M, 684.0)
    S(a("but he has money"), M, 880.0); title(a("citizenship by investment") - 0.3, 3.2, "Citizenship by investment", "Run for another country")
    S(a("olympic team so yes"), M, 1288.0); date(a("in 2028") , 2.6, "2028", "Los Angeles")
    S(a("and i respect that"), M, 1404.0)
    S(a("deserve his flowers"), TE, 14.0)
    S(a("putting on for black"), M, 1090.0)
    S(a("and of course the"), PF, 198.0, bw=1)
    S(a("push bro out"), M, 1154.0, bw=1)
    # 8 close ---------------------------------------------------------------------------------------
    S(PART[8] - 0.05, M, 1355.5, slow=0.6, flash=1)
    number(a("speed 1035") + 0.1, 3.0, "10.35", "Real to you?", "")
    S(a("keep on hating"), M, 1440.0)
    S(a("would you rather"), M, 1426.0, slow=0.6)
    S(a("let me know"), M, 1364.0, slow=0.7)

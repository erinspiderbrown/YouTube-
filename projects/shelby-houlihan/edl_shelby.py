"""Shelby Houlihan: soundbites + EDL (modern style, tools/modern.py incl. 'board').
Footage: local news (KGW, KREM, KOIN, WHO 13), LetsRun, Des Moines Register, Alec Eagon "The Extra Year", TRACK: All-Access,
Erik Boal Sports, Cameron Hanes, Troy Lynch (fan). No NCAA/ESPN, FloTrack/MileSplit, RunnerSpace, NBC, Olympic, Diamond League, World Athletics.
Avoid: koin_burrito 84-115 s (NBC-bugged race), who13_trials 0-24 s (TV race), kgw_2022_interview 15-45 s (Valieva) and 92-108 s,
hanes profanity (404-408, 529-533, 619-624, 799-802 s). Soundbite times are word-checked against tx/*.json; all raw."""

TAGS = {
    "kgw_burrito_2021": "KGW News · June 2021", "krem_ban": "KREM 2 News · June 2021", "kgw_cas_upheld": "KGW News · September 2021",
    "koin_burrito": "KOIN 6 News · June 2021", "who13_trials": "WHO 13 News · June 2021", "kgw_2022_interview": "KGW News · 2022",
    "letsrun_burrito": "LetsRun · March 2025", "letsrun_schumacher": "Jerry Schumacher · LetsRun · June 2021",
    "letsrun_first_team": "LetsRun · February 2025", "letsrun_2026_season": "LetsRun · July 2026", "letsrun_ultimate_last": "LetsRun · September 2026",
    "letsrun_2019_champ": "LetsRun · July 2019", "dmreg_5000_2019": "Des Moines Register · July 2019",
    "eagon_extra_year": "Alec Eagon · The Extra Year · 2021", "trackallaccess_workout": "TRACK: All-Access · January 2025",
    "boal_the_ten_2026": "Erik Boal Sports · March 2026", "troylynch_asu_2015": "Arizona State, 2015 · Troy Lynch",
    "hanes_lift_run_shoot": "Cameron Hanes · Lift. Run. Shoot. · 2025",
}

# cold open: her June 2021 statement video
PRE_SB = ("krem_ban", 0.75, 7.31, "Shelby Houlihan's statement · KREM 2 News · June 2021")
R = {"raw": 1}
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("in 2016 she made", 2), "eagon_extra_year", 323.77, 332.03, "Shelby on Jerry Schumacher · Alec Eagon, The Extra Year · 2021", R),
    (("then at the world championships in doha", 3), "letsrun_2019_champ", 201.36, 217.74, "Shelby Houlihan, US champion · LetsRun · July 2019", R),
    (("then in july 2020", 3), "eagon_extra_year", 376.93, 379.1, "Shelby Houlihan · Alec Eagon, The Extra Year · 2021", R),
    (("she said she ordered", 4), "kgw_burrito_2021", 59.58, 82.08, "Shelby Houlihan's statement · KGW News · June 2021", R),
    (("now the court of arbitration", 6), "letsrun_schumacher", 326.34, 347.08, "Jerry Schumacher, Bowerman Track Club · LetsRun · June 2021", R),
    (("but they said the burrito", 6), "krem_ban", 36.35, 54.17, "Shelby Houlihan's statement · KREM 2 News · June 2021", R),
    (("and she couldnt prove", 6), "kgw_cas_upheld", 80.62, 95.5, "KGW News on the CAS ruling · September 2021", R),
    (("she went to the swiss court", 6), "who13_trials", 3.98, 9.44, "WHO 13 News · June 2021", R),
    (("so she missed tokyo", 6), "kgw_cas_upheld", 128.98, 134.82, "KGW News · September 2021", R),
    (("and it aint just the races", 6), "letsrun_schumacher", 365.24, 371.88, "Jerry Schumacher · LetsRun · June 2021", R),
    (("then she went to world indoors", 7), "letsrun_first_team", 77.36, 81.76, "Shelby's first race with a team after the ban · LetsRun · February 2025", R),
    (("then she won the us title", 7), "hanes_lift_run_shoot", 41.49, 59.3, "Shelby on her World Indoor silver · Cameron Hanes · 2025", R),
    (("this year been up and down", 8), "letsrun_2026_season", 298.66, 306.42, "Shelby on brands, still unsponsored · LetsRun · July 2026", R),
    (("and that put her 10th", 8), "boal_the_ten_2026", 71.6, 76.2, "Shelby after her first 10,000 · Erik Boal Sports · March 2026", R),
    (("and that same month", 8), "letsrun_ultimate_last", 3.08, 22.36, "Shelby after World Ultimate · LetsRun · September 2026", R),
    (("i aint gonna hold you", 9), "letsrun_burrito", 3.46, 17.04, "Shelby Houlihan · LetsRun · March 2025", R),
    (("honestly i dont know", 9), "letsrun_2026_season", 315.22, 323.34, "Shelby Houlihan · LetsRun · July 2026", R),
    (("so y all tell me", 9), "hanes_lift_run_shoot", 625.02, 627.3, "Shelby Houlihan · Cameron Hanes · 2025", R),
]

KB = "kgw_burrito_2021"; KR = "krem_ban"; KC = "kgw_cas_upheld"; KO = "koin_burrito"; WHO = "who13_trials"; K22 = "kgw_2022_interview"
LB = "letsrun_burrito"; JS = "letsrun_schumacher"; FT_ = "letsrun_first_team"; L26 = "letsrun_2026_season"; ULT = "letsrun_ultimate_last"
L19 = "letsrun_2019_champ"; DM = "dmreg_5000_2019"; EA = "eagon_extra_year"; TA = "trackallaccess_workout"; BO = "boal_the_ten_2026"
ASU = "troylynch_asu_2015"; HA = "hanes_lift_run_shoot"

TIMELINE = [("Dec 2020", "Positive test", "nandrolone", 0), ("Jun 2021", "Ban announced", "4 years", 1), ("Jun 2021", "Pulled from Olympic Trials", "", 0),
            ("2021", "CAS upholds the ban", "", 0), ("2022", "Swiss court appeal", "lost", 0), ("Jan 2025", "Ban ends", "missed Tokyo + Paris", 1)]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open --------------------------------------------------------------------------------
    S(PART[1] - 0.05, KB, 24.0, flash=1)
    S(a("but before all that"), L19, 30.0); name(a("shelby houlihan was") + 0.2, 3.0, "Shelby Houlihan", "Bowerman Track Club")
    S(a("not one of the fastest"), EA, 760.0, slow=0.6)
    O(a("the fastest woman america") - 0.1, 5.0, ("board", "American records · Shelby Houlihan", [("1500m", "3:54.99", "2019", 1), ("5000m", "14:23.92", "2020", 1)], "Both still hers"))
    S(a("then one day"), KR, 22.0); number(a("banned 4 years") + 0.2, 2.6, "4", "Year ban", "Nandrolone · June 2021")
    S(a("and her explanation"), KB, 100.0)
    S(a("so did a burrito"), KC, 78.0)
    S(a("or is it something"), K22, 47.0, bw=1)
    S(a("cause i really feel"), EA, 30.0)
    # 2 who she is --------------------------------------------------------------------------------
    S(PART[2] - 0.05, ASU, 20.0, flash=1); chapter(PART[2] + 0.2, "01", "The Burrito Girl")
    S(a("she went to arizona state"), ASU, 45.0)
    S(a("in 2014"), ASU, 82.0); date(a("in 2014"), 2.8, "2014", "NCAA 1500m champion · Arizona State")
    S(a("after college"), EA, 58.0); name(a("jerry schumacher") , 2.8, "Jerry Schumacher", "Coach · Bowerman Track Club")
    S(a("one of the best pro"), EA, 233.0)
    S(a("in 2016 she made"), K22, 50.0); number(a("finished 11th") , 2.6, "11th", "5000m final · Rio 2016", "")
    S(a("on paper"), EA, 120.0)
    # 3 the rise ----------------------------------------------------------------------------------
    S(PART[3] - 0.05, KB, 24.0, flash=1); chapter(PART[3] + 0.2, "02", "The Fastest Ever")
    S(a("in 2018 she broke"), K22, 62.0); number(a("in 2018 she broke") + 0.3, 2.8, "14:34.45", "5000m American record", "2018")
    S(a("in 2019 she won both"), DM, 30.0); title(a("in 2019 she won both"), 3.0, "2019", "US champion · 1500m and 5000m")
    S(a("at usas"), L19, 60.0)
    S(a("then at the world championships in doha"), K22, 78.0)
    S(a("354"), KO, 50.0, punch=0.2); number(a("354"), 3.2, "3:54.99", "1500m American record", "4th · World Championships, Doha 2019")
    S(a("and finished 4th"), DM, 100.0)
    S(a("then in july 2020"), EA, 760.0); date(a("then in july 2020"), 2.8, "July 2020", "Bowerman time trial · Portland")
    S(a("she ran 1423"), WHO, 38.0, punch=0.3); number(a("she ran 1423") + 0.3, 3.2, "14:23.92", "5000m American record", "Broke her own record by ~10 s")
    S(a("and broke her own"), WHO, 48.0)
    S(a("she had a kick"), EA, 870.0)
    S(a("going into tokyo"), L19, 40.0)
    # 4 the ban -----------------------------------------------------------------------------------
    S(PART[4] - 0.05, KR, 24.0, flash=1, bw=1); chapter(PART[4] + 0.2, "03", "The Ban")
    S(a("then june of 2021"), KR, 30.0, bw=1); date(a("then june of 2021"), 2.8, "June 14, 2021", "Days before the Olympic Trials")
    S(a("shelby go on instagram"), KB, 36.0)
    S(a("she said back in december"), KR, 50.0); title(a("she said back in december"), 3.0, "December 15, 2020", "Out-of-competition test · nandrolone")
    S(a("and her explanation was"), KB, 140.0)
    S(a("she ate a burrito"), KC, 10.0)
    S(a("she said she ordered"), KC, 38.0)
    S(a("but they gave her pork"), KB, 95.0)
    S(a("and she said pig"), KB, 112.0)
    # 5 Schumacher -------------------------------------------------------------------------------
    S(PART[5] - 0.05, EA, 58.0, flash=1)
    S(a("jerry schumacher got"), JS, 300.0); name(a("jerry schumacher got") + 0.2, 2.8, "Jerry Schumacher", "Bowerman Track Club · June 2021")
    # 6 the ruling --------------------------------------------------------------------------------
    S(PART[6] - 0.05, KC, 76.0, flash=1); chapter(PART[6] + 0.2, "04", "The Ruling")
    S(a("the people that decide"), KC, 84.0)
    S(a("they actually said"), KB, 60.0)
    S(a("but they said the burrito"), KC, 100.0); quote(a("possible but unlikely") - 0.4, 3.4, "Possible, but unlikely.", "Court of Arbitration for Sport")
    S(a("and she couldnt prove"), K22, 66.0, bw=1)
    S(a("so the 4 years stood"), KC, 120.0, bw=1)
    S(a("usatf tried"), WHO, 34.0)
    S(a("but world athletics"), KO, 60.0, bw=1)
    S(a("she went to the swiss court"), K22, 80.0, bw=1)
    S(a("so she missed tokyo"), EA, 875.0, bw=1)
    O(a("so she missed tokyo") - 0.1, 9.0, ("board", "The case", TIMELINE, "Her account vs the ruling"))
    S(a("and it aint just the races"), EA, 233.0)
    S(a("she lost her nike"), K22, 80.0, bw=1)
    S(a("one of her own"), EA, 878.0); name(a("gabriella") + 0.1, 2.8, "Gabriela DeBues-Stafford", "Left Bowerman Track Club · 2021")
    S(a("so you got people"), EA, 300.0)
    # 7 the comeback ------------------------------------------------------------------------------
    S(PART[7] - 0.05, TA, 88.0, flash=1); chapter(PART[7] + 0.2, "05", "The Revenge Tour")
    S(a("her ban finally ended"), TA, 0.0); date(a("her ban finally ended"), 2.8, "January 2025", "Ban over")
    S(a("first race back"), TA, 340.0); number(a("she ran 8") + 0.3, 3.0, "8:31.56", "3000m · Razorback Invitational", "First race back · 2025")
    S(a("then she went to world indoors"), FT_, 20.0)
    S(a("and got a silver"), HA, 105.0); number(a("and got a silver") + 0.2, 2.8, "Silver", "3000m · World Indoors, Nanjing 2025", "")
    S(a("then she won the us title"), TA, 700.0); title(a("then she won the us title") , 2.8, "2025", "US 5000m champion")
    S(a("and at the world championships in tokyo"), TA, 880.0); number(a("ended up 4th") + 0.2, 3.0, "4th", "5000m · World Championships, Tokyo 2025", "~2 seconds from a medal")
    S(a("she called it"), HA, 460.0)
    S(a("and still no shoe"), HA, 560.0, bw=1)
    # 8 this year ---------------------------------------------------------------------------------
    S(PART[8] - 0.05, BO, 10.0, flash=1); chapter(PART[8] + 0.2, "06", "Up And Down")
    S(a("she ran her first ever"), BO, 40.0); number(a("and won it in 30") + 0.2, 3.0, "30:50.10", "10,000m · The TEN · March 2026", "#10 on the US all-time list")
    S(a("she was 2nd at usas"), L26, 20.0); title(a("she was 2nd at usas"), 2.8, "July 2026", "2nd · US 5000m")
    S(a("then in september"), ULT, 30.0, bw=1); title(a("then in september"), 3.0, "September 2026", "Last · World Ultimate Championships")
    S(a("she finished last"), ULT, 60.0, bw=1)
    S(a("and that same month"), L26, 60.0); title(a("skechers finally") , 2.8, "September 2026", "Signs with Skechers")
    S(a("she 33 now"), TA, 1330.0)
    # 9 the verdict -------------------------------------------------------------------------------
    S(PART[9] - 0.05, LB, 30.0, flash=1); chapter(PART[9] + 0.2, "07", "Do You Believe It?")
    S(a("i ll go back and forth"), EA, 570.0)
    S(a("on paper she did"), TA, 1000.0)
    S(a("she running fast"), BO, 90.0)
    S(a("some people see that"), HA, 105.0)
    S(a("other people say"), KC, 100.0, bw=1)
    S(a("and they aint never"), KB, 24.0, bw=1)
    S(a("honestly i dont know"), L26, 100.0)
    S(a("what i do know"), EA, 760.0, slow=0.6)
    S(a("and she still came back"), TA, 1260.0)
    S(a("so y all tell me"), HA, 785.0)
    S(a("do y all believe"), KB, 24.0, slow=0.7)

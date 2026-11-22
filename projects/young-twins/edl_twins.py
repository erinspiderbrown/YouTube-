"""Leo & Lex Young: soundbites + EDL (modern style, tools/modern.py incl. 'board').
Footage: the twins' own L&L vlogs, fan/independent cameras (hdRunners, Pali Project, Trials of Miles), PrepCalTrack (Rich Gonzalez)
interviews, CITIUS, LetsRun, RUNNING REPORT, COFFEECLUB. No NCAA/ESPN broadcast, FloTrack/MileSplit, RunnerSpace, NBC, Olympic.
Rules: no injury talk. Soundbite times are word-checked (scratchpad/twins_scripts/refine_out.txt); all marked raw."""

TAGS = {
    "woodbridge21_ll_vlog": "Woodbridge Classic 2021 · L&L", "woodbridge21_pali_finish": "Woodbridge Classic 2021 · Pali Project",
    "woodbridge21_leo_int": "Leo Young · PrepCalTrack (Rich Gonzalez) · 2021", "brosnan_woodbridge21_int": "Sean Brosnan · PrepCalTrack · 2021",
    "altitude_camp21_hdrunners": "Newbury Park, Big Bear camp 2021 · hdRunners", "nico_advice21_hdrunners": "Nico Young · hdRunners · 2021",
    "runninglane21_ll_vlog": "RunningLane XC Nationals 2021 · L&L", "nxn22_ll_vlog": "Nike Cross Nationals 2022 · L&L",
    "nxn22_hdrunners": "Nike Cross Nationals 2022 · hdRunners", "tanya_nxn22_int": "PrepCalTrack (Rich Gonzalez) · NXN 2022",
    "cifss22_twins_int": "PrepCalTrack (Rich Gonzalez) · CIF-SS 2022", "state22_lex_int": "Lex Young · PrepCalTrack · CIF State 2022",
    "commit_stanford_ll": "Leo & Lex Young · L&L · 2022", "lagp23_ll_vlog": "USATF LA Grand Prix 2023 · L&L",
    "lagp23_citius_lex_int": "Lex Young · CITIUS MAG · May 2023", "runningreport23_twins_stanford": "Leo & Lex Young · RUNNING REPORT · June 2023",
    "citius23_lex_ncaaxc": "Lex Young · CITIUS MAG · NCAA XC 2023", "letsrun23_lex_freshman": "Lex Young · LetsRun · NCAA XC 2023",
    "ncaa_qualify23_ll_vlog": "Stanford · West Regional 2023 · L&L", "coffeeclub24_cut": "COFFEECLUB podcast · 2024",
    "mcnichols26_ll_vlog": "Stanford · Terre Haute, September 2026 · L&L", "nuttycombe26_ll_vlog": "Stanford · Nuttycombe 2026 · L&L",
    "nico_double_ll": "Nico, Leo & Lex Young · L&L · 2021", "trialsofmiles_state22_sweep": "CIF State 2022 · Trials of Miles",
    "wcc23_leo_hdrunners": "World Cross Country 2023 · hdRunners", "clovis21_twins_int": "PrepCalTrack (Rich Gonzalez) · Clovis 2021",
    "brosnan_citius22_int": "Sean Brosnan · CITIUS MAG · 2022",
}

# cold open: their high school coach, the night Leo ran 13:38
PRE_SB = ("brosnan_woodbridge21_int", 271.65, 274.8, "Sean Brosnan, Newbury Park coach · PrepCalTrack · September 2021")
R = {"raw": 1}
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("the twins grew up", 2), "woodbridge21_leo_int", 237.8, 243.6, "Leo Young on Nico · PrepCalTrack · September 2021", R),
    (("and newberry park wasnt just good", 2), "nico_advice21_hdrunners", 36.3, 39.95, "Nico Young · hdRunners · November 2021", R),
    (("they was winning young", 3), "altitude_camp21_hdrunners", 579.9, 593.2, "Newbury Park runner · hdRunners · 2021", R),
    (("so they senior year", 3), "tanya_nxn22_int", 233.2, 242.0, "PrepCalTrack (Rich Gonzalez) · Nike Cross Nationals 2022", R),
    (("and by their self", 4), "nxn22_ll_vlog", 545.9, 549.8, "Leo Young after NXN 2022 · L&L", R),
    (("at running lane nationals", 4), "woodbridge21_ll_vlog", 553.9, 565.45, "Leo Young on his 13:38 · L&L · 2021", R),
    (("leo ran 339", 4), "lagp23_citius_lex_int", 1.0, 7.86, "Lex Young, high school record holder · CITIUS MAG · May 2023", R),
    (("so on paper", 4), "cifss22_twins_int", 68.0, 78.5, "PrepCalTrack (Rich Gonzalez) · CIF-SS 2022", R),
    (("they was famous before", 5), "cifss22_twins_int", 96.4, 107.85, "Lex Young · PrepCalTrack · CIF-SS 2022", R),
    (("i aint gonna hold you", 6), "commit_stanford_ll", 421.6, 437.7, "Leo & Lex Young commit to Stanford · L&L · 2022", R),
    (("but look at the numbers", 6), "commit_stanford_ll", 560.3, 564.5, "Leo & Lex Young · L&L · 2022", R),
    (("fall of 2023", 6), "runningreport23_twins_stanford", 193.4, 201.6, "Before Stanford · RUNNING REPORT · June 2023", R),
    (("2024 leo 92nd", 6), "letsrun23_lex_freshman", 148.95, 153.55, "Lex Young after his first NCAA XC · LetsRun · November 2023", R),
    (("then yesterday leo", 6), "nuttycombe26_ll_vlog", 0.0, 3.45, "Leo Young before NCAA XC 2026 · L&L · October 2026", R),
    (("three years at stanford", 7), "citius23_lex_ncaaxc", 0.0, 7.5, "Lex Young · CITIUS MAG · November 2023", R),
    (("and it aint just them", 8), "mcnichols26_ll_vlog", 407.7, 428.5, "Leo Young · L&L · September 2026", R),
    (("so the record that made", 9), "state22_lex_int", 265.95, 273.3, "Lex Young, CIF State champion · PrepCalTrack · 2022", R),
    (("so you gotta ask", 11), "coffeeclub24_cut", 162.8, 181.95, "Leo & Lex Young · COFFEECLUB podcast · 2024",
     {"raw": 1, "vsrc": "ncaa_qualify23_ll_vlog", "vss": 400.0, "quote": "There's a pressure to do really well… you don't really know what to expect.", "who": "The Young twins on college · 2024"}),
    (("and look at they brother", 11), "nico_advice21_hdrunners", 49.3, 55.95, "Nico Young · hdRunners · November 2021", R),
]

WB = "woodbridge21_ll_vlog"; PALI = "woodbridge21_pali_finish"; RL = "runninglane21_ll_vlog"; LG = "lagp23_ll_vlog"
NX = "nxn22_ll_vlog"; NH = "nxn22_hdrunners"; CAMP = "altitude_camp21_hdrunners"; ND = "nico_double_ll"; NA = "nico_advice21_hdrunners"
CM = "commit_stanford_ll"; Q23 = "ncaa_qualify23_ll_vlog"; MC = "mcnichols26_ll_vlog"; NU = "nuttycombe26_ll_vlog"
ST = "trialsofmiles_state22_sweep"; WC = "wcc23_leo_hdrunners"

NCAA_ROWS = [("2023", "Leo 185th", "Lex 74th", 0), ("2024", "Leo 92nd", "Lex 63rd", 0),
             ("2025", "Leo 72nd", "Lex did not race", 0), ("2026", "Leo 117th", "Lex 154th", 1)]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open: yesterday -----------------------------------------------------------------
    S(PART[1] - 0.05, MC, 280.0, flash=1); date(a("yesterday at ncaa"), 3.0, "Saturday, November 21, 2026", "NCAA Cross Country · Terre Haute, Indiana")
    S(a("leo young finished"), MC, 300.0); number(a("leo young finished") + 0.3, 2.8, "117th", "Leo Young · NCAA XC 2026", "Stanford")
    S(a("his twin brother lex"), MC, 318.0, bw=1); number(a("his twin brother lex") + 0.4, 2.8, "154th", "Lex Young · NCAA XC 2026", "Stanford")
    S(a("and if you was following"), WB, 200.0)
    S(a("a few years ago"), PALI, 4.0)
    S(a("cause these two"), RL, 560.0)
    S(a("next big thing"), LG, 900.0)
    S(a("so what happened"), MC, 340.0, bw=1)
    # 2 who they are -----------------------------------------------------------------------------
    S(PART[2] - 0.05, ND, 20.0, flash=1); chapter(PART[2] + 0.2, "01", "Nico's Little Brothers")
    S(a("leo and lex is"), ND, 60.0); name(a("leo and lex is") + 0.2, 3.0, "Leo & Lex Young", "Twins · Camarillo, California")
    S(a("nico the olympian"), NA, 15.0); name(a("nico the olympian") + 0.2, 2.6, "Nico Young", "Northern Arizona · 2024 Olympian")
    S(a("the twins grew up"), ND, 120.0)
    S(a("they ended up"), CAMP, 40.0)
    S(a("in california"), CAMP, 120.0)
    S(a("and newberry park wasnt"), CAMP, 200.0)
    S(a("track and field news"), CAMP, 260.0); quote(a("track and field news") + 0.2, 4.6, "The greatest prep cross country team in American history.", "Track & Field News · February 2022")
    S(a("four state titles"), ST, 0.0); number(a("four state titles"), 2.6, "4", "California state XC titles", "Newbury Park")
    S(a("a nike cross nationals"), NH, 60.0)
    S(a("and the twins was right"), NH, 120.0)
    # 3 winning young / coach leaves -------------------------------------------------------------
    S(PART[3] - 0.05, CAMP, 300.0, flash=1); chapter(PART[3] + 0.2, "02", "The Greatest Team Ever")
    S(a("back in 2019"), CAMP, 340.0); date(a("back in 2019"), 2.8, "December 2019", "Nike Cross Nationals · Leo, the only freshman")
    S(a("and nico was the one"), NA, 70.0)
    S(a("so from 14"), CAMP, 380.0)
    S(a("then right before"), CAMP, 440.0)
    S(a("sean brosnan"), "brosnan_woodbridge21_int", 30.0); name(a("sean brosnan") + 0.2, 2.8, "Sean Brosnan", "Left Newbury Park for UCLA · August 2022")
    S(a("left for ucla"), "brosnan_citius22_int", 40.0)
    S(a("so they senior year"), NH, 30.0)
    S(a("without the coach"), NX, 300.0)
    # 4 the marks --------------------------------------------------------------------------------
    S(PART[4] - 0.05, NX, 455.0, flash=1, bw=1)
    S(a("leo ran 1338"), WB, 220.0); number(a("leo ran 1338") + 0.3, 3.4, "13:38", "3 miles · Woodbridge 2021", "Fastest high school time ever")
    S(a("the fastest high school"), PALI, 6.0, slow=0.6)
    S(a("at running lane nationals"), RL, 590.0); number(a("leo ran 1405") , 3.0, "14:05", "5K · RunningLane XC Nationals 2021", "Leo 14:05.07 · Lex 14:05.49")
    S(a("and lex ran 1405"), RL, 620.0)
    S(a("then in 2023"), LG, 520.0); date(a("then in 2023"), 2.6, "May 26, 2023", "USATF LA Grand Prix")
    S(a("lex broke the national"), LG, 760.0)
    S(a("1334"), LG, 990.0, punch=0.2); number(a("1334"), 3.2, "13:34.96", "5000m · Lex Young", "National high school record")
    S(a("leo ran 339"), LG, 1010.0); number(a("leo ran 339") + 0.2, 2.6, "3:39.39", "1500m · Leo Young", "High school")
    S(a("stanford signed"), CM, 188.0)
    S(a("a freshman year"), CM, 300.0); title(a("a freshman year"), 3.0, "November 2023", "Both sign NIL deals with On")
    S(a("so on paper"), Q23, 100.0)
    # 5 famous before college ---------------------------------------------------------------------
    S(PART[5] - 0.05, WC, 0.0, flash=1)
    S(a("in january of 2023"), WC, 4.0); date(a("in january of 2023"), 2.8, "January 2023", "USATF U20 XC champion · Leo Young")
    S(a("then he went to the world"), WC, 8.0); number(a("finished 16th"), 3.0, "16th", "U20 World Cross Country · Bathurst 2023", "Top non-East African · USA bronze")
    S(a("and the us team"), NH, 150.0)
    S(a("lex got pac"), Q23, 120.0); title(a("lex got pac"), 3.0, "2023", "Lex Young · Pac-12 Freshman of the Year")
    S(a("and on top of that"), ND, 160.0)
    S(a("over 100"), CM, 60.0); number(a("over 100"), 2.6, "100K+", "Instagram followers", "Plus their own YouTube channel")
    S(a("everybody knew"), CM, 120.0)
    # 6 the numbers --------------------------------------------------------------------------------
    S(PART[6] - 0.05, Q23, 590.0, flash=1); chapter(PART[6] + 0.2, "03", "The Stanford Years")
    S(a("when they got to stanford"), Q23, 130.0)
    S(a("but look at the numbers"), Q23, 600.0, blur=1)
    S(a("fall of 2023"), Q23, 610.0, blur=1); O(a("fall of 2023") - 0.2, 21.0, ("board", "NCAA Cross Country · Leo & Lex Young", NCAA_ROWS, "No All-Americans"))
    S(a("2025 leo 72nd"), Q23, 630.0, blur=1)
    S(a("then yesterday leo"), MC, 290.0, blur=1)
    S(a("thats four years"), MC, 330.0, bw=1); number(a("thats four years") + 0.4, 3.4, "0", "All-Americans", "Cross country or track · 2023–2026")
    S(a("not in cross country"), NU, 450.0, bw=1)
    # 7 Lex ------------------------------------------------------------------------------------------
    S(PART[7] - 0.05, LG, 1020.0, flash=1); chapter(PART[7] + 0.2, "04", "Lex")
    S(a("he ran 1334"), LG, 1030.0); O(a("he ran 1334"), 7.0, ("board", "Lex Young · 5000m", [("2023", "High school", "13:34.96", 1), ("2025", "Best at Stanford", "13:35.52", 0)], "Slower in college"))
    S(a("his best 5000"), Q23, 640.0, bw=1)
    S(a("three years at stanford"), "citius23_lex_ncaaxc", 30.0)
    S(a("then he missed"), Q23, 660.0, bw=1)
    S(a("and stanford aint never"), MC, 360.0, bw=1)
    # 8 Stanford as a team ----------------------------------------------------------------------------
    S(PART[8] - 0.05, MC, 290.0, flash=1)
    S(a("stanford as a team"), NU, 425.0); number(a("31 years"), 3.0, "31", "Straight NCAA XC team appearances", "Ended in 2025")
    S(a("and in 2025"), Q23, 600.0, bw=1)
    S(a("this year they made it back"), MC, 300.0); number(a("finished 17th"), 2.6, "17th", "Stanford men · NCAA XC 2026", "")
    S(a("so the whole program"), NU, 440.0)
    S(a("when you got two"), MC, 320.0)
    S(a("people gonna start"), NU, 470.0, bw=1)
    # 9 the record is gone ---------------------------------------------------------------------------
    S(PART[9] - 0.05, LG, 1000.0, flash=1)
    S(a("lex high school record"), LG, 980.0)
    S(a("a year later"), RL, 640.0, bw=1); number(a("daniel simmons"), 3.4, "13:25.86", "Daniel Simmons · June 2024", "New national high school record")
    S(a("so the record that made"), "state22_lex_int", 30.0, bw=1)
    S(a("and he still aint"), Q23, 650.0, bw=1)
    # 10 being fair --------------------------------------------------------------------------------
    S(PART[10] - 0.05, NU, 430.0, flash=1); chapter(PART[10] + 0.2, "05", "To Be Fair")
    S(a("leo did get better"), NU, 460.0)
    S(a("he dropped his mile"), MC, 280.0); O(a("he dropped his mile"), 6.0, ("board", "Leo Young · high school → Stanford", [("Mile", "4:00.77 → 3:56.17", "", 1), ("1500m", "3:39.39 → 3:35.96", "", 1)], "He did improve"))
    S(a("and in 2025"), Q23, 120.0); number(a("missed the final"), 3.0, "0.26", "seconds from the NCAA 1500 final", "Leo Young · 2025")
    S(a("lex ran 2748"), Q23, 660.0); number(a("lex ran 2748") + 0.2, 3.0, "27:48.93", "10,000m · Lex Young", "2nd at ACC · 2025")
    S(a("so they aint bad"), NU, 480.0)
    S(a("but good college runner"), WB, 240.0, bw=1)
    # 11 the brother ---------------------------------------------------------------------------------
    S(PART[11] - 0.05, ND, 80.0, flash=1); chapter(PART[11] + 0.25, "06", "Fell Off Or Overhyped?")
    S(a("nico went to northern arizona"), NA, 100.0)
    S(a("same family"), ND, 200.0)
    S(a("was it stanford"), CM, 195.0)
    S(a("was it the pressure"), NX, 340.0, bw=1)
    S(a("or was the hype"), CAMP, 500.0)
    S(a("honestly i think"), WB, 250.0, slow=0.7)
    S(a("you cant be the greatest"), PALI, 5.0, slow=0.5)
    S(a("and then just be regular"), MC, 300.0, bw=1)
    S(a("so y all tell me"), ND, 30.0)
    S(a("did the young twins"), NH, 90.0, slow=0.7)

"""Jane & Rocky at NCAA XC Nationals 2026: soundbites + EDL (modern style, tools/modern.py incl. 'board').
User rules (21 Nov 2026): no injuries/illness/"not 100%" in words or pictures; just that they showed up and failed.
Footage rules: no NCAA Championships / ESPN / conference broadcasts, no FloTrack/MileSplit, no RunnerSpace, no NBC/Olympic,
no Diamond League. No allowed 2026 race video existed at build time: 2026 race moments use today's school photos
(Wake Forest, Louisville, New Mexico athletics) and 2025 fan footage from John Hedengren's camera, credited with its year.
Clips: scratchpad/nats26/clips (INDEX.md); photo push-ins p_*.mp4 made from the school recap photos."""

GRAPHIC = "crop=iw*0.94:ih*0.9:iw*0.03:0"   # LetsRun odds graphic, ticker cropped off

TAGS = {
    "jane25_hedengren_full6k": "NCAA XC 2025 · John Hedengren", "jane25_hedengren_reel": "NCAA XC 2025 · John Hedengren",
    "men25_hedengren_full10k": "NCAA XC 2025 · John Hedengren", "kipchoge25_hedengren_reel": "NCAA XC 2025 · John Hedengren",
    "jane25_letsrun": "LetsRun · November 2025", "rocky25_citius": "CITIUS MAG · NCAA XC 2025",
    "jane26_big12_byu": "Big 12 XC 2026 · BYU Cougars", "jane26_uvu_dad": "UVU Invitational 2026 · John Hedengren",
    "gapes26_anz_int": "Athletics New Zealand · 2026", "gapes26_seregional_urban": "Urban Announcing · Southeast Regional 2026",
    "gapes26_ndinvite_fan": "HSE CC Dad · Notre Dame Invitational 2026", "gapes26_stride": "The Stride Report · November 21, 2026",
    "alabama26_stride": "The Stride Report · November 21, 2026", "zang26_stride": "The Stride Report · November 21, 2026",
    "rocky26_pre_stride": "The Stride Report · November 20, 2026", "rocky26_5k_citius": "CITIUS MAG · June 2026",
    "kipruto26_10k_boal": "Erik Boal Sports · April 2026", "preview26_letsrun_live": "LetsRun · race morning, November 21, 2026",
    "presser26_letsrun": "LetsRun · press conference, November 20, 2026", "terrehaute26_wtwo": "WTWO News · Terre Haute, November 2026",
    "p_rocky26_wake": "Photo: Wake Forest Athletics · November 21, 2026", "p_kipruto26_louisville": "Louisville Athletics · November 21, 2026",
    "p_unm26_champs": "New Mexico Athletics · November 21, 2026",
}

WOMEN10 = [("1", "Hannah Gapes", "NC State · 18:44.3", 1), ("2", "Salma Elbadra", "South Carolina · 18:51.8", 0),
           ("3", "Caren Kiplagat", "Alabama · 18:52.8", 0), ("4", "Isca Chelangat", "Arkansas · 18:56.6", 0),
           ("5", "Joy Naukot", "West Virginia · 18:56.7", 0), ("6", "Mercy Kinyanjui", "West Virginia · 18:57.4", 0),
           ("7", "Elizabeth Khatevi", "Texas A&M-CC · 18:57.6", 0), ("8", "Billah Jepkirui", "Oklahoma State · 18:59.2", 0),
           ("9", "Brighter Jepchumba", "Eastern Kentucky · 18:59.4", 0), ("10", "Cynthia Jemutai", "Alabama · 18:59.8", 0)]
BYU4 = [("26th", "Lexi Goff", "19:18.5", 0), ("27th", "Taylor Lovell", "19:19.5", 0),
        ("35th", "Riley Chamberlain", "19:24.3", 0), ("39th", "Jane Hedengren", "19:26.1", 1)]

# cold open: Rocky the day before the race
PRE_SB = ("rocky26_pre_stride", 64.5, 73.15, "Rocky Hansen, the day before · The Stride Report · November 20, 2026")
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("and it wasnt even close", 3), "jane25_letsrun", 184.4, 193.75, "Jane Hedengren after 2nd in 2025 · LetsRun · November 22, 2025"),
    (("jane ran", 3), "gapes26_stride", 75.8, 85.75, "Hannah Gapes, NCAA champion · The Stride Report · November 21, 2026", {"raw": 1}),
    (("now rocky", 4), "alabama26_stride", 372.6, 377.5, "Alabama, NCAA team champions · The Stride Report · November 21, 2026", {"raw": 1}),
    (("at 8k he was", 4), "preview26_letsrun_live", 1702.3, 1712.45, "LetsRun live preview · race morning · November 21, 2026"),
    (("kipruto won in", 4), "kipruto26_10k_boal", 50.9, 60.6, "Elsingi Kipruto · Erik Boal Sports · April 2026", {"raw": 1}),
    (("when you leading nationals", 4), "gapes26_stride", 213.4, 218.45, "Hannah Gapes · The Stride Report · November 21, 2026"),
    (("in the womens race", 5), "alabama26_stride", 353.0, 357.0, "Nick Stenuf, Alabama coach · The Stride Report · November 21, 2026", {"raw": 1}),
    (("the mens race was", 5), "zang26_stride", 241.3, 246.4, "Katy Zang, 15th, first American · The Stride Report · November 21, 2026", {"raw": 1}),
    (("so y all tell me", 6), "jane25_letsrun", 165.8, 171.25, "Jane Hedengren · LetsRun · November 22, 2025"),
]

J6 = "jane25_hedengren_full6k"; JR = "jane25_hedengren_reel"; M10 = "men25_hedengren_full10k"; RW = "p_rocky26_wake"
PV = "preview26_letsrun_live"; ND = "gapes26_ndinvite_fan"; TH = "terrehaute26_wtwo"


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cooked ------------------------------------------------------------------------------
    S(PART[1] - 0.05, RW, 0.0, flash=1)
    S(a("and i aint gonna"), TH, 24.0); date(a("and i aint gonna"), 3.0, "Saturday, November 21, 2026", "NCAA Cross Country · Terre Haute, Indiana")
    S(a("jane came in as the favorite"), "jane26_big12_byu", 9.0); name(a("jane came in as the favorite") + 0.3, 2.8, "Jane Hedengren", "BYU · the favorite")
    S(a("she was the runner up"), JR, 20.0)
    S(a("everybody had her"), PV, 2195.0, crop=GRAPHIC)
    S(a("and she ended up"), J6, 1312.0, bw=1); number(a("and she ended up") + 0.6, 3.6, "39th", "Jane Hedengren · NCAA XC 2026", "19:26.1")
    S(a("not top 10"), J6, 1342.0, bw=1)
    S(a("and rocky he was"), "rocky25_citius", 30.0); name(a("and rocky he was") + 0.3, 2.6, "Rocky Hansen", "Wake Forest · 2025 runner-up")
    S(a("he was leading this race"), M10, 900.0)
    S(a("and he still ended up"), RW, 5.0, bw=1); number(a("and he still ended up") + 0.4, 2.6, "6th", "Rocky Hansen · NCAA XC 2026", "28:38.4")
    S(a("so i gotta ask it"), TH, 121.0)
    S(a("are these two choke"), J6, 1420.0, slow=0.7)
    # 2 Jane ----------------------------------------------------------------------------------
    S(PART[2] - 0.05, JR, 3.0, flash=1); chapter(PART[2] + 0.2, "01", "Jane")
    S(a("last year as a freshman"), J6, 1296.0); number(a("she ran"), 3.2, "18:38.9", "Fastest freshman time in meet history", "2nd · NCAA XC 2025")
    S(a("the fastest freshman"), JR, 25.0)
    S(a("and she was second"), J6, 1840.0)
    S(a("this year she won the big 12"), "jane26_big12_byu", 9.0); title(a("this year she won the big 12"), 3.0, "Big 12 Championship · October 31, 2026", "Won by 10 seconds")
    S(a("and even ncaa"), "presser26_letsrun", 60.0); quote(a("and even ncaa") + 0.3, 3.8, "She should still be considered the favorite.", "NCAA.com · November 2, 2026")
    S(a("now i know some people"), "jane26_uvu_dad", 5.0)
    S(a("i aint trying to hear it"), J6, 1300.0, bw=1)
    S(a("she showed up"), J6, 1150.0)
    S(a("and she got cooked"), J6, 1352.0, bw=1)
    S(a("if you aint ready"), "jane26_uvu_dad", 14.0, slow=0.7, bw=1)
    # 3 the race ------------------------------------------------------------------------------
    S(PART[3] - 0.05, ND, 76.0, flash=1); chapter(PART[3] + 0.2, "02", "Not Even Close")
    S(a("hannah gapes from"), "gapes26_anz_int", 12.0); name(a("hannah gapes from"), 2.8, "Hannah Gapes", "NC State · New Zealand")
    S(a("took it out from the start"), ND, 20.0)
    S(a("and led basically"), ND, 436.0)
    S(a("and she won in"), "gapes26_seregional_urban", 8.0); number(a("and she won in") + 0.3, 3.4, "18:44.3", "Hannah Gapes · NCAA champion", "New course record")
    S(a("a new course record"), "gapes26_stride", 20.0)
    S(a("jane ran"), J6, 1362.0, bw=1); number(a("jane ran") + 0.2, 3.4, "19:26.1", "Jane Hedengren · 39th", "42 seconds behind")
    S(a("and it gets worse"), J6, 1830.0)
    S(a("lexi goff"), J6, 1282.0, bw=1); O(a("lexi goff") - 0.3, 6.6, ("board", "BYU at NCAA XC 2026", BYU4, "Jane: BYU's 4th runner"))
    S(a("byu came in ranked"), "jane26_big12_byu", 17.0)
    S(a("and alabama won"), "alabama26_stride", 360.0); title(a("and alabama won"), 3.0, "NCAA women's team champions 2026", "Alabama · first title ever")
    # 4 Rocky ---------------------------------------------------------------------------------
    S(PART[4] - 0.05, RW, 0.0, flash=1); chapter(PART[4] + 0.2, "03", "Rocky")
    S(a("rocky hanson from wake forest"), "rocky26_5k_citius", 60.0); name(a("rocky hanson from wake forest"), 2.6, "Rocky Hansen", "Wake Forest · senior")
    S(a("he was second last year"), "rocky25_citius", 60.0); title(a("he was second last year"), 3.0, "NCAA XC 2025", "2nd · 28:38.0 · behind Habtom Samuel")
    S(a("one of the top dudes"), M10, 700.0)
    S(a("at 8k he was"), M10, 1000.0); title(a("at 8k he was"), 3.0, "8K · NCAA XC 2026", "Rocky Hansen leading the race")
    S(a("on paper"), RW, 3.0)
    S(a("then elsingy kipruto"), "p_kipruto26_louisville", 0.0)
    S(a("he just took off"), M10, 1100.0)
    S(a("and rocky couldnt go"), M10, 1150.0, bw=1)
    S(a("kipruto won in"), "p_kipruto26_louisville", 4.0); number(a("kipruto won in") + 0.3, 3.6, "28:27.7", "Elsingi Kipruto · Louisville", "Course record")
    S(a("and rocky faded"), RW, 6.0, bw=1); number(a("and rocky faded") + 0.5, 3.4, "6th", "Rocky Hansen · 28:38.4", "10.7 seconds behind the win")
    S(a("when you leading nationals"), M10, 1300.0)
    S(a("you gotta get the job done"), "rocky26_pre_stride", 20.0)
    # 5 the takeover --------------------------------------------------------------------------
    S(PART[5] - 0.05, TH, 125.0, flash=1); chapter(PART[5] + 0.2, "04", "The Takeover")
    S(a("in the womens race"), ND, 600.0, blur=1); O(a("in the womens race") + 0.1, 5.4, ("board", "Women's top 10 · NCAA XC 2026", WOMEN10, "All international"))
    S(a("the whole top 10"), ND, 650.0, blur=1)
    S(a("the first american was"), "zang26_stride", 30.0); name(a("the first american was") + 0.4, 3.0, "Katy Zang", "Indiana · 15th · first American")
    S(a("the mens race was"), M10, 720.0)
    S(a("international runners all over"), "kipchoge25_hedengren_reel", 10.0)
    S(a("lets run even"), PV, 1000.0); number(a("lets run even") + 0.4, 3.6, "45%", "of scorers on qualifying teams were international", "LetsRun · November 2026")
    S(a("of the scores"), J6, 1272.0)
    S(a("and the weather was perfect"), PV, 300.0)
    S(a("course records went down"), "gapes26_seregional_urban", 15.0)
    S(a("i really feel like"), ND, 700.0)
    S(a("the last time nationals"), ND, 780.0, bw=1, blur=1); title(a("the last time nationals"), 3.6, "NCAA XC 2018 · Madison, Wisconsin", "Snow · won by American Dani Jones")
    S(a("danny jones"), ND, 760.0)
    S(a("so when its a pure speed"), M10, 800.0)
    S(a("our people gotta"), "zang26_stride", 100.0)
    S(a("and they didnt"), J6, 1372.0, bw=1)
    # 6 the verdict ---------------------------------------------------------------------------
    S(PART[6] - 0.05, J6, 1296.0, flash=1); chapter(PART[6] + 0.2, "05", "The Verdict")
    S(a("are jane and rocky"), RW, 2.0)
    S(a("or did they just get outrun"), ND, 440.0)
    S(a("cause to me"), "jane26_big12_byu", 12.0)
    S(a("when you the favorite"), JR, 30.0)
    S(a("or you the girl"), "jane26_uvu_dad", 8.0, slow=0.7)
    S(a("you gotta shine"), "p_unm26_champs", 0.0)
    S(a("let me know"), J6, 1420.0)

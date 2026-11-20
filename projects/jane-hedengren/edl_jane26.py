"""Jane Hedengren NCAA XC 2026 preview: soundbites + EDL (modern style, tools/modern.py incl. 'board').
Footage rules: no NCAA Championships / ESPN / Big 12 or other conference broadcasts, no FloTrack/MileSplit, no Olympic/NBC,
no Diamond League. No RunnerSpace (user, 20 Nov 2026). Race footage: her dad's camera, BYU's own camera, fan cams, Nike/KSL docs, team vlogs.
Clips: scratchpad/jane26/clips (INDEX.md). Soundbite times: scratchpad/jane26/tx/*.json."""

TAGS = {
    "j_nike": "Nike · Run Bigger · 2025", "j_ksl": "KSL · Beyond the Game · 2025",
    "j_uvu26": "UVU Invitational 2026 · John Hedengren", "j_uvu26_dad": "UVU Invitational 2026 · John Hedengren",
    "j_byu_big12": "Big 12 XC 2026 · BYU Cougars", "j_millrose": "Millrose Games 2026",
    "g_anz_int": "Athletics New Zealand · September 2026", "g_se_regional": "Urban Announcing · Southeast Regional 2026",
    "g_nd_dad": "HSE CC Dad · Notre Dame Invitational 2026", "g_nd_muchmore": "Jim Muchmore · Notre Dame Invitational 2026",
    "j_longrun": "TRACK: All-Access · BYU", "j_stride": "BYU workout", "j_wtwo_course": "WTWO News · November 2026",
    "j_lavern_6k": "LaVern Gibson 6K · Game Action 360", "j_unm_kosgei": "Noah Reed Reports · Mountain Regional 2026", "j_bedridden": "LetsRun · NCAA outdoors, June 2026",
    "j_letsrun_x": "LetsRun · Millrose 2026", "j_lastlap_int": "The Last Lap Podcast · BYU awards 2026",
    "j_byutv_team": "BYUtv Sports Nation · 2026", "j_letsrun_slump": "LetsRun Track Talk · September 2026",
}

SEASON = [("March", "NCAA indoors", "3000 + 5000 champion", 1), ("April", "NCAA record · 10,000", "30:46.80", 1),
          ("April", "NCAA record · 5000", "14:50.50", 1), ("June", "NCAA outdoors (sick)", "3rd 10,000 · 9th 5000", 0),
          ("September", "Cowboy Jamboree", "3rd", 0), ("October", "Pre-Nats", "Missed (illness)", 0),
          ("October 31", "Big 12", "Won by 10 seconds", 1), ("November 13", "Regionals", "Rested", 0)]
THREATS = [("Hannah Gapes", "NC State", "Unbeaten · course record 18:57", 1), ("Billah Jepkirui", "Oklahoma State", "Beat Jane in September", 0),
           ("Pamela Kosgei", "New Mexico", "Beat Jane in the 10,000 in June", 0)]

# cold open: her high school coach
PRE_SB = ("j_ksl", 220.4, 223.6, "Jaimie Ribera, Jane's high school coach · KSL · 2025")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("but then you look at", 3), "j_ksl", 85.9, 97.8, "Jane Hedengren · KSL · 2025"),
    (("and thats not who jane", 3), "j_bedridden", 48.9, 58.1, "Jane Hedengren after NCAA outdoors · LetsRun · June 2026"),
    (("and her and jane aint raced", 5), "g_se_regional", 4.0, 19.6, "Hannah Gapes · Southeast Regional · Urban Announcing · November 13, 2026"),
    (("plus the team title", 6), "j_lastlap_int", 262.8, 272.1, "BYU women's cross country · The Last Lap Podcast · 2026"),
    (("if jane shows up", 7), "j_ksl", 192.0, 200.0, "Jane Hedengren · KSL · 2025"),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 the question ---------------------------------------------------------------------
    S(PART[1] - 0.05, "j_wtwo_course", 24.0, flash=1); date(a("is tomorrow"), 3.0, "Saturday, November 21, 2026", "NCAA Cross Country · Terre Haute")
    S(a("and i got a question"), "j_lavern_6k", 99.0)
    S(a("is jane hendergren"), "j_nike", 366.0, slow=0.8); name(a("is jane hendergren") + 0.4, 3.0, "Jane Hedengren", "BYU · sophomore")
    S(a("get the job done"), "j_uvu26_dad", 5.0, slow=0.7)
    S(a("because on paper"), "j_byu_big12", 9.0)
    S(a("shes the favorite"), "j_uvu26", 413.0)
    S(a("everybody got her"), "j_millrose", 384.0)
    S(a("but we done seen favorites fold"), "j_millrose", 640.0, bw=1)
    S(a("jane has had some moments"), "j_bedridden", 72.0, bw=1)
    # 2 last year -----------------------------------------------------------------------
    S(PART[2] - 0.05, "j_nike", 220.0, flash=1); chapter(PART[2] + 0.2, "01", "Last Year")
    S(a("she was a favorite going in"), "j_nike", 73.0)
    S(a("and she still lost"), "j_letsrun_x", 100.0, bw=1); number(a("and she still lost"), 3.0, "18:38.9", "Fastest freshman in meet history", "2nd · NCAA XC 2025")
    S(a("doris from alabama"), "j_wtwo_course", 105.0); name(a("doris from alabama"), 2.8, "Doris Lemngole", "Alabama · 2-time NCAA champion")
    S(a("now doris is gone"), "j_lavern_6k", 160.0)
    S(a("shes the one person"), "j_uvu26", 230.0)
    S(a("and she aint even in this race"), "j_wtwo_course", 57.0)
    S(a("so that mean if jane"), "j_ksl", 15.0)
    S(a("theres really no excuse"), "j_uvu26_dad", 13.0)
    S(a("people gonna start calling her"), "j_bedridden", 216.0, bw=1)
    # 3 the highs and the lows ---------------------------------------------------------
    S(PART[3] - 0.05, "j_nike", 268.0, flash=1); chapter(PART[3] + 0.2, "02", "On Paper")
    S(a("one thing about me"), "j_nike", 171.0)
    S(a("when jane is right"), "j_millrose", 454.0)
    S(a("back in march"), "j_millrose", 175.0)
    O(a("back in march"), 9.5, ("board", "Jane's 2026", SEASON[:3], "At 19 years old"))
    S(a("then she broke the ncaa record in the 10k"), "j_stride", 300.0)
    S(a("and then a couple weeks later"), "j_stride", 175.0)
    S(a("at nineteen years old"), "j_ksl", 163.0)
    S(a("thats somebody that shines"), "j_nike", 150.0)
    S(a("she got sick right before"), "j_bedridden", 120.0, bw=1); title(a("ended up third"), 3.0, "NCAA outdoors · June 2026", "3rd 10,000 · 9th 5000")
    S(a("and thats not who jane"), "j_longrun", 468.0, bw=1)
    # 4 this fall -----------------------------------------------------------------------
    S(PART[4] - 0.05, "j_uvu26", 138.0, flash=1); chapter(PART[4] + 0.2, "03", "This Fall")
    S(a("september at the cowboy jamboree"), "j_letsrun_slump", 493.0); title(a("she finished third"), 2.8, "Cowboy Jamboree · September 2026", "3rd · first regular-season loss")
    S(a("that was the first time she ever lost"), "j_uvu26", 597.0, bw=1)
    S(a("then she missed pre nationals"), "j_lavern_6k", 59.0, bw=1)
    S(a("getting over being sick"), "j_bedridden", 152.0, bw=1)
    S(a("but then at big 12s"), "j_byu_big12", 9.0); title(a("but then at big 12s"), 3.0, "Big 12 Championship · October 31", "Won by 10 seconds · in the rain")
    S(a("she beat the same girl"), "j_byu_big12", 17.0)
    S(a("thats the jane that gets the job done"), "j_byu_big12", 17.0, slow=0.7)
    S(a("then at regionals last week"), "j_longrun", 201.0)
    S(a("so she aint raced since"), "j_stride", 525.0); number(a("so she aint raced since"), 3.0, "21 days", "Since her last race", "October 31 → November 21")
    S(a("either shes fresh and ready"), "j_longrun", 870.0)
    S(a("and thats what were going to find out"), "j_lavern_6k", 230.0)
    # 5 the threats ---------------------------------------------------------------------
    S(PART[5] - 0.05, "g_nd_muchmore", 57.0, flash=1); chapter(PART[5] + 0.2, "04", "The Threat")
    S(a("named hannah grapes"), "g_anz_int", 12.0); name(a("named hannah grapes"), 3.0, "Hannah Gapes", "NC State · New Zealand")
    S(a("she hasnt lost one time"), "g_nd_dad", 203.0)
    S(a("she won pre nationals"), "j_lavern_6k", 199.0); number(a("eighteen 57"), 3.0, "18:57", "Course record · Pre-Nats", "First woman under 19:00 on this course")
    S(a("the first woman to ever break"), "g_nd_dad", 508.0)
    S(a("then last week at regional"), "g_se_regional", 75.0)
    S(a("that kaitlyn toohey had"), "j_wtwo_course", 121.0)
    S(a("and her and jane aint raced"), "j_uvu26_dad", 17.0)
    S(a("you got the girl from oklahoma state"), "j_letsrun_slump", 137.0)
    S(a("pamela from new mexico"), "j_unm_kosgei", 33.0); name(a("pamela from new mexico"), 2.6, "Pamela Kosgei", "New Mexico")
    S(a("so theres people in that race"), "j_unm_kosgei", 99.0)
    O(a("so theres people in that race"), 4.5, ("board", "Who can beat Jane?", THREATS, ""))
    # 6 history -------------------------------------------------------------------------
    S(PART[6] - 0.05, "j_nike", 317.0, flash=1); chapter(PART[6] + 0.2, "05", "History")
    S(a("second girl from byu"), "j_byutv_team", 25.0)
    S(a("the only one before"), "j_ksl", 222.0); name(a("winning ordon"), 2.8, "Whittni Orton", "BYU · 2021 NCAA champion")
    S(a("first american to win since"), "j_millrose", 245.0); name(a("parker valby"), 2.6, "Parker Valby", "Florida · 2023 champion")
    S(a("plus the team title"), "j_byutv_team", 125.0); title(a("plus the team title"), 3.0, "NCAA team champions since 2020", "BYU or NC State · every year")
    # 7 the call ------------------------------------------------------------------------
    S(PART[7] - 0.05, "j_ksl", 193.0, flash=1); chapter(PART[7] + 0.2, "06", "The Call")
    S(a("i think its a good chance"), "j_uvu26", 505.0)
    S(a("shes too talented"), "j_nike", 24.0)
    S(a("but if she run like"), "j_bedridden", 264.0, bw=1)
    S(a("grapes gonna drag her"), "g_anz_int", 100.0)
    S(a("but i wanna know"), "j_nike", 366.0)
    S(a("is jane gonna come through"), "j_uvu26_dad", 9.0, slow=0.7)
    S(a("or is she gonna go out there"), "j_millrose", 300.0)
    S(a("y all let me know"), "j_nike", 317.0)

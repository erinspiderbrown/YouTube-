"""Gout Gout: "Investigating Australia's Fastest Man... Are His Times Real?" (28 Nov 2026). Soundbites + EDL.
Premium layer (tools/premium.py): interview IDs + word-synced subs, race clocks, gap/board/timeline/wipe graphics,
cinematic transitions. Footage: Vic Pascoe / fan films from the stands for every race; interviews (ABC, Seven Spotlight,
Beyond The Records, Nova, CBC, CITIUS, Emerole/The Final Leg, Ready Set Go, 10 News, ITV, CBS 60 Minutes audio only).
Rules: no NBC/Peacock, Olympic, World Athletics broadcast, Diamond League feed, FloTrack/MileSplit, RunnerSpace.
WA-branded mixed zones (Lyles CITIUS Tokyo) -> audio only over other B-roll. Clips with burned-in subtitles
(abc_1967, bolt_itv, dad_sunrise) get no extra subs. Guards: never say the clock or gauge was wrong; argue from conditions."""

TAGS = {
    "fan_1967": "Sydney, April 12, 2026 · fan video from the stands · Vic Pascoe", "co_open": "Sydney, April 12, 2026 · fan video · Vic Pascoe",
    "fan_heat1": "Sydney heats · fan video · Vic Pascoe", "fan_heat2": "Sydney heats · fan video · Vic Pascoe",
    "fan_1000a": "Brisbane, Feb 21, 2026 · fan video · Vic Pascoe", "fan_1000b": "Brisbane, Feb 21, 2026 · fan video",
    "fan_qld100h": "QLD Champs 2026 · fan video", "fan_qld100f": "QLD Champs 2026 · fan video", "fan_qld200s": "QLD Champs 2026 · fan video",
    "fan_qld200f": "QLD Champs 2026 · fan video", "fan_jun100h": "Australian Juniors 2026 · fan video", "fan_jun100s": "Australian Juniors 2026 · fan video",
    "fan_jun100f": "Australian Juniors 2026 · fan video", "fan_murphy_oce": "Oceania Champs 2026 · fan video",
    "abc_1967": "ABC News", "spot7": "Seven · Spotlight", "btr_lyles": "Beyond The Records podcast", "nova": "Nova",
    "bolt_guardian": "The Guardian", "bolt_itv": "ITV News", "lyles_citius": "CITIUS MAG", "aw_tokyo": "Athletics Weekly",
    "ostrava_presser": "Golden Spike Ostrava", "bailey_cbc": "CBC Sports", "brown_cbc": "CBC Sports", "dad_sunrise": "Seven · Sunrise",
    "gatlin_rsg": "Ready Set Go podcast", "citius_wind": "CITIUS MAG", "emerole_react": "Anderson Emerole", "emerole_fl": "The Final Leg",
    "citius_taylor": "CITIUS MAG", "murphy_sasi": "SASI", "ten_illness": "10 News First", "citius_oslo": "CITIUS MAG",
    "fl_whathappened": "The Final Leg", "citius_season": "YouTube · Gout Gout injury statement", "min60": "CBS 60 Minutes", "erin_tiktok": "TikTok · @erinspiderbrown · June 29, 2026", "citius_tate": "CITIUS MAG podcast", "fl_tate": "The Final Leg",
}
C_CAP = "crop=iw:ih*0.84:0:0"          # cut the burned-in caption band of the fan films
GG = ("Gout Gout", "19.67 · U20 world record", "")

# cold open: his coach banging on the window, "Is it legal?" -> over the fan film of the race + the 19.67 clock
PRE_SB = ("abc_1967", 48.03, 54.31, "Di Sheppard, Gout's coach · ABC News",
          dict(vsrc="co_open", vss=0.0, name=("Di Sheppard", "Gout Gout's coach", "Audio · ABC News")))
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts]) - snap() extends every bite to whole sentences
    (("gout gout was born", 2), "bailey_cbc", 96.00, 102.46, "Donovan Bailey · CBC Sports",
     dict(subs=1, name=("Donovan Bailey", "1996 Olympic 100m champion", "CBC Sports"), subfix=[("1967", "19.67")])),
    (("years later she see", 2), "spot7", 648.32, 665.87, "Di Sheppard · Seven Spotlight",
     dict(subs=1, name=("Di Sheppard", "His only coach", "Seven · Spotlight"))),
    (("but here go the first", 4), "btr_lyles", 808.42, 829.88, "Gout Gout on his 20.04 · Beyond The Records",
     dict(subs=1, name=("Gout Gout", "On the 20.04 at 16", "Beyond The Records podcast"))),
    (("but here go the first", 4), "bolt_itv", 0.00, 2.94, "Usain Bolt · ITV News", dict(name=("Usain Bolt", "", "ITV News"))),
    (("yeah in 2025", 5), "nova", 1491.30, 1497.92, "Nova · December 2025",
     dict(subs=1, name=("Nova radio", "On his wind-aided 19.84", "December 2025"))),
    (("yeah in 2025", 5), "nova", 1536.30, 1545.34, "Gout Gout · Nova", dict(subs=1, tr="none")),
    (("then come 2026", 6), "brown_cbc", 56.92, 61.00, "Aaron Brown · CBC Sports",
     dict(subs=1, name=("Aaron Brown", "Canadian Olympic sprinter", "CBC Sports"))),
    (("then at the maurie plant", 7), "ten_illness", 83.04, 88.12, "Gout Gout, QLD Champs · 10 News First",
     dict(subs=1, name=("Gout Gout", "QLD Champs, March 2026", "10 News First"))),
    (("now listen", 8), "abc_1967", 14.87, 26.23, "Gout Gout after the 19.67 · ABC News",
     dict(name=("Gout Gout", "Minutes after the 19.67", "ABC News"))),
    (("aint no way a whole", 8), "citius_wind", 650.85, 667.35, "Chris Chavez · CITIUS MAG",
     dict(subs=1, raw=1, name=("Chris Chavez", "On the wind gauge and the bend", "CITIUS MAG"))),
    (("now lets go down", 9), "citius_wind", 87.68, 92.08, "Chris Chavez · CITIUS MAG", dict(subs=1)),
    (("two months later in oslo", 10), "gatlin_rsg", 4843.39, 4849.01, "Justin Gatlin · Ready Set Go",
     dict(subs=1, name=("Justin Gatlin", "2004 Olympic 100m champion", "Ready Set Go podcast"), subfix=[("for God, God,", "for Gout Gout,"), ("God, God,", "Gout Gout,")])),
    (("then he ran 150", 10), "citius_oslo", 29.28, 33.30, "Gout Gout after Oslo · CITIUS MAG",
     dict(subs=1, name=("Gout Gout", "After 20.60 in Oslo", "CITIUS MAG"))),
    # the receipt: Erin's own TikTok, June 29 (profanity skipped: only 0-15 s and 73.7-87.4 s)
    (("then july", 11), "erin_tiktok", 0.0, 14.88, "TikTok · @erinspiderbrown · June 29, 2026",
     dict(subs=1, raw=1, name=("Erin Brown", "June 29, 2026 · five days before Pre", "TikTok"), subfix=[("1985", "19.85")])),
    (("then july", 11), "erin_tiktok", 73.74, 87.40, "TikTok · @erinspiderbrown · June 29, 2026",
     dict(subs=1, raw=1, tr="none", subfix=[("1985", "19.85")])),
    (("gout was supposed to be", 11), "citius_tate", 93.95, 114.95, "Chris Chavez · CITIUS MAG podcast, July 2026",
     dict(subs=1, raw=1, name=("Chris Chavez", "On Tate's 19.75 vs Gout's 19.67", "CITIUS MAG podcast"),
          subfix=[("gout gots", "Gout Gout's"), ("Gout gots", "Gout Gout's"), ("gout gets", "Gout Gout"), ("nine seven nine six 1967", "19.67"), ("P.B.s", "PBs")])),
    (("so here go my verdict", 12), "bailey_cbc", 68.75, 72.15, "Donovan Bailey · CBC Sports", dict(subs=1, raw=1)),
]
SPLIT_AT = {}

F67 = "fan_1967"


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    B = lambda *rows: rows
    SFX = lambda t, nm, g=0.4: O(t, 0.5, ("sfx", nm, g))
    AMB = lambda t0, t1, nm, v=0.2: O(t0, t1 - t0, ("amb", nm, v))
    # 1 the take --------------------------------------------------------------------------------------
    S(PART[1] - 0.05, F67, 17.6, crop=C_CAP, slow=0.6)
    O(PART[1] + 0.3, 3.6, ("title", "Australian Championships · April 12, 2026", "19.67"))
    S(a("and that little comment"), "btr_lyles", 970.0, tr="zoom")
    O(a("yahoo") - 0.1, 3.2, ("stamp", "Quoted", "Yahoo · SportBible · Runner's Tribe"))
    S(a("so i went back"), "fan_heat1", 16.0, tr="rgb")
    SFX(a("so i went back"), "files", 0.35)
    S(a("every wind reading"), "fan_qld200s", 1.0, slow=0.7)
    S(a("and by the time"), "fan_1000b", 9.9, slow=0.8, tr="push")
    O(a("and by the time") + 0.4, 3.6, ("wipe", ["Wind, heats, every finalist.", "The whole file."], "The investigation"))
    # 2 the coach ------------------------------------------------------------------------------------------
    S(PART[2] - 0.05, "spot7", 786.0, tr="leak"); chapter(PART[2] + 0.3, "01", "Ipswich")
    O(a("gout gout was born") + 3.3, 3.2, ("date", "December 29, 2007", "Ipswich, Queensland"))
    S(a("his mama and daddy"), "fan_qld100f", 24.0, crop=C_CAP, slow=0.8, tr="blur")
    S(a("and her story crazy"), "spot7", 1135.0, tr="zoom")
    O(a("back in the early") + 0.2, 4.4, ("title", "Di Sheppard · early 2000s", "Grocery store → school uniforms"))
    S(a("they told her only"), "spot7", 1310.0, bw=1)
    S(a("so she quit"), "spot7", 1150.0, slow=0.8)
    # 3 the hype -------------------------------------------------------------------------------------------
    S(PART[3] - 0.05, "spot7", 1484.0, tr="leak"); chapter(PART[3] + 0.3, "02", "The Hype")
    S(a("that broke peter norman"), "fan_jun100h", 18.6, slow=0.6, tr="vpush")
    O(a("that broke peter norman") + 0.5, 4.2, ("title", "Australian record · since 1968", "20.06 → 20.04"))
    S(a("faster than usain bolt"), "bolt_guardian", 8.0, tr="whip")
    S(a("a couple months before"), "nova", 300.0, tr="blur")
    SFX(a("a couple months before") + 0.8, "shutters", 0.35)
    O(a("four million") - 0.2, 4.6, ("wipe", ["$4 million? $6 million?", "Never confirmed."], "The adidas deal"))
    S(a("but just like that"), "fan_1000b", 17.6, slow=0.7, tr="zoom")
    # 4 the wind -------------------------------------------------------------------------------------------
    S(PART[4] - 0.05, "fan_qld200s", 1.0, slow=0.5, tr="leak"); chapter(PART[4] + 0.3, "03", "The Wind")
    AMB(PART[4], PART[5], "amb_wind", 0.22)
    O(a("every last one") - 13.0, 14.5, ("board", "Every sub-10 / sub-20 before 2026", B(
        ("100m · Dec 2024", "10.04", "+3.4 wind", 1), ("200m · Mar 2025", "19.98", "+3.4 wind", 1),
        ("100m · Apr 2025", "9.99", "+3.5 wind", 1), ("100m · Apr 2025", "9.99", "+2.6 wind", 1),
        ("200m · Apr 2025", "19.84", "+2.2 wind", 1)), "Legal limit +2.0 · all run in Australia"))
    # 5 overseas -------------------------------------------------------------------------------------------
    S(PART[5] - 0.05, "brown_cbc", 91.0, tr="blur")
    O(a("czech republic") - 1.0, 3.6, ("title", "Ostrava · June 2025 · wind 0.0", "20.02"))
    S(a("but put him in a real"), "aw_tokyo", 30.0, bw=1, tr="rgb")
    O(a("the world championships in tokyo") + 0.6, 4.4, ("title", "World Championships · Tokyo 2025", "20.23 · 20.36 · out"))
    # 6 the 10.00 -----------------------------------------------------------------------------------------------
    S(PART[6] - 0.05, "fan_1000a", 3.0, tr="leak"); chapter(PART[6] + 0.2, "04", "The 10 Flat")
    O(a("his first race of the year") + 0.3, 5.0, ("clock", 0.0, "Brisbane · Feb 21, 2026 · wind +0.9", 1.0, 10.0))
    SFX(a("his first race of the year") + 0.2, "gun_roar", 0.32)
    S(a("legal but look"), "fan_1000b", 17.6, slow=0.6, tr="push")
    S(a("six of the"), "fan_qld200s", 1.0, bw=1, tr="rgb")
    O(a("six of the") + 0.2, 4.0, ("number", "+2.8", "Same meet · one of the men's 100s", "6 readings over the limit that day"))
    S(a("the rest of the season"), "fan_qld100f", 5.7, crop=C_CAP, tr="whip")
    O(a("the rest of the season") + 0.3, 7.0, ("board", "100m · rest of 2026", B(
        ("Brisbane · Feb", "10.00", "+0.9", 1), ("QLD Champs · Mar", "10.20", "+1.5", 0), ("Juniors heat · Apr", "10.19", "+0.3", 0),
        ("Juniors semi · Apr", "10.44", "-2.2", 0), ("Juniors final · Apr", "10.21", "+0.5", 0)), ""))
    S(a("he aint never came close"), "fan_jun100f", 11.5, slow=0.7, tr="blur")
    # 7 the 200 ------------------------------------------------------------------------------------------------
    S(PART[7] - 0.05, "fan_qld200f", 16.5, crop=C_CAP, tr="vpush")
    S(a("and he said he was sick"), "fan_qld200f", 29.0, crop=C_CAP)
    S(a("in the rain"), "fan_qld200s", 17.0, bw=1, slow=0.7, tr="blur")
    O(a("in the rain") + 0.3, 4.2, ("title", "Maurie Plant Meet · Melbourne", "Kennedy 20.38 · Gout 20.43"))
    t_rain = a("in the rain"); AMB(t_rain - 0.5, a("so going into") + 1.0, "amb_rain", 0.28)
    S(a("so going into"), "fan_qld200f", 20.0, crop=C_CAP, slow=0.6, tr="zoom")
    # 8 Sydney -------------------------------------------------------------------------------------------------
    S(PART[8] - 0.05, "fan_heat1", 3.0, tr="leak"); chapter(PART[8] + 0.2, "05", "Sydney")
    AMB(PART[8], PART[9], "amb_wind", 0.2)
    S(a("in the morning"), "fan_heat1", 16.0, slow=0.8, tr="push")
    O(a("in the morning") + 0.1, 2.2, ("clock", 0.0, "Morning heat · wind +0.4", 1.0, 20.11))
    S(a("that afternoon in the final"), F67, 17.8, crop=C_CAP, slow=0.6, tr="whip")
    SFX(a("that afternoon in the final") - 0.1, "gun_roar", 0.3)
    O(a("that afternoon in the final") + 0.4, 5.0, ("gap", "Final · afternoon", 19.67, "Heat · morning", 20.11, "0.44 seconds", "Same day · same track"))
    O(a("now listen") + 0.5, 4.6, ("number", "+2.3", "Women's 200m final, minutes before", "Same track · same afternoon"))
    S(a("and look at the mens final"), "fan_heat2", 16.0, bw=1, tr="rgb")
    O(a("dudes ran a personal best") - 0.6, 9.0, ("board", "Men's 200m final · 7 of 8 ran PBs", B(
        ("Gout Gout", "19.67", "PB · heat 20.11", 1), ("Aidan Murphy", "19.88", "PB · old best 20.41", 1), ("Calab Law", "20.21", "PB", 1),
        ("Christopher Ius", "20.26", "PB", 1), ("Archer McHugh", "20.37", "PB", 1), ("Rory Easton", "20.37", "PB", 1)),
        "Wind +1.7 · women's final just before +2.3"))
    S(a("yeah world athletics"), F67, 40.0, crop=C_CAP, tr="blur")
    O(a("that race was windy") - 0.2, 3.6, ("wipe", ["That race was windy."], ""))
    # 9 the finalists ------------------------------------------------------------------------------------------
    S(PART[9] - 0.05, F67, 96.0, crop=C_CAP, slow=0.5, bw=1, tr="leak"); chapter(PART[9] + 0.2, "06", "The Next Race")
    t9 = a("gout 1967") - 0.4
    rows = [("Gout Gout", 19.67, 20.60, "Oslo DL · Jun 10", 0.0), ("Aidan Murphy", 19.88, 20.28, "Oceania heat · May 21 (final 20.05)", a("aidan murphy") - t9),
            ("Calab Law", 20.21, 20.85, "Tokyo · May 17", a("calab law") - t9), ("Christopher Ius", 20.26, 21.02, "Oceania heat (final 20.68)", a("christopher") - t9),
            ("Archer McHugh", 20.37, None, "no 200m rest of 2026", a("archer") - t9), ("Rory Easton", 20.37, 21.42, "Oceania heat · DNF final", a("rory easton") - t9),
            ("Sebastian Milverton", 20.83, None, "no 200m rest of 2026", a("sebastian") - t9)]
    O(t9, a("and joseph") - t9 + 1.0, ("drift", "Sydney final → his very next 200m", rows))
    S(t9, F67, 60.0, crop=C_CAP, slow=0.5, blur=1)
    S(a("and joseph"), "fan_heat2", 24.0, bw=1, tr="zoom")
    S(a("so seven dudes"), F67, 22.0, crop=C_CAP, slow=0.45, tr="blur")
    O(a("so seven dudes") + 0.3, 5.0, ("wipe", ["7 PBs in one final.", "Not one ran it again."], "2026"))
    SFX(a("so seven dudes") + 0.2, "heartbeat", 0.35)
    # 10 Oslo + the receipt ------------------------------------------------------------------------------------
    S(PART[10] - 0.05, "citius_oslo", 8.0, bw=1, tr="leak"); chapter(PART[10] + 0.2, "07", "The Receipt")
    O(a("two months later in oslo") + 0.4, 3.8, ("title", "Oslo · June 10, 2026 · Diamond League debut", "20.60 · 6th"))
    S(a("then he ran 150"), "citius_season", 99.0, tr="blur")
    S(a("so june 29th"), "erin_tiktok", 2.0, tr="rgb")
    SFX(a("so june 29th") + 0.1, "phone", 0.4)
    O(a("so june 29th") + 0.2, 3.4, ("stamp", "Rec · TikTok", "Posted June 29, 2026"))
    # 11 Pre + the withdrawal ----------------------------------------------------------------------------------
    S(PART[11] - 0.05, "citius_tate", 30.0, tr="zoom")
    O(a("tate taylor ran 1975") + 0.2, 4.6, ("number", "19.75", "Tate Taylor · Pre Classic · July 4", "into a -0.9 headwind"))
    SFX(a("he pulled out"), "glitch", 0.3)
    S(a("he pulled out"), "citius_season", 99.0, bw=1)
    S(a("four days later"), "citius_season", 120.0, bw=1, tr="blur")
    O(a("four days later") + 0.3, 4.4, ("board", "July 2026", B(("Jun 29", "TikTok", "the prediction", 0), ("Jul 4", "19.75", "Tate Taylor · Pre", 1), ("Jul 4", "out", "Gout scratches · tightness", 0), ("Jul 9", "out", "hamstring · out of World U20s", 1)), ""))
    S(a("now i aint his doctor"), "erin_tiktok", 74.0, tr="rgb")
    O(a("but i said it on") + 0.2, 4.4, ("quote", "Everything happened exactly how I said it would.", "Erin Brown"))
    # 12 verdict -----------------------------------------------------------------------------------------------
    S(PART[12] - 0.05, F67, 96.0, crop=C_CAP, slow=0.6, bw=1, tr="leak"); chapter(PART[12] + 0.2, "08", "The Verdict")
    AMB(PART[12], PART[12] + 40, "heartbeat", 0.16)
    O(a("take away that one day") + 0.3, 4.6, ("wipe", ["Outside Sydney,", "never under 20 legal."], ""))
    S(a("his next best legal"), "fan_qld200f", 18.0, crop=C_CAP, bw=1, tr="push")
    O(a("his next best legal") - 0.2, 8.0, ("board", "His 200m races, 2026", B(
        ("QLD Champs semi · Mar", "20.59", "+0.9", 0), ("QLD Champs final · Mar", "20.42", "-2.1", 0), ("Maurie Plant · Mar", "20.43", "2nd", 0),
        ("Sydney heat · Apr", "20.11", "+0.4", 0), ("Sydney final · Apr", "19.67", "+1.7", 1), ("Oslo · Jun", "20.60", "6th", 0)),
        "Next-best legal 200m ever: 20.02 (Ostrava 2025)"))
    S(a("meanwhile tate taylor"), "citius_tate", 300.0, tr="zoom")
    S(a("so no i dont believe"), F67, 22.0, crop=C_CAP, slow=0.45, tr="blur")
    O(a("that wasnt australias") - 0.1, 5.0, ("wipe", ["Not Australia's fastest man.", "Australia's windiest day."], ""))
    SFX(a("that wasnt australias") - 0.2, "boom", 0.45)
    S(a("i said it in april"), "btr_lyles", 4018.0, tr="blur")

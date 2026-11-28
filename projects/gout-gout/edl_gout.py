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
    "fl_whathappened": "The Final Leg", "citius_season": "YouTube · Gout Gout injury statement", "min60": "CBS 60 Minutes",
}
C_CAP = "crop=iw:ih*0.84:0:0"          # cut the burned-in caption band of the fan films
GG = ("Gout Gout", "19.67 · U20 world record", "")

# cold open: his coach banging on the window, "Is it legal?" -> over the fan film of the race + the 19.67 clock
PRE_SB = ("abc_1967", 48.03, 54.31, "Di Sheppard, Gout's coach · ABC News",
          dict(vsrc="co_open", vss=0.0, name=("Di Sheppard", "Gout Gout's coach", "Audio · ABC News")))
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("gout gout was born", 2), "bailey_cbc", 96.00, 102.46, "Donovan Bailey · CBC Sports",
     dict(subs=1, name=("Donovan Bailey", "1996 Olympic 100m champion", "CBC Sports"), subfix=[("1967", "19.67")])),
    (("then in december", 3), "spot7", 648.32, 665.87, "Di Sheppard · Seven Spotlight",
     dict(subs=1, name=("Di Sheppard", "His only coach", "Seven · Spotlight"))),
    (("then in december", 3), "min60", 491.52, 498.72, "Di Sheppard · CBS 60 Minutes (audio)",
     dict(vsrc="fan_qld100f", vss=24.0, crop=C_CAP, subs=1)),
    (("but here go the first", 4), "btr_lyles", 808.42, 829.88, "Gout Gout on his 20.04 · Beyond The Records",
     dict(subs=1, name=("Gout Gout", "On the 20.04 at 16", "Beyond The Records podcast"))),
    (("but here go the first", 4), "bolt_itv", 0.00, 2.94, "Usain Bolt · ITV News", dict(name=("Usain Bolt", "", "ITV News"))),
    (("but here go the first", 4), "lyles_citius", 142.64, 146.52, "Noah Lyles, Tokyo 2025 · CITIUS MAG (audio)",
     dict(vsrc="fan_1000b", vss=9.9, subs=1, name=("Noah Lyles", "On Gout at 17", "Audio · CITIUS MAG"))),
    (("now to be fair", 5), "nova", 1491.30, 1497.92, "Nova · December 2025",
     dict(subs=1, name=("Nova radio", "On his wind-aided 19.84", "December 2025"))),
    (("now to be fair", 5), "nova", 1536.30, 1545.34, "Gout Gout · Nova", dict(subs=1, tr="none")),
    (("then come 2026", 6), "brown_cbc", 56.92, 61.00, "Aaron Brown · CBC Sports",
     dict(subs=1, name=("Aaron Brown", "Canadian Olympic sprinter", "CBC Sports"))),
    (("then at the maury plant", 7), "ten_illness", 83.04, 88.12, "Gout Gout, QLD Champs · 10 News First",
     dict(subs=1, name=("Gout Gout", "QLD Champs, March 2026", "10 News First"))),
    (("the womens 200 final", 8), "abc_1967", 14.87, 26.23, "Gout Gout after the 19.67 · ABC News",
     dict(name=("Gout Gout", "Minutes after the 19.67", "ABC News"))),
    (("now imma give", 9), "citius_wind", 87.68, 92.08, "Chris Chavez · CITIUS MAG",
     dict(subs=1, name=("Chris Chavez", "CITIUS MAG", ""))),
    (("now imma give", 9), "citius_wind", 653.70, 667.38, "Chris Chavez · CITIUS MAG", dict(subs=1, tr="none")),
    (("now imma give", 9), "emerole_react", 32.55, 35.23, "Anderson Emerole",
     dict(subs=1, name=("Anderson Emerole", "Former Team USA sprinter", "YouTube"))),
    (("and aiden murphy went", 9), "abc_1967", 82.99, 87.45, "Di Sheppard · ABC News", dict(name=("Di Sheppard", "Gout's coach", "ABC News"))),
    (("but what about gout", 9), "emerole_fl", 2475.46, 2486.08, "Anderson Emerole · The Final Leg",
     dict(subs=1, subfix=[("Nineteen six seven", "19.67"), ("1967", "19.67")])),
    (("two months later in oslo", 9), "gatlin_rsg", 4843.39, 4849.01, "Justin Gatlin · Ready Set Go",
     dict(subs=1, name=("Justin Gatlin", "2004 Olympic 100m champion", "Ready Set Go podcast"), subfix=[("for God, God,", "for Gout Gout,"), ("God, God,", "Gout Gout,")])),
    (("then in july", 9), "citius_oslo", 29.28, 33.30, "Gout Gout after Oslo · CITIUS MAG",
     dict(subs=1, name=("Gout Gout", "After 20.60 in Oslo", "CITIUS MAG"))),
    (("so here go what", 10), "bailey_cbc", 62.70, 71.56, "Donovan Bailey · CBC Sports", dict(subs=1)),
    (("so now i want", 11), "spot7", 2667.91, 2681.27, "Gout Gout · Seven Spotlight",
     dict(subs=1, name=("Gout Gout", "", "Seven · Spotlight"))),
]
SPLIT_AT = {}

F67 = "fan_1967"


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    B = lambda *rows: rows
    # 1 the take --------------------------------------------------------------------------------------
    S(PART[1] - 0.05, F67, 17.6, crop=C_CAP, slow=0.6)
    O(PART[1] + 0.3, 3.6, ("title", "Australian Championships · April 12, 2026", "19.67"))
    S(a("and that little comment"), "btr_lyles", 970.0, tr="whip")
    S(a("so i did what"), "fan_heat1", 16.0, tr="blur")
    S(a("i went back and pulled"), "fan_qld200s", 1.0, slow=0.7)
    S(a("lay it all out"), "fan_1000b", 9.9, slow=0.8)
    O(a("at the end y all") + 0.2, 3.4, ("wipe", ["Are his times real?"], "The investigation"))
    # 2 Ipswich --------------------------------------------------------------------------------------------
    S(PART[2] - 0.05, "spot7", 786.0, tr="leak"); chapter(PART[2] + 0.3, "01", "Ipswich")
    O(a("gout gout was born") + 3.3, 3.2, ("date", "December 29, 2007", "Ipswich, Queensland"))
    S(a("his mama and daddy"), "fan_qld100f", 24.0, crop=C_CAP, slow=0.8)
    S(a("he was out there playing"), "spot7", 1310.0, tr="blur")
    S(a("she a grandmother"), "spot7", 1135.0)
    # 3 the hype -------------------------------------------------------------------------------------------
    S(PART[3] - 0.05, "spot7", 1484.0, tr="leak"); chapter(PART[3] + 0.3, "02", "The Hype")
    S(a("that broke peter norman"), "fan_jun100h", 18.6, slow=0.6)
    O(a("that broke peter norman") + 0.5, 4.2, ("title", "Australian record · since 1968", "20.06 → 20.04"))
    S(a("faster than usain bolt"), "bolt_guardian", 8.0, tr="whip")
    S(a("a couple months before"), "nova", 300.0)
    S(a("and just like that"), "fan_1000b", 17.6, slow=0.7)
    # 4 the wind -------------------------------------------------------------------------------------------
    S(PART[4] - 0.05, "fan_qld200s", 1.0, slow=0.5, tr="leak"); chapter(PART[4] + 0.3, "03", "The Wind")
    O(a("every last one") - 13.0, 14.5, ("board", "Every sub-10 / sub-20 before 2026", B(
        ("100m · Dec 2024", "10.04", "+3.4 wind", 1), ("200m · Mar 2025", "19.98", "+3.4 wind", 1),
        ("100m · Apr 2025", "9.99", "+3.5 wind", 1), ("100m · Apr 2025", "9.99", "+2.6 wind", 1),
        ("200m · Apr 2025", "19.84", "+2.2 wind", 1)), "Legal limit: +2.0 · all run in Australia"))
    # 5 overseas -------------------------------------------------------------------------------------------
    S(PART[5] - 0.05, "brown_cbc", 91.0, tr="leak")
    O(a("czech republic") - 1.0, 3.6, ("title", "Ostrava · June 2025 · wind 0.0", "20.02 · legal"))
    S(a("but at the world championships"), "aw_tokyo", 30.0, bw=1)
    O(a("but at the world championships") + 0.8, 4.4, ("title", "World Championships · Tokyo 2025", "20.23 heat · 20.36 semi · out"))
    # 6 the 10.00 -----------------------------------------------------------------------------------------------
    S(PART[6] - 0.05, "fan_1000a", 3.0, tr="leak"); chapter(PART[6] + 0.2, "04", "The 10 Flat")
    O(a("his first race of the year") + 0.3, 5.0, ("clock", 0.0, "Brisbane · Feb 21, 2026 · wind +0.9", 1.0, 10.0))
    S(a("legal but look"), "fan_1000b", 17.6, slow=0.6)
    S(a("six of the"), "fan_qld200s", 1.0, bw=1)
    O(a("six of the") + 0.2, 4.0, ("title", "Same meet · 49 wind readings", "6 over the legal limit"))
    S(a("the rest of the season"), "fan_qld100f", 5.7, crop=C_CAP, tr="whip")
    O(a("the rest of the season") + 0.3, 7.0, ("board", "100m · rest of 2026", B(
        ("Brisbane · Feb", "10.00", "+0.9", 1), ("QLD Champs · Mar", "10.20", "+1.5", 0), ("Juniors heat · Apr", "10.19", "+0.3", 0),
        ("Juniors semi · Apr", "10.44", "-2.2", 0), ("Juniors final · Apr", "10.21", "+0.5", 0)), ""))
    S(a("he aint never came close"), "fan_jun100f", 11.5, slow=0.7)
    # 7 the 200 ------------------------------------------------------------------------------------------------
    S(PART[7] - 0.05, "fan_qld200f", 16.5, crop=C_CAP, tr="leak")
    S(a("and he said he was sick"), "fan_qld200f", 29.0, crop=C_CAP)
    S(a("in the rain"), "fan_qld200s", 17.0, bw=1, slow=0.7)
    O(a("in the rain") + 0.3, 4.2, ("title", "Maurie Plant Meet · Melbourne", "Kennedy 20.38 · Gout 20.43"))
    S(a("so going into nationals"), "fan_qld200f", 20.0, crop=C_CAP, slow=0.6)
    # 8 Sydney -------------------------------------------------------------------------------------------------
    S(PART[8] - 0.05, "fan_heat1", 3.0, tr="leak"); chapter(PART[8] + 0.2, "05", "Sydney")
    S(a("in the morning heat"), "fan_heat1", 16.0, slow=0.8)
    O(a("in the morning heat") + 0.1, 2.2, ("clock", 0.0, "Morning heat · wind +0.4", 1.0, 20.11))
    S(a("that night in the final"), F67, 17.8, crop=C_CAP, slow=0.6, tr="whip")
    O(a("that night in the final") + 0.4, 5.0, ("gap", "Final · night", 19.67, "Heat · morning", 20.11, "0.44 seconds", "Same day · same track"))
    S(a("and look at the mens final"), "fan_heat2", 16.0, bw=1)
    O(a("dudes ran a personal best") - 0.6, 9.5, ("board", "Men's 200m final · 7 of 8 ran PBs", B(
        ("Gout Gout", "19.67", "PB · heat 20.11", 1), ("Aidan Murphy", "19.88", "PB · old best 20.41", 1), ("Calab Law", "20.21", "PB", 1),
        ("Christopher Ius", "20.26", "PB", 1), ("Archer McHugh", "20.37", "PB", 1), ("Rory Easton", "20.37", "PB", 1)),
        "Wind +1.7 · women's 200m final just before: +2.3"))
    S(a("and every single dude"), F67, 40.0, crop=C_CAP)
    # 9 the other side -----------------------------------------------------------------------------------------
    S(PART[9] - 0.05, "emerole_fl", 2281.0, tr="leak"); chapter(PART[9] + 0.2, "06", "The Other Side")
    S(a("nobody ever reported"), F67, 37.7, crop=C_CAP, slow=0.7)
    S(a("and aiden murphy went"), "fan_murphy_oce", 15.0)
    S(a("two months later in oslo"), "citius_oslo", 8.0, bw=1, tr="whip")
    O(a("two months later in oslo") + 0.4, 3.8, ("title", "Oslo · June 10, 2026 · Diamond League debut", "20.60 · 6th"))
    S(a("then in july"), "citius_season", 99.0)
    # 10 the question ------------------------------------------------------------------------------------------
    S(PART[10] - 0.05, F67, 96.0, crop=C_CAP, slow=0.6, bw=1, tr="leak")
    O(a("but take away that") + 0.3, 4.6, ("wipe", ["Outside Sydney:", "never under 20 legal"], ""))
    O(a("his next best legal") - 0.2, 9.0, ("board", "His 200m races, 2026", B(
        ("QLD Champs semi · Mar", "20.59", "+0.9", 0), ("QLD Champs final · Mar", "20.42", "-2.1", 0), ("Maurie Plant · Mar", "20.43", "2nd", 0),
        ("Sydney heat · Apr", "20.11", "+0.4", 0), ("Sydney final · Apr", "19.67", "+1.7", 1), ("Oslo · Jun", "20.60", "6th", 0)),
        "Next-best legal 200m ever: 20.02 (Ostrava 2025)"))
    S(a("his next best legal"), "fan_qld200f", 18.0, crop=C_CAP, bw=1)
    S(a("so tell me how a dude"), F67, 22.0, crop=C_CAP, slow=0.45)
    # 11 verdict -----------------------------------------------------------------------------------------------
    S(PART[11] - 0.05, "nova", 1300.0, tr="leak")
    O(a("is gout gout really") + 0.1, 6.5, ("wipe", ["Australia's fastest man ever?", "Or one perfect day?"], ""))
    S(a("or did one perfect day"), F67, 96.0, crop=C_CAP, slow=0.6)
    S(a("let me know"), "btr_lyles", 4018.0)

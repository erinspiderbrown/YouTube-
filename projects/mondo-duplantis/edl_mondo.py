"""Mondo Duplantis: soundbites + EDL in the modern style (tools/modern.py: date, number, name, title, quote, chapter).
Footage rules (user, 20 Nov 2026): no Olympic footage (Olympics channel / NBC / Olympic broadcasts), no FloTrack/MileSplit,
fan-shot/re-uploads first.
No Diamond League footage (user, 20 Nov 2026): nothing from the Wanda Diamond League channel or its interview feed, and no TV-broadcast
re-uploads from Diamond League meets; fan/phone clips from the stands and independent outlets' own interviews only. Paris 2024 (6.25) and Karalis's Olympic bronze are graphics only, over non-Olympic footage.
Clips: scratchpad/mondo/clips (INDEX.md). Soundbite times come from scratchpad/mondo/tx/*.json."""

TAGS = {
    "stock_trackoholic": "Stockholm Diamond League 2026 · re-upload",
    "stock_lemon": "Stockholm Diamond League 2026 · re-upload",
    "stock_reaction_stt": "Stockholm 2026 · Sports Talk Tech",
    "stock_dl_interview": "Wanda Diamond League · June 2026",
    "stock_citius_marschall": "CITIUS MAG · June 2026",
    "london_citius": "CITIUS MAG · London, July 2026",
    "paris_613": "Paris Diamond League 2026 · re-upload",
    "monaco_607": "Wanda Diamond League · Monaco 2026",
    "euros_2026": "European Championships · Birmingham 2026",
    "laus_mondo621": "Lausanne 2026 · Sports Passion",
    "laus_karalis616_ig": "Lausanne 2026 · via Emmanouil Karalis",
    "laus_citius_karalis": "CITIUS MAG · Lausanne 2026",
    "zur_karalis620_ig": "Zurich 2026 · via Emmanouil Karalis",
    "zur_karalis620_pvs": "Zurich 2026 · Pole Vault Science",
    "zur_citius_mondo": "CITIUS MAG · Zurich 2026",
    "zur_rs_mondo": "RunnerSpace · Zurich 2026",
    "zur_citius_karalis": "CITIUS MAG · Zurich 2026",
    "bru_aw_mondo": "Athletics Weekly · Brussels 2026",
    "bru_karalis612_ig": "Brussels 2026 · via Emmanouil Karalis",
    "bru_karalis612_reup": "Brussels 2026 · re-upload",
    "bru_dl_karalis": "Wanda Diamond League · Brussels 2026",
    "bud_reup": "Ultimate Championship · Budapest 2026 · re-upload",
    "bud_citius_mondo": "CITIUS MAG · Budapest 2026",
    "bud_aw_karalis": "Athletics Weekly · 2026",
    "wr621": "6.21 · Eugene 2022 · Fan video · Jacob Thompson",
    "wr623": "6.23 · Prefontaine Classic 2023 · Fan video · Joe Edwards",
    "wr624": "6.24 · Xiamen 2024 · Wanda Diamond League",
    "wr626": "6.26 · Silesia 2024 · Wanda Diamond League",
    "wr628_pvs": "6.28 · Stockholm 2025 · Pole Vault Science",
    "wr628_fan": "6.28 · Stockholm 2025 · Fan video",
    "wr630_dan78": "6.30 · Tokyo 2025 · from the stands · dan78",
    "wr630_hoot": "6.30 · Tokyo 2025 · Team Hoot Pole Vault",
    "wr631": "6.31 · Uppsala 2026 (indoor) · Pole Vault Science",
    "young_mondo": "Born to Fly · Brennan Robideaux",
    "young_mondo_pt2": "Born to Fly · Brennan Robideaux",
    "young_mondo_prodigy": "Born to Fly · Brennan Robideaux",
    "karalis_profile": "SPORT24 · Greece",
    "karalis_fail": "Jumpman",
    "wedding": "Expressen",
    "wedding_proposal": "Vogue Scandinavia · 2024",
}

# cold open: Mondo, minutes after the Stockholm loss
PRE_SB = ("stock_reaction_stt", 23.0, 38.1, "Mondo Duplantis · Stockholm, June 7, 2026 · Sports Talk Tech")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("four summers in a row", 2), "wr630_dan78", 36.5, 42.5, "6.30 · Tokyo 2025 · from the stands"),
    (("ill let y all decide", 4), "bud_citius_mondo", 275.1, 277.5, "Mondo Duplantis · CITIUS MAG · Budapest, September 2026"),
    (("sam kendrick wins", 5), "london_citius", 16.1, 21.8, "Mondo Duplantis · CITIUS MAG · London, July 2026"),
    (("so who wins a trophy", 5), "bru_aw_mondo", 8.3, 15.8, "Mondo Duplantis · Athletics Weekly · Brussels, September 2026"),
    (("and here go the crazy part", 6), "zur_citius_karalis", 66.5, 74.4, "Emmanouil Karalis · CITIUS MAG · Zurich, August 2026"),
    (("and then brussels", 7), "zur_citius_karalis", 13.8, 21.1, "Emmanouil Karalis · CITIUS MAG · Zurich, August 2026"),
    (("now lets keep it real", 8), "bud_aw_karalis", 110.5, 115.9, "Emmanouil Karalis · Athletics Weekly · September 2026"),
    (("and heres the thing", 8), "zur_citius_mondo", 52.0, 62.9, "Mondo Duplantis · CITIUS MAG · Zurich, August 2026"),
    (("so imagine when", 8), "laus_citius_karalis", 48.4, 57.9, "Emmanouil Karalis · CITIUS MAG · Lausanne, August 2026"),
    (("in luzon the gap", 8), "bud_aw_karalis", 93.1, 97.3, "Emmanouil Karalis · Athletics Weekly · September 2026"),
    (("his body needs to recover", 9), "bud_citius_mondo", 282.0, 293.4, "Mondo Duplantis · CITIUS MAG · Budapest, September 2026"),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    TR, DL = "stock_trackoholic", "stock_dl_interview"
    # 1 Stockholm ------------------------------------------------------------------------
    S(PART[1] - 0.05, "wr628_fan", 0.5, flash=1); date(a("june 7th"), 3.2, "June 7, 2026", "Diamond League · Stockholm")
    S(a("stockholm sweden"), "wr628_fan", 4.0)
    S(a("his home meet"), "stock_reaction_stt", 3.0)
    S(a("his family in the stands"), "wr623", 66.0)
    S(a("for almost three years"), "wr621", 22.0, slow=0.6)
    S(a("forty meets in a row"), "wr630_dan78", 6.0); number(a("forty meets in a row"), 3.0, "40", "Meets in a row without a loss", "July 2023 – June 2026")
    S(a("nobody touched him"), "wr623", 54.0)
    S(a("and tonight"), "wr628_fan", 7.0)
    S(a("cant get over six meters"), "stock_reaction_stt", 15.0, bw=1)
    S(a("curtis marshall from australia"), "stock_citius_marschall", 20.0); name(a("curtis marshall from australia"), 2.8, "Kurtis Marschall", "Australia")
    number(a("clears 590"), 2.8, "5.90", "Kurtis Marschall", "Winning height")
    S(a("mondo is stuck at"), "stock_reaction_stt", 34.0, bw=1); number(a("mondo is stuck at"), 2.8, "5.80", "Mondo Duplantis", "2nd place · at home")
    S(a("he lost at home"), "stock_citius_marschall", 60.0, bw=1)
    S(a("and that wasnt the last time"), "london_citius", 60.0)
    S(a("so is this the beginning"), "bud_reup", 36.0, slow=0.7)
    S(a("greatest pole vaulter"), "wr630_dan78", 40.0)
    S(a("a man from greece"), "zur_karalis620_pvs", 7.0)
    S(a("waiting on this moment"), "karalis_profile", 75.0)
    # 2 the streak -----------------------------------------------------------------------
    S(PART[2] - 0.05, "young_mondo", 13.0, flash=1); chapter(PART[2] + 0.2, "01", "The Streak")
    S(a("you gotta understand what mondo"), "young_mondo", 113.0)
    S(a("broke the world record for the first time"), "young_mondo_prodigy", 56.0); number(a("in 2020"), 3.0, "6.17", "First world record", "February 2020 · age 20")
    S(a("he was 20 years old"), "young_mondo_pt2", 104.0)
    S(a("he just kept going"), "young_mondo_prodigy", 30.0)
    S(a("one centimeter at a time"), "young_mondo_pt2", 58.0)
    S(a("every time he breaks it"), "wr631", 137.0)
    S(a("people say thats on purpose"), "wr631", 11.0)
    S(a("july 24 2022"), "wr621", 2.0, flash=1); date(a("july 24 2022"), 3.0, "July 24, 2022", "World Championships · Eugene")
    S(a("world championships eugene"), "wr621", 12.0)
    number(a("eugene six 21"), 2.6, "6.21", "World record", "Eugene · 2022"); S(a("world record 2023"), "wr621", 21.5, slow=0.6)
    S(a("2023 prefontaine"), "wr623", 6.0)
    S(a("six 23 world record"), "wr623", 39.0); number(a("six 23 world record"), 2.4, "6.23", "World record", "Prefontaine Classic · 2023")
    S(a("2024 xiamen"), "wr623", 78.0); number(a("six 24 then"), 2.2, "6.24", "World record", "Xiamen · April 2024")
    S(a("then the olympic final in paris"), "young_mondo_prodigy", 47.0); number(a("then the olympic final in paris"), 2.4, "6.25", "World record", "Paris Olympics · August 2024")
    S(a("then in poland"), "wr621", 26.0); number(a("then in poland"), 2.2, "6.26", "World record", "Silesia · August 2024")
    S(a("2025 stockholm"), "wr628_fan", 3.0); number(a("2025 stockholm"), 2.2, "6.28", "World record", "Stockholm · June 2025")
    S(a("budapest six 29"), "wr628_fan", 6.0); number(a("budapest six 29"), 2.2, "6.29", "World record", "Budapest · August 2025")
    S(a("and in tokyo"), "wr630_dan78", 20.0)
    S(a("world championships six 30"), "wr630_dan78", 30.0); number(a("world championships six 30"), 2.6, "6.30", "World record", "Tokyo · September 2025")
    S(a("four summers in a row"), "wr630_dan78", 56.0); title(a("four summers in a row"), 3.2, "Outdoor world records", "2022 · 2023 · 2024 · 2025")
    S(a("every single summer"), "wr631", 158.0)
    S(a("in 2025 he didnt lose"), "wr623", 90.0)
    S(a("sixteen meet sixteen wins"), "wr630_dan78", 90.0); number(a("sixteen meet sixteen wins"), 2.8, "16–0", "2025 season", "Unbeaten")
    # 3 the summer it stopped ------------------------------------------------------------
    S(PART[3] - 0.05, "wr631", 116.0, flash=1); chapter(PART[3] + 0.2, "02", "The Summer It Stopped")
    S(a("he did set a record"), "wr631", 137.0); number(a("march 631"), 3.0, "6.31", "World record · indoors", "Uppsala · March 2026")
    S(a("but that was indoors"), "wr631", 95.0)
    S(a("the outdoor season is what"), "paris_613", 25.0)
    S(a("outdoors this year he tried"), "laus_mondo621", 19.0); number(a("he tried 632"), 2.6, "6.32", "World record attempt", "Missed")
    S(a("zurich missed"), "zur_rs_mondo", 10.0)
    S(a("budapest missed"), "bud_reup", 25.0)
    S(a("ultimate championships missed"), "bud_reup", 5.0)
    S(a("his best jump all summer"), "bud_reup", 36.0); number(a("his best jump all summer"), 2.8, "6.25", "Best outdoor jump of 2026", "Zurich · August 2026")
    S(a("so for the first time since 2021"), "bud_citius_mondo", 57.0, bw=1)
    S(a("a whole outdoor season"), "paris_613", 36.0, bw=1)
    S(a("did not break the world record"), "bud_reup", 56.0, bw=1); title(a("did not break the world record"), 3.0, "No outdoor world record", "First summer since 2021")
    # 4 the wedding ----------------------------------------------------------------------
    S(PART[4] - 0.05, "wedding_proposal", 17.0, flash=1); chapter(PART[4] + 0.2, "03", "The Wedding")
    S(a("five days after that loss"), "stock_reaction_stt", 40.0, bw=1)
    S(a("got married"), "wedding", 9.0)
    date(a("june 12th"), 3.0, "June 12, 2026", "Wedding · South of France"); S(a("a big wedding"), "wedding_proposal", 28.0)
    S(a("his long time girlfriend"), "wedding_proposal", 40.0); name(a("his long time girlfriend"), 3.0, "Desiré Inglander", "Engaged in 2024")
    S(a("right after the loss"), "stock_reaction_stt", 22.0)
    S(a("now y all know what they say"), "wedding_proposal", 51.0)
    S(a("the hunger changes"), "wedding_proposal", 62.0)
    S(a("is this what happened"), "wedding_proposal", 74.0, bw=1)
    S(a("or is this just a coincidence"), "wedding", 24.0)
    S(a("he said himself he felt unfocused"), "stock_reaction_stt", 28.0)
    S(a("and he skipped the very next"), "wedding", 17.0)
    S(a("ill let y all decide"), "wedding_proposal", 85.0)
    # 5 the leg --------------------------------------------------------------------------
    S(PART[5] - 0.05, "london_citius", 9.0, flash=1); date(PART[5] + 0.1, 3.0, "July 2026", "Diamond League · London")
    number(a("clears 595"), 2.6, "5.95", "London Diamond League", "Then he stopped")
    S(a("then something just doesnt feel right"), "london_citius", 44.0, bw=1)
    S(a("in his left thigh"), "london_citius", 79.0)
    S(a("sam kendrick wins"), "london_citius", 114.0); name(a("sam kendrick wins"), 2.6, "Sam Kendricks", "USA · won London")
    S(a("mundo is second again"), "london_citius", 131.0, bw=1)
    S(a("then september"), "bru_aw_mondo", 2.0, flash=1); date(a("then september"), 3.0, "September 4, 2026", "Diamond League Final · Brussels")
    S(a("the trophy he had won"), "young_mondo_prodigy", 39.0); number(a("five years in a row"), 2.6, "5", "Straight Diamond League titles", "2021–2025")
    S(a("hes warming up"), "bru_aw_mondo", 20.0)
    S(a("he pulls out"), "bru_aw_mondo", 40.0, bw=1)
    S(a("so who wins a trophy"), "bru_karalis612_reup", 1.0)
    S(a("the man from greece"), "bru_karalis612_reup", 4.0, slow=0.7)
    # 6 the man from Greece --------------------------------------------------------------
    S(PART[6] - 0.05, "karalis_profile", 40.0, flash=1); chapter(PART[6] + 0.2, "04", "The Man From Greece")
    name(a("his name is") + 0.6, 3.2, "Emmanouil Karalis", "Greece · \"Manolo\"")
    S(a("everybody calls him manolo"), "zur_citius_karalis", 11.0)
    S(a("hes from athens"), "karalis_profile", 160.0); date(a("born october"), 3.0, "October 20, 1999", "Born · Athens, Greece")
    S(a("thats three weeks before mondo"), "young_mondo", 13.0)
    S(a("same age"), "karalis_profile", 250.0)
    S(a("theyve been jumping against each other"), "karalis_fail", 105.0)
    S(a("his dad was a decathlete"), "karalis_profile", 120.0)
    S(a("and here go the crazy part"), "karalis_fail", 175.0, punch=0.5)
    S(a("2018 world indoors"), "young_mondo_prodigy", 39.0); number(a("2018 world indoors"), 3.0, "5.80", "Karalis beat Mondo (5.70)", "2018 World Indoors · both 18")
    S(a("but after that"), "karalis_profile", 210.0, bw=1)
    S(a("2022 world championships he didnt"), "karalis_fail", 175.0, bw=1); number(a("22nd"), 2.6, "22nd", "2022 World Championships", "Out in qualifying")
    S(a("2022 europeans"), "laus_citius_karalis", 30.0, bw=1); title(a("2022 europeans"), 2.8, "2022 European Championships", "Out in qualifying")
    S(a("2023 world championships"), "karalis_profile", 280.0, bw=1); title(a("he didnt clear a single bar"), 3.0, "2023 World Championships", "No height")
    S(a("he got all the talent"), "zur_karalis620_pvs", 20.0)
    S(a("he disappears"), "karalis_profile", 230.0, bw=1)
    # 7 the build ------------------------------------------------------------------------
    S(PART[7] - 0.05, "karalis_fail", 175.0, flash=1); chapter(PART[7] + 0.2, "05", "The Build")
    S(a("2024 pairs"), "karalis_fail", 105.0); title(a("2024 pairs"), 2.8, "2024 Olympics · Paris", "Bronze")
    S(a("world championships in tokyo"), "wr630_dan78", 81.0); title(a("world championships in tokyo"), 2.8, "2025 World Championships · Tokyo", "Silver · behind Mondo")
    S(a("right behind mondo"), "wr630_dan78", 56.0)
    S(a("and this year"), "karalis_profile", 75.0)
    S(a("then august and lausanne"), "laus_karalis616_ig", 1.0); number(a("then august and lausanne") + 1.0, 2.6, "6.16", "Karalis", "Lausanne · August 20, 2026")
    S(a("that same night"), "laus_mondo621", 2.0); number(a("that same night"), 2.6, "6.21", "Mondo", "Same night")
    S(a("first time in history"), "laus_karalis616_ig", 2.0, slow=0.6); title(a("first time in history"), 3.0, "First time ever", "Two men over 6.16 in one competition")
    S(a("one week later zurich"), "zur_karalis620_pvs", 2.0); date(a("one week later zurich"), 2.6, "August 27, 2026", "Weltklasse · Zurich")
    S(a("carlis clear"), "zur_karalis620_ig", 3.0, slow=0.6); number(a("carlis clear"), 3.0, "6.20", "Karalis · Greek record", "No. 2 all-time")
    S(a("that makes him the second best"), "zur_karalis620_pvs", 24.0)
    S(a("then he even took three tries"), "zur_citius_karalis", 34.0); number(a("then he even took three tries"), 2.8, "6.32", "Karalis's first world-record attempts", "Zurich · 3 misses")
    S(a("and then brussels"), "bru_karalis612_ig", 1.0)
    S(a("mondos hurt"), "bru_aw_mondo", 50.0, bw=1)
    S(a("wins his first diamond league trophy"), "bru_karalis612_ig", 4.0, slow=0.7); number(a("a meet record"), 2.8, "6.12", "Meet record", "First Diamond League trophy")
    # 8 the gap --------------------------------------------------------------------------
    S(PART[8] - 0.05, "bud_reup", 5.0, flash=1); chapter(PART[8] + 0.2, "06", "The Gap")
    S(a("mondo still won every championship"), "euros_2026", 8.0)
    S(a("world indoors"), "euros_2026", 10.0); title(a("world indoors"), 3.4, "2026 championships · all won by Mondo", "World Indoors · Europeans · Ultimate")
    S(a("ultimate championships carlis"), "bud_reup", 15.0)
    S(a("hasnt beaten him since 2018"), "bud_reup", 66.0)
    S(a("but look at who came second"), "bud_reup", 46.0)
    S(a("carlis every time"), "bud_aw_karalis", 30.0); title(a("carlis every time"), 3.0, "Runner-up to Mondo every time", "World Indoors 6.05 · Europeans 6.00 · Ultimate 6.15")
    S(a("and heres the thing"), "zur_citius_karalis", 100.0)
    S(a("still aint consistent"), "karalis_fail", 175.0, bw=1)
    S(a("at europeans this year"), "euros_2026", 5.0)
    S(a("the same month he jumped"), "zur_karalis620_pvs", 10.0)
    S(a("he could only clear six meters"), "euros_2026", 2.0, bw=1); number(a("he could only clear six meters"), 2.8, "6.00", "Karalis at the Europeans", "Weeks before 6.16 and 6.20")
    S(a("early this season"), "karalis_profile", 100.0, bw=1); title(a("seventh at shanghai"), 3.0, "Early 2026", "7th Shanghai · 4th Oslo")
    S(a("he said himself he wasnt believing"), "laus_citius_karalis", 40.0)
    S(a("so imagine when he figures"), "zur_karalis620_pvs", 28.0, slow=0.7)
    S(a("shows up at a championship"), "zur_karalis620_ig", 3.0)
    S(a("in luzon the gap"), "laus_mondo621", 28.0); number(a("in luzon the gap"), 2.6, "5 cm", "Lausanne", "Mondo 6.21 · Karalis 6.16")
    S(a("in zurich five centimeters"), "zur_karalis620_pvs", 15.0); number(a("in zurich five centimeters"), 2.6, "5 cm", "Zurich", "Mondo 6.25 · Karalis 6.20")
    # 9 the question ---------------------------------------------------------------------
    S(PART[9] - 0.05, "bud_citius_mondo", 19.0, flash=1); chapter(PART[9] + 0.2, "07", "The End?")
    S(a("in october mondo announced"), "bud_citius_mondo", 94.0); date(a("in october"), 3.0, "October 2, 2026", "Skipping the 2027 indoor season")
    S(a("he said he had too much going on"), "bud_citius_mondo", 132.0)
    S(a("his body needs to recover"), "london_citius", 79.0, bw=1)
    S(a("dont get it twisted"), "wr630_dan78", 40.0, slow=0.7)
    S(a("still the best in the world"), "wr623", 42.0)
    S(a("hes 27"), "wr631", 11.0); number(a("he still holds the world record"), 3.0, "6.31", "World record", "Mondo Duplantis")
    S(a("might come back in 2027"), "wr630_dan78", 68.0)
    S(a("but for the first time in his career"), "stock_reaction_stt", 10.0, bw=1)
    S(a("hes lost more than"), "stock_reaction_stt", 28.0, bw=1)
    S(a("the world record didnt fall"), "bud_reup", 56.0, bw=1)
    S(a("a man from greece standing right there"), "zur_karalis620_pvs", 30.0)
    S(a("is this the end of mondo"), "bud_reup", 36.0, slow=0.6)
    S(a("or is carlis about to find out"), "bru_karalis612_ig", 4.0)
    S(a("wake up a champion"), "laus_karalis616_ig", 6.0)
    S(a("let me know down below"), "wr630_dan78", 81.0)

"""Michael Norman: soundbites + EDL (cinematic step-up: tools/modern.py + tools/cinema.py, speed ramps, depth-pull photos).
Footage: Jordan Testerman + Evan Barnes (HS fan video), Times of San Diego (Mt. SAC 2019), Gary George / Inland Valley News,
LetsRun, CITIUS MAG, Walter Dix (LetsRun), The Erin Brown (Aug 2021 prediction), Wikimedia Commons photos (jenaragon94 CC BY 2.0,
Phil Roeder CC BY 2.0). No NBC/NCAA/ESPN/FloTrack/MileSplit/RunnerSpace/Olympic/Diamond League/World Athletics video.
Avoid: cif2016_barnes 86-92 s and 113-119 s (burned captions), hs_timetrial (other athletes). All soundbite times word-checked
against tx/*.json (small.en); raw."""

PH = "Photo · jenaragon94 · CC BY 2.0"
TAGS = {
    "cif2015_400": "2015 CIF State Meet · Jordan Testerman", "cif2016_barnes": "2016 CIF State Meet · Evan Barnes",
    "arcadia2016": "2016 Arcadia Invitational · Jordan Testerman", "mtsac_tosd": "Times of San Diego · Mt. SAC Relays 2019",
    "mtsac_testerman": "Mt. SAC Relays 2019 · Jordan Testerman", "mtsac_fan": "Mt. SAC Relays 2019 · fan video",
    "mtsac_interviews": "Inland Valley News · Mt. SAC 2019", "letsrun_trials2016": "LetsRun · 2016 Olympic Trials",
    "dix_college": "LetsRun · 2016 Olympic Trials", "letsrun_doha": "LetsRun · Doha 2019", "citius_gold2022": "CITIUS MAG · Eugene 2022",
    "letsrun_gold2022": "LetsRun · Eugene 2022", "letsrun_100m2023": "LetsRun · USAs 2023", "citius_100m2023": "CITIUS MAG · USAs 2023",
    "citius_comeback2024": "CITIUS MAG · May 2024", "citius_trials_r1_2024": "CITIUS MAG · 2024 Olympic Trials",
    "citius_trials_final2024": "CITIUS MAG · 2024 Olympic Trials", "citius_surgery2026": "CITIUS MAG · April 2026",
    "erin_tokyo_prediction": "The Erin Brown · August 2021",
    "ph_p00": PH, "ph_p01": PH, "ph_p02": PH, "ph_p03": PH, "ph_p04": PH, "ph_p05": PH, "ph_p06": PH, "ph_p07": PH,
    "ph_p08": PH, "ph_p09": PH, "ph_p10": PH, "ph_p11": PH, "ph_p18": PH, "ph_p12": "Photo · Phil Roeder · CC BY 2.0",
}

# cold open: 18-year-old Norman, 2016 Trials: "What do you think you're capable of?" "I have no idea. I guess the time will only tell."
PRE_SB = ("letsrun_trials2016", 334.95, 342.20, "Michael Norman, age 18 · LetsRun · 2016 Olympic Trials")
R = {"raw": 1}
T16 = "letsrun_trials2016"
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("and now hes 28", 1), "mtsac_interviews", 102.10, 108.40, "Michael Norman after 43.45 · Inland Valley News · April 2019", R),
    (("liles finished fourth", 2), T16, 47.40, 60.30, "Michael Norman, age 18 · LetsRun · 2016 Olympic Trials", R),
    (("and here go the difference", 3), T16, 276.30, 293.10, "Michael Norman on skipping college · LetsRun · 2016", R),
    (("michael norman went to college", 3), "dix_college", 21.40, 30.95, "Walter Dix, Olympic medalist · LetsRun · 2016", R),
    (("and honestly i cant even", 3), T16, 240.20, 263.45, "Michael Norman on choosing USC · LetsRun · 2016", R),
    (("then he signed with nike", 3), "dix_college", 41.20, 54.85, "Walter Dix · LetsRun · 2016", R),
    (("this is one of the fastest", 4), "mtsac_interviews", 87.10, 99.55, "Michael Norman · Inland Valley News · Mt. SAC 2019", R),
    (("then in tokyo", 5), "letsrun_doha", 0.00, 10.95, "Michael Norman after the semifinal · LetsRun · Doha 2019", R),
    (("then in tokyo", 5), "letsrun_doha", 16.75, 21.15, "Michael Norman · LetsRun · Doha 2019", R),
    (("no medal", 5), "erin_tokyo_prediction", 391.05, 400.40, "The Erin Brown · before the Tokyo final · August 2021", R),
    (("but i feel like we gotta", 6), "citius_gold2022", 3.40, 17.60, "Michael Norman, world champion · CITIUS MAG · 2022", R),
    (("so yeah he got gold", 6), "citius_gold2022", 101.70, 113.60, "Michael Norman · CITIUS MAG · Eugene 2022", R),
    (("it was one of the slowest", 6), "citius_gold2022", 50.20, 61.80, "Michael Norman · CITIUS MAG · Eugene 2022", R),
    (("he leaves his coach", 7), "letsrun_100m2023", 5.30, 9.70, "Michael Norman · LetsRun · USAs 2023", R),
    (("he didnt even run the 400", 7), "letsrun_100m2023", 73.80, 81.50, "Michael Norman · LetsRun · USAs 2023", R),
    (("so the world champion in the 400", 7), "citius_comeback2024", 286.70, 298.35, "Michael Norman on 2023 · CITIUS MAG · May 2024", R),
    (("then he comes back", 8), "citius_100m2023", 100.30, 121.30, "Michael Norman · CITIUS MAG · USAs 2023", R),
    (("but he said before", 8), "citius_trials_final2024", 6.45, 8.40, "Michael Norman, 2nd · CITIUS MAG · 2024 Olympic Trials", R),
    (("but he said before", 8), "citius_trials_final2024", 30.80, 42.40, "Michael Norman · CITIUS MAG · 2024 Olympic Trials", R),
    (("and then in paris", 8), "citius_comeback2024", 143.00, 155.75, "Michael Norman, May 2024 · CITIUS MAG", R),
    (("and then in paris", 8), "citius_trials_final2024", 207.90, 213.00, "Michael Norman · CITIUS MAG · June 2024", R),
    (("this year he came back", 9), "citius_surgery2026", 46.05, 63.45, "Michael Norman on 2024 · CITIUS MAG · April 2026", R),
    (("this year he came back", 9), "citius_surgery2026", 72.05, 91.10, "Michael Norman on his surgery · CITIUS MAG · 2026", R),
    (("he won some smaller", 9), "citius_surgery2026", 13.90, 20.55, "Michael Norman, first race back · CITIUS MAG · April 2026", R),
    (("he won a 400", 9), "citius_surgery2026", 103.85, 126.50, "Michael Norman on his new coach · CITIUS MAG · 2026", R),
    (("every time its a global", 10), T16, 75.30, 83.95, "Michael Norman, age 18 · LetsRun · 2016", R),
    (("the talent is there", 10), "letsrun_doha", 84.95, 92.45, "Michael Norman · LetsRun · Doha 2019", R),
    (("he got more talent", 10), T16, 175.95, 183.20, "Michael Norman, age 18 · LetsRun · 2016", R),
    (("and thats the thing about", 10), "citius_comeback2024", 98.85, 116.75, "Michael Norman · CITIUS MAG · May 2024", R),
    (("then you gotta do it again", 10), "citius_gold2022", 264.60, 267.62, "Michael Norman · CITIUS MAG · 2022", R),
    (("she was a sprinter", 11), T16, 96.95, 123.70, "Michael Norman on his parents · LetsRun · 2016", R),
    (("i aint gonna say", 12), "citius_surgery2026", 142.80, 157.00, "Michael Norman · CITIUS MAG · April 2026", R),
    (("or is he going to come back", 12), "citius_surgery2026", 205.70, 214.45, "Michael Norman · CITIUS MAG · April 2026", R),
]

SPLIT_AT = {"and here go the difference": 69.6}   # whisper puts "And" late here; split in the measured pause (68.3-70.9 s)

TS = "mtsac_tosd"; TE = "mtsac_testerman"; MF = "mtsac_fan"; MI = "mtsac_interviews"; C15 = "cif2015_400"; C16 = "cif2016_barnes"
AR = "arcadia2016"; DX = "dix_college"; DO = "letsrun_doha"; G22 = "citius_gold2022"; L22 = "letsrun_gold2022"; L23 = "letsrun_100m2023"
C23 = "citius_100m2023"; CB = "citius_comeback2024"; R1 = "citius_trials_r1_2024"; TF = "citius_trials_final2024"; S26 = "citius_surgery2026"
EP = "erin_tokyo_prediction"
def P(n): return f"ph_p{n:02d}"

GLOBAL = [("Doha", "2019", "Out in semi", "bad"), ("Tokyo", "2021", "5th", "bad"), ("Eugene", "2022", "Gold", "good"),
          ("Budapest", "2023", "Skipped", "none"), ("Paris", "2024", "8th", "bad"), ("USAs", "2026", "No final", "bad")]
def tracker(O, t, upto, dur=4.2): O(t, dur, ("tracker", "Global championships · 400m", GLOBAL, upto, upto))
def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open --------------------------------------------------------------------------------
    S(PART[1] - 0.05, TS, 40.0, flash=1, ramp=(2.5, 0.4)); lb(O, PART[1], 12.0)
    title(a("michael norman might") + 0.3, 3.4, "The Tragic Downfall Of", "Michael Norman")
    S(a("this dude opened up"), TS, 86.0, punch=0.3); number(a("running 43") + 0.1, 3.2, "43.45", "400m · season opener", "Mt. SAC · April 20, 2019")
    S(a("and people was really"), TS, 60.0, slow=0.5)
    S(a("and now hes 28"), CB, 300.0, bw=1)
    S(a("he finished dead last"), P(12), 0.0, bw=1); tracker(O, a("he finished dead last"), 4, 3.6)
    S(a("he missed a whole year"), S26, 60.0, bw=1)
    S(a("in this summer"), TF, 60.0, bw=1)
    S(a("so how do you go"), TS, 307.0, slow=0.6)
    S(a("lets jump into it"), TS, 34.0, ramp=(0.8, 0.35))
    # 2 high school ------------------------------------------------------------------------------
    S(PART[2] - 0.05, C16, 97.0, flash=1); chapter(PART[2] + 0.2, "01", "The Prodigy"); lb(O, PART[2], 3.4)
    S(a("2016 olympic trials"), P(1), 0.0); date(a("2016 olympic trials"), 2.8, "July 2016", "Olympic Trials · 200m · Eugene")
    S(a("and there was two"), P(0), 0.0); O(a("noah liles"), 3.2, ("scope", 300, 470, "Michael Norman", "Vista Murrieta HS · age 18"))
    S(a("liles finished fourth"), P(3), 0.0)
    S(a("and norman was fifth"), P(2), 0.0, punch=0.4); number(a("running 20") + 0.1, 3.0, "20.14", "200m · Olympic Trials final", "5th · as a high schooler")
    S(a("two kids from high school"), P(4), 0.0)
    S(a("in the year before"), C15, 30.0); date(a("in the year before"), 2.6, "June 2015", "CIF State Meet · Clovis, California")
    S(a("norman ran 45"), C15, 48.0, ramp=(1.2, 0.45)); number(a("in the 400") , 3.2, "45.19", "400m · national HS record (tied)", "CIF State Meet · 2015")
    S(a("and he ran like seven"), C16, 20.0)
    S(a("so both of them"), AR, 12.0)
    # 3 the difference -----------------------------------------------------------------------------
    S(PART[3] - 0.05, P(18), 0.0, flash=1); chapter(PART[3] + 0.2, "02", "The Choice")
    S(a("noah laws turned pro"), T16, 300.0)
    O(a("noah laws turned pro") - 0.2, 6.5, ("versus", ("Noah Lyles", "Turned pro out of high school"), ("Michael Norman", "Went to USC"),
      [("2016 Trials 200m", "4th", "5th"), ("First pro season", "2016", "2018")], "Same final. Two paths."))
    S(a("michael norman went to college"), P(5), 0.0)
    S(a("he went to usc"), P(6), 0.0)
    S(a("and honestly i cant even"), P(7), 0.0)
    S(a("because he did really well"), P(5), 3.0, punch=0.3); number(a("he ran 44") + 0.1, 3.0, "44.52", "400m indoors · world best", "NCAA Indoors · March 2018")
    S(a("and then at the ncaa"), P(8), 0.0); number(a("he ran 43") + 0.1, 3.0, "43.61", "400m · collegiate record", "World lead · June 2018")
    S(a("he won a bowman"), P(9), 0.0); title(a("he won a bowman"), 3.0, "2018", "The Bowerman Award")
    S(a("then he signed with nike"), P(12), 0.0)
    S(a("everything was going"), P(10), 0.0)
    # 4 2019 --------------------------------------------------------------------------------------
    S(PART[4] - 0.05, TS, 12.0, flash=1, ramp=(1.2, 0.4)); chapter(PART[4] + 0.2, "03", "43.45"); lb(O, PART[4], 3.4)
    S(a("his very first 400"), TE, 8.0, amb=1); date(a("his very first 400"), 2.6, "April 20, 2019", "Mt. SAC Relays · Torrance, California")
    S(a("he runs 43"), TS, 52.0, ramp=(1.0, 0.35), punch=0.6)
    S(a("as a season opener"), TS, 86.0)
    S(a("this is one of the fastest"), TS, 130.0)
    S(a("only a few men"), TS, 248.0)
    S(a("then he ran 1970"), P(11), 0.0)
    O(a("then he ran 1970") - 0.1, 5.6, ("board", "Michael Norman · the speed", [("100m", "9.86", "2020", 0), ("200m", "19.70", "2019", 0), ("400m", "43.45", "2019", 1)], "Under 10 · under 20 · under 44"))
    S(a("and the only man"), TS, 270.0)
    S(a("so everybody was saying"), TS, 305.0, slow=0.6)
    # 5 the chokes --------------------------------------------------------------------------------
    S(PART[5] - 0.05, DO, 30.0, flash=1, bw=1); chapter(PART[5] + 0.2, "04", "The First Choke"); lb(O, PART[5], 3.4)
    S(a("2019 world championships"), DO, 40.0, bw=1); date(a("2019 world championships"), 2.8, "October 2019", "World Championships · Doha")
    S(a("hes the favorite"), DO, 60.0)
    S(a("he basically shut it down"), DO, 100.0, bw=1, slow=0.6); tracker(O, a("he basically shut it down"), 0, 4.4)
    S(a("then in tokyo"), EP, 260.0)
    S(a("he makes the final"), P(11), 0.0, bw=1)
    S(a("and then he faced"), EP, 420.0); tracker(O, a("and then he faced"), 1, 4.2)
    S(a("no medal"), TS, 60.0, bw=1, slow=0.5)
    S(a("he never ran faster"), TS, 86.0, bw=1)
    O(a("he never ran faster") + 0.4, 4.6, ("counter", 0, 2776, "days since his personal best", "43.45 · April 20, 2019"))
    S(a("and dont come at me"), DO, 130.0)
    S(a("so the year opened up"), TS, 300.0, bw=1)
    S(a("and at this point"), P(12), 0.0, bw=1)
    # 6 2022 --------------------------------------------------------------------------------------
    S(PART[6] - 0.05, G22, 120.0, flash=1); chapter(PART[6] + 0.2, "05", "The Gold"); lb(O, PART[6], 3.4)
    S(a("he won the world title"), G22, 140.0); date(a("he won worlds"), 2.8, "July 2022", "World Championships · Eugene")
    number(a("with a 44") + 0.1, 3.0, "44.29", "400m · world champion", "Eugene · July 22, 2022"); tracker(O, a("with a 44") + 3.2, 2, 3.4)
    S(a("honest 44"), L22, 20.0)
    O(a("honest 44") - 0.1, 6.2, ("board", "World Championship 400m winning times", [("2013", "43.74", "Merritt", 0), ("2015", "43.48", "van Niekerk", 0), ("2017", "43.98", "van Niekerk", 0), ("2019", "43.48", "Gardiner", 0), ("2022", "44.29", "Norman", 1)], "Slowest winning time since 2011"))
    S(a("and karani james"), L22, 50.0); number(a("running 44 4") + 0.1, 2.8, "44.48", "Kirani James · silver", "0.19 behind")
    S(a("and thats the olympic champion"), G22, 160.0)
    S(a("so yeah he got gold"), G22, 200.0)
    S(a("but it wasnt the dominant"), TS, 60.0, slow=0.6)
    S(a("it was one of the slowest"), G22, 230.0)
    # 7 2023 --------------------------------------------------------------------------------------
    S(PART[7] - 0.05, L23, 30.0, flash=1); chapter(PART[7] + 0.2, "06", "The Switch"); lb(O, PART[7], 3.4)
    S(a("he switches to the 100"), C23, 30.0); date(a("he switches to the 100"), 2.6, "2023", "Switches to the 100m")
    S(a("he leaves his coach"), L23, 50.0); name(a("goes to john smith"), 2.8, "John Smith", "New coach · 2023")
    S(a("and usa is"), C23, 60.0, bw=1)
    S(a("and he doesnt even make"), L23, 90.0, bw=1)
    S(a("he didnt even run the 400"), C23, 80.0, bw=1); tracker(O, a("he didnt even run the 400") + 0.3, 3, 4.0)
    S(a("so the world champion in the 400"), CB, 270.0, bw=1)
    # 8 Paris -------------------------------------------------------------------------------------
    S(PART[8] - 0.05, R1, 10.0, flash=1); chapter(PART[8] + 0.2, "07", "Paris"); lb(O, PART[8], 3.4)
    S(a("2024 olympic trials"), TF, 20.0); date(a("2024 olympic trials"), 2.6, "June 2024", "Olympic Trials · Eugene")
    number(a("his second 4441") + 0.3, 2.8, "44.41", "2nd · Olympic Trials", "Makes the team for Paris")
    S(a("but he said before"), R1, 40.0)
    S(a("and then in paris"), TF, 120.0, bw=1)
    S(a("he made the final"), CB, 30.0, bw=1, slow=0.6); lb(O, a("he made the final") - 0.2, 7.0)
    number(a("dead last") + 0.2, 3.0, "8th", "Olympic 400m final · Paris 2024", "45.62 · last"); tracker(O, a("dead last") + 3.4, 4, 3.6)
    S(a("meanwhile noah laws"), T16, 52.0)
    O(a("meanwhile noah laws") - 0.1, 6.0, ("versus", ("Noah Lyles", "Turned pro in 2016"), ("Michael Norman", "Went to USC"),
      [("Paris 2024", "Olympic 100m gold", "8th, 400m final"), ("Individual world titles", "4+", "1")], "Same 2016 Trials final"))
    S(a("then norman didnt race"), S26, 40.0, bw=1)
    S(a("in 2025 he had surgery"), S26, 70.0, bw=1); title(a("in 2025 he had surgery"), 3.0, "2025", "Surgery · no races")
    S(a("it was a pelvis"), S26, 150.0, bw=1)
    # 9 2026 --------------------------------------------------------------------------------------
    S(PART[9] - 0.05, S26, 5.0, flash=1); chapter(PART[9] + 0.2, "08", "The Comeback?")
    S(a("he won some smaller"), S26, 100.0); title(a("he won a 400"), 2.8, "May 2026", "Wins the 400m · LA Track Festival")
    S(a("so it looked like"), S26, 180.0)
    S(a("but then at usas"), S26, 200.0, bw=1); date(a("but then at usas"), 2.6, "July 2026", "USA Championships · not in the final"); tracker(O, a("but then at usas") + 2.8, 5, 3.8)
    S(a("the world champion from 2022"), TS, 307.0, bw=1, slow=0.5)
    # 10 soft mentally ----------------------------------------------------------------------------
    S(PART[10] - 0.05, DO, 150.0, flash=1); chapter(PART[10] + 0.2, "09", "Soft?"); lb(O, PART[10], 4.0)
    S(a("i feel like michael norman"), DO, 155.0)
    S(a("every time its a global"), T16, 80.0)
    S(a("he gets hurt"), DO, 100.0, bw=1)
    S(a("he shut it down"), L23, 100.0, bw=1)
    S(a("the talent is there"), TS, 60.0, slow=0.5)
    S(a("he got more talent"), TS, 280.0)
    S(a("he cant hold up"), TF, 100.0)
    S(a("and thats the thing about"), G22, 260.0)
    S(a("every year at usa"), TF, 300.0)
    S(a("and you gotta beat"), L22, 30.0)
    S(a("then you gotta do it again"), G22, 270.0)
    # 11 Japan ------------------------------------------------------------------------------------
    S(PART[11] - 0.05, P(4), 0.0, flash=1); chapter(PART[11] + 0.2, "10", "The Hot Take"); lb(O, PART[11], 3.4)
    S(a("his mom is from japan"), T16, 110.0)
    S(a("she was a sprinter"), P(2), 0.0)
    S(a("and i really feel like"), TS, 280.0)
    S(a("japan never had"), TS, 60.0, slow=0.6); number(a("japan never had") + 0.2, 3.0, "0", "Japanese men under 44.0", "in the 400m · ever")
    S(a("so he would have been the man"), P(10), 0.0)
    S(a("no killers at the trials"), MI, 120.0)
    S(a("way less pressure"), TS, 290.0)
    S(a("im not saying"), P(8), 0.0)
    # 12 verdict ----------------------------------------------------------------------------------
    S(PART[12] - 0.05, TS, 305.0, flash=1, bw=1); chapter(PART[12] + 0.2, "11", "Wasted?"); lb(O, PART[12], 14.0)
    S(a("because when you look"), TS, 86.0, bw=1)
    O(a("turned out 4345") - 0.3, 4.2, ("board", "The talent", [("100m", "9.86", "", 0), ("200m", "19.70", "", 0), ("400m", "43.45", "", 1)], ""))
    S(a("he had the speed"), TS, 52.0, bw=1, slow=0.5)
    S(a("global championships he was"), P(12), 0.0, bw=1); tracker(O, a("global championships he was"), 5, 7.5)
    S(a("i aint gonna say"), S26, 160.0, bw=1)
    S(a("was he ever gonna"), DO, 120.0, bw=1)
    S(a("so yall tell me"), TS, 307.0, slow=0.6)
    S(a("or is he going to come back"), S26, 190.0)
    S(a("yall let me know"), P(0), 0.0, slow=0.7)

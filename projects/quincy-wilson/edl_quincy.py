"""Quincy Wilson (27 Nov 2026): soundbites + EDL. Cloned voice (A3b + dialect opener), own score W1-W6.
Footage (no NBC/Peacock, Olympic, World Athletics, Diamond League, FloTrack/MileSplit, RunnerSpace, NCAA/conference, USATF feeds):
fan video from the stands (2024 Trials 44.66 + 44.59 by Seth Jenny Athletics, 44.10 in Memphis, Penn Relays 2023/2024),
his own channel ("The Decision"), CITIUS MAG mixed-zone interviews, Sports Stars of Tomorrow (family), WJLA, WUSA9, FOX 5 DC,
Maryland Athletics. No usable Paris footage exists outside NBC/Olympic feeds: Paris is told with photos/interviews."""

TAGS = {
    "fan_trials4466": "2024 Olympic Trials · fan video · Seth Jenny Athletics", "fan_trials4459": "2024 Olympic Trials · fan video · Seth Jenny Athletics",
    "fan_4410": "Memphis, July 2025 · fan video · RunnnSphere", "fan_penn24final": "Penn Relays · fan video · Hairston Media",
    "fan_penn24prelim": "Penn Relays · fan video · Angelo Clark", "fan_penn23": "Penn Relays 2023 · fan video",
    "fan_arcadia26": "Arcadia Invitational 2026 · Erik Boal Sports", "own_decision": "Quincy Wilson · The Decision",
    "sst_family": "Sports Stars of Tomorrow", "wjla_int": "WJLA · 7News DC", "wusa_penn26": "WUSA9 · April 2026",
    "wusa_prank": "WUSA9", "fox5_commit": "FOX 5 DC · November 2025", "umd_bmitch": "Maryland Athletics",
    "cit_4459": "CITIUS MAG · 2024 Olympic Trials", "cit_lee_tears": "CITIUS MAG · 2024 Olympic Trials",
    "cit_penn24": "CITIUS MAG · Penn Relays 2024", "cit_4466": "CITIUS MAG · 2024 Olympic Trials",
}

R = {"raw": 1}
# cold open: Quincy after breaking the 42-year-old record for the second time
PRE_SB = ("cit_4459", 13.40, 24.60, "Quincy Wilson, 16, after his 44.59 · CITIUS MAG · 2024 Olympic Trials")
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("his dad roy", 2), "own_decision", 507.42, 522.18, "Quincy Wilson · The Decision"),
    (("he started running when", 3), "sst_family", 146.92, 159.20, "Quincy Wilson · Sports Stars of Tomorrow"),
    (("he started running when", 3), "sst_family", 188.64, 203.06, "Joe Lee, Bullis coach · Sports Stars of Tomorrow"),
    (("then come the 2024", 4), "sst_family", 41.84, 54.62, "Quincy Wilson · Sports Stars of Tomorrow"),
    (("he made the final", 4), "cit_4459", 46.84, 53.24, "Quincy Wilson · CITIUS MAG"),
    (("and whats crazy is", 4), "cit_lee_tears", 140.63, 156.77, "Joe Lee · CITIUS MAG · 2024 Olympic Trials"),
    (("but team usa put him", 5), "cit_lee_tears", 249.11, 266.73, "Joe Lee · CITIUS MAG · 2024 Olympic Trials"),
    (("in august", 5), "wjla_int", 97.54, 119.64, "Quincy Wilson on the call · WJLA"),
    (("and then 2025", 6), "sst_family", 254.76, 265.32, "Quincy Wilson on Paris · Sports Stars of Tomorrow"),
    (("then his senior year", 8), "own_decision", 1037.89, 1059.97, "Quincy Wilson commits to Maryland · The Decision"),
    (("and now he got somebody", 8), "wusa_penn26", 37.79, 42.67, "Quincy Wilson · WUSA9 · Penn Relays 2026"),
    (("so where is he headed", 10), "sst_family", 203.48, 219.42, "Quincy Wilson · Sports Stars of Tomorrow"),
    (("and the big one is", 11), "own_decision", 145.0, 164.0, "Quincy Wilson · The Decision"),
    (("so i want to hear", 11), "sst_family", 340.66, 358.44, "Quincy Wilson · Sports Stars of Tomorrow"),
]
SPLIT_AT = {}

T6 = "fan_trials4466"; T9 = "fan_trials4459"; M10 = "fan_4410"; PF = "fan_penn24final"; PP = "fan_penn24prelim"; P23 = "fan_penn23"
AR = "fan_arcadia26"; DEC = "own_decision"; SS = "sst_family"; WJ = "wjla_int"; WP = "wusa_penn26"; WK = "wusa_prank"; FX = "fox5_commit"
UM = "umd_bmitch"; C9 = "cit_4459"; LT = "cit_lee_tears"; CP = "cit_penn24"; C6 = "cit_4466"


def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 open ----------------------------------------------------------------------------------------
    S(PART[1] - 0.05, T6, 60.0, flash=1); lb(O, PART[1], 9.0)
    title(PART[1] + 0.8, 3.4, "Olympic gold at 16 · fastest high schooler ever", "Quincy Wilson")
    S(a("sixteen years old"), WK, 31.0)
    S(a("and he came home"), T9, 80.0, slow=0.6)
    S(a("at 17 he ran"), M10, 33.0, slow=0.6)
    number(a("at 17 he ran") + 1.0, 3.0, "44.10", "400m at 17", "Fastest high schooler ever")
    S(a("and now this little dude"), UM, 150.0)
    S(a("a kid that fast"), M10, 140.0)
    S(a("so im gonna break down"), T6, 87.0, slow=0.6)
    # 2 military kid ---------------------------------------------------------------------------------
    S(PART[2] - 0.05, SS, 122.0, flash=1); chapter(PART[2] + 0.2, "01", "Military Kid"); lb(O, PART[2], 3.4)
    date(a("quincy was born") + 0.3, 3.0, "January 8, 2008", "New London, Connecticut")
    S(a("his dad roy"), SS, 318.0)
    S(a("so they moved around"), SS, 171.0)
    S(a("his mom monique"), SS, 269.0)
    S(a("and they actually moved"), SS, 360.0)
    S(a("run for coach"), LT, 26.0)
    # 3 early records --------------------------------------------------------------------------------
    S(PART[3] - 0.05, DEC, 242.0, flash=1); chapter(PART[3] + 0.2, "02", "Before The Hype"); lb(O, PART[3], 3.4)
    S(a("in july 2022"), P23, 41.0)
    number(a("in july 2022") + 1.0, 3.2, "47.59", "400m at 14 · July 2022", "Breaks Obea Moore's 30-year-old age record")
    S(a("then at 15"), DEC, 403.0)
    S(a("so before he even"), DEC, 564.0)
    # 4 Trials --------------------------------------------------------------------------------------
    S(PART[4] - 0.05, T6, 30.0, flash=1); chapter(PART[4] + 0.2, "03", "The Trials"); lb(O, PART[4], 3.4)
    S(a("hes 16 running against"), T6, 47.0)
    S(a("in the first round"), T6, 60.0, slow=0.6)
    number(a("in the first round") + 1.2, 3.2, "44.66", "400m · Olympic Trials round 1", "High school record")
    S(a("that broke darrell"), T6, 74.0)
    O(a("that broke darrell") + 0.5, 4.2, ("board", "US high school 400m record", [("Darrell Robinson", "44.69", "1982", 0), ("Quincy Wilson", "44.66", "June 21, 2024", 1)], "42 years"))
    S(a("then two days later"), T9, 60.0)
    number(a("then two days later") + 2.4, 3.0, "44.59", "Olympic Trials semifinal", "Broke it again · age 16")
    S(a("he made the final"), T9, 112.0)
    S(a("and his coach joe lee"), LT, 140.0)
    S(a("and whats crazy is"), T9, 117.0, slow=0.7)
    # 5 Paris ---------------------------------------------------------------------------------------
    S(PART[5] - 0.05, WK, 18.0, flash=1); chapter(PART[5] + 0.2, "04", "Paris"); lb(O, PART[5], 3.4)
    S(a("and his coach really pranked"), WK, 43.0)
    S(a("in august"), WK, 31.0, slow=0.8)
    number(a("in august") + 2.4, 3.2, "16y 214d", "Youngest US male track Olympian", "Passes Jim Ryun")
    S(a("he led off the"), SS, 220.0)
    S(a("team usa won the final"), SS, 360.0)
    S(a("since he ran the"), FX, 198.0)
    S(a("sixteen years old with olympic"), WK, 18.0, slow=0.7)
    # 6 2025 ---------------------------------------------------------------------------------------
    S(PART[6] - 0.05, PF, 94.0, flash=1); chapter(PART[6] + 0.2, "05", "Takeoff"); lb(O, PART[6], 3.4)
    S(a("at the penn relays he anchored"), PF, 132.0)
    number(a("thats a high schooler") - 0.2, 3.0, "43.99", "4x400 anchor split · Penn Relays 2025", "Bullis 3:06.31 · national high school record")
    S(a("he took a l"), PP, 125.0)
    S(a("at new balance nationals"), PP, 54.0)
    S(a("and he still went out"), PP, 89.0, slow=0.7)
    # 7 44.10 + Maryland ----------------------------------------------------------------------------
    S(PART[7] - 0.05, M10, 11.0, flash=1); chapter(PART[7] + 0.2, "06", "44.10"); lb(O, PART[7], 3.4)
    S(a("in memphis he ran"), M10, 33.0, slow=0.6)
    number(a("in memphis he ran") + 1.2, 3.4, "44.10", "Memphis · July 12, 2025", "High school + U18 world record")
    S(a("thats the high school record"), M10, 78.0)
    S(a("and just to put that"), M10, 100.0, slow=0.7)
    S(a("he did it at"), M10, 123.0)
    S(a("and in november"), FX, 40.0)
    S(a("texas am south carolina"), FX, 278.0)
    S(a("and he picked maryland"), FX, 436.0)
    # 8 senior year + the rival ----------------------------------------------------------------------
    S(PART[8] - 0.05, WP, 53.0, flash=1); chapter(PART[8] + 0.2, "07", "Senior Year"); lb(O, PART[8], 3.4)
    S(a("at the penn relays bullis won"), WP, 74.0)
    title(a("at the penn relays bullis won") + 0.6, 3.2, "Penn Relays 2026 · Championship of America", "Bullis 3:10.15 · first US boys win in 19 years")
    S(a("and he anchored it"), WP, 117.0)
    S(a("and now he got somebody"), AR, 22.0)
    name(a("theres another kid") + 0.6, 3.0, "Jayden DeLeon", "Montgomery Blair HS · signed with LSU")
    S(a("quincy beat him indoors"), AR, 112.0)
    O(a("quincy beat him indoors") + 0.3, 9.0, ("versus", ("Quincy Wilson", "Bullis · Maryland"), ("Jayden DeLeon", "Montgomery Blair · LSU"),
       [("NB Indoor Nationals · March", "45.37", "45.38"), ("World U20 final · Eugene · August", "44.62", "44.47")], "4x400 gold together"))
    S(a("and 2 days later"), AR, 201.0)
    S(a("quincy still running"), AR, 291.0)
    # 9 never seen this ------------------------------------------------------------------------------
    S(PART[9] - 0.05, M10, 140.0, flash=1); chapter(PART[9] + 0.2, "08", "Never Seen This"); lb(O, PART[9], 3.4)
    S(a("quincy did it in high school"), SS, 360.0)
    S(a("and now he walking into college"), UM, 60.0)
    S(a("a lot of the best"), T9, 20.0, slow=0.6)
    # 10 where he's headed -------------------------------------------------------------------------
    S(PART[10] - 0.05, UM, 150.0, flash=1); chapter(PART[10] + 0.2, "09", "Maryland"); lb(O, PART[10], 3.4)
    S(a("he close to home"), FX, 516.0)
    S(a("the college record"), T6, 74.0, slow=0.6)
    O(a("the college record") + 0.4, 4.4, ("board", "NCAA 400m record", [("Michael Norman", "43.61", "2018", 0), ("Quincy Wilson", "44.10", "PB at 17", 1)], "0.49 away"))
    S(a("give him a couple years"), DEC, 242.0)
    # 11 LA 2028 ------------------------------------------------------------------------------------
    S(PART[11] - 0.05, T6, 87.0, flash=1, slow=0.5); chapter(PART[11] + 0.2, "10", "LA 2028"); lb(O, PART[11], 20.0)
    O(a("he gonna be 20") + 0.2, 3.8, ("counter", 16, 20, "years old at LA 2028", "Olympic gold at 16 · next shot at 20"))
    S(a("last time he went"), WK, 31.0)
    S(a("next time i think"), M10, 150.0, slow=0.7)
    S(a("so i want to hear"), M10, 160.0)
    S(a("can he come through"), AR, 336.0)

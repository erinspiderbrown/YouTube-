"""Noah Lyles fall-off (26 Nov 2026): soundbites + EDL. Cloned voice (A3b + dialect opener), own score N1-N7.
Footage (no NBC/Peacock, Olympic, World Athletics, Diamond League, FloTrack, RunnerSpace, ESPN, USATF feeds): fan video from the
stands (Paris 2024 100 final, Tokyo 2025 200 final, 2016 Trials heat, Tokyo close-ups), Noah's own channel (training, depression
short, 400m opener), his Instagram post via CITIUS, CITIUS MAG / LetsRun mixed-zone interviews, CGTN, AP, USA TODAY, his podcast
Beyond The Records. The Budapest press-conference audio plays over B-roll (WA backdrop). fan_tokyo200 has cartoon watermarks in the
bottom corners: always cropped (CROPS)."""

TAGS = {
    "fan_paris100": "Paris 2024 · fan video from the stands", "fan_tokyo200": "Tokyo 2025 · fan video from the stands",
    "fan_trials16": "2016 Olympic Trials · fan video · Seth Jenny Athletics", "fan_kame": "Tokyo 2025 · fan video",
    "fan_close": "Tokyo 2025 · fan video", "own_training": "Noah Lyles · Trackside Diaries", "own_400": "Noah Lyles · own channel",
    "own_depression": "Noah Lyles · own channel", "cit_ig_end": "Noah Lyles on Instagram · via CITIUS MAG", "cit_pullup": "CITIUS MAG · 2026 USAs",
    "cit_979": "CITIUS MAG · 2026 USAs", "cit_indoor3rd": "CITIUS MAG · 2026 USA Indoors", "cit_kaalund": "CITIUS MAG · 2026 USAs",
    "cit_thompson": "CITIUS MAG · 2025", "lr_anthony": "LetsRun · 2026 USA Indoors", "lr_2016": "LetsRun · 2016 Olympic Trials",
    "cgtn_empty": "CGTN Sports Scene · Tokyo 2025", "ap_mom": "AP · August 2024", "usat_dep": "USA TODAY · 2021",
    "btr_covid": "Beyond The Records podcast", "pc_budapest": "Budapest 2023 press conference · JoyNews",
}

R = {"raw": 1}
# cold open: his own Instagram video ending the 2026 season
PRE_SB = ("cit_ig_end", 0.55, 11.90, "Noah Lyles on Instagram · September 4, 2026")
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("so ima ask", 1), "ap_mom", 0.0, 9.10, "Noah Lyles · AP · August 2024", R),
    (("and instead of going", 2), "lr_2016", 105.52, 119.34, "Noah Lyles, 18 · LetsRun · 2016 Olympic Trials"),
    (("but the one thing that keep", 4), "pc_budapest", 495.60, 515.10, "Noah Lyles · Budapest 2023 press conference",
     dict(raw=1, vsrc="own_training", vss=430.0, quote="World champion of what? The United States?", who="Noah Lyles on NBA champions, Budapest 2023")),
    (("but on the track", 4), "own_depression", 17.38, 37.80, "Noah Lyles · own channel"),
    (("and noah left that track", 5), "ap_mom", 124.0, 134.34, "Noah Lyles after the Paris 200 · AP"),
    (("so two olympics", 5), "btr_covid", 456.20, 468.14, "Noah Lyles · Beyond The Records podcast"),
    (("and then 2026", 8), "cgtn_empty", 34.87, 49.39, "Noah Lyles after his 4th world 200 title · CGTN · Tokyo 2025"),
    (("then at usas in july", 8), "lr_anthony", 35.54, 54.36, "Jordan Anthony, 2026 US 60m champion · LetsRun"),
    (("but 2 days later", 8), "cit_979", 4.78, 7.82, "Noah Lyles after his 9.79 · CITIUS MAG"),
    (("would usually run in his sleep", 8), "cit_kaalund", 44.86, 69.28, "Garrett Kaalund, 2026 US 200m champion · CITIUS MAG"),
    (("then in september", 9), "cit_pullup", 0.0, 15.70, "Noah Lyles after pulling up · CITIUS MAG · July 2026"),
    (("so he skipped", 9), "cit_ig_end", 16.86, 54.54, "Noah Lyles on Instagram · September 4, 2026"),
    (("but i do think his prime", 10), "cit_kaalund", 151.76, 168.56, "Garrett Kaalund · CITIUS MAG"),
    (("so yall tell me", 11), "ap_mom", 158.24, 173.56, "Noah Lyles · AP · August 2024"),
]
SPLIT_AT = {}

PA = "fan_paris100"; TK = "fan_tokyo200"; T16 = "fan_trials16"; KM = "fan_kame"; FC = "fan_close"; TR = "own_training"; O4 = "own_400"
DP = "own_depression"; IG = "cit_ig_end"; PU = "cit_pullup"; C9 = "cit_979"; IN = "cit_indoor3rd"; KA = "cit_kaalund"; TH = "cit_thompson"
LA = "lr_anthony"; L16 = "lr_2016"; CG = "cgtn_empty"; AP = "ap_mom"; UD = "usat_dep"; BT = "btr_covid"

def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open -----------------------------------------------------------------------------------
    S(PART[1] - 0.05, TK, 210.0, flash=1); lb(O, PART[1], 9.0)
    S(a("one of the greatest"), PA, 50.0, slow=0.5)
    title(PART[1] + 0.6, 3.2, "8-time world champion · Olympic champion", "Noah Lyles")
    S(a("top six or seven"), FC, 5.0)
    S(a("dude got world titles"), TK, 225.0)
    S(a("he got the american record"), TR, 40.0)
    S(a("but this year"), IN, 40.0, bw=1)
    S(a("he pulled up in the 200"), KA, 20.0, bw=1)
    S(a("and then he shut"), IG, 20.0, bw=1)
    S(a("and the one thing he want"), PA, 20.0, slow=0.6)
    S(a("he still aint"), PA, 25.0, slow=0.6)
    # 2 the kid -------------------------------------------------------------------------------------
    S(PART[2] - 0.05, T16, 0.0, flash=1); chapter(PART[2] + 0.2, "01", "The Kid"); lb(O, PART[2], 3.4)
    date(a("2016 olympic trials"), 2.8, "July 2016", "US Olympic Trials · Eugene")
    S(a("and he make the 200 final"), T16, 8.0, slow=0.7)
    number(a("fourth in") + 0.2, 3.0, "20.09", "200m · 4th at the Olympic Trials", "High school record")
    S(a("a high school record"), L16, 10.0)
    S(a("everybody knew"), L16, 130.0)
    # 3 the run -------------------------------------------------------------------------------------
    S(PART[3] - 0.05, TR, 90.0, flash=1); chapter(PART[3] + 0.2, "02", "The Face Of The Sport"); lb(O, PART[3], 3.4)
    S(a("2019 in doha"), TR, 140.0); title(a("2019 in doha") + 0.3, 2.8, "Doha 2019", "First world 200m title")
    S(a("then in 2022"), O4, 50.0)
    number(a("and break michael") - 0.6, 3.2, "19.31", "200m · American record", "Breaks Michael Johnson's 19.32 (1996)")
    S(a("a record that been sitting"), TR, 600.0, slow=0.7)
    S(a("and in 2023 in budapest"), TR, 1200.0)
    O(a("he won the 100") - 0.3, 4.2, ("board", "Budapest 2023 · world titles", [("100m", "9.83", "Gold", 1), ("200m", "19.52", "Gold", 1), ("4x100m", "37.38", "Gold", 1)], "First since Usain Bolt in 2015"))
    S(a("at that point"), FC, 2.0, slow=0.8)
    S(a("and he was talking like it"), FC, 15.0)
    # 4 the Olympic 200 -----------------------------------------------------------------------------
    S(PART[4] - 0.05, UD, 20.0, flash=1); chapter(PART[4] + 0.2, "03", "The One Race"); lb(O, PART[4], 3.4)
    S(a("tokyo 2021"), UD, 60.0, bw=1); title(a("tokyo 2021") + 0.2, 2.8, "Tokyo 2021", "200m bronze · the favorite")
    S(a("and he get bronze"), UD, 120.0, bw=1)
    S(a("and he was real open"), UD, 95.0)
    S(a("and i respect him"), DP, 40.0)
    # 5 Paris ---------------------------------------------------------------------------------------
    S(PART[5] - 0.05, PA, 8.0, flash=1); chapter(PART[5] + 0.2, "04", "Paris"); lb(O, PART[5], 3.4)
    S(a("he won the"), PA, 30.0)
    S(a("he beat"), PA, 44.0, slow=0.4); number(a("five thousandths") - 0.2, 3.2, "0.005", "Paris 100m · Lyles 9.784, Thompson 9.789", "Olympic champion")
    S(a("olympic champion"), PA, 20.0, slow=0.6)
    S(a("but then the 200"), PA, 40.0, bw=1)
    S(a("he tests positive"), AP, 85.0, bw=1)
    S(a("run anyway"), PA, 12.0, bw=1, slow=0.6)
    name(a("won it in") - 0.5, 2.8, "Letsile Tebogo", "200m Olympic champion · 19.46")
    S(a("and noah left that track"), PA, 50.0, bw=1, slow=0.6)
    O(a("so two olympics") + 0.2, 4.2, ("board", "Olympic 200m", [("Tokyo 2021", "19.74", "Bronze", 0), ("Paris 2024", "19.70", "Bronze", 0)], "Still no gold in his event"))
    # 6 the one he's missing ------------------------------------------------------------------------
    S(PART[6] - 0.05, TK, 240.0, flash=1); chapter(PART[6] + 0.2, "05", "Zero"); lb(O, PART[6], 3.4)
    S(a("yeah he got the 100 gold"), PA, 55.0, slow=0.6)
    S(a("thats the race he built"), TK, 260.0)
    O(a("usain bolt won") + 0.2, 4.0, ("board", "Olympic 200m golds", [("Usain Bolt", "3", "2008 · 2012 · 2016", 1), ("Noah Lyles", "0", "Bronze · Bronze", 0)], ""))
    S(a("noah got zero"), FC, 20.0, bw=1, slow=0.7)
    S(a("and when you trying"), TR, 1500.0)
    # 7 2025 ----------------------------------------------------------------------------------------
    S(PART[7] - 0.05, TR, 1700.0, flash=1); chapter(PART[7] + 0.2, "06", "The Cracks"); lb(O, PART[7], 3.4)
    S(a("in may he pulled"), TR, 1800.0, bw=1); title(a("in may he pulled") + 0.3, 2.8, "May 2025", "Out of his opener · tight ankle")
    S(a("now to be fair"), FC, 8.0, slow=0.7)
    S(a("his 4th straight"), TK, 280.0); number(a("his 4th straight") + 0.2, 3.0, "4", "Straight world 200m titles", "Tokyo 2025 · ties Usain Bolt")
    S(a("but in the 100"), TH, 60.0)
    S(a("and after the 200"), FC, 25.0, slow=0.7)
    quote(a("he said that himself") - 2.4, 3.4, "Nothing will ever fill that empty feeling.", "Noah Lyles, Tokyo 2025")
    # 8 2026 ----------------------------------------------------------------------------------------
    S(PART[8] - 0.05, IN, 20.0, flash=1); chapter(PART[8] + 0.2, "07", "2026"); lb(O, PART[8], 3.4)
    S(a("us indoors in march"), IN, 90.0); number(a("finished 3rd") + 0.2, 2.8, "3rd", "US Indoors 60m", "Jordan Anthony 6.45 · Lyles 6.51")
    S(a("his own training partner"), LA, 5.0)
    S(a("then at usas in july"), C9, 30.0); number(a("so the speed") - 0.8, 2.8, "9.79", "100m · US champion", "July 2026")
    S(a("but 2 days later"), C9, 80.0, bw=1)
    S(a("his event he pull up"), KA, 30.0, bw=1)
    S(a("garrett"), KA, 120.0); name(a("garrett") + 0.2, 2.6, "Garrett Kaalund", "US 200m champion · 20.04")
    # 9 the end of the season -----------------------------------------------------------------------
    S(PART[9] - 0.05, PU, 20.0, flash=1); chapter(PART[9] + 0.2, "08", "Done For The Year"); lb(O, PART[9], 3.4)
    S(a("then in september"), IG, 30.0, bw=1)
    S(a("a small strain"), IG, 40.0, bw=1)
    S(a("so he skipped"), TR, 1900.0, bw=1); title(a("so he skipped") + 0.4, 3.0, "September 2026", "Misses Budapest · $150,000 first prize")
    S(a("thats noah lyles"), FC, 10.0, slow=0.7)
    S(a("missing the biggest"), TK, 300.0, bw=1)
    # 10 my take ------------------------------------------------------------------------------------
    S(PART[10] - 0.05, TR, 2000.0, flash=1); chapter(PART[10] + 0.2, "09", "My Take"); lb(O, PART[10], 3.4)
    S(a("he still ran"), C9, 100.0)
    S(a("he 29 now"), TR, 2100.0)
    S(a("the injuries keep"), PU, 10.0, bw=1)
    S(a("and the young boys"), TH, 200.0)
    S(a("they all faster"), TH, 400.0)
    S(a("and that 200 olympic"), PA, 22.0, slow=0.6)
    O(a("he only got one more") + 0.2, 4.4, ("counter", 0, 31, "years old at LA 2028", "One more shot at the Olympic 200"))
    S(a("and he gonna be 31"), TK, 320.0)
    # 11 verdict ------------------------------------------------------------------------------------
    S(PART[11] - 0.05, FC, 14.0, flash=1); chapter(PART[11] + 0.2, "10", "The Verdict"); lb(O, PART[11], 12.0)
    S(a("top six or seven all-time"), TK, 330.0)
    S(a("but if he never get"), PA, 55.0, slow=0.6, bw=1)
    S(a("people gonna always say"), FC, 28.0, slow=0.7)
    S(a("so yall tell me"), TR, 2150.0)
    S(a("come back healthy"), TR, 2200.0, slow=0.7)

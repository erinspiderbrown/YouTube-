"""Cooper Lutkenhaus: soundbites + EDL ("He's Still In High School... And He's A World Champion" / will he fall off?).
Voice: Erin Brown 2026 clone (vo_cooper.mp3). Cinematic layer: tools/modern.py + tools/cinema.py.
Footage: fan video from the stands at 2025 USAs (Cooper Lutkenhaus's own channel; Mark & Kathryn), TRACK: All-Access workouts,
LetsRun + CITIUS MAG interviews. No NBC/USATF broadcast, FloTrack/MileSplit, RunnerSpace, Diamond League, World Athletics or
Olympic video; 2026 Diamond League races are told with interviews + graphics only.
Avoid: mk_u18wr 0-6 s and 115-122 s (burned captions). Soundbite times word-checked with small.en word timestamps (win.py)."""

TAGS = {
    "own_usa25": "2025 USAs · fan video · Cooper Lutkenhaus", "mk_u18wr": "2025 USAs · fan video · Mark & Kathryn",
    "tao_workout25": "TRACK: All-Access · April 2025", "tao_firstworkout": "TRACK: All-Access · August 2025",
    "tao_wcworkout": "TRACK: All-Access · March 2026", "lr_after142": "LetsRun · 2025 USAs", "lr_brazier": "LetsRun · 2025 USAs",
    "lr_wic": "LetsRun · World Indoors 2026", "lr_oslo": "LetsRun · Oslo 2026", "citius_pre": "CITIUS MAG · Prefontaine 2026",
    "citius_usa26": "CITIUS MAG · 2026 USAs", "lr_kessler": "LetsRun · 2026 USAs", "citius_millrose": "CITIUS MAG · Millrose 2026",
    "lr_prodebut": "LetsRun · January 2026",
}

R = {"raw": 1}
# cold open: Hobbs Kessler, 2026 USAs: "even if you're Cooper Lutkenhaus, that doesn't last forever. He's going to have some stumbles..."
PRE_SB = ("lr_kessler", 199.45, 205.50, "Hobbs Kessler, 3rd at 2026 USAs · LetsRun")
A1 = "lr_after142"; WI = "lr_wic"; OS = "lr_oslo"; PR = "citius_pre"; U6 = "citius_usa26"; KE = "lr_kessler"; BZ = "lr_brazier"
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("and i aint gonna hold you", 1), OS, 65.76, 73.92, "Cooper Lutkenhaus, 17 · LetsRun · Oslo 2026", R),
    (("as a freshman in 2024", 2), A1, 305.05, 318.26, "Cooper Lutkenhaus, 16 · LetsRun · August 2025", R),
    (("he go to usas", 4), "own_usa25", 11.85, 17.60, "Stadium announcer · 2025 USAs · fan video", R),
    (("he finished second", 4), A1, 34.02, 45.28, "Cooper Lutkenhaus after 1:42.27 · LetsRun", R),
    (("thats an under", 4), BZ, 122.10, 133.40, "Donavan Brazier, 2019 world champion · LetsRun", R),
    (("the first 16 year old american", 4), A1, 74.45, 84.72, "Cooper Lutkenhaus · LetsRun · 2025 USAs", R),
    (("right after that nike", 5), A1, 373.62, 383.02, "Cooper Lutkenhaus, before he turned pro · LetsRun · Aug 2025", R),
    (("and he said it himself", 6), WI, 166.52, 170.04, "Cooper Lutkenhaus on Tokyo · LetsRun · March 2026", R),
    (("now a lot of kids", 6), WI, 62.50, 77.82, "Cooper Lutkenhaus on Tokyo · LetsRun · March 2026", R),
    (("he did that over spring", 7), WI, 0.00, 12.30, "Cooper Lutkenhaus, world indoor champion · LetsRun", R),
    (("a 17 year old beat", 8), OS, 14.76, 24.18, "Cooper Lutkenhaus after beating Wanyonyi · LetsRun · Oslo", R),
    (("then at usas in new york", 8), PR, 48.92, 57.12, "Cooper Lutkenhaus after Pre · CITIUS MAG · July 2026", R),
    (("and he skipped it", 9), PR, 88.50, 103.56, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
    (("a kid who already got paid", 9), U6, 160.40, 171.76, "Cooper Lutkenhaus after the US title · CITIUS MAG", R),
    (("and when he lost at pre", 10), U6, 406.18, 423.50, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
    (("and to me thats the biggest", 10), KE, 122.86, 151.22, "Hobbs Kessler on Cooper · LetsRun · July 2026", R),
    (("thats a lot to put on a kid", 11), U6, 71.82, 82.52, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
    (("let me know in the comments", 11), PR, 133.82, 136.98, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
]
SPLIT_AT = {}

U25 = "own_usa25"; MK = "mk_u18wr"; W25 = "tao_workout25"; FW = "tao_firstworkout"; WC = "tao_wcworkout"; MR = "citius_millrose"; PD = "lr_prodebut"

SEASON = [("Millrose", "Feb", "U20 WR", "good"), ("USA Indoors", "Mar", "Gold", "good"), ("World Indoors", "Mar", "Gold", "good"),
          ("Stockholm", "Jun", "1st", "good"), ("Oslo", "Jun", "1st", "good"), ("Pre", "Jul", "2nd", "bad"), ("USAs", "Jul", "Gold", "good")]
def season(O, t, upto, dur=4.2): O(t, dur, ("tracker", "2026 season · 800m", SEASON, upto, upto))
def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open -------------------------------------------------------------------------------------
    S(PART[1] - 0.05, U25, 118.0, flash=1, ramp=(2.0, 0.4)); lb(O, PART[1], 10.0)
    title(a("is 17 years old") + 0.2, 3.4, "Still in high school", "Cooper Lutkenhaus")
    S(a("and he already a world"), WI, 20.0)
    S(a("he beat the olympic"), MK, 95.0, slow=0.6)
    S(a("he won usas by more"), U25, 126.0, ramp=(0.8, 0.4))
    S(a("and nike already paid"), WC, 70.0)
    S(a("every time i see a kid"), FW, 520.0, slow=0.7)
    S(a("i start getting nervous"), W25, 470.0, bw=1)
    S(a("cause i seen this movie"), FW, 610.0, bw=1)
    O(a("mary cain") - 0.1, 4.6, ("board", "Teen prodigies who signed pro", [("Mary Cain", "Nike at 17", "2013", 0), ("Athing Mu", "Nike at 19", "2021", 0), ("Cooper Lutkenhaus", "Nike at 16", "2025", 1)], ""))
    S(a("all of them were supposed"), FW, 660.0, bw=1)
    S(a("so is cooper really"), W25, 160.0, slow=0.6)
    S(a("or is he about to be"), FW, 880.0, bw=1, slow=0.6)
    # 2 Justin, Texas ---------------------------------------------------------------------------------
    S(PART[2] - 0.05, W25, 40.0, flash=1); chapter(PART[2] + 0.2, "01", "Justin, Texas"); lb(O, PART[2], 3.4)
    S(a("he from justin texas"), W25, 120.0); date(a("he from justin texas"), 2.8, "Justin, Texas", "Northwest High School")
    S(a("and he run for northwest"), W25, 300.0)
    S(a("his dad george"), W25, 8.0)
    S(a("so this aint some kid"), W25, 240.0, punch=0.4)
    S(a("as a freshman in 2024"), W25, 330.0); number(a("he ran 147") + 0.1, 3.0, "1:47.58", "800m · Texas state record", "As a freshman · 2024")
    S(a("and broke the texas"), W25, 200.0)
    S(a("most grown man"), W25, 400.0, slow=0.6)
    # 3 the record ------------------------------------------------------------------------------------
    S(PART[3] - 0.05, W25, 460.0, flash=1); chapter(PART[3] + 0.2, "02", "The Record"); lb(O, PART[3], 3.4)
    S(a("he broke the high school indoor"), MR, 10.0)
    S(a("he won the texas state title"), W25, 560.0)
    S(a("and then at brooks"), W25, 640.0, punch=0.3)
    S(a("in june 2025"), W25, 690.0); number(a("he ran 146") + 0.1, 3.0, "1:46.26", "800m · national high school record", "Brooks PR · June 2025")
    S(a("and broke michael granville"), W25, 700.0)
    O(a("and broke michael granville") + 0.2, 4.2, ("board", "US high school 800m record", [("Michael Granville", "1:46.45", "1996", 0), ("Cooper Lutkenhaus", "1:46.26", "June 2025", 1)], "29 years untouched"))
    S(a("and that record been"), W25, 30.0, slow=0.7)
    S(a("29 years nobody"), W25, 720.0, bw=1)
    S(a("then two weeks later"), W25, 760.0)
    S(a("in the pouring rain"), W25, 600.0, slow=0.6); number(a("he ran 145") + 0.1, 3.0, "1:45.45", "800m · his own HS record again", "Nike Nationals · in the rain")
    S(a("and broke his own record"), W25, 520.0, punch=0.3)
    # 4 Eugene ----------------------------------------------------------------------------------------
    S(PART[4] - 0.05, U25, 0.5, flash=1); chapter(PART[4] + 0.2, "03", "1:42.27"); lb(O, PART[4], 3.4)
    S(a("he go to usas"), U25, 20.0); date(a("he go to usas"), 2.8, "August 3, 2025", "USA Championships · Eugene")
    S(a("16 years old running"), MK, 18.0)
    S(a("and he run 142"), U25, 117.0, ramp=(1.2, 0.4)); number(a("and he run 142") + 0.6, 3.2, "1:42.27", "800m · U18 world record", "Age 16 · 2nd at USAs")
    S(a("he finished second"), MK, 100.0, slow=0.6)
    S(a("behind donovan brazier"), U25, 126.0, slow=0.5); name(a("behind donovan brazier"), 2.8, "Donavan Brazier", "1st · 1:42.16 · 2019 world champion")
    S(a("and he beat bryce"), MK, 125.0)
    S(a("thats an under"), MK, 135.0)
    S(a("and just like that"), MK, 150.0)
    S(a("the first 16 year old american"), MK, 160.0, slow=0.7)
    # 5 Nike ------------------------------------------------------------------------------------------
    S(PART[5] - 0.05, FW, 140.0, flash=1); chapter(PART[5] + 0.2, "04", "The Deal"); lb(O, PART[5], 3.4)
    S(a("right after that nike"), FW, 95.0); title(a("right after that nike") + 0.3, 3.0, "August 2025", "Signs pro with Nike at 16")
    S(a("he give up his high school"), FW, 190.0)
    S(a("everything at 16"), FW, 320.0, punch=0.3)
    S(a("and look i know"), FW, 330.0, bw=1)
    O(a("thats exactly what mary") - 0.1, 6.8, ("versus", ("Mary Cain", "Nike Oregon Project"), ("Cooper Lutkenhaus", "Nike"),
      [("Turned pro", "17 · 2013", "16 · 2025"), ("First Worlds", "17 · 10th, Moscow", "16 · out in heats, Tokyo"), ("Coach", "Alberto Salazar", "His high school coach")], "Same move. Different setup."))
    S(a("thats exactly what mary"), FW, 360.0, bw=1)
    S(a("and a few years later"), FW, 750.0, bw=1)
    S(a("and by 2024 she was"), FW, 660.0, bw=1, slow=0.6)
    S(a("so when i saw"), FW, 700.0, bw=1)
    S(a("here we go again"), FW, 930.0, bw=1, slow=0.6)
    # 6 Tokyo -----------------------------------------------------------------------------------------
    S(PART[6] - 0.05, FW, 400.0, flash=1, bw=1); chapter(PART[6] + 0.2, "05", "Tokyo"); lb(O, PART[6], 3.4)
    date(a("his first world championships"), 2.8, "September 2025", "World Championships · Tokyo")
    S(a("and it did not go well"), FW, 560.0, bw=1)
    S(a("he got out there"), FW, 440.0, bw=1)
    S(a("ran most of the race"), FW, 500.0, bw=1, slow=0.6)
    S(a("and finished seventh"), FW, 600.0, bw=1); number(a("and finished seventh") + 0.3, 3.0, "7th", "800m heat · Tokyo", "1:47.68 · out in round 1")
    S(a("and he said it himself"), WI, 150.0)
    S(a("that was the first real test"), FW, 800.0, bw=1, slow=0.6)
    # 7 the response ----------------------------------------------------------------------------------
    S(PART[7] - 0.05, WC, 110.0, flash=1); chapter(PART[7] + 0.2, "06", "The Response"); lb(O, PART[7], 3.4)
    S(a("he came back in 2026"), WC, 160.0, ramp=(1.0, 0.45))
    S(a("he broke the world under 20"), MR, 40.0); number(a("the 600 at") + 0.1, 2.8, "U20 WR", "600m · Millrose Games", "February 2026")
    S(a("he broke the under 20 indoor"), PD, 30.0)
    S(a("he won the us indoor"), WC, 190.0); season(O, a("he won the us indoor"), 1, 2.4)
    S(a("and then in march"), WI, 25.0); number(a("and won it") + 0.1, 3.0, "1:44.24", "World Indoor 800m champion", "Youngest ever · age 17")
    S(a("and won it"), WC, 330.0, punch=0.4)
    S(a("and became the youngest"), WI, 100.0); season(O, a("and became the youngest") + 0.6, 2, 3.0)
    S(a("he did that over spring"), WC, 345.0)
    S(a("then he went back to class"), WC, 1030.0, punch=0.3)
    # 8 Diamond League --------------------------------------------------------------------------------
    S(PART[8] - 0.05, WC, 170.0, flash=1); chapter(PART[8] + 0.2, "07", "Diamond League"); lb(O, PART[8], 3.4)
    S(a("his first ever diamond"), WC, 180.0); date(a("his first ever diamond"), 2.6, "June 7, 2026", "Diamond League debut · Stockholm")
    S(a("win in 142"), OS, 1.0); number(a("win in 142") + 0.1, 2.8, "1:42.70", "Stockholm · 1st", "Beats Marco Arop"); season(O, a("win in 142") + 2.9, 3, 2.2)
    S(a("a few days later in oslo"), OS, 30.0); number(a("he ran 142 08") + 0.1, 3.0, "1:42.08", "World U20 record · Oslo", "Beats Olympic champion Wanyonyi by 0.01")
    S(a("under 20 world record"), WC, 560.0)
    S(a("and he dive at the line"), OS, 40.0, slow=0.6); season(O, a("beat emmanuel") + 0.5, 4, 2.6)
    S(a("a 17 year old beat"), OS, 50.0)
    S(a("he did lose one race"), PR, 20.0); name(a("brandon miller got him"), 2.6, "Brandon Miller", "1st · Prefontaine Classic · 1:43.68"); season(O, a("that's the only 800") , 5, 3.0)
    S(a("and thats the only"), WC, 760.0)
    S(a("then at usas in new york"), U6, 30.0); number(a("he won by 1") + 0.1, 3.0, "1.07 s", "Winning margin · 2026 USAs", "Biggest since 2014"); season(O, a("7 wins out of 8") - 0.4, 6, 3.2)
    # 9 senior year -----------------------------------------------------------------------------------
    S(a("the biggest winning", PART[8]), WC, 880.0)
    S(a("7 wins out of 8", PART[8]), U6, 100.0)
    # 9b
    S(PART[9] - 0.05, U6, 60.0, flash=1); chapter(PART[9] + 0.2, "08", "Senior Year"); lb(O, PART[9], 3.4)
    S(a("there was a big new"), WC, 400.0); title(a("there was a big new"), 3.0, "September 2026", "World Ultimate Championship · Budapest")
    S(a("and he skipped it"), WC, 500.0)
    S(a("he shut his season down"), W25, 600.0, slow=0.7)
    S(a("a kid who already got paid"), W25, 700.0)
    S(a("and he chose to go"), W25, 730.0)
    S(a("the smartest thing"), W25, 160.0, slow=0.6)
    # 10 will he fall off? ----------------------------------------------------------------------------
    S(PART[10] - 0.05, WC, 600.0, flash=1); chapter(PART[10] + 0.2, "09", "Will He Fall Off?"); lb(O, PART[10], 4.0)
    S(a("honestly i dont think so"), WC, 650.0)
    S(a("the kids who fell off"), FW, 900.0, bw=1)
    S(a("new coaches new cities"), FW, 640.0, bw=1)
    S(a("still training with the same"), WC, 500.0); name(a("still training with the same"), 2.8, "Chris Capeau", "His coach since sophomore year · Northwest HS")
    S(a("still running like"), WC, 700.0)
    S(a("and when he lost at pre"), PR, 100.0)
    S(a("and when he got cooked"), WI, 60.0)
    S(a("he didnt make excuses"), WC, 840.0)
    S(a("he came back better"), WC, 960.0, punch=0.3)
    # 11 LA 2028 -------------------------------------------------------------------------------------
    S(PART[11] - 0.05, MK, 90.0, flash=1); chapter(PART[11] + 0.2, "10", "LA 2028"); lb(O, PART[11], 14.0)
    S(a("is a brutal event"), U25, 70.0, slow=0.6)
    S(a("and the pressure only"), U25, 84.0)
    S(a("la 2028"), U25, 100.0); O(a("la 2028") + 0.2, 4.6, ("counter", 0, 596, "days until LA 2028", "He'll be 19"))
    S(a("and everybody gonna expect"), MK, 104.0, slow=0.6)
    S(a("thats a lot to put on a kid"), WC, 1050.0)
    S(a("so yall tell me"), U25, 120.0, slow=0.6)
    S(a("the next great american"), MK, 105.0, slow=0.5)
    S(a("or is he going to be"), FW, 880.0, bw=1)
    S(a("let me know in the comments"), W25, 470.0, slow=0.7)

"""Cooper Lutkenhaus v2, THE RISE (user, 26 Nov 2026): soundbites + EDL. Title: "He's Still In High School... And He's A World Champion".
Voice: Erin Brown 2026 clone, approved A3b style (light respelling + casual accent tag, stability 0.4, atempo 0.94 + match_rhythm).
Footage: fan video from the stands at 2025 USAs (Cooper Lutkenhaus's own channel; Mark & Kathryn), TRACK: All-Access workouts,
LetsRun + CITIUS MAG interviews (Oslo/Pre mixed-zone bites play audio-only over workout B-roll: no Diamond League backdrop on screen, user 26 Nov 2026). No NBC/USATF broadcast, FloTrack/MileSplit, RunnerSpace, Diamond League, World Athletics or
Olympic video. Avoid: mk_u18wr 0-6 s and 115-122 s (burned captions); tao_wcworkout ~250-310 s and tao_firstworkout 0-47 s,
234-282 s (picture-in-picture insets). Soundbite times word-checked with small.en word timestamps (scratchpad win.py)."""

TAGS = {
    "own_usa25": "2025 USAs · fan video · Cooper Lutkenhaus", "mk_u18wr": "2025 USAs · fan video · Mark & Kathryn",
    "tao_workout25": "TRACK: All-Access · April 2025", "tao_firstworkout": "TRACK: All-Access · August 2025",
    "tao_wcworkout": "TRACK: All-Access · March 2026", "lr_after142": "LetsRun · 2025 USAs", "lr_brazier": "LetsRun · 2025 USAs",
    "lr_wic": "LetsRun · World Indoors 2026", "lr_oslo": "LetsRun · Oslo 2026", "citius_pre": "CITIUS MAG · Prefontaine 2026",
    "citius_usa26": "CITIUS MAG · 2026 USAs", "lr_kessler": "LetsRun · 2026 USAs", "citius_millrose": "CITIUS MAG · Millrose 2026",
    "lr_prodebut": "LetsRun · January 2026",
}

R = {"raw": 1}
# cold open: right after winning World Indoors: "How does it feel to make history?" "Man, I don't know."
PRE_SB = ("lr_wic", 0.00, 5.62, "Cooper Lutkenhaus, 17, world indoor champion · LetsRun · March 2026")
A1 = "lr_after142"; WI = "lr_wic"; OS = "lr_oslo"; PR = "citius_pre"; U6 = "citius_usa26"; KE = "lr_kessler"; BZ = "lr_brazier"
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("so let me show", 1), OS, 65.76, 73.92, "Cooper Lutkenhaus, 17 · LetsRun · Oslo 2026", dict(raw=1, vsrc="tao_wcworkout", vss=345.0, quote="Would you ever think you'd be this good at this age? Definitely not.", who="Cooper Lutkenhaus, 17")),
    (("and his dad george", 2), A1, 305.05, 318.26, "Cooper Lutkenhaus, 16 · LetsRun · August 2025", R),
    (("as a freshman in 2024", 3), U6, 406.18, 423.50, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
    (("and its like he jumped", 3), A1, 444.40, 450.90, "Cooper Lutkenhaus on Coach Capeau · LetsRun · 2025", R),
    (("the whole stadium", 4), "own_usa25", 11.85, 17.60, "Stadium announcer · 2025 USAs · fan video", R),
    (("and finished second", 4), A1, 34.02, 45.28, "Cooper Lutkenhaus after 1:42.27 · LetsRun", R),
    (("thats a under 18", 4), BZ, 122.10, 133.40, "Donavan Brazier, 2019 world champion · LetsRun", R),
    (("to ever make a world", 4), A1, 74.45, 84.72, "Cooper Lutkenhaus · LetsRun · 2025 USAs", R),
    (("but he kept it simple", 5), A1, 373.62, 383.02, "Cooper Lutkenhaus, before going pro · LetsRun · Aug 2025", R),
    (("then came tokyo", 6), A1, 283.40, 290.30, "Cooper Lutkenhaus, before Tokyo · LetsRun · Aug 2025", R),
    (("he called it the worst", 6), WI, 166.52, 170.04, "Cooper Lutkenhaus on Tokyo · LetsRun · March 2026", R),
    (("and instead of that", 6), WI, 62.50, 77.82, "Cooper Lutkenhaus on Tokyo · LetsRun · March 2026", R),
    (("he did that over spring", 7), WI, 5.82, 12.30, "Cooper Lutkenhaus, world indoor champion · LetsRun", R),
    (("a high schooler beat", 8), OS, 14.76, 24.18, "Cooper Lutkenhaus after beating Wanyonyi · LetsRun · Oslo", dict(raw=1, vsrc="tao_wcworkout", vss=880.0, quote="I thought he got me at the line.", who="Cooper Lutkenhaus, after Oslo")),
    (("then at usas in new york", 8), PR, 48.92, 57.12, "Cooper Lutkenhaus after Pre · CITIUS MAG · July 2026", dict(raw=1, vsrc="tao_wcworkout", vss=960.0, quote="If 1:44 is my bad race, I'm happy with that.", who="Cooper Lutkenhaus, after his only loss")),
    (("hobbs kessler said", 9), BZ, 125.26, 133.40, "Donavan Brazier · LetsRun · 2025 USAs", R),
    (("and then cooper did", 9), KE, 122.86, 151.22, "Hobbs Kessler on Cooper · LetsRun · July 2026", R),
    (("and he skipped it", 9), PR, 88.50, 103.56, "Cooper Lutkenhaus · CITIUS MAG · July 2026", dict(raw=1, vsrc="tao_workout25", vss=640.0, quote="One more year of high school.", who="Cooper Lutkenhaus, July 2026")),
    (("so think about where", 10), U6, 160.40, 171.76, "Cooper Lutkenhaus after the US title · CITIUS MAG", R),
    (("if he keep going", 10), A1, 291.86, 303.86, "Cooper Lutkenhaus, 16, on 2028 · LetsRun · Aug 2025", R),
    (("so yall tell me", 10), U6, 71.82, 82.52, "Cooper Lutkenhaus · CITIUS MAG · July 2026", R),
    (("let me know in the comments", 10), PR, 133.82, 136.98, "Cooper Lutkenhaus · CITIUS MAG · July 2026", dict(raw=1, vsrc="tao_wcworkout", vss=700.0, quote="I know I'm better than that, so I just gotta go out and prove it.", who="Cooper Lutkenhaus")),
]
SPLIT_AT = {}

U25 = "own_usa25"; MK = "mk_u18wr"; W25 = "tao_workout25"; FW = "tao_firstworkout"; WC = "tao_wcworkout"; MR = "citius_millrose"; PD = "lr_prodebut"

SEASON = [("Millrose", "Feb", "U20 WR", "good"), ("USA Indoors", "Mar", "Gold", "good"), ("World Indoors", "Mar", "Gold", "good"),
          ("Stockholm", "Jun", "1st", "good"), ("Oslo", "Jun", "1st", "good"), ("Pre", "Jul", "2nd", "bad"), ("USAs", "Jul", "Gold", "good")]
def season(O, t, upto, dur=4.2): O(t, dur, ("tracker", "2026 season · 800m", SEASON, upto, upto))
def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open -------------------------------------------------------------------------------------
    S(PART[1] - 0.05, U25, 118.0, flash=1, ramp=(2.0, 0.4)); lb(O, PART[1], 9.0)
    S(a("went overseas"), WI, 20.0)
    S(a("and was back in class"), WC, 1030.0)
    title(a("his name is") + 0.2, 3.4, "Still in high school", "Cooper Lutkenhaus")
    S(a("his name is"), MK, 95.0, slow=0.6)
    S(a("and he already beat"), U25, 126.0, ramp=(0.8, 0.4))
    S(a("ive been watching track"), FW, 520.0, slow=0.7)
    S(a("so let me show"), W25, 160.0, slow=0.6)
    S(a("from a freshman nobody"), W25, 330.0)
    S(a("best young runner"), U25, 120.0, slow=0.6)
    # 2 Justin, Texas ---------------------------------------------------------------------------------
    S(PART[2] - 0.05, W25, 40.0, flash=1); chapter(PART[2] + 0.2, "01", "Justin, Texas"); lb(O, PART[2], 3.4)
    date(a("cooper from justin"), 2.8, "Justin, Texas", "Northwest High School")
    S(a("a small town"), W25, 120.0)
    S(a("and he run for northwest"), W25, 300.0)
    S(a("he didnt even start"), W25, 240.0, punch=0.4)
    S(a("it wasnt till the summer"), W25, 400.0, slow=0.7)
    S(a("and his dad george"), W25, 8.0)
    # 3 The Record ------------------------------------------------------------------------------------
    S(PART[3] - 0.05, W25, 460.0, flash=1); chapter(PART[3] + 0.2, "02", "The Record"); lb(O, PART[3], 3.4)
    S(a("as a freshman in 2024"), W25, 200.0); number(a("he ran 147") + 0.1, 3.0, "1:47.58", "800m · Texas state record", "As a freshman · 2024")
    S(a("and broke the texas"), W25, 380.0)
    S(a("then his sophomore year"), W25, 2.0); name(a("with a new coach") + 0.4, 2.8, "Chris Capeau", "Coach · Northwest High School")
    S(a("and its like he jumped"), W25, 560.0, punch=0.3)
    S(a("he broke the high school indoor"), MR, 10.0)
    S(a("he won the state title"), W25, 640.0)
    S(a("in june 2025"), W25, 690.0); number(a("he ran 146") + 0.1, 3.0, "1:46.26", "800m · national high school record", "Brooks PR · June 2025")
    S(a("and broke michael granville"), W25, 700.0)
    O(a("and broke michael granville") + 0.2, 4.2, ("board", "US high school 800m record", [("Michael Granville", "1:46.45", "1996", 0), ("Cooper Lutkenhaus", "1:46.26", "June 2025", 1)], "29 years untouched"))
    S(a("there since 1996"), W25, 30.0, slow=0.7)
    S(a("two weeks later"), W25, 760.0)
    S(a("in the pouring rain"), W25, 600.0, slow=0.6); number(a("he ran 145") + 0.1, 3.0, "1:45.45", "800m · his own HS record again", "Nike Nationals · in the rain")
    S(a("and broke his own record"), W25, 520.0, punch=0.3)
    # 4 1:42.27 ---------------------------------------------------------------------------------------
    S(PART[4] - 0.05, U25, 0.5, flash=1); chapter(PART[4] + 0.2, "03", "1:42.27"); lb(O, PART[4], 3.4)
    S(a("usas in eugene"), U25, 20.0); date(a("usas in eugene"), 2.8, "August 3, 2025", "USA Championships · Eugene")
    S(a("he in the final"), MK, 18.0)
    S(a("and with 200 to go"), U25, 100.0)
    S(a("then he just start"), MK, 85.0, slow=0.7)
    S(a("the whole stadium"), U25, 117.0, ramp=(1.2, 0.4))
    S(a("and he run 142"), U25, 124.0, slow=0.6); number(a("and he run 142") + 0.4, 3.2, "1:42.27", "800m · U18 world record", "Age 16 · 2nd at USAs")
    S(a("and finished second"), MK, 100.0, slow=0.6)
    S(a("right behind donovan"), U25, 126.0, slow=0.5); name(a("right behind donovan"), 2.8, "Donavan Brazier", "1st · 1:42.16 · 2019 world champion")
    S(a("and ahead of bryce"), MK, 125.0)
    S(a("thats a under 18"), MK, 135.0)
    S(a("and it made him"), MK, 150.0)
    S(a("to ever make a world"), MK, 160.0, slow=0.7)
    # 5 Nike ------------------------------------------------------------------------------------------
    S(PART[5] - 0.05, FW, 140.0, flash=1); chapter(PART[5] + 0.2, "04", "Going Pro"); lb(O, PART[5], 3.4)
    title(a("nike signed him") + 0.3, 3.0, "August 2025", "Signs pro with Nike at 16")
    S(a("sixteen years old"), FW, 190.0)
    S(a("but he kept it simple"), FW, 320.0)
    S(a("he stayed home in texas"), W25, 730.0)
    S(a("he kept training"), FW, 95.0); name(a("he kept training"), 2.6, "Chris Capeau", "Still his coach · Northwest HS")
    S(a("and he kept going to class"), FW, 360.0)
    # 6 Tokyo -----------------------------------------------------------------------------------------
    S(PART[6] - 0.05, FW, 400.0, flash=1); chapter(PART[6] + 0.2, "05", "Tokyo"); lb(O, PART[6], 3.4)
    date(a("his first world championships"), 2.8, "September 2025", "World Championships · Tokyo")
    S(a("and honestly it was"), FW, 560.0, bw=1)
    S(a("he ran most of his heat"), FW, 500.0, bw=1, slow=0.6)
    number(a("in the first round") - 0.4, 3.0, "1:47.68", "800m heat · Tokyo", "7th · out in round 1")
    S(a("he called it the worst"), WI, 150.0)
    S(a("and instead of that"), FW, 800.0)
    S(a("and went back to work"), FW, 700.0, punch=0.3)
    # 7 The Response ----------------------------------------------------------------------------------
    S(PART[7] - 0.05, WC, 110.0, flash=1); chapter(PART[7] + 0.2, "06", "World Champion"); lb(O, PART[7], 3.4)
    S(a("and then 2026 happened"), WC, 160.0, ramp=(1.0, 0.45))
    S(a("he broke the under 20 world"), MR, 40.0); number(a("in the 600") + 0.1, 2.8, "U20 WR", "600m · Millrose Games", "February 2026")
    S(a("he broke the under 20 indoor"), PD, 30.0)
    S(a("he won the us indoor"), WC, 190.0); season(O, a("he won the us indoor"), 1, 2.4)
    S(a("and then in march"), WI, 25.0)
    S(a("and won it in"), WC, 330.0, punch=0.4); number(a("and won it in") + 0.3, 3.0, "1:44.24", "World Indoor 800m champion", "Youngest ever · as a high school junior")
    S(a("that made him the youngest"), WI, 100.0); season(O, a("that made him the youngest") + 0.6, 2, 3.0)
    S(a("he did that over spring"), WC, 345.0)
    S(a("and then he went right back"), WC, 1030.0, punch=0.3)
    # 8 Diamond League --------------------------------------------------------------------------------
    S(PART[8] - 0.05, WC, 170.0, flash=1); chapter(PART[8] + 0.2, "07", "Beating The Best"); lb(O, PART[8], 3.4)
    S(a("diamond league in stockholm"), WC, 180.0); date(a("diamond league in stockholm"), 2.6, "June 7, 2026", "Diamond League debut · Stockholm")
    S(a("marco arop"), WC, 380.0); number(a("to win in") + 0.3, 2.8, "1:42.70", "Stockholm · 1st", "Beats Marco Arop")
    S(a("a few days later in oslo"), WC, 400.0); number(a("he'd run 142") + 0.3, 3.0, "1:42.08", "World U20 record · Oslo", "Beats Olympic champion Wanyonyi by 0.01")
    S(a("another under 20"), WC, 560.0)
    S(a("and he'd dive at the line"), U25, 124.0, slow=0.5); season(O, a("by one hundredth") + 0.2, 4, 2.6)
    S(a("a high schooler beat"), MK, 108.0, slow=0.6)
    S(a("his only loss"), WC, 760.0); name(a("brandon miller got him") - 0.2, 2.6, "Brandon Miller", "1st · Prefontaine Classic · 1:43.68")
    S(a("then at usas in new york"), U6, 30.0); number(a("he won by") + 0.4, 3.0, "1.07 s", "Winning margin · 2026 USAs", "Biggest since 2014")
    S(a("the biggest winning"), WC, 880.0)
    S(a("seven wins out of eight"), U6, 100.0); season(O, a("seven wins out of eight") - 0.3, 6, 3.4)
    # 9 respect + senior year -------------------------------------------------------------------------
    S(PART[9] - 0.05, U6, 60.0, flash=1); chapter(PART[9] + 0.2, "08", "Senior Year"); lb(O, PART[9], 3.4)
    S(a("donovan brazier said"), MK, 140.0)
    S(a("hobbs kessler said"), KE, 100.0)
    S(a("and then cooper did"), WC, 400.0)
    S(a("there was a big new"), WC, 500.0); title(a("there was a big new"), 3.0, "September 2026", "World Ultimate Championship · Budapest")
    S(a("and he skipped it"), WC, 600.0)
    S(a("he shut his season"), W25, 600.0, slow=0.7)
    # 10 now ------------------------------------------------------------------------------------------
    S(PART[10] - 0.05, WC, 650.0, flash=1); chapter(PART[10] + 0.2, "09", "What's Next"); lb(O, PART[10], 12.0)
    S(a("he a high school senior"), W25, 470.0)
    S(a("he a world champion"), WI, 120.0)
    S(a("he got a pro deal"), WC, 700.0)
    S(a("and he done beat"), U25, 126.0, slow=0.5)
    S(a("and la 2028"), U25, 70.0, slow=0.6); O(a("and la 2028") + 0.2, 4.6, ("counter", 0, 596, "days until LA 2028", "He'll be 19"))
    S(a("if he keep going"), WC, 840.0)
    S(a("we could be watching"), MK, 104.0, slow=0.6)
    S(a("grow up right in front"), WC, 960.0, punch=0.3)
    S(a("so yall tell me"), U25, 120.0, slow=0.6)
    S(a("how fast yall think"), MK, 105.0, slow=0.5)
    S(a("let me know in the comments"), W25, 470.0, slow=0.7)

"""Drew Hunter: soundbites + EDL (modern style, tools/modern.py).
Footage: Loudoun Now "Loudoun Unscripted" (2016), Rich Gonzalez Gatorade AOY interview (Jul 2016), Darrell Anderson fan video
(Penn Relays 2016), Tracklandia, Inside Tinman Elite (Tinman Elite channel), Billy Toad, CITIUS MAG, LetsRun.
No NCAA/ESPN, FloTrack/MileSplit, RunnerSpace, NBC, Olympic, Diamond League, World Athletics.
Avoid: tinman_s3_trailer 48-64 s (profanity), letsrun_asics 413-419 s (profanity). Soundbite times are word-checked
against tx/*.json (small.en); all raw."""

TAGS = {
    "loudoun_unscripted": "Loudoun Now · Loudoun Unscripted · 2016", "gatorade_2016": "Rich Gonzalez · Gatorade AOY Awards · July 2016",
    "penn_dmr_fan": "Penn Relays 2016 · fan video, Darrell Anderson", "tracklandia_tinman": "Tracklandia · The Tinman Elite · 2021",
    "tinman_s3_trailer": "Inside Tinman Elite · Season 3 · 2021", "tinman_building_future": "Inside Tinman Elite · 2022",
    "tinman_bu_indoor": "Inside Tinman Elite · 2022", "toad_trials": "Billy Toad · August 2021",
    "citius_coach": "CITIUS MAG · November 2021", "letsrun_trials4th": "LetsRun · 2024 Olympic Trials",
    "citius_13_08": "CITIUS MAG · May 2024", "citius_portland": "CITIUS MAG · Portland Track Festival · June 2025",
    "letsrun_asics": "LetsRun · March 2025", "letsrun_sound2026": "LetsRun · February 2026",
}

PRE_SB = ("loudoun_unscripted", 7.30, 14.30, "Loudoun Now · Loudoun Unscripted · 2016")
R = {"raw": 1}
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("that was ten years ago", 1), "gatorade_2016", 21.88, 25.0, "Gatorade National Athlete of the Year · Rich Gonzalez · July 2016", R),
    (("so drew grew up", 2), "loudoun_unscripted", 46.10, 53.50, "Drew Hunter, Loudoun Valley HS · Loudoun Now · 2016", R),
    (("wanted for his school", 3), "penn_dmr_fan", 14.50, 21.50, "Penn Relays 2016 · fan video, Darrell Anderson", R),
    (("on paper this was", 3), "gatorade_2016", 142.30, 152.00, "Drew Hunter · Rich Gonzalez · July 2016", R),
    (("you a kid", 4), "gatorade_2016", 71.50, 85.70, "Drew on skipping college · Rich Gonzalez · July 2016", R),
    (("but a lot of people", 4), "gatorade_2016", 168.30, 181.90, "Drew Hunter · Rich Gonzalez · July 2016", R),
    (("and they became like", 5), "tracklandia_tinman", 194.10, 196.30, "Coach Tom Schwartz · Tracklandia · 2021", R),
    (("he actually said", 5), "toad_trials", 33.50, 44.50, "Drew on missing the Tokyo Trials · Billy Toad · 2021", R),
    (("and around that same time", 5), "tinman_s3_trailer", 0.80, 5.90, "Inside Tinman Elite · Season 3 · 2021", R),
    (("now here go the part", 6), "citius_coach", 391.00, 400.48, "Drew on his mom coaching him · CITIUS MAG · 2021", R),
    (("thats how close", 6), "letsrun_trials4th", 7.78, 13.36, "Drew Hunter, 4th · LetsRun · 2024 Olympic Trials", R),
    (("so every time", 6), "letsrun_trials4th", 297.70, 301.95, "Drew Hunter · LetsRun · 2024 Olympic Trials", R),
    (("and honestly thats what", 6), "letsrun_trials4th", 140.30, 152.58, "Drew Hunter · LetsRun · 2024 Olympic Trials", R),
    (("he wrote something", 7), "citius_portland", 107.50, 116.40, "Drew Hunter · CITIUS MAG · June 2025", R),
    (("so that whole chapter", 7), "letsrun_asics", 284.40, 295.25, "Drew on his Adidas contract ending · LetsRun · March 2025", R),
    (("is he gonna make the team", 8), "toad_trials", 196.55, 200.32, "Drew Hunter · Billy Toad · 2021", R),
]

LU = "loudoun_unscripted"; GA = "gatorade_2016"; PN = "penn_dmr_fan"; TL = "tracklandia_tinman"; S3 = "tinman_s3_trailer"
BF = "tinman_building_future"; BU = "tinman_bu_indoor"; TD = "toad_trials"; CC = "citius_coach"; TR = "letsrun_trials4th"
C13 = "citius_13_08"; CP = "citius_portland"; AS = "letsrun_asics"; LS = "letsrun_sound2026"

PRO = [("1500m", "11th", "2017 USAs", 0), ("1500m", "6th", "2018 USAs", 0), ("2 mile", "1st", "2019 US Indoors", 1),
       ("5000m", "5th", "2019 USAs", 0), ("Trials", "Injured", "2021", 0), ("10,000m", "4th", "2024 Olympic Trials", 1), ("5000m", "4th", "2025 USAs", 0)]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open ---------------------------------------------------------------------------------
    S(PART[1] - 0.05, LU, 14.4, flash=1); date(a("back in 2016") + 0.2, 2.6, "2016", "Loudoun Valley High School · Virginia")
    S(a("you already know"), LU, 36.0); name(a("the name drew hunter") + 0.2, 3.0, "Drew Hunter", "Loudoun Valley HS · Purcellville, Virginia")
    S(a("this dude was not"), PN, 12.4)
    S(a("broke alan webb"), LU, 21.4, punch=0.3); number(a("broke alan webb") + 0.2, 3.0, "3:58", "Mile · HS indoor record", "Broke Alan Webb's mark · 2016")
    S(a("he was the first high schooler"), LU, 62.2); number(a("break eight minutes") , 3.0, "7:59", "3000m", "First US high schooler under 8:00")
    S(a("and everybody i mean"), LU, 40.6)
    S(a("every college wanted"), BF, 89.3)
    S(a("he had already committed"), LU, 57.4)
    S(a("and then he did something"), GA, 30.0)
    S(a("heres the thing"), TR, 40.0)
    S(a("drew hunter has never"), TR, 100.0); number(a("drew hunter has never") + 0.2, 3.2, "0", "Olympic or World Championship teams", "10 years as a pro")
    S(a("so what happened"), S3, 26.4, slow=0.6)
    # 2 the kid -----------------------------------------------------------------------------------
    S(PART[2] - 0.05, LU, 7.2, flash=1); chapter(PART[2] + 0.2, "01", "The Kid From Purcellville")
    S(a("drew is from"), LU, 11.9)
    S(a("and he ran for"), LU, 26.3)
    S(a("and running is literally"), BF, 44.8)
    S(a("his dad mark"), BF, 60.0); name(a("his dad mark") + 0.1, 3.0, "Marc Hunter", "His dad · ran 13:36 for 5000m")
    S(a("his mom joanne"), BU, 616.0); name(a("his mom joanne") + 0.1, 3.0, "Joan Hunter", "His mom · ran at West Virginia")
    S(a("and get this"), LU, 48.0)
    S(a("so drew grew up"), LU, 43.0)
    S(a("and honestly i feel"), LU, 59.8)
    S(a("comparing him to"), LU, 52.6)
    # 3 the prodigy -------------------------------------------------------------------------------
    S(PART[3] - 0.05, LU, 21.5, flash=1); chapter(PART[3] + 0.2, "02", "The Prodigy")
    S(a("january 16th"), LU, 14.4); date(a("january 16th"), 2.8, "January 2016", "Camel City Elite · Winston-Salem")
    number(a("first high schooler ever"), 3.0, "7:59.33", "3000m · indoors", "First US high schooler under 8:00")
    S(a("a week later"), LU, 62.4)
    number(a("he runs 358") + 0.1, 3.2, "3:58.25", "Mile · Armory, New York", "Breaks Alan Webb's HS indoor record")
    S(a("the guy his parents"), BF, 70.0)
    S(a("then he goes to"), PN, 0.0); title(a("then he goes to") + 0.3, 3.0, "April 2016", "Penn Relays · distance medley")
    S(a("he gets the baton"), PN, 6.0)
    S(a("like 50 meters behind"), PN, 10.4)
    S(a("and runs about four"), PN, 12.4, punch=0.3); number(a("and runs about four") + 0.3, 3.0, "~4:00", "Mile anchor leg", "From 50 m down to the win")
    S(a("wanted for his school"), PN, 22.0)
    S(a("that clip got"), PN, 26.0)
    S(a("he was gatorade"), GA, 14.8); title(a("he was gatorade"), 3.0, "2016", "Gatorade National Runner of the Year")
    S(a("on paper this was"), LU, 64.6, slow=0.6)
    # 4 the decision ------------------------------------------------------------------------------
    S(PART[4] - 0.05, BF, 89.2, flash=1); chapter(PART[4] + 0.2, "03", "The Decision")
    S(a("had already committed to oregon"), LU, 57.4)
    S(a("oregon the best"), BF, 100.0)
    S(a("and then in july 2016"), GA, 22.0); date(a("and then in july 2016"), 2.8, "July 8, 2016", "Turns pro with Adidas")
    S(a("10 years he was"), GA, 37.0, punch=0.3); number(a("10 years he was"), 3.0, "10", "Year contract · Adidas", "Signed at 18 · skipped college")
    S(a("and im not gonna lie"), GA, 52.0)
    S(a("you a kid"), GA, 100.0)
    S(a("but a lot of people"), TL, 154.0, bw=1)
    S(a("what happened to allen webb"), TL, 161.0, bw=1); title(a("what happened to allen webb"), 3.2, "Alan Webb · Mary Cain", "Both turned pro as teenagers")
    S(a("dont always go"), TL, 147.0, bw=1)
    # 5 Tinman ------------------------------------------------------------------------------------
    S(PART[5] - 0.05, TL, 26.8, flash=1); chapter(PART[5] + 0.2, "04", "Tinman Elite")
    S(a("he moved to boulder"), TL, 30.5); date(a("he moved to boulder"), 2.6, "2017", "Boulder, Colorado")
    S(a("and him and his boys"), TL, 20.1)
    S(a("and they became like"), TL, 73.0)
    S(a("the merch the vlogs"), TL, 167.0)
    S(a("in february 2019"), TL, 138.0); number(a("in february 2019") + 0.2, 3.2, "8:25.29", "2 mile · US indoor champion", "February 2019 · meet record")
    S(a("then that summer"), S3, 38.0); title(a("then that summer"), 2.8, "2019", "5th · US 5000m")
    S(a("then the injury started"), S3, 4.8, bw=1, slow=0.6)
    S(a("he tore his plantar"), TD, 20.0, bw=1)
    S(a("he had to pull out"), S3, 52.0, bw=1); title(a("he had to pull out"), 3.0, "2019", "Out of Worlds · foot injury")
    S(a("then the big one"), TD, 60.0, bw=1)
    S(a("he missed olympic trials"), TD, 120.0, bw=1); title(a("he missed olympic trials"), 3.0, "2021", "Misses the Olympic Trials · torn plantar fascia")
    S(a("he actually said"), TD, 210.0)
    S(a("and around that same time"), S3, 9.0)
    S(a("tin man elite split"), S3, 36.0)
    S(a("his mom ended up"), BF, 602.0); name(a("his mom ended up"), 3.0, "Joan Hunter", "Head coach · Tinman Elite")
    # 6 so close ----------------------------------------------------------------------------------
    S(PART[6] - 0.05, BF, 579.5, flash=1); chapter(PART[6] + 0.2, "05", "One Spot")
    S(a("2024 olympic trials"), TR, 0.5); date(a("2024 olympic trials"), 2.8, "June 2024", "Olympic Trials · 10,000m")
    S(a("top three go to"), C13, 2.0)
    S(a("and drew hunter finishes"), TR, 30.0, punch=0.4); number(a("finishes fourth"), 2.9, "4th", "10,000m · 2024 Olympic Trials", "27:53.35 · top 3 went to Paris")
    S(a("thats how close"), TR, 60.0, bw=1)
    S(a("then 2025"), CP, 10.0); number(a("then 2025") + 0.2, 3.0, "4th", "5000m · 2025 US Championships", "13:27.16")
    S(a("so every time"), TR, 120.0)
    S(a("hes right there"), BF, 610.0)
    O(a("hes right there") - 0.3, 4.2, ("board", "Drew Hunter at nationals", PRO, "No Olympic or World team"))
    S(a("and honestly thats what"), BU, 686.0)
    S(a("but when you had the hype"), LU, 21.0, bw=1, slow=0.6)
    S(a("people expecting him"), TR, 200.0)
    # 7 the comeback? -----------------------------------------------------------------------------
    S(PART[7] - 0.05, LS, 10.0, flash=1); chapter(PART[7] + 0.2, "06", "Not Washed")
    S(a("cause this year"), CP, 30.0)
    S(a("he won a usa road"), LS, 30.0); title(a("he won a usa road"), 2.8, "2026", "US Road 5K champion")
    S(a("and then in september"), AS, 30.0)
    number(a("he ran 13") + 0.1, 3.4, "13:14", "Road 5K · American record", "World Road Running Champs · Copenhagen · Sept 2026")
    S(a("he wrote something"), AS, 100.0)
    quote(a("running careers are over") - 0.2, 3.6, "Running careers are over in the blink of the eye.", "Drew Hunter · his newsletter · May 2026")
    S(a("and he said he still"), AS, 200.0)
    S(a("and that adidas deal"), GA, 25.0)
    S(a("so that whole chapter"), AS, 320.0)
    S(a("hes 29 now"), TD, 400.0, slow=0.6)
    # 8 your call ---------------------------------------------------------------------------------
    S(PART[8] - 0.05, TR, 250.0, flash=1); chapter(PART[8] + 0.2, "07", "Your Call")
    S(a("was skipping college"), BF, 89.3)
    S(a("was it the injuries"), S3, 4.8, bw=1)
    S(a("or is drew hunter"), CP, 60.0)
    S(a("cause on paper"), LS, 50.0)
    S(a("but he still aint"), TR, 280.0, bw=1)
    S(a("and thats what people"), BF, 625.0)
    S(a("is he gonna make the team"), BF, 620.0)
    S(a("or is he gonna be one"), LU, 14.2, bw=1, slow=0.6)
    S(a("im not sure"), LU, 7.2)

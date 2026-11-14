"""Alan Webb: soundbites + EDL (times are cleaned-VO seconds via the phrase finder A)."""

TAGS = {
    "w_pre2001": "FOX SPORTS NET · PREFONTAINE CLASSIC 2001", "w_tracktown": "TRACKTOWN USA · #THISISTRACKTOWN",
    "w_letterman": "CBS · LATE SHOW WITH DAVID LETTERMAN · 2001", "w_pre2004": "PREFONTAINE CLASSIC · JUNE 2004",
    "w_trials04": "US OLYMPIC TRIALS · SACRAMENTO 2004", "w_athens": "NBC · ATHENS OLYMPICS 2004",
    "w_worlds05": "WORLD CHAMPIONSHIPS · HELSINKI 2005", "w_usas07": "USA CHAMPIONSHIPS · 2007",
    "w_osaka07": "WORLD CHAMPIONSHIPS · OSAKA 2007", "w_lagat07": "WORLD CHAMPIONSHIPS · OSAKA 2007",
    "w_trials08": "US OLYMPIC TRIALS · EUGENE 2008", "w_lr2012": "LETSRUN · OLYMPIC TRIALS 2012",
    "w_lr2014": "LETSRUN · MILLROSE GAMES 2014", "w_podcast26": "THE RUNNING EFFECT PODCAST · MAY 2026",
    "w_pre2001b": "PREFONTAINE CLASSIC · MAY 27, 2001",
}

PRE_SB = ("w_tracktown", 63.8, 76.9, "TRACKTOWN USA · PREFONTAINE CLASSIC, MAY 27, 2001")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("the fastest mile", 1), "w_pre2001", 589.7, 610.9, "FOX SPORTS NET · PRE CLASSIC 2001"),
    (("he was on david", 2), "w_pre2001", 674.4, 688.9, "ALAN WEBB · AGE 18 · MAY 2001"),
    (("track and field news", 2), "w_letterman", 27.8, 35.6, "CBS · LATE SHOW WITH DAVID LETTERMAN"),
    (("and here comes a white", 3), "w_pre2004", 215.3, 224.4, "PRE CLASSIC BROADCAST · 2004"),
    (("so he goes to michigan", 4), "w_letterman", 318.1, 332.7, "CBS · LATE SHOW WITH DAVID LETTERMAN"),
    (("2004 the olympic year", 5), "w_pre2004", 86.0, 100.9, "PRE CLASSIC BROADCAST · 2004"),
    (("then he wins the olympic", 5), "w_pre2004", 349.7, 364.9, "PRE CLASSIC · JUNE 19, 2004"),
    (("so he goes to athens", 5), "w_trials04", 255.3, 261.3, "US OLYMPIC TRIALS · JULY 2004"),
    (("first round", 5), "w_athens", 8.9, 26.0, "NBC · ATHENS 2004"),
    (("and then he came back", 6), "w_athens", 386.9, 393.9, "NBC · ATHENS, AUGUST 20, 2004"),
    (("8th and the", 6), "w_osaka07", 51.6, 58.1, "WORLD CHAMPIONSHIPS · OSAKA 2007"),
    (("2008 olympic trials", 7), "w_osaka07", 217.0, 237.5, "WORLD CHAMPIONSHIPS · OSAKA 2007"),
    (("february 2014", 7), "w_lr2012", 140.7, 147.7, "ALAN WEBB · OLYMPIC TRIALS 2012"),
    (("then he tries a triathlon", 7), "w_lr2014", 7.1, 18.8, "ALAN WEBB · RETIRING, FEB 2014"),
    (("number four", 8), "w_podcast26", 1343.0, 1355.5, "ALAN WEBB · THE RUNNING EFFECT PODCAST, MAY 2026"),
    (("today hes coaching", 9), "w_lr2014", 48.7, 68.8, "ALAN WEBB · FEB 2014"),
    (("so what y all think", 9), "w_pre2001", 723.5, 728.9, "FOX SPORTS NET · PRE CLASSIC 2001"),
]


def edl(a, S, O, stat, say, stack, name, stamp, chapter, PART):
    # 1 cold open -----------------------------------------------------------------------
    S(a("may 27th"), "w_pre2001", 230.0, amb=1); say(a("may 27th"), 2.2, "MAY 27, 2001", "white", "t")
    S(a("eugene oregon"), "w_pre2001", 200.0, amb=1); say(a("eugene oregon"), 2.4, "PREFONTAINE CLASSIC · EUGENE", "white", "b", "PREFONTAINE")
    S(a("an 18 year old"), "w_pre2001", 162.0, punch=1.2); say(a("18 year old"), 1.8, "AGE 18", "orange", "t")
    S(a("against grown men"), "w_pre2001", 235.0, amb=1); say(a("pros"), 1.4, "VS. THE PROS", "white", "c", None, 160)
    S(a("353"), "w_pre2001", 650.0); stat(a("353") + 0.1, 3.0, "3:53.43", "FASTEST HIGH SCHOOL MILE EVER", "gold")
    S(a("later nobody"), "w_pre2001", 660.0, slow=0.6); say(a("nobody has touched"), 2.4, "25 YEARS · STILL THE RECORD", "orange", "b", "25")
    S(a("they said he"), "w_pre2004", 300.0, amb=1); say(a("save america"), 2.4, "THE SAVIOR OF AMERICAN MILING", "white", "b", "SAVIOR")
    S(a("he never won"), "w_athens", 330.0, bw=1); stat(a("he never won") + 0.3, 2.6, "0", "OLYMPIC OR WORLD MEDALS", "red")
    S(a("so what happened"), "w_athens", 390.0, bw=1, punch=0.6); say(a("so what happened"), 2.6, "WHAT WENT WRONG?", "orange", "c", "WRONG?", 170)
    # 2 the kid from Reston -------------------------------------------------------------
    S(PART[2] - 0.15, "w_pre2001", 160.0, flash=1); chapter(PART[2], "01", "THE KID FROM RESTON")
    name(a("south lakes") - 0.3, 3.0, "ALAN WEBB", "SOUTH LAKES HS · RESTON, VIRGINIA")
    S(a("as a sophomore"), "w_pre2001b", 40.0, amb=1); stat(a("4 06") + 0.1, 2.4, "4:06", "MILE · NATIONAL SOPHOMORE RECORD", "gold")
    S(a("that broke jim"), "w_pre2001", 170.0); say(a("jim ryan"), 2.0, "JIM RYUN'S RECORD", "white", "b", "RYUN'S")
    S(a("his senior year"), "w_pre2001b", 90.0, amb=1); say(a("january 2001"), 2.0, "JANUARY 2001 · NEW YORK", "white", "t")
    stat(a("indoors") - 0.2, 2.6, "3:59.86", "1ST US HIGH SCHOOLER UNDER 4:00 INDOORS", "gold")
    S(a("first american high"), "w_pre2001b", 130.0, amb=1)
    S(a("then may"), "w_pre2001", 420.0, amb=1)
    S(a("he breaks jim"), "w_pre2001", 600.0, slow=0.5); stat(a("36 years") - 0.1, 2.6, "36", "YEARS RYUN'S RECORD STOOD", "orange")
    S(a("he was on david"), "w_letterman", 15.0); say(a("letterman") - 0.3, 2.0, "THE LATE SHOW", "white", "t")
    S(a("track and field news"), "w_letterman", 125.0); say(a("high school athlete"), 2.4, "HS ATHLETE OF THE YEAR", "gold", "b", "YEAR")
    # 3 the savior ----------------------------------------------------------------------
    S(PART[3] - 0.15, "w_pre2001", 30.0, flash=1); chapter(PART[3], "02", "THE SAVIOR")
    S(a("the american athletes"), "w_pre2001", 60.0, amb=1)
    S(a("the world record"), "w_pre2001", 12.0); name(a("the world record") + 0.6, 3.0, "HICHAM EL GUERROUJ", "MOROCCO · MILE WORLD RECORD 3:43.13")
    S(a("the best"), "w_pre2001", 140.0, amb=1); stack(a("the best"), 3.6, ["MOROCCO", "KENYA", "ALGERIA"], "orange")
    S(a("and here comes a white"), "w_pre2001", 180.0); say(a("suburbs"), 2.0, "A KID FROM THE D.C. SUBURBS", "white", "b", "KID")
    S(a("people wasn"), "w_pre2001", 690.0); say(a("the future of"), 2.6, "THE FUTURE OF US DISTANCE RUNNING", "orange", "b", "FUTURE")
    # 4 Michigan ------------------------------------------------------------------------
    S(PART[4] - 0.15, "w_letterman", 40.0, flash=1); chapter(PART[4], "03", "MICHIGAN")
    S(a("big 10 championships"), "w_letterman", 45.0); stack(a("big 10 championships"), 5.0, ["BIG TEN XC CHAMPION", "ALL-AMERICAN", "BIG TEN 1500 CHAMPION"], "gold")
    S(a("and then one year"), "w_letterman", 80.0, bw=1); say(a("he leaves"), 1.8, "1 YEAR · GONE", "red", "c", None, 160)
    S(a("he goes back"), "w_pre2004", 150.0); say(a("scott") - 0.2, 2.6, "BACK TO COACH SCOTT RACZKO", "white", "b", "RACZKO")
    S(a("19 years old"), "w_pre2004", 200.0, amb=1); say(a("19 years old"), 2.2, "PRO AT 19 · NIKE", "white", "c", "19", 160)
    # 5 Athens --------------------------------------------------------------------------
    S(PART[5] - 0.15, "w_pre2004", 110.0, flash=1); chapter(PART[5], "04", "ATHENS")
    S(a("he wins the"), "w_pre2004", 330.0, amb=1); stat(a("350") + 0.1, 2.6, "3:50", "PRE CLASSIC MILE · JUNE 2004", "gold")
    S(a("then he wins the olympic"), "w_trials04", 262.0, amb=1); say(a("olympic trials") - 0.2, 2.2, "OLYMPIC TRIALS CHAMPION", "gold", "b", "CHAMPION")
    S(a("so he goes to athens"), "w_athens", 0.0, amb=1); say(a("athens"), 2.0, "ATHENS 2004", "white", "t")
    S(a("america great hope"), "w_athens", 76.0)
    S(a("first round"), "w_athens", 280.0, amb=1); stat(a("ninth") - 0.1, 2.2, "9TH", "IN HIS HEAT · OUT", "red")
    S(a("heat hes out"), "w_athens", 305.0, bw=1); stamp(a("hes out"), 1.6, "ELIMINATED")
    S(a("never even made"), "w_athens", 330.0, bw=1, slow=0.6)
    # 6 the year everything clicked -----------------------------------------------------
    S(PART[6] - 0.15, "w_worlds05", 600.0, flash=1); chapter(PART[6], "05", "2007")
    S(a("2005 he made"), "w_worlds05", 640.0, amb=1); stat(a("9th") - 0.1, 2.0, "9TH", "WORLD CHAMPIONSHIPS FINAL · 2005", "red")
    S(a("but 2007"), "w_pre2004", 300.0, amb=1); say(a("was crazy"), 1.6, "2007", "orange", "c", None, 180)
    stack(a("330 in the"), 4.4, ["1500M · 3:30.54", "800M · 1:43.84"], "gold")
    S(a("and in july"), "w_usas07", 200.0); say(a("in belgium"), 2.0, "BRASSCHAAT, BELGIUM", "white", "t")
    stat(a("346") + 0.1, 3.0, "3:46.91", "AMERICAN MILE RECORD", "gold")
    S(a("that record stood"), "w_usas07", 250.0, amb=1); stat(a("16 years") - 0.1, 2.4, "16", "YEARS AS THE AMERICAN RECORD", "orange")
    S(a("he win usa"), "w_usas07", 330.0, amb=1)
    S(a("he goes to the world"), "w_osaka07", 80.0, amb=1); say(a("osaka"), 1.8, "OSAKA 2007", "white", "t")
    S(a("8th and the"), "w_osaka07", 234.0); stat(a("8th and the") + 0.0, 2.2, "8TH", "WORLD CHAMPIONSHIPS FINAL", "red")
    S(a("it went to an american"), "w_lagat07", 55.0, bw=1); name(a("bernard") - 0.2, 2.8, "BERNARD LAGAT", "USA · 2007 WORLD CHAMPION")
    # 7 the fall ------------------------------------------------------------------------
    S(PART[7] - 0.15, "w_trials08", 30.0, flash=1); chapter(PART[7], "06", "THE FALL")
    S(a("he only needs"), "w_trials08", 150.0, amb=1); say(a("top three"), 1.8, "TOP 3 → BEIJING", "white", "b", "TOP")
    S(a("5th no beijing"), "w_trials08", 230.0, bw=1); stat(a("5th no beijing"), 2.0, "5TH", "OLYMPIC TRIALS 2008", "red"); stamp(a("no beijing"), 1.6, "NO BEIJING")
    S(a("2009 he moves"), "w_lr2012", 80.0); name(a("alberto") - 0.2, 2.4, "ALBERTO SALAZAR", "COACH · 2009–2011")
    S(a("2010 achilles"), "w_lr2012", 114.0, bw=1); stamp(a("surgery"), 1.6, "ACHILLES SURGERY")
    S(a("2011 he leaves"), "w_lr2012", 160.0, bw=1)
    S(a("he moves up"), "w_lr2012", 180.0, bw=1); stack(a("he moves up"), 3.0, ["5000M", "10,000M"], "white")
    S(a("february 2014"), "w_lr2014", 75.0, bw=1); say(a("february 2014"), 2.0, "FEBRUARY 2014 · MILLROSE", "white", "t")
    say(a("retires at"), 2.0, "RETIRED · AGE 31", "red", "c", "31", 160)
    S(a("then he tries a triathlon"), "w_lr2014", 90.0, bw=1); stamp(a("crashed the bike") - 0.3, 1.8, "CRASHED")
    S(a("he went out there"), "w_athens", 315.0, bw=1)
    # 8 what went wrong -----------------------------------------------------------------
    S(PART[8] - 0.15, "w_athens", 380.0, flash=1, bw=1); chapter(PART[8], "07", "WHAT WENT WRONG")
    S(a("the hype"), "w_letterman", 200.0); say(a("the hype") - 0.3, 2.4, "#1 · THE HYPE", "orange", "t", "#1")
    S(a("every race after"), "w_pre2004", 98.0, amb=1)
    S(a("championships"), "w_osaka07", 120.0, amb=1); say(a("championships") - 0.3, 2.4, "#2 · CHAMPIONSHIPS", "orange", "t", "#2")
    S(a("he was flying"), "w_usas07", 280.0)
    S(a("but then big"), "w_osaka07", 200.0, bw=1)
    S(a("three the training"), "w_podcast26", 600.0); say(a("three the training"), 2.4, "#3 · THE TRAINING", "orange", "t", "#3")
    say(a("full arnold") - 0.2, 2.6, "“ARNOLD SCHWARZENEGGER BODYBUILDING”", "white", "b", "ARNOLD")
    S(a("number four"), "w_lr2012", 115.0, bw=1); say(a("number four"), 2.4, "#4 · HIS BODY", "orange", "t", "#4")
    S(a("coach after"), "w_trials08", 200.0, bw=1)
    # 9 so what y'all think -------------------------------------------------------------
    S(PART[9] - 0.15, "w_podcast26", 1200.0, flash=1)
    S(a("allen webb wasn"), "w_usas07", 330.0); stack(a("american record holder") - 0.3, 3.6, ["AMERICAN RECORD", "US CHAMPION", "OLYMPIAN"], "gold")
    S(a("but he was supposed"), "w_pre2001", 690.0, slow=0.6)
    S(a("and he never won"), "w_athens", 390.0, bw=1); stat(a("and he never won") + 0.3, 2.4, "0", "GLOBAL MEDALS", "red")
    S(a("today hes coaching"), "w_podcast26", 1800.0); name(a("ave maria") - 0.4, 2.8, "ALAN WEBB TODAY", "HEAD COACH · AVE MARIA UNIVERSITY")
    S(a("record this summer"), "w_pre2001", 610.0, slow=0.5); say(a("utah"), 2.2, "2026 · A UTAH SENIOR CAME UP SHORT", "white", "b", "SHORT")
    S(a("25 years later it"), "w_pre2001", 655.0); stat(a("25 years later it") + 0.2, 2.6, "3:53.43", "STILL THE RECORD · 25 YEARS", "gold")
    S(a("so what y all think"), "w_pre2001", 700.0)
    O(a("is it the hype") - 0.2, 6.0, ("endq", "THE HYPE? THE TRAINING?", "OR DID HE PEAK IN HIGH SCHOOL?"))
    S(a("y all let me") - 0.3, "w_letterman", 380.0)

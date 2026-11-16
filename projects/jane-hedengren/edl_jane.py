"""Jane Hedengren: soundbites + EDL (times are cleaned-VO seconds via the phrase finder A).
No FloTrack/MileSplit footage. Phrases use _tok forms: apostrophes dropped, numbers <=20 as words,
and whisper's own spellings of the cleaned VO (e.g. "hendergren", "tui", "kalen")."""

TAGS = {
    "j_nike": "NIKE · RUN BIGGER (2025)", "j_ksl": "KSL · BEYOND THE GAME (2025)",
    "j_nxn24": "RUNNERSPACE · NIKE CROSS NATIONALS 2024", "j_nin_mile": "RUNNERSPACE · NIKE INDOOR NATIONALS 2025",
    "j_ncaaxc25": "ESPN · NCAA CROSS COUNTRY 2025", "j_millrose_int": "LETSRUN · MILLROSE GAMES 2026",
    "j_ncaa10k26": "ESPN · NCAA CHAMPIONSHIPS · JUNE 2026", "j_bedridden": "LETSRUN · NCAA CHAMPIONSHIPS · JUNE 2026",
    "j_letsrun_slump": "LETSRUN TRACK TALK · SEPTEMBER 2026", "j_big12_26": "BIG 12 CONFERENCE · XC CHAMPIONSHIP 2026",
    "j_stride": "THE STRIDE REPORT · JANUARY 2026", "j_cain_nyt": "NEW YORK TIMES OPINION · 2019",
    "j_valby_usa": "LETSRUN · USATF CHAMPIONSHIPS 2026",
    "t_nxn2017": "RUNNERSPACE · NIKE CROSS NATIONALS 2017", "t_ncaaxc22": "ESPN · NCAA CROSS COUNTRY 2022",
    "t_letsrun26": "LETSRUN · BOSTON, APRIL 2026", "t_trials24": "RUNNERSPACE · OLYMPIC TRIALS 2024",
    "t_mile2018": "NEW BALANCE NATIONALS · 2018", "t_citius_pro": "CITIUS MAG · DECEMBER 2023",
    "a_ncaa200": "ESPN · NCAA CHAMPIONSHIPS 2022", "a_citius_trials24": "CITIUS MAG · OLYMPIC TRIALS 2024",
    "a_wc_4x100": "WORLD CHAMPIONSHIPS · EUGENE 2022",
}

# cold open: Jane in her own words, Nike film
PRE_SB = ("j_nike", 268.9, 275.2, "JANE HEDENGREN · NIKE, 2025")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("her name is", 1), "j_nike", 64.7, 71.0, "RACE CALL · 2025"),
    (("then 2025 was", 2), "j_nxn24", 1082.0, 1107.1, "RUNNERSPACE · NXN 2024 · COURSE RECORD 16:32.7"),
    (("april she runs", 2), "j_nin_mile", 512.3, 522.6, "RUNNERSPACE · NIKE INDOOR NATIONALS · MARCH 2025"),
    (("now this where", 3), "j_nike", 130.3, 142.5, "NIKE · RUN BIGGER (2025)"),
    (("and in college", 3), "j_ksl", 116.0, 128.1, "TIMPVIEW COACH JAIMIE RIBERA · KSL"),
    (("then indoors", 4), "j_ncaaxc25", 1109.2, 1124.2, "ESPN · NCAA CROSS COUNTRY · NOV 22, 2025"),
    (("third in the", 5), "j_bedridden", 17.4, 27.2, "JANE HEDENGREN · LETSRUN · JUNE 2026"),
    (("september the cowboy", 5), "j_ncaa10k26", 1373.3, 1386.8, "ESPN · NCAA 10,000M FINAL · JUNE 2026"),
    (("october the pre", 5), "j_letsrun_slump", 49.1, 66.3, "LETSRUN TRACK TALK · SEPT 2026"),
    (("but sick at", 5), "j_big12_26", 1261.1, 1276.0, "BIG 12 XC CHAMPIONSHIP · OCT 31, 2026"),
    (("and it aint just", 6), "t_letsrun26", 148.6, 157.3, "KATELYN TUOHY · LETSRUN · APRIL 2026"),
    (("abby steiner", 6), "j_cain_nyt", 41.8, 57.0, "MARY CAIN · NYT OPINION 2019 · SALAZAR DENIED HER CLAIMS"),
    (("dominant in high", 6), "a_citius_trials24", 49.6, 52.9, "ABBY STEINER · CITIUS MAG · 2024"),
    (("so it can be", 6), "j_valby_usa", 115.0, 122.3, "PARKER VALBY · LETSRUN · JULY 2026"),
    (("thats a coach", 6), "j_stride", 887.6, 902.8, "COACH DILJEET TAYLOR · THE STRIDE REPORT"),
    (("november 21st", 8), "j_ncaaxc25", 1258.1, 1287.6, "ESPN · NCAA CROSS COUNTRY 2025"),
    (("so what y all", 9), "j_stride", 906.0, 921.8, "JANE HEDENGREN · THE STRIDE REPORT"),
]


def edl(a, S, O, stat, say, stack, name, stamp, chapter, PART):
    # 1 cold open -----------------------------------------------------------------------
    S(a("y all remember"), "t_ncaaxc22", 1004.0, amb=1); say(a("kaitlyn toohey"), 2.0, "KATELYN TUOHY", "white", "b")
    S(a("the greatest high"), "t_nxn2017", 1150.0, amb=1); say(a("the greatest high"), 2.4, "GREATEST HS RUNNER EVER", "orange", "b", "GREATEST")
    S(a("and then she disappeared"), "t_letsrun26", 30.0, bw=1); stamp(a("disappeared"), 1.4, "GONE")
    S(a("well theres a girl"), "j_ksl", 10.5, amb=1); say(a("from utah"), 1.6, "UTAH", "white", "t")
    S(a("broke almost every"), "j_nike", 146.0, punch=0.8)
    stack(a("high school records"), 3.6, ["HIGH SCHOOL RECORDS", "COURSE RECORDS", "NCAA RECORDS"], "gold")
    S(a("high school records"), "j_nxn24", 900.0, amb=1)
    S(a("chorus records"), "j_big12_26", 600.0, amb=1)
    S(a("ncaa records"), "j_ncaa10k26", 22.0, amb=1)
    S(a("shes twenty years"), "j_nike", 244.0); name(a("shes twenty years"), 3.0, "JANE HEDENGREN", "BYU · AGE 20")
    S(a("and right now"), "j_bedridden", 60.0, bw=1)
    S(a("so is jane"), "j_ncaa10k26", 1379.0, bw=1, slow=0.6); say(a("next one to fall"), 2.4, "THE NEXT TO FALL OFF?", "red", "c", "FALL", 160)
    # 2 the kid from Provo --------------------------------------------------------------
    S(PART[2] - 0.15, "j_nike", 5.0, flash=1); chapter(PART[2], "01", "THE KID FROM PROVO")
    S(a("10th view"), "j_ksl", 214.0); say(a("10th view"), 2.4, "TIMPVIEW HS · PROVO, UTAH", "white", "b", "TIMPVIEW")
    S(a("her dad was"), "j_nike", 16.5); name(a("her dad was"), 2.8, "JOHN HEDENGREN", "HER DAD · ALL-AMERICAN RUNNER")
    S(a("so its in"), "j_nike", 293.0, amb=1)
    S(a("december 2024"), "j_nxn24", 160.0, amb=1); say(a("december 2024"), 2.2, "NIKE CROSS NATIONALS · DEC 2024", "white", "t")
    S(a("she wins it"), "j_nxn24", 860.0, punch=0.6); stat(a("course record") + 0.1, 2.4, "16:32.7", "NXN COURSE RECORD", "gold")
    S(a("she breaks kaitlyn"), "t_nxn2017", 1160.0, bw=1); say(a("she breaks kaitlyn"), 2.2, "TUOHY'S RECORD · GONE", "orange", "b", "GONE")
    S(a("march"), "j_ksl", 120.0, amb=1)
    S(a("she runs the 5k"), "j_nike", 125.0, amb=1); stat(a("fifteen thirteen"), 2.4, "15:13.26", "5000M · FASTEST HS GIRL EVER", "gold")
    S(a("three days later"), "j_nin_mile", 330.0, amb=1); stat(a("426"), 2.4, "4:26.14", "INDOOR MILE · NATIONAL RECORD", "gold")
    S(a("april she runs"), "j_ksl", 109.0, amb=1); stat(a("fourteen 57"), 2.6, "14:57.93", "1ST HS GIRL UNDER 15:00", "gold")
    S(a("june the mile"), "j_nike", 103.0, amb=1); stat(a("423 50"), 2.4, "4:23.50", "MILE · NATIONAL RECORD", "gold")
    S(a("best in high school"), "t_mile2018", 350.0, bw=1); say(a("best in high school"), 2.4, "TUOHY'S BEST: 4:33", "white", "b", "4:33")
    S(a("jane ran ten"), "j_nike", 58.0, punch=0.4); say(a("ten seconds faster"), 2.0, "10 SECONDS FASTER", "orange", "c", "10", 160)
    S(a("then nine seventeen"), "j_ksl", 122.0, amb=1); stack(a("then nine seventeen"), 4.6, ["2 MILE · 9:17.75", "3000M · 8:40.03"], "gold")
    S(a("then eight 40"), "j_nike", 105.0, amb=1)
    S(a("nine national high"), "j_nike", 136.0); stat(a("nine national high") + 0.1, 2.8, "9", "NATIONAL HS RECORDS · 1 YEAR", "gold")
    # 3 same story, new name ------------------------------------------------------------
    S(PART[3] - 0.15, "t_nxn2017", 1170.0, flash=1); chapter(PART[3], "02", "SAME STORY, NEW NAME")
    S(a("kaitlyn toohey had"), "t_nxn2017", 1180.0, amb=1); say(a("kaitlyn toohey had"), 2.0, "TUOHY · NXN CHAMPION", "white", "b", "TUOHY")
    S(a("jane got one"), "j_nxn24", 1108.0, amb=1); say(a("jane got one"), 1.6, "JANE · NXN CHAMPION", "orange", "b", "JANE")
    S(a("kaitlyn signed with"), "t_citius_pro", 40.0); say(a("adidas"), 1.6, "ADIDAS", "white", "c", None, 160)
    S(a("jane signed the nil"), "j_nike", 233.0); say(a("nil deal"), 1.8, "NIL DEAL · NIKE", "orange", "c", "NIKE", 160)
    S(a("kalen signed with"), "t_ncaaxc22", 1008.0, amb=1); say(a("north carolina state"), 2.0, "NC STATE · NCAA TITLES", "white", "b", "NC")
    S(a("jane went with"), "j_stride", 250.0, amb=1); name(a("coach dejeet") - 0.2, 2.8, "DILJEET TAYLOR", "BYU HEAD COACH")
    S(a("coach dejeet"), "j_stride", 868.0)
    # 4 freshman year -------------------------------------------------------------------
    S(PART[4] - 0.15, "j_ncaaxc25", 60.0, flash=1); chapter(PART[4], "03", "FRESHMAN YEAR")
    say(a("october 2025"), 2.0, "OCTOBER 2025", "white", "t"); S(a("her first college race"), "j_ncaaxc25", 260.0, amb=1)
    stamp(a("course record she wins") , 1.4, "COURSE RECORD", "gold")
    S(a("she wins the big"), "j_big12_26", 400.0, amb=1); say(a("big twelve"), 1.8, "BIG 12 CHAMPION", "orange", "b", "BIG")
    S(a("ncaa cross country second"), "j_ncaaxc25", 379.0, amb=1)
    S(a("second place"), "j_ncaaxc25", 971.0, amb=1); stat(a("second place"), 2.2, "2ND", "NCAA XC · AS A FRESHMAN", "orange")
    S(a("fastest freshman"), "j_ncaaxc25", 1210.0, slow=0.6)
    S(a("december fourteen"), "j_stride", 300.0, amb=1); stat(a("fourteen 44"), 2.6, "14:44.79", "5000M · COLLEGIATE RECORD", "gold")
    S(a("february 2026"), "j_millrose_int", 20.0); say(a("milrose"), 2.0, "MILLROSE GAMES · FEB 2026", "white", "t")
    stat(a("eight 34 98"), 2.6, "8:34.98", "3000M · UNDER TUOHY'S 8:35.20", "gold")
    S(a("and guess who"), "t_ncaa5k22", 660.0, bw=1); say(a("kaitlyn tui"), 1.8, "TUOHY'S RECORD", "white", "c", "TUOHY'S", 160)
    S(a("march nc double"), "j_ncaa10k26", 30.0, amb=1)
    stack(a("she wins the 5k"), 4.0, ["NCAA 5000M CHAMPION", "NCAA 3000M CHAMPION"], "gold")
    S(a("first freshman"), "j_ncaa10k26", 40.0); say(a("first freshman"), 2.4, "1ST FRESHMAN EVER · THE DOUBLE", "orange", "b", "1ST")
    S(a("april ncaa record"), "j_ncaa10k26", 500.0, amb=1); stat(a("april ncaa record") + 0.3, 2.4, "30:46.80", "10,000M · NCAA RECORD", "gold")
    S(a("two weeks later"), "j_ncaa10k26", 700.0, amb=1); stat(a("two weeks later") + 0.3, 2.4, "14:50.50", "5000M · NCAA RECORD", "gold")
    # 5 the first cracks ----------------------------------------------------------------
    S(PART[5] - 0.15, "j_ncaa10k26", 50.0, flash=1, bw=1); chapter(PART[5], "04", "THE FIRST CRACKS")
    S(a("ncaa outdoors june"), "j_ncaa10k26", 212.0, amb=1); say(a("june 2026"), 2.0, "NCAA OUTDOORS · JUNE 2026", "white", "t")
    S(a("shes sick going"), "j_bedridden", 25.0, bw=1); stamp(a("sick"), 1.4, "SICK")
    S(a("third in the 10k"), "j_ncaa10k26", 1300.0, slow=0.6); stack(a("third in the 10k"), 3.4, ["10,000M · 3RD", "5000M · 9TH"], "red")
    S(a("ninth in the"), "j_bedridden", 100.0, bw=1)
    S(a("september the cowboy"), "j_big12_26", 68.0, amb=1); say(a("cowboy jamboree"), 2.0, "COWBOY JAMBOREE · SEPT 2026", "white", "t")
    S(a("she hadnt raced"), "j_letsrun_slump", 20.0)
    S(a("third the first"), "j_letsrun_slump", 504.0); stat(a("third the first"), 2.2, "3RD", "1ST REGULAR-SEASON LOSS", "red")
    S(a("october the pre"), "j_letsrun_slump", 160.0); say(a("pre national"), 2.2, "PRE-NATIONALS · OCTOBER 2026", "white", "t")
    S(a("jane didnt run"), "j_big12_26", 1323.0, bw=1); stamp(a("jane didnt run"), 1.6, "DNS")
    S(a("her coach said"), "j_stride", 894.0, bw=1); say(a("tail end"), 2.4, "“TAIL END OF AN ILLNESS”", "white", "b", "ILLNESS")
    S(a("now dont get me"), "j_big12_26", 700.0, amb=1)
    S(a("won the big"), "j_big12_26", 1240.0, punch=0.8); stat(a("by ten seconds"), 2.2, "10 SEC", "BIG 12 WIN · OCT 31, 2026", "gold")
    S(a("but sick at"), "j_bedridden", 150.0, bw=1)
    stack(a("but sick at"), 4.6, ["JUNE · SICK", "SEPTEMBER · A LOSS", "OCTOBER · SICK"], "red")
    S(a("a loss in september"), "j_letsrun_slump", 874.0, bw=1)
    S(a("where have we heard"), "t_letsrun26", 150.0, bw=1, punch=0.5)
    # 6 they all fell off ---------------------------------------------------------------
    S(PART[6] - 0.15, "t_ncaaxc22", 1010.0, flash=1); chapter(PART[6], "05", "THEY ALL FELL OFF")
    S(a("she won in college"), "t_ncaa5k22", 650.0, amb=1)
    S(a("then she turned pro"), "t_citius_pro", 60.0)
    S(a("and then it was injuries"), "t_trials24", 90.0, bw=1); say(a("injuries"), 1.6, "INJURIES", "red", "c", None, 160)
    S(a("she said she was keeping"), "t_letsrun26", 100.0, bw=1)
    S(a("then she stopped"), "t_letsrun26", 60.0, bw=1, slow=0.6); stamp(a("stopped racing"), 1.6, "STOPPED RACING")
    S(a("mary kane"), "j_cain_nyt", 321.0); name(a("mary kane"), 2.8, "MARY CAIN", "FASTEST GIRL IN AMERICA · AGE 17")
    S(a("went pro"), "j_cain_nyt", 367.0)
    S(a("later she said"), "j_cain_nyt", 7.0, bw=1)
    S(a("she says she was never"), "j_cain_nyt", 99.0, bw=1)
    S(a("steiner fastest"), "a_ncaa200", 20.0, amb=1); name(a("steiner fastest") - 0.3, 2.6, "ABBY STEINER", "FASTEST COLLEGE WOMAN EVER")
    S(a("two years later she"), "a_citius_trials24", 30.0, bw=1)
    S(a("y all seen that"), "a_wc_4x100", 100.0, bw=1)
    S(a("dominant in high"), "t_nxn2017", 1170.0, bw=1)
    S(a("dominant in college"), "t_ncaaxc22", 1010.0, bw=1)
    S(a("then gone"), "t_letsrun26", 160.0, bw=1, slow=0.6); stamp(a("then gone"), 1.4, "GONE")
    S(a("now the one that came"), "j_valby_usa", 30.0); name(a("parker valby"), 2.8, "PARKER VALBY", "6 NCAA TITLES · 2024 OLYMPIAN")
    S(a("broke her foot"), "j_valby_usa", 100.0, bw=1); say(a("broke her foot"), 2.0, "BROKEN FOOT · ~1 YEAR OUT", "red", "b", "FOOT")
    S(a("this year she ran"), "j_valby_usa", 60.0); stat(a("1439"), 2.4, "14:39.88", "5000M PB · 3RD AT USAs 2026", "gold")
    S(a("nobodys saying"), "j_big12_26", 1290.0, amb=1)
    S(a("jane coach is literally"), "j_stride", 140.0, amb=1)
    S(a("she cut back"), "j_stride", 450.0, amb=1); say(a("cut back"), 1.8, "LESS TRAINING", "white", "c", "LESS", 160)
    S(a("her coach said more"), "j_stride", 870.0)
    say(a("more is not"), 2.6, "“MORE IS NOT NECESSARILY BETTER”", "white", "b", "BETTER")
    say(a("sometimes less"), 2.6, "“SOMETIMES LESS IS ACTUALLY MORE”", "orange", "b", "LESS")
    # 7 what's different ----------------------------------------------------------------
    S(PART[7] - 0.15, "j_stride", 600.0, flash=1); chapter(PART[7], "06", "WHAT'S DIFFERENT")
    S(a("tui turned pro"), "t_citius_pro", 120.0, bw=1); say(a("left her college"), 2.2, "TUOHY · LEFT NC STATE EARLY", "white", "b", "LEFT")
    S(a("jane is still"), "j_stride", 160.0); say(a("same coach"), 2.6, "SAME COACH · SAME TEAM", "orange", "b", "SAME")
    S(a("with the team around"), "j_big12_26", 1600.0)
    S(a("and when they asked"), "j_nike", 211.0); name(a("kara goucher"), 2.8, "KARA GOUCHER", "2-TIME OLYMPIAN")
    S(a("she said usain"), "j_nike", 233.0, slow=0.6); say(a("she said usain"), 2.0, "“USAIN BOLT”", "orange", "c", "BOLT", 170)
    S(a("and personally"), "j_nike", 266.0)
    S(a("but she said usain"), "j_nxn24", 600.0, amb=1)
    S(a("she said there is"), "j_nike", 244.0, punch=0.5); say(a("no one comparable"), 2.6, "“NO ONE COMPARABLE TO HER”", "white", "b", "COMPARABLE")
    # 8 what's next ---------------------------------------------------------------------
    S(PART[8] - 0.15, "j_ncaaxc25", 30.0, flash=1); chapter(PART[8], "07", "WHAT'S NEXT")
    say(a("november 21st"), 2.4, "NCAA XC · NOV 21 · TERRE HAUTE", "white", "t")
    S(a("last year she got"), "j_ncaaxc25", 1130.0, amb=1); stat(a("second"), 2.0, "2ND", "NCAA XC 2025", "orange")
    S(a("this year shes"), "j_big12_26", 1250.0); say(a("the favorite"), 1.8, "THE FAVORITE", "gold", "c", "FAVORITE", 160)
    S(a("if she wins"), "j_nike", 146.0, slow=0.7)
    S(a("if she dont"), "t_letsrun26", 155.0, bw=1)
    S(a("and thats just"), "j_ncaa10k26", 1380.0, bw=1)
    # 9 so what y'all think -------------------------------------------------------------
    S(PART[9] - 0.15, "j_nike", 352.0, flash=1)
    S(a("i hope this girl"), "j_nike", 350.0)
    S(a("we already watched"), "t_letsrun26", 158.0, bw=1)
    S(a("really a handful"), "j_cain_nyt", 64.0, bw=1)
    S(a("i dont wanna"), "j_nike", 377.0, slow=0.7)
    S(a("so what y all"), "j_ksl", 16.0)
    O(a("is jane") - 0.2, 6.0, ("endq", "THE NEXT GREAT AMERICAN RUNNER?", "OR THE NEXT TO FALL OFF?"))
    S(a("or is she"), "j_ncaa10k26", 50.0, slow=0.6)

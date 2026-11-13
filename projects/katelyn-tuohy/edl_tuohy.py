"""Katelyn Tuohy: soundbites + EDL (times are cleaned-VO seconds via the phrase finder A)."""

TAGS = {
    "t_nxn2017": "RUNNERSPACE · NIKE CROSS NATIONALS 2017", "t_nxn2019": "RUNNERSPACE · NIKE CROSS NATIONALS 2019",
    "t_mile2018": "NEW BALANCE NATIONALS · 2018", "t_gatorade": "GATORADE · PLAYER OF THE YEAR 2018",
    "t_ncaa5k22": "ESPN · NCAA CHAMPIONSHIPS 2022", "t_ncaaxc22": "ESPN · NCAA CROSS COUNTRY 2022",
    "t_citius_pro": "CITIUS MAG · DECEMBER 2023", "t_citius_xc23": "CITIUS MAG · NCAA XC 2023",
    "t_trials24": "RUNNERSPACE · OLYMPIC TRIALS 2024", "t_sunset24": "RUNNERSPACE · SUNSET TOUR 2024",
    "t_sander25": "CITIUS MAG · DR. SANDER 2025", "t_sanderrace25": "RUNNERSPACE · DR. SANDER 2025",
    "t_portland25": "TRACKLANDIA · PORTLAND 2025", "t_asics26": "RUNNERSPACE · WINSTON-SALEM 2026",
    "t_letsrun26": "LETSRUN · BOSTON, APRIL 2026",
    "ph_record": "PHOTO: JENARAGON94 · CC BY 2.0", "ph_armory1": "PHOTO: JENARAGON94 · CC BY 2.0",
    "ph_armory2": "PHOTO: JENARAGON94 · CC BY 2.0", "ph_armory3": "PHOTO: JENARAGON94 · CC BY 2.0",
    "ph_armory4": "PHOTO: JENARAGON94 · CC BY 2.0", "ph_armory5": "PHOTO: JENARAGON94 · CC BY 2.0",
    "ph_armory6": "PHOTO: JENARAGON94 · CC BY 2.0", "ph_portland": "PHOTO: JOE PEACOCK · CC BY-SA 4.0",
}

PRE_SB = ("t_nxn2017", 1124.6, 1137.6, "RUNNERSPACE · NIKE CROSS NATIONALS 2017")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("six years later", 1), "t_gatorade", 54.0, 64.3, "HER HIGH SCHOOL COACH · GATORADE 2018"),
    (("she broke mary", 2), "t_mile2018", 344.0, 356.0, "NEW BALANCE NATIONALS · MILE · 4:33.87"),
    (("one coach told", 2), "t_gatorade", 119.4, 126.4, "KATELYN TUOHY · GATORADE 2018"),
    (("november 2022", 4), "t_ncaa5k22", 659.6, 665.6, "ESPN · NCAA 5000M FINAL · JUNE 11, 2022"),
    (("then 2023", 4), "t_ncaaxc22", 1005.0, 1013.3, "ESPN · NCAA CROSS COUNTRY · NOV 19, 2022"),
    (("everything they said", 4), "t_ncaa5k22", 680.3, 694.8, "ESPN · ON COACH LAURIE HENES"),
    (("and thats where it started", 5), "t_citius_pro", 195.1, 203.6, "KATELYN TUOHY · ON TURNING PRO · DEC 2023"),
    (("her first race of the whole", 6), "t_trials24", 62.7, 85.0, "KATELYN TUOHY · OLYMPIC TRIALS 2024"),
    (("she did come back", 6), "t_trials24", 356.8, 375.1, "KATELYN TUOHY · OLYMPIC TRIALS 2024"),
    (("june 2025", 6), "t_sander25", 36.1, 52.9, "KATELYN TUOHY · JANUARY 2025"),
    (("one week later", 7), "t_asics26", 271.0, 275.0, "RUNNERSPACE · HER LAST WIN · FEB 21, 2026"),
    (("they asked her if", 7), "t_letsrun26", 101.3, 117.0, "KATELYN TUOHY · APRIL 18, 2026"),
    (("and we gonna respect", 7), "t_letsrun26", 152.8, 157.0, "KATELYN TUOHY · APRIL 18, 2026"),
    (("she didnt run it literally", 7), "t_letsrun26", 80.0, 87.4, "KATELYN TUOHY · APRIL 18, 2026"),
    (("now imma keep it real", 9), "t_letsrun26", 162.0, 170.5, "KATELYN TUOHY · HER LAST INTERVIEW · APRIL 2026"),
    (("so what y all think", 9), "t_trials24", 390.3, 402.5, "KATELYN TUOHY · 2024"),
]


def edl(a, S, O, stat, say, stack, name, stamp, chapter, PART):
    # 1 cold open -----------------------------------------------------------------------
    S(a("december 2017"), "t_nxn2017", 1110.0, amb=1); say(a("december 2017"), 2.0, "DECEMBER 2017", "white", "t")
    S(a("a 15 year old"), "t_nxn2017", 1095.0, amb=1); say(a("15 year old"), 1.8, "AGE 15", "white", "t")
    S(a("wins the biggest"), "t_nxn2017", 1112.0, amb=1, punch=1.0); say(a("biggest high school"), 2.6, "NIKE CROSS NATIONALS", "orange", "b", "NATIONALS")
    S(a("by 40 seconds"), "t_nxn2017", 1170.0, slow=0.6); stat(a("by 40 seconds"), 2.4, "40 SEC", "WINNING MARGIN", "gold")
    S(a("her county gave"), "ph_armory3", 0.0); say(a("tuohy day") - 0.6, 2.6, "“KATELYN TUOHY DAY”", "orange", "c", "DAY", 150)
    S(a("she was just a sophomore"), "ph_armory4", 0.0); say(a("sophomore"), 1.6, "A SOPHOMORE", "white", "b")
    S(a("the new york times"), "ph_armory1", 0.0); say(a("next great running hope") - 0.2, 3.0, "“AMERICA'S NEXT GREAT RUNNING HOPE”", "white", "b", "HOPE")
    S(a("six years later"), "t_sanderrace25", 422.0, amb=1); say(a("pro deal"), 2.2, "PRO DEAL · ADIDAS", "white", "b", "ADIDAS")
    S(a("and now"), "t_letsrun26", 30.0, bw=1)
    S(a("she aint raced"), "ph_portland", 0.0, bw=1); stamp(a("since april"), 1.8, "NO RACES SINCE APRIL")
    S(a("at least not"), "t_asics26", 200.0, bw=1)
    S(a("no updates"), "ph_armory2", 0.0, bw=1); stack(a("no updates"), 2.6, ["NO UPDATES", "NOTHING"], "red")
    S(a("so where did"), "t_letsrun26", 150.0, bw=1, punch=0.8); say(a("so where did"), 2.6, "WHERE DID SHE GO?", "orange", "c", "GO?", 170)
    # 2 the phenom ----------------------------------------------------------------------
    S(PART[2] - 0.15, "t_nxn2017", 300.0, flash=1, amb=1); chapter(PART[2], "01", "THE PHENOM")
    name(a("north rockland") - 0.3, 3.0, "KATELYN TUOHY", "NORTH ROCKLAND HS · ROCKLAND COUNTY, NY")
    S(a("and y all gotta"), "t_nxn2017", 420.0, amb=1)
    S(a("she wasnt just good"), "t_nxn2017", 560.0, amb=1)
    S(a("she was breaking records"), "ph_armory5", 0.0); say(a("decades") - 0.2, 1.8, "DECADES", "orange", "c", None, 170)
    S(a("at 15"), "ph_armory6", 0.0); stat(a("1537"), 2.6, "15:37", "5000M · AGE 15 · HS RECORD", "gold")
    S(a("fastest high school girl"), "ph_armory1", 3.0); say(a("fastest high school girl"), 2.0, "FASTEST HS GIRL EVER", "white", "b", "EVER")
    S(a("at 16"), "t_mile2018", 120.0, amb=1); stat(a("the mile in") + 0.3, 2.8, "4:33.87", "MILE · AGE 16 · HS RECORD", "gold")
    S(a("that broke the high school"), "t_mile2018", 330.0, amb=1); stat(a("36 years"), 2.4, "36", "YEARS THE OLD RECORD STOOD", "orange")
    S(a("she broke mary"), "ph_record", 0.0); say(a("mary cain"), 2.2, "MARY CAIN'S 3000M RECORD", "white", "b", "3000M")
    S(a("racing against pros"), "ph_armory2", 0.0); say(a("racing against pros"), 2.0, "VS. THE PROS", "orange", "t")
    S(a("nike cross nationals"), "t_nxn2017", 160.0, amb=1)
    S(a("she won in three"), "t_nxn2017", 1150.0); stat(a("she won in three") + 0.2, 2.6, "3×", "NXN CHAMPION · 2017–2019", "gold")
    S(a("nobody had ever"), "t_nxn2017", 1220.0); say(a("nobody had ever"), 2.2, "FIRST EVER", "orange", "c", None, 170)
    S(a("one coach told"), "ph_armory3", 0.0); say(a("best high school runner") - 0.2, 3.0, "“THE BEST HIGH SCHOOL RUNNER EVER”", "white", "b", "BEST")
    # 3 the weight ----------------------------------------------------------------------
    S(PART[3] - 0.15, "ph_armory4", 0.0, flash=1, bw=1); chapter(PART[3], "02", "THE WEIGHT")
    S(a("all that attention"), "t_gatorade", 30.0, bw=1); say(a("on a teenager"), 1.8, "ON A TEENAGER", "red", "b")
    S(a("she said it herself"), "t_gatorade", 104.0, bw=1); say(a("a lot of pressure") - 0.2, 3.0, "“A LOT OF PRESSURE AND ATTENTION”", "white", "b", "PRESSURE")
    S(a("she said she stopped"), "ph_armory6", 0.0, bw=1); stack(a("she said she stopped"), 4.6, ["STOPPED READING ARTICLES", "STOPPED READING COMMENTS"], "red")
    S(a("and right after"), "t_nxn2017", 1300.0, bw=1, slow=0.5); stamp(a("knee surgery"), 1.8, "KNEE SURGERY")
    # 4 NC State ------------------------------------------------------------------------
    S(PART[4] - 0.15, "t_ncaa5k22", 70.0, flash=1, amb=1); chapter(PART[4], "03", "NC STATE")
    name(a("coach") - 0.2, 2.6, "LAURIE HENES", "HEAD COACH · NC STATE")
    S(a("freshman year"), "t_ncaa5k22", 160.0, bw=1); say(a("she was hurt"), 1.8, "HURT", "red", "c", None, 170)
    S(a("but year two"), "t_ncaa5k22", 300.0, amb=1)
    S(a("june 2022"), "t_ncaa5k22", 652.0, amb=1); stat(a("ncaa champion"), 2.6, "15:18.39", "NCAA 5000M CHAMPION · 2022", "gold")
    S(a("november 2022"), "t_ncaaxc22", 960.0, amb=1); say(a("cross country champion") - 0.3, 2.2, "NCAA XC CHAMPION", "gold", "t", "CHAMPION")
    S(a("she ran down"), "t_ncaaxc22", 1000.0, punch=0.8); say(a("parker valby"), 2.0, "RAN DOWN PARKER VALBY", "white", "b", "VALBY")
    S(a("then 2023"), "t_citius_xc23", 8.0); say(a("she went crazy"), 1.6, "2023", "orange", "c", None, 170)
    S(a("ncaa record in a mile"), "t_ncaa5k22", 520.0, amb=1); stack(a("ncaa record in a mile"), 5.4, ["NCAA RECORD · MILE 4:24.26", "NCAA RECORD · 3000M 8:35.20", "NCAA RECORD · 5000M 15:03.12"], "gold")
    S(a("2 more ncaa"), "t_ncaa5k22", 700.0, amb=1)
    S(a("4 individual"), "t_ncaaxc22", 1200.0); stack(a("4 individual"), 4.0, ["4 INDIVIDUAL NCAA TITLES", "3 TEAM TITLES", "3 NCAA RECORDS"], "gold")
    S(a("everything they said"), "t_ncaa5k22", 800.0)
    # 5 going pro -----------------------------------------------------------------------
    S(PART[5] - 0.15, "t_sanderrace25", 72.0, flash=1); chapter(PART[5], "04", "GOING PRO")
    say(a("turns pro") - 0.2, 2.2, "PRO · ADIDAS", "white", "t", "ADIDAS")
    S(a("and she skips"), "t_sunset24", 1042.0); say(a("her last year"), 2.4, "SKIPS HER LAST COLLEGE SEASON", "orange", "b", "SKIPS")
    S(a("and thats where"), "t_sanderrace25", 452.0, bw=1); say(a("sideways") - 0.2, 1.8, "SIDEWAYS", "red", "c", None, 170)
    # 6 the slide -----------------------------------------------------------------------
    S(PART[6] - 0.15, "t_trials24", 10.0, flash=1); chapter(PART[6], "05", "THE SLIDE")
    say(a("olympic year"), 1.8, "2024 · OLYMPIC YEAR", "white", "t")
    S(a("she did not race"), "ph_armory6", 0.0, bw=1); stat(a("she did not race"), 2.4, "0", "RACES · WINTER & SPRING 2024", "red")
    S(a("a hamstring"), "t_trials24", 95.0, bw=1); stack(a("a hamstring"), 4.6, ["HAMSTRING TEAR", "BACK", "IT BAND", "KNEE"], "red")
    S(a("her first race of the whole"), "t_trials24", 20.0); say(a("olympic trials") - 0.2, 2.0, "OLYMPIC TRIALS 2024", "white", "t")
    S(a("she makes the final"), "t_trials24", 160.0, bw=1); stat(a("12th") - 0.1, 2.2, "12TH", "OLYMPIC TRIALS 5000M FINAL", "red")
    stamp(a("no pairs"), 1.6, "NO PARIS")
    S(a("she did come back"), "t_sunset24", 890.0, amb=1); say(a("in la"), 2.2, "WIN · SUNSET TOUR, LA · 15:07", "gold", "b", "WIN")
    S(a("january 2025"), "t_sanderrace25", 425.0, amb=1); stat(a("she ran 425") + 0.2, 2.6, "4:25.54", "MILE · WORLD LEAD", "gold")
    S(a("june 2025"), "t_portland25", 905.0, amb=1); say(a("she won in portland"), 2.0, "WIN · PORTLAND · 15:04", "gold", "b", "WIN")
    S(a("but then the usa"), "ph_portland", 0.0, bw=1); stat(a("19th") - 0.1, 2.4, "19TH", "USA CHAMPS 5000M · 2025", "red")
    S(a("in december"), "t_portland25", 870.0, bw=1)
    # 7 the disappearance ---------------------------------------------------------------
    S(PART[7] - 0.15, "t_asics26", 120.0, flash=1); chapter(PART[7], "06", "THE DISAPPEARANCE")
    S(a("she ran the mile"), "t_asics26", 140.0, amb=1); stat(a("8th") - 0.1, 2.0, "8TH", "MILE · JAN 2026", "red")
    S(a("february"), "t_asics26", 230.0, amb=1); say(a("she wins a mile"), 2.0, "WIN · 4:32.39", "gold", "b", "WIN")
    S(a("that was her last win"), "t_asics26", 300.0, slow=0.5); say(a("last win"), 1.8, "HER LAST WIN", "orange", "b", "LAST")
    S(a("one week later"), "ph_armory6", 0.0, bw=1); stat(a("15th out of 16") - 0.2, 2.6, "15TH / 16", "USA INDOORS 3000M · 2026", "red")
    S(a("then in april"), "t_letsrun26", 2.0); stat(a("10th") - 0.1, 2.0, "10TH", "BOSTON 5K · APRIL 18, 2026", "red")
    S(a("after that race"), "t_letsrun26", 40.0)
    S(a("they asked her if"), "t_letsrun26", 150.0)
    S(a("and we gonna respect"), "ph_portland", 2.0, bw=1)
    S(a("but she said"), "t_letsrun26", 85.0); say(a("definitely") - 0.1, 2.0, "“DEFINITELY”", "white", "c", None, 170)
    S(a("she didnt run it"), "ph_armory2", 0.0, bw=1); stamp(a("did not run it"), 1.6, "DID NOT RUN")
    S(a("july the usa"), "t_portland25", 300.0, bw=1); say(a("her home state"), 2.0, "NEW YORK · HER HOME STATE", "white", "b", "HOME")
    stamp(a("she wasnt there"), 1.6, "NOT THERE")
    S(a("no races"), "ph_armory5", 0.0, bw=1); stack(a("not from her"), 4.0, ["NOT FROM HER", "NOT FROM HER COACH", "NOT FROM ADIDAS"], "red")
    S(a("april 18th"), "t_letsrun26", 60.0, bw=1, slow=0.5); say(a("april 18th"), 2.4, "APRIL 18, 2026", "white", "c", None, 160)
    S(a("that was the last time"), "t_letsrun26", 200.0, bw=1, punch=1.0); say(a("last time"), 2.0, "HER LAST RACE", "red", "b", "LAST")
    # 8 the comeback that wasn't --------------------------------------------------------
    S(PART[8] - 0.15, "t_sanderrace25", 62.0, flash=1); chapter(PART[8], "07", "THE COMEBACK THAT WASN'T")
    S(a("and her name was on it"), "ph_portland", 0.0); say(a("her name was on it") - 0.2, 2.2, "PRO FIELD · DASH TO THE FINISH LINE 5K", "white", "b", "FIELD")
    S(a("they said she will race"), "t_sanderrace25", 540.0); say(a("first time since april") - 0.3, 2.6, "“FOR THE FIRST TIME SINCE APRIL”", "orange", "b", "FIRST")
    S(a("october 31st"), "t_sanderrace25", 190.0, amb=1); say(a("halloween"), 1.8, "OCT 31, 2026 · CENTRAL PARK", "white", "t")
    S(a("and when the results"), "ph_armory3", 0.0, bw=1); stamp(a("top nine"), 1.8, "NOT IN THE TOP 9")
    S(a("no time"), "ph_portland", 3.0, bw=1); stack(a("no time"), 2.6, ["NO TIME", "NO EXPLANATION"], "red")
    S(a("and while she"), "t_ncaa5k22", 560.0, slow=0.6, bw=1)
    S(a("her ncaa record"), "t_ncaa5k22", 600.0, bw=1); say(a("two girls broke it"), 2.6, "NCAA 3000M RECORD · BROKEN TWICE, FEB 2026", "white", "b", "BROKEN")
    S(a("her course record"), "t_ncaaxc22", 1100.0, bw=1); say(a("broke this fall") - 0.4, 2.2, "COURSE RECORD · BROKEN SEPT 2026", "white", "b", "BROKEN")
    # 9 so what y'all think -------------------------------------------------------------
    S(PART[9] - 0.15, "t_letsrun26", 162.0, flash=1)
    S(a("shes 24"), "ph_portland", 0.0); stat(a("shes 24") + 0.2, 2.2, "24", "YEARS OLD", "orange")
    S(a("most women dont"), "t_portland25", 760.0); say(a("late 20s"), 2.0, "DISTANCE PEAK: LATE 20s", "white", "b", "LATE")
    S(a("but look at it"), "t_nxn2017", 1112.0, slow=0.5)
    S(a("three national titles"), "t_nxn2019", 242.0); stack(a("three national titles"), 7.0, ["3 NXN TITLES", "4 NCAA TITLES", "NCAA RECORDS", "12TH · 19TH · 15TH"], "gold")
    S(a("and then nothing"), "ph_armory4", 0.0, bw=1); say(a("nothing"), 1.8, "NOTHING", "red", "c", None, 180)
    S(a("so what y all think"), "t_trials24", 300.0)
    S(a("was it pressure"), "ph_armory3", 0.0); O(a("was it pressure"), 6.0, ("endq", "THE PRESSURE? THE INJURIES? GOING PRO?", "OR IS SHE COMING BACK?"))
    S(a("or is she about"), "t_ncaaxc22", 1010.0, slow=0.6)
    S(a("y all let me know") - 0.3, "t_ncaa5k22", 820.0)

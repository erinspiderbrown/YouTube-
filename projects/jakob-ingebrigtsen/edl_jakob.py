"""Jakob Ingebrigtsen: soundbites + EDL (times are cleaned-VO seconds via the phrase finder A).
Footage rules (user, 17 Nov 2026): no official Olympic footage, no NCAA/conference/World Championships broadcasts,
no FloTrack/MileSplit. Race moments come from independent photographers on Wikimedia Commons (p_* clips) and
Jakob's own channel; k_fearless 690-1180 s holds World Championships broadcast shots and is never used."""

TAGS = {
    "k_fearless": "JAKOB INGEBRIGTSEN · FEARLESS (2025)", "k_48hours": "JAKOB INGEBRIGTSEN · YOUTUBE",
    "k_dthreshold": "JAKOB INGEBRIGTSEN · YOUTUBE", "k_tracksession": "JAKOB INGEBRIGTSEN · YOUTUBE",
    "k_qa": "JAKOB INGEBRIGTSEN · YOUTUBE Q&A", "k_kristoffer": "KRISTOFFER INGEBRIGTSEN · YOUTUBE",
    "k_pov_alvarez": "ALVAREZ FILMS", "k_prodirect": "PRO:DIRECT RUNNING",
    "k_citius_cowards": "CITIUS MAG · BRUSSELS 2026", "k_citius_ultimate": "CITIUS MAG · BUDAPEST 2026",
    "k_citius_worlds23": "CITIUS MAG · BUDAPEST 2023", "k_citius_pre24": "CITIUS MAG · EUGENE 2024",
    "k_aw_euro26": "ATHLETICS WEEKLY · BIRMINGHAM 2026", "k_aw_2021": "ATHLETICS WEEKLY · 2021",
    "k_letsrun22": "LETSRUN · EUGENE 2022", "k_mh_kerr": "MARATHON HANDBOOK · 2026",
    "k_ea_u20_2017": "EUROPEAN ATHLETICS · GROSSETO 2017", "k_ea_xc2018": "EUROPEAN ATHLETICS · TILBURG 2018",
    "p_steeple1": "PHOTO: FILIP BOSSUYT · CC BY 2.0", "p_steeple2": "PHOTO: FILIP BOSSUYT · CC BY 2.0",
    "p_steeple3": "PHOTO: FILIP BOSSUYT · CC BY 2.0", "p_kerr23": "PHOTO: FILIP BOSSUYT · CC BY 2.0",
    "p_budapest5k": "PHOTO: FILIP BOSSUYT · CC BY 2.0", "p_tampere18": "PHOTO: ERIK VAN LEEUWEN · GFDL",
    "p_paris1": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0", "p_paris2": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0",
    "p_paris3": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0", "p_paris4": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0",
    "p_paris5": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0", "p_paris6": "PHOTO: DAIEUXETDAILLEURS · CC BY 4.0",
    "p_zurich1": "PHOTO: QUEJAYTEE · CC BY-SA 4.0", "p_zurich2": "PHOTO: QUEJAYTEE · CC BY-SA 4.0",
}

# cold open: Jakob in his own words (his FEARLESS film)
PRE_SB = ("k_fearless", 655.9, 665.43, "JAKOB INGEBRIGTSEN · FEARLESS (2025)")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("his name is", 1), "k_ea_xc2018", 113.3, 125.3, "JAKOB, 18 · EUROPEAN ATHLETICS · DEC 2018"),
    (("so jacob grew up", 2), "k_aw_2021", 194.1, 209.7, "JAKOB INGEBRIGTSEN · ATHLETICS WEEKLY · 2021"),
    (("then 2018 happens", 3), "k_ea_u20_2017", 82.7, 88.5, "JAKOB, 16 · EUROPEAN ATHLETICS · 2017"),
    (("and then he starts winning", 3), "k_aw_2021", 619.6, 629.9, "JAKOB INGEBRIGTSEN · ATHLETICS WEEKLY · 2021"),
    (("and jacob and josh kerr", 4), "k_citius_worlds23", 609.9, 621.2, "ON JOSH KERR'S 2023 WORLD TITLE · CITIUS MAG"),
    (("then in the 2024 paris", 4), "k_mh_kerr", 1255.3, 1271.7, "MARATHON HANDBOOK · MAY 2026"),
    (("and when hes healthy", 5), "k_citius_cowards", 41.6, 60.3, "AFTER 4TH IN BRUSSELS · CITIUS MAG · SEPT 2026"),
    (("but he seems to get", 5), "k_letsrun22", 128.1, 136.4, "LETSRUN · MAY 2022"),
    (("and then his body", 7), "k_fearless", 358.69, 372.17, "ON THE TRIAL · FEARLESS (2025)"),
    (("september 2025 world", 7), "k_fearless", 123.69, 141.25, "ON HIS ACHILLES · FEARLESS (2025)"),
    (("one month later budapest", 8), "k_aw_euro26", 373.1, 380.6, "ATHLETICS WEEKLY · BIRMINGHAM 2026"),
    (("now imma keep", 9), "k_citius_ultimate", 142.1, 151.5, "CITIUS MAG · BUDAPEST · SEPT 2026"),
    (("so what do yall think", 9), "k_qa", 279.3, 293.9, "ASKED IF HE'S THE GOAT · JAKOB'S CHANNEL"),
]


def edl(a, S, O, stat, say, stack, name, stamp, chapter, PART):
    # 1 cold open -----------------------------------------------------------------------
    S(a("august 2018"), "p_tampere18", 0.0); say(a("august 2018"), 2.6, "AUGUST 2018 · BERLIN", "white", "b", "BERLIN")
    S(a("the european championships"), "k_prodirect", 125.0)
    S(a("a 17 year old"), "p_steeple2", 0.0, punch=0.5); say(a("17 year old"), 2.0, "17 YEARS OLD", "orange", "c", "17", 160)
    S(a("from a little town"), "k_kristoffer", 62.0)
    S(a("lines up against grown"), "p_tampere18", 3.0)
    S(a("and he wins it"), "k_ea_xc2018", 12.0, punch=0.4); stat(a("wins it") + 0.1, 2.2, "GOLD", "EUROPEAN 1500M · AGE 17", "gold")
    S(a("then a few days"), "k_fearless", 1253.0)
    S(a("he wins that too"), "p_budapest5k", 0.0, punch=0.5); stat(a("wins that too") + 0.1, 2.2, "GOLD", "EUROPEAN 5000M · AGE 17", "gold")
    S(a("nobody had ever"), "k_tracksession", 494.0); stamp(a("double at the"), 1.6, "FIRST EVER")
    S(a("his name is"), "k_fearless", 53.0); name(a("jakob ingebrigtsen and"), 3.0, "JAKOB INGEBRIGTSEN", "NORWAY")
    S(a("built for this"), "k_48hours", 819.0, punch=0.3)
    S(a("but the man who"), "k_fearless", 298.5, bw=1)
    S(a("facing in court"), "k_fearless", 302.0, punch=0.2); stamp(a("in court"), 1.6, "COURT")
    S(a("let me tell"), "k_dthreshold", 677.0)
    # 2 built in Sandnes ----------------------------------------------------------------
    S(PART[2] - 0.15, "k_kristoffer", 52.0, flash=1); chapter(PART[2], "01", "BUILT IN SANDNES")
    S(a("born september"), "k_kristoffer", 67.0); say(a("born september"), 2.6, "SEPT 19, 2000 · SANDNES, NORWAY", "white", "b", "SANDNES")
    S(a("seven kids"), "k_kristoffer", 82.0); stat(a("seven kids") + 0.1, 2.2, "7", "KIDS IN THE HOUSE", "orange")
    S(a("his dad coached"), "k_fearless", 512.0, bw=1); name(a("his dad coached"), 2.6, "GJERT INGEBRIGTSEN", "HIS DAD · HIS COACH", "white")
    S(a("his big brother"), "k_kristoffer", 127.0); stat(a("1500 title in 2012"), 2.4, "2012", "HENRIK · EUROPEAN 1500M CHAMPION", "gold")
    S(a("1500 title"), "k_tracksession", 216.0)
    S(a("his other brother"), "k_kristoffer", 145.0); stat(a("won in 2016") + 0.1, 2.2, "2016", "FILIP · EUROPEAN 1500M CHAMPION", "gold")
    S(a("so jacob grew up"), "k_kristoffer", 160.0)
    S(a("literally chasing"), "k_dthreshold", 286.0, punch=0.4)
    S(a("norway put the whole"), "k_48hours", 11.0); say(a("a show called"), 2.4, "TEAM INGEBRIGTSEN · TV SERIES", "orange", "b", "TEAM INGEBRIGTSEN")
    S(a("a show called"), "k_48hours", 33.0)
    S(a("they filmed them"), "k_kristoffer", 440.0)
    S(a("may 2017"), "p_steeple1", 0.0); say(a("may 2017"), 2.6, "MAY 2017 · PREFONTAINE CLASSIC", "white", "t", "PREFONTAINE")
    S(a("in eugene oregon"), "p_steeple3", 0.0)
    S(a("is only 16"), "k_ea_u20_2017", 5.0, punch=0.3); say(a("only 16"), 1.8, "16 YEARS OLD", "orange", "c", "16", 160)
    S(a("he runs the mile"), "p_steeple2", 2.0, punch=0.6); stat(a("the mile in") + 0.3, 2.6, "3:58.07", "MILE · AGE 16", "gold")
    S(a("the youngest person"), "k_ea_u20_2017", 40.0); say(a("youngest person"), 2.6, "YOUNGEST EVER UNDER 4:00", "white", "b", "YOUNGEST")
    S(a("16 years old"), "k_ea_u20_2017", 66.0, bw=1)
    # 3 the prodigy becomes the champ ---------------------------------------------------
    S(PART[3] - 0.15, "p_tampere18", 1.0, flash=1); chapter(PART[3], "02", "THE PRODIGY BECOMES THE CHAMP")
    S(a("the berlin double"), "k_ea_xc2018", 125.0); stack(a("the berlin double"), 3.0, ["1500M · GOLD", "5000M · GOLD"], "gold")
    S(a("hes fourth at"), "k_dthreshold", 220.0); stat(a("fourth at") + 0.1, 2.4, "4TH", "2019 WORLDS 1500M · AGE 19", "white")
    S(a("at 19 years"), "k_aw_2021", 60.0)
    S(a("then august 2021"), "k_dthreshold", 253.0); say(a("august 2021"), 2.4, "AUGUST 2021 · TOKYO", "white", "b", "TOKYO")
    S(a("the 1500 meter final"), "k_fearless", 1535.0)
    S(a("is 20 years old"), "k_aw_2021", 640.0, punch=0.3); say(a("20 years old"), 1.8, "20 YEARS OLD", "orange", "c", "20", 160)
    S(a("he runs"), "k_fearless", 1288.0, punch=0.5); stat(a("he runs") + 0.4, 2.6, "3:28.32", "OLYMPIC RECORD", "gold")
    S(a("gold medal"), "k_fearless", 1300.0); stamp(a("gold medal"), 1.5, "GOLD", "gold")
    S(a("the kid that was"), "k_kristoffer", 172.0, bw=1, slow=0.6)
    S(a("now olympic champion"), "k_fearless", 1429.0); say(a("olympic champion"), 2.2, "OLYMPIC CHAMPION", "orange", "c", "CHAMPION", 150)
    S(a("and then he starts"), "p_budapest5k", 2.0); stack(a("and then he starts") + 0.4, 4.0, ["2022 · WORLD 5000M GOLD", "2023 · WORLD 5000M GOLD"], "gold")
    S(a("at every world"), "k_tracksession", 383.0)
    S(a("gold gold"), "k_citius_worlds23", 30.0)
    # 4 the rivals ----------------------------------------------------------------------
    S(PART[4] - 0.15, "p_kerr23", 0.0, flash=1); chapter(PART[4], "03", "THE RIVALS")
    S(a("in the 1500 the event"), "k_tracksession", 564.0)
    S(a("he kept getting beat"), "k_fearless", 159.0, bw=1)
    S(a("2022 world championships"), "k_letsrun22", 50.0); stat(a("outkicks him") , 2.4, "SILVER", "2022 WORLDS · JAKE WIGHTMAN WINS", "white")
    S(a("outkicks him"), "k_dthreshold", 726.0)
    S(a("2023 world championships"), "p_kerr23", 2.0, punch=0.4); name(a("josh kerr"), 2.6, "JOSH KERR", "GREAT BRITAIN · SCOTLAND")
    S(a("same thing"), "k_citius_worlds23", 100.0)
    S(a("silver again"), "k_citius_worlds23", 200.0, bw=1); say(a("silver again"), 1.8, "SILVER AGAIN", "white", "c", "AGAIN", 150)
    S(a("and jacob and josh kerr"), "p_kerr23", 4.0, punch=0.3)
    S(a("said it himself"), "k_mh_kerr", 1140.0); say(a("i wouldnt say"), 2.6, "KERR: \"I WOULDN'T SAY WE'RE BUDDIES\"", "white", "b", "BUDDIES")
    S(a("then in the 2024 paris"), "p_paris2", 0.0); say(a("2024 paris"), 2.6, "PARIS 2024 · 1500M FINAL", "white", "b", "1500M FINAL")
    S(a("the 1500m final"), "p_paris3", 0.0)
    S(a("takes it out from"), "p_paris4", 0.0)
    S(a("and he gets passed"), "p_paris5", 0.0, punch=0.5)
    S(a("win gold"), "p_paris6", 0.0); stack(a("win gold") - 0.3, 4.6, ["GOLD · COLE HOCKER", "SILVER · JOSH KERR", "BRONZE · YARED NUGUSE"], "gold")
    S(a("gets fourth"), "p_paris1", 0.0, bw=1); stamp(a("gets fourth"), 1.6, "4TH")
    S(a("he said i ruined"), "k_fearless", 406.0, bw=1); say(a("i ruined"), 2.4, "\"I RUINED THE RACE FOR MYSELF\"", "white", "b", "RUINED")
    S(a("a few days later"), "k_fearless", 1500.0); stat(a("olympic gold again"), 2.4, "GOLD", "PARIS 2024 · 5000M", "gold")
    S(a("olympic gold again"), "k_fearless", 1535.0, slow=0.7)
    # 5 the records ---------------------------------------------------------------------
    S(PART[5] - 0.15, "k_tracksession", 425.0, flash=1); chapter(PART[5], "04", "THE RECORDS")
    S(a("3000 meters") - 0.4, "k_tracksession", 494.0, punch=0.8); stat(a("world record") - 0.2, 2.4, "7:17.55", "3000M · WORLD RECORD", "gold")
    S(a("2000 meters") - 0.4, "k_dthreshold", 645.0, punch=0.8); stat(a("world record") - 0.2, 2.4, "4:43.13", "2000M · WORLD RECORD", "gold")
    S(a("february 2025"), "k_tracksession", 327.0); say(a("february 2025"), 2.2, "FEB 2025 · LIEVIN, FRANCE", "white", "t", "LIEVIN")
    S(a("the mile"), "k_tracksession", 564.0, punch=0.6); stat(a("world record") - 0.2, 2.4, "3:45.14", "INDOOR MILE · WORLD RECORD", "gold")
    S(a("and the 1500 inside"), "k_48hours", 819.0, punch=0.8); stat(a("another world record") - 0.2, 2.6, "3:29.63", "INDOOR 1500M · WORLD RECORD", "gold")
    S(a("another world record") + 0.3, "k_tracksession", 578.0)
    S(a("but he seems to get"), "k_fearless", 1324.0)
    S(a("and non"), "k_dthreshold", 759.0)
    # 6 the family war ------------------------------------------------------------------
    S(PART[6] - 0.15, "k_fearless", 287.0, flash=1, bw=1); chapter(PART[6], "05", "THE FAMILY WAR")
    S(a("something was breaking"), "k_fearless", 512.0, bw=1)
    S(a("in 2022"), "k_48hours", 1037.0); say(a("in 2022"), 2.0, "2022", "white", "t")
    S(a("stopped being coached"), "k_fearless", 547.0, bw=1)
    S(a("jakob started coaching"), "k_dthreshold", 726.0); say(a("coaching himself"), 2.0, "COACHING HIMSELF", "orange", "b", "HIMSELF")
    S(a("then october 2023"), "k_fearless", 88.0); say(a("october 2023"), 2.6, "OCTOBER 2023 · VG NEWSPAPER", "white", "t", "VG")
    S(a("goes public"), "k_fearless", 287.0, bw=1)
    S(a("we have grown up"), "k_dthreshold", 41.0, bw=1); say(a("very aggressive"), 2.6, "\"VERY AGGRESSIVE AND CONTROLLING\"", "white", "c", "AGGRESSIVE", 110)
    S(a("physical violence"), "k_dthreshold", 612.0, bw=1)
    say(a("physical violence"), 2.8, "\"PHYSICAL VIOLENCE AND THREATS\"", "red", "c", "VIOLENCE", 110)
    S(a("their dad denied"), "k_kristoffer", 291.0, bw=1); stamp(a("denied it"), 1.4, "DENIED", "white")
    S(a("his lawyer said"), "k_fearless", 1359.0, bw=1); say(a("i have never"), 2.8, "\"I HAVE NEVER USED VIOLENCE AGAINST MY CHILDREN\"", "white", "b", "NEVER", 100)
    S(a("not everybody in"), "k_fearless", 1465.0, bw=1)
    S(a("another brother martin"), "k_fearless", 1218.0, bw=1); name(a("another brother martin"), 2.6, "MARTIN INGEBRIGTSEN", "BACKED HIS DAD", "white")
    S(a("2024 police"), "k_fearless", 298.5); stamp(a("charged the dad"), 1.4, "CHARGED")
    S(a("march 2025 the trial"), "k_fearless", 302.0, punch=0.4); stack(a("six weeks"), 3.0, ["6 WEEKS", "40+ WITNESSES"], "white")
    S(a("over 40 witnesses"), "k_fearless", 321.0, bw=1)
    S(a("jakob testifies"), "k_fearless", 335.0, punch=0.4); say(a("jakob testifies"), 2.6, "TESTIFIES AGAINST HIS FATHER", "white", "b", "FATHER")
    S(a("june 16th"), "k_fearless", 319.0); say(a("the verdict"), 2.0, "JUNE 16, 2025 · THE VERDICT", "white", "t", "VERDICT")
    S(a("the dad is cleared"), "k_fearless", 304.0, bw=1); say(a("cleared on all"), 2.6, "CLEARED · ALL CHARGES INVOLVING JAKOB", "white", "b", "CLEARED")
    S(a("involving jacob"), "k_fearless", 323.0, bw=1)
    S(a("reasonable doubt"), "k_fearless", 1394.0, bw=1)
    S(a("but hes convicted"), "k_fearless", 1429.0, bw=1); say(a("his daughter"), 2.4, "GUILTY · ASSAULTING HIS DAUGHTER INGRID", "red", "b", "GUILTY")
    S(a("a 15 day"), "k_fearless", 1359.0, bw=1); stat(a("a 15 day") + 0.1, 2.6, "15 DAYS", "SUSPENDED SENTENCE · NO JAIL", "red")
    S(a("so jacob testified"), "k_fearless", 371.0, bw=1)
    S(a("in court and his"), "k_fearless", 306.0, bw=1)
    # 7 the body breaks -----------------------------------------------------------------
    S(PART[7] - 0.15, "k_fearless", 229.0, flash=1); chapter(PART[7], "06", "THE BODY BREAKS")
    S(a("march 2025 he wins"), "k_tracksession", 146.0); stack(a("he wins the"), 3.4, ["WORLD INDOORS 2025", "1500M · GOLD", "3000M · GOLD"], "gold")
    S(a("and the 3000"), "k_tracksession", 383.0)
    S(a("achilles goes"), "k_fearless", 231.0, punch=0.3); stamp(a("achilles goes"), 1.5, "ACHILLES")
    S(a("misses the whole"), "k_fearless", 441.0, bw=1)
    S(a("september 2025 world"), "k_fearless", 441.0, bw=1); say(a("in tokyo"), 2.2, "TOKYO 2025", "white", "t")
    S(a("he doesnt even make"), "k_fearless", 653.0, bw=1); stat(a("of the heats"), 2.2, "OUT", "1500M · FIRST ROUND", "red")
    S(a("10th in the 5k"), "k_fearless", 688.0, bw=1); stat(a("10th in the 5k"), 2.0, "10TH", "5000M FINAL", "red")
    S(a("february 2026 achilles"), "k_dthreshold", 579.0, bw=1); stamp(a("achilles surgery"), 1.6, "SURGERY")
    S(a("achilles surgery") + 0.2, "k_fearless", 229.0, punch=0.4)
    # 8 the comeback --------------------------------------------------------------------
    S(PART[8] - 0.15, "k_dthreshold", 253.0, flash=1); chapter(PART[8], "07", "THE COMEBACK")
    S(a("seen the best"), "k_fearless", 1182.0, bw=1)
    S(a("august 10th 2026"), "k_aw_euro26", 20.0); say(a("august 10th"), 2.6, "AUG 10, 2026 · BIRMINGHAM", "white", "t", "BIRMINGHAM")
    S(a("his first race in"), "k_dthreshold", 302.0); stat(a("first race in") + 0.2, 2.4, "11", "MONTHS WITHOUT A RACE", "orange")
    S(a("he wins the"), "k_aw_euro26", 100.0, punch=0.4); stat(a("he wins the") + 0.3, 2.6, "GOLD", "EUROPEAN 5000M · 13:15.29", "gold")
    S(a("one month later budapest"), "k_citius_ultimate", 20.0); say(a("budapest"), 2.6, "BUDAPEST · ULTIMATE CHAMPIONSHIP", "white", "t", "ULTIMATE")
    S(a("the 5"), "p_zurich2", 0.0)
    S(a("cole hawker"), "p_zurich1", 0.0); stack(a("cole hawker"), 4.0, ["COLE HOCKER", "PARKER WOLFE", "GRANT FISHER", "NICO YOUNG"], "white")
    S(a("the whole american"), "p_zurich2", 3.0, punch=0.4)
    S(a("jakob outkicks"), "k_pov_alvarez", 0.0, punch=0.5)
    S(a("and runs"), "k_citius_ultimate", 140.0, punch=0.4); stat(a("and runs") + 0.4, 2.6, "12:59.24", "ULTIMATE CHAMPION · 5000M", "gold")
    S(a("and wins"), "k_dthreshold", 302.0); stat(a("and wins") + 0.3, 2.4, "$150,000", "PRIZE MONEY", "gold")
    # 9 so what y'all think -------------------------------------------------------------
    S(PART[9] - 0.15, "k_fearless", 1606.0, flash=1)
    S(a("this man broke"), "p_steeple2", 1.0); stack(a("this man broke"), 6.0, ["SUB-4 MILE · AGE 16", "OLYMPIC GOLD · AGE 20", "COURT VS HIS DAD · AGE 24"], "orange")
    S(a("won olympic gold"), "k_fearless", 1288.0)
    S(a("and went against"), "k_fearless", 300.0, bw=1)
    S(a("but right now"), "k_citius_ultimate", 300.0)
    S(a("so what do yall"), "k_fearless", 1641.0); say(a("the greatest distance"), 2.8, "GREATEST OF HIS GENERATION?", "white", "c", "GREATEST", 130)
    S(a("of his generation"), "k_tracksession", 7.0)
    S(a("did his dad make"), "k_fearless", 304.0, bw=1); say(a("did his dad make"), 3.2, "MADE BY HIS DAD... OR IN SPITE OF HIM?", "orange", "c", "SPITE", 110)
    S(a("in spite of"), "k_fearless", 1394.0, bw=1)
    S(a("let me know"), "k_dthreshold", 775.0)

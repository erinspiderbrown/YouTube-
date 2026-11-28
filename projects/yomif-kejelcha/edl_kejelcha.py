"""Yomif Kejelcha "11 Seconds" (27 Nov 2026): soundbites + EDL. Cloned voice (A3b + dialect opener), own score K1-K6.
PREMIUM layer (tools/premium.py): every interview gets an ID (iname) + word-synced subtitles (subs); race clock, gap,
timeline and wipe headlines replace the old stat slams; cinematic transitions (whip/blur/leak/push) on chosen cuts.
Footage rules: no NBC/Peacock, BBC, Olympic, World Athletics broadcast, Diamond League, FloTrack/MileSplit, RunnerSpace.
London race = real fan phone clips first (fan_reya/nico/summit/cutty/gj); the host feed only in seconds if at all.
cit_tokyo has a World Championships logo wall -> audio only over other B-roll (logo-wall rule)."""

TAGS = {
    "fan_reya": "London Marathon 2026 · fan video", "fan_nico": "London Marathon 2026 · fan video",
    "fan_summit": "London Marathon 2026 · fan video", "fan_cutty": "London Marathon 2026 · fan video",
    "fan_gj": "London Marathon 2026 · fan video", "co_finish": "London Marathon 2026 · fan video",
    "fan_noxxid": "London Marathon 2026 · fan video", "alv_fastest": "London 2026 · Alvarez Films",
    "alv_sub2": "London 2026 · Alvarez Films", "alv_sawe": "London 2026 · Alvarez Films",
    "let_disbelief": "LetsRun.com", "cit_post": "CITIUS MAG", "cit_pre": "CITIUS MAG", "aw_fav": "Athletics Weekly",
    "mh_prerace": "Marathon Handbook", "let_sawe": "LetsRun.com", "itv_sawe": "ITV News", "livenow_gault": "LiveNOW from FOX",
    "fan_doha1": "Doha 2019 · fan video from the stands", "fan_doha2": "Doha 2019 · fan video from the stands",
    "fan_doha3": "Doha 2019 · fan video from the stands", "fan_boston1": "Boston 2019 · fan video",
    "fan_boston2": "Boston 2019 · fan video", "let_mile_wr": "LetsRun.com", "let_millrose": "LetsRun.com",
    "alv_valencia1": "Valencia Half 2024 · Alvarez Films", "alv_valencia2": "Valencia Half 2024 · Alvarez Films",
    "ba_tribuna": "Buenos Aires 2026 · La Tribuna Del Running", "santamadre": "SANTAMADRE · 56:51",
    "alv_ba_start": "Buenos Aires 2026 · Alvarez Films", "adidas_sub2": "adidas · History in Time",
    "ph_mill_close": "Photo: jenaragon94 · CC BY 2.0", "ph_mill_tape": "Photo: jenaragon94 · CC BY 2.0",
    "ph_mill_trophy": "Photo: jenaragon94 · CC BY 2.0", "ph_mill_run": "Photo: jenaragon94 · CC BY 2.0",
    "ph_mill_run2": "Photo: jenaragon94 · CC BY 2.0", "ph_mill_close2": "Photo: jenaragon94 · CC BY 2.0",
    "ph_payton": "Photo: jenaragon94 · CC BY 2.0", "ph_london2017": "London 2017 · Photo: Samuel Blanck · CC0",
    "ph_tokyo_pf": "Tokyo 2025 photo finish · JME91800 · CC BY-SA 4.0",
    "corredor": "CORREDOR", "podium": "Podium Athletics", "alv_training": "Alvarez Films", "fan_mall": "London Marathon 2026",
}

# vertical phone clips -> full-frame 16:9 crops (no blurred side bars), clear of burned captions
C_REYA = "crop=iw:iw*9/16:0:ih*0.30"; C_NICO = "crop=iw:iw*9/16:0:ih*0.36"; C_SUMMIT = "crop=iw:iw*9/16:0:ih*0.33"
C_CUTTY = "crop=iw:iw*9/16:0:ih*0.38"; C_GJ = "crop=iw:iw*9/16:0:ih*0.16"

KJ = ("Yomif Kejelcha", "1:59:41 · 2nd · marathon debut")
# cold open: two days before London he says 1:59 is "not possible" (audio over him running it)
PRE_SB = ("mh_prerace", 3.56, 10.78, "Yomif Kejelcha, two days before London · Marathon Handbook",
          dict(vsrc="fan_reya", vss=6.0, crop=C_REYA, subs=1, name=("Yomif Kejelcha", "Two days before London", "Marathon Handbook")))
R = {"raw": 1}
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("yall i aint", 1), "livenow_gault", 213.70, 225.04, "Jonathan Gault, LetsRun · via LiveNOW from FOX",
     dict(vsrc="co_finish", vss=0.0, subs=1, name=("Jonathan Gault", "LetsRun.com", "Audio · LiveNOW from FOX"), tr="whip",
          subfix=[("second man of the two hours", "second man under two hours")])),
    (("yomif was born", 2), "cit_post", 20.98, 23.96, "Yomif Kejelcha · CITIUS MAG", dict(subs=1, name=KJ)),
    (("yomif was born", 2), "let_disbelief", 14.38, 34.68, "Yomif Kejelcha · LetsRun.com", dict(subs=1, tr="none")),
    # childhood: ran 3 km to school every day (audio; the podcast video has burned Spanish subtitles)
    (("but outdoors on the big", 3), "corredor", 1819.52, 1845.36, "Yomif Kejelcha · CORREDOR podcast",
     dict(vsrc="alv_training", vss=200.0, subs=1, name=("Yomif Kejelcha", "On growing up in Ethiopia", "CORREDOR podcast"),
          subfix=[("I'm going to run", "I'm gonna run"), ("anyone is going to beat me", "nobody gonna beat me")])),
    # Millrose 2019: through his interpreter
    (("now he did come back", 3), "let_millrose", 160.44, 166.88, "Millrose Games 2019 · LetsRun.com",
     dict(subs=1, name=("Yomif Kejelcha", "3:48.46 · 0.01 off the world record", "Via interpreter · LetsRun"))),
    # Tokyo 2025: World Champs logo wall behind him -> audio over the real photo finish
    (("so he moved to the roads", 6), "cit_tokyo", 82.72, 91.08, "Yomif Kejelcha after Tokyo 2025 · CITIUS MAG",
     dict(vsrc="ph_tokyo_pf", vss=0.0, subs=1, name=("Yomif Kejelcha", "Silver · 0.06 behind", "Audio · CITIUS MAG"))),
    # London setup: Sawe's coach, then Kejelcha's own plan
    (("the race went out fast", 7), "adidas_sub2", 538.04, 551.02, "Claudio Berardelli · adidas",
     dict(subs=1, name=("Claudio Berardelli", "Sabastian Sawe's coach", "adidas · History in Time"))),
    (("the race went out fast", 7), "cit_pre", 148.95, 165.49, "Yomif Kejelcha, two days out · CITIUS MAG",
     dict(subs=1, name=("Yomif Kejelcha", "Two days before London", "CITIUS MAG"))),
    # 38 km: both men realise it's on
    (("according to his nutrition", 7), "cit_post", 28.54, 47.82, "Yomif Kejelcha · CITIUS MAG", dict(subs=1, name=KJ)),
    (("according to his nutrition", 7), "itv_sawe", 204.35, 226.21, "Sabastian Sawe · ITV News",
     dict(subs=1, name=("Sabastian Sawe", "1:59:30 · world record", "ITV News"), subfix=[("Sowe", "Sawe")])),
    # 41 km
    (("and right after the line", 8), "cit_post", 72.06, 90.72, "Yomif Kejelcha · CITIUS MAG",
     dict(subs=1, subfix=[("my neck is stuck", "my leg is stuck"), ("my neck is done", "my leg is done")])),
    (("now think about this", 9), "let_sawe", 12.30, 32.82, "Sabastian Sawe · LetsRun.com",
     dict(subs=1, name=("Sabastian Sawe", "Winner · 1:59:30", "LetsRun.com"))),
    # when his manager told him the time (vertical video call -> audio over him)
    (("and 4 months later", 9), "podium", 30.00, 39.20, "Yomif Kejelcha · Podium Athletics",
     dict(vsrc="aw_fav", vss=4.0, subs=1, name=("Yomif Kejelcha", "On seeing the time", "Audio · Podium Athletics"),
          subfix=[("run at under 12.", "run under two"), ("under 12.", "under two")])),
    (("but the rematch", 10), "let_disbelief", 137.36, 145.04, "Yomif Kejelcha on Haile Gebrselassie · LetsRun.com",
     dict(subs=1, name=("Yomif Kejelcha", "On Haile Gebrselassie", "LetsRun.com"))),
    # 1:58 or Olympic gold in LA?
    (("and honestly i really feel", 10), "corredor", 1089.24, 1100.90, "Yomif Kejelcha · CORREDOR podcast",
     dict(vsrc="santamadre", vss=842.0, subs=1, name=("Yomif Kejelcha", "1:58 or Olympic gold?", "Audio · CORREDOR podcast"),
          subfix=[("158", "1:58")])),
    (("so i want to hear", 11), "cit_post", 147.12, 151.08, "Yomif Kejelcha · CITIUS MAG", dict(subs=1)),
]
SPLIT_AT = {}

LD = "let_disbelief"; CP = "cit_post"


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 open ----------------------------------------------------------------------------------------
    S(PART[1] - 0.05, LD, 54.0)
    title(PART[1] + 0.4, 3.6, "London Marathon · April 26, 2026", "Yomif Kejelcha")
    S(a("yomif kejelcha ran"), "fan_reya", 6.5, crop=C_REYA, slow=0.5, tr="whip")
    O(a("yomif kejelcha ran") + 0.2, 4.4, ("clock", 7128, "Whitehall · km 41"))
    S(a("under 2 hours"), "fan_gj", 5.6, crop=C_GJ, slow=0.6, tr="blur")
    S(a("in his first marathon"), CP, 30.0)
    S(a("only one man in history"), "fan_nico", 6.8, crop=C_NICO, slow=0.6, tr="whip")
    S(a("and that man beat him"), "fan_summit", 9.4, crop=C_SUMMIT, slow=0.45, blur=1)
    O(a("and that man beat him"), 6.2, ("gap", "Sabastian Sawe", 7170, "Yomif Kejelcha", 7181, "11 seconds", "London Marathon · April 26, 2026"))
    S(a("and here go the thing"), LD, 83.0, tr="blur")
    S(a("this man been losing"), "fan_doha3", 126.0, slow=0.7, bw=1, tr="push")
    t = a("this man been losing", end=True)
    S(t + 0.4, "fan_boston2", 150.0, bw=1, slow=0.6, tr="blur")
    O(t + 0.5, 4.6, ("wipe", ["0.01", "0.06", "11 seconds"], "Lost by"))
    S(a("so ima break down"), "aw_fav", 2.0, tr="blur")
    S(a("came from a dude"), "fan_reya", 0.5, crop=C_REYA, slow=0.6)
    # 2 Showa ---------------------------------------------------------------------------------------
    S(PART[2] - 0.05, "alv_training", 22.0, tr="leak"); chapter(PART[2] + 0.2, "01", "Showa, Ethiopia")
    O(a("yomif was born") + 0.4, 3.2, ("date", "August 1, 1997", "Showa · Oromia, Ethiopia"))
    S(a("and the story goes"), "alv_training", 112.0, slow=0.7)
    S(a("his daddy put him"), "santamadre", 844.0, bw=1)
    S(a("he went and joined"), "alv_training", 248.0)
    S(a("by 16 he was"), "alv_training", 203.0, slow=0.6, tr="whip")
    O(a("by 16 he was") + 0.3, 3.4, ("title", "World Youth Champion · 3000m", "Age 16"))
    S(a("at 17 he won"), "alv_training", 293.0)
    S(a("and at 18 he was"), "ph_mill_run2", 0.0, tr="blur")
    O(a("and at 18 he was") + 0.3, 3.4, ("title", "World Indoor Champion · 3000m", "2016 · 2018"))
    S(a("so this kid was a winner"), "ph_mill_trophy", 0.0)
    # 3 Millrose -------------------------------------------------------------------------------------
    S(a("but outdoors on the big"), "ph_london2017", 0.0, tr="leak"); chapter(a("but outdoors on the big") + 0.7, "02", "Hundredths")
    O(a("fourth at worlds") + 0.2, 4.2, ("title", "World Championships · 5000m", "4th · 2015   4th · 2017"))
    S(a("then in 2019 at"), "ph_mill_run", 0.0, tr="whip")
    O(a("then in 2019 at") + 0.3, 3.0, ("date", "February 9, 2019", "Millrose Games · New York"))
    S(a("record from 1997"), "ph_mill_close", 0.0)
    S(a("he ran 348"), "ph_mill_tape", 0.0, bw=1)
    O(a("he ran 348") + 0.2, 5.6, ("gap", "El Guerrouj, 1997", 228.45, "Kejelcha, 2019", 228.46, "0.01 seconds", "Indoor mile world record"))
    S(a("now he did come back"), "fan_boston2", 205.0, slow=0.6, tr="blur")
    O(a("now he did come back") + 1.4, 3.6, ("title", "Boston · March 3, 2019", "3:47.01 · World Record"))
    S(a("but remember that number"), "ph_mill_close2", 0.0, bw=1)
    # 4 Doha + 2023 + Paris ------------------------------------------------------------------------
    S(PART[4] - 0.05, "fan_doha1", 60.0, tr="push")
    O(PART[4] + 0.3, 3.0, ("date", "October 6, 2019", "World Championships · Doha"))
    S(a("he went on the bell"), "fan_doha3", 120.0, slow=0.8)
    S(a("and ran wide the whole"), "fan_doha3", 126.0, slow=0.55)
    S(a("cheptegei ran him down"), "fan_doha1", 236.0, slow=0.7)
    O(a("cheptegei ran him down") + 1.0, 5.0, ("gap", "Joshua Cheptegei", 1608.36, "Yomif Kejelcha", 1609.34, "0.98 seconds", "Doha 2019 · 10,000m"))
    S(a("in 2023 it got crazy"), "ph_payton", 0.0, bw=1, tr="blur")
    O(a("in 2023 it got crazy") + 0.2, 8.0, ("timeline", "Decided by hundredths", [(2019, "Millrose mile", "+0.01", "vs world record"), (2023, "Florence 5000m", "+0.03", "Mohamed Katir"), (2023, "Pre Classic 3000m", "+0.01", "Jakob Ingebrigtsen")]))
    S(a("then at the paris olympics"), "fan_doha2", 300.0, bw=1, tr="push")
    O(a("then at the paris olympics") + 0.3, 4.0, ("title", "Paris 2024 · 10,000m", "6th · 0.88 from gold"))
    # 5 Tokyo ----------------------------------------------------------------------------------------
    S(PART[5] - 0.05, "ph_tokyo_pf", 0.0, tr="leak"); chapter(PART[5] + 0.2, "03", "Six Hundredths")
    O(a("he leading at the bell") + 0.2, 4.0, ("clock", 1715, "Tokyo 2025 · 10,000m final lap"))
    S(a("he leading at the bell"), "fan_doha3", 177.0, bw=1)
    S(a("and in the last few meters"), "ph_tokyo_pf", 2.0, tr="whip")
    O(a("28") + 0.6, 5.4, ("gap", "Jimmy Gressier", 1735.77, "Yomif Kejelcha", 1735.83, "0.06 seconds", "Tokyo 2025 · 10,000m"))
    S(a("and after he said"), "cit_pre", 60.0, bw=1)
    # 6 the roads ------------------------------------------------------------------------------------
    S(a("so he moved to the roads"), "alv_valencia1", 0.0, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.5, tr="leak")
    chapter(a("so he moved to the roads") + 0.2, "04", "The Roads")
    S(a("in valencia in 2024"), "alv_valencia2", 0.0, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.5)
    O(a("in valencia in 2024") + 0.8, 3.6, ("title", "Valencia Half Marathon · 2024", "57:30 · World Record"))
    S(a("so now people starting"), "cit_pre", 20.0)
    S(a("even he wasnt sure"), "cit_pre", 100.0)
    S(a("his coaches believed"), "alv_training", 383.0)
    S(a("and for his debut"), "fan_noxxid", 0.5, tr="whip")
    O(a("and for his debut") + 0.8, 3.2, ("date", "April 26, 2026", "London Marathon"))
    S(a("against the best marathoner"), "adidas_sub2", 539.0)
    S(a("from kenya who"), "fan_summit", 9.4, crop=C_SUMMIT, slow=0.5)
    # 7 London ---------------------------------------------------------------------------------------
    S(PART[7] - 0.05, "fan_cutty", 2.4, crop=C_CUTTY, slow=0.4, tr="leak"); chapter(PART[7] + 0.2, "05", "London")
    O(a("halfway in 1 hour") + 0.2, 3.6, ("title", "Halfway", "1:00:29"))
    S(a("at 30k they was"), "alv_sawe", 0.0, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.6)
    S(a("then from 30 to 35"), "alv_fastest", 0.0, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.5, tr="whip")
    O(a("then from 30 to 35") + 0.3, 4.4, ("title", "30 → 35 km", "13:54"))
    S(a("under 2 hours was really"), "alv_sawe", 3.0, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.5)
    S(a("from 35 to 40"), "alv_sub2", 2.4, crop="crop=iw:iw*9/16:0:ih*0.36", slow=0.45)
    O(a("from 35 to 40") + 0.3, 4.0, ("title", "35 → 40 km", "13:42"))
    S(a("and kajolcha side by side"), "fan_cutty", 3.2, crop=C_CUTTY, slow=0.35)
    S(a("according to his nutrition"), "cit_post", 160.0)
    S(a("one slipped at"), "fan_cutty", 2.6, crop=C_CUTTY, slow=0.3, bw=1)
    # 8 the finish -----------------------------------------------------------------------------------
    S(PART[8] - 0.05, "fan_nico", 6.8, crop=C_NICO, slow=0.5, tr="whip")
    O(PART[8] + 0.3, 4.2, ("clock", 7080, "Westminster · km 41"))
    S(a("and yamif legs was done"), "fan_reya", 8.0, crop=C_REYA, slow=0.45, bw=1)
    S(a("sawe ran that last"), "fan_summit", 9.6, crop=C_SUMMIT, slow=0.5)
    S(a("crossed the line"), "co_finish", 2.0, tr="blur")
    S(a("and 11 seconds later"), "fan_reya", 11.0, crop=C_REYA, slow=0.4)
    O(a("and 11 seconds later") + 0.4, 6.0, ("gap", "Sabastian Sawe", 7170, "Yomif Kejelcha", 7181, "11 seconds", "London Marathon · April 26, 2026"))
    S(a("jacob kiplimo came"), "fan_noxxid", 21.0, slow=0.7)
    S(a("all 3 of them"), "fan_noxxid", 0.5)
    S(a("and right after the line"), "let_disbelief", 100.0, tr="blur")
    S(a("he didnt even know"), "let_disbelief", 120.0, slow=0.8)
    # 9 the reaction ---------------------------------------------------------------------------------
    S(PART[9] - 0.05, "let_disbelief", 52.0, tr="leak"); chapter(PART[9] + 0.2, "06", "Second Place")
    O(a("that's the fastest debut") + 0.2, 6.6, ("wipe", ["Fastest debut ever", "2nd fastest ever", "Ethiopian record"], "1:59:41"))
    S(a("and he went home"), "cit_post", 210.0, bw=1)
    S(a("most people would"), "aw_fav", 8.0)
    S(a("he said its a competition"), "cit_post", 120.0)
    S(a("he said now i believe"), "let_disbelief", 150.0, slow=0.8)
    S(a("and 4 months later"), "ba_tribuna", 0.0, crop="crop=iw:iw*9/16:0:ih*0.3", slow=0.5, tr="whip")
    O(a("in buenos aires") + 0.6, 3.8, ("title", "Buenos Aires · August 23, 2026", "56:51 · World Record"))
    S(a("took the world record"), "ba_tribuna", 11.0, crop="crop=iw:iw*9/16:0:ih*0.3", slow=0.6)
    # 10 the rematch ---------------------------------------------------------------------------------
    S(PART[10] - 0.05, "santamadre", 605.0, tr="leak"); chapter(PART[10] + 0.2, "07", "The Rematch")
    S(a("he was supposed to run valencia"), "alv_valencia1", 0.0, crop="crop=iw:iw*9/16:0:ih*0.36", bw=1, slow=0.7)
    S(a("so right now"), "santamadre", 1085.0, slow=0.7)
    S(a("with his eyes on 158"), "santamadre", 1248.0)
    O(a("with his eyes on 158") + 0.2, 3.4, ("title", "Next target", "1:58"))
    S(a("cause on paper"), "fan_doha3", 128.0, bw=1, slow=0.6)
    O(a("but this man ran with") + 0.1, 8.5, ("timeline", "Beaten by", [(2019, "Cheptegei", "2nd", "0.98 s"), (2023, "Ingebrigtsen", "2nd", "0.01 s"), (2025, "Gressier", "2nd", "0.06 s"), (2026, "Sawe", "2nd", "11 s")]))
    # 11 question ------------------------------------------------------------------------------------
    S(PART[11] - 0.05, "let_disbelief", 30.0, tr="blur")
    O(a("is yomif kejelche") + 0.1, 4.4, ("wipe", ["Choke artist?", "Or born in the wrong era?"], ""))
    S(a("and when him and sawe"), "fan_nico", 7.0, crop=C_NICO, slow=0.5, tr="whip")
    S(a("let me know"), "let_disbelief", 54.0)

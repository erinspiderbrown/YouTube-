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
    # 2 (test tail) ---------------------------------------------------------------------------------
    S(PART[2] - 0.05, "fan_doha3", 20.0)

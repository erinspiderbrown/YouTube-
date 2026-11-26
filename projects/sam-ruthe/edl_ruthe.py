"""Sam Ruthe (26 Nov 2026): soundbites + EDL. Rise -> Boston 3:48.88 -> the lesson vs Hocker -> stress fracture -> the decision -> comeback question.
Voice: Erin Brown 2026 clone, approved A3b style. Footage: Athletics NZ race uploads (their own streams), John Hedengren's fan video
from the stands at the BU Terrier Classic (race + mixed zone), Sam Ruthe's own "Back on Track" series, LetsRun, NZ Herald, Stuff,
Washington Post, the Ruthe family channel, a fan clip from the ASICS Sound Invite. No FloTrack/FloSports, RunnerSpace, NBC/Peacock,
Diamond League, World Athletics or Olympic video. Stuff's North Carolina race pictures are a broadcast feed: their Sam quotes play
audio-only over other B-roll. Avoid: nz353 > 240 s and nz800 > 140 s (TVNZ+ end card), bot1 0-14 s / 286-296 s (title, colour bars),
bot2 0-12 s / 300 s+ and bot4 0-12 s / 302 s+ (titles, Nike end card), bot3 0-18 s (title)."""

TAGS = {
    "sub4": "ACA Mile Night 2025 · Athletics New Zealand", "nztie": "NZ Championships 2025 · Athletics New Zealand",
    "nz338": "NZ Secondary Schools 2025 · Athletics New Zealand", "nz800": "Potts Classic 2026 · Athletics New Zealand",
    "nz353": "Cooks Classic 2026 · Athletics New Zealand", "bu_fan": "BU Terrier Classic 2026 · fan video · John Hedengren",
    "bot1": "Back on Track · Sam Ruthe", "bot2": "Back on Track · Sam Ruthe", "bot3": "Back on Track · Sam Ruthe",
    "bot4": "Back on Track · Sam Ruthe", "lr_ben": "LetsRun · Boston 2026", "lr_sam": "LetsRun · Boston 2026",
    "herald": "NZ Herald · February 2026", "wapo": "The Washington Post · March 2025", "stuff": "Stuff · February 2026",
    "fam_nats": "Ruthe family channel · Dec 2025", "fan_sound": "ASICS Sound Invite 2026 · fan video · Stuart Terrill",
}

R = {"raw": 1}
# cold open: the sub-4 at 15, the commentator's call ("Here they come... That's a sub four, baby. That's a sub four.")
PRE_SB = ("sub4", 246.30, 265.40, "Commentary · ACA Mile Night · March 19, 2025")
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("so i want to go through", 1), "lr_ben", 104.60, 111.40, "Ben Ruthe, Sam's dad · LetsRun · Boston", R),
    (("but i really respect this part", 2), "bu_fan", 511.92, 525.50, "Sam Ruthe on his dad · fan video · Boston"),
    (("when he finally did start", 3), "bu_fan", 649.66, 661.18, "Ben Ruthe · fan video · Boston"),
    (("both", 3), "nztie", 218.40, 238.10, "Commentary · NZ 1500m final · March 2025", R),
    (("that made him the youngest", 3), "wapo", 49.80, 63.50, "Sam Ruthe, 15, after the sub-4 · Washington Post"),
    (("then in january", 4), "fam_nats", 61.54, 78.72, "Sam Ruthe after his 3:38.62 · Dec 2025"),
    (("and a week before boston", 4), "nz800", 112.0, 128.5, "Commentary · Potts Classic 800m · Jan 2026"),
    (("the plan was to sit", 5), "lr_sam", 54.74, 66.68, "Sam Ruthe, 16 · LetsRun · Boston"),
    (("so now this", 5), "bu_fan", 305.14, 322.40, "Sam Tanner, 2-time Olympian · fan video · Boston"),
    (("thats a world under", 5), "bu_fan", 438.72, 457.14, "Sam Ruthe after 3:48.88 · fan video · Boston"),
    (("two weeks later", 6), "herald", 12.60, 22.30, "NZ Prime Minister Christopher Luxon · NZ Herald", R),
    (("some people online said", 6), "stuff", 44.90, 58.00, "Sam Ruthe after racing Cole Hocker · Stuff",
     dict(raw=1, vsrc="fan_sound", vss=30.0, quote="I thought I could just glide in behind Cole Hocker... I had to fight to where I wanted to end up.", who="Sam Ruthe, 16")),
    (("then he went back to boston", 6), "stuff", 106.00, 116.10, "Sam Ruthe · Stuff · February 2026",
     dict(raw=1, vsrc="bu_fan", vss=200.0, quote="I got so much learning experience from the race tactics.", who="Sam Ruthe, 16")),
    (("and then in april", 7), "stuff", 85.10, 93.00, "Sam Ruthe on Glasgow · Stuff · February 2026",
     dict(raw=1, vsrc="bot4", vss=150.0, quote="By the time the Commonwealth Games comes around, I should be in 3:48 or better form.", who="Sam Ruthe, February 2026")),
    (("just like that", 7), "bot1", 242.21, 262.95, "Sam Ruthe · Back on Track, Ep. 1"),
    (("in may he pulled", 8), "bot2", 62.23, 79.55, "Sam Ruthe · Back on Track, Ep. 2"),
    (("his coach said", 8), "bot3", 116.48, 126.12, "Sam Ruthe · Back on Track"),
    (("and look i covered", 9), "bot4", 285.00, 302.96, "Sam Ruthe after his first run back · Back on Track"),
    (("so yall tell me", 9), "bot1", 271.26, 285.64, "Sam Ruthe · Back on Track, Ep. 1"),
]
SPLIT_AT = {}

S4 = "sub4"; TIE = "nztie"; SS = "nz338"; E8 = "nz800"; CK = "nz353"; BU = "bu_fan"; B1 = "bot1"; B2 = "bot2"; B3 = "bot3"; B4 = "bot4"
LB = "lr_ben"; LS = "lr_sam"; HE = "herald"; FS = "fan_sound"

def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 cold open ---------------------------------------------------------------------------------------
    S(PART[1] - 0.05, BU, 170.0, flash=1); lb(O, PART[1], 9.0)
    S(a("and this kid flew"), BU, 30.0)
    S(a("ran his first race"), BU, 195.0, slow=0.7)
    S(a("and beat a bunch"), BU, 245.0, slow=0.5)
    number(a("for the mile") - 1.6, 3.2, "3:48.88", "Mile · world U18 best", "Age 16 · Boston · Jan 31, 2026")
    S(a("his name is"), BU, 272.0)
    title(a("his name is") + 0.3, 3.2, "16 years old · New Zealand", "Sam Ruthe")
    S(a("and honestly"), B4, 15.0, slow=0.7)
    S(a("cause jakob"), CK, 140.0)
    S(a("couldnt even run that"), BU, 255.0, slow=0.5)
    S(a("how this kid got here"), B4, 190.0)
    S(a("race and the way"), B1, 30.0, bw=1)
    S(a("not how anybody"), B1, 72.0, bw=1, slow=0.7)
    # 2 Tauranga ----------------------------------------------------------------------------------------
    S(PART[2] - 0.05, B4, 140.0, flash=1); chapter(PART[2] + 0.2, "01", "Tauranga"); lb(O, PART[2], 3.4)
    date(a("sam from tauranga"), 2.8, "Tauranga, New Zealand", "Bay of Plenty · North Island")
    S(a("a beach town"), B4, 245.0)
    S(a("and running is basically"), B4, 205.0)
    S(a("his dad ben"), B1, 300.0); name(a("his dad ben") + 0.2, 2.6, "Ben Ruthe", "Dad · former NZ record holder")
    S(a("his mom jess"), B2, 102.0)
    S(a("and his grandma rosemary"), B4, 98.0, slow=0.7)
    title(a("and his grandma rosemary") + 0.3, 3.4, "Grandma Rosemary Wright", "800m gold · 1970 Commonwealth Games")
    S(a("then went to the olympics"), B4, 225.0)
    S(a("his dad said he remembers"), B1, 301.0)
    S(a("before he was even"), B2, 145.0, slow=0.7)
    S(a("his parents didnt"), B2, 52.0)
    S(a("no crazy mileage"), B4, 112.0)
    S(a("nobody pushing him"), B2, 60.0, slow=0.7)
    # 3 Age 15 ------------------------------------------------------------------------------------------
    S(PART[3] - 0.05, B3, 30.0, flash=1); chapter(PART[3] + 0.2, "02", "Fifteen"); lb(O, PART[3], 3.4)
    name(a("his coach craig") + 0.2, 2.6, "Craig Kirkwood", "Coach")
    S(a("with sam tanner"), CK, 30.0); name(a("with sam tanner") + 0.2, 2.6, "Sam Tanner", "2-time Olympian · training partner")
    S(a("and thats who hes been"), E8, 40.0)
    S(a("and it didnt take long"), TIE, 30.0)
    S(a("in february"), TIE, 90.0); number(a("in february") + 1.8, 3.2, "3:41.25", "1500m · world age-15 best", "Beats Jakob Ingebrigtsen's 3:42.44")
    S(a("world best for a"), TIE, 150.0)
    S(a("a month later at nationals"), TIE, 170.0)
    S(a("he ran with his training"), TIE, 200.0)
    S(a("and they literally tied"), TIE, 236.0, slow=0.6)
    number(a("so they had to share") - 0.8, 3.0, "3:44.31", "Dead heat · NZ 1500m title", "Shared with Sam Tanner")
    S(a("then on march"), S4, 15.0); date(a("then on march") + 0.2, 2.8, "March 19, 2025", "ACA Mile Night · Auckland")
    S(a("with tanner pacing"), S4, 120.0)
    S(a("he ran the mile in"), S4, 230.0, slow=0.6); number(a("he ran the mile in") + 1.0, 3.2, "3:58.35", "Mile · youngest sub-4 ever", "Age 15 · 341 days")
    S(a("that made him the youngest"), S4, 270.0)
    S(a("younger than jacob"), S4, 330.0, slow=0.7)
    S(a("he was 25 days"), S4, 412.0, slow=0.7)
    # 4 Nike + records ----------------------------------------------------------------------------------
    S(PART[4] - 0.05, B4, 20.0, flash=1); chapter(PART[4] + 0.2, "03", "Stacking Records"); lb(O, PART[4], 3.4)
    title(a("nike signed him") + 0.2, 3.0, "April 2025", "Signs with Nike at 15")
    S(a("and instead of moving"), B4, 70.0)
    S(a("he stayed home"), B4, 255.0)
    S(a("stayed with the same coach"), B3, 60.0)
    S(a("then at the end of"), SS, 20.0)
    S(a("he ran 338"), SS, 110.0); number(a("he ran 338") + 0.3, 3.0, "3:38.62", "1500m · NZ schools record", "In a semi-final · by 8 seconds")
    S(a("and that was in a semifinal"), SS, 160.0)
    S(a("and it broke the schools"), SS, 200.0)
    S(a("then in january"), E8, 60.0)
    S(a("he beat sam tanner"), E8, 100.0, slow=0.7); number(a("in the 800 in") + 0.4, 2.8, "1:45.86", "800m · beats Sam Tanner", "Potts Classic · Jan 2026")
    S(a("and a week before boston"), CK, 150.0)
    S(a("the fastest mile ever"), CK, 236.0, slow=0.6); number(a("the fastest mile ever") - 0.6, 3.0, "3:53.83", "Mile · fastest ever at 16", "Cooks Classic · Jan 24, 2026")
    # 5 Boston ------------------------------------------------------------------------------------------
    S(PART[5] - 0.05, BU, 10.0, flash=1); chapter(PART[5] + 0.2, "04", "Boston"); lb(O, PART[5], 3.4)
    S(a("january 31st"), BU, 45.0); date(a("january 31st"), 2.8, "January 31, 2026", "BU Terrier Classic · Boston")
    S(a("he flew in"), LS, 20.0)
    S(a("and he had never raced"), BU, 60.0)
    S(a("the plan was to sit"), BU, 165.0)
    S(a("but tanners leg"), BU, 180.0, slow=0.7)
    S(a("so now this"), BU, 195.0)
    S(a("and he was 3 years"), BU, 215.0)
    S(a("with a lap to go"), BU, 240.0, slow=0.7); name(a("he went right around") + 0.3, 2.6, "Pieter Sisk", "Belgian Olympian · 2nd · 3:50.31")
    S(a("closed his last"), BU, 250.0, slow=0.5)
    S(a("and won it in"), BU, 258.0, slow=0.6); number(a("and won it in") + 0.3, 3.4, "3:48.88", "Mile · world U18 best", "Last lap 28.38")
    S(a("thats a world under"), BU, 270.0)
    S(a("and it broke sir john"), BU, 278.0)
    O(a("and it broke sir john") + 0.2, 4.4, ("board", "New Zealand mile record", [("John Walker", "3:49.08", "Oslo 1982", 0), ("Sam Ruthe", "3:48.88", "Boston 2026", 1)], "44 years · broken at 16"))
    S(a("john walker a olympic"), BU, 283.0, slow=0.6)
    # 6 The lesson --------------------------------------------------------------------------------------
    S(PART[6] - 0.05, FS, 5.0, flash=1); chapter(PART[6] + 0.2, "05", "The Lesson"); lb(O, PART[6], 3.4)
    name(a("with cole hocker") + 0.2, 2.6, "Cole Hocker", "Olympic 1500m champion")
    S(a("in north carolina"), FS, 40.0); date(a("in north carolina") + 0.2, 2.6, "February 14, 2026", "ASICS Sound Invite · North Carolina")
    S(a("and this where he found"), FS, 60.0)
    S(a("hocker ran 345"), BU, 100.0, bw=1)
    S(a("and sam got boxed"), BU, 120.0, bw=1, slow=0.7); number(a("and finished seventh") - 0.2, 2.8, "7th · 3:52.46", "Mile · boxed in, lane 2", "Hocker 3:45.94 · American record")
    S(a("some people online"), LS, 5.0, bw=1)
    S(a("and honestly i think"), BU, 150.0)
    S(a("and the way he talked"), FS, 80.0)
    S(a("contact sport"), BU, 230.0, punch=0.3)
    quote(a("contact sport") - 1.8, 3.6, "You need to be more brutal.", "Sam Ruthe")
    S(a("then he went back to boston"), BU, 35.0)
    number(a("and ran 743") + 0.2, 2.6, "7:43.16", "3000m · NZ U20 record", "Boston · Feb 22, 2026")
    S(a("and when he got home"), B4, 180.0)
    S(a("national title in the 1500"), CK, 210.0)
    # 7 Everything lined up -> fracture -----------------------------------------------------------------
    S(PART[7] - 0.05, B3, 40.0, flash=1); chapter(PART[7] + 0.2, "06", "Lined Up"); lb(O, PART[7], 3.4)
    S(a("he got named to his first"), B4, 230.0)
    S(a("he was entered in the bowerman"), CK, 60.0)
    S(a("and the commonwealth games"), B4, 98.0)
    S(a("the same country"), B4, 245.0)
    S(a("his dad even said"), B1, 302.5)
    S(a("and then in april"), B1, 25.0, bw=1)
    S(a("stress fracture in his fibula"), B1, 40.0, bw=1, slow=0.7); title(a("stress fracture in his fibula") + 0.4, 3.0, "April 2026", "Stress fracture · fibula")
    S(a("and it wasnt even from running"), B1, 154.0, bw=1, slow=0.6)
    S(a("just like that"), B1, 230.0, bw=1)
    # 8 The decision ------------------------------------------------------------------------------------
    S(PART[8] - 0.05, B2, 20.0, flash=1); chapter(PART[8] + 0.2, "07", "The Decision"); lb(O, PART[8], 3.4)
    S(a("he could have rushed"), B1, 58.0)
    S(a("instead he started filming"), B2, 20.0)
    S(a("showing the crutches"), B1, 105.0)
    S(a("the swimming"), B2, 125.0)
    S(a("and the bike"), B2, 190.0)
    S(a("nine hours in three"), B2, 230.0, slow=0.7)
    S(a("in may he pulled"), B3, 40.0)
    S(a("pulled out of world"), B3, 100.0)
    S(a("his coach said"), B3, 200.0); name(a("his coach said") + 0.2, 2.6, "Craig Kirkwood", "Coach")
    S(a("and then he made"), B4, 20.0)
    S(a("leaving school at the end"), B4, 250.0)
    title(a("leaving school at the end") + 0.4, 3.2, "End of 2026", "Leaving school to run full time")
    S(a("europe in"), B4, 268.0, slow=0.7)
    # 9 What's next -------------------------------------------------------------------------------------
    S(PART[9] - 0.05, B4, 120.0, flash=1); chapter(PART[9] + 0.2, "08", "What's Next"); lb(O, PART[9], 10.0)
    S(a("his first run back"), B4, 185.0); title(a("his first run back") + 0.3, 2.8, "June 2026", "First run back · after 8 weeks")
    S(a("and the new zealand summer"), B4, 210.0)
    S(a("so im not gonna sit"), S4, 330.0)
    S(a("but this one feels different"), B4, 245.0)
    S(a("since he was"), B2, 100.0)
    S(a("he gonna be 18"), BU, 258.0, slow=0.5)
    O(a("he gonna be 18") + 0.2, 4.4, ("counter", 0, 18, "years old at the 2027 Worlds", "19 at LA 2028"))
    S(a("and 19 at the la"), S4, 412.0, slow=0.6)
    S(a("so yall tell me"), BU, 272.0)
    S(a("is he gonna be the next"), CK, 236.0, slow=0.5)
    S(a("or did this injury"), B1, 40.0, bw=1, slow=0.7)
    S(a("let me know in the comments"), B4, 290.0, slow=0.7)

"""Kevin Dare tribute (27 Nov 2026): soundbites + EDL. Cloned voice (A3b + quiet/respectful tag), own score K1-K6.
No video of Kevin or his family exists online, so his father's voice comes from NPR's April 2002 story (Tom Goldman), played
over real places: the University of Minnesota Field House (where it happened), Penn State's indoor track (the meet named after
him, fan-shot), State College aerials, snowy campus in February, box-collar footage. Never show a vaulter getting hurt.
Footage rules: no NBC/Peacock, FloTrack/MileSplit, RunnerSpace, NCAA/conference broadcasts, Olympic, Diamond League."""

TAGS = {
    "npr_2002": "NPR · All Things Considered · April 2002",
    "umn_fieldhouse": "University of Minnesota Field House", "fox9_fieldhouse": "FOX 9 Minneapolis-St. Paul",
    "kdi_2014": "Kevin Dare Invitational · Penn State · fan video", "kdi_2017": "Kevin Dare Invitational · Penn State · fan video",
    "psu_jumps": "Penn State Athletics", "psu_award": "Penn State Athletics", "psu_2004": "Penn State pole vault · 2004 · fan video",
    "mondo_slowmo": "Born To Fly Film", "hs_gopro": "High school pole vault · fan video", "collar_gill": "Gill Athletics",
    "sc_drone": "State College · drone · Patrick Cines", "umn_drone": "Minneapolis · drone · PrimoMedia",
    "umn_snow": "University of Minnesota · Adventure Walk 4K", "roach_vault": "Leon Roach vaulting · family video",
    "jj_johnson": "Jan Johnson · Your Pivot Journey", "hoot_softbox": "Team Hoot Pole Vault", "gill_nfhs": "Gill Athletics",
    "fox_roach": "KTLA · September 2009",
    "ph_kevin": "Kevin Dare · Penn State Athletics", "ph_eric": "Eric Dare · StateCollege.com",
}

R = {"raw": 1}
NPR = "npr_2002"
ED = "Ed Dare, Kevin's father · NPR · April 2002"
# cold open: his dad on the last thing Kevin said to him
PRE_SB = (NPR, 69.10, 79.20, ED, dict(vsrc="umn_fieldhouse", vss=16.0, quote="Dad... this is my day.", who="Kevin Dare, to his father, before the jump"))
SB_LIST = [  # ((insert before phrase, part), src, a, b, credit[, opts])
    (("and he could jump", 3), NPR, 35.90, 47.40, "NPR · All Things Considered · April 2002",
     dict(raw=1, vsrc="kdi_2014", vss=110.0)),
    (("they rushed him", 5), NPR, 101.40, 120.60, ED,
     dict(raw=1, vsrc="umn_fieldhouse", vss=30.0, quote="I immediately left my seat and ran down to the track.", who="Ed Dare")),
    (("the whole building", 6), NPR, 120.80, 134.50, "NPR · April 2002",
     dict(raw=1, vsrc="ph_kevin", vss=0.0, quote="53 days of just absolute living hell.", who="Ed Dare, on what would have been Kevin's 20th birthday")),
    (("but ed and terri", 8), NPR, 164.80, 182.30, ED,
     dict(raw=1, vsrc="umn_snow", vss=117.0, quote="Young athletes are dying.", who="Ed Dare, April 2002")),
    (("now to be fair", 8), NPR, 316.50, 330.30, ED,
     dict(raw=1, vsrc="hs_gopro", vss=84.0, quote="No one's going to sit here and tell me that a helmet would not have protected those athletes.", who="Ed Dare")),
    (("but i really feel", 8), "jj_johnson", 287.86, 298.60, "Jan Johnson, USATF pole vault safety chair · Your Pivot Journey"),
    (("but i really feel", 8), "jj_johnson", 643.10, 669.90, "Jan Johnson · on the steel plant box", R),
    (("and kevin name never", 9), "jj_johnson", 538.90, 557.60, "Jan Johnson · Your Pivot Journey", R),
    (("and kevin name never", 9), "fox_roach", 53.10, 85.40, "KTLA · September 2009 · Leon Roach, 19, UC San Diego", R),
    (("his brother eric grew", 9), "psu_award", 6.55, 12.85, "Penn State · Kevin Dare Most Inspirational Award", R),
    (("so the next time", 10), NPR, 442.10, 460.10, ED,
     dict(raw=1, vsrc="kdi_2017", vss=80.0, quote="The day that I can go out there and watch vaulters compete again...", who="Ed Dare")),
]
SPLIT_AT = {}

FH = "umn_fieldhouse"; F9 = "fox9_fieldhouse"; K14 = "kdi_2014"; K17 = "kdi_2017"; PJ = "psu_jumps"; PA = "psu_award"; P04 = "psu_2004"
MO = "mondo_slowmo"; GP = "hs_gopro"; CO = "collar_gill"; SC = "sc_drone"; UD = "umn_drone"; SN = "umn_snow"; RV = "roach_vault"
KV = "ph_kevin"; ER = "ph_eric"


def lb(O, t, dur): O(t, dur, ("letterbox",))


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 open ----------------------------------------------------------------------------------------
    S(PART[1] - 0.05, KV, 0.0, flash=1); lb(O, PART[1], 10.0)
    title(PART[1] + 1.0, 3.6, "Penn State · 2001 US junior champion", "Kevin Dare")
    S(a("one of the best young"), MO, 3.0, slow=0.6)
    S(a("he was already a national"), K14, 404.0)
    S(a("and one saturday"), UD, 125.0)
    S(a("with his mama"), FH, 20.0, slow=0.8)
    S(a("he went up for a jump"), MO, 12.0, slow=0.5)
    S(a("and he never came back"), FH, 40.0, bw=1, slow=0.7)
    S(a("aint nobody"), F9, 88.0, bw=1)
    S(a("so im gonna break down"), K14, 477.0, bw=1)
    # 2 the kid -------------------------------------------------------------------------------------
    S(PART[2] - 0.05, SC, 76.0, flash=1); chapter(PART[2] + 0.2, "01", "State College"); lb(O, PART[2], 3.4)
    S(a("his dad ed"), SC, 185.0)
    S(a("them two did everything"), ER, 0.0)
    S(a("eric threw the javelin"), SC, 290.0)
    S(a("and the way people talk"), KV, 4.0)
    S(a("natural leader"), PJ, 24.0)
    # 3 the rise ------------------------------------------------------------------------------------
    S(PART[3] - 0.05, GP, 28.0, flash=1); chapter(PART[3] + 0.2, "02", "The Rise"); lb(O, PART[3], 3.4)
    S(a("as a high schooler"), GP, 100.0, slow=0.7)
    title(a("as a high schooler") + 0.3, 3.0, "2000 · PIAA state champion", "Won it in a jump-off, in the rain")
    S(a("then in"), MO, 20.0, slow=0.5)
    number(a("national championship") + 0.3, 3.4, "16-6¾", "US junior champion · June 2001", "Pole vault")
    S(a("he competed for team"), K14, 184.0)
    S(a("and he went all the way"), K14, 257.0)
    S(a("then kevin stayed home"), SC, 132.0)
    S(a("right down the street"), PJ, 145.0)
    # 4 Penn State ----------------------------------------------------------------------------------
    S(PART[4] - 0.05, PJ, 200.0, flash=1); chapter(PART[4] + 0.2, "03", "Penn State"); lb(O, PART[4], 3.4)
    S(a("helped penn state win"), P04, 0.5, slow=0.8)
    S(a("and in practice"), PJ, 240.0)
    S(a("so going into his sophomore"), KV, 6.0)
    S(a("then come february"), UD, 160.0)
    date(a("the big ten indoor") + 0.2, 3.2, "February 23, 2002", "Big Ten Indoor Championships · Minneapolis")
    S(a("the big ten indoor"), FH, 64.0)
    S(a("his mom and dad"), FH, 25.0, slow=0.8)
    S(a("his roommate and best"), K14, 330.0)
    # 5 the jump ------------------------------------------------------------------------------------
    S(PART[5] - 0.05, FH, 45.0, flash=1); chapter(PART[5] + 0.2, "04", "The Jump"); lb(O, PART[5], 12.0)
    S(a("the bar was at"), MO, 18.0, slow=0.45)
    number(a("the bar was at") + 0.6, 3.2, "15-7", "First attempt at the height", "His best: 16-6¾")
    S(a("he ran down the runway"), GP, 60.0, slow=0.6)
    S(a("but he stalled"), MO, 25.0, slow=0.35, bw=1)
    S(a("one of the minnesota coaches"), FH, 50.0, bw=1)
    S(a("he came down head"), CO, 25.0, bw=1, slow=0.6)
    S(a("where you plant the pole"), CO, 45.0, bw=1, slow=0.6)
    S(a("dave was the closest"), FH, 55.0, bw=1)
    S(a("they rushed him"), UD, 190.0, bw=1)
    S(a("kevin dare was"), KV, 0.0, bw=1)
    O(a("kevin dare was") + 0.3, 3.6, ("title", "1982 – 2002", "Kevin Dare"))
    S(a("and back home"), SC, 343.0, bw=1)
    # 6 the meet ------------------------------------------------------------------------------------
    S(PART[6] - 0.05, F9, 93.0, flash=1, bw=1); chapter(PART[6] + 0.2, "05", "The Meet Stops"); lb(O, PART[6], 3.4)
    S(a("they canceled the pole"), FH, 30.0, bw=1)
    S(a("that saturday night"), SN, 272.0)
    S(a("but by sunday"), SN, 350.0)
    S(a("so the big ten canceled"), FH, 15.0, bw=1)
    S(a("instead the athletes"), K14, 551.0, slow=0.7)
    S(a("penn state athletic director"), PJ, 290.0)
    quote(a("penn state athletic director") + 1.0, 4.4, "An outstanding, personable young man.", "Tim Curley, Penn State athletic director")
    # 7 not the only one ----------------------------------------------------------------------------
    S(PART[7] - 0.05, SN, 428.0, flash=1); chapter(PART[7] + 0.2, "06", "Not The Only One"); lb(O, PART[7], 3.4)
    S(a("that same year"), GP, 122.0, bw=1)
    title(a("that same year") + 1.2, 3.6, "2002", "Jesus Quesada (Florida) · Samoa Fili (Kansas)")
    S(a("by then about"), SN, 506.0, bw=1)
    number(a("by then about") + 0.4, 3.0, "20", "Pole vault deaths since 1980", "Daily Pennsylvanian, April 2002")
    S(a("said something that i"), ER, 6.0)
    quote(a("he said had i known") + 0.2, 3.8, "Had I known what I know right now, Kevin would not be jumping.", "Ed Dare, 2002")
    # 8 the fight -----------------------------------------------------------------------------------
    S(PART[8] - 0.05, CO, 0.0, flash=1); chapter(PART[8] + 0.2, "07", "The Fight"); lb(O, PART[8], 3.4)
    S(a("a couple months later"), SC, 26.0)
    S(a("that august"), CO, 30.0)
    title(a("that august") + 0.3, 3.4, "August 2002 · Big Ten", "Longer pits · box collars required")
    S(a("high school rules"), K17, 25.0)
    S(a("a company came out"), CO, 55.0, slow=0.7)
    S(a("and ed worked on a helmet"), GP, 84.0, slow=0.7)
    S(a("not everybody agreed"), K14, 17.0)
    S(a("the head of usa"), PJ, 62.0, slow=0.7)
    # 9 the legacy ----------------------------------------------------------------------------------
    S(PART[9] - 0.05, K17, 76.0, flash=1); chapter(PART[9] + 0.2, "08", "His Name"); lb(O, PART[9], 3.4)
    S(a("his family started"), K14, 110.0)
    title(a("his family started") + 0.4, 3.2, "Kevin Dare Foundation", "Scholarships · the Kevin Dare Invitational")
    S(a("the kevin dare invitational"), K17, 100.0)
    S(a("his brother eric grew"), ER, 0.0)
    S(a("years later eric"), ER, 7.0)
    S(a("because like he said"), MO, 30.0, slow=0.5)
    # 10 the end ------------------------------------------------------------------------------------
    S(PART[10] - 0.05, MO, 5.0, flash=1, slow=0.5); lb(O, PART[10], 30.0)
    S(a("with that soft collar"), CO, 60.0, slow=0.6)
    S(a("i want yall to remember"), KV, 0.0)
    S(a("rest easy"), KV, 8.0)
    O(a("rest easy"), 4.0, ("title", "Kevin James Dare", "1982 – 2002"))
    S(a("and let me know"), K17, 110.0)

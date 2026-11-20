"""NCAA XC 2026 men's preview: soundbites + EDL (modern style: tools/modern.py incl. the new animated 'board').
Footage rules: no NCAA Championships channel / ESPN / conference broadcasts, no FloTrack/MileSplit, no Olympic/NBC,
no Diamond League. Race footage is RunnerSpace's own streams, school streams, fan phones and John Hedengren's camera.
Clips: scratchpad/men26/clips (INDEX.md). Soundbite times: scratchpad/men26/tx/*.json."""

TAGS = {
    "hansen_ncaa25_citius": "CITIUS MAG · NCAA XC 2025",
    "hansen_ncaa25_runmichigan": "RunMichigan · NCAA XC 2025",
    "hansen_acc25_runnerspace": "RunnerSpace · ACC XC 2025",
    "hansen_ncaa5k26_citius": "CITIUS MAG · NCAA 5000 · June 2026",
    "hansen_sub4_dad": "UVA, April 2023 · Jacob Hansen",
    "hansen_sub4_citius": "UVA, April 2023 · CITIUS MAG",
    "hansen_usatfxc25_runnerspace": "RunnerSpace · USATF XC 2025",
    "cheserek_2013_fan": "Terre Haute 2013 · Fan video · Jordan Guenther",
    "cheserek_2013_goducks": "GoDucks · 2013",
    "cheserek_2016_letsrun": "LetsRun · Terre Haute 2016",
    "kurgat_2019_letsrun": "LetsRun · Terre Haute 2019",
    "blanks_2023_letsrun": "LetsRun · NCAA XC 2023",
    "ekipruto_10k_boal": "Erik Boal Sports · April 2026",
    "mcnichols26_terrehaute_runnerspace": "RunnerSpace · Terre Haute, September 2026",
    "kipchoge_ncaa25_hedengren": "NCAA XC 2025 · John Hedengren",
    "ncaa25_hedengren_full": "NCAA XC 2025 · John Hedengren",
    "nutty26_runnerspace": "RunnerSpace · Nuttycombe 2026",
    "se_regional26": "Southeast Regional 2026 · Urban Announcing",
    "okstate_jamboree26": "Oklahoma State Athletics · Cowboy Jamboree 2026",
    "terrehaute_wtwo_2026": "WTWO News · November 2026",
    "laverngibson_wtwo_updates": "WTWO News · 2026",
    "laverngibson_course_run": "LaVern Gibson course · Daddy, Did You Win?",
}

CHAMPS = [("2013", "Edward Cheserek", "Kenya", 1), ("2014", "Edward Cheserek", "Kenya", 1), ("2015", "Edward Cheserek", "Kenya", 1),
          ("2016", "Patrick Tiernan", "Australia", 0), ("2017", "Justyn Knight", "Canada", 0), ("2018", "Morgan McDonald", "Australia", 0),
          ("2019", "Edwin Kurgat", "Kenya", 1), ("2020", "Conner Mantz", "USA", 0), ("2021", "Conner Mantz", "USA", 0),
          ("2022", "Charles Hicks", "GB / USA", 0), ("2023", "Graham Blanks", "USA", 0), ("2024", "Graham Blanks", "USA", 0),
          ("2025", "Habtom Samuel", "Eritrea", 0)]
WEATHER = [("2013", "Terre Haute · wind chill in the teens, mud", "Kenyan won", 1),
           ("2016", "Terre Haute · 36°, windy", "Cheserek 3rd", 0),
           ("2018", "Madison · 30°, snow on the course", "Australian won", 0),
           ("2019", "Terre Haute · 36°, rain, mud", "Kenyan won", 1),
           ("2021", "Tallahassee · about 60°", "American won", 0),
           ("2023", "Charlottesville · 62°, sunny", "American won", 0),
           ("2026", "Terre Haute forecast · sunny, 57°", "?", 1)]
RIVALS = [("Elsingi Kipruto", "Louisville", "Southeast Regional champ", 1), ("Brian Musau", "Oklahoma State", "Midwest Regional champ", 0),
          ("Denis Kipngetich", "Oklahoma State", "Big 12 champ", 0), ("Solomon Kipchoge", "Washington State", "West Regional champ", 0),
          ("New Mexico", "No. 1 team", "Running as a pack", 0)]

# cold open: Rocky Hansen minutes after finishing 2nd last year
PRE_SB = ("hansen_ncaa25_citius", 46.1, 51.6, "Rocky Hansen · CITIUS MAG · NCAA XC, November 2025")
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("and thats the year", 2), "cheserek_2016_letsrun", 8.8, 15.8, "Edward Cheserek after 3rd · LetsRun · 2016"),
    (("2019 it was 36 degrees", 2), "cheserek_2013_goducks", 50.5, 56.5, "Edward Cheserek after winning · GoDucks · 2013"),
    (("and they lost some races", 2), "kurgat_2019_letsrun", 36.0, 48.9, "Edwin Kurgat after winning · LetsRun · 2019"),
    (("then this summer", 3), "hansen_ncaa25_citius", 61.1, 77.2, "Rocky Hansen · CITIUS MAG · NCAA XC 2025"),
    (("and samuel aint even there", 4), "hansen_ncaa5k26_citius", 116.1, 120.0, "Rocky Hansen · CITIUS MAG · June 2026"),
    (("oklahoma state got two", 5), "ekipruto_10k_boal", 50.9, 60.7, "Elsingi Kipruto · Erik Boal Sports · April 2026"),
    (("so for me it really", 6), "hansen_acc25_runnerspace", 79.8, 88.0, "Rocky Hansen · RunnerSpace · 2025"),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    H25, NUT, MC = "ncaa25_hedengren_full", "nutty26_runnerspace", "mcnichols26_terrehaute_runnerspace"
    # 1 the drought ---------------------------------------------------------------------
    S(PART[1] - 0.05, "terrehaute_wtwo_2026", 24.0, flash=1)
    date(a("championships are tomorrow"), 3.0, "Saturday, November 21, 2026", "NCAA Cross Country · Terre Haute, Indiana")
    S(a("and there is something"), H25, 752.0)
    S(a("a kenyan man has not won"), H25, 822.0, slow=0.7)
    S(a("not won ncaa cross country"), "kipchoge_ncaa25_hedengren", 13.0)
    number(a("since 2019"), 2.8, "2019", "Last Kenyan champion", "Edwin Kurgat · Iowa State")
    S(a("now thats six straight years"), H25, 1308.0, bw=1)
    S(a("thats crazy to me"), H25, 892.0)
    S(a("from 2012 to 2019"), "cheserek_2013_goducks", 69.0); number(a("five out of eight"), 2.6, "5 of 8", "Kenyan titles", "2012–2019")
    S(a("edward cesarek"), "cheserek_2013_fan", 3.0, slow=0.6); name(a("edward cesarek"), 2.8, "Edward Cheserek", "Oregon · 3 straight titles")
    S(a("in 2019 edwin"), "kurgat_2019_letsrun", 6.0); name(a("in 2019 edwin"), 2.6, "Edwin Kurgat", "Iowa State · 2019")
    O(a("and since then its been"), 7.0, ("board", "NCAA cross country champions", CHAMPS, "No Kenyan winner since 2019"))
    S(a("and since then its been"), "blanks_2023_letsrun", 95.0)
    S(a("charles hicks"), H25, 962.0)
    S(a("graham blanks"), "blanks_2023_letsrun", 158.0)
    S(a("hupton samuel"), H25, 1308.0, slow=0.7)
    S(a("and yeah no kenyans"), H25, 1522.0)
    # 2 the weather ---------------------------------------------------------------------
    S(PART[2] - 0.05, "laverngibson_course_run", 205.0, flash=1); chapter(PART[2] + 0.2, "01", "The Weather")
    S(a("nationals is in november"), "laverngibson_course_run", 287.0)
    S(a("so its usually cold"), H25, 928.0)
    S(a("like half of these races"), H25, 718.0, bw=1)
    S(a("in 2018 in madison"), "laverngibson_course_run", 369.0, bw=1); title(a("in 2018 in madison"), 2.8, "2018 · Madison, Wisconsin", "Snow on the course")
    S(a("2016 in indiana"), "laverngibson_course_run", 451.0); title(a("2016 in indiana"), 2.8, "2016 · Terre Haute", "36° · windy")
    S(a("going for his fourth title"), "cheserek_2016_letsrun", 3.0, bw=1)
    S(a("but i looked into it"), "cheserek_2013_goducks", 29.0)
    O(a("cuz the coldest nastiest"), 6.5, ("board", "Kenyans in the worst weather", WEATHER[:4], "Terre Haute's 2 nastiest races: Kenyans won both"))
    S(a("cuz the coldest nastiest"), "cheserek_2013_fan", 8.0)
    S(a("the kings won them"), "cheserek_2013_goducks", 128.0)
    S(a("2013 windchill"), "cheserek_2013_goducks", 147.0)
    S(a("and they lost some races"), "blanks_2023_letsrun", 221.0)
    S(a("so whatever the reason is"), "terrehaute_wtwo_2026", 121.0)
    S(a("nobody gets to use"), H25, 1068.0)
    number(a("the forecast in indiana"), 3.0, "57°", "Saturday forecast · Terre Haute", "Sunny · no rain"); S(a("the forecast in indiana"), "laverngibson_wtwo_updates", 47.0)
    S(a("57 degrees when they go off"), "se_regional26", 15.0)
    S(a("no rain no snow"), "terrehaute_wtwo_2026", 105.0)
    S(a("its the first time theyve been back"), "laverngibson_wtwo_updates", 69.0)
    S(a("twenty degrees warmer"), "terrehaute_wtwo_2026", 57.0)
    # 3 Rocky Hansen --------------------------------------------------------------------
    S(PART[3] - 0.05, "hansen_ncaa25_runmichigan", 21.0, flash=1); chapter(PART[3] + 0.2, "02", "Rocky Hansen")
    name(a("rocky hanson") + 0.4, 3.0, "Rocky Hansen", "Wake Forest · senior")
    S(a("he runs for wake forest"), "hansen_acc25_runnerspace", 18.0)
    S(a("hes from north carolina"), "hansen_sub4_citius", 77.0)
    S(a("first high schooler in north carolina"), "hansen_sub4_dad", 252.0); number(a("run sub four"), 2.8, "3:59.56", "First NC high schooler under 4:00", "April 2023")
    S(a("last year at nationals"), H25, 788.0)
    S(a("he went straight to the front"), H25, 822.0, slow=0.7)
    S(a("he finished second"), H25, 1342.0); number(a("he finished second"), 2.8, "4.1", "Seconds behind the winner", "2nd · NCAA XC 2025")
    S(a("then this summer"), "hansen_ncaa5k26_citius", 41.0); title(a("then this summer"), 2.8, "NCAA 5000 · June 2026", "2nd behind Habtom Samuel")
    S(a("behind samuel again"), "kipchoge_ncaa25_hedengren", 28.0)
    S(a("track and field news"), "hansen_ncaa5k26_citius", 284.0); title(a("track and field news"), 3.0, "Track & Field News preseason", "No. 1 · only American in the top 10")
    # 4 the worry -----------------------------------------------------------------------
    S(PART[4] - 0.05, NUT, 1149.0, flash=1); chapter(PART[4] + 0.2, "03", "The Worry")
    S(a("he only raced twice"), NUT, 1238.0)
    S(a("didnt win either one"), NUT, 1201.0)
    S(a("he was 4th"), NUT, 1289.0); title(a("he was 4th"), 3.0, "2026 cross country", "4th Nuttycombe · 2nd ACC · skipped regionals")
    S(a("and he skipped regionals"), "hansen_ncaa5k26_citius", 447.0, bw=1)
    S(a("so we really dont know"), "hansen_ncaa5k26_citius", 528.0, bw=1)
    S(a("and samuel aint even there"), H25, 1308.0)
    S(a("he went pro"), H25, 1522.0)
    S(a("so the guy whos beaten"), "kipchoge_ncaa25_hedengren", 18.0)
    S(a("a whole new group"), H25, 752.0, slow=0.7)
    # 5 the Kenyans ---------------------------------------------------------------------
    S(PART[5] - 0.05, MC, 4.0, flash=1); chapter(PART[5] + 0.2, "04", "The Contenders")
    name(a("from louisville"), 2.8, "Elsingi Kipruto", "Louisville")
    S(a("hes the guy that beat"), "ekipruto_10k_boal", 35.0)
    S(a("and then he won the southeast"), "se_regional26", 75.0); number(a("southeast regionals in 28"), 2.6, "28:20", "Southeast Regional · Kipruto")
    S(a("brian massal"), "okstate_jamboree26", 2797.0); name(a("brian massal"), 2.8, "Brian Musau", "Oklahoma State")
    S(a("thats who i wanna see win"), "okstate_jamboree26", 2367.0)
    S(a("and then you got dennis"), MC, 30.0); name(a("and then you got dennis"), 2.6, "Denis Kipngetich", "Oklahoma State · Big 12 champ")
    S(a("solomon kipchoge"), "kipchoge_ncaa25_hedengren", 23.0); name(a("solomon kipchoge"), 2.6, "Solomon Kipchoge", "Washington State")
    S(a("finished third in nationals"), H25, 1138.0)
    S(a("and then new mexico"), NUT, 1309.0)
    O(a("and then new mexico"), 5.5, ("board", "Who can beat Rocky Hansen?", RIVALS, ""))
    S(a("some of them are even saying"), MC, 47.0)
    # 6 the call ------------------------------------------------------------------------
    S(a("comes down to this"), "hansen_ncaa25_citius", 287.0); chapter(a("comes down to this"), "05", "The Call")
    S(a("if rocky hansons"), NUT, 1149.0)
    S(a("he run from the front"), H25, 822.0)
    S(a("i think he got a real shot"), "hansen_sub4_citius", 230.0)
    S(a("but if hes still"), "hansen_usatfxc25_runnerspace", 44.0, bw=1)
    S(a("wins for the first time since 2019"), MC, 64.0)
    O(a("and its going to be good weather"), 3.8, ("board", "Tomorrow · Terre Haute", WEATHER[6:], "Sunny · no rain · no excuses"))
    S(a("and its going to be good weather"), "terrehaute_wtwo_2026", 121.0)
    S(a("so who y all got"), MC, 55.0)
    S(a("let me know"), "kipchoge_ncaa25_hedengren", 13.0)

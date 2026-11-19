"""Athing Mu: soundbites + EDL in the modern style (tools/modern.py: date, number, name, title, quote, chapter).
Footage rules (user, 18 Nov 2026): fan-shot/re-uploads first; NBC allowed for this video but no NBC clip over 8 s
(a_feisty_fall and a_tokyo_final_reup are NBC/OBS re-uploads: every shot from them stays short); no FloTrack/MileSplit.
Clips are in scratchpad/athing/clips (see footage.md). Soundbite times come from scratchpad/athing/tx/*.json."""

TAGS = {
    "a_fan_trials2024_fall": "2024 US Olympic Trials · Fan video · Seth Jenny",
    "a_feisty_fall": "2024 US Olympic Trials · via Feisty Media",
    "a_fan_eugene_lastlap": "2022 World Championships · Fan video",
    "a_tokyo_final_reup": "Tokyo 2020 800m final · re-upload",
    "a_tokyo_presser": "Tokyo 2020 press conference · BeanymanNews",
    "a_cbs_philly_tokyo": "CBS Philadelphia · August 2021",
    "a_njspotlight_tokyo": "NJ Spotlight News · August 2021",
    "a_trenton_airport": "Peterson's Breaking News of Trenton · 2021",
    "a_trenton_parade": "Peterson's Breaking News of Trenton · 2021",
    "a_trenton_speech": "Trenton homecoming · Kyle Franko · 2021",
    "a_keely_reacts": "Athletics Weekly · June 2024",
    "a_runnerspace_mtsac2025": "RunnerSpace · Mt. SAC Relays 2025",
    "a_bodega_2025": "Bodega Track · July 2025",
    "a_citius_pre2025": "CITIUS MAG · July 2025",
    "a_citius_usa2025": "CITIUS MAG · August 2025",
    "a_citius_budapest2023": "CITIUS MAG · August 2023",
    "a_citius_pre2023": "CITIUS MAG · September 2023",
    "a_pre2023_ar": "Prefontaine Classic 2023 · TrackalertsTV",
    "a_pivot_podcast": "The Pivot Podcast · March 2023",
    "a_callyoursister": "Call Your Sister podcast · November 2024",
    "a_rw_600m_2019": "Runner's World · February 2019",
    "a_own_2019_musiccity": "Athing Mu's YouTube channel · 2019",
    "a_kags_tamu": "KAGS · August 2021",
    "a_letsrun_kersee2023": "LetsRun · July 2023",
}

FALLCROP = "crop=iw:ih*0.56:0:ih*0.42"   # below Feisty's burned-in captions

# cold open: the stands at Hayward, the crowd as the final starts
PRE_SB = ("a_fan_trials2024_fall", 4.0, 9.0, "2024 US Olympic Trials · Fan video · Seth Jenny")
SB_LIST = [  # ((before phrase, part), src, a, b, credit, {opts})
    (("and one of the pros", 3), "a_rw_600m_2019", 26.4, 39.5, "Athing Mu, 16 · Runner's World · February 2019"),
    (("february 24th", 3), "a_cbs_philly_tokyo", 54.2, 57.6, "Al Jennings · CBS Philadelphia · 2021"),
    (("then she anchors", 4), "a_cbs_philly_tokyo", 14.8, 20.7, "CBS Philadelphia · August 2021"),
    (("they light up the bridge", 4), "a_tokyo_presser", 51.1, 61.0, "Tokyo 2020 press conference"),
    (("2022 world championships", 5), "a_trenton_speech", 107.8, 111.5, "Athing Mu · Trenton homecoming · 2021"),
    (("three months later", 5), "a_citius_budapest2023", 611.6, 614.9, "Athing Mu · CITIUS MAG · Budapest, August 2023"),
    (("but three weeks later", 6), "a_citius_budapest2023", 386.1, 394.9, "Athing Mu · CITIUS MAG · Budapest, August 2023"),
    (("three times she thought", 6), "a_pivot_podcast", 832.2, 850.7, "Athing Mu · The Pivot Podcast · March 2023"),
    (("she told us herself", 11), "a_pivot_podcast", 2720.5, 2722.4, "Athing Mu · The Pivot Podcast · March 2023"),
    (("and 6 weeks later", 7), "a_keely_reacts", 148.6, 162.9, "Keely Hodgkinson · Athletics Weekly · June 2024"),
    (("march 2025", 8), "a_callyoursister", 1929.1, 1934.6, "Athing Mu · Call Your Sister podcast · November 2024"),
    (("august 1st 2025", 8), "a_citius_pre2025", 139.8, 159.8, "Athing Mu after Pre 2025 · CITIUS MAG"),
    (("this is the last race", 8), "a_citius_usa2025", 148.8, 151.6, "Athing Mu after USAs 2025 · CITIUS MAG"),
    (("so what really went wrong", 11), "a_trenton_speech", 133.6, 143.8, "Athing Mu · Trenton homecoming · 2021"),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    F, T, E = "a_fan_trials2024_fall", "a_tokyo_final_reup", "a_fan_eugene_lastlap"
    # 1 the fall -------------------------------------------------------------------------
    S(PART[1] - 0.05, F, 1.0, flash=1); date(a("june 24th"), 3.2, "June 24, 2024", "US Olympic Trials · Eugene, Oregon")
    S(a("hayward field"), F, 3.0)
    S(a("the olympic trials finals"), F, 5.2, punch=0.6)
    S(a("defending olympic champion"), T, 46.0, slow=0.7); name(a("defending olympic champion"), 3.0, "Athing Mu", "2021 Olympic 800m champion")
    S(a("american record"), T, 42.0)
    S(a("fastest time in the semis"), F, 12.0)
    S(a("200 meters in"), "a_feisty_fall", 2.4, crop=FALLCROP)
    S(a("she goes down"), "a_feisty_fall", 4.0, crop=FALLCROP, slow=0.45, bw=1)
    S(a("she gets up"), "a_feisty_fall", 10.0, crop=FALLCROP)
    S(a("finishes last place"), F, 186.0, punch=0.4)
    S(a("22 seconds"), F, 186.0); number(a("22 seconds"), 3.0, "22.33", "Seconds behind the winner", "Trials final · 2:19.69")
    S(a("three years earlier"), T, 40.0, slow=0.6)
    S(a("best 800 meter runner"), E, 21.0, slow=0.7)
    S(a("since august 1st"), "a_citius_usa2025", 30.0, bw=1); date(a("since august 1st"), 3.0, "August 1, 2025", "Her last race")
    S(a("aint raced one time"), "a_citius_usa2025", 200.0, bw=1)
    S(a("so whats happened"), "a_pivot_podcast", 2410.0)
    S(a("where is she right now"), "a_callyoursister", 1376.0)
    S(a("stay to the end"), F, 172.0)
    # 2 Trenton --------------------------------------------------------------------------
    S(PART[2] - 0.05, "a_trenton_parade", 13.0, flash=1); chapter(PART[2] + 0.2, "01", "Trenton")
    S(a("her family fled"), "a_trenton_parade", 174.0)
    title(a("south sudan"), 3.0, "Family origin", "What is now South Sudan")
    S(a("number six of seven"), "a_trenton_airport", 292.0)
    S(a("first born in america"), "a_trenton_parade", 254.0)
    S(a("her big brother"), "a_trenton_parade", 94.0)
    S(a("so at six years old"), "a_own_2019_musiccity", 8.0)
    S(a("crazy part"), "a_own_2019_musiccity", 66.0, punch=0.5)
    S(a("never ran for her high school"), "a_own_2019_musiccity", 72.0)
    S(a("only club track"), "a_own_2019_musiccity", 98.0)
    S(a("her coach al jennings"), "a_cbs_philly_tokyo", 54.2); name(a("her coach al jennings"), 3.2, "Al Jennings", "Founder · Trenton Track Club")
    S(a("he says she had"), "a_cbs_philly_tokyo", 60.0)
    # 3 16 with braces -------------------------------------------------------------------
    S(PART[3] - 0.05, "a_rw_600m_2019", 3.0, flash=1); date(PART[3] + 0.1, 3.0, "February 24, 2019", "USA Indoor Championships · New York")
    S(a("grown pros"), "a_rw_600m_2019", 112.0)
    S(a("is 16"), "a_rw_600m_2019", 10.0, slow=0.7)
    S(a("braces on her teeth"), "a_rw_600m_2019", 64.0)
    S(a("she runs a 600"), "a_rw_600m_2019", 31.0, punch=0.5); number(a("she runs a 600"), 3.2, "1:23.57", "American record · 600m", "Age 16")
    S(a("a new american record"), "a_rw_600m_2019", 1.0)
    S(a("raven rogers"), "a_rw_600m_2019", 51.0); name(a("raven rogers"), 3.0, "Raevyn Rogers", "Pro · beat by Mu at 16")
    S(a("remember that name"), "a_rw_600m_2019", 44.0, slow=0.6)
    # 4 the rise -------------------------------------------------------------------------
    S(PART[4] - 0.05, "a_kags_tamu", 30.0, flash=1); chapter(PART[4] + 0.2, "02", "The Rise")
    S(a("collegiate record"), "a_kags_tamu", 120.0); number(a("ncaa champion"), 3.0, "49.57", "NCAA 400m champion", "Collegiate record · June 2021")
    S(a("then she turns pro"), "a_kags_tamu", 300.0)
    S(a("signs with nike"), "a_letsrun_pre2021", 30.0)
    S(a("the olympic trials she wins"), "a_cbs_philly_tokyo", 50.0); number(a("the olympic trials she wins") + 0.3, 2.8, "1:56.07", "Olympic Trials · June 2021")
    S(a("august 3rd"), T, 1.0, flash=1); date(a("august 3rd"), 3.0, "August 3, 2021", "Olympic 800m final · Tokyo")
    S(a("the olympic final"), T, 6.0)
    S(a("takes the lead"), "a_cbs_philly_tokyo", 30.0)
    S(a("nobody ever touches her"), T, 37.0)
    number(a("155"), 3.2, "1:55.21", "American record", "Olympic gold · age 19"); S(a("american record gold"), T, 46.0, slow=0.6)
    S(a("shes 19 years old"), "a_njspotlight_tokyo", 24.0)
    S(a("since 1968"), "a_njspotlight_tokyo", 28.0); title(a("since 1968"), 3.0, "First US woman since", "Madeline Manning · 1968")
    S(a("then she anchors"), "a_cbs_philly_tokyo", 22.0)
    S(a("trenton throws her a parade"), "a_trenton_parade", 201.0)
    S(a("they light up the bridge"), "a_trenton_parade", 147.0)
    # 5 the cracks -----------------------------------------------------------------------
    S(PART[5] - 0.05, E, 6.0, flash=1); date(PART[5] + 0.1, 3.0, "July 24, 2022", "World Championships · Eugene")
    S(a("she holds keely"), E, 18.0, slow=0.6)
    S(a("world champion"), E, 45.0, punch=0.3); number(a("world champion"), 3.0, "0.08", "Seconds ahead of Keely Hodgkinson", "1:56.30 · World champion")
    S(a("that made her the youngest"), "a_trenton_speech", 82.0)
    S(a("shes 20"), "a_trenton_airport", 328.0)
    S(a("but here go what nobody knew"), "a_pivot_podcast", 1352.0, bw=1)
    S(a("messed up hip"), "a_pivot_podcast", 1372.0, punch=0.4)
    S(a("three months later"), "a_letsrun_kersee2023", 20.0)
    S(a("she leaves her college coach"), "a_letsrun_kersee2023", 150.0)
    S(a("bobby kersey"), "a_letsrun_kersee2023", 300.0); name(a("bobby kersey"), 3.2, "Bobby Kersee", "New coach · November 2022")
    S(a("mostly known for sprints"), "a_letsrun_kersee2023", 450.0)
    # 6 the doubt ------------------------------------------------------------------------
    S(PART[6] - 0.05, "a_pivot_podcast", 167.0, flash=1); chapter(PART[6] + 0.2, "03", "The Doubt")
    S(a("says something"), "a_pivot_podcast", 858.0)
    S(a("three times she thought"), "a_pivot_podcast", 866.0, punch=0.4)
    S(a("that summer"), "a_citius_budapest2023", 30.0)
    S(a("her coach told the la times"), "a_letsrun_kersee2023", 520.0, bw=1)
    S(a("she deletes her social media"), "a_citius_budapest2023", 200.0)
    S(a("for the first time as a pro"), "a_citius_budapest2023", 320.0, bw=1)
    S(a("bronze"), "a_citius_budapest2023", 420.0, bw=1); title(a("bronze"), 2.8, "World Championships · Budapest", "Bronze · 1:56.61")
    S(a("three weeks later"), "a_pre2023_ar", 2.0, flash=1)
    S(a("154"), "a_pre2023_ar", 20.0, punch=0.3); number(a("154"), 3.2, "1:54.97", "New American record", "Prefontaine Classic · September 2023")
    S(a("so she still had it"), "a_pre2023_ar", 60.0)
    S(a("which makes what happened next"), "a_pre2023_ar", 80.0, bw=1)
    # 7 the Trials -----------------------------------------------------------------------
    S(PART[7] - 0.05, F, 64.0, flash=1); chapter(PART[7] + 0.2, "04", "The Fall")
    S(a("she tears her hamstring"), F, 70.0, bw=1)
    S(a("sports illustrated reported"), F, 87.0)
    S(a("cleared to run"), F, 96.0)
    S(a("she makes the final"), F, 111.0)
    S(a("then the final"), F, 4.0, punch=0.5)
    S(a("shes cutting in"), "a_feisty_fall", 2.0, crop=FALLCROP, slow=0.6)
    S(a("raven rogers"), "a_feisty_fall", 3.6, crop=FALLCROP, slow=0.4); name(a("raven rogers"), 2.6, "Raevyn Rogers", "2021 Olympic bronze medalist")
    S(a("the same woman"), "a_rw_600m_2019", 51.0, bw=1)
    S(a("rogers stays up"), "a_feisty_fall", 4.4, crop=FALLCROP, slow=0.35, bw=1)
    S(a("she finishes last"), "a_feisty_fall", 17.0)
    S(a("2 19 69"), F, 186.0); number(a("2 19 69"), 3.0, "2:19.69", "Last place · Trials final")
    S(a("her team"), F, 144.0)
    S(a("denied"), F, 153.0, bw=1); title(a("denied"), 2.4, "Protest", "Denied")
    S(a("they appealed"), F, 166.0, bw=1); title(a("they appealed") + 0.6, 2.4, "Appeal", "Denied")
    S(a("in paris"), "a_keely_reacts", 10.0); name(a("keely hodgson"), 3.0, "Keely Hodgkinson", "Paris 2024 Olympic champion")
    S(a("she doesnt really talk"), "a_callyoursister", 852.0)
    # 8 the comeback ---------------------------------------------------------------------
    S(PART[8] - 0.05, "a_callyoursister", 721.0, flash=1); chapter(PART[8] + 0.2, "05", "The Comeback")
    S(a("a russian runner"), "a_callyoursister", 1114.0); name(a("a russian runner"), 3.0, "Yegor Nikolayev", "2012 Olympian · 1500m")
    S(a("she tries to come back"), "a_runnerspace_mtsac2025", 138.0)
    S(a("a 5k"), "a_runnerspace_mtsac2025", 193.0)
    S(a("she steps off"), "a_runnerspace_mtsac2025", 413.0, slow=0.7)
    S(a("then her second race"), "a_bodega_2025", 49.0); number(a("then her second race") + 0.6, 3.0, "4:10.70", "1500m · 2nd in her heat", "May 2025")
    S(a("then the pre fontaine"), "a_citius_pre2025", 20.0)
    S(a("last place"), "a_citius_pre2025", 60.0, bw=1); number(a("last place"), 3.0, "2:03.44", "10th of 10 · Prefontaine Classic", "July 2025")
    S(a("august 1st 2025"), "a_citius_usa2025", 11.0); date(a("august 1st 2025"), 3.0, "August 1, 2025", "US Championships · semifinal")
    S(a("159"), "a_citius_usa2025", 55.0); number(a("159"), 3.0, "1:59.79", "Out in the semifinal")
    S(a("she doesnt even make the final"), "a_citius_usa2025", 99.0, bw=1)
    # 9 the silence ----------------------------------------------------------------------
    S(PART[9] - 0.05, "a_letsrun_kersee2023", 560.0, flash=1, bw=1); date(PART[9] + 0.1, 3.0, "September 2025", "She leaves Bobby Kersee")
    S(a("moves to dallas"), "a_callyoursister", 1900.0); title(a("moves to dallas"), 3.0, "New home", "Dallas, Texas")
    S(a("kersee calls it"), "a_letsrun_kersee2023", 380.0); quote(a("kersee calls it"), 3.4, "It was just a life decision.", "Bobby Kersee to LetsRun, December 2025")
    S(a("she never explained it"), "a_callyoursister", 2031.0, bw=1)
    S(a("2026 comes"), F, 172.0, bw=1); title(a("2026 comes"), 2.8, "2026", "No races")
    S(a("nike says"), "a_citius_usa2025", 300.0, bw=1)
    S(a("a source told"), "a_citius_usa2025", 420.0, bw=1)
    S(a("people started making videos"), "a_callyoursister", 2162.0)
    # 10 the answer ----------------------------------------------------------------------
    S(PART[10] - 0.05, "a_callyoursister", 2555.0, flash=1); date(PART[10] + 0.1, 3.0, "October 15, 2026", "Instagram")
    S(a("shes pregnant"), "a_callyoursister", 2686.0, punch=0.3)
    S(a("can't wait"), "a_callyoursister", 2817.0); quote(a("can't wait"), 3.4, "Can't wait to meet our little Sunshine!", "Athing Mu-Nikolayev, October 15, 2026")
    S(a("so thats where she went"), "a_callyoursister", 2948.0)
    S(a("living in dallas"), "a_callyoursister", 3079.0)
    S(a("she still holds"), "a_pre2023_ar", 40.0); number(a("she still holds"), 3.2, "1:54.97", "Still the American record")
    # 11 the end -------------------------------------------------------------------------
    S(PART[11] - 0.05, F, 40.0, flash=1)
    S(a("the hip"), E, 30.0)
    S(a("the hamstring"), F, 70.0, bw=1)
    S(a("the coach"), "a_letsrun_kersee2023", 300.0)
    S(a("the fall"), "a_feisty_fall", 4.4, crop=FALLCROP, slow=0.4, bw=1)
    S(a("or did she just stop"), "a_pivot_podcast", 1360.0, bw=1)
    S(a("she told us herself"), "a_pivot_podcast", 2718.0)
    S(a("and she still won"), T, 48.0, slow=0.6)
    S(a("world title"), E, 45.0)
    S(a("broke the american record"), "a_pre2023_ar", 2.0)
    S(a("is less than 2 years"), "a_trenton_parade", 442.0); title(a("is less than 2 years"), 3.0, "LA 2028", "Less than 2 years away")
    S(a("she aint said"), "a_trenton_parade", 486.0)
    S(a("do yall think"), "a_trenton_airport", 346.0)
    S(a("let me know"), "a_trenton_airport", 310.0)

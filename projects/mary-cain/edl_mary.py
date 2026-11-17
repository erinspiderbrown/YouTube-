"""Mary Cain: soundbites + EDL in the NEW modern style (user, 17 Nov 2026).
Graphics: tools/modern.py (date, number, name, title, quote, chapter). No stickers, stamps or slams.
Footage: NYT Opinion 2019 video op-ed (logo removed with delogo; NYT's own text overlays are never used: 8-11, 20-26,
36-41, 166-171, 232-241, 290-305 and 400+ are skipped), LetsRun, Armory Track, a fan video of Millrose 2013,
the Lindsey Hein podcast (2020) and WBUR CitySpace (2026). No Olympic/NCAA/Worlds broadcasts, no FloTrack.
Audio-only soundbites (360p podcasts) play her voice over clean B-roll with the words on screen (vsrc/quote)."""

TAGS = {
    "m_nyt": "New York Times Opinion · 2019", "m_letsrun2015": "LetsRun · June 2015", "m_salazar2013": "LetsRun · June 2013",
    "m_armory2012": "Armory Track · 2012", "m_millrose2013": "Millrose Games 2013 · Fan video", "m_freshman2011": "Armory Track · 2011",
    "m_hein2020": "I'll Have Another podcast · 2020", "m_wbur2026": "WBUR CitySpace · 2026",
}

# cold open: Mary in her own words
PRE_SB = ("m_nyt", 42.0, 56.9, "New York Times Opinion · 2019")
SB_LIST = [  # ((before phrase, part), src, a, b, credit, {opts})
    (("her name is", 1), "m_nyt", 4.4, 6.7, "New York Times Opinion · 2019"),
    (("by 16", 2), "m_armory2012", 61.1, 70.4, "Mary, 15 · Armory Track · 2012"),
    (("salazar was the head", 2), "m_nyt", 19.2, 27.9, "New York Times Opinion · 2019"),
    (("then in november", 3), "m_salazar2013", 0.0, 17.4, "Alberto Salazar on Mary · LetsRun · June 2013"),
    (("and her body started", 5), "m_nyt", 101.5, 123.2, "New York Times Opinion · 2019"),
    (("2015 she was", 5), "m_letsrun2015", 142.9, 155.4, "Mary, 19 · LetsRun · June 2015"),
    (("in 2016 she leaves", 5), "m_nyt", 242.2, 261.8, "New York Times Opinion · 2019"),
    (("then september 30", 6), "m_letsrun2015", 235.6, 254.4, "Asked about Salazar · LetsRun · June 2015"),
    (("so where is", 8), "m_hein2020", 188.2, 204.7, "I'll Have Another podcast · 2020",
     {"vsrc": "m_nyt", "vss": 380.0, "quote": "That's why I told my story. I don't want people to feel alone.", "who": "Mary Cain, 2020"}),
    (("mary cain broke records", 9), "m_wbur2026", 93.0, 108.4, "WBUR CitySpace · 2026",
     {"vsrc": "m_nyt", "vss": 58.0, "quote": "Despite being a full-time medical student at Stanford... I hope the story that I tell can help others.", "who": "Mary Cain, 2026"}),
    (("which one matters more", 9), "m_nyt", 365.7, 378.4, "New York Times Opinion · 2019"),
]


def edl(a, S, O, number, title, name, quote, date, chapter, PART):
    # 1 the video ------------------------------------------------------------------------
    S(a("november 7th"), "m_nyt", 61.0, flash=1); date(a("november 7th"), 3.4, "November 7, 2019", "New York Times Opinion")
    S(a("sits in front"), "m_nyt", 148.0)
    S(a("no race"), "m_nyt", 2.0)
    S(a("just her talking"), "m_nyt", 254.0)
    S(a("the video has"), "m_nyt", 280.0); number(a("20 million") - 0.2, 2.8, "20,000,000", "Views", "New York Times Opinion")
    S(a("and it helped"), "m_nyt", 354.0, punch=1.0)
    S(a("most powerful coach"), "m_nyt", 102.0, bw=1)
    S(a("her name is"), "m_nyt", 52.0)
    S(a("six years before"), "m_millrose2013", 160.0, slow=0.6)
    S(a("fastest girl america"), "m_nyt", 12.5, punch=0.6)
    # 2 Bronxville -----------------------------------------------------------------------
    S(PART[2] - 0.1, "m_nyt", 58.0, flash=1); chapter(PART[2] + 0.2, "01", "Bronxville")
    S(a("just outside the city"), "m_nyt", 172.0)
    S(a("as a freshman"), "m_freshman2011", 200.0, slow=0.8); number(a("she ran the 1500"), 2.8, "4:17", "National freshman record", "1500m · June 2011")
    S(a("a national record"), "m_armory2012", 30.0)
    S(a("by 16"), "m_millrose2013", 101.0, slow=0.6)
    S(a("olympic trials"), "m_nyt", 132.5, punch=0.5)
    S(a("and thats when"), "m_nyt", 354.0); name(a("a man named"), 3.2, "Alberto Salazar", "Head coach · Nike Oregon Project")
    S(a("salazar was the head"), "m_nyt", 317.0)
    S(a("nike built that"), "m_nyt", 88.0)
    S(a("and he was the guy"), "m_nyt", 90.0)
    S(a("mofera"), "m_nyt", 92.0); title(a("mofera"), 3.6, "Nike Oregon Project", "Mo Farah · Galen Rupp")
    S(a("he started coaching"), "m_nyt", 102.0); date(a("october 2012"), 2.6, "October 2012")
    S(a("still in high school"), "m_armory2012", 95.0)
    # 3 the rise -------------------------------------------------------------------------
    S(PART[3] - 0.1, "m_millrose2013", 53.0, flash=1); chapter(PART[3] + 0.2, "02", "The Rise")
    S(a("january 2013"), "m_millrose2013", 172.0, slow=0.6); title(a("january 2013"), 3.2, "January 2013", "High school indoor mile record")
    S(a("may 2013"), "m_nyt", 42.0, slow=0.8); number(a("she runs the 1500") + 0.4, 3.0, "4:04.62", "American junior record", "1500m · May 2013")
    S(a("american junior"), "m_millrose2013", 140.0, slow=0.6)
    S(a("june at the"), "m_nyt", 156.0); number(a("in the 800") + 0.4, 3.0, "1:59.51", "High school record", "800m · Prefontaine Classic · June 2013")
    S(a("another record"), "m_nyt", 42.5, slow=0.7)
    S(a("that summer"), "m_nyt", 311.5, punch=0.8); title(a("in moscow"), 3.4, "Moscow · August 2013", "World Championships · 1500m")
    S(a("shes 17"), "m_nyt", 312.5); number(a("shes 17"), 2.8, "17", "Years old", "Youngest American ever on a Worlds team")
    S(a("the youngest american"), "m_nyt", 28.0)
    S(a("and she makes the final"), "m_nyt", 313.0)
    S(a("then in november"), "m_nyt", 317.0)
    S(a("no college"), "m_nyt", 330.0, punch=0.4)
    S(a("she signs with nike"), "m_nyt", 338.0)
    S(a("senior in high school"), "m_armory2012", 104.0, bw=1)
    # 4 the deal -------------------------------------------------------------------------
    S(PART[4] - 0.1, "m_nyt", 368.5, flash=1); chapter(PART[4] + 0.2, "03", "The Deal")
    S(a("usa indoor champion"), "m_nyt", 12.0, slow=0.7); title(a("usa indoor champion"), 3.6, "2014", "US indoor champion · World junior champion")
    S(a("on paper"), "m_nyt", 370.0, slow=0.8)
    S(a("but thats not"), "m_nyt", 396.0)
    S(a("in that video"), "m_nyt", 271.0)
    S(a("thinner and thinner"), "m_nyt", 42.5, slow=0.6, bw=1); quote(a("thinner and thinner"), 3.6, "Thinner, and thinner, and thinner.", "Mary Cain")
    S(a("set a number"), "m_nyt", 359.0); number(a("114") - 0.1, 3.0, "114", "Pounds", "The goal weight she says Salazar set")
    S(a("in front of her teammates"), "m_nyt", 88.5, bw=1)
    S(a("birth control"), "m_nyt", 122.5)
    # 5 the body breaks ------------------------------------------------------------------
    S(PART[5] - 0.1, "m_nyt", 158.0, flash=1, bw=1); chapter(PART[5] + 0.2, "04", "The Body Breaks")
    S(a("lost her period"), "m_nyt", 148.0, bw=1); number(a("three years") - 0.3, 2.6, "3", "Years without a period")
    S(a("broke five bones"), "m_nyt", 182.0, bw=1); number(a("five bones"), 2.4, "5", "Broken bones")
    S(a("doctors have a name"), "m_nyt", 174.0); title(a("reds"), 3.6, "RED-S", "Relative Energy Deficiency in Sport")
    S(a("when you dont give"), "m_nyt", 158.5, slow=0.7)
    S(a("your bones get weak"), "m_nyt", 42.0, bw=1, slow=0.6)
    S(a("could not stay healthy"), "m_nyt", 208.0, bw=1)
    S(a("2015 she was"), "m_millrose2013", 219.0, bw=1); number(a("8th"), 2.4, "8th", "USA Championships · 2015")
    S(a("2016 the olympic trials"), "m_nyt", 233.5, bw=1); number(a("11th"), 2.4, "11th", "Olympic Trials · 2016")
    S(a("got darker"), "m_nyt", 212.0, bw=1)
    S(a("in 2016 she leaves"), "m_nyt", 396.0, bw=1)
    S(a("the girl who broke"), "m_nyt", 2.5, bw=1, slow=0.7)
    # 6 the fall of Salazar ---------------------------------------------------------------
    S(PART[6] - 0.1, "m_nyt", 62.0, flash=1, bw=1); chapter(PART[6] + 0.2, "05", "The Fall")
    S(a("then september 30"), "m_nyt", 354.0); date(a("september 30"), 3.2, "September 30, 2019", "USADA bans Salazar 4 years")
    S(a("for doping violations"), "m_nyt", 22.5, bw=1)
    S(a("couple weeks later"), "m_nyt", 317.5); title(a("nike shuts down"), 3.4, "October 2019", "Nike shuts down the Oregon Project")
    S(a("and four weeks"), "m_nyt", 254.5); date(a("mary posts a video"), 2.8, "November 7, 2019")
    S(a("nike said"), "m_nyt", 319.0); quote(a("deeply troubling"), 4.6, "Deeply troubling allegations which have not been raised by Mary or her parents before.", "Nike, November 2019")
    S(a("that she and her parents"), "m_nyt", 62.0)
    S(a("they also said"), "m_nyt", 335.0)
    S(a("salazar denied it"), "m_nyt", 102.5, bw=1)
    S(a("but mary wasnt"), "m_nyt", 82.0); number(a("talked to nine") + 0.2, 2.8, "9", "More former Oregon Project runners", "Sports Illustrated · November 2019")
    S(a("and they backed"), "m_nyt", 88.0)
    # 7 the ban --------------------------------------------------------------------------
    S(PART[7] - 0.1, "m_nyt", 354.5, flash=1); chapter(PART[7] + 0.2, "06", "The Ban")
    S(a("the u s center"), "m_nyt", 317.0, bw=1)
    S(a("banned salazar for life"), "m_nyt", 22.5, bw=1, punch=0.6); title(a("banned salazar for life"), 3.6, "2021 · US Center for SafeSport", "Salazar banned for life")
    S(a("for sexual and emotional"), "m_nyt", 102.0, bw=1)
    S(a("the same year"), "m_nyt", 317.0); number(a("20 million") - 0.2, 2.8, "$20,000,000", "Lawsuit vs. Salazar and Nike", "October 2021")
    S(a("november 2023"), "m_nyt", 330.5); date(a("november 2023"), 3.0, "November 2023", "Settled · terms not disclosed")
    S(a("nobodys saying"), "m_nyt", 2.0)
    # 8 where she is now ----------------------------------------------------------------
    S(PART[8] - 0.1, "m_nyt", 383.0, flash=1); chapter(PART[8] + 0.2, "07", "Now")
    S(a("she started her own team"), "m_nyt", 386.0); title(a("atlanta nyc"), 3.4, "Atalanta NYC", "Founded by Mary Cain")
    S(a("women who run"), "m_nyt", 388.0)
    S(a("mentor young girls"), "m_nyt", 382.0)
    S(a("in 2024"), "m_nyt", 172.5); title(a("running for ireland"), 3.0, "2024", "Now running for Ireland")
    S(a("april 2026"), "m_nyt", 195.0); title(a("this is"), 3.6, "April 2026", "This Is Not About Running")
    S(a("not about running"), "m_nyt", 386.5)
    S(a("and right now"), "m_nyt", 391.0); title(a("medical school"), 3.4, "Today", "Medical student · Stanford University")
    S(a("at stanford"), "m_nyt", 62.0)
    # 9 the end --------------------------------------------------------------------------
    S(PART[9] - 0.1, "m_millrose2013", 160.0, flash=1, slow=0.6)
    S(a("ran a world final"), "m_nyt", 312.5)
    S(a("turned pro"), "m_nyt", 368.5)
    S(a("she never won"), "m_nyt", 396.0, slow=0.8)
    S(a("everybody said"), "m_nyt", 312.0)
    S(a("the coach is banned"), "m_nyt", 102.0, bw=1)
    S(a("the team is gone"), "m_nyt", 92.0, bw=1)
    S(a("watching how"), "m_nyt", 380.5)
    S(a("which one matters more"), "m_nyt", 52.5); quote(a("which one matters more"), 5.5, "The medal she never won, or the video she did make?")
    S(a("let me know"), "m_nyt", 62.5)

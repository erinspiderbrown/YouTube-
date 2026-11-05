# Oscar Pistorius (documentary style, voiceover)

Idea #2 from `ideas/viral_video_ideas_2026-11.md`. Working title: **The Olympic Sprinter Who Shot His Girlfriend Through A Door** (vidIQ 96).

Why this one:
- Oscar Pistorius docs are doing 79K–887K views.
- Your crime story (Robert Howard) did 5.7x your usual views.
- Big true-crime channels already cover it, so this one leads with the track angle: the CAS fight, London 2012, the Paralympic blade outburst.

## Status
- [x] Facts checked (below)
- [x] Script v1: `script_v1.md` (1,298 words, about 8:30 with pauses; about 8,700 characters, roughly 8,500 ElevenLabs credits per take)
- [ ] User approves the script
- [x] Voiceover v1: `oscar-pistorius_voiceover_v1.mp3`, 7:50 at 167 wpm. Word timings are in `vo_v1_words.json`.
  - Recorded in ElevenLabs flow "Oscar Pistorius documentary voiceover" (pPXcfbuQkzpC0Af2Kib8) with the same settings as Drummond v4: eleven_v4, the user's voice, stability 0.45, similarity 0.85.
  - The user's reference is the 01 cold open ("that's perfect"); every other section is held to it.
  - **Take picks:** 01A 02A 03A 04B 05B 06A 07B, chosen by closeness to 01A (pitch, pitch range, spectrum, pace; `voiceover/take_scores.json`) plus a clean read.
    - 05A said "said" for "say".
    - 07A slipped a line.
  - **Pacing:** `tools/space_voiceover.py --target-wpm 168 --min-tempo 0.91 --ref 01_takeA_raw.mp3`.
    - Each section's speaking speed is matched to 01A. Only 05 needed a light 0.936 atempo; the others are untouched.
    - The rest of the time goes into the natural pauses (sentence ends get twice the extra), so there is no stretching and no robotic sound.
    - Then the Drummond warm EQ and -16 LUFS. Sections measure -16.5 to -17.2 LUFS.
  - Spoken change: "Judge Thokozile Masipa" is read as "Judge Masipa" (the full name goes on screen).
- [x] Real footage and photos: 51 clips (AP, Reuters, EWN, SABC, eNCA, Telegraph, Guardian, NYT, Al Jazeera, Olympic/Paralympic channels) and 13 Commons photos. List in `credits.md`. The News Direct CGI re-enactment is excluded.
- [ ] Edit (neon documentary look, `tools/neon.py`) → thumbnail → upload package

## Footage plan (real first, AI only for gaps)
- **London 2012 Olympics:** 400m heat and semi, the Kirani James bib swap, the SA 4x400 final.
- **London 2012 Paralympics:** the 200m T44 final vs Alan Oliveira and the live interview complaint.
- **Earlier career:** Athens 2004 Paralympics 200m.
- **Legal:** the 2008 CAS ruling news.
- **The case:** trial broadcast footage from 2014 (it was televised), the verdict days in 2014, 2015, 2016 and 2017, the January 2024 parole release news.
- **Photos:** Wikimedia Commons photos of Pistorius (and any freely licensed photos of Reeva Steenkamp), credited in the description.
- **Import route:** YouTube broadcast/news uploads come in free through vidIQ, the same as Drummond.

## Facts and sources (checked 5 Nov 2026)
- **Birth and childhood:**
  - Born 1986, Johannesburg, with fibular hemimelia in both legs. Both legs amputated below the knee at about 11 months.
  - His mother Sheila died in March 2002, when he was 15.
  - [Wikipedia](https://en.wikipedia.org/wiki/Oscar_Pistorius), [IOL tribute 2012](https://www.iol.co.za/sport/oscar-pays-tribute-to-late-mom-1356316)
- **Athens 2004:** gold in the 200m T44, bronze in the 100m. [CNN fast facts](https://ktvz.com/news/national-world/cnn-europe-mideast-africa/2021/11/10/oscar-pistorius-fast-facts/)
- **The blade ban:** the IAAF barred him in January 2008 over his blades. CAS overturned it in May 2008 because the IAAF couldn't prove an advantage. Same source.
- **London 2012:** first double-amputee track athlete at the Olympics. Eighth in his 400m semi, and he anchored SA's 4x400 final (8th). Same source.
- **London 2012 Paralympics:** lost the 200m T44 final to Alan Oliveira by 0.07s (21.45), his first 200m loss in nine years. Complained about blade length, then apologised for the timing the next day. [IOL](https://www.iol.co.za/sport/pistorius-cries-foul-after-shock-loss-1374224), [Al Jazeera](https://www.aljazeera.com/amp/sports/2012/9/3/pistorius-apologises-for-outburst-after-loss)
- **The restaurant gun:** in January 2013 a friend's pistol went off under his table at Tasha's, Melrose Arch, with children at the next table. He was convicted on that count with a 3-year suspended sentence. [News24](https://www.news24.com/you/Archive/tashas-shooting-oscar-swears-his-finger-wasnt-on-the-trigger-20170728)
- **14 Feb 2013:**
  - Before dawn, he fired four shots through a locked toilet door in his Pretoria home. Reeva Steenkamp was hit three times.
  - He says he thought she was an intruder and that he broke the door down with a cricket bat (his own account).
  - Charged with murder on 15 Feb. Bail on 22 Feb.
  - [SBS timeline](https://www.sbs.com.au/news/article/timeline-oscar-pistorius-murder-of-reeva-steenkamp/rqtik9obd), [OFM timeline](https://www.ofm.co.za/article/154628/Oscar-Pistorius-timeline)
- **The 2014 trial:**
  - Neighbours heard a woman screaming; he testified the screams were his. He read her Valentine's card in court.
  - [NBC](https://www.nbcnews.com/storyline/pistorius-trial/pistorius-done-testifying-after-reading-reevas-valentines-card-n80626), [HuffPost](https://huffingtonpost.co.uk/entry/oscar-pistorius-trial_b_5153010)
- **First verdict:** on 12 Sep 2014 Judge Masipa found him guilty of culpable homicide, not murder. Sentenced to 5 years on 21 Oct 2014; sent to house arrest 19 Oct 2015. [Al Jazeera](https://www.aljazeera.com/sports/2014/9/12/pistorius-found-guilty-of-culpable-homicide)
- **Murder conviction:**
  - 3 Dec 2015: the Supreme Court of Appeal convicted him of murder (dolus eventualis). Judge Leach said he "gambled with the life" of the victim.
  - [TimesLIVE](https://www.timeslive.co.za/amp/news/south-africa/2015-12-03-supreme-court-of-appeal-finds-oscarpistorius-guilty-of-murder-oscarappeal/), [Mail & Guardian](https://mg.co.za/article/2015-12-03-reeva-steenkamps-murder-finally-catches-up-with-oscar-pistorius/)
- **Sentencing for murder:** 6 Jul 2016, Masipa gave 6 years. [SAnews](https://www.sanews.gov.za/node/31488)
- **Sentence increased:** 24 Nov 2017, the SCA raised it to 13 years 5 months (the 15-year minimum, less time served). [Irish Times](https://www.irishtimes.com/news/world/africa/oscar-pistorius-jail-sentence-more-than-doubled-to-13-years-1.3303911), [Mail & Guardian](https://mg.co.za/article/2017-11-24-sca-increases-oscar-pistoriuss-murder-sentence-to-13-years)
- **Parole:**
  - Denied 31 Mar 2023; granted Nov 2023; released 5 Jan 2024.
  - Parole runs to Dec 2029. Conditions: anger management and gender-based-violence programmes, no alcohol, no media.
  - [TimesLIVE](https://www.timeslive.co.za/news/south-africa/2023-03-31-oscar-pistorius-is-denied-parole/), [ESPN](https://www.espn.com/olympics/story/_/id/39246006/oscar-pistorius-released-prison-parole), [Al Jazeera](https://www.aljazeera.com/news/2024/1/5/oscar-pistorius-released-on-parole-after-serving-nine-years-for-murder)
- **Reeva's family:** her father Barry Steenkamp died in 2023. June Steenkamp said the family are "the ones serving a life sentence." [NBC](https://www.nbcnews.com/news/world/oscar-pistorius-granted-parole-january-murder-reeva-steenkamp-rcna126544), [Yahoo/People](https://uk.news.yahoo.com/ones-serving-life-sentence-says-173759344.html)
- **Left out on purpose:**
  - Tabloid 2026 claims (an alias at Ironman races, a new girlfriend): unverified.
  - Graphic injury details: no need.
  - The "put on your shoes / put on your legs" line is from his own memoir and is phrased as "the way Oscar told it".

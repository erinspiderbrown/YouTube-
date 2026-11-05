# NCAA cross country "takeover" (documentary style, voiceover)

The user's idea (5 Nov 2026): Africans taking over the NCAA, and how one group is mad about it, though only the cross country people. It's a new lane, current college running rather than retro sprint stories.

Working title: **Why Americans Can't Win College Cross Country Anymore** (vidIQ 94).

## Why this one, and why now
- **Deadline:** NCAA DI cross country nationals are on **Sat 21 Nov 2026** at LaVern Gibson, Terre Haute. Publish before that and the race becomes the payoff, with a possible follow-up video after it.
- The full NCAA XC race uploads do 286K–441K views (29–37x).
- Small channels are breaking out on this exact debate:
  - Eamonn Kichuk, "Hidden NCAA Rule Destroying American Distance Runners": 38x.
  - Coach Rob, "NCAA XC Just Got VERY Messy": 65K.
- Nobody has done a story-driven documentary on it. What's out there is podcasts, forum threads and news.
- Fits the channel's pattern: a real controversy, a fall, a twist (the NCAA changed the rules), and real footage everywhere.

## Status
- [x] Research and fact check (below)
- [x] Script v4, final for the build: `script_v4.md`. The user's angle: no rules broken, college is for adults, the online hate (with real comments), and the doping double standard.
- [x] Voiceover v1: `ncaa-xc_voiceover_v1.mp3`, 9:44, word timings in `vo_v1_words.json`.
  - ElevenLabs flow "NCAA XC takeover documentary voiceover" (0w93Ox1Az1tKlFWACLvx): the user's voice dk6cvd5UilZRrcpZ7dNK, eleven_v4, stability 0.45, similarity 0.85, 9 nodes (01–08, with 06 split into 06a/06b).
  - Takes: 01B, 02A, 03B, 04A, 05A, 06aA, 06bB, 07A, 08B. Picked by transcript match; the full script was checked and no lines were skipped.
  - The run cost 22,746 credits and used up the monthly quota (0 left), so some second takes failed. Every section still has one good take.
  - Paced with `tools/space_voiceover.py --target-wpm 166 --min-tempo 0.94 --gap 1.0 --ref 01B`, then the warm EQ.
- [x] Real footage: 13 clips imported through vidIQ. Commons photos and the comment receipts are listed in `credits.md`.
- [x] Edit v1: `ncaa_build.py` + `ncaa_mograph.py`, 9:56. Neon look, real comments on screen (usernames hidden), and the Drummond music bed and SFX.
- [x] Thumbnail v1: `thumbnail.py`, saved as `thumbnail_v1.jpg`. "WHAT RULE?" + the real comment + a Lemngole cut-out (Commons, CC BY-SA 4.0).
- [x] Upload package: `youtube_upload.md`
- [ ] User review of the v1 edit

## Facts and sources
| Claim in script | Source |
|---|---|
| 2025 NCAA XC: Nov 22, Gans Creek, Columbia MO. Men: Habtom Samuel (ERI, New Mexico) 1st, Rocky Hansen (USA) 2nd, Kipchoge (KEN) 3rd, Musau (KEN) 4th, Messaoudi (MAR) 5th, Kipngetich (KEN) 6th. Oklahoma State won with 57 pts. Women: Doris Lemngole (KEN, Alabama) won in 18:25.4, a course and meet record, and Hedengren was 2nd. | [Wikipedia](https://en.wikipedia.org/wiki/2025_NCAA_Division_I_Cross_Country_Championships), [CITIUS](https://citiusmag.com/articles/ncaa-cross-country-championships-2025-recap-analysis) |
| April 1977 T&FN cover: "Foreigners Dominate NCAA" | [Track & Field News](https://trackandfieldnews.com/a-foreign-wave-rises-high-in-the-ncaa/) |
| Henry Rono, Washington State: NCAA XC champion 1976, '77 and '79. Four world records in 81 days in 1978. | [Wikipedia](https://en.wikipedia.org/wiki/Henry_Rono) |
| Kipchoge: 28-year-old freshman at Texas Tech in 2024, ran 59:37 for the half (Lille 2023), then transferred to WSU. 3rd at 2025 NCAAs. Turned 30 in May 2026. | [Canadian Running](https://runningmagazine.ca/the-scene/ncaa-school-faces-backlash-over-28-year-old-kenyan-freshman/), [Deseret](https://www.deseret.com/sports/2025/11/20/nil-changing-the-game-for-colleges-universties/), [CITIUS](https://citiusmag.com/articles/ncaa-cross-country-championships-2025-recap-analysis) |
| 43% of men and 38% of women foreign (LetsRun count). Top three men's teams: 18 of 21 runners foreign, all but one from Africa. Scholarbook pitch to Eyestone. Eyestone quotes ("embarrassed", "I'd take a Kenyan if he was born in the U.S."). | [Deseret](https://www.deseret.com/sports/2025/11/20/nil-changing-the-game-for-colleges-universties/), [EssentiallySports](https://www.essentiallysports.com/olympics-track-and-field-news-former-olympic-medallist-reveals-harsh-ncaa-cross-country-reality-amid-ongoing-foreign-athletes-debate/) |
| Test-score requirement dropped (permanent in 2023), full cost of attendance, roster limits | [EssentiallySports](https://www.essentiallysports.com/olympics-track-and-field-news-former-olympic-medallist-reveals-harsh-ncaa-cross-country-reality-amid-ongoing-foreign-athletes-debate/) |
| Dave Smith: "change the rulebook" or "shut up and coach". Eyestone: "shortcut". | [CITIUS](https://citiusmag.com/articles/ncaa-cross-country-championships-2025-recap-analysis) |
| Fitz Dunkley: same rules, different reaction (missions, COVID year) | [EssentiallySports](https://www.essentiallysports.com/olympics-track-and-field-news-former-olympic-medallist-reveals-harsh-ncaa-cross-country-reality-amid-ongoing-foreign-athletes-debate/) |
| "5-in-5": five years of eligibility, the international clock starts at 19, redshirts and most waivers end | [CITIUS](https://citiusmag.com/articles/ncaa-eligibility-reform-college-track-field), [LetsRun](https://www.letsrun.com/news/2026/07/the-end-of-the-28-year-old-freshman-inside-the-ncaas-new-age-cap/) |
| 2026 Big 12: Hedengren won by 10 seconds over Billah Jepkirui (Oklahoma State) | [Deseret](https://www.deseret.com/sports/2026/11/02/jane-hedengren-byu-women-cross-country-claim-big-12-conference-titles/), [World-Track](https://world-track.org/2026/10/jane-hedengren-byu-2026-big-12-cross-country-championships-results/) |
| 2026 nationals: Nov 21, Terre Haute | [NCAA.com](https://www.ncaa.com/news/cross-country-women/article/2026-07-17/2026-ncaa-cross-country-national-championships-date-time-tv-channel-history) |

### Still to confirm before the voiceover
- **The 5-in-5 vote date** ("summer of 2026", "seven months later"): one source says the DI Cabinet adopted it unanimously on 23 June 2026. LetsRun's piece is from July 2026, but LetsRun blocks this machine, so check the NCAA release.
- **When 5-in-5 takes effect:** sources disagree on fall 2026 versus fall 2027 enrollees. The script says nothing about timing on purpose.
- **The 43%/38% LetsRun count:** Deseret's article ran two days before the 2025 meet, so the count is probably from 2024. The script says "one recent NCAA championship".
- **Left out on purpose:**
  - A reported post by former Trump aide Theodore Wold (one source only, and the post may be deleted).
  - The "97 Kenyans via Scholarbook/Townhall" figure (CITIUS says it's unverified).
  - Kenyan doping statistics, because none of these runners is accused and it would smear them.

## Script v2 (user's direction, 5 Nov 2026): notes and open items
- **Angle:**
  - The African runners broke no rules.
  - College has no age limit, and everyone gets the same eligibility.
  - The athletes are bettering their situation.
  - Online hate from a certain crowd, kept separate from coaches like Eyestone, who argue policy in the open (not hate, and not to be framed as hate).
- **The online-hate section needs real receipts.** No news report documents racist abuse aimed at these runners; Eyestone's "someone will say you're racist" quote is the only race-related line found. The comment quotes in 01 and 05 ("Send 'em home", "go back where they came from") are placeholders until the user supplies real screenshots. Show those on screen with handles blurred, or reword the lines.
  - The user's own wording, "certain white people online", is held back as "a certain crowd online". It goes in only if the screenshots support it, as the user's call.
- **Doping beat (section 06):** this is the exception to "nobody broke rules".
  - Caroline Jeptanui (Tulane) finished 12th at the 2024 NCAAs while provisionally suspended by ADAK since 28 Sep 2024. She wasn't on the AIU or ADAK lists. [LetsRun](https://www.letsrun.com/news/2025/02/tulanes-caroline-jeptanui-finished-12th-at-ncaa-xc-champs-while-suspended-for-an-anti-doping-violation/), [FloTrack](https://www.flotrack.org/articles/13832952-tulane-athlete-earned-all-american-honors-while-allegedly-suspended)
  - TCU scratched Tabitha Ngao from the 2025 NCAA indoor championships over a provisional suspension. [LetsRun](https://www.letsrun.com/news/2025/03/another-kenyan-has-been-competing-in-the-ncaa-while-suspended-tcu-scratched-tabitha-ngao-from-ncaa-championships/)
  - Check the final rulings before recording. Both are named only by school in the script.
- **"Clock starts when you enroll":** true of the old four-in-five rule. Track did charge some seasons for organized competition after a delay following high school (national-team events were exempt), so "start whenever you want" is simplified and not stated outright. It no longer applies to new international athletes under 5-in-5.
- "Agricultural education": Kipchoge's major, per [Canadian Running](https://runningmagazine.ca/the-scene/ncaa-school-faces-backlash-over-28-year-old-kenyan-freshman/).

## Script v3: doping double standard, sources and wording limits
The user is on the African athletes' side and wants targeted testing and US cover-ups covered.
| Claim | Source | Wording kept to |
|---|---|---|
| Kenya is in World Athletics Category A (highest risk) and has been for years. At least 3 no-notice out-of-competition tests in the 10 months before a major championship. Ethiopia and Kenya averaged about 7 OOC tests per athlete before Paris. The US is not Category A. | [World Athletics/AIU](https://worldathletics.org/news/news/aiu-all-athletes-high-risk-countries-eligible-oregon22), [Athletics Africa](https://athletics.africa/news/africa/kenya/athletics-kenya-plans-extensive-testing-tokyo25-20765), [Guardian NG](https://guardian.ng/?p=2825140) | "Test one group more and you catch more" is an argument, not a measured finding, so the script doesn't say *all* of Kenya's positives come from extra testing. |
| Exum files (2003): 30,000+ pages, 100+ US positives from 1988 to 2000, athletes who won 19 Olympic medals. Carl Lewis positive for 3 stimulants at the 1988 Trials, cleared on appeal. | [ESPN](https://www.espn.com/oly/news/2003/0416/1540029.html), [Swimming World](https://swimmingworldmagazine.com/news/usoc-covered-up-over-100-positive-drug-tests-among-us-athletes-former-drug-czar-charges), [Tampa Bay Times](https://www.tampabay.com/archive/2003/05/01/usoc-followed-rules-in-track-doping-case/) | Lewis's denial and the IAAF ruling that the USOC followed its rules are both in the script, so the claim is fair to him. |
| WADA (Aug 2024): USADA let doped athletes keep competing as informants (at least 3 cases from 2011 to 2014). USADA disputes the framing. | [NPR via KPBS](https://www.kpbs.org/news/national/2024/08/08/with-the-summer-olympics-in-full-swing-sports-anti-doping-agencies-escalate-feud), [Capital FM](https://capitalfm.africa/wada-questions-integrity-of-u-s-anti-doping-agency/) | USADA's reason ("catch bigger fish") stays in. |
| Knighton: positive for trenbolone in 2024, cleared (contaminated meat), ran Paris (4th). World Athletics and WADA appealed, and CAS gave a 4-year ban on 12 Sep 2025. | [AP via News4Jax](https://www.news4jax.com/sports/2025/09/12/olympic-sprinter-erriyon-knighton-gets-4-year-ban-for-positive-test-for-anabolic-steroid/), [CITIUS](https://citiusmag.com/articles/erriyon-knighton-banned-cas-doping-violation-2025) | |
| BALCO (Marion Jones, Tim Montgomery) | Covered in earlier channel research | "One of the biggest", not "the most". |

The user's line that Americans are "involved in the most scandals" has no count behind it, so the script says "one of the biggest… was American" and "only one side get the whole country blamed". The one line "Kenya got some" cheaters stays in. It's what makes the double-standard point hard to argue with.

## Footage plan (real first)
- **NCAA Championships YouTube:** full 2024 and 2025 DI men's races (`D5cb8-HwALQ`, `goYXdAHTpXg`) and the women's races. Use the finish, Samuel's win, Hansen 2nd, the OSU pack, and Lemngole's record.
- **FloTrack:** 2025 men's and women's press conferences (`Rry6iCUJzko`, `3Lg_quCyhpc`).
- Henry Rono archival footage from 1978 (search), plus a Commons photo.
- Kipchoge: Lille half 2023, WSU regionals and nationals clips.
- **2026 Big 12 race** (Hedengren vs Jepkirui), Cowboy Jamboree 2026.
- Graphics:
  - The T&FN 1977 cover headline rebuilt as a neon card (don't show the real cover unless licensed).
  - Results board with flags.
  - 43%/38% stat card.
  - "5-in-5" rule card with the clock at 19.
  - Eyestone vs Smith quote cards.
- AI or stock only for gaps (Lubbock and Pullman establishing shots, a Kenyan training camp).

# Titles + thumbnails: what converts (study, 11 Nov 2026)

## The channel's own data (views at 11 Nov)
| Video | Views | Pattern |
|---|---|---|
| I Exposed a Nike Sprinter — Then Everything Changed | 44K | story loop with a twist ("then…") |
| He Wouldn't Leave The Track. So Track Got Rid Of Him | 16K / 6 days | cause → consequence, absurd image |
| Who's Doping In This Photo? (You Picked Wrong) | 11K | a puzzle the viewer plays; red circle + arrow, "IT WAS HIM." |
| 31-Year-Old NCAA Runner QUITS Team… | 11K | one shocking fact |
| America's Fastest High Schooler... What Went Wrong? | 4.4K / 7 hours | user's own thumbnail; best start in weeks |
| The Rise Of Letsile Tebogo… | 2.6K | flat "rise of" + medal portrait: no tension |
| The Fastest Man In College Every Year Since 2016 | 3.9K | info list, 4 faces + 4 years |
| The Olympic Sprinter Who Shot His Girlfriend… | 1.6K | |

Winners: 2-3 words on the thumbnail that open a question, one strange or tense moment, sometimes receipts (articles, a stamp).
Losers: portraits, medals, lists of years, nothing to solve.

## Outside the niche (same story shape: hyped young athlete → paid → never delivered)
- "The Worst Draft Pick in NFL History" (UrinatingTree) 1.25M — thumbnail "TOTAL PLAYS IN NFL: 4", hyped photo vs. on his knees. **One brutal number.**
- "How 1 Deal Destroyed England's Biggest Rapper's Legacy" 290K — brand logo + serious face + money. **Brand + face + deal.**
- "Meet The Biggest BUST In NFL History" 257K / 1 month — face surrounded by the insults people called him.
- "What HAPPENED to these Viral High School Hoopers?" 718K; Jumpman "What Happened To Every Teen Prodigy Called The 'Next Usain Bolt'?" 455K (face replaced by "?").
- The two existing Candace Hill videos (Track and Field Nation 59K, Jumpman 41K) used smiling photos + "What happened to…" — no tension.

## Rules going forward
1. Thumbnail text ≠ title. Thumbnail = the hook in 2-4 words or one number; title = the story/twist.
2. One number or one contrast beats information. Before (peak, colour) vs. after (B&W).
3. Use the brand when money is the story (ASICS, Nike logo from real footage).
4. Receipts work on this channel (articles with a red box, stamps).
5. Avoid "The Rise Of…", "Where Are They Now", plain topic titles. Prefer "X. Then Y." / "… — Then Everything Changed".
6. Upload with YouTube Studio "Test & compare" (up to 3 thumbnails) and let YouTube pick.
Tools: `tools/thumb_number.py` (one-number before/after), `tools/thumb_downfall.py`, `tools/thumb_template.py`.

## Result, 12 Nov 2026
- Boling, with the user's own house-style thumbnail (action cutout + big face + "WHAT HAPPENED?") and title "America's Fastest High Schooler... What Went Wrong?": **20,000 views on day 1**, the channel's best start.
- Candace's "SHE FINESSED ASICS?" (downfall style) did less. **Default to the house style (tools/thumb_template.py)** for "what happened to…" stories; use downfall/number styles as Test & compare variants.

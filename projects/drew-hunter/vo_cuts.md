# Voiceover cleanup: Drew Hunter

Raw take: `2220 W Mission Ln 7.m4a` (user's Dropbox), 407.9 s → `vo_clean.wav` 364.2 s. Script: `clean_voiceover.py`.

## Removed
| raw time | what | why |
|---|---|---|
| 0–3.3 | "Mmm." | lead-in |
| 80.97–86.33 | first "when Allen Webb was a freshman in high school" | user repeated the line; the clean second read is kept |
| 243.80–247.21 | first "He had to pull off the world championships." | user restarted it with "in 2019"; second read kept |
| 32 silences | every quiet run over 0.75 s (between words, mid-sentence or inside a stretched word) cut to 0.6 s | cut inside measured silence (noise floor + 12 dB), 12 ms fades |

No tempo change; the user's pace is kept. Kept on purpose: ad-libs ("quote unquote", "but as of right now, or yet at least").

## Checks
Re-transcribed the cleaned file (medium.en) → `words.json`. Both repeats gone; every number came back whole:
2016, 8 minutes, 13:36, 7:59, 3:58, 50 meters, 4 minutes, July 2016, 10-year, 18, February 2019, 8:25, 2019, 2024, 10,000, 2025, 13:14, 29, 2028.
Read note: the user said "January 16th" for "January 2016" (the 7:59 was 30 Jan 2016). Cover with a "JAN 2016" date graphic.

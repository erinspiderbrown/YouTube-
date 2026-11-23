# Voiceover cleanup: IShowSpeed 10.35

Raw take: `2220 W Mission Ln 6.m4a` (the user's Dropbox), 346.9 s → cleaned `vo_clean.wav`, 327.5 s. Script: `clean_voiceover.py`.

## Removed
| raw time | what | why |
|---|---|---|
| 51.02–54.02 | false start "Ato Boldon … since –" | the user restarted the line; the clean second read is kept |
| 14.38–14.88 | "goddamn" | ad-friendly; the sentence reads clean without it |
| 328.95–329.31 | "ass" | ad-friendly |
| 8 long pauses (6.5 s in all) | silences over 1.0 s shortened to 0.4 s | `pause_cuts(min_gap=1.0, keep=0.4)`; every cut sits inside measured silence |

Lead-in silence trimmed (start 8.22 s). No tempo change, no word stretched: the user's own pace is kept.
Kept on purpose: the user's ad-libs ("I'm tripping, this year", "and it was fake, everybody knew it was fake"), "pissed" in Speed's soundbite.

## Chain
highpass 75 Hz → afftdn (light noise reduction) → de-esser → gentle compressor (2.5:1) → small EQ (−1.5 dB 180 Hz, +1.5 dB 3.5 kHz) → loudnorm −16 LUFS, 12 ms fades on every join.

## Checks
- Re-transcribed the cleaned file (medium.en) → `words.json`; every number in the read came back whole: 10.35, 10.3, 10.5, 70%, 10.7, 10.8, 10.2, 10.6, 186 million, 50, 12 flat, 19.67, 200, 20.6, 2028, 5.
- Soundbite splits use `gap_point()` and each one was checked to land in measured silence (≤ −59 dB) between two words.

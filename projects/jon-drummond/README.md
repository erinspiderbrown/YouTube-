# Jon Drummond (documentary style, voiceover)

Voiceover generated in ElevenLabs (flow "Jon Drummond documentary voiceover", EwtCtvyEoktyTmEPgx7r) with the user's own cloned voice (voice id dk6cvd5UilZRrcpZ7dNK), model eleven_v4, style tags "[relaxed] [laid back] [Texas accent]".

## CURRENT: v3 voiceover (approved style, 5 Nov 2026)
- `jon-drummond_voiceover_v3.mp3`: full track, 8:33, about 165 wpm, -16 LUFS.
- `voiceover_v3/*_takeA_raw.mp3`: straight from ElevenLabs. `*_paced.mp3`: timed to 166 wpm with rubberband (pitch and formant preserved) and loudness-normalised.
  - Section 5 is wordier, so its sentence pauses were lengthened by about 0.26 s instead of stretched harder.
- Script: `script_v3.md`. Every paragraph uses `[calm] [relaxed] [Texas accent]`, with no whisper/low-voice/suspense tags and no CAPS. Slang throughout, nothing proper.
- ElevenLabs voice_settings: stability 0.75, similarity 0.9. Take B of every section is in ElevenLabs as an alternate (flow nodes labelled "V3 0x").
- User's pace preference: about **165–170 wpm**. 159 is too slow, 176 too fast. Calm read, not enthusiastic.
- Re-pace tool: `python3 -I tools/pace_voiceover.py --target-wpm 166 --out FULL.mp3 <raw sections>`.

## Older versions
v1 (below) was too excited and too fast. v2 (`voiceover_v2/`, `script_v2_chill.md`) was too quiet and drifted into sounding like AI.

## Audio in this folder (v1)
- `jon-drummond_full-voiceover.mp3`: all 7 sections (take A), joined with 0.7 s gaps. 7:41.
- `voiceover/`: every section, both takes (A/B), from the final batch (4 Nov 2026, 20:07–20:08 UTC):

| # | Section | Starts with | ~Length |
|---|---|---|---|
| 01 | Cold open | "Aight, so check it. You see this man right here?" | 0:56 |
| 02 | Background | "Aight… so before we get to Paris…" | 0:41 |
| 03 | Sydney 2000 | "Sydney, 2000. Olympic final, 4 by 1." | 1:09 |
| 04 | Rule change & Paris 2003 | "So under the old false start rule…" | 1:02 |
| 05 | Aftermath & take | "And when he finally walks off?…" ends "…It was just halftime." | 1:15 |
| 06 | Coaching & the ban | "Once his runnin' career wound down…" | 1:34 |
| 07 | Hall of Fame & ending | "And here go the part that make this whole thing feel scripted…" ends "…the sport let go of him." | 1:00 |

Earlier drafts that are still in the ElevenLabs flow: a 3-section version (19:56) and the dramatic and Multilingual v2 tests.
The flow also has music beds M1–M5 (dark cinematic, 65–140 s) and 7 SFX (record scratch, sub-boom, whoosh, starting gun, crowd roar, rubber stamp, newspaper rip). They aren't downloaded yet.

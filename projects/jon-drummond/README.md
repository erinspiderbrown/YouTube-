# Jon Drummond (documentary style, voiceover)

Voiceover generated in ElevenLabs (flow "Jon Drummond documentary voiceover", EwtCtvyEoktyTmEPgx7r) with the user's own cloned voice (voice id dk6cvd5UilZRrcpZ7dNK), model eleven_v4, style tags "[relaxed] [laid back] [Texas accent]".

## Video build (documentary style)
- `jd_build.py`: shot list (78 shots, keyed to voiceover times), HUD keywords, SFX cues and music placement. Stages: shots, transitions, compose, audio, mux.
- `jd_mograph.py`: 29 graphics:
  - subject file, delay clock, case stamp, title, Philly→Odessa→TCU route map, medal timeline
  - Sydney team, medal stand, emails counter, rep card, false-start rule explainer, Paris map, FALSE START
  - fallout timeline, 2010 one-and-done / Bolt, London 2012, Tyson Gay tests, ruling, 8-year sanction
  - same-year split, "now" card, chapter cards, quote cards, end line
- B-roll:
  - 7 AI clips from the user's ElevenLabs shot list (ltx-v2-fast, 6 s each: S01, S03–S08). ElevenLabs credits ran out before S09–S32.
  - Free Pexels stock reused from Montverde (blocks, sprinters, stopwatch, lab, gavel, documents, newspapers, lightning, laptop).
- Music: the user's ElevenLabs tracks M1–M5, placed per section and ducked under the voice. SFX: the user's 7 ElevenLabs effects plus synthesized transition and HUD sounds.
- Not used yet: the 2 REAL clips (Paris 2003 protest, 1996 Trials). They're uploaded assets in ElevenLabs with no download URL via the connector. The user can send YouTube links to pull them in via vidIQ import.

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

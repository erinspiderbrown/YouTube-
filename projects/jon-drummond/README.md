# Jon Drummond (documentary style, voiceover)

Voiceover generated in ElevenLabs (flow "Jon Drummond documentary voiceover", EwtCtvyEoktyTmEPgx7r) with the user's own cloned voice (voice id dk6cvd5UilZRrcpZ7dNK), model eleven_v4, style tags "[relaxed] [laid back] [Texas accent]".

## CURRENT VOICE: v4 voiceover (5 Nov 2026)
- The user says v3/v3b still sounds robotic, mostly toward the end, and wants it consistent from start to finish. Some words are mispronounced.
- `script_v4.md`:
  - No IPA.
  - "Drummund" spelling, every, his self.
  - Same settings for every section: stability 0.45, similarity 0.85.
- ElevenLabs nodes "V4 01" to "V4 07 (natural, consistent)" in flow EwtCtvyEoktyTmEPgx7r are ready to run.
- Cost: 19,350 credits for 2 takes each (≈9,700 for one). The account has 125 credits left of a 161,000 monthly quota.
- Done: all 7 nodes run with 2 takes each, 19,350 credits.
  - Takes picked by transcript match: 01B, 02A, 03A, 04A, 05A, 06A, 07A.
  - Placed on the v3 timeline with rephrase_voiceover (0.95 tempo, up to 1.08 to fit), then the warm EQ.
  - Speech level is within 0.8 dB across all sections. File: `jon-drummond_voiceover_v4.mp3`.
- Steps used:
  1. Run all 7 nodes.
  2. Pick the better take per section.
  3. Run `tools/rephrase_voiceover.py` against `vo_v3_words.json` so the edit stays in sync.
  4. Apply the warm EQ chain, then run `jd_build.py audio mux` and encode.

## CURRENT: video v2 (neon + real footage, 5 Nov 2026)
User feedback on v1:
- Liked the editing direction, the sounds and their voice. The music bed helps mask the AI artifacts in the voice, so it stays.
- Wanted it **more futuristic: "neon and it should pop."**
- Wanted their real Dropbox footage of Drummond lying on the track in the cold open.
- Wanted real pictures of the relay members, and **every real photo and real video that can be pulled from the internet**.

What v2 does:
- `jd_build.py`: 127 shots. Shot kinds:
  - `a`: archival full-bleed
  - `f`: archival framed in neon over a blurred backdrop
  - `p`: Commons photo card with name tag
  - `g`: graphic
  - `v`: stock/AI
- Every archival shot carries an `ARCHIVE // PLACE · YEAR` tag.
- Real footage (scratchpad `real/`, sources in `credits.md`):
  - User's Dropbox Paris 2003 protest and 1996 Trials.
  - France 2 broadcast of the protest.
  - NBC and France TV Sydney 2000 relay, with the USA lineup lower third and Greene's tongue-out.
  - Stuttgart '93 world record, Atlanta '96, Bolt's Daegu 2011 false start, London 2012 women's world record, PBS on Tyson Gay.
- Real photos (Wikimedia Commons, credits in `credits.md`):
  - Team card: Drummond, Williams, Greene, plus a Brian Lewis frame from the '96 Trials. Each pops in as the voiceover says the name.
  - Kissinger on the medal stand.
  - Michael Johnson on the quote card.
  - Wilt, Overbrook, West Philly, Odessa College, TCU, Paris 2003, London 2012, Tyson Gay, USADA.
- Neon look (`tools/neon.py`):
  - Graphics: synthwave floor grid, HUD corners and bloom.
  - HUD keywords: cyan brackets with coloured glow (`hud.render(..., neon=True)`).
  - Transitions alternate orange and cyan glow.
  - Stock gets a punchier teal/orange grade.
- Most AI clips were replaced by real footage. Music, SFX and voiceover are unchanged from v1.
- Output: scratchpad `output/jon-drummond_v2_master.mp4` (+ 720p preview and ~200 MB 1080p).

## Video build v1 (documentary style)
- `jd_build.py` (v1 version in git history): shot list (78 shots, keyed to voiceover times), HUD keywords, SFX cues and music placement. Stages: shots, transitions, compose, audio, mux.
- `jd_mograph.py`: 29 graphics:
  - subject file, delay clock, case stamp, title, Philly→Odessa→TCU route map, medal timeline
  - Sydney team, medal stand, emails counter, rep card, false-start rule explainer, Paris map, FALSE START
  - fallout timeline, 2010 one-and-done / Bolt, London 2012, Tyson Gay tests, ruling, 8-year sanction
  - same-year split, "now" card, chapter cards, quote cards, end line
- B-roll:
  - 7 AI clips from the user's ElevenLabs shot list (ltx-v2-fast, 6 s each: S01, S03–S08). ElevenLabs credits ran out before S09–S32.
  - Free Pexels stock reused from Montverde (blocks, sprinters, stopwatch, lab, gavel, documents, newspapers, lightning, laptop).
- Music: the user's ElevenLabs tracks M1–M5, placed per section and ducked under the voice. SFX: the user's 7 ElevenLabs effects plus synthesized transition and HUD sounds.
- v1 did not use the 2 REAL clips (Paris 2003 protest, 1996 Trials). v2 pulls them from the user's Dropbox (`/Issam Coach/JD VUDEO/`).

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

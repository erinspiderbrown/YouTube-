# The Boling edit: the approved documentary style (user, 10 Nov 2026)

"The production level of this video was probably the highest that I've seen you do, from finding the clips,
inserting them, the photos, the news clips, all of the above. Save this style of editing for future videos."
Video: https://youtu.be/kPf1d0eAMrE (v2, 9:28). Build: `boling_build.py` (copy it for the next project).

## 1. Voiceover (user reads it)
- Clean with `clean_voiceover.py`: highpass, denoise, gentle compression, EQ, loudnorm -16. Long pauses go down to about 0.65 s. No tempo change.
- **Cut every flub.** Whisper hides restarts, so check three ways:
  1. a verbatim re-transcribe with a disfluent prompt
  2. each pause-separated chunk transcribed on its own
  3. the waveform energy
  
  Put each flubbed take in `MIST` (snapped to silences), then re-time the words with `retime_words.py`. Re-listen to every cut point by transcribing that window again.

## 2. Footage
- Import everything through vidIQ (free):
  - race broadcasts (NCAA, SEC, World Athletics, NBC)
  - fan race videos (never FloTrack or MileSplit footage: user rule, 11 Nov 2026)
  - local and national news (CBS, KHOU)
  - documentary shorts about the athlete (Park Stories)
  - the athlete's own vlogs
  - Wikimedia Commons photos via the Composio workbench
- Make a 6x5 contact sheet per clip with timestamps, then zoom sheets on the key moments (the athlete's leg, the finish, the scoreboard).
- Transcribe every clip with faster-whisper to find quotable soundbites.
- If a race has no footage, say so in the delivery note and use a stat graphic over related footage. Never show a race the athlete isn't in as if he were.

## 3. Soundbites (what gives it its length and weight)
- About 15 real moments where the clip plays with its own sound and the voiceover pauses (`SB_LIST`, anchored by phrase within its part). Use these:
  - **Cold open:** the most emotional one (his dad: "...it goes 9.98, I'm just like, oh my God").
  - **News:** proof the hype was real (the CBS report).
  - **Live race calls:** the big moments ("Here comes Boling... the stadium is going crazy", "He will not be denied").
  - **People close to him:** dad and coaches for the human side ("only three men in the US will make that team").
  - **The athlete himself:** ambition, then reality ("I'm not going to stop until I reach to be the best").
  - **Irony after the low point:** his dad, "If he says he's going to the Olympics, I'm buying a ticket... do not doubt this kid", right after NO PARIS.
- Each soundbite shows its source credit and is loudness-matched to -17 LUFS.

## 4. Picture
- **Graphics:** `tools/kinetic.py`, animated, never static boxes:
  - `stat`: the number rolls, slams in, a colour bar wipes and the label types on
  - `words`: kinetic words, one after another
  - `stack`, `name` (lower third), `stamp`
  - `chapter` slate at each part ("01 THE HYPE WAS REAL", "02 GEORGIA", ...)
  - `endq`: the closing question
- **Editing:**
  - punch-in (+13% in 0.12 s) on every number
  - black-and-white + red graphics on setbacks (14th, 9th, 6th, 8th, NO PARIS)
  - slow-mo 0.5x on finishes and flashbacks
  - a white flash cut on each chapter start
  - a small source credit bottom-right for the first 3.5 s of each shot
- Footage grade: contrast 1.07, saturation 1.1, light vignette; slow 3.5% push-in on every shot.

## 5. Sound
- A dark bed per chapter (`projects/jon-drummond/music`), sidechain-ducked under voice + soundbites.
- Race clips keep their crowd sound low (0.16).
- SFX: about 30 in a 9.5-minute video, only on chapters, stamps, stats and the end question, varied kinds. At least 6 s between stat hits and 3 s between any two hits. Nothing on plain cuts.

## 6. Article receipts (added on Candace Hill, 11 Nov 2026)
- Screenshot the real news articles with Playwright, wrapping the key line in a red outline box
  (`projects/candace-hill/art2.js`), then turn each into a 12 s push-in toward the box (zoompan; see the
  `art_*.mp4` step in the Candace notes). Use them as shots with the outlet + date as the source credit.
- Check every number against the broadcast's own results board, not only Wikipedia (Wikipedia said 8th in the
  2021 Trials final; NBC's board showed 9th of 9).

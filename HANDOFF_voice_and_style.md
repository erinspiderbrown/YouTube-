# Handoff: approved voice + documentary editing style (from "YouTube video editor", 24 Nov 2026)

The user asked for the approved ElevenLabs voice and the documentary editing style to be used on their other YouTube channel (the GTA 6 videos). Everything below is what is approved and in use on The Erin Brown channel as of 24 Nov 2026. The track-specific footage rules don't carry over (see the end).

Source repo: `erinspiderbrown/YouTube-`, branch `claude/laughing-hopper-6b0xlg`. Reusable files: `tools/modern.py`, `tools/match_rhythm.py`, `tools/safe_cuts.py`, `tools/make_captions.py`, and the latest full build `projects/shelby-houlihan/shelby_build.py` + `edl_shelby.py` (copy them as a template).

---

## 1. The voice: "Erin Brown 2026" (current default, approved 22 Nov 2026)

- **ElevenLabs Instant Voice Clone on the user's own account.** voice_id `uBqzFhqGLj9GteaUaPDl`. Made from about 28 min of the user's own reads.
- **Access:** the user's Composio `elevenlabs` connection is their own account. The ElevenLabs MCP (`creative_add_flow_node`, tts) works too.
- **Settings:** model `eleven_v4`, voice_settings `{"stability": 0.3, "similarity": 0.9}`. The key is `similarity`, not `similarity_boost`; read the node back before running.
- **No style tags.** Don't use `[calm]`, `[relaxed]` or `[Texas accent]`. The user said the old takes were "too slow and chill" and "too proper".
- **Pace:** never slow the words.
  - Run `tools/match_rhythm.py IN.mp3 OUT.mp3`. It only lengthens existing pauses toward about 0.7 s.
  - The user's real reads measure about 120 wpm, about 19 pauses per 100 words, median pause 0.70 s.
  - Don't use `space_voiceover.py` or any tempo change.
- **Spell the script how the user talks.** TTS reads the spelling, so:
  - "da" for the, "dis/dat/dese/dey/dem", "wit".
  - Drop the g ("runnin'", "winnin'").
  - Drop plural/possessive s where they would ("Nico Young little brother").
  - "ain't", "gon'", "'cause", "y'all", "tryna", "somethin'", "a lotta".
  - Dates with ordinals ("June 24th").
- **Openers and phrases:**
  - No "Man," or "Aight" warm-up openers; get straight into it.
  - Say "I ain't gon' hold you", never "I ain't gon' sugarcoat it".
- **Script voice:** like the user talking to camera, not AI.
  - Full run-on sentences, their own opinions ("I really feel like", "honestly I think"), side comments.
  - Avoid "here's what's on the line", "and that's not all", "so here it is".
  - No stacked one-line dramatic fragments, no rule-of-three lists, no date-place opener stacks, no same opener/closer every video.
  - No strong profanity (keeps it ad-friendly).
- **When the user reads it themselves (shorter videos):**
  - Give them a teleprompter Artifact (big text, one section per screen, "Part 1, 2…").
  - Clean their recording: noise reduction, levels, cut flubs and repeats inside measured silence (`tools/safe_cuts.py`).
  - Keep their natural pace; no tempo change.
  - Mute strong profanity.
- **Music:** keep a dark bed under the voice. It also masks AI artifacts in the clone.
- **Quality checks:**
  - Never clip a word, especially years and numbers.
  - Re-transcribe the final VO and check that every number in the script comes back whole.
  - Test about 25 s and let the user pick before a full record in a new style.

## 2. Editing style: modern cinematic documentary (current, from 17 Nov 2026)

The user approved the Boling v2 structure (10 Nov) and later asked for a modern, high-quality look. Both parts are combined below and used on the Twins, Shelby, Nationals and IShowSpeed videos.

**Look:** a current Netflix/Apple sports doc. New, crisp and sharp.
- **Not** an old-film look: no grain, no vintage textures.
- **No "slap stickers":** no orange/white kinetic words, stamps or slamming stat boxes, no neon stat boxes.

**Structure**
- Vary the structure every video so it doesn't feel repetitive.
- **Cold open** on the strongest real moment.
- Chapters with a clean chapter card.
- Length: **at least 8 minutes.** Get it from real soundbites or extra script sections, never by slowing or padding the voice.

**Soundbites (the backbone)**
- About 15 per 6 min of voiceover: real clips play **with their own sound while the voiceover pauses**. Use news segments, live calls, interviews, the person in their own words, and reactions.
- Split the VO only in measured silence (`gap_point()`: the quietest 80 ms near the phrase start; never cut mid-word).
- Loudness-match soundbites to -17 LUFS.
- Show a small source credit bottom-right on each.

**Footage hunt**
- Import YouTube clips with vidIQ `vidiq_video_upload` (url). It's free, up to 299 MB; then poll `vidiq_job_poll` and curl the `videoUrl`. Direct yt-dlp gets 403 from this machine.
- Make contact sheets to pick moments, and transcribe every clip (faster-whisper) to find the soundbites.
- Prefer real footage over AI/stock, which only fills gaps.

**Graphics:** `tools/modern.py`
- Clean Inter type, mostly white with soft shadows, small tracked-caps kickers, big light-weight numerals, thin rules.
- One sparing red accent `(226,72,58)`, never a box.
- Everything eases in (fade + small drift + blur-to-sharp) and eases out; nothing slams, shakes or flashes.
- Kinds: `date`, `title`, `number`, `name` (lower third), `quote`, `chapter`, `source`, `label` (motion-tracked style callout), `board`.
- Each one is rendered to a .mov with alpha and overlaid with ffmpeg.

**Picture**
- Crisp clean grade, light vignette, slow push-in on stills (3D-parallax feel on photos).
- Punch-in on key numbers or words.
- Black-and-white on low points.
- Slow-mo / smooth speed ramps on big moments and flashbacks.
- Modern transitions.
- Cuts every 2–5 s.

**Sound**
- A dark, suspenseful bed per chapter, sidechain-ducked under voice and soundbites. Never upbeat.
- Very few SFX, varied, never back to back: at least 6 s between "stat" hits, 3 s between any two hits, none on plain cuts.
- Final mix about -16 LUFS.

**Thumbnails and titles that performed**
- Titles: short and simple. The best format: "___ Ever... What Went Wrong?" plus a curiosity question.
- Thumbnails: one sharp, bright, real photo, a big face, and a 2-line cream condensed question beside it.

**Posting**
- **YouTube:**
  - Every scheduled video goes public at **6:00 AM Mountain** (13:00 UTC in winter).
  - Upload with vidIQ (`vidiq_social_post_draft_create` → `vidiq_social_post_publish`; `publishAt` for scheduling), or with Upload-Post.
  - Captions: an .srt from `tools/make_captions.py`, uploaded with Composio `YOUTUBE_UPLOAD_CAPTION_TRACK`.
  - Monetization can't be set by any API. Remind the user to check the Monetization tab.
- **TikTok:**
  - Make a vertical version: a blurred, darkened copy filling the frame, with the 16:9 video centred.
  - Overlay a high-quality cover on the first 1.2 s.
  - Caption starts with `#5MinutePlus`.
- **No second confirmation:** once the user says "post", draft, check and publish.
- The track channel's Facebook Page (E.Diamondz) and its YouTube channel IDs belong to the track channel. Ask which accounts the GTA channel uses.

## 3. What does NOT carry over

These are track-specific: the footage bans (NCAA/ESPN/NBC/Olympic/Diamond League/FloTrack/RunnerSpace), Wikimedia athlete photos, and race-footage preferences. For GTA 6, the matching concern is Content ID: prefer fan or creator footage and short clips, and ask the user which trailer or gameplay sources are safe to use.

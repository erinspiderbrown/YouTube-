# YouTube editing project

This repo is for editing the user's YouTube videos. Read this before any editing work.

## Two video formats

Every video is one of these two. Ask which one if it isn't clear.

### 1. Podcast style (user on screen)
- The user is on camera, talking.
- Footage comes from the user.
- Editing work is mainly on-camera footage: cuts, pacing, punch-ins and the like.
- On top of the on-camera footage, the user also wants:
  - **B-roll / relevant content found online** that matches what's being said.
  - **On-screen graphics and motion elements** to keep viewers engaged.
  - **Sound effects** that add energy **without distracting** from the talking.
- **Storytelling:** cut back and forth between the podcast and B-roll that shows exactly what's being talked about.
  - Host sets something up → cut to the footage as proof → back to the host for the reaction or explanation.
  - Consider a cold open on the most striking B-roll before showing the podcast set.
- References (breakdowns in `examples/podcast/`):
  - https://youtu.be/9H7itfichRg: intro editing (first ~30 sec). Punch-ins, keyword pop-ups, whooshes and pops.
  - https://youtu.be/A0t7WdoAUtM: storytelling and B-roll intercutting, kinetic text bars, music ducked or cut under B-roll.
- Accent colour in use: **orange (#FF7A1A)** with dark/white text bars. The user said "orange screen graphics"; still confirm whether they meant orange or just on-screen graphics.
- **Music:** the user disliked the upbeat lo-fi bed but asked for a **dark, mysterious, suspenseful** bed, low under the voice. Default to that for this kind of content; never upbeat.
- **Style:** the user wants a **futuristic** look (HUD keywords, digital transitions, varied transition sounds). Flat orange text bars read as "beginner" to them.
- Editing pipeline: `tools/` (transcribe, face-tracked framing, graphics). Example project: `projects/montverde/`.

### 2. Documentary style (voiceover, user not on screen)
- The user reads a script as a voiceover. They do not appear on camera.
- B-roll comes from two places:
  - Footage the user provides.
  - Footage Claude finds or makes.
- **The user says exactly what they want.** Follow their shot-by-shot directions. Don't make up creative choices they didn't ask for. If a direction is unclear, ask.
- **Real over generated:** the user wants every real photo and real video of the people and events that can be found online, especially real footage of the moment the voiceover describes.
  - Photos: Wikimedia Commons, with credits in the description. Commons rate-limits this machine's IP, so fetch through the Composio workbench.
  - Video: YouTube links imported via vidIQ, plus the user's Dropbox clips.
  - AI or stock clips only fill gaps.
- **Look:** futuristic **neon that pops**: glow/bloom, cyan + orange neon, HUD tags on archival footage, neon-framed photo cards. See `tools/neon.py` and `projects/jon-drummond/`.
- Keep the music bed under the voice: it masks AI artifacts in the cloned voice.

## The user's voice: use this for ALL YouTube and TikTok voiceovers
The user approved this exact setup ("test 3", Nov 2026, the NCAA 100m champions video). Don't switch back to anything proper-sounding; they reject it every time.
- **ElevenLabs:** voice `dk6cvd5UilZRrcpZ7dNK` (Erin Brown), model `eleven_v4`, voice_settings **stability 0.25, similarity 0.8**. Pass the voice as `voice_id`, not `voice`.
- **Tags at the start of every paragraph:** `[tellin' a story on the block] [nasal voice] [Texas street accent] [relaxed, not proper]`. For a death or tribute, swap the first tag for `[quiet, respectful]` and keep the rest.
- **Write the script how the user talks, not proper English.** Urban, Texas, casual: "Ten dudes." "One of 'em banned 'til twenty twenty-nine." "He go pro, and two years later he world champ." "Where they at now." Drop extra verbs ("he twenty-three", "this America"), use "ain't", "gon'", "tryna", "somethin'", "'cause", "a lotta". Facts stay exactly right.
- **Pronunciation and spelling for the voice:**
  - Kenya / Kenyan: write **Kinya / Kinyan / Kinyans** (user says "Kin-yan", Texas). Stretch those words a little (`tools/slow_words.py`, factor 0.88).
  - Years and times as words: "twenty sixteen", "nine eight-two", "nineteen seventy-three", "twenty-oh-six".
  - "N C double-A", "L S U", "U S A" spelled with spaces.
  - Letsile Tebogo: write **Let-see-lay Tuhbowho** (user: first name "Let see lay"; last name "Tuh bow ho" said fast, run together).
- **Energy:** chill, not hype. The user said the Tebogo take was "too enthusiastic". Add `[chill, not hype]` to the tags, and keep lines plain street talk (no narrator phrasing like "a village about an hour outside the capital").
- **Pace:** `tools/space_voiceover.py --tempo-scale 0.93 --target-wpm 148 --min-tempo 0.9 --max-extra 1.2 --gap 1.3`. The user said the first takes were too fast; this is the approved speed.
- Before a full re-record of a new style, test ~25 s first and let the user pick.

## Scheduling uploads
- The user wants every scheduled video to go public at **11:00 AM Mountain** (18:00 UTC in winter), not 6 AM. Keep the date they give.
- **Schedule through Upload-Post** (Composio toolkit `upload_post`, profile `default`, YouTube channel The Erin Brown connected). It has its own YouTube quota. `UPLOAD_POST_SCHEDULE_POST` with `content_type: video`, `platforms: ["youtube"]`, `video` = a public MP4 URL (Higgsfield `media_upload` gives one), `scheduled_date` in UTC. It posts publicly at that time; set thumbnail/category/tags afterwards with Composio YouTube (those calls don't use the upload quota).
- Composio's own YouTube upload (`YOUTUBE_MULTIPART_UPLOAD_VIDEO`) shares a daily upload quota that is usually used up; don't rely on it.

## Reference examples
- `examples/podcast/`: example videos/clips for podcast style.
- `examples/documentary/`: example videos/clips for documentary style.
- `examples/links.md`: YouTube links and notes on what to study in each one.

**Getting YouTube videos in:** the user can just paste a YouTube link.
- Use the vidIQ tool `vidiq_video_upload` with `url` set to the link. It downloads on vidIQ's servers, costs 0 credits, and handles up to 299 MB.
- Poll `vidiq_job_poll`, then `curl` the returned `videoUrl` into the scratchpad.
- Direct yt-dlp/youtube-dl from this cloud machine gets 403 from YouTube. Don't try to work around that.
- Other sources: the user's Dropbox (connected through Composio) or files they upload.

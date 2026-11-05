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

## Reference examples
- `examples/podcast/`: example videos/clips for podcast style.
- `examples/documentary/`: example videos/clips for documentary style.
- `examples/links.md`: YouTube links and notes on what to study in each one.

**Getting YouTube videos in:** the user can just paste a YouTube link.
- Use the vidIQ tool `vidiq_video_upload` with `url` set to the link. It downloads on vidIQ's servers, costs 0 credits, and handles up to 299 MB.
- Poll `vidiq_job_poll`, then `curl` the returned `videoUrl` into the scratchpad.
- Direct yt-dlp/youtube-dl from this cloud machine gets 403 from YouTube. Don't try to work around that.
- Other sources: the user's Dropbox (connected through Composio) or files they upload.

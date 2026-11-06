# Handoff: where things stand (updated 6 Nov 2026)

To continue in a new chat:
1. Open the repo `erinspiderbrown/YouTube-` on branch **`claude/blissful-euler-adwpg2`**.
2. Say: "Read HANDOFF.md, CLAUDE.md and projects/oscar-pistorius/README.md, then continue."

Everything below is committed on that branch, except large media, which lives on the session's machine and is listed with how to get it back.

## Current job: Shea Foster documentary (`projects/shea-foster/`), started 6 Nov 2026
The user said: "Disregard the Marion Jones video. Just focus on this video." They asked me to build the whole thing overnight.
- **Done:**
  - Script `script_v2.md`: Southern read; the drawer/EPO story is told first-person from the user's talks with his teammates.
  - Voiceover `voiceover/sf_vo_full.mp3` (5:32). ElevenLabs flow pPXcfbuQkzpC0Af2Kib8, nodes "SF 01–07".
  - Music `music/M1_dark.mp3`, `M2_verdict.mp3`. SFX in `sfx/`.
  - Build: `sf_build.py` (+ `sf_gfx.py`), Jxmy style, 6:15, with 5 real audio bites from Foster's own 2024 doc.
  - Thumbnails `thumbnail_v1.py` (A/B/C). Upload package `youtube_upload.md`.
  - **Delivered 6 Nov 2026:** 1080p (202 MB) + thumbnails A/B/C in Dropbox `/Shea Foster/`. User approved ("Absolute cinema"), picked thumbnail A. Scheduled publish: Mon 9 Nov 2026 6:00 a.m. MT (13:00 UTC). YouTube API upload quota hit on 6 Nov; retry reminder set for 7 Nov 08:20 UTC.
- **Faces:** every runner except Foster is blurred. Foster is the bleached-blond runner holding the 3rd-place trophy in 17.jpg/20.jpg (face-matched with SFace).
- **Media not in git:** scratchpad `shea/` (dropbox photos, `real/` clips: NGTF bCnvO33Dcn0, 6LAX0Cp96Zw, jhbWcMw03Zo, hyTTK0DXCv0; `assets/`, `ai/`).
- Marion Jones is cancelled (keep `projects/marion-jones/style_jxmy.md` for the edit style).

## Done earlier: Oscar Pistorius (`projects/oscar-pistorius/`)
- **Done:**
  - Fact-checked script, approved by the user (`script_v1.md`, sources in `README.md`).
  - Full voiceover, approved style: `oscar-pistorius_voiceover_v1.mp3` (7:50), word timings in `vo_v1_words.json`. Built with `tools/space_voiceover.py`; ElevenLabs flow "Oscar Pistorius documentary voiceover".
  - 51 real clips and 13 Commons photos found. Every source and link is in `credits.md`.
- **Voiceover approved:** the user said "keep going".
- **Edit v1 done (5 Nov 2026):** `op_build.py` (7:56), thumbnail `thumbnail_v1.py`, `youtube_upload.md`. 1080p + thumbnails are in Dropbox `/Oscar Pistorius/`. User approved ("Absolute cinema"), picked thumbnail A. Scheduled publish: Mon 9 Nov 2026 6:00 a.m. MT (13:00 UTC). YouTube API upload quota hit on 6 Nov; retry reminder set for 7 Nov 08:20 UTC.
  - To rebuild in a new chat: re-import the clips (credits.md) into scratchpad `pistorius/real/`, the photos into `pistorius/photos/`, fix the `SCR` path at the top of `op_build.py`, then `python3 -I projects/oscar-pistorius/op_build.py`. Needs `pip install opencv-python-headless`.
- **Next:**
  1. Build the edit the same way as `projects/jon-drummond/jd_build.py`: real footage timed to the voiceover, neon look (`tools/neon.py`, `tools/hud.py`), music bed under the voice, SFX.
  2. Thumbnail.
  3. Upload package: title "The Olympic Sprinter Who Shot His Girlfriend Through A Door", description with credits, tags.
- **Do not use** the News Direct CGI re-enactment clip.
- **Media not in git:** the clips are in the session scratchpad `pistorius/real/`. In a new chat, re-import them free with vidIQ (`vidiq_video_upload` with the YouTube links in `credits.md`, then `vidiq_job_poll`, then curl). Re-download the photos from Wikimedia Commons through the Composio workbench (this machine's IP gets rate-limited).

## Finished: Jon Drummond (`projects/jon-drummond/`)
- Video published 5 Nov 2026: "He Wouldn't Leave The Track. So Track Got Rid Of Him".
- Upload package: `youtube_upload.md`.
- Thumbnails: current is v4, HD red-card frame (`thumbnail_v4.py`). Files are in Dropbox `/Jon Drummond/`.

## Next video ideas
`ideas/viral_video_ideas_2026-11.md`: ranked list backed by vidIQ data. Pistorius is #2; Marion Jones (#1) and Tim Montgomery (#3) are next.

## Podcast-style recordings waiting in Dropbox
These are 1–2 minute on-camera clips of the user, recorded 4 Nov 2026:
- `/Kendall Ellis`
- `/Yohan blake`
- `/Europe Being Rolled`
- `/Rylan`

## Accounts and tools
- vidIQ for research and free YouTube imports.
- ElevenLabs for the voice: the user's cloned voice is `dk6cvd5UilZRrcpZ7dNK`. Credits run out often; the user tops up.
- Dropbox and Commons through Composio.
- Higgsfield storage to stage files for Dropbox.
- Adobe has no generative fill here; use ElevenLabs image edit and paste back only the edited patch.

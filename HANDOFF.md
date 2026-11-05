# Handoff: where things stand (updated 5 Nov 2026)

To continue in a new chat:
1. Open the repo `erinspiderbrown/YouTube-` on branch **`claude/blissful-euler-adwpg2`**.
2. Say: "Read HANDOFF.md, CLAUDE.md and projects/oscar-pistorius/README.md, then continue."

Everything below is committed on that branch, except large media, which lives on the session's machine and is listed with how to get it back.

## Current job: Oscar Pistorius documentary (`projects/oscar-pistorius/`)
- **Done:**
  - Fact-checked script, approved by the user (`script_v1.md`, sources in `README.md`).
  - Full voiceover, approved style: `oscar-pistorius_voiceover_v1.mp3` (7:50), word timings in `vo_v1_words.json`. Built with `tools/space_voiceover.py`; ElevenLabs flow "Oscar Pistorius documentary voiceover".
  - 51 real clips and 13 Commons photos found. Every source and link is in `credits.md`.
- **Voiceover approved:** the user said "keep going".
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

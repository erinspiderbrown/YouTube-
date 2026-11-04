---
name: youtube-import
description: Download YouTube videos into this workspace from a pasted link, for studying edits frame by frame or using clips as B-roll. Use whenever the user pastes a YouTube link (youtube.com/watch, youtu.be, Shorts) and wants the video itself, not just a summary.
---

# Import YouTube videos

This cloud machine can't download from YouTube directly: yt-dlp and youtube-dl get HTTP 403. Don't try to work around that (no player-client tricks, cookies or proxies). Use vidIQ's server-side import instead.

## Steps
1. For each link, call `mcp__vidIQ__vidiq_video_upload` with `url` = the YouTube link and a short `title`. Load it with ToolSearch first if needed. It costs 0 credits and handles up to 299 MB, which covers most videos under 30 min at 720p.
2. It returns an `mcpJobId`. Poll `mcp__vidIQ__vidiq_job_poll`; a download takes a few minutes. Don't poll in a tight loop. Use `send_later` (3 min) if it's still running.
3. When it's `completed`, `curl -sSfL` the returned `videoUrl` into the scratchpad, e.g. `<scratchpad>/examples_dl/<videoId>.mp4`.
4. Check with `ffprobe` (duration, resolution, audio).
5. Then do what the user asked:
   - **Study the edit:** detect cuts with `ffmpeg -vf "select='gt(scene,0.28)',metadata=print"`, build a contact sheet (`tile`), and note text, overlays, transitions and pacing. Save notes to `examples/podcast/` or `examples/documentary/`.
   - **B-roll:** trim the requested range (`-ss`/`-to`) and use it in the edit. Keep it short and transformative (commentary/fair use) unless the user owns the footage.

## If it fails
- Over 299 MB: ask for a timestamp range and import a shorter piece, or ask the user to put the file in Dropbox (connected via Composio, account "Erin Brown Track & Field") and pull it from there.
- vidIQ not connected: say so and offer the Dropbox route.

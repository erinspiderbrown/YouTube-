# Scheduled YouTube upload job: Montverde video

The user asked Claude to upload and schedule the video themselves: **go live Thu 5 Nov 2026, 10:00 AM Mountain = 2026-11-05T17:00:00Z**.

Composio's shared YouTube app hit its daily upload quota on 4 Nov ("Video Uploads per day", resets 08:00 UTC = 1:00 AM MST). Run this job after 08:00 UTC on 5 Nov.

## Sources (user's own Higgsfield storage)
- Video (1080p, 202.8 MB, 9:00): https://d2ol7oe51mr4n9.cloudfront.net/user_3LcEFdqZuIv3oGXP4pI7v67JXeg/4f23b294-8b9a-47dc-82fc-1331de07e5d0.mp4
- Thumbnail (1280x720 JPG): https://d2ol7oe51mr4n9.cloudfront.net/user_3LcEFdqZuIv3oGXP4pI7v67JXeg/975a38ba-b74b-47b7-b2ce-6bdb8cf0fe69.jpg
- Title, description and tags: `youtube_upload.md` in this folder (use the description block verbatim). Category 17 (Sports).
- Channel: The Erin Brown (@theerinbrowntv, UCiMHg3V2Q414zFIjb8PyTcg), Composio account `youtube_orison-shawy`.

## Steps (Composio)
1. Workbench: download the video URL to /home/user/montverde_v5_1080p.mp4, then `upload_local_file` to get an s3key. A staged s3key from 4 Nov may have expired, so re-stage.
2. `YOUTUBE_MULTIPART_UPLOAD_VIDEO` with privacyStatus **private**, categoryId "17", title, description and tags. Fallback: `YOUTUBE_UPLOAD_VIDEO`. Record the videoId.
3. Schedule with `proxy_execute("PUT", "/videos", "youtube", query_params={"part": "status"}, body={"id": VID, "status": {"privacyStatus": "private", "publishAt": "2026-11-05T17:00:00Z", "selfDeclaredMadeForKids": False, "embeddable": True, "license": "youtube", "publicStatsViewable": True}})`. Endpoint form is "/videos" (not the full googleapis URL).
4. `YOUTUBE_UPDATE_THUMBNAIL` with the thumbnail URL (needs a phone-verified channel; if 403, tell the user to add it in Studio).
5. Verify with `YOUTUBE_GET_VIDEO_DETAILS_BATCH` (parts snippet, status): status.publishAt == 2026-11-05T17:00:00Z and privacyStatus == private.

## Retry policy
- On 429 quota errors: retry every 30 min. If not uploaded by 15:30 UTC (8:30 AM MST), stop and tell the user to upload manually with the links above, scheduling 10 AM in the YouTube app.
- Never upload twice: before retrying, list recent channel uploads and check the title isn't already there.

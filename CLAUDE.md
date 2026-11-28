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
  - **Content ID (user, 16 Nov 2026): no race footage from NCAA or Power-conference broadcasts.** The NCAA Championships channel (Turner Sports) and the Big 12 channel (XOS Digital Sports) both claimed the Jane Hedengren video and blocked earnings. Avoid ESPN/NCAA/conference race broadcasts and World Championships/Olympic broadcasts. Use Tracklandia, LetsRun/CITIUS interviews, athlete/family/team channels, documentaries (Nike, KSL) and workout vlogs as race B-roll.
  - **No official Olympic footage** (user, 17 Nov 2026): nothing from the Olympics channel, Olympics.com, NBC/Peacock or other Olympic broadcasts. Prefer independent photographers' and videographers' footage, athlete/family/team channels, interviews and documentaries.
  - **Race footage, all videos (user, 18 Nov 2026): fan-shot videos and re-uploads are the preferred source.** Look for them first (fans filming from the stands, phone/TV re-uploads on small channels) before official broadcasts.
  - **No NBC footage, in any video (user, 23 Nov 2026).** Nothing from NBC, NBC Sports, Peacock or NBC-affiliate race broadcasts, and no re-uploads or news packages showing NBC-bugged footage (check local news clips for the NBC/Peacock bug and skip those seconds). This replaces the one-off Athing Mu exception (18 Nov 2026, max 8 s per clip), which no longer applies.
  - **No Diamond League footage** (user, 20 Nov 2026, on the Mondo Duplantis video): nothing from the Wanda Diamond League channel or its interview feed (RunnerSpace/CITIUS sometimes re-post the same DL feed), and no TV-broadcast re-uploads from Diamond League meets. Fan/phone clips from the stands, athletes' own clips and independent outlets' own interviews are fine. Stay away from anything with official Diamond League branding (user, 26 Nov 2026): when an independent interview was filmed in front of a Diamond League logo wall, play its audio over other B-roll with the quote on screen instead of showing it.
  - **No RunnerSpace footage, in any video** (user, 20 Nov 2026, on the Jane NCAA preview): no RunnerSpace race streams, replays, highlights or interviews, and no re-uploads with their logo.
  - **Never use FloTrack or MileSplit footage (both FloSports), in any video** (user, 11 Nov 2026). No FloTrack broadcasts, FloTrack/MileSplit uploads or interviews, or re-uploads showing their logo or watermark. Check news packages for MileSplit-watermarked race footage too. Citing their articles as a text source is fine.
- **The approved editing style (from 10 Nov 2026): the Boling v2 edit.** The user called it "probably the highest production level" so far and asked to save it for future videos. The template is `projects/matthew-boling/boling_build.py`; the full recipe is in `projects/matthew-boling/EDIT_STYLE.md`. In short:
  - **Real soundbites play with their own sound while the voiceover pauses:** news segments, live race calls, family and coaches from documentaries, the athlete in their own words (interviews, vlogs). Aim for about 15 per 6 min of VO. They give the video its length (8+ min) and credibility. Never pad or slow the voice for length.
  - **Cold open** on the strongest soundbite (Boling: his dad watching the 9.98 come up on the scoreboard).
  - **Footage hunt:** race broadcasts, local news, documentary shorts and the athlete's own channel, imported via vidIQ. Make contact sheets to pick moments, and transcribe every clip to find the soundbites.
  - **Graphics:** `tools/kinetic.py`. Animated numbers that roll and slam, kinetic words, lower thirds, stamps (NO PARIS), and a chapter slate per part with a flash cut. A small source credit goes bottom-right. No neon stat boxes (the user: "not all that").
  - **Editing:**
    - punch-in on every number or key word
    - black-and-white on the low points
    - slow-mo on finishes and flashbacks
    - cuts every 2–5 s
  - **Sound:**
    - a dark bed per chapter, ducked under the voice
    - very few SFX, varied, never back to back (6 s minimum between stat hits, 3 s between any two hits, none on plain cuts)
    - soundbites loudness-matched (-17 LUFS)
  - **User-read voiceover:** cut every flub and restart. Re-transcribe the raw takes verbatim in short chunks plus check the waveform (`clean_voiceover.py` MIST list), then re-time with `retime_words.py`.
- **Style refresh needed (user, 17 Nov 2026):** the Boling v2 look is now "repetitive". The user wants it **more cinematic and professional**: no more "slap stickers" (the orange/white kinetic words, stamps and stat slams read as too simple), and scripts must stop following the same format ("Lemme tell y'all" → chapters → "So what y'all think" every time). Vary the structure per video and build a ~30 s style test for the user to approve before the next full edit. **Not an old-film look** (user: no grain, no vintage): the target is **new, modern, high quality**, like a current Netflix/Apple sports doc. Crisp clean grade, sharp footage, clean modern sans type with smooth (not slamming) animation, motion-tracked labels, 3D parallax on photos, smooth speed ramps and modern transitions.
- **Standing edit rules for EVERY video from now on (user, 28 Nov 2026, Gout Gout v3):**
  - **Interviews never cut mid-sentence.** Snap every soundbite to whole sentences (start at a sentence start, end on the sentence's last word; `snap()` in projects/gout-gout/gout_build.py), 0.15 s audio fade in / 0.45 s fade out, and a smooth picture transition both INTO and OUT OF every interview. An abrupt mid-sentence cut is "tacky".
  - **Real ambience and sound design:** a low stadium/room-tone bed under the whole video, scene beds that match the picture (wind, rain, crowd), a matching sound on every transition (whoosh/glitch/boom), shutters/ticks on graphics. Generate fresh with ElevenLabs sound effects (`eleven_text_to_sound_v3`); library for Gout in projects/gout-gout/sfx/.
  - **Varied, high-quality transitions** (premium.py: zoom, rgb, bloom, vpush, whip, push, blur, leak, luma, dip), not the same one twice in a row.
  - **No "Claude-looking" graphics.** The user can spot the default look in every AI-made video: Inter/Anton/Bebas type, red or yellow pills, dark glass boxes, yellow highlighted numbers, plain bar tables, thin tracked caps. Every video gets its OWN visual identity built from its story (a motif, palette and type pairing you choose for that video, e.g. Gout = wind-gauge/weather-map look). Keep on-screen quotes (the user likes them), restyled to match. Show the user a style frame before the full render.
- Older look (Jon Drummond, banned substances): neon glow/HUD (`tools/neon.py`). Use it only if the user asks.
- Keep the music bed under the voice: it masks AI artifacts in the cloned voice.
- **New, unique music for every video (user, 26 Nov 2026):** every video so far reused the same beds (Drummond M1-M5, Tebogo triumph). Don't reuse old beds. Generate a fresh score per video, one track per mood/chapter, written for that story (ElevenLabs `eleven_music_v2_5`, instrumental, prompt names the story beat and instruments; e.g. projects/sam-ruthe music nodes M1-M7 in flow aXvnFu3COJL7mFlxv084). Still dark/mysterious/suspenseful by default, never upbeat lo-fi, ducked under the voice.

## The user reads their own scripts (from 10 Nov 2026)
The user said viewers notice the AI voice and that it "doesn't really sound like me". **For videos that aren't too long, the user records the voiceover themselves.** Claude writes the script and does the editing.
- Write the script in the user's own words (see the script rules below), split into short sections they can read in one take.
- **Numbers in scripts the user reads:** always digits, never spelled out ("9.98", "4x400", "6th", "2-time", "1 spot", "US", "NCAA"). Dates: month as a word, day and year as numbers ("April 27, 2019"). The "years and times as words" rule below is only for the cloned voice.
- **Scripts must not sound like AI (user, 20 Nov 2026: viewers say recent scripts "don't sound like me", "not my style").** Stop the house format: no date-place-event stacks as openers ("June 7, 2026. Stockholm."), no runs of one-line dramatic fragments, no "here's what's on the line" / "and that's not all" / "so here it is", no rule-of-three lists, no same opener/closer every time ("Lemme tell y'all", "And here go the crazy part", "Drop it in the comments"). Write it like the user talking to camera: full run-on sentences, their own opinions ("I really feel like", "honestly I think"), side comments, "y'all", "ain't", "'cause", casual grammar. Teleprompter parts are just "Part 1, 2…", no catchy headings. No strong profanity (ad-friendly). Use the user's own terms (user, 20 Nov 2026): "choke artist", "get the job done", "on paper", "come through", "shine"; frame previews as a question like "is she a choke artist or does she get the job done?".
- Give the user a **teleprompter page**: an Artifact with big text, one section per screen, and a scroll at their pace. Where the page can use the mic, it records each take there; otherwise the user records on their phone and sends the files.
- **Never clip a word, especially years** (user, 13 Nov 2026: "2024" came out as "2020"). Whisper word end times run early on numbers, so never cut at whisper end + padding. Place every pause or flub cut inside measured silence with `tools/safe_cuts.py` (`pause_cuts`, `safe_point`), then re-transcribe the cleaned voiceover and run `check_numbers(script, words)`: every year and number in the script must come back whole before the edit is built.
- **Soundbite splits too:** the voiceover is split wherever a soundbite is inserted. Never split at whisper start - 0.25; use `gap_point()` (projects/alan-webb/webb_build.py): the quietest 80 ms in measured audio around the phrase start, and check every split sits between the end of one word and the onset of the next.
- Take their recordings from the chat upload, the page, or their Dropbox. Clean them up: noise reduction, levels, cut the breaths and mistakes, keep their natural pace. **Do not** run them through `space_voiceover.py` or any tempo change. Then transcribe for timing and edit as usual.
- Use the cloned voice below only for long videos, or when the user asks for it.

## The cloned voice (long videos only, or when the user asks)
**NEW DEFAULT from 22 Nov 2026: "Erin Brown 2026"** (Instant Voice Clone on the user's own ElevenLabs account, voice_id `uBqzFhqGLj9GteaUaPDl`, made from ~28 min of the user's own reads; their Composio `elevenlabs` connection is the user's account). Settings: `eleven_v4`, stability 0.3, similarity 0.9, **no style tags** (no `[calm] [relaxed]`). The user said the old takes were "too slow and chill" and "too proper".
- **Same accent the whole video, every video (user, 28 Nov 2026, Gout Gout):** the clone drifted into an Australian accent on the parts full of Australian names/places, and the user was furious ("Never do no shit like this again"). Keep the user's own Black Texas accent, slang and dialect from the first word to the last, whatever country the story is in. Every node's tag must pin it: `[casual Black Texas accent, American Southern, NOT Australian/British/African, talking to a friend, laid-back, not hyped, unhurried]`. Checking by transcript is not enough: compare every part against part 1 for accent drift before building, and regenerate any part that sounds different.
- **Accent drift, round 2 (user, 28 Nov 2026, Gout v3):** even with the pinned tag, eleven_v4 still slid into Australian on some parts. Never write "Australian" (or any accent to avoid) in a tag: the model hears the word and drifts toward it; describe only the accent you want. Don't A/B new models; use the settled recipe below.
- **Voice recipe is settled; don't experiment (user, 28 Nov 2026: "I don't know why we have to do this every single video. We already made regular videos with the voice sounding the way it's supposed to").** Always use the approved A3b recipe from Kejelcha / Lyles / Dare / Cooper: `eleven_v4`, voice `uBqzFhqGLj9GteaUaPDl`, stability 0.4, similarity 0.9, tag `[casual Black Texas accent, talking to a friend, laid-back, not hyped, unhurried]` and nothing more, "da/dat/dey" spelling, then atempo 0.94 + match_rhythm. `eleven_multilingual_v2` was rejected ("furthest from sounding like me"); a heavier "Dallas Texas, Southern drawl" tag was "too much Southern". For stories abroad, cut place names the script doesn't need, record 2 takes per part, and screen with `tools/voice_sim2.py` (similarity to the approved VOs: good takes ~0.82–0.85, multilingual ~0.67–0.70).
- **Name pronunciations (user):** Calab Law = "Kay-lub" (write "Kay-lub Law"); Christopher Ius = "use" (write "Christopher Use").
- **Transition sounds (user, 28 Nov 2026):** don't put a whoosh on every transition ("too repetitive"). Sound only on interview entrances, chapter cards, glitches and data graphics; whooshes 7 s+ apart, rotated, never the same file twice in a row.
- **Race names (user, 28 Nov 2026):** write "da hundred" / "da two hundred" / "da four hundred", never "hunnid" (it sounds forced).
- **Take the user's side (user, 28 Nov 2026, Gout Gout):** when the user takes a stance, argue it with the facts; no "other side" chapter and no fence-sitting ending ("y'all decide"). State an inconvenient fact once, plainly, then keep arguing. Keep accusations as the user's opinion drawn from facts shown on screen (never say officials faked a reading or an athlete faked an injury as fact).
- **Pace:** never slow the words. Use `tools/match_rhythm.py IN OUT` (only lengthens pauses toward ~0.7 s). Do not use `space_voiceover.py` for this voice. The user's reads measure ~19 pauses per 100 words, median pause 0.70 s.
- **Spell it how the user talks** (TTS reads the spelling): "da" for the, "dis/dat/dese/dey/dem", "wit", drop the g ("runnin'"), drop plural/possessive s where they would ("Nico Young little brother", "choke artist"), "ain't", "gon'", "'cause", "y'all". Dates with ordinals ("June 24th"), "4x4" not "4x400".
- **Opening part must sound like the user, not proper (user, 26 Nov 2026, Sam Ruthe):** the first part of the Ruthe VO sounded "too proper, unlike me, not using my dialect". Write Part 1 heavier in their dialect than the rest: "Y'all," "'bout", "lil dude", "a whole bunch of", "His name Sam Ruth" (no "is"), "I ain't gon' hold you", "the dude everybody say", "I'ma break down", "Ain't nobody see that comin'". No narrator-style setup sentences.
- **Openers/phrases (user, 22 Nov 2026):** no "Man,"/"Aight" warm-up openers, just get into it. Not "I ain't gon' sugarcoat it"; the user says "I ain't gon' hold you".
- Older voice below (PVC "Erin Brown" `dk6cvd5UilZRrcpZ7dNK`) only if the user asks.

**Default from 9 Nov 2026: the "Felix / Jacobs" voice.** The user said the voice on their Allyson Felix and Marcell Jacobs videos "is the closest to mine" and asked for it on every future YouTube narration. It's the setup first made for the Jon Drummond video (v4), reused for "Felix vs Tarmoh" (ElevenLabs flow `4LlukseKRsgRiOUAzkpV`; the Drummond take is flow `EwtCtvyEoktyTmEPgx7r`, nodes "V4 0x"). No Jacobs flow exists in ElevenLabs any more; it was made with the same recipe.
- **ElevenLabs:** voice `dk6cvd5UilZRrcpZ7dNK` (Erin Brown), model `eleven_v4`, voice_settings **stability 0.45, similarity 0.85**. Pass the voice as `voice_id`, and set the settings with `creative_update_node` `model_parameters={"voice_id": ..., "voice_settings": {"stability": 0.45, "similarity": 0.85}}`. The key is `similarity`, not `similarity_boost`; a wrong key is dropped silently, so read the node back before running.
- **Tags at the start of every paragraph:** `[calm] [relaxed] [Texas accent]`. Put `[pause]` before a turn or a reveal (`[pause] [calm] [relaxed] [Texas accent] Then a few hours later…`).
- **Script voice in that recipe:** "Aight, so check it out." "Mane." "Bruh." "Lemme tell y'all." "And here go the crazy part." "They was sellin' her as the golden girl." Ellipses for beats ("And third… Jeneba Tarmoh.").
- The previous setup ("test 3": stability 0.25, similarity 0.8, tags `[tellin' a story on the block] [nasal voice] [Texas street accent] [relaxed, not proper] [chill, not hype]`) made the NCAA 100m, Tebogo and banned-substances voiceovers. The user says it's okay but talks too proper. Use it only if the user asks.
- For a death or tribute, add `[quiet, respectful]` in front of the tags.
- **Write the script how the user talks, not proper English.** Urban, Texas, casual: "Ten dudes." "One of 'em banned 'til twenty twenty-nine." "He go pro, and two years later he world champ." "Where they at now." Drop extra verbs ("he twenty-three", "this America"), use "ain't", "gon'", "tryna", "somethin'", "'cause", "a lotta". Facts stay exactly right.
- **Pronunciation and spelling for the voice:**
  - Kenya / Kenyan: write **Kinya / Kinyan / Kinyans** (user says "Kin-yan", Texas). Stretch those words a little (`tools/slow_words.py`, factor 0.88).
  - Years and times as words: "twenty sixteen", "nine eight-two", "nineteen seventy-three", "twenty-oh-six".
  - "N C double-A", "L S U", "U S A" spelled with spaces.
  - Letsile Tebogo: write **Let-see-lay Tuhbowho** (user: first name "Let see lay"; last name "Tuh bow ho" said fast, run together).
- **Energy:** chill, not hype. The user said the Tebogo take was "too enthusiastic". Add `[chill, not hype]` to the tags, and keep lines plain street talk (no narrator phrasing like "a village about an hour outside the capital").
- **Pace:** `tools/space_voiceover.py --tempo-scale 0.93 --target-wpm 148 --min-tempo 0.9 --max-extra 1.2 --gap 1.3`. The user said the first takes were too fast; this is the approved speed.
- Before a full re-record of a new style, test ~25 s first and let the user pick.

## TikTok versions of long videos (user, 15 Nov 2026)
- **Every long video converted for TikTok gets its own high-quality vertical cover.** The user called a quick cut-out cover "low quality, poor edited, no effort" and approved the rebuilt Webb one (`projects/alan-webb/tiktok_cover.jpg`, made by `projects/alan-webb/make_tiktok_cover.py`). Recipe:
  - Start from the YouTube thumbnail's real photo at full resolution. Keep it as one photo with its own background; never paste a rough cut-out onto a flat colour.
  - Crop tight so the subject fills the 1080x1920 width. Put the face mid-frame, clear of TikTok's buttons on the right and the caption at the bottom.
  - Extend the top with the photo's own sky or background, blended so there's no seam.
  - Use the thumbnail's own title, big, in the top third, in the same style (cream Bebas Neue with a soft shadow for the Webb/Tuohy look).
  - Redraw graphics like the red arrow crisply, behind the subject, and remove the photo's old faint copy.
  - Grade it: contrast, darker edges, light grain. Check the face at full size before showing it.
  - Show the user the cover before posting.
- **Vertical video:** blurred, darkened copy of the video filling the frame, with the 16:9 video centred. The cover is overlaid on the first 1.2 s (TikTok uses the opening frame as the cover; vidIQ can't set one), and the audio keeps playing under it.
- **Posting:** vidIQ `vidiq_video_upload` (localFile), then `vidiq_social_post_draft_create` to Erin Spider Brown (`_000ssAV0cJxYmcJ0XSxwm8rgS87rI5_tVPx`), public, comments on, music confirmed. The caption starts with `#5MinutePlus`. Then publish.
- **No second confirmation (user, 19 Nov 2026):** when the user says to post on a platform, that is the approval, for every platform and tool (vidIQ to TikTok/YouTube/Instagram/Facebook/X, Composio Facebook, Upload-Post). Draft, check it, and publish straight away; don't ask "should I post?" again. Show the result (link/status) afterwards. TikTok processing of a 10-minute video can take 10+ minutes.

## Facebook (user, 17 Nov 2026)
- The user's Facebook Page is **E.Diamondz** (id 506309812910570), connected through Composio (`facebook` toolkit), not vidIQ.
- Post with `FACEBOOK_CREATE_VIDEO_POST` (`page_id`, `file_url` = the hosted 16:9 MP4, title, description), then `FACEBOOK_SET_VIDEO_THUMBNAIL` (`is_preferred: true`) with the YouTube thumbnail.
- Caption: the TikTok caption without `#5MinutePlus`, plus the YouTube link.

## Scheduling uploads
- **Every scheduled YouTube video goes public at 6:00 AM Mountain** (13:00 UTC in winter, 12:00 UTC in summer) (user, 23 Nov 2026; replaces the earlier 11:00 AM rule). Keep the date they give.
- **Upload through Upload-Post** (Composio toolkit `upload_post`, profile `default`, YouTube channel The Erin Brown connected). It has its own YouTube quota. The flow that gets everything on before the video goes public:
  1. Host the MP4 at a public URL (Higgsfield `media_upload` → PUT → `media_confirm`).
  2. `UPLOAD_POST_SCHEDULE_POST` (`content_type: video`, `platforms: ["youtube"]`, `video` = URL, title, description, `scheduled_date` a few minutes from now).
  3. Before it runs, `PATCH https://api.upload-post.com/api/uploadposts/schedule/<job_id>` via `COMPOSIO_PROXY_EXECUTE` (JSON) with `fields: {privacyStatus: "private", youtube_publish_at: "<release time UTC>", categoryId: "17"}`. It then uploads as a private video that YouTube itself publishes at the release time.
  4. Get the video ID from `GET /api/uploadposts/history`, then with Composio YouTube (no upload quota): `PUT /videos?part=snippet` for tags + category, `YOUTUBE_UPDATE_THUMBNAIL`, and `YOUTUBE_UPLOAD_CAPTION_TRACK` with an .srt from `tools/make_captions.py SCRIPT.md WORDS.json OUT.srt` (script text timed to the VO's whisper words).
  Upload-Post drops tags and thumbnail sent through Composio, which is why step 4 sets them.
- **Monetization must be on for every video.** No API we have can switch it (the YouTube Data API has no monetization field). It comes from the channel's upload defaults (Studio → Settings → Upload defaults → Advanced settings → Monetization: On). Remind the user to check the Monetization tab on any video uploaded before that default was set.
- Composio's own YouTube upload (`YOUTUBE_MULTIPART_UPLOAD_VIDEO`) shares a daily upload quota that is usually used up; don't rely on it.
- **Upload-Post's free plan allows 10 uploads a month** (hit on 17 Nov 2026). When it refuses, upload with `YOUTUBE_MULTIPART_UPLOAD_VIDEO` (privacy private) right after its quota resets at 08:00 UTC, then set `publishAt` and the thumbnail with vidIQ.

- **Titles (user, 20 Nov 2026): short, simple, to the point** (e.g. "Is Rocky Hansen About To Get EXPOSED?"). No long two-part titles with "..." setups.

## What's working (Studio stats the user shared, 17 Nov 2026)
- Tuohy "America's Greatest High School Runner Ever... What Went Wrong?": 196.4K views in 3 days, CTR 8.7%, AVD 3:42 (of 9:54).
- Boling "America's Fastest High Schooler... What Went Wrong?": 136.2K in 6 days, CTR 5.7%, AVD 3:40.
- Abby Steiner 36.2K (CTR 6.3%), Candace Hill 32.3K (CTR 6.3%), Jane 9.7K in day 1 (CTR 7.7%, AVD 4:13), Alan Webb 4.2K in 2 days (CTR 4.5%, AVD 4:17).
- Takeaways: famous American prodigy + "America's ___ Ever... What Went Wrong?" titles win. The best CTRs come from the clean thumbnails: one sharp real photo,
  big cream condensed question (WHERE DID SHE GO? / NEXT TO FALL?). Retention sits around 40%, so the first minute and the middle need the most work.

## Reference examples
- `examples/thumbnails/README.md`: **thumbnail house style = the user's own Boling thumbnail** (`examples/thumbnails/user_boling_what_happened.png`, 10 Nov 2026). One bright stadium scene, the athlete's peak action cutout upper-left, a big front-lit close-up face on the right, a heavy italic 2-line question bottom-left (white + yellow→orange gradient, red swoosh). Build with `tools/thumb_template.py`. The earlier Ev Hand notes are superseded.
  - **Downfall videos** use the second style the user liked (11 Nov 2026): one huge real sad/defeated face on textured blue with 3 words ("HE **LOST** EVERYTHING.": small white, giant red, white with a yellow underline). Build with `tools/thumb_downfall.py`. Never paint on tears.
- `examples/podcast/`: example videos/clips for podcast style.
- `examples/documentary/`: example videos/clips for documentary style.
- `examples/links.md`: YouTube links and notes on what to study in each one.

**Getting YouTube videos in:** the user can just paste a YouTube link.
- Use the vidIQ tool `vidiq_video_upload` with `url` set to the link. It downloads on vidIQ's servers, costs 0 credits, and handles up to 299 MB.
- Poll `vidiq_job_poll`, then `curl` the returned `videoUrl` into the scratchpad.
- Direct yt-dlp/youtube-dl from this cloud machine gets 403 from YouTube. Don't try to work around that.
- Other sources: the user's Dropbox (connected through Composio) or files they upload.

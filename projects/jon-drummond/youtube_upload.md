# Jon Drummond: YouTube upload package

Research (vidIQ, 5 Nov 2026):
- JxmyHighroller, the NBA storytelling channel (2.7M subs). His biggest videos are story titles with a twist and no names:
  - "He Made A Million Dollar Shot And They Didn't Want To Pay Him": 19.8M views, 10x his normal
  - "When Disrespecting Another Player Goes Too Far": 14.8M
  - "He Should Have Never Said This"
  - Thumbnails: the real moment, a red arrow or circle, and at most a 3–4 word caption.
- The Erin Brown, the user's channel. The top story videos pair an emotional real frame with 2–4 huge glowing words:
  - "Tori Bowie: What Actually Killed Her": 13.7x
  - "Sha'Carri Last Place Finish": 12.5x, "ITS OVER" thumbnail
  - "I Exposed a Nike Sprinter — Then Everything Changed": 8.3x

## Titles (vidIQ score for this channel)
1. **He Wouldn't Leave The Track. So Track Got Rid Of Him. (96)** ← recommended
2. Jon Drummond: The Dark Truth Behind Track's Craziest Protest (93)
3. The Sprinter Who Stopped The World Championships For An Hour (92)
4. He Refused To Leave The Track... 11 Years Later He Was Banned (91)
5. When Protesting A False Start Goes Too Far (85)
6. From Olympic Gold To An 8 Year Ban: The Jon Drummond Story (85)

Unscored backups in the same styles:
- They Called Him A Disgrace. Then They Made Him Coach Team USA.
- He Protested For An Hour… Then The Sport Changed Forever
- The Most Disrespectful Protest In Track & Field History

## Thumbnail v4: CURRENT (HD real frames, layered; files in `thumbnails/` and Dropbox `/Jon Drummond/`)
The user said the v3 photo "looks terrible" and the design was too simple. v4 swaps in much sharper real footage:
- **Source:** a clean HD re-upload of the Paris 2003 race coverage, imported free with vidIQ from YouTube Short `f1Ss4gMlnyA` (it has Japanese subtitles burned in).
- **Frames used:**
  - The official raising the red card over Drummond as he shouts with his hands up.
  - Him lying on the track with his hands behind his head.
  - The start-sensor printout: "Lane4 0.052 Sec Fault".
- **Removing the subtitles:** ElevenLabs gemini-3-pro-image made a cleaned copy of each frame. That copy was aligned to the real frame (SIFT + homography), and only the small subtitle patch was pasted back with a feather. Everything else, including both faces, is original pixels.
- **Cut-out:** BiRefNet on the red-card frame.

Thumbnails (script: `thumbnail_v4.py`):
- **A `drummond_thumb_v4_A.jpg`: "I DIDN'T MOVE!"** ← use with title #1.
  - Cut-out of the official raising the red card over Drummond, on a dark red stadium with light rays. The card is boosted with a white edge glow.
  - A yellow arrow runs from the quote to the card.
  - Photo card of him lying on the track, tagged "50 MINUTES".
  - The sensor printout with 0.052 / Fault circled.
- **B `drummond_thumb_v4_B.jpg`: "HE WOULDN'T / LEAVE"**, same art. Upload A and B in YouTube Studio → **Test & Compare**.

## Thumbnail v3 (niche-tested style; files in `thumbnails/` and Dropbox `/Jon Drummond/`)
Research (vidIQ outliers, 5 Nov 2026). The thumbnails winning on athlete scandal/downfall stories:
- "RayGun and the Story of the 'Worst Olympian Ever'" (Scandal): 373K, 7.1x. Cut-out athlete on a dark stadium, a 0-18 scoreboard, "WORST OLYMPIAN EVER?" in stacked distressed white type, red brush underline.
- David King, "The Tragic Success Of China's Greatest Hurdler": 11x. Real moment + "HE DIDN'T WANT **THIS**".
- CATASTROPHIYA, "They couldn't save the OLYMPIC CHAMPION": 530K, 20x. "SHE STILL **HANGS**".
- "FRAMED" (NHRA scandal): 188x. One red-boxed word + an arrow to the proof.
- "THE END" (Bol Bol ban), "SHE DIED INSTANTLY", "Liar." (1.1M, 27x).

What the winners share:
- One real subject, big, on a dark background.
- One proof element.
- 2–4 huge condensed words that ask a question the title doesn't answer.
- One red accent, and nothing else. The busier collage style (v2) isn't what's winning.

Thumbnails (script: `thumbnail_v3.py`):
- **A `drummond_thumb_v3_A.jpg`: "WORST PROTEST EVER?"** ← use with title #1.
  - The real Paris 2003 frame of Drummond, hands up and eyes closed ("I didn't move"), cut out over a dark Stade de France with a red backlight.
  - An LED results board behind him reads FALSE START.
  - Stacked distressed white type with a red brush underline.
  - The question invites the "was he wrong or was the rule wrong?" debate that the pinned comment asks.
- **B `drummond_thumb_v3_B.jpg`: "HE WOULDN'T / LEAVE"**, with LEAVE in glowing red. Same art. Use it as the second Test & Compare option, or pair it with title #3 ("The Sprinter Who Stopped The World Championships For An Hour").

Both read clearly at phone and sidebar size. Upload A and B (plus v2 #1 if you want a third) in YouTube Studio → **Test & Compare**.

## Thumbnails v2 (high-res, layered; files in `thumbnails/` and Dropbox `/Jon Drummond/`)
How they're built: the real broadcast frames were upscaled 3x with Topaz "Recover 3", a faithful restoration that keeps his real face (in the ElevenLabs flow "Jon Drummond thumbnails"). The "Redefine" mode was rejected because it changed his face. BiRefNet makes the cut-out. Rendered at 2560x1440 and saved at 1280x720. Script: `thumbnail_v2.py`.
- **1 `drummond_thumb_v2_1.jpg`: Protest vs Ban** ← recommended with title #1.
  - Cut-out of Drummond, hands up ("I didn't move"), with a white sticker outline and cyan glow, over the Stade de France (Paris 2003).
  - A tilted USADA "Anti-Doping Decision" case file with a red BANNED 8 YEARS stamp.
  - A circle inset of him lying on the track, plus 2003 / 2014 tags.
- **2 `drummond_thumb_v2_2.jpg`: HE WOULDN'T LEAVE.** Your channel's proven big-glowing-words style. Officials stand over him on the track; an inset of him arguing has an arrow to his face, plus a PARIS 2003 tag.
- **3 `drummond_thumb_v2_3.jpg`: Jimmy-style.** The overhead shot of him alone on the track with a red ring and arrow, a face close-up inset, and "HE WOULDN'T MOVE".

Upload all three in YouTube Studio → **Test & Compare**.
(The v1 thumbnails A/B/C are still in `thumbnails/`.)

## Description
```
In 2003, Jon Drummond laid down on the track at the World Championships in Paris… and wouldn't leave. The whole meet stopped for damn near an hour.

Olympic gold medalist. Captain of Team USA's 4x100. The biggest showman in track & field. Eleven years later, the sport banned him for 8 years.

So how do you go from refusing to leave the track… to getting banned from it? Let me tell y'all.

⏱️ CHAPTERS
0:00 He Wouldn't Leave
1:03 Who Was Jon Drummond?
1:46 Sydney 2000: Gold… And The Party
3:04 The False Start Rule That Changed Everything
3:34 Paris 2003: The Protest
4:17 The Fallout
5:46 The Coach: Tyson Gay & London 2012
6:58 The Ruling: 8 Years
7:24 Hall Of Fame & A Ban… Same Year

💬 Was the protest wrong… or was the rule wrong? Let me know in the comments.

🔔 Subscribe for more track & field stories nobody else is telling.

PHOTOS (Wikimedia Commons)
Jon Drummond, 1994 Jenner Classic: Kevin Scannell, CC BY 4.0
Bernard Williams: Erik van Leeuwen, CC BY-SA 3.0
Maurice Greene, Sydney 2000: Jimmy Harris, CC BY 2.0
Michael Johnson: Kb1367, CC BY-SA 4.0
Tyson Gay, London 2012 / USA 4x100 London 2012: Tab59, CC BY-SA 2.0
Henry Kissinger: U.S. Department of State, public domain
Wilt Chamberlain, 1960: Bill Allen, public domain
Row houses, West Philly: Axcordion, CC BY-SA 3.0
Overbrook High School: Peetlesnumber1, CC BY-SA 4.0
Odessa College: Billy Hathorn, CC BY-SA 3.0
TCU campus: public domain
Paris 2003 World Championships: Gruni70, CC BY-SA 3.0
London 2012 Olympic Stadium: Jpbowen, CC BY-SA 3.0
USADA logo: public domain
Licenses: creativecommons.org/licenses

ARCHIVE FOOTAGE
2003 World Championships, Paris (fan footage + France 2 broadcast)
1996 US Olympic Trials (NBC), 2000 Sydney Olympics (NBC / France Télévisions)
1993 World Championships, Stuttgart (IAAF), 1996 Atlanta Olympics
2011 World Championships, Daegu (Universal Sports), 2012 London Olympics
PBS NewsHour (2013)
Archive footage used for commentary and criticism.

#trackandfield #jondrummond #sprinting #olympics #falsestart
```

## Tags
jon drummond, jon drummond false start, jon drummond paris 2003, jon drummond protest, jon drummond banned, false start protest, sprinter refuses to leave track, track and field documentary, track and field drama, track and field history, world championships 2003, false start rule, usain bolt false start, maurice greene, sydney 2000 4x100, tyson gay, tyson gay doping, usada ban, track coach banned, team usa relay, the erin brown

## Pinned comment
"Real talk: was Drummond wrong for laying on that track… or was the one-false-start rule the real problem? 👇"

## Upload settings
- Category: Sports
- Language: English
- Captions: auto-generate, then fix "Drummond" (it may come out as "Drumming")
- End screen: link your Tori Bowie video (best story performer) + subscribe

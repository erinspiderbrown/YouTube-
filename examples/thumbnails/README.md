# Thumbnail style: THE HOUSE STYLE is the user's own Boling thumbnail

**From 10 Nov 2026, model every thumbnail on `user_boling_what_happened.png`** (the user made it themselves for
"America's Fastest High Schooler... What Went Wrong?" and said: "create something similar for my future thumbnails").
After four rounds the user rejected: stat boards and props, rectangular split panels, grunge text, black-and-white
"selective colour", ghosted overlays and dark moody grades. Don't go back to those.

## What it is
- **One bright, daylight scene, no panels or borders.** The background is a real packed stadium crowd, softly blurred
  (depth of field), with blue sky, warm light and high clarity.
- **The same athlete twice:**
  - **The peak moment (glory):** an action cutout in the upper-left/centre, about 70% of the frame height (his
    mid-air long jump in the Strake Jesuit kit, bib visible).
  - **A big close-up face:** on the right, about 45–55% of the width. The head is cropped slightly at the top, the
    shoulders reach the bottom, it's front-lit and smiling/reacting, and real props like the interview mics (KHOU 11)
    and the medal ribbon show.
- **Text bottom-left, 2 lines, heavy italic sans:**
  - "WHAT" in white with a soft grey gradient.
  - "HAPPENED?" bigger, in a yellow → orange gradient.
  - Dark outline and a strong drop shadow, with a red brush swoosh under line 2.
  - The text sits left of the face and doesn't cover it.
- **Everything crisp, HD and saturated.** Both photos are real, from the same era (high school), and graded to match
  each other and the background.

## How to make one
- Use `tools/thumb_template.py`. It does the background, action, face, text and swoosh, with the font
  `tools/fonts/Montserrat-BlackItalic.ttf`:
  `python3 tools/thumb_template.py --bg CROWD.jpg --action ACTION.png --face FACE.png --l1 WHAT --l2 HAPPENED? --out OUT.jpg`
  - Make the cutouts with rembg (`isnet-general-use`; `birefnet-portrait` for faces). Check the masks; a
    see-through shirt means re-run with the portrait model.
- **Pick the photos first; they make or break it.**
  - **FACE:** a bright, front-lit head-and-shoulders shot looking slightly off-camera (podium/interview/press photo).
    Not a dark or moody documentary frame.
  - **ACTION:** the athlete's most famous moment, sharp and big.
  - **BG:** a real crowd or stadium from the same event, if possible.
  - Real photos only (the user's rule).
- **Text:** 1–2 words per line and a question works best ("WHAT HAPPENED?", "WHAT WENT WRONG?", "WHERE IS HE NOW?").
  Keep it different from the title.

---

# Earlier reference: Ev Hand (@evhandd), 9 Nov 2026 (superseded by the house style above)

The user (9 Nov 2026): "he really does great YouTube thumbnails that perform really well. Take that into consideration when editing my next thumbnails."
Channel: https://youtube.com/@evhandd (UCpejmzf5hYcckscyg79JeLQ). Sports-business explainers, 12 long videos, best 266K / 150K / 120K views.
Contact sheets of all 12 (maxres): `evhandd/sheet1.jpg` (top 4 by views), `sheet2.jpg`, `sheet3.jpg`.

| Views | Video | Thumbnail |
|---:|---|---|
| 266K | The NFL's Secret Super Bowl T-Shirt Operation | Eli Manning holding the trophy in a "CHAMPIONS" shirt, left. A warehouse of shrink-wrapped "CONFIDENTIAL · Patriots 19-0 merchandise" boxes. Ev side-eyeing it, bottom right. Yellow "????" and a curved arrow to the shirt. |
| 151K | What Happens If an NFL Team's Plane Goes Down? | A team walking up the stairs into a jet. Ev on the right, holding a manila folder stamped "DISASTER PLAN". Red curved arrow from him to the plane. |
| 121K | Everyone Was Wrong About the USA World Cup | A real tweet card ("...expose just how A SHITHOLE of a country the USA is", 4.8M views) over a ruined city on the left. Ev pointing at it, shocked, with a USA crowd on the right. |
| 87K | Caleb Williams Just Pulled a Michael Jordan | Two TVs: "NIKE 1985" and "CADDIX 2026", both with black "CENSORED" bars. Ev in the middle pointing at both. |

## What every one of them does
1. **One clear story you get in a second.** The thumbnail is a little scene, not a collage: the thing, the mystery, a reaction.
2. **A real, recognisable person or object** (Eli Manning with the trophy, Roger Goodell, a team plane, a T206 Honus Wagner card, a Miami jersey). Photoreal, bright, HD, cinematic lighting. Composited scenes look like one photo.
3. **The host's face reacting** in almost every one: side-eye, shocked hands on head, pointing, wincing. Cut out cleanly, sharp, big (about a third to half the frame height), usually on the right.
4. **Props and labels as physical objects, not floating text:**
   - a price tag ("$5,000,000", "$1M??", "$20M")
   - a stamped folder ("DISASTER PLAN")
   - a hang tag ("ILLEGAL")
   - a fine notice ("YOU'VE BEEN FINED · LATE HIT · $11,941")
   - tape labels ("NIKE 1985")
   - black "CENSORED" bars
   - an evidence bag
5. **Text: 1–3 words, huge.**
   - Heavy condensed sans with a black outline, or white on a red or black box.
   - Examples: "THIS IS LEGAL?", "50 BODIES", "BANNED", "SECRET LIVES", "$10M COACHING WAR".
   - Yellow is used for one keyword ("THE MONEY GO?").
   - Question marks and dollar amounts make the curiosity gap.
6. **Hand-drawn curved arrows** (white, red or yellow) pointing from the face or text to the reveal.
7. **Comparisons:** two things side by side with "VS" or two price tags ($1M vs $20M, NIKE 1985 vs CADDIX 2026).
8. **Clean and bright**, no clutter, nothing small. It still reads at phone size.

## How to apply it to The Erin Brown
- Build each thumbnail as **one scene with a reveal**: the athlete (real HD photo), the evidence as a physical prop (a tagged syringe, a stamped "POSITIVE" lab report, a price tag, a stopwatch frozen at 9.79), one or two big words, and a curved arrow.
- **The host's face:** Ev's thumbnails all have his own reacting face. If the user wants that, we need a few HD photos of them making the faces (side-eye, shocked, pointing, hands on head) on a plain background. Until then, use the athlete's own reaction photo in that spot.
- Real photos only (the user's rule). A composited background may be generated to set the scene (warehouse, lab, courtroom), but people and the key object stay real.
- Keep the earlier HD rules from `projects/banned-substances/thumbnail_research.md`: only ever downscale photos, light grading, sharp cutouts.

## Downfall videos: the "HE LOST EVERYTHING." style (user approved the concept, 11 Nov 2026)
Reference: `downfall_ref_internetjanitor.jpg` (InternetJanitor, Ben Shapiro, 1.7M views in 2 days). Demo: `downfall_demo_boling.jpg`.
- One huge, front-on close-up of the subject's face, centred, filling the frame, on a plain textured deep-blue background.
- 3 words across the top: a small white italic word on the left, a GIANT red block word over the forehead, and a white italic word on the right with a yellow marker underline.
- The face must be a real photo or video frame where the person already looks sad, shocked or defeated. Never paint on tears or change the expression.
- Build with `tools/thumb_downfall.py` (cut the face with rembg birefnet-portrait first, then frame it with `--crop`).
- Use it for downfall / fell-off / "what went wrong" videos. Keep the user's Boling style (stadium + action + face) for other videos.

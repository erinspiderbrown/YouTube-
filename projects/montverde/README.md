# Montverde Academy: "Swept Under the Rug" (podcast style)

Source footage: Dropbox folder "Issam Coach" (11:39 to-camera recording, post-race interview clip, 6 photos).

## Edit v4 (current): user feedback "too repetitive, too simple"
- Name cards **only on each person's first mention** (Gerald, Issam, Adaejah). Repeat cards removed.
- 13 animated motion graphics (`tools/mograph.py`):
  - Florida map with Montverde pin; Americas map routing 3 positive tests to Suriname / BVI / Jamaica.
  - "3 countries → 1 school" convergence; Africa map "target testing" (Kenya, Ethiopia).
  - Coach case-status stepper; "provisional suspension" dictionary card; coach ↔ athletic-director diagram.
  - Issam "What he lost" timeline; JADCO vs AIU/WADA comparison; GW1516 explainer.
  - Positive-test tracker (3, then 4); team grid "who got caught".
- More stock B-roll: plane (international travel), laptop/suit (LinkedIn), newspaper, lightning, start line.
- Transitions baked into every insert, cycling whip-pan / zoom-blur / RGB glitch / flash, with matching SFX. The A-roll gets motion blur around whips.
- A-roll punch-in zooms on every keyword and on extra emphasis beats. Subtle film grain over everything.
- Stock shots get a slow push-in so nothing sits static.

## Edit v3
- Ending cut after "this doping shit is a joke" (source 9:59). The "go dope / anti-doping is propaganda" section is removed. Runtime about 9:00.
- All 27 swear words before that point are muted (short fades, no bleep).
- Shadow removal ~4x faster: heavy work at half resolution, wall model refreshed every 3 frames.

## Edit v2
- **Wall shadow removed**: `tools/deshadow.py` fits a smooth model of the wall's lighting around the head and lifts the cast shadow up to it, frame by frame. Hair, skin, mic and poster are protected.
- **Animated name cards** (`tools/cards.py`) on every name mention, replacing the full-screen photos:
  - The photo pops in on screen-right. The orange name bar and role bar wipe in.
  - Stamps slam on: PROVISIONALLY SUSPENDED (Gerald), SUSPENDED (Issam), NIL DEAL SIGNED (Adaejah).
  - Each card has whoosh/pop/hit SFX.

## Edit v1
- Pauses tightened with jump cuts. Every cut changes framing between wide, medium and close-up. Crops come from 4K and are centred on the face (`tools/faces.py`).
- Colour and lighting: highlight roll-off on the white wall, lifted skin tones, slight warmth, soft light falloff around the subject.
- Cold open → title card ("Swept under the rug") → main story → end card.
- B-roll matched to the line being said: photos of Gerald Phiri, Issam Asinga and Adaejah Hodge, plus free Pexels stock (track, lab testing, water bottles, campus, gavel, Florida).
- Issam's post-race interview cut in right after the line about the Adidas deal, before "the week before that, he got suspended".
- Orange keyword bars, lower thirds for names, and a credit tag on the photo with a visible photographer watermark.
- Audio: voice cleanup (HPF, denoise, EQ, compression), no music (user removed it; `MUSIC_GAIN = 0`), synthesized whoosh/pop/hit SFX, loudness at -14 LUFS.

`build.py` holds the full edit decision list (B-roll, keywords, lower thirds) in source-time seconds. Edit it and re-run to change the cut.

## Stock credits (Pexels, free licence; credit in the description)
Mikhail Nilov, cottonbro studio, umar muazu, Yaroslav Shuraev, KoolShooters, K, CAPTKHO kho, Taryn Elliott,
RDNE Stock project, Pressmaster, Gustavo Fring, Roberto Zepeda, 2type, Ricky Esquivel, pickarick,
KATRIN BOLOVTSOVA, Riccardo Zerbinati.

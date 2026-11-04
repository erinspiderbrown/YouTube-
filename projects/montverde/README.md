# Montverde Academy: "Swept Under the Rug" (podcast style)

Source footage: Dropbox folder "Issam Coach" (11:39 to-camera recording, post-race interview clip, 6 photos).

## Edit v2 (current)
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
- Audio: voice cleanup (HPF, denoise, EQ, compression), AI-generated royalty-free music bed (vidIQ) ducked under voice, synthesized whoosh/pop/hit SFX, loudness at -14 LUFS.

`build.py` holds the full edit decision list (B-roll, keywords, lower thirds) in source-time seconds. Edit it and re-run to change the cut.

## Stock credits (Pexels, free licence; credit in the description)
Mikhail Nilov, cottonbro studio, umar muazu, Yaroslav Shuraev, KoolShooters, K, CAPTKHO kho, Taryn Elliott,
RDNE Stock project, Pressmaster, Gustavo Fring, Roberto Zepeda, 2type, Ricky Esquivel, pickarick,
KATRIN BOLOVTSOVA, Riccardo Zerbinati.

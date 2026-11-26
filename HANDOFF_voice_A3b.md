# Erin Brown voice: approved setup "A3b" (26 Nov 2026, used on the Cooper Lutkenhaus video)

Paste this into any chat that needs to read a script in Erin's voice.

## ElevenLabs settings
- Voice: **Erin Brown 2026**, voice_id `uBqzFhqGLj9GteaUaPDl` (Instant Voice Clone on Erin's own ElevenLabs account)
- Model: `eleven_v4`
- voice_settings: `{"stability": 0.4, "similarity": 0.9}` (the key is `similarity`, not `similarity_boost`; read the node back before running)
- Put this tag at the start of every part (one generation per part):
  `[casual Black Texas accent, talking to a friend, laid-back, not hyped, unhurried]`

## How to write the text for the voice
- Light respelling, only on key words: "junya" (junior), "Texis" (Texas), "hunnid" (hundred), drop the g ("runnin'", "watchin'"), drop "is" where Erin would ("he seventeen", "he doin' right now").
- Keep normal "the / this / that / with". Do NOT write da/dis/dat/wit: it sounded weird.
- Numbers and years as words ("one forty-two point two seven", "twenty twenty-five", "eight hunnid").
- Erin has watched track/followed it for under 10 years: never "my whole life".
- Casual, how Erin talks: "y'all", "ain't", "'cause", "gon'", "I really feel like", "honestly". No "Man,"/"Aight" warm-up openers.

## After generating
1. Slow it a tad: `ffmpeg -i part.mp3 -filter:a atempo=0.94 part_slow.wav`
2. Natural pauses: `python3 tools/match_rhythm.py part_slow.wav part_rhythm.wav` (in the YouTube- repo; it only lengthens pauses toward ~0.7 s, never slows words)
3. Join the parts with 0.9 s of silence between them.
4. Loudness: `ffmpeg -i joined.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 vo.wav`
5. Keep a dark music bed under it (it hides small AI artifacts).

Erin's feedback that led here: the earlier takes were "too proper" (Junior, Texas, everything), then "a bit fast and a bit too enthusiastic". A3b fixed both.

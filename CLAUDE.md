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
- Reference for the intro (first ~30 sec): https://youtu.be/9H7itfichRg (see `examples/links.md`).

### 2. Documentary style (voiceover, user not on screen)
- The user reads a script as a voiceover. They do not appear on camera.
- B-roll comes from two places:
  - Footage the user provides.
  - Footage Claude finds or makes.
- **The user says exactly what they want.** Follow their shot-by-shot directions. Don't make up creative choices they didn't ask for. If a direction is unclear, ask.

## Reference examples
- `examples/podcast/`: example videos/clips for podcast style.
- `examples/documentary/`: example videos/clips for documentary style.
- `examples/links.md`: YouTube links and notes on what to study in each one.

Note: this cloud environment can't download YouTube videos directly (YouTube returns 403).
Frame-by-frame study needs the clips saved as files in the repo (keep each under 100 MB, or use Git LFS).

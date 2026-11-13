---
name: talking-head-video-vox-style-edit
description: Edit a person's own talking-head footage (founder / expert to camera) into a vertical 9:16 Instagram Reel in Vox-style newspaper collage — tightened jump-cut A-roll, the speaker as a picture-in-picture circle that morphs to full screen and back, full-screen collage scenes and infographics for most lines (face on screen only 20–40 %), torn-paper word-by-word captions, brand colours only, lo-fi music and sparse SFX, rendered with HyperFrames. Use when the user uploads talking-head/selfie footage and wants it "edited for Reels", "Vox style", "with motion plates / motion graphics", "explainer", "B-roll/infographics over me", or "less of my face" (reference: SM explainer/).
---

# Talking-head video → Vox-style Reel edit

Reference build: `SM explainer/` (87 s, Purple Seed founder, "the only content that works on social media").
Read its `TREATMENT.md`, `index.html` and `audio/mix.py` before starting — copy patterns, don't reinvent.
Visual language comes from `thirty-one-years/` (see the `collage-story-video` skill for the collage look).

## The format (what the user approved)
- 9:16, 1080×1920, 30 fps. Length = everything they say, tightened (pauses → 0.2 s jump cuts). No VO, no script
  rewriting — the footage *is* the script.
- **Face on screen 20–40 %.** Full-screen face only on direct-to-camera beats: the hook (credentials), each
  "First / Second / Lastly" or punchline line, the CTA line. Everything else is a collage scene.
- **Speaker as a PiP circle** over every collage scene: centre (240,1310), r=185, 12 px paper border + 7 px brand ring
  + offset shadow; bottom-left so it clears Instagram's right-hand buttons and bottom caption zone. The circle
  **morphs** (0.62 s, expo.inOut) between full screen ↔ circle ↔ taped photo at every switch. First version
  (r=140, tight) "looked funny" — keep head + shoulders with air around them. No jump-cut punch-ins inside the circle.
- **Three screen modes**: `face` (full screen + overlay plates in the sky/top zone y≈120–440 and the chest zone),
  `pip` (collage scene underneath, circle on top), `photo` (speaker shrinks into a taped, torn-edged photo under a
  headline — use once or twice for variety).
- **Collage scenes**: halftone cut-outs duotoned to ink→paper on warm newsprint, Playfair headlines, labels on
  brand-colour bars (Montserrat Black), Permanent Marker scribbles, Caveat notes, Courier stamps/counters,
  big brand-colour circle behind the hero object, ink arrows/strings drawn on, highlighter swipes, torn-paper
  wipes (brand colour) between consecutive collage scenes. Infographics are code, not art: counters/odometers,
  meters, bar charts, growth curves, Venn diagrams, calendars, thought bubbles, phones with live HTML screens.
- **Captions**: torn paper strips at y≈1590, 1–4 words per chunk, active word = brand-colour box with paper text.
  Hidden only while a headline spells out the same line.
- **People in art = modern metro-city consumers** in contemporary clothes (the user rejected "Indian villagers" —
  traditional dress/rural look). Say "modern urban [country] metro-city people in contemporary western clothing".
  If the market is specific (e.g. India), also ask for the ethnicity explicitly — generations drifted Western.
- No client logo unless they ask; third-party brands as typed text only (no logos/packaging).
- **Music**: lo-fi hip-hop bed (user's pick for explainers). **SFX: sparse and quiet** — the user found ~150 cues
  "forced" and loud; the approved version has ~35 (one every 2–3 s at most) at −6 dB: circle swishes, torn-paper
  wipes, section stamps, a counter tick, 4–6 "action" sounds (switch, plug, TV, page flip, tap/ding). No pops on
  every element, no marker squeaks, no typewriter.

## Workflow — approval at every ★ (the user asked to go step by step)
1. **Folder + ingest.** Create the project folder (with `footage/`). GitHub's web upload caps files at **25 MB** —
   ask for a Google Drive/Dropbox link instead. Allow `drive.google.com` + `drive.usercontent.google.com` with
   `update_environment`; `gdown` folder listing works but its downloads redirect to `doc-*-docs.googleusercontent.com`
   (blocked, wildcard) — download each file id with
   `curl -L "https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t"`.
   Gitignore raw footage (`footage/*.mp4`, `work/`, `renders/`, `previews/`, `art/raw/`, `art/rb/`, `.hyperframes/`).
2. **Brand.** Pull palette + fonts from the client's site CSS (count hex frequency in their stylesheets; allow the
   host with `update_environment` if blocked). Ask for the logo only if they want it on screen.
3. **Transcribe** — `scripts/transcribe.py <project>` (ElevenLabs Scribe, word timestamps; key is proxy-injected).
4. ★ **A-roll** — `scripts/cut.py <project>` → tightened `work/aroll_hold.mp4` + `work/voice.wav` + `edl.json` +
   `transcript.json`. Send a 540×960 preview (`previews/01-tight-cut.mp4`), list what was cut, ask for approval.
5. ★ **Plate plan** — table: time · line · screen mode · plate. Mark face beats to land inside 20–40 %, report the %.
   Offer B-roll options with real costs (AI video ≈35 credits / 5 s on Higgsfield; cut-outs ≈3 credits each, or
   ≈0.75 each when generated 4-per-sheet). The approved answer was **all collage + infographics + PiP circle**.
6. **Art** — Higgsfield `nano_banana_pro`, 2k, 2 credits per sheet: put 2–4 *separate, well-spaced* clippings on one
   sheet (prompt: see `reference/patterns.md`), `remove_background` (1 credit; submit in waves ≤4), then
   `scripts/prep_art.py` splits by connected components, trims, duotones into the palette (`--keep-yellow` for a
   solid-yellow phone/TV screen you'll overlay with HTML) and writes WebP. Check `get_preferences` before the first
   generation; quote credits up front.
7. ★ **Build in batches** (intro, then one batch per section/pillar, then outro). For each batch: build scenes,
   `npx hyperframes snapshot --at …`, read the contact sheet, fix overlaps/off-screen text/early reveals, render
   just that span (`render --start A --end B --workers 2`), downscale to 540×960, send, wait for approval.
8. ★ **Music + SFX** — ask the vibe (lo-fi recommended), `scripts/score_lofi.py`, `scripts/sfx.py`, cue list →
   `scripts/mix.py` (−14 LUFS, −1 dBTP). Point `<audio>` at `audio/mix.wav`, full render, re-encode
   `-crf 20 -preset slow` (≈75 MB for 87 s, under GitHub's 100 MB), `.srt`, `TREATMENT.md`, `CREDITS`, commit, push.
9. Audio-only revisions: don't re-render — remix and remux (`ffmpeg -i final.mp4 -i audio/mix.wav -map 0:v -map 1:a
   -c:v copy -c:a aac -b:a 192k`).

## Gotchas (all hit on the reference build)
- **One big ffmpeg graph with 30+ trims of the same input gets OOM-killed** — encode each segment separately,
  frame-quantise boundaries (round to 1/30 s) and concat; don't use `-shortest` (it dropped 3 frames).
- **HyperFrames copies the whole project into its render plan (2 GB cap → `PLAN_TOO_LARGE`)** — keep raw takes,
  intermediate segments, old renders and raw art *outside* the project folder (e.g. `/home/user/<proj>-raw/`).
- The A-roll must outlast the last morph: hold the last frame (`tpad=stop_mode=clone:stop_duration=2.3`) or the
  circle turns black over the end card. Re-encode with `-g 30` (sparse keyframes warning).
- Don't give the camera wrapper its own `data-start` — `video_nested_in_timed_element`. Only the `<video>` is timed.
- A collage scene that starts before its tear covers the previous scene — start each scene at the tear's midpoint.
- `stroke-dasharray` dotted lines can't be dash-drawn; reveal them with an animated `clip-path: inset()` instead.
- Elements animated in with `fromTo` from a small y offset are visible before their start — offset far off-screen.
- Bash safety check rejects heredocs containing backticks/`$$` — write edit scripts with the file tool, then run them.
- ElevenLabs sound-generation needs `duration_seconds ≥ 0.5`; a failed request leaves a 0-byte file the next run
  skips — delete empties before re-running.
- Mid-video morph timing: start each camera transition ~0.25 s before the line boundary so it lands on the cut.
- Never fabricate stats: on-screen numbers come only from what the speaker says (or told you, e.g. "9 years").
- Proofread the transcript before captions: Scribe mishears brand names (a short clip gave "Purple Seat") and
  writes numbers as digits ("1,500") — fix the words in `transcript.json`, then rerun `captions.py`.

## Files
- `scripts/transcribe.py` — per-take audio → ElevenLabs Scribe JSON (`work/audio/*.json`).
- `scripts/cut.py` — tighten takes into the A-roll (gap max 0.32 s → 0.2 s, 12 ms audio fades, light voice clean-up).
- `scripts/captions.py` — transcript → `data.js` (caption chunks, cut points) + `.srt`.
- `scripts/duotone.py`, `scripts/prep_art.py` — palette duotone, sheet splitting, WebP.
- `scripts/score_lofi.py` — parameterised lo-fi bed (filter-open hook, drum drops, end ring-out).
- `scripts/sfx.py` — paper/UI SFX kit (ElevenLabs). `scripts/mix.py` — voice + ducked music + `cues.json`.
- `reference/patterns.md` — camera-mode maths, caption/tear/ink helpers, art prompts, layout zones.

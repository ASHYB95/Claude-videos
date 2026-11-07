---
name: collage-story-video
description: Make a story-led, emotional, animated (no live footage) vertical brand video in Vox-style newspaper collage — halftone photo cut-outs on newsprint, serif headlines, marker scribbles, torn notes — duotoned into brand colours only, with narration plus character voices (ElevenLabs), piano/strings score and paper foley, rendered with HyperFrames. Use when the user wants a "real situation" story, emotion-led brand film, Vox/collage/paper-cut style, or animated documentary look (reference: thirty-one-years/).
---

# Collage story video (Vox-style, brand colours only)

Reference build: `thirty-one-years/` (61 s). Read its `index.html`, `TREATMENT.md`, `art/` and `audio/` first.

## The look (what the user approved — and what they rejected)
- ✅ **Black-and-white halftone photo cut-outs** (people, hands, objects) with rough paper edges; torn rectangular "clippings"; newsprint + graph-paper grounds; big high-contrast serif (Playfair Display 900/italic); bold labels on yellow bars (Figtree); Permanent Marker scribbles; Caveat handwritten notes; Courier stamps; a big brand-yellow circle behind the subject.
- ✅ **Brand colours only**: every photo duotoned charcoal → cream (`scripts/duotone.py`); accents only from the brand palette (yellow primary, pastels secondary). No red, no colour emoji.
- ❌ Cute cartoon/sticker illustration. ❌ **Green-screen backgrounds** — generate elements on newsprint and cut them out with Higgsfield `remove_background` (~1 credit each).
- Motion: slow pushes, clippings slide/settle with back-ease, ink drawn on as it's spoken (SVG `pathLength="1"` + `strokeDashoffset`), highlighter swipes (background-size), torn-paper wipes between scenes (a brand-yellow tear for the product "turn"), stop-motion grain (`ease:'steps(N)'`), motion blur.

## Story structure (~45–60 s)
Who they are (warmth, specifics) → the problem (scattered people, the envelope fails) → the product as the turn (one link, QR) → the payoff is emotional, not monetary (messages, read twice) → brand tagline + CTA. Real quotes read by **different voices** land hardest.

## Workflow (approval at each ★)
1. Research brand (copy, claims, palette, logo/mascot) as in `screen-led-promo-ad` step 1.
2. ★ Script table (time · VO · visual). Narrator e.g. ElevenLabs "George" (warm storyteller), speed ~0.97; quotes with other voices.
3. ★ Storyboard before audio: build the animated `index.html` and present **real frames** as a storyboard sheet.
4. **Art on Higgsfield** (`nano_banana_pro`, 2k, ~2 credits): first make a character anchor, then reference it (`medias:[{role:'image_references', value:<job_id>}]`) for every other shot of that character. Prompt base: "Vintage newspaper collage clipping: black-and-white halftone photograph printed on aged newsprint, coarse halftone dots, high contrast, cut out roughly along the outline with a thin torn paper edge, lying flat on crumpled old newspaper pages with faint illegible small print. Grayscale only. No readable text." Spot-colour items (pencil, phone screen) → "painted solid #F9B910".
   - Pro plan allows **4 concurrent jobs**: batch generation queues, but `remove_background` errors — submit in waves of 4.
   - A phone with a solid-yellow screen lets you detect the screen rect and overlay a live HTML app screen.
5. `scripts/prep_cutouts.py` pattern: trim, downscale ≤1100 px, split multi-clipping sheets by connected components, duotone (`--keep-yellow` for accents); flat textures → JPEG.
6. Build: scenes as `.clip` divs, `tearAt(T)` transitions, layout-dependent ink computed from `offsetLeft/Top` (not getBoundingClientRect). **Torn edges must be percentage-based clip-paths** (pixel ones measured before images load clipped the logo). Give logo `<img>` explicit width+height.
7. Audio: `scripts/score_emotional.py` (piano + strings, bar length set so a bar lands on the turn; strings enter at the turn, dip under quotes, swell at the payoff), `scripts/sfx.py` (tear, tape, marker, stamp, typewriter, pencil, slide, flutter, pin), `scripts/mix.py`. Keep scribble/pencil SFX **low** (user asked to cut them).
8. Render (~7 min); the grain makes files huge (~180 MB) → re-encode `-crf 20 -preset slow` (~50 MB, SSIM ≈0.98) to stay under GitHub's 100 MB. `.srt` from alignment, `CREDITS`, commit.

## Gotchas
- The Bash safety check rejects heredocs containing backticks/`$$` — write scripts with the file tool.
- Characters, companies and quotes are fictional; never fabricate stats.

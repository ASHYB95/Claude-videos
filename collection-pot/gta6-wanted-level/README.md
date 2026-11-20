# GTA 6 week: "Things that raised your wanted level this week" (Instagram carousel)

Topical, no hard sell. 6 slides, 1080×1350, built as one 6480×1350 strip in `carousel.html` and sliced by `render.js`.

**Brand (Collection Pot Brand Guidelines, Nov 2026):** Pot of Gold #F9B910, Work Bash Black #2F2F32, Wedding White #FFFCF8.
Layouts follow guidelines p.44 "The Pot as a background" (`ref/guidelines-p44-pot-as-background.jpg`): the official Pot
(`brand/PotShape.svg`) is scaled far beyond the frame so its straight shoulders and soft base divide each slide into gold and
white, and every slide divides the space differently (white wedge · gold rising · gold base above · white corner · giant tilted
Pot · Pot corner holding the logo). Small solid/outlined Pots and sparkles act as punctuation next to Chip.
Official stacked logo (`brand/LogoStacked.svg`). Sentence-case headlines (Figtree Black standing in for Faro Display Lucky).
No free-form blobs or waves. Previous version (Pots in a continuous strip) kept as `carousel-v2-strip.html`.

| # | Copy | Wanted level | Chip |
|---|---|---|---|
| 1 | Things that raised your **wanted level** this week: | ★★★★★★ | placeholder (wink) → *final: guilty, hiding a controller* |
| 2 | 01. Blocking out Thursday 9–5 as **"Deep focus. Do not disturb."** | ★★★☆☆☆ | placeholder (proud) → *final: headphones + coffee* |
| 3 | 02. Buying a mouse jiggler so your Teams status stays green **while you're in Vice City.** | ★★★★★☆ | ✅ final: gaming on a beanbag |
| 4 | 03. Camera off for Friday's all-hands: **"Sorry, my Wi-Fi's really bad today."** | ★★☆☆☆☆ | placeholder (happy) → *final: innocent shrug + laptop* |
| 5 | 04. Coming down with the Thursday–Friday flu. **The whole team. Same day.** | ★★★★★★ | placeholder (excited) → *final: blanket + thermometer, controller peeking out* |
| 6 | Stay safe out there. **HR is watching.** | ★★★★★★ | placeholder (wave) → *final: binoculars* |

## Caption
GTA 6 dropped and suddenly everyone's Wi-Fi is "really bad" 👀
What's your wanted level this week? Tag the colleague who's on six stars. ⭐⭐⭐⭐⭐⭐

## Guardrails
No Rockstar/GTA logos, art, characters or fonts; the wanted-level stars and "Vice City" carry the reference.

## Chip's face (brand rule)
Chip's white eye patches are shaped like an **upside-down Pot** (rounded dome on top, straight sides tapering down
towards the beak), as in `ref/chip-eyes-reference.jpg`. The current Chips had round patches, so `chip/fix_face.py`
paints the old face out and fits the reference face (eye patches, pupils, beak) onto each head; `--wink` closes the
right eye. Originals are in `chip/orig/`. Run it on any new Chip render that comes out with round eyes:
`python3 -I chip/fix_face.py in.png out.png [--wink] --blur 1.2` (use `--blur 0.6` for sharp, high-res renders).
When generating new Chips, add to the prompt: "white eye patches shaped like an upside-down pot (rounded top, straight
sides tapering towards the beak), not round".

## Finishing the Chip poses (needs ~16 Higgsfield credits)
Placeholders are cut from `ref/chip-character-sheet.png` (low-res). To replace them:
1. Generate with `nano_banana_pro`, 1:1, 2k, `image_references` = the uploaded character sheet (Higgsfield media `cd43c0d6-6f50-4f3e-a7ab-c81ead87bee9`).
   Prompt base: *"Chip, the exact penguin mascot from the reference character sheet: soft matte 3D clay-like render, black body, white belly, signature double quiff, big round eyes, orange-yellow beak, yellow feet. Full body. Pose: …  Soft studio lighting, gentle contact shadow. Isolated on a plain flat light grey background. No text, no logos."*
   Poses: guilty with a controller behind his back · yellow headphones, eyes closed, coffee mug · innocent shrug, laptop under wing · pink blanket burrito, thermometer in beak, controller peeking out · peering through binoculars.
2. Cut out for free: `python3 -I chip/cutout.py raw.png chip/<name>.png --tol 18`
3. Swap the `src` in `carousel.html`, then `node render.js` → `out/gta6-01.png … gta6-06.png`.

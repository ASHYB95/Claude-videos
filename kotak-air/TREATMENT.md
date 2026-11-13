# Kotak Air Credit Card — Key Features (built)

Internal refresher for the Kotak credit card sales team: features and USPs in 39 s, key conditions as footnotes.
1080×1920 · 39 s · VO: Alice (ElevenLabs, English) · Script: SCRIPT.md · Facts: FACTS.md · Storyboard: storyboard/storyboard.jpg

## Look
- Light studio sweep (white → #e4eaf2) with a faint warm red glow behind the card; colour Kotak logo top-centre.
- Two-tone headlines: red eyebrow ("01 · EARN ON TRAVEL"), red key number, navy supporting line. Roboto 900/700.
- Real Kotak Air card (brand/kotak-air-card.png — cut from the site hero, name removed, 2× upscaled), floating in 3D with a floor shadow; poses per beat.
- White rounded panels with red icons on soft-red circles; scalloped white stickers (NO CAP, 4 lounges, 1% fuel, ₹0 joining fee).
- Conditions as grey footnotes (28 px) — reference text the team can pause on.

## Build notes
- Brand: navy #003974, red #ED1C24 (from the site's logo SVG), Roboto (site font; latin-ext subset for ₹).
- ElevenLabs is on the free plan: library voices and Voice Design are blocked via the API, so the VO uses the premade "Alice".
- Network: environment "claude-videos" allows www.kotak.bank.in, kotak.bank.in, images.kotak.bank.in, www.kotak.com, kotak.com.

## Regenerate
voices/tts.py → audio/sfx.py → audio/score.py → audio/mix.py → voices/srt.py →
`npx hyperframes render -q delivery -o renders/kotak-air.mp4`

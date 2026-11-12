# OneClickDrive — "One Click Away" (approved, built)

Screens-only promo: no footage. Rebuilt oneclickdrive.com screens in a 3D phone on a brand stage, kinetic type, 3D pop-outs.
1080×1920 · 32.6 s · VO: Sarah (ElevenLabs) · prices in AED. Script: SCRIPT.md · Storyboard: storyboard/storyboard.jpg

## Build notes
- Real flow from the live site: Home → RENT SPORTS tile → Sports Cars listing (Porsche 718 Boxster 2024, AED 649/day) → WhatsApp button (pre-filled message to the supplier).
- No timer on the steps (the site makes no booking-time claim) — a 3-segment progress bar instead.
- Claims on screen are all from the site; "*" footnote: rates, deposits & delivery are set by each supplier.
- Brand: orange #ed8413 (fills), deep orange #cc4700 (text on light, for contrast), charcoal #373737, Mulish.
- Screen UI is marked data-layout-ignore (it is texture at phone scale); pop-outs carry data-layout-allow-overlap.
- Network: environment "claude-videos" allows www.oneclickdrive.com, media.oneclickdrive.com, static.oneclickdrive.com.
- Currency: set cookie currency=AED before capturing (the site defaults to USD by geo).

## Regenerate
voices/tts.py → audio/sfx.py → audio/score.py → audio/mix.py → voices/srt.py →
`npx hyperframes render -q delivery -o renders/oneclickdrive.mp4`

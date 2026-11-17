# Collection Pot — "Gift Card on Send" (approved storyboard v1, built)

Territory: poor gift giving / product feature. 1080×1920 · ≈24 s · VO: Alice (ElevenLabs). Brand guidelines Nov 2026 applied.

| # | Time | Visual | VO |
|---|---|---|---|
| 1 | 0–3.5 | B-roll (POV, no faces): a hand holds a "World's Best Boss" mug; the other hand opens the cupboard: it is already packed with the same mug. "World's best boss…" / "World's worst gift." (worst in gold) | "World's best boss… world's worst gift." |
| 2 | 3.1–3.8 | Gold Pot shape grows out of the mug and fills the frame | – |
| 3 | 3.5–6.8 | Phone rises onto gold stage: Jo's leaving Pot · £185 · 14 chipped in. "The panic-buy era is over." | "The era of the panic-bought office gift is over." |
| 4 | 6.8–9.2 | Push-in, tap SEND THE POT. Card: "Everyone chips in…" | "With Collection Pot, everyone chips in," |
| 5 | 9.2–11.9 | Send options; Gift Card on Send · NEW selected. "…then add a gift card on send." + sticker | "and you attach a gift card when you send the Pot." |
| 6 | 11.9–13.9 | Pick a gift card: M&S, £185. "Pick one they'll actually want." | "Pick one they'll actually want," |
| 7 | 13.9–15.6 | Message types out, push-in, tap SEND. Card: "Add a heartfelt message… and send." | "add a heartfelt message, and send." |
| 8 | 15.6–18.9 | Pot sent; M&S e-gift card + messages pop out in 3D, Pot confetti. "They pick the gift. You all get the credit." | same |
| 9 | 18.9–23.8 | End card: gold + cream Pot crop, logo fades in, "Easy to sort. Impossible to forget.", CREATE A POT, collectionpot.com | "Collection Pot. Easy to sort. Impossible to forget." |

## Regenerate
`python3 src/build.py` (index.src.html → index.html) → voices/tts.py → audio/sfx.py → audio/score.py → audio/mix.py →
`npx hyperframes render -q delivery -o renders/collection-pot-giftcard.mp4`

Timings shared by `src/index.src.html` and `audio/mix.py` (VO starts 0.30 / 3.65 / 6.85 / 12.15 / 16.45 / 19.15 s).

## Fonts
`fonts/Faro-DisplayLucky.woff2` is the client-licensed headline font and is **not committed** (public repo). Copy it into `fonts/` before rendering; without it headlines fall back to the system font.

## v2 client notes (applied)
- Opening text reads "World's best boss…" / "World's worst gift."
- Headlines hand over cleanly (each is out before the next comes in).
- Logo simply fades in (no Pot-into-O build).
- All SFX −6 dB (half amplitude) via `SFX_GAIN` in audio/mix.py.

## v3 client note (applied)
- No human faces: opener replaced with a POV cupboard reveal (GPT Image 2.6 start/end keyframes → Seedance 2.5, 4 s, 1080p). Door + mug-clink SFX replace the tissue rustle.

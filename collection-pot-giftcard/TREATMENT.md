# Collection Pot — "Gift Card on Send" (approved storyboard v1, built)

Territory: poor gift giving / product feature. 1080×1920 · ≈24 s · VO: Alice (ElevenLabs). Brand guidelines Nov 2026 applied.

| # | Time | Visual | VO |
|---|---|---|---|
| 1 | 0–3.5 | B-roll: boss lifts a "World's Best Boss" mug from a gift box, smile → grimace. "World's best boss…" + expressive "Worst gift." | "World's best boss… world's worst gift." |
| 2 | 3.1–3.8 | Gold Pot shape grows from the gift box and fills the frame | – |
| 3 | 3.5–6.8 | Phone rises onto gold stage: Jo's leaving Pot · £185 · 14 chipped in. "The panic-buy era is over." | "The era of the panic-bought office gift is over." |
| 4 | 6.8–9.2 | Push-in, tap SEND THE POT. Card: "Everyone chips in…" | "With Collection Pot, everyone chips in," |
| 5 | 9.2–11.9 | Send options; Gift Card on Send · NEW selected. "…then add a gift card on send." + sticker | "and you attach a gift card when you send the Pot." |
| 6 | 11.9–13.9 | Pick a gift card: M&S, £185. "Pick one they'll actually want." | "Pick one they'll actually want," |
| 7 | 13.9–15.6 | Message types out, push-in, tap SEND. Card: "Add a heartfelt message… and send." | "add a heartfelt message, and send." |
| 8 | 15.6–18.9 | Pot sent; M&S e-gift card + messages pop out in 3D, Pot confetti. "They pick the gift. You all get the credit." | same |
| 9 | 18.9–23.8 | End card: gold + cream Pot crop, logo builds (Pot pops into the O), "Easy to sort. Impossible to forget.", CREATE A POT, collectionpot.com | "Collection Pot. Easy to sort. Impossible to forget." |

## Regenerate
`python3 src/build.py` (index.src.html → index.html) → voices/tts.py → audio/sfx.py → audio/score.py → audio/mix.py →
`npx hyperframes render -q delivery -o renders/collection-pot-giftcard.mp4`

Timings shared by `src/index.src.html` and `audio/mix.py` (VO starts 0.30 / 3.65 / 6.85 / 12.15 / 16.45 / 19.15 s).

## Fonts
`fonts/Faro-DisplayLucky.woff2` is the client-licensed headline font and is **not committed** (public repo). Copy it into `fonts/` before rendering; without it headlines fall back to the system font.

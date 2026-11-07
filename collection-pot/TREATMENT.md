# Collection Pot — "Set Up in Under a Minute" (approved v2, built)

Screen-led walkthrough with AI B-roll (Higgsfield). 1080×1920 (9:16) · ~35 s · VO: Alice (ElevenLabs).
Real collectionpot.com screens (reference/screens) shown in a phone; cinematic B-roll between them.

| # | Time | Visual | VO |
|---|---|---|---|
| 1 | 0–4 | B-roll: office envelope passed desk to desk, someone hunting for change | "Organising a leaving gift? Forget the envelope doing laps of the office." |
| 2 | 4–7 | B-roll → phone: hand picks up phone, push into screen | "With Collection Pot, you can set one up in under a minute." |
| 3 | 7–10 | Screen: "What can we help with?" → tap Leaver | "Pick the occasion…" |
| 4 | 10–14 | Screen: "Should everyone chip in?" → "Chipping in money is optional", GBP | "…choose money, messages, or both…" |
| 5 | 14–18 | Screen: Pot page, "Invite others" → link + QR pop out | "…then share one link, or a QR code, with the whole team." |
| 6 | 18–22 | B-roll: colleagues tapping phones at desks; remote worker smiling at laptop | "Everyone chips in and signs the card, wherever they are." |
| 7 | 22–27 | Screen: demo Pot message wall → spend options | "Then cash it out free, or send it as an e-gift for sixty-plus retailers." |
| 8 | 27–31 | B-roll: leaver reading messages, laughing; team cheers | "Less admin. More celebrating." |
| 9 | 31–35 | End card: Chip, logo, CREATE A POT, collectionpot.com | "Collection Pot. Collect together, celebrate together. Create yours free today." |

## Brand
Charcoal #2f2f32 · cream #fffcf8 · pot yellow #f9b910 · pastels pink #f0abd1, mint #bcefe1, lilac #cfb0f0, orange #fc9e59, sky #a3def5 · headline font Faro Bold (commercial; pick an OFL look-alike) + Inter · mascot Chip the penguin (reference/brand).

## Notes for the next session
- Higgsfield MCP must be connected as a claude.ai connector (https://mcp.higgsfield.ai/mcp) before starting the session.
- Environment "claude-videos" allows www/app.collectionpot.com and collectionpot-static.b-cdn.net.
- Headless Chrome on collectionpot.com 404s some /_next/static chunks; reference/capture-flow.js routes those through curl.
- Create flow seen so far: occasion → "Should everyone chip in?" + currency → (further steps not yet captured; stop before sign-up).

## Build (as made)
- Fast cut: B-roll shots on screen 1.0–2.8 s each; whip pans, a match cut through the phone screen, yellow and double (yellow + charcoal) wipes.
- Clip 2 screen replacement: the real collectionpot.com homepage is tracked onto the phone in the hand, then the cut goes through the screen into the 3D phone.
- Setup shown as 3 steps with a running 0:00 → 0:48 timer; screens rebuilt on-brand (cream #fffcf8, charcoal #2f2f32, yellow #f9b910, Figtree Black + Inter, real occasion icons, Chip avatars, real QR to collectionpot.com).
- Camera: push-ins that follow each tap, tilt down to NEXT, pull-backs for 3D pop-outs (link, QR, team, messages, spend cards).
- Audio: VO at 1.08× pace, music 120 BPM C major, ducked under VO, mastered to -14 LUFS.
- Regenerate: voices/tts.py → audio/sfx.py → audio/score.py → audio/mix.py → `npx hyperframes render -q delivery -o renders/collection-pot.mp4`.

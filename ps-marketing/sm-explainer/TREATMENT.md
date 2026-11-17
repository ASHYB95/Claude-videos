# The Only Content That Works — Purple Seed (SM explainer, ~87 s, 9:16 Reel)

Founder talking head + Vox-style newspaper-collage plates. Face on screen ~24 % of the time (full screen
only on the punchy direct-to-camera beats); the rest he's a picture-in-picture circle (bottom-left, purple
ring) over collage scenes, with circle ↔ full-screen morphs at every switch. Torn-paper captions throughout.

**Look:** halftone cut-outs duotoned to ink #222024 → paper (scripts/duotone.py) on warm newsprint; accents
from purpleseed.in only — purple #6c2ea4, yellow #fec42d, lilac #cdb7e6. Playfair Display (headlines),
Montserrat Black (labels, stand-in for the site's Gotham), Permanent Marker, Caveat, Courier Prime.
No Purple Seed logo (by request); no third-party logos — brand names appear as typed text only.

**Sound:** original lo-fi hip-hop bed (audio/score_lofi.py, 84 BPM, Dm9–G13–Cmaj9–Am9), ducked −8 dB under
speech, one-beat drum drops before each pillar card; paper/UI foley (audio/sfx.py, ElevenLabs);
audio/mix.py → mix.wav at −14 LUFS / −1 dBTP.

| Time | He says | Screen |
|---|---|---|
| 0:00 | "At Purple Seed… fifteen hundred brands" | Face · "Founder, Purple Seed" tag → 1,500 BRANDS counter, "in 9 years!" |
| 0:04 | "…every major social platform" | PiP · hand + phone feed on a purple circle, 7 platform names pinned with ink strings |
| 0:08 | "And here's what we've understood" | Face |
| 0:10 | "…the only content that works on social media" | Taped photo · headline builds, *works* highlighted, cards 01/02/03 |
| 0:13 | "First, educational content" | PiP · 01 stamp, *Educational content.*, lightbulb switches on |
| 0:17 | "…leave them with value… teach them" | Crowd "your audience", value meter fills, book + "Did you know?" |
| 0:23 | Whole Truth Foods example | Generic pouch + INGREDIENTS label, consumer, dotted journey, magnifier, circled label |
| 0:32 | "Second is emotional content" | Face · 02 stamp, EMOTIONAL, theatre masks |
| 0:34 | "smile, cry, laugh, empathetic, sympathetic" | PiP · contact sheet, each portrait stamped on its word |
| 0:38 | "…come back for more. Humans are emotional creatures." | Face · yellow note → headline |
| 0:42 | Humans of Bombay / New York | PiP · pinned street portraits, 100,000s followers, growth curve "almost overnight!", *feel something.* |
| 0:52 | "And lastly, topical content" | 03 stamp, *Topical content.*, tear-off calendar flips |
| 0:54 | "…the best out of the three" | Face · cards 01/02/03, 03 circled "the best one!" |
| 0:58 | "…IPL, Diwali, Christmas" | PiP · crowd's thought bubble fills: cricket ball + bat, diya, bauble |
| 1:03 | "plug in your product… really, really well" | Hand plugs "your product / service" in (spark), "the feeling ✓", results bars |
| 1:10 | "…a brand trying to integrate IPL" | Vintage TV, live stadium, YOUR BRAND × IPL banner, BRAND × IPL stamps |
| 1:14 | "into their brand story. It just works" | Face · IT JUST WORKS ✓ stamp |
| 1:16 | "merge two or three of these pillars…" | PiP · three paper circles merge into a Venn, star = "each piece of content" |
| 1:22 | "…going viral" | Face · *viral* ↗ strip |
| 1:24 | (end card) | Follow *for more.* — phone profile, FOLLOW → FOLLOWING ✓ |

## Rebuild
1. Put the five takes (Drive folder) in `footage/`, then `python3 scripts/cut.py` → `edl.json`, `transcript.json`,
   `work/voice.wav`, `work/aroll_hold.mp4` (transcription: ElevenLabs Scribe → `work/audio/*.json`).
2. `python3 scripts/captions.py` → `data.js`, `SM-explainer.srt`.
3. `python3 audio/score_lofi.py && python3 audio/mix.py`.
4. `npm run check`, then `npx hyperframes render -o renders/full.mp4` (keep raw takes/renders out of the folder:
   the renderer copies the whole project into its plan and caps it at 2 GB).

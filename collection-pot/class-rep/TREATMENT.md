# Class Rep — Collection Pot (awkward-organiser story, 39.4 s, 9:16)

Vox-style animated newspaper collage (`collage-story-video` skill). Jo, the Year 3 class rep, tells it herself like a voice note to a friend; the brand is only a plug at the end.
Brand: Collection Pot Brand Guidelines (Nov 2026) — Pot of Gold #F9B910, Work Bash Black #2F2F32, Wedding White #FFFCF8; secondaries pink #F0ABD1, blue #A3DEF5, purple #CFB0F0 (never on gold).
Headlines in sentence case, Figtree 900 standing in for Faro Display Lucky (commercial); buttons in Inter SemiBold uppercase; the Pot used as background device and as punctuation; stacked logo animated per the logo motion principles (Pot pops into the O, letters reveal from behind it).
Art: Higgsfield stills on newsprint (Jo anchor + referenced poses), backgrounds removed with Higgsfield, duotoned to charcoal → cream (art/duotone.py). Logo, Pot shape and Chip extracted as vectors from the guidelines PDF.
Storyboard: storyboard.jpg (real frames from index.html).

| # | Time | Voice | Line |
|---|---|---|---|
| 1 | 0:00 | Jo | So I'm class rep this year. Which apparently means I'm doing the teacher gift. |
| 2 | 0:06 | Jo | I pop a message in the class WhatsApp. Five quid each for Miss Clarke. |
| 3 | 0:10 | Dave / Priya / Sam | Can I give it you Friday? · Is it five or ten? · Ooh, we've already got her something! |
| 4 | 0:16 | Jo | Eleven thumbs-up. Zero fivers. |
| 5 | 0:19 | Jo | Three weeks of 'just a gentle reminder'. A sandwich bag of coins at the gate. And I'm still forty quid short… so guess who's topping it up. |
| 6 | 0:30 | Jo | Next year? One Collection Pot, one link… and I'm putting the kettle on. |
| 7 | 0:35 | Tagline (Daniel) | Collection Pot. Easy to sort. Impossible to forget. |

## Sound
- Voices (ElevenLabs, free plan → premade voices only): Jo = Lily (eleven_v3, one take so it plays like a voice note, cut into beats and tightened in voices/assemble.py, +8% tempo); Dave = George, Priya = Alice, Sam = Jessica (eleven_v3); tagline = Daniel (multilingual v2).
- Timings come from ElevenLabs speech-to-text (voices/*.stt.json); voices/retime.py writes the scene starts/cues into index.html.
- Music (audio/score_playful.py): light pizzicato oom-pah under the set-up, a deflating bassoon "womp" on "Zero fivers", a busier minor-key groove through the chasing, a dead stop for "so guess who's topping it up", then celesta + sleigh bells + warm strings from "Next year?" to the end card.
- SFX are loudness-matched then sit 12–26 dB under the voice (user asked for quiet SFX); scribble/marker sounds lowest.
- Mix -14 LUFS, -1 dBTP (audio/mix.py).

## Regenerate
voices/tts.py → voices/assemble.py → voices/retime.py → audio/sfx.py → audio/score_playful.py → audio/mix.py → `npx hyperframes@0.9.20 render -q delivery -o renders/class-rep.mp4` → re-encode `-crf 20 -preset slow` to class-rep.mp4.

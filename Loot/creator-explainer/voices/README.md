# Voiceover

- `raw/dNN.mp3`: Higgsfield **Text to Speech V2**, `variant: elevenlabs`, preset voice **Dylan**
  (`voice_id b847bc29-f184-583a-8ad9-d1f1e16d1a60`, `voice_type preset`). Text in `lines.json`.
  ~0.3 credits a line. The ElevenLabs account ran out of free credits, so the VO moved to Higgsfield.
- `dNN.wav`: trimmed and sped 1.06× (pitch kept):
  `ffmpeg -i raw/dNN.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,atempo=1.06" -ar 44100 -ac 1 dNN.wav`
- `pauses.json`: phrase pauses measured with `silencedetect` (Higgsfield returns no word timings);
  they place the cues in `index.html` and the captions in `srt.py`.
- To change voice: regenerate the 10 lines with another `voice_id` from Higgsfield's voice list,
  re-run the ffmpeg step, check the pauses, then `audio/mix.py` and `voices/srt.py`.

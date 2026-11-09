#!/bin/sh
# One command, from the project's source folder: frames → score → mix → master → mux → subtitles → poster.
# Needs the Lemo-Opuscar library (core + music tiers, sample libraries vcsl vsco2ce karoryfer freepats).
# Voice lines are already in voices/ (regenerate with `sh tools_tts.sh`, check with `python3 tools_asr.py`; both use ElevenLabs).
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd); OUT=$HERE/..; NAME=right4paws-serve
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the Lemo-Opuscar library folder"; exit 1; }
sh "$HERE/tools/fonts.sh"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 24 --size 1080x1920 --workers 4 --out "$HERE/out/video.mp4"
.venv/bin/python "$HERE/music/score.py"
.venv/bin/python "$HERE/mix.py"
.venv/bin/python "$HERE/master.py"          # −14 LUFS / −1 dBTP in numpy (ffmpeg 6's loudnorm under-reports length)
ffmpeg -hide_banner -loglevel error -y -i "$HERE/out/video.mp4" -i "$HERE/out/master.wav" -map 0:v -map 1:a -vf "noise=alls=3:allf=t" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$OUT/$NAME.mp4"
python3 -c "import json;e=json.load(open('$HERE/events.json'));json.dump(sorted([{'t0':x['t'],'t1':x['t1'],'text':x['text']} for x in e['ev'] if x['type']=='sub'],key=lambda x:x['t0']),open('$HERE/cues.json','w'),ensure_ascii=False)"
.venv/bin/python core/render/srt.py "$HERE/cues.json" "$OUT/$NAME.srt"
ffmpeg -hide_banner -loglevel error -y -ss 44.6 -i "$OUT/$NAME.mp4" -frames:v 1 -q:v 2 "$OUT/poster.jpg"
echo "✓ $OUT/$NAME.mp4"

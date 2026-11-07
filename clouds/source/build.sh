#!/bin/sh
# One command: TTS → events → score → mix → picture → master. Copy this folder to $LIB/films/clouds first.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../.." && pwd)}; export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the lemo-opuscar library folder"; exit 1; }
cd "$LIB"; mkdir -p "$HERE/out"
[ -f "$HERE/voices/dur.json" ] || .venv/bin/python core/tts/tts.py "$HERE/lines.json" "$HERE/voices"
node core/render/events.mjs "$HERE"
.venv/bin/python "$HERE/score.py"      # needs: sh tools/fetch.sh instruments vsco2ce && sh tools/fetch.sh instruments vcsl
.venv/bin/python "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps 24 --size 1080x1920 --workers 4 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/clouds.mp4" 24 0
.venv/bin/python core/render/srt.py "$HERE/subs.json" "$HERE/clouds.srt"

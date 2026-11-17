#!/bin/sh
# One command: events → score → mix → picture → master.  LIB = the lemo-opuscar library folder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:?set LIB to the lemo-opuscar library folder (github.com/lemomo-ai/lemo-opuscar); copy this folder to $LIB/films/mango first}
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
cd "$LIB"
[ -f "$HERE/voices/dur.json" ] || .venv/bin/python core/tts/tts.py "$HERE/lines.json" "$HERE/voices"
mkdir -p "$HERE/out"
node core/render/events.mjs "$HERE"
.venv/bin/python "$HERE/score.py"
.venv/bin/python "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps 24 --size 1080x1920 --workers 4 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/mango.mp4" 24 0
.venv/bin/python core/render/srt.py "$HERE/subs.json" "$HERE/mango.srt"

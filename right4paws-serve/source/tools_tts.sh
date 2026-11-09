#!/bin/sh
# ElevenLabs TTS for every line in lines.json -> voices/<id>.wav (48 kHz mono, edges trimmed) + voices/dur.json
# usage: sh tools_tts.sh [id ...]   (no ids = all lines)
set -e
cd "$(dirname "$0")"; mkdir -p voices
VOICE=${VOICE:-pqHfZKP75CvOlQylNhV4}   # "Bill" (ElevenLabs premade)
ids=${*:-$(python3 -c "import json;print(' '.join(l['id'] for l in json.load(open('lines.json'))))")}
for id in $ids; do
  body=$(python3 -c "import json,sys;l=[x for x in json.load(open('lines.json')) if x['id']=='$id'][0];print(json.dumps({'text':l['text'],'model_id':'eleven_multilingual_v2','voice_settings':{'stability':l.get('stability',0.5),'similarity_boost':0.8,'style':l.get('style',0.25),'use_speaker_boost':True,'speed':l.get('speed',0.96)}}))")
  code=$(curl -sS -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE?output_format=mp3_44100_128" -H "xi-api-key: dummy" -H "Content-Type: application/json" -d "$body" -o "voices/$id.mp3" -w "%{http_code}")
  [ "$code" = 200 ] || { echo "✗ $id: HTTP $code"; cat "voices/$id.mp3"; exit 1; }
  ffmpeg -loglevel error -y -i "voices/$id.mp3" -af "silenceremove=start_periods=1:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_threshold=-48dB,areverse,apad=pad_dur=0.04" -ar 48000 -ac 1 "voices/$id.wav"
  echo "✓ $id"
done
python3 - <<'PY'
import json, wave
d = {}
for l in json.load(open('lines.json')):
    try: w = wave.open(f"voices/{l['id']}.wav"); d[l['id']] = round(w.getnframes() / w.getframerate(), 3)
    except FileNotFoundError: pass
json.dump(d, open('voices/dur.json', 'w'), indent=1); print(d)
PY

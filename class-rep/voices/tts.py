# ElevenLabs TTS with timestamps. lines.json: [id, voice_id, model_id, text]. Skips ids that already have an mp3.
import json, urllib.request, base64, os, sys
here = os.path.dirname(os.path.abspath(__file__))
force = set(sys.argv[1:])
for vid, voice, model, text in json.load(open(os.path.join(here, "lines.json"))):
    if os.path.exists(os.path.join(here, f"{vid}.mp3")) and vid not in force: continue
    if model == "eleven_v3":
        vs = {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": True, "speed": 1.1}
    else:
        vs = {"stability": 0.6, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True, "speed": 0.95}
    body = json.dumps({"text": text, "model_id": model, "voice_settings": vs}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    d = json.load(urllib.request.urlopen(req))
    open(os.path.join(here, f"{vid}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(here, f"{vid}.align.json"), "w")); print(vid, "ok")

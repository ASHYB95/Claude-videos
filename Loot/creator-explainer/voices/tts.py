"""ElevenLabs VO with word timings. Skips lines that already have an mp3.
Run: python3 voices/tts.py  (the proxy injects the API key)"""
import json, urllib.request, urllib.error, base64, os
here = os.path.dirname(os.path.abspath(__file__))
VS = {"stability": 0.42, "similarity_boost": 0.8, "style": 0.4, "use_speaker_boost": True, "speed": 1.06}
for vid, voice, text in json.load(open(os.path.join(here, "lines.json"))):
    if os.path.exists(os.path.join(here, f"{vid}.mp3")): continue
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": VS}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    try:
        d = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print(vid, e.code, e.read()[:300]); raise
    open(os.path.join(here, f"{vid}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(here, f"{vid}.align.json"), "w")); print(vid, "ok")

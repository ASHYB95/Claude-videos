import json, urllib.request, base64, sys, os
V = "Xb7hH8MSUJpSbSDYk0k2"  # Alice
here = os.path.dirname(os.path.abspath(__file__))
for vid, text in json.load(open(os.path.join(here, "lines.json"))):
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.08}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    d = json.load(urllib.request.urlopen(req))
    open(os.path.join(here, f"{vid}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(here, f"{vid}.align.json"), "w"))
    print(vid, "ok")

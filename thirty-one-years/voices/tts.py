import json, urllib.request, base64, os
here = os.path.dirname(os.path.abspath(__file__))
for vid, voice, text in json.load(open(os.path.join(here, "lines.json"))):
    if os.path.exists(os.path.join(here, f"{vid}.mp3")): continue
    quote = vid.startswith('q')
    vs = {"stability": 0.45 if quote else 0.55, "similarity_boost": 0.8, "style": 0.35 if quote else 0.3, "use_speaker_boost": True, "speed": 0.97}
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": vs}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    d = json.load(urllib.request.urlopen(req))
    open(os.path.join(here, f"{vid}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(here, f"{vid}.align.json"), "w")); print(vid, "ok")

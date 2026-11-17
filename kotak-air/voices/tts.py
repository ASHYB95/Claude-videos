# Generates one VO take per line in lines.json (ElevenLabs, key injected by the proxy).
import json, urllib.request, urllib.error, base64, os, sys
here = os.path.dirname(os.path.abspath(__file__))
force = set(sys.argv[1:])
for vid, voice, text in json.load(open(os.path.join(here, "lines.json"))):
    if os.path.exists(os.path.join(here, f"{vid}.mp3")) and vid not in force: continue
    vs = {"stability": 0.5, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.12}
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": vs}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    try:
        d = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print(vid, e.code, e.read()[:400]); sys.exit(1)
    open(os.path.join(here, f"{vid}.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(os.path.join(here, f"{vid}.align.json"), "w"), ensure_ascii=False); print(vid, "ok")

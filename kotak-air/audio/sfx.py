# Extra SFX for this film (ElevenLabs sound generation). Generic UI sounds reused from oneclickdrive/collection-pot.
import json, urllib.request, urllib.error, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {"sticker": ("soft glossy sticker slapped onto a plastic card, light satisfying pop, short, clean UI sound", 0.5)}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    try: open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")
    except urllib.error.HTTPError as e: print(k, e.code, e.read()[:200])

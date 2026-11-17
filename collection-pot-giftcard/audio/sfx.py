# New SFX for this cut (ElevenLabs Sound Effects). Others are reused from ../collection-pot/audio.
import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "tissue": ("loud crinkling tissue paper being pulled out of a gift box, crisp paper rustle, close microphone", 1.5),
 "door": ("kitchen wall cupboard door opening, soft wooden swing and a light hinge click, close, clean, short", 1.0),
 "clink": ("a few ceramic mugs clinking gently together on a shelf, soft, short", 0.8),
 "typing": ("soft quick tapping on a smartphone touchscreen keyboard, gentle key clicks, close, clean", 1.2),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

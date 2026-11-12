# New SFX for this ad (ElevenLabs sound generation). Generic ones (tap, whoosh, pop...) reused from collection-pot.
import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "strike": ("quick thick marker pen strike-through across paper, single fast scribble swipe", 0.6),
 "pindrop": ("cartoon map pin dropping and landing with a soft bouncy thud, playful UI sound", 0.6),
 "rev": ("sports car engine short throttle blip rev, close mic, clean, no tyre squeal", 1.5),
 "tick": ("short soft mechanical counter ticking, rolling number flip, UI", 0.9),
 "stamp": ("heavy rubber stamp slam on a desk, punchy, short", 0.6),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

import json, urllib.request, os, sys
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "tap":     ("crisp satisfying button click, modern app UI tap, clearly audible, short", 0.5),
 "type":    ("rapid light smartphone touchscreen keyboard typing clicks, soft, clean", 2.0),
 "whoosh":  ("fast cinematic air whoosh swish, smooth, modern product video transition", 1.2),
 "spin":    ("sleek futuristic whoosh with rising shimmer, object spinning past camera", 1.5),
 "pop":     ("soft glassy UI pop bubble notification, clean, short", 0.5),
 "shimmer": ("magical digital sparkle shimmer loading sound, airy, soft, modern UI", 2.0),
 "swipe":   ("soft paper-like card slide swoosh, UI element flying in, clean", 0.8),
 "send":    ("message sent swoosh, upward airy whoosh, modern messaging app", 0.8),
 "impact":  ("deep cinematic logo impact hit with soft sub boom and short tail, premium tech brand", 2.5),
 "riser":   ("short clean tension riser, airy white noise sweep up, 1.5 seconds", 1.5),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "coins":    ("a few coins dropping into a ceramic pot, bright metallic clinks, close and clean", 1.2),
 "kaching":  ("cheerful cash register ka-ching bell, short, clean, modern", 1.0),
 "popper":   ("party popper pop with confetti burst, festive, short", 1.0),
 "notif":    ("pleasant soft two-note phone notification chime, modern, friendly", 0.8),
 "paper":    ("paper envelope being passed hand to hand, quick paper rustle and slide", 1.2),
 "cheer":    ("small group of office colleagues cheering and clapping happily, warm, short burst", 2.5),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

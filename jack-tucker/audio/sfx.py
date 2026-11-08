# ElevenLabs sound effects for the Hijack-for-Artists promo.
import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "tap":     ("single crisp soft UI tap click on a glass phone screen, very short, clean", 0.5),
 "whoosh":  ("fast airy whoosh transition, modern, clean, short", 0.8),
 "pop":     ("soft bubbly UI pop, light and satisfying, very short", 0.5),
 "swipe":   ("quick soft swipe swish of a finger across a phone screen, short", 0.5),
 "impact":  ("deep punchy cinematic boom hit with short tail, modern trailer logo hit", 1.2),
 "shimmer": ("bright sparkle shimmer chime, magical, short, clean", 1.0),
 "notif":   ("pleasant modern two-note phone notification chime, soft, friendly", 0.8),
 "coin":    ("single bright digital coin ping, clean and satisfying, short", 0.6),
 "typing":  ("fast light typing on a phone touch keyboard, six soft taps", 0.8),
 "scan":    ("quick phone camera QR code scan beep, short electronic confirmation", 0.6),
 "crowd":   ("busy bar at night with live music in the background, crowd chatter, glasses clinking", 4.0),
 "cheer":   ("small group of friends at a table cheering and clapping happily in a live music cafe", 3.0),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

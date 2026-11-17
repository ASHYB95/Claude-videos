# Sound effects for SM explainer. Paper foley is reused from thirty-one-years/audio;
# the rest is generated once with ElevenLabs sound-generation (key injected by the proxy).
import json, urllib.request, os, shutil
here = os.path.dirname(os.path.abspath(__file__))
ref = os.path.join(here, '..', '..', 'thirty-one-years', 'audio')
for n in ['tear', 'tape', 'marker', 'stamp', 'typer', 'slide', 'flutter', 'pin', 'whoosh', 'pop']:
    dst = os.path.join(here, f'sfx_{n}.mp3')
    if not os.path.exists(dst): shutil.copy(os.path.join(ref, f'sfx_{n}.mp3'), dst)
SFX = {
 "swish":  ("soft airy swish, a quick smooth whoosh of a circle shrinking, clean, subtle, short", 0.7),
 "plug":   ("electrical plug pushed firmly into a wall socket, solid click with a tiny electric spark crackle", 0.9),
 "tap":    ("single finger tap on a smartphone glass screen, soft clean click", 0.5),
 "ding":   ("bright friendly app notification ding, single soft bell, modern", 0.8),
 "flip":   ("three paper calendar pages flipped quickly one after another, crisp paper flicks", 0.9),
 "tv":     ("old cathode ray television switching on, a click then a short static fizz settling", 1.2),
 "crowd":  ("distant cricket stadium crowd cheering and clapping, warm roar, no commentary, no words", 4.0),
 "tick":   ("mechanical counter numbers rolling fast, light rapid ticking, short", 1.2),
 "switch": ("old light switch flicked on, single clean click", 0.5),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

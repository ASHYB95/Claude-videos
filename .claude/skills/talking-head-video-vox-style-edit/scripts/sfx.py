#!/usr/bin/env python3
"""Generate (once) the paper + UI sound-effect kit with ElevenLabs sound-generation.

Usage: python3 sfx.py <out_dir> [name ...]     (no names = whole kit)
Paper foley is copied from thirty-one-years/audio when that folder exists (same repo), otherwise generated.
The ElevenLabs key is injected by the session proxy. duration_seconds must be >= 0.5.
A failed request can leave a 0-byte file — this script deletes empties first so a re-run retries them.

Approved usage on the reference build: ~35 cues for 87 s, -6 dB trim. Swish (circle morphs), tear (scene wipes),
stamp (section cards + one big punchline), tick (counters) and a handful of one-off action sounds.
"""
import json, os, shutil, sys, urllib.request

out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
os.makedirs(out, exist_ok=True)
ref = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'thirty-one-years', 'audio')
KIT = {
 # paper foley
 "tear":   ("a sheet of paper being torn quickly, crisp, close", 1.0),
 "stamp":  ("rubber stamp thud on paper, single, crisp", 0.6),
 "tape":   ("a strip of masking tape pulled off the roll and pressed down", 1.0),
 "slide":  ("a photograph print sliding across a wooden table, soft paper swish", 0.8),
 "pin":    ("a push pin pressed into a cork board, small tap", 0.5),
 "pop":    ("small soft paper pop, light and short", 0.5),
 "whoosh": ("quick soft whoosh, paper flying past", 0.6),
 "marker": ("felt-tip marker scribbling quickly on paper, short", 1.0),
 "typer":  ("old mechanical typewriter typing a few keys", 1.0),
 # UI / action
 "swish":  ("soft airy swish, a quick smooth whoosh of a circle shrinking, clean, subtle, short", 0.7),
 "tick":   ("mechanical counter numbers rolling fast, light rapid ticking, short", 1.2),
 "switch": ("old light switch flicked on, single clean click", 0.5),
 "plug":   ("electrical plug pushed firmly into a wall socket, solid click with a tiny electric spark crackle", 0.9),
 "flip":   ("three paper calendar pages flipped quickly one after another, crisp paper flicks", 0.9),
 "tv":     ("old cathode ray television switching on, a click then a short static fizz settling", 1.2),
 "crowd":  ("distant stadium crowd cheering and clapping, warm roar, no commentary, no words", 4.0),
 "tap":    ("single finger tap on a smartphone glass screen, soft clean click", 0.5),
 "ding":   ("bright friendly app notification ding, single soft bell, modern", 0.8),
}
want = sys.argv[2:] or list(KIT)
for n in want:
    dst = os.path.join(out, f'sfx_{n}.mp3')
    if os.path.exists(dst) and os.path.getsize(dst) == 0: os.remove(dst)
    if os.path.exists(dst): continue
    src = os.path.join(ref, f'sfx_{n}.mp3')
    if os.path.exists(src): shutil.copy(src, dst); print(n, 'copied'); continue
    text, dur = KIT[n]
    body = json.dumps({"text": text, "duration_seconds": max(0.5, dur), "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
                                 headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    data = urllib.request.urlopen(req, timeout=120).read()
    open(dst, "wb").write(data); print(n, 'generated')

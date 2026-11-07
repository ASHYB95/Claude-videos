import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {
 "tear":     ("a sheet of paper being torn quickly, crisp, close", 1.0),
 "tape":     ("a strip of masking tape pulled off the roll and pressed down", 1.0),
 "marker":   ("felt-tip marker scribbling quickly on paper, short", 1.0),
 "stamp":    ("rubber stamp thud on paper, single, crisp", 0.6),
 "typer":    ("old mechanical typewriter typing a few keys and a bell ding", 1.5),
 "pencil":   ("pencil writing on paper, soft scratchy, short phrase", 1.5),
 "slide":    ("a photograph print sliding across a wooden table, soft paper swish", 0.8),
 "flutter":  ("several paper notes fluttering down onto a table, soft", 1.6),
 "pin":      ("a push pin pressed into a cork board, small tap", 0.5),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

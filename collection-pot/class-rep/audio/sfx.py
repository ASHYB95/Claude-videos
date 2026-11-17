import json, urllib.request, os
here = os.path.dirname(os.path.abspath(__file__))
SFX = {   # new for this film; tear/slide/stamp/marker/tape/pop/whoosh/flutter reused from thirty-one-years, coins/tap/send from collection-pot
 "kettle":   ("an electric kettle switch clicked on, a single plastic click, then a faint soft rumble", 1.2),
 "notes":    ("two banknotes pulled out of a leather purse, quick paper rustle", 0.8),
}
for k, (t, d) in SFX.items():
    out = os.path.join(here, f"sfx_{k}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": t, "duration_seconds": d, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
        headers={"Content-Type": "application/json", "xi-api-key": "proxy-injected"})
    open(out, "wb").write(urllib.request.urlopen(req).read()); print(k, "ok")

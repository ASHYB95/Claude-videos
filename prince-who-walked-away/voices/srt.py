# Build the .srt from ElevenLabs character alignment: one cue per sentence (long sentences split at a comma).
import json, os, re
here = os.path.dirname(os.path.abspath(__file__))
VO = {'v1': 0.6, 'v2': 7.45, 'v3': 13.1, 'q1': 19.6, 'v4': 23.25, 'v5': 30.6, 'v6': 36.4, 'v7': 44.7, 'q2': 48.6, 'v8': 51.45, 'v9': 58.85}
# subtitles show the script as written (numbers as digits)
SHOW = {'Two thousand five hundred years ago': '2,500 years ago', 'At twenty-nine': 'At 29'}
cues = []
for k, off in VO.items():
    a = json.load(open(os.path.join(here, f'{k}.align.json')))
    ch, st, en = a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']
    text = ''.join(ch); i = 0
    for m in re.finditer(r'[^.?!:]+[.?!:]?', text):
        s, e = m.start(), m.end()
        seg = text[s:e]
        parts = [seg] if len(seg.strip()) <= 42 else re.findall(r'[^,]+,?', seg)
        # merge tiny comma parts back together
        merged = []
        for p in parts:
            if merged and len((merged[-1] + p).strip()) <= 42: merged[-1] += p
            else: merged.append(p)
        pos = s
        for p in merged:
            a0 = pos + (len(p) - len(p.lstrip())); a1 = pos + len(p.rstrip()) - 1; pos += len(p)
            if a1 < a0: continue
            t = text[a0:a1 + 1].strip()
            for x, y in SHOW.items(): t = t.replace(x, y)
            cues.append([off + st[a0], off + en[a1], t, k])
# hold each cue until just before the next one (max +0.6 s)
for j in range(len(cues)):
    nxt = cues[j + 1][0] if j + 1 < len(cues) else cues[j][1] + 1.0
    cues[j][1] = min(nxt - 0.05, cues[j][1] + 0.6)
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
out = []
for n, (a0, a1, t, k) in enumerate(cues, 1):
    who = {'q1': 'CHANNA: ', 'q2': 'SIDDHARTHA: '}.get(k, '')
    out.append(f'{n}\n{ts(a0)} --> {ts(a1)}\n{who}{t}\n')
open(os.path.join(os.path.dirname(here), 'prince-who-walked-away.srt'), 'w').write('\n'.join(out)); print(len(cues), 'cues')

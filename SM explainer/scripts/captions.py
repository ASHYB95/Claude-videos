#!/usr/bin/env python3
"""transcript.json + edl.json -> data.js (caption chunks, cut points) and SM-explainer.srt.

Chunks: break on punctuation, on pauses > 0.28 s, or at MAX_CHARS, so each torn-paper strip
holds 1-4 words on one line.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, 'transcript.json')))
E = json.load(open(os.path.join(ROOT, 'edl.json')))
MAX_CHARS, MAX_WORDS = 20, 4

chunks, cur = [], []
def flush():
    global cur
    if cur: chunks.append(cur); cur = []
newtake = {k for k, sg in enumerate(E['segments']) if sg['new_take']}
for i, w in enumerate(W):
    if cur and w['seg'] in newtake and w['seg'] != cur[-1]['seg']:
        flush()
    if cur:
        n = len(' '.join(x['text'] for x in cur + [w]))
        if n > MAX_CHARS or len(cur) >= MAX_WORDS or w['start'] - cur[-1]['end'] > 0.28:
            flush()
    cur.append(w)
    if re.search(r'[.,?!]$', w['text']):
        flush()
flush()
# merge orphan single short words into the previous chunk when it fits
out = []
for c in chunks:
    if out and len(c) == 1 and not re.search(r'[.?!]$', out[-1][-1]['text']) and len(c[0]['text']) <= 4 and c[0]['start'] - out[-1][-1]['end'] < .3 \
            and len(' '.join(x['text'] for x in out[-1] + c)) <= MAX_CHARS + 4:
        out[-1] += c
    else:
        out.append(c)
# ...and lone lead-in words ("And", "So") forward into the next chunk
fw = []
for c in out:
    if fw and len(fw[-1]) == 1 and not re.search(r'[.,?!]$', fw[-1][0]['text']) and len(fw[-1][0]['text']) <= 4 \
            and c[0]['start'] - fw[-1][0]['end'] < .7 and len(' '.join(x['text'] for x in fw[-1] + c)) <= MAX_CHARS + 4:
        fw[-1] = fw[-1] + c
    else:
        fw.append(c)
out = fw
cap = []
for k, c in enumerate(out):
    t0 = c[0]['start'] - 0.04
    t1 = (out[k + 1][0]['start'] - 0.04) if k + 1 < len(out) else c[-1]['end'] + 0.4
    t1 = min(t1, c[-1]['end'] + 0.6)
    cap.append(dict(t0=round(t0, 3), t1=round(t1, 3), w=[[x['text'], x['start'], x['end']] for x in c]))
cuts = [s['out_in'] for s in E['segments']]
takes = [s['out_in'] for s in E['segments'] if s['new_take']]
js = 'window.CAPS=' + json.dumps(cap, separators=(',', ':')) + ';\nwindow.CUTS=' + json.dumps(cuts) + ';\nwindow.TAKES=' + json.dumps(takes) + ';\nwindow.AROLL_DUR=' + str(E['duration']) + ';\n'
open(os.path.join(ROOT, 'data.js'), 'w').write(js)

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'
srt = []
for k, c in enumerate(cap):
    srt.append(f"{k + 1}\n{ts(c['t0'])} --> {ts(c['t1'])}\n{' '.join(x[0] for x in c['w'])}\n")
open(os.path.join(ROOT, 'SM-explainer.srt'), 'w').write('\n'.join(srt))
print(len(cap), 'caption chunks')
for c in cap[:24]: print(f"{c['t0']:6.2f}-{c['t1']:6.2f}  " + ' '.join(f"{x[0]}@{x[1]:.2f}" for x in c['w']))

# Build oneclickdrive.srt from ElevenLabs alignments + the VO placement used in audio/mix.py
import json, os
here = os.path.dirname(os.path.abspath(__file__))
PL = {'v1': [(0, 99, 0.25)], 'v2': [(0, 99, 5.3)], 'v3': [(0, 1.12, 9.3), (1.12, 4.02, 9.75), (4.02, 99, 10.15)],
      'v4': [(0, 99, 17.4)], 'v5': [(0, 99, 20.6)], 'v6': [(0, 99, 24.5)], 'v7': [(0, 99, 28.0)]}
def words(v):
    a = json.load(open(f'{here}/{v}.align.json')); out = []; cur = ''; s = e = 0
    for c, t0, t1 in zip(a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']):
        if c == ' ':
            if cur: out.append([cur, s, e]); cur = ''
            continue
        if not cur: s = t0
        cur += c; e = t1
    if cur: out.append([cur, s, e])
    return out
W = []
for v, pl in PL.items():
    for w, s, e in words(v):
        for a, b, off in pl:
            if a <= s < b: W.append([w.replace('...', '…'), s + off, e + off]); break
# v3 offsets: segment 1 placed at 9.3 (offset 9.3); seg 2 offset 9.75; seg 3 offset 10.15
# merge "One Click Drive" → OneClickDrive
M = []
for w in W:
    if M and M[-1][0] in ('One', 'OneClick') and w[0].startswith(('Click', 'Drive')):
        M[-1][0] += w[0]; M[-1][2] = w[2]
    else: M.append(w)
cues, cur = [], []
for w in M:
    cur.append(w)
    if w[0][-1] in '.?,…':
        if len(cur) > 6: h = (len(cur) + 1) // 2; cues += [cur[:h], cur[h:]]
        else: cues.append(cur)
        cur = []
if cur: cues.append(cur)
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}'
with open(os.path.join(os.path.dirname(here), 'oneclickdrive.srt'), 'w') as f:
    for i, c in enumerate(cues, 1):
        end = c[-1][2] + 0.15
        if i < len(cues): end = min(end, cues[i][0][1] - 0.02)
        f.write(f'{i}\n{ts(c[0][1])} --> {ts(end)}\n{" ".join(w[0] for w in c)}\n\n')
print(len(cues), 'cues')

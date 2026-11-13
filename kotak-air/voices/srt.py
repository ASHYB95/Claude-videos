# Build kotak-air.srt from the ElevenLabs alignments + VO starts (audio/mix.py). Written form (₹, numerals).
import json, os
here = os.path.dirname(os.path.abspath(__file__))
START = {1: 0.35, 2: 2.72, 3: 8.00, 4: 12.04, 5: 16.49, 6: 22.52, 7: 28.66, 8: 34.45}
CHUNKS = {  # (caption text, index of its first spoken word)
 1: [("Introducing the Kotak Air Credit Card.", 0)],
 2: [("Earn 3 Air Miles per ₹100", 0), ("on flights and hotels booked via Kotak Unbox.", 7)],
 3: [("And 1 Air Mile per ₹100", 0), ("on everything else, with no cap.", 7)],
 4: [("Get 1,000 bonus Air Miles on joining,", 0), ("and again every year on renewal.", 8)],
 5: [("Redeem 1 Air Mile for ₹1 on flights and hotels,", 0), ("or transfer to 8 airline and hotel partners.", 11)],
 6: [("Enjoy 4 complimentary domestic lounge visits a year,", 0), ("plus a 1% fuel surcharge waiver.", 8)],
 7: [("There's no joining fee,", 0), ("and the annual fee is just ₹999 + GST.", 4)],
 8: [("Kotak Air Credit Card.", 0), ("Turn everyday spends into travel.", 4)],
}
def words(i):
    a = json.load(open(f'{here}/v{i}.align.json')); out = []; cur = ''; s = e = 0
    for c, t0, t1 in zip(a['characters'], a['character_start_times_seconds'], a['character_end_times_seconds']):
        if c == ' ':
            if cur: out.append((cur, s, e)); cur = ''
            continue
        if not cur: s = t0
        cur += c; e = t1
    if cur: out.append((cur, s, e))
    return out
cues = []
for i, ch in CHUNKS.items():
    w = words(i); off = START[i]
    for k, (txt, w0) in enumerate(ch):
        w1 = ch[k + 1][1] - 1 if k + 1 < len(ch) else len(w) - 1
        cues.append([txt, w[w0][1] + off, w[w1][2] + off + 0.15])
for k in range(len(cues) - 1): cues[k][2] = min(cues[k][2], cues[k + 1][1] - 0.02)
def ts(t): m = int(t // 60); s = t % 60; return f'00:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
with open(os.path.join(os.path.dirname(here), 'kotak-air.srt'), 'w') as f:
    for n, (txt, a, b) in enumerate(cues, 1): f.write(f'{n}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')
print(len(cues), 'cues')

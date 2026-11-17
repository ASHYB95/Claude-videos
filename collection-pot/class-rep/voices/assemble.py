# Cut Jo's single take into beats, tighten pauses, interleave the parents + tagline, and write
#   vo.wav (voice track), cues.json (scene/word times for index.html) and ../class-rep.srt.
# Times for each source come from ElevenLabs speech-to-text (*.stt.json), which matches the audio.
import json, subprocess, os, numpy as np
import scipy.io.wavfile as wf
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
SR = 44100; TEMPO = 1.08; QTEMPO = 1.04   # a touch quicker, still natural
def load(f, tempo=1.0):
    af = ['-af', f'atempo={tempo}'] if tempo != 1.0 else []
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, *af, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def words(f, k=1.0):
    return [(w['text'], w['start'] / k, w['end'] / k) for w in json.load(open(f))['words'] if w['type'] in ('word', 'audio_event')]
jo = load('jo.mp3', TEMPO); JW = words('jo.stt.json', TEMPO)
def jt(word, n=0):  # start time (in the sped-up take) of the n-th occurrence of a word
    hits = [w for w in JW if w[0].strip('",.?!').lower() == word.lower()]; return hits[n][1]
def onset(t0, thr=0.02):  # first moment after t0 where Jo's voice comes back in
    i = int(t0 * SR); w = int(.01 * SR)
    while i + w < len(jo) and np.sqrt(np.mean(jo[i:i + w] ** 2)) < thr: i += w
    return i / SR
def je(word, n=0):
    hits = [w for w in JW if w[0].strip('",.?!').lower() == word.lower()]; return hits[n][2]
# Jo beats (source in/out in sped-up take). The sigh is shortened by starting it late.
sigh = [w for w in JW if w[0] == '[sighs]'][0]
BEATS = [
    ('j1a', jt('so') - .06, je('year') + .1),
    ('j1b', jt('which') - .05, je('gift') + .12),
    ('j2a', jt('i', 0) - .06, je('whatsapp') + .08),
    ('j2b', onset(je('whatsapp') + .05) - .04, je('clark') + .15),
    ('j3', jt('eleven') - .06, je('fivers') + .12),
    ('j4', sigh[2] - .75, je('reminder') + .12),
    ('j5', jt('a', 2) - .06, je('gate') + .1),
    ('j6a', jt('and', 0) - .06, je('short') + .12),
    ('j6b', jt('so', 1) - .06, je('up', 1) + .15),
    ('j7a', jt('next') - .06, je('year', 1) + .1),
    ('j7b1', jt('one', 0) - .05, je('pot') + .1),
    ('j7b2', jt('one', 1) - .05, je('on') + .25),
]
segs = {k: (jo[int(a * SR):int(b * SR)], [(w, s - a, e - a) for w, s, e in JW if s >= a - .01 and e <= b + .01]) for k, a, b in BEATS}
QT = {'q1': ('q1', 0, 99), 'q2': ('q2', 0, 99), 'q3': ('q3', 0, 99), 'tag1': ('tag', 0, 1), 'tag2': ('tag', 2, 4), 'tag3': ('tag', 5, 7)}
for k, (q, i0, i1) in QT.items():   # (source, first word index, last word index)
    x = load(f'{q}.mp3', QTEMPO); ws = words(f'{q}.stt.json', QTEMPO)[i0:i1 + 1]; a = max(0, ws[0][1] - .06); b = ws[-1][2] + (.2 if i1 == 99 or k == 'tag3' else .1)
    segs[k] = (x[int(a * SR):int(b * SR)], [(w, s - a, e - a) for w, s, e in ws])
# running order with the gap (s) before each piece
ORDER = [('j1a', .3), ('j1b', .3), ('j2a', .4), ('j2b', .3), ('q1', .4), ('q2', .28), ('q3', .28), ('j3', .38), ('j4', .3), ('j5', .28), ('j6a', .25), ('j6b', .45), ('j7a', .55), ('j7b1', .3), ('j7b2', .32), ('tag1', .55), ('tag2', .32), ('tag3', .3)]
TAIL = 0.9
t = 0; place = {}
for k, gap in ORDER:
    t += gap; place[k] = t; t += len(segs[k][0]) / SR
DUR = round(t + TAIL, 2)
buf = np.zeros(int(DUR * SR) + SR)
for k, _ in ORDER:
    x = segs[k][0].copy(); f = int(.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(place[k] * SR); buf[i:i + len(x)] += x
buf = buf[:int(DUR * SR)]
wf.write('vo.wav', SR, (np.clip(buf, -1, 1) * 32767).astype(np.int16))
cues = {'dur': DUR, 'seg': {k: [round(place[k], 3), round(place[k] + len(segs[k][0]) / SR, 3)] for k, _ in ORDER},
        'words': {k: [[w, round(place[k] + s, 3), round(place[k] + e, 3)] for w, s, e in segs[k][1]] for k, _ in ORDER}}
json.dump(cues, open('cues.json', 'w'), indent=1)
# SRT (one caption per beat; parents get their own)
TXT = {'j1a': "So I'm class rep this year.", 'j1b': "Which apparently means I'm doing the teacher gift.", 'j2a': "I pop a message in the class WhatsApp.", 'j2b': "Five quid each for Miss Clarke.",
       'q1': "Can I give it you Friday?", 'q2': "Is it five or ten?", 'q3': "Ooh, we've already got her something!", 'j3': "Eleven thumbs-up. Zero fivers.",
       'j4': "Three weeks of 'just a gentle reminder'.", 'j5': "A sandwich bag of coins at the gate.", 'j6a': "And I'm still forty quid short…", 'j6b': "so guess who's topping it up.",
       'j7a': "Next year?", 'j7b1': "One Collection Pot,", 'j7b2': "one link… and I'm putting the kettle on.", 'tag1': "Collection Pot.", 'tag2': "Easy to sort.", 'tag3': "Impossible to forget."}
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}'
srt = []
for n, (k, _) in enumerate(ORDER, 1):
    a, b = cues['seg'][k]; srt.append(f'{n}\n{ts(a)} --> {ts(b + .15)}\n{TXT[k]}\n')
open('../class-rep.srt', 'w').write('\n'.join(srt))
print('DUR', DUR); [print(k, cues['seg'][k]) for k, _ in ORDER]

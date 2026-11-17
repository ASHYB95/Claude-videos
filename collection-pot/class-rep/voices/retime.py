# Re-time index.html (scene starts T, spoken cues C, data-start/duration) from voices/cues.json. Idempotent.
import json, re, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
c = json.load(open(os.path.join(here, 'cues.json')))
seg = c['seg']; W = c['words']
def w(k, word, n=0):
    hits = [x for x in W[k] if x[0].strip('",.?!\'').lower() == word.lower()]; return hits[n][1]
r = lambda x: round(x, 2)
T = {'s1': 0, 's2': r(seg['j2a'][0] - .3), 's3': r(seg['q1'][0] - .3), 's4': r(seg['j3'][0] - .3), 's5a': r(seg['j4'][0] - .15),
     's5b': r(seg['j5'][0] - .25), 's5c': r(seg['j6a'][0] - .2), 's6': r(seg['j7a'][0] - .15), 's7': r(seg['tag1'][0] - .25), 'end': c['dur']}
C = {'s1gift': r(w('j1b', 'teacher') - .25),
     's2msg': r(w('j2a', 'message') - .1), 's2five': r(seg['j2b'][0]), 's2seen': r(w('j2b', 'miss')),
     'q1': r(seg['q1'][0]), 'q2': r(seg['q2'][0]), 'q3': r(seg['q3'][0]),
     'thumbs': r(w('j3', 'eleven')), 'zero': r(w('j3', 'zero')),
     'three': r(w('j4', 'three')), 'w1': r(seg['j4'][0] + .4), 'w2': r(seg['j4'][0] + 1.1), 'w3': r(seg['j4'][0] + 1.85),
     'coins': r(seg['j5'][0] + .05), 'short': r(w('j6a', 'forty') - .2), 'who': r(seg['j6b'][0]),
     'next': r(w('j7a', 'next')), 'link': r(seg['j7b1'][0]), 'kettle': r(w('j7b2', 'kettle') - .1),
     'logo': r(seg['tag1'][0]), 'sort': r(w('tag2', 'easy')), 'forget': r(w('tag3', 'impossible'))}
f = os.path.join(root, 'index.html'); h = open(f).read()
h = re.sub(r'const T = \{[^}]*\};', 'const T = ' + json.dumps(T).replace('"', '') .replace(':', ': ') + ';', h)
h = re.sub(r'const C = \{.*?\n\};', 'const C = ' + json.dumps(C, indent=2).replace('"', '').replace('\n}', '\n};')[:-1] + '', h, flags=re.S)
order = ['s1', 's2', 's3', 's4', 's5a', 's5b', 's5c', 's6', 's7']
for i, k in enumerate(order):
    a = T[k]; b = T[order[i + 1]] if i + 1 < len(order) else T['end']
    h = re.sub(rf'(<div id="{k}" class="clip" data-start=")[^"]*(" data-duration=")[^"]*(")', rf'\g<1>{a}\g<2>{r(b - a)}\g<3>', h)
D = c['dur']
h = re.sub(r'(data-composition-id="main" data-start="0" data-duration=")[^"]*(")', rf'\g<1>{D}\g<2>', h)
h = re.sub(r'(<div id="(?:tearL|grainL)" class="clip" data-start="0" data-duration=")[^"]*(")', rf'\g<1>{D}\g<2>', h)
audio = f'<audio id="mix" src="audio/mix.wav" data-start="0" data-duration="{D}" data-track-index="20"></audio>'
h = h.replace('<!--AUDIO-->', audio)
h = re.sub(r'<audio id="mix"[^>]*></audio>', audio, h)
open(f, 'w').write(h)
print(T); print(C)

# Mix: voices (vo.wav) + playful score + paper/phone foley -> mix.wav at -14 LUFS.
# SFX are loudness-matched first, then placed well under the voice (user note: keep SFX quiet).
import numpy as np, subprocess, os, re, json
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
SR = 44100
html = open(os.path.join(root, 'index.html')).read()
def obj(name):
    body = re.search(rf'const {name} = \{{(.*?)\}};', html, re.S).group(1)
    return {k: float(v) for k, v in re.findall(r'(\w+):\s*([\d.]+)', body)}
T, C = obj('T'), obj('C'); DUR = T['end']; N = int(SR * DUR)
def load(p, ch=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)
def db(x): return 10 ** (x / 20)
def rms(x): return np.sqrt(np.mean(x ** 2) + 1e-12)
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i and i >= 0: buf[i:j] += x[:j - i] * g

vo = np.zeros((N, 2)); place(vo, load(f'{root}/voices/vo.wav'), 0)
speech = vo[np.abs(vo[:, 0]) > 0.02]; SPEECH = rms(speech)          # reference speech level

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = (np.abs(vo).max(1) > 0.015).astype(float)
w = int(0.25 * SR); act = np.convolve(act, np.ones(w) / w, 'same') > 0.03
duck = np.where(act, db(-7), 1.0); k = int(0.2 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
mus *= SPEECH / rms(mus[mus[:, 0] != 0]) * db(-11)                    # music ~11 dB under speech, ~18 dB when she talks
out = mus * duck[:, None]

names = ['tear', 'slide', 'stamp', 'marker', 'pop', 'whoosh', 'coins', 'tap', 'send', 'kettle', 'notes']
S = {}
for n in names:   # loudness-match every effect to the speech level (by its loudest 60 ms), so cue gains read as "dB under the voice"
    x = load(f'{here}/sfx_{n}.mp3'); win = int(.06 * SR)
    peak = max(rms(x[i:i + win]) for i in range(0, max(1, len(x) - win), win // 2)); S[n] = x * (SPEECH / peak)
cues = [  # (sfx, time, dB under the voice)
    ('slide', .15, -16), ('pop', .25, -18), ('slide', .4, -16), ('stamp', 1.0, -16), ('marker', 1.9, -26), ('pop', C['s1gift'], -15),
    ('pop', T['s2'] + .05, -19), ('slide', T['s2'] + .1, -15),
    *[('tap', C['s2msg'] - .2 + i * .2, -24) for i in range(6)], ('send', C['s2msg'] + 1.05, -17), ('slide', C['s2five'], -18), ('stamp', C['s2seen'] + .2, -13),
    ('whoosh', T['s3'] - .28, -15), *[x for q in ('q1', 'q2', 'q3') for x in (('slide', C[q] - .15, -19), ('pop', C[q], -15))],
    ('pop', C['thumbs'], -16), *[('pop', C['thumbs'] + .1 + i * .24, -21) for i in range(4)], ('stamp', C['zero'] + .16, -10),
    ('marker', C['zero'] + .3, -24), ('marker', C['zero'] + .5, -26),
    ('slide', T['s5a'] + .05, -17), ('slide', C['w1'], -14), ('slide', C['w2'], -14), ('slide', C['w3'], -14),
    ('marker', C['w2'] - .15, -24), ('marker', C['w3'] - .15, -24), ('whoosh', T['s5b'] - .3, -17),
    ('slide', T['s5b'] + .05, -16), ('coins', C['coins'], -12), ('coins', C['coins'] + .65, -19), ('slide', C['coins'] + .3, -19), ('marker', C['coins'] + .8, -26),
    ('slide', T['s5c'] + .05, -14), ('marker', C['short'] + .3, -26), ('slide', C['short'] + .6, -16),
    ('slide', C['who'], -15), ('notes', C['who'] + .15, -15), ('marker', C['who'] - .1, -26),
    ('tear', T['s6'] - .35, -11), ('pop', T['s6'] + .1, -17), ('slide', T['s6'] + .25, -16), ('slide', C['link'], -15),
    ('kettle', C['kettle'] - .25, -13), ('marker', C['kettle'], -26),
    ('tear', T['s7'] - .35, -12), ('pop', C['logo'], -13), ('whoosh', C['logo'] + .7, -22), ('slide', C['sort'] + .3, -18), ('pop', C['sort'] + .55, -16),
]
cues += [('tear', T[s] - .35, -12) for s in ('s2', 's4', 's5c')]
for n, t, g in cues: place(out, S[n], t, db(g))
out += vo
fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
inp = ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp]
meas = subprocess.run(['ffmpeg', '-hide_banner', '-y', *inp, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-af', ln, '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav', DUR, len(cues), 'sfx cues')

# Original score for "The Mound of the Dead": harp-like plucks, a buzzing tanpura-style drone, frame drum, flute.
# D major pentatonic (D E F# A B) for the living city; D minor colour (D F G A C) for the decline; back to D major for the reveal.
# 84 BPM (beat 0.714 s). Not based on any raga or existing melody.
import sys, os, json
sys.path.insert(0, os.environ.get('LIB', '.'))
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from core.audio import sampler as S, pluck as P
from core.audio.sfx import SR, add
HERE = os.path.dirname(os.path.abspath(__file__))
EV = json.load(open(os.path.join(HERE, 'iso', 'events.json')))['ev']
DUR = 47.0; N = int(DUR * SR)
mix = np.zeros((N, 2), np.float32)
rng = np.random.default_rng(8)
BEAT = 60 / 84
m = S.midi
def tt(d): return np.arange(int(d * SR)) / SR
def sos(k, f, o=2): return butter(o, f, k, fs=SR, output='sos')
MAJ = ['D', 'E', 'F#', 'A', 'B']; MIN = ['D', 'F', 'G', 'A', 'C']
def pent(i, octv=4, scale=MAJ): return f"{scale[i % 5]}{octv + i // 5}"
def harp(t, p, v=.5, pan=0, g=.6, d=3.0): add(mix, P.pluck('harp', m(p) if isinstance(p, str) else p, d, vel=v), t, g, pan)
def kal(t, p, v=.5, pan=0, g=.35): add(mix, P.pluck('kalimba', m(p), 1.5, vel=v), t, g, pan)
# —— tanpura-style drone: Pa Sa Sa Sa (low), each pluck a buzzing harmonic tone with a long decay
def tan(f, d=3.2, v=.12):
    x = tt(d); y = np.zeros(len(x))
    for h in range(1, 14):
        jaw = 1 + .6 * np.sin(2 * np.pi * (.35 + h * .07) * x + h)   # slow harmonic swirl (the "jawari" shimmer)
        y += np.sin(2 * np.pi * f * h * x * (1 + .0006 * h)) * (1 / h ** .9) * jaw
    return y * np.exp(-x / 2.2) * (1 - np.exp(-x / .01)) * v
hz = lambda p: 440 * 2 ** ((m(p) - 69) / 12)
def drone(t0, t1, notes, v=.12):
    t = t0; k = 0
    while t < t1:
        add(mix, tan(hz(notes[k % 4]), v=v), t, 1, [-.3, .3, .1, -.1][k % 4]); t += BEAT * 1.05; k += 1
drone(0, 27.8, ['A2', 'D3', 'D3', 'D2'])
drone(27.6, 40.6, ['A2', 'D3', 'D3', 'D2'], v=.09)
drone(40.2, 46.0, ['A2', 'D3', 'D3', 'D2'], v=.12)
# —— frame drum: dum (low, open) and tek (rim)
def dum(v=1): x = tt(.5); f = 58 + 40 * np.exp(-x / .04); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / .2) + sosfilt(sos('low', 400), rng.standard_normal(len(x))) * np.exp(-x / .03) * .3) * v
def tek(v=1): x = tt(.15); return (sosfilt(sos('band', [1800, 5000]), rng.standard_normal(len(x))) * np.exp(-x / .02) + np.sin(2 * np.pi * 420 * x) * np.exp(-x / .04) * .3) * v
def groove(t0, t1, density=1.0, v=.5):
    t = t0; bar = 0
    while t < t1:
        pat = [(0, 'd', 1), (1.5, 't', .6), (2, 'd', .7), (3, 't', .8), (3.5, 't', .5)] if density >= 1 else [(0, 'd', 1), (2.5, 't', .5)]
        for b, k, a in pat:
            tb = t + b * BEAT
            if tb >= t1: break
            add(mix, (dum if k == 'd' else tek)(a), tb, v, -.15 if k == 'd' else .25)
        t += 4 * BEAT; bar += 1
groove(8.6, 15.0, .5, .45); groove(15.0, 22.0, .5, .4); groove(22.0, 27.6, 1.0, .5); groove(36.4, 40.4, .5, .25)
# —— harp: dawn ostinato, then a note per landing character, a run on the grid, notes per action
def arp(t0, t1, notes, step=BEAT / 2, v=.38, g=.5):
    t = t0; k = 0
    while t < t1: harp(t, notes[k % len(notes)], v * (1 if k % 4 == 0 else .75), -.2 + .1 * (k % 5), g); t += step; k += 1
arp(0.0, 8.6, ['D3', 'A3', 'D4', 'F#4', 'A4', 'F#4', 'D4', 'A3'])
arp(8.6, 15.0, ['D3', 'A3', 'E4', 'F#4', 'B4', 'F#4', 'E4', 'A3'], v=.34)
arp(22.0, 27.6, ['D3', 'F#3', 'A3', 'D4', 'E4', 'D4', 'A3', 'F#3'], step=BEAT / 2, v=.32)
arp(27.6, 34.6, ['D3', 'A3', 'C4', 'F4', 'A3', 'C4'], step=BEAT, v=.3, g=.45)
li = 0
for x in EV:
    ty = x['type']
    if ty == 'land':
        p = pent(li % 10, 4); li += 1
        harp(x['t'], p, .55 if x.get('big') else .45, .2, .55)
        if x.get('accent'): kal(x['t'], pent(li % 5, 5), .55, -.2)
    elif ty == 'trace': harp(x['t'], pent(x['k'], 4), .5, -.4 + x['k'] * .1, .55)
    elif ty == 'edge': harp(x['t'], ['D5', 'F#5', 'A5'][x['k']], .55, .3, .55); kal(x['t'], ['D5', 'F#5', 'A5'][x['k']], .5, .3)
    elif ty == 'glyph': harp(x['t'], pent(x['k'] + 3, 4, MIN), .45, -.3 + x['k'] * .12, .5)
    elif ty == 'reveal':
        for k, p in enumerate(['D3', 'A3', 'D4', 'F#4', 'A4', 'D5', 'F#5']): harp(x['t'] + k * .09, p, .55, -.3 + k * .1, .6, 4.0)
    elif ty == 'thunk': harp(x['t'], 'D2', .6, 0, .5, 2.0)
# —— flute: phrases in the gaps between lines, soft under the voice
FL = [(0.2, 'A4', .7), (1.0, 'B4', .35), (1.4, 'D5', 1.4), (3.0, 'B4', .5), (3.6, 'A4', 1.2),
      (14.6, 'F#5', .4), (14.95, 'A5', .5),
      (21.6, 'E5', .3), (21.9, 'D5', .4),
      (27.4, 'A4', .4), (27.9, 'C5', .5), (28.6, 'A4', 1.2), (34.1, 'F4', .6), (34.6, 'D4', 2.0),
      (40.2, 'A4', .4), (40.6, 'B4', .3), (40.9, 'D5', .6), (41.6, 'F#5', 1.0), (43.0, 'E5', .5), (43.6, 'D5', 2.6)]
fl = S.render([(t, 'flute', p, d, .42, .15, .8) for t, p, d in FL], dur=DUR, master=False)
mix[:len(fl)] += fl[:N] * .9
# final low D on harp
harp(43.6, 'D2', .6, 0, .55, 4.0)
mix = S.room(mix, size=.5, mix=.22)
mix = np.tanh(mix * .9) * .85
sf.write(os.path.join(HERE, 'out', 'music.wav'), mix.astype(np.float32), SR)
print('music', DUR, float(np.abs(mix).max()))

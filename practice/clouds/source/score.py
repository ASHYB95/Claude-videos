# Original West-Coast cool jazz, 120 BPM swing (bar 2.0 s, beat 0.5 s), F major.
# Vibraphone comping + a chord per step (stamped with each medallion), flute melody, walking pizzicato bass,
# brushes (snare taps + swish) and a light ride, finger snaps, glockenspiel "celesta" plinks for droplets.
# Sections: intro 0–6 · step 1 6–12 · step 2 12–20 · step 3 20–28 (half-time feel) · step 4 28–36 (silence 33.5–34.0) · payoff 36–42 · tip 42–46.5 · end tag
import sys, os, json
sys.path.insert(0, os.environ.get('LIB', '.'))
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from core.audio import sampler as S
from core.audio.sfx import SR, add
HERE = os.path.dirname(os.path.abspath(__file__))
S.seed(5)
BAR, BEAT = 2.0, 0.5
SW = 0.62                     # swing ratio of the off-beat 8th
DUR = 49.5; N = int(DUR * SR)
EV = json.load(open(os.path.join(HERE, 'events.json')))['ev']
rng = np.random.default_rng(3)
m = S.midi
# progression per bar (I–vi–ii–V family in F, with step chords on the stamps)
PROG = {  # bar index → (root, chord tones for vibes, scale for the walk)
}
CH = {'F': ('F2', ['A3', 'C4', 'E4', 'G4']), 'Dm': ('D2', ['F3', 'A3', 'C4', 'E4']), 'Gm': ('G2', ['Bb3', 'D4', 'F4', 'A4']), 'C7': ('C2', ['Bb3', 'E4', 'G4', 'D5']),
      'Am': ('A2', ['C4', 'E4', 'G4', 'B4']), 'Bb': ('Bb2', ['D4', 'F4', 'A4', 'C5']), 'Eb7': ('Eb2', ['G3', 'Db4', 'F4', 'Bb4'])}
SEQ = ['F', 'Dm', 'Gm', 'C7']
STEPCH = ['F', 'Gm', 'Am', 'Bb']           # each step's own vibraphone chord
def chord_at(bar):
    t = bar * BAR
    if 6 <= t < 12: base = ['F', 'Dm', 'Gm'][int((t - 6) // 2) % 3]
    elif 12 <= t < 20: base = ['Gm', 'C7', 'F', 'Dm'][int((t - 12) // 2) % 4]
    elif 20 <= t < 28: base = ['Am', 'Dm', 'Gm', 'C7'][int((t - 20) // 2) % 4]
    elif 28 <= t < 36: base = ['Bb', 'Gm', 'C7', 'F'][int((t - 28) // 2) % 4]
    elif 36 <= t < 42: base = ['F', 'Bb', 'C7'][int((t - 36) // 2) % 3]
    else: base = SEQ[bar % 4]
    return base
ev = []
def note(t, inst, p, d, v, pan=0, g=1): ev.append((t, inst, p, d, v, pan, g))
sw8 = lambda b: b * BEAT if b == int(b) else (int(b) + SW) * BEAT   # swung 8th positions
nbars = int(DUR // BAR) + 1
for bar in range(nbars):
    t0 = bar * BAR
    if t0 >= 46.5: break
    hush = 33.5 <= t0 + 1.9 and t0 < 34.0
    root, tones = CH[chord_at(bar)]
    half = 20 <= t0 < 28            # step 3: half-time feel (lighter, longer notes)
    intro = t0 < 6
    # walking bass (quarters), half notes in step 3
    scale = [m(root), m(root) + 4 if chord_at(bar) in ('F', 'Bb') else m(root) + 3, m(root) + 7, m(root) + 9 if chord_at(bar) in ('F', 'Bb') else m(root) + 10]
    beats = [0, 2] if half else [0, 1, 2, 3]
    for i, b in enumerate(beats):
        tt = t0 + b * BEAT
        if 33.5 <= tt < 34.0: continue
        if intro and b > 0 and t0 < 2: continue
        note(tt, 'contrabass_pizz', scale[i % 4] + (0 if i < 2 else 0), BEAT * (1.9 if half else 0.95), .62, .1)
    # vibraphone comp: "Charleston" (1 and the and-of-2), soft mallets
    if not (33.5 <= t0 + 1.0 < 34.0):
        for b in ([0, 1.5] if not half else [0]):
            for k, p in enumerate(tones):
                note(t0 + sw8(b) + k * .012, 'vibraphone', p, BEAT * (1.4 if b == 0 else .9) * (2 if half else 1), .36 if not intro else .3, -.25 + k * .15, .9)
    # brushes + ride (from step 1), snaps in the intro
    if intro:
        for b in (1, 3): ev.append(('snap', t0 + b * BEAT))
    else:
        for b in range(4):
            tt = t0 + b * BEAT
            if 33.5 <= tt < 34.0: continue
            if not half or b in (1, 3): ev.append(('brush', tt, .5 if b % 2 else .32))
            ev.append(('ride', tt, .26));
            if not half: ev.append(('ride', t0 + (b + SW) * BEAT, .14))
        ev.append(('swish', t0, BAR))
# flute melody: a simple swung tune in F, phrased between narration lines (sparse under voice)
MEL = [  # (time, pitch, dur)
    (0.0, 'C5', .4), (0.33, 'D5', .2), (0.5, 'F5', .9), (1.5, 'A5', .4), (2.0, 'G5', .9), (3.0, 'F5', .4), (3.33, 'D5', .4), (4.0, 'C5', 1.2), (5.0, 'A4', .4), (5.33, 'C5', .4),
    (10.9, 'F5', .3), (11.2, 'G5', .3), (11.5, 'A5', .5),
    (18.2, 'D5', .3), (18.5, 'F5', .3), (18.8, 'A5', .3), (19.1, 'C6', .8),
    (27.0, 'A5', .3), (27.3, 'G5', .3), (27.6, 'E5', .6),
    (36.0, 'F5', .4), (36.33, 'A5', .4), (36.66, 'C6', .6), (40.3, 'C6', .3), (40.6, 'A5', .3), (40.9, 'F5', .3), (41.2, 'G5', .3), (41.5, 'A5', .9),
    (46.5, 'C6', .5), (47.0, 'A5', .5), (47.5, 'F5', 1.6)]
for t, p, d in MEL: note(t, 'flute', p, d, .45, .2, .8)
# step chords (vibes, hard mallets, rolled) on each iris and each payoff medallion; glock plinks for droplets
for x in EV:
    if x['type'] == 'chord':
        root, tones = CH[STEPCH[x['i']]]
        for k, p in enumerate(tones + [S.name(m(tones[0]) + 12)]): note(x['t'] + k * .035, 'vibraphone_hard', p, 1.6, .5, -.3 + k * .15, 1.0)
    if x['type'] == 'plink': note(x['t'], 'glockenspiel', ['C6', 'E6', 'G6', 'A6', 'C7', 'E7'][x['i']], 1.2, .5, -.2 + x['i'] * .08)
    if x['type'] == 'letter' and x['i'] % 2 == 0: note(x['t'], 'glockenspiel', S.name(m('C6') + [0, 2, 4, 5, 7, 9, 11, 12][(x['i'] // 2) % 8]), .5, .28, .3)
    if x['type'] == 'tick': note(x['t'], 'glockenspiel', ['G6', 'E6', 'C6'][x['k']], .8, .4, .3)
    if x['type'] == 'confetti':
        for k, p in enumerate(['F5', 'A5', 'C6', 'F6', 'A6']): note(x['t'] + k * .05, 'glockenspiel', p, 1.0, .4, -.3 + k * .15)
# final chord (vibes tremolo) at 46.5 → ring
for k, p in enumerate(['F3', 'A3', 'C4', 'E4', 'G4']):
    for r in range(10): note(46.5 + r * .11 + k * .01, 'vibraphone', p, .5, .3 * (1 - r / 12), -.3 + k * .15, .9)
note(46.5, 'contrabass_pizz', 'F2', 2.0, .7, .1)
# rain: descending glock drops
for i, p in enumerate(['A6', 'F6', 'D6', 'C6', 'A5', 'F5']): note(44.25 + i * .18, 'glockenspiel', p, .8, .35, .2 - i * .08)
mix = S.render([e for e in ev if isinstance(e[1], str) and e[0] not in ('snap', 'brush', 'ride', 'swish')], dur=DUR, master=False)
def sos(k, f, o=2): return butter(o, f, k, fs=SR, output='sos')
def tt_(d): return np.arange(int(d * SR)) / SR
for e in ev:
    if e[0] == 'snap': x = sosfilt(sos('band', [1800, 4500]), rng.standard_normal(int(.08 * SR))) * np.exp(-tt_(.08) / .012); add(mix, x * .5, e[1], .6, .25)
    if e[0] == 'brush': x = S.hit('snare2', 'taps', e[2]); add(mix, x, e[1], .5, -.1)
    if e[0] == 'ride':
        d = .5; tt = tt_(d); x = sosfilt(sos('high', 5000), rng.standard_normal(len(tt))) * np.exp(-tt / .18) * .5 + sum(np.sin(2 * np.pi * f * tt) for f in (3100, 4270, 5890)) * np.exp(-tt / .25) * .05
        add(mix, x * e[2], e[1], .7, .35)
    if e[0] == 'swish': d = e[2]; tt = tt_(d); x = sosfilt(sos('band', [2500, 8000]), rng.standard_normal(len(tt))) * (0.4 + 0.6 * np.sin(np.pi * tt / d)) * .03; add(mix, x, e[1], 1, -.2)
mix = S.room(mix, size=.4, mix=.18)
mix = np.tanh(mix * .9) * .85
sf.write(os.path.join(HERE, 'out', 'music.wav'), mix.astype(np.float32), SR)
print('music', DUR, float(np.abs(mix).max()))

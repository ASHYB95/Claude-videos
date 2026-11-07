# Score: Minuet in G major, BWV Anh. 114 (Petzold, public domain), chamber arrangement on the film's grid (♩=120, 3/4, bar 1.5 s)
# 0–10.5 "before": lazy solo bassoon · 10.5–22.5 full A (clarinet, nylon guitar, pizz bass, shaker) · 22.5–27 B, light (waiting)
# 27–28.5 silence · 28.5–34.5 B continued, full · 34.5–40.5 last A phrase, ritardando, final chord + music box
import sys, json, os
sys.path.insert(0, os.environ.get('LIB', '.'))
import numpy as np, soundfile as sf
from core.audio import sampler as S, pluck as P
from core.audio.sfx import SR, add, limit
HERE = os.path.dirname(os.path.abspath(__file__))
S.seed(7)
q, e, h, dq = 1.0, 0.5, 2.0, 3.0   # in beats
MEL = {  # bar: [(pitch, beats)]
 1: [('D5', q), ('G4', e), ('A4', e), ('B4', e), ('C5', e)], 2: [('D5', q), ('G4', q), ('G4', q)],
 3: [('E5', q), ('C5', e), ('D5', e), ('E5', e), ('F#5', e)], 4: [('G5', q), ('G4', q), ('G4', q)],
 5: [('C5', q), ('D5', e), ('C5', e), ('B4', e), ('A4', e)], 6: [('B4', q), ('C5', e), ('B4', e), ('A4', e), ('G4', e)],
 7: [('F#4', q), ('G4', e), ('A4', e), ('B4', e), ('G4', e)], 8: [('A4', dq)],
 13: [('C5', q), ('D5', e), ('C5', e), ('B4', e), ('A4', e)], 14: [('B4', q), ('C5', e), ('B4', e), ('A4', e), ('G4', e)],
 15: [('A4', q), ('B4', e), ('A4', e), ('G4', e), ('F#4', e)], 16: [('G4', dq)],
 17: [('B5', q), ('G5', e), ('A5', e), ('B5', e), ('G5', e)], 18: [('A5', q), ('D5', e), ('E5', e), ('F#5', e), ('D5', e)],
 19: [('G5', q), ('E5', e), ('F#5', e), ('G5', e), ('D5', e)], 20: [('C#5', q), ('B4', e), ('C#5', e), ('A4', q)],
 21: [('A4', e), ('B4', e), ('C#5', e), ('D5', e), ('E5', e), ('F#5', e)], 22: [('G5', q), ('F#5', q), ('E5', q)],
 23: [('F#5', q), ('A4', q), ('C#5', q)], 24: [('D5', dq)],
}
CH = {1: 'G', 2: 'G', 3: 'C', 4: 'G', 5: 'Am', 6: 'G', 7: 'D', 8: 'D', 13: 'C', 14: 'G', 15: 'D', 16: 'G',
      17: 'G', 18: 'D', 19: 'Em', 20: 'A', 21: 'A', 22: 'Em', 23: 'A', 24: 'D'}
CHN = {'G': ('G2', 'B3', 'D4'), 'C': ('C3', 'E3', 'G3'), 'Am': ('A2', 'C4', 'E4'), 'D': ('D3', 'F#3', 'A3'),
       'Em': ('E2', 'G3', 'B3'), 'A': ('A2', 'C#4', 'E4')}
# (start time, bar list, section)
PLAN = [(0.0, [1, 2, 3, 4, 5, 6, 7], 'before'), (10.5, [1, 2, 3, 4, 5, 6, 15, 16], 'full'),
        (22.5, [17, 18, 19], 'light'), (28.5, [21, 22, 23, 24], 'full'), (34.5, [13, 14, 15, 16], 'end')]
BEAT = 0.5
ev = []
def melody(t0, bar, inst, shift=0, vel=.62, pan=-.15, stretch=1.0, gain=1.0):
    t = t0
    for p, b in MEL[bar]:
        d = b * BEAT * stretch
        ev.append((t, inst, S.midi(p) + shift, d * .95, vel + (.06 if t == t0 else 0), pan, gain)); t += d
def accomp(t0, bar, guitar=True, bass=True, shaker=False, stretch=1.0, vel=.55):
    r, a, b = CHN[CH[bar]]; B = BEAT * stretch
    if bass: ev.append((t0, 'contrabass_pizz', S.midi(r) + (12 if S.midi(r) < 40 else 0), 1.2 * stretch, vel + .1, .1))
    if guitar:
        ev.append(('pl', t0, S.midi(r) + 12, 1.4 * stretch, vel, .25))
        for k in (1, 2): ev.append(('pl', t0 + k * B, S.midi(a), .5 * stretch, vel * .8, .3)); ev.append(('pl', t0 + k * B + .02, S.midi(b), .5 * stretch, vel * .75, .35))
    if shaker:
        for k in range(3): ev.append((t0 + k * B, 'shaker', 'down' if k == 0 else 'up', None, .22 if k else .3, -.3))
for t0, bars, sec in PLAN:
    t = t0
    for i, bar in enumerate(bars):
        last = sec == 'end' and i == len(bars) - 1
        st = 1.0 if not last else 1.0
        if sec == 'before':
            melody(t, bar, 'bassoon', -12, vel=.5, pan=0)
            if i % 2 == 0: accomp(t, bar, guitar=False, vel=.4)
        elif sec == 'full':
            melody(t, bar, 'clarinet', 0, vel=.62)
            accomp(t, bar, shaker=True)
        elif sec == 'light':
            melody(t, bar, 'clarinet_stac', -12, vel=.55)
            accomp(t, bar, guitar=True, bass=False, vel=.42)
        elif sec == 'end':
            stretch = 1.0 + (0.35 if i == len(bars) - 2 else 0)
            melody(t, bar, 'clarinet', 0, vel=.6)
            melody(t, bar, 'flute', 12, vel=.38, pan=.2, gain=.6)
            if not last: accomp(t, bar, shaker=False)
        t += 1.5
# final chord (bar 16 of the end phrase lands at 39.0)
for p in ('G2', 'D3', 'G3', 'B3', 'D4'): ev.append(('pl', 39.0, S.midi(p), 2.5, .5, .2))
ev.append((39.0, 'contrabass_pizz', S.midi('G2'), 2.0, .6, .1))
# glockenspiel on each ingredient landing + sparkles + end ping, from the picture's events
EVS = json.load(open(os.path.join(HERE, 'events.json')))['ev']
GL = ['G5', 'B5', 'D6', 'G6', 'B6', 'D7']
for x in EVS:
    if x['type'] == 'glock': ev.append((x['t'], 'glockenspiel', GL[x['i']], 1.5, .55, (x.get('pan') or 0) * .5))
    if x['type'] == 'sparkle': ev.append((x['t'], 'glockenspiel', 'D7', 1.0, .3, .3))
    if x['type'] == 'musicbox':
        ev.append(('mb', x['t'], S.midi('G6'), 0, .7, .1)); ev.append(('mb', x['t'] + .25, S.midi('D6'), 0, .5, -.1)); ev.append(('mb', x['t'] + .5, S.midi('G5'), 0, .5, 0))
# render
DUR = 42.0
smp = [x for x in ev if x[0] not in ('pl', 'mb')]
mix = S.render(smp, dur=DUR, master=False)
for x in ev:
    if x[0] == 'pl': add(mix, P.pluck('nylon_guitar', x[2], x[3] + .6, vel=x[4]), x[1], .55, x[5])
    if x[0] == 'mb': add(mix, P.pluck('music_box', x[2], None, vel=x[4]), x[1], .5, x[5])
mix = S.room(mix, size=.35, mix=.16)
mix = limit(mix, .9)
sf.write(os.path.join(HERE, 'out', 'music.wav'), mix.astype(np.float32), SR)
print('music', mix.shape[0] / SR, 's peak', float(np.abs(mix).max()))

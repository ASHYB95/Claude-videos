"""Right4Paws · How to Serve — original score: a West-Coast cool-jazz combo.
vibraphone (chords, step chords, glissandi) / flute (theme) / jazz double bass (walking) / brushes + ride / celesta / finger snaps.
♩ = 120, 4/4 (bar = 2 s), 46 s = 23 bars. F major; back up a whole step (G major) from 34.0.
Run from the library root: .venv/bin/python <project>/music/score.py
"""
import sys, os, json
sys.path.insert(0, '.')
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from core.audio import sampler as S
from core.audio.sfx import SR, add

OUT = os.path.dirname(os.path.abspath(__file__))
S.seed(4)
rng = np.random.default_rng(4)
B = 0.5; BAR = 4 * B; DUR = 46.0; N = int(round(DUR * SR)); SW = 0.6


def T(bar, beat=0.0, swing=SW):
    whole = np.floor(beat + 1e-9); frac = beat - whole
    if abs(frac - .5) < 1e-6: frac = swing
    return (bar - 1) * BAR + (whole + frac) * B


def M(p): return S.midi(p) if isinstance(p, str) else p
def jit(ms=6): return float(rng.uniform(-ms, ms)) / 1000
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)


stems = {k: np.zeros((N, 2), np.float32) for k in ('drums', 'bass', 'vib', 'lead')}
hits = []
def hit(t, label): hits.append(dict(t=round(float(t), 4), label=label))


def motor(x, rate=5.0, depth=.3, t0=0.0):
    t = np.arange(len(x)) / SR + t0
    return x * (1 - depth * (.5 + .5 * np.sin(2 * np.pi * rate * t))).astype(np.float32)


def vib(t, pitches, dur, vel=.4, pan=-.25, hard=False, trem=0.0, gain=1.0):
    for i, p in enumerate(pitches if isinstance(pitches, (list, tuple)) else [pitches]):
        x = S.note('vibraphone_hard' if hard else 'vibraphone', M(p), dur, vel=vel)
        if trem: x = motor(x, depth=trem, t0=i * .013)
        add(stems['vib'], x, t + i * .004, gain, pan + (i - 1.5) * .07)


def vib_run(t0, pitches, step, vel0=.3, vel1=.6, pan=-.2, ring=1.0):
    n = len(pitches)
    for i, p in enumerate(pitches):
        add(stems['vib'], S.note('vibraphone_hard', M(p), ring, vel=vel0 + (vel1 - vel0) * i / max(1, n - 1)), t0 + i * step, 1.0, pan + .5 * i / n - .25)


def flute(t, p, beats, vel=.5, stac=False, pan=.22, gain=1.0):
    if stac and M(p) >= 69: x = S.note('flute_stac', M(p), .2, vel=vel)
    else: x = S.note('flute', M(p), max(.12, beats * B * .9), vel=vel, release=.09)
    add(stems['lead'], x, t - .02, gain, pan)


def celesta(t, p, vel=.5, pan=.35, gain=1.0):
    g = S.note('glockenspiel', M(p), 2.0, vel=min(.5, vel * .7))
    f = S.hz(M(p)); d = 1.6; tt = np.arange(int(d * SR)) / SR
    s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / .55) + .35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / .18)) * np.minimum(1, tt / .002)
    x = np.zeros(max(len(g), len(s)), np.float32); x[:len(g)] += g * .6; x[:len(s)] += (s * .22 * vel).astype(np.float32)
    add(stems['lead'], x, t, gain, pan)


def bass(t, p, beats=.9, vel=.6, gain=1.0):
    add(stems['bass'], S.note('jazz_bass', M(p), max(.1, beats * B), vel=vel, release=.08), t - .015, gain, 0)


def dk(t, var, vel, dur=None, pan=.3, gain=1.0): add(stems['drums'], S.hit('drum_kit', var, vel, dur), t, gain, pan)


def brush_tap(t, v=.5, pan=-.1):
    d = .16; tt = np.arange(int(d * SR)) / SR; n = rng.standard_normal(len(tt))
    x = bp(n, 1500, 9000) * np.exp(-tt / .045) + .5 * bp(n, 300, 1200) * np.exp(-tt / .02) + .25 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / .03)
    add(stems['drums'], (x / 3.2 * v).astype(np.float32), t, 1, pan)


def brush_sweep(t, d, v=.3, pan=-.15):
    tt = np.arange(int(d * SR)) / SR; n = rng.standard_normal(len(tt))
    x = bp(n, 1800, 7500) + .35 * bp(n, 500, 1800)
    add(stems['drums'], (x * np.sin(np.pi * tt / d) ** 1.5 / 4 * v).astype(np.float32), t, 1, pan)


def snap(t, v=.6, pan=.35):
    """finger snap: a bright noise crack + a tiny skin pop"""
    d = .09; tt = np.arange(int(d * SR)) / SR; n = rng.standard_normal(len(tt))
    x = bp(n, 1800, 6500, 3) * np.exp(-tt / .012) + .4 * np.sin(2 * np.pi * 1100 * tt) * np.exp(-tt / .008)
    add(stems['drums'], (x / 2.2 * v).astype(np.float32), t, 1, pan)


def brushes(bar0, bar1, v=.3):
    for bar in range(bar0, bar1):
        for h in (0, 2): brush_sweep(T(bar, h) + jit(4), 2 * B * 1.05, v * .8)
        for bt in (1, 3):
            brush_tap(T(bar, bt) + jit(4), v * 1.25)
            add(stems['drums'], S.hit('hihat', 'pedal', .35 * v / .3, .3), T(bar, bt) + .004, .45, .45)


def ride(bar0, bar1, vel=.3):
    for bar in range(bar0, bar1):
        for b in [0, 1, 1.5, 2, 3, 3.5]:
            dk(T(bar, b, .58) + jit(4), 'ride_right', vel * (1.0 if b in (1, 3) else .7), dur=1.4, pan=.35, gain=.6)
        for bt in (1, 3): add(stems['drums'], S.hit('hihat', 'pedal', .4, .3), T(bar, bt) + .004, .5, .45)


# ---------------------------------------------------------------- harmony
V = {  # vibraphone voicings (rootless, all ≥ F3)
    'Fmaj7': ['A3', 'C4', 'E4', 'G4'], 'F69': ['A3', 'D4', 'G4', 'C5'], 'D7': ['F#3', 'C4', 'E4', 'A4'], 'Gm7': ['F3', 'Bb3', 'D4', 'F4'],
    'C7': ['G3', 'Bb3', 'E4', 'A4'], 'Bbmaj7': ['A3', 'D4', 'F4', 'C5'], 'Eb9': ['G3', 'Db4', 'F4', 'Bb4'], 'Am7': ['G3', 'C4', 'E4', 'G4'],
    'Gm9': ['F3', 'Bb3', 'D4', 'A4'], 'C13': ['Bb3', 'E4', 'A4', 'D5'], 'D7b9': ['F#3', 'C4', 'Eb4', 'A4'], 'C7sus': ['Bb3', 'C4', 'F4', 'G4'],
    # G major (up a whole step)
    'G69': ['B3', 'E4', 'A4', 'D5'], 'Gmaj7': ['F#3', 'B3', 'D4', 'A4'], 'E7': ['G#3', 'D4', 'F#4', 'B4'], 'Am7g': ['G3', 'C4', 'E4', 'G4'],
    'D7g': ['F#3', 'C4', 'E4', 'A4'], 'Bm7': ['A3', 'D4', 'F#4', 'A4'], 'Cmaj7': ['B3', 'E4', 'G4', 'C5'], 'Am9': ['G3', 'C4', 'E4', 'B4'],
}
ROOT = {'Fmaj7': 'F2', 'F69': 'F2', 'D7': 'D2', 'Gm7': 'G2', 'C7': 'C2', 'Bbmaj7': 'Bb1', 'Eb9': 'Eb2', 'Am7': 'A2', 'Gm9': 'G2', 'C13': 'C2',
        'D7b9': 'D2', 'C7sus': 'C2', 'G69': 'G2', 'Gmaj7': 'G2', 'E7': 'E2', 'Am7g': 'A2', 'D7g': 'D2', 'Bm7': 'B1', 'Cmaj7': 'C2', 'Am9': 'A2'}
QUAL = lambda c: 3 if ('m' in c and 'maj' not in c) else 4
# bar → chords (one per bar, or two per bar on beats 0 and 2)
PROG = {1: ['Fmaj7', 'D7'], 2: ['Gm7', 'C7'], 3: ['Fmaj7', 'D7'], 4: ['Gm7', 'C7'], 5: ['F69'], 6: ['Bbmaj7'], 7: ['Am7', 'D7'], 8: ['Gm7', 'C7'],
        9: ['Bbmaj7'], 10: ['Eb9'], 11: ['Am7', 'D7'], 12: ['Gm9'], 13: ['C13'], 14: ['Fmaj7', 'D7b9'], 15: ['Gm9', 'C13'], 16: ['Gm7', 'C7'], 17: ['D7g'],
        18: ['Gmaj7', 'E7'], 19: ['Am7g', 'D7g'], 20: ['Bm7', 'E7'], 21: ['Am7g', 'D7g'], 22: ['G69'], 23: ['G69']}


def walk(bar, vel=.6):
    """walking bass: quarter notes, chromatic approach into the next chord"""
    ch = PROG.get(bar); nxt = PROG.get(bar + 1) or PROG.get(bar + 2) or ch
    if not ch: return
    beats = []
    for i, c in enumerate(ch):
        r = M(ROOT[c]); n = 4 // len(ch)
        pat = [r, r + QUAL(c), r + 7, r + 9] if n == 4 else [r, r + 7]
        beats += pat[:n]
    nr = M(ROOT[(nxt or ch)[0]]); beats[-1] = nr + (1 if beats[-1] > nr else -1)
    for b, p in enumerate(beats):
        while p > M('G3'): p -= 12
        bass(T(bar, b) + jit(5), p, .92, vel * (1.0 if b in (0, 2) else .86))


def comp(bar, vel=.3, charleston=True):
    ch = PROG[bar]
    for i, c in enumerate(ch):
        b0 = i * (4 // len(ch))
        vib(T(bar, b0) + jit(3), V[c], 1.4 * B, vel)
        if charleston and len(ch) == 1: vib(T(bar, 1.5) + jit(3), V[c], .6 * B, vel * .75)


THEME = [  # (bar offset, beat, note, beats, stac) — F major, original
    (0, 0.0, 'C5', .5, 0), (0, 0.5, 'D5', .5, 0), (0, 1.0, 'F5', 1.0, 0), (0, 2.0, 'A5', .5, 1), (0, 2.5, 'G5', .5, 0), (0, 3.0, 'F5', .5, 0), (0, 3.5, 'D5', .5, 0),
    (1, 0.0, 'E5', 1.5, 0), (1, 1.5, 'C5', .5, 0), (1, 2.0, 'D5', .5, 1), (1, 2.5, 'F5', .5, 0), (1, 3.0, 'A4', 1.0, 0),
]
def theme(bar0, vel=.45, up=0, skip=()):
    for bo, bt, p, ln, st in THEME:
        if (bo, bt) in skip: continue
        flute(T(bar0 + bo, bt) + jit(4), M(p) + up, ln, vel, stac=bool(st))


# ================================================================ 0–4 hook: snaps + walking bass, a stab on the pack (2.5)
for bar in (1, 2):
    for bt in (1, 3): snap(T(bar, bt) + jit(3), .55)
    walk(bar, .55)
vib(T(1, 0), V['Fmaj7'], 1.2 * B, .22)
hit(2.5, 'pack thump: vib stab + kick')
vib(2.5, V['C7'], .5 * B, .45, hard=True); dk(2.5, 'kick_drum_left', .5, pan=0, gain=.55)
# ================================================================ 4–8 title: band in, theme under the narration, three stamps, gliss into the iris
hit(4.0, 'title: band in'); dk(4.0, 'crash_right', .35, dur=2.0, pan=.35, gain=.4)
brushes(3, 5, .28)
for bar in (3, 4): walk(bar, .6); comp(bar, .26)
theme(3, .36)
for i, (t, p) in enumerate([(6.0, 'A4'), (6.5, 'C5'), (7.0, 'F5')]): vib(t, [p, M(p) + 12], .8, .55, hard=True); hit(t, f'stamp {i + 1}')
vib_run(7.5, ['C4', 'D4', 'F4', 'G4', 'A4', 'C5', 'D5', 'F5', 'G5', 'A5'], .048, .25, .6); hit(7.5, 'iris gliss')
# ================================================================ 8–16 step 1 (F6/9). Land on 10.0; music cut 11.5–12.0; ding 12.0
hit(8.0, 'STEP 1 chord F6/9'); vib(8.0, V['F69'], 2.4 * B, .55, hard=True, trem=.3); celesta(8.0, 'F6', .45)
brushes(5, 9, .3)
for bar in (5, 6, 7, 8): walk(bar, .6)
comp(6, .28); comp(7, .28); comp(8, .28)
flute(9.5, 'C5', .5, .4); flute(T(5, 3.5), 'F5', .5, .45); vib(10.0, ['F4', 'A4', 'C5'], .4, .5, hard=True); hit(10.0, 'land')
for k, p in enumerate(['A5', 'G5', 'A5', 'G5', 'A5', 'G5']): flute(10.5 + k * .17, p, .3, .22, pan=.3)   # needle wobble trill
hit(12.0, 'ding: 30 kg'); celesta(12.0, 'A6', .7); celesta(12.02, 'F6', .5); vib(12.0, V['F69'], 1.6, .4, trem=.3)
celesta(14.0, 'C7', .45)
for bt, p in [(2, 'A4'), (2.5, 'C5'), (3, 'D5'), (3.5, 'F5')]: flute(T(8, bt), p, .5, .38)
# ================================================================ 16–22 step 2 (B♭maj7): scoop 17.0, lift 18.1, flick 19.05, call-out 19.5
hit(16.0, 'STEP 2 chord Bbmaj7'); vib(16.0, V['Bbmaj7'], 2.4 * B, .55, hard=True, trem=.3)
brushes(9, 12, .3)
for bar in (9, 10, 11): walk(bar, .6)
comp(10, .26); comp(11, .26)
flute(18.1, 'D6', .5, .4, stac=True); flute(19.05, 'F6', .3, .45, stac=True); celesta(19.5, 'D6', .6); celesta(20.0, 'F6', .4)
for bt, p in [(2, 'C5'), (2.5, 'D5'), (3, 'F5'), (3.5, 'G5')]: flute(T(11, bt), p, .5, .38)
# ================================================================ 22–32 step 3 (Gm9): bands on 24.5 / 26.5 / 30.0; stop dead at 32.0
hit(22.0, 'STEP 3 chord Gm9'); vib(22.0, V['Gm9'], 2.4 * B, .55, hard=True, trem=.3)
brushes(12, 17, .3)
for bar in (12, 13, 14, 15, 16): walk(bar, .6)
comp(13, .26); comp(14, .26); comp(15, .26)
for t, p in [(24.5, 'D6'), (26.5, 'F6'), (30.0, 'A6')]:
    celesta(t, p, .6); vib_run(t, [M(p) - 12 - 7, M(p) - 12 - 3, M(p) - 12], .06, .3, .45, ring=.8); hit(t, 'band on')
comp(16, .26); flute(T(16, 2), 'G5', 1.0, .38)
# bar 17 (32–34): the bowl comes down — the band keeps going on D7 and walks up into G
brushes(17, 18, .3); walk(17, .6); vib(32.0, V['D7g'], 2.6 * B, .36, trem=.3); vib(T(17, 2), V['D7g'], 1.4 * B, .3)
for bt, p in [(2.0, 'D5'), (2.5, 'E5'), (3.0, 'F#5'), (3.5, 'A5')]: flute(T(17, bt), p, .5, .38)
celesta(33.6, 'D7', .35)
# ================================================================ 32.0–33.6 total silence (enforced below); 33.6 clink is foley
# ================================================================ 34–40 up a whole step (G): sticks + theme, then the tip
hit(34.0, 'BACK UP A STEP: G'); vib(34.0, V['G69'], 2 * B, .6, hard=True, trem=.3); dk(34.0, 'crash_right', .5, dur=2.4, pan=.35, gain=.55)
dk(34.0, 'kick_drum_left', .45, pan=0, gain=.55); celesta(34.0, 'G6', .55)
ride(18, 20, .3)
for bar in (18, 19, 20, 21): walk(bar, .62)
comp(18, .3); comp(19, .28); comp(20, .26); comp(21, .26)
theme(18, .4, up=2)
brushes(20, 22, .26)
hit(37.2, 'arrow: flute slide down'); [flute(37.2 + k * .07, p, .2, .28) for k, p in enumerate(['D6', 'C6', 'B5', 'A5', 'G5', 'F#5'])]
celesta(38.6, 'B6', .55); hit(38.6, 'pill pop')
# ================================================================ 40–46 end card: theme reprise, summary chords (the three step chords, up a step), final ring
dk(40.0, 'crash_right', .3, dur=2.0, pan=.35, gain=.35)
theme(21, .3, up=2, skip={(1, 3.0)})
hit(42.0, 'summary chords'); [vib(t, V[c], .9, .42, hard=True, trem=.25) for t, c in [(42.0, 'G69'), (42.5, 'Cmaj7'), (43.0, 'Am9')]]
bass(42.0, 'G2', .9, .55); bass(42.5, 'C2', .9, .55); bass(43.0, 'A1', .9, .55); bass(43.5, 'D2', .9, .55)
hit(44.0, 'final G6/9'); vib(44.0, V['G69'] + ['G5'], 2.0, .5, hard=True, trem=.3); bass(44.0, 'G1', 3.0, .6); celesta(44.0, 'D7', .5); celesta(44.03, 'G6', .5)
brush_sweep(44.0, 1.4, .25)

# ---------------------------------------------------------------- silences + mixdown
def gate(x, t0, t1, fade=.025):
    a, b = int(t0 * SR), int(t1 * SR); f = int(fade * SR)
    x[max(0, a - f):a] *= np.linspace(1, 0, a - max(0, a - f))[:, None]; x[a:b] = 0
    if b < len(x): x[b:b + f] *= np.linspace(0, 1, min(f, len(x) - b))[:, None]
for k in stems:
    gate(stems[k], 11.5, 12.0)                # needle creep: music out for half a bar
fade = np.ones(N, np.float32); fs = int(44.6 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
gains = dict(drums=.8, bass=1.0, vib=.85, lead=.9)
mix = sum(stems[k] * gains[k] for k in stems) * fade[:, None]
mix = S.room(mix, size=.35, mix=.14)
gate(mix, 11.5, 12.0)
peak = np.max(np.abs(mix)) or 1
mix = (mix / peak * .89).astype(np.float32)
for k in stems: sf.write(os.path.join(OUT, f'stem_{k}.wav'), (stems[k] * gains[k] * fade[:, None] / peak * .89).astype(np.float32), SR)
sf.write(os.path.join(OUT, 'score.wav'), mix, SR)
json.dump(hits, open(os.path.join(OUT, 'hits.json'), 'w'), indent=1)
print('score.wav', round(N / SR, 2), 's · hits', len(hits))

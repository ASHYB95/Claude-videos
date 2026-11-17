# Original upbeat R&B, 92 BPM, F minor: Fm9 – B♭m9 – E♭maj9 – A♭maj7. All synthesised (no samples).
# Grid: a bar starts on the drop at 4.0 s. Intro keys+snaps · drop 4.0 · drums out 10.9 (riser) · back 11.83 · fill → 19.65 · break 24.87 · final hit 28.13
import os, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000; HERE = os.path.dirname(os.path.abspath(__file__))
BPM = 92; B = 60 / BPM; BAR = 4 * B; G0 = 4.0 - 2 * BAR
DUR = 30.5; N = int(DUR * SR)
L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(11)
def tt(d): return np.arange(int(d * SR)) / SR
def sos(kind, f, o=2): return butter(o, f, kind, fs=SR, output='sos')
def put(x, t, g=1.0, pan=0.0):
    s = int(t * SR)
    if s < 0: x = x[-s:]; s = 0
    e = min(N, s + len(x))
    if s >= N or e <= s: return
    x = x[:e - s] * g; L[s:e] += x * np.sqrt((1 - pan) / 2) * 1.414; R[s:e] += x * np.sqrt((1 + pan) / 2) * 1.414
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def rhodes(m, d, v=.5):
    t = tt(d + .8); f = hz(m); env = np.exp(-t / 1.6) * (1 - np.exp(-t / .004)); rel = np.clip((d + .8 - t) / .8, 0, 1)
    idx = 1.8 * np.exp(-t / .25) * v
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) + .25 * np.sin(2 * np.pi * 7.02 * f * t) * np.exp(-t / .05)
    return x * env * rel * v
def bass(m, d, v=.8):
    t = tt(d + .05); f = hz(m); x = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)
    x = np.tanh(x * 1.6) * (1 - np.exp(-t / .005)) * np.clip((d + .05 - t) / .05, 0, 1) * np.exp(-t / 1.2)
    return x * v
def kick(v=1):
    t = tt(.4); f = 45 + 80 * np.exp(-t / .03); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16) * v
def snare(v=1):
    t = tt(.3); n = sosfilt(sos('band', [900, 7000]), rng.standard_normal(len(t))) * np.exp(-t / .09)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05)
    clap = np.zeros(len(t))
    for dt in (0, .011, .023): s = int(dt * SR); clap[s:] += sosfilt(sos('band', [1200, 3500]), rng.standard_normal(len(t) - s)) * np.exp(-np.arange(len(t) - s) / SR / .03)
    return (n * .6 + tone * .5 + clap * .5) * v
def hat(v=1, open_=False):
    t = tt(.25 if open_ else .06); return sosfilt(sos('high', 7000), rng.standard_normal(len(t))) * np.exp(-t / (.08 if open_ else .015)) * v
def snap(v=1):
    t = tt(.08); return sosfilt(sos('band', [1800, 4500]), rng.standard_normal(len(t))) * np.exp(-t / .012) * v
def sq(m, d, v=.3):
    t = tt(d); return np.sign(np.sin(2 * np.pi * hz(m) * t)) * np.exp(-t / (d * .8)) * v * .35
CH = [[53, 56, 60, 63, 67], [58, 61, 65, 68, 72], [51, 55, 58, 62, 65], [56, 60, 63, 67, 70]]   # voicings (midi)
ROOT = [41, 46, 39, 44]
bars = [G0 + k * BAR for k in range(14)]
for k, b0 in enumerate(bars):
    if b0 > DUR: break
    c = k % 4; vo = CH[c]
    intro = b0 < 4.0 - 1e-3
    for i, m in enumerate(vo):   # keys: hit on 1, anticipated push on the "and" of 2
        put(rhodes(m, B * 1.6, .32 if not intro else .26), b0 + i * .008, 1, -.3 + i * .15)
        put(rhodes(m + (12 if i == 4 else 0), B * 1.2, .22), b0 + 2.5 * B + i * .008, 1, .3 - i * .15)
    for bt in (1, 3):            # snaps on 2 & 4
        put(snap(.55), b0 + bt * B, 1, .25)
    if intro: continue
    hush = b0 + BAR > 10.9 and b0 < 11.8
    drums = not hush and not (b0 > 24.8 and b0 < 27.4)
    if drums:
        for bt, v in ((0, 1), (1.75, .7), (2.5, .85)): put(kick(v), b0 + bt * B, .9)
        for bt in (1, 3): put(snare(.8), b0 + bt * B, .55, 0)
        for s in range(16):      # swung 16th hats
            off = (s // 2) * B / 2 + (s % 2) * B / 4 * 1.2 * (1 if s % 2 else 0)
            put(hat(.35 if s % 4 else .5, open_=(s == 14)), b0 + off, .5, .35)
    # bass line
    r = ROOT[c]
    for bt, d, dm in ((0, B * 1.4, 0), (1.75, B * .5, 0), (2.5, B * .9, 7 if c % 2 else 12), (3.5, B * .45, 10)):
        if hush and bt > 0: break
        put(bass(r + dm - 12, d, .75), b0 + bt * B, .9, 0)
# riser + pad in the hush (10.9 → 11.83), tom fill before 19.65
t = tt(.93); rz = sosfilt(sos('band', [400, 6000]), rng.standard_normal(len(t))) * (t / .93) ** 2 * .35
put(rz, 10.9, 1, 0)
for m in CH[2]: put(rhodes(m, .9, .2), 10.9, 1, 0)
for i, f in enumerate((180, 150, 120, 95)):
    tq = tt(.3); put(np.sin(2 * np.pi * np.cumsum(f * (1 + .5 * np.exp(-tq / .03))) / SR) * np.exp(-tq / .12) * .7, bars[6] - B + i * B / 4, 1, -.4 + i * .27)
put(sosfilt(sos('high', 3000), rng.standard_normal(SR * 2)) * np.exp(-tt(2) / .6) * .25, bars[6], 1, 0)   # crash
# final hit at 28.13 + chord ring
th = 28.13
put(kick(1.1), th, 1); put(sosfilt(sos('high', 3000), rng.standard_normal(SR * 2)) * np.exp(-tt(2) / .7) * .28, th, 1)
for i, m in enumerate(CH[0]): put(rhodes(m, 1.6, .4), th + i * .01, 1, -.3 + i * .15)
put(bass(29, 1.6, .9), th, 1)
# Delu's chiptune voice from the picture's events
EV = json.load(open(os.path.join(HERE, 'events.json')))['ev']
for x in EV:
    if x['type'] == 'spawn':
        for i, m in enumerate((72, 76, 79, 84)): put(sq(m, .09, .5), x['t'] + i * .06, 1, .2)
    if x['type'] == 'ding':
        for i, m in enumerate((77, 80, 84, 89)): put(sq(m, .12, .5), x['t'] + i * .07, 1, 0)
    if x['type'] == 'jump8': put(sq(84, .12, .5), x['t'], 1, .2); put(sq(91, .1, .4), x['t'] + .07, 1, .2)
    if x['type'] == 'sit8': put(sq(67, .1, .4), x['t'], 1, -.2)
# chiptune arp while the meter counts (11.9–13.0)
for i in range(12): put(sq([65, 68, 72, 75][i % 4] + 12 * (i // 8), .07, .32), 11.9 + i * .09, 1, .3)
# intro low-pass + master
mix = np.stack([L, R], 1)
cut = int(4.0 * SR); lp = sos('low', 1400)
mix[:cut] = sosfilt(lp, mix[:cut], axis=0) * 1.15
mix = np.tanh(mix * 0.9) * 0.8
fade = np.ones(N); fade[int(29.6 * SR):] = np.linspace(1, 0, N - int(29.6 * SR)); mix *= fade[:, None]
sf.write(os.path.join(HERE, 'out', 'music.wav'), mix.astype(np.float32), SR)
print('music', DUR, 'peak', float(np.abs(mix).max()))

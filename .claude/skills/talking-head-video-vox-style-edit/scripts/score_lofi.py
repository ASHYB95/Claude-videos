# Original lo-fi hip-hop bed for a talking-head Reel. Pure synthesis (numpy/scipy), no samples, no licensing.
# 84 BPM, swung 16ths, Dm9 - G13 - Cmaj9 - Am9 (one bar each), Rhodes-ish FM keys + soft pad with tape wobble,
# dusty kick/snare, sub bass, vinyl crackle.
#   0 - OPEN   hook: full beat but low-passed (under the face + first overlay)
#   OPEN       filter opens as the first collage scene lands
#   DROPS      one-beat drum drop before each section card (e.g. 01 / 02 / 03)
#   END        last chord rings under the end card, crackle tail to DUR
# Usage: python3 score_lofi.py --dur 86.7 --open 3.8 --drops 13.0,31.4,52.2 --end 84.3 --out audio/music.wav
# (reference values are SM explainer's). Can't listen? check it with ffmpeg showwavespic: no silent holes per bar.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
import sys
def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
SR = 44100; DUR = float(arg('--dur', 86.7)); N = int(SR * DUR)
OPEN = float(arg('--open', 3.8))
OUT = arg('--out', 'music.wav')
BPM = 84; BEAT = 60 / BPM; BAR = 4 * BEAT
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(84)

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if j > i and i >= 0: buf[i:j] += x[:j - i] * g

KEYS = np.zeros((N, 2)); DRUMS = np.zeros(N); BASS = np.zeros(N)
CH = [[53, 57, 60, 64], [53, 59, 64, 69], [52, 55, 59, 62], [55, 60, 64, 67]]   # Dm9, G13, Cmaj9, Am9 (upper voicings)
RT = [38, 43, 36, 45]
END = float(arg('--end', DUR - 2.4))

# ---- Rhodes-ish keys: 2-op FM with decaying index, tremolo, slow tape wobble ----
wob = 1 + 0.0022 * np.sin(2 * np.pi * 0.55 * np.arange(N) / SR) + 0.0012 * np.sin(2 * np.pi * 0.13 * np.arange(N) / SR)
def rhodes(m, d, vel=1.0):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    idx = 1.6 * np.exp(-t * 6) + 0.25
    ph = 2 * np.pi * f * t
    x = np.sin(ph + idx * np.sin(ph)) + 0.15 * np.sin(2 * ph) * np.exp(-t * 3)
    e = np.minimum(1, t / 0.006) * np.exp(-t * 0.38) * np.minimum(1, (d - t) / 0.08)
    return x * e * vel
bars = int(np.ceil(DUR / BAR))
for b in range(bars):
    t0 = b * BAR
    if t0 > END + 0.5: break
    c = CH[b % 4]
    last = t0 + BAR > END
    d = (DUR - t0 - 0.05) if last else BAR * 1.06
    # chord on 1 (slightly strummed), and a softer re-hit on the "and" of 2
    for k, m in enumerate(c):
        x = rhodes(m, d, .22)
        add(KEYS[:, 0], x, t0 + k * 0.012, 1.0 - k * 0.12); add(KEYS[:, 1], x, t0 + k * 0.012, 0.7 + k * 0.12)
        if not last:
            y = rhodes(m + 12 if k == 3 else m, BEAT * 1.4, .1)
            add(KEYS[:, 0], y, t0 + 1.5 * BEAT + 0.02 * k, .8); add(KEYS[:, 1], y, t0 + 1.5 * BEAT + 0.02 * k, 1.0)
    # soft pad underneath so the bar never empties out
    for k, m in enumerate(c):
        n = int(d * SR); tt = np.arange(n) / SR
        tri = sum((2 / np.pi) * np.arcsin(np.sin(2 * np.pi * hz(m) * (1 + dt) * tt)) for dt in (-0.003, 0.003)) / 2
        pe = np.minimum(1, tt / 0.35) * np.minimum(1, (d - tt) / 0.4)
        add(KEYS[:, k % 2], lp(tri * pe, 900), t0, .05)
    if last: break
# tape wobble: tiny time-varying resample of the keys bus
idx = np.cumsum(wob) - wob[0]; idx = np.clip(idx, 0, N - 1)
for ch in range(2): KEYS[:, ch] = np.interp(idx, np.arange(N), KEYS[:, ch])
KEYS[:, 0] = lp(KEYS[:, 0], 3200); KEYS[:, 1] = lp(KEYS[:, 1], 3200)

# ---- drums (swung) ----
def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR; f = 46 + 85 * np.exp(-t * 28)
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5))
def snare():
    n = int(0.32 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 28)
    noise = bp(rng.standard_normal(n), 1200, 5200) * np.exp(-t * 16)
    return lp(0.5 * body + 0.8 * noise, 4200)
def hat(open_=False):
    n = int((0.16 if open_ else 0.05) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (18 if open_ else 75))
K, S = kick(), snare()
SW = 0.6  # swing: the off-16th lands 60% of the way through the 8th
def grid(b, step):  # step in 16ths within a bar (0..15)
    pair, off = divmod(step, 2)
    return b * BAR + pair * BEAT / 2 + (off * SW * BEAT / 2)
DROPS = [float(x) for x in arg('--drops', '').split(',') if x]
def dropped(t): return any(T - BEAT <= t < T for T in DROPS) or t >= END + 0.6
for b in range(bars):
    for st in [0, 7, 10]:                    # kick: 1, a-of-2, and-of-3
        t = grid(b, st)
        if not dropped(t): add(DRUMS, K, t, .9 if st == 0 else .7)
    for st in [4, 12]:                       # snare on 2 and 4
        t = grid(b, st)
        if not dropped(t): add(DRUMS, S, t + 0.012, .55)
    for st in range(0, 16, 2):               # 8th hats, swung ghosts
        t = grid(b, st)
        if not dropped(t): add(DRUMS, hat(st == 14), t, .16 if st % 4 == 0 else .11)
        t2 = grid(b, st + 1)
        if not dropped(t2) and st in (2, 10): add(DRUMS, hat(), t2, .06)
DRUMS = lp(DRUMS, 6500)

# ---- sub bass ----
def sub(m, d):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * hz(m) * t); x = np.tanh(1.4 * x)
    return x * np.minimum(1, t / 0.01) * np.exp(-t * 1.1) * np.minimum(1, (d - t) / 0.05)
for b in range(bars):
    t0 = b * BAR
    if t0 > END: break
    r = RT[b % 4]
    if t0 + BAR > END:
        add(BASS, sub(r, DUR - t0 - .1), t0, .5); break
    add(BASS, sub(r, BEAT * 1.6), t0, .55)
    add(BASS, sub(r + 7 if b % 2 else r + 12, BEAT * .9), grid(b, 7), .4)
    add(BASS, sub(r, BEAT * 1.2), grid(b, 10), .45)
BASS = lp(BASS, 220)

# ---- hook filter: drums + keys muffled until the first collage scene (OPEN) ----
def sweep(x, t_open, f_lo=700):
    y = lp(x, f_lo, 2); a = np.clip((np.arange(len(x)) / SR - (t_open - 0.3)) / 0.6, 0, 1)
    return y * (1 - a) + x * a
DRUMS = sweep(DRUMS, OPEN)
for ch in range(2): KEYS[:, ch] = sweep(KEYS[:, ch], OPEN, 1100)

# ---- vinyl crackle + hiss ----
crack = np.zeros(N); pos = rng.integers(0, N, int(DUR * 9))
for p_ in pos:
    n = rng.integers(20, 90); add(crack, rng.standard_normal(n) * np.exp(-np.arange(n) / 12) * rng.uniform(.05, .3), p_ / SR)
crack = hp(crack, 900) + lp(hp(rng.standard_normal(N), 2000), 7000) * 0.008

mix = np.zeros((N, 2))
mix += KEYS * 0.95
mix[:, 0] += DRUMS * .9 + BASS * .8 + crack * .55
mix[:, 1] += DRUMS * .9 + BASS * .8 + crack * .55
# gentle glue: soft clip, then normalise
mix = np.tanh(mix * 1.3) / 1.3
fo = int(0.9 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
mix /= np.abs(mix).max() / 0.85
wf.write(OUT, SR, (mix * 32767).astype(np.int16)); print(OUT, DUR, 's')

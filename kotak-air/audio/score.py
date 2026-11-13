# Original score for "Kotak Air Credit Card — Key Features". Pure synthesis (numpy/scipy), no samples.
# 104 BPM (beat 0.577 s, bar 2.308 s), E major: E – B – C#m – A. Warm, premium, light.
# 0–2.55 soft pad + bell intro with a riser · 2.55 groove in (card moves to the feature slot) ·
# 28.5 lift for the fees beat (extra octave bells) · 34.3 final chord on the end card, ring-out to 39.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 39.0; N = int(SR * DUR); BEAT = 60 / 104; BAR = 4 * BEAT
DROP = 2.55; END = 34.3; LIFT = 28.5; T0 = DROP - 2 * BAR
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(round(t * SR)); x = x[max(0, -i):]; i = max(0, i); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan))); add(R, x, t, g * (1 + min(0, pan)))
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); A = max(1, int(a * SR)); Rr = max(1, int(r * SR)); e[:A] = np.linspace(0, 1, A); e[-Rr:] *= np.linspace(1, 0, Rr); return e
def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1
def tri(f, d):
    t = np.arange(int(d * SR)) / SR; return 2 * np.abs(2 * ((t * f) % 1) - 1) - 1

CH = [[64, 68, 71, 76], [59, 63, 66, 71], [61, 64, 68, 73], [57, 61, 64, 69]]   # E B C#m A
ROOT = [40, 47, 49, 45]
def ci(t): return int(round((t - T0) / BAR - 0.49)) % 4
def bars(a, b): return [T0 + k * BAR for k in range(-2, 40) if a - 1e-6 <= T0 + k * BAR < b - 1e-6]
def beats(a, b, step=BEAT):
    k0 = int(np.ceil((a - T0) / step - 1e-6)); out = []
    while T0 + k0 * step < b - 1e-6: out.append(T0 + k0 * step); k0 += 1
    return out

def kick():
    n = int(0.34 * SR); t = np.arange(n) / SR; f = 50 + 95 * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def clap():
    n = int(0.22 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 24) + 0.6 * np.exp(-((t - 0.01) % 0.012) * 380) * (t < 0.035)
    return bp(x * e, 1200, 6500)
def shaker():
    n = int(0.06 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 7000) * np.exp(-t * 70) * np.minimum(1, t * 300)
def swell(d):
    n = int(d * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 3000) * (t / d) ** 2.5
def cym():
    n = int(2.0 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 5000) * np.exp(-t * 2.2)
K, C, SH, CY = kick(), clap(), shaker(), cym()

kicks = []
def groove(t0, t1, kick_g=0.7, clap_g=0.26, sh=0.08, half=False):
    for b in beats(t0, t1):
        n = int(round((b - T0) / BEAT))
        if not half or n % 2 == 0: st(K, b, kick_g); kicks.append(b)
        if n % 2 == 1: st(C, b, clap_g, 0.04)
        for k in range(4): st(SH, b + k * BEAT / 4, sh * (1.0 if k % 2 else 0.5), 0.3 if k % 2 else -0.3)
groove(DROP, LIFT, 0.68, 0.24, 0.075)
groove(LIFT, END, 0.74, 0.28, 0.09)
for t in [DROP, LIFT, END]: st(CY, t, 0.12)
st(swell(2.3), DROP - 2.3, 0.14)      # riser into the groove
st(swell(1.6), END - 1.6, 0.10)       # lift into the end card

side = np.ones(N)
for b in kicks:
    i = int(b * SR); n = int(0.28 * SR); seg = 1 - 0.45 * np.exp(-np.arange(n) / SR * 12); side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

# warm sub bass (root + fifth movement)
bass = np.zeros(N)
for t in bars(DROP, END):
    r = ROOT[ci(t + 0.01)]
    for off, o, d in [(0, 0, 0.9), (1.5, 0, 0.35), (2, 7, 0.5), (3, 0, 0.45), (3.5, 12, 0.25)]:
        n = int(d * SR); tt = np.arange(n) / SR
        add(bass, np.tanh(1.3 * np.sin(2 * np.pi * hz(r + o) * tt)) * env(n, 0.006, 0.12), t + off * BEAT)
n = int(4.2 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(np.sin(2 * np.pi * hz(40) * tt)) * env(n, 0.006, 3.0), END)
st(lp(bass, 380) * side, 0, 0.38)

# electric-piano style chords (soft, on 1 and the "and" of 2)
def ep(notes, d):
    n = int(d * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for m in notes:
        f = hz(m); x += (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 6)) * np.exp(-tt * 2.2)
    return x / len(notes) * env(n, 0.004, 0.25)
for t in bars(T0 - BAR, END):
    notes = CH[ci(t + 0.01)]
    for off, d, g in [(0, 1.4, 0.30), (1.5, 0.9, 0.18), (2.5, 0.9, 0.16)]:
        tt0 = t + off * BEAT
        if 0 <= tt0 < END: st(ep(notes, d), tt0, g * (0.6 if tt0 < DROP else 1.0) * side[min(N - 1, int(tt0 * SR))], -0.1)

# airy pad under everything
pad = np.zeros(N)
for t in bars(T0 - BAR, END):
    x = sum(saw(hz(m), BAR + 0.08, det) for m in CH[ci(t + 0.01)] for det in (-0.004, 0.004)) / 8
    add(pad, lp(x, 1500) * env(len(x), 0.25, 0.35), t)
tt = np.arange(N) / SR
pad *= np.where(tt < DROP, 1.5, 1.0)
st(pad * side, 0, 0.09)

# bell motif (glassy, travel-sparkle)
def bell(m, d=0.6):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt * 12)) * np.exp(-tt * 6)
MOT = [(0, 83), (0.75, 80), (1.5, 76), (2.5, 78), (3, 80)]
for t in bars(T0, END):
    shift = [0, -5, -3, -7][ci(t + 0.01)]
    g = 0.07 if t < DROP else 0.10
    for off, m in MOT: st(bell(m + shift), t + off * BEAT, g, 0.3 if off % 1 else -0.3)
    if t >= LIFT - 1e-6:
        for off, m in MOT: st(bell(m + shift + 12, 0.4), t + off * BEAT + 0.003, 0.05, -0.15)

# end card: final chord + bell arpeggio
x = sum(saw(hz(m), 4.6, det) for m in [52, 64, 68, 71, 76, 80] for det in (-0.005, 0, 0.005)) / 18
st(lp(x, 2600) * env(len(x), 0.02, 3.6), END, 0.24)
st(ep([64, 68, 71, 76], 4.4), END, 0.32)
for k, m in enumerate([76, 80, 83, 88]): st(bell(m, 1.4), END + 0.15 + k * 0.11, 0.10)

out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(37.6 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]; out = np.tanh(out * 1.05) / np.tanh(1.05); out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav')

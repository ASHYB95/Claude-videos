# Original score for "Collection Pot — Set Up in Under a Minute". Pure synthesis (numpy/scipy), no samples.
# 120 BPM (beat 0.5 s, bar 2 s), C major: C – G – Am – F. Upbeat, bright, friendly.
# 0–4.45 hook groove (filtered), 4.45 lift, 7.25 full groove + marimba motif, 24.0 celebration chorus,
# 29.6 final hit on CREATE A POT, ring out to 32.2.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 32.6; N = int(SR * DUR); BEAT = 0.5
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i and i >= 0: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan))); add(R, x, t, g * (1 + min(0, pan)))
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); A = max(1, int(a * SR)); Rr = max(1, int(r * SR)); e[:A] = np.linspace(0, 1, A); e[-Rr:] *= np.linspace(1, 0, Rr); return e
def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1

CH = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]   # C G Am F
ROOT = [36, 43, 45, 41]
def ci(t): return int(t // 2) % 4

# drums
def kick():
    n = int(0.38 * SR); t = np.arange(n) / SR; f = 48 + 120 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) + 0.2 * np.exp(-t * 400) * rng.standard_normal(n)
def clap():
    n = int(0.25 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 20) + 0.7 * np.exp(-((t - 0.01) % 0.012) * 380) * (t < 0.04)
    return bp(x * e, 1000, 6000)
def shaker():
    n = int(0.07 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 6000) * np.exp(-t * 60) * np.minimum(1, t * 300)
def crash():
    n = int(2.2 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 4000) * np.exp(-t * 1.8)
K, C, SH, CR = kick(), clap(), shaker(), crash()

def groove(t0, t1, kick_g=0.9, clap_g=0.38, sh=0.12, four=True):
    b = t0
    while b < t1 - 1e-6:
        beat = int(round(b / BEAT))
        if four or beat % 2 == 0: st(K, b, kick_g)
        if beat % 2 == 1: st(C, b, clap_g, 0.05)
        for k in range(4): st(SH, b + k * BEAT / 4, sh * (1.0 if k % 2 else 0.55), 0.3 if k % 2 else -0.3)
        b += BEAT
groove(0.0, 4.45, kick_g=0.7, clap_g=0.3, sh=0.08, four=False)
groove(4.5, 7.25, kick_g=0.75, clap_g=0.32, sh=0.1, four=False)
groove(7.25, 23.9, kick_g=0.9, clap_g=0.38, sh=0.12)
groove(24.0, 29.5, kick_g=0.95, clap_g=0.45, sh=0.14)
for t in [7.25, 24.0, 29.6]: st(CR, t, 0.22)
for k in range(8): st(C, 7.25 - 0.5 + k * 0.0625, 0.12 + k * 0.03)        # snare-roll into the drop
for k in range(8): st(C, 24.0 - 0.5 + k * 0.0625, 0.12 + k * 0.035)
# sidechain
side = np.ones(N)
kicks = list(np.arange(0, 4.45, 1.0)) + list(np.arange(4.5, 7.25, 1.0)) + list(np.arange(7.25, 23.9, 0.5)) + list(np.arange(24.0, 29.5, 0.5))
for b in kicks:
    i = int(b * SR); n = int(0.3 * SR); seg = 1 - 0.55 * np.exp(-np.arange(n) / SR * 12); side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

# bass: bouncy octave pattern
bass = np.zeros(N); t = 4.5
while t < 29.5:
    r = ROOT[ci(t)]
    for off, o in [(0, 0), (0.5, 12), (0.75, 0), (1.0, 0), (1.5, 12), (1.75, 0)]:
        n = int(0.22 * SR); tt = np.arange(n) / SR; f = hz(r + o)
        add(bass, np.tanh(1.5 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))) * env(n, 0.004, 0.08), t + off)
    t += 2.0
n = int(2.4 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(np.sin(2 * np.pi * hz(36) * tt)) * env(n, 0.005, 1.5), 29.6)
st(lp(bass, 400) * side, 0, 0.42)

# chord stabs (off-beat, plucky)
def stab(notes, d=0.18, bright=3800):
    x = sum(saw(hz(m), d, det) for m in notes for det in (-0.005, 0.005)) / (2 * len(notes))
    n = len(x); return lp(x, bright) * np.exp(-np.arange(n) / SR * 16)
t = 0.0
while t < 29.5:
    bright = 1500 if t < 4.45 else (2600 if t < 7.25 else 4200)
    g = 0.22 if t < 7.25 else 0.26
    for off in (0.25, 0.75, 1.25, 1.75): st(stab(CH[ci(t)], bright=bright), t + off, g * side[min(N - 1, int((t + off) * SR))], 0.15)
    t += 2.0
# pad under everything (soft)
pad = np.zeros(N)
for bar in range(17):
    t0 = bar * 2.0; x = sum(saw(hz(m), 2.05, det) for m in CH[bar % 4] for det in (-0.004, 0.004)) / 8
    add(pad, lp(x, 1800) * env(len(x), 0.2, 0.3), t0)
pad *= np.where(np.arange(N) / SR > 29.6, 0, 1)
st(pad * side, 0, 0.12)

# marimba motif (from the drop)
def marimba(m, d=0.35):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 40)) * np.exp(-tt * 9)
MOT = [(0, 76), (0.5, 79), (0.75, 76), (1.0, 72), (1.5, 74), (1.75, 76)]
t = 7.25
while t < 29.5:
    if not (15.5 <= t < 17.75):
        shift = [0, -5, -3, -7][ci(t)]
        for off, m in MOT: st(marimba(m + shift), t + off, 0.16, 0.25 if off % 1 else -0.25)
        if t >= 24.0:
            for off, m in MOT: st(marimba(m + shift + 12, 0.25), t + off + 0.002, 0.07, -0.1)
    t += 2.0
# end: final chord on CREATE A POT
x = sum(saw(hz(m), 2.6, det) for m in [48, 60, 64, 67, 72, 76] for det in (-0.005, 0, 0.005)) / 18
st(lp(x, 3200) * env(len(x), 0.01, 2.0), 29.6, 0.34)
for k, m in enumerate([72, 76, 79, 84]): st(marimba(m, 0.8), 29.6 + k * 0.08, 0.15)

out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(31.4 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]; out = np.tanh(out * 1.1) / np.tanh(1.1); out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav')

# Original score for "Collection Pot — Gift Card on Send". Pure synthesis (numpy/scipy), no samples.
# 120 BPM, C major (C – G – Am – F). Bars are offset so the drop lands on the Pot wipe at 3.5 s.
# 0–3.5 polite, filtered intro + a deflating slide on "worst gift" · 3.5 drop into the groove ·
# 16.0 accent as the gift cards land on Costa · 20.0 celebration chorus on the end card · 22.5 final hit on CREATE A POT.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 24.8; N = int(SR * DUR); BEAT = 0.5; OFF = 1.5   # bar k starts at OFF + 2k
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(14)
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
CH = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]
ROOT = [36, 43, 45, 41]
def ci(t): return int((t - OFF) // 2) % 4

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
        beat = int(round((b - OFF) / BEAT))
        if four or beat % 2 == 0: st(K, b, kick_g)
        if beat % 2 == 1: st(C, b, clap_g, 0.05)
        for k in range(4): st(SH, b + k * BEAT / 4, sh * (1.0 if k % 2 else 0.55), 0.3 if k % 2 else -0.3)
        b += BEAT
# intro: shaker only, polite
b = 0.0
while b < 3.0:
    for k in range(4): st(SH, b + k * BEAT / 4, 0.06 * (1.0 if k % 2 else 0.5), 0.3 if k % 2 else -0.3)
    b += BEAT
groove(3.5, 19.25, kick_g=0.9, clap_g=0.38, sh=0.12)
groove(20.0, 22.5, kick_g=0.95, clap_g=0.45, sh=0.14)
for t in [3.5, 16.0, 20.0, 22.5]: st(CR, t, 0.2)
for k in range(8): st(C, 3.0 + k * 0.0625, 0.1 + k * 0.03)           # snare roll into the drop
for k in range(8): st(C, 19.5 + k * 0.0625, 0.1 + k * 0.035)
side = np.ones(N)
kicks = list(np.arange(3.5, 19.25, 0.5)) + list(np.arange(20.0, 22.5, 0.5))
for b in kicks:
    i = int(b * SR); n = int(0.3 * SR); seg = 1 - 0.55 * np.exp(-np.arange(n) / SR * 12); side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

# deflating slide on "worst gift" (comic, gentle)
n = int(0.75 * SR); tt = np.arange(n) / SR; f = 330 * np.exp(-tt * 1.6)
womp = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * env(n, 0.02, 0.3)
st(lp(womp, 1800), 2.12, 0.16)

# bass
bass = np.zeros(N)
brk = lambda x: 19.25 <= x < 20.0 or x >= 22.5
for t in np.arange(3.5, 22.5, 2.0):
    r = ROOT[ci(t)]
    for off, o in [(0, 0), (0.5, 12), (0.75, 0), (1.0, 0), (1.5, 12), (1.75, 0)]:
        if brk(t + off): continue
        n = int(0.22 * SR); tt = np.arange(n) / SR; f = hz(r + o)
        add(bass, np.tanh(1.5 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))) * env(n, 0.004, 0.08), t + off)
n = int(2.0 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(np.sin(2 * np.pi * hz(36) * tt)) * env(n, 0.005, 1.4), 22.5)
st(lp(bass, 400) * side, 0, 0.42)

def stab(notes, d=0.18, bright=3800):
    x = sum(saw(hz(m), d, det) for m in notes for det in (-0.005, 0.005)) / (2 * len(notes))
    n = len(x); return lp(x, bright) * np.exp(-np.arange(n) / SR * 16)
t = -0.5
while t < 22.5:
    bright = 1300 if t < 3.5 else 4200
    g = 0.18 if t < 3.5 else 0.25
    for off in (0.25, 0.75, 1.25, 1.75):
        tt0 = t + off
        if tt0 < 0 or tt0 >= 22.5 or (2.1 <= tt0 < 3.5) or (19.25 <= tt0 < 20.0): continue          # stabs drop out under the grimace
        st(stab(CH[ci(tt0)], bright=bright), tt0, g * side[min(N - 1, int(tt0 * SR))], 0.15)
    t += 2.0
pad = np.zeros(N)
for bar in range(-1, 11):
    t0 = OFF + bar * 2.0
    if t0 >= 22.5: break
    x = sum(saw(hz(m), 2.05, det) for m in CH[bar % 4] for det in (-0.004, 0.004)) / 8
    add(pad, lp(x, 1600) * env(len(x), 0.2, 0.3), max(0, t0))
pad *= np.where(np.arange(N) / SR > 22.5, 0, 1)
st(pad * side, 0, 0.11)

def marimba(m, d=0.35):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 40)) * np.exp(-tt * 9)
MOT = [(0, 76), (0.5, 79), (0.75, 76), (1.0, 72), (1.5, 74), (1.75, 76)]
t = 3.5
while t < 22.5:
    if not (13.5 <= t < 15.5 or 17.5 <= t < 20.0):
        shift = [0, -5, -3, -7][ci(t)]
        for off, m in MOT: st(marimba(m + shift), t + off, 0.15, 0.25 if off % 1 else -0.25)
        if t >= 20.0:
            for off, m in MOT: st(marimba(m + shift + 12, 0.25), t + off + 0.002, 0.07, -0.1)
    t += 2.0
x = sum(saw(hz(m), 2.2, det) for m in [48, 60, 64, 67, 72, 76] for det in (-0.005, 0, 0.005)) / 18
st(lp(x, 3200) * env(len(x), 0.01, 1.8), 22.5, 0.32)
for k, m in enumerate([72, 76, 79, 84]): st(marimba(m, 0.8), 22.5 + k * 0.08, 0.15)

out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(23.8 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]; out = np.tanh(out * 1.1) / np.tanh(1.1); out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav')

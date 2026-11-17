# Original score for "Delulu Keyboard — Say It Right". Pure synthesis (numpy/scipy), no samples.
# 120 BPM (beat 0.5 s, bar 2 s). Fmaj9 – Am9 – Cmaj9 – G6 add9.
# 0–4 s intro (pad + filtered arp), 4.0 drop, 26.4 breakdown into the end card, final hit at 29.2.
import numpy as np, os
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 33.5; N = int(SR * DUR); BEAT = 0.5
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan))); add(R, x, t, g * (1 + min(0, pan)))
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR; ph = (t * f * (1 + det)) % 1; return 2 * ph - 1
def env(n, a, r, sus=1.0):
    e = np.ones(n) * sus; A = max(1, int(a * SR)); Rr = max(1, int(r * SR))
    e[:A] = np.linspace(0, sus, A); e[-Rr:] *= np.linspace(1, 0, Rr); return e

CH = [[53, 57, 60, 64, 67], [57, 60, 64, 67, 71], [48, 55, 59, 62, 64], [55, 59, 62, 64, 69]]  # Fmaj9 Am9 Cmaj9 G6/9
ROOT = [41, 45, 36, 43]
def chord_at(t): return int(t // 2) % 4

# ---------- drums ----------
def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 32); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.25 * np.exp(-t * 300) * rng.standard_normal(n) * 0.3
def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 18) + 0.6 * np.exp(-((t - 0.012) % 0.011) * 400) * (t < 0.035)
    return bp(x * e, 900, 5000) * 0.9
def hat(o=False):
    n = int((0.16 if o else 0.045) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (22 if o else 90))
K, C, H, HO = kick(), clap(), hat(), hat(True)

def groove(t0, t1, kick_on=True, full=True):
    b = t0
    while b < t1 - 1e-6:
        beat = int(round(b / BEAT))
        if kick_on: st(K, b, 0.95)
        if full and beat % 2 == 1: st(C, b, 0.42, pan=0.05)
        st(H, b + BEAT / 2, 0.16 if full else 0.10, pan=0.25)
        if full: st(H, b + BEAT / 4, 0.05, pan=-0.25); st(H, b + 3 * BEAT / 4, 0.05, pan=-0.25)
        if full and beat % 8 == 7: st(HO, b + BEAT / 2, 0.12, pan=0.3)
        b += BEAT

groove(4.0, 26.0)
groove(29.2, 31.2)
# fills: snare rolls into section seams
for seam in [10.5, 16.0, 21.5]:
    for k in range(4): st(C, seam - 0.5 + k * 0.125, 0.18 + k * 0.05)

# sidechain envelope from kick positions
side = np.ones(N)
for b in list(np.arange(4.0, 26.0, BEAT)) + list(np.arange(29.2, 31.2, BEAT)):
    i = int(b * SR); n = int(0.32 * SR); seg = 1 - 0.7 * np.exp(-np.arange(n) / SR * 11)
    side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

# ---------- pad ----------
pad = np.zeros(N)
for bar in range(0, 17):
    t0 = bar * 2.0
    if t0 >= DUR: break
    notes = CH[bar % 4]; d = 2.05
    x = sum(saw(hz(m), d, det) for m in notes for det in (-0.004, 0.0, 0.0045)) / 15
    x = lp(x, 1400 if t0 < 4 else 2400) * env(len(x), 0.25, 0.3)
    add(pad, x, t0)
pad *= np.where(np.arange(N) / SR < 4, np.linspace(0.3, 1, N), 1)
padS = pad * np.where((np.arange(N) / SR > 4) & (np.arange(N) / SR < 26), side, 1)
st(padS, 0, 0.42)

# ---------- sub bass ----------
bass = np.zeros(N)
t = 4.0
while t < 26.0:
    r = ROOT[chord_at(t)]
    for k, off in enumerate([0, 0.75, 1.0, 1.5]):
        d = 0.45 if k != 1 else 0.22
        n = int(d * SR); tt = np.arange(n) / SR; f = hz(r)
        x = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt)
        add(bass, np.tanh(1.6 * x) * env(n, 0.005, 0.06), t + off)
    t += 2.0
for t0 in [29.2, 30.2]:
    n = int(1.0 * SR); tt = np.arange(n) / SR
    add(bass, np.tanh(1.4 * np.sin(2 * np.pi * hz(ROOT[0]) * tt)) * env(n, 0.005, 0.4), t0)
st(lp(bass, 220) * side, 0, 0.5)

# ---------- pluck arp ----------
def pluck(m, d=0.22, bright=3500):
    n = int(d * SR); tt = np.arange(n) / SR
    x = (saw(hz(m), d) + saw(hz(m), d, 0.006)) * 0.5
    return lp(x, bright) * np.exp(-tt * 14)
t = 0.0; step = BEAT / 2; k = 0
while t < 26.4:
    notes = CH[chord_at(t)]; pat = [0, 2, 4, 3, 1, 4, 2, 3]
    m = notes[pat[k % 8]] + 12
    bright = 1600 if t < 4 else 4200
    g = 0.11 if t < 4 else 0.13
    st(pluck(m, bright=bright), t, g, pan=0.35 if k % 2 else -0.35)
    st(pluck(m, bright=bright), t + 0.375, g * 0.3, pan=-0.35 if k % 2 else 0.35)  # dotted-8th echo
    t += step; k += 1

# chord stabs on tone words (16.1–18.6) and on the CTA
for tt in [16.1, 16.6, 17.18, 17.81, 18.55]:
    notes = CH[chord_at(tt)]; d = 0.3
    x = sum(saw(hz(m + 12), d, det) for m in notes for det in (-0.006, 0.006)) / 10
    st(lp(x, 5000) * env(len(x), 0.004, 0.2), tt, 0.22)

# ---------- end: lush final chord ----------
x = sum(saw(hz(m + 12), 3.4, det) for m in CH[0] for det in (-0.005, 0, 0.005)) / 15
st(lp(x, 3000) * env(len(x), 0.02, 2.4), 29.2, 0.32)

# ---------- master ----------
out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(31.4 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]
out = np.tanh(out * 1.1) / np.tanh(1.1)
out /= np.max(np.abs(out)) / 0.89
import scipy.io.wavfile as wf
wf.write(os.path.join(here, "music.wav"), SR, (out * 32767).astype(np.int16))
print("music.wav", DUR, "s")

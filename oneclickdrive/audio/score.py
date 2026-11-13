# Original score for "OneClickDrive — One Click Away". Pure synthesis (numpy/scipy), no samples.
# 126.3 BPM (beat 0.475 s, bar 1.9 s), D major: D – A – Bm – G. Grid origin puts bar lines on the
# phone reveal (5.0), the map (20.2), the price chorus (24.0) and the end card (27.8).
# 0–5.0 filtered hook groove · 5.0 drop · 17.0–20.2 stop-time hits under "No commission…" ·
# 20.2 groove back · 24.0 chorus · 27.8 final chord on the end card · 30.3 sting on Get the app.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 32.6; N = int(SR * DUR); BEAT = 0.475; BAR = 4 * BEAT; T0 = 5.0 - 3 * BAR
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)
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

CH = [[62, 66, 69, 74], [57, 61, 64, 69], [59, 62, 66, 71], [55, 59, 62, 67]]   # D A Bm G
ROOT = [38, 45, 47, 43]
def ci(t): return int(round((t - T0) / BAR - 0.49)) % 4
def beats(a, b, step=BEAT):
    k0 = int(np.ceil((a - T0) / step - 1e-6)); out = []
    while T0 + k0 * step < b - 1e-6: out.append(T0 + k0 * step); k0 += 1
    return out

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
def boom():
    n = int(1.2 * SR); t = np.arange(n) / SR; f = 40 + 80 * np.exp(-t * 18)
    return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 3.5)
K, C, SH, CR, BM = kick(), clap(), shaker(), crash(), boom()

kicks = []
def groove(t0, t1, kick_g=0.9, clap_g=0.38, sh=0.12, four=True):
    for b in beats(t0, t1):
        n = int(round((b - T0) / BEAT))
        if four or n % 2 == 0: st(K, b, kick_g); kicks.append(b)
        if n % 2 == 1: st(C, b, clap_g, 0.05)
        for k in range(4): st(SH, b + k * BEAT / 4, sh * (1.0 if k % 2 else 0.55), 0.3 if k % 2 else -0.3)
groove(0.0, 5.0, kick_g=0.65, clap_g=0.28, sh=0.07, four=False)
groove(5.0, 17.0, kick_g=0.9, clap_g=0.38, sh=0.12)
groove(20.2, 24.0, kick_g=0.85, clap_g=0.36, sh=0.12)
groove(24.0, 27.8, kick_g=0.95, clap_g=0.45, sh=0.14)
groove(27.8, 31.6, kick_g=0.0, clap_g=0.0, sh=0.06)
for t in [5.0, 20.2, 24.0, 27.8]: st(CR, t, 0.2)
for t0 in [5.0, 24.0]:
    for k in range(8): st(C, t0 - 0.475 + k * 0.059, 0.1 + k * 0.035)      # snare roll into the drop
# stop-time hits under "No commission. No booking fees. No mark-ups."
for t in [17.38, 18.25, 19.2]: st(BM, t, 0.55); st(K, t, 0.8); st(CR, t, 0.1)

side = np.ones(N)
for b in kicks:
    i = int(b * SR); n = int(0.3 * SR); seg = 1 - 0.55 * np.exp(-np.arange(n) / SR * 12); side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

# bass: bouncy octave pattern
bass = np.zeros(N)
for t in [T0 + k * BAR for k in range(40)]:
    if t < 5.0 - 1e-6 or (17.0 <= t < 20.2 - 1e-6) or t >= 27.8 - 1e-6: continue
    r = ROOT[ci(t + 0.01)]
    for off, o in [(0, 0), (1, 12), (1.5, 0), (2, 0), (3, 12), (3.5, 0)]:
        n = int(0.21 * SR); tt = np.arange(n) / SR; f = hz(r + o)
        add(bass, np.tanh(1.5 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))) * env(n, 0.004, 0.08), t + off * BEAT)
for t, r in [(17.38, 38), (18.25, 45), (19.2, 47)]:
    n = int(0.8 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(1.4 * np.sin(2 * np.pi * hz(r) * tt)) * env(n, 0.004, 0.5), t)
n = int(2.6 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(np.sin(2 * np.pi * hz(38) * tt)) * env(n, 0.005, 1.6), 27.8)
st(lp(bass, 420) * side, 0, 0.42)

# chord stabs (off-beat, plucky)
def stab(notes, d=0.17, bright=3800):
    x = sum(saw(hz(m), d, det) for m in notes for det in (-0.005, 0.005)) / (2 * len(notes))
    n = len(x); return lp(x, bright) * np.exp(-np.arange(n) / SR * 16)
for t in [T0 + k * BAR for k in range(40)]:
    if t < -BAR or t >= 27.8 - 1e-6 or (17.0 <= t < 20.2 - 1e-6): continue
    bright = 1400 if t < 5.0 - 1e-6 else 4200
    g = 0.2 if t < 5.0 - 1e-6 else 0.25
    for off in (0.5, 1.5, 2.5, 3.5):
        tt = t + off * BEAT
        if tt >= 0: st(stab(CH[ci(t + 0.01)], bright=bright), tt, g * side[min(N - 1, int(tt * SR))], 0.15)
# pad (soft) — swells through the stop-time section
pad = np.zeros(N)
for k in range(-1, 15):
    t0 = T0 + k * BAR; x = sum(saw(hz(m), BAR + 0.05, det) for m in CH[k % 4] for det in (-0.004, 0.004)) / 8
    add(pad, lp(x, 1800) * env(len(x), 0.2, 0.3), t0)
tt = np.arange(N) / SR
pad *= np.where(tt > 27.8, 0, 1) * np.where((tt > 17.0) & (tt < 20.2), 1.8, 1.0)
st(pad * side, 0, 0.12)

# marimba motif (from the drop)
def marimba(m, d=0.35):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 40)) * np.exp(-tt * 9)
MOT = [(0, 78), (1, 81), (1.5, 78), (2, 74), (3, 76), (3.5, 78)]
for t in [T0 + k * BAR for k in range(40)]:
    if t < 5.0 - 1e-6 or (17.0 <= t < 20.2 - 1e-6) or t >= 27.8 - 1e-6: continue
    shift = [0, -5, -3, -7][ci(t + 0.01)]
    for off, m in MOT: st(marimba(m + shift), t + off * BEAT, 0.15, 0.25 if off % 1 else -0.25)
    if t >= 24.0 - 1e-6:
        for off, m in MOT: st(marimba(m + shift + 12, 0.25), t + off * BEAT + 0.002, 0.07, -0.1)
# end card: final chord + sparkle, sting on the button press
x = sum(saw(hz(m), 3.4, det) for m in [50, 62, 66, 69, 74, 78] for det in (-0.005, 0, 0.005)) / 18
st(lp(x, 3000) * env(len(x), 0.01, 2.6), 27.8, 0.3)
for k, m in enumerate([74, 78, 81, 86]): st(marimba(m, 0.8), 27.8 + k * 0.08, 0.14)
for k, m in enumerate([81, 86]): st(marimba(m, 0.9), 30.3 + k * 0.07, 0.16)
x = sum(saw(hz(m), 2.2, det) for m in [55, 62, 67, 71, 74] for det in (-0.005, 0.005)) / 10
st(lp(x, 2200) * env(len(x), 0.05, 1.6), 30.3, 0.14)

out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(31.5 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]; out = np.tanh(out * 1.1) / np.tanh(1.1); out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav')

# Original score for "The Prince Who Walked Away". Pure synthesis (numpy/scipy), no samples.
# Gentle piano + a tanpura-like drone on D/A, ~70 BPM; bar length set so a bar lands exactly on the sunrise turn (51.2 s).
# Shadow (B minor / E minor) through the sights, the night and the fasting; hope enters with Sujata; suspended under the vow;
# D major with strings and melody at sunrise; resolves on the Buddha.
import numpy as np, os
from scipy.signal import butter, sosfilt, fftconvolve
import scipy.io.wavfile as wf
SR = 44100; DUR = 66.0; N = int(SR * DUR)
TURN = 51.2; BAR = TURN / 15; BEAT = BAR / 4
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(29)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i and i >= 0: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan))); add(R, x, t, g * (1 + min(0, pan)))

C = {'D': [50, 57, 62, 66, 69], 'Bm': [47, 54, 59, 62, 66], 'G': [43, 50, 55, 59, 62], 'A': [45, 52, 57, 61, 64], 'Asus': [45, 52, 57, 62, 64],
     'Em': [40, 47, 52, 55, 59], 'D/F#': [42, 50, 57, 62, 66]}
#        0    1     2    3    4     5     6     7     8    9     10    11   12      13    14      15   16   17   18   19
PROG = ['D', 'Bm', 'G', 'A', 'Bm', 'Em', 'Bm', 'Bm', 'G', 'Em', 'Bm', 'G', 'D/F#', 'Em', 'Asus', 'D', 'G', 'D', 'D', 'D']
SPARSE = {6: 2, 9: 2, 10: 2, 14: 2, 7: 1, 8: 1}   # bar -> keep every Nth 8th (thin under Channa, the fasting and the vow)

def piano(m, d=2.2, vel=1.0):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m); x = np.zeros(n)
    for k, (amp, dec) in enumerate([(1, 2.2), (.45, 3.2), (.22, 4.5), (.12, 6), (.06, 8)]):
        fk = f * (k + 1) * (1 + 0.0004 * (k + 1) ** 2)
        x += amp * np.sin(2 * np.pi * fk * t) * np.exp(-t * dec * (0.6 + f / 900))
    x += 0.04 * rng.standard_normal(n) * np.exp(-t * 90)
    a = int(0.004 * SR); x[:a] *= np.linspace(0, 1, a)
    return lp(x, 2500 + 2500 * vel) * vel
def strings(notes, d, bright=2200):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in notes:
        for det in (-0.004, 0.0, 0.0045):
            vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * t + rng.uniform(0, 6))
            ph = np.cumsum(hz(m) * (1 + det) * vib) / SR
            x += 2 * (ph % 1) - 1
    x = lp(x / (3 * len(notes)), bright)
    e = np.minimum(1, t / 0.9) * np.minimum(1, (d - t) / 0.9); return x * e
def tanpura(m, d=4.5):
    # plucked string with a buzzing bridge: many harmonics whose brightness swells and decays slowly
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m); x = np.zeros(n)
    for k in range(1, 16):
        swell = np.exp(-((t - 0.25 * (1 + k / 8)) ** 2) / (0.5 + k * .04))
        x += (1 / k ** .8) * np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6)) * (0.35 + 0.65 * swell)
    x *= np.exp(-t * 0.55); a = int(0.01 * SR); x[:a] *= np.linspace(0, 1, a)
    return lp(x, 2600) / 6

# --- tanpura drone: Pa Sa Sa Sa(low), four plucks a bar, the whole film ---
TAN = [45, 50, 50, 38]
for b in range(19):
    for k, m in enumerate(TAN):
        g = 0.09 if b in SPARSE else 0.07
        if b >= 15: g = 0.06
        st(tanpura(m), b * BAR + k * BEAT, g, -0.3 if k % 2 else 0.3)

# --- piano arpeggios ---
ARP = [0, 2, 3, 4, 3, 2, 1, 2]
for b, ch in enumerate(PROG):
    t0 = b * BAR
    if t0 >= 63.5: break
    nt = C[ch]; steps = int(BAR / (BEAT / 2)); every = SPARSE.get(b, 1)
    if b >= 18:  # final chord rings out instead of arpeggios
        for k, m in enumerate(nt): st(piano(m + (12 if k >= 3 else 0), 5.5, .7), t0 + k * .06, .14, .1 * (k - 2))
        st(piano(nt[0] - 12, 6, .8), t0, .2); break
    for k in range(steps):
        if k % every: continue
        tt = t0 + k * BEAT / 2; idx = ARP[k % 8]; m = nt[idx] + (12 if idx >= 3 else 0)
        vel = 0.5 + 0.15 * (k % 4 == 0) + (0.12 if b >= 15 else 0)
        st(piano(m, 2.6, vel), tt, 0.16, 0.25 if k % 2 else -0.25)
    st(piano(nt[0] - 12, 3.5, 0.8), t0, 0.2)
# melody: a small hopeful phrase with Sujata, the full rising motif at sunrise
MEL = {11: [74, 76], 12: [78, 74], 15: [74, 76, 78], 16: [79, 78, 74], 17: [76, 78, 81]}
for b, ms in MEL.items():
    for k, m in enumerate(ms):
        st(piano(m, 3.2, 0.85), b * BAR + k * BAR / len(ms) + 0.02, 0.15 if b >= 15 else 0.11, 0.1)

# --- strings: enter softly with Sujata, dip under the vow, swell at sunrise ---
SGAIN = {11: .3, 12: .42, 13: .55, 14: .35, 15: .9, 16: .85, 17: .75, 18: .55}
for b, g in SGAIN.items():
    t0 = b * BAR; ch = C[PROG[b]]
    st(strings([m + 12 for m in ch[1:4]], BAR + 1.0, 1800 + 1200 * g), t0 - 0.3, (0.24 if b >= 15 else 0.16) * g, -0.15)
    st(strings([ch[0]], BAR + 1.0, 900), t0 - 0.3, 0.12 * g, 0.15)
st(strings([62, 66, 69, 74], 5.5, 2600), 18 * BAR, 0.12)

# --- reverb (synthetic hall) ---
ir_n = int(2.8 * SR); t = np.arange(ir_n) / SR
irL = lp(rng.standard_normal(ir_n) * np.exp(-t * 2.3), 5000); irR = lp(rng.standard_normal(ir_n) * np.exp(-t * 2.3), 5000)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
out = np.stack([L * 0.8 + fftconvolve(L, irL)[:N] * 0.45, R * 0.8 + fftconvolve(R, irR)[:N] * 0.45], 1)
fade = np.ones(N); fs = int(63.4 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2; out *= fade[:, None]
out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16)); print('music.wav', round(BAR, 3))

# Original score for "Thirty-One Years". Pure synthesis (numpy/scipy), no samples.
# Gentle piano + strings in D major, ~71 BPM; bar length set so a bar lands exactly on the Collection Pot turn (23.7 s).
import numpy as np, os
from scipy.signal import butter, sosfilt, fftconvolve
import scipy.io.wavfile as wf
SR = 44100; DUR = 62.5; N = int(SR * DUR)
BAR = 23.7 / 7; BEAT = BAR / 4
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(31)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i and i >= 0: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan)) ); add(R, x, t, g * (1 + min(0, pan)))

# chords per bar (MIDI): D major
C = {'D': [50, 57, 62, 66, 69], 'Bm': [47, 54, 59, 62, 66], 'G': [43, 50, 55, 59, 62], 'A': [45, 52, 57, 61, 64], 'Asus': [45, 52, 57, 62, 64],
     'Em': [40, 47, 52, 55, 59], 'D/F#': [42, 50, 57, 62, 66]}
PROG = ['D', 'Bm', 'G', 'A', 'Bm', 'G', 'Em', 'D', 'A', 'Bm', 'G', 'D', 'G', 'D/F#', 'Bm', 'G', 'A', 'D', 'D']

def piano(m, d=2.2, vel=1.0):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    x = np.zeros(n)
    for k, (amp, dec) in enumerate([(1, 2.2), (.45, 3.2), (.22, 4.5), (.12, 6), (.06, 8)]):
        fk = f * (k + 1) * (1 + 0.0004 * (k + 1) ** 2)
        x += amp * np.sin(2 * np.pi * fk * t) * np.exp(-t * dec * (0.6 + f / 900))
    x += 0.04 * rng.standard_normal(n) * np.exp(-t * 90)            # hammer
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

# --- piano: arpeggios throughout ---
ARP = [0, 2, 3, 4, 3, 2, 1, 2]       # chord-tone indices, 8ths
for b, ch in enumerate(PROG):
    t0 = b * BAR
    if t0 >= 61.0: break
    notes = C[ch]
    if b == 6:   # Em then hanging Asus4 — the stuck envelope
        halves = [(C['Em'], 0), (C['Asus'], BAR / 2)]
    else: halves = [(notes, 0)]
    for nt, off in halves:
        span = BAR if len(halves) == 1 else BAR / 2
        steps = int(span / (BEAT / 2))
        for k in range(steps):
            tt = t0 + off + k * BEAT / 2
            sparse = (b >= 12 and b <= 13 and k % 2)          # thin out under the quotes
            if sparse: continue
            idx = ARP[k % 8]; m = nt[idx] + (12 if idx >= 3 else 0)
            vel = 0.55 + 0.15 * (k % 4 == 0) + (0.1 if b >= 7 else 0)
            st(piano(m, 2.6, vel), tt, 0.16, 0.25 if k % 2 else -0.25)
        st(piano(nt[0] - 12, 3.5, 0.8), t0 + off, 0.2)            # bass note
# melody (from the turn): a simple rising motif
MEL = {7: [74, 76, 78], 8: [76, 73], 9: [74, 71], 10: [71, 74], 11: [78, 76, 74], 14: [74, 78], 15: [79, 78, 74], 16: [76, 73, 76], 17: [78]}
for b, ms in MEL.items():
    for k, m in enumerate(ms):
        st(piano(m, 3.0, 0.85), b * BAR + k * BAR / len(ms) + 0.02, 0.15, 0.1)

# --- strings: enter at the turn, swell under messages, dip for the quotes, swell at 'read twice' ---
SGAIN = {7: .35, 8: .45, 9: .55, 10: .65, 11: .7, 12: .3, 13: .3, 14: .7, 15: .85, 16: .8, 17: .7, 18: .4}
for b, g in SGAIN.items():
    t0 = b * BAR; ch = C[PROG[b]]
    s = strings([m + 12 for m in ch[1:4]], BAR + 1.0, 1800 + 1200 * g)
    st(s, t0 - 0.3, 0.16 * g, -0.15)
    st(strings([ch[0]], BAR + 1.0, 900), t0 - 0.3, 0.12 * g, 0.15)  # cello root
# final chord
st(strings([62, 66, 69, 74], 5.0, 2600), 17 * BAR, 0.14)

# --- reverb (synthetic hall) ---
ir_n = int(2.8 * SR); t = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-t * 2.3); irR = rng.standard_normal(ir_n) * np.exp(-t * 2.3)
irL = lp(irL, 5000); irR = lp(irR, 5000); irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
wetL = fftconvolve(L, irL)[:N]; wetR = fftconvolve(R, irR)[:N]
outL = L * 0.8 + wetL * 0.45; outR = R * 0.8 + wetR * 0.45
out = np.stack([outL, outR], 1)
fade = np.ones(N); fs = int(60.2 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2; out *= fade[:, None]
out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16)); print('music.wav', round(BAR, 3))

# Original score for LOOT "Secure the Bag". Pure synthesis (numpy/scipy), no samples.
# Dark trap: 140 BPM (beat 0.4286 s, bar 1.714 s), F minor, Fm – Db – Ab – Eb.
# Bar grid puts a downbeat on the LOOT slam (6.38 s).
# 0–6.38 filtered intro + riser · 6.38 drop · 40.5–45.9 break under the slate rule scene ·
# 45.9 second drop (bag secured) · 52.38–56.8 stop-time hits on "No boss / No schedule / …" ·
# 56.9 final hit on the end card, pad ring-out to 60.5.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 60.5; N = int(SR * DUR)
BPM = 140; BEAT = 60 / BPM; BAR = 4 * BEAT; DROP1 = 6.38; T0 = DROP1 - 4 * BAR
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
    e = np.ones(n); A = min(n, max(1, int(a * SR))); Rr = min(n, max(1, int(r * SR))); e[:A] = np.linspace(0, 1, A); e[n - Rr:] *= np.linspace(1, 0, Rr); return e
def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1
def sq(f, d):
    t = np.arange(int(d * SR)) / SR; return np.sign(np.sin(2 * np.pi * f * t))

CH = [[65, 68, 72], [61, 65, 68], [68, 72, 75], [63, 67, 70]]     # Fm Db Ab Eb (mid voicing)
ROOT = [29, 25, 32, 27]                                            # F1 Db1 Ab1 Eb1 (808)
def bar_of(t): return int(np.floor((t - T0) / BAR + 1e-6))
def ci(t): return bar_of(t) % 4
def grid(a, b, step):
    k0 = int(np.ceil((a - T0) / step - 1e-6)); out = []
    while T0 + k0 * step < b - 1e-6: out.append(T0 + k0 * step); k0 += 1
    return out

def kick():
    n = int(0.3 * SR); t = np.arange(n) / SR; f = 50 + 140 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) + 0.25 * np.exp(-t * 500) * rng.standard_normal(n)
def snare():
    n = int(0.32 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return bp(x, 1500, 8000) * np.exp(-t * 16) * 0.9 + 0.5 * body
def clap():
    n = int(0.25 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 22) + 0.7 * np.exp(-((t - 0.008) % 0.011) * 380) * (t < 0.035)
    return bp(x * e, 1100, 6500)
def hat(d=0.045):
    n = int(d * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 7500) * np.exp(-t * (90 if d < 0.06 else 25))
def b808(m, d, glide_from=None):
    n = int(d * SR); t = np.arange(n) / SR; f = np.full(n, hz(m))
    if glide_from is not None: f = hz(m) + (hz(glide_from) - hz(m)) * np.exp(-t * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR); x = np.tanh(2.2 * x) * 0.8
    return x * env(n, 0.004, min(0.12, d * 0.4)) * np.exp(-t * 0.6)
def boom():
    n = int(1.6 * SR); t = np.arange(n) / SR; f = 34 + 90 * np.exp(-t * 14)
    return np.tanh(2.4 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 2.4)
def crash():
    n = int(2.6 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 5000) * np.exp(-t * 1.6)
def pluck(m, d=0.22):
    x = 0.6 * sq(hz(m), d) + 0.4 * saw(hz(m), d, 0.004); n = len(x); t = np.arange(n) / SR
    bright = lp(x, 3200) * np.exp(-t * 26); body = lp(x, 900) * np.exp(-t * 7)
    return (0.7 * bright + 0.6 * body) * env(n, 0.002, 0.03)
def pad(ch, d):
    x = sum(saw(hz(m - 12), d, dt) for m in ch for dt in (-0.004, 0.004)) / (2 * len(ch))
    return lp(x, 1100) * env(len(x), 0.5, 0.6)
def riser(d):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    y = np.zeros(n); seg = 2048
    for i in range(0, n, seg):
        f = 300 + 7000 * (i / n) ** 2; y[i:i + seg] = bp(x[i:i + seg], f, f * 1.6)
    return y * (t / d) ** 2
K, SN, CL, BM, CR = kick(), snare(), clap(), boom(), crash()

def drums(a, b, full=True, hatroll=True):
    for bt in grid(a, b, BEAT):
        k = int(round((bt - T0) / BEAT)) % 8     # 2-bar trap pattern in beats
        if k in (0, 3) or (k == 5 and full): st(K, bt, 0.95)
        if k in (2, 6): st(SN, bt, 0.55); st(CL, bt + 0.004, 0.35, 0.15)
    for h in grid(a, b, BEAT / 2):
        st(hat(), h, 0.16, -0.25)
    if hatroll:  # 1/16 + 1/32 rolls on the last beat of every 2nd bar
        for bt in grid(a, b, BAR * 2):
            r0 = bt + BAR * 2 - BEAT
            if r0 + BEAT <= b:
                for i in range(6): st(hat(0.03), r0 + i * BEAT / 4 * (1 if i < 4 else 0.5) + (0 if i < 4 else BEAT / 2), 0.12, -0.25)

def bassline(a, b, gain=0.55, lpf=None):
    for bs in grid(a, b, BAR):
        c = ci(bs + 0.01); m = ROOT[c]
        hits = [(0, 0.95), (1.5, 0.45), (2.5, 0.9)] if c % 2 == 0 else [(0, 1.4), (2.0, 0.5), (3.0, 0.9)]
        for off, ln in hits:
            t = bs + off * BEAT
            if a <= t < b:
                x = b808(m + (12 if off == 3.0 else 0), ln * BEAT * 1.9, glide_from=(m + 12 if off == 0 and c == 2 else None))
                if lpf: x = lp(x, lpf)
                st(x, t, gain)

def arp(a, b, gain=0.10, brightness=1.0):
    pat = [0, 1, 2, 1, 0, 2, 1, 2]
    for i, t in enumerate(grid(a, b, BEAT / 2)):
        ch = CH[ci(t + 0.01)]; m = ch[pat[i % 8]] + (12 if i % 16 >= 12 else 0)
        x = pluck(m); x = lp(x, 2500 * brightness) if brightness < 1 else x
        st(x, t, gain, 0.35 if i % 2 else -0.35)

def pads(a, b, gain=0.13):
    for bs in grid(a - BAR, b, BAR):
        s, e = max(a, bs), min(b, bs + BAR)
        if e - s > 0.1: st(pad(CH[ci(bs + 0.01)], e - s + 0.4), s, gain)

# ---- intro 0–6.38: pad + ticking hats + filtered arp, riser into the drop
pads(0, DROP1, 0.10)
arp(0.2, DROP1, 0.06, brightness=0.35)
for h in grid(0.2, DROP1, BEAT / 2): st(hat(), h, 0.07, -0.25)
st(BM, 1.72, 0.35)                       # the tear
st(riser(2.0), DROP1 - 2.0, 0.18)
for t in (3.2, 4.18, 5.12): st(K, t, 0.6); st(lp(CL, 3000), t, 0.25)   # RAW / REAL / YOU
# ---- drop 1: 6.38–40.5
st(BM, DROP1, 0.85); st(CR, DROP1, 0.22)
drums(DROP1, 40.5); bassline(DROP1, 40.5); arp(DROP1, 40.5, 0.075); pads(DROP1, 40.5, 0.07)
for t in (16.95, 30.1, 35.3):            # small lifts on section changes
    st(CR, t, 0.12); st(lp(BM, 200), t, 0.3)
# ---- break 40.5–45.9 (slate): low-passed bass, pad, sparse kick
pads(40.5, 45.9, 0.13); bassline(40.5, 45.9, 0.45, lpf=180)
for t in grid(40.5, 45.9, BAR): st(K, t, 0.6)
arp(40.5, 45.9, 0.05, brightness=0.3)
st(riser(1.6), 45.9 - 1.6, 0.2)
# ---- drop 2: 45.9–52.3
st(BM, 45.92, 0.8); st(CR, 45.92, 0.22)
drums(45.9, 52.3); bassline(45.9, 52.3); arp(45.9, 52.3, 0.085); pads(45.9, 52.3, 0.08)
# ---- stop-time 52.3–56.8: hits on each line, hats keep time
for t in (52.38, 53.22, 54.18, 55.02, 55.78):
    st(K, t, 0.9); st(SN, t, 0.4); st(b808(ROOT[0], 0.5), t, 0.5)
for h in grid(52.3, 56.6, BEAT / 2): st(hat(), h, 0.1, -0.25)
pads(52.3, 56.8, 0.06)
st(riser(1.0), 55.85, 0.16)
# ---- final hit + ring-out
st(BM, 56.92, 0.9); st(CR, 56.92, 0.26)
st(pad(CH[0], 3.6), 56.92, 0.16); st(b808(ROOT[0], 2.6), 56.92, 0.5)
for i, m in enumerate([72, 77, 80, 84]): st(pluck(m, 0.5), 57.55 + i * BEAT / 2, 0.08, (-0.3, 0.3)[i % 2])

mix = np.stack([L, R], 1)
fade = int(1.2 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
mix /= np.abs(mix).max() / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (mix * 32767).astype(np.int16))
print('music.wav', round(len(mix) / SR, 2), 's')

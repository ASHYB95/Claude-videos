# Original score for "Hijack for Artists". Pure synthesis (numpy/scipy), no samples.
# 120 BPM (beat 0.5 s, bar 2 s), A minor: Am – F – C – G. Nightlife groove: moody intro, lift into the product,
# breakdown under the dedication moment, bigger chorus on the payoff, final hit on "gigs".
# The beat grid is offset so the first drop lands on the wipe into the product (3.55 s).
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; DUR = 67.0; N = int(SR * DUR); BEAT = 0.5; OFF = 3.55
here = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(23)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def add(buf, x, t, g=1.0):
    i = int(round(t * SR)); j = min(N, i + len(x))
    if i < 0: x = x[-i:]; i = 0
    if j > i: buf[i:j] += x[:j - i] * g
def st(x, t, g=1.0, pan=0.0):
    add(L, x, t, g * (1 - max(0, pan))); add(R, x, t, g * (1 + min(0, pan)))
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); A = max(1, int(a * SR)); Rr = max(1, int(r * SR)); e[:A] = np.linspace(0, 1, A); e[-Rr:] *= np.linspace(1, 0, Rr); return e
def saw(f, d, det=0.0):
    t = np.arange(int(d * SR)) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1
def beats(t0, t1, step=BEAT):
    k0 = int(np.ceil((t0 - OFF) / step - 1e-6)); k1 = int(np.floor((t1 - OFF) / step - 1e-6))
    return [OFF + k * step for k in range(k0, k1 + 1)]

CH = [[57, 60, 64, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 59, 62, 67]]   # Am F C G
ROOT = [45, 41, 48, 43]
def ci(t): return int(np.floor((t - OFF + 1e-6) / 2)) % 4

# --- drums
def kick():
    n = int(0.4 * SR); t = np.arange(n) / SR; f = 46 + 130 * np.exp(-t * 34)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + 0.18 * np.exp(-t * 400) * rng.standard_normal(n)
def clap():
    n = int(0.28 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    e = np.exp(-t * 18) + 0.7 * np.exp(-((t - 0.01) % 0.012) * 380) * (t < 0.04)
    return bp(x * e, 900, 6500)
def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (14 if open_ else 70))
def crash():
    n = int(2.6 * SR); t = np.arange(n) / SR; return hp(rng.standard_normal(n), 3800) * np.exp(-t * 1.6)
def riser(d):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
    out = np.zeros(n); seg = int(0.05 * SR)
    for i in range(0, n, seg):
        f = 400 + 7000 * (i / n) ** 2; out[i:i + seg] = bp(x[i:i + seg + 1][:seg], f * 0.7, min(f * 1.4, 18000))
    return out * (t / d) ** 2
K, C, HC, HO, CR = kick(), clap(), hat(), hat(True), crash()

KICKS = []
def groove(t0, t1, kick_g=0.9, clap_g=0.36, hat_g=0.10, open_g=0.08, four=True):
    for b in beats(t0, t1):
        k = int(round((b - OFF) / BEAT))
        if four or k % 2 == 0: st(K, b, kick_g); KICKS.append(b)
        if k % 2 == 1: st(C, b, clap_g, 0.05)
        st(HO, b + 0.25, open_g, 0.2)
        for q in range(4): st(HC, b + q * 0.125, hat_g * (1.0 if q % 2 else 0.5), -0.25 if q % 2 else 0.25)
def roll(t_end, g0=0.1, step=0.0625, n=8):
    for k in range(n): st(C, t_end - (n - k) * step, g0 + k * 0.035)

# intro: muffled, heard from outside the room
intro = np.zeros(N)
for b in beats(0, 3.5):
    add(intro, K, b, 0.8)
st(lp(intro, 260), 0, 0.9)
st(riser(1.4), 2.15, 0.10)
roll(3.55, 0.06)
groove(3.55, 27.6)                                        # A: product
st(riser(1.6), 29.95, 0.12); roll(31.55, 0.08)            # breakdown → B
groove(31.55, 54.0, kick_g=0.92, clap_g=0.38, hat_g=0.11)
st(riser(1.2), 53.1, 0.12); roll(54.3, 0.1)
groove(54.55, 59.0, kick_g=0.98, clap_g=0.44, hat_g=0.13, open_g=0.1)   # payoff chorus
groove(59.05, 63.0, kick_g=0.85, clap_g=0.34, hat_g=0.09, four=True)    # end card
for t in [3.55, 31.55, 54.3, 63.1]: st(CR, t, 0.22)
# sidechain
side = np.ones(N)
for b in KICKS:
    i = int(b * SR); n = int(0.3 * SR); seg = 1 - 0.5 * np.exp(-np.arange(n) / SR * 12); side[i:i + n] = np.minimum(side[i:i + n], seg[:max(0, min(n, N - i))])

def active(t): return (3.55 <= t < 27.6) or (31.55 <= t < 63.0)
# --- bass: offbeat octave pluck
bass = np.zeros(N)
for b in beats(3.55, 63.0):
    if not active(b): continue
    r = ROOT[ci(b)]
    for off, o in [(0.0, 0), (0.25, 12)]:
        n = int(0.2 * SR); tt = np.arange(n) / SR; f = hz(r + o - 12)
        add(bass, np.tanh(1.8 * (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt))) * env(n, 0.004, 0.09), b + off)
n = int(3.4 * SR); tt = np.arange(n) / SR; add(bass, np.tanh(np.sin(2 * np.pi * hz(33) * tt)) * env(n, 0.005, 2.5), 63.1)
st(lp(bass, 420) * side, 0, 0.44)

# --- pad: warm, the whole way (filtered in intro and breakdown)
pad = np.zeros(N)
for k in range(-2, 31):
    t0 = OFF + k * 2.0
    if t0 > 63.1: break
    x = sum(saw(hz(m), 2.05, det) for m in CH[k % 4] for det in (-0.004, 0.004)) / 8
    add(pad, x * env(len(x), 0.25, 0.3), t0)
pad_f = np.where((np.arange(N) / SR < 3.55) | ((np.arange(N) / SR > 27.6) & (np.arange(N) / SR < 31.55)), 0, 1)
st(lp(pad, 900) * (1 - pad_f), 0, 0.16)          # dark pad in intro / breakdown
st(lp(pad, 2200) * pad_f * side, 0, 0.11)

# --- plucked arp (16ths over chord tones)
def pluck(m, d=0.22, bright=3600):
    x = (saw(hz(m), d, -0.004) + saw(hz(m), d, 0.004)) / 2; n = len(x)
    return lp(x, bright) * np.exp(-np.arange(n) / SR * 14)
ARP = [0, 1, 2, 3, 2, 1, 2, 3]
for b in beats(3.55, 63.0, 0.25):
    if not active(b): continue
    k = int(round((b - OFF) / 0.25)); notes = CH[ci(b)]
    m = notes[ARP[k % 8]] + 12
    st(pluck(m, bright=2600 if b < 10.55 else 3800), b, 0.085 * side[min(N - 1, int(b * SR))], 0.35 if k % 2 else -0.35)

# --- breakdown keys under the dedication moment (soft electric piano)
def ep(m, d=1.9):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    return (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 3)) * np.exp(-tt * 1.6)
for k, t0 in enumerate([27.65, 29.65]):
    for m in CH[(k + 1) % 4]: st(ep(m + 12), t0 + 0.02 * CH[(k + 1) % 4].index(m), 0.07)
for k, m in enumerate([76, 79, 81, 84, 81, 79]): st(ep(m, 0.9), 27.9 + k * 0.5, 0.05, 0.2 if k % 2 else -0.2)

# --- lead motif (from section B, doubled in the chorus)
def lead(m, d=0.32):
    n = int(d * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sin(2 * np.pi * f * tt)
    return lp(x, 3000) * np.exp(-tt * 7) * env(n, 0.005, 0.05)
MOT = [(0, 76), (0.5, 79), (0.75, 81), (1.25, 79), (1.5, 76), (1.75, 74)]
for k in range(0, 40):
    t0 = OFF + k * 2.0
    if t0 < 31.55 - 0.01 or t0 >= 62.9: continue
    shift = [0, -4, -1, -2][ci(t0)]
    for off, m in MOT:
        st(lead(m + shift), t0 + off, 0.06, 0.2 if off % 1 else -0.2)
        if t0 >= 54.3: st(lead(m + shift + 12, 0.22), t0 + off + 0.004, 0.035, -0.15)

# --- final hit on "gigs"
x = sum(saw(hz(m), 3.6, det) for m in [45, 57, 64, 69, 72, 76] for det in (-0.005, 0, 0.005)) / 18
st(lp(x, 3000) * env(len(x), 0.01, 3.0), 63.1, 0.32)
for k, m in enumerate([76, 81, 84, 88]): st(pluck(m, 1.2, 5000), 63.1 + k * 0.07, 0.09)

out = np.stack([L, R], 1)
fade = np.ones(N); fs = int(65.6 * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 2
out *= fade[:, None]; out = np.tanh(out * 1.1) / np.tanh(1.1); out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav')

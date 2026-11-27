# Synthesised SFX for the LOOT film (numpy/scipy, no samples): paper rip, cha-ching, vault lock,
# digital glitch, camera shutter, key click. Generic UI sounds (tap, whoosh, pop, swipe, impact,
# shimmer, notif, send, riser, stamp, tick, rev) are reused from oneclickdrive/audio in this repo.
import numpy as np, os
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
SR = 44100; here = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(5)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    wf.write(os.path.join(here, f'sfx_{name}.wav'), SR, (x * 32767).astype(np.int16))

def rip(d=0.42):
    n = int(d * SR); t = np.arange(n) / SR
    crack = np.zeros(n); k = 0
    while k < n:                                   # dense irregular fibre snaps
        L = int(rng.uniform(0.002, 0.008) * SR); a = rng.uniform(0.3, 1.0)
        crack[k:k + L] += a * rng.standard_normal(min(L, n - k)) * np.exp(-np.arange(min(L, n - k)) / (L / 3))
        k += int(rng.uniform(0.001, 0.006) * SR)
    body = bp(rng.standard_normal(n), 900, 5000) * 0.5
    e = np.minimum(1, t / 0.02) * np.exp(-np.maximum(0, t - d * 0.6) * 18)
    return (bp(crack, 1200, 9000) + body) * e
def chaching():
    n = int(1.1 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f0, t0, g in ((2093, 0.0, 1), (2637, 0.0, .7), (3136, 0.11, 1), (4186, 0.11, .6)):   # bell strikes
        tt = np.maximum(0, t - t0); on = t >= t0
        for h, hg in ((1, 1), (2.76, .4), (5.4, .2)):
            x += on * g * hg * np.sin(2 * np.pi * f0 * h * tt) * np.exp(-tt * (5 + h * 3))
    drawer = lp(rng.standard_normal(n), 900) * np.exp(-t * 30) * 0.6            # register "ka"
    coins = np.zeros(n)
    for i in range(9):
        t0 = 0.05 + i * 0.035 + rng.uniform(0, .02); i0 = int(t0 * SR); L = int(0.09 * SR)
        f = rng.uniform(4500, 7500); tt = np.arange(L) / SR
        coins[i0:i0 + L] += 0.35 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60)
    return x * 0.5 + drawer + coins
def lock():
    n = int(0.5 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 120)
    clank = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 22) for f in (820, 1330, 2110)) * 0.25
    tt = np.maximum(0, t - 0.06); click2 = hp(rng.standard_normal(n), 3000) * np.exp(-tt * 160) * (t > 0.06) * 0.7
    return thump + click * 0.8 + clank + click2
def glitch():
    n = int(0.36 * SR); t = np.arange(n) / SR; x = np.zeros(n); k = 0
    while k < n:
        L = int(rng.uniform(0.015, 0.05) * SR); f = rng.choice([180, 360, 720, 1440, 95])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) * rng.uniform(.4, 1)
        if rng.random() < 0.35: seg = rng.standard_normal(L) * .7
        x[k:k + L] += seg[:max(0, min(L, n - k))]; k += L + int(rng.uniform(0, .012) * SR)
    x = np.round(x * 6) / 6                     # bit-crush
    return x * np.exp(-t * 3)
def shutter():
    n = int(0.22 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for t0 in (0.0, 0.085):
        tt = np.maximum(0, t - t0); x += (t >= t0) * hp(rng.standard_normal(n), 1800) * np.exp(-tt * 140)
    return x
def key():
    n = int(0.06 * SR); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t * 180) + 0.4 * np.sin(2 * np.pi * 420 * t) * np.exp(-t * 90)

save('rip', rip()); save('chaching', chaching()); save('lock', lock()); save('glitch', glitch()); save('shutter', shutter())
for i in range(4): save(f'key{i}', key())
print('sfx ok')

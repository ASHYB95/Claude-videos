"""Master out/mix.wav → out/master.wav at −14 LUFS integrated, true peak ≤ −1 dBTP (4× oversampled check).
Loudness per ITU-R BS.1770-4 (K-weighting, 400 ms blocks, −70 LUFS absolute and −10 LU relative gates), done here in numpy so the
master doesn't depend on ffmpeg's loudnorm. Run from the library root: .venv/bin/python <project>/master.py"""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import lfilter, resample_poly
sys.path.insert(0, '.')
from core.audio.sfx import limit
D = os.path.dirname(os.path.abspath(__file__))
x, sr = sf.read(os.path.join(D, 'out', 'mix.wav'), always_2d=True)

def kweight(x, sr):
    # stage 1: high shelf (+4 dB above ~1.5 kHz); stage 2: high-pass (~38 Hz). Coefficients from BS.1770 via bilinear design.
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = np.tan(np.pi * f0 / sr); Vh = 10 ** (G / 20); Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b1 = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a1 = [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    f0, Q = 38.13547087602444, 0.5003270373238773
    K = np.tan(np.pi * f0 / sr)
    a2 = [1, 2 * (K * K - 1) / (1 + K / Q + K * K), (1 - K / Q + K * K) / (1 + K / Q + K * K)]
    b2 = [1, -2, 1]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)

def lufs(x, sr):
    y = kweight(x, sr); n = int(.4 * sr); hop = int(.1 * sr)
    z = np.array([np.sum(np.mean(y[i:i + n] ** 2, axis=0)) for i in range(0, len(y) - n, hop)])
    L = -0.691 + 10 * np.log10(z + 1e-12)
    z1 = z[L > -70]; Lr = -0.691 + 10 * np.log10(np.mean(z1)) - 10
    z2 = z1[(-0.691 + 10 * np.log10(z1 + 1e-12)) > Lr]
    return -0.691 + 10 * np.log10(np.mean(z2))

def tp(x): return 20 * np.log10(np.max(np.abs(resample_poly(x, 4, 1, axis=0))) + 1e-12)

y = x.copy(); ceil = 10 ** (-1.6 / 20)
for it in range(6):
    g = 10 ** ((-14.0 - lufs(y, sr)) / 20); y = limit(y * g, ceil)
    I, T = lufs(y, sr), tp(y)
    if T > -1.0: ceil *= 10 ** ((-1.1 - T) / 20)
    if abs(I + 14) < 0.15 and T <= -1.0: break
print(f'master: {I:.2f} LUFS, true peak {T:.2f} dBTP ({it + 1} passes)')
sf.write(os.path.join(D, 'out', 'master.wav'), y.astype(np.float32), sr, subtype='PCM_24')

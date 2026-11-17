# Mix: VO (Alice, ElevenLabs) + music (score.py) + SFX → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 23.8; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
out = np.zeros((N, 2)); vo = np.zeros((N, 2))
def place(buf, x, t, g=1.0, maxlen=None):
    if maxlen: x = x[:int(maxlen * SR)].copy(); f = int(0.03 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

VO = {'v1': 0.30, 'v2': 3.65, 'v3': 6.85, 'v4': 12.15, 'v5': 16.45, 'v6': 19.15}   # must match index.html timings
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t)

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-8), 1.0); k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-15)

names = ['tap', 'whoosh', 'pop', 'swipe', 'shimmer', 'notif', 'popper', 'send', 'tissue', 'typing', 'door', 'clink']
S = {n: load(f'{here}/sfx_{n}.mp3') for n in names}
# per-sfx trim to a common loudness (from measured mean levels)
TRIM = {'tap': 4, 'whoosh': -6, 'pop': 10, 'swipe': 8, 'shimmer': 2, 'notif': -6, 'popper': -6, 'send': -7, 'tissue': 6, 'typing': 2, 'door': -4, 'clink': 10}
cues = [
    ('door', 1.72, -12), ('clink', 2.25, -12),
    ('whoosh', 3.12, -9), ('pop', 3.62, -13), ('pop', 4.0, -16), ('pop', 4.12, -17),
    ('whoosh', 6.7, -15),
    ('pop', 7.31, -14),
    ('tap', 9.0, -9), ('swipe', 9.18, -13),
    ('pop', 9.96, -12), ('shimmer', 10.0, -18),
    ('tap', 10.62, -9), ('tap', 11.3, -9), ('swipe', 11.45, -13),
    ('tap', 12.85, -9), ('pop', 12.93, -14), ('tap', 13.48, -9), ('swipe', 13.62, -13),
    ('pop', 14.15, -15), ('typing', 14.05, -14, 0.95),
    ('tap', 15.4, -8), ('send', 15.48, -11), ('popper', 15.62, -15), ('pop', 15.8, -12),
    ('pop', 16.08, -13), ('pop', 16.32, -14), ('pop', 16.5, -15), ('notif', 16.1, -17),
    ('whoosh', 18.72, -11),
    ('swipe', 19.2, -13),
    ('pop', 22.02, -12), ('shimmer', 22.05, -17),
]
SFX_GAIN = -6   # all SFX at half amplitude (client note, v2)
for c in cues:
    n, t, g = c[:3]; place(out, S[n], t, db(g + TRIM[n] + SFX_GAIN), c[3] if len(c) > 3 else None)
out += vo
fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp)
# VO vs music check: RMS in VO-active windows vs the music bed alone there
def rms(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
m = act
print('mix.wav  · VO rms %.1f dB · music-under-VO rms %.1f dB' % (rms(vo[m]), rms((mus * duck[:, None] * db(-15))[m])))

# Mix: VO (Alice, ElevenLabs) + music (score.py) + SFX (ElevenLabs) → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 32.2; N = int(SR * DUR)
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

VO = {'v1': 0.15, 'v2': 4.65, 'v3': 8.3, 'v4': 15.65, 'v5': 19.15, 'v6': 24.05, 'v7': 26.35}
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t)

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-8), 1.0); k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-15)

names = ['tap', 'whoosh', 'pop', 'swipe', 'impact', 'shimmer', 'coins', 'kaching', 'popper', 'notif', 'paper', 'cheer']
S = {n: load(f'{here}/sfx_{n}.mp3') for n in names}
# per-sfx trim so the cue gains below share a common loudness (from measured mean levels)
TRIM = {'tap': 4, 'whoosh': -6, 'pop': 10, 'swipe': 8, 'impact': -6, 'shimmer': 2, 'coins': 2, 'kaching': -2, 'popper': -6, 'notif': -6, 'paper': 6, 'cheer': -8}
cues = [
    ('paper', 0.05, -12), ('pop', 0.62, -12), ('pop', 2.1, -14), ('swipe', 3.0, -10),
    ('whoosh', 4.4, -9), ('pop', 4.9, -12), ('pop', 6.85, -14),
    ('whoosh', 7.22, -10), ('shimmer', 7.3, -18),
    ('tap', 8.05, -10), ('swipe', 8.18, -14), ('tap', 8.75, -10), ('tap', 9.3, -10), ('swipe', 9.42, -14),
    ('pop', 9.92, -18), ('pop', 10.37, -18), ('tap', 11.15, -10), ('tap', 11.68, -10), ('swipe', 11.8, -14),
    ('tap', 12.15, -10), ('swipe', 12.2, -13), ('tap', 12.72, -10), ('notif', 12.76, -16),
    ('whoosh', 12.78, -14), ('whoosh', 13.3, -14),
    ('pop', 14.45, -14), ('pop', 14.51, -15), ('pop', 14.57, -16), ('pop', 14.63, -16), ('pop', 14.69, -17), ('notif', 14.75, -13),
    ('whoosh', 15.2, -9),
    ('notif', 15.95, -13), ('coins', 16.0, -14), ('notif', 16.72, -14), ('notif', 17.2, -14), ('coins', 17.25, -15),
    ('whoosh', 17.74, -10),
    ('coins', 17.95, -13), ('pop', 17.95, -15), ('pop', 18.17, -15), ('pop', 18.39, -15), ('kaching', 18.95, -12),
    ('swipe', 19.05, -13), ('whoosh', 19.48, -13), ('tap', 19.55, -11), ('kaching', 20.0, -14),
    ('whoosh', 21.38, -13), ('pop', 21.5, -14), ('tap', 21.5, -11), ('shimmer', 21.9, -16),
    ('whoosh', 23.65, -9), ('cheer', 23.95, -9), ('popper', 24.85, -10),
    ('whoosh', 26.18, -10), ('impact', 26.38, -14),
    ('pop', 28.3, -15), ('pop', 28.37, -15), ('pop', 28.44, -16), ('pop', 28.51, -16), ('pop', 28.58, -17),
    ('pop', 29.55, -12), ('tap', 30.2, -8),
]
for n, t, g in cues: place(out, S[n], t, db(g + TRIM[n]))
out += vo
fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav')

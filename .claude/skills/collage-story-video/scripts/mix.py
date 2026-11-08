# Mix: narration (George) + colleague voices + score + paper foley → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 61.5; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
out = np.zeros((N, 2)); vo = np.zeros((N, 2))
def place(buf, x, t, g=1.0, maxlen=None):
    if maxlen: x = x[:int(maxlen * SR)].copy(); f = int(0.04 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g
VO = {'v1': 0.6, 'v2': 6.8, 'v3': 13.5, 'v4': 23.9, 'v5': 33.5, 'q1': 41.4, 'q2': 43.8, 'q3': 46.0, 'v6': 48.7, 'v7': 55.6}
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t, db(-1.5) if k.startswith('q') else 1.0)

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.3 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-6), 1.0); k = int(0.25 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-13)

names = ['tear', 'tape', 'marker', 'stamp', 'typer', 'pencil', 'slide', 'flutter', 'pin', 'whoosh', 'pop']
S = {n: load(f'{here}/sfx_{n}.mp3') for n in names}
TRIM = {'tear': -12, 'tape': -1, 'marker': -4, 'stamp': 0, 'typer': 3, 'pencil': -6, 'slide': 16, 'flutter': 18, 'pin': 17, 'whoosh': -12, 'pop': 6}
cues = [('slide', 0.6, -10), ('slide', 2.4, -10), ('stamp', 2.55, -6), ('typer', 2.8, -14, 1.0), ('marker', 3.35, -10), ('slide', 5.1, -12)]
cues += [('tear', T - 0.35, -8) for T in (6.6, 13.3, 20.0, 23.7, 33.3, 41.2, 48.4, 55.3)]
cues += [('slide', 6.6, -12), ('slide', 7.75, -10), ('marker', 8.1, -10), ('slide', 9.65, -10), ('marker', 9.95, -10), ('slide', 10.5, -9), ('marker', 11.1, -8), ('marker', 11.95, -10),
         ('slide', 13.4, -9), ('marker', 14.75, -14), ('marker', 15.0, -10), ('whoosh', 15.8, -12),
         ('slide', 16.1, -9), ('pin', 16.9, -8), ('pin', 17.12, -8), ('pin', 18.0, -8), ('pin', 18.25, -8), ('marker', 18.3, -10),
         ('slide', 20.05, -10), ('slide', 20.35, -10), ('slide', 21.2, -12), ('marker', 22.3, -8), ('marker', 22.45, -8), ('stamp', 22.5, -8),
         ('slide', 24.3, -8), ('stamp', 24.65, -8), ('slide', 26.25, -10), ('slide', 27.0, -10), ('marker', 27.05, -11), ('slide', 28.5, -10), ('marker', 28.55, -11),
         ('slide', 30.1, -9), ('tape', 30.55, -8), ('tape', 30.65, -10), ('marker', 30.6, -12), ('slide', 31.7, -10),
         ('stamp', 33.5, -7), ('typer', 33.7, -14, 3.0), ('flutter', 33.85, -8), ('flutter', 34.9, -9), ('pencil', 34.4, -28), ('pencil', 36.2, -30),
         ('slide', 35.8, -10), ('slide', 37.2, -10), ('slide', 38.55, -10), ('stamp', 39.4, -8),
         ('slide', 41.3, -13), ('marker', 42.4, -16), ('slide', 43.7, -13), ('marker', 44.6, -16), ('slide', 45.9, -13), ('marker', 46.45, -16),
         ('slide', 48.6, -10), ('slide', 51.3, -12), ('slide', 52.3, -12), ('flutter', 52.85, -9), ('marker', 53.55, -10), ('marker', 53.8, -12),
         ('stamp', 55.5, -8), ('slide', 55.7, -10), ('marker', 58.1, -14), ('pop', 58.5, -12), ('pop', 58.64, -13), ('pop', 58.78, -14), ('stamp', 59.2, -7)]
for c in cues:
    n, t, g = c[:3]; ml = c[3] if len(c) > 3 else None
    place(out, S[n], t, db(g + TRIM[n]), ml)
out += vo
fo = int(0.8 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=10', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav')

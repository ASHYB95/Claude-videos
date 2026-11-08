# Mix: narration (George) + Channa (Bill) + Siddhartha (Eric) + score + paper foley -> mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 64.6; N = int(SR * DUR)
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
# voice-over start times (index.html scenes are timed to these)
VO = {'v1': 0.6, 'v2': 7.45, 'v3': 13.1, 'q1': 19.6, 'v4': 23.25, 'v5': 30.6, 'v6': 36.4, 'v7': 44.7, 'q2': 48.6, 'v8': 51.45, 'v9': 58.85}
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t, db(-1.0) if k.startswith('q') else 1.0)

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.3 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-6), 1.0); k = int(0.25 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-13)

names = ['tear', 'tape', 'marker', 'stamp', 'slide', 'flutter', 'pin', 'whoosh', 'pop', 'hooves', 'bowl']
S = {n: load(f'{here}/sfx_{n}.mp3') for n in names}
TRIM = {'tear': -12, 'tape': -1, 'marker': -4, 'stamp': 0, 'slide': 16, 'flutter': 18, 'pin': 17, 'whoosh': -12, 'pop': 6, 'hooves': -4, 'bowl': -2}
M = -16  # scribbles stay low (user note on the reference film)
cues = [('tear', T - 0.35, -8) for T in (7.2, 12.9, 19.4, 23.0, 30.4, 36.2, 44.5, 48.4, 51.2, 58.6)]
cues += [('slide', .5, -10), ('stamp', 2.3, -6), ('marker', 4.3, M), ('slide', 4.9, -10), ('tape', 5.0, -12),
         ('slide', 7.3, -10), ('marker', 7.7, M), ('slide', 8.3, -10), ('marker', 8.7, M), ('slide', 9.8, -9), ('marker', 10.4, M - 2), ('slide', 11.2, -11), ('pin', 11.6, -8),
         ('marker', 14.5, M - 2), ('slide', 16.0, -10), ('stamp', 16.3, -7), ('slide', 16.9, -10), ('stamp', 17.2, -7), ('slide', 17.8, -10), ('stamp', 18.15, -6),
         ('slide', 19.55, -10), ('slide', 19.6, -13), ('marker', 21.65, M - 2),
         ('hooves', 24.3, -9, 2.4), ('slide', 25.6, -10), ('marker', 26.2, M), ('slide', 27.6, -11),
         ('slide', 30.7, -10), ('marker', 31.9, M - 2), ('marker', 32.5, M - 2), ('stamp', 34.1, -4),
         ('slide', 36.35, -10), ('marker', 38.5, M), ('slide', 39.6, -11), ('slide', 39.85, -12), ('marker', 40.4, M), ('marker', 41.35, M), ('slide', 42.45, -11),
         ('whoosh', 44.6, -16), ('slide', 44.65, -10), ('slide', 45.2, -11), ('marker', 46.75, M),
         ('slide', 48.55, -10), ('slide', 48.6, -13), ('marker', 49.35, M - 2),
         ('bowl', 51.25, -8), ('slide', 51.4, -12), ('slide', 53.4, -12), ('marker', 55.0, M - 2), ('slide', 55.6, -12), ('marker', 56.8, M - 2),
         ('slide', 58.8, -10), ('pop', 60.5, -14), ('marker', 61.5, M - 2)]
for c in cues:
    n, t, g = c[:3]; ml = c[3] if len(c) > 3 else None
    place(out, S[n], t, db(g + TRIM[n]), ml)
out += vo
fo = int(0.9 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=10', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav')

# Mix: VO (Alice, ElevenLabs) + music (score.py) + SFX → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 39.0; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

# VO placement (same starts as audio/vo_track.py; index.html cues are timed to these)
START = {1: 0.35, 2: 2.72, 3: 8.00, 4: 12.04, 5: 16.49, 6: 22.52, 7: 28.66, 8: 34.45}
vo = np.zeros((N, 2))
for i, t in START.items(): place(vo, load(f'{root}/voices/v{i}.mp3'), t)

# music, ducked under the VO
mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-7), 1.0); k = int(0.15 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
MUSIC = -16; SFX = -12
tt = np.arange(N) / SR; lift = np.where(tt > 37.75, db(8), 1.0); lift = np.convolve(lift, np.ones(int(0.3 * SR)) / int(0.3 * SR), 'same')
out = mus * (duck * lift)[:, None] * db(MUSIC)
musbus = out.copy()

# SFX: each normalised so its loudest 120 ms sits at -14 dBFS RMS; cue gains relative to that
names = ['whoosh', 'pop', 'shimmer', 'tick', 'swipe', 'tap', 'sticker']
S = {}
for n in names:
    x = load(f'{here}/sfx_{n}.mp3'); m = (x ** 2).mean(1); w = int(0.12 * SR)
    peak = np.sqrt(np.convolve(m, np.ones(w) / w, 'valid').max()); S[n] = x * (db(-14) / max(peak, 1e-6))
cues = [
    ('whoosh', 0.0, -12), ('shimmer', 0.6, -12),
    ('whoosh', 2.4, -8), ('pop', 2.85, -12), ('swipe', 4.85, -12),
    ('whoosh', 7.75, -9), ('pop', 8.2, -12), ('swipe', 9.8, -12), ('sticker', 11.05, -4),
    ('whoosh', 11.8, -9), ('tick', 12.3, -10), ('swipe', 13.6, -12), ('pop', 13.85, -12), ('pop', 15.5, -12),
    ('whoosh', 16.25, -9), ('pop', 16.8, -12), ('swipe', 19.75, -12),
] + [('tap', 20.2 + i * 0.07, -18) for i in range(8)] + [
    ('whoosh', 22.3, -9), ('pop', 22.7, -12), ('sticker', 23.0, -4), ('sticker', 26.35, -4),
    ('whoosh', 28.4, -9), ('pop', 28.95, -12), ('sticker', 29.2, -4), ('swipe', 31.0, -12),
    ('whoosh', 34.2, -6), ('shimmer', 35.4, -9),
]
sfx = np.zeros((N, 2))
for n, t, g in cues: place(sfx, S[n], t, db(g + SFX))
out = out + sfx + vo
fo = int(0.6 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', '48000', f'{here}/mix.wav'], check=True)
os.remove(tmp)
# report: VO vs bed while the voice is speaking (you can't listen — check the numbers)
bed = out - vo
for i, t in START.items():
    a, b = int(t * SR), int((t + 4) * SR); m = act[a:b]
    r = lambda x: 20 * np.log10(np.sqrt((x[a:b][m] ** 2).mean()) + 1e-9)
    print(f'v{i}  VO {r(vo):6.1f}   music {r(musbus):6.1f}   sfx {r(sfx):6.1f}   VO-bed gap {r(vo) - r(bed):5.1f}')
a = int(35.8 * SR); print('end-card music only (37–39 s) RMS', round(20 * np.log10(np.sqrt((musbus[int(37 * SR):] ** 2).mean()) + 1e-9), 1))
print('mix.wav')

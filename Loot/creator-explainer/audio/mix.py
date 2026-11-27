# Mix: VO (Higgsfield TTS, voice "Dylan") + music (score.py) + SFX → mix.wav at -14 LUFS.
import numpy as np, subprocess, os, glob
SR = 44100; DUR = 60.5; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

# ---- VO: line start times drive every cue in index.html
VO = {'d01': 0.40, 'd02': 6.00, 'd03': 10.25, 'd04': 16.95, 'd05': 23.75, 'd06': 30.20, 'd07': 35.45, 'd08': 41.00, 'd09': 46.05, 'd10': 52.40}
vo = np.zeros((N, 2))
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.wav'), t, db(1.5))

# ---- music, ducked under the VO
mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-9), 1.0); k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
tt = np.arange(N) / SR
lift = np.where(tt < 6.3, db(7), np.where(tt > 56.8, db(2), 1.0))       # quiet intro bed needs lifting
MUSIC = -6
musbus = mus * (duck * lift)[:, None] * db(MUSIC)

# ---- SFX: each normalised so its loudest 120 ms sits at -14 dBFS RMS; cue gains are relative to that
S = {}
for p in glob.glob(f'{here}/sfx_*.*'):
    n = os.path.basename(p)[4:].rsplit('.', 1)[0]
    x = load(p); m = (x ** 2).mean(1); w = int(0.12 * SR)
    peak = np.sqrt(np.convolve(m, np.ones(min(w, len(m))) / min(w, len(m)), 'valid').max()); S[n] = x * (db(-14) / max(peak, 1e-6))
cues = [
    ('whoosh', 0.05, -20), ('rip', 1.72, -7), ('tick', 2.05, -16),
    ('impact', 3.2, -12), ('impact', 4.18, -12), ('impact', 5.12, -10),
    ('whoosh', 5.45, -9), ('rip', 5.8, -12),
    ('impact', 6.38, -8), ('rip', 6.6, -9), ('swipe', 6.95, -18), ('whoosh', 7.35, -15),
    ('tap', 9.45, -9), ('whoosh', 9.6, -13), ('swipe', 9.75, -16),
    ('pop', 10.95, -16),
] + [('key%d' % (i % 4), 11.95 + i * 0.05, -19) for i in range(12)] + [
    ('pop', 12.4, -13), ('tap', 12.85, -9), ('swipe', 12.98, -18), ('swipe', 13.32, -18), ('swipe', 13.66, -18), ('pop', 13.7, -13),
    ('swipe', 14.0, -18), ('pop', 13.95, -14), ('whoosh', 14.6, -16), ('pop', 14.6, -13), ('stamp', 14.98, -7),
    ('shimmer', 15.95, -12), ('notif', 15.98, -13),
    ('whoosh', 16.55, -9),
    ('pop', 17.05, -16), ('tap', 17.98, -9), ('swipe', 18.12, -16), ('tap', 18.82, -9), ('swipe', 18.96, -16),
    ('tick', 19.55, -15), ('tick', 20.25, -15), ('pop', 21.32, -9), ('chaching', 21.4, -14), ('pop', 22.25, -11),
    ('whoosh', 23.5, -16), ('swipe', 23.8, -16),
    ('tap', 25.02, -9), ('pop', 25.12, -11), ('tap', 25.5, -9), ('pop', 26.22, -11), ('pop', 27.2, -12), ('tick', 27.3, -15),
    ('pop', 27.52, -12), ('tick', 27.62, -15), ('tap', 28.3, -7), ('stamp', 28.4, -10), ('shutter', 29.25, -9),
    ('whoosh', 29.85, -13), ('whoosh', 29.98, -12), ('tap', 30.98, -6), ('impact', 31.0, -14),
    ('pop', 31.58, -11), ('lock', 32.25, -6), ('pop', 33.05, -11), ('chaching', 33.1, -13),
    ('whoosh', 34.9, -9),
    ('pop', 36.3, -16), ('stamp', 37.33, -11), ('shutter', 37.4, -11), ('tap', 38.2, -9), ('swipe', 38.34, -16),
    ('tap', 38.78, -9), ('pop', 39.0, -11), ('tap', 39.66, -7), ('send', 39.7, -9), ('pop', 39.95, -13),
    ('whoosh', 40.5, -9), ('rev', 40.6, -14),
    ('pop', 41.2, -12), ('notif', 41.25, -15), ('stamp', 42.2, -6), ('impact', 43.0, -13), ('impact', 43.4, -13), ('tick', 44.3, -11),
    ('whoosh', 45.65, -9), ('whoosh', 45.85, -12),
    ('impact', 46.93, -9), ('impact', 47.28, -10), ('chaching', 47.4, -7),
    ('tap', 48.75, -9), ('swipe', 48.9, -16), ('pop', 49.3, -11), ('chaching', 49.35, -14), ('pop', 50.55, -11), ('tick', 50.9, -15),
    ('whoosh', 51.85, -9),
    ('impact', 52.38, -10), ('impact', 53.22, -10), ('impact', 54.18, -9), ('whoosh', 54.85, -13),
    ('impact', 55.02, -12), ('impact', 55.25, -12), ('glitch', 55.78, -10), ('impact', 56.02, -11), ('glitch', 56.1, -10),
    ('whoosh', 56.4, -9), ('rip', 56.8, -9),
    ('impact', 56.95, -6), ('swipe', 57.2, -16), ('chaching', 57.55, -9), ('pop', 57.95, -11), ('shimmer', 59.1, -15),
]
SFX = -6
sfx = np.zeros((N, 2))
for n, t, g in cues: place(sfx, S[n], t, db(g + SFX))

out = musbus + sfx + vo
fo = int(0.6 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp)
# report: VO vs bed level while the voice is speaking (you can't listen — check the numbers)
bed = musbus + sfx
for k, t in VO.items():
    i = int(t * SR); j = i + int(5 * SR); m = act[i:j]
    r = lambda x: 20 * np.log10(np.sqrt((x[i:j][m] ** 2).mean()) + 1e-9)
    print(f'{k} @{t:5.2f}  VO {r(vo):6.1f}   music {r(musbus):6.1f}   sfx {r(sfx):6.1f}   VO-bed gap {r(vo) - r(bed):5.1f}')
print('mix.wav')

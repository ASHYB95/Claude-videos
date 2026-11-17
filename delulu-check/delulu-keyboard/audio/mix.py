# Mix: VO (Alice) + music (score.py) + ElevenLabs SFX → mix.wav, loudness-normalised to -14 LUFS.
import numpy as np, subprocess, os, json
SR = 44100; DUR = 32.5; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)

def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
out = np.zeros((N, 2)); vo = np.zeros((N, 2))
def place(buf, x, t, g=1.0, maxlen=None, fade=0.03):
    if maxlen: x = x[:int(maxlen * SR)].copy(); f = int(fade * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

VO = {'v1': 0.3, 'v2': 4.0, 'v3': 6.2, 'v4': 10.8, 'v5': 16.1, 'v6': 21.6, 'v7': 26.7}
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t, 1.0)

# music, ducked under VO
mus = load(f'{here}/music.wav')[:N]
mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-8), 1.0); k = int(0.12 * SR)
duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-16)

S = {n: load(f'{here}/sfx_{n}.mp3') for n in ['tap', 'type', 'whoosh', 'spin', 'pop', 'shimmer', 'swipe', 'send', 'impact', 'riser']}
cues = [
    ('type', 0.5, -14, 1.4), ('type', 2.5, -14, 0.95), ('riser', 2.55, -12, None), ('spin', 3.85, -8, None),
    ('pop', 4.9, -12, None),
    ('whoosh', 6.05, -12, None), ('swipe', 6.45, -14, None), ('pop', 6.9, -18, None), ('pop', 7.6, -18, None), ('pop', 8.75, -18, None), ('pop', 9.7, -18, None),
    ('whoosh', 10.45, -11, None), ('tap', 11.1, -8, None), ('shimmer', 11.6, -14, 1.8),
    ('swipe', 13.5, -13, None), ('swipe', 13.66, -15, None), ('swipe', 13.82, -16, None), ('pop', 14.9, -14, None), ('whoosh', 15.6, -13, None),
    ('pop', 16.0, -13, None), ('pop', 16.45, -13, None), ('pop', 17.03, -13, None), ('pop', 17.66, -13, None), ('pop', 18.4, -13, None), ('pop', 19.15, -11, None),
    ('whoosh', 21.2, -13, None), ('swipe', 21.6, -13, None), ('swipe', 23.0, -13, None), ('send', 23.7, -10, None),
    ('whoosh', 24.25, -14, None), ('pop', 24.5, -13, None), ('pop', 25.35, -13, None),
    ('whoosh', 26.25, -10, None), ('impact', 26.5, -6, None), ('tap', 29.2, -9, None), ('pop', 29.7, -15, None),
]
TRIM = {'impact': -6, 'riser': -10, 'spin': -6, 'whoosh': -6, 'send': -6, 'type': -4, 'pop': 10, 'swipe': 8, 'shimmer': 4, 'tap': 0}
for n, t, g, ml in cues: place(out, S[n], t, db(g + TRIM[n]), ml)
out += vo * db(0)
fo = int(0.6 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'
out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav')

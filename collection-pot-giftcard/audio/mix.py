# Mix: VO (Alice, ElevenLabs) + music (score.py) + SFX → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 24.4; N = int(SR * DUR)
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

VO = {'v1': 0.30, 'v2': 3.65, 'v3': 6.85, 'v4': 11.95, 'v5': 16.95, 'v6': 19.65}   # must match index.html timings
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
    ('tap', 4.55, -9), ('tap', 5.08, -9), ('swipe', 5.22, -13),          # Someone else · NEXT · page
    ('tap', 5.85, -9), ('tap', 6.18, -10), ('typing', 6.22, -15, 0.3),   # Leaver · name field · "Jo"
    ('swipe', 6.85, -13), ('whoosh', 6.85, -16), ('pop', 7.42, -14),     # → real Pot, push-in, card
    ('whoosh', 9.0, -17),                                               # scroll messages
    ('swipe', 11.85, -13),                                              # → gift cards
    ('pop', 14.87, -12), ('pop', 15.16, -14),                           # sticker · John Lewis
    ('whoosh', 15.46, -10), ('pop', 16.01, -12), ('shimmer', 16.05, -18),  # flick → Costa
    ('swipe', 16.75, -13), ('popper', 17.0, -16),
    ('pop', 17.14, -13), ('pop', 17.34, -14), ('pop', 17.54, -15),       # cards + message pop out
    ('whoosh', 19.22, -11), ('swipe', 19.7, -13),
    ('pop', 22.52, -12), ('shimmer', 22.55, -17),
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

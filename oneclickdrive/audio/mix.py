# Mix: VO (Sarah, ElevenLabs) + music (score.py) + SFX (ElevenLabs) → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 32.6; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
out = np.zeros((N, 2)); vo = np.zeros((N, 2))
def place(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g
def seg(x, a, b):  # cut [a,b) seconds with short fades
    y = x[int(a * SR):int(b * SR)].copy(); f = int(0.02 * SR); y[:f] *= np.linspace(0, 1, f)[:, None]; y[-f:] *= np.linspace(1, 0, f)[:, None]; return y

# VO placement (word timings drive the cues in index.html)
for k, t in {'v1': 0.25, 'v2': 5.3, 'v4': 17.4, 'v5': 20.6, 'v6': 24.5, 'v7': 28.0}.items():
    place(vo, load(f'{root}/voices/{k}.mp3'), t)
v3 = load(f'{root}/voices/v3.mp3')   # the 3 steps: one take, split at its pauses so each screen gets room
place(vo, seg(v3, 0.0, 1.12), 9.3)            # "Pick a car type…"
place(vo, seg(v3, 1.12, 4.02), 9.75 + 1.12)   # "…compare real prices from verified suppliers…"
place(vo, seg(v3, 4.02, len(v3) / SR), 10.15 + 4.02)  # "…and message the supplier direct on WhatsApp."

# music, ducked under the VO
mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-8), 1.0); k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
MUSIC = -7; SFX = -10   # global trims (dB): music up, SFX well down
tt = np.arange(N) / SR; hook = np.where(tt < 4.9, db(4), np.where(tt > 27.8, db(3), 1.0))   # lift the quieter intro groove and the end-card ring-out
out += mus * (duck * hook)[:, None] * db(MUSIC)

# SFX: each normalised so its loudest 120 ms sits at -14 dBFS RMS, then cue gains are relative to that
names = ['tap', 'whoosh', 'pop', 'swipe', 'impact', 'shimmer', 'notif', 'send', 'riser', 'spin', 'strike', 'pindrop', 'rev', 'tick', 'stamp']
S = {}
for n in names:
    x = load(f'{here}/sfx_{n}.mp3'); m = (x ** 2).mean(1); w = int(0.12 * SR)
    peak = np.sqrt(np.convolve(m, np.ones(w) / w, 'valid').max()); S[n] = x * (db(-14) / max(peak, 1e-6))
cues = [
    ('whoosh', 0.15, -14), ('pop', 1.85, -10), ('tap', 1.85, -14),
    ('pop', 2.25, -8), ('strike', 2.68, -9), ('pop', 3.0, -8), ('strike', 3.38, -9), ('pop', 3.8, -8), ('strike', 4.38, -9),
    ('rev', 4.55, -15), ('whoosh', 4.75, -7), ('spin', 5.05, -14), ('pop', 5.25, -10),
    ('whoosh', 6.75, -16), ('swipe', 8.2, -16),
    ('pop', 9.15, -14), ('swipe', 9.2, -14), ('tap', 10.05, -6), ('swipe', 10.25, -10),
    ('swipe', 10.6, -13), ('pop', 11.65, -8), ('pop', 12.0, -10), ('pop', 12.2, -10), ('pop', 12.4, -10),
    ('pop', 12.95, -9), ('shimmer', 12.95, -16), ('whoosh', 13.72, -16),
    ('swipe', 14.0, -13), ('tap', 14.95, -6), ('pop', 15.15, -10), ('send', 15.25, -9), ('tick', 15.95, -16), ('notif', 16.25, -9),
    ('whoosh', 17.0, -9), ('stamp', 17.38, -6), ('stamp', 18.25, -6), ('stamp', 19.2, -6), ('riser', 19.6, -14),
    ('whoosh', 20.28, -7),
    ('pop', 20.6, -12), ('pop', 20.75, -12),
    ('pindrop', 21.4, -8), ('pop', 21.6, -13), ('pindrop', 22.3, -8), ('pop', 22.5, -13), ('pindrop', 23.2, -8), ('pop', 23.4, -13),
    ('whoosh', 24.02, -7), ('whoosh', 24.12, -10),
    ('tick', 24.6, -8), ('whoosh', 25.4, -15), ('pop', 25.45, -12), ('pop', 25.57, -12), ('pop', 25.69, -12), ('pop', 25.81, -12),
    ('pop', 26.65, -8), ('shimmer', 26.7, -15), ('rev', 27.3, -13),
    ('whoosh', 27.72, -9), ('pop', 28.0, -10), ('pop', 29.65, -9), ('tap', 30.25, -5), ('shimmer', 30.7, -13),
]
sfx = np.zeros((N, 2))
for n, t, g in cues: place(sfx, S[n], t, db(g + SFX))
musbus = out.copy(); out += sfx
out += vo
fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp)
# report: VO vs bed level per VO line (you can't listen — check the numbers)
bed = out - vo
for a, b in [(0.25, 5.0), (5.3, 9.0), (9.3, 16.9), (17.4, 20.2), (20.6, 24.1), (24.5, 27.6), (28.0, 31.4)]:
    i, j = int(a * SR), int(b * SR); m = act[i:j]   # measure only while the voice is speaking
    r = lambda x: 20 * np.log10(np.sqrt((x[i:j][m] ** 2).mean()) + 1e-9)
    print(f'{a:5.1f}-{b:5.1f}  VO {r(vo):6.1f}   music {r(musbus):6.1f}   sfx {r(sfx):6.1f}   VO-bed gap {r(vo) - r(bed):5.1f}')
print('mix.wav')

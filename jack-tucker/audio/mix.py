# Mix: VO (Chris, ElevenLabs) + music (score.py) + SFX (ElevenLabs, sfx.py) → mix.wav at -14 LUFS.
import numpy as np, subprocess, os
SR = 44100; DUR = 67.0; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
out = np.zeros((N, 2)); vo = np.zeros((N, 2))
def place(buf, x, t, g=1.0, maxlen=None):
    if maxlen: x = x[:int(maxlen * SR)].copy(); f = int(0.25 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

# VO placements (seconds) — these drive the whole edit
VO = {'v01': 0.35, 'v02': 3.75, 'v03': 7.05, 'v04': 10.75, 'v05': 17.05, 'v06': 23.3, 'v07': 27.85, 'v08': 32.25,
      'v09': 35.7, 'v10': 39.9, 'v11': 44.05, 'v12': 47.3, 'v13': 50.8, 'v14': 54.6, 'v15': 59.75}
for k, t in VO.items(): place(vo, load(f'{root}/voices/{k}.mp3'), t)

mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
act = np.abs(vo).max(1) > 0.01
w = int(0.25 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.02
duck = np.where(act, db(-8), 1.0); k = int(0.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
out += mus * duck[:, None] * db(-14)

names = ['tap', 'whoosh', 'pop', 'swipe', 'impact', 'shimmer', 'notif', 'coin', 'typing', 'scan', 'crowd', 'cheer']
S = {n: load(f'{here}/sfx_{n}.mp3') for n in names}
# per-sfx trim to a common ~-20 dB mean (measured with ffmpeg volumedetect)
TRIM = {'tap': 10, 'whoosh': 1.6, 'pop': 5.3, 'swipe': -7.8, 'impact': -9.3, 'shimmer': 5.2, 'notif': 2.2, 'coin': 3.2,
        'typing': 2.6, 'scan': 0, 'crowd': -2.3, 'cheer': 5.8}
cues = [
    # hook
    ('impact', 0.33, -16), ('impact', 1.27, -17), ('impact', 1.93, -16), ('whoosh', 3.28, -8),
    # the turn
    ('whoosh', 3.6, -14), ('impact', 4.6, -9), ('shimmer', 4.95, -16), ('pop', 5.6, -11), ('coin', 5.65, -14), ('whoosh', 6.7, -17),
    # set up
    ('swipe', 6.9, -15), ('typing', 7.05, -12), ('typing', 7.42, -13), ('tap', 7.8, -10), ('swipe', 7.86, -15), ('pop', 8.0, -11),
    ('whoosh', 8.85, -15), ('pop', 8.95, -11), ('pop', 9.45, -13),
    # guests scan
    ('whoosh', 10.42, -12), ('whoosh', 10.6, -14), ('scan', 11.45, -12), ('swipe', 11.5, -16), ('whoosh', 13.85, -18),
    ('swipe', 14.95, -15), ('pop', 15.1, -11), ('pop', 15.79, -11),
    # live queue
    ('whoosh', 16.85, -12), ('tap', 17.85, -10), ('tap', 18.42, -10), ('whoosh', 18.5, -15), ('coin', 18.9, -11), ('swipe', 19.25, -15),
    ('pop', 19.98, -12), ('pop', 21.56, -12), ('notif', 21.62, -14), ('whoosh', 21.62, -16), ('pop', 22.1, -14),
    # your yes
    ('whoosh', 23.0, -13), ('swipe', 23.05, -15), ('tap', 23.72, -10), ('tap', 24.32, -9), ('shimmer', 24.36, -14), ('coin', 24.4, -13),
    ('whoosh', 24.85, -16), ('pop', 25.35, -13), ('pop', 25.95, -11),
    # the moment (B-roll B)
    ('notif', 28.85, -11), ('cheer', 30.0, -10), ('notif', 30.75, -12),
    # live chat
    ('whoosh', 31.95, -12), ('pop', 33.2, -13), ('tap', 33.9, -10), ('swipe', 33.95, -13), ('tap', 34.45, -10), ('pop', 34.8, -15),
    # nightly goal
    ('whoosh', 35.45, -12), ('whoosh', 35.55, -13), ('coin', 37.4, -17), ('coin', 37.7, -16), ('coin', 38.0, -15), ('coin', 38.3, -14),
    ('coin', 38.6, -13), ('whoosh', 38.25, -16), ('whoosh', 38.4, -16), ('impact', 38.92, -14), ('shimmer', 38.95, -13),
    # skins
    ('whoosh', 39.65, -12), ('tap', 40.29, -10), ('swipe', 40.29, -16), ('tap', 40.76, -10), ('swipe', 40.76, -16), ('tap', 41.38, -10),
    ('swipe', 41.38, -16), ('pop', 42.2, -13), ('pop', 42.28, -14), ('pop', 42.36, -14), ('pop', 42.44, -15), ('tap', 43.14, -10),
    # stream
    ('whoosh', 43.75, -13), ('whoosh', 43.85, -13), ('pop', 44.88, -11), ('swipe', 45.0, -14), ('pop', 45.2, -16), ('pop', 45.35, -16), ('pop', 45.5, -16),
    # analytics
    ('whoosh', 46.9, -12), ('swipe', 47.75, -16), ('pop', 47.85, -11), ('swipe', 48.95, -16), ('pop', 49.02, -11),
    # payout
    ('swipe', 50.6, -15), ('whoosh', 51.5, -17), ('coin', 51.92, -11), ('pop', 52.95, -11), ('notif', 52.97, -12),
    # payoff (B-roll C)
    ('whoosh', 54.06, -9), ('whoosh', 54.12, -10), ('impact', 54.3, -12), ('cheer', 54.6, -14),
    # end card
    ('whoosh', 59.3, -11), ('impact', 59.72, -9), ('shimmer', 60.0, -16), ('pop', 61.3, -14), ('pop', 61.42, -14), ('pop', 61.54, -14),
    ('pop', 62.2, -11), ('tap', 63.08, -8), ('shimmer', 63.12, -12),
]
place(out, S['crowd'], 0.0, db(-8 + TRIM['crowd']), maxlen=3.6)      # bar ambience under the hook
for n, t, g in cues: place(out, S[n], t, db(g + TRIM[n]))
out += vo
fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp)
# report VO vs music level (can't listen, so check numerically)
def rms(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
m = act.astype(bool)
print('mix.wav  | VO rms (speech) %.1f dB, music rms under VO %.1f dB, music rms in gaps %.1f dB' %
      (rms(vo[m]), rms((mus * duck[:, None] * db(-14))[m]), rms((mus * db(-14))[~m])))

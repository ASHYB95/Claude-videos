# Mix: voice (work/voice.wav, from scripts/cut.py) + lo-fi bed (music.wav, ducked under speech)
# + paper/UI foley cued to the on-screen action -> mix.wav at -14 LUFS, true peak -1 dB.
import numpy as np, subprocess, os
SR = 48000; DUR = 86.7; N = int(SR * DUR)
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
def db(x): return 10 ** (x / 20)
def place(buf, x, t, g=1.0, maxlen=None):
    if maxlen:
        x = x[:int(maxlen * SR)].copy(); f = min(len(x), int(0.06 * SR)); x[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t * SR); j = min(N, i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g

out = np.zeros((N, 2)); vo = np.zeros((N, 2))
place(vo, load(f'{root}/work/voice.wav'), 0.0)

# ---- music: ducked while he speaks, lifted for the end card ----
mus = load(f'{here}/music.wav')[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
env = np.abs(vo).max(1)
w = int(0.05 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
act = env > 0.012
w = int(0.35 * SR); act = np.convolve(act.astype(float), np.ones(w) / w, 'same') > 0.05
gain = np.where(act, db(-8), 1.0)
t = np.arange(N) / SR
gain = np.where(t > 84.55, db(4), gain)                       # end card: let the beat breathe
k = int(0.3 * SR); gain = np.convolve(gain, np.ones(k) / k, 'same')
out += mus * gain[:, None] * db(-15)

# ---- foley: every sample normalised to the same RMS, then cued ----
names = ['tear', 'tape', 'marker', 'stamp', 'typer', 'slide', 'flutter', 'pin', 'whoosh', 'pop',
         'swish', 'plug', 'tap', 'ding', 'flip', 'tv', 'crowd', 'tick', 'switch']
S = {}
for n in names:
    x = load(f'{here}/sfx_{n}.mp3')
    nz = x[np.abs(x).max(1) > 1e-3]
    rms = np.sqrt((nz ** 2).mean()) if len(nz) else 1
    S[n] = x * (db(-20) / max(rms, 1e-6))
C = []
def c(n, tt, g, ml=None): C.append((n, tt, g, ml))
# P1 credentials
c('pop', .08, -12); c('whoosh', 1.68, -18); c('stamp', 1.86, -8); c('tick', 1.92, -15, 1.3); c('marker', 2.7, -20, .45); c('slide', 3.2, -15)
# camera morphs (full screen <-> circle <-> photo)
for tt in [3.78, 7.82, 10.4, 13.0, 31.4, 33.5, 38.3, 42.2, 54.1, 57.55, 73.8, 76.25, 81.95, 84.3]: c('swish', tt, -11)
c('pop', 85.35, -11)
# torn-paper transitions
for T in [16.9, 22.6, 52.2, 70.45]: c('tear', T - .35, -9)
# P2 platforms
c('slide', 3.85, -13)
for i in range(7): c('pop', 4.62 + i * .21, -15 - (i % 2))
c('marker', 6.9, -20, .5)
# P3 headline in a taped photo
for tt in [10.95, 11.75, 12.4]: c('slide', tt, -17)
c('tape', 11.0, -12, .6)
for i in range(3): c('pop', 12.75 + i * .12, -15)
# S4 01 Educational
c('stamp', 13.25, -8); c('slide', 13.6, -13); c('switch', 14.55, -8); c('marker', 15.45, -20, .4)
# S5 value
c('slide', 16.95, -13); c('pop', 17.45, -15); c('slide', 18.95, -15); c('slide', 19.3, -16); c('stamp', 19.6, -11)
c('pop', 20.15, -13); c('pop', 20.55, -15); c('marker', 21.5, -20, .5)
# S6 Whole Truth
c('typer', 22.7, -19, .6); c('slide', 23.0, -13)
for tt in [24.6, 24.82, 25.12]: c('pop', tt, -17)
c('pop', 26.75, -15); c('slide', 27.3, -17); c('marker', 28.6, -20, .5); c('slide', 29.4, -13); c('marker', 30.6, -20, .5)
# F7a 02 Emotional
c('stamp', 31.75, -8); c('pop', 32.25, -15); c('slide', 32.6, -15)
# S7 emotions
c('typer', 33.9, -19, .6); c('pop', 34.4, -16)
for tt in [35.21, 35.71, 36.13, 36.99, 37.83]: c('pop', tt - .25, -17); c('stamp', tt, -11)
# F7b
c('pop', 38.9, -15); c('whoosh', 40.15, -17); c('slide', 40.3, -13)
# S8 Humans of...
c('typer', 42.55, -19, .5); c('slide', 43.3, -13); c('pin', 43.6, -12); c('slide', 44.3, -13); c('pin', 44.6, -12)
c('stamp', 46.3, -8); c('tick', 46.35, -15, 1.1); c('slide', 47.5, -15); c('slide', 48.0, -16); c('marker', 48.55, -20, .5)
c('whoosh', 49.4, -17); c('typer', 49.8, -19, .5); c('slide', 51.3, -15)
# S9 03 Topical
c('stamp', 52.45, -8); c('slide', 52.5, -13); c('flip', 53.28, -9); c('marker', 53.85, -20, .4)
# F10 best of three
for i in range(3): c('pop', 54.45 + i * .12, -15)
c('pop', 56.85, -11); c('marker', 56.95, -20, .4); c('whoosh', 57.62, -17)
# S10 thought bubble + plug
c('slide', 57.75, -13)
for i in range(3): c('pop', 58.5 + i * .1, -17)
c('marker', 58.75, -22, .6); c('typer', 59.2, -19, .6)
for tt in [60.87, 61.79, 62.83]: c('pop', tt - .17, -14); c('stamp', tt, -11)
c('whoosh', 63.75, -13); c('plug', 64.48, -6); c('pop', 64.95, -15); c('marker', 66.75, -20, .5)
c('slide', 68.2, -13)
for tt in [68.95, 69.55, 69.82]: c('pop', tt, -13)
c('marker', 69.6, -20, .5)
# S12 TV
c('typer', 70.8, -19, .7); c('slide', 70.85, -13); c('tv', 71.1, -11); c('crowd', 71.3, -21, 2.9)
c('stamp', 72.2, -8); c('pop', 72.85, -15); c('stamp', 73.5, -8)
# F13 it just works
c('slide', 74.3, -15); c('stamp', 75.75, -4); c('whoosh', 76.25, -17)
# S13 Venn
c('typer', 76.5, -19, .5)
for tt in [76.85, 77.1, 77.35]: c('pop', tt, -13)
c('slide', 78.0, -15); c('swish', 78.1, -12); c('pop', 79.2, -10); c('marker', 81.0, -20, .5)
# F14 going viral
c('slide', 82.9, -13)
# S15 end card
c('slide', 84.5, -15); c('slide', 84.65, -13); c('marker', 85.45, -20, .4); c('tap', 85.95, -7); c('ding', 86.03, -8)

for n, tt, g, ml in C: place(out, S[n], tt, db(g), ml)
out += vo
fo = int(0.7 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav', len(C), 'cues')

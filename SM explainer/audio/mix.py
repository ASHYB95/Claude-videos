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
# v2 (client note): ~75% fewer effects, only where they mark a moment, and every effect 6 dB quieter.
SFX_TRIM = -6
# transitions: camera morphs (full screen <-> circle <-> photo) and torn-paper wipes
for tt in [3.78, 7.82, 10.4, 13.0, 31.4, 33.5, 38.3, 42.2, 54.1, 57.55, 73.8, 76.25, 81.95, 84.3]: c('swish', tt, -12)
for T in [16.9, 22.6, 52.2, 70.45]: c('tear', T - .35, -10)
# the big beats
c('stamp', 1.86, -9); c('tick', 1.92, -16, 1.3)          # 1,500 brands counter
c('stamp', 13.25, -9); c('stamp', 31.75, -9); c('stamp', 52.45, -9)   # 01 / 02 / 03
c('switch', 14.55, -9)                                    # bulb switches on
c('tick', 46.35, -16, 1.1)                                # followers counter
c('flip', 53.28, -11)                                     # calendar
c('plug', 64.48, -8)                                      # plug in your product
for tt in [68.95, 69.55, 69.82]: c('pop', tt, -15)        # "work well, really, really well"
c('tv', 71.1, -12); c('crowd', 71.3, -22, 2.9)            # the IPL TV
c('stamp', 75.75, -6)                                     # IT JUST WORKS
c('swish', 78.1, -13)                                     # the pillars merge
c('tap', 85.95, -9); c('ding', 86.03, -10)                # FOLLOW -> FOLLOWING

for n, tt, g, ml in C: place(out, S[n], tt, db(g + SFX_TRIM), ml)
out += vo
fo = int(0.7 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = f'{here}/_pre.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', str(SR), f'{here}/mix.wav'], check=True)
os.remove(tmp); print('mix.wav', len(C), 'cues')

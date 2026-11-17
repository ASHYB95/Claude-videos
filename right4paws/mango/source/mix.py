# Mix: voice (chain + ducking) + score + foley from events.json → out/mix.wav (48 kHz stereo)
import sys, os, json
sys.path.insert(0, os.environ.get('LIB', '.'))
import numpy as np, soundfile as sf, soxr
from scipy.signal import fftconvolve
from core.audio.sfx import SR, add, limit, compress, bp, lp, hp, noise, brown, t_, env_exp, whoosh, thump, ding, pop, click, clack, norm
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, 'events.json'))); DUR = E['dur']; EV = E['ev']
N = int(DUR * SR) + SR
rng = np.random.default_rng(3)
fol = np.zeros((N, 2), np.float32); vox = np.zeros((N, 2), np.float32)
amb = np.zeros((N, 2), np.float32)

def env(d, a=.02, r=.1):
    x = np.ones(int(round(d * SR))); na, nr = int(a * SR), int(r * SR)
    if na: x[:na] = np.linspace(0, 1, na)
    if nr: x[-nr:] *= np.linspace(1, 0, nr)
    return x
def crayon(d, speed=8, v=1.0):   # stick-slip: band-passed noise, grainy, rhythmic back-and-forth
    n = bp(noise(d), 1200, 5200); tt = t_(d)
    am = 0.55 + 0.45 * np.abs(np.sin(np.pi * speed * tt + rng.random())) ; grain = (rng.random(len(n)) < .08) * rng.random(len(n))
    return n * am * (0.6 + 0.8 * lp(grain, 300) * 6) * env(d, .03, .08) * .35 * v
def jingle(v=1.0):
    d = .5; tt = t_(d); out = np.zeros(len(tt))
    for k, dt in enumerate((0, .07, .13)):
        s = int(dt * SR); f = 3300 + 900 * k
        out[s:] += (np.sin(2 * np.pi * f * tt[:len(tt) - s]) + .5 * np.sin(2 * np.pi * f * 1.47 * tt[:len(tt) - s])) * np.exp(-tt[:len(tt) - s] / .08)
    return out * .12 * v
def sniff(): d = .14; return hp(bp(noise(d), 1500, 6000), 800) * np.sin(np.pi * t_(d) / d) ** 2 * .35
def sigh(): d = .8; return lp(noise(d), 1400) * np.sin(np.pi * t_(d) / d) ** 1.5 * .22
def hmph(): d = .22; return (lp(noise(d), 900) * np.sin(np.pi * t_(d) / d) * .35) + np.pad(thump(.25, 110)[:int(d * SR)], (0, 0))[:int(d * SR)]
def rattle(d=.5, n=10, f0=2500, v=1.0):
    out = np.zeros(int(d * SR) + SR // 5)
    for _ in range(n):
        s = int(rng.random() * d * SR); c = clack(1.4 + rng.random() * .8, .5 + .5 * rng.random())
        c = bp(c, f0 * .6, min(f0 * 3, 20000)); out[s:s + len(c)] += c[:len(out) - s]
    return out * .35 * v
def chirp():
    d = .09; tt = t_(d); f = 3200 + 1800 * tt / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * .05
def whine(): d = .6; tt = t_(d); f = 720 + 160 * tt / d + 12 * np.sin(2 * np.pi * 6 * tt); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * .05
def crunch(): d = .09; return bp(noise(d), 700, 4500) * env_exp(d, .025) * .45
def brush(d, v=1.0):
    n = lp(noise(d), 1800) + .3 * bp(noise(d), 2500, 6000) * (rng.random(int(round(d * SR))) < .3)
    return n * env(d, .15, .4) * .3 * v

for x in EV:
    t, ty = x['t'], x['type']; pan = x.get('pan', 0) or 0
    if ty == 'scribble': add(fol, crayon(x['dur'], 9), t, .9, pan)
    elif ty == 'scratch': add(fol, crayon(x['dur'], 3), t, .8, pan)
    elif ty == 'write': add(fol, crayon(x['dur'], 5), t, .7, 0)
    elif ty == 'crayonoff': add(fol, click(.8, .4), t, .4, .4)
    elif ty == 'sigh': add(fol, sigh(), t, 1, 0)
    elif ty == 'pellets': add(fol, rattle(.6, 12, 1800), t, .9, pan)
    elif ty == 'sniff': add(fol, sniff(), t, 1, pan)
    elif ty == 'hmph': add(fol, hmph(), t, .9, 0)
    elif ty == 'jingle': add(fol, jingle(), t, 1, .1)
    elif ty == 'whoosh': add(fol, whoosh(x.get('dur', .35), .7), t, .6, 0)
    elif ty == 'thump': add(fol, thump(1.0, 58), t, 1.0, 0); add(fol, bp(noise(.12), 150, 900) * env_exp(.12, .03), t, .6, 0)
    elif ty == 'flaps': add(fol, bp(noise(.08), 200, 1500) * env_exp(.08, .02), t, .5, -.2); add(fol, bp(noise(.08), 200, 1500) * env_exp(.08, .02), t + .15, .5, .2)
    elif ty == 'pop': add(fol, pop(.7), t, .5, 0)
    elif ty == 'plop': add(fol, thump(.6, 130), t, .55, pan)
    elif ty == 'tail': add(fol, thump(.35, 85), t, .4, .3)
    elif ty == 'page':
        d = x['dur']; add(fol, lp(noise(d), 2500) * np.sin(np.pi * t_(d) / d) ** 2 * .2, t, 1, 0)
        add(fol, whoosh(.5, .5), t + d * .4, .5, -.3); add(fol, bp(noise(.07), 300, 3000) * env_exp(.07, .02), t + d - .05, .6, -.4)
    elif ty == 'birds':
        for k in range(14): add(amb, chirp(), t + k * .45 + rng.random() * .3, 1, -.6 + 1.2 * rng.random())
    elif ty == 'ding': add(fol, ding(.5), t, .35, .4)
    elif ty == 'tick': add(fol, click(1.6, .5), t, .25, -.45)
    elif ty == 'whine': add(fol, whine(), t, 1, 0)
    elif ty == 'pour': add(fol, rattle(x['dur'], 60, 3200, 1.2), t, 1.0, .3)
    elif ty == 'munch': add(fol, crunch(), t + rng.random() * .03, .9, .2)
    elif ty == 'snort': add(fol, lp(noise(.12), 1200) * env_exp(.12, .04) * .3, t, 1, 0)
    elif ty == 'brush': add(fol, brush(x['dur']), t, 1, -.5 * x.get('dir', 1))
# room tone throughout, a little brighter on page two
room = lp(brown(DUR + 1), 500); room = room / (np.abs(room).max() + 1e-9) * .012
add(amb, room, 0, 1, 0)

# —— voice: high-pass → compress → tilt EQ (warm, softer highs) → near-field reverb; placed on the timeline
def vchain(x):
    x = hp(x, 80); x = compress(x, .2, 2.5, .008, .14)
    x = x + .25 * lp(x, 250) - .25 * hp(x, 6500)
    ir = rng.standard_normal(int(.6 * SR)) * np.exp(-np.arange(int(.6 * SR)) / (.12 * SR)); ir = lp(ir, 3500); ir /= np.sqrt((ir ** 2).sum())
    wet = fftconvolve(x, ir)[:len(x) + int(.3 * SR)] * 10 ** (-18 / 20)
    y = np.zeros(len(wet)); y[:len(x)] += x; y += wet
    return norm(y, .8)
for x in EV:
    if x['type'] != 'voice': continue
    w, sr = sf.read(os.path.join(HERE, 'voices', x['id'] + '.wav'))
    if w.ndim > 1: w = w.mean(1)
    w = soxr.resample(w, sr, SR)
    add(vox, vchain(w), x['t'], .78, 0)

# —— music, ducked under the voice (~ -7 dB)
mus, msr = sf.read(os.path.join(HERE, 'out', 'music.wav'))
m = np.zeros((N, 2)); m[:min(N, len(mus))] = mus[:N]
ve = np.abs(vox).max(1); k = int(.25 * SR)
ve = np.convolve(ve, np.ones(k) / k, 'same'); ve = np.clip(ve / (ve.max() + 1e-9) * 4, 0, 1)
duck = 1 - .55 * ve
mix = m * 1.25 * duck[:, None] + fol * .9 * (1 - .3 * ve[:, None]) + amb + vox
mix = limit(mix[:int(DUR * SR)], .95)
sf.write(os.path.join(HERE, 'out', 'mix.wav'), mix.astype(np.float32), SR)
print('mix', len(mix) / SR, 'peak', float(np.abs(mix).max()))

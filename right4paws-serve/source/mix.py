"""Mix: score (music/score.wav) + ElevenLabs narration (voices/) + procedural foley at events.json times + room tone → out/mix.wav
Run from the library root: .venv/bin/python <project>/mix.py
Three layers: ambience (warm room tone + a very quiet mantel clock on the beat grid), foley by material (steel bowl, cardboard pack,
dry flakes, water, paper wipes, rubber stamps), music ducking ~8 dB under the voice.
Silences: 11.5–12.0 music out (room tone stays); 32.0–33.6 total silence: the first sound after it is the bowl on the floor."""
import sys, os, json, numpy as np, soundfile as sf
sys.path.insert(0, '.')
from core.audio.sfx import SR, t_, env_exp, bp, lp, hp, noise, norm, brown, click, clack, whoosh, creak, thump, ding, pop, add, compress, limit
D = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(D, 'events.json')))
DUR = E['dur']; N = int(round(DUR * SR)); EV = E['ev']
rng = np.random.default_rng(4)
def nz(d): return rng.standard_normal(len(t_(d)))
def env_ad(d, a=.004, tau=.1):
    x = env_exp(d, tau); n = int(a * SR)
    if n: x[:n] *= np.linspace(0, 1, n)
    return x
def M(*xs): n = max(len(x) for x in xs); return sum(np.pad(x, (0, n - len(x))) for x in xs)
def sine(f, d): return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, len(t_(d))).astype(float)) / SR)

# ---------------- foley by material ----------------
def steel(f0=520, d=1.4, v=1.0, tau=.35):      # a steel bowl: inharmonic partials + a contact click
    parts = [(1, 1, tau), (2.32, .6, tau * .7), (4.25, .35, tau * .45), (6.63, .2, tau * .3), (9.1, .1, tau * .2)]
    x = sum(a * sine(f0 * r * (1 + .002 * np.sin(2 * np.pi * 3 * t_(d))), d) * env_exp(d, ta) for r, a, ta in parts)
    x = x + hp(nz(d), 2500) * env_exp(d, .004) * 1.2 + lp(nz(d), 400) * env_exp(d, .02) * .6
    return norm(x) * v
def clang(): return norm(M(steel(470, 1.6, 1, .45), np.pad(steel(470, .8, .5, .2), (int(.09 * SR), 0))))
def jingle():                                    # the collar tag
    x = np.zeros(int(.4 * SR))
    for k, o in enumerate([0, .05, .11]):
        s = steel(2600 + 340 * k, .25, .6, .05); i = int(o * SR); x[i:i + len(s)] += s[:len(x) - i]
    return norm(x)
def cardboard_thump(p=0):
    d = .35; tt = t_(d)
    return norm(M(sine(95 * 2 ** (p / 12) * (1 - .35 * tt), d) * env_exp(d, .06), lp(nz(d), 900) * env_exp(d, .03) * .8, bp(nz(d), 1500, 4000) * env_exp(d, .01) * .3))
def fall(d=.3): return norm(bp(nz(d), 600, 3000) * np.linspace(.2, 1, len(t_(d))) ** 2)
def paper_swish(d=.3): return norm(bp(nz(d), 1800, 8000)) * np.sin(np.pi * t_(d) / d) ** 2
def pen_write(d=.5): x = bp(nz(d), 2000, 7000) * (0.5 + .5 * np.abs(np.sin(2 * np.pi * 11 * t_(d)))); return norm(x) * np.sin(np.pi * t_(d) / d)
def stamp():
    d = .3; tt = t_(d)
    return norm(sine(140 * (1 - .4 * tt), d) * env_exp(d, .035) + lp(nz(d), 1800) * env_exp(d, .012) * .9)
def iris(d=.5): tt = t_(d); return norm(bp(nz(d), 1000, 6000) * np.linspace(1, .2, len(tt))) * np.sin(np.pi * tt / d)
def boing(d=.45):                                # cartoon jump: a rising jaw-harp twang
    tt = t_(d); f = 180 + 260 * (tt / d) ** .7; f = f * (1 + .06 * np.sin(2 * np.pi * 22 * tt))
    return norm(sine(f, d) + .3 * sine(2 * f, d)) * env_ad(d, .01, .25)
def spring(d=.8):                                # the scale's spring taking the weight: a wobbly low "boyoyoing"
    tt = t_(d); f = 120 * (1 + .25 * np.sin(2 * np.pi * 16 * tt) * np.exp(-tt / .3))
    return norm(sine(f, d) + .4 * sine(2.7 * f, d) * env_exp(d, .1)) * env_ad(d, .005, .3)
def land(): return norm(M(lp(nz(.2), 500) * env_exp(.2, .03), thump(.6, 75)[:int(.2 * SR)] * .7))
def wobble(d=1.5):                               # needle swinging: a slide whistle that settles
    tt = t_(d); f = 1050 + 380 * np.sin(2 * np.pi * 2.6 * tt) * np.exp(-tt / .6)
    return norm(sine(f, d)) * env_ad(d, .03, .7) * .8
def scoop(d=.5):                                 # a cup pushed into dry flakes
    tt = t_(d); grit = (rng.random(len(tt)) > .93) * rng.standard_normal(len(tt))
    return norm(bp(grit, 1500, 7000) * 1.5 + bp(nz(d), 400, 2500) * .25) * np.sin(np.pi * tt / d) ** .8
def tap(): return norm(sine(1850, .12) * env_exp(.12, .03) + sine(3420, .12) * env_exp(.12, .015) * .5 + hp(nz(.12), 3000) * env_exp(.12, .003))
def flick(): return norm(M(clack(1.5, 1)[:int(.08 * SR)], paper_swish(.18) * .5))
def patter(d=.6):                                # a few flakes landing on the counter
    x = np.zeros(int(d * SR))
    for k in range(9):
        o = int(rng.uniform(0, d - .05) * SR); c = hp(nz(.03), 2000) * env_exp(.03, .004); x[o:o + len(c)] += c * rng.uniform(.4, 1)
    return norm(x)
def pour(d=1.4):                                 # flakes rattling into a steel bowl
    tt = t_(d); grit = (rng.random(len(tt)) > .88) * rng.standard_normal(len(tt))
    x = bp(grit, 2000, 8000) * 1.2 + bp(nz(d), 600, 2200) * .15
    ring = sum(sine(f, d) * .02 for f in (1100, 2550, 4700))
    return norm(x + ring * (grit != 0).cumsum() / max(1, (grit != 0).sum())) * np.minimum(1, tt / .08) * np.minimum(1, (d - tt) / .25)
def sprinkle(d=1.3):                             # warm water drops: little "plip"s
    x = np.zeros(int(d * SR))
    for k in range(16):
        o = int(rng.uniform(0, d - .1) * SR); dd = .07; f = rng.uniform(900, 1700)
        p = sine(f * (1 + 1.2 * t_(dd) / dd), dd) * env_exp(dd, .015); x[o:o + len(p)] += p * rng.uniform(.4, 1)
    return norm(x)
def hiss(d=2.0): tt = t_(d); return norm(bp(nz(d), 3500, 9000)) * np.sin(np.pi * tt / d) * .5
def mash():                                      # a fork pressing wet food
    d = .28; tt = t_(d)
    return norm(bp(nz(d), 180, 900) * env_ad(d, .02, .08) + sine(220 * (1 - .4 * tt / d), d) * env_exp(d, .05) * .3)
def clank():                                     # THE bowl on the floor after the silence
    return norm(M(steel(610, 1.8, 1, .5), thump(.8, 90)[:int(.3 * SR)] * .5))
def munch(d=1.7):                                # happy crunching, ~6 bites a second
    x = np.zeros(int(d * SR))
    for k in range(int(d * 6)):
        o = int((k / 6 + rng.uniform(-.02, .02)) * SR); c = bp(nz(.09), 900, 5000) * env_ad(.09, .002, .025)
        if o + len(c) < len(x): x[o:o + len(c)] += c * rng.uniform(.6, 1)
    return norm(x)
def thumps(d=1.6):                               # tail thumping the floor
    x = np.zeros(int(d * SR))
    for k in range(int(d * 4.5)):
        o = int(k / 4.5 * SR); c = thump(.7, 70)[:int(.15 * SR)]
        if o + len(c) < len(x): x[o:o + len(c)] += c
    return norm(x)
def slide(d=.5):                                 # slide whistle down: "less"
    f = np.linspace(1500, 700, len(t_(d))); return norm(sine(f * (1 + .01 * np.sin(2 * np.pi * 6 * t_(d))), d)) * np.sin(np.pi * t_(d) / d) ** .6
def tink(): return norm(steel(3200, .5, 1, .12))
def wood_tick(): return norm(clack(1.1, 1)[:int(.1 * SR)])

fx = np.zeros((N, 2)); vo = np.zeros((N, 2)); amb = np.zeros((N, 2))
for e in EV:
    t, ty, g = e['t'], e['type'], e.get('g', 1.0)
    if ty in ('vo', 'sub', 'room', 'silence', 'sparkle'): continue
    if ty == 'jingle': add(fx, jingle(), t, .18 * g, -.2)
    elif ty == 'clang': add(fx, clang(), t, .6 * g, -.35)
    elif ty == 'clink': add(fx, steel(560, .5, 1, .12), t, .5 * g, -.35)
    elif ty == 'fall': add(fx, fall(.3), t, .25 * g, .35)
    elif ty == 'thump': add(fx, cardboard_thump(), t, .8 * g, .3)
    elif ty == 'swish': add(fx, paper_swish(.3), t, .35 * g)
    elif ty == 'pen': add(fx, pen_write(e.get('d', .5)), t, .18 * g, -.2)
    elif ty == 'pop': add(fx, pop(1), t, .3 * g, .2)
    elif ty == 'stamp': add(fx, stamp(), t, .7 * g, [-.4, 0, .4][int(round((t - 6.0) / .5)) % 3])
    elif ty == 'iris': add(fx, iris(.5), t, .25 * g)
    elif ty == 'creak': add(fx, creak(1), t, .12 * g, .3)
    elif ty == 'boing': add(fx, boing(), t, .3 * g, 0)
    elif ty == 'land': add(fx, land(), t, .6 * g, -.2)
    elif ty == 'spring': add(fx, spring(), t, .35 * g, -.2)
    elif ty == 'wobble': add(fx, wobble(e.get('d', 1.5)), t, .1 * g, .3)
    elif ty == 'ding': add(fx, ding(1), t, .2 * g, .3)
    elif ty == 'whoosh': add(fx, whoosh(.35, 1), t, .3 * g, .3)
    elif ty == 'scoop': add(fx, scoop(.5), t, .45 * g, -.2)
    elif ty == 'rustle': add(fx, scoop(.3), t, .3 * g, 0)
    elif ty == 'tap': add(fx, tap(), t, .3 * g, .1)
    elif ty == 'flick': add(fx, flick(), t, .5 * g, .2)
    elif ty == 'patter': add(fx, patter(.6), t, .3 * g, .35)
    elif ty == 'pour': add(fx, pour(e.get('d', 1.4)), t, .55 * g, .2)
    elif ty == 'sprinkle': add(fx, sprinkle(e.get('d', 1.3)), t, .35 * g, .2)
    elif ty == 'hiss': add(fx, hiss(e.get('d', 2.0)), t, .06 * g, .2)
    elif ty == 'mash': add(fx, mash(), t, .55 * g, .2)
    elif ty == 'clank': add(fx, clank(), t, .95 * g, .25)
    elif ty == 'munch': add(fx, munch(e.get('d', 1.7)), t, .4 * g, .15)
    elif ty == 'thumps': add(fx, thumps(e.get('d', 1.6)), t, .3 * g, -.4)
    elif ty == 'slide': add(fx, slide(e.get('d', .5)), t, .18 * g, .1)
    elif ty == 'swing': add(fx, paper_swish(.4), t, .25 * g, 0)
    elif ty == 'tink': add(fx, tink(), t, .2 * g, .35)

# ---------------- narration ----------------
voice_env = np.zeros(N)
for e in EV:
    if e['type'] != 'vo': continue
    y, sr = sf.read(os.path.join(D, 'voices', e['id'] + '.wav'))
    if y.ndim > 1: y = y.mean(1)
    assert sr == SR, (sr, SR)
    y = compress(norm(y, .9), thr=.3, ratio=3.0)
    add(vo, y, e['t'], .85, 0)
    s = int(e['t'] * SR); voice_env[s:s + len(y)] = 1

# ---------------- ambience: warm room tone + a quiet mantel clock on the beat ----------------
room = lp(brown(DUR), 900) * .018
amb += np.stack([room, np.roll(room, 311)], 1)
for k in range(int(DUR)): add(amb, wood_tick(), float(k), .025, -.6)

# ---------------- music + ducking ----------------
mus, msr = sf.read(os.path.join(D, 'music', 'score.wav')); assert msr == SR
mus = mus[:N] if len(mus) >= N else np.pad(mus, ((0, N - len(mus)), (0, 0)))
k = int(.12 * SR); sm = np.convolve(voice_env, np.ones(k) / k, 'same')
mus = mus * (1 - sm * (1 - 10 ** (-8 / 20)))[:, None]

# ---------------- silences ----------------
def gate(buf, a, b, keep=0.0, fade=.03):
    s, e = int(a * SR), int(b * SR); f = int(fade * SR)
    m = np.ones(N); m[s:e] = keep
    m[max(0, s - f):s] = np.linspace(1, keep, min(f, s)); m[e:e + f] = np.linspace(keep, 1, len(m[e:e + f]))
    buf *= m[:, None]
gate(amb, 32.0, 33.58); gate(fx, 32.0, 33.58)      # total silence; the clank at 33.6 is the first sound after it

mix = mus * .55 + fx * .9 + vo + amb
mix = limit(mix, .95)
os.makedirs(os.path.join(D, 'out'), exist_ok=True)
sf.write(os.path.join(D, 'out', 'mix.wav'), mix.astype(np.float32), SR)
r = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
print('mix.wav', mix.shape, 'peak', round(float(np.abs(mix).max()), 3), '| rms vo', round(r(vo[voice_env > 0]), 1), 'music', round(r(mus * .55), 1), 'fx', round(r(fx * .9), 1))

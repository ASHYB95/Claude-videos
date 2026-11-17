# Original score for "Class Rep" — light, slightly awkward pizzicato comedy cue with a Christmas lift. Pure synthesis, no samples.
# Oom-pah pizzicato under the set-up; a "womp" stop on "Zero fivers"; busier, tenser groove through the chasing;
# a dead stop before "so guess who's topping it up"; then celesta + sleigh bells + warm strings from "Next year?" to the end card.
import numpy as np, os, json
from scipy.signal import butter, sosfilt, fftconvolve
import scipy.io.wavfile as wf
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
cues = json.load(open(os.path.join(root, 'voices', 'cues.json'))); seg = cues['seg']
def word(k, w):
    return [x for x in cues['words'][k] if x[0].strip('",.?!').lower() == w][0][1]
SR = 44100; DUR = cues['dur']; N = int(SR * (DUR + 0.5))
BPM = 112; BEAT = 60 / BPM
ZERO = word('j3', 'zero'); B0 = seg['j4'][0] - .15; SHORT = word('j6a', 'forty') - .2; STOP = seg['j6a'][1] + .02   # groove stops as 'short.' ends
TURN = seg['j7a'][0] - .15
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def st(x, t, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(x))
    if j <= i or i < 0: return
    L[i:j] += x[:j - i] * g * (1 - max(0, pan)); R[i:j] += x[:j - i] * g * (1 + min(0, pan))

def pizz(m, vel=1.0, d=0.6):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m); x = np.zeros(n)
    for k, a in enumerate([1, .55, .35, .22, .12, .07]):
        x += a * np.sin(2 * np.pi * f * (k + 1) * t + rng.uniform(0, 6)) * np.exp(-t * (7 + 5 * k) * (0.7 + f / 700))
    x += 0.08 * rng.standard_normal(n) * np.exp(-t * 300)          # finger snap
    a = int(.002 * SR); x[:a] *= np.linspace(0, 1, a)
    return lp(x, 3200) * vel
def bassoon(m, d=0.32, vel=1.0, glide=0.0, vib=0.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = hz(m) * 2 ** (glide * t / d / 12) * (1 + vib * np.sin(2 * np.pi * 5.5 * t))
    ph = np.cumsum(f) / SR; x = 0.6 * (2 * (ph % 1) - 1) + 0.4 * np.sign(np.sin(2 * np.pi * ph))
    x = lp(x, 900, 3); e = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.06)
    return x * e * vel
def celesta(m, vel=1.0, d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    idx = 2.2 * np.exp(-t * 6)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 4 * t)) * np.exp(-t * 2.6)
    x += 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 5)
    a = int(.002 * SR); x[:a] *= np.linspace(0, 1, a); return x * vel
def bells(vel=1.0):
    n = int(.22 * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for _ in range(4):
        o = int(rng.uniform(0, .025) * SR); f = rng.uniform(5200, 9800)
        x[o:] += np.sin(2 * np.pi * f * t[:n - o]) * np.exp(-t[:n - o] * 38)
    x += bp(rng.standard_normal(n), 6000, 12000) * np.exp(-t * 30) * .6
    return x * vel * .5
def strings(notes, d, bright=2000):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in notes:
        for det in (-0.004, 0.0, 0.0045):
            vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * t + rng.uniform(0, 6)); ph = np.cumsum(hz(m) * (1 + det) * vib) / SR
            x += 2 * (ph % 1) - 1
    x = lp(x / (3 * len(notes)), bright); e = np.minimum(1, t / 0.7) * np.minimum(1, (d - t) / 0.6); return x * e

CH = {'C': [48, 55, 60, 64, 67], 'Am': [45, 52, 57, 60, 64], 'F': [41, 53, 57, 60, 65], 'G': [43, 50, 55, 59, 62], 'Dm': [50, 53, 57, 62, 65],
      'Em': [40, 52, 55, 59, 64], 'A7': [45, 52, 55, 61, 64], 'E7': [40, 52, 56, 59, 62], 'C7': [48, 55, 58, 64, 67], 'D7': [50, 54, 57, 60, 66],
      'G7': [43, 53, 55, 59, 62], 'Fm': [41, 53, 56, 60, 65], 'Ab': [44, 51, 56, 60, 63], 'Dm7': [50, 53, 57, 60, 65]}
def oompah(t0, t1, prog, busy=False, mel=None):
    k = 0; t = t0
    while t < t1 - 0.05:
        ch = CH[prog[k % len(prog)]]
        for b in range(2):                       # two beats per chord: "oom" on 1, "pah" on 2
            tb = t + b * BEAT
            if tb >= t1 - 0.05: break
            if b == 0: st(bassoon(ch[0] - 12 if ch[0] > 45 else ch[0], .3, .9), tb, .22)
            else: [st(pizz(m, .7, .35), tb + i * .006, .13, -.3 + .3 * i) for i, m in enumerate(ch[2:5])]
            if busy:                              # off-beat 8th pizz ostinato for tension
                st(pizz(ch[3] + 12, .5, .3), tb + BEAT / 2, .09, .35)
        if mel and k < len(mel) and mel[k] is not None:   # little staccato melody
            for j, m in enumerate(mel[k]): st(pizz(m, .9, .45), t + j * BEAT / 2, .16, .15)
        k += 1; t += 2 * BEAT
# A: set-up + replies
MEL_A = [[72, 74, 76], None, [77, 76, 74], None, [72, 74, 76], [79], [77, 76, 74, 71], None, [72, 74, 76], None, [77, 79], None, [81, 79, 77, 76], [74]]
REPLIES = seg['q1'][0] - .3
oompah(0.0, REPLIES, ['C', 'Am', 'F', 'G'], mel=MEL_A)
oompah(REPLIES, ZERO - .08, ['Dm', 'G', 'Em', 'A7', 'Dm', 'G'], mel=[[74, 77], None, [76, 79], None, [74, 77], [79, 77, 76, 74], [72], None])
# the "womp": a deflating bassoon on "Zero fivers"
for i, (m, d) in enumerate([(55, .26), (54, .26), (53, .26), (52, .8)]):
    st(bassoon(m, d, 1.0, glide=(-.6 if i == 3 else 0), vib=(.012 if i == 3 else 0)), ZERO + .05 + i * .27, .3)
# B: three weeks of chasing — busier, then minor on "forty quid short", dead stop before the punchline
oompah(B0, SHORT, ['C', 'E7', 'Am', 'C7', 'F', 'D7', 'G', 'G7'], busy=True, mel=[None, [76, 77, 76], None, [79, 78, 79], None, [81, 80, 81], [83, 84], None])
oompah(SHORT, STOP, ['Fm', 'Ab', 'Fm', 'G7'], busy=True)
st(pizz(43, 1, .5), STOP, .22); st(pizz(36, 1, .7), STOP + .17, .2)          # plink-plonk, then silence for the punchline
# turn: harp-like celesta glissando up into "Next year?"
for i, m in enumerate([60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 79, 84]): st(celesta(m, .7, 1.0), TURN - .55 + i * .045, .09, -.4 + i * .07)
# C: warm Christmas lift to the end card
PC = [('F', 2), ('G', 2), ('Em', 2), ('Am', 2), ('Dm7', 2), ('G', 2), ('C', 2), ('F', 1), ('G', 1), ('C', 6)]
t = TURN
for name, beats in PC:
    ch = CH[name]; d = beats * BEAT
    st(strings([m + 12 for m in ch[1:4]], d + .6, 1900), t - .1, .10, -.15)
    st(strings([ch[0]], d + .6, 700), t - .1, .09, .15)
    st(bassoon(ch[0] - 12 if ch[0] > 45 else ch[0], min(d, 1.0) * .9, .7), t, .14)
    ARP = [ch[2] + 12, ch[3] + 12, ch[4] + 12, ch[3] + 24]
    for j in range(int(beats * 2)):
        if name == 'C' and beats == 6 and j > 3: break
        st(celesta(ARP[j % 4], .75, 1.4), t + j * BEAT / 2, .085, .25 if j % 2 else -.25)
    t += d
END_C = t - 6 * BEAT
st(celesta(84, .9, 2.5), END_C, .11); st(celesta(79, .8, 2.5), END_C + .02, .08)
# sleigh bells through the lift (8ths, accented on the beat)
tb = TURN
while tb < DUR - .3:
    k = round((tb - TURN) / (BEAT / 2)); st(bells(1.0 if k % 2 == 0 else .55), tb, .10, .3); tb += BEAT / 2
# reverb (small room / hall blend)
ir_n = int(1.8 * SR); tt = np.arange(ir_n) / SR
irL = lp(rng.standard_normal(ir_n) * np.exp(-tt * 3.5), 6000); irR = lp(rng.standard_normal(ir_n) * np.exp(-tt * 3.5), 6000)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
oL = L * .85 + fftconvolve(L, irL)[:N] * .3; oR = R * .85 + fftconvolve(R, irR)[:N] * .3
out = np.stack([oL, oR], 1)[:int(DUR * SR)]
fs = int((DUR - .6) * SR); out[fs:] *= np.linspace(1, 0, len(out) - fs)[:, None] ** 1.5
out /= np.max(np.abs(out)) / 0.89
wf.write(os.path.join(here, 'music.wav'), SR, (out * 32767).astype(np.int16))
print('music.wav', round(DUR, 2), 'zero', round(ZERO, 2), 'stop', round(STOP, 2), 'turn', round(TURN, 2))

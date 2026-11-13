#!/usr/bin/env python3
"""Mix: speaker voice + lo-fi bed (ducked under speech, lifted for the end card) + sparse SFX cues
-> stereo WAV at -14 LUFS / -1 dBTP (Instagram).

Usage:
  python3 mix.py --voice work/voice.wav --music audio/music.wav --sfx audio --cues cues.json \
                 --dur 86.7 --lift 84.55 --out audio/mix.wav [--trim -6] [--music-db -15] [--duck-db -8]

cues.json: [["swish", 3.78, -12], ["tear", 16.55, -10], ["tick", 1.92, -16, 1.3], ...]
           = [sfx name (audio/sfx_<name>.mp3), time s, gain dB, optional max length s]
Every SFX file is first normalised to the same RMS, so gains are comparable across files.
--trim is added to every cue (the client asked for "50 % quieter" -> -6 dB; that's the default).
Keep it sparse: ~1 cue per 2-3 s at most (see cues_example.json, the approved reference list).
"""
import json, os, subprocess, sys
import numpy as np

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
SR = 48000
DUR = float(arg('--dur', 60)); N = int(SR * DUR)
VOICE, MUSIC, SFXD = arg('--voice', 'work/voice.wav'), arg('--music', 'audio/music.wav'), arg('--sfx', 'audio')
CUES, OUT = arg('--cues', 'cues.json'), arg('--out', 'audio/mix.wav')
TRIM, LIFT = float(arg('--trim', -6)), float(arg('--lift', DUR - 2.1))
MUSIC_DB, DUCK_DB = float(arg('--music-db', -15)), float(arg('--duck-db', -8))

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
place(vo, load(VOICE), 0.0)

# music: ducked while the speaker talks, lifted for the end card
mus = load(MUSIC)[:N]; mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
env = np.convolve(np.abs(vo).max(1), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
act = np.convolve((env > 0.012).astype(float), np.ones(int(0.35 * SR)) / int(0.35 * SR), 'same') > 0.05
gain = np.where(act, db(DUCK_DB), 1.0)
gain = np.where(np.arange(N) / SR > LIFT, db(4), gain)
k = int(0.3 * SR); gain = np.convolve(gain, np.ones(k) / k, 'same')
out += mus * gain[:, None] * db(MUSIC_DB)

# sfx
cues = json.load(open(CUES)) if os.path.exists(CUES) else []
cache = {}
for c in cues:
    n, t, g = c[0], float(c[1]), float(c[2]); ml = c[3] if len(c) > 3 else None
    if n not in cache:
        x = load(os.path.join(SFXD, f'sfx_{n}.mp3')); nz = x[np.abs(x).max(1) > 1e-3]
        cache[n] = x * (db(-20) / max(np.sqrt((nz ** 2).mean()) if len(nz) else 1, 1e-6))
    place(out, cache[n], t, db(g + TRIM), ml)

out += vo
fo = int(0.7 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
tmp = OUT + '.f32'; out.astype(np.float32).tofile(tmp)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', tmp,
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', str(SR), OUT], check=True)
os.remove(tmp); print(OUT, len(cues), 'cues')

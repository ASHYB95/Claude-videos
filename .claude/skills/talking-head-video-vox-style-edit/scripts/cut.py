#!/usr/bin/env python3
"""Tighten the talking-head takes into one A-roll.

Usage: python3 cut.py <project_dir> [--dry]

Reads footage/*.mp4 + work/audio/*.json (ElevenLabs Scribe word timings),
removes leading/trailing silence and shortens every pause longer than GAP_MAX
to KEEP_GAP. Writes:
  work/aroll.mp4     1080x1920 30fps H.264, voice audio (cleaned)
  work/voice.wav     the same voice track on its own (for the mix)
  edl.json           segments + per-segment output times
  transcript.json    word timings re-mapped onto the A-roll timeline
"""
import json, glob, os, subprocess, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else '.')  # project dir
GAP_MAX = 0.32   # pauses longer than this get shortened
KEEP_GAP = 0.20  # ...to this (split as pad after / pad before)
PAD = KEEP_GAP / 2
HEAD, TAIL = 0.06, 0.16  # breath between takes = HEAD + TAIL

clips = sorted(glob.glob(os.path.join(ROOT, 'footage', '*.mp4')))
if not clips: sys.exit(f'no takes in {ROOT}/footage (put the raw .mp4 takes there; keep them out of git)')
segs, words_out = [], []
t_out = 0.0
for ci, path in enumerate(clips):
    b = os.path.splitext(os.path.basename(path))[0]
    d = json.load(open(os.path.join(ROOT, 'work', 'audio', b + '.json')))
    ws = [w for w in d['words'] if w['type'] == 'word']
    # group words into runs separated by long pauses
    runs, cur = [], [ws[0]]
    for w in ws[1:]:
        if w['start'] - cur[-1]['end'] > GAP_MAX:
            runs.append(cur); cur = [w]
        else:
            cur.append(w)
    runs.append(cur)
    for ri, run in enumerate(runs):
        first, last = ri == 0, ri == len(runs) - 1
        a = run[0]['start'] - (HEAD if first else PAD)
        z = run[-1]['end'] + (TAIL if last else PAD)
        a = max(a, 0.0)
        a = round(a * 30) / 30; z = a + round((z - a) * 30) / 30
        seg = dict(clip=b, src_in=round(a, 3), src_out=round(z, 3), out_in=round(t_out, 3),
                   new_take=first, text=' '.join(w['text'] for w in run))
        for w in run:
            words_out.append(dict(text=w['text'], start=round(t_out + w['start'] - a, 3),
                                  end=round(t_out + w['end'] - a, 3), seg=len(segs)))
        t_out += z - a
        seg['out_out'] = round(t_out, 3)
        segs.append(seg)

total = segs[-1]['out_out']
json.dump(dict(fps=30, duration=round(total, 3), segments=segs), open(os.path.join(ROOT, 'edl.json'), 'w'), indent=1)
json.dump(words_out, open(os.path.join(ROOT, 'transcript.json'), 'w'), indent=0)
print(f'{len(segs)} segments, {total:.2f}s (from {sum(json.load(open(os.path.join(ROOT,"work","audio",os.path.basename(c)[:-4]+".json")))["words"][-1]["end"] for c in clips):.1f}s of speech span)')

if '--dry' in sys.argv:
    sys.exit()

# ---- render: one small ffmpeg per segment, then concat ----
W = os.path.join(ROOT, 'work', 'segs'); os.makedirs(W, exist_ok=True)
F = 0.012  # 12 ms audio fades at every cut, no clicks
lst_v, lst_a = [], []
for k, s in enumerate(segs):
    src = os.path.join(ROOT, 'footage', s['clip'] + '.mp4')
    dur = round(s['src_out'] - s['src_in'], 4)
    v, au = os.path.join(W, f'v{k:02d}.mp4'), os.path.join(W, f'a{k:02d}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-threads', '4', '-ss', str(s['src_in']), '-i', src, '-t', str(dur),
                    '-vf', 'fps=30,scale=1080:1920:flags=lanczos,setsar=1', '-an', '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '30', v], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s['src_in']), '-i', src, '-t', str(dur), '-vn',
                    '-af', f'aresample=48000,apad,atrim=0:{dur},afade=t=in:d={F},afade=t=out:st={dur - F:.4f}:d={F}',
                    '-ac', '1', '-c:a', 'pcm_s16le', au], check=True)
    lst_v.append(f"file '{v}'"); lst_a.append(f"file '{au}'")
    print(f'  seg {k:02d} {dur:.2f}s', flush=True)
open(os.path.join(W, 'v.txt'), 'w').write('\n'.join(lst_v))
open(os.path.join(W, 'a.txt'), 'w').write('\n'.join(lst_a))
raw = os.path.join(W, 'voice_raw.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(W, 'a.txt'), '-c', 'pcm_s16le', raw], check=True)
# light voice clean-up: rumble cut, gentle denoise, presence, even dynamics
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af',
                'highpass=f=85,afftdn=nf=-28,equalizer=f=3200:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2',
                '-ar', '48000', os.path.join(ROOT, 'work', 'voice.wav')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(W, 'v.txt'),
                '-i', os.path.join(ROOT, 'work', 'voice.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', os.path.join(ROOT, 'work', 'aroll.mp4')], check=True)
# the composition uses this one: last frame held 2.3 s (the PiP shrinks away over the end card),
# keyframe every second so HyperFrames seeks fast
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ROOT, 'work', 'aroll.mp4'),
                '-vf', 'tpad=stop_mode=clone:stop_duration=2.3', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17',
                '-g', '30', '-keyint_min', '30', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart',
                os.path.join(ROOT, 'work', 'aroll_hold.mp4')], check=True)
# keep only what the render needs inside the project (HyperFrames copies the whole folder into its render plan)
import shutil
shutil.rmtree(W, ignore_errors=True); os.remove(os.path.join(ROOT, 'work', 'aroll.mp4'))
print('wrote work/aroll_hold.mp4, work/voice.wav')

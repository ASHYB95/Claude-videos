# Places the VO takes on the timeline -> audio/vo.wav (39 s, 48 kHz stereo).
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__)); v = os.path.join(here, '..', 'voices')
START = {1: 0.35, 2: 2.72, 3: 8.00, 4: 12.04, 5: 16.49, 6: 22.52, 7: 28.66, 8: 34.45}
DUR = 39.0
args, f = ['ffmpeg', '-y', '-loglevel', 'error'], []
for i, t in START.items():
    args += ['-i', os.path.join(v, f'v{i}.mp3')]
    f.append(f'[{i-1}:a]aresample=48000,adelay={int(t*1000)}|{int(t*1000)}[a{i}]')
f.append(''.join(f'[a{i}]' for i in START) + f'amix=inputs={len(START)}:normalize=0,apad=whole_dur={DUR},atrim=0:{DUR}[out]')
args += ['-filter_complex', ';'.join(f), '-map', '[out]', '-ac', '2', '-ar', '48000', os.path.join(here, 'vo.wav')]
subprocess.run(args, check=True); print('vo.wav ok')

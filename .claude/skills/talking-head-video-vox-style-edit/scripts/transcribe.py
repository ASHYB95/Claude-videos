#!/usr/bin/env python3
"""Transcribe every take in <project>/footage with ElevenLabs Scribe (word timestamps).

Usage: python3 transcribe.py <project_dir>
Writes <project>/work/audio/<take>.mp3 (16 kHz mono) and <take>.json, prints each take's text
and any pause > 0.3 s (useful for spotting fumbles before cutting).
The ElevenLabs key is injected by the session proxy; the header value here is a placeholder.
"""
import glob, json, os, subprocess, sys, urllib.request, uuid

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
out = os.path.join(root, 'work', 'audio'); os.makedirs(out, exist_ok=True)
takes = sorted(glob.glob(os.path.join(root, 'footage', '*.mp4')) + glob.glob(os.path.join(root, 'footage', '*.mov')))
if not takes: sys.exit('no takes in footage/')

def scribe(path):
    b = uuid.uuid4().hex
    parts = []
    for k, v in [('model_id', 'scribe_v1'), ('timestamps_granularity', 'word'), ('tag_audio_events', 'true'), ('diarize', 'false')]:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(path)}"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
                 + open(path, 'rb').read() + b'\r\n')
    body = b''.join(parts) + f'--{b}--\r\n'.encode()
    req = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text', data=body,
                                 headers={'Content-Type': f'multipart/form-data; boundary={b}', 'xi-api-key': 'proxy-injected'})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())

for t in takes:
    name = os.path.splitext(os.path.basename(t))[0]
    mp3, js = os.path.join(out, name + '.mp3'), os.path.join(out, name + '.json')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', t, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '64k', mp3], check=True)
    if not os.path.exists(js):
        json.dump(scribe(mp3), open(js, 'w'))
    d = json.load(open(js)); ws = [w for w in d['words'] if w['type'] == 'word']
    line, prev = '', None
    for w in ws:
        if prev is not None and w['start'] - prev > 0.3: line += f' [{w["start"] - prev:.2f}s] '
        line += w['text'] + ' '; prev = w['end']
    print(f'== {name}  ({ws[0]["start"]:.2f}–{ws[-1]["end"]:.2f}s)\n{line}\n')

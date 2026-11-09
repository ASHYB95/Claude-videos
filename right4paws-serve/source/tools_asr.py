"""Check every voice line with ElevenLabs speech-to-text (word for word); writes voices/words.json with word timings.
usage: python3 tools_asr.py [id ...]"""
import json, subprocess, sys, re
lines = json.load(open('lines.json')); ids = sys.argv[1:] or [l['id'] for l in lines]
norm = lambda s: re.sub(r"[^a-z0-9' ]", ' ', s.lower().replace('-', ' ')).split()
words = json.load(open('voices/words.json')) if ids != [l['id'] for l in lines] and __import__('os').path.exists('voices/words.json') else {}
bad = 0
for l in lines:
    if l['id'] not in ids: continue
    out = subprocess.run(['curl', '-sS', '-X', 'POST', 'https://api.elevenlabs.io/v1/speech-to-text', '-H', 'xi-api-key: dummy',
                          '-F', 'model_id=scribe_v1', '-F', 'language_code=en', '-F', f"file=@voices/{l['id']}.wav"], capture_output=True, text=True).stdout
    d = json.loads(out)
    if 'text' not in d: print('✗', l['id'], out[:200]); bad += 1; continue
    heard, want = norm(d['text']), norm(l.get('asr', l['text']))
    ok = heard == want
    words[l['id']] = [{'w': w['text'], 't0': w['start'], 't1': w['end']} for w in d.get('words', []) if w.get('type') == 'word']
    print('✓' if ok else '✗', l['id'], '|', d['text'])
    bad += not ok
json.dump(words, open('voices/words.json', 'w'), indent=0)
sys.exit(1 if bad else 0)

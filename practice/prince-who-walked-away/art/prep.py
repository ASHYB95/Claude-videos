# Prep cut-outs: trim to alpha, downscale, duotone to charcoal -> cream (gold accents kept with --keep-yellow).
# Run from art/:  python3 -I prep.py   (reads cut/<name>_rb.png, writes ../assets/<name>.png)
import cv2, numpy as np, subprocess, os, sys
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
def trim_resize(i, m=1100):
    ys, xs = np.where(i[..., 3] > 10); i = i[max(0, ys.min()-4):ys.max()+5, max(0, xs.min()-4):xs.max()+5]
    h, w = i.shape[:2]; s = min(1, m / max(h, w))
    return cv2.resize(i, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA) if s < 1 else i
# name: (keep gold accent, max size)
J = {'prince': (1, 1100), 'king': (0, 900), 'palace': (0, 1100), 'himalaya': (0, 1100), 'oldman': (0, 800), 'sick': (0, 900),
     'funeral': (0, 900), 'channa': (0, 1100), 'wife': (0, 1000), 'horse': (0, 1000), 'sujata': (1, 1100), 'tree': (0, 1100),
     'ascetic': (0, 1100), 'meditate': (0, 1100), 'face': (0, 1100), 'buddha': (1, 1100)}
# rectangular photo-print clippings: the remover sometimes eats sky/pale areas inside the print -> refill inside the outline
FILL = {'palace', 'himalaya', 'tree', 'king', 'wife', 'horse', 'channa', 'funeral'}
def fill_holes(i):
    a = i[..., 3]; m = (a > 12).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max(cs, key=cv2.contourArea); f = np.zeros_like(m); cv2.drawContours(f, [big], -1, 255, -1)
    f = cv2.erode(f, np.ones((7, 7), np.uint8)); f = cv2.GaussianBlur(f, (5, 5), 0)
    i = i.copy(); i[..., 3] = np.maximum(a, f); return i
only = sys.argv[1:]
tmp = os.path.join(here, '_t.png')
for name, (ky, m) in J.items():
    if only and name not in only: continue
    src = f'cut/{name}_rb.png'
    if not os.path.exists(src): print('missing', name); continue
    i = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if name in FILL: i = fill_holes(i)
    cv2.imwrite(tmp, trim_resize(i, m))
    subprocess.run(['python3', '-I', 'duotone.py', tmp, f'../assets/{name}.png'] + (['--keep-yellow'] if ky else []), check=True, capture_output=True)
    print(name)
os.remove(tmp)

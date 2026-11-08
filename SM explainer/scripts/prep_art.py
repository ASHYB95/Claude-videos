#!/usr/bin/env python3
"""Split background-removed art sheets (art/rb/sN.png) into single cut-outs, trim, downscale
and duotone them into Purple Seed ink/paper (accents snapped to brand yellow where asked).
Writes assets/<name>.png. Usage: python3 scripts/prep_art.py  (names mapped below)."""
import cv2, numpy as np, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A, RB = os.path.join(ROOT, 'assets'), os.path.join(ROOT, 'art', 'rb')
DUO = os.path.join(ROOT, 'scripts', 'duotone.py')

def trim_resize(i, m=1100):
    ys, xs = np.where(i[..., 3] > 10)
    i = i[max(0, ys.min() - 4):ys.max() + 5, max(0, xs.min() - 4):xs.max() + 5]
    h, w = i.shape[:2]; s = min(1, m / max(h, w))
    return cv2.resize(i, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA) if s < 1 else i

def split(i, minarea=30000):
    a = (i[..., 3] > 40).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(a)
    ks = [k for k in range(1, n) if st[k][4] > minarea]
    ks.sort(key=lambda k: (st[k][1] + st[k][3] / 2) // (i.shape[0] / 3) * 10000 + st[k][0])  # rows, then x
    out = []
    for k in ks:
        m = cv2.dilate((lab == k).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
        p = i.copy(); p[..., 3] = np.minimum(p[..., 3], m); out.append(p)
    return out

def duo(img, name, extra=()):
    tmp = os.path.join(ROOT, 'art', '_t.png'); cv2.imwrite(tmp, img)
    subprocess.run([sys.executable, '-I', DUO, tmp, os.path.join(A, name + '.png'), *extra], check=True, capture_output=True)
    os.remove(tmp)

# sheet -> names in reading order (rows top->bottom, then left->right); None = skip
NAMES = {
    's0': ['bulb', 'magnifier', 'book', 'pouch'],
    's1': None,  # filled in after inspecting the split
    's2': ['hand_plug', 'hand_phone'],
    's3': ['tv', 'masks'],
    's4': ['face_smile', 'face_cry', 'face_laugh'],
    's5': ['face_empathy', 'face_sympathy', 'hob', 'hony'],
    's6': ['crowd'],
}
YEL = {'hand_phone', 'tv'}
if __name__ == '__main__':
    only = sys.argv[1:] or list(NAMES)
    for sh in only:
        src = os.path.join(RB, sh + '.png')
        if not os.path.exists(src): print('missing', src); continue
        parts = split(cv2.imread(src, cv2.IMREAD_UNCHANGED))
        names = NAMES.get(sh) or [f'{sh}_{k}' for k in range(len(parts))]
        print(sh, len(parts), 'parts ->', names)
        for p, nm in zip(parts, names):
            if nm: duo(trim_resize(p, 1100 if nm in ('crowd', 'hand_phone', 'hand_plug', 'tv') else 800), nm, ['--keep-yellow'] if nm in YEL else [])

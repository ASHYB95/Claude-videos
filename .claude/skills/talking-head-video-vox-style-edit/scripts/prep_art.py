#!/usr/bin/env python3
"""Split a background-removed Higgsfield art sheet into single cut-outs, trim, downscale,
duotone into the brand palette and save as WebP (small enough to commit).

Usage:
  python3 prep_art.py <sheet_rb.png> <out_dir> name1,name2,... [--max 800] [--yellow name,name]
                      [duotone flags passed through, e.g. --ink #222024 --paper #ece8de]
Names map to the pieces in reading order (rows top->bottom, then left->right); use '-' to skip one.
Run it once with a dummy name list to see how many pieces it finds (it prints the count).
A flat photo (no cut-out, e.g. a stadium for a TV screen): duotone.py it directly and save as JPEG.
"""
import cv2, numpy as np, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
sheet, out_dir, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
rest = sys.argv[4:]
def take(flag, default):
    if flag in rest:
        i = rest.index(flag); v = rest[i + 1]; del rest[i:i + 2]; return v
    return default
MAX = int(take('--max', 800)); YEL = set(take('--yellow', '').split(',')) - {''}
os.makedirs(out_dir, exist_ok=True)

def trim_resize(i, m):
    ys, xs = np.where(i[..., 3] > 10)
    i = i[max(0, ys.min() - 4):ys.max() + 5, max(0, xs.min() - 4):xs.max() + 5]
    h, w = i.shape[:2]; s = min(1, m / max(h, w))
    return cv2.resize(i, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA) if s < 1 else i

def split(i, minarea=30000):
    a = (i[..., 3] > 40).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(a)
    ks = [k for k in range(1, n) if st[k][4] > minarea]
    ks.sort(key=lambda k: (st[k][1] + st[k][3] / 2) // (i.shape[0] / 3) * 10000 + st[k][0])
    out = []
    for k in ks:
        m = cv2.dilate((lab == k).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
        p = i.copy(); p[..., 3] = np.minimum(p[..., 3], m); out.append(p)
    return out

parts = split(cv2.imread(sheet, cv2.IMREAD_UNCHANGED))
print(f'{os.path.basename(sheet)}: {len(parts)} pieces -> {names}')
for p, nm in zip(parts, names):
    if nm in ('', '-'): continue
    tmp_in, tmp_out = os.path.join(out_dir, '_t.png'), os.path.join(out_dir, '_d.png')
    cv2.imwrite(tmp_in, trim_resize(p, MAX))
    subprocess.run([sys.executable, '-I', os.path.join(here, 'duotone.py'), tmp_in, tmp_out, *rest,
                    *(['--keep-yellow'] if nm in YEL else [])], check=True, capture_output=True)
    cv2.imwrite(os.path.join(out_dir, nm + '.webp'), cv2.imread(tmp_out, cv2.IMREAD_UNCHANGED), [cv2.IMWRITE_WEBP_QUALITY, 90])
    os.remove(tmp_in); os.remove(tmp_out)
    print('  ', nm + '.webp')

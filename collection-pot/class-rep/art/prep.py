# Cut-outs -> trimmed, downscaled, brand-duotoned PNGs in ../assets. Run from class-rep/art:  python3 -I prep.py [names...]
import cv2, numpy as np, subprocess, sys, os, json
OUT = '../assets'
def trim_resize(i, m=1100):
    ys, xs = np.where(i[..., 3] > 10); i = i[max(0, ys.min()-4):ys.max()+5, max(0, xs.min()-4):xs.max()+5]
    h, w = i.shape[:2]; s = min(1, m / max(h, w))
    return cv2.resize(i, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA) if s < 1 else i
def split(i, minarea=40000):
    a = (i[..., 3] > 40).astype(np.uint8); a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(a); out = []
    ks = sorted([k for k in range(1, n) if st[k][4] > minarea], key=lambda k: (st[k][1] // 500, st[k][0]))
    for k in ks:
        m = cv2.dilate((lab == k).astype(np.uint8)*255, np.ones((5, 5), np.uint8)); p = i.copy(); p[..., 3] = np.minimum(p[..., 3], m); out.append(p)
    return out
def duo(src, dst, keep=False):
    subprocess.run(['python3', '-I', 'duotone.py', src, dst] + (['--keep-yellow'] if keep else []), check=True, capture_output=True)
TMP = '_t.png'
SINGLE = {'jo_main': 0, 'jo_stress': 0, 'jo_tea': 0, 'coins': 0, 'school': 0, 'purse': 0, 'hand_phone': 1}
SPLIT = {'parents': ('parent', 700), 'thumbs': ('thumb', 700)}
want = sys.argv[1:] or list(SINGLE) + list(SPLIT)
for name in want:
    f = f'cut/{name}_rb.png'
    if not os.path.exists(f): print('missing', f); continue
    i = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    if name in SINGLE:
        cv2.imwrite(TMP, trim_resize(i)); duo(TMP, f'{OUT}/{name}.png', SINGLE[name]); print(name)
    else:
        base, m = SPLIT[name]
        for k, p in enumerate(split(i)):
            cv2.imwrite(TMP, trim_resize(p, m)); duo(TMP, f'{OUT}/{base}_{k}.png'); print(f'{base}_{k}')
    if name == 'hand_phone':  # locate the solid-yellow screen so a live HTML chat can sit on it
        o = cv2.imread(f'{OUT}/hand_phone.png', cv2.IMREAD_UNCHANGED)
        hsv = cv2.cvtColor(o[..., :3], cv2.COLOR_BGR2HSV)
        m = ((hsv[..., 0] > 12) & (hsv[..., 0] < 38) & (hsv[..., 1] > 110) & (hsv[..., 2] > 90)).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + int(np.argmax(st[1:, 4]))
        cnt = cv2.findContours((lab == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
        (cx, cy), (rw, rh), ang = cv2.minAreaRect(cnt)
        if rw > rh: rw, rh, ang = rh, rw, ang - 90
        if ang < -45: ang += 90
        if ang > 45: ang -= 90
        q = {'w': o.shape[1], 'cx': round(cx, 1), 'cy': round(cy, 1), 'rw': round(rw, 1), 'rh': round(rh, 1), 'ang': round(ang, 2)}
        json.dump(q, open(f'{OUT}/hand_phone_screen.json', 'w')); print(q)
if os.path.exists(TMP): os.remove(TMP)

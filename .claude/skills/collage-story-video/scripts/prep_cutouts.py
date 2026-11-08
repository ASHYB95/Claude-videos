import cv2, numpy as np, subprocess, sys, os
def trim_resize(i, m=1100):
    ys, xs = np.where(i[..., 3] > 10); i = i[max(0, ys.min()-4):ys.max()+5, max(0, xs.min()-4):xs.max()+5]
    h, w = i.shape[:2]; s = min(1, m / max(h, w))
    return cv2.resize(i, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA) if s < 1 else i
def split(i, minarea=40000):
    a = (i[..., 3] > 40).astype(np.uint8); a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(a); out = []
    ks = sorted([k for k in range(1, n) if st[k][4] > minarea], key=lambda k: (st[k][1] // 400, st[k][0]))
    for k in ks:
        m = cv2.dilate((lab == k).astype(np.uint8)*255, np.ones((5, 5), np.uint8)); p = i.copy(); p[..., 3] = np.minimum(p[..., 3], m); out.append(p)
    return out
J = {'margaret_wave': 0, 'priya': 0, 'margaret_phone': 0, 'margaret_laugh': 0, 'hand_phone': 1, 'hand_pencil': 1, 'hand_point': 0, 'building': 0, 'envelope': 0, 'kitchen': 0, 'm1994': 0}
for name, ky in J.items():
    i = cv2.imread(f'cut2/{name}_rb.png', cv2.IMREAD_UNCHANGED); cv2.imwrite('/tmp/_t.png', trim_resize(i))
    subprocess.run(['python3', '-I', 'duotone.py', '/tmp/_t.png', f'final/{name}.png'] + (['--keep-yellow'] if ky else []), check=True, capture_output=True)
for name in ['colleagues', 'props']:
    i = cv2.imread(f'cut2/{name}_rb.png', cv2.IMREAD_UNCHANGED)
    for k, p in enumerate(split(i)):
        cv2.imwrite('/tmp/_t.png', trim_resize(p, 800)); subprocess.run(['python3', '-I', 'duotone.py', '/tmp/_t.png', f'final/{name}_{k}.png'], check=True, capture_output=True)
for name, w in [('newsbg', 1080), ('ukmap', 1100)]:
    i = cv2.imread(f'np/{name}.png'); h = int(i.shape[0] * w / i.shape[1]); cv2.imwrite('/tmp/_t.png', cv2.resize(i, (w, h), interpolation=cv2.INTER_AREA))
    subprocess.run(['python3', '-I', 'duotone.py', '/tmp/_t.png', f'final/{name}.png', '--contrast', '0.9'], check=True, capture_output=True)
print(sorted(os.listdir('final')))

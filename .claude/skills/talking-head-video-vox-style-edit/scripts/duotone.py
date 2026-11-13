#!/usr/bin/env python3
"""Brand duotone: map an image's tones onto ink -> paper, optionally snapping a solid accent
(e.g. a phone/TV screen generated as flat yellow) to a brand colour while keeping its shading.
Alpha is preserved.

Usage: python3 duotone.py in.png out.png [--ink #222024] [--paper #ece8de] [--contrast 1.12]
                         [--keep-yellow [--yellow #fec42d]] [--keep-purple [--purple #6c2ea4]]
Defaults are the Purple Seed palette (paper a touch lighter than the site's #e7e3d7 so cut-outs read on it).
Backgrounds/textures: use --contrast 0.75 for a soft newsprint ground.
"""
import cv2, numpy as np, sys

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
def bgr(h):
    h = h.lstrip('#'); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], np.float32)

src, dst = sys.argv[1], sys.argv[2]
contrast = float(arg('--contrast', 1.12))
ink, paper = bgr(arg('--ink', '#222024')), bgr(arg('--paper', '#ece8de'))
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
alpha = img[..., 3] if img.shape[2] == 4 else None
L = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
L = np.clip((L - 0.5) * contrast + 0.5, 0, 1)
out = ink * (1 - L[..., None]) + paper * L[..., None]
hsv = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2HSV).astype(np.float32)
h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255

def snap(mask, colour):
    global out
    m = cv2.GaussianBlur(mask.astype(np.float32), (5, 5), 0)[..., None]
    ref = np.percentile(v[mask], 90) if mask.any() else 1
    shade = np.clip(v / max(ref, 1e-3), 0.55, 1.0)[..., None]
    out = out * (1 - m) + (colour * shade) * m

if '--keep-yellow' in sys.argv:
    snap((h > 12) & (h < 38) & (s > 0.45) & (v > 0.35), bgr(arg('--yellow', '#fec42d')))
if '--keep-purple' in sys.argv:
    snap((h > 120) & (h < 160) & (s > 0.35) & (v > 0.2), bgr(arg('--purple', '#6c2ea4')))
out = np.clip(out, 0, 255).astype(np.uint8)
if alpha is not None: out = np.dstack([out, alpha])
cv2.imwrite(dst, out); print(dst)

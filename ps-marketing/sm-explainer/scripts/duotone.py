# Purple Seed duotone: map an image's tones onto ink #222024 -> warm paper #ece8de
# (a touch lighter than the site's #e7e3d7 so cut-outs read on it), optionally snapping
# a solid accent to brand purple #6c2ea4 or yellow #fec42d while keeping its shading.
# Alpha is preserved.
# Usage: python3 duotone.py in.png out.png [--contrast 1.15] [--keep-purple] [--keep-yellow]
import cv2, numpy as np, sys
src, dst = sys.argv[1], sys.argv[2]
contrast = float(sys.argv[sys.argv.index('--contrast') + 1]) if '--contrast' in sys.argv else 1.12
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
alpha = img[..., 3] if img.shape[2] == 4 else None
L = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
L = np.clip((L - 0.5) * contrast + 0.5, 0, 1)
ink = np.array([0x24, 0x20, 0x22], np.float32)     # BGR of #222024
paper = np.array([0xde, 0xe8, 0xec], np.float32)   # BGR of #ece8de
out = ink * (1 - L[..., None]) + paper * L[..., None]
hsv = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2HSV).astype(np.float32)
h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
def snap(mask, bgr):
    global out
    m = cv2.GaussianBlur(mask.astype(np.float32), (5, 5), 0)[..., None]
    ref = np.percentile(v[mask], 90) if mask.any() else 1
    shade = np.clip(v / max(ref, 1e-3), 0.55, 1.0)[..., None]
    out = out * (1 - m) + (np.array(bgr, np.float32) * shade) * m
if '--keep-yellow' in sys.argv:
    snap((h > 12) & (h < 38) & (s > 0.45) & (v > 0.35), [0x2d, 0xc4, 0xfe])   # #fec42d
if '--keep-purple' in sys.argv:
    snap((h > 120) & (h < 160) & (s > 0.35) & (v > 0.2), [0xa4, 0x2e, 0x6c])  # #6c2ea4
out = np.clip(out, 0, 255).astype(np.uint8)
if alpha is not None: out = np.dstack([out, alpha])
cv2.imwrite(dst, out); print(dst)

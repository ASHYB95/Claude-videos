# Brand duotone: map an image's tones onto Collection Pot charcoal (#2f2f32) → cream (#fffcf8),
# and snap any yellow accent to brand yellow (#f9b910), keeping its shading. Alpha is preserved.
# Usage: python3 duotone.py in.png out.png [--contrast 1.15] [--keep-yellow]
import cv2, numpy as np, sys
src, dst = sys.argv[1], sys.argv[2]
contrast = float(sys.argv[sys.argv.index('--contrast') + 1]) if '--contrast' in sys.argv else 1.12
keep_y = '--keep-yellow' in sys.argv
img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
alpha = img[..., 3] if img.shape[2] == 4 else None
bgr = img[..., :3].astype(np.float32)
L = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
L = np.clip((L - 0.5) * contrast + 0.5, 0, 1)
ink = np.array([0x32, 0x2f, 0x2f], np.float32)      # BGR of #2f2f32
paper = np.array([0xf8, 0xfc, 0xff], np.float32)    # BGR of #fffcf8
out = ink * (1 - L[..., None]) + paper * L[..., None]
if keep_y:
    hsv = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    ymask = ((h > 12) & (h < 38) & (s > 0.45) & (v > 0.35)).astype(np.float32)
    ymask = cv2.GaussianBlur(ymask, (5, 5), 0)[..., None]
    yel = np.array([0x10, 0xb9, 0xf9], np.float32)  # BGR of #f9b910
    shade = np.clip(v / max(np.percentile(v[ymask[..., 0] > 0.5], 90) if (ymask > 0.5).any() else 1, 1e-3), 0.55, 1.0)[..., None]
    out = out * (1 - ymask) + (yel * shade) * ymask
out = np.clip(out, 0, 255).astype(np.uint8)
if alpha is not None: out = np.dstack([out, alpha])
cv2.imwrite(dst, out); print(dst)

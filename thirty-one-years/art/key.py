# Green-screen key for the Higgsfield collage stills → transparent PNG cut-outs (white sticker border kept).
# Usage: python3 key.py raw.png out_prefix [--split]   (--split: one PNG per separate cut-out on the sheet)
import cv2, numpy as np, sys
src, prefix = sys.argv[1], sys.argv[2]; split = '--split' in sys.argv
img = cv2.imread(src).astype(np.float32)
b, g, r = img[..., 0], img[..., 1], img[..., 2]
# greenness: how much G dominates R and B
gd = g - np.maximum(r, b)
alpha = 1 - np.clip((gd - 40) / 60, 0, 1)          # gd<=40 → opaque, gd>=100 → transparent
alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
# despill: clamp green to max(r,b) where it leaks into edges
g2 = np.minimum(g, np.maximum(r, b) + 6)
out = np.dstack([b, g2, r]).clip(0, 255).astype(np.uint8)
a8 = (alpha * 255).astype(np.uint8)
# drop tiny specks
n, lab, stats, _ = cv2.connectedComponentsWithStats((a8 > 128).astype(np.uint8))
keep = np.zeros_like(a8)
comps = [k for k in range(1, n) if stats[k][4] > 4000]
for k in comps: keep[lab == k] = 255
keep = cv2.dilate(keep, np.ones((5, 5), np.uint8))
a8 = np.minimum(a8, keep)
rgba = np.dstack([out, a8])
def save(arr, path):
    ys, xs = np.where(arr[..., 3] > 8)
    y0, y1, x0, x1 = max(0, ys.min() - 4), ys.max() + 5, max(0, xs.min() - 4), xs.max() + 5
    cv2.imwrite(path, arr[y0:y1, x0:x1]); print(path, x1 - x0, y1 - y0)
if split:
    comps = sorted(comps, key=lambda k: (stats[k][1] // 300, stats[k][0]))  # rows, then left→right
    for i, k in enumerate(comps):
        m = cv2.dilate((lab == k).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
        part = rgba.copy(); part[..., 3] = np.minimum(part[..., 3], m)
        save(part, f'{prefix}_{i}.png')
else:
    save(rgba, f'{prefix}.png')

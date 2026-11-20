# Cut Chip poses out of a flat light background (character sheet crops or plain-background renders)
# by flood-filling the background from the image border. No credits needed.
# Usage: python3 -I cutout.py in.png out.png [x0 y0 x1 y1] [--tol 22]
import cv2, numpy as np, sys
a = sys.argv[1:]; tol = 22
if '--tol' in a: i = a.index('--tol'); tol = int(a[i + 1]); del a[i:i + 2]
src, dst = a[0], a[1]
img = cv2.imread(src)
if len(a) >= 6:
    x0, y0, x1, y1 = map(int, a[2:6]); img = img[y0:y1, x0:x1]
h, w = img.shape[:2]
mask = np.zeros((h + 2, w + 2), np.uint8)
flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
for x in range(0, w, 6):
    for y in (0, h - 1):
        if mask[y + 1, x + 1] == 0: cv2.floodFill(img, mask, (x, y), 0, (tol,) * 3, (tol,) * 3, flags)
for y in range(0, h, 6):
    for x in (0, w - 1):
        if mask[y + 1, x + 1] == 0: cv2.floodFill(img, mask, (x, y), 0, (tol,) * 3, (tol,) * 3, flags)
bg = mask[1:-1, 1:-1] > 0
# keep only the largest foreground blob (drops stray marks / neighbouring labels)
fg = (~bg).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
if n > 1:
    big = 1 + int(np.argmax(st[1:, 4])); keep = lab == big
    for k in range(1, n):   # also keep sizeable pieces near the main blob (e.g. a held prop)
        if k != big and st[k, 4] > 0.02 * st[big, 4]: keep |= lab == k
    fg = keep.astype(np.uint8)
alpha = cv2.GaussianBlur(cv2.erode(fg * 255, np.ones((2, 2), np.uint8)).astype(np.float32), (3, 3), 0)
out = np.dstack([img, alpha.astype(np.uint8)])
ys, xs = np.where(out[..., 3] > 10)
out = out[max(0, ys.min() - 4):ys.max() + 5, max(0, xs.min() - 4):xs.max() + 5]
cv2.imwrite(dst, out); print(dst, out.shape[1], out.shape[0])

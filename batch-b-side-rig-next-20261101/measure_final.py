"""Batch B final measurements (PIL only). Prints JSON-ready numbers for REPORT:
neck gap before/after (piece-overlay simulation at wrist-fix vs batch-b
neck centres), side/back waist widths vs Row7_10, palm coverage vs fused
palm, back v2 render bbox, side bent render bbox, FK frame count.
"""
import os, json
from PIL import Image
import numpy as np

OUT = os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101')
CJ = os.path.expanduser('~/workspace/cape-jones-rig')
S = 0.9557
SB = 1.20

def load(p):
    return np.array(Image.open(p).convert('RGBA'))

def place(canvas, im, cx, cy, s):
    h, w = im.shape[:2]
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    a = np.array(Image.fromarray(im).resize((nw, nh), Image.LANCZOS))
    x0, y0 = int(round(cx - nw / 2)), int(round(cy - nh / 2))
    H, W = canvas.shape
    x1, y1 = x0 + nw, y0 + nh
    cx0, cy0 = max(0, x0), max(0, y0); cx1, cy1 = min(W, x1), min(H, y1)
    if cx1 <= cx0 or cy1 <= cy0: return
    sub = a[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    canvas[cy0:cy1, cx0:cx1] = np.maximum(canvas[cy0:cy1, cx0:cx1], sub[:, :, 3])

def col_tb(alpha, x):
    ys = np.where(alpha[:, x] > 10)[0]
    return (int(ys[0]), int(ys[-1])) if len(ys) else (None, None)

head = load(os.path.join(CJ, 'side-pack-new-20261101', 'side_head_profile.png'))
neck = load(os.path.join(CJ, 'side-pack-new-20261101', 'side_cowl_neck.png'))
out = {}
for tag, cy in [('before', 367), ('after', 357)]:
    ch = np.zeros((1600, 1400), dtype=np.uint8); cn = np.zeros((1600, 1400), dtype=np.uint8)
    place(ch, head, 662, 200, S); place(cn, neck, 663, cy, S)
    face, centre, back = [], [], []
    for x in range(560, 760):
        _, hb = col_tb(ch, x); nt, _ = col_tb(cn, x)
        if hb is not None and nt is not None:
            g = nt - hb
            if x >= 700: face.append(g)
            if 640 <= x < 680: centre.append(g)
            if x < 660: back.append(g)
    out['neck_' + tag] = {
        'face_mean': round(sum(face) / len(face), 1), 'face_min': min(face), 'face_max': max(face), 'face_n': len(face),
        'centre_mean': round(sum(centre) / len(centre), 1),
        'back_mean': round(sum(back) / len(back), 1), 'back_max': max(back)}
    print('NECK', tag, out['neck_' + tag])

# waist widths: side torso+pelvis silhouette at belt height (canvas y 790)
torso = load(os.path.join(CJ, 'side-pack-new-20261101', 'side_torso_belt.png'))
pelvis = load(os.path.join(CJ, 'side-pack-new-20261101', 'side_pelvis_hip.png'))
sil = np.zeros((1600, 1400), dtype=np.uint8)
place(sil, torso, 670, 655, S); place(sil, pelvis, 677, 835, S)
for y in [760, 790, 820]:
    xs = np.where(sil[y] > 10)[0]
    print('SIDE waist y', y, 'x', int(xs[0]), int(xs[-1]), 'w', int(xs[-1] - xs[0] + 1))
    out.setdefault('side_waist', {})[str(y)] = int(xs[-1] - xs[0] + 1)
# back waist: belt+pelvis piece width at SB
print('BACK waist fused belt+pelvis width canvas', round(192 * SB, 1))
print('ROW7_10 width canvas side', round(206 * S, 1), 'back', round(206 * SB, 1), 'height side', round(82 * S, 1), 'back', round(82 * SB, 1))
out['row7'] = {'w_side': round(206 * S, 1), 'w_back': round(206 * SB, 1),
               'h_side': round(82 * S, 1), 'h_back': round(82 * SB, 1)}
# palm coverage: fused palm region (forearm piece rows 159-272, cols 0-96)
fa = load(os.path.join(CJ, 'back-pack-base-20261101', 'back_forearm_gauntlet_hand_left.png'))
sub = fa[159:, :, 3]
ys, xs = np.where(sub > 10)
print('FUSED palm native bbox w', int(xs.max() - xs.min() + 1), 'h', int(ys.max() - ys.min() + 1),
      'canvas@SB', round((xs.max() - xs.min() + 1) * SB, 1), 'x', round((ys.max() - ys.min() + 1) * SB, 1))
r5 = load(os.path.join(CJ, 'sliced-clean-20261031', 'A-root', '08-body-parts-limbs-capes', 'Row5_15.png'))
h10 = load(os.path.join(CJ, 'pack1', 'Hand_10.png'))
print('ROW5_15 canvas@SB', round(121 * SB, 1), 'x', round(121 * SB, 1))
print('HAND_10 canvas@SB', round(161 * SB, 1), 'x', round(110 * SB, 1))
out['palm'] = {'fused_w': round((xs.max() - xs.min() + 1) * SB, 1),
              'fused_h': round((ys.max() - ys.min() + 1) * SB, 1),
              'row5': round(121 * SB, 1), 'hand10_w': round(161 * SB, 1), 'hand10_h': round(110 * SB, 1)}
# render bboxes (non-background-grey content)
for f, bg in [('back-rig-standing-v2-20261101.png', 170), ('side-open-hand-bent-20261101.png', 170),
              ('side-open-hand-rest-20261101.png', 170)]:
    p = os.path.join(OUT, f)
    if not os.path.exists(p):
        print('MISSING', f); continue
    im = np.array(Image.open(p).convert('RGB')).astype(int)
    non = (np.abs(im[:, :, 0] - bg) > 10) | (np.abs(im[:, :, 1] - bg) > 10) | (np.abs(im[:, :, 2] - bg) > 10)
    ys, xs = np.where(non)
    print('RENDER', f, 'bbox x', int(xs.min()), int(xs.max()), 'y', int(ys.min()), int(ys.max()))
    out['render_' + f] = [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())]
fk = sorted(fn for fn in os.listdir(os.path.join(OUT, 'frames-fk')) if fn.endswith('.png')) if os.path.exists(os.path.join(OUT, 'frames-fk')) else []
print('FK frames:', len(fk), fk)
out['fk_frames'] = len(fk)
with open(os.path.join(OUT, 'measurements-20261101.json'), 'w') as fh:
    json.dump(out, fh, indent=1)
print('WROTE measurements-20261101.json')

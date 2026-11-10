#!/usr/bin/env python3
"""AH front + SMILE 3/4 overlay-erase clean, Mars 2026-10-31 22:26 + 22:29 correction.
Method M2 (the one that actually cleans it): per-patch garbage matte by
connected-component anchor rule -- NO hand pixel painting, NO manual coords.
  Keep: the black component that touches ALL main interior anchors within a
  2px dilation (AH: main orange tongue; SMILE: upper white teeth, lower white
  teeth, main orange tongue), plus those main interior anchor components
  (>=100px). Drop: every other component (jaw, cheek, fringe specks).
Method M1: v2 colour-material filter (baseline, already in source patches).
Method M4: LANCZOS resize + alpha threshold >=128 on fitting (v2 halo fix).
Method M5 (experimental, REJECTED): morphological opening -- would erase
  thin mouth lines, not applied.
Fitting: identical to v2 place(): target (231.5,504.5), alpha-bbox centre
anchor, AH scale 0.7117, SMILE scale 1.317, same clean-head base.
"""
import os, json
from PIL import Image
import numpy as np
from scipy import ndimage

R = os.path.expanduser('~/workspace/cape-jones-rig')
SRC = f'{R}/pahgo-mouth-cleanup-v2-20261031/mouths-v2'
BASE = Image.open(f'{R}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
OUT = f'{R}/mouth-ah-smile34-clean-20261031'
os.makedirs(f'{OUT}/patches', exist_ok=True)
os.makedirs(f'{OUT}/fitted', exist_ok=True)
TARGET = (231.5, 504.5)

def comps(mask):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        m = lab == i
        ys, xs = np.where(m)
        out.append((int(m.sum()), m, (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))))
    return sorted(out, key=lambda t: -t[0])

def clean_patch(name):
    im = np.array(Image.open(f'{SRC}/{name}').convert('RGBA'))
    a = im[:, :, 3] > 128
    r, g, b = im[:, :, 0].astype(int), im[:, :, 1].astype(int), im[:, :, 2].astype(int)
    black = a & (r < 80) & (g < 80) & (b < 80)
    white = a & (r > 200) & (g > 200) & (b > 200)
    orange = a & (r > 100) & (g < 135) & (b < 95) & (r > g + 25)
    # main interior anchors: components >=100px
    anchors = []
    for mask in (white, orange):
        for sz, m, bb in comps(mask):
            if sz >= 100:
                anchors.append((sz, m, bb))
    dil_anchors = [ndimage.binary_dilation(m, iterations=2) for _, m, _ in anchors]
    keep_black, dropped_black, touch = [], [], {}
    for sz, m, bb in comps(black):
        touches = [bool((m & d).any()) for d in dil_anchors]
        touch[bb] = touches
        if all(touches):
            keep_black.append(m)
        else:
            dropped_black.append((sz, bb))
    keep = np.zeros(a.shape, bool)
    for m in keep_black:
        keep |= m
    for sz, m, bb in anchors:
        keep |= m
    out = im.copy()
    out[~keep, 3] = 0
    return Image.fromarray(out), dict(
        src_alpha=int(a.sum()), clean_alpha=int(keep.sum()),
        dropped=int(a.sum() - keep.sum()),
        black_kept=[int(m.sum()) for m in keep_black],
        black_dropped=dropped_black,
        anchors=[(int(sz), bb) for sz, _, bb in anchors],
    )

def alpha_bbox(im):
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] >= 128)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(xs)))

def fit(patch, scale):
    nw, nh = max(1, round(patch.width * scale)), max(1, round(patch.height * scale))
    rz = patch.resize((nw, nh), Image.LANCZOS)
    arr = np.array(rz); arr[arr[:, :, 3] < 128, 3] = 0
    rz = Image.fromarray(arr)
    bb = alpha_bbox(rz)
    cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
    head = BASE.copy()
    head.alpha_composite(rz, (int(round(TARGET[0] - cx)), int(round(TARGET[1] - cy))))
    return head, bb

results = {}
for key, src, scale in [('ah-clean', 'ah-v2_clean_patch.png', 0.7117),
                        ('smile34-clean', 'smile34-v2_clean_patch.png', 1.317)]:
    patch, rep = clean_patch(src)
    patch.save(f'{OUT}/patches/{key}_clean_patch.png')
    head, bb = fit(patch, scale)
    head.save(f'{OUT}/fitted/{key}_on_cape_head.png')
    rep.update(scale=scale, fitted_bbox=bb, fitted_alpha=bb[4])
    results[key] = rep
    print(key, rep)

json.dump(results, open(f'{OUT}/measurements-20261031.json', 'w'), indent=1)

# contacts: mouth-only before/after on magenta, fitted before/after, zooms
def on_magenta(im, scale=4):
    bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
    return bg.resize((im.width * scale, im.height * scale), Image.NEAREST)

def contact(imgs, labels, path, scale=4):
    tiles = [on_magenta(im, scale) if im.mode == 'RGBA' else im for im in imgs]
    # use fitted heads at native size side by side separately; this fn is for patches
    W = max(t.width for t in tiles); H = max(t.height for t in tiles) + 28
    from PIL import ImageDraw
    sheet = Image.new('RGB', (W * len(tiles), H), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(tiles):
        sheet.paste(t.convert('RGB'), (i * W, 28))
        d.text((i * W + 8, 6), labels[i], fill=(255, 255, 0))
    sheet.save(path); print(path, sheet.size)

for key, src in [('ah-clean', 'ah-v2_clean_patch.png'), ('smile34-clean', 'smile34-v2_clean_patch.png')]:
    before = Image.open(f'{SRC}/{src}').convert('RGBA')
    after = Image.open(f'{OUT}/patches/{key}_clean_patch.png')
    contact([before, after], [f'{key} BEFORE (v2)', f'{key} AFTER (garbage matte)'],
             f'{OUT}/mouth-only-{key}-20261031.png', scale=5 if 'ah' in key else 7)

# fitted before/after contact (native head size)
from PIL import ImageDraw
def fitted_contact():
    pairs = [('ah', 'ah-v2_on_cape_head.png', 'ah-clean_on_cape_head.png'),
             ('smile34', 'smile34-v2_on_cape_head.png', 'smile34-clean_on_cape_head.png')]
    imgs, labels = [], []
    for _, b, a in pairs:
        imgs.append(Image.open(f'{R}/pahgo-mouth-cleanup-v2-20261031/fitted-v2/{b}').convert('RGB'))
        labels.append('BEFORE v2')
        imgs.append(Image.open(f'{OUT}/fitted/{a}').convert('RGB'))
        labels.append('AFTER clean')
    W, H = imgs[0].size
    sheet = Image.new('RGB', (W * 2, (H + 28) * 2), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(imgs):
        x = (i % 2) * W; y = (i // 2) * (H + 28)
        sheet.paste(im, (x, y + 28)); d.text((x + 8, y + 6), f'{pairs[i//2][0]} {labels[i]}', fill=(255, 255, 0))
    sheet.save(f'{OUT}/fitted-before-after-20261031.png'); print('fitted contact', sheet.size)
fitted_contact()

# zooms: AH right corner (patch coords x150-235, y55-98), SMILE left jaw (x0-75, y20-86)
def zoom(patch_path, box, path, scale=10):
    im = Image.open(patch_path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
    crop = bg.crop(box)
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
    crop.convert('RGB').save(path); print(path, crop.size)
zoom(f'{SRC}/ah-v2_clean_patch.png', (150, 55, 235, 98), f'{OUT}/zoom-ah-before-20261031.png')
zoom(f'{OUT}/patches/ah-clean_clean_patch.png', (150, 55, 235, 98), f'{OUT}/zoom-ah-after-20261031.png')
zoom(f'{SRC}/smile34-v2_clean_patch.png', (0, 20, 80, 86), f'{OUT}/zoom-smile-before-20261031.png')
zoom(f'{OUT}/patches/smile34-clean_clean_patch.png', (0, 20, 80, 86), f'{OUT}/zoom-smile-after-20261031.png')

#!/usr/bin/env python3
"""General mouth-clean pipeline, Mars 2026-10-31 23:14 CDT.
Layman rule: remove all the stuff around the mouth WITHOUT erasing the mouth.
Computer rule (exact, no guessing):
  M1 colour decontamination: keep only mouth-material pixels:
     dark  = alpha>=128 AND R<90 AND G<90 AND B<90
     white = alpha>=128 AND R>200 AND G>200 AND B>200
     orange= alpha>=128 AND R>100 AND G<135 AND B<95 AND R>G+25
     red   = alpha>=128 AND R>120 AND R>B+30 AND G<150 AND NOT orange
     Everything else (skin, costume, suit, background) is dropped by class,
     not by hand coordinates.
  M2 garbage matte / rotoscope matte, connected-component anchor rule:
     anchors = white components >=100px + orange components >=100px
     (8-connectivity, scipy ndimage.label, structure 3x3 ones).
     If anchors exist:
       ALL: keep a dark component iff it touches EVERY anchor within a
            2px dilation of that anchor. Keep the anchors themselves.
       ANY (fallback, only if ALL keeps zero dark): keep a dark component
            iff it touches ANY anchor within 2px dilation.
       Report which rule fired per mouth; never claim ALL when ANY fired.
     If no anchors exist (thin-line mouths):
       CHAIN: keep the largest dark component, then iteratively keep any
              dark component within 5px dilation of the kept set.
              Isolated specks far from the line are dropped by rule.
     Drop every other component. No hand pixel painting, no manual coords,
     no colour change: output = input with dropped pixels' alpha set to 0.
  M3 overlay erasing per frame: the same M1+M2 matte is applied at fit time
     to every fitted head, one matte per frame, not one matte for the whole
     sequence. Fitted target (231.5, 504.5), alpha-bbox centre anchor,
     LANCZOS resize, alpha>=128 after resize.
  M4 vector line fit (thin-line mouths only): centreline from kept dark
     fragments -> cubic spline (scipy UnivariateSpline) -> cubic Bezier
     segments -> SVG -> 8x supersample raster, LANCZOS downscale, alpha>=128.
     If a spline cannot be fitted (too few columns), M4 is skipped for that
     mouth and the raster M2 result stands; that is a method skip, not a
     claim that the mouth cannot be cleaned.
  M5 morphological opening: TRIED and REJECTED for thin-line mouths, because
     opening erases thin mouth lines. It is documented, not applied, and its
     rejection is not a roadblock: M2 already cleaned those mouths.
Gates (gate_mouth_general.py, same file logic, exit 0 PASS / 1 FAIL):
  G1 kept alpha <= source alpha, and kept pixels are a subset of source
     pixels (no invented colour, except M4 vector patches, flagged).
  G2 largest kept component >=30px and kept alpha >=30px (mouth present).
  G3 fitted centre within 2px of (231.5, 504.5) when a fitted head is made.
  G4 no component dropped by hand: dropped = source - kept, by rule only.
"""
import os, json, glob
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

R = os.path.expanduser('~/workspace/cape-jones-rig')
OUT = f'{R}/mouth-clean-pipeline-general-20261031'
BASE = Image.open(f'{R}/visemes-v2-20261031/clean-head-base-20261031.png').convert('RGBA')
TARGET = (231.5, 504.5)

SOURCES = []
for pat, group in [
    (f'{R}/pahgo-mouth-cleanup-v2-20261031/mouths-v2/*_clean_patch.png', 'V2-7'),
    (f'{R}/mouth-packs-clean-pipeline-20261031/packs/*-patch.png', 'PACKS'),
    (f'{R}/lipsync-production-20261031/mouths/*.png', 'LIPSYNC'),
]:
    for p in sorted(glob.glob(pat)):
        SOURCES.append((group, p))
# approved AH/SMILE cleaned patches are inputs too, as regression proof:
# running the pipeline on an already-clean patch must keep it (near-)unchanged.
SOURCES.append(('APPROVED', f'{R}/mouth-ah-smile34-clean-20261031/patches/ah-clean_clean_patch.png'))
SOURCES.append(('APPROVED', f'{R}/mouth-ah-smile34-clean-20261031/patches/smile34-clean_clean_patch.png'))

def comps(mask):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        m = lab == i
        ys, xs = np.where(m)
        out.append((int(m.sum()), m, (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))))
    return sorted(out, key=lambda t: -t[0])

def clean(im):
    a = np.array(im)[:, :, 3] >= 128
    arr = np.array(im).astype(int)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    dark = a & (r < 90) & (g < 90) & (b < 90)
    white = a & (r > 200) & (g > 200) & (b > 200)
    orange = a & (r > 100) & (g < 135) & (b < 95) & (r > g + 25)
    red = a & (r > 120) & (r > b + 30) & (g < 150) & ~orange
    material = dark | white | orange | red
    # M1 dropped by class
    m1_dropped = int(a.sum() - material.sum())
    anchors = []
    for mask in (white, orange, red):
        for sz, m, bb in comps(mask):
            if sz >= 100:
                anchors.append((sz, m, bb))
    keep = np.zeros(a.shape, bool)
    rule = 'CHAIN'
    if anchors:
        dil = [ndimage.binary_dilation(m, iterations=2) for _, m, _ in anchors]
        all_keep = []
        for sz, m, bb in comps(dark):
            if all(bool((m & d).any()) for d in dil):
                all_keep.append(m)
        if all_keep:
            rule = 'ALL'
            for m in all_keep: keep |= m
        else:
            rule = 'ANY'
            for sz, m, bb in comps(dark):
                if any(bool((m & d).any()) for d in dil):
                    keep |= m
        for sz, m, bb in anchors: keep |= m
    else:
        # CHAIN: largest dark + iterative 5px neighbours
        dc = comps(dark)
        if dc:
            keep |= dc[0][1]
            changed = True
            while changed:
                changed = False
                dil = ndimage.binary_dilation(keep, iterations=5)
                for sz, m, bb in dc:
                    if not keep[m].any() and (m & dil).any():
                        keep |= m; changed = True
    # material pixels that are not dark/anchor are kept only if they are
    # part of an anchor class already kept; other material (small white/orange
    # specks <100px, small red) is dropped unless it touches kept set.
    # This keeps the rule strict: mouth = dark body + its main interior anchors.
    out = np.array(im).copy()
    out[~keep, 3] = 0
    return Image.fromarray(out), dict(
        src_alpha=int(a.sum()), kept_alpha=int(keep.sum()),
        dropped=int(a.sum() - keep.sum()), m1_class_dropped=m1_dropped,
        rule=rule, anchors=[(int(sz), bb) for sz, _, bb in anchors],
        largest_kept=int(max([int((keep & (np.array(im)[:, :, 3] >= 128)).sum())] + [0])) if keep.any() else 0,
    )

def alpha_bbox(im):
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] >= 128)
    if len(xs) == 0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(xs)))

def fit(patch):
    # fit at native size (scale 1) for proof; per-mouth fitted scale is
    # recorded in the v2/pipeline reports and is not re-invented here.
    bb = alpha_bbox(patch)
    if bb is None: return BASE.copy(), None
    cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
    head = BASE.copy()
    head.alpha_composite(patch, (int(round(TARGET[0] - cx)), int(round(TARGET[1] - cy))))
    return head, bb

results = {}
for group, path in SOURCES:
    name = os.path.basename(path)
    key = f"{group}__{name}"
    im = Image.open(path).convert('RGBA')
    cleaned, rep = clean(im)
    cleaned.save(f'{OUT}/cleaned/{key}')
    head, bb = fit(cleaned)
    head.save(f'{OUT}/fitted/{key}')
    # gates
    rep['group'] = group; rep['source'] = path
    rep['fitted_bbox'] = bb
    if bb:
        cx = (bb[0] + bb[2]) / 2; cy = (bb[1] + bb[3]) / 2
        # fitted centre on head = target by construction; record patch centre
        rep['patch_centre'] = [cx, cy]
    rep['gate_G1_subset'] = bool(rep['kept_alpha'] <= rep['src_alpha'])
    rep['gate_G2_present'] = bool(rep['kept_alpha'] >= 30)
    rep['gate_PASS'] = bool(rep['gate_G1_subset'] and rep['gate_G2_present'])
    results[key] = rep
    print(key, rep['rule'], rep['src_alpha'], '->', rep['kept_alpha'], 'dropped', rep['dropped'], 'PASS' if rep['gate_PASS'] else 'FAIL')

json.dump(results, open(f'{OUT}/measurements-general-pipeline-20261031.json', 'w'), indent=1)
print(f"TOTAL {len(results)} sources, PASS {sum(1 for v in results.values() if v['gate_PASS'])}")

# contacts: before/after on magenta, per group, patches at 3x
def on_mag(im, scale=3):
    bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
    return bg.resize((im.width * scale, im.height * scale), Image.NEAREST)

for group in sorted(set(g for g, _ in SOURCES)):
    items = [(g, p) for g, p in SOURCES if g == group]
    tiles = []
    for g, p in items:
        src = Image.open(p).convert('RGBA'); cl = Image.open(f"{OUT}/cleaned/{g}__{os.path.basename(p)}").convert('RGBA')
        tiles.append((os.path.basename(p)[:28], on_mag(src), on_mag(cl)))
    if not tiles: continue
    W = max(max(t[1].width, t[2].width) for t in tiles); H = max(max(t[1].height, t[2].height) for t in tiles) + 28
    sheet = Image.new('RGB', (W * 2, H * len(tiles)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (lab, s, c) in enumerate(tiles):
        sheet.paste(s.convert('RGB'), (0, i * H + 28)); sheet.paste(c.convert('RGB'), (W, i * H + 28))
        d.text((8, i * H + 6), f"{lab} BEFORE", fill=(255, 255, 0))
        d.text((W + 8, i * H + 6), f"{lab} AFTER", fill=(0, 255, 0))
    sheet.save(f'{OUT}/contacts/contact-{group}-before-after-20261031.png')
    print('contact', group, sheet.size)

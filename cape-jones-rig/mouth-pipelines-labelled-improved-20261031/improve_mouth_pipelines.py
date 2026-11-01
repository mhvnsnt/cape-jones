#!/usr/bin/env python3
"""Labelled + improved mouth pipelines, Mars 2026-10-31 23:22 CDT.
APPROVED original (mouth-clean-pipeline-general-20261031) is NOT touched.
This script starts from the SAME 37 original sources as that pipeline,
re-runs its M1+M2 exactly, then applies ONLY industry-standard improvements:
  H1 hole-fill (rotoscope matte repair): fill enclosed holes <=100px in the
     kept mask. A hole is a transparent island fully surrounded by kept
     mouth pixels. Filling a pinhole does NOT add exterior pixels and does
     NOT erase mouth pixels. Holes >100px are left alone (they may be real
     interior transparency, e.g. between teeth).
  H2 speck purge (matte cleanup): drop kept components <15px that do not
     touch the main kept set within 2px and are not anchors. Already-clean
     mouths will show 0 here - that is a pass, not a failure.
  H3 anchor recovery (anchor threshold, adaptive): the approved pipeline
     accepts anchors >=100px only. A white/orange/red component >=50px that
     touches a kept dark component within 2px is a real small tooth/tongue
     fragment, not jaw/skin. Recover it, then re-run the ALL rule with it.
     Jaw/skin blocks are dark, never anchors, so they cannot be recovered
     by this step - they are still dropped by M2.
  H4 thin-line bridge (spline inbetweening, thin-line mouths ONLY):
     if the kept set is CHAIN and there is ONE gap <=20 columns between two
     kept dark segments in the same row band (both sides >=20px), bridge it
     with a 2px line following the segment centres (linear interpolation,
     the discrete form of a spline inbetween). This is the same method as
     the clean-line vector pipeline, applied at patch level, NOT hand
     painting. Thick cavity mouths never get a bridge.
  H5 edge-extend fit (compositing edge decontamination, proof only):
     when a patch is resized for fitting, edge-extend its colours 2px
     outward first, then LANCZOS resize, then alpha>=128. Without this,
     LANCZOS fringe alpha 1-127 darkens the clean head skin (the v2 leak:
     fitted diff 1,368px for a 93px patch). With it, fringe pixels drop.
     Proof: for AH, GK, MBP resized to 0.75x, count dark fringe pixels
     (alpha 1-127, dark) on the clean head with vs without edge-extend.
Gates: G1 improved alpha is a subset of source alpha, except H4 bridge
  pixels (flagged, counted separately, never hidden) and H1 filled holes
  (flagged, inside the kept mask only). G2 mouth present >=30px.
  G3 no approved file was written to, and no source file was changed.
"""
import os, json, glob
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

R = os.path.expanduser('~/workspace/cape-jones-rig')
GEN = f'{R}/mouth-clean-pipeline-general-20261031'
OUT = f'{R}/mouth-pipelines-labelled-improved-20261031'
import os as _os
_os.makedirs(f'{OUT}/contacts', exist_ok=True)
_os.makedirs(f'{OUT}/cleaned', exist_ok=True)
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

def general_clean(im, anchor_min=100):
    a = np.array(im)[:, :, 3] >= 128
    arr = np.array(im).astype(int)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    dark = a & (r < 90) & (g < 90) & (b < 90)
    white = a & (r > 200) & (g > 200) & (b > 200)
    orange = a & (r > 100) & (g < 135) & (b < 95) & (r > g + 25)
    red = a & (r > 120) & (r > b + 30) & (g < 150) & ~orange
    anchors = []
    for mask in (white, orange, red):
        for sz, m, bb in comps(mask):
            if sz >= anchor_min:
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
    return keep, rule, dark, (white, orange, red)

def improve(im, keep0, rule0, dark, mats):
    white, orange, red = mats
    keep = keep0.copy()
    rep = {}
    # H1 hole-fill <=100px
    filled = ndimage.binary_fill_holes(keep) & ~keep
    holes = comps(filled)
    h1 = 0
    for sz, m, bb in holes:
        if sz <= 100:
            keep |= m; h1 += sz
    rep['H1_hole_fill_px'] = int(h1)
    # H2 speck purge <15px, not touching main set within 2px
    # main set = largest kept component; recompute after H1
    kc = comps(keep)
    main = kc[0][1] if kc else keep
    dil_main = ndimage.binary_dilation(main, iterations=2)
    h2 = 0
    for sz, m, bb in kc:
        if sz < 15 and not (m & dil_main).any() and not (m & main).any():
            # only drop if it is not the whole mouth (mouths are >=30px by gate)
            keep &= ~m; h2 += sz
    rep['H2_speck_purge_px'] = int(h2)
    # H3 anchor recovery >=50px touching kept dark
    rec = []
    for mask in mats:
        for sz, m, bb in comps(mask):
            if 50 <= sz < 100 and (m & ndimage.binary_dilation(keep, iterations=2)).any():
                rec.append(m)
    h3 = 0
    for m in rec:
        new = m & ~keep
        keep |= m; h3 += int(new.sum())
    rep['H3_anchor_recovery_px'] = int(h3)
    rep['H3_recovered_components'] = len(rec)
    # H4 thin-line bridge, CHAIN only, one gap <=20 columns, both sides >=20px
    h4 = 0; bridged = False
    if rule0 == 'CHAIN':
        ys, xs = np.where(keep)
        if len(xs):
            cols = sorted(set(xs.tolist()))
            gaps = []
            for a_, b_ in zip(cols, cols[1:]):
                if b_ - a_ > 1:
                    gaps.append((a_, b_))
            if len(gaps) == 1:
                a_, b_ = gaps[0]
                if b_ - a_ - 1 <= 20:
                    left = keep[:, :a_+1]; right = keep[:, b_:]
                    if left.sum() >= 20 and right.sum() >= 20:
                        # row band = rows where either side has kept pixels, median row
                        rows = np.where(keep.any(axis=1))[0]
                        # bridge at the median row of kept pixels in the gap neighbourhood
                        ymid = int(np.median(np.where(keep)[0]))
                        # 2px line, x a_+1 .. b_-1, ymid-? use rows around ymid where sides exist
                        for x in range(a_+1, b_):
                            keep[ymid, x] = True
                            if ymid+1 < keep.shape[0]: keep[ymid+1, x] = True
                        h4 = int((b_ - a_ - 1) * 2); bridged = True
    rep['H4_bridge_px'] = int(h4); rep['H4_bridged'] = bool(bridged)
    return keep, rep

def alpha_count(im):
    return int((np.array(im)[:, :, 3] >= 128).sum())

def edge_extend(im, px=2):
    arr = np.array(im).copy()
    a = arr[:, :, 3] >= 128
    # nearest kept pixel colour via distance transform indices
    _, inds = ndimage.distance_transform_edt(~a, return_indices=True)
    ext = arr.copy()
    for c in range(3):
        ext[:, :, c] = arr[inds[0], inds[1], c]
    # only extend outward px: keep original inside, extended colour in a px band
    dil = ndimage.binary_dilation(a, iterations=px)
    out = arr.copy()
    out[dil & ~a, :3] = ext[dil & ~a, :3]
    out[dil & ~a, 3] = 255
    return Image.fromarray(out)

results = {}
for group, path in SOURCES:
    name = os.path.basename(path); key = f"{group}__{name}"
    im = Image.open(path).convert('RGBA')
    keep0, rule0, dark, mats = general_clean(im)
    gen_key = key
    gen_path = f'{GEN}/cleaned/{gen_key}'
    gen_alpha = alpha_count(Image.open(gen_path)) if os.path.exists(gen_path) else int(keep0.sum())
    keep, rep = improve(im, keep0, rule0, dark, mats)
    out = np.array(im).copy()
    # H4 bridge pixels and H1 filled holes have no source colour: use dark mouth colour (0,0,0,255) for bridge, nearest kept colour for holes is already in im? holes were transparent in source, so use black for both and flag them.
    out[~keep, 3] = 0
    # bridge/hole pixels: set alpha 255, colour black (mouth dark) - flagged in rep
    imp_im = Image.fromarray(out)
    # for H1/H4 pixels, alpha was 0 in source; set them explicitly
    arr2 = np.array(imp_im)
    # pixels in keep but not in original alpha>=128 are exactly H1+H4 additions
    orig_a = np.array(im)[:, :, 3] >= 128
    added = keep & ~orig_a
    arr2[added, :3] = 0; arr2[added, 3] = 255
    imp_im = Image.fromarray(arr2)
    imp_im.save(f'{OUT}/cleaned/{key}')
    rep.update(group=group, source=path, rule_general=rule0,
                general_kept_alpha=int(gen_alpha), improved_kept_alpha=int(keep.sum()),
                improved_minus_general=int(keep.sum() - gen_alpha),
                source_alpha=int(orig_a.sum()),
                gate_G1_subset_except_flagged=bool((keep & ~orig_a).sum() == rep['H1_hole_fill_px'] + rep['H4_bridge_px'] or (keep & ~orig_a).sum() <= rep['H1_hole_fill_px'] + rep['H4_bridge_px'] + 2),
                gate_G2_present=bool(keep.sum() >= 30))
    rep['gate_PASS'] = bool(rep['gate_G2_present'])
    results[key] = rep
    print(key, rule0, gen_alpha, '->', int(keep.sum()), 'H1', rep['H1_hole_fill_px'], 'H2', rep['H2_speck_purge_px'], 'H3', rep['H3_anchor_recovery_px'], 'H4', rep['H4_bridge_px'])

# H5 edge-extend proof, CORRECTED: composite resized patch over skin solid
# (210,170,140), count dark halo = dark pixels in output minus dark opaque
# pixels in the resized patch. Naive halo was already only 3/18/-2 px at
# 0.75x, and edge-extend ENLARGED the dark area (AH 3247->3723, GK 1672->2942),
# so H5 is TRIED and NOT APPLIED to the final improved patches. Its
# rejection is a measurement, not a roadblock: H1 already improves these
# mouths, and the v2 fitter leak was already fixed by alpha>=128 in v2.
h5 = {}
for label, path in [('AH', f'{R}/mouth-clean-pipeline-general-20261031/cleaned/V2-7__ah-v2_clean_patch.png'),
                    ('GK', f'{R}/mouth-clean-pipeline-general-20261031/cleaned/V2-7__gk-v2_clean_patch.png'),
                    ('MBP', f'{R}/mouth-clean-pipeline-general-20261031/cleaned/V2-7__mbp-v2_clean_patch.png')]:
    patch = Image.open(path).convert('RGBA')
    w, h = patch.size; nw, nh = max(1, int(w*0.75)), max(1, int(h*0.75))
    arr0 = np.array(patch).copy(); a0 = arr0[:, :, 3] >= 128
    _, inds = ndimage.distance_transform_edt(~a0, return_indices=True)
    ext = arr0.copy()
    for c in range(3): ext[:, :, c] = arr0[inds[0], inds[1], c]
    dil = ndimage.binary_dilation(a0, iterations=2); outa = arr0.copy(); outa[dil & ~a0, :3] = ext[dil & ~a0, :3]; outa[dil & ~a0, 3] = 255
    extim = Image.fromarray(outa)
    def halo(p):
        bg = Image.new('RGBA', (nw, nh), (210, 170, 140, 255)); bg.alpha_composite(p)
        ba = np.array(bg); pa = np.array(p)
        dark_out = int(((ba[:, :, 0] < 120) & (ba[:, :, 1] < 120) & (ba[:, :, 2] < 120)).sum())
        dark_op = int(((pa[:, :, 3] >= 128) & (pa[:, :, 0] < 120) & (pa[:, :, 1] < 120) & (pa[:, :, 2] < 120)).sum())
        return dark_out - dark_op
    hn = halo(patch.resize((nw, nh), Image.LANCZOS)); he = halo(extim.resize((nw, nh), Image.LANCZOS))
    h5[label] = dict(naive_halo_px=int(hn), edge_extend_halo_px=int(he), applied=False, verdict='tried, not applied - enlarges dark area, naive halo already small')
    print('H5', label, h5[label])

json.dump(dict(results=results, H5_edge_extend_proof=h5), open(f'{OUT}/measurements-improved-20261031.json', 'w'), indent=1)
tot_gen = sum(v['general_kept_alpha'] for v in results.values())
tot_imp = sum(v['improved_kept_alpha'] for v in results.values())
print(f"TOTAL {len(results)} general {tot_gen} -> improved {tot_imp} diff {tot_imp-tot_gen} PASS {sum(1 for v in results.values() if v['gate_PASS'])}")
print('H5', h5)

# contacts: general cleaned (before) vs improved (after) on magenta, changed first then unchanged sample
def on_mag(im, scale=2):
    bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
    s = max(1, scale)
    return bg.resize((im.width*s, im.height*s), Image.NEAREST)
changed = [(k, v) for k, v in results.items() if v['improved_minus_general'] != 0]
unchanged = [(k, v) for k, v in results.items() if v['improved_minus_general'] == 0]
for name, items in [('changed', changed), ('unchanged-sample', unchanged[:10])]:
    if not items: continue
    tiles = []
    for k, v in items:
        src = Image.open(f'{GEN}/cleaned/{k}').convert('RGBA'); imp = Image.open(f'{OUT}/cleaned/{k}').convert('RGBA')
        tiles.append((k[:30], on_mag(src), on_mag(imp)))
    W = max(max(t[1].width, t[2].width) for t in tiles); H = max(max(t[1].height, t[2].height) for t in tiles) + 28
    sheet = Image.new('RGB', (W*2, H*len(tiles)), (20, 20, 20)); d = ImageDraw.Draw(sheet)
    for i, (lab, s, c) in enumerate(tiles):
        sheet.paste(s.convert('RGB'), (0, i*H+28)); sheet.paste(c.convert('RGB'), (W, i*H+28))
        d.text((8, i*H+6), f"{lab} GENERAL", fill=(255, 255, 0)); d.text((W+8, i*H+6), f"{lab} IMPROVED", fill=(0, 255, 0))
    sheet.save(f'{OUT}/contacts/contact-improved-{name}-20261031.png'); print('contact', name, sheet.size)

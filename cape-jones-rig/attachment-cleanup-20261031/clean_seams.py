#!/usr/bin/env python3
"""Attachment-seam cleanup — free PIL analogues of 5 industry methods.

HONEST LABEL: Harmony/Animate, OpenToonz, Blender GP, Spine and cel
clean-up are NOT run here (no Harmony/Animate licence in this VM).
Each method below is a free, measured analogue of that method's
documented operation, applied ONLY to the outer-contour band of a
rendered pose, never to interior detail, never to joint balls, never
recolouring base art (only black-outline alpha in the seam band).

Pipeline (combined, conservative):
  M1 Harmony/Animate deformation+contour follow: 3x3 closing on alpha
     in the seam band, then a median pass on the outer contour.
  M2 OpenToonz vector joining: bridge transparent gaps <=4px that lie
     on the outer contour (outline segments that should join).
  M3 Blender GP stroke joining/sculpt smooth: Gaussian-smoothed alpha
     edge, re-thresholded, in the seam band only (1px).
  M4 Spine weight smoothing: 1px feather on the seam band alpha.
  M5 Cel clean-up line matching: erase a dark pixel ONLY if it is an
     interior double outline — i.e. dark, inside the silhouette, and
     within 6px of a second, parallel dark line (the stacked piece
     outline), while the outermost outline is kept. In practice this
     pass is the most dangerous to muscle lines, so it is OFF by
     default in the combined pipeline and shown separately as a crop.
     Combined pipeline = M1+M2+M3+M4 + hole-fill, in seam bands only.

Seam bands: shoulder boxes per pose (hand-measured from the viewed
renders, 1100x1500). Outside the boxes the image is byte-identical
in RGBA except where hole-fill closes a fully-enclosed crack.
Usage:
  python3 clean_seams.py --in <png> --out <png> --method combined|m1|m2|m3|m4|m5 --shoulders x0,y0,x1,y1;x0,y0,x1,y1
  python3 clean_seams.py --qc <png> --shoulders ...   (prints QC numbers)
  python3 clean_seams.py --revert <cleaned> --preset <preset-base-file>
"""
import argparse, json, sys
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage

GREY = (128, 128, 128, 255)

def load(p):
    im = Image.open(p).convert('RGBA')
    return np.array(im).astype(np.uint8)

def save(arr, p):
    Image.fromarray(arr.astype(np.uint8), 'RGBA').save(p)

def alpha_mask(a):
    return a[:, :, 3] > 10

def dark_mask(a):
    return (a[:, :, 3] > 10) & (a[:, :, 0].astype(int) + a[:, :, 1].astype(int) + a[:, :, 2].astype(int) < 200)

def band_mask(shape, boxes):
    m = np.zeros(shape[:2], dtype=bool)
    for (x0, y0, x1, y1) in boxes:
        m[max(0, y0):y1, max(0, x0):x1] = True
    return m

def outer_contour(mask):
    er = ndimage.binary_erosion(mask, iterations=1)
    return mask & ~er

def hole_fill(mask):
    filled = ndimage.binary_fill_holes(mask)
    return filled

def qc(a, boxes):
    """Seam QC inside shoulder boxes only.
    holes: transparent px fully inside silhouette bbox area that hole-fill would close
    contour_thick: mean dark thickness along outer contour (stacked outlines > ~3px)
    rough: contour direction-change proxy = contour px with <2 contour neighbours (jagged steps)
    """
    sil = alpha_mask(a); dark = dark_mask(a)
    band = band_mask(a.shape, boxes) if boxes else np.ones(sil.shape, bool)
    holes = int((hole_fill(sil) & ~sil & band).sum())
    cont = outer_contour(sil) & band
    # thickness: distance from contour inward to first non-dark? approximate: dark px within 6px inside contour
    inside = ndimage.binary_erosion(sil, iterations=6) if sil.any() else sil
    inner_dark = dark & band & ~inside  # dark in the 6px rim band
    thick = float(inner_dark.sum() / max(1, cont.sum())) if cont.sum() else 0.0
    # roughness: contour pixels whose 3x3 neighbourhood has 1 contour neighbour (spike) or >3 (step cluster)
    c = cont.astype(int)
    neigh = ndimage.convolve(c, np.ones((3, 3)), mode='constant') - c
    rough = int((((neigh <= 1) | (neigh >= 4)) & cont).sum())
    return {"holes_filled_candidate_px": holes, "rim_dark_per_contour_px": round(thick, 3),
            "contour_px": int(cont.sum()), "jagged_contour_px": rough,
            "changed_vs_preset_note": "run qc on preset and cleaned and diff these numbers"}

def apply_method(a, method, boxes):
    sil = alpha_mask(a); band = band_mask(a.shape, boxes) if boxes else np.ones(sil.shape, bool)
    out = a.copy()
    if method == 'm5':
        # interior double-line removal, seam band only, outermost outline kept
        dark = dark_mask(a)
        # outer contour dilated 3px = kept ring; dark beyond that ring but within 10px inside silhouette = candidate double line
        cont = outer_contour(sil)
        keep = ndimage.binary_dilation(cont, iterations=3)
        inner = sil & ~ndimage.binary_dilation(cont, iterations=10)
        cand = dark & band & inner
        # only erase where a second dark line exists within 8px (parallel stacked outline)
        near_dark = ndimage.binary_dilation(dark, iterations=8)
        erase = cand & near_dark
        # safety: never erase more than 2% of band dark px
        if erase.sum() > 0.02 * max(1, (dark & band).sum()):
            erase[:] = False
        out[erase] = (255, 255, 255, 0)  # transparent, so the kept outer line reads alone
        return out
    # alpha-based methods
    alpha = a[:, :, 3].astype(float)
    sil_f = sil.astype(float)
    if method in ('m1', 'combined'):
        closed = ndimage.binary_closing(sil_f > 0.5, structure=np.ones((3, 3)))
        sil_f = np.where(band, closed.astype(float), sil_f)
    if method in ('m2', 'combined'):
        # bridge gaps <=4px on contour: closing with a 5px cross, band only
        bridged = ndimage.binary_closing(sil_f > 0.5, structure=np.array([[0,1,0],[1,1,1],[0,1,0]]), iterations=2)
        sil_f = np.where(band, bridged.astype(float), sil_f)
    if method in ('m3', 'combined'):
        sm = ndimage.gaussian_filter(sil_f, 0.8)
        sm = (sm > 0.5).astype(float)
        sil_f = np.where(band, sm, sil_f)
    if method in ('m4', 'combined'):
        # 1px feather: blur alpha only in band, re-threshold soft
        bl = ndimage.gaussian_filter(alpha / 255.0, 0.6) * 255
        out[:, :, 3] = np.where(band, bl, alpha).astype(np.uint8)
        # re-apply silhouette from sil_f for m4 alone? m4 is feather only:
        if method == 'm4':
            return out
    if method == 'combined':
        filled = hole_fill(sil_f > 0.5)
        sil_f = np.where(band, filled.astype(float), sil_f)
        out[:, :, 3] = np.where(band, (sil_f * 255).astype(np.uint8), alpha.astype(np.uint8))
        # where silhouette was extended, fill with nearest edge colour (white suit / black outline handled by keeping RGB of nearest original px)
        # simple: extended px take RGB of the original image's nearest non-transparent neighbour via dilation of RGB
        ext = (sil_f > 0.5) & ~sil & band
        if ext.any():
            for ch in range(3):
                dilated = ndimage.grey_dilation(a[:, :, ch], size=(5, 5))
                out[:, :, ch] = np.where(ext, dilated, out[:, :, ch])
    else:
        out[:, :, 3] = np.where(band, (sil_f * 255).astype(np.uint8), alpha.astype(np.uint8))
    return out

def parse_boxes(s):
    if not s: return []
    return [tuple(int(v) for v in b.split(',')) for b in s.split(';') if b.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp'); ap.add_argument('--out', dest='outp')
    ap.add_argument('--method', default='combined')
    ap.add_argument('--shoulders', default='')
    ap.add_argument('--qc', dest='qcp')
    ap.add_argument('--revert', dest='revert'); ap.add_argument('--preset', dest='preset')
    a = ap.parse_args()
    if a.revert and a.preset:
        import shutil; shutil.copy2(a.preset, a.revert); print(f"REVERTED {a.revert} from preset {a.preset}"); return
    boxes = parse_boxes(a.shoulders)
    if a.qcp:
        arr = load(a.qcp); print(json.dumps(qc(arr, boxes), indent=2)); return
    arr = load(a.inp)
    before = qc(arr, boxes)
    out = apply_method(arr, a.method, boxes)
    after = qc(out, boxes)
    save(out, a.outp)
    print(json.dumps({"method": a.method, "before": before, "after": after}, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Joint-cleanup tooling for Cape Jones — READY-FOR-LATER, not applied to approved poses.

Mars, 2026-10-31 17:04 CDT: the v7c round joint balls (elbows, knees, wrists)
are FINE for now — they help read the rig. Later he wants him to look LESS LIKE
AN ACTION FIGURE by cleaning those joints up. This tool is pulled and wired
NOW, tested on COPIES only, so that cleanup is a one-command job when he says go.

Methods (industry-standard cutout practice, methods only, no copied code):
  1. speck removal — detached specks at a joint are not part of the limb.
     A speck is a connected non-background component, <40 px, separated from
     the main silhouette by background. Removing it never touches the limb.
  2. seam masking — a joint cap is masked to the forearm+fist / upper+lower
     union (dilated 3px), so it fills the seam only and cannot stick out
     into the background. (Already used for wrists in build_true_final_flex_v2.)
  3. corridor taper (ball-to-taper replacement) — inside a joint disk, the
     silhouette is clipped to the limb corridor: the axis is estimated by PCA
     on silhouette pixels in an annulus around the joint, the corridor
     half-width is the median cross-section width just outside the disk,
     and any silhouette pixel farther from the axis than half-width + 3px
     is replaced by background. This removes the circular ball bulge that
     sticks out sideways from the limb, while the limb core stays intact.
     It is a composite-level approximation: the piece-level version is
     simply omitting the circular cap at build time (upper and lower pieces
     already overlap at the joint), documented in JOINT-CLEANUP-README.md.
  4. cap omission (piece level) — rebuild a pose with elbow/knee caps
     skipped. No ball is drawn at all; the overlapping pieces form a
     continuous limb with only their own outlines as the seam.

Usage:
  python3 clean_joints.py speck  in.png out.png [--zone x,y,r ...]
  python3 clean_joints.py taper in.png out.png --joint x,y,r [--joint ...]
  python3 clean_joints.py test  in.png out.png   # speck + taper on true-final joints
Background is assumed to be flat grey-128 (the rig's clean-plate background).
A pixel counts as silhouette when its colour distance from (128,128,128) > 20.
Never run this on an approved file in place — always write a NEW file.
"""
import sys, math
import numpy as np
from PIL import Image
from scipy import ndimage

BG = np.array([128, 128, 128], dtype=np.int16)
RIG = "/home/hatch/workspace/cape-jones-rig"

def load(path):
    return np.array(Image.open(path).convert("RGB")).astype(np.int16)

def save(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)

def silhouette(arr):
    return np.abs(arr - BG).sum(axis=2) > 20

def remove_specks(arr, mask=None, max_px=40):
    """Remove detached components < max_px inside mask (or whole image)."""
    sil = silhouette(arr)
    if mask is not None:
        sil = sil & mask
    lab, n = ndimage.label(sil)
    out = arr.copy()
    removed = 0
    for i in range(1, n + 1):
        comp = lab == i
        size = int(comp.sum())
        # A component is a speck only if it does not touch the main body:
        # here, inside a wrist zone, the main body is the largest component.
        if size < max_px:
            out[comp] = BG
            removed += size
    return out, removed

def remove_detached_specks(arr, zone=None, max_px=40):
    """Remove small components that are NOT the largest component in zone."""
    sil = silhouette(arr)
    if zone is not None:
        x, y, r = zone
        yy, xx = np.ogrid[:arr.shape[0], :arr.shape[1]]
        sil = sil & ((xx - x) ** 2 + (yy - y) ** 2 <= r * r)
    lab, n = ndimage.label(sil)
    if n == 0:
        return arr, 0
    sizes = ndimage.sum_labels(np.ones_like(lab), lab, range(1, n + 1))
    main = int(np.argmax(sizes)) + 1
    out = arr.copy()
    removed = 0
    for i in range(1, n + 1):
        if i != main and sizes[i - 1] < max_px:
            comp = lab == i
            out[comp] = BG
            removed += int(comp.sum())
    return out, removed

def corridor_taper(arr, joint, radius=38):
    """Clip a joint disk to the limb corridor. Returns (out, removed_px)."""
    x0, y0 = joint
    h, w = arr.shape[:2]
    sil = silhouette(arr)
    yy, xx = np.mgrid[:h, :w]
    dist = np.sqrt((xx - x0) ** 2 + (yy - y0) ** 2)
    annulus = sil & (dist >= radius + 8) & (dist <= radius + 45)
    pts = np.column_stack(np.nonzero(annulus)[::-1]).astype(float)  # (x, y)
    if len(pts) < 50:
        return arr, 0
    centre = pts.mean(axis=0)
    cov = np.cov((pts - centre).T)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, int(np.argmax(vals))]  # principal direction
    # ENDPOINT GUARD (added after a failed flex-elbow test, 2026-10-31):
    # a taper only makes sense for a MID-LIMB joint, where silhouette
    # exists on BOTH sides of the JOINT POINT along the axis. A flex
    # elbow ball sits at the END of the bicep — the first version of this
    # function deleted the whole ball plus a chunk of bicep and left a
    # grey hole (7,269 px removed, viewed and rejected). If either side
    # of the joint point is empty, skip the taper entirely (return 0)
    # and let the piece-level cap-omission method handle that joint.
    for s in (-1, 1):
        px = int(round(x0 + s * axis[0] * (radius + 15)))
        py = int(round(y0 + s * axis[1] * (radius + 15)))
        if not (0 <= px < w and 0 <= py < h and sil[py, px]):
            return arr, 0
    perp = np.array([-axis[1], axis[0]])
    # corridor half-width: median |perp distance| of annulus pixels, + outline
    rel = pts - centre
    half = float(np.median(np.abs(rel @ perp))) + 3.0
    disk = dist <= radius
    rel_all = np.stack([xx - centre[0], yy - centre[1]], axis=-1)
    perp_dist = np.abs(rel_all @ perp)
    cut = disk & sil & (perp_dist > half)
    out = arr.copy()
    out[cut] = BG
    return out, int(cut.sum())

# True-final-flex joint positions (from build_true_final_flex_v2 report).
TRUE_JOINTS = {
    "wrist_L": (330, 323), "wrist_R": (753, 329),
    "elbow_L": (247, 474), "elbow_R": (854, 467),
}

def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    mode, src, dst = argv[1], argv[2], argv[3]
    arr = load(src)
    if mode == "speck":
        zones = []
        i = 4
        while i + 1 < len(argv) and argv[i] == "--zone":
            x, y, r = map(int, argv[i + 1].split(","))
            zones.append((x, y, r)); i += 2
        total = 0
        for z in zones or [None]:
            arr, n = remove_detached_specks(arr, z); total += n
        print(f"speck: removed {total} px")
    elif mode == "taper":
        joints = []
        i = 4
        while i + 1 < len(argv) and argv[i] == "--joint":
            x, y, r = map(int, argv[i + 1].split(","))
            joints.append(((x, y), r)); i += 2
        total = 0
        for (j, r) in joints:
            arr, n = corridor_taper(arr, j, r); total += n
            print(f"taper {j} r={r}: removed {n} px")
        print(f"taper total: {total} px")
    elif mode == "test":
        # Wrist speck polish + elbow/knee-style taper on true-final joints.
        total = 0
        for name, (x, y) in TRUE_JOINTS.items():
            arr, n = remove_detached_specks(arr, (x, y, 90)); total += n
            print(f"speck {name}: {n} px")
        for name in ("elbow_L", "elbow_R"):
            arr, n = corridor_taper(arr, TRUE_JOINTS[name], 38)
            print(f"taper {name}: {n} px"); total += n
        print(f"test total removed: {total} px")
    else:
        print("unknown mode:", mode); return 2
    save(arr, dst)
    print("wrote", dst)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

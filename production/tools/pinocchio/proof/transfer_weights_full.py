#!/usr/bin/env python3
# transfer_weights_full.py — map Pinocchio weights from a decimated mesh
# back onto the full-resolution mesh via nearest-vertex lookup.
#
# Usage:
#   python3 transfer_weights_full.py <full.obj> <dec.obj> <weights_dec.bin> <weights_full_out.bin>
#
# Reads vertex positions straight from the OBJ files (no Blender needed).
# Output format identical to rig's weights.bin (int32 nv, int32 nj, float32 rows).
# Requires: numpy, scipy.

import struct, sys
import numpy as np
from scipy.spatial import cKDTree

def read_obj_verts(path):
    verts = []
    with open(path) as f:
        for line in f:
            if line.startswith("v "):
                verts.append([float(x) for x in line.split()[1:4]])
    return np.asarray(verts, dtype=np.float64)

def read_weights(path):
    with open(path, "rb") as f:
        nv, nj = struct.unpack("ii", f.read(8))
        w = np.fromfile(f, dtype=np.float32, count=nv * nj).reshape(nv, nj)
    return w, nv, nj

def main():
    full_p, dec_p, wdec_p, out_p = sys.argv[1:5]
    print("[xfer] reading OBJs...", flush=True)
    vf = read_obj_verts(full_p)
    vd = read_obj_verts(dec_p)
    w, nvd, nj = read_weights(wdec_p)
    assert nvd == len(vd), f"dec weight rows {nvd} != dec verts {len(vd)}"
    print(f"[xfer] full verts={len(vf)} dec verts={len(vd)} joints={nj}", flush=True)
    print("[xfer] building KD-tree...", flush=True)
    tree = cKDTree(vd)
    print("[xfer] querying nearest neighbors...", flush=True)
    _, idx = tree.query(vf, k=1, workers=-1)
    wf = w[idx].astype(np.float32)
    print(f"[xfer] mean nearest distance: {np.linalg.norm(vf - vd[idx], axis=1).mean():.6f}", flush=True)
    with open(out_p, "wb") as f:
        f.write(struct.pack("ii", len(vf), nj))
        wf.tofile(f)
    print(f"[xfer] wrote {out_p}", flush=True)

if __name__ == "__main__":
    main()

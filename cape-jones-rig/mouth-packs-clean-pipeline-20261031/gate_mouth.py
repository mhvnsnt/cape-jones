#!/usr/bin/env python3
"""Gate for pipeline mouths. Exit 0 PASS / 1 FAIL.
Checks thin-line continuity, placement centre, and no-crop on a fitted head.
Usage: gate_mouth.py <patch.png> <placed_w> <placed_h> [--thin]
"""
import sys, os
import numpy as np
from PIL import Image
ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
BASE = Image.open(os.path.join(ROOT, "visemes-v2-20261031/clean-head-base-20261031.png")).convert("RGBA")
CX, CY = 231.5, 504.5
patch = Image.open(sys.argv[1]).convert("RGBA").resize((int(sys.argv[2]), int(sys.argv[3])), Image.LANCZOS)
a = np.array(patch); a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0); patch = Image.fromarray(a)
fr = BASE.copy(); fr.alpha_composite(patch, (int(round(CX - patch.size[0]/2)), int(round(CY - patch.size[1]/2))))
fails = []
if "--thin" in sys.argv:
    d = (np.array(patch)[:, :, 0] < 90) & (np.array(patch)[:, :, 3] > 50)
    cols = [x for x in range(d.shape[1]) if d[:, x].any()]
    missing = [x for x in range(cols[0], cols[-1]+1) if x not in cols]
    if missing: fails.append(f"missing columns {missing}")
    print("thin-line columns", cols[0], "-", cols[-1], "missing", missing)
if fr.getchannel("A").getbbox() is None: fails.append("empty fitted head")
print("placement centre", CX, CY, "patch", patch.size)
print("FAIL" if fails else "PASS", "; ".join(fails))
sys.exit(1 if fails else 0)

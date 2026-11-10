"""Crossed white-outline poses for BOTH Cape Consumed versions.
SYMBIOTE WHITE-OUTLINE RULE: front part gets WHITE outline anytime body
crosses in front of itself, mandatory, not decoration. Applies to bare
(no cape) AND upper-only (collar only) alike.
Reuses build_base (patched capeless builder) + its white_outline().
"""
import os, sys, json
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_base import build, blacken, apply_symbol, bbox, CROSS, white_outline

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(ROOT, "cape-consumed-bare-upper-20261031")

def grey(im, path):
    bg = Image.new("RGBA", im.size, (128, 128, 128, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(path)

meas = json.load(open(os.path.join(OUT, "measurements-20261031.json")))
meas["crossed_white_outline"] = {}
for mode, label in (("none", "bare"), ("collar", "upper_only")):
    cross, behind, front = build(CROSS, cape_mode=mode)
    cross_b, m = blacken(cross)
    cross_s, sym = apply_symbol(cross_b, m)
    behind_b, _ = blacken(behind)
    front_b, _ = blacken(front)
    ring, ring_px, overlap_px, full_ring_px = white_outline(front_b, behind_b, width=4)
    out = np.asarray(cross_s).copy()
    out[ring, :3] = np.array([255, 255, 255], dtype=np.uint8)
    out[ring, 3] = 255
    white = Image.fromarray(out, "RGBA")
    white.save(os.path.join(OUT, f"cape-consumed-{label}-crossed-WHITE-OUTLINE-20261031.png"))
    grey(white, os.path.join(OUT, f"cape-consumed-{label}-crossed-WHITE-OUTLINE-20261031-on-grey.png"))
    meas["crossed_white_outline"][label] = {
        "config": "v7c arm_upper L40/R-40, arm_lower L120/R-120, legs apose",
        "cape_back_main_present": False,
        "cape_collar_present": mode == "collar",
        "crossed_alpha_px": int(m.sum()),
        "crossed_bbox": bbox(cross),
        "front_forearm_alpha_px": int((np.asarray(front)[..., 3] > 10).sum()),
        "front_over_behind_overlap_px": overlap_px,
        "white_crossing_ring_px_width4": ring_px,
        "full_ring_px_width4_for_reference": full_ring_px,
        "symbol_white_px": sym,
    }
    print(label, meas["crossed_white_outline"][label])

with open(os.path.join(OUT, "measurements-20261031.json"), "w") as f:
    json.dump(meas, f, indent=2)
print("done")

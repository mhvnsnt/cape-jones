"""COWL-SNAP, UPPER-ONLY (refined 2026-10-31): the buried segment is the BICEP.
Upper arm is drawn AFTER collar/torso (above collar), lower arm stays in its
normal position (after torso, BEFORE head). This fixes a collar-cut bicep
without covering the face — the whole-chain version would wrongly cover
JoJo 02's face (see audit). Same angles, same pieces, no redrawn art.
"""
import os, sys
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031")
from test_snaps import figure, BASE, CUT
from PIL import Image
OUT="/home/hatch/workspace/cape-jones-rig/face-cowl-snap-wire100-20261031"
# figure() in test_snaps supports snap face/cowl as whole-chain; for upper-only we
# re-implement by rendering normal then compositing ONLY the upper layers on top.
# Simpler and exact: render with snap='cowl' (whole chain on top) for these two
# poses, where lower_vs_head=0, so lower-on-top vs lower-normal are identical.
# Verify that claim below by comparing against a lower-normal render.
import test_snaps as ts
# Monkey-patch: build a variant where cowl = upper only, lower normal.
import math
from PIL import Image as PILImage
def figure_cowl_upper(cx, cfg, head=0, sides=("L","R")):
    c = ts.figure(cx, cfg, head, snap=None)
    # draw upper arms on top of everything (collar + torso + head edge) at same
    # positions as the normal render: recompute shoulder/elbow from cfg
    for side in sides:
        ball, sh_anchor = ts.ARM[side]
        shoulders={"L":(cx-120,445),"R":(cx+120,445)}
        sh=shoulders[side]
        up,_,cap = ts.ARM_PIECES[side]
        ts.limb(c, os.path.join(CUT,up), sh, cfg["arm_upper"][side], sh_anchor)
    return c

FIXES = [
 ("ginyu-03-dance-shimmy-hips-out", {"arm_upper":{"L":-130,"R":130},"arm_lower":{"L":-60,"R":60},"leg_upper":{"L":-20,"R":35},"leg_lower":{"L":30,"R":-20}}, 10),
 ("v7c-jump-arms-up", {"arm_upper":{"L":-150,"R":150},"arm_lower":{"L":-150,"R":150},"leg_upper":{"L":-20,"R":20},"leg_lower":{"L":45,"R":-45}}, 0),
]
for name, cfg, head in FIXES:
    fixed = figure_cowl_upper(550, cfg, head)
    fixed.save(f"{OUT}/{name}-COWL-SNAP-20261031.png")
    # compare vs whole-chain snapped test render (where available)
    whole = f"{OUT}/test-{'ginyu-03' if 'ginyu' in name else 'v7c-jump'}-snapped-20261031.png"
    if os.path.exists(whole):
        import numpy as np
        a=np.array(fixed.convert("RGB")).astype(int); b=np.array(PILImage.open(whole).convert("RGB")).astype(int)
        print(name, "vs whole-chain snapped rgb-diff>20:", int((np.abs(a-b).max(axis=2)>20).sum()))
    print(name, "saved")

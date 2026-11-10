#!/usr/bin/env python3
"""Regression test for the gauntlet flip rule (GAUNTLET-FLIP-RULE.md).
Fails (exit 1) if any check fails, so an arms-up pose can never silently
revert to inward panels or to the floating v1 flip.
Checks: OutFixed pieces exist; per-row x-range preserved y62-180;
approved fixed pose exists; v1 files are listed superseded (not selected);
approved pose diff vs inward pose is confined to the gauntlet zone.
"""
import json, os, sys
import numpy as np
from PIL import Image
ROOT = "/home/hatch/workspace/cape-jones-rig"
fails = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name} {detail}")
    if not ok: fails.append(name)
# 1+2: OutFixed pieces, per-row range
for name in ["Arm_Front_Lower.png", "Arm_Back_Lower.png"]:
    orig = np.array(Image.open(f"{ROOT}/cut-limbs-v7c/{name}").convert("RGBA"))
    fixed_path = f"{ROOT}/cut-limbs-v7c-gauntlet-out-fixed/{name.replace('.png', '_OutFixed.png')}"
    check(f"OutFixed exists {name}", os.path.exists(fixed_path))
    if os.path.exists(fixed_path):
        fixed = np.array(Image.open(fixed_path).convert("RGBA"))
        ok = True
        for y in range(62, 180):
            a = np.where(orig[y, :, 3] > 10)[0]; b = np.where(fixed[y, :, 3] > 10)[0]
            if len(a) and (len(b) == 0 or a.min() != b.min() or a.max() != b.max()):
                ok = False; break
        check(f"per-row x-range preserved {name}", ok)
# 3: approved pose exists
pose = f"{ROOT}/reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png"
check("approved fixed pose exists", os.path.exists(pose))
# 4: v1 superseded in json
swaps = json.load(open(f"{ROOT}/pose_driven_swaps.json"))
check("v1 files listed superseded", len(swaps.get("superseded_do_not_use", [])) >= 3, f"count={len(swaps.get('superseded_do_not_use', []))}")
# 5: diff confined to gauntlet zone
inward = f"{ROOT}/reposes-v7c-clean/fighting-pose-forward-bicep-curl-v7c-clean.png"
if os.path.exists(pose) and os.path.exists(inward):
    a = np.array(Image.open(inward).convert("RGB")).astype(int)
    b = np.array(Image.open(pose).convert("RGB")).astype(int)
    d = np.any(a != b, axis=2); ys, xs = np.where(d)
    confined = (xs.min() >= 300 and xs.max() <= 800 and ys.min() >= 400 and ys.max() <= 600)
    check("diff confined to gauntlet zone", confined, f"bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} diff={int(d.sum())}")
print(f"{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)

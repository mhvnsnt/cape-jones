#!/usr/bin/env python3
"""Stage the true-prop-separation v2 deliverables into a tree that mirrors
the repo paths, ready to land on branch true-prop-separation-20261123.
PSDs (~50 MB each) are NOT staged here — they go to a GitHub Release
(see docs/TRUE-PROP-SEPARATION.md)."""
import os
import shutil
import hashlib
import json

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
TS = os.path.join(WD, "true-sep")
STAGE = os.path.join(TS, "stage")

# (source, staged repo path)
FILES = [
    # plate set
    ("plate/background-complete.png", "production/2d-parking-lot/purple-lot-layered-v2/background-complete.png"),
    ("plate/composite-sodium.png", "production/2d-parking-lot/purple-lot-layered-v2/composite-sodium.png"),
    ("plate/composite-purple.png", "production/2d-parking-lot/purple-lot-layered-v2/composite-purple.png"),
    ("plate/proof-moved-car.png", "production/2d-parking-lot/purple-lot-layered-v2/proof-moved-car.png"),
    ("plate/background.json", "production/2d-parking-lot/purple-lot-layered-v2/background.json"),
    ("plate/masks.json", "production/2d-parking-lot/purple-lot-layered-v2/masks.json"),
    ("plate/mask-qa.png", "production/2d-parking-lot/purple-lot-layered-v2/mask-qa.png"),
    # plate prop + shadow layers
    ("plate/layers/blue_car_mid.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/blue_car_mid.png"),
    ("plate/layers/cars_left_row.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/cars_left_row.png"),
    ("plate/layers/cars_right_row.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/cars_right_row.png"),
    ("plate/layers/stop_sign.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/stop_sign.png"),
    ("plate/layers/street_lamp_far.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/street_lamp_far.png"),
    ("plate/layers/street_lamp_right.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/street_lamp_right.png"),
    ("plate/layers/car_shadows.png", "production/2d-parking-lot/purple-lot-layered-v2/layers/car_shadows.png"),
    # board 01 set
    ("boards/cj-pl-01/background-complete.png", "production/2d-parking-lot/boards-layered/cj-pl-01/background-complete.png"),
    ("boards/cj-pl-01/composite-sodium.png", "production/2d-parking-lot/boards-layered/cj-pl-01/composite-sodium.png"),
    ("boards/cj-pl-01/composite-purple.png", "production/2d-parking-lot/boards-layered/cj-pl-01/composite-purple.png"),
    ("boards/cj-pl-01/background.json", "production/2d-parking-lot/boards-layered/cj-pl-01/background.json"),
    ("boards/cj-pl-01/masks.json", "production/2d-parking-lot/boards-layered/cj-pl-01/masks.json"),
    ("boards/cj-pl-01/mask-qa.png", "production/2d-parking-lot/boards-layered/cj-pl-01/mask-qa.png"),
    ("boards/cj-pl-01/layers/blue_car_mid.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/blue_car_mid.png"),
    ("boards/cj-pl-01/layers/cars_left_row.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/cars_left_row.png"),
    ("boards/cj-pl-01/layers/cars_right_row.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/cars_right_row.png"),
    ("boards/cj-pl-01/layers/jones.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/jones.png"),
    ("boards/cj-pl-01/layers/stop_sign.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/stop_sign.png"),
    ("boards/cj-pl-01/layers/street_lamp_far.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/street_lamp_far.png"),
    ("boards/cj-pl-01/layers/street_lamp_right.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/street_lamp_right.png"),
    ("boards/cj-pl-01/layers/car_shadows.png", "production/2d-parking-lot/boards-layered/cj-pl-01/layers/car_shadows.png"),
    # pipeline scripts
    ("segment.py", "rig/true-prop-separation/segment.py"),
    ("complete_bg.py", "rig/true-prop-separation/complete_bg.py"),
    ("build_psd.py", "rig/true-prop-separation/build_psd.py"),
    ("proof_moved_car.py", "rig/true-prop-separation/proof_moved_car.py"),
    ("stage_tree.py", "rig/true-prop-separation/stage_tree.py"),
    # docs
    ("TRUE-PROP-SEPARATION.md", "docs/TRUE-PROP-SEPARATION.md"),
    ("GUMBALL-BACKGROUNDS-USE.md", "docs/GUMBALL-BACKGROUNDS-USE.md"),
]
# shared light/grade layers (v1 synthetics, stored once)
for f in sorted(os.listdir(os.path.join(TS, "light"))):
    FILES.append((f"light/{f}",
                  f"production/2d-parking-lot/purple-lot-layered-v2/light/{f}"))

if os.path.exists(STAGE):
    shutil.rmtree(STAGE)
manifest = []
total = 0
for src, dst in FILES:
    s = os.path.join(TS, src)
    d = os.path.join(STAGE, dst)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copyfile(s, d)
    h = hashlib.sha256(open(d, "rb").read()).hexdigest()
    n = os.path.getsize(d)
    total += n
    manifest.append({"path": dst, "bytes": n, "sha256": h})
    print(f"{n:>10}  {dst}")
manifest.append({"_total_bytes": total, "_files": len(manifest),
                 "_psds_not_in_tree": {
                     "plate/purple-lot-layered-v2.psd": {
                         "bytes": os.path.getsize(os.path.join(TS, "plate", "purple-lot-layered-v2.psd")),
                         "sha256": hashlib.sha256(open(os.path.join(TS, "plate", "purple-lot-layered-v2.psd"), "rb").read()).hexdigest()},
                     "boards/cj-pl-01/cj-pl-01-layered-v2.psd": {
                         "bytes": os.path.getsize(os.path.join(TS, "boards", "cj-pl-01", "cj-pl-01-layered-v2.psd")),
                         "sha256": hashlib.sha256(open(os.path.join(TS, "boards", "cj-pl-01", "cj-pl-01-layered-v2.psd"), "rb").read()).hexdigest()}}})
with open(os.path.join(STAGE, "MANIFEST.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print(f"staged {len(manifest)-1} files, {total} bytes total (+ MANIFEST.json)")
print("PSDs staged for Release upload (not in the tree):")
print("  plate/purple-lot-layered-v2.psd",
      os.path.getsize(os.path.join(TS, "plate", "purple-lot-layered-v2.psd")))
print("  boards/cj-pl-01/cj-pl-01-layered-v2.psd",
      os.path.getsize(os.path.join(TS, "boards", "cj-pl-01", "cj-pl-01-layered-v2.psd")))

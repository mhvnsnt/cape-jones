#!/usr/bin/env python3
"""CJ-01 to CJ-10 plates rebuilt by LAYER REMOVAL ONLY, Mars 2026-11-01 15:59 CST.

Wrong method (superseded, do NOT use): erasing / alpha-zeroing discs out of a
finished PNG, inpainting, rim-hole-fill, cropping. That was shots-CJ01-CJ30-no-orbs-20261101/.

Correct method here:
- Take the exact source rig builders that made the plates:
  * joint_locked_rig_v7b.py (CJ-01, CJ-02, CJ-04, cut-limbs-v7)
    CORRECTED: the clips-v7 punch plates were built with v7b, not v7.
    v7b-stripped matches the labelled source outside the label mask
    exactly, 0 px (per art-owed-punch-plates-20261031). A v7 rebuild
    was tried first and FAILED that check (52-60k px outside mask).
  * joint_locked_rig_v7c.py (CJ-03, CJ-05, CJ-06..CJ-10, cut-limbs-v7c)
- Omit two layers, by code, never by editing a finished image:
  1. labels layer: the red numbered ARM/LEG discs + ARM/LEG text.
     v7c: labels=False (its own flag). v7b: the label-drawing block is
     removed from the exec'd source before it runs.
  2. cap layer: cap_at() replaced with a no-op, for all 4 joints
     (2 elbows, 2 knees). No cap disc is drawn at all.
- Everything else is byte-for-byte the original builder: same pieces,
  same paste order, same anchors, same angles, same grey canvas.
- Then the plates go through the SAME grey->transparent conversion as
  transparent-plates-sweep-20261031/convert_plates.py (bg median, dist>30,
  closing, hole fill, components >=800, 1px feather). That conversion is
  a plate-making step from the source builder, not an eraser on a final.
- Pose configs are from clips/punch-clip.json, clips/walk-clip.json,
  clips/dance-clip.json, plus the arm2-variant name for CJ-05
  (a2l = arm2 lower = -70, impact pose otherwise).

If omitting caps leaves a joint seam, it is left visible and reported.
No patch, no inpaint, no crop, no alpha-zero on the finished plate.
"""
import json, math, os, pathlib
from PIL import Image
import numpy as np
from scipy import ndimage

RIG = pathlib.Path("/home/hatch/workspace/cape-jones-rig")
OUT = RIG / "shots-CJ01-CJ10-layer-removed-20261101"
GREY = OUT / "work" / "grey"
PLATES = OUT / "work" / "plates"
GREY.mkdir(parents=True, exist_ok=True)
PLATES.mkdir(parents=True, exist_ok=True)

def load_builder(path, version):
    src = pathlib.Path(path).read_text()
    if version in ("v7", "v7b"):
        # cut off at first top-level build() call, remove label block
        src = src.split('build("joint-apose-v7')[0]
        # remove ONLY the label drawing block: from "from PIL import ImageDraw"
        # up to (but not including) the canvas.convert save line
        lines = src.splitlines()
        out_lines = []
        skip = False
        for ln in lines:
            if ln.strip().startswith("from PIL import ImageDraw"):
                skip = True
            if skip and ln.strip().startswith("canvas.convert"):
                skip = False
            if skip:
                continue
            out_lines.append(ln)
        src = "\n".join(out_lines)
    else:
        src = src.split('build("joint-apose-v7')[0]
    ns = {}
    exec(src, ns)
    # LAYER REMOVAL 2: cap layer disabled entirely
    ns["cap_at"] = lambda canvas, cap_path, joint: None
    return ns

NS7B = load_builder(RIG / "joint_locked_rig_v7b.py", "v7b")
NS7C = load_builder(RIG / "joint_locked_rig_v7c.py", "v7c")

def cfg(au_l, al_l, au_r, al_r, lu_l, ll_l, lu_r, ll_r):
    return {"arm_upper": {"L": au_l, "R": au_r}, "arm_lower": {"L": al_l, "R": al_r},
            "leg_upper": {"L": lu_l, "R": lu_r}, "leg_lower": {"L": ll_l, "R": ll_r}}

# shot, builder, config, original sweep plate
POSES = [
    ("CJ-01", "v7b", cfg(-20, -120, 20, 160, -10, 10, 10, -10),
     "clips-v7__punch__punch-01-windup-v7.png"),
    ("CJ-02", "v7b", cfg(-90, -90, 20, 160, -15, 15, 15, -15),
     "clips-v7__punch__punch-07-extend-snap-v7.png"),
    # CJ-03 CORRECTED: arm2 lower -110 (Mars-locked punch frame, per
    # art-owed-punch-plates-20261031/build_clean_punch_plates.py), NOT 160.
    # 160 was the extend-snap pose and gave the wrong right arm.
    ("CJ-03", "v7c", cfg(-90, -90, 20, -110, -15, 15, 15, -15),
     "clips-v7c__punch-impact-locked-v7c.png"),
    ("CJ-04", "v7b", cfg(-20, -20, 20, 20, -10, 10, 10, -10),
     "clips-v7__punch__punch-21-recover-v7.png"),
    ("CJ-05", "v7c", cfg(-90, -90, 20, -70, -15, 15, 15, -15),
     "clips-v7c__punch-arm2-variants__punch-impact-a2l-minus70-across-down-v7c.png"),
    ("CJ-06", "v7c", cfg(-25, -25, 15, 15, -25, 5, 20, -20),
     "clips-v7c-clean-20261031__walk__walk-01-contact-v7c-clean.png"),
    ("CJ-07", "v7c", cfg(-20, -20, 20, 20, 0, 0, 0, 0),
     "clips-v7c-clean-20261031__walk__walk-13-passing-v7c-clean.png"),
    ("CJ-08", "v7c", cfg(-15, -15, 25, 25, 20, -20, -25, 5),
     "clips-v7c-clean-20261031__walk__walk-25-contact-v7c-clean.png"),
    ("CJ-09", "v7c", cfg(-150, -150, 20, 20, -20, 20, 10, -10),
     "clips-v7c-clean-20261031__dance__dance-01-a-v7c-clean.png"),
    ("CJ-10", "v7c", cfg(-20, -20, 150, 150, 10, -10, -20, 20),
     "clips-v7c-clean-20261031__dance__dance-13-b-v7c-clean.png"),
]

def convert(src, dst):
    im = Image.open(src).convert("RGB")
    arr = np.array(im).astype(float)
    corners = np.concatenate([arr[:5, :5].reshape(-1, 3), arr[:5, -5:].reshape(-1, 3),
                              arr[-5:, :5].reshape(-1, 3), arr[-5:, -5:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))
    mask = dist > 30
    mask = ndimage.binary_closing(mask, structure=np.ones((3, 3)), iterations=2)
    mask = ndimage.binary_fill_holes(mask)
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    keep = np.zeros_like(mask)
    for i in range(1, n + 1):
        if (lab == i).sum() >= 800:
            keep |= (lab == i)
    alpha = (keep * 255).astype(float)
    alpha = ndimage.gaussian_filter(alpha, 0.8)
    alpha_u8 = np.clip(alpha, 0, 255).astype(np.uint8)
    rgb = arr.copy()
    a = np.clip(alpha / 255.0, 0.01, 1.0)[..., None]
    rgb = np.clip((arr - bg * (1 - a)) / a, 0, 255)
    rgb[keep] = arr[keep]
    rgba = np.zeros((*arr.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = rgb.astype(np.uint8)
    rgba[:, :, 3] = alpha_u8
    Image.fromarray(rgba, "RGBA").save(dst)
    return int((alpha_u8 > 10).sum())

results = []
for shot, ver, c, orig_plate in POSES:
    ns = NS7B if ver == "v7b" else NS7C
    # builders save to their own OUT; redirect to our grey dir
    ns["OUT"] = str(GREY)
    grey_name = f"{shot}-layer-removed-grey.png"
    if ver == "v7c":
        ns["build"](grey_name, c, labels=False)
    else:
        ns["build"](grey_name, c)
    grey_path = GREY / grey_name
    plate_path = PLATES / f"{shot}-plate-layer-removed.png"
    alpha_px = convert(str(grey_path), str(plate_path))
    results.append({"shot": shot, "builder": ver, "config": c,
                    "grey": str(grey_path), "plate": str(plate_path),
                    "alpha_px": alpha_px, "original_sweep_plate": orig_plate})
    print(shot, ver, "alpha_px", alpha_px)

json.dump(results, open(OUT / "work" / "plates-built.json", "w"), indent=1)
print("DONE", len(results))

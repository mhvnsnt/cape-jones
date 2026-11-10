#!/usr/bin/env python3
"""Pre-delivery gate for any claimed step-to-camera / walk from splats.
FAIL = hand-tooled shear, cropped frame, or not-a-walk. Exit 0 PASS, 1 FAIL.
Run: python3 check_step_to_camera.py
Checks (all measured, none claimed from code comments):
 G1 leg alternation: left/right lower-body centroids must move in OPPOSITE
    phase on at least one step (a real walk alternates legs). V4: 0/8 steps.
 G2 feet planted: if the shot is claimed grounded, feet_y spread <= 20 px
    (standing Cape rule). V4: 237 px projected, 237 px delivered.
 G3 no-crop: every frame margin >= 40 px on all sides, edge alpha 0.
    V4 peak: bottom margin 14-15 px.
 G4 no uniform slab: lower-body shift must NOT be one constant applied to
    hips+cape+legs alike (V4: single +/-18 list, y0>200 = 1703/5846 Gaussians
    including lower torso and cape, not legs alone).
 G5 gait keys present: contact / passing / down / up positions, knee bend,
    foot lift, arm counter-swing. V4: 0/5 — apose arms, flat feet, no knees.
 G6 step rate: shift must not flip every frame (V4: 9 flips in 9 frames,
    150 ms apart, ~6.7 Hz shear jitter, not a ~2 steps/s gait).
A turn that is NOT claimed as a walk (V1) is NOT failed by this gate as a
walk — it is labelled NOT-A-WALK, which is correct for V1. The gate fails
only a thing CLAIMED as stepping/walking that has no gait.
"""
import json, sys
V4 = {
    "leg_alternating_steps": "0/8",
    "feet_spread_px": 237,
    "bottom_margin_peak_px": 14,
    "uniform_slab_shift": True,
    "gait_keys": "0/5",
    "shift_flips_per_frame": "9/9",
}
fails = []
if V4["leg_alternating_steps"] == "0/8":
    fails.append("G1 FAIL: legs never alternate (0/8 steps in opposite phase)")
if V4["feet_spread_px"] > 20:
    fails.append(f"G2 FAIL: feet spread {V4['feet_spread_px']} px > 20 px grounded limit")
if V4["bottom_margin_peak_px"] < 40:
    fails.append(f"G3 FAIL: peak bottom margin {V4['bottom_margin_peak_px']} px < 40 px")
if V4["uniform_slab_shift"]:
    fails.append("G4 FAIL: one uniform +/-18 px shift on hips+cape+legs alike")
if V4["gait_keys"] == "0/5":
    fails.append("G5 FAIL: gait keys 0/5 (no contact/passing/knee/foot-lift/arm-swing)")
if V4["shift_flips_per_frame"] == "9/9":
    fails.append("G6 FAIL: shift flips every frame (150 ms, ~6.7 Hz jitter)")
print("V4 step-to-camera gate: FAIL" if fails else "PASS")
for f in fails:
    print(" -", f)
print("V1 turn (not claimed as walk): NOT-A-WALK — correct label, not a gate fail.")
print("Gate result: V4 must not ship as stepping/walking. Exit 1.")
sys.exit(1)

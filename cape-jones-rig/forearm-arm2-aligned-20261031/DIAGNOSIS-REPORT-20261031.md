# Arm2 alignment diagnosis + fix — 2026-10-31
Mars (16:31 CDT): Arm2 v2 is NOT correct, NOT lined up correctly. Diagnosis below is
measured, not eyeballed. Full rule doc: ARM-ALIGNMENT-RULE.md in the rig root.
QC script: check_arm_alignment.py in the rig root.

## Numbers
- Reference v7c Arm_Back_Lower: forearm axis 4.1 deg (manual) / 4.8 deg (QC), offset -6.3 px.
- BAD v2 Arm2: forearm axis 23.3 deg (manual) / 19.8 deg (QC), drift +34 px (y10-90),
  fist kink -26 px vs extrapolated axis, wrist cap ~35 px left of axis, cuff tilted with shear.
  QC: offset delta +12.8 px, angle delta +15.0 deg — FAIL (both tolerances 10).
- Arm1 v2 (for comparison): offset delta +0.7 px PASS, angle delta +18.2 deg FAIL.
  Arm1 is tilted but intact; Arm2 is broken. Neither v2 arm is clean.
- FIXED v3: forearm axis 5.6 deg, offset delta +4.8 px, angle delta +0.8 deg — PASS.
  First v3 attempt had its own 19 px art-centre error (crop-centre placement); corrected
  by shifting shaft/cuff -19 px, fist unchanged. That error is documented, not hidden.

## Files (new dated folder, bad v2 never overwritten)
- forearm-v3-arm2-back-aligned-20261031.png (249x215, clean, no lines baked in)
- proof-arm2-alignment-before-after-20261031.png (lines on proof only, reference only)
- build_arm2_aligned.py, build_proof.py

## Still owed
- Mars approval of v3: 0/1. Current v2 Arm2 is NOT approved.
- Arm1 v2 straightening pass (QC FAIL on angle): owed, not claimed here.
- Arm2 different-angle fist pose integration: separate owed item; this fix is the standard
  Arm2 forearm+fist, not the diff-angle pose.

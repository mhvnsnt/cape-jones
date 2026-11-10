# READ FIRST: w5r arm-joint defect (owner pt98u, 2026-11-10)

`cape_jones_rigged_w5r*.blend` in this folder has its arm bone chain **one joint too far out**:
the rig "shoulder" sits at the elbow crease, the "elbow" sits at the wrist, and the "wrist" sits at the fingertips.
Any retarget onto these blends gives the "H" arms the owner keeps flagging: shoulder to bicep stuck sideways like a T-pose, and the forearm hanging down.

The repo blend is **not** rewritten. It is still the defective file.
For any guard, fight or arm work, use the gate-first pipeline in `production/guard-stance-v2-20261110/`:
- `tools/guard_shot_pipeline.sh` runs `tests/test_guard_arms.py`. The gate must FAIL on the raw blend.
- It then rebuilds the fixed rig with `tools/build_rig_v2.py`. The gate must PASS on it before any render.
- It then bakes the cloth and renders.
A raw w5r render that skips this gate is a regression.

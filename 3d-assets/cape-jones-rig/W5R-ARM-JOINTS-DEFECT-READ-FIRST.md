# READ FIRST: w5r arm-joint defect (owner pt98u, 2026-11-10)

`cape_jones_rigged_w5r*.blend` in this folder has its arm bone chain **one joint too far out**:
the rig "shoulder" sits at the elbow crease, the "elbow" sits at the wrist, and the "wrist" sits at the fingertips.
Any retarget onto these blends gives the "H" arms the owner keeps flagging: shoulder to bicep stuck sideways like a T-pose, and the forearm hanging down.

The repo blend is **fixed in place** (Phase 2a landing, 2026-11-10): `cape_jones_rigged_w5r_clean.blend`,
`cape_jones_rigged_w5r.blend`, and the rig embedded in `3d-assets/living_room.blend` were repaired with the
guard pipeline (`tools/build_rig_v2.py` over `cj_arm_guard.ensure_arm_fix()`; same repo paths, blob replacement).
The gate in `production/guard-stance-v2-20261110/` must now PASS on the repo blend itself. A raw w5r render that
skips this gate is still a regression.
`cape_jones_rigged_w5r_idle.blend` was LEFT as-is (sitting/idle line — see LANDING.md); its canonical replacement
is `cape_jones_rigged_w5r_idle_armsdown.blend`, and `sitting_pose_library_armsdown.blend` is the going-forward
default for the sitting library. The armsdown ACTION (`mocap_sit_canon_armsdown`, rest hang 17.8–18.5°) is blessed
via those variants and the verified scene release `scene1-armsdown-20261110`
(https://github.com/mhvnsnt/cape-jones/releases/tag/scene1-armsdown-20261110).
For any guard, fight or arm work, use the gate-first pipeline in `production/guard-stance-v2-20261110/`:
- `tools/guard_shot_pipeline.sh` runs `tests/test_guard_arms.py`. The gate must FAIL on the raw blend.
- It then rebuilds the fixed rig with `tools/build_rig_v2.py`. The gate must PASS on it before any render.
- It then bakes the cloth and renders.
A raw w5r render that skips this gate is a regression.

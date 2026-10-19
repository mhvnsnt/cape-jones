# Mocap Retarget Tool

Production-grade motion capture retargeting for the 94-bone Cape Jones rig.

## Files

- `retarget.py` — Main retargeter. Imports a CMU FBX, transfers rotations in
  world space with rest-pose correction, places the pelvis, damps head fidget.
  Run: `blender -b 3d-assets/living_room.blend --python production/tools/mocap-retarget/retarget.py`
- `place.py` — Placement calibration. Numerically solves root/pelvis locations
  (the rig's bone axes are rotated; direct assignment fails). Run on the output
  blend: `blender -b proof/sitting_mocap.blend --python production/tools/mocap-retarget/place.py`

## Critical math (do not "simplify")

The retarget MUST use parent-relative rest rotations:
```
R_local = (W_parent @ M_rel)⁻¹ @ W_desired
M_rel = parent.matrix_local⁻¹ @ bone.matrix_local
```
Using armature-space `M_local` (instead of `M_rel`) produces garbage poses
(thighs backward, chest sideways). This was the v2 bug, fixed in v3.

Bone location axes are also rotated. NEVER assign `bone.location` directly from
world coordinates. Use the numerical calibration in `place.py`.

## Source facing

CMU skeletons face -Y (verified from foot bone direction). The CJ rig faces -Y.
No yaw correction needed. (v1 wrongly applied 180°; fixed in v2.)

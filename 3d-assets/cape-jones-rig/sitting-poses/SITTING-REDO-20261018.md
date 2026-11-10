# Sitting Pose Redo — Root Cause & Fix (2026-10-18)

Owner verdict on the sitting turntables: "none of these are sitting... he's floating around with one arm running down and one arm pulling up, he's not sitting, he's not in the right position — none of that is right at all."

## Root Cause (two bugs)

### Bug 1: Turntables rendered from the wrong blend
The sitting turntable MP4s were rendered from `cape_jones_rigged_w5r_idle.blend`
(or `cape_jones_rigged_w5r.blend`), which do NOT contain the `pose_sit_*` actions.
The turntable script's `bpy.data.actions.get("pose_sit_normal")` returned None,
printed "WARN: action or armature not found", and rendered the character in the
blend's default pose (standing). The sitting pose library blend
(`sitting_pose_library.blend`) was never used.

### Bug 2: rotation_mode mismatch (the deeper bug)
The `pose_sit_*` actions keyframe `rotation_quaternion`, but the rig's pose bones
default to `rotation_mode='XYZ'` (euler). Blender SILENTLY IGNORES quaternion
keyframes on bones in euler mode. Result: even when the correct action WAS applied,
the limbs stayed in T-pose — only the root bone's location (seat position) applied.

This is the same class of bug as the documented "GLB imports use QUATERNION —
euler edits silently ignored" gotcha, but in reverse.

## Fix
1. **Render from the correct blend** (`sitting_pose_library.blend`) with the pose
   actions actually applied.
2. **Set `rotation_mode='QUATERNION'`** on all pose bones before applying the
   action (in `render_sitting_redo.py`).
3. **Permanent fix**: `sitting_pose_library.blend` updated — all 85 pose bones set
   to QUATERNION mode and saved (via `fix_pose_library_rotation_mode.py`).
4. **Render him IN the living room chair** (not gray space) using the sit-target
   lane's measured chair transform. Cape hidden for sitting proofs (cape drape is
   the cape lane's work, per SITTING-POSE-LIBRARY.md).

## Verification
All 5 poses rendered in the living room and viewed with own eyes (OWN-EYES law):
- pose_sit_normal: upright, arms at sides, knees bent, feet on floor ✓
- pose_sit_leg_folded: right leg folded on seat ✓
- pose_sit_lean_forward: pensive, elbows on knees ✓
- pose_sit_recline: leaned back, relaxed ✓
- pose_sit_shrug: arms up/out, comedic shrug ✓

The 5 turntable MP4s in `sitting-poses/turntables/` are replaced with correct
videos (6s each: front view + three-quarter view, him actually sitting in the chair).

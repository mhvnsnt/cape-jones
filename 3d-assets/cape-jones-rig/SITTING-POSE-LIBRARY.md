# Sitting Pose Library — Cape Jones

Owner directive 2026-10-17: "the pose library thing we gotta get that together, the sitting and all of that."
Lane: `lane/sitting-pose-library-v2-20261017` (RESTART — previous lane died in a daemon restart with nothing pushed).

He sits ~90% of the time. Five core sitting poses, all full-body FK on the 85-bone
W5r rig, feet grounded exactly, seated on the canon recliner.

## Poses
1. `sit_normal` — main upright relaxed sit, feet flat, arms hanging naturally.
2. `sit_leg_folded` — one leg folded up, foot flat on the seat (his reference).
3. `sit_lean_forward` — pensive/focused, elbows on knees, hands clasped.
4. `sit_recline` — leaned back, legs extended, hands behind head (Space Ghost desk energy).
5. `sit_shrug` — comedic shrug, elbows out, hands up, leaning back (Aqua Teen energy).
   (True arms-crossed was attempted but is anatomically impossible: 0.244m arms cannot
   span the 0.353m to the opposite chest. Hands-behind-head likewise impossible.)

## Files
- `3d-assets/cape-jones-rig/sitting_pose_library.blend` — the library. Each pose is an
  Action (`pose_<name>`, frame 1, all 85 pose bones keyed) marked as a Pose Asset.
  The `idle_heroic_breathe` action is preserved (fake user set). Cape hidden in proof
  renders (53-fragment pre-rebuild mesh); CorrectiveSmooth disabled for proof renders
  only (memory).
- `3d-assets/cape-jones-rig/sitting-poses/*.png` — one Cycles proof render per pose,
  verified by eye: no chair/floor clipping, feet grounded, silhouette reads.
- `3d-assets/cape-jones-rig/tools/sit_pose_builder.py` — the builder script (reproducible).

## Measured setup (from the blend files themselves, not the doc text)
- Chair `loungeChairRelax(Clone)`: location (2.653, 2.312, 0), **270° yaw** (the blend file;
  SCENE-CANON.md text says 225° — the file wins, matches the lane brief).
- Seat top z = 0.37 (flat cushion), seat front edge x = 2.878, backrest x = 3.24–3.33.
- The chair has NO armrests (no verts above z=0.4 outside the backrest).
- Character faces -Y in armature space; root bone carries yaw -90° + seat translation
  so every pose action is self-contained (apply pose → he sits in the chair).

## Rig math notes (for future posers)
- Pose-bone `rotation_quaternion`/`location` are interpreted in the bone's REST-LOCAL
  frame, not armature space. The root bone points +Z, so setting a raw Z-quaternion
  on it produces a Y-rotation in armature space. All posing here goes through
  `set_bone(name, M_desired)` which solves the basis from the desired armature-space
  matrix — never set raw quaternions on bones.
- Feet grounded EXACTLY: after posing, root Z is nudged so the lowest ankle sits at
  z=0.064 (rest ankle height = flat foot on floor). Per-pose ankle residuals are printed
  by the builder and must read 0.064.
- Seat height 0.37 vs 0.925m character: his hip joint sits at z≈0.42 (sunk slightly into
  the cushion); thighs angle steeply down (~60° below horizontal), shins vertical —
  like a small character in a big recliner, feet planted. This is correct, not a bug.

## Cape drape validation: PENDING
The cape rebuild lane is producing a single-sheet cloth cape. Poses were built now
per directive (don't wait). Cape drape/clipping validation against these poses is
PENDING on the cape lane's delivery. Fingers left at rest — the hands lane owns
finger articulation.

## Canon
Palette locked: suit #FFFFFF, cowl #3E1473, cape #000000. Scale 0.925m locked.

## V6 update — 2026-11-07: the permanent no-H-pose rule + corrected default library

**PERMANENT RULE (owner, 2026-11-07): Natural idle = arms down, sitting
and standing. The H pose (biceps up, arms pointed out, hands straight)
may appear ONLY when the owner explicitly directs it (the robot,
King Tut, a deliberate gag). Never naturally, in any idle, ever.**

Audit of this library (measured from the evaluated poses, upper-arm
angle from hanging straight down):

- All five sitting poses were already arms-down: sit_normal 8.3°,
  sit_leg_folded 8.3°, sit_recline 9.2°, sit_lean_forward 22.8°
  (elbows-on-knees lean — the pose itself), sit_shrug 23.0° with the
  forearms folded to 158.8° (the shrug gesture itself — deliberate,
  kept as authored).
- The H carrier was `idle_heroic_breathe`: it keys `rotation_euler`
  but all 85 pose bones are QUATERNION rotation mode, so the action
  was completely inert — layered anywhere, it showed the rig's
  arms-out rest pose (80°). In the older w5r idle file the same
  action is live but its mirrored arm keys flip the right arm to
  152° on the current rig.

**Going-forward default: `sitting_pose_library_armsdown.blend`**
(alongside the original in this folder). It is the same library with
ONLY the breathe repaired: live channels, arms hanging 9.5–17.6°
across the breathing loop (riding the breath, arms-down class),
chest pitch variation 8.6° (the breathing is alive again). All five
`pose_sit_*` actions are fcurve-identical to the original — seat
translations, bent legs and recliner yaw are exactly as saved; only
the idle changed. The original `sitting_pose_library.blend` stays
untouched as the historical file. The w5r idle file got the same
repair as `cape_jones_rigged_w5r_idle_armsdown.blend` (only its 12
arm curves changed). Repair tool: `production/dance-proof-3d-v6/fix_breathe.py`.
Full diagnosis: `production/dance-proof-3d-v6/README.md`.

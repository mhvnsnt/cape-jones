# SIT TARGETS — real sitting on the living-room recliner

Lane 1 of the living-room scene wave, owner directive 2026-10-17 ~20:51 CDT:
"he needs to be able to actually sit down on that chair... right now he's kind
of standing in the recliner seat instead of sitting on it."

Branch: `scene/sit-targets-20261017` (repo mhvnsnt/cape-jones).
This lane changes NO scene geometry: `living_room.blend` is untouched
(no binary merge conflicts). Deliverables are data + scripts + renders;
an integration lane applies them later.

## Files in 3d-assets/living-room/sit-targets/

- `chair_measurements.json` — exact world transform, bbox, seat/backrest/footrest
  geometry of `loungeChairRelax(Clone)`, measured from the blend itself.
- `place_sitter.py` — appends the rig + a sitting pose into the living room,
  applies it, and VERIFIES the sit (butt/back/feet + zero mesh intersection).
  Run: `blender -b 3d-assets/living_room.blend --python
  3d-assets/living-room/sit-targets/place_sitter.py -- <pose> [--render]`
- `verify_all_poses.py` — numeric PASS/FAIL table for all 5 poses, one session.
- `renders/` — own-eyes verification renders (front / side / 3-4).

## Measured chair geometry (world units = meters, from the blend)

- Object `loungeChairRelax(Clone)`: location (2.653, 2.312, 0),
  yaw -90 deg (270 deg), scale 1. **Canon placement — never moves.**
- Sitter forward = world **-X** (chair faces the TV/conversation zone).
- World bbox: x [2.653, 3.328], y [1.822, 2.312], z [0, 0.63].
  (9.7 cm clear of WallRight at x = 3.425.)
- Seat cushion: top z = 0.354 (front edge x = 2.878) rising to 0.373 (back),
  center (3.032, 2.067, 0.362). Slight 2.8-deg rise to the back.
- Backrest: front face at x = 3.268 (seat level) leaning back to x = 3.305
  at the top edge (z = 0.63) — ~8 deg recline. Low back: supports to mid-torso.
- Footrest flap: EXTENDED in the current blend, nearly flat, top z = 0.102,
  spanning x [2.653, 2.918]. (Retraction belongs to the recliner-mechanism lane.)
- No armrests on this chair.

## Sit targets

| Target | Position (world) | Meaning |
|---|---|---|
| `butt_target` | (3.120, 2.067, 0.368) | buttocks contact, biased to seat back |
| `back_target` | (3.290, 2.067, 0.500) | mid-back contact on the backrest plane |
| `feet_target` (recline) | (2.780, 2.067, 0.115) | soles/calves on the extended footrest |
| feet (other poses) | floor z = 0 | flat on the floor |

## How the character is placed (no guesswork)

The five `pose_sit_*` actions in
`3d-assets/cape-jones-rig/sitting_pose_library.blend` are SELF-CONTAINED:
each action's root bone carries the -90 deg yaw + the seat translation
(recline (3.018, 2.067); normal/leg_folded/shrug (3.060, 2.067);
lean_forward (2.972, 2.067)). Applying the action to `CapeJones_Rig`
seats him — the script only appends, applies, corrects, and verifies.

### Placement correction (the actual bug this lane fixes)

All five actions bake a root offset that sinks the feet THROUGH the floor:
soles at z=-0.020 (normal/leg_folded/lean_forward/shrug) and z=-0.089
(recline). The pose doc's own spec is "lowest ankle sits at z=0.064".
`place_sitter.py` measures the ankle bone's world Z and lifts the root by
`delta = 0.064 - ankle_z` along world Z (converted into the root bone's
rest-local frame — the root bone points +Z, so a naive local-z set is
wrong). After the lift: ankles at 0.064, soles flat on z=0, pelvis at
~0.41 (doc spec), zero BVH overlap with the chair. Idempotent: if the pose
lane re-bakes correctly, delta ~ 0.

### Footrest note (for the owner / pose lane)

All five library poses put the feet flat on the FLOOR (verified against the
library's own proof renders, which show the same). The recliner's footrest
flap is EXTENDED in the current blend, but none of the five poses rest the
legs on it — the legs hang with soles on the floor behind/under the flap's
back edge. This lane's placement is correct per the poses as authored. If the
owner wants a true "legs up on the footrest" recline, the sitting-pose lane
needs to articulate it (thighs forward ~70-80 deg at the hips); no root
translation can achieve that.

Locks respected: character scale 0.925 (armature object stays at scale 1.0,
never rescaled); 3D colorway untouched; mug untouched; chair unmoved.

## Verification (all 5 poses, in the living room)

Numeric gates in `place_sitter.py` — **ALL 5 POSES PASS**:

| Pose | Ankle z | Pelvis z | Soles | BVH overlap | Result |
|---|---|---|---|---|---|
| pose_sit_normal | 0.064 | 0.409 | 0.000 (floor) | 0 | ALL PASS |
| pose_sit_leg_folded | 0.064 | 0.409 | 0.000 (floor) | 0 | ALL PASS |
| pose_sit_lean_forward | 0.064 | 0.409 | 0.000 (floor) | 0 | ALL PASS |
| pose_sit_recline | 0.064 | 0.409 | 0.000 (floor) | 0 | ALL PASS |
| pose_sit_shrug | 0.064 | 0.409 | 0.000 (floor) | 0 | ALL PASS |

Gates: ankle at 0.064 (pose-doc spec) | pelvis ~0.41 = butt on seat (seat top
0.362) | soles at 0.000 = flat on floor, no clipping | BVH body-vs-chair
overlap = 0 (zero mesh intersection, the hard gate). Full log:
`sit-lane-scratch/all_verifies.log` (lane scratch, not committed).

Renders (own-eyes verified): `renders/sit_pose_sit_normal_{front,side,threeq}.png`
plus `renders/sit_pose_sit_recline_front.png` — butt on seat, torso upright
against the backrest zone, feet flat on floor, no clipping, no floating, no
sinking. The pre-fix state (feet 2-9 cm through the floor) is superseded.
A temporary fill light was used for visibility only (never saved; the blend
is untouched by this lane).

## Notes for the integration lane

- `place_sitter.py --save-preview PATH` writes a separate preview .blend;
  never save over `living_room.blend` from this lane.
- If the recliner-mechanism lane retracts the footrest, re-run
  `verify_all_poses.py`: the recline pose expects the footrest EXTENDED.
- Cape drape validation against these poses is owned by the cape lane
  (pending there); this lane verifies body-vs-chair only.

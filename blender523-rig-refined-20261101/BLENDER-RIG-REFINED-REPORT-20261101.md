# Blender rig refined, Mars 2026-11-01 14:06 CST

Fixed build was really close, about 85-90%, not fully accurate. This refinement
gets it a little better, using the 2D rig as ground truth, with Grease Pencil.

## Ground truth, no guessing
- PARTS-LABEL-AUDIT-20261031.md lines 38, 178: ARM1 = left = Arm_Front,
  ARM2 = right = Arm_Back, LEG1 = left = Leg_Front, LEG2 = right = Leg_Back.
- joint_locked_rig_v7c.py: shoulders L (430,445) R (670,445),
  hips L (470,740) R (615,740).
- locked-default-rig.json, rig-apose-v7c-clean-transparent.png (1100x1500).
- Previous fixed build: blender523-rig-fixed-20261101/, untouched, not overwritten.

## Grease Pencil overlay, how it was used
- 2D apose brought into Blender at the same world scale (200 px = 1 unit):
  reference plane 5.5 x 7.5, centre (0,1.25), Z 0.20.
- Grease Pencil object GP_Apose_Overlay, 4 strokes, traced from the apose
  alpha silhouette (left edge, right edge, head top, foot bottom),
  source gp-silhouette.json, Z 0.25. It stays in the .blend, hidden from
  the clean renders. Proof render: renders/pose-rest-GP-OVERLAY.png
  (reference + GP visible over the Blender figure).
- Renders under Xvfb + LIBGL_ALWAYS_SOFTWARE=1 (headless EEVEE needs a
  display; a plain background run failed on libEGL, that run produced
  nothing and was discarded, not claimed).

## Measured before vs after, rest pose, 2D canvas pixels
Method: per-row left/right edge, 10 rows y=300..1200, Blender render mapped
through camera ortho 6.2, centre Y 1.03, into 2D canvas coords.
- Fixed mean edge deviation: 34.7 px.
- Refined mean edge deviation: 12.8 px.
- Fixed bbox in 2D: (309,254)-(791,1335). Refined: (239,254)-(887,1292).
  Apose: (248,253)-(876,1295). Top off by 1 px, bottom off by 3 px.
- Worst fixed rows, arms: y700 92 px, y800 91 px, y600 54 px.
  Same rows refined: y700 6 px, y800 1 px, y600 6 px, y500 27 px -> 2 px.

## Pieces that moved, and by how much
- Arms, rest only: Arm1-Upper -20 deg, Arm2-Upper +20 deg (2D apose upper
  angles, whole pieces, no cut, no wrist cut). Forearm pegs match.
  Crossed (f25, +/-55) and flex (f37, -60/+60) absolute angles unchanged.
- Legs, rest only: Leg1-Thigh -9 deg, Leg2-Thigh +10 deg (wide stance).
  Leg drawing planes shifted up 0.15 units = 30 px (centre 1018.5 -> 988.5),
  so feet land on the apose foot line 1295 instead of 1337.
  Shuffle (f48) absolute angles unchanged.
- NOT moved, already within ~7 px: Head, Neck, Cape_Collar (shoulder band
  only, Z 0.05 below Torso 0.08), Torso_Chest, Pelvis, Belt_Overlay,
  Cape_Back_Main (Torso-parented, top 2.95 at shoulders, bottom -1.22).

## Renders, all 700x950, eye-checked against the 2D apose
- renders/pose-rest.png — arms angled out, fists at sides, legs wide,
  feet planted pointing left (viewer-left) / right (viewer-right).
- renders/pose-crossed-chest-snap.png — whole arm chains above torso,
  below head, bicep on top, continuous, no torso eating any arm.
- renders/pose-flex-obtuse.png — 120 deg spread at ortho 6.2, but fists
  crop at both frame edges. This is NOT the flex deliverable.
- renders/pose-flex-obtuse-WIDE.png — same f37 pose, ortho 8.5, both
  fists fully in frame. This IS the flex deliverable, same fix as the
  fixed build used.
- renders/pose-rest-GP-OVERLAY.png — GP + reference overlay proof.

## Kept from the fixed build
Mapping, cape Torso-parented, collar below torso, head base on neck
(overlap 0.31), crossed arms Z 0.11 above torso 0.08 below head 0.12,
17 pegs, 11 drawings, FK 6/6, parents_ok, crossed hand world
[1.308, 2.137, 0.0] unchanged, no crop, no square crop, no wrist cut,
no hand-draw. Previous fixed folder untouched.

## Still off, plainly
- Whole pieces cannot match the 2D cut-limb elbow/knee bend exactly.
  At y900 the refined left edge is 286 vs apose 331: the whole-arm fist
  hangs lower/further out than the cut-arm fist.
  At y1200 the refined right edge is 793 vs apose 734: the whole-leg
  toe swings further out than the cut-leg toe.
- Rest legs are straight angled lines, not cut thigh+shin: knees sit
  further out than the 2D apose, shins slant outward where the apose
  shins are near-vertical. Closing that last gap needs cut upper/lower
  limbs in Blender, which this refinement deliberately did not do
  (whole pieces only, same as the fixed build).
- True arms-up flex with whole pieces is still not claimed here;
  flex here is the wide-out 120 deg spread, same as the fixed build.

## Status
- Mars approval of this refined rig: 0/1.
- Repo landing: local only, no PR claimed, not verified on main.
- Folder: blender523-rig-refined-20261101/ (new dated folder, fixed
  build untouched). .blend: cape_jones_toon_blender523_REFINED.blend.
  Gate: gate-result-refined.json, PASS_WITH_KNOWN_LIMITS (limits above).

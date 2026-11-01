# Blender 5.2.3 rig — FIXED, Mars 2026-11-01 12:52 CST correction

## What was wrong (old build, blender523-toon-20261101/)
Mars, verbatim in substance: Arm1/Leg1 swapped with Arm2/Leg2, cape collar
not in place, cape not in place, neck/head not fully in place. Aligned but
wrong, lazy placement. He was right on all four, and the audit proves why:

- Old: Arm1 = Arm_Back, Arm2 = Arm_Front, Leg1 = Leg_Back,
  Leg2 = Leg_Front_CLEAN. Audit (PARTS-LABEL-AUDIT-20261031.md lines 38,
  178) says the opposite: ARM1 = our left = Arm_Front, ARM2 = our right =
  Arm_Back, LEG1 = our left = Leg_Front, LEG2 = our right = Leg_Back.
  "Front/Back" in filenames = limb identity, NOT body-facing.
- Old: Cape_Collar Z 0.09, ABOVE Torso Z 0.08, centre pivot. Result: the
  full collar bib covered the chest (see before-after-pose-rest.png).
  2D front rig pastes Collar BEFORE Torso, so Torso covers the collar's
  lower part and only the shoulder band shows.
- Old: Cape peg parented to Root, centre pivot at (0,3.2), cape top 5.28,
  towering above the head (4.83). 2D front rig: Cape_Back_Main top 410,
  i.e. at shoulder level, bottom 1243, i.e. above the feet.
- Old: Neck peg = Collar peg (both 3.9), Head centre pivot. The collar
  bib then overlapped the neck/head junction and the head looked
  unseated, even though head bottom and neck top technically overlapped.

## What changed (this build, blender523-rig-fixed-20261101/)
Transform, no invented pegs: X = (x2d-550)/200, Y = 5.0-y2d/200,
200 px = 1 Blender unit, from joint_locked_rig_v7c.py joints and
locked-default-rig.json paste tops/centres. Camera: sensor_fit VERTICAL
explicitly (AUTO made the first fixed pass crop head and feet in
portrait), ortho 6.2 for rest/crossed (figure 5.44 tall, centre 1.03,
0.38 margin top/bottom); flex re-rendered wide at ortho 8.5, pose
unchanged, because wide-out arms (width ~5.6) do not fit a 4.57-wide
portrait frame — first flex pass cropped both fists at the frame edges
and was discarded, never shown to Mars.

| Piece | Source file | Side / peg | Anchor (2D -> Blender) | What changed |
|---|---|---|---|---|
| Arm1 upper | sliced/Arm_Front.png (whole) | viewer-left, Arm1-Upper-P | shoulder (430,445) -> (-0.60, 2.78), anchor (76,30) | Was Arm_Back. Now Arm_Front. |
| Arm2 upper | sliced/Arm_Back.png (whole) | viewer-right, Arm2-Upper-P | shoulder (670,445) -> (0.60, 2.78), anchor (76,30) | Was Arm_Front. Now Arm_Back. |
| Leg1 | sliced/Leg_Front.png (whole, canonical) | viewer-left, Leg1-Thigh-P | hip (470,740) -> (-0.40, 1.30) | Was Leg_Back. Now Leg_Front, NOT _CLEAN. Foot points left. |
| Leg2 | sliced/Leg_Back.png (whole, canonical) | viewer-right, Leg2-Thigh-P | hip (615,740) -> (0.33, 1.30) | Was Leg_Front_CLEAN. Now Leg_Back. Foot points right. |
| Cape_Back_Main | sliced/Cape_Back_Main.png | Cape-P, child of Torso | neckline top 410 -> top 2.95, centre 0.87, Z -0.20 | Was Root-parented, top 5.28 above head. Now Torso-parented, top at shoulders, bottom -1.22 (0.47 above feet). |
| Cape_Collar | sliced/Cape_Collar.png | CapeCollar-P, child of Torso | centre (550,462.5) -> (0, 2.69), top 3.15, Z 0.05 | Was Z 0.09 above Torso. Now Z below Torso (0.08), so only the shoulder band shows, as in v7c apose. Moves with torso. |
| Neck | sliced/Neck.png, scale 1.05 | Neck-P, child of Torso | centre (550,403.5) -> (0, 2.98), top 3.20, bottom 2.77, Z 0.10 | Scale 1.05 from locked-default-rig.json, kept. Now sits under head with 0.31 overlap, above collar in Z. |
| Head_Front | sliced/Head_Front.png | Head-P (skull base), child of Neck | base (550,422) -> (0, 2.89), centre 3.32, top 3.75, Z 0.12 | Was centre pivot. Now base pivot (CAPE-JONES-RIG.md 0.50/0.95), so the head base lands on the neck, no gap. |
| Torso_Chest | sliced/Torso_Chest.png | Torso-P, child of Pelvis | centre (550,559.5) -> (0, 2.20), top 3.00, Z 0.08 | Unchanged piece; Z now correctly above collar, below neck. |
| Pelvis | sliced/Pelvis.png | Pelvis-P | centre (550,745) -> (0, 1.28), Z 0.04 | Unchanged. |
| Belt_Overlay | sliced/Belt_Overlay.png | Torso-P | centre (550,709) -> (0, 1.46), Z 0.085 | Unchanged. |
| Forearm/hand pegs | (markers only, no drawing) | Arm1-Forearm-P elbow (414,637), Arm2-Forearm-P elbow (693,637); hand pegs at fist centres (430/670,870) | v7c elbow vectors: L (-16,192), R (23,192) from shoulder anchors | Whole arm pieces already include their fists. No separate hand drawing, no wrist cut, no hand-draw. Hand pegs follow forearm pegs by parenting. |
| Knee pegs | (markers only, no drawing) | Leg1-Knee-P (488,1014), Leg2-Knee-P (631,1014) | v7c knee vectors: L (18,274), R (16,274) from hip anchors | Whole leg pieces, no cut. |

Rest Z, v7c paste order: Cape -0.20, Leg1 0.01, Leg2 0.02, Arm1 0.03,
Arm2 0.035, Pelvis 0.04, Collar 0.05, Torso 0.08, Belt 0.085, Neck 0.10,
Head 0.12. Both arms below torso at rest. Crossed f25: both arm planes
keyed to Z 0.11, above torso, below head (arm-front-snap R01, whole
chain, per arm, per frame).

## Eye-check, against rig-apose-v7c-clean-transparent.png
- Rest: head fully visible, cowl + face, purple neck band under chin,
  collar as two shoulder pads only (not a bib), cape behind at shoulder
  level ending above the feet, torso/belt/pelvis seated, viewer-left
  foot points left, viewer-right foot points right, both feet complete.
  Matches the 2D apose, except rest arms hang straight down (fists at
  thigh) where the apose arms angle slightly out — rest vs apose, not
  an error.
- Crossed: whole arm chains cross the chest above the torso, below the
  head, bicep on top, continuous, no torso eating any arm. Elbow ball
  circle is visible at the crossing centre — that is the whole-piece
  elbow circle, not a cut or a second hand.
- Flex wide-out: 120° spread, arms out, both fists fully in frame,
  head/neck/collar/cape/legs unchanged and seated. Labelled wide-out
  spread, NOT arms-up flex: a whole arm rotated to arms-up puts its
  fist upside-down, and cutting the arm to split upper/forearm is
  banned, so a true arms-up flex is still not claimed here.
- Before/after files (old frame 550x375 landscape, new frame 700x950
  portrait, so sizes differ — shapes and placements are the comparison):
  before-after-pose-rest.png, before-after-pose-crossed-chest-snap.png,
  before-after-pose-flex-obtuse.png. Before = old swapped build,
  After = this fixed build.

## Gate
gate-result.json: PASS, 12/12 checks (mapping x4, parents, FK 6/6,
collar below torso, cape below head top, head-neck overlap > 0,
crossed snap Z between torso and head, flex 100-160°, no crop /
wrist cut / hand-draw). Pose table: pose-table.json (f1 rest, f25
crossed, f37 flex, f48 shuffle Leg1 lifted / Leg2 planted).
Knee-feet in these poses: straight/straight at rest, crossed and flex
do not bend knees, shuffle is Leg1-lift only — the universal
knee-feet rule (knees direction == toes direction, per frame, both
legs, exception only when Mars names a specific pose) is enforced in
the gate file, and no leg1-exception is claimed for these renders.

## Files
- build_blender523_rig_fixed.py — fixed builder, all anchors sourced above
- cape_jones_toon_blender523_FIXED.blend — saved, re-openable, 17 pegs, 11 drawings, FK 6/6, parents_ok true
- blender523-fixed-verify.json — Blender 5.2.3 LTS, hand world at crossed f25 [1.308, 2.137, 0.0]
- renders/pose-rest.png (700x950), renders/pose-crossed-chest-snap.png (700x950), renders/pose-flex-obtuse.png (700x950, wide camera)
- renders/toon-blender523-FIXED-test-clip-SFX.mp4 — 3.0s, 700x950, from the 3 Blender stills 1s each, synthesized blips, NOT a 48-frame Blender animation, NOT -14 LUFS
- renders/toon-blender523-FIXED-test-clip.mp4 — silent version, reference only
- before-after-*.png, pose-table.json, gate-result.json
- work/BEFORE-*.png — old renders, kept, not overwritten, not deleted

## Still owed, plainly
- Mars approval of this fixed rig: 0/1.
- Repo landing: local only, no PR claimed, not verified on main.
- Official Harmony trial/licence, in-Harmony rendering, .tpl/.plt proof:
  separate, not claimed here (this task was the Blender rig fix only).
- True arms-up flex with whole pieces: not claimed (see flex note above).
- A 48-frame Blender EEVEE animation: not rendered here; the clip is
  from the 3 key stills, labelled as such.

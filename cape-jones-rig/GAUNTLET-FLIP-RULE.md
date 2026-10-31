# Gauntlet flip rule — pose-driven piece swap, approved 2026-10-31 15:00 CDT

APPROVED POSE: reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png
Mars, 2026-10-31 15:00 CDT: "that one's perfect." This is the locked reference
for arms-up-in-front poses. Do NOT re-derive it from scratch. Do NOT reuse
the v1 floating version.

## Industry form of this rule (how the pros log it)

This is a POSE-DRIVEN PIECE SWAP — the cutout equivalent of two standard
industry systems, used together:

1. Pose Space Deformation / driven-key correctives: a corrective shape is
   tied to a joint angle, so when a joint passes a threshold the correction
   blends in automatically, driven by the joint itself, not by hand per frame.
   Pose space deformation is defined as deforming a mesh according to the
   angle of the joint bent, with corrective poses tied to specific skeleton
   positions. In Maya it is the Pose Deformer, in Blender it is Corrective
   Shape Keys.
2. Cutout drawing substitution: in a cutout puppet, hands, feet, and other
   extremities live on separate layers from the limbs, so a drawing can be
   swapped during animation without distorting the limb — the Toon Boom
   method for multi-pose deformation rigs, where extremities are kept
   separate so they can be swapped in for different poses.

Our version, in those terms:
- DRIVER = elbow bend + arm-up position (see Condition below).
- DRIVEN = lower-arm piece swap, original -> OutFixed, at 100% when the
  condition is met, 0% otherwise. No in-between, no per-frame hand flip.
- CORRECTIVE = cuff band only, per-row mirrored in place (see Method).
  Everything else in the limb is untouched, exactly as a corrective
  blendshape leaves the rest of the mesh alone.

## Condition — when the flip applies (and when it does NOT)

APPLIES when ALL of these are true:
- Arms are UP and IN FRONT of the torso, fists up near the shoulders,
  forearms in front of the chest — the fighting pose / forward bicep curl.
- Reference angles (this pose): arm_upper L -25 / R 25, arm_lower
  L 160 / R -160. Threshold rule for future poses: |arm_lower| >= 120
  AND the forearm is in front of the torso (not behind, not at the side).
- Then gauntlet panels MUST face OUTWARD / toward the camera, NEVER
  inward toward each other. Inward-facing panels in an arms-up pose are
  misplaced, by definition.

DOES NOT APPLY:
- Arms down, arms at the side, T-pose, A-pose, walk, jump, dance, flying
  (unless a future arms-up frame in those clips meets the condition above,
  frame by frame — the swap is per-frame, driven by the angle, not by clip name).
- Never apply the flip globally to the default lower pieces. The default
  pieces stay original; the swap is a pose-driven override.

## Method — exact placement, so it never regresses

- Source pieces: cut-limbs-v7c/Arm_Front_Lower.png (153x289),
  Arm_Back_Lower.png (158x288).
- Cuff band: y62 to y180 only. Above y62 (forearm/elbow) and below y180
  (fist) are kept pixel-identical in the source piece.
- Flip: PER-ROW mirror within each row's own alpha span (xmin to xmax
  for that row). Every row's x-range after the flip is EXACTLY its
  x-range before. That is why the fixed version sits in the exact world
  spot and connects to the arm, while v1 did not.
- Output pieces: cut-limbs-v7c-gauntlet-out-fixed/Arm_Front_Lower_OutFixed.png,
  Arm_Back_Lower_OutFixed.png.
- Builder: same shoulders (430,445)/(670,445), same elbows (ball centres
  (60,222)/(99,222)), same angles, same anchors, same elbow caps, same
  bicep/upper pieces, same fists. Only the lower piece filename changes.
- World-space check, fixed vs inward: differing pixels 17,082/1,650,000
  = 1.0%, bbox x323-775 y433-565 — gauntlet zone only. Nothing else moved.

## What was wrong with v1 (superseded, do not use)

- v1: cut-limbs-v7c-gauntlet-out/Arm_*_Lower_Out.png, whole-band flip
  around the piece centre. Front cuff shifted +44px, Back cuff -61px
  off the forearm/fist centre, so the gauntlets floated loosely.
- v1 is SUPERSEDED by the fixed version. Any future build that uses v1
  fails the regression test below.

## Regression prevention

- pose_driven_swaps.json in this folder is the machine-readable version
  of this rule: condition, driver angles, driven piece mapping.
  Future builders MUST read it; they must not hardcode a flip, and they
  must not flip by whole-band mirror.
- check_gauntlet_flip.py runs these checks and fails (non-zero) if any
  fails: (1) OutFixed pieces exist; (2) per-row x-range preserved vs
  original for every row y62-180; (3) approved fixed pose file exists;
  (4) v1 file is present in the superseded list in this doc (it is not
  deleted — checkpoint rule — but it must never be selected for an
  arms-up pose); (5) the approved pose's diff vs the inward pose is
  confined to the gauntlet zone (bbox within x300-800, y400-600).
- Run that test before any arms-up clip is shipped, and before any
  gauntlet piece is changed. A change to a lower piece re-runs the test.

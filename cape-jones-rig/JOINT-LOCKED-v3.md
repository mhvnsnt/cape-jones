# Joint-locked rig v3 — LOCKED, 2026-10-31
Mars, 2026-10-31 11:42 CDT: shoulders must stay attached to the torso,
hips must stay attached to the pelvis, joints locked so limbs cannot
float apart. Arms are on the correct sides. Everything else was good.

This v3 is the correction. It does NOT replace the v8 T-pose lock —
v8 is still the default T-pose. V3 is the joint system that every
repose must use from now on, instead of whole-piece rotation.

## Industry-standard method used
- Hierarchy, not hand placement: torso -> shoulder joint -> upper arm
  -> elbow joint -> lower arm; pelvis -> hip joint -> upper leg
  -> knee joint -> lower leg.
- Fixed joints: shoulder L (430,445), shoulder R (670,445), both
  inside the torso (left 400, right 700, top 400, bottom 703).
  Hip L (495,760), hip R (605,760), both inside the pelvis
  (left 441, right 659, top 680, bottom 803).
- Pinning: upper limb's shoulder/hip anchor is pasted at the joint,
  then the layer is rotated around that joint. Lower limb's elbow/knee
  anchor is pasted at elbow/knee = joint + length*(sin(angle), cos(angle)),
  then rotated around that elbow/knee. Upper and lower share the exact
  same elbow/knee point, so they cannot float apart.
- Layer order: upper limbs under torso/pelvis (joint tucked under
  the body), lower arms over torso (forearm/fist in front, e.g. flex).
  Lower legs are below the pelvis, so their order vs pelvis does not
  change the joint.
- Rotation rule, calibrated with a test sheet: 0 = limb straight down,
  positive angle = toward screen-right. End = joint + length *
  (sin(angle), cos(angle)).
- Anchors (unscaled): arm upper shoulder (76,30), elbow (76,285);
  arm lower elbow (76,20); leg upper hip (77,40), knee (77,325);
  leg lower knee (77,25). Scale 0.95. Upper arm length 242, upper
  leg length 271.

## Poses built and visually checked, v3
- joint-apose-v3: arms down-out, legs down-out, shoulders/hips attached.
- joint-flex-v3: upper down-out 25, lower +-160, fists at chest sides
  in front of torso, elbows attached, shoulders attached.
- joint-punch-v3: R arm horizontal 90, L arm back, legs stepping,
  all joints attached.
- joint-jump-v3: arms up-out, legs tucked out, knees attached.
- joint-dance-v3: arms swinging opposite, legs wide, joints attached.
- joint-seated-v3: thighs out 45, shins down, knees attached.
  This is a seated/wide stance, not a true recline — a reclined torso
  piece is still missing for a true lounge.

## Flying sheets status, checked 2026-10-31
Branch feature/character-parts-expansions-20261031 exists in
cape-jones, commit 3eed63b6, but characters/sheets/variations/
contains ONLY NOTE.md and README.md — 0/5 flying sheet images
landed in the repo. The other lane's note about a binary encoding
constraint matches what the API shows. Those sheets are NOT usable
from the repo until the images actually land. Next work is to build
flying poses from this joint-locked rig (arms-out soaring, diving,
forward flight) instead of waiting on new generated sheets.

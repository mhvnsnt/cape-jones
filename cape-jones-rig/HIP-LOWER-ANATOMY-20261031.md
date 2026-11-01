# Hip-lower fix — anatomy note (Mars, 2026-10-31 17:28-17:29 CDT)

## The problem, found in the builder
The flex builders dipped the pelvis (over-exaggerated dip 28px, deep squat
dip 52px) but kept the hip joint fixed at y740 in both versions. So the
thigh tops sat too high relative to the dropped pelvis — the hip looked
attached at the top edge of the pelvis instead of seated inside it.

## Anatomy (researched, not guessed)
- The hip joint is the femoral head in the acetabulum. The acetabulum is
  part of the pelvis itself (ilium + ischium + pubis), so the hip centre
  is rigidly part of the pelvis: when the pelvis drops in a squat, the hip
  centre drops with it. It cannot stay fixed while the pelvis drops.
- Deep-squat kinematics (overhead deep squat study, healthy adults): hip
  flexion peaks around 120 degrees, anterior pelvic tilt runs roughly
  15-33 degrees through the squat, with the pelvis tilting as the femur
  flexes. In a front view, more hip flexion = the femur tilts more
  horizontal and its vertical projection shortens (foreshortening).
- In a squat the knees and feet stay planted while the pelvis drops, so
  the thigh must re-angle to the same knee: hip lower + knee fixed =
  thigh tilt increases a few degrees + thigh foreshortens a few percent.
  That is the "tilt the hip joint lower, like bending on the knee" Mars
  described — the joint lowers with the pelvis, the thigh bends to meet
  the same knee, nothing detaches.

## Amount applied — and why not the full dip
- Applied: hip y740 -> y760, i.e. **20px lower, both sides, both versions**.
- Full pelvis translation (28px / 52px) was NOT applied: with knees and
  feet locked (Mars's constraint), that would force 11-16% thigh
  shortening and change the approved squat depth. 20px is the
  joint-seating correction Mars asked for — "a little, slightly" — both
  versions were already very close to perfect.
- Thigh re-angle to the SAME knee, measured:
  - Over-exaggerated: L -22.00 -> -23.48 deg, R +22.00 -> +24.02 deg;
    foreshorten 0.927 / 0.931 (~7%).
  - Deep squat: L -34.00 -> -36.37 deg, R +34.00 -> +36.84 deg;
    foreshorten 0.935 / 0.940 (~6%).
- Knees unchanged (over: L (388,988), R (727,976); deep, after the
  original 29px delivery shift: knees at their delivered positions).
  Feet unchanged: ground line y1299 in both versions; over version
  overall bbox y279-1299, x222-879 identical to source; deep version
  overall bbox y332-1299 identical to source, head/feet/leg ranges and
  centroids identical to source.
- Pelvis, torso, arms, fists, wrist cleanup, cape hem: unchanged from
  each source version. Deep version keeps the original 29px delivery
  shift that planted its feet at y1299.
- True final flex relaxed-clean: NOT touched (md5 verified unchanged).

## Files
- full-final-flex-over-exaggerated-hip-lower-20261031.png
- full-final-flex-exaggerated-deep-squat-hip-lower-20261031.png
- over-exaggerated-hip-lower-before-after-20261031.png
- deep-squat-hip-lower-before-after-20261031.png
- over-exaggerated-hip-lower-leg-crops-20261031.png
- deep-squat-hip-lower-leg-crops-20261031.png
- Builder: build_hip_lower.py (piece-level, never image-space rotation)
- Approval: 0/1 each (Mars approves).

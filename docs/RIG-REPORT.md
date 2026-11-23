# PURPLE LOT V2 — Rig Report (2D)

**Status:** rig PROVEN by dance test (own-eyes, 2026-11-22). V2 cut VERIFIED
own-eyes (2026-11-22): 480f, 20.000s, 1280x720, 24fps, h264, silent.
**Deliverables:** `production/2d-parking-lot/video/purple-lot-v2.mp4` (480f, 20.000s,
1280x720, 24fps, silent) + `dance/dance-test.mp4` (96f proof) in this PR's workdir
record (see `CHECKPOINT.md` in the lane workdir).

## What the rig is — honestly

- **Native Blender cutout rig, NOT COA Tools 2.** No COA install was found or
  verified on this VM, so the puppet is built with a native Blender armature +
  textured image planes (Emission/shadeless, alpha). The part set, pivots,
  parenting and layer stack are the repo's own (`cape-jones-rig/`, locked
  T-pose v8, 2026-10-31): 28 real sliced parts from `cape-jones-sliced.zip`,
  12 bones (pelvis, torso, neck, head, armR/L, handR/L, legR/L, capeTop,
  capeTip), 12 part planes + 14 hand planes (7 per side) + remote prop +
  2 pupil overlays + ground shadow. A COA build later swaps the renderer,
  not the rig data.
- **Renderer is Cycles CPU, not EEVEE** (EEVEE needs `libEGL.so.1`, missing on
  this VM; the `apt-get install libegl1` approval was not answered — not
  retried). ~5.5 s/frame at 32 samples, 1280x720.
- **Elbow/knee cuts are OWED.** Arms and legs are one piece each in the slice
  set — no elbow or knee joint. Bends read through whole-limb rotation; a
  mid-limb cut is future work, not claimed here.
- **Cape is a 2-bone chain** (Cape_Top / Cape_Tip, split at 55% height, 8%
  overlap) driven by a damped-spring follow-through in the choreography, not
  a cloth sim and not Wiggle 2 (no Wiggle 2 in this pipeline). Lag /
  overshoot / settle are visible in the dance test.
- **Remote prop cropped from repo art** (`pose-02-raise.png`, 123x168 px) —
  no separate remote part exists in the slice set.
- **Pupil overlays drawn** (two small dark ellipses) — no pupil part exists in
  the slice set; pupils appear only from f428 per canon.
- **Plates rebuilt, not claimed.** `production/2d-parking-lot/v2/` did not
  exist in the repo (HANDOFF's 4/4 claim was contradicted on 2026-11-22).
  Clean plates were rebuilt from board 01 by inpainting Jones out (v4: patch
  fill + 60px feather + per-row tone match). Known limits: faint seam/line
  jog at the patch edges, half-clipped blue car at the patch's right edge
  (was behind Jones in board 01). The purple plate is the sodium plate
  through the repo purple-streetlight grade (playbook: the light moves in
  post, the drawing stays clean). Board 05 inpaint was abandoned — the hero
  figure is too big to inpaint cleanly.

## Proof

- **Dance test — PASS own-eyes.** `dance/dance-test.mp4`, 96f @ 24fps, 4.000s:
  idle bounce, step-touch, arm raises, twist + settle, on the lot, cape
  follow-through visible (frame 65: cape flares left on the twist).
- **Defect found and fixed in the dance:** hand swap planes floated off the
  wrists (detached gloves, frames c0033/c0065). Cause was placement, not the
  parent math: the planes had been centred at the hand-bone midpoint. Fix:
  centred on the wrist; verified numerically at rest and at arm -150 deg
  (hand centre == wrist exactly). A canonical-inverse experiment that
  double-applied the placement and broke every part was reverted; the
  tail-based bone-parent inverse is the verified-correct one for Blender 5.0
  on this machine.
- **V2 cut:** 480 frames, 240 pose keys on twos (computer tweening between
  poses), camera per shot (wide ortho 71 / medium 34 / medium-close 26),
  hand swaps (Grip + remote from f121), pupils from f428, V1 gag plates for
  the close-up f169-205 (board 04 + ib-04b — the canon staging the rig cannot
  do), 48f crossfade f206-253, hard cut to black f469-480. Grades are the
  repo's verbatim chains (`production/pipeline/grades.py`: BULB_ORANGE with
  brightness -0.08 for sodium, PURPLE_STREETLIGHT for purple), applied in
  ffmpeg — a numpy re-implementation of the same chains diverges from
  ffmpeg's YUV eq on blue (~17/255 mean abs diff), so the grades stay in
  ffmpeg; the crossfade is a per-frame PIL blend of the two graded streams
  because ffmpeg xfade stretched a 480f pair to 685f. Verified cut:
  480 frames, 20.000s, 1280x720, 24fps, h264, silent, sha256
  e18a78b760d966389634e88f6bf9e39fa18ecbf712643b482d644214c2c8483f.

## Counting, honestly

- 480 frames, 240 pose keys on twos. The rig tweens between keys — the
  motion is continuous, not 240 separately drawn cels. That meets the
  owner's floor (240 drawings minimum) as 240 keys, not as 240 hand drawings.
  V1 had 17 drawings across 480 frames; V2 has 240 keys across 480 frames.
- The close-up gag (f169-205) reuses 2 V1 plates; the rest is rig animation.

## Still unproven / next (do NOT claim)

- AnimLab peg / deformer (step 2) — PR #429: placement + export proven,
  peg partial. Grease Pencil stays animation core until rig/deformer fully
  proven.
- Boards and in-betweens (step 3).
- Elbow/knee cuts, Wiggle 2 cape, COA Tools 2 build, EEVEE rendering.
- Voice ("ah, that's better") and original track — owner-gated, silent cut.

## Versus the V2 cut already on main (PR #430, checked 2026-11-22)

Main already has `production/2d-parking-lot/video/purple-lot-v2.mp4`
(1,998,110 B, sha256 `b2e8b691…6486e38`), built by a parallel lane with the
stronger rig on paper: Blender 5.2.4 + COA Tools 2 (Aodaruma fork) + Wiggle 2,
44 re-sliced parts with elbow/knee cuts, 11 eye swaps, 6 cape variants.
**But its delivered video is visibly broken at 3/3 beats this lane checked
own-eyes (f1, f313, f441): forearms + hands do not render — the arms end at
the elbow cuffs; the head is oversized; the cape is a flat black slab.**
That lane's own report says its own-eyes pass was never done. This lane's
cut (sha256 `e18a78b7…8483f`) has full arms/hands at every beat checked,
cape with shape + follow-through, and the remote visible in the grip.
Side-by-side sheets in the workdir: `v2/compare-f313.png`,
`v2/compare-f441.png`; main's cut saved at `v2/main-cut/`.
**Landing is HELD for the parent/owner call** — this lane did not push, did
not commit from the sparse checkout (NO-SPARSE-COMMIT LAW), and removed its
staged copies (`git status` clean). The parent decides: replace main's cut
with this one, fix main's cut's forearm render bug and keep it, or merge the
two rigs (their parts + eyes + Wiggle on this lane's verified pipeline).

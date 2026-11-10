# ARM-FRONT-SNAP AUTOMATIC FIX — 2026-11-01

Mars order 2026-11-01 11:25 CST: when he crosses his arms down across
his chest in front of him, for that moment the arms MUST go to the
top layer so they are not eaten by his chest, with automatic senses
wired up 100%, as talked about 2026-10-31. "Other than that it's
perfect" — recorded as CONDITIONAL approval: clips otherwise perfect,
pending this snap fix. NOT full approval until snap-fixed versions
are shown to Mars. Approval of these fixed versions: 0/1.

## Sensor wired (automatic, not manual per frame)
File: `arm_front_snap_sensor.py` in this folder.
- Angle mode (mandatory BEFORE rendering): render that side's forearm
  alone, count alpha overlap with the Torso_Chest mask at 1100x1500.
  snap = overlap > 1000 px. Out-to-side 0-268 px, crossed 1538-8969 px
  (dance-arm-snap audit, 63 frames). Upper-arm overlap is NOT the
  test (always 4000+ px at the shoulder).
- Validation, not a claim: the sensor reproduces the dance f015 audit
  exactly — L 7963 px, R 7416 px — and the independent
  check_pose_snap.py gate gives L 12318 / R 12503 px for the new
  crossed-down pose vs this sensor's 12295 / 12489 px (within 0.2%,
  rounding only).
- Gate tests: crossed-down pose, applied chest both sides: PASS
  (exit 0, `snap-gate-audit-20261101.csv`). Same pose, applied none:
  FAIL (exit 1, `snap-gate-negative-test-20261101.csv`) — the gate
  correctly rejects an unsnapped crossed pose. Arms-out control:
  0 px both sides, no snap, PASS.
- Apply: snap_figure.py chest pass — whole chain (upper + forearm +
  fist + elbow cap) above torso, BELOW head (torso < arm < head).
  Face snap (lower_vs_head > 5000) goes above head instead.
  Cowl snap stays upper-only, candidate + eye-check only, never
  automatic; whole-chain cowl is BANNED (JoJo 02 L).
- No hand-draw, no wrist cut, no piece change, no flip: only layer
  order per frame, sensed automatically. Snap lasts only while the
  condition holds on that frame; it returns to normal order the
  moment the arm goes back out to the sides.

## True pixel fix delivered (crossed-down pose)
- `crossed-down-CHEST-SNAP-fixed-20261101.png` (1100x1500):
  upper L 20 / lower L 90, upper R -20 / lower R -90, legs standing.
  Sensor: L snap, 12295 px; R snap, 12489 px. Eye-checked: bicep-to-
  elbow chain continuous over the chest, head above the arm.
- `crossed-down-NORMAL-eaten-control-20261101.png`: same angles, no
  snap. Eye-checked: biceps hidden behind the chest, forearm/fist
  floating at the waist — the exact eaten look Mars flagged.
  The control is proof, not a deliverable to show as fixed.
- Johnny _13 note: _13 in ANIMATION-EXAMPLES is a show pose sheet
  (arms crossed forward), not a Cape Jones frame. Its Cape Jones
  equivalent is this crossed-down pose + dance f015 (both arms
  snapped) and f083 (R only, 2145 px). No show art was copied.

## Movement clips + dance-test: what was actually found
- Method: 3 fps contact sheets, eye-checked with my own eyes, plus
  source-builder audits. Per-clip list:
  `CLIP-SNAP-AUDIT-20261101.csv`.
- Result: 0 eaten frames found in any of the 8 movement clips or in
  the dance-test visual at 3 fps sampling. Crossed-down-across-chest
  moments DO occur in clips 01, 02, 03, 04, 07 and in the dance-test
  twist frames — and in every sampled one the arm already reads
  continuous over the chest (forearms drawn after the torso in
  those builders, uppers visible at the chest sides). Clips 05, 06,
  08 have no chest crossing in the sample (arms out/up, waist-cross
  only in 08).
- Honest labelling (Mars 2026-11-01 11:46 rule, applied here): all 8
  movement clips are NEW FILES with OLD VISUALS — re-cuts of silent
  Oct 31 Cape Jones videos with SFX added only, timing description
  from audit, Cape Jones pieces only, no show footage/rig/art/audio
  in any clip. Clip 2 is corrected to DANCE, not a kick (its old
  wav sweep/impact sat on a flex moment); a true forward kick is
  still owed, foreshortened kick-leg piece first. Clip 4 (Smiling
  Friends pose-swap) was separately approved 1/1 by Mars as
  "100% perfect" — that approval is for clip 4 itself, NOT for
  these snap-fixed re-issues, which remain 0/1 until shown.
- Honest limit, not hidden: a flat MP4 cannot be re-layered — the
  pixels behind a torso are gone, and no flat-video patch can
  restore them. If Mars spots an eaten frame this sampling missed,
  that frame goes back to a rig re-render with the sensor ON, not
  to a pixel patch. The flat-video proxy in the sensor script was
  RETIRED as a discriminator in this task: at 6 fps it flagged 100%
  of frames as candidates because the white torso itself fills the
  chest band on every frame. Its candidate numbers are NOT used
  as findings anywhere here; the verdicts above are eye-check +
  source audit, per the rule's own eye-check-decides clause.
- Rig-chains note: build_chains.py does NOT use arm-front-snap
  (its only "snap" is punch snap, a different thing). Clips 03-07
  therefore carry no builder snap audit of their own — their
  PASS here rests on the eye-check above, and any future rig-chain
  rebuild must run the sensor first (see wire-in below).

## Fixed versions delivered (originals untouched)
Folder `fixed/`, 11 MP4s + 8 GIFs, stream copy so sound is kept
exactly (original audio tracks untouched, byte sizes identical to
the originals — visual unchanged because no eaten frame was found
to fix; the fix delivered for the clips is the wired sensor + gate
+ audit, and the true pixel fix is the crossed-down pose above):
- 8 movement clips, `-arm-snap-fixed-20261101.mp4` (+ GIFs).
- Dance-test silent visual, JP excerpt, EN excerpt, same suffix.
  (Excerpts only — the full-length Videos 1-5 are a separate
  running task; see below. These excerpts are NOT the full-length
  deliverable.)
- File list + sizes + SHA-16: `fixed/FIXED-FILES-20261101.json`.
- Flicker re-run (`flicker-rerun-20261101.csv`, whole-frame proxy
  at 12 fps, 480 px): all 11 fixed MP4s PASS — 0 jumps >= 25.5
  luminance in the 8 clips (max jump 0.5-5.3). Dance-test MP4s show
  2 jumps of 66.6 — those are the two painted-background segment
  cuts (room -> stage -> night city), not forearm flashes, and 2
  jumps over 4.5 s is below the 3-per-second threshold.

## Wired into future builders (mandatory pre-delivery step)
For Videos 1-5 and every future pose/clip/shot, before rendering:
1. Run `arm_front_snap_sensor.py --angles` (or the same
   forearm-vs-torso overlap measurement inside the builder) on
   every pose's arm angles, per side, per frame.
2. Feed the decision into snap_figure.py (chest / face / cowl-upper
   passes) or the Harmony/Animate/Tahoma equivalent (Z-nudge /
   layer-order keyframe, snap ON = arm above torso, OFF = normal).
3. Run check_pose_snap.py; gate must exit 0 and the audit CSV
   must ship with the video. Exit 1 = do not deliver.
4. Chest snap is warning + eye-check: if the eye-check says the
   upper is eaten and no snap was applied, that is a FAIL.
This step sits in front of frozen builders (joint_locked_rig_v7c.py,
build_poses.py are NOT edited).

## Still owed
- Mars approval of the snap-fixed versions: 0/1.
- Videos 1-5 (full length, running in parallel tasks): sensor must
  be applied to them when they finish, with their own per-frame
  snap lists — NOT claimed here, since they are not finished yet.
- Any eaten frame Mars spots beyond the 3 fps sampling: rig
  re-render with sensor ON, not a flat-video patch.
- Landing: this folder is local-only; no PR claimed until a landing
  run verifies it on main (parent PR route, do not duplicate-claim
  side-rig-fixed PR #332 or landing PR #333).

# LOCK RECORD — Blender motion arm-front-snap, PERFECT 1/1

Mars, 2026-11-01 16:20 CST, approving
`blender523-legs-fixed-MOTION-SNAP-EARLY-20261101.mp4`:
"that's perfect, lock that in, lock that in as the perfect way to do that,
and remember that."

## What is locked — do NOT change, overwrite, or re-render

- Clip: `blender523-motion-arm-snap-early-20261101/blender523-legs-fixed-MOTION-SNAP-EARLY-20261101.mp4`
  - 700x950, 24fps, 48 frames, 2.0s, h264, faststart (moov at 36), silent
  - 119,850 bytes
  - md5 `0e158d1e517f652e18260962379fba9e` (re-verified in this job, unchanged)
  - sha256 `6fabf88c27970d0ed79ba8f91629340939f5b23469369fa8cb5d301b4dc37c06`
- Blend: `blender523-motion-arm-snap-early-20261101/cape_jones_toon_blender523_SNAP_EARLY.blend`
  - md5 `f3ac2f14d308d73470b6483ee24e8b24`
  - sha256 `6dbbcf7b58ed91f8560764c444d44df960a98e99ea95b532e06f9fbe9df182a2`
- Source of the lock: `blender523-overlay-locked-20261101/cape_jones_toon_blender523_OVERLAY_LOCKED.blend`
  (legs-fixed perfect placements, GP overlay hidden for clean renders).
- This study job ran its template tests ONLY on copies in /tmp, never on
  the locked clip or blend. Both hashes above match the pre-study values.

## The locked rule — automatic default for EVERY future Blender motion build

| Item | Locked value |
|---|---|
| Snap ON | f13, arms-out, BEFORE any torso crossing |
| Crossing window, held | f14-f36, every frame, both arms |
| Snap OFF | f37 only, wide flex, arms clear of torso; rest Z again at f48 |
| Snap Z | 0.11, both arm draw planes |
| Torso Z | 0.08 |
| Head Z | 0.12 |
| Stack for chest crossing | torso (0.08) < arm (0.11) < head (0.12) |
| Stack for face crossing | torso < head < arm (per standing face-snap rule, R02) |
| Rest Z, Arm_Front | 0.03 |
| Rest Z, Arm_Back | 0.035 |
| Chains | Whole arm chains, upper + forearm + fist, per arm, per frame |
| Timeline | f1 rest -> f13 arms-out -> f25 crossed peak -> f37 flex 120 deg wide -> f48 shuffle, Leg1 lifted, Leg2 planted |

Why the old version failed, in one line: the old build keyed snap only at
f25, the crossed peak, so arms moving toward the torso from f14 were
still below torso Z and the torso ate the start of the crossing.
Snap-sooner is not "snap harder at the peak" — it is "be in front
before the overlap starts, and stay in front until the overlap ends."

## What this lock does NOT claim

- It does not make every future clip perfect. It makes the snap timing
  automatic. Poses, angles, legs, cape, and timing still need their own
  checks, and a future clip is perfect only when Mars sees it and says so.
- True arms-up flex with whole pieces is still not claimed; flex here
  is wide-out 120 deg. Whole legs still rotate as one around the hip
  (legs-fixed known limit).
- This record is local only. No repo PR was made in this job, and this
  lock is not verified on main until a landing batch says so.

## Where the rule is wired, not just written

- `motion_template.py` in this folder: SNAP_ON=13, CROSS_START=14,
  CROSS_END=36, SNAP_OFF=37, SNAP_Z=0.11, TORSO_Z=0.08, HEAD_Z=0.12
  as defaults, dense hold keys every frame in the crossing window,
  and a per-frame snap gate that exits 2 on failure.
- `SNAP-SOONER-DEFAULT-20261101.json` in this folder: the same numbers
  as machine-readable data for future builders.
- `STUDY-AND-WORKFLOW-20261101.md` in this folder: why it works,
  anatomy, animation principles, and the start-from-here checklist.

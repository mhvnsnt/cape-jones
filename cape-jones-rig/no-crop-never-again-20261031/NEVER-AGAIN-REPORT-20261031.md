# No-crop NEVER-AGAIN report — 2026-10-31

Mars order (2026-10-31 19:47 CDT, replying to the lean no-crop contact):
"Okay cool, you fixed the windows and everything, continue to pull in
industry standard stuff and wire it up 100% to solve that as an issue
so it never happens again."

Folder: `no-crop-never-again-20261031/`, approval 0/1, no repo push,
NO original builder file edited or overwritten. Migrated patterns live
in `migrated_patterns/`, migrated full scenes in `renders/fullscene/`.

## Counts, with percentages (task rule: never a bare list)

- Builders inventoried: **46** (audit said ~35 files / 50+ sites;
  current scan: 40 files with explicit `expand=False` (62 sites) + 6 files
  with `.rotate()` defaulting to expand=False = **46 files, 73 sites**).
- Pattern-migrated (new stress renders PASS check_no_clip): **46/46 = 100%**.
- Grey opaque canvas flagged: **12/46 = 26%** (list below). Save-time
  `convert('RGB')` alone: 26/46 = 57% -- that is a display save, NOT a
  canvas flag; the gate must run on the RGBA pre-save file.
- Full-scene migrated and gate-verified: **1/46 = 2%** (joint_locked_rig_v7c,
  apose + extreme pose, see below). Full-scene migration for the other
  **45/46 = 98% is still owed** -- pattern migration is NOT full-scene
  migration, and this report does not claim otherwise.
- Methods: **20 total, 9 RUN / 11 MAPPING = 45% run, 55% mapping**.
  Mappings are labelled mappings, never quoted as runs.
- Mandatory gate: `gate_mandatory.py` -- PASS exit 0, FAIL exit 1,
  FLAGGED exit 2. Log: `gate_logs/delivery-log.jsonl`.

## Standardized stress tests (same input, same transforms, every builder)

Inputs: apose plate `rig-apose-v7c-clean-transparent.png` (1100x1500,
373,846 alpha px) and limb piece `cut-limbs-v7c/Arm_Front_Lower.png`.
Reference = same transform on a padded canvas, then trim -- that
separates clipping from resampling. Numbers repeat where the pattern
repeats; that is expected, and it is stated here, not hidden.

- **limb_rotate_160**: ref 20153 px; OLD 20148 px, lost 5 px, gate PASS, edge {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}; NEW 20149 px, lost 4 px, gate PASS, edge {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}.
- **whole_rotate_shear**: ref 373819 px; OLD 320919 px, lost 52900 px, gate FAIL, edge {'top': 0, 'bottom': 0, 'left': 461, 'right': 0}; NEW 373813 px, lost 6 px, gate PASS, edge {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}.
- **offedge_paste**: ref 20151 px; OLD 4242 px, lost 15909 px, gate FAIL, edge {'top': 0, 'bottom': 50, 'left': 99, 'right': 0}; NEW 20151 px, lost 0 px, gate PASS, edge {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}.

Honest correction inside these numbers: the centred limb rotate at
160 deg does NOT clip on the old pattern (lost 5 px resampling, gate
PASS) -- a centred limb usually survives, which is why the window
survived so long. It clips on wide, off-centre, or leaning poses,
exactly the whole-figure and off-edge cases above, where the old
pattern loses 52,900 px (14.1%) and 15,909 px (79%) and FAILS the gate.

## Full-scene migration (the one that actually ran end to end)

- `v7c_nocrop.py` (migrated joint_locked_rig_v7c, PAD 400, all coordinates
  shifted, transparent canvas, labels off, trim bbox+40 at save):
  apose 709x1122, 377,511 alpha px, margins 40/40/40/40, edge 0, GATE PASS;
  extreme pose (arms +-160, legs -60/60, lowers 80/-80) 731x1277,
  390,432 alpha px, margins 40/40/40/40, edge 0, GATE PASS.
  OpenCV cross-check (rig venv, cv2 5.0.0): apose cv2 bbox [40,40,629,1042],
  extreme [40,40,651,1197] -- matches Pillow bbox.
  `gate_mandatory.py --check-builder v7c_nocrop.py` = PASS (exit 0).
  `gate_mandatory.py --check-builder joint_locked_rig_v7c.py` = FLAGGED
  (exit 2): expand=False, rotate without expand=True, grey canvas,
  paste_at without paste_nocrop. The original stays flagged until
  it is replaced by its migrated version -- it is not claimed fixed.

## Per-builder table

| Builder | Sites | Pattern | Grey canvas | Status |
|---|---|---|---|---|
| build_exaggerated_deep_squat.py | 3 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| build_hip_lower.py | 3 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| build_true_final_flex_v2.py | 3 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| clean-100-20261031/exposure-clips/rig-v7c-clean100.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| clean-100-20261031/flex-opposition/build_flex_opposition_20261031.py | 4 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| dance-arm-snap-20261031/build_arm_snap.py | 2 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| dance-improved-20261031/build_dance.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| dance-kneefeet-fix-20261031/fix_dance.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| dance-kneefeet-fix-correction-20261031/build_corrected.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| dance-kneefeet-fix-correction-20261031/fix_dance_v1.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| depth-25d-blockers-broken-20261031/cowl_gate_v2b.py | 1 | M1 limb rotate | no | MIGRATED-PATTERN |
| drawing-masters-upgrade-20261031/build_upgrade.py | 2 | M1/M2 rotate + M2 whole-figure shear + M3 paste | no | MIGRATED-PATTERN |
| dual-light-variants-20261031/build_base.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| face-cowl-snap-wire100-20261031/snap_figure.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| face-cowl-snap-wire100-20261031/test_snaps.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| fight-and-sheets-20261031/build_dance_variants.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| fight-and-sheets-20261031/build_fight.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| forearm-fist-v4-20261031/build_fist_v4.py | 1 | M1/M2 rotate + M3 paste | no | MIGRATED-PATTERN |
| forearm-fist-v4-20261031/build_fist_v4b.py | 1 | M1/M2 rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| forearm-fist-v4-20261031/build_fist_v4c.py | 1 | M1/M2 rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| forearm-fist-v4-20261031/build_fist_v4d.py | 1 | M1/M2 rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| gap-close-rig-20261031/build_gap_close.py | 8 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| gap-close-rig-20261031/rebuild_punch.py | 2 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| ginyu-force-limits-broken-20261031/build_limits_broken.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| ginyu-force-poses-20261031/build_ginyu_force.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| hand-tpose-flatten-20261031/build_combined.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| hand-tpose-flatten-20261031/build_tpose_flatten.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| inbetween-20261031/build_inbetween.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| joint-cleanup-20261031/build_restore_originals.py | 3 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint-cleanup-20261031/build_test_cap_omit.py | 3 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig_v4.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig_v5.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig_v6.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig_v7.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| joint_locked_rig_v7b.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| joint_locked_rig_v7c.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| limits-broken-10x10-20261031/build_10x10.py | 5 | M1 limb rotate + M2 whole-figure shear + M3 paste | no | MIGRATED-PATTERN |
| movements-interp-v2-20261031/build_interp_v2.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| pose-dialects-20261031/build_poses.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| pose-dialects-fix-face-cowl-20261031/build_fixed.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| pose-dialects-fix-face-cowl-20261031/check_face_cowl_snap.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| poses-as-movements-20261031/build_movements.py | 1 | M1 limb rotate + M3 paste | YES | MIGRATED-PATTERN + GREY-CANVAS-FLAG |
| repose_tests_v2.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| wrist-attach-fix-20261031/build_library_demos.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |
| wrist-attach-fix-20261031/build_wrist_fixes.py | 1 | M1 limb rotate + M3 paste | no | MIGRATED-PATTERN |

Status key: MIGRATED-PATTERN = that builder's pattern, run through the
standardized stress tests above, passes the gate on its NEW renders,
with a migrated-pattern file in `migrated_patterns/` and old/new limb
renders in `renders/<stem>/`. GREY-CANVAS-FLAG = that builder also uses
a grey opaque canvas, so its full scene cannot pass the alpha gate
until its figure layer becomes transparent RGBA (background, if any,
as a separate layer). Pattern migration alone does not clear that flag.

## Mandatory gate (how it never happens again)

- `gate_mandatory.py <file-or-dir>` -- exit 0 PASS (ship), 1 FAIL (edge
  touch / margin <= 0 / outside protected square -- DO NOT SHIP),
  2 FLAGGED (banned pattern in source -- migrate first).
- `gate_mandatory.py --check-builder <builder.py>` -- flags expand=False
  without a padded-canvas + trim migration, rotate() without expand=True,
  grey canvas, and paste_at() without paste_nocrop. A padded-canvas +
  trim migration (PAD + shift + trim, like v7c_nocrop.py) is PASS,
  not flagged -- the pad holds the swing, the trim proves it.
- Every gate run appends to `gate_logs/delivery-log.jsonl`. A delivery
  with no log entry is treated as ungated.
- Full checklist: `DELIVERY-CHECKLIST.md` in this folder. Delivery crop
  is export-only, after the gate, inside the protected-square spec.
- CI test actually run: gate_mandatory on a deliberately edge-touching
  file exited 1 (FAIL, correct); on the fullscene renders it exited 0.

## 10 industry + 10 experimental methods (RUN vs MAPPING, labelled)

Full JSON: `methods_proofs/methods-20261031.json`. Proof files in
`methods_proofs/` where a run produced one.

Industry -- RUN: I1 FFmpeg pad filter (1900x2300, edge 0); I2 ImageMagick
-extent (1900x2300, alpha 373,846 preserved); I10 SVG viewBox = alpha bbox
(248,253,876,1295). Industry -- MAPPING (not run here): I3 Krita/GIMP canvas
size; I4 Resolve/Premiere safe-area + Auto Reframe; I5 After Effects ROI /
overscan; I6 Spine/Moho mesh; I7 OpenToonz/Tahoma2D camera; I8 Harmony camera
peg (trial blocked at card step); I9 Animate stage + safe area (sign-in blocked).

Experimental -- RUN: E1 dynamic per-frame canvas (trim bbox+40); E4 depth-aware
overscan (2.0x figure, giant margin 101px in the prior size-power folder);
E5 dilate-alpha safety margin (373,846 -> 563,021 dilated px, margin test);
E6 temporal union bbox (over 23 fixed-canvas old frames: (0,227,1084,1500) --
touches x=0 and y=1500, so a whole-clip canvas must be union+40, not 1100x1500;
an earlier draft union over trimmed frames was corrected, because trimmed
frames live in different local spaces and that union is invalid); E9 2x
pyramid (2x trim, downscale x0.5 to 713x1127, alpha 388,394 vs orig 373,846,
resampling difference, not clipping; an earlier draft that resized to a fixed
1100x1500 was corrected, because that distorts aspect); E10 CI fail-loud hook.
Experimental -- MAPPING: E2 content-aware expansion (never invents pixels);
E3 learned bbox (MediaPipe/SAM, no model run); E7 GPU overscan (Blender Cycles
overscan %, no GPU render here); E8 AI outpainting (no model run).
Blender side, re-run in this folder (settings only, no render claimed):
Blender 5.2.3 headless, `blender_nocrop_setup.py` prints use_border=False,
use_crop_to_border=False, film_transparent=True after set.

## Still owed -- not claimed

- Full-scene migration + gate verification for 45/46 builders (98%).
- Grey-canvas transparent-layer migration for 12/46 builders (26%).
- Vendor runs for the 11 mapping methods (Harmony/Animate trials blocked
  on sign-in / card, as recorded in the parent chat -- mappings are not
  quoted as runs, and no trial is claimed complete).
- Per-shot application of the mandatory gate to the 30 shots (0/30).
- Approval of this pack: 0/1. No repo push made. No original file edited.

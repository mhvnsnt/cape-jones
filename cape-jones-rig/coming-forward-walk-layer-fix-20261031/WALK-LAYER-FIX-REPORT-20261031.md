# Coming-forward walk — layer fix — 20261031

Mars's order (2026-10-31 20:39 CDT, replying to coming-forward-walk-20261031.gif):
arms down in front, but the biceps are underneath the torso — one of the
already-solved layering issues. Fix it the way it has been fixed before,
wire the spot-and-fix-ahead-of-time gate up 100%, show the fixed version.
No new layering rule was invented. This is the existing snap system.

## What was wrong, exactly

The original walk builder called `snap.figure(550, cfg)` with NO snap
argument — the normal pass: upper arm BEFORE torso/collar, lower arm
AFTER torso. So when an arm came down in front of the chest, the torso
painted over the bicep. The forearm/fist was already in front; the
bicep was eaten. That is Mars's "biceps underneath his torso" defect,
not a new pose problem.

## Per-frame measurement (88 side-frames: 44 frames × L/R)

Gate used: `pose-dialects-fix-face-cowl-20261031/check_face_cowl_snap.py`
(angle gate, runs BEFORE rendering) + two after-the-fact pixel proofs.
No block range: every row below is its own frame/side decision.

- Face snap: lower_vs_head = 0 on ALL 88 side-frames. No face snap
  anywhere. Face gate (>5,000 px) never trips.
- Cowl snap: elbow_dy = +164..+184 px (elbow BELOW shoulder) on every
  side-frame, from the angle-gate run. Cowl-candidate requires elbow
  >50 px ABOVE shoulder, so no cowl candidate anywhere. Whole-chain
  cowl is BANNED anyway; cowl is upper-only.
- Chest snap (forearm-vs-torso >1,000 px): 18/88 side-frames.

Chest-snap rows (all CHEST-SNAP, layer order torso < arm < head):

| frame | side | forearm+fist vs torso (px) | bicep eaten, old pass (px) | chest-masked upper total, report-only (px) |
|---:|---|---|---:|---:|
| 0 | L | 2,200 | 10,937 | 10,393 |
| 0 | R | 1,383 | 10,871 | 10,280 |
| 1 | L | 2,010 | 10,962 | 10,418 |
| 1 | R | 1,285 | 10,879 | 10,276 |
| 2 | L | 1,656 | 10,877 | 10,345 |
| 3 | L | 1,236 | 10,876 | 10,314 |
| 37 | L | 1,236 | 10,876 | 10,314 |
| 38 | L | 1,656 | 10,877 | 10,345 |
| 39 | L | 2,010 | 10,962 | 10,418 |
| 39 | R | 1,285 | 10,879 | 10,276 |
| 40 | L | 2,200 | 10,937 | 10,393 |
| 40 | R | 1,383 | 10,871 | 10,280 |
| 41 | L | 2,200 | 10,937 | 10,393 |
| 41 | R | 1,383 | 10,871 | 10,280 |
| 42 | L | 2,200 | 10,937 | 10,393 |
| 42 | R | 1,383 | 10,871 | 10,280 |
| 43 | L | 2,200 | 10,937 | 10,393 |
| 43 | R | 1,383 | 10,871 | 10,280 |

Counts: L chest-snap 11 frames (0,1,2,3,37,38,39,40,41,42,43);
R chest-snap 7 frames (0,1,39,40,41,42,43). Total 18/88 = 20%.
No-snap: 70/88 = 80%, forearm-vs-torso 0–989 px on those rows.

Honest measurement limits, stated not hidden:
- "Forearm vs torso" is the v7c lower-limb piece, which is ONE crop
  containing cuff + fist. The fist cannot be segmented separately
  from the forearm in this rig, so there is no separate hand-vs-torso
  pixel count — lower_vs_torso IS forearm+fist combined. No hand
  number was invented.
- "Bicep eaten" (upper_eaten, 5,889–10,962 px per side-frame over the
  whole walk) is the pixel diff between the normal pass and the
  chest-snap pass for that side. It is torso+collar occlusion of the
  upper arm, NOT the decision criterion.
- Chest-masked split (torso-only, collar excluded) is REPORT ONLY:
  torso-only diff is 5,200–6,300 px on EVERY frame, even passing
  frames, because upper arms always overlap the torso at the shoulder
  attachment. A chest-masked >1,000 rule would snap every frame and
  break side arms, so it was removed from the gate and kept as a
  report column only. The decision criterion stays the forearm gate
  (>1,000 px) + Mars's 20:39 eye-check that the bicep-under-torso
  in this walk IS wrong.
- Chest is a WARNING in the refined rule generally. In THIS walk
  Mars already ruled it wrong, so the gate treats these 18 rows as
  FAIL when unsnapped (G3) — that is his ruling applied, not a
  general rule change.

## The fix

New builder `build_walk_layer_fix.py` in this folder (frozen builders
NOT edited, original walk untouched). It calls
`face-cowl-snap-wire100-20261031/snap_figure.py figure(550, cfg, snap=...)`
with the per-frame table from `walk_snap_table.json` (88 rows):
chest rows get the whole arm chain AFTER torso, BEFORE head
(torso < arm < head); all other rows get the normal pass. Everything
else is identical to the original walk: same keys
(CONTACT-L @0.70, PASSING @0.95, CONTACT-R @1.20, PASSING @1.40,
CONTACT-L @1.60 + 4f hold @1.60), SEG=10, 44 frames @24fps,
1600×1800 canvas, grey background + ground band, feet-on-1500 anchor.

Proof the fix changed ONLY the snapped rows (old vs fixed frame diff,
pixels differing >10):
frame 0: 5,403; frame 1: 5,473; frame 2: 2,834; frame 3: 3,008;
frame 20 (no snap): 0 — pixel-identical; frame 37: 12,241;
frame 39: 26,231; frame 40: 26,458; frame 43: 26,458.
Non-snap frames are untouched by construction and by measurement.

## Gate wired as a mandatory pre-delivery step (the point of the order)

`gate_walk_snap.py` + `walk_snap_table.json`, run by
`build_walk_layer_fix.py` as a subprocess BEFORE any frame is built —
if the gate does not exit 0 on applied=fixed, the builder refuses
to build. Rules: G1 face requires face-snap; G2 cowl-whole BANNED,
cowl-upper only with eye-check; G3 chest-snap + eye-check requires
applied chest/face in this walk (Mars 20:39 ruling); G4 chest-masked
px REPORT ONLY, never a fail; G5 face snap with NO SNAP reason is a
FAIL. Exit 0 PASS / 1 FAIL / 2 missing table.

Measured gate results:
- Old walk (applied=old): FAIL, exit 1, 18 fails — exactly the 18
  chest rows above, each "CHEST-SNAP + eye-check upper eaten,
  applied=none".
- Fixed walk (applied=fixed): PASS, exit 0, 0 fails (88 rows, 88
  report-only chest-masked warnings, which are not fails).

Fixed-walk measurements (`fixed_walk_measurements.json`):
44 frames, feet_y = 1500 on all 44, spread 0 px, edge-touch frames
none, min margin 299 px, PASS True. Feet-planted and no-crop
behaviour unchanged from the original walk.

## Industry-standard layer-order methods — run vs mapping

RUN in this build (not just named):
- `snap_figure.py` per-frame draw-order override: chest = whole chain
  re-drawn after torso, before head. This is the keyframed Z-nudge
  pattern.
- `gate_walk_snap.py` mandatory pre-delivery gate (above).

MAPPINGS (industry equivalents already wired in
`face-cowl-snap-wire100-20261031/INDUSTRY-LAYERING-METHODS-20261031.md`,
not re-run as vendor tools here):
- Harmony Z-depth ordering + drawing substitution (snap = keyframed
  Z-nudge) — matches the chest pass.
- Animate layer parenting / reparenting (snap = temporary reparent
  for one frame).
- Godot Z index + RemoteTransform2D (render order independent of
  hierarchy).
- Spine keyable draw order + whole-asset cutting.
- Traditional cel stacking (default cape-back, legs, torso, arm,
  neck, head; snap = documented override).
- OpenToonz / Tahoma2D SO (stacking order) value animated per frame.
- Blender Grease Pencil layer tree: MAPPING only in that doc, not a
  claimed GP file here.
Not applicable, named: true 3D camera depth, auto lip-sync.

## Files in this folder

- `coming-forward-walk-LAYER-FIXED-20261031.gif` (44f @24fps) — NEW,
  viewed by Muse (contact + frame 40 full frame).
- `coming-forward-walk-LAYER-FIXED-20261031.mp4`
- `frames-fixed/` — 44 JPG frames.
- `before-after-contact-20261031.png` — old vs fixed frames 0, 20,
  40 + frame-40 torso zoom, viewed by Muse.
- `walk_snap_table.json` — 88-row per-frame/per-side table.
- `gate_walk_snap.py`, `gate_fixed.json` — mandatory gate.
- `build_walk_layer_fix.py`, `build_table.py`,
  `measure_upper_eaten.py`, `measure_chest_masked.py`,
  `upper_eaten_measurements.json`, `chest_masked_measurements.json`,
  `fixed_walk_measurements.json`, `build_fixed.log`.

## Status

- Size-transformation power approval 1/1 stands separately, NOT
  re-asked.
- Fixed walk approval: 0/1 — Mars has not seen the fixed version yet.
- No repo push (per task). Original walk and frozen builders untouched.
- Trade-off carried from the dance arm-snap work, stated plainly:
  snapped uppers are bulkier over the chest than the old eaten
  version — that bulk IS the arm being in front, which is what Mars
  asked for. If he wants it slimmer, that is a new piece/redraw
  decision, not a layer-order fix.

# Preset B arm-front-snap fix — 2026-11-01

## Correction, Mars 2026-11-01 14:42 CST — learn it, do not make him repeat it

Preset 2 = B, Foster's punch/walk structure, Foster's walking punch cycle.
When he starts walking, after about 2–3 seconds in the move (3.08s in the
move itself, 4.08s in the clean output because of the 1s frozen stand),
his arms cross his torso and were NOT on the top layer — the upper arms
were eaten by the torso and the forearms/fists floated.

**Arm-front-snap is automatic for EVERY build from now on, including walk
cycles, not a per-clip request.** When an arm/forearm/fist crosses the
torso/chest threshold, the WHOLE arm chain (upper + forearm + fist +
elbow cap) snaps momentarily to the layer ABOVE the torso, per arm, per
frame, torso < arm < head for chest-only. Torso must NEVER eat arms,
especially upper arms / biceps. This applies to A, B, C, and every
future preset and clip, automatically, so Mars does not have to repeat it.

## What B is, exactly

Clean B, `B-FOSTERS-STRUCTURE-CLEAN-20261101.mp4`, 164f, 1100x750,
24fps, 6.833333s, md5 `6d733f4e1d022a4574faf1ab3d8e7b10` (unchanged below):

- Output 0–23: 1s frozen stand, first frame of the move (apose, no snap).
- Output 24–97: punch segment, 74f — chain-punch re-cut frames 0–73
  (windup → snap → impact → recover → across-down placement).
- Output 98–163: walk segment, 66f — chain-walk frames 0–65
  (contact A → passing A → contact B → passing B, repeated).
- Sound: `B-FOSTERS-STRUCTURE-20261101.wav`, same in the snapped version.
- Background: grey-128 video frame, same in both versions.
- No banner, no placeholder label in either clean version.

B is NOT from the successor chain that A and C were cut from, so the
A/C snap fix could not simply be re-cut for B. B had to be re-rendered
from its own two rig-angle chains (see Method).

## Method — re-render, not flat-video re-layering

A flat MP4 cannot be re-layered: the eaten upper-arm pixels are gone.
So both chains were re-rendered from rig angles with the sensor ON,
exactly as the A/C successor snap fix did:

- Sensor: `arm-front-snap-auto-20261101/arm_front_snap_sensor.py`,
  `sense_from_angles(cfg)` — forearm alone vs Torso_Chest mask at
  1100x1500, snap = overlap > 1000px (measured gap: out-to-side
  0–268px, crossed 1538–8969px in the original audit).
- Renderer: `anatomy-fix-bundle-20261101/build_anatomy_fix.py`,
  `figure2/render2` — snapped side's whole chain after torso, before
  neck/head (torso < arm < head). Face-top keys: none in punch or walk,
  so chest_top = snap sides.
- Frame generation replicates `rig-chains-20261031/build_chains.py`
  exactly: hold counts, 7 inbetween (punch) / 5 inbetween (walk),
  breakdown +10deg upper at j=3, +8deg lower at j=5, punch overshoot
  5% arms-only + settle + return to apose, walk cycle (ends on
  contact A) so no overshoot/return. Ground compensation measured
  with render2 (layer order does not change the silhouette union).
- No foot mirror: the anatomy bundle's leg1-exception is NOT reused
  here. Legs follow the original punch/walk configs, universal
  knee-feet rule only.
- No other change: same segments, same timing, same sound, same
  background, same poses. Only arm layer order changes, and only on
  snap frames.

Builder: `build_b_snap.py` in this folder. Xsheet regenerator (sensor
only, no re-render, used after a CSV writer bug in the first run):
`gen_xsheet.py`. The first run's render was kept; only the xsheet was
regenerated. The CSV bug was a missing arm field in stand rows, fixed
in both scripts.

## Measured, not guessed — sensor counts

Full chains, before the B cut:

- Punch chain: 75f, snap 51f.
- Walk chain: 67f, snap 33f.

In the clean B output (164f):

- Snap frames total: **83/164**.
- Punch segment: **51/74** output frames.
- Walk segment: **32/66** output frames.
- Stand: 0/24 (apose, no snap).

Walk snap runs, output frames (clean timing; subtract 24f / 1.0s for
move timing, where walk starts at move frame 74 = 3.08s):

- 98–102, both arms, walk contact A, 4.08–4.25s.
- 103, right arm only, 4.29s.
- 104–108, both arms, 4.33–4.50s.
- 109, left arm only, 4.54s.
- 127, left arm only, 5.29s.
- 128–134, both arms, 5.33–5.58s.
- 135, right arm only, 5.62s.
- 136–140, both arms, 5.67–5.83s.
- 141, left arm only, 5.88s.
- 159, left arm only, 6.62s.
- 160–163, both arms, 6.67–6.79s.

Walk contact A example, output 98 = walk frame 0: L overlap 5076px,
R overlap 4218px, chest_top L,R, arm_upper L 30 / R -30, arm_lower
L -20 / R 20.

Punch snap runs, output frames: 31 (L only), 32–41 (both), 42–43 (R
only), 44–52 (both), 53–65 (R only), 66 (both), 77 (R only), 78–79
(both), 80–91 (L only). Punch across-down hold example, output 82 =
punch frame 58: L overlap 6919px, R 0px, chest_top L, arm_upper
L -70 / R 40, arm_lower L 80 / R -40.

Full per-frame table: `B-ARM-SNAP-XSHEET-20261101.csv` (164 rows).

## What was eaten before, eye-checked

Output frame 98, walk contact A, original clean B:

- Before: upper arms missing. Shoulders show torso/cape, biceps are
  absent, forearms + fists float below elbow caps. The chain is split:
  upper rendered before torso (eaten), forearm after torso (floating).
- After (snapped): both upper arms present on top of the torso,
  continuous shoulder → elbow → forearm → fist, biceps bulging over
  the chest sides. Same pose, same angles, only layer order changed.

Output frame 136, walk passing B, snapped: arms continuous on top,
biceps over torso sides, not eaten. Output frame 82, punch
across-down hold, snapped: left arm crossing the chest on top of
the torso, continuous. Check stills in `check/`: `orig-98.png`,
`new-98.png`, `new-136.png`, `new-82.png`.

Frame-difference measurement (original vs snapped, same frame):

- Frame 98 (snap): mean abs diff 1.08, pixels diff >30 = 0.6% of frame.
- Frame 136 (snap): mean abs diff 1.23, pixels diff >30 = 0.7%.
- Frame 67 (non-snap control, punch inbetween): mean abs diff 0.49,
  pixels diff >30 = 0.1% — re-encode baseline only.
- Snap frames change ~6x more pixels than the non-snap control,
  concentrated in the arm region, as expected for an upper-arm layer
  change. Non-snap frames are the same pose, re-encode noise only.

## Delivered

Folder: `preset-b-arm-snap-20261101/`

- `B-FOSTERS-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.mp4`, 1100x750,
  24fps, 164f, 6.833333s, h264 + AAC, decode_ok, md5
  `1ecc666968d88f053cac1a6f269acb66`, moov at 36 (faststart),
  380,023 bytes.
- `B-FOSTERS-STRUCTURE-ARM-SNAP-FIXED-CLEAN-20261101.gif` alongside,
  md5 `282a136a8a13a877d9be4b392fe42eb9`.
- Same sound as clean B, same 1s frozen stand, same segments.
- No banner on any frame, no placeholder label in the filename.
- Flicker gate, whole-frame WCAG proxy, 12fps, threshold 25.5:
  82 sampled frames, max jump 2.14, 0 flashes, PASS.
- Original clean B untouched: md5 re-checked after this build,
  still `6d733f4e1d022a4574faf1ab3d8e7b10`. Original wav untouched.

## Still owed, plainly

- Mars approval of snapped B: **0/1**. Do not call B fixed to Mars
  until he sees the snapped clip and says the walk arms are on top.
- Repo landing: local only, no PR claimed, not verified on main.
  This snapped B is NOT yet in the repo preset folder; the repo
  preset landing (PR #337) contains the unsnapped clean B.
- B's other off-ness: Mars said B is a little off and needs
  fixing/improving later, and that after snapped B is shown he has
  one more detail to fix about B, unknown yet, not guessed here.
  This snap fix covers arm layer only. It does NOT claim B is
  perfect, and it does NOT claim the other detail is fixed.
- Arm-front-snap from now on: automatic in every builder, including
  walk cycles. Any future clip that ships with a torso-eaten arm
  is a builder bug, not a per-clip request.

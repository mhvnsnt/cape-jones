# Arm-front-snap eaten in last seconds — FIXED, Mars 2026-11-01 12:52 CST

## Identification, measured, not guessed

Placeholder B last 3s = walk only, no chest-cross — ruled out.
Placeholder A last 3s and Placeholder C both contain the same eaten poses,
because both are cut from the same successor chain
(`rig-chains-20261031/successor-pose-dialects-20261031.mp4`, 134f, 5.583333s).

Sensor: `arm-front-snap-auto-20261101/arm_front_snap_sensor.py`
`sense_from_angles()` — forearm alpha vs Torso_Chest mask at 1100x1500,
snap >1000px. Builder root cause, from `rig-chains-20261031/build_chains.py`
`figure()`: a non-top arm renders its upper arm BEFORE pelvis/torso and its
forearm AFTER torso, so a crossing non-top arm is split — bicep hidden
behind torso, forearm + fist floating in front. Flat MP4 cannot be
re-layered; this fix re-renders from the rig with the sensor ON.

Snap failures in the successor chain:
- JoJo 02 fashion twist: R 7,385px, top=(), snap R only. R bicep eaten,
  R forearm + fist floating across chest.
- Stand 02 user figure only: L 4,651px, R 2,728px, top=(), snap both.
  Both biceps cut at the shoulders, forearms crossed at waist.
- NOT failures: JoJo 03 R 2,135px but top=(R,) already (face-top, above head);
  Ginyu 01 sensor 0px/0px.

## Fix method

`build_snap_successor.py` re-renders the full successor chain (DIAL_KEYS,
n_inb=5, same transitions, same ground compensation: silhouette bottom =
652 video px, measured with the original render) with snap ON, using the
anatomy bundle's proven `figure2()`:
- per frame, per arm: `sense_from_angles(cfg)`
- chest_top = sensor sides not in face_top
- face_top = original top keys (union in transitions, as in original builder)
- chest snap = whole chain (upper + forearm + fist + cap) after torso,
  before neck/head: torso < arm < head
- face_top = whole chain after head, as originally
- no knee-feet bundle exception here; feet follow the original cfg

`recut_fixed_placeholders.py` re-cuts A and C from the snapped successor
with the exact original builder steps: same segments, same 1s frozen stand,
same banner on every frame, same original wav, faststart, GIF + contact
sheet. Originals untouched.

## Verified results

Snapped successor: `successor-pose-dialects-ARM-SNAP-FIXED-20261101.mp4`
- 134 frames, 1100x750, 5.583333s — frame-for-frame match to original 134f
- xsheet `successor-snapped-xsheet-20261101.csv`: 134 rows, 40 snap frames
- JoJo 02 key frames 24–27: R 7,385px, chest R, face empty
- Stand 02 key frames 120–123: L 4,651px, R 2,728px, chest L,R

Fixed Placeholder A (primary, the "first one"):
`TEMPLATE-PLACEHOLDER-A-SMILING-STRUCTURE-ARM-SNAP-FIXED-20261101.mp4`
- 121f, 1100x750, 24fps, video 5.041667s, h264 + AAC, decode_ok
- md5 72748da39071aa6a45b0f81fc2c14191, 332K
- Stand 02 at 4.54s: before — both biceps thin / cut at the shoulders by
  torso; after — both biceps bulge over torso, black outline continuous
  shoulder → elbow → forearm → fist, fists crossed at waist.
  Before/after: `full/A_4p54.png` vs `full/AFIXED_4p54.png`,
  crops `full/crop_A_4p54.png` vs `full/crop_AFIXED_4p54.png`.
- A at 2.04s is a JoJo 03 transition, already face-top, so it is unchanged
  in the fixed clip — that frame was not a snap failure. The eaten frames
  in A are Stand 02 (4.54s, last 3 seconds) and the JoJo 02 boundary at 2.0s.

Fixed Placeholder C (same JoJo 02 pose, follow-through of the same fix):
`TEMPLATE-PLACEHOLDER-C-SMILING-5LAYER-ARM-SNAP-FIXED-20261101.mp4`
- 120f, 1100x750, 24fps, video 5.000000s, h264 + AAC, decode_ok
- md5 38b7fae3982d752adefb6cbd828fd87d, 330K
- JoJo 02 at 2.04s: before — R arm across chest, forearm + fist visible,
  but no bicep at the right shoulder, torso white fills the shoulder;
  after — R bicep is a large white bulge at the right shoulder, on top of
  torso, continuous to elbow, forearm, fist.
  Before/after: `full/C_2p04.png` vs `full/CFIXED_2p04.png`,
  crops `full/crop_C_2p04.png` vs `full/crop_CFIXED_2p04.png`.

Sound: kept, original A and C wavs, same snap/blip timing. A audio stream
is 5.080s vs original 5.038s (2 AAC frames, encoder padding); video is
exactly 5.041667s in both.

Flicker, whole-frame WCAG proxy, 12fps, threshold 25.5:
- Fixed A: 61 frames, max jump 2.13, flashes 0 — PASS
- Fixed C: 60 frames, max jump 2.14, flashes 0 — PASS
- Original A for comparison: 61 frames, max jump 2.13, flashes 0

Originals untouched, md5-checked:
- A original 35adf1f3d7c9bf2991293e97db570b07 — matches pre-fix record
- C original a2b5832977601a27f37b9753a09e3771 — matches pre-fix record
- Successor original 147954985eb02e92d4eaec9e88f022c2 — untouched

Key before/after stills (full-res, not key renders):
- JoJo 02: `full/ORIG_JoJo_0.png` vs `full/FIXED_JoJo_0.png`
- Stand 02: `full/ORIG_Stand_.png` vs `full/FIXED_Stand_.png`

## Approval / landing

- Mars approval of the fixed A and C clips: 0/1 — Mars has not seen them yet.
  Do not claim fixed until Mars sees the fixed clip and says the arms are on top.
- Repo landing: local only, no PR claimed. Folder to land, PR-only, after
  Mars approval: `arm-snap-last3-fix-20261101/` (excluding `work/` scratch
  and `frames-snapped/` intermediate JPGs if the landing lane prefers).
- This fix does not close the earlier "one OTHER crossed-arms version is
  still WRONG" (2026-11-01 11:48 CST) until Mars confirms the fixed A (and C)
  are the version he meant.

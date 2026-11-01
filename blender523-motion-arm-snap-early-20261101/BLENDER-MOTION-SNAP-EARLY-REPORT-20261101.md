# Blender motion — arm-front-snap earlier — 2026-11-01

Mars 2026-11-01 15:58 CST, reacting to blender523-legs-fixed-MOTION-20261101.mp4:
motion is good except arms start to get eaten by torso. Arms need to go
to the top layer above torso SOONER, before crossing it, and stay on
top while crossing, then it will be perfect.

## What changed — only Z keys, nothing else

Source: blender523-overlay-locked-20261101/cape_jones_toon_blender523_OVERLAY_LOCKED.blend
(legs-fixed perfect placements, GP overlay hidden for clean renders).

Old snap: arm draw planes keyed to Z 0.11 only at f25 (crossed peak).
Torso Z 0.08, head Z 0.12. Arms moving toward the torso from f14
(after f13 arms-out) were still ramping up from rest Z, so the torso
ate the start of the crossing.

New snap: both arm draw planes (Draw-Arm_Front.png, Draw-Arm_Back.png,
whole chains — upper + forearm + fist, no piece change) keyed to
Z 0.11 at f13 (arms-out, before any crossing), held at f14, f25,
f32 and f36, then back to rest Z only at f37 (wide flex, arms clear
of torso), and rest Z again at f48.

Poses, angles, timing, legs, head, neck, collar, cape, camera
(ortho 8.5, 700x950) unchanged. Only arm draw location-Z keys moved.

Timeline reminder: f1 rest, f13 arms-out, f14-f25 inbound crossing,
f25 crossed peak, f25-f36 outbound crossing, f37 flex 120° wide,
f48 shuffle (Leg1 lifted, Leg2 planted).

## Verification — per-frame Z evaluation, script asserted

From snap-early-verify.json, evaluated in Blender from the saved blend:

| frame | Arm_Front Z | Arm_Back Z | torso Z | above torso? |
|---|---|---|---|---|
| f1 rest | 0.03 | 0.035 | 0.08 | rest, beside torso |
| f13 arms-out (NEW snap) | 0.11 | 0.11 | 0.08 | yes |
| f14 first crossing frame | 0.11 | 0.11 | 0.08 | yes |
| f20 mid-crossing | 0.11 | 0.11 | 0.08 | yes |
| f25 crossed peak | 0.11 | 0.11 | 0.08 | yes, below head 0.12 |
| f32 outbound | 0.11 | 0.11 | 0.08 | yes |
| f36 last hold | 0.11 | 0.11 | 0.08 | yes |
| f37 flex (snap off) | 0.03 | 0.035 | 0.08 | clear, wide flex |
| f48 | 0.03 | 0.035 | 0.08 | flex hold |

Crossing window f14-f36: every frame evaluated at exactly 0.11 for
both arms, script assertion passed, no frame below torso during
crossing.

Eye check: frame_020 (mid-crossing) and frame_025 (crossed peak)
both show biceps/upper arms on top of the torso, continuous
shoulder → elbow → forearm → fist, no torso eating any arm.

## Deliverable

- blender523-legs-fixed-MOTION-SNAP-EARLY-20261101.mp4 — 700x950,
  24fps, 48 frames, 2.0s, h264, faststart (moov at 36),
  md5 0e158d1e517f652e18260962379fba9e, 119,850 bytes, silent
  (no audio claimed, same as the original motion clip).
- Frames: frames/frame_001.png – frame_048.png
- Blend: cape_jones_toon_blender523_SNAP_EARLY.blend
- Builders: fix_snap_early.py (keys + frames 1-34), render_rest.py
  (Z verification + frames 35-48 after the first render run stopped
  at frame 34 when its Blender process ended; the snap-early blend
  was already saved, so only 35-48 were re-rendered, no frames
  were changed or re-keyed in between).
- Verify: snap-early-verify.json

Previous motion clip untouched, not overwritten.

## Status

Approval 0/1. This version becomes perfect only after Mars sees it
and confirms arms are never eaten. Repo landing local only,
no PR claimed, not verified on main.

## Known limits, unchanged from legs-fixed

Whole leg rotates as one around the hip; true arms-up flex with
whole pieces is still not claimed (flex here is wide-out 120°).

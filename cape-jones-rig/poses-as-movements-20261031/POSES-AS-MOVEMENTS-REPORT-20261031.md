# Poses as movements, on video — 2026-10-31

Mars, ~18:46 CDT, replying to the v7c-jump COWL-SNAP still: these stills are
good, but poses are not just stills — they are movements, animations — so he
needs to see them on video, and keep building more of them.

## Answer to Mars's question in that message
The still he was looking at (v7c-jump arms-up COWL-SNAP) is NOT a Recoome
pose — "raccoon" in his voice message reads as Recoome. It is Cape Jones's
own v7c jump test pose, arms up, with the wire-100 cowl-snap applied (bicep
over the black cape-collar, upper-only). Recoome's poses are REC-01/02/03 in
the Ginyu Force set, and they are separate files. The pose above it in the
wire-100 sheet is Ginyu 03, a Ginyu-style dance shimmy, not a named member.

## Method, stated plainly
Keys are EXISTING rig poses. Inbetweens are IMAGE interpolation (eased
crossfade between consecutive key images, plus whole-image translation for
jump height / shimmy sway) at 24fps. This is NOT rig-angle inbetweening.
Keys pass knee-feet + face/cowl snap because they are the original files
(layer order preserved inside each key image). A mid-blend frame can ghost
slightly at 50% blend — that is the honest limit of this method.
No new art drawn, no file Mars has seen overwritten.

## Videos (GIF + MP4 each, 24fps, viewed via contacts)
- jump-cowl-snap-movement: 46f / 1.9s — apose, crouch, takeoff, COWL-SNAP
  apex, tuck, land, apose. DEFECT: source clips-v7c jump frames carry
  baked-in red debug label dots (labels are debug only) — this version is
  NOT clean. Use the clean version below instead.
- jump-cowl-snap-movement-clean: 38f / 1.6s — apose, apex raised 100px,
  apose, no debug dots, no clip frames. This is the clean jump to show.
- shimmy-cowl-snap-movement: 70f / 2.9s — Ginyu 03 COWL-SNAP shimmy, hips
  sway +/-40px, +/-3deg, 2 full cycles. Sway blends ghost (double figure
  at mid-blend) — honest limit of translation + crossfade.
- ginyu-force-movement: 64f / 2.7s — neutral, Recoome, Burter, Jeice,
  Guldo, Captain, Captain spread (roll-call order, announce hold, fast
  snap inbetween, hold).
- pose-dialects-movements: 108f / 4.5s — neutral, each of the 8 dialect
  poses, back to neutral between each. Stand pairs are aspect-preserved
  (wide canvas, so they read smaller in frame — correct proportion, not
  squeezed; a v1 with forced 550x750 resize distorted them and was rebuilt).
- move-punch-to-flex: 33f / 1.4s — punch impact, fighting pose, true final flex.
- move-jump-to-shimmy: 33f / 1.4s — land, shimmy, shimmy.
- move-serve-to-guard: 33f / 1.4s — Jeice serve, Guldo guard, fighting pose.
- move-rollcall-snap-to-spread: 33f / 1.4s — Captain entrance, crossed
  command, Captain spread.
Total: 9 videos (8 movement videos + 1 clean jump rebuild), 420 frames.

## New movement-poses
The 4 new sequences above are the new movement-poses, each with a key still
(*-key-still-20261031.png = middle pose of its sequence). They are new
SEQUENCES built from existing rig poses, not new rig-drawn poses — labelled
as such, not claimed as new masters.

## Checks
- Knee-feet: keys pass (original files); blends do not re-pose limbs, so
  no new knee-feet violation is introduced, only blend ghosting.
- Face/cowl snap: keys pass (FACE-SNAP JoJo 03, COWL-SNAP Ginyu 01/03 and
  jump apex are the fixed files); blends preserve each key's layer order.
- No file Mars saw overwritten; all outputs in poses-as-movements-20261031/.

## Approval
Mars approval of each video: 0/1 — the stills being approved does NOT
approve the videos. No repo push made in this task.

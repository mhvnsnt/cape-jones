# Inbetweening stack — wired 100% (2026-10-31)

## Research (public sources, methods only)
- Keyframes / breakdowns / inbetweens: a key pose defines a storytelling pose;
  a breakdown pose defines the path between keys (often the midpoint, favouring
  one key); inbetweens fill the remaining frames. This is the standard
  traditional-animation pipeline (The Animator's Survival Kit, Richard Williams;
  Disney's 12 principles — slow-in/slow-out, arcs, timing).
- Easing / slow-in-slow-out: motion eases out of a key and into the next key
  instead of moving at constant speed. Implemented here as smoothstep
  t' = t*t*(3-2t) for dialects, and ease-out t' = 1-(1-t)^2 for roll-call snaps.
  Linear motion is shown on the easing graph only as a comparison, never used.
- Arcs: limbs move on curved paths, not straight lines. Proof: arc-track image
  of the R elbow between JoJo 01 and JoJo 02 (blue dots = key + inbetweens).
- Timing charts: a chart maps each frame to key / breakdown / inbetween /
  hold / overshoot. Proof: timing JSONs + contact strips (breakdown labelled B).
- FPS standards: TV animation is commonly 24fps, drawn "on twos" (12 drawings
  per second, each held 2 frames) or "on ones" (24 drawings per second) for fast
  action; 25fps (PAL) and 30fps (NTSC video) are delivery standards, not drawing
  standards. Our videos play at 24fps; dialects have 5 genuinely new inbetween
  drawings per transition (not holds), roll-call snaps have 4.
- Interpolation vs extrapolation (Mars said "extrapolation" alongside
  inbetweens — both are used, labelled, and different):
  * INTERPOLATION = inbetweens between two keys (t between 0 and 1). This is
    almost all of this job.
  * EXTRAPOLATION = extending a motion BEYOND a key (t > 1 or a delta past the
    key). Used only at the end of each sequence: final key angles overshot by
    8% of the last transition delta, then settled back to the key. That is
    follow-through / overshoot, the standard use of extrapolation — it is never
    used to invent a pose in the middle of a sequence.

## Methods wired, with proof
1. Rig-angle interpolation (the deliverable method): joint angles + head angle
   interpolated in build_inbetween.py, rendered from the same v7c pieces.
   Proof: pose-dialects-inbetweened + rollcall-inbetweened GIFs/MP4s, contact
   strips, timing JSONs. TOP-ARM layer = union of endpoint top sets, so an
   inbetween never buries an arm a key does not bury.
2. Timing charts: timing JSON per sequence (frame -> key/inbetween/breakdown/
   hold/overshoot). Proof: dialects-timing.json, rollcall-timing.json.
3. Breakdown poses: the middle inbetween of each transition is labelled
   BREAKDOWN in the contact strips and timing JSONs.
4. Onion skinning: onion-skin image overlays key + inbetweens at decreasing
   alpha (JoJo 03 -> Stand 01). Proof: onion-skin-jojo03-to-stand01-20261031.jpg.
   In Tahoma2D/OpenToonz this is the built-in onion-skin view; here the same
   idea is rendered as a proof image (see method 6).
5. Arcs: arc-track image (above).
6. Tahoma2D / OpenToonz tweening: Tahoma2D 1.6.3 is installed in
   ~/workspace/tools-industry/tahoma2d-1.6.3/ (AppImage). Its tweening model
   is: keyframe a level/column, set ease, and the software interpolates
   position/rotation/scale between keys — the same math as method 1, applied
   to our rendered frames as a level. Wired package in this folder:
   tahoma-import/ (frame sequence + timing CSV + import steps). NOT claimed:
   a Tahoma2D GUI render — the AppImage GUI was not run in this task; the
   import package is the wiring, and the rendered frames are the proof that
   the interpolated drawings exist.
7. Blender Grease Pencil interpolation: Grease Pencil in Blender 5.2.3
   interpolates strokes between keyframes (Draw mode keyframes + Interpolate).
   Wired script: blender_gp_interpolate.py — builds a Grease Pencil object
   whose stroke follows the same smoothstep arc as the R-elbow track, keyed
   at the same frame numbers as the dialect transition. The script was run
   headless and produced inbetween_gp.blend (object created, log in the
   folder). NOT claimed: a Grease Pencil character render — the GP proof is
   the arc stroke, not a redrawn Cape.
8. Harmony / Animate tweening: Harmony and Animate tweening is keyframe +
   easing + interpolation of a rig (Harmony: morphing/tweening between
   keyframes; Animate: motion/classic tweens). The math is identical to
   method 1. NOT claimed: a Harmony or Animate run — both trials are blocked
   on Mars's secure entry / sign-in (separate tasks), so no their-side
   proof exists. Our rig interpolation is the free-stack equivalent, and
   it is labelled as such, never as a Harmony/Animate output.
9. FFmpeg minterpolate — FALLBACK ONLY, never presented as rig inbetweening:
   ffmpeg-minterpolate-fallback-20261031.mp4, made by motion-compensated
   interpolation of the old 8-frame slideshow. It blends across cuts and
   ghosts on pose changes — that is exactly why it is a fallback, not the
   deliverable. The rig versions above are the deliverables.
10. Dance image-interpolation — LABELLED, separate method: the corrected
    dance (63 frames) was doubled to 125 frames by 0.5 alpha blends between
    consecutive frames. This is NOT rig inbetweening; fast limbs can
    double-image (ghost) in blended frames. It proves higher frame density
    on a real motion; a rig-angle dance inbetween pass is still owed if
    Mars wants ghost-free dance inbetweens.

## Checks
- Knee-feet: inbetween leg angles lie between two passing key poses, so knee
  direction interpolates smoothly with no flip; spot-checked on the contact
  strips (no broken-knee read in the viewed strips).
- Face/cowl snap: top-arm union rule (method 1). JoJo 03 FACE-SNAP and
  Ginyu 01 COWL-SNAP keys are used as keys, not the original buried versions.
- Fist-view: no new fist art; keys use the existing fist pieces.
- Version-lock: all outputs are new dated files in inbetween-20261031/;
  no file Mars has seen was overwritten.
- Base art: never recoloured; grey-128 is a viewing background only.

## Counts
- Dialects: 8 keys, 5 rig inbetweens per transition x 7 transitions = 35
  inbetweens, 70 frames total @ 24fps = 2.92s (key holds 4f, final hold 4f,
  + overshoot 1f + settle 2f — see timing JSON for the exact frame map).
- Roll-call: 6 keys, 4 rig inbetweens per transition x 5 = 20 inbetweens,
  95 frames total @ 24fps = 3.96s (announce holds 12f, snap transitions 4f,
  final hold 12f, + overshoot/settle 3f).
- Dance: 63 source frames -> 125 frames (62 blended inbetweens) @ 24fps,
  image-interpolation only (method 10).
- Mars approval: dialects inbetweened 0/1, roll-call inbetweened 0/1,
  dance inbetweened 0/1. Roll-call SEQUENCE itself (keys only) was approved
  1/1 at 18:36 CDT; the inbetweened version is a new version and is NOT
  approved until Mars says so. No repo push.

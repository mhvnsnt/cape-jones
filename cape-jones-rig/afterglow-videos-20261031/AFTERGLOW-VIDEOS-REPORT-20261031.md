# Afterglow videos — punch limb + all 30 shots (Mars, 2026-10-31 17:56 CDT)

## Preset (approved 17:49 CDT, Default Afterglow Preset)
Soft rim = soft halo, ONE layer. Default cyan (0,200,255), dilate 6, blur 5,
lag 6, fade 0.50/0.40/0.30/0.20/0.12/0.06. Light-trail rule: trail ONLY in
motion, NEVER at the current position, zero at rest. A first punch build
failed this rule on windup holds (trail drawn at the same spot = a static
rim) and on the final rest frame (only 4 rest frames after recover, inside
the 6-frame lag); both were fixed — same-position trails are skipped, and
the punch was extended to 24 frames so the final frame is true zero.

## 1) Punch limb video — Blender compositor, 24/24 frames
Piece: approved v5 Arm2 FLIPPED forward-punch forearm (knuckles top,
unrotated) ONLY — limb-specific, not whole body. Path: windup hold 3f ->
snap extend across-up (-110) 4f -> impact hold 4f -> recover 3f -> rest
hold 10f. Blender 5.2.3 compositor: dark bg -> AlphaOver trail layer ->
AlphaOver plate layer, Standard view transform (NOT AgX, so cyan is
preserved), CPU, real render, write_still=True. First Blender attempt
failed on a missing PIL import in the script (fixed: bg pre-made outside
Blender); second attempt completed 24/24.
Viewed: windup clean (no trail), snap trail behind the fist, impact
trail, rest frame clean (zero). Files: punch-limb-afterglow-blender-20261031.mp4
+ .gif, contact sheet, blender_punch24/ frames, blender_layers_punch24/.

## 2) All 30 shots — 30/30
Each shot: 12-frame GIF + MP4, trail colour = that shot's rim colour from
shot-specs-30-20261031.json, recorded in shot-afterglow-index-20261031.json
(input RGB + on-screen sample RGB + mix cause). Blender compositor key
frame per shot 30/30 (blender_keys_out/, frame 5): bg -> trail -> plate,
Standard view, no Glare. Full shot GIFs/MP4s are PIL trail renders using
the identical layers (not frame-by-frame Blender renders) — that
distinction is stated, not hidden.
- Moving shots 15/30 (50%): CJ-02, CJ-04, CJ-05, CJ-06, CJ-07, CJ-08, CJ-09,
  CJ-10, CJ-11, CJ-12, CJ-13, CJ-14, CJ-15, CJ-21, CJ-22 — trail present in
  motion, final frame zero.
- Hold/still shots 15/30 (50%): CJ-01, CJ-03, CJ-16, CJ-17, CJ-18, CJ-19,
  CJ-20, CJ-23, CJ-24, CJ-25, CJ-26, CJ-27, CJ-28, CJ-29, CJ-30 — NO trail
  generated while still; on-screen sample = background only (zero at rest).
- Colour: moving shots on-screen sample is input colour alpha-blended
  over dark bg (e.g. gold 255,180,80 -> 197,139,63); hue preserved, no AgX
  shift, because Standard view + no Glare were used. Hold shots: no shift
  because there is no trail.
- Honest limit: shot tests use the clean apose transparent plate as a
  stand-in for every shot, NOT each shot's final plate/background. They
  prove the afterglow application per shot colour/motion class; they are
  NOT final shots. Final-shot plates/backgrounds are still owed per shot.

## 3) Push / land / wire
Push-ready in afterglow-videos-20261031/: builders, Blender scripts,
layers, frames, GIFs, MP4s (31: punch + 30 shots), keys, contact sheets,
index JSON, this report. NOT yet pushed in this task — landing batch
still has to push + verify on main by size+SHA. Nothing deleted.

## Approval (Mars approves)
- Punch limb afterglow video: 0/1
- Shot afterglow videos: 0/30
- Default Afterglow Preset itself: already APPROVED 1/1 (17:49 CDT)

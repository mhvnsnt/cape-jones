# AFTERGLOW SHOT PRESETS — saved 2026-10-31 ~18:31 CDT (Mars)

All 30 shot afterglows saved as presets, per Mars: "those are all really cool, save all of those as presets, the different colors and things."
Source: afterglow-videos-20261031/ — Blender compositor key frame per shot (30/30, frame 5, Standard view, no Glare) + PIL trail renders using the identical trail/plate layers for the full GIFs/MP4s.
Rule, unchanged: trail in motion only, ZERO at rest. Hold shots generate no trail while still — that is the rule applied, not a missing effect.

## Upgrade axes (for future powers/effects work, defaults = approved Default Afterglow Preset)
- scale_x / scale_y: scale the trail independently per axis.
- expand_horizontal / expand_vertical: expand the trail outward horizontally / vertically (trail width, spread, bloom reach).
- trail_lag_frames / trail_fade: how far behind the limb the trail sits, and how fast it fades.
- power_effects: empty by default — future powers/effects slot (e.g. energy orbs, sparks, colour shifts per power). Pull industry-standard methods for each new effect, do not hand-tool a fake one.
- Colour tracking per preset: input RGB + on-screen sample RGB + mix cause are recorded in the JSON, per the colour-shift rule.

## Presets (30/30)

- AFTERGLOW-CJ-01 (punch-windup): trail input [255, 178, 229], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-02 (punch-extend-snap): trail input [255, 178, 229], on-screen [197, 137, 177], moving, Level 2
- AFTERGLOW-CJ-03 (punch-impact-locked): trail input [255, 120, 115], on-screen [18, 18, 28], hold-still (zero at rest), Level 2 (+ separate FX passes, not god rays)
- AFTERGLOW-CJ-04 (punch-recover): trail input [255, 180, 80], on-screen [197, 139, 63], moving, Level 2
- AFTERGLOW-CJ-05 (punch-across-down-placement): trail input [255, 255, 255], on-screen [197, 197, 197], moving, Level 2
- AFTERGLOW-CJ-06 (walk-street-contact): trail input [255, 255, 255], on-screen [197, 197, 197], moving, Level 2
- AFTERGLOW-CJ-07 (walk-town-passing): trail input [255, 180, 80], on-screen [197, 139, 63], moving, Level 2
- AFTERGLOW-CJ-08 (walk-alley-night): trail input [160, 185, 255], on-screen [123, 142, 197], moving, Level 2
- AFTERGLOW-CJ-09 (dance-a): trail input [255, 178, 229], on-screen [197, 137, 177], moving, Level 2
- AFTERGLOW-CJ-10 (dance-b): trail input [255, 190, 220], on-screen [197, 146, 170], moving, Level 2
- AFTERGLOW-CJ-11 (dance-combined-finale): trail input [220, 150, 255], on-screen [170, 115, 197], moving, Level 3
- AFTERGLOW-CJ-12 (flying-hover): trail input [255, 180, 80], on-screen [197, 139, 63], moving, Level 3
- AFTERGLOW-CJ-13 (flying-soar): trail input [255, 200, 110], on-screen [197, 154, 85], moving, Level 3
- AFTERGLOW-CJ-14 (flying-dive): trail input [255, 155, 75], on-screen [197, 119, 59], moving, Level 3
- AFTERGLOW-CJ-15 (flying-forward-foreshortened): trail input [140, 200, 255], on-screen [108, 154, 197], moving, Level 2
- AFTERGLOW-CJ-16 (flex-anticipation-before-tighten): trail input [255, 180, 90], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-17 (arms-up-reference): trail input [255, 230, 140], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-18 (true-flex-double-bicep): trail input [255, 165, 95], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-19 (fighting-pose-forward-bicep-curl): trail input [255, 180, 80], on-screen [18, 18, 28], hold-still (zero at rest), Level 3 (dual-light)
- AFTERGLOW-CJ-20 (fighting-stance-arms-up-high): trail input [255, 150, 60], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-21 (jump-crouch-takeoff): trail input [140, 220, 210], on-screen [108, 170, 162], moving, Level 2
- AFTERGLOW-CJ-22 (jump-tuck-landing): trail input [255, 180, 80], on-screen [197, 139, 63], moving, Level 3
- AFTERGLOW-CJ-23 (lounge-seated-room): trail input [255, 185, 95], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-24 (desk-seated): trail input [255, 185, 95], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-25 (room-standing-device-gag): trail input [255, 185, 95], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-26 (dialogue-neutral-unsure): trail input [255, 255, 255], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-27 (dialogue-shout-angry): trail input [255, 130, 120], on-screen [18, 18, 28], hold-still (zero at rest), Level 2
- AFTERGLOW-CJ-28 (rooftop-sunset): trail input [255, 155, 75], on-screen [18, 18, 28], hold-still (zero at rest), Level 3
- AFTERGLOW-CJ-29 (rooftop-night-city): trail input [160, 185, 255], on-screen [18, 18, 28], hold-still (zero at rest), Level 3
- AFTERGLOW-CJ-30 (alley-neon-dual-light): trail input [255, 178, 229], on-screen [18, 18, 28], hold-still (zero at rest), Level 3 (dual-light)

Mars approval of the preset system itself: saved per his order, 2026-10-31. Individual shot videos remain approval 0/30 until he approves them. No repo push made by this save alone.

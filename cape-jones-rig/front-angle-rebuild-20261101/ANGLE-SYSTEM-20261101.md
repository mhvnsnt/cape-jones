# 2D ANGLE SYSTEM — wired 2026-11-01

Mars, 2026-11-01 00:58 CDT, replying to Angle 01: "none of these so far are front angle. They're all three quarter angles. all of them every single one of these pictures is a three quarter angle just from a higher or lower perspective"

Mars is right. The 10-angle set in canonical-main-room-10-angles-20261101 is
renamed honestly here: 3/4-ANGLE SET (two-wall corner perspective, higher/lower
framing variants), NOT a front set. Do not claim it as front.

## Industry methods wired 100% (this job)

1. 5-view turnaround (animation model sheet): front 0°, 3/4 front ~45°,
   side/profile 90°, 3/4 back ~135°, back 180°. Same scale, horizontal
   construction lines (head top, eyes, shoulders, waist, feet) across views.
   Sources: standard turnaround — front establishes baseline height/width,
   3/4 front is most-used, side locks posture/depth, back closes the set.
2. Interior elevation (architecture): flat, scaled, orthographic projection,
   viewer line of sight perpendicular to the wall. NO perspective, NO
   foreshortening, NO vanishing point. Vertical lines stay vertical,
   horizontal lines stay horizontal, true scaled height/width on that face.
3. Orthographic vs perspective camera rule: perspective = focal/vanishing
   point, nearer objects larger. Orthographic = no focal point, parallel
   edges stay parallel, size does not shrink with distance. A true front
   room plate uses the orthographic/elevation rule, even when rendered as
   a cartoon plate.
4. Single-wall test (the gate used before delivery): a true front image
   shows ONE flat back wall only. If a second wall / corner seam is visible,
   it is a 3/4 corner view, not front — regardless of how level the camera is.
   Higher/lower camera height alone does NOT make a corner view a front view.
5. Level eye-height + leveled ground: camera height = standing eye height,
   ground line is a single horizontal line, floor is a flat band at the
   bottom, ceiling a flat band at the top. No tilted horizon, no corner seam.

## Angle spec — reusable, per angle

| angle | camera azimuth | camera height | projection | walls visible | perspective |
|---|---|---|---|---|---|
| FRONT-TV | 0°, perpendicular to TV wall | eye level, level | orthographic / elevation | 1 flat wall only | none, no vanishing point |
| FRONT-CHAIR | 0°, perpendicular to chair wall | eye level, level | orthographic / elevation | 1 flat wall only | none, no vanishing point |
| SIDE-PROFILE | 90°, perpendicular to side wall | eye level, level | orthographic / elevation | 1 flat wall only | none, no vanishing point |
| 3/4-FRONT (old set) | ~45° | eye / low / high variants | perspective, two-wall corner | 2 walls + corner seam | 1–2 vanishing points |
| 3/4-BACK | ~135° | eye level | perspective, two-wall corner | 2 walls + corner seam | 1–2 vanishing points |
| BACK | 180° | eye level | orthographic / elevation | 1 flat wall only | none |

How to use it for the next angle: pick a row first, write camera azimuth +
height + walls-visible before generating, then check the result against the
single-wall test. If a corner seam appears, the result fails the front test
even if the prompt said "front".

## Why TV + chair cannot both be flat on their original walls at once

In the approved 2D, the TV is on the left wall and the chair is on the
right wall — perpendicular walls. A single flat front view can show only
ONE of those walls flat. So the true front plates re-stage furniture onto
the one flat wall plane, stage-set style, like a sitcom front elevation:
FRONT-TV puts the chair facing camera in front of the TV wall; FRONT-CHAIR
puts the chair facing camera against its own flat wall with the sunset
window flat beside it. That re-staging is stated, not hidden — it is the
price of a true front, and it is different from the 3/4 corner room where
both walls are visible at once.

## Files in this folder

- angles/front-tv-true-front-20261101.png — 2096×1184
- angles/front-chair-true-front-20261101.png — 2096×1184
- angles/side-chair-profile-true-side-20261101.png — 2096×1184
- contacts/contact-true-front-angles-20261101.png
- ANGLE-SYSTEM-20261101.md (this file), ANGLE-SPECS-20261101.json
- approved-2d-reference-20261101.png — copy of approved 2D, untouched original elsewhere

Approved 2D untouched. Old 10-angle set untouched, renamed in this report
only (not renamed on disk by this job). No repo push by this job.
Approval: true front set 0/1 separately.

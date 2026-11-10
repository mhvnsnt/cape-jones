# Drawing-masters upgrade — G1 — 2026-10-31

Approval: 0/1. No existing file overwritten, no repo push. Base art untouched.
Base: `rig-apose-v7c-clean-transparent.png` (1100x1500, alpha bbox 248,253–876,1295,
373,846 alpha px). Folder: `drawing-masters-upgrade-20261031/`.

## The two effects Mars singled out — now named EFFECTS, not turns

### LINEART-INVISIBLE (old X04 edge lineart, was a faint accident)
Real extraction, actually run: OpenCV 5.0.0 in the rig venv, Canny (50,150) on
greyscale + Canny on the alpha mask, combined. Colour (60,60,60) throughout.
- L1 faint, 1px, alpha 70: 47,514 line px, 12.71% of silhouette
- L2 medium, 2px, alpha 120: 125,004 line px, 33.44%
- L3 visible, 3px, alpha 180: 167,388 line px, 44.77%
- L-depth, line-weight-by-depth (near/left 3px, mid 2px, far/right 1px), alpha 140:
  118,906 line px, 31.81%
- Sobel cross-check, alpha 120: 32,952 line px, 8.81% (thinner, sparser — Canny is
  the keeper, Sobel is the check)
Body fill is zero in all of them: outline only, so the figure reads as going
invisible, with the outline still there. That is the effect, controllable by
weight and opacity, not the old FIND_EDGES accident.

### BLACK-SILHOUETTE (old X08 solarize, was a colour-inversion accident)
Clean alpha-to-black fill, no solarize, no random inversion:
- S1 pure black: 373,846 black px = the full silhouette, alpha preserved
- S2 black + cyan rim (180,245,255), 3px dilate-minus-alpha: 23,907 rim px
- S3 black + light-grey (200,200,200) interior lineart: 47,514 line px over black
Solarize is NOT used anywhere in this set. The old X08 is superseded as an
effect by S1–S3, and is still NOT a turn.

## Whole G1 set, rebuilt, correctly labelled (contact: drawing-masters-upgrade-contact)
APPROXIMATION (usable as an approximation, never as a true view):
I01 foreshorten 0.72 (792 wide); I02 foreshorten 0.45 (495 wide, face STILL
front-facing — stated plainly, it is a width squeeze, not a side view);
I03 mirror flip (a flipped front, NOT a true back); I04 far-side dark, now a
smooth gradient 0.95 left to 0.62 right (old hard half-cut replaced);
I06 skew; I08 segment twist; I09 counter-rot; X01 depth-by-scale 0.85;
X02 scale+dark; X03 shear; X09 flip+dark.
REFERENCE only: I10 grey silhouette reference.
NOT A TURN, kept in the set and labelled as such, never presented as a turn:
I05 vertical flip (figure upside down — useful only as a fall/upside-down pose
study); I07 perspective quad (sideways-distorted — perspective-distortion test
only); X10 quad back (sideways-distorted — same, test only).
NOT A TURN, effect/processing only: X05 blur+sharpen, X06 posterize, X07 contrast.
All 18 individual files are in `individual/`, transparent, auto-fit.

## Industry-standard methods wired (9 run / wired, 4 reference-only)
RUN / WIRED in the builder: (1) OpenCV Canny edge detection, (2) OpenCV Sobel
edge detection, (3) alpha-to-black silhouette fill, (4) dilate-minus-alpha rim,
(5) Loomis foreshortening by measured width factors (0.72 / 0.45) with head-height
kept at full 1500px height, (6) perspective grid construction (separate diagram,
vanishing point at 550,120, figure placed on the grid — a construction aid, NOT
a turn), (7) depth-by-scale (0.85, plus the 2.5D rule scale = 1.0 + 0.25×Z),
(8) atmospheric far-side darkening (smooth gradient, not a hard cut),
(9) line-weight-by-depth (3/2/1px bands), (10) silhouette readability test
(S1 pure black reads as a caped figure at full size; small-size readability
was not formally scored and is not claimed).
REFERENCE ONLY, honestly labelled, NOT run: Blender Freestyle line rendering
(needs a 3D scene, not a flat plate), Toon Boom Harmony lineart extraction,
OpenToonz/Tahoma2D lineart, Anime2Sketch-style learned line extraction
(no model downloaded, no vendor run claimed).
Mirror/back construction: I03 is a flip, not a back. A true back needs a
redrawn back master, same as a true side.

## I02 profile-head study — honest limit
`I02-profile-head-study-20261031.png` shows the I02 narrow figure beside
`sliced/Head_Profile.png` at 2x, in a red placement box. It is a STUDY ONLY,
not a composited side master, for two plain reasons: (1) the apose plate is
baked flat, so the front head cannot be removed without cutting the collar
behind it; (2) the sliced profile head does not match the apose head in
scale or style cleanly. A clean side master needs a layered rebuild or a
redraw, not a paste-over.

## No-crop-window rule — gate PASS
Every individual and effect file is auto-fit: canvas = alpha bbox + 40px pad.
Gate in `measurements-20261031.json`: 26/26 checked, 0 edge-touch failures.
One real bug was caught and fixed in this task: grayscale and posterize in
PIL drop alpha to 255 everywhere (full-canvas alpha), which tripped the gate;
both now restore the base alpha channel before saving. Contacts fit tiles by
containment (no distortion, no crop); contacts are viewing sheets on grey,
individual files stay transparent.

## Still owed (not claimed here)
True hand-drawn 3/4, side, back, and torso-twist masters: 0/4. Unblocker is a
redrawn master (artist pass, or Mars's call to commission one). Derived views
in this set are approximations only, and the report does not upgrade them
into masters.

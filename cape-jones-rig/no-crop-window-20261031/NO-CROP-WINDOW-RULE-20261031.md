# NO-CROP-WINDOW RULE (Mars, 2026-10-31 19:22 CDT, standing)

Mars's words, plainly: he has a transparent background, so he does
NOT need a crop window around him or around any of his pieces. When
he leans over a certain amount, a fixed window crops his foot off
or crops pieces of him off. That window is unnecessary.

## The rule, in one line
**The canvas fits the figure. Never the figure fits the window.**

## What that means, concretely
1. No fixed canvas is ever a window. If a rotation, shear, lean, or
   paste can move any alpha pixel outside the canvas, the canvas
   must grow first (transparent padding), and the result must be
   trimmed only to the figure's own alpha bbox plus padding.
2. Transparent background throughout. Figure files are RGBA with
   alpha 0 outside the figure. No grey, no white, no background
   baked into a figure file. A checker or grey background in a
   contact sheet is DISPLAY ONLY, for viewing, and is labelled as
   such — it is never part of the figure.
3. No piece is ever clipped to its original box. A piece pasted
   partly off-canvas must expand the canvas, not lose the part
   that sticks out. A piece rotated must be rotated on a padded
   layer, not in place on a fixed layer.
4. The gate is mandatory before delivery: `check_no_clip.py` must
   PASS — alpha touches NO canvas edge (top/bottom/left/right all
   0), alpha bbox margin > 0 on every side. A frame that touches
   the edge is treated as clipped until proven otherwise.
5. A delivery crop (for YouTube 16:9, TikTok 9:16, etc.) happens
   ONLY at export, only after the no-clip gate passes on the full
   figure, and only inside the protected-square spec. It is never
   part of building, posing, or inbetweening.
6. If a count changes, say why. Resize changes alpha count by
   scaling. Blur spreads alpha. Rotation/shear resample by <0.02%.
   None of those are clipping. Clipping is: alpha pixels present
   in the padded-truth transform but missing from the fixed-window
   transform, AND/OR alpha touching the canvas edge. Quote both
   numbers, not just one.

## How to build under this rule (the wired path)
- Whole figure: `no_crop.rotate_nocrop()`, `no_crop.shear_nocrop()`,
  `no_crop.transform_nocrop()` — pad, transform, trim to bbox + 40px.
- Pieces / limbs: `no_crop.limb_layer_nocrop()` +
  `no_crop.paste_nocrop()` — padded layer, expanded canvas, shift
  returned so coordinates stay trackable.
- Check: `python3 check_no_clip.py <file-or-dir>` — exit 0 PASS,
  exit 1 FAIL, JSON per file with size, alpha, bbox, edge touch,
  margins, and an OpenCV boundingRect cross-check when cv2 is
  installed (cv2 5.0.0 in the rig venv, actually run here).
- Blender side: render border OFF (`use_border = False`,
  `use_crop_to_border = False`), film transparent, camera fit to
  the subject — see `blender_nocrop_setup.py`, actually executed
  headless against Blender 5.2.3 in this folder (settings only,
  no render claimed).

## What this rule does NOT say
- It does not say "never crop anything ever." Trimming transparent
  pixels outside the alpha bbox + padding is not cropping the
  figure, because there is no figure there. Delivery export crops
  are a separate, spec'd step (see rule 5).
- It does not say the old builders are fixed. They are audited in
  `CROP-WINDOW-AUDIT-20261031.md` and listed as still needing
  migration, file by file. This folder proves the path and re-renders
  G5 + lean tests; claiming the whole rig is fixed would be a lie
  until each builder's output passes the gate.

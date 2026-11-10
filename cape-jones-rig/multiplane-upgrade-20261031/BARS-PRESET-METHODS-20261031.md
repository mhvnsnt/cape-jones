# BARS PRESET — methods wired (multiplane upgrade, 20261031)

Status: EXPERIMENTAL preset, approval 0/1. Original multiplane test = WORKS,
real 2.5D depth, APPROVED as a depth test, NOT approved as a final shot.
Test bars (55px, alpha 210, every 180px) were test only, not final.

## The one feet rule (used everywhere, do not invent a second one)
Feet anchor = alpha-bbox bottom of the figure, placed on a world ground
line, and scaling / camera moves grow or move ABOVE that anchor, never
from the centre. In this preset: world ground Gy=700, figure paste y=47,
resized-figure bbox bottom 653, so 47+653=700 every frame, world and
screen (vertical camera = 0). The SAME rule applies to:
- size-transformation power: scale grows upward from the feet anchor,
  feet y constant while scale changes;
- coming-forward walking: feet contact the world ground line at each
  step, scale grows as the figure comes forward, feet stay on the line.
If a template's feet y moves, it is not planted, whatever its label says.

## Methods wired
1. Disney multiplane camera (1937) — REAL RUN in PIL. Layers at different
   distances move at different rates: far 0.3, Cape/ground 1.0, foreground
   1.8. Camera pan 0..120 px. This is the depth read Mars approved.
2. Parallax rate by depth — REAL RUN. screen_x = world_x - camera_x *
   parallax; world_x recovered as screen_x + camera_x * parallax, and
   feet_centre_x_world is constant to ±1 px (rounding) across all 24
   frames. Relative distance = 1/parallax: far 3.33x hero distance,
   foreground 0.56x hero distance.
3. Foreground occlusion / layer order — REAL RUN. Order back-to-front:
   far bg, ground, Cape, foreground bars. Bars are IN FRONT of Cape, so
   Cape reads as behind the bars. Occlusion is measured over Cape figure
   pixels only (foreground alpha AND Cape alpha), not over the bbox.
4. Atmospheric perspective / blur by depth — REAL RUN. Far bg blurred
   1.2 and darkened x0.85; Cape sharp (blur 0); foreground blur 2.0 test /
   1.0 final. Far = hazier/darker, near = sharper, same as the original.
5. Blender real-camera multiplane — SCENE CONSTRUCTION REAL RUN in
   Blender 5.2.3, NO RENDER CLAIMED. Script `build_multiplane_blender.py`
   ran and saved `bars-preset-blender-20261031.blend` with a camera and
   three planes at distances matching the parallax table (far 3.33, hero
   1.0, foreground 0.56), camera lateral keyframes frames 1-24. No Blender
   frame is claimed as rendered here; the PIL renders are the proof.
   If a Blender render is wanted, render that .blend and report its own
   output.
6. Depth of field by Z — METHOD MAPPING. Blur increases with distance
   from the hero plane (far 1.2, hero 0); foreground blur is a stylistic
   close-focus choice, stated as such, not a physical DOF calculation.
7. OpenToonz / Tahoma2D camera / stage — METHOD MAPPING. Same layer +
   camera-move model as (1): stage layers move at different rates under
   one camera. No OpenToonz GUI run is claimed.
8. After Effects 3D camera on 2D layers — METHOD MAPPING. Same model:
   2D layers at different Z under a 3D camera produce the same parallax
   table. No After Effects run is claimed.

Count: 8 methods total, 5 real runs (1-4 PIL, 5 Blender scene
construction), 3 method mappings (6-8), labelled as such. No vendor
tool run is claimed where it did not run, and no Blender render is
claimed.

## Foreground: test vs final
- TEST: 55px wide, alpha 210, every 180px, blur 2.0 — original, heavy,
  occludes Cape for stretches. Kept in the preset for comparison only.
- FINAL: 28px wide, alpha 140, every 260px, blur 1.0 — thinner, sparser,
  still reads as bars in front, occludes far less figure area (see
  feet-measurements JSON, occlusion per frame). Final pick is Mars's;
  both are runnable from the same builder with one flag.

## No-crop gate
Gate checks CAPE ALPHA pixels, not the transparent image canvas:
paste_x + bbox_left >= 0, paste_x + bbox_right < 1100,
paste_y + bbox_top >= 0, paste_y + bbox_bottom < 750.
All 24 frames pass for both variants (see feet-measurements JSON).
An earlier gate version checked the image canvas and falsely failed;
it was fixed to alpha pixels, and the fix is recorded here, not hidden.

## Still owed
- Mars approval 0/1 (upgraded preset, feet fix, final bars pick).
- Final foreground pick: test vs final bars (both shown).
- Per-shot multiplane 0/30; this preset is one camera move, not 30 shots.
- Blender multiplane render (script provided, render not claimed).
- No repo push in this task.

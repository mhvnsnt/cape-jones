# Shafts Volumetric Upgrade — what this is, in plain words

## What the old test was (G3, and why Mars could not tell what it was)
G3 was a SHAFT-METHOD TEST ONLY. It was flat PIL rectangles with blur 0/1/3/6/8,
drawn OVER the figure. It was NOT real volumetric light, NOT lights shining down
on him, and NOT shafts behind him. That is why it did not read as lights: the
rectangles covered his body instead of falling behind him, and there was no light
source, no ceiling, no direction, and no separation between shafts.
Do NOT present the G3 sheet again as a volumetric result.

## What the new proof is (this folder)
REAL volumetric light, made in Blender 5.2.3 Cycles on CPU:
lights sit ABOVE Cape, shine straight DOWN, pass through gaps between ceiling
slats, and fall as separate warm columns behind him. Cape stands IN FRONT of the
shafts. The shafts never cover him. A labelled diagram names the light source,
its direction (DOWN), the ceiling slats, and Cape in front.

## Files (all 1100x1500 unless noted, approval 0/1, no repo push, no overwrites)
- shafts-only-cycles-v2-20261031.png — MAIN shaft layer, Blender Cycles, v2 (corrected)
- shafts-only-cycles-20261031.png — v1 first attempt, kept for comparison, defects listed below
- figure-only-plate-20261031.png — Cape arms-up plate, transparent, untouched source copy
- composite-shafts-behind-v2-20261031.png — MAIN composite: shafts BEHIND Cape
- composite-shafts-behind-20261031.png — v1 composite
- shafts-masked-behind-figure-v2-20261031.png — shaft layer with figure silhouette masked out
- diagram-labelled-20261031.png — composite with arrows + plain-word labels
- contact-labelled-20261031.png — shafts-only / figure-only / composite / diagram, side by side
- ae-light-rays-PROXY-20261031.png — PROXY only, NOT Adobe After Effects (see Methods)
- build_cycles_down_shafts.py / build_cycles_down_shafts_v2.py — Blender scene scripts
- build_composite_v2.py, measure_v2.py, check_no_clip.py, build_glare.py (attempted, see Methods)
- measurements-v2-20261031.json — measured numbers

## Measurements (v2, measured, not guessed)
- Canvas 1100x1500. Figure alpha bbox x 222-879, y 240-1282. No-crop gate PASS:
  edge alpha max 0, so no foot or piece is clipped by a window. Canvas fits the figure.
- Shaft separation, mid-height (rows 500-700, column profile, midpoint threshold):
  3 clear columns, x 282-379, 494-604, 721-816. Peak mean 54.8, valley mean 22.9,
  so columns ARE distinct from the dark gaps between them. Lower height: same 3 columns,
  x 263-400, 466-633, 698-833, peak 29.3 vs valley 18.5.
  Top height: only 1 column passes threshold (517-582, peak 115.0 vs valley 19.0)
  because the ceiling slats block the top row — that is a framing defect, listed below.
  The scene was built for 5 gaps (-3.0, -1.5, 0, 1.5, 3.0); only 3 read clearly.
  The outer 2 are too dim to pass threshold. DO NOT claim 5 distinct shafts.
- Shaft brightness: shaft centre mean RGB (72.4, 62.8, 47.1) vs dark corner
  mean (22.9, 20.4, 18.8). Shafts are brighter than background, but they fade with
  height — they are not as bright at the bottom as at the top.
- Figure occlusion: shaft-over-opaque-figure max difference 0.0. PASS by construction:
  shafts are multiplied by (1 - figure_alpha) before pasting, and the figure is pasted
  on top at full opacity where alpha is 255. No shaft pixel washes over his body.
- v1 composite gate was also PASS on no-crop and shaft-over-figure, but v1's
  shaft-count measurement at a single row returned 0 and is NOT quoted — that was a
  measurement bug (threshold too high for mid-height shafts), not a real count.

## Defects, plainly (v2 is the main proof, not production-ready)
- v1 defects: only 3 bright columns, dust dots too big (looked like glowing balls),
  floor plane read as a grey wall band instead of light pools on the ground.
- v2 fixes: dust shrunk to radius 0.015 and 50 motes (now small specks), floor removed
  (shafts fade into dark instead of hitting a fake wall).
- v2 defects remaining: ceiling slats dominate the top of the frame (large black blocks);
  only 3 of 5 shaft columns read clearly; shafts fade and get dim toward the bottom;
  no ground light pools (floor was removed rather than fixed — pools are a separate
  per-shot pass, not faked here); no GPU sequence (CPU Cycles only, 32 samples,
  volume step 1.0, ~11 minutes for the 1100x1500 v2 render).
- Therefore: NOT claimed production-ready. It passes behind-figure + no-crop, but
  fails the full 5-column separation test.

## Methods wired (8 total)
1. Blender Cycles Principled Volume — REAL RUN. Density 0.28, anisotropy 0.7,
   warm colour (1.0, 0.85, 0.55), CPU, 32 samples, 1100x1500. This is the tool used.
2. Crepuscular separation by occluders — REAL RUN. 6 ceiling slats at z 6.8, gaps
   at -3.0/-1.5/0/1.5/3.0, plus a Sun straight down and 5 spot lights above the gaps
   pointing straight down. Gaps are what make separate shafts, not drawn rectangles.
3. Dust motes in the shafts — REAL RUN, corrected in v2. 50 tiny emission spheres
   inside gap columns only, radius 0.015. v1 used radius 0.035 and read as balls.
4. Shaft masking — REAL RUN. Shaft layer multiplied by (1 - figure_alpha) before
   compositing, so shafts literally do not exist under the figure silhouette.
5. Blender Eevee volumetric — METHOD ONLY, NOT RUN here. xvfb-run exists on this VM,
   but no Eevee render was completed in this task; Eevee needs a GPU/display path
   and headless runs abort on missing libEGL in earlier work. Do NOT claim an Eevee
   render. Eevee volume settings are documented in the prior godray v2 script for a
   future GPU/display run.
6. Blender / Natron Glare (Fog Glow) — ATTEMPTED, NOT COMPLETED as a file.
   Blender 5.2 changed the compositor API: no Composite node type (File Output is
   the output node), Glare is socket-driven with enum strings 'Fog Glow'/'High',
   and File Output base_path is not an attribute in 5.2. Three script attempts failed
   on those API changes. The Glare file is NOT in this folder and must not be claimed.
   A soft-glow variant was NOT substituted silently; the Cycles shafts stand alone.
7. After Effects CC Light Rays — PROXY ONLY, labelled PROXY.
   ae-light-rays-PROXY-20261031.png is a PIL Gaussian-blur blend of the shaft layer,
   showing what a radial ray fan would do. Adobe After Effects did NOT run here.
8. Sun Beams / compositor rays (Natron-style) — METHOD MAPPING ONLY.
   The same fan/blur logic as (7), plus the Blender Glare intent in (6). No Natron run.
Counts: real runs 4/8 (Cycles volume, occluder separation, dust, shaft masking),
method/proxy/attempted 4/8 (Eevee, Glare attempted, AE proxy, Natron mapping).
Full GPU volumetric sequence: NOT run, still owed. Per-shot shafts: 0/30, still owed.

## Still owed
- Approval 0/1 for this proof. - 5-column separation fix (slats smaller / camera wider /
  outer spots brighter, re-render, re-measure). - Ground light pools as a real pass,
  aligned to the figure's feet. - Blender 5.2 Glare file output (File Output node API
  in 5.2, not the old Composite node). - Eevee volumetric run on a display/GPU route.
- Full GPU volumetric sequence (Kaggle/Colab free tier, specific run approval).
- Per-shot shafts 0/30, with real shot plates and backgrounds, not the arms-up stand-in.

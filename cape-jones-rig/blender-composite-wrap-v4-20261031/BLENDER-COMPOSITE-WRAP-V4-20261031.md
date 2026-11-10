# Blender composite wrap v4 — every v3 honest limit addressed

Mars 2026-10-31 17:37–17:38 CDT: pull industry-standard stuff that CAN do the
linework/gradients v3 could only approximate, wire it 100%, so the honest
limits are no longer limits. Rim rule unchanged: HARD rim + ONE soft layer
(soft rim = soft halo).

## What v4 actually runs (methods, all in this folder)
1. **Normal-from-depth relight** (`relight_normal_v4.py`, scipy + numpy):
   depth = distance-to-silhouette-edge (EDT, rounded volume profile) minus
   valleys at the art's own THIN dark interior lines (thin-stroke test: dark
   AND locally darker than neighbourhood — solid dark cape is NOT a line),
   smoothed. Normals = (-dz/dx, -dz/dy, 1) normalised (Sobel). Shading =
   N.L per pixel for cyan backlight (upper-left) + gold front key (right).
   Albedo is kept; shading/tint are recomputed. This is the implementable
   core of intrinsic-image / 2D relighting research (Neural LightRig,
   GeoRelight, PIXLRelight) and the same normal math Blender uses on a mesh.
2. **Cycles volumetric shafts + true dust** (`blender_godray_v4_cycles.py`,
   Blender 5.2.3 LTS, CPU Cycles): Principled Volume density 0.45,
   anisotropy 0.6, 3 Track-To cyan spots (12000/6000/6000), 5 occluder bars,
   120 emission icosphere dust motes INSIDE the volume.
3. **Blender 5.2.3 compositor final** (`blender_composite_wrap_v4.py`, run
   under xvfb-run — bare headless aborts on missing libEGL): 1100x1500,
   scene.compositing_node_group, SetAlpha + AlphaOver, shafts screen-blended,
   soft rim + inner wrap multiplied by the sideweight map.
   Solid cyan/bright-cyan images are 1100x1500 (v3's 640x360 solids would
   not cover a full-height frame).

## Limit-by-limit verdict (plain, no limit claimed gone if it is not)
1. Interior = 2D approximation → **REPLACED by per-pixel normal relight.**
   Shading now comes from measured normals, fold lines are normal valleys.
   STILL ESTIMATED: normals come from silhouette+linework depth, NOT a true
   3D character model. A mesh normal pass remains the only way to get true
   side-facing normals (see 4).
2. Fold relief 1–2px at 640x360 → **FULL-HEIGHT 1100x1500 frames.** Pec/abs/
   fold relief reads clearly at full height. Interior change measured:
   85,734 px differ >20 inside the apose alpha (of 373,846), mean diff 18.24.
   The relight itself is deliberately not over-strong — it is visible, not
   a repaint.
3. Painted shafts → **CYCLES shafts, no longer painted.** Shaft layer mean
   RGB (10.5, 55.6, 62.6), 4,256 px >200. RESOLUTION HONESTY: a full
   1100x1500 Cycles volume render did NOT finish in 25 min on this VM CPU
   (timeout, no output). The shaft layer actually used is a 550x750 Cycles
   render (same scene, 32 samples), upscaled 2x with 0.8 blur for the comp.
   The CHARACTER is full-height; the shaft layer is upscaled Cycles, not
   full-res Cycles. Shaft separation is still SOFT (glow bands, not crisp
   crepuscular beams) — crisp-shaft pass still owed.
4. Side-weighted wrap → **WIRED, but visibly WEAK — not claimed as done.**
   Soft rim + inner wrap alphas ARE multiplied by (0.30 + 0.70*sideweight)
   in the compositor. Measured rim-only diff: backlit (left) mean 77.9 vs
   right mean 77.4 — essentially no visible difference, because estimated
   normals are mostly front-facing (diff_back mean 0.702, low variance).
   Strong side-weighting still needs a true 3D side-normal pass.
5. Painted dust specks → **TRUE in-volume dust motes.** 120 emission
   spheres inside the volume render as bright dots in the shaft layer and
   in the final frames. (Upscaled with the shaft layer — see 3.)
6. Background-dominated pixel proof → **ISOLATED proofs.** Rim+wrap-only:
   v4 full apose vs v4 apose-norim (identical bg, shafts, relit plate) =
   127,646 px differ >20, bbox x242–882 y251–1309 — rim/wrap only, zero
   background change. Interior-only: relit vs original plate inside alpha
   (see 2). The old 202,808 px v3 number is NOT reused.

## Files
- wrap-v4-apose-20261031.png, wrap-v4-armsup-20261031.png,
  wrap-v4-fighting-20261031.png (all 1100x1500, Blender compositor)
- wrap-v4-apose-norim-20261031.png (proof control, no rim/wrap)
- proof-v3-vs-v4-wrap-20261031.png, proof-interior-detail-v4-20261031.png
- scratch/: relit plates, depth maps, normal maps, sideweight maps,
  shafts-cycles-v4.png (550x750 native), shafts upscaled, bg 1100x1500
- Scripts + .blend files in this folder. No repo push made.
- Approval: 0/1 (Mars approves).

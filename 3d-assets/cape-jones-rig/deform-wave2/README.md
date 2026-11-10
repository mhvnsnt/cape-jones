# Wave-2 Deform Audit — Procedural Corrective Pipeline

Automated numeric deform scanner + procedural fix pipeline for the Cape Jones rig.
No hand-edited weights anywhere — every fix is a re-runnable script.

## Pipeline

1. **dump_wave2.py** — Headless Blender sweep of 15 joint poses (shoulders fwd/side,
   hips, knees, wrists, ankles, spine bend/twist). Dumps rest/posed positions,
   normals, group weights, bone delta quats to `scratch/*.npz`.
2. **analyze_wave2.py** — Laplacian-motion residual audit + weight-bleed audit.
   Flags zones, builds corrective shape-key deltas (rest-space, inverse-blended-
   rotation mapped) + hinge weight smoothing. Emits `wave2_correctives.npz`.
   - Spine uses per-vert dominant bone-pair mapping (a single-pair mapping
     created surface cracks — fixed via adaptive mapping).
3. **apply_wave2.py** — Applies `wave2_correctives.npz` + `wave2_keys.json`
   (rotation-diff and transform-channel drivers), rewrites smoothed hinge
   weights, saves the fixed blend.
   Usage: `blender -b <in.blend> --python apply_wave2.py -- <out.blend>`
4. **verify_keys.py** — Poses each joint 0/50/100%, reads evaluated shape-key
   values via depsgraph. Expects ~0 at rest, monotonic rise, ~1 at full.
5. **render_wave2.py** — Before/after proof renders per zone (same camera/pose).
   Usage: `blender -b <blend> --python render_wave2.py -- <outdir> <TAG> <POSE>`
   Light/tiny variants exist for memory-constrained renders.

## Flagged zones (all fixed)

| Zone | Max residual | Fix |
|------|--------------|-----|
| shoulderL/R | 38.6/43.5mm | corrective + clavicle/upperarm smoothing |
| hipL/R | 55.0/59.1mm | corrective + pelvis/thigh smoothing |
| kneeL/R | 21.8/21.7mm | corrective + thigh/shin smoothing (driver ranges empirically recalibrated) |
| ankleL/R | p99 12.4/12.3mm | corrective + shin/foot smoothing |
| spine_fwd/twist | 47.8/75.6mm | corrective with per-vert adaptive bone-pair mapping |

## Driver verification (all OK)

All 10 corrective drivers verify 0.000 at rest → 1.000 at full bend, monotonic,
with spine cross-axis fire at 0.000.

## Proofs

`proofs/` contains before/after stills for all 10 zones, viewed with own eyes.
The spine_fwd corrective initially introduced surface cracks (wrong rotation
mapping for spine_2-dominated verts); fixed via per-vert adaptive mapping —
cracks gone, verified visually.

# 3D-side-ready tools (NOT the current Cape work) — EXPERIMENTAL, documented only

Scope rule from Mars, 2026-10-31 ~18:44 CDT: this is the 2D side of Cape
Jones, focused on 2D until Mars says otherwise. 2.5D/3D effects are pulled
in ONLY where they make the 2D feel perspective-bending. The tools below
are pulled + documented so the 3D side of the show (which is struggling)
has a ready stack later. They are NOT used to turn current Cape work into
a 3D project, and no 3D Cape model was built in this pass.

## Ready stack for the 3D side (free/open first, industry-standard methods)
1. Blender 5.2.3 LTS (already installed, `~/workspace/tools-industry/blender-5.2.3-linux-x64/blender`)
   — the 3D host: modelling, rigging, Cycles/Eevee, Grease Pencil in 3D
   space, camera + depth. Proven in this pass for GP + compositor work.
2. Grease Pencil in 3D space — 2D drawings on 3D planes, camera moves
   around them, multiplane as a 3D camera move. The GP layer tree in this
   folder ports directly: layers become GP layers on a 3D-facing object.
3. Multiplane / parallax as a real camera — the 2.5D test in this folder
   (parallax 0.3 / 1.0 / 1.8) becomes a Blender camera dolly with layers
   at different Z distances, no fake scaling needed.
4. Depth-by-scale + depth-of-field — the Z table in this folder
   (scale = 1.0 + 0.25*Z) becomes real Z distance + camera DOF blur in 3D;
   the 2D blur values (far 2.0, mid-far 1.0) are the 2D stand-ins.
5. Spine / Moho-style mesh warping for pseudo-3D turn — the pseudo-turn
   test (width squash + layer-order flip at midpoint) is the 2D version;
   in 3D it becomes a real mesh/bone turn, with the same layer-flip rule
   (forward limb above torso after the midpoint).
6. Alembic / .abc caches (already proven on the Nick archive: Blender
   imports .abc natively) — the 3D side's animation interchange format.
7. Cycles volumetric (god-ray v2: density 0.35-0.45, anisotropy 0.6) — the
   3D side's atmosphere, already proven for 2D backgrounds in this project.

## What is NOT claimed here
- No 3D Cape model, no 3D rig, no 3D render of Cape was built in this pass.
- These tools are documented as ready, not wired into a 3D pipeline —
  wiring a 3D pipeline is a separate Mars-approved job, not smuggled in
  under a 2D task.

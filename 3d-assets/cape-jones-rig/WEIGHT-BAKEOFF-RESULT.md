# Weight Bake-Off — result handoff for the rig lane

**From:** weight bake-off lane (`rig/weight-bakeoff-20261017`, merged to main)
**Date:** 2026-10-17 · **Full report:** `docs/research/WEIGHT-BAKEOFF-2026.md`
**Driver:** `tools/weights/cj_bakeoff/bakeoff.py` · **Proofs:** `docs/research/bakeoff-proofs/`

## Winner: W5r — Surface Heat Diffuse weights + Preserve Volume + Corrective Smooth

The only pipeline that produces **usable full-mesh weights** on this model
(991,082/991,082 verts weighted, 0.00% unweighted). Blender's own Bone Heat fails
completely on the Tripo mesh (`failed to find solution`, 100% empty groups —
even on a 105k decimated proxy).

**Scores (W5r):** P1 rest ✅ · P2 arms_raised ⚠️ · P3 elbow_90 ✅ · P4 knee_deep ❌ ·
P5 shoulder_raise ❌ · P6 head_turn ✅ · P7 crouch ❌

**Honest headline:** no entry passes all 7 poses. W5r is the clear winner but needs
**manual cleanup in 2 zones** before it's production-ready (see below).

## How to reproduce the winning weights (exact recipe)

```bash
# 1. Generate weights (headless, ~15 min: import 69s + shd ~13min + parse)
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
  -b --python tools/weights/cj_bakeoff/bakeoff.py -- --entry W3 --poses P1
# blend lands at ~/workspace/weight-bakeoff-scratch/blends/W3.blend

# 2. Add the W5r modifier stack (or do it in the GUI):
#    - Armature modifier: enable "Preserve Volume" (dual-quaternion skinning)
#    - Add Corrective Smooth modifier AFTER the Armature modifier: Factor 0.5, Iterations 3
```

The solver binary must be built once: `tools/weights/surface-heat-diffuse/build_linux.sh`
(g++ — source is MIT, in-repo). Headless flow documented in
`tools/weights/surface-heat-diffuse/HEADLESS.md`.

## These weights pair with the CJ-TEST skeleton (weights are skeleton-bound)

20 bones, defined in `bakeoff.py::BONES` — character faces +X, native 0.925 m,
**do not rescale**. Bone layout: root→Hips→Spine→Chest→Neck→Head;
Shoulder.L/R→UpperArm→ForeArm→Hand; Thigh.L/R→Shin→Foot (L = +Y).

## Applying the winning TECHNIQUE to the BlenRig 6 rig

Do NOT transfer the vertex groups directly (different bone names/counts). Instead:

1. Take the posed/rest BlenRig 6 DEF-bone armature + the Cape Jones mesh.
2. Run the same headless flow (`weights_surface_heat()` in `bakeoff.py` takes any
   `(mesh, rig)` pair): write mesh/bone txt → run `shd` → read weights →
   plain `ARMATURE` modifier.
3. Enable Preserve Volume on the Armature modifier; add Corrective Smooth (0.5, 3).
4. Add twist-bone chains on upper arms/forearms per `add_twist_bones()` in
   `bakeoff.py` (Copy Rotation, twist axis only, influence 0.5, weights split
   50/50 on the distal half). The bake-off measured no gain on hinge poses, but
   twist bones address *axial* twist collapse (not in the 7-pose suite) — still
   recommended as standard practice per `bannon-video-pipe/docs/AI_RIGGING_RESEARCH.md`.
5. Then do the manual cleanup below — the auto weights get you 90% there.

## Known defect zones (manual cleanup targets — all visible in bakeoff-proofs/)

1. **Right shoulder (character's R):** pinches/collapses on forward raise (P5) and
   kinks on overhead raise (P2). The solver is asymmetric here (Shoulder.R claims
   ~688k verts vs Shoulder.L ~300k). Repaint the deltoid falloff by hand.
2. **Feet/ankles:** crumple into a blob on deep knee bend (P4) and crouch (P7).
   Check the ankle blend region (Shin↔Foot transition too wide/misplaced).
3. **Slab artifact under the thigh (P4/P7):** a flat sheet of verts gets left behind
   when thighs swing forward — likely cape/inner-thigh verts with wrong bone
   assignment. Find and reassign.
4. **Cape:** becomes a rigid board on crouch (P7, W2 especially). The cape needs its
   own bones or the cloth sim from the cape lane — rigid body-follow will never drape.

## Losers (don't use)

- **Blender Bone Heat** (incl. 105k proxy + Data Transfer): total failure on this mesh.
- **Blender Envelope:** candy-wrapper shoulders, elbow pinch, cape smeared into a sheet.
- **BrutalFist `auto_rig_humanoid.py`:** builds its skeleton sideways on Z-up imports
  (`hi.y - lo.y` Y-up assumption — Hips→Head chain runs along +Y through the arm
  axis) AND its Bone Heat fails. Flagged for the brutalfist lane to fix the axis.
- **Mesh-deform auto-cage (BlenRig technique):** binds fine, but a naive convex-hull
  cage (11 verts) turns limbs into paddles. Needs the rig lane's fitted cage.

## Pose suite (for re-testing after cleanup)

`bakeoff.py --entry W5 --poses all --from-blend <your.blend>` re-renders all 7 poses
(P1 rest, P2 arms_raised, P3 elbow_90, P4 knee_deep, P5 shoulder_raise, P6 head_turn,
P7 crouch). Pose eulers in the shared `POSES` dict are measurement-verified
(mirrored bones take the SAME z-euler sign).

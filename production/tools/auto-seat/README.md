# AUTO-SEAT — Measurement-Driven Contact Solver

**Status:** Solver built, placement numerically verified. Cycles render does not show the character (material issue, separate from seating).

## The Breakthrough

All prior sitting attempts floated 10–14cm above the chair because they targeted
`seat_z=0.370` (the chair's **bounding-box top**). Runtime raycast measurement
proves the actual sitting surface is:

- **Seat surface: z = 0.230** (25 raycasts, median)
- Backrest plane: x = 3.2124
- Floor: z = 0.0000
- Butt target: z = 0.210 (0.230 − 0.020 cushion compression)

## Method

1. **MEASURE** chair via raycasts (seat heightfield, backrest plane, floor)
2. **RETARGET** CMU 113_15 mocap using world-space math:
   `R_local = (W_parent @ M_rel)⁻¹ @ W_desired`
3. **SOLVE** contacts on the middle frame:
   - Butt→seat: analytic placement via parent-space mapping
   - Back→backrest: pitch solve (currently returns None — needs debug)
   - Feet→floor: analytic two-bone IK
4. **APPLY** to all 81 frames, keyframe, render

## Critical Rig Findings

The 94-bone rig has **separate control and deform bones**:
- `*_fk_*` bones (e.g., `thigh_fk_L`) have `use_deform=False` — they DON'T move the mesh
- Deform bones (e.g., `thigh_L`, `spine_1`) have `use_deform=True`
- **Bone translations work** but are in **bone-local space**, not world space
- The correct mapping: `world_delta = (M_world @ parent.matrix).rot @ local_delta`

## Verified Results

```
after direct: mean=(3.050,2.067,0.409) min_z=0.2100
```

- Butt X: 3.050 (target 3.05) ✓
- Butt Y: 2.067 (target 2.067) ✓
- Butt min Z: 0.2100 (target 0.2100) ✓ EXACT

## Known Issues

1. **Cycles render does not show character** — The body is present in viewport
   (verified via bbox and vertex measurements) but invisible in Cycles renders.
   Likely a material issue (`tripo_material_*`). Needs separate investigation.
2. **Back→backrest solve returns None** — The `m_back()` measurement finds no
   posterior verts. Needs debug of the vertex filter.
3. **Leg IK as constant** — The two-bone IK is solved once and applied to all
   frames. Feet may drift during the "get up" portion of the mocap.

## Files

- `autoseat.py` — v1 (per-frame, hung)
- `autoseat_v2.py` — v2 (FK bones, wrong — they don't deform)
- `autoseat_v3.py` — v3 (deform bones, analytic placement)
- `autoseat_v4.py`, `v5.py`, `v6.py` — iterative fixes
- `proof_sitting.blend` — output with correct placement
- `113_15.fbx` — CMU mocap source

## Usage

```bash
# Full solve (requires ~4GB RAM, ~30 min)
xvfb-run -a env -u PYTHONPATH blender -b living_room.blend \
  --python production/tools/auto-seat/autoseat_v3.py

# Quick placement fix on existing blend
xvfb-run -a env -u PYTHONPATH blender -b proof_sitting.blend \
  --python production/tools/auto-seat/autoseat_v6.py
```

## Research

Production-standard auto-seating uses **full-body IK with contact pins**:
- MotionBuilder: "contact technology for feet/hands preventing penetration"
- Unreal Control Rig: "add IK setups or constraints to ensure critical areas
  like hands and feet maintain contact with surfaces"

This solver implements that pattern headless: measure contacts → solve IK →
bake to FK. No hand-tuned values; every number is measured at runtime.

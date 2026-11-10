# Sitting Physics World

Owner directive 2026-10-19 ~16:13 CDT. Interactive physics for the sitting scene.

## What was built

### 1. Placement (LOCKED)
His widget placement applied to `CapeJones_Rig` in `scene_sit_placed.blend`:
- Delta matrix (Blender Z-up, column-major): `[0.29237170472273677,-0.9563047559630354,0,0, 0.9563047559630354,0.29237170472273677,0,0, 0,0,1,0, 0.07750696541475,4.337572671573705,-0.325,1]`
- This is CANON — do not modify without his word.

### 2. Functional Recliner (coupled mechanism)
- `recliner_rigged.blend` integrated (from `3d-assets/living-room/recliner/`)
- `recline` property: 0=retracted (default, no leg clipping), 1=extended
- **Coupled leg IK**: `foot_ik_L/R` follow the footrest pad via `ReclinerFollow` constraints (influence=recline). `ik_leg_L/R` driven by recline. When the rest extends, feet lift and move forward with it — no clipping.
- Old static chair `loungeChairRelax(Clone)` hidden.

### 3. Rigid-Body World
- **Active** (sleeping until hit): `okayest_hero_mug` (+handle, +text parented)
- **Passive**: Floor, coffee table, side table, recliner base
- Mug knocks off table if hit; table tips if hit hard.

### 4. Cape (cloth)
- Separate `CapeJones_Cape` mesh (221 verts) created at shoulders
- Cloth modifier with `cape_pin` vertex group (top rows pinned)
- Body and chair have Collision modifiers
- **Note**: Cloth bake requires a GPU or more RAM than the VM has. The modifier is set up; bake on a stronger machine. For stills, the base draped mesh is used.

### 5. Mesh Hole Repair (in progress)
Separate lane building automated repair pipeline for armpit/neck/cape holes. See `production/tools/mesh-repair/` (when complete).

## Files
- Blend scenes: `~/workspace/sitcanon-work/scene_sit_placed.blend` (placement), `scene_sit_phys.blend` (full physics)
- Scripts: `scripts/` (placement, recliner, coupling, rigid bodies, cape)
- Proof renders: `~/workspace/your_files/phys-proof-v1/` (render blocked by VM OOM on 910k mesh — see note)

## Render Note
Full-scene Cycles render OOMs on the 8GB VM (910k vert body). The 73k decimated mesh (`capejones_placed.glb`) renders fine and verifies placement. Full-quality render needs Kaggle GPU or similar.

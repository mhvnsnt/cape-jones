# SOURCES — anims/show/cape-jones/ (show clips for Cape Jones)

Show-context clips ONLY. Never fight movesets — the anim-gate law holds:
show clips play in SHOW / CUTSCENE / INTRO_OUTRO contexts, never FIGHT.

## Rig target (IMPORTANT — differs from western-heart's cape-jones clips)

These clips target the **CapeJones_Rig** (94 bones, 0.925 m native, cape-jones
repo canon — `3d-assets/cape-jones-rig/RIG-DOCS.md`), the owner's actual Cape
Jones show mesh. They do NOT target western-heart's `cyborg-x.glb`
(160-joint T7 Alisa port) — that rig has its own clip set in western-heart
`anims/show/cape-jones/` (PR wh#849, open). Bone names differ; clips are not
interchangeable. This directory is the show test-ground copy.

## Clips

| Slot | File | Source motion | Frames @ fps | Baked |
|---|---|---|---|---|
| idle | `idle.glb` | CMU `140_06.bvh` ("Idle", 3563f @120fps; used f200–680) | 121 @ 30 | 2026-10-23 |

## Motion source

- **CMU Graphics Lab Motion Capture Database** (`mocap.cs.cmu.edu`), via the
  BVH conversion mirror `una-dinosauria/cmu-mocap` (GitHub).
  File in-repo: `3d-assets/animation/mocap-cmu/140_06.bvh`
  (see `3d-assets/animation/mocap-cmu/MANIFEST.md`).
- License (verbatim CMU): "Use this data! This data is free for use in
  research and commercial projects worldwide." Attribution: "The data used in
  this project was obtained from mocap.cs.cmu.edu. The database was created
  with funding from NSF EIA-0196217."
- No hand-made or procedural animation. No fight movesets.

## Retarget method

- `tools/show-retarget/retarget_idle_cape.py` (committed) + bone map
  `tools/show-retarget/bonemap_cmu_to_capejones.json`.
- Rotation-delta retarget, parent-first, scale-safe (adapted from
  western-heart `tools/anim-retarget/retarget_rot.py`, proven on the
  cyborgx wave clip):
  `R_target_pose = (R_src_pose @ R_src_rest^-1) @ R_target_rest`
- Baked DIRECTLY onto deform bones (pelvis, spine_1/3, chest, neck_1/2,
  head, upperarm/forearm/hand, thigh/shin/foot/toe, thumb+index fingers) —
  the mesh is skinned to deform bones and FK→deform constraints do not
  survive GLB export, so the FK layer is bypassed for the baked clip.
- In-place (no root translation — idle). Source faces −Y, rig faces −Y
  (measured yaw 1.2°, negligible).
- Exported from a clean Blender session (factory settings): single armature
  + single action → one `show_idle` animation, 282 channels.
- Bind check on reimport against `3d-assets/cape-jones-rig/cape-jones-show.glb`:
  **940/940 fcurves bound** to the 94-bone rig.

## Model QA (2026-10-23)

- Weight audit (`tools/show-retarget/qa_weights.py` logic): 117,637
  head-region verts — dominant bones are head/jaw/neck/clavicle/chest;
  **0 verts dominated by spine/pelvis/lower** → PASS, no face-stretch bug.
- T-pose front/side renders: `shared/cast/proof/cape_tpose_front.png`,
  `shared/cast/proof/cape_tpose_side.png` (viewed).
- Moving proof: `shared/cast/proof/cape_idle_in_cape_room_v1.mp4`
  (Cape idling in the living room, Eevee) + checkframes PNG (viewed).
- Known exporter artifact: the model GLB carries a stray 24-vert `Cube`
  node at origin (same family as the documented Icosphere stray). Harmless:
  auto-hidden by the proof render script; does not affect skinning.

## Model export

- `3d-assets/cape-jones-rig/cape-jones-show.glb` — CapeJones_Rig (94) +
  CapeJones_Body + CapeJones_Cape, rest pose, skins, materials/textures.
  Exported from `3d-assets/living_room.blend` (never saved). The .blend is
  the source of truth; this GLB is the show pipeline's working copy.

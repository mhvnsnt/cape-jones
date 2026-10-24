# Moving show-clip proof — Cape Jones (own rig) idling in his living room (2026-10-23 CT)

Handoff step 1 ("render a moving proof clip in cape-jones and view it") — with
the owner's actual Cape Jones mesh on the repo's 94-bone CapeJones_Rig
(not a stand-in).

- Video: `cape_idle_in_cape_room_v1.mp4` — 640x360, h264, 61 frames @ 30 fps
  = 2.03 s (source 121f @30fps, frame_step 2, real-time speed).
- Check frames: `cape_idle_in_cape_room_v1_checkframes.png` (t = 0 / 1.0 / 2.0 s).
  Viewed: Cape stands on the living-room floor by the rug, breathing/shifting
  weight in a mocap idle; pose changes frame to frame (no T-pose), feet stay
  on the floor, nothing off-frame.
- Model: `3d-assets/cape-jones-rig/cape-jones-show.glb` (CapeJones_Rig,
  94 bones, 0.925 m native; body + cape, rest pose, skins, materials).
- Clip: `anims/show/cape-jones/idle.glb` — CMU `140_06` ("Idle") retargeted
  with `tools/show-retarget/retarget_idle_cape.py` (rotation-delta,
  parent-first, baked onto deform bones). Binding gate: **940/940 fcurves
  bound** to the 94-bone rig.
- Render: `blender -b 3d-assets/living_room.blend -P <wrapper of
  shared/cast/render_show_clip_in_room.py> -- cape-jones-show.glb idle.glb 0
  <out> '[1.2,0.9,0]' 121 BLENDER_EEVEE_NEXT 2` (Blender 4.2.0, Eevee).
  The .blend is never saved; room lighting/colours untouched (canon violet
  LED wash). The room's own rest-pose Cape figure is hidden for this proof.
- Show clip is SHOW-context only (ANIM-GATE); never in FIGHT.
- License: CMU Graphics Lab Motion Capture Database, free incl. commercial.
  "The data used in this project was obtained from mocap.cs.cmu.edu. The
  database was created with funding from NSF EIA-0196217."

## Model QA (same session)

- Weight audit: 117,637 head-region verts; dominant bones head/jaw/neck/
  clavicle/chest; **0 verts dominated by spine/pelvis/lower** → PASS
  (no face-stretch bug).
- T-pose: `cape_tpose_front.png`, `cape_tpose_side.png` (viewed).
- Known: model GLB carries a stray 24-vert `Cube` node at origin (glTF
  exporter artifact, same family as the documented Icosphere stray).
  Auto-hidden by the proof render; does not affect skinning.

## Work log

- Claimed: agent-ops#62. Branch: `cape-jones/3d-work-20261023`.
- Retarget: adapted western-heart `tools/anim-retarget/retarget_rot.py`
  (proven on cyborgx wave, wh#849) to the 94-bone CapeJones_Rig; bakes onto
  deform bones directly because FK→deform constraints don't survive GLB.
- Export gotcha (documented for the crew): the glTF exporter splits actions
  per-bone when the file holds multiple actions — bake/export from a clean
  (factory-settings) scene with exactly one action. Also: Blender imports
  GLB times→frames at the *current* scene fps — set 30 fps before importing
  a 30 fps clip or motion plays fast.
- /tmp on this box is a 512 MB tmpfs — work ran in ~/workspace/scratch/cj-3d.

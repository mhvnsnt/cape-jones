# CMU MoCap Starter Pack — MANIFEST

**Source:** Carnegie Mellon Graphics Lab Motion Capture Database
(http://mocap.cs.cmu.edu), via the BVH conversion mirror
`una-dinosauria/cmu-mocap` (GitHub). Downloaded 2026-10-17 as individual
subject files — no login, no signup.

## License (verbatim from CMU)

> "Use this data! This data is free for use in research and commercial
> projects worldwide. If you publish results obtained using this data, we
> would appreciate it if you would send the citation to your published paper
> to jkh+mocap@cs.cmu.edu, and also would add this text to your
> acknowledgments section: 'The data used in this project was obtained from
> mocap.cs.cmu.edu. The database was created with funding from NSF
> EIA-0196217.'"

The BVH conversion adds no further restrictions (cgspeed release notes).
**Commercial-safe, attribution appreciated.**

## Files (13 motions, 31-bone skeleton, 120fps BVH)

| File | CMU description | Animation-set slot | Frames |
|---|---|---|---|
| `140_06.bvh` | Idle | **Idle** (priority #1) | 3563 |
| `140_07.bvh` | Idle | **Idle** (variant) | 1236 |
| `13_05.bvh` | sit on stepstool, hands against chin, fidget | **Sitting idle** (90% screen-time set) | 4404 |
| `02_01.bvh` | walk | Walk | 344 |
| `07_01.bvh` | walk | Walk (variant) | 317 |
| `02_03.bvh` | run/jog | Run | 174 |
| `13_01.bvh` | sit on high stool, stand up | Sit/stand | 2314 |
| `13_29.bvh` | sit on stepstool, stand up, swing legs | Sit/stand (playful variant) | 4593 |
| `18_08.bvh` | conversation — explain with hand gestures | **Dialogue gestures** | 2087 |
| `13_26.bvh` | direct traffic, wave | Gesture (wave) | 3029 |
| `13_14.bvh` | laugh | **Reaction** | 2425 |
| `18_10.bvh` | quarrel — angry hand gestures | **Reaction** (anger) | 1806 |
| `13_09.bvh` | drink soda | Everyday (mug gag potential) | 1103 |

**Verified 2026-10-17:** all 13 import cleanly in Blender 4.0.2 headless
(`bpy.ops.import_anim.bvh`) — 31 bones each, frame counts as listed.

## Retarget notes for the rig/animation specialist

- CMU skeleton: 31 bones, different proportions/naming vs our 85-bone rig —
  **retarget required** (Rokoko addon, Auto-Rig Pro, or Blender native).
- CMU bone lengths are in inches × scale: multiply by **0.056444** for meters
  (per CMU FAQ). Our rig is 0.925m native — rescale on retarget, never rescale
  the rig.
- Motions are 120fps; the show pipeline frame rate is the specialist's call —
  bake to the working rate on import.
- Sitting clips reference stools/chairs that don't exist in our scene — the
  specialist adapts to the living-room chair (chair at 270° yaw under window,
  per SCENE-CANON.md). Cape collision is the specialist's domain.
- Full DB (thousands of motions) stays upstream — this pack is the starter
  set; pull more per-motion via the same URL pattern:
  `https://raw.githubusercontent.com/una-dinosauria/cmu-mocap/master/data/XXX/XX_XX.bvh`
  with the index at `cmu-mocap-index-text.txt` in that repo.
| `15_04.bvh` | dance / everyday moves (multi-activity trial) | **Dance loop — 3D dance proof v4**: window @ frame 12625 (front-facing, in-one-spot, seam-clean; see docs/production/AUTO-RIG-MOCAP-RESEARCH.md) | 22550 |

**Added 2026-10-31 (v4 dance lane):** `15_04.bvh` pulled from the same
CMU/cgspeed source under the same license above. Also pulled but NOT
committed: subjects 60/61 (salsa — rejected for the v4 shot: the dancer
faces ~-90° profile, partner work) and 05_03/05_11 (too short for the
loop window); disposition logged in the research doc.

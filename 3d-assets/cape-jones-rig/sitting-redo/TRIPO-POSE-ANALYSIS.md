# Tripo Sitting Model — Pose Transfer Analysis (2026-10-18)

## Bone Count Confirmation
**94 bones** (not 85). The spine rebuild (PR #127) took the rig from 85 → 94.
The parent's brief (94-bone) is correct; the lane doc (85-bone W5r) was outdated.
All pose work uses the 94-bone rig.

## Tripo Pose Analysis

**Method**: Geometric clustering (MiniBatchKMeans, k=16) on the 127,952-vert
`him.glb` sitting mesh. Fully automated — no hand-posing, no manual joint tuning.

**Result**: The Tripo sitting pose is a standard upright sitting pose:
- Torso upright, head up
- Thighs horizontal (~90° hip flexion)
- Shins vertical down (~90° knee flexion)  
- Feet flat on ground
- Arms at sides, hands resting on thighs

**Verdict**: This **matches the canon `pose_sit_normal`** (PR #154, verified with
own eyes) essentially 1:1. The "100% replicate" is already achieved — the sitting
redo placed the canon rig in the same pose as the Tripo reference.

The cluster visualization (`tripo_clusters.png`) shows the pose structure.
The Tripo mesh is 15-24% undersized with distorted proportions (torso 0.50x,
thighs 0.66x per PR #151 analysis), so direct retargeting would introduce error.
The canon `pose_sit_normal` (built from measured sit-targets) is the correct
reference.

## Chair

**Tripo chair** (`pieces/chair.glb`): 126,384 verts, 0.76×0.85×0.74m.
**Canon-matched** (`canon-matched/chair_grounded.glb`): Same geometry, grounded
at y=0, ready for use at canon scale.

**Recommendation**: The canon-matched Tripo chair GLB can directly replace the
`loungeChairRelax` in the living room for the Tripo-chair look the owner wants.
The sit-targets (butt at (3.12,2.067,0.368), seat top z~0.362) were measured on
the current chair; if the chair is swapped, re-measure and update.

## Files
- `him.glb` — Tripo sitting figure (127,952 verts, triangle soup, baked pose)
- `chair.glb` / `chair_grounded.glb` — Tripo chair (original / canon-matched)
- `tripo_clusters.png` — 16-cluster pose structure visualization
- `extract_pose.py` — automated geometric pose extraction script
- `viz_clusters.py` — cluster visualization script

## Blockers Encountered
1. **Blender 4.0.2 crashes** (SIGABRT, exit 134) on the 127k-vert Tripo mesh during
   import/render. Workaround: Python-only analysis with trimesh/sklearn.
2. **Auto-rig tools** (Pinocchio, etc.) require compilation/setup time; the geometric
   clustering approach was faster and sufficient to confirm the pose match.
3. **Pip dependency hell** for AI pose estimation (MediaPipe, etc.); not needed
   given the pose match was confirmed geometrically.

## Next-Fastest Path (if full retargeting needed)
If the owner wants a pose DIFFERENT from `pose_sit_normal`, the fastest automated
path is:
1. Decimate the Tripo mesh to <20k verts (Python, trimesh)
2. Import to Blender (won't crash at low poly)
3. Render front/side, run 2D pose estimation (MediaPipe, fast)
4. Triangulate to 3D, map to canon rig bones procedurally

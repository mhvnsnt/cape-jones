# mesh-repair — automated repair pipeline for Tripo-assembled characters

## The problem (root cause — two parts)

`CapeJones_Body` (910k verts) rendered with holes "torn all over": gaping
armpits, shotgun-blast holes across the upper neck/torso, holes in the cape.
The working theory was weight-painting / mocap-retarget damage.

**Automated diagnosis proved two separate defects:**

### 1. Unwelded part seams (the holes)

| measurement | value |
|---|---|
| disconnected open shells in the base mesh | 314 (zero closed) |
| boundary edges in the **rest** mesh | 62,174 |
| rest-pose boundary loop radii | max 0.156, p99 0.135 — all **degenerate/pinched** |
| same loops in the **sitting pose** | radii 2–5.8 (growth of 4–5.8 units) |
| new boundary loops created by the pose | 5 |

The mesh was **never welded**: 314 part shells share *coincident but
topologically unmerged* boundary verts (Tripo part assembly with no
remove-doubles pass). In rest pose the seams are pinched shut (radius ~0.02,
invisible). Under armature deformation, coincident verts carrying *different*
bone weights fly apart — 11% of sampled coincident pairs have weight
differences > 1.0 — so every part seam unzips in proportion to joint
rotation. **The pose doesn't tear the mesh; it reveals that the mesh was
never one piece.** Weight painting is innocent: zero verts have zero weight.

### 2. Mesh/rig object transform mismatch (the scatter)

The sitting placement moved **only the rig object**
(`CapeJones_Rig` → `(0.078, 4.338, -0.325)`, `-73°` yaw) and left the body
mesh object at identity. The Armature modifier assumes mesh space == armature
rest space, so with the rig 4.4 units from where the mesh sits, the deform
computed garbage: **182,557 verts displaced >2 units (bbox diag 1.37 → 14.3)**.
The skeleton itself was correct (pelvis lands 0.44 units from the chair);
only the mesh object transform was stale. Disabling the Armature modifier
returns the mesh to exactly rest size (diag 1.368, 0 flyers), proving the
modifier input — not the pose, not the weights — is the culprit.

## The fix

**A. Align the mesh to the rig** (`align_mesh_to_rig.py`): copy the rig's
world transform onto the body object. This does not move the character's
intended placement — it *restores* it (pelvis stays on the chair). Rule for
all future placements: the mesh object must carry the rig's world transform
(or be parented to it); moving the rig alone re-breaks the deform.

**B. Weld the seams with a modifier, not a destructive edit**
(`apply_weld.py`): builds a `weld_seams` vertex group containing exactly the
boundary verts found by `detect_seams.py`, then inserts a **Weld modifier**
(threshold 0.02, group-limited) **before** the Armature modifier:

```
WeldSeams (0.02, weld_seams group) -> Armature -> CorrectiveSmooth
```

* Coincident seam verts merge *before* deformation, so each seam deforms as
  one vert with blended weights — the skin **stretches** across joints
  instead of gaping. (This is the automated weight-redistribution the
  mandate asked for; the existing `corr_shoulderL/R` shape keys from PR #158
  keep handling volume.)
* Group-limiting means only seam verts can merge — lips, fingers, cloth
  layers and other close-but-separate interior verts are never touched.
* Non-destructive: delete the modifier and the source mesh is byte-identical.
* Pose-independent: it lives in the modifier stack, so **every future
  pose/animation is repaired automatically** — no per-pose work.

Measured result on the sitting scene: posed boundary edges **62,174 → 1,349**
(97.8% of seam edges welded shut); flyers **182,557 → 0** after alignment.

Why not edit-mode remove-doubles: on a 910k-vert / 11-shape-key mesh it OOMs
an 8GB box (edit-mode bmesh + undo). The modifier path uses numpy only and
peaks under 1.5GB.

## Pipeline

```
production/tools/mesh-repair/
├── README.md            this file
├── align_mesh_to_rig.py re-sync body object transform to the rig (placement fix)
├── detect_seams.py      numpy boundary-edge detection -> seam_vert_indices.npy
├── apply_weld.py        weld_seams group + Weld modifier before Armature
├── verify_repair.py     posed-mesh boundary recount + JSON verdict
└── run_pipeline.py      driver: align -> detect -> weld -> verify -> save NEW blend
```

One shot (never overwrites the input):

```bash
python3 run_pipeline.py \
  --input  scene_sit_placed.blend \
  --output scene_sit_placed_repaired.blend \
  --body   CapeJones_Body \
  --rig    CapeJones_Rig \
  --threshold 0.02
```

Or step by step inside headless Blender (all steps are numpy-only, no bmesh):

```bash
B=~/workspace/tools/blender/blender-4.0.2-linux-x64/blender
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python align_mesh_to_rig.py -- CapeJones_Body CapeJones_Rig
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python detect_seams.py -- CapeJones_Body ./wk
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python apply_weld.py  -- CapeJones_Body ./wk/seam_vert_indices.npy 0.02
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python verify_repair.py -- CapeJones_Body ./wk/verify.json
```

`verify_repair.py` reports `rest_boundary_edges`, `posed_boundary_edges`,
`posed_loop_count` and `welded_ok` (true when posed boundaries are under 5%
of the rest count). Remaining loops are listed with centroid/radius for review.

## Standing use

* **New character / new Tripo pull:** run `run_pipeline.py` on its blend before
  rigging. If `seam_fraction` is ~0, the mesh was already welded — the
  modifier is a harmless no-op.
* **New pose/animation tearing appears:** re-run `verify_repair.py` on the
  posed file; if `welded_ok` is false, re-run the full pipeline (threshold
  can go up in 0.005 steps; past 0.03, inspect — real gaps start merging).
* **True holes (non-degenerate rest loops):** none were found in this asset
  (max rest loop radius 0.156, all welded). If `verify_repair.py` ever flags
  a remaining loop with a large rest radius, that is genuinely missing
  topology — fill it with Blender's `Mesh > Clean Up > Fill Holes` on a
  lightweight proxy, then transfer; do not raise the weld threshold to
  "fix" it.

## Provenance

* Diagnosed 2026-10-19 on `scene_sit_placed.blend` (sitting pose, locked
  placement — untouched by this tool).
* Existing deform work preserved: PR #158 wave-2 correctives
  (`corr_shoulderL/R`, `corr_hipL/R`, …), PR #133 fingertip fix, and the
  `CorrectiveSmooth` modifier are all left in place; the weld runs before
  them in the stack.
* Proof renders (clay close-ups, before/after): armpit L/R, neck, chest —
  see the PR.

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

**B. Average the seams — no topology change** (`average_seams.py`):
for each coincident seam-vert cluster, set identical deform weights
(averaged, then normalized) and identical shape-key positions on all members.
Identical rest position + identical weights + identical shape offsets =
identical deformed position, so the seam stays shut (degenerate, invisible)
through every pose.

This was chosen over a Weld *modifier* for a hard technical reason: merging
verts changes the vert count (910,374 → 849,146), which permanently disables
the CorrectiveSmooth modifier — it needs the original mesh for reference,
and a topology-changing modifier before it breaks that correlation
(verified: fresh CorrectiveSmooth outputs all zeros with a Weld upstream).
The averaging approach changes zero topology, so CorrectiveSmooth, all 11
shape keys, UVs and vertex groups are preserved intact, and the skin
**stretches** across joints instead of gaping (the automated
weight-redistribution the mandate asked for; the existing `corr_shoulderL/R`
shape keys from PR #158 keep handling volume).

Only boundary-boundary coincident pairs are averaged — clothing-over-skin
contacts (seam vert meeting an interior vert) are left alone, so layered
parts can still slide.

Measured result on the sitting scene: flyers **182,557 → 0**, world bbox
diag **14.335 → 1.099**; posed seam separation **max 0.0026** (threshold 0.02,
was up to ~5.0 before repair); coincident-pair weight diff **exactly 0.0**;
CorrectiveSmooth **working** (verified non-zero output delta).

## Pipeline

```
production/tools/mesh-repair/
├── README.md            this file
├── align_mesh_to_rig.py re-sync body object transform to the rig (placement fix)
├── detect_seams.py      numpy boundary-edge detection -> seam_vert_indices.npy
├── average_seams.py     average weights + shape keys across coincident seam clusters
├── verify_repair.py     posed-mesh boundary recount + JSON verdict
└── run_pipeline.py      driver: align -> detect -> average -> verify -> save NEW blend
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
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python average_seams.py -- CapeJones_Body ./wk/seam_vert_indices.npy 0.02
xvfb-run -a env -u PYTHONPATH $B -b in.blend --python verify_repair.py -- CapeJones_Body ./wk/verify.json
```

`verify_repair.py` reports `seam_verts`, `posed_max_seam_separation`,
`posed_p99_seam_separation`, `posed_frac_seams_open`,
`corrective_smooth_working` and `repaired_ok` (true when max separation is
under threshold and CorrectiveSmooth is alive). Note: boundary-edge COUNT
does not drop with averaging (no topology change) — separation is the
correct metric.

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

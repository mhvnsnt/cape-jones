# Weight Bake-Off 2026 — Cape Jones model

**Lane:** `rig/weight-bakeoff-20261017` · **Date:** 2026-10-17 · **Owner directive:** run the
Cape Jones model through EVERY weight-painting/skinning pipeline we've built across the
repos, plus open-source ones if ours aren't enough. Compare on test poses, keep the best,
wire the winner into the repo.

**Test model:** `~/workspace/cj-rev2-scratch/cape_jones_plain.glb` — 54 MB, valid glTF,
991,082 verts / 1,915,208 tris, native **0.925 m** (DO NOT RESCALE — owner scale lock).
Unrigged Tripo bake: T-pose, arms along ±Y, faces +X, cape fused behind (−X).
No skeleton, no weights, no vertex groups on import (verified headless, Blender 4.0.2).

**Common test rig (CJ-TEST skeleton):** 20 bones, built by
`tools/weights/cj_bakeoff/bakeoff.py::BONES` from measured mesh landmarks
(arm centerline z≈0.26, elbow |y|≈0.27, wrist |y|≈0.40, knee z≈−0.185, ankle z≈−0.37 —
see `docs/research/WEIGHT-BAKEOFF-2026.md` method notes). Bone placement verified:
every bone midpoint inside the mesh (KDTree nearest-surface check, worst case
Chest 0.064 m vs 0.16 m limit). The SAME skeleton is used for every entry, so the
comparison is apples-to-apples. Weights are skeleton-bound — see the handoff note
for how to carry the winning technique to the BlenRig 6 rig.

**Test poses (7):** P1 rest · P2 arms_raised · P3 elbow_90+ · P4 knee_deep ·
P5 shoulder_raise · P6 head_turn · P7 crouch.
**Acceptance:** no candy-wrapper elbows, no collapsing shoulders/hips.
**Render setup:** Cycles CPU, 480×270, 6 samples, clay material, 3/4 front view —
every proof render below was read with own eyes.

## 1. Inventory of OUR weight pipelines

| # | Pipeline | Location | What it does | How to run |
|---|---|---|---|---|
| W1 | Blender Bone Heat (`ARMATURE_AUTO`) | built into Blender 4.0.2 (GPL) | diffusion-based automatic weights | `bpy.ops.object.parent_set(type='ARMATURE_AUTO')` |
| W2 | Blender Envelope weights | built into Blender 4.0.2 (GPL) | bone-envelope distance falloff | `bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')` |
| W4 | BrutalFist `auto_rig_humanoid.py` | `brutalfist-fix/tools/animation/auto_rig_humanoid.py` | end-to-end: builds its own bounding-box landmark skeleton, then Bone Heat; exports rigged GLB | `blender -b --python tools/animation/auto_rig_humanoid.py -- in.glb out.glb` |
| W5 | bannon-video-pipe stack | `bannon-video-pipe/docs/AI_RIGGING_RESEARCH.md` §1 | Bone Heat + Armature-modifier **Preserve Volume** (true dual-quaternion skinning) + **Corrective Smooth** modifier | 3 lines of bpy (see doc) |
| W6 | bannon-video-pipe twist bones | same doc §4 | split limbs into twist segments; Copy Rotation (twist axis only, 0.5→1.0 down chain); redistribute weights with gradient falloff | scriptable headless; bakes cleanly to GLB |
| W7 | BlenRig 6 mesh-deform cage | `production/tools/blenrig6` (`blenrig.bind_mdef_modifiers`) | cage deformed by armature → Mesh Deform bind on the body (BlenRig's core skinning method; full guide-fitted bind belongs to the rig lane) | convex-hull cage → decimate → `ARMATURE_AUTO` on cage → `meshdeform_bind` |
| — | Corrective shape keys (driver-driven) | bannon-video-pipe doc §3 | sculpt corrective at problem pose, drive via bone rotation; exports to glTF as morph targets | Pose Shape Keys addon (Blender Studio, OSS) — render/game portable, listed for the rig lane |
| — | Blender weight cleanup tools | built-in | Normalize All, Mirror, Data Transfer (`VGROUP_WEIGHTS`), smooth brushes — scripted cleanup after any auto pass | `bpy` / Weight Paint mode |

**Searched, not applicable:** `wmxix-mesh-decode`/yukes-extractors (no repo in workspace —
only the lead name from the task; nothing found), `western-heart/tools` (no weight/skin
scripts — searched `*weight*`/`*skin*`), cape-jones `tools/` + `production/pipeline`
(no skinning scripts; `coa_tools2/operators/edit_weights.py` is 2D cutout-animation,
not 3D skinning), `brutalfist-fix/tools/weight-paint-pwa` (three.js weight-*painting*
PWA viewer — manual painting UI, not an auto-weight pipeline; noted for the manual lane).

## 2. Open-source pulls (2026 research, verified licenses)

| Tool | License | Verdict |
|---|---|---|
| **Surface Heat Diffuse Skinning** v3.4.2 (meshonline) — "never fails" Bone Heat alternative | MIT | ✅ PULLED → `tools/weights/surface-heat-diffuse/` (Linux solver compiled from `src/` via `build_linux.sh`; headless flow documented in `HEADLESS.md`; binary gitignored as build artifact) |
| DV Skin Tools (weight-painting workflow tools) | GPL-3.0 | documented only — requires Blender 4.2+ (we run 4.0.2); not auto-skinning |
| Easy Weight (Blender Studio) | Blender/OSS | documented only — paint-mode QoL, not a weight generator |
| Voxel Heat Diffuse Skinning (meshonline) | **paid** | ❌ skipped — no-paid law |
| Adaptive Auto Skinning (Jessy Leite, 80.9% artist-match on 202-char benchmark, Sept 2026) | **paid** (Superhive) | ❌ skipped — no-paid law; revisit if a free tier appears |

## 3. Results

Scoring per pose: ✅ clean · ⚠️ minor artifact · ❌ fails acceptance.
"n/a" = entry produced no usable weights, poses not judgeable.

### W1 — Blender Bone Heat (built-in)

> `Warning: Bone Heat Weighting: failed to find solution for one or more bones`
> (verbatim, 307 s on the full mesh) → **20 empty vertex groups, 991,082/991,082 verts
> (100.0%) with NO weights.** All 7 pose renders identical to rest pose.

| P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a | n/a | n/a |

**Verdict: FAIL.** Blender's heat solver cannot handle this 991k-vert Tripo mesh
(non-manifold bake, dense). This is the failure the open-source pull (W3) exists to fix.

### W1p — Bone Heat on decimated proxy (80k), Data-Transfer to full mesh

*Rescue variant of the same technique — result pending.*

### W3 — Surface Heat Diffuse Skinning (meshonline, MIT)

*Result pending — run in flight.*

### W2 — Blender Envelope weights

*Result pending.*

### W4 — BrutalFist auto_rig_humanoid.py (our pipeline, as-is)

*Result pending. Note for the record: `build_humanoid()` derives height from
`hi.y - lo.y` (Y-up assumption); a Blender-imported glTF is Z-up, so the landmark
skeleton is expected to be wrong on this model. The bake-off runs it unmodified —
fixing the axis assumption is a brutalfist-lane decision, flagged in the handoff.*

### W5 — W1 weights + Preserve Volume + Corrective Smooth

*Blocked on W1's failure — rebased onto the winning weight set (see §4).*

### W6 — W1 weights + twist bones

*Blocked on W1's failure — rebased onto the winning weight set (see §4).*

### W7 — BlenRig-6-style mesh-deform cage

*Result pending.*

## 4. Comparison matrix & winner

*Pending — filled after all entries render and are read.*

## 5. AI-tooling status

| Tool | Status | Detail |
|---|---|---|
| GitHub Copilot CLI v1.0.98 | ✅ LIVE | PAT-authenticated 2026-10-17 ~00:08 (fine-grained "Copilot CLI" token, `COPILOT_GITHUB_TOKEN` in `~/.bashrc`). Used for repo research/iteration in this lane. `.github/copilot-instructions.md` landed with repo conventions (scale lock, colorway `#731AE5`, branch→PR→merge, `xvfb-run -a` + `env -u PYTHONPATH`, verify-before-claiming). |
| Aider (`~/workspace/tools/aider`) | ❌ key-blocked | Needs `GEMINI_API_KEY` — env var confirmed EMPTY (read-only check). Ready-to-run task once the key lands (below). |
| Cline CLI | ❌ not installed + key-blocked | `cline` not on PATH (npm globals show only `@github/copilot`). Needs install + `GEMINI_API_KEY`. Ready-to-run task below. |
| Colab (`notebooks/colab/` pattern) | ➖ not needed | Weight computation is CPU-bound bpy/shd work that runs fine headless on the VM; no GPU step justified — extending the notebook pattern would be show, not substance. |
| Browser/OAuth flows | ➖ NEEDS-PARENT-BROWSER | Per lane rules, no live-browser OAuth attempted (Mixamo/Cinevva/Tripo web riggers stay documented-only). |

**Aider ready-to-run (the moment `GEMINI_API_KEY` lands):**
```bash
export GEMINI_API_KEY="$GEMINI_API_KEY"   # from secure storage, never chat/files
cd ~/workspace/cape-jones-bakeoff
aider --model gemini-2.5-pro \
  --message "In tools/weights/cj_bakeoff/bakeoff.py, add a W8 entry: Laplacian-smoothed
  distance-falloff weights (closest-bone distance, smoothstep falloff, 20 Laplacian
  smooth iterations, normalize). Reuse build_skeleton/POSES/apply_pose. Keep headless
  (blender -b) compatible, no new dependencies."
```

**Cline ready-to-run (once `cline` CLI is installed and keyed):**
```bash
cline "In the cape-jones repo on branch rig/weight-bakeoff-20261017, read
docs/research/WEIGHT-BAKEOFF-2026.md section 3, then implement the documented
follow-up with the lowest effort-to-gain ratio as a new commit on this branch.
Do not touch other lanes' branches."
```

## 6. Method notes (reproducibility)

- Blender 4.0.2 headless: `xvfb-run -a env -u PYTHONPATH <blender> -b --python ...`
  (bare `-b` segfaults — libEGL; system numpy breaks Blender's Python).
- glTF import ≈ 69 s; Cycles CPU 480×270 @ 6 samples ≈ 35 s/frame on 1.9M tris.
- Workbench/matcap rendering segfaults under xvfb here — Cycles used instead.
- 7 GB VM RAM: one Blender at a time; BVH on the full mesh OOMs (RC=137) —
  KDTree used for the bone-inside-mesh check instead.
- Scratch (blends, full-res renders): `~/workspace/weight-bakeoff-scratch/` (NOT /tmp —
  512M tmpfs). Proof renders referenced below are copied to `docs/research/bakeoff-proofs/`.

## 7. Proof renders

*Copied here as entries complete. Every image below was read with own eyes in this lane.*

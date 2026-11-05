# Cape Jones 3D Dance v5 — Rig-First Research: Auto-Rigging, Skin-Weight Solving, Deformation Correctives

**Date:** 2026-11-02 · **Target:** Blender 5.2.3, headless Linux · **Character:** 0.925 m stylized hero, existing custom 94-bone FK/IK armature, BlenRig 6 mesh-deform cage available, mesh may be non-manifold / multi-part
**Constraint set:** open/free only, license noted for everything. No paid software, no cracked installers, no account sign-ins. Paid/account-walled tools are covered METHODS-ONLY.
**Research method:** live web research 2026-11-02 (browser search + source pages, 2025–2026 sources prioritised). Every URL below is copied verbatim from a search result. Where a licence or maintenance claim could not be verified from a primary source, it is flagged UNVERIFIED rather than asserted.

---

## 0. Executive verdict — the recommended stack (all open/free, all headless-capable)

Do **not** replace the rig with an ML auto-rigger's skeleton. The character already has a designed 94-bone rig and choreography built for it. The failure is almost certainly **weights + joint placement + LBS volume loss**, not skeleton topology. Recommended pipeline, in order:

1. **Control rig (a): CloudRig** — already carried in the repo as `production/tools/cloudrig`. Regenerate/extend the control layer on top of the existing deform skeleton. Rigify is the fallback / metarig vocabulary. Neither re-skins anything — that is deliberate: rig generation and skinning are separate problems.
2. **Skin weights (b): Surface Heat Diffuse Skinning (MIT, free, GitHub)** as the first re-bind — it is the open sibling of Voxel Heat Diffuse Skinning and is explicitly built to *never* throw Blender's bone-heat failure — **on a cleaned, temporarily scaled-up copy** of the mesh. Then **Data Transfer** weights from a clean low-res proxy/cage if parts still fail. Blender built-in bone-heat is the same algorithm family and is fine *after* cleanup; it is not fine on the raw multi-part mesh.
3. **For a gold-standard offline weight solve (optional, higher effort): libigl Bounded Biharmonic Weights via fTetWild tetrahedralisation (MPL-2.0)** — NOT TetGen (AGPL) and NOT MOSEK (commercial). This is a build-a-tool job, not a plug-in.
4. **Correctives (c): native, exportable, no add-on dependency** — (i) Armature `Preserve Volume` (dual-quaternion skinning) ON for Blender-side proof, understanding it does not travel to most game/glTF runtimes; (ii) Corrective Smooth (Delta-Mush family) restricted by a painted vertex group to shoulder/bicep only; (iii) sculpted pose-space corrective shape keys for the shoulder driven by a **reproduced RBF solver in pure Python** (Wendland kernel, `scipy`-style RBF interpolation baked to shape-key drivers) — this reproduces the SHAPES / RBF Nodes method without buying it; (iv) helper/twist bones (upper-arm twist, clavicle/shoulder helper, bicep bulge bone) — the AccuRIG/Auto-Rig Pro method, reproducible free.
5. **UniRig (MIT, SIGGRAPH 2025)** is the one ML system worth a *side experiment*: run it on a decimated copy, harvest its **joint positions and skin weights as a reference / Data Transfer source**, compare shoulder placement against the hand-built rig. Do not adopt its skeleton wholesale. **RigNet is superseded and effectively abandonware for this purpose** (see §A7).

**Scale warning specific to this character:** at 0.925 m the mesh is small for Blender's heat solver. A repeatedly documented fix is to scale mesh+armature up (10× is commonly cited in weight-painting guides), bind, then scale back — or set the Corrective Smooth `Scale` parameter correctly. Test this before blaming the algorithm.

---

## 1. Diagnosis: why shoulders/biceps go "broken and stiff" — and what actually fixes each cause

| # | Likely cause on this character | Evidence pattern in the literature | Fix (section) |
|---|---|---|---|
| 1 | Bone-heat bind failed / partially failed on non-manifold, multi-island mesh, leaving unweighted or single-bone (stiff, 0/1) regions | 2026 triage of 46 Mixamo characters in Blender 4.5: every failure was a multi-piece character (one had 385 islands) with heavy non-manifold geometry; single-mesh manifold humanoids almost never failed — https://jessyleite.dev/posts/blender-bone-heat-weighting-failed/ | Clean-up + Surface Heat Diffuse / proxy Data Transfer (§B1–B2) |
| 2 | Upper-arm bone head placed too high / outside the volume, clavicle not sharing the shoulder load | Shoulder is consistently named the worst deformation region; fixes are bone placement first, then diffuse weights at the crease — https://blenderartists.org/t/can-i-achieve-a-better-deformation-of-the-mesh/1266339 | Re-place clavicle/upper-arm, split shoulder load across clavicle + upper arm + shoulder-helper (§5) |
| 3 | Linear blend skinning volume loss / "candy-wrapper" twist on the bicep/forearm | LBS collapses at bends/twists; DQS preserves volume but bulges; PSD correctives fix the residual — https://game-ace.com/blog/game-character-skinning/ | Preserve Volume + twist bones + PSD correctives (§C1–C3) |
| 4 | Corrective Smooth used globally as a substitute for weights | "Corrective smooth is useful but only as the icing on the cake… Get the deformation without corrective smooth as good as possible and only then use it selectively" — same Blender Artists thread above | Weights first; Corrective Smooth masked to shoulder only (§C1) |
| 5 | Mesh too small (0.925 m) / unapplied scale confusing the solver | Weight guides list scale-up-then-bind as a standard bone-heat rescue; Corrective Smooth gained an explicit Scale parameter for exactly this — https://docs.blender.org/manual/ar/4.3/modeling/modifiers/deform/corrective_smooth.html | Apply transforms; bind at larger scale (§5) |
| 6 | No twist distribution: one upper-arm bone takes all forearm rotation | AccuRIG's published method allocates *additional bone segments* to redistribute twist weights and stop forearm wringing — https://www.reallusion.com/auto-rig/accurig/ | Add 1–2 twist/helper bones per arm (§C3) |

---

## (a) AUTOMATIC RIGGING — ranked shortlist

### A1. CloudRig (Blender Studio) — RANK 1 for this lane ★ already in the repo
- **What it does:** Rig *generation*, not auto-detection. From a simple metarig (bones + per-bone component types: Limb: Biped Leg, Chain: FK / Toon / Physics, Spine: IK/FK, etc.) it generates the full control rig — helper bones, constraints, drivers, IK/FK, custom shapes, rig UI. Used for Blender Studio open movies from Coffee Run (2020) through Project Storm (Blender 5.0, body rig built with CloudRig). Still actively presented at BCON26 (2026).
- **License:** Blender add-ons are GPL-family; CloudRig is distributed free via the Blender Extensions platform. Exact licence file in the repo submodule should be read in-tree before redistribution — flagged, not assumed.
- **Get it:** https://extensions.blender.org/add-ons/cloudrig/ · docs: https://studio.blender.org/tools/addons/cloudrig/introduction · component types: https://studio.blender.org/tools/addons/cloudrig/cloudrig-types · BCON26 talk listing: https://studio.blender.org/blog/bcon26-blender-studio-talks/?utm_medium=homepage
- **Headless Linux:** Yes — it is pure Blender Python (`bpy`), generation is scriptable, no modal/viewport step required in principle. The cape-jones repo already carries it at `production/tools/cloudrig` (per task brief) — use that pinned copy, do not re-download a different version mid-lane.
- **What it solves / doesn't:** Solves control-rig quality, IK/FK switching, action/constraint-based shoulder helpers. Does **not** detect joints from the mesh and does **not** paint weights. Pair it with §B for skinning.
- **Verdict:** KEEP AS PRIMARY. This is the industry-standard *open* answer in 2026 — "several studios rely on" Rigify+CloudRig per the 2026 add-on survey: https://www.strayspark.studio/blog/best-blender-rigging-addons-2026

### A2. Rigify (built into Blender) — RANK 2
- **What it does:** Metarig → generated control rig (IK/FK limbs, tweak bones, widgets). You place the metarig bones by hand/coordinate; generation is one operator.
- **License:** GPL (part of Blender). **Get it:** bundled — Add ▸ Armature ▸ Human (Meta-Rig); no download.
- **Headless Linux:** Yes, fully — documented as "fully headless-capable (no modal ops)": add metarig, set edit-bone head/tail by coordinate, `rigify_generate()` — https://github.com/newsbubbles/riggs/blob/HEAD/notes/01-landscape.md
- **Limits:** *No feature detection* — joint landmarks must be supplied (by hand, by the existing rig, or harvested from UniRig, §A3). Only `DEF-` bones deform.
- **Verdict:** The vocabulary CloudRig extends. Use Rigify samples/metarig conventions even when generating with CloudRig so retargeting and naming stay standard.

### A3. UniRig (VAST-AI / Tsinghua, SIGGRAPH 2025) — RANK 3, best ML option ★
- **What it does:** End-to-end learned rigging: a GPT-like autoregressive transformer predicts a topologically valid skeleton ("Skeleton Tree Tokenization"), then a bone-point cross-attention head predicts per-vertex skinning weights (+ bone attributes). Trained on Rig-XL / Articulation-XL (14,000+ rigged models). Input .obj/.fbx/.glb/.vrm → output rigged .fbx.
- **License:** **MIT** for the code (multiple independent 2026 surveys agree it is "the only cleanly commercial-OK local option" among ML riggers). ⚠️ Verify the Hugging Face *checkpoint* licence card separately from the code licence before commercial use — the surveys explicitly flag this split.
- **Get it:** https://github.com/VAST-AI-Research/UniRig/tree/3241154cd5cdd56a81f0e32a1e73db7f2d22cc8b · checkpoints auto-download from Hugging Face (`VAST-AI/UniRig`) on first inference run.
- **Headless Linux:** Yes — CLI scripts (`generate_skeleton.sh`, `generate_skin.sh`, `run.py --task=...`), Python 3.11, PyTorch ≥ 2.3.1. Needs a GPU for sane speed (the lane has Kaggle/Colab per workspace notes; CPU inference is minutes-scale, not interactive). No account needed for the repo; HF checkpoint download is the only network fetch.
- **Limits:** Its skeleton is *its own learned topology*, not your 94-bone rig — adopting it means re-doing choreography retargeting. Quality "degrades sharply when skeleton prediction misses limbs" (2026 feasibility survey: https://github.com/jangtrinh/design-os-3d-blender/blob/HEAD/research/oss-models.md).
- **Verdict:** EXPERIMENT, DON'T ADOPT. Best use here: run on a decimated copy, use predicted shoulder/elbow positions as an objective second opinion on joint placement, and Data-Transfer its skin weights onto the real mesh as a candidate weight set to A/B against §B1.

### A4. Make-It-Animatable / MIA (CVPR 2025 Highlight) — RANK 4, best humanoid-specific ML
- **What it does:** Predicts bones + blend weights + pose-to-rest transforms for humanoids in <1 s, in *arbitrary input poses* (not just T/A-pose — rare and valuable). Targets the **Mixamo skeleton**, the easiest retarget in the ecosystem. Particle-based shape autoencoder; supports meshes and 3D Gaussian splats.
- **License:** ⚠️ **AMBIGUOUS — flagged honestly.** One 2026 survey found Apache-2.0 on GitHub vs CC-BY-NC-4.0 on the HF Space. Resolve the actual LICENSE file in the repo before any commercial/sellable use. Research/internal comparison use is the safe posture until resolved.
- **Get it:** https://github.com/jasongzy/Make-It-Animatable · paper: https://openaccess.thecvf.com/content/CVPR2025/html/Guo_Make-It-Animatable_An_Efficient_Framework_for_Authoring_Animation-Ready_3D_Characters_CVPR_2025_paper.html
- **Headless Linux:** Yes — Python/PyTorch CLI, uses Blender's `bpy` internally for dataset/pairing work; pretrained weights via HF (Git LFS). GPU expected.
- **Verdict:** Strong second ML opinion, especially *because* it outputs a Mixamo-topology rig — useful as a retarget bridge. Licence ambiguity keeps it below UniRig.

### A5. BlenRig 6 (Juan Pablo Bouza) — RANK 5, already available to this character
- **What it does:** Film-quality biped auto-rig + skinning *system*: armature + **Mesh Deform cage** + lattices, pre-weighted proxy (only hands/face rely on weight painting), automatic corrective shape keys + drivers, sculpt-in-pose shape-key workflow, reproportion mode (fit armature → bake mesh/armature → fit cage → Mesh Deform modifier drives the real mesh with *no direct weights on it*).
- **License:** **GPL** — "BlenRig is GPL… available in a public GIT repository" (Blender Studio release post).
- **Get it:** https://studio.blender.org/blog/blenrig-blenrig-public-release/ · product/free-download page: https://superhivemarket.com/products/blenrig?search_id=32785865 · archived Blender-org fork: https://projects.blender.org/archive/blenrig
- **Headless Linux:** Partially — the rig itself is plain bones/constraints/drivers (headless-safe once built), but the *guided reproportion/baking workflow is interactive by design*. Build interactively once, automate afterwards.
- **Verdict:** HIGH VALUE FOR THE SHOULDER SPECIFICALLY, because the cage sidesteps the whole weight problem: skin the *cage* (simple, manifold, low-res — bone heat works on it), let Mesh Deform carry the messy hero mesh. This is also the classic rescue quoted in Blender Artists shoulder threads: "make a quick cage, autoweight it, then data transfer weights back onto your mesh." The task brief says the cage is already available — use it (§5, step 3b).

### A6. Pinocchio (Baran & Popović, SIGGRAPH 2007) — RANK 6, method yes / code caution
- **What it does:** The classical template-embedding auto-rigger: fits a predefined skeleton template *inside* the mesh volume (penalising bone positions outside/at the surface), then computes heat-diffusion weights (the direct ancestor of Blender's bone-heat). No ML.
- **License:** ⚠️ **Core library LGPL-2.1-or-later; only the demo is MIT.** A 2026 implementer (QtMeshEditor #407) explicitly refused to vendor it for this reason and re-implemented the *published algorithm* from scratch instead — the algorithm is published and unencumbered, the code is LGPL: https://github.com/fernandotonon/qtmesheditor/issues/407 and https://github.com/fernandotonon/QtMeshEditor/pull/754
- **Headless Linux:** The original C++ builds on Linux, but the codebase is 2007-era, unmaintained as a product, and assumes a roughly upright, manifold mesh — exactly what this mesh may not be.
- **Verdict:** RESEARCH-CODE / METHOD ONLY for this lane. Its two ideas are already in the stack: template embedding (= place the existing metarig correctly) and heat weights (= §B2). Do not pull the LGPL library into the repo.

### A7. RigNet (Xu et al., SIGGRAPH 2020) — NOT RECOMMENDED, flagged honestly ⛔
- **What it does:** The field's founding learned rigger: GMEdgeConv joint prediction + mean-shift clustering → BoneNet connectivity → SkinNet weights refined from volumetric geodesic distances.
- **License:** **GPL-3.0 or commercial licence from UMass** — stated on its own project page: http://zhan-xu.github.io/rig-net/
- **Hard limits (from its own docs):** input must be simplified to **1K–5K vertices** (`simplify_quadric_decimation(4000)`), normalised to unit scale, voxelised at 88³ with the external `binvox` tool, ~120 s/shape, rest-pose input expected, legacy CUDA-era dependencies.
- **Maintenance verdict:** Superseded on every axis by UniRig (same task, MIT, 2025, larger data). 2026 surveys list it verbatim as "does both, but GPLv3, unmaintained, legacy CUDA… Superseded" — https://github.com/newsbubbles/riggs/blob/HEAD/notes/01-landscape.md
- **Verdict:** ABANDONWARE-FOR-THIS-PURPOSE. Do not start a RigNet integration in 2026. Its one transferable idea — *volumetric geodesic distance as a skinning prior* — is reproduced by §B5/B1 without the code.

### A8. Newer ML riggers — research radar only (2025–2026)
From the 2026 C#-port survey (https://github.com/zeljkovranjes/auto-rigger/blob/HEAD/README.md) and CharForge's living paper (https://majieddd.github.io/charforge/paper/): **MagicArticulate** (ByteDance, autoregressive skeleton + diffusion skinning, research-stage), **Puppeteer** (ByteDance, skeleton + PartField skinning transformer, needs NVIDIA GPU), **SkinTokens/TokenRig** (VAST-AI 2026, skeleton+skin as one token sequence, ~14 GB VRAM / CUDA 12.1 / flash-attn), **HumanRig** (Alibaba, humanoid-specialised, uniform topology, built for messy AI meshes, requires T-pose), **RigAnything** (Adobe, **non-commercial research licence — excluded**), **Anymate** (Apache-2.0 per survey, mainly a dataset/benchmark contribution). None beats UniRig+MIA on licence+ maturity for this lane today. **Flag: research-code-only until proven otherwise.**

### A9. METHODS-ONLY: Auto-Rig Pro / Mixamo / AccuRIG (paid or account-walled — do not pull)
| Tool | Status | Technique worth reproducing free |
|---|---|---|
| **Auto-Rig Pro** (~$40+, paid) | Best-selling Blender add-on 2026; its "Smart" auto-placement is a viewport-modal operator — "full headless ARP is unverified and risky" (survey above) | **Landmark-based placement:** a small set of human-placed/estimated landmarks → full limb chains with correct bone roll → bind. Reproduce: landmarks from the existing rig / UniRig prediction → CloudRig generation. Its FBX/game export stage *is* scriptable, but that does not justify a purchase for this fix. |
| **Mixamo** (Adobe, free but account + upload, GUI-only, no API) | "Disqualified from an autonomous pipeline" — no CLI/headless path (survey above) | **Five-marker method:** chin / wrists / elbows / knees / groin markers → server skeleton + weights (https://www.tripo3d.ai/blog/rig-ai-generated-character-for-mixamo). Reproduce locally: those 5 landmarks + symmetry + proportion rules are enough to auto-place a humanoid metarig; MIA (§A4) is literally trained to emit this skeleton offline. |
| **AccuRIG** (Reallusion, free download but standalone GUI, Windows-oriented) | No headless/Linux pipeline path verified | **Three published methods, all reproducible:** (1) correctable guide markers + finger-count choice; (2) **extra twist bone segments to redistribute forearm twist weights**; (3) **partitioned weights that retain volume around joints by accounting for central bone + surrounding musculature**, incl. obstructed-shoulder / oversized-head handling — https://www.reallusion.com/auto-rig/accurig/ |

---

## (b) SKIN-WEIGHT SOLVING — ranked shortlist

### B1. Surface Heat Diffuse Skinning (Mesh Online) — RANK 1 for the immediate re-bind ★
- **What it does:** Drop-in replacement for Blender's "With Automatic Weights" that diffuses heat *iteratively toward a stable solution* instead of solving the surface Laplacian once — the author's stated goal is a solver that **never fails** where bone-heat fails. Ships as a Blender add-on (Python + small native helper); the **Voxel** sibling (paid product) voxelises the character into a solid and diffuses *through the volume*, so 20 overlapping shells skin as one body.
- **License:** **MIT** — "The project has been released under the very permissive MIT license" (repo README). The *Voxel* product is paid (~$30, Superhive/Blender Market listings) — **do not buy/pull it for this lane; reproduce its method if needed (§B5).**
- **Get it (free code):** https://github.com/meshonline/Surface-Heat-Diffuse-Skinning · paid Voxel product page (reference only): https://www.mesh-online.net/voxel.html
- **Headless Linux:** ⚠️ PARTIAL / VERIFY IN-TREE. The free repo's prebuilt is old (page states last updated April 2, 2022; product line supports Blender 2.78–3.3 / Voxel line to ~4.1-alpha). Source is provided and buildable, and the algorithm is simple iteration, but **Blender 5.2.3 compatibility of the shipped binary is NOT verified** — budget a port/smoke-test step, or re-implement the iteration in pure `bpy`/numpy (feasible: it operates on vertex groups). Flagged honestly: this is the best *algorithm* for the job and a stale *package*.
- **What it solves:** Exactly failure-cause #1 — binds multi-part/non-manifold characters that bone-heat refuses, with bone-heat-comparable quality on clean areas.

### B2. Blender built-in bone-heat ("With Automatic Weights") + cleanup discipline — RANK 2
- **What it does:** Steady-state heat diffusion on the mesh surface; each bone is a heat source (Pinocchio-family). `Ctrl+P ▸ Armature Deform ▸ With Automatic Weights`, scriptable as `bpy.ops.object.parent_set(type='ARMATURE_AUTO')`.
- **License:** GPL (Blender itself). **Get it:** built in, nothing to pull.
- **Headless Linux:** Yes, fully scriptable — this is its main advantage over B1.
- **Preconditions (the whole game):** Merge by Distance (0.0001 m) → Degenerate Dissolve → Delete Loose → Select All by Trait ▸ Non-Manifold and fix → Recalculate Outside normals → apply all transforms → every deform bone inside the mesh volume (a root/helper bone outside the silhouette returns no samples and aborts the bind) → bind per loose part if islands persist. Sources: https://jessyleite.dev/posts/blender-bone-heat-weighting-failed/ and https://app.cinevva.com/guides/blender-weight-painting-problems
- **Post-passes (built-in, scriptable, do all of them):** Weights ▸ Clean → Limit Total (4) → Normalize All → Smooth (selected bones only; "All" leaks weights) → Mirror Vertex Groups. Then Data Transfer (§B3).
- **Verdict:** The free floor. On a *cleaned proxy* it is good; on the raw hero mesh it is the thing that already failed.

### B3. Proxy/cage weighting + Mesh Data Transfer — RANK 2 (tied, the production rescue pattern)
- **What it does:** Skin a simple, manifold, low-res stand-in (decimated copy, convex-ish proxy, or the **BlenRig mesh-deform cage**), where any solver succeeds, then transfer weights to the hero mesh with Blender's **Data Transfer** modifier/operator (vertex groups, Nearest Face Interpolated / Projected Face Interpolated mapping). Identical-topology copies can transfer by index; retopologised targets use the projected mapping.
- **License:** GPL (Blender built-in). **Headless:** Yes, fully scriptable.
- **Why it ranks this high for CJ:** It decouples "mesh quality" from "weight quality" permanently — every future mesh edit re-inherits good weights. It is also how BlenRig is designed to work (cage carries weights; hero mesh follows via Mesh Deform, weights optionally baked back by transfer).
- **Limits:** Nearest-face transfer smears across thin gaps (inner arm ↔ torso at the armpit is the classic artefact) — mask the shoulder region and hand-check it (§5).

### B4. libigl Bounded Biharmonic Weights (BBW) + fTetWild — RANK 3, gold standard, build-a-tool ★
- **What it does:** The academic gold standard for automatic weights (Jacobson et al. 2011): minimise Laplacian (biharmonic) energy per bone subject to 0 ≤ w ≤ 1, partition-of-unity, and handle-interpolation constraints — a QP solved by libigl's active-set solver. Produces exceptionally smooth, local, artefact-free shoulder gradients *on a tetrahedralisation of the volume*.
- **License — read carefully, this is the trap cluster:**
  - **libigl core: MPL-2.0** (per-file MPL headers; some optional components differ).
  - **TetGen (libigl's default tetrahedraliser): AGPL-3.0 / commercial** — linking it contaminates distribution. Multiple 2026 implementers refused BBW for exactly this reason.
  - **MOSEK (optional fast QP solver): commercial — do not use;** libigl's built-in active-set solver is the free path.
  - **Cork** (mentioned in the brief): Cork is libigl's *boolean* library dependency, not the BBW solver — it is not what tetrahedralises or solves BBW. Flagging the conflation so no lane goes hunting for "Cork skinning."
  - **Clean path: fTetWild / PyTetWild — MPL-2.0**, robust tetrahedralisation that *accepts imperfect, non-manifold, self-intersecting input* ("triangle soups → tet mesh") — which is precisely this character's problem. Python wheels exist for Linux: https://pypi.org/project/pytetwild/0.2.0/ · BBW tutorial: https://libigl.github.io/tutorial/ (ch. 403, Bounded Biharmonic Weights)
- **Headless Linux:** Yes — C++ (header-heavy libigl) or Python (`pyigl` + `pytetwild`), all CLI. This is a *pipeline tool the lane builds once* (mesh + bone segments → tet mesh → BBW → write vertex groups via `bpy`), not an add-on.
- **Verdict:** Highest-quality weights obtainable free, highest integration cost. Justify it only if B1+B3 still leave a bad shoulder after correctives — or build it as the standing re-rig tool for all future characters, in which case it pays for itself.

### B5. Geodesic Voxel Binding (GVB) — METHOD, reimplement (no clean open code)
- **What it is:** Maya's production smooth-bind method (also the first engine in the new standalone "Armature" tool): voxelise the body, measure distance **through the voxelised volume, not through the air**, bind by geodesic falloff. This is why Mixamo/Maya-class binds don't leak weights across the armpit or between touching limbs — Euclidean/closest-point binds do, structurally, and "no tuning fixes" it (analysis: https://github.com/fernandotonon/qtmesheditor/issues/819).
- **Open-code status — flagged honestly:** a 2026 architecture review states the robust methods (GVB; 2024 Robust Biharmonic Geometric Fields) "have no usable open code and would need clean-room reimplementation" — https://github.com/davidbayus/hiho-software/blob/HEAD/HIHO_MOCAP/HIHO_MOCAP_WRAPPER_ARCHITECTURE.md
- **Reproduction recipe (all free parts):** voxelise with Blender/OpenVDB or numpy occupancy grid at ~92–128³ (adaptive/octree refinement for fingers is a 2026 WIP in the community, not a product) → Dijkstra/fast-marching distance from each bone segment *through interior voxels only* → weight = falloff(geodesic distance), top-4, normalise → write vertex groups. CharForge's open pipeline uses exactly this idea for the same reason: "distance measured through the voxelised body rather than through the air — so a vest glued to an arm is not near the arm's bone" (https://majieddd.github.io/charforge/paper/). This *is* the Voxel Heat Diffuse method, generalised — B1's paid sibling is a productised cousin.
- **Verdict:** The right *second-generation* tool if the lane builds one thing: build GVB, not a BBW clone — it tolerates the raw mesh, BBW needs the tet step first.

### B6. Dem Bones (EA SEED) + py-dem-bones — RANK 4, special-purpose solver ★
- **What it does:** Smooth Skinning Decomposition with Rigid Bones (SSDR, Le & Deng 2012; Dem Bones, Le & Lewis 2019): given **example poses** (an animated mesh sequence, or a set of sculpted ROM poses / blendshapes), it *solves for* sparse non-negative affine skinning weights + rigid bone transforms that reproduce those poses. Also: auto joint generation, converting blendshapes → LBS, and solving bone transforms when weights are known.
- **License:** **BSD-3-Clause** (core, EA) — clean and permissive. Python bindings: `py-dem-bones` on PyPI (BSD-3, host-independent numpy API, with a documented Blender adapter for sampling/writing weights): https://pypi.org/project/py-dem-bones/ · core: https://www.ea.com/technology/news/open-source-dem-bones (links the `electronicarts/dem-bones` GitHub repo) · Godot port (same algorithm, useful reference): https://github.com/V-Sekai/godot-dem-bones
- **Headless Linux:** Yes — header-only C++ core (Eigen + OpenMP) with a CLI, and the Python package is pip-installable. No Maya required (the Maya bindings are a separate, MIT, wrapper: https://github.com/robertjoosten/maya-dem-bones).
- **What it does NOT do:** It is **not a static-mesh binder**. With no example poses it has nothing to solve from. ⚠️ Do not schedule it as the primary re-bind.
- **Where it *is* the winner for CJ:** the dance lane *has* poses. Feed it the choreography's extreme shoulder poses (sculpted/corrected to look right) and let it solve weights that reproduce *those* deformations — i.e. bake artistic intent into weights. Also the correct tool for converting any sculpted corrective poses into a Dem-Bones/delta-mush-style compressed skinning set.
- **Maintenance:** EA's repo is a finished research release (2019–2021 era, stable, not a living product); `py-dem-bones` is actively versioned (0.13.x on PyPI at crawl time). Flag: *stable/finished*, not abandonware — the algorithm doesn't expire — but expect no upstream feature work.

### B7. Neural skin heads (UniRig skin / MIA weights / SkinTokens) — RANK 5
Covered in §A3/A4/A8. Their weights are learned from thousands of animator rigs and are often *better than bone-heat at shoulders on first pass*, but they arrive attached to their own skeleton/vertex sampling and must be transferred (B3) and cleaned (B2 post-passes) before use on the hero mesh. Treat as candidate weight *sources*, never as final weights.

### B8. Harmonic weights (plain, unbounded) — note only
`igl::harmonic` with k=1/k=2 and Blender's heat are the unbounded ancestors of BBW: smooth, but weights can go negative/overshoot and lack locality without BBW's bound constraints. No reason to choose plain harmonic over B1/B2/B4 in 2026. (libigl tutorial ch. 401–403, URL in §B4.)

---

## (c) DEFORMATION CORRECTIVES — ranked shortlist

### C1. Blender built-ins, used in the right order — RANK 1 ★
All GPL/bundled, all headless-scriptable, all already in Blender 5.2.3:
1. **Armature modifier ▸ Preserve Volume = dual-quaternion skinning (DQS).** Blends rotations as rotations; the standard fix for candy-wrapper twist and joint collapse. ⚠️ Travel warning: most game engines and the glTF skinning path are LBS-only — DQS looks right in Blender and *different* after export. Use it for Blender-rendered dance proof; for exported targets, bake its benefit into twist bones + PSD keys (C2/C3) instead.
2. **Corrective Smooth modifier (= Blender's Delta-Mush-family smoother).** Relaxes only the *deformation delta* against the rest state, preserving detail. Manual: https://docs.blender.org/manual/ar/4.3/modeling/modifiers/deform/corrective_smooth.html — Settings that matter here: place it **after** Armature, `Smooth Type = Length Weight`, Factor ~0.5, Iterations 5–10, **restrict with a painted vertex group to shoulder/upper-arm only**, Pin Boundaries on open edges, set `Scale` for the 0.925 m character, use Bind Coordinates if Subsurf/Mirror sit before it.
3. **B-Bones (bendable bones) with custom in/out handles** for spine/upper-arm segments — cheap curvature distribution before any corrective is authored.
4. **Mesh Deform (the BlenRig cage)** — see §A5/C4.
- **Verdict:** This stack, *masked and ordered correctly*, is 80% of the shoulder fix. Every fancier system below either feeds it or bakes it.

### C2. Sculpted pose-space deformation (PSD) corrective shape keys + drivers — RANK 2 ★ (the industry-standard answer)
- **What it is:** Pose the arm into the broken configuration (e.g. upper-arm raised 120°, rotated forward), sculpt the shoulder/bicep back to the correct volume/silhouette as a shape key, drive that key from the bone's rotation. One key per problem pose per joint; combinations handled by C3.
- **Free tooling:** Pure Blender (shape keys + driver expressions / Action Constraints via CloudRig's Actions system: https://projects.blender.org/Mets/CloudRig/wiki/Actions — cited from CloudRig's own docs) plus **Pose Shape Keys**, Blender Studio's free extension for storing/re-applying sculpted correctives across weight/rig changes: http://extensions.blender.org/add-ons/pose-shape-keys/
- **Headless Linux:** Authoring is sculpting (interactive), *application is data* — keys + drivers evaluate headless and export as blendshapes, unlike add-on-dependent solvers. This exportability is why PSD ranks above RBF-as-a-live-solver.
- **Authoring discipline:** Sculpt correctives only *after* weights pass §5's ROM test; keep topology unchanged; one deformation region per key (mask vertex groups per joint, Pose Shape Keys supports this); mirror with symmetry tooling rather than sculpting twice.

### C3. RBF interpolation over PSD poses — RANK 3 as a *live solver*, RANK 1 as a *method to reproduce*
- **What it is:** Single-axis drivers fail on ball joints: a shoulder corrective depends on (swing X, swing Z, twist) simultaneously. Radial Basis Functions interpolate smoothly between *multiple recorded poses* in that multi-dimensional pose space — the studio-standard solution for shoulders/hips/face.
- **Commercial reference (methods only):** brave rabbit's **RBF Nodes** ("Drive correctives for shoulders, hips and other complex bones from their rotation… define inputs, outputs, set a few poses, the solver interpolates", Wendland kernel default) and **SHAPES** (create/edit correctives in the deformed pose; note SHAPES is sold on a trust-based licence *stated as GNU GPL* on its store page, with a **free RBF Nodes runtime** for playback — but the authoring tools are paid products; do not treat the store page as a free download): https://superhivemarket.com/products/rbf-nodes?search_id=50471078 · https://superhivemarket.com/products/shapes--shape-key-editor?search_id=50479130
- **Free reproduction (recommended):** RBF interpolation is textbook math, not a product secret. Implement in pure Python: record N shoulder poses → feature vector = upper-arm + clavicle quaternion/axis-angle components → solve Wendland-RBF weights (numpy/scipy `RBFInterpolator` in a Kaggle/Colab or local venv, *outside* Blender's bundled Python if scipy is absent) → **bake the result back to native Blender**: either (a) per-frame driver *expressions* are too weak — instead (b) sample the RBF on a grid and fit ordinary shape-key drivers, or (c) ship a tiny GPL Python driver handler in the .blend. Baking (b) keeps the rig add-on-free and exportable.
- **Also reproducible from a paid product's public docs — JointForge method:** bake Corrective Smooth (Delta Mush) into per-joint corrective shape keys sampled every ~30° of each joint's used range, driven by bone rotation, validated frame-by-frame against the Delta Mush reference: https://superhivemarket.com/products/jointforge/docs — the *method* (sample → bake → drive → measure) is fully described in its public documentation and reimplementable with C1+C2 alone; the product itself is paid, do not pull it.
- **Verdict:** Build the tiny RBF baker once; it is the difference between "shoulder fixed in the test pose" and "shoulder fixed across the whole dance."

### C4. BlenRig cage + lattices + auto shape keys — RANK 3 (tied)
BlenRig (§A5) already generates corrective shape keys + drivers automatically for its joints and provides muscle-bulge/lattice layers and a sculpt-shapekeys workflow on top of the cage. If the lane keeps the BlenRig cage in the CJ rig (per brief), authoring shoulder correctives *in BlenRig's system* is less new tooling than bolting PSD onto the custom rig. Cost: BlenRig's conventions own the rig — mixing BlenRig correctives with CloudRig generation on the same bones needs a deliberate decision, not an accident. **Recommendation: pick ONE corrective home — native PSD/RBF (C2+C3) on the CloudRig rig — and use BlenRig only as the cage/transfer source (B3), unless the existing CJ file is already BlenRig-driven end-to-end.**

### C5. Helper / twist / bulge bones (constraint-driven correctives) — RANK 2 (tied, do with C2)
The cheapest correctives are bones, not shapes: (1) **upper-arm twist bone(s)** taking 50%→0% of forearm twist along the arm (AccuRIG method, §A9); (2) **clavicle/shoulder helper** that counter-rotates/translates with upper-arm elevation to keep the deltoid volume (Auto-Rig Pro / CloudRig limb components do this with drivers/Action Constraints); (3) **bicep bulge bone** scaled/translated by elbow flexion via a simple driver, weighted to the bicep belly. All native Blender, all headless, all export as ordinary bones+weights. For a *stylised* 0.925 m hero this trio plus good weights may make sculpted PSD unnecessary except at extreme dance poses — test before sculpting.

### C6. Research-only correctives — flagged, do not schedule
- **Neural Blend Shapes / learned PSD** (pose-conditioned corrective shapes inferred by a network): strong papers, no maintained Blender-integrated open release verified in this sweep.
- **Delta-mush skinning compression (Dem Bones' second act):** real and BSD-licensed via §B6, but it is a *runtime representation* project, not a Blender viewport fix.
- **GN Rigging System** (Geometry-Nodes LBS+DQS+Delta Mush, Superhive): interesting, paid-store product — methods reference only: https://superhivemarket.com/products/gn-rigging-system?search_id=50476004

---

## 5. Concrete recipe A — the shoulder/bicep fix (do in this order; stop when the ROM test passes)

**ROM test (define "fixed" before touching anything):** scripted headless pose sweep of the existing dance's shoulder range — upper-arm elevation −30°…+170°, horizontal adduction/abduction, axial twist ±90°, elbow flexion 0…140° — rendered from 3 fixed cameras at each extreme. A pose passes if: no self-intersection at the armpit, deltoid silhouette stays convex, bicep keeps ≥ ~80% rest volume (eyeball against reference stills), no single-vertex-group (hard-edged) crease. Keep these renders as the before/after proof pair.

1. **Freeze the good parts.** Duplicate the .blend; lock the working 94-bone rig as the reference. All work below is on deform bones only — never on IK/FK control bones (they must have Deform OFF during any bind, or they steal weights).
2. **Clean a binding copy of the mesh:** apply transforms → Merge by Distance → Degenerate Dissolve → Delete Loose → fix Non-Manifold selection → recalc normals. Split by loose parts; note every island (islands are bound separately or via the cage, step 3b). Temporarily scale mesh+armature ×10 if bone-heat errors persist at 0.925 m scale.
3. **Re-bind weights, two candidate paths, keep both:**
   - **3a.** Surface Heat Diffuse (B1, after its Blender-5.2 smoke test) or, if the add-on fails on 5.2, built-in bone-heat (B2) on the cleaned copy.
   - **3b.** Cage path: bone-heat the BlenRig cage / a decimated proxy (it will succeed — it's simple and manifold), Data Transfer (Projected Face Interpolated) onto the hero mesh (B3). Mask + hand-inspect the armpit/shoulder transfer zone.
   - Run B2 post-passes on both (Clean → Limit 4 → Normalize → Smooth shoulder bones only). A/B them in the ROM test; keep the winner per region if necessary (weights are per-vertex-group data — mixing sources by region is legitimate).
4. **Fix joint placement before painting anything:** clavicle head at the sternum pivot, clavicle tail at the true shoulder point; upper-arm head *inside* the deltoid volume, slightly below the acromion line, never above the silhouette. Re-check bone roll so the upper-arm's local axes match the dance's main swing plane. (Placement errors cannot be painted away — §1, cause #2.)
5. **Add the arm helper set (C5):** 1 upper-arm twist bone (50% twist share), 1 forearm twist bone, shoulder-helper driven by upper-arm elevation, bicep-bulge bone driven by elbow flexion. Weight them by copying/blur from the parent bone's group, then Limit/Normalize again.
6. **Armature Preserve Volume ON** for Blender-side evaluation; re-run ROM. Note any pose that only passes *because* of DQS if the final target is an LBS runtime — those poses go on the PSD list regardless.
7. **Corrective Smooth, masked** (C1.2) on shoulder+upper arm only. Re-run ROM. If a pose still collapses, it is a PSD pose, not a "more smoothing" pose.
8. **Sculpt PSD correctives (C2)** for the failing extremes (typically: arm fully raised — deltoid flattening; arm across body — armpit pinch; elbow fully flexed — bicep/tricep intersection). Drive single-axis keys with drivers; drive *combination* poses (raise+twist) through the reproduced RBF baker (C3), baked back to native drivers.
9. **Optional Dem Bones pass (B6):** if sculpted ROM poses exist as meshes, solve a weight set from them and compare against step 3's winner in the ROM test. Keep whichever wins; record the other as the fallback.
10. **Lock it:** Pose Shape Keys-style external storage of the sculpted correctives (so a future weight change doesn't destroy them), ROM renders filed as proof, weight stats logged (max influences, unweighted vertex count = 0, per-group totals).

## 6. Concrete recipe B — full-body standing re-rig (when a from-scratch rig is actually wanted)

1. **Landmarks first (Mixamo/ARP method, reproduced):** establish the landmark set on the mesh — the Mixamo five (chin, wrists, elbows, knees, groin) extended with ankles, shoulder points, hip points, spine levels, neck base. Source them from (in priority order) the existing rig's joint positions, a UniRig run (§A3), an MIA run (§A4). Human-verify the shoulder/hip landmarks — every downstream error starts here.
2. **Generate the control rig with CloudRig** (§A1) from a metarig placed at those landmarks (Rigify conventions, §A2). Regenerable > hand-built: proportion changes become re-generation, not re-rigging.
3. **Skin with §5 steps 2–3** (clean → Surface Heat/bone-heat or cage transfer → post-passes). For a *standing production tool* reused across characters, this is the moment the GVB reimplementation (§B5) or BBW+fTetWild tool (§B4) earns its build cost — pick GVB for messy meshes, BBW for clean ones.
4. **Helper bones + masked Corrective Smooth + PSD/RBF correctives** (§5 steps 5–8) for shoulders, hips, elbows, knees — in that priority order.
5. **Acceptance = full ROM suite + one real dance clip retargeted and rendered**, not a T-pose screenshot. (Per standing owner law: no fighter/character is proof before its pipeline is finished and shown in motion.)

## 7. Headless-Linux feasibility summary

| System | Headless Linux? | GPU needed? | Blender 5.2.3 fit |
|---|---|---|---|
| CloudRig / Rigify / BlenRig (generation) | ✅ `bpy` scripted | No | CloudRig current (Extensions platform, 2.2.x, generation speedups landing for 5.3); BlenRig 6 targets Blender 4.x-era — verify on 5.2 in a smoke test |
| Blender bone-heat / Data Transfer / Corrective Smooth / PSD | ✅ built-in | No | Native |
| Surface Heat Diffuse (MIT) | ⚠️ source build / port likely needed | No | ❓ shipped builds predate 5.2 — smoke-test first (B1) |
| UniRig | ✅ CLI | Practically yes | External — FBX in/out |
| Make-It-Animatable | ✅ CLI | Yes | External — Mixamo-topology FBX out |
| Dem Bones / py-dem-bones | ✅ CLI / pip | No (CPU, OpenMP) | Via its Blender adapter / custom `bpy` writer |
| libigl BBW + fTetWild | ✅ C++/Python tool to build | No | External — weights imported as vertex groups |
| GVB reimplementation | ✅ once built (numpy/OpenVDB) | No (GPU optional) | External — same import path |
| Pinocchio (original code) | ⚠️ builds, unmaintained | No | Not integrated — method only |
| RigNet | ⚠️ legacy CUDA stack | Yes | ⛔ Do not integrate |
| Auto-Rig Pro / Mixamo / AccuRIG | ❌ GUI/modal/account | — | Methods only (A9) |

## 8. Licence trap table (the short version every lane should pin)

| Trap | Reality |
|---|---|
| RigNet "open source" | GPL-3.0 **or paid commercial** (UMass). Plus abandonware-grade deps. |
| Pinocchio "MIT" | Only the demo. Library is **LGPL-2.1+**. Algorithm is free to reimplement; code is not free to vendor statically. |
| libigl "free BBW" | Core MPL-2.0 ✅, but default tet path **TetGen = AGPL** and fast QP path **MOSEK = commercial**. Use fTetWild (MPL-2.0) + active-set solver. |
| Voxel Heat Diffuse "has a free version" | The free sibling is **Surface** Heat (MIT). The **Voxel** product itself is paid (~$30). Reproduce the voxel method (§B5) instead of pulling the product. |
| SHAPES "GPL" | Store page states GPL + trust-based paid licences; authoring tool is a paid product, runtime is free. Methods only; reproduce RBF (§C3). |
| MIA "Apache-2.0" | Conflicting CC-BY-NC-4.0 signal on HF. **Unresolved** — internal/research use until the repo LICENSE is read. |
| UniRig "MIT" | Code MIT ✅; **checkpoint licence is a separate check** on the HF model card. |
| Mixamo / AccuRIG "free" | Free of charge ≠ automatable: account/upload/GUI-walled. Methods only, per task rules. |
| Blender add-ons generally | GPL-family — fine to *use* headless in-pipeline; redistribution of the add-on code itself carries GPL duties. The *rigs/weights they produce* are your data. |

## 9. Honest flags — abandonware / research-code / unverified

- **RigNet:** superseded + GPL + legacy deps → abandonware for new work (§A7).
- **Pinocchio original code:** 2007, unmaintained as a product; algorithm alive everywhere (§A6).
- **Surface Heat Diffuse package:** algorithm current-best for the failure mode, *package* stale (2022 prebuilds; Blender ≤3.3/4.1-era support claims) — porting risk is real and budgeted in §5 step 3a (§B1).
- **Dem Bones upstream:** finished research release, stable not dead; active maintenance lives in the bindings (`py-dem-bones`) (§B6).
- **MagicArticulate / Puppeteer / SkinTokens / HumanRig / Anymate:** research code, varying licences/GPU demands; none verified as a maintained Blender-integrated product in this sweep (§A8).
- **Adaptive-voxel GPU skinning (Jessy Leite, 2026):** promising WIP announced for beta testing on Blender Artists (https://blenderartists.org/t/wip-a-new-adaptive-voxel-auto-skinning-weights-method-looking-for-beta-testers/1643862) — not a released open tool at research time; watch, don't depend.
- **CloudRig exact licence file** and **BlenRig 6 on Blender 5.2.3**: to be confirmed in-tree / by smoke test in the lane's first session — flagged here rather than asserted.

## 10. Primary sources (all URLs copied verbatim from 2026-11-02 search results)

- UniRig repo: https://github.com/VAST-AI-Research/UniRig/tree/3241154cd5cdd56a81f0e32a1e73db7f2d22cc8b
- 2026 auto-rig landscape survey (UniRig/MIA/RigNet/ARP/Rigify/Mixamo/AccuRIG, headless notes): https://github.com/newsbubbles/riggs/blob/HEAD/notes/01-landscape.md
- ML rigger port survey (RigNet GPL, SkinTokens, Puppeteer, RigAnything NC): https://github.com/zeljkovranjes/auto-rigger/blob/HEAD/README.md
- RigNet project page (GPL/commercial licence statement): http://zhan-xu.github.io/rig-net/
- Make-It-Animatable repo: https://github.com/jasongzy/Make-It-Animatable · paper: https://openaccess.thecvf.com/content/CVPR2025/html/Guo_Make-It-Animatable_An_Efficient_Framework_for_Authoring_Animation-Ready_3D_Characters_CVPR_2025_paper.html
- CloudRig extension: https://extensions.blender.org/add-ons/cloudrig/ · intro: https://studio.blender.org/tools/addons/cloudrig/introduction · types: https://studio.blender.org/tools/addons/cloudrig/cloudrig-types
- 2026 Blender rigging add-on survey (ARP vs Rigify/CloudRig vs BlenRig): https://www.strayspark.studio/blog/best-blender-rigging-addons-2026
- BlenRig GPL release: https://studio.blender.org/blog/blenrig-blenrig-public-release/
- Pinocchio LGPL analysis / clean reimplementation: https://github.com/fernandotonon/qtmesheditor/issues/407 · https://github.com/fernandotonon/QtMeshEditor/pull/754
- Bone-heat failure triage (46-character test, non-manifold/island causes): https://jessyleite.dev/posts/blender-bone-heat-weighting-failed/
- Weight-painting problem/fix guide (voxel vs surface heat, post-passes): https://app.cinevva.com/guides/blender-weight-painting-problems
- Surface Heat Diffuse Skinning (MIT): https://github.com/meshonline/Surface-Heat-Diffuse-Skinning · Voxel product (reference): https://www.mesh-online.net/voxel.html
- Dem Bones (EA, BSD-3): https://www.ea.com/technology/news/open-source-dem-bones · Python bindings: https://pypi.org/project/py-dem-bones/ · Maya wrapper (MIT): https://github.com/robertjoosten/maya-dem-bones · Godot port: https://github.com/V-Sekai/godot-dem-bones
- libigl tutorial (BBW ch. 403, DQS ch. 404): https://libigl.github.io/tutorial/ · BBW/GVB production analysis: https://github.com/fernandotonon/qtmesheditor/issues/819 · GVB open-code status: https://github.com/davidbayus/hiho-software/blob/HEAD/HIHO_MOCAP/HIHO_MOCAP_WRAPPER_ARCHITECTURE.md
- fTetWild Python (MPL-2.0): https://pypi.org/project/pytetwild/0.2.0/
- Corrective Smooth manual: https://docs.blender.org/manual/ar/4.3/modeling/modifiers/deform/corrective_smooth.html
- Shoulder deformation practice (placement, cage+transfer, corrective-smooth discipline): https://blenderartists.org/t/can-i-achieve-a-better-deformation-of-the-mesh/1266339
- Skinning technique comparison (LBS/DQS/PSD, candy-wrapper): https://game-ace.com/blog/game-character-skinning/
- RBF Nodes (method reference): https://superhivemarket.com/products/rbf-nodes?search_id=50471078 · SHAPES: https://superhivemarket.com/products/shapes--shape-key-editor?search_id=50479130 · JointForge bake method: https://superhivemarket.com/products/jointforge/docs
- Pose Shape Keys extension (Blender Studio): http://extensions.blender.org/add-ons/pose-shape-keys/
- AccuRIG published methods (twist segments, partitioned volume weights): https://www.reallusion.com/auto-rig/accurig/
- Mixamo marker method: https://www.tripo3d.ai/blog/rig-ai-generated-character-for-mixamo
- CharForge living paper (GVB rationale, learned-rigging status): https://majieddd.github.io/charforge/paper/

*End of research report. Companion lane decisions (which corrective home, whether to build GVB/BBW) are flagged inline at §B4/B5 and §C4 — they are the two genuine forks; everything else in §5/§6 is sequenced and ready to execute.*

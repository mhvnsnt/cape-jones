# Rigging Stack 2026 — research, pulls, and rejections

**Date:** 2026-10-16 · **Lane:** rig/cape-jones-fullstack-20261016 · **Character:** Cape Jones (Tripo AI mesh, 991k verts, native 0.925 m, Blender 4.0.2)

## What we already had (own rigging study material — read first)

| Source | What it gave this rig |
|---|---|
| `bannon-video-pipe/docs/AI_RIGGING_RESEARCH.md` (2026-10-09) | Measured failure it fixed: auto-weighted shoulders web/tear past ~15° arm raise. Adopted: Armature modifier **Preserve Volume** (true dual-quaternion skinning), **Corrective Smooth** masked to problem zones, **corrective shape keys driven by bone rotation** (only corrective that survives GLB export as morph targets), **twist-bone recipe**, Pose Shape Keys addon pointer. Its "explicitly NOT recommended" list (paid tools) was honored. |
| `api-catalog/raw/01-3d-mesh-rigging.md` (2026-10-06) | Tooling landscape: Blender headless, trimesh, Pinocchio (LGPL-2.1), RigNet (GPL-3.0), Mixamo, AccuRig 2.0, Rigify ("best for new characters"), Blender built-in weight tools (Weight Paint brushes, Normalize All, Mirror, Data Transfer). License flags reused. |
| `brutalfist-fix/docs/ANIMATION_RIG_PIPELINE.md` + `tools/animation/auto_rig_humanoid.py` | Prior auto-rig conventions; informed the FK/IK + pole-target architecture. |
| `tools/open-toon/docs/implementation/HM01-RIG-PROPERTIES.md`, `HM03-RIG-FOUNDATION.md` | Rig property/foundation conventions. |
| `tools/wmxix-mesh-decode/yukes-extractors/tekken57-blender-scripts/export_bone_weights_*.py` | Real shipped-game bone-weight exports (WWE/Tekken) — reference for how production weights distribute across 4 influences max, hard locks on hands/feet/head. |
| `god-molecule-studio/tools/puppet/wizard-rig-proof/RIG_PROOF*.md` | Prior rig proof/verification format — basis for the pose-test verification contract used here. |

## 2026 open-source stack (real sources, checked 2026-10-16)

**Rigify (GPL, bundled with Blender 4.0.2).** Still the free production standard in 2026
([strayspark.studio 2026 guide](https://www.strayspark.studio/blog/how-to-rig-a-character-in-blender-2026),
[animalanimator.com Aug 2026](https://animalanimator.com/blender-rigify-for-rigging-animals-and-making-epic-animations/),
[roble3/cc-blender-skill](https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/10-rigging/00-overview.md)).
Generates full FK/IK control rig from a fitted meta-rig. **Decision: not used for this character.**
Why: the task spec demands clean custom naming (no ORG-/DEF-/MCH- prefix soup), a cape bone-chain,
weapon attachment bones, and exact stretch/no-stretch zone control. Fitting Rigify's meta-rig needs the
same measured joint detection as building the custom rig, and the generator adds ~160 deform bones the
animator never touches (the elithril/blender-kiln measurement: 107 of 160 deform bones influencing nothing
on a mismatched mesh). Custom two-layer FK/IK rig chosen instead; documented in RIG-DOCS.md.

**Pose Shape Keys (Blender Studio, Demeter Dzadik, free).**
The corrective-shape-key authoring accelerator our own research recommends
([extensions.blender.org](http://extensions.blender.org/add-ons/pose-shape-keys/),
[studio.blender.org training](https://studio.blender.org/training/blender-studio-rigging-tools/pose-shape-keys/)).
**Decision: evaluated, deferred.** It ships as a 4.2+ extension; this pipeline is Blender 4.0.2
(no extensions platform). Corrective shape keys are authored here with built-in tools + the repo's own
`tools/rigging/corrective_builder.py` instead. Revisit on Blender upgrade.

**Adaptive Auto Skinning (Jessy Leite, covered 80.lv 2026-09-23).**
Voxel-based one-click GPU skinning; 80.9% dominant-bone match vs artist reference on a 202-character
benchmark — best automatic method tested. **Decision: rejected for this pipeline.** Requires Blender 4.2–5.2;
we are on 4.0.2. Noted for the upgrade path.

**Voxel Heat Diffuse Skinning ($30 paid).** Better auto-weights than Blender heat, handles messy/overlapping
geometry. **Decision: rejected** — paid (our standing policy from AI_RIGGING_RESEARCH: paid rigging tools
not recommended), and unnecessary: the procedural zone painter gives exact stretch/no-stretch control.

**BlenRig 6 (free, film-pedigree auto-rig).** Full body + facial rig generator.
**Decision: rejected for this character** — its generated rig structure doesn't match the required bone
layout/naming, and guided proportion-fitting is still manual work comparable to our measured joint detection.

**Pinocchio (LGPL-2.1, Baran & Popović 2007 — the Mixamo ancestor).** Template skeleton fitting + heat
diffusion, CPU, <1 min/character. **Decision: rejected** — old research code, needs build/integration work,
and template-fitting fights the custom bone layout. Kept on the watch list for background-character batches.

**RigNet (GPL-3.0, neural rigging).** Predicts joints + skinning from mesh. **Decision: rejected** —
research-only maturity, needs rest-pose input, struggles off-standard proportions, GPL-3.0.

**Mixamo (Adobe, free w/ account) / AccuRig 2.0 (Reallusion, free).** Production-quality auto-riggers.
**Decision: rejected as primary** — browser-only/manual (Mixamo), Windows-only GUI (AccuRig); neither is
scriptable in our headless Linux pipeline, and neither produces the required custom rig. Kept as animation
*clip* sources (retarget path documented in AI_RIGGING_RESEARCH).

## What was pulled in (wired into this repo, `tools/rigging/`)

All own-code, license-clean, tested on Blender 4.0.2 headless:

| Tool | What it does |
|---|---|
| `build_rig.py` | Imports the Tripo GLB (plain, meshopt-transcoded), builds the 54-bone animator rig from measured joints, FK/IK switches with drivers, pole targets, bendy-bone segments, DQ Preserve Volume + masked Corrective Smooth. |
| `weight_zones.py` | Procedural weight painter: numpy zone engine implementing the stretch/no-stretch map (elbows/knees/shoulders/hips/waist = gradient zones; hands/feet/head/chest-plate = hard locks), cape grid weights, corrective-smooth mask, 4-influence limit. |
| `pose_test.py` | 7-pose verification suite (T-pose, arms-raised, elbow 100°, knee 100°, shoulder raise, head turn, crouch) with world-space rotation posing + Cycles clay renders. |
| `joint_detect.py` | Cross-section slice analysis that measured every joint position from the mesh (no eyeballed pivots). |
| `corrective_builder.py` | Driven corrective-shape-key builder (pose → sculpt delta → bone-rotation driver). Used if pose tests show residual pinching. |
| `README.md` | What each tool is, how to run it, Blender version requirements. |

## Rejected, honestly

- Paid tools (Auto-Rig Pro, Voxel Heat Diffuse Skinning, Weight Paint Tools): license/cost policy, and the procedural painter already beats them on zone control.
- Cloth sim for the cape: non-deterministic, bake management, can't hit held gag poses — bone chain chosen (the cape is a body gag; art-directability wins). Documented in RIG-DOCS.md.
- Separate twist bones: folded into bendy-bone segments (3 per long limb bone) + dual-quaternion skinning, which distribute twist without extra mechanism bones. The AAA twist-bone recipe from our research remains available if twist tests ever fail.
- Rigify generator: spec mismatch (naming, cape chain, weapon bones), dead-bone overhead.
- 4.2+-only tools (Pose Shape Keys extension, Adaptive Auto Skinning, BVH Motion Retargeter): Blender version wall; revisit on upgrade.

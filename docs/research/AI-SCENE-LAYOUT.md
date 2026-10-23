# AI Scene Layout Research — smart 3D interior arrangement, no guesswork

**Date:** 2026-10-16 · **Researcher:** subagent (deep research lane) · **Trigger:** owner order — our living-room scene shipped with furniture randomly placed; get real research on AI layout systems, real repos, real licenses.

**Bottom line first:** every neural layout generator we verified invents layouts from scratch. We don't need invention — the owner already drew the layout target (the 2D living-room reference). So the winning pipeline is NOT a generative model. It is: **reference anchors + interior-design rule/constraint engine + deterministic Blender placement + render-verify loop**. That is the only stack that respects his drawing as the ground truth. Details in §6.

---

## 1. Neural / AI 3D interior layout systems

| System | What it is | Input → Output | Open in 2026? | Free-compute viable? | Verdict |
|---|---|---|---|---|---|
| **LayoutGPT** ([UCSB-AI/LayoutGPT](https://github.com/UCSB-AI/LayoutGPT)) | LLM (GPT-4) + in-context exemplars from ATISS data for 3D-FRONT rooms | room type + dims → furniture positions/sizes/rotations (22 categories) | Code open; needs OpenAI key | ❌ needs GPT-4, repo inactive ~1yr | **Skip.** Key-gated, stale, and generates *invented* layouts, not reference-matching. |
| **ATISS** ([nv-tlabs/ATISS](https://github.com/nv-tlabs/ATISS)) | Autoregressive transformer, NeurIPS 2021. The classic learned layout model. | room polygon → autoregressively adds furniture (category, center, size, rotation) | ✅ open, pretrained models exist; community fork [alex1099000/atiss](https://github.com/alex1099000/atiss) adds a production `infer.py` JSON API + ONNX/TensorRT export | ✅ could run on Kaggle GPU | **Document-only.** Samples plausible rooms from learned distribution — cannot reproduce the owner's specific drawing. |
| **SceneFormer** ([cy94/sceneformer](https://github.com/cy94/sceneformer)) | Transformer sequence generator, 3DV 2021 | seed → indoor scene object sequence | ✅ code open BUT dead: SUNCG dataset pulled, only partial "shape conditioned" release, untouched ~5yrs | ❌ cannot train/test properly | **Skip.** Abandoned. |
| **DiffuScene** ([tangjiapeng/DiffuScene](https://github.com/tangjiapeng/DiffuScene)) | Denoising diffusion for indoor scenes, CVPR 2024; supports unconditional gen, text-prompted, and *scene rearrangement* | text/partial scene → full layout (bbox + retrieved 3D-FUTURE meshes) | ✅ open, pretrained models on Google Drive | ⚠️ GPU + heavy deps; 3D-FRONT/3D-FUTURE are non-commercial licensed | **Document-only.** Rearrangement mode is the interesting idea (tidy messy rooms), but it rearranges toward *learned norms*, not toward the owner's drawing; license-poisoned datasets. |
| **LEGO-Net** ([QiuhongAnnaWei/LEGO-Net](https://github.com/QiuhongAnnaWei/LEGO-Net)) | CVPR 2023: learns "canonical arrangements" — tidies perturbed rooms | noisy layout → regularized layout | ✅ open; needs 3D-FRONT data (Drive) | ⚠️ training-heavy | **Document-only.** Concept applies (denoise bad placements), but trained norms ≠ owner's art direction. |
| **InstructScene** ([chenguolin/InstructScene](https://github.com/chenguolin/InstructScene)) | ICLR 2024: instruction-driven synthesis w/ semantic graph prior | text instruction + semantic graph → 3D room | ✅ open | ⚠️ GPU, research-grade | **Document-only.** Cool direction (graph-constrained = controllable), but no production path and still invents layouts. |
| **Holodeck** ([allenai/Holodeck](https://github.com/allenai/Holodeck)) | CVPR 2024 (AI2): LLM plans floor plan + objects; placement solved by **DFS / MILP constraint solver**; assets retrieved via CLIP/SBERT over Objathor/Objaverse | text query ("a living room") → AI2-THOR scene JSON | ✅ open | ⚠️ needs OpenAI key (GPT-4o default), AI2-THOR, Unity; community forks swap in OpenAI-compatible models (e.g. DashScope/Qwen) | **Document-only, but steal the PATTERN.** The architecture is exactly right: LLM emits *spatial constraints* → deterministic solver places objects (no overlaps, inside walls). This is the technique our rule engine copies. |
| **PlanIT** ([peterzs/planit](https://github.com/peterzs/planit)) | SIGGRAPH 2019: relation-graph plan → spatial prior instantiation | relation graph → placed objects | ✅ code open; ❌ authors lost the dataset and ALL pretrained models | ❌ cannot run | **Skip.** Dead upstream. |
| **LayoutDreamer** ([arXiv:2502.01949](https://arxiv.org/abs/2502.01949)) | Physics-guided text-to-3D *compositional* generation on 3D Gaussian Splatting | text → scene graph → optimized 3DGS scene | Paper only in 2025; generation-focused | ❌ 3DGS pipeline, GPU-heavy | **Skip.** Object-level layout for Gaussian scenes, not furniture-room layout. |

**Honest aggregate:** the neural route is the wrong tool for THIS job. It solves "invent a plausible room"; we need "place THESE items WHERE HE DREW THEM, correctly spaced". Keep these citations for future original-room generation; do not burn GPU quota on them for the living room.

---

## 2. Rule-based / constraint layout (the actual answer)

Interior design has a published, stable rule corpus — it is the cheapest "AI" there is: deterministic rules a human designer would apply. Sources verified 2026-10-16 ([Coohom room-planner guide](https://www.coohom.com/article/visualizing-furniture-placement-with-a-room-planner), [Coohom floor-planner guide](https://www.coohom.com/article/floor-planner-how-to-use), [FasterCapital arrangement guide](https://fastercapital.com/topics/furniture-arrangement-and-layout-optimization.html)):

- **Walkways:** 36" (0.91 m) minimum for main paths; 30–36" around dining tables; 42" in kitchens.
- **Sofa ↔ coffee table:** 16–18" (0.40–0.46 m) gap — conversation zone.
- **TV viewing:** ~1.5–2.5× screen diagonal from seat; seating faces screen straight-on or ≤30° off-axis.
- **Focal-point anchoring:** largest seating faces the focal point (TV/window); secondary pieces angle in.
- **Zones:** group by function (viewing zone, traffic lanes); never block doorways/windows with tall furniture.
- **Rug rule:** front legs of all seating on the rug.
- **Balance:** symmetrical pairs around focal point feel orderly; don't shove everything against walls.

**What we pulled in:** these rules are now code in this repo — `tools/layout-rules/` (`layout_rules.json` + `validate_layout.py` + `apply_layout_blend.py`, see README there). The validator checks a JSON layout for: room bounds, pairwise AABB overlap, walkway clearance, sofa↔coffee-table gap, TV viewing distance/angle, door-swing clearance. It runs headless (no Blender, no GPU) so the *build lane* can iterate layouts in seconds.

**Borrowed from research:** Holodeck's constraint-solver split — *designer brain emits constraints, deterministic engine places objects*. Our "designer brain" is the owner's reference drawing + the rule corpus; the engine is `validate_layout.py` + `apply_layout_blend.py`. No LLM hallucination allowed in the placement step.

---

## 3. Blender + LLM tooling

- **ahujasid/mcp-for-blender** (community server, ~29k★, MIT, Blender 3.0+, pushed Sept 2026 — [repo](https://github.com/ahujasid/mcp-for-blender)): 36 tools — `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, **`execute_blender_code`** (arbitrary bpy), `bpy_api_lookup`, export GLB/FBX, plus Poly Haven / Sketchfab / **Poly Pizza search+download**, Hyper3D Rodin, Hunyuan3D. Core works with **any LLM** (Ollama/LM Studio/local) — only cloud asset services need keys. Verdict: **PULL IN as workflow.** It is the missing "eyes + hands" for the refinement loop: agent takes a viewport screenshot, moves a piece with bpy, re-renders, judges. Note: `BLENDER_MCP_SAFE_MODE=1` blocks file/network/process access in generated scripts; call `disable_telemetry`.
- **Official Blender MCP server** (blender.org, needs Blender 5.1+): docs lookup + scene analysis only — weaker than community. **Skip** for now.
- **Prompting pattern** (verified in community notes): inspect scene first → screenshot before AND after every change → small steps → check bounding boxes for clipping/scale. Written into our recipe in §6.

---

## 4. Procedural room builders

- **Infinigen** ([princeton-vl/infinigen](https://github.com/princeton-vl/infinigen), 3-clause BSD): full procedural world/room generator, Infinigen-Indoors furnishes rooms from procedural assets. **Verdict: document-only.** It *generates* geometry AND random layouts — the opposite of matching a reference drawing; full scene gen needs CUDA (NVIDIA-only) so our CPU VM can't run it, and it would replace the owner's art with random furniture. Borrow nothing now.
- **Archimesh** (bundled with Blender, GPL, [docs](https://docs.blender.org/manual/en/4.0/addons/add_mesh/archimesh.html)): generates rooms, doors, windows, stairs, shelves, lamps — **geometry only, zero layout intelligence**. **Verdict: PULL IN as a note, not code.** Useful later for the doorway/window geometry step (§6, step 5) — it can cut the window/door holes in the walls instead of hand-modeling them.

---

## 5. Free furniture asset sources (license-checked 2026-10-16)

| Source | License | Format | Verdict |
|---|---|---|---|
| **Quaternius** ([quaternius.com](https://quaternius.com)) | QAL v1.0 — **owner already approved 2026-10-16** | FBX/OBJ/Blend (Ultimate Furniture Pack 20 models, Ultimate Home Interior 123) | ✅ PULL IN. Already house-approved; style is low-poly cartoon — matches the show. |
| **Kenney** ([kenney.nl/assets](https://kenney.nl/assets), Furniture Kit 140 models) | **CC0** (confirmed on [kenney.nl/support](https://kenney.nl/support): "all game assets … public domain (CC0)") | OBJ/FBX/glTF (GLB included) | ✅ PULL IN. Commercial-safe, no attribution. |
| **Poly Pizza** ([poly.pizza](https://poly.pizza)) | **Per-item: CC0 or CC-BY** — NOT all CC0. Free API key. | GLB native | ✅ PULL IN with care. Check each item's license; CC-BY needs an attribution line in our docs. Directly searchable from blender-mcp. |
| **Sketchfab** ([sketchfab.com](https://sketchfab.com)) | Filter Downloadable + CC0/CC-BY/CC-BY-SA per item; free token | glTF/GLB | ✅ PULL IN with care. Same per-item license check. |
| **Poly Haven** ([polyhaven.com](https://polyhaven.com)) | CC0 | textures, models, HDRI | ✅ PULL IN. Wall/floor textures + HDRIs for the room. |
| 3D-FUTURE / 3D-FRONT / ShapeNet / OmniObject3D / Pix3D / ABO | CC-BY-NC or non-commercial / email-gated | — | ❌ Skip. Research-only or NC — owner sells things. |

---

## 6. RECOMMENDATION — the living-room re-layout pipeline

**Stack:** reference anchors (his drawing) → rule-engine validation → deterministic Blender placement → render-verify loop → owner judgment. No generative model in the critical path.

### Step-by-step recipe for the build lane

0. **Ground truth = the drawing.** Anchor list (from `~/workspace/user/files/1000174416_0_yip0.png`, owner 2026-10-16): pink loveseat (character seat — **stay EMPTY**, character goes in later for the light-flicker gag); CRT TV with rabbit-ear antenna on wooden TV stand; VCR/DVD player + boxes + green monster toy on stand shelves; purple round side table with `WORLD'S OKAYEST HERO` mug; window on right wall (trees/sky); doorway to hallway behind TV area; wall decor: `FRY EM UP` shrimp poster, purple squid hanging, framed red ghost picture. Keep approved 3D colorway (pink furniture + purple LED glow) — do NOT copy the 2D colors.
1. **Encode the layout as JSON.** For each furniture item: name, footprint (W×D×H in meters), target position + rotation, and its *anchor relation* ("side table 0.45 m left of loveseat", "TV stand against back wall, TV faces loveseat"). Write `3d-assets/living_room_layout.json` — this file is the reviewable, diffable contract.
2. **Validate headless.** Run `python tools/layout-rules/validate_layout.py 3d-assets/living_room_layout.json` — checks room bounds, pairwise AABB overlap, walkway ≥0.9 m, sofa↔table gap, TV distance/angle, door-swing clearance. Fix violations in JSON, not in Blender. Fast loop, no GPU.
3. **Apply in Blender.** Run `apply_layout_blend.py` headless: opens `3d-assets/living_room.blend`, moves ONLY the furniture objects to the validated JSON transforms, **touches nothing else** (colors, LED walls, materials stay). Then renders 3–4 viewport previews (front / top-down / hero camera).
4. **Owner-eyes check.** He judges the renders like always. If a piece looks wrong: adjust the JSON, re-validate, re-apply, re-render.
5. **Staging order (owner law):** furniture correctly FIRST. Then window + doorway (use Archimesh for clean wall holes), then wall decor (posters/squid/ghost frame as planes with the existing 2D art), then the ghost-cave basement.
6. **Optional refinement loop:** once blender-mcp is wired (ahujasid/mcp-for-blender), the agent can do screenshot→move→re-render micro-adjustments with any local LLM — but the JSON layout stays the source of truth; MCP moves get written back into it.
7. **Pull furniture gaps:** anything we don't have (CRT TV with antenna, side table, TV stand shelves) comes from Quaternius/Kenney/Poly Pizza per §5, logged with license in the repo; stylized low-poly to match the show.

**What NOT to do:** don't run ATISS/DiffuScene/Holodeck/Infinigen to "generate a nicer living room" — they will produce a *different* room. The drawing is the spec.

---

## 7. Pull-in log (RESEARCH-TO-REPO)

| Finding | Verdict | Status |
|---|---|---|
| Interior-design rule corpus | PULL IN | ✅ committed: `tools/layout-rules/` (rules JSON, validator, Blender applier, README) |
| Holodeck constraint-solver pattern (constraints → deterministic solver) | PULL IN (pattern only) | ✅ adopted in §6 recipe; Holodeck itself NOT installed (key + Unity weight) |
| ahujasid/mcp-for-blender | PULL IN (workflow) | ✅ documented in §3 + §6 step 6; install on the build lane when ready |
| Quaternius / Kenney / Poly Pizza / Sketchfab / Poly Haven | PULL IN | ✅ licensed-source table in §5; fetch per §6 step 7 |
| Archimesh (Blender-bundled) | PULL IN (note) | ✅ §4 + §6 step 5; no code needed, it's in Blender already |
| LayoutGPT / ATISS / SceneFormer / DiffuScene / LEGO-Net / InstructScene / PlanIT / LayoutDreamer / Infinigen | document-only or skip | ✅ §1/§4 with honest reasons — findings without pull-in are recorded, not orphaned |

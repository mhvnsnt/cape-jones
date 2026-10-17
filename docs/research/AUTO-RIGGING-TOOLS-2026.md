# Auto-Rigging Tools for Blender — 2026 research (for the Cape Jones full-stack rig)

**Researched:** 2026-10-16 (overnight idle pipeline). **Method:** 2026 sources only
(StraySpark 2026 rigging/animation roundups, Tripo 2026 auto-rigger guide, Superhive
product pages, Blender Studio docs). No training-data guesses. License verdicts are
the pull/skip decision — commercial use must be allowed.

**Context:** REV3's big task is full-stack rig + animate of the Cape Jones model
(native 0.925 m, no rescale): skinning/meshing with correct stretch/no-stretch
weight zones. The free-tools team is wiring Aider/Colab/Cline into this repo; this
doc picks the rigging tool for them to use.

## Verdict table

| Tool | Cost | License | Pull? | Notes |
|---|---|---|---|---|
| **BlenRig 6** | Free | GPL-3.0 ✅ commercial OK | ✅ **PULLED** (`production/tools/blenrig6`, `master_blender4`) | Best FREE full body+face auto-rig in 2026 roundups. Mesh-deform muscle system, IK/FK + stretch, face rig. Used on open movies/studio shorts. Verified: 99/99 py compile, headless install+enable OK on Blender 4.0.2 |
| Rigify + CloudRig | Free (built into Blender 4.x) | Blender/GPL ✅ | n/a — already installed | Baseline. Metarig → generate. Weaker deformation + face than BlenRig; fine as fallback |
| FaceIt | **Paid** (Blender Market) | commercial | ❌ skipped | Best face rigging, but paid — violates the no-paid rule. Documented only |
| Auto-Rig Pro | **Paid** | commercial | ❌ skipped | 2026 top pick overall, but paid. Documented only |
| Voxel Heat Diffuse Skinning | **Paid** | commercial | ❌ skipped | Best auto-weights for tricky meshes; paid |
| X-Muscle System | **Paid** | commercial | ❌ skipped | Muscle/jiggle realism; paid |
| Mixamo (Adobe) | Free (account) | Adobe terms — check before commercial use | ⚠️ optional, browser lane | Web auto-rigger + huge mocap library. Upload model, download rigged FBX. Good for rapid prototyping, not for the hero rig |
| Cinevva Auto Rigger | Free browser tier / $29 Blender addon | check terms | ⚠️ optional | Browser: upload GLB/FBX/OBJ → rigged GLB back. Fast option if BlenRig stalls on the Tripo mesh |
| Tripo one-click rigging | Free tier (Tripo platform) | check terms | ⚠️ optional | Tripo's 2026 guide lists one-click universal rigging in their suite — worth checking whether the already-pulled Tripo model has a rigged variant |

## Why BlenRig 6 for this task

1. **Face + body in one free system.** The face is where Rigify's basic bones fall
   short; BlenRig ships a real facial rig — needed for the dialogue/expression work.
2. **Deformation quality.** Mesh-deform cage + lattices give muscle-like sliding
   skin — directly addresses "correct stretch/no-stretch weight zones."
3. **Guided workflow.** Rigging Assistant Guides walk through reproportion → binding
   → weight cleanup, which is the exact REV3 work list.
4. **Proven.** Open movies, Pettson and Findus, Kiribati feature, Man in the High
   Castle VFX — not a toy.

## Caveats for the rig lane

- BlenRig rigs are **control rigs, not game skeletons.** For any engine export:
  duplicate DEF bones → Copy Transforms constraints → bake visual transforms →
  export baked armature + mesh (documented in the blenderartists BlenRig 6 thread).
- Steeper setup than paid Auto-Rig Pro; the guides are the manual — read them.
- Blender 4.x only on this branch (`master_blender4`); Blender 3.x unsupported.

## Sources

- https://www.strayspark.studio/blog/best-blender-rigging-addons-2026 (roundup, 110 days old at research time)
- https://www.strayspark.studio/blog/best-blender-animation-addons-2026
- https://www.tripo3d.ai/content/en/guide/the-best-ai-auto-rigger-tools-for-blender (2026 market analysis)
- https://superhivemarket.com/products/blenrig (BlenRig 6 product page, free)
- https://studio.blender.org/training/blenrig/56965fc3c379cf44546120e1/ (Blender Studio: GPL, public git repo)

## Update 2026-10-17 — SkinTokens / TokenRig pulled (overnight idle pipeline)

**Winner for "auto-rig Tripo models perfectly" (owner-directed task):**
SkinTokens/TokenRig by VAST-AI-Research — the SAME team that makes Tripo. Unified
autoregressive model: one mesh in → full skeleton + dense skinning weights out,
single command. MIT license (license gate PASSED), 98–133% skinning accuracy
improvement over UniRig per authors. Pulled 2026-10-17 to
`production/tools/skintokens-autorig/` (code only, 15MB; `.git` stripped; all
`.py` pass `py_compile`; MIT LICENSE verified on disk). Wiring:
`production/tools/skintokens-autorig/CAPE-JONES-WIRING.md`.

| Detail | Value |
|---|---|
| Repo | https://github.com/VAST-AI-Research/SkinTokens |
| License | MIT ✅ commercial use allowed |
| Needs GPU | Yes — NVIDIA ≥14 GB VRAM; run on Kaggle/Colab, not the VM |
| Command | `python demo.py --input model.glb --output rigged.glb --use_transfer` |
| Skin onto existing skeleton | `--use_skeleton` (BlenRig × TokenRig combo lane) |
| Weights (download on GPU machine, never committed) | `articulation_xl_quantization_256_token_4`, `skin_vae_2_10_32768` via `python download.py --model` |
| Known caveat | Single-pass; if weights bleed on the cape/edge zones, post-process or fall back to UniRig two-stage |

**Runner-up documented, not pulled:** UniRig (https://github.com/VAST-AI-Research/UniRig,
MIT) — predecessor two-stage pipeline (skeleton → skinning). Kept as the documented
fallback if TokenRig's single pass underperforms on a mesh.

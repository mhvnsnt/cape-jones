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

## Update 2026-10-17 — afk-rig 0.1.2 pulled (overnight idle pipeline)

**New lane: deterministic local auto-rigger built FOR AI agents.**
afk-rig (afk.ai) — CLI + MCP server (stdio) that auto-fits a skeleton to a
GLB, then lets the agent inspect renders, correct joints (`set`/`move`/`aim`/
`rotate`/`fit`, mirrored), apply surgical skin-weight rules, and export with
animations. No GPU, no weights download, runs on the VM.

| Detail | Value |
|---|---|
| Source | npm tarball (no public GitHub repo): https://registry.npmjs.org/afk-rig/-/afk-rig-0.1.2.tgz |
| License | MIT (code, `LICENSE` on disk) ✅ + CC0 1.0 (assets, `assets/LICENSE-CC0.md` on disk) ✅ — rigs and rigged models cleared for commercial use |
| Pulled to | `production/tools/afk-rig/` (vendored, 17MB, largest file 5.0MB — under 50MB rule; `node_modules/` removed before commit) |
| Wiring | `production/tools/afk-rig/CAPE-JONES-WIRING.md` |
| Verified | `npm install --omit=dev` → `--help` prints full command list; `skeletons` → 9 rigs (human: 66 bones incl. fingers); `animations human --search walk` → 10 walk clips; all run clean 2026-10-17 |
| One-shot | `afk-rig auto model.glb --skeleton human --out rigged.glb --animations all` |
| Agent loop | `start` → `render --joints all --labels` → `inspect --issues` → `set/aim/fit` → `weights --add` → `bind` → `export` |
| MCP | `afk-rig mcp` — stdio server (Claude Code / Cursor / Windsurf / Claude Desktop) |
| Cape Jones uses | (1) fast local pass for new Tripo models; (2) `weights` rules + `render --weights` + `slice`/`ray` to repair the W5r bake-off shoulder/feet defect zones; (3) 178 CC0 human clips as the EP01 animation-blocking library; (4) `--hands all-fingers`, cape mesh excluded from fitting (`meshes --exclude`) |

**RigAnything re-verified 2026-10-17 (overnight idle pipeline):** license at
https://github.com/Isabella98Liu/RigAnything is the **Adobe Research License —
noncommercial research only** (copyright Adobe Inc.). The REJECTED row in
`AUTO-RIG-TRIPO-2026.md` stands confirmed — not pulled, per the owner's license
law.

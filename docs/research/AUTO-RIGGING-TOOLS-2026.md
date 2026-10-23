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
| **COLMAP** (colmap/colmap) — auto-scanning | Free | **new BSD ✅ commercial OK (own-eyes verified 2026-10-18)** | ✅ **PULLED 2026-10-18** (production/tools/colmap/, upstream @ f202e4e) | SfM + MVS photogrammetry, GUI + CLI, pycolmap pip bindings, CUDA wheels. 12,978 stars, active. See 2026-10-18 update below |
| CEB SAM 3D Body Loader (cebstudios) — mocap + retargeting | Free to download | ❌ **commercial gate FAIL** | ❌ **REJECTED** | 100% free 2026-10-17, but author's own page warns underlying models (SAM 3D Body, GEM-X/NVlabs) carry licenses "restricted to non-commercial research". Free ≠ commercial-safe. Windows-only, not a git repo. See 2026-10-18 update below |

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

## Update 2026-10-18 — auto-retargeting + auto-scanning research (overnight idle pipeline)

The AUTO-RIGGING PRIORITY law lists five axes: auto-rigging, auto-boning,
auto-scanning, auto-skinning, auto-retargeting. The first two are now covered
(Pinocchio / UniRig / TokenRig / afk-rig / BlenRig 6 / CloudRig pulled + wired).
This run researched the two uncovered axes with live 2026 sources (browser
search + own-eyes page reads). **Nothing pulled this run** — disk at the 85%
ceiling — so this is research-only. The next run with disk headroom can pull
the READY rows directly.

### Auto-retargeting (mocap → character rig)

| Tool | License | Verdict | Notes |
|---|---|---|---|
| Rokoko Studio Blender plugin | proprietary, free to use | ⚠️ fallback, not a pull | "Free Rokoko Blender retargeting plugin" (Blender Secrets via rokoko.com). Closed-source — doesn't fit the open-source pull convention. Own-eyes ToS re-check 2026-10-18: plugin is account-gated (sign-in required in-plugin), no open-source repo exists, and the public ToS (rokoko.com/terms) is a generic Shopify template with NO explicit grant of commercial rights for free-tier recordings. Vision free tier = 30s/month single-cam recordings — a bottleneck for a show pipeline. Pragmatic fallback only; confirm commercial terms with Rokoko before any production use. |
| **CEB SAM 3D Body Loader** (cebstudios) | ❌ **commercial gate FAIL** | ❌ **REJECTED — do not pull** | Went 100% FREE 2026-10-17 (own-eyes read of patreon.com/cebstudios post, 2026-10-18). BUT the author's own page carries a Commercial Use Disclaimer: "the underlying models and AI inference projects … carry their own distinct licenses and terms of use (**some of which may be restricted to non-commercial research**)". Underlying: SAM 3D Body (Meta AI Research), GEM-X (NVIDIA NVlabs), Fast-SAM-3D-Body. Free ≠ commercial-safe — fails the owner's license law. Also Windows-only, Patreon-zip distribution (not a git repo). |
| "Good Good" retargeting tool (Pro Constantinou) | **no license stated / proprietary distribution** | ❌ **REJECTED — do not pull** | 80.lv 2026-06-17 technique note (hip-placement + limb-proportion matching) stands as useful research. **2026-10-18 final verdict (own-eyes read of the tutorial video description, "Better Mocap Retargeting + Live Retarget Plugin", GoodGood channel, published Jun 14, 2026):** no product name, no price, NO license terms, no Blender version in the description. The creator built "my own retargeting plugin" and distributes it to **Patreon supporters only** (sole link: https://www.patreon.com/goodgood3d). No open-source repo, no explicit commercial-use grant — fails the license law. Rejected as a pull; technique note kept for reference. |
| MakeHuman MakeWalk | GPL | legacy, skip | BVH→MH-rig retargeter (2018-era docs). MPFB — its successor — is already pulled; no new value. |
| **Simple Retarget Tool** (cgvirus) | **GPL-3.0 ✅ commercial OK (own-eyes verified 2026-10-18 in-tree LICENSE)** | ✅ **PULLED 2026-10-18** (`production/tools/simple-retarget-tool/`, upstream @ 3adcfaf) | Free single-file Blender addon: retargets Mixamo / BVH / iClone animation → Rigify, Daz3D (G3/G8), custom rigs. V2 added one-click "Set Rest Pose" + preset import/export; V3 added blend-shape-safe rest pose. 144 stars, 3 releases, 2 py files, 60KB, no deps, py_compile clean. Wiring: `production/tools/simple-retarget-tool/CAPE-JONES-WIRING.md`. This closes the open gap named in the net line below — first free, open-source, commercial-safe, account-free BVH→rig retargeter in the stack. |

**Update 2026-10-18 (overnight idle pipeline):** the net gap below is now CLOSED —
Simple Retarget Tool (GPL-3.0, own-eyes license-verified) pulled into
`production/tools/simple-retarget-tool/`. The rig lane can now use it + the
178 CC0 clips (afk-rig) for retarget workflows. Rokoko stays the pragmatic
fallback for live streaming / advanced cleanup only.

Net: **no open-source, commercial-safe mocap retargeting tool found this run**
beyond what's covered. Rokoko's free plugin stays the pragmatic fallback (ToS
checked 2026-10-18: account-gated, no explicit commercial grant on the free
tier — confirm with Rokoko before production use); the rig lane should use
afk-rig's 178 CC0 motion clips + BlenRig 6 for retarget workflows until a
clean open option appears.

### Auto-scanning (photogrammetry → 3D mesh)

| Tool | License | Verdict | Notes |
|---|---|---|---|
| **COLMAP** (colmap/colmap) | **new BSD ✅ commercial OK (own-eyes verified 2026-10-18)** | ✅ **PULLED 2026-10-18** (production/tools/colmap/, upstream @ f202e4e) | 12,978 stars / 3,127 commits / active (upstream @ f202e4e (pulled 2026-10-18, code-only, BSD-3 own-eyes on disk). README: "The COLMAP library is licensed under the new BSD license" — full BSD-3 text verified on the repo page (Copyright 2016 ETH Zurich and UNC Chapel Hill; 2016–2026 The COLMAP Contributors). GitHub shows NOASSERTION badge (no SPDX identifier) — same situation as rhubarb-lip-sync, resolved by the in-file text. SfM + MVS, GUI + CLI, `pip install pycolmap` (+ CUDA wheels `pycolmap-cuda12`), prebuilt binaries + Docker. GPU-lane tool (dense MVS wants CUDA); code-only pull, no weights. |
| Meshroom / AliceVision | **MPL-2.0 ✅ commercial OK (own-eyes verified 2026-10-18)** | ✅ **PULLED 2026-10-18** (`production/tools/meshroom/` @ 7c6f5c5, `production/tools/alicevision/` @ 3afba20) | AliceVision's own IP wiki (own-eyes read 2026-10-18): "licensed under an open source license that allows **free personal and commercial use**", "**no additional restrictions for corporate use**"; models created with it are the user's own IP. MPL-2.0 is weak (file-level) copyleft — commercial use permitted, larger works can be proprietary. License text own-eyes re-verified in-tree 2026-10-18 (`LICENSE-MPL2.md` both repos). NVIDIA-CUDA heavy (dense meshing wants CUDA); node-graph GUI. GPU-lane tool; code-only pull. |
| Agisoft Metashape / RealityCapture / RealityScan | paid or proprietary | ❌ skipped | Out of scope per the no-paid law. Documented only. |

Cape Jones use for auto-scanning: digitize real props, costumes, and reference
maquettes into textured meshes for the show pipeline. COLMAP first (cleanest
license), Meshroom second (MPL-2.0, commercial use explicitly permitted —
verified 2026-10-18). **Pulled 2026-10-18 (overnight idle pipeline, disk at
84% — under the 85% gate):** `production/tools/meshroom/` (Python node-pipeline
app, 4.9MB code-only, @ 7c6f5c5) + `production/tools/alicevision/` (C++ SfM/MVS
engine, 65MB code-only, @ 3afba20). 317/317 Python files pass py_compile; all
shell scripts pass bash -n; branding logos stripped; upstream agent guides
renamed (MESHROOM-UPSTREAM-*.md). Wiring docs at
`production/tools/{meshroom,alicevision}/CAPE-JONES-WIRING.md` (GPU-lane build
path — Kaggle/Colab, dense MVS wants CUDA; no weights, classical CV).

### Sources

- https://github.com/colmap/colmap (README + LICENSE, own-eyes 2026-10-18)
- https://www.patreon.com/cebstudios/posts/ceb-sam-3d-body-172610949 (own-eyes 2026-10-18)
- https://80.lv/articles/try-this-new-mocap-retargeting-tool-for-blender (2026-06-17)
- https://www.rokoko.com/insights/exploring-the-fusion-of-ragdoll-physics-and-mocap-animation-in-blender-with-blender-secrets
- https://vagon.io/blog/free-vs-paid-photogrammetry-meshroom-or-agisoft-metashape
- https://foro3d.com/en/2026/january/photogrammetry-software-comparison-meshroom-vs-agisoft-metashape-vs-realitycapture.html
- https://github-wiki-see.page/m/alicevision/Meshroom/wiki/Intellectual-property (own-eyes 2026-10-18: MPL-2.0, "free personal and commercial use", "no additional restrictions for corporate use")

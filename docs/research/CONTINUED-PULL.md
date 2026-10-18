# CONTINUED PULL (2026-10-16) — Filling the Gaps

Owner: "keep pulling more stuff in that would be relevant." Aggressive gap-fill pass.

## Gap Analysis (from full tools inventory review)

| Gap | Status | Solution |
|-----|--------|----------|
| Storyboard → timed animatic (auto) | ❌ Missing | ✅ Built `animatic_builder.py` |
| Anime speed lines / impact frames | ❌ Missing | ✅ Built `anime_fx.py` |
| Screen shake for hits | ❌ Missing | ✅ Built into `anime_fx.py` |
| VHS / CRT / retro effects | ❌ Missing | ✅ Built `retro_fx.py` |
| Social delivery presets (TikTok/Shorts/IG) | ❌ Missing | ✅ Built `social_export.sh` |
| Anime-specific upscale/interpolate/restore | ❌ Missing | 🔄 Cloning TheAnimeScripter |
| Title cards / kinetic typography / bumpers | ❌ Missing | ✅ Cloned html-animation |
| Browser-based storyboard w/ audio timing | Partial (Storyboarder) | ✅ Cloned choxos/storyboard |
| Script → narrated video (auto animatic) | ❌ Missing | ✅ Cloned explainroo |
| Anime-style 3D rendering (cel shader) | ✅ Pulled | three-anime-style in production/tools/ (MIT, pulled 2026-10-16) |

## Custom-Built Pipeline Scripts

All in `post-pipeline/`, all CPU-only, all tested.

### `anime_fx.py` — Anime 2D effect overlays
- `--speed-lines`: Radial manga speed lines (surprise/speed). Transparent PNG sequence.
- `--impact`: White flash + starburst impact frames.
- `--speed-overlay INPUT`: Composite speed lines onto video at timestamp.
- `--shake-input INPUT`: Screen shake via animated crop (for hits/explosions).
- Tested: generates correct radial lines, verified visually.

### `retro_fx.py` — VHS/CRT retro effects
- `--vhs`: Tracking distortion + chromatic aberration + noise + soft blur.
- `--crt`: Scanlines + vignette + phosphor glow.
- `--chromatic` / `--noise` / `--scanlines`: Individual effects.
- `--intensity 0.1-2.0`: Strength control.
- For the trippy/Adult Swim vibe segments.

### `social_export.sh` — Social delivery presets
- `tiktok`/`shorts`/`reels`: 9:16 (1080x1920), smart center crop.
- `instagram-square`: 1:1 (1080x1080).
- `instagram-portrait`: 4:5 (1080x1350).
- `--focus-top` / `--focus-bottom`: Crop bias for character framing.
- All outputs: yuv420p + faststart (platform-compatible).

### `animatic_builder.py` — Storyboard → timed animatic
- Input: board images + CSV/JSON timing file.
- Optional: temp audio track, crossfade transitions.
- Output: 1080p MP4 animatic at 24fps.
- Closes the Storyboarder → animation gap.

## Cloned Tools

### `html-animation/` (acelera-agency, MIT, 14MB)
Motion graphics as code. Frame-exact animated logos, kinetic typography.
**Key feature**: exports MP4 in 1:1, 4:5, AND 9:16 from a single HTML file.
Use for: Adult Swim-style bumpers, title cards, "___ JONES" name gags.

### `storyboard/` (choxos, MIT, 1.1MB)
Browser + Tauri motion graphics editor. Storyboard → keyframes → audio timing → video export.
New (Sept 2026). Complements Storyboarder with web-based workflow.

### `explainroo/` (vincentsch, 6.4MB)
Script → narrated explainer video. Kokoro voice + Whisper timing + canvas renderer → MP4.
Use for: automated temp animatics with scratch dialogue.

### `TheAnimeScripter/` (NevermindNilas, ✅ core pulled, 7.5MB)
THE anime video toolkit. Updated 4 days ago. Core CLI + src/ modules intact.
Models download on-demand (by design).
- Upscale: 15+ anime-specific models (AnimeSR, AniScale 2, SPAN, etc.)
- Interpolate: RIFE 4.6–4.26, GMFSS Fortuna
- Restore: denoise, deblur, dehalo, deband (anime-tuned)
- Dedup, scene detection, depth maps, segmentation
- CLI + standalone + After Effects panel
This replaces/augments our generic RIFE pipeline with anime-specific models.

## Pipeline Integration

```
Storyboarder / storyboard/ → boards
  → animatic_builder.py → timed animatic (+ temp audio)
  → [owner draws keyframes]
  → ToonComposer / ToonCrafter → animation
  → anime_fx.py → speed lines / impact / shake
  → retro_fx.py → VHS/CRT grade (optional)
  → finish.py → color grade + audio mix
  → social_export.sh → TikTok / Shorts / IG versions
  → delivery
```

## Still To Pull (network blocked, retry later) — RESOLVED 2026-10-16
- `three-anime-style/` (xymeow, MIT): Cel-shaded anime rendering for Three.js 3D segments — ✅ PULLED 2026-10-16 into `production/tools/three-anime-style/` (22MB). NOTE: unblock-browser-items.json claimed a sibling agent had pulled it, but it was NOT on main — verified against the repo and pulled fresh.
- `video-gif-studio/` (miles990): Storyboard planning + music beat analysis — ✅ RECOVERED via PR #34 (126MB, on main).
- `AnimeEffects/` (AnimeEffectsDevs): 2D animation tool (GPL-3.0) — ✅ cloned (17MB).
- `hyperframes-effects-gallery/`: 255-effect catalog (transitions, captions) — ✅ correct URL found (genoooool/hyperframes-effects-gallery), PULLED 2026-10-16 into `production/tools/hyperframes-effects-gallery/` (427MB: 230MB previews, 1.5MB catalog JSON). License caveat: upstream effects keep original licenses per THIRD_PARTY_NOTICES.md.
- `cartoon-studio/` (Jellypod-Inc, **Apache-2.0 — commercial use OK**): 2D animated cartoon-show studio desktop app (Electron + Vite + TypeScript) — script in, MP4 out. Stage (drag SVG chars onto 1920x1080 canvas), Dialogue (87 voices across 8 TTS providers w/ word timestamps), Play (film-cabinet preview, render to MP4). Key pieces for our pipeline: `scripts/rig-svg.ts` CLI (SVG mouth auto-rig, 9-shape Preston Blair/Rhubarb mouth catalog, vowel-heuristic lip-sync cues), HyperFrames HTML→MP4 render path (pairs with our `hyperframes-effects-gallery/` pull), reproducible output from script+voices+characters (no LLM in the render loop). ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/cartoon-studio/` (6.4MB, source-only, no node_modules, commit e773568f). Note: runs on API keys (BYOK, encrypted in OS keyring); upstream TTS/LLM keys are owner-provided — render code itself is offline-capable. Candidate uses: Ashes mouth-pack SVG rigging workflow, episode animatic→MP4 render path evaluation.

### `AnimeEffects/` (AnimeEffectsDevs, ✅ cloned, 17MB)
2D modular animation tool. GPL-3.0. Updated Dec 2025. C++ based.

### `rhubarb-lip-sync/` (DanielSWolf, ✅ cloned, 147MB)
Automatic lip-sync from audio: phoneme recognition (Pocketsphinx-based) → Preston Blair/Rhubarb mouth-shape timeline. The standard OSS lip-sync reference used by cartoon-studio's mouth catalog. MIT verified (LICENSE.md, full MIT text — GitHub API reports NOASSERTION but the license file is explicit; commercial use OK). Upstream active (updated 2026-10-17). Upstream `.github/` workflows stripped per convention. ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/rhubarb-lip-sync/` (shallow depth-1, source-only). Candidate uses: dialogue → mouth-shape timelines for Ashes mouth-pack and cartoon-studio SVG rigs (replaces vowel-heuristic fallback), episode dialogue tracks.


### `colmap/` (ETH Zurich/UNC, new BSD ✅ commercial OK, 25MB)
Industry-standard Structure-from-Motion + Multi-View Stereo photogrammetry pipeline (C++17, optional CUDA; Qt GUI + `pycolmap` Python bindings). BSD-3 text own-eyes verified in-tree (Copyright 2016 ETH Zurich and UNC Chapel Hill; 2016-2026 The COLMAP Contributors; GitHub spdx badge NOASSERTION but license file explicit — same resolution as rhubarb-lip-sync). Shallow depth-1 @ f202e4e, no submodules; upstream `.github/` stripped, upstream `AGENTS.md` renamed to `COLMAP-UPSTREAM-AGENTS.md` (not a repo law file); thirdparty LICENSE files kept (VLFeat, SiftGPU, PoissonRecon, LSD, Symforce-Caspar); all 22 Python files pass py_compile; no binaries >2MB. ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/colmap/`. Wiring doc: `production/tools/colmap/CAPE-JONES-WIRING.md` (GPU-lane build path — Kaggle/Colab, dense MVS wants CUDA; classical CV, no weights). Candidate uses: the AUTO-SCANNING axis — digitize real props/costumes/maquettes into textured meshes for the show pipeline; fabric drape reference for the Wiggle-2 cape sim; living-room prop reconstruction.

### `pencil2d/` (pencil2d, ✅ cloned, 20MB)
Hand-drawn 2D frame-by-frame animation app (Qt/C++). Bitmap + vector layers, onion skinning, camera layer, sound scrubbing. GPL-2.0 verified (LICENSE.TXT in-tree + GitHub API spdx_id=GPL-2.0, commercial use OK); upstream active (updated 2026-10-17). Upstream `.github/` workflows stripped per convention. ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/pencil2d/` (610 files, shallow depth-1, no binaries >50MB). Candidate uses: hand-drawn 2D keyframes for Cape Jones shorts, EP01 gag-book sketches (fills the lightweight-frame-by-frame slot from FULL-PRODUCTION-STACK.md row 197).

### `piper-tts/` (rhasspy, ✅ cloned, 47MB)
Fast local offline neural text-to-speech: C++ inference binary + Python package + HTTP server. MIT verified (LICENSE.md in-tree + GitHub API spdx_id=MIT, commercial use OK); upstream archived 2026 (project complete/stable, v1.2.0). Upstream `.github/` workflows stripped per convention; all 233 upstream blobs verified present. ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/piper-tts/` (shallow depth-1, source-only; `etc/test_voice.onnx` 27MB kept for smoke tests; voice files stay OUT of git — download on demand from rhasspy/piper-voices). Wiring doc: `production/tools/piper-tts/PIPER-TTS.md`. Candidate uses: scratch dialogue/temp narration for animatics without API keys (pairs with `rhubarb-lip-sync/` audio→mouth-shape + `cartoon-studio/` dialogue), podcast/narration drafts, voice prototyping before ElevenLabs/actor recordings.

### `cloudrig/` (Blender Studio / Demeter Dzadik, ✅ cloned, 17MB)
Modular rig-generation extension for Blender — metarig + component types (spine, limbs, chains, face action system) → regenerate control rigs from checkboxes, no hand-rebuilding. The rig tool behind Blender Studio's Sprite Fright / Rain / Snow / Storm. GPL-3.0 verified (CloudRig/LICENSE in-tree, commercial use OK); upstream active (pushed 2026). Shallow depth-1 from https://projects.blender.org/Mets/CloudRig (HEAD 05b6ddd9) + bs_utils submodule at pinned 88556987 (fetched via HTTPS — upstream .gitmodules was SSH-only; URL switched to https in-tree; upstream `.gitea/` CI + `.vscode/` stripped per convention). ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/cloudrig/` (231 files, no binaries >50MB). Candidate uses: regenerable parametric control rigs for Cape Jones / Ashes (direct answer to the AUTO-RIGGING PRIORITY law and the owner's "more bones/joints" rig complaint — 5-joint flexible spine component etc.), pairs with GNM face params and the BlenRig6 pull.

### `meshroom/` + `alicevision/` (alicevision org, ✅ cloned, 70MB code-only)
Meshroom: Python + Qt node-graph photogrammetry pipeline app (each node wraps an AliceVision binary; `.mg` graphs chain full pipelines — photogrammetry, camera tracking, HDR). AliceVision: the production-grade C++ SfM/MVS engine underneath (Mikros Image / VFX lineage) — `src/aliceVision/` modules exposed as `aliceVision_*` CLI binaries, `.mg` graph templates in `meshroom/`, `pyTests/` suite. MPL-2.0 verified (own-eyes read of `LICENSE-MPL2.md` in both trees + AliceVision IP wiki: "free personal and commercial use", "no additional restrictions for corporate use"; libmv-derived code MIT per `LICENSE-MIT-libmv.md`; commercial use OK). Shallow depth-1 @ 7c6f5c5 (Meshroom) / 3afba20 (AliceVision), `develop` branch, no submodules; Meshroom branding logos stripped; upstream `AGENTS.md`/`CLAUDE.md` renamed to `MESHROOM-UPSTREAM-*.md` (never confused with repo law files); 317/317 Python files pass py_compile; all shell scripts pass bash -n; no binaries >2MB in-tree (`.spi3d` LUTs in `src/aliceVision/image/share/` are upstream color-science data assets, kept deliberately); no model weights (classical CV). ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/meshroom/` (4.9MB) + `production/tools/alicevision/` (65MB). Wiring docs: `production/tools/{meshroom,alicevision}/CAPE-JONES-WIRING.md` (GPU-lane build path — Kaggle/Colab, dense MVS wants CUDA). Candidate uses: the AUTO-SCANNING axis — node-graph photogrammetry for repeatable prop/costume/maquette digitization into textured meshes; repeatable `.mg` graphs re-runnable headless via `meshroom_batch`; fabric drape reference for the Wiggle-2 cape sim; living-room prop reconstruction. Research verdict row in AUTO-RIGGING-TOOLS-2026.md updated READY→PULLED; Rokoko retargeting-plugin ToS re-checked (account-gated, no explicit commercial grant on free tier — fallback only).

## Disk Impact
Custom scripts: <50KB. Clones: ~42MB. Total pull: <45MB.

## Retry Status (2026-10-16 ~04:00 EDT) — updated ~16:30 EDT
- `three-anime-style/`: ✅ PULLED 2026-10-16 into production/tools/three-anime-style/ (MIT, 22MB).
- `video-gif-studio/`: ✅ recovered via PR #34 (on main).
- `hyperframes-effects-gallery/`: ✅ correct URL found (genoooool/hyperframes-effects-gallery). Status below.

## 2026-10-18 06:44 CDT (idle pipeline) — PULLED Simple Retarget Tool into cape-jones
- **Simple Retarget Tool** (cgvirus/Simple-Retarget-Tool-Blender @ 3adcfaf): free Blender addon, retargets Mixamo/BVH/iClone animation → Rigify, Daz3D (G3/G8), custom rigs. V2 one-click "Set Rest Pose" + preset import/export; V3 blend-shape-safe rest pose.
- **License:** GPL-3.0 — own-eyes verified in-tree (`LICENSE`, GNU GPL Version 3, 29 June 2007). Commercial-safe as a tool (same standing as afk-rig).
- **Pull:** 60KB, 2 Python files (py_compile clean), no deps, no binaries, no weights. Found via live 2026 search after the retargeting axis showed "no open-source, commercial-safe tool" in the 06:14 run's research. Closes that gap.
- **Wiring:** `production/tools/simple-retarget-tool/CAPE-JONES-WIRING.md` (install, 5-step retarget workflow, rest-pose gotchas, hip/limb proportion tip carried from the "Good Good" technique note, Blender 4.x/5.x API note).
- **Docs:** AUTO-RIGGING-TOOLS-2026.md retargeting table gained the PULLED row + gap-closed update.

## 2026-10-18 07:44 CDT (idle pipeline) — PULLED MHR (Momentum Human Rig) into cape-jones
- **MHR** (facebookresearch/MHR, Meta, `main` @ d96fafa33bbf018647c70c3525e91f53e79d2a14): parametric 3D human body model — ATLAS-integrated, artist-oriented. 18,439 verts, 127 joints, 7 LODs; 45 identity / 204 pose / 72 FACS expression params (decoupled skeleton + shape); sparse non-linear MLP pose correctives per joint (geodesic-sparsity masked); dual GPU/CPU solver (PyTorch + PyMomentum); SAM 3D Body perception. The "different org's GNM" from PARAMETRIC-BODY.md — Meta's answer to Google's GNM.
- **License:** Apache-2.0 — own-eyes verified in-tree (`LICENSE`, Apache License Version 2.0, January 2004); GitHub SPDX badge `Apache-2.0`. Free AND commercial-safe.
- **Pull:** 9MB, shallow depth-1, 25/25 Python files pass py_compile, 1 shell script passes bash -n; `.github/` (CI) stripped; no binaries >2MB except `tools/mhr_LOD_conversion/lod1_to_lod0_mapping.npz` (2.3MB upstream LOD-mapping data asset, kept deliberately); **no model assets in repo** — they download GPU-lane via `mhr-download-assets` (`https://github.com/facebookresearch/MHR/releases/latest/download/assets.zip`, see `mhr/download_assets.py`).
- **Wiring:** `production/tools/mhr/CAPE-JONES-WIRING.md` (GPU-lane Kaggle/Colab build path; four Cape Jones uses: learned-corrective reference for the PSD porting plan, anatomical joint placement, pose prior for mocap retargeting, SMPL-X bridge via `tools/mhr_smpl_conversion/`).
- **Docs:** PARAMETRIC-BODY.md row 3 verdict Pull-ready→PULLED; pending list updated (MHR row removed — was blocked on the 85% disk gate, pulled at 68%).
- Closes the PARAMETRIC-BODY.md "Pull-ready (not yet local — disk)" row — the last disk-blocked body-model pull.

## 2026-10-18 17:14 CDT (idle pipeline) — SOMA-X license VERIFIED (Apache-2.0); Adaptive Auto Skinning REJECTED (paid)
- **SOMA-X** (NVlabs/SOMA-X, NVIDIA, `main` @ 56a3d957a549c66425b500fddf7f3183bc6fbdff, 19 commits, 820★, 65 forks): canonical differentiable representation for parametric human bodies/hands — unifies 5 identity backends (SOMA-Shape, MHR, SMPL-X, Anny, GarmentMeasurements) under one 77-joint skeleton + a single MLP pose-correctives model trained once on shared SOMA topology (mitigates standard LBS artifacts without per-model corrective learning). `SOMALayer` (body: mid/low/extra-low LODs) + `SOMAHandLayer` (wrist-local L/R hands); NVIDIA Warp-accelerated runtime skinning/fitting; USD/NPZ I/O, pose inversion, procedural rig controls, conversion tools. PyPI `py-soma-x`.
- **License:** Apache-2.0 — own-eyes verified three ways (GitHub repo page "License: Apache License 2.0", README "licensed under Apache-2.0", gh api `license: Apache-2.0`). Free AND commercial-safe. Caveat recorded: optional backends SMPL/SMPL-H/SMPL-X + MANO need user-supplied licensed model files (NOT redistributed upstream — same non-commercial registration wall as our SMPL-X note).
- **Code pull:** QUEUED, not pulled this run. Disk was 88% and climbing (live rig-audit + fingertip-proof render lanes writing frames) vs the keep-disk-under-85 gate. The SOMA-X git repo is ~21MB code-only with zero weights — no local-disk reason to block beyond the transient gate. Next idle run under 85%: `pull-to-repo.sh https://github.com/NVlabs/SOMA-X.git <checkout> production/tools/soma-x`, strip `.github/`+`.vscode/`, write `CAPE-JONES-WIRING.md` (GPU/Kaggle path: assets auto-download from HF `nvidia/SOMA-X` at first use — weights stay off local disk and off GitHub), flip PARAMETRIC-BODY.md row 4 verdict to PULLED.
- **Adaptive Auto Skinning** (Jessy Leite, Sept 2026) — ❌ **REJECTED, do not pull.** $35.00 USD paid product on SuperHive (own-eyes: JSON-LD Product.offers price 35.00 USD, "Free updates within the version you bought", 30-day refund). Not free, no open-source repo, no commercial-use grant for free tier — fails the owner's free+commercial license law the same way the "Good Good" Patreon-gated plugin did. Bakeoff plan revised: MPFB precomputed weights vs our W5r surface-heat-diffuse only. AAS technique notes (adaptive voxel grid, skeleton-geometry-based solver, 80.9% artist-weight match on 202 characters) kept in PARAMETRIC-BODY.md §5 for reference.
- **Docs:** PARAMETRIC-BODY.md row 4 verdict `check upstream`→license-verified + pull-queued; §5 auto-skinning item → AAS REJECTED verdict + reference technique notes; pending list → both items resolved with verdicts (Mixamo FBX retarget remains the last pending parametric-body item — needs owner's Adobe account, browser lane).

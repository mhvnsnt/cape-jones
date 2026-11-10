# GEMINI FULL PULL — Complete AI Video & Animation Studio Stack

**Pulled:** 2026-10-16 | **Owner order:** "everything it said bro" — no exceptions, no skipping.

Everything Gemini suggested, pulled in and documented. Code repos are local; heavy model weights download on Kaggle GPU via the setup scripts in `ai-video/kaggle-setup/`.

---

## 1. Wan 2.2 (Alibaba) ✅ CODE PULLED

- **What:** Open-weights text-to-video / image-to-video. Apache 2.0 (fully open for commercial use).
- **Local:** `~/workspace/tools/ai-video/wan2.2/` (18MB code)
- **Models:** 14B (full, ~40GB VRAM), A14B, 5B (T4-compatible)
- **Kaggle T4:** Use the **5B model** (`Wan-AI/Wan2.2-TI2V-5B`) or DiffSynth-Studio with FP8 + layer-by-layer offload for 14B.
- **Setup:** `ai-video/kaggle-setup/wan22_setup.sh`
- **Use for Cape Jones:** Generate animated backgrounds, environment plates, establishing shots.
- **Status:** Code ready. Weights download on Kaggle (~10GB for 5B).

## 2. HunyuanVideo (Tencent) ✅ CODE PULLED

- **What:** Cinematic AI video generation. Best camera moves and physics in open-source tier.
- **Local:** `~/workspace/tools/ai-video/hunyuanvideo/` (52MB code)
- **VRAM:** Full model needs **80GB+** (A100/H100 only). **NOT runnable on free Kaggle T4.**
- **Kaggle T4 path:** **HunyuanVideoGP** (GPU Poor version by DeepBeepMeep) + FP8 weights. Reduced quality but runs.
- **Setup:** `ai-video/kaggle-setup/hunyuan_setup.sh`
- **Use for Cape Jones:** High-end cinematic shots when we get A100 access. GP version for T4 experiments.
- **Status:** Code ready. Full weights need paid GPU; GP version works on T4.

## 3. Mochi 1 (Genmo) ✅ CODE PULLED

- **What:** 10B parameter video model. Unmatched smooth, physically believable motion. Apache 2.0.
- **Local:** `~/workspace/tools/ai-video/mochi/` (16MB code)
- **Weights:** ~40GB download from HuggingFace (`genmo/mochi-1-preview`) or via `scripts/download_weights.py`.
- **Kaggle T4:** Supported with `--cpu_offload`. Also works natively in ComfyUI via ComfyUI-MochiWrapper (already in our custom_nodes).
- **Setup:** `ai-video/kaggle-setup/mochi_setup.sh`
- **Use for Cape Jones:** Smoothest motion generation. Character action shots, background loops.
- **Status:** Code ready. Weights are large (~40GB) — download on Kaggle, not local.

## 4. LTX-Video (Lightricks) ✅ CODE PULLED

- **What:** The optimization king. Fast generation for quick iteration on consumer GPUs.
- **Local:** `~/workspace/tools/ai-video/ltx-video/` (868KB code)
- **Models:** `ltxv-13b-0.9.8-dev` (highest quality), `ltxv-13b-0.9.8-distilled-fp8` (real-time on H100, T4-friendly), `ltxv-13b-0.9.7-dev-fp8`.
- **Kaggle T4:** Use the **distilled-fp8** variant. Requires only ~8GB VRAM.
- **Setup:** `ai-video/kaggle-setup/ltx_setup.sh`
- **Use for Cape Jones:** Fast iteration on backgrounds, quick concept videos, real-time previews.
- **Status:** Code ready. T4-compatible with fp8 model.

## 5. ComfyUI + Frame Interpolation ✅ FULL INSTALL

- **What:** The undisputed hub for free AI video orchestration. Visual node-based workflows.
- **Local:** `~/workspace/tools/ai-video/comfyui/` (96MB + custom nodes)
- **Custom nodes installed:**
  - `comfyui-frame-interpolation/` — **RIFE v4.26, FILM, GMFSS Fortuna** (the exact suite Gemini recommended)
  - `ComfyUI-MochiWrapper/` — Mochi 1 in ComfyUI
- **Kaggle T4:** Fully supported. Launch with `python3 main.py --listen 0.0.0.0 --port 8188`.
- **Setup:** `ai-video/kaggle-setup/comfyui_setup.sh`
- **Use for Cape Jones:** Visual workflow for frame interpolation (alternative to our CLI RIFE), AI-assisted frame generation, upscaling chains.
- **VFI models:** Download from https://github.com/Fannovel16/comfyui-frame-interpolation#models
- **Status:** Installed with nodes. Ready to launch on Kaggle.

## 6. Unreal Engine 5 ⚠️ DOCUMENTED (not downloaded)

- **What:** Industry standard for real-time 3D cinematics, rendering, physics environments.
- **Why not downloaded:** UE5 is **~30-40GB** download, requires Epic Games Launcher account, and is primarily a 3D tool. Our pipeline is 2D-focused.
- **Install (when needed):**
  1. Download Epic Games Launcher from https://www.unrealengine.com/download
  2. Install Unreal Engine 5.x (free until $1M revenue)
  3. Linux: Build from source at https://github.com/EpicGames/UnrealEngine (requires Epic account linked to GitHub)
- **Use for Cape Jones:** 3D background environments, physics simulations, camera moves rendered as 2D plates. Future expansion.
- **Status:** Documented. Pull when we need 3D.

## 7. Cascadeur ⚠️ BROWSER DOWNLOAD REQUIRED

- **What:** AI-assisted 3D character animation. Physics-based posing, AutoPhysics, neural AutoPosing. Replaces mocap for action animation.
- **Version:** 2026.2.3 (released 2026-10-01)
- **Download:** https://cascadeur.com/download → click **"For Linux"** (554.33 MB)
- **Why browser:** Download links are JS-driven, no direct URL. **Parent agent needs to grab this via browser.**
- **Tiers:** Free (non-commercial, .casc export only) / Indie ($96/yr) / Pro ($396/yr, rent-to-own)
- **Linux:** Ubuntu 20.04+. Our VM should run it.
- **Use for Cape Jones:** 3D reference animation for complex action poses, physics-correct movement reference for 2D tracing.
- **Status:** Download page confirmed. Needs browser download.

## 8. OpenToonz ✅ CODE PULLED

- **What:** The actual open-source software used by **Studio Ghibli**. Traditional studio-style 2D animation.
- **Local:** `~/workspace/tools/opentoonz/` (24MB source)
- **Note:** We already have Tahoma2D (a fork of OpenToonz). This is the upstream original.
- **Build:** Requires Qt5, SuperLU, etc. See `~/workspace/tools/opentoonz/README.md`. Prebuilt binaries at https://opentoonz.github.io/e/download/opentoonz.html
- **Use for Cape Jones:** Traditional cut-out animation, Ghibli-style pipeline, alternative to Tahoma2D.
- **Status:** Source pulled. Use prebuilt binary for actual work (faster than compiling).

## 9. Krita AI Diffusion Plugin ✅ DOWNLOADED

- **What:** AI image generation inside Krita. Uses ComfyUI as backend. For AI-assisted frame generation.
- **Local:** `~/workspace/tools/krita-ai-diffusion/krita_ai_diffusion-1.53.0.zip` (3.1MB)
- **Version:** 1.53.0 (latest)
- **Install:** In Krita → Tools → Scripts → Import Python Plugin from File → select the ZIP → restart Krita → Settings → Dockers → AI Image Generation.
- **Backend:** Uses ComfyUI (our install at `ai-video/comfyui/` can serve as the backend).
- **GPU:** Needs 6GB+ VRAM for local use. On our CPU VM, connect to a remote ComfyUI server on Kaggle.
- **Use for Cape Jones:** AI-assisted background painting, texture generation, frame cleanup.
- **Status:** Downloaded. Install into Krita when needed.

---

## Already Have (Verified Working)

| Tool | Location | Status |
|------|----------|--------|
| FFmpeg | system | ✅ Working (backbone of pipeline) |
| Blender 4.0.2 + Grease Pencil | `~/workspace/tools/blender/` | ✅ Working (headless via xvfb) |
| Krita 6.0.4 | `~/workspace/tools/krita-6.0.4/` | ✅ Extracted |
| RIFE (CLI) | `~/workspace/tools/rife-v46/` | ✅ Working on Kaggle GPU (1.3 min for 216 pairs) |
| ToonCrafter | `~/workspace/tools/tooncrafter/` | ✅ Tuned, Kaggle-ready |

---

## GPU Compatibility Summary

| Tool | Kaggle T4 (16GB) | Needs Better GPU |
|------|-------------------|------------------|
| Wan 2.2 (5B) | ✅ | 14B needs 40GB+ |
| LTX-Video (fp8) | ✅ | — |
| Mochi 1 | ✅ (cpu_offload) | Faster on A100 |
| ComfyUI + VFI | ✅ | — |
| HunyuanVideo | ⚠️ GP version only | Full needs 80GB (A100/H100) |
| Cascadeur | N/A (desktop app) | — |
| OpenToonz | N/A (desktop app) | — |
| Krita AI Diffusion | ✅ (via remote ComfyUI) | Local needs 6GB+ VRAM |

---

## Pipeline Integration

**Current pipeline:** `FlipaClip → flipaclip_post.sh → ToonCrafter/RIFE (Kaggle) → finish.py → delivery`

**New capabilities to wire in:**
- [ ] Wan 2.2 / LTX-Video for AI background generation → feed into compositing stage
- [ ] ComfyUI VFI as alternative interpolation backend
- [ ] Krita AI Diffusion for background painting (connect to Kaggle ComfyUI server)
- [ ] Mochi 1 for smooth motion reference clips
- [ ] Cascadeur for 3D action reference → trace for 2D

**Next step:** Build Kaggle notebooks for Wan 2.2 and LTX-Video background generation (same pattern as the RIFE/ToonCrafter notebooks).

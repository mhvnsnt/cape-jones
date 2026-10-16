# Complementary Stack — Everything That Teams With Our Pipeline

Pulled 2026-10-16. Every tool here complements the existing Cape Jones production pipeline.
Free/open-source only. GPU work targets Kaggle T4.

---

## 1. LIP SYNC (the missing piece — now filled)

### LatentSync `tools/latentsync/`
- **What:** End-to-end AI lip sync (ByteDance). Audio + video in, lip-synced video out.
- **License:** Apache 2.0 (commercial OK)
- **Why:** Works on animated characters, not just real faces. No usage limits.
- **GPU:** Needs GPU → Kaggle T4. Model: `ByteDance/LatentSync-1.6` on HuggingFace.
- **Use case:** Cape Jones dialogue scenes. Feed a FlipaClip face close-up + voice audio → synced mouth.
- **Kaggle setup:** Clone repo, pip install requirements, download model from HF, run inference script.

### OpenFaceFX `tools/openfacefx/`
- **What:** Audio + transcript → viseme animation curves. MIT, numpy-only (runs on CPU!).
- **Why:** Outputs directly to **OpenToonz/Moho `.dat`** (Preston-Blair mouth names), **Rhubarb TSV/JSON**, Papagayo `.pgo`.
- **Use case:** Generate mouth-shape cue sheets for hand-drawn dialogue. The `.dat` output drops straight into OpenToonz/Tahoma2D.
- **Install:** `pip install openfacefx` or `pip install -e .` from the cloned repo.
- **Example:** `python -m openfacefx naive --text "hello" --wav voice.wav -o mouth.dat`

### Rhubarb Lip Sync (documented, download on Kaggle)
- **What:** Industry-standard game-dev lip sync. Outputs JSON mouth cues.
- **Why:** 5 seconds CPU per 30s clip. Every 2D pipeline knows its format.
- **Download:** https://github.com/DanielSWolf/rhubarb-lip-sync/releases (Linux zip timed out on VM — grab it on Kaggle)
- **Note:** OpenFaceFX can emit Rhubarb-compatible output, so this is optional.

### MuseTalk `tools/musetalk/`
- **What:** MIT-licensed lip sync, commercial use OK.
- **Why:** Backup/alternative to LatentSync.
- **Status:** ✅ Cloned (34MB)

---

## 2. COMFYUI CUSTOM NODES

### VFI (Video Frame Interpolation) `tools/comfyui-vfi-node/`
- **What:** RIFE frame interpolation as ComfyUI nodes.
- **Install:** Copy to `ComfyUI/custom_nodes/`, pip install requirements, place `flownet.pkl` in `rife/train_log/`.

### AnimateDiff-Evolved `tools/comfyui-animatediff-evolved/`
- **What:** Improved AnimateDiff for ComfyUI. Animate still images with motion modules.
- **Models needed (download on Kaggle):** Motion modules from https://huggingface.co/guoyww/animatediff → `ComfyUI/models/animatediff_models/`
- **Use case:** Bring a Cape Jones keyframe to life, generate background loops.

---

## 3. AGENTIC VIDEO PRODUCTION

### OpenMontage `tools/openmontage/`
- **What:** "World's first open-source agentic video production system." 12 pipelines, 100+ tools, 700+ agent skill files.
- **License:** AGPL-3.0
- **Why:** This is the closest thing to what we're building — an AI agent that runs video production end-to-end. Study its pipeline architecture, steal its patterns.
- **Status:** ✅ Cloned (161MB). Has AGENTS.md, CLAUDE.md, CODEX.md — agent skill files to study.

### reelmimic `tools/reelmimic/`
- **What:** "Show it a video you love. Get a new video in the same style." AI crew plans, builds and reviews.
- **Tags:** 2d-animation, ai-video, style-transfer
- **Status:** ✅ Cloned (73MB)
- **Use case:** Style-match reference footage for Cape Jones segments.

### ai-video-captions `tools/ai-video-captions/`
- **What:** Free AI video caption generator. 6 trending styles (Hormozi, MrBeast, Karaoke), word-level animation, 100+ languages. Whisper + FFmpeg.
- **Status:** ✅ Cloned (4.4MB)
- **Use case:** Social clips, promo cuts for the show.

---

## 4. 3D ASSETS FOR THE 3D SEGMENT

Owner's 3D segment (2026-10-16): 3D Cape Jones in 3D living room, LED remote, lights changing colors, 15 seconds.

### Quaternius CC0 Packs (need browser download — JS-driven itch.io widget)
Download from https://quaternius.com (all CC0, free for commercial use):
1. **Ultimate House Interior Pack** (`/packs/ultimatehouseinterior.html`) — living room furniture
2. **Ultimate Furniture Pack** (`/packs/ultimatefurniture.html`) — additional furniture
3. **Simple Buildings Pack** (`/packs/simplebuildings.html`) — ATHF-style house exterior
4. **Universal Animation Library 2** — humanoid animations for the 3D character
5. **Ultimate Animated Character Pack** — backup character models

### Other CC0 3D sources (documented)
- **Kenney.nl** (https://kenney.nl/assets) — all CC0, huge library
- **KayKit** (https://kaylousberg.itch.io) — CC0 interior/environment packs
- **Khronos glTF Sample Assets** — CC0/CC-BY furniture and architecture
- **Poly Pizza** (https://poly.pizza) — all CC0, search "living room", "sofa", "TV"

---

## 5. VERTICAL SCALING (doing more with what we have)

### Batch processing
- OpenFaceFX has built-in batch mode: `python -m openfacefx batch --dir voice/ --out tracks/ --jobs 8`
- **`post-pipeline/batch_process.sh`** ✅ Written and syntax-checked. Takes a directory of FlipaClip exports, runs `flipaclip_post.sh` + `finish.py` on each. Logs successes/failures, continues past errors.
- Usage: `batch_process.sh <input_dir> <output_dir> [grade] [led_preset]`

### Kaggle queue management
- Current pattern: one notebook per job, manual browser run.
- **TODO:** Kaggle API token would enable automated queue submission. Owner needs to generate one at kaggle.com/settings.

### Automated QC
- `finish.py` already has basic QC.
- **Pulled earlier:** `tools/ai-qc/` — check what's in there and wire it deeper.

---

## 6. HORIZONTAL SCALING (new capabilities)

| Capability | Tool | Status |
|---|---|---|
| Lip sync (AI video) | LatentSync | Cloned, needs Kaggle setup |
| Lip sync (cue sheets) | OpenFaceFX | Cloned, pip-installable, CPU-ready |
| Lip sync (classic) | Rhubarb | Documented, download on Kaggle |
| Character animation | Wan2.2-Animate-14B | Pulled earlier, Kaggle guide exists |
| Pose transfer | one-to-all-animation | Pulled earlier |
| Fast previz | LTX-Video | Pulled earlier, Kaggle guide exists |
| Agentic production | OpenMontage | Cloning |
| 3D living room | Quaternius packs | Needs browser download |

---

## 7. GEMINI LIST DOUBLE-CHECK

| Gemini item | Our status |
|---|---|
| Wan 2.2 | ✅ Pulled, Kaggle guide written |
| HunyuanVideo | ✅ Documented (too heavy for T4, needs better GPU) |
| Mochi 1 | ✅ Documented (20GB+ VRAM needed, photorealistic focus) |
| LTX-Video | ✅ Pulled, Kaggle guide written |
| ComfyUI-Frame-Interpolation | ✅ ComfyUI pulled, VFI nodes pulled |
| FFmpeg | ✅ Backbone of pipeline |
| Unreal Engine 5 | ⏳ Pull in progress (separate task) |
| Blender | ✅ Installed |
| Cascadeur | ⏳ Browser download in progress (separate task) |
| OpenToonz | ✅ Have Tahoma2D (better fork) |
| Krita + AI Diffusion | ✅ Krita installed, AI plugin in progress (separate task) |

---

## 8. 2026 NEW RELEASES (from GitHub trending)

- **OpenMontage** (Oct 2026, 269★) — agentic video production. Cloning.
- **reelmimic** (Oct 2026, 1,265★) — "show it a video you love, get a new video in the same style." 2D-animation tagged. **TODO: pull this.**
- **ai-video-captions** — Whisper + FFmpeg animated captions (Hormozi/MrBeast styles). **TODO: pull for social clips.**
- **awesome-video-skills** — curated video-making skills for AI agents. **TODO: review for pipeline ideas.**

---

## Pipeline integration

Updated pipeline with new capabilities:

```
FlipaClip → flipaclip_post.sh (cleanup → interpolate) → finish.py (grade → QC → audio)
                                                                    ↓
NEW: Dialogue → OpenFaceFX/LatentSync → lip-synced video → finish.py
NEW: 3D segment → Blender + Quaternius assets → composite → finish.py
NEW: Batch → batch_process.sh → full pipeline per file
```

---

## TODO (for parent agent)

1. **Browser downloads needed:**
   - Quaternius packs (5 packs from quaternius.com — JS-driven itch.io widget):
     - Ultimate House Interior Pack (`/packs/ultimatehouseinterior.html`)
     - Ultimate Furniture Pack (`/packs/ultimatefurniture.html`)
     - Simple Buildings Pack (`/packs/simplebuildings.html`)
     - Universal Animation Library 2
     - Ultimate Animated Character Pack
   - Cascadeur (already tasked separately)
2. **Kaggle setup guides to write:**
   - LatentSync inference notebook (model: `ByteDance/LatentSync-1.6` on HF)
   - MuseTalk inference notebook (backup)
   - ComfyUI + VFI nodes + AnimateDiff-Evolved on Kaggle T4
3. **Wire into pipeline:**
   - OpenFaceFX `.dat` output → Tahoma2D/OpenToonz mouth shapes (for dialogue scenes)
   - LatentSync → `finish.py` as a `--lipsync` stage
   - `batch_process.sh` tested on real batch
4. **Done this task:** ✅ reelmimic, ✅ ai-video-captions, ✅ batch_process.sh, ✅ all lip-sync tools, ✅ ComfyUI nodes, ✅ OpenMontage

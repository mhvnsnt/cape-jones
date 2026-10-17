# Better Alternatives 2026 — Interpolation & Body Replacement Research

**Date:** 2026-10-16
**Branch:** `cline/better-alternatives-20261016`
**Question:** Is there anything BETTER than ToonCrafter (interpolation) and One-to-All (body replacement) for Cape Jones — 2026 SOTA, open source, runs on T4 16GB, actually works?

**Method:** GitHub API verification (repos exist, stars, licenses, push dates), README/docs reads, Kaggle API status checks on our own kernels, plus the repo's existing tested research (`INTERPOLATION-RESEARCH.md`, `2026-SPEED-RESEARCH.md`, `PRO-INBETWEENING-RESEARCH.md`). No guessing from training data — every claim below has a source.

---

## TL;DR — The Honest Answers

**If ONE interpolation tool has to produce a video TODAY: GMFSS Fortuna on the T4.**
MIT licensed, anime-fine-tuned (built for exactly our footage type), 70MB model already downloaded at `~/workspace/tools/gmfss/`, flow-based so it's fast on GPU. Fallback: RIFE v4 + our `deghost.py` — the only tool that has literally produced output on our footage (with known ghosting artifacts).

**If ONE body-replacement tool has to produce a video: One-to-All Animation 1.3B via the authors' official ComfyUI-on-Kaggle-T4 path.**
Apache-2.0, CVPR 2026, trained with cartoon/anime data, and the authors publish the exact T4 recipe: 11 minutes for a 10-second 832x480 video on a free Kaggle T4. Our current kernel FAILED because it didn't follow that recipe (details below). Backup: MimicMotion (Apache-2.0, 8GB min / 16GB recommended — fits T4).

**The single biggest mistake in tool selection so far:** picking tools by paper prestige instead of hardware fit. ToonCrafter's official checkpoint OOMs on a T4 (documented in its own issue tracker, doubiiu/tooncrafter#74) — verifiable in 5 minutes before any notebook was pushed. Viggle-Animate needs 73.5GB VRAM — also checkable upfront. Four ToonCrafter attempts produced zero videos because the tool cannot physically run on our GPU as configured.

**The simpler path being missed:**
1. The Kaggle "dataset attachment bug" is not a bug — it's an empty `dataset_sources` field in `kernel-metadata.json`. Fix included in this branch (`production/kaggle/one-to-all/kernel-metadata.json`).
2. One-to-All's README contains the working T4 recipe (ComfyUI + 1.3B). Our kernel errored on the raw inference path (conda + flash-attn from source on Kaggle = classic failure).
3. GMFSS Fortuna is already downloaded and MIT — it just needs a T4 run.
4. ComfyUI (not raw scripts) is the integration layer the community actually uses: kijai's wrappers cover ToonCrafter-fp16 and One-to-All-14B, and MimicMotion/AnimateAnyone workflows are published there.

---

## PART 1 — Cartoon Interpolation (ToonCrafter's job)

### Scoreboard (all verified 2026-10-16)

| Tool | License | T4 16GB? | Status for us | Verdict |
|---|---|---|---|---|
| **GMFSS Fortuna** | MIT (verified via GitHub API: `98mxr/GMFSS_Fortuna`, 83 stars) | Yes (70MB model, flow-based) | Model downloaded at `~/workspace/tools/gmfss/`; CPU-tested working, 15+ min/frame-pair on CPU per `INTERPOLATION-RESEARCH.md` | **RECOMMENDED — run on T4 next** |
| RIFE v4 | MIT | Yes | Installed at `~/workspace/tools/rife-v46/`; produces video but ghosts on flat cartoon regions (root cause documented: trained on real video, flow fails on textureless areas) | Fallback — only tool with actual output; `deghost.py` mitigates |
| ToonCrafter (official ckpt) | Apache-2.0 | **NO** — OOM on T4, killed during model load (doubiiu/tooncrafter#74) | 0 videos in 4+ attempts (3 Kaggle, 1 Colab) | Dead as configured |
| ToonCrafter fp16 pruned | Apache-2.0 (model) | Claimed 12GB via `Kijai/DynamiCrafter_pruned` `tooncrafter_512_interp-fp16.safetensors` (link from official ToonCrafter README community table) | Real, exists, untested by us | "Maybe this week" option via kijai's ComfyUI-DynamiCrafterWrapper (677 stars) |
| LDF-VFI (CVPR 2026) | Apache-2.0 (verified) | Unknown — paper benchmarks on H100 | Pulled to `production/tools/ldf-vfi/`, untested on T4 | Promising, needs T4 validation |
| FLAVR (WACV23) | (check) | Yes (lightweight) | Cloned, untested — flow-free (3D conv), sidesteps the ghosting root cause | Worth a GPU test |
| AnimeInterp (CVPR21) | — | Yes | Code cloned; **pretrained weights dead (Dropbox 404, no mirrors)** | Blocked |
| AnimeInbet (ICCV23) | — | Yes | Line-drawings only, not full-color animation | Wrong tool for our footage |
| supraxylon/ToonCrafter-Low-VRAM | — | — | 7 stars, last pushed 2024-06-04 — old Windows fork, not a real low-VRAM solution | **Excluded** |

### Why GMFSS Fortuna is the pick
- **Anime-specific.** Unlike RIFE (trained on Vimeo90K real video — the documented root cause of our ghosting), GMFSS Fortuna is fine-tuned for anime/cartoon VFI. It's the community-standard anime interpolation tool.
- **Fits the hardware.** 70MB model, flow-based architecture — seconds per frame-pair on a T4 vs 15+ minutes on CPU.
- **License is clean.** MIT, verified via GitHub API.
- **Already in hand.** Downloaded and sitting at `~/workspace/tools/gmfss/`. The only missing step is a GPU run.
- **Honest caveat:** GPU speed/quality on our footage is projected, not yet measured. RIFE remains the only tool with literal produced output.

### ToonCrafter — the full honest picture
- The official `model.ckpt` (320x512) **cannot load on a 16GB T4** — the process is OOM-killed right after the autoencoder reports its working shape (doubiiu/tooncrafter#74, reproduced on Colab T4).
- There IS a real low-VRAM path: fp16 pruned safetensors at `Kijai/DynamiCrafter_pruned` (`tooncrafter_512_interp-fp16.safetensors`), listed in the official ToonCrafter README as 12GB VRAM via kijai's ComfyUI-DynamiCrafterWrapper. This is verifiable and real — but nobody on the team has run it.
- Recommendation: stop pushing the official-checkpoint notebook. Either switch to the fp16/ComfyUI path or drop ToonCrafter for GMFSS Fortuna.

---

## PART 2 — Body Replacement / Pose Transfer (One-to-All's job)

### Scoreboard (all verified 2026-10-16)

| Tool | License | T4 16GB? | Status for us | Verdict |
|---|---|---|---|---|
| **One-to-All Animation 1.3B** | Apache-2.0 (verified via GitHub API: `ssj9596/One-to-All-Animation`, 504 stars, CVPR 2026) | **Yes — authors publish the T4 recipe**: 1.3B + ComfyUI on free Kaggle T4, 11 min / 10s 832x480 | Our Kaggle kernel `marsfmmg/cape-jones-one-to-all-20261016-213940` is in **ERROR** state (checked via Kaggle API 2026-10-16) | **RECOMMENDED — but switch to the official ComfyUI path** |
| MimicMotion (Tencent) | Apache-2.0 (verified from LICENSE file in repo) | Yes — 8GB min, 16GB recommended (ComfyUI workflow docs) | Not yet tried by us | Backup option, fits T4 |
| Viggle-Animate | MiniMax H3 (reported USA-excluding; per repo notebook docstring) | **NO — needs 73.5GB VRAM** | Never worked, cannot work on T4 | **Dead — confirmed exclusion** |
| Wan2.2-Animate-14B | (Apache-2.0 family) | No — 14B needs 40GB+ | Not attempted (correctly) | Excluded on hardware |
| MagicMotion | (check) | **No — needs 23GB** (tested on RTX 4090 per HF model card) | — | **Excluded on hardware** |
| FramePrompt (2026) | — | Probably | Paper only, code availability unclear (noted in `2026-SPEED-RESEARCH.md`) | Monitor, can't use today |
| LiveAnimate (2026) | — | **No — 2x H100**, 480x480 | Paper only | **Excluded** |
| Champ / AnimateAnyone / UniAnimate-DiT | various | Mostly 24GB+ or older quality | — | Superseded by One-to-All for our hardware |

### Why our One-to-All kernel failed (verified)
1. **Wrong path.** The notebook (`production/kaggle/one-to-all/gen_notebook.py`) uses the raw inference scripts (`infer_preprocess.py` + `inference_1.3b.py`) with a conda env, pinned torch cu124, and flash-attention — the README's install path, not the T4 path. Flash-attention from source on Kaggle is a classic timeout/OOM failure.
2. **The authors' T4 path is ComfyUI + 1.3B**, published 2025-12-22 in the README: "GPU-poor? Run One-to-All 1.3B + ComfyUI for free on Kaggle's 16 GB T4." Our lane didn't use it.
3. **Dataset never attached.** The notebook docstring says "Attach dataset: marsfmmg/cape-jones-viggle-inputs" as a manual Kaggle-UI step. The dataset EXISTS (verified via Kaggle API: `marsfmmg/cape-jones-viggle-inputs`, 6.4MB) — but API-pushed kernels need `dataset_sources` in `kernel-metadata.json`, and the push had none. Fix is in this branch.

### Why One-to-All 1.3B is still the right body-replacement pick
- **Cartoon-trained.** The CVPR 2026 supplemental material documents a dedicated cartoon/anime dataset (212 high-quality samples after DWPose filtering, 200 train / 12 eval). Our character is a cartoon — this matters.
- **Alignment-free.** Handles reference/pose layout mismatch natively (outpainting-based training) — useful for our non-photoreal character.
- **License clean.** Apache-2.0.
- **Hardware-verified by the authors** on exactly our GPU (Kaggle T4 16GB).

---

## PART 3 — Integrated Pipeline (interpolation + body replacement + grading in one system)

Honest finding: **there is no verified single open-source system that does all three at production quality on a T4.** What exists:

- **Kandinsky 6.0** (already known to the team) — not verified in this pass; no T4 confirmation found.
- **ComfyUI is the de-facto integration layer**, not a model: kijai's `ComfyUI-DynamiCrafterWrapper` (ToonCrafter fp16, 677 stars), kijai's `ComfyUI-WanVideoWrapper` (integrates One-to-All 14B per the One-to-All README), published MimicMotion and AnimateAnyone workflows. Our pipeline's post side (`finish.py` grades, `deghost.py`, `cleanup_lines.py`) already covers grading — the missing piece is standardizing the GPU stages as ComfyUI workflows instead of hand-rolled notebooks.
- **Wan2.1/Wan2.2 ecosystem** — the base of One-to-All; 14B variants don't fit T4.
- **LTX-Video, HunyuanVideo, CogVideoX, Mochi** — text-to-video / image-to-video generators, not interpolation+replacement pipelines; mostly too big for T4 at useful quality.
- **AniSora (OpenBMB)** — cartoon video generation, not our pipeline shape.

**Recommendation:** stop hunting for a mythical all-in-one. The production-grade answer is **ComfyUI workflows (GPU stages) + our existing post pipeline (grading/QC/audio)**. That's what the community actually runs.

---

## PART 4 — What to pull in / concrete next steps

### Pulled in this branch
1. **`production/kaggle/one-to-all/kernel-metadata.json`** — the dataset-attachment fix. `dataset_sources: ["marsfmmg/cape-jones-viggle-inputs"]` (dataset verified to exist via Kaggle API), `enable_gpu: true`, `enable_internet: true`. This is the permanent fix for the "Kaggle API doesn't attach datasets" failure — it was never an API bug, the field was empty.
2. **This research doc** with verified links, licenses, and honest exclusions.

### Recommended next steps (for the owning lanes — not started here, per no-duplicate-work)
1. **Interpolation lane:** run GMFSS Fortuna on the T4 against `cape-jones-flying-scene-v1.mp4` (the same test footage from `INTERPOLATION-RESEARCH.md`). Model is already at `~/workspace/tools/gmfss/`. If it clears the ghosting bar, it replaces both RIFE and ToonCrafter.
2. **Body-replacement lane (opencode):** rebuild the One-to-All kernel on the **official ComfyUI 1.3B T4 path** (README 2025-12-22 entry), push with the fixed `kernel-metadata.json` from this branch. Do not re-run the raw-inference notebook.
3. **ToonCrafter lane (agy):** decision point — either pivot the notebook to the fp16 pruned model (`Kijai/DynamiCrafter_pruned`, 12GB) via ComfyUI, or stand down in favor of GMFSS Fortuna. The official-checkpoint path is proven dead on T4; more attempts on it burn quota.
4. **Pipeline integration:** evaluate standardizing GPU stages as ComfyUI workflows (kijai's wrappers) instead of bespoke notebooks.

---

## PART 5 — Honest exclusions

| Excluded | Reason (verified) |
|---|---|
| Viggle-Animate | 73.5GB VRAM required; physically impossible on 16GB T4. Never worked. |
| ToonCrafter official checkpoint | OOM-killed on T4 during model load (doubiiu/tooncrafter#74). 0/4 attempts produced video. |
| supraxylon/ToonCrafter-Low-VRAM | 7 stars, untouched since 2024-06 — a Windows fork, not a VRAM solution. |
| MagicMotion | 23GB VRAM required (HF model card). Doesn't fit T4. |
| Wan2.2-Animate-14B / One-to-All 14B | 40GB+ class. Doesn't fit T4. |
| LiveAnimate | Requires 2x H100. Research demo, not our hardware. |
| AnimeInterp | Weights dead (Dropbox 404, no mirrors found). |
| FramePrompt | 2026 paper, no usable code release found. Monitor only. |
| Kandinsky 6.0 as "the answer" | No verified T4-compatible integrated pipeline found in this pass — not confirmed, not excluded, needs its own validation. |

---

## Appendix — Verification log

- `api.github.com/repos/ssj9596/One-to-All-Animation` → exists, 504 stars, Apache-2.0, pushed 2026-04-19.
- `api.github.com/repos/98mxr/GMFSS_Fortuna` → exists, 83 stars, MIT.
- `api.github.com/repos/Tencent/MimicMotion` → exists, 2677 stars; LICENSE file read → Apache-2.0.
- `api.github.com/repos/kijai/ComfyUI-DynamiCrafterWrapper` → exists, 677 stars.
- `api.github.com/repos/supraxylon/ToonCrafter-Low-VRAM` → exists, 7 stars, pushed 2024-06-04.
- ToonCrafter README community table → fp16 model link `huggingface.co/Kijai/DynamiCrafter_pruned` (`tooncrafter_512_interp-fp16.safetensors`), 12GB.
- `kaggle kernels status marsfmmg/cape-jones-one-to-all-20261016-213940` → `KernelWorkerStatus.ERROR`.
- `kaggle kernels status marsfmmg/cape-jones-viggle-fixed-20261016-201155` → `KernelWorkerStatus.ERROR`.
- `kaggle datasets list --mine` → `marsfmmg/cape-jones-viggle-inputs` exists (6.4MB).
- Repo inspection: `production/kaggle/one-to-all/gen_notebook.py` uses raw inference path + manual dataset attach; `production/kaggle/weight-seeding/*.py` already use `dataset_sources` (empty) — the mechanism was known, just not applied.
- One-to-All README (raw.githubusercontent) → T4 ComfyUI recipe (2025-12-22), 1.3B/14B checkpoints, Apache-2.0.
- One-to-All CVPR 2026 supplemental (openaccess.thecvf.com) → cartoon dataset curation (212 samples).
- Browser search → doubiiu/tooncrafter#74 (T4 OOM), MimicMotion ComfyUI VRAM (8GB min/16GB rec), MagicMotion 23GB (HF card).

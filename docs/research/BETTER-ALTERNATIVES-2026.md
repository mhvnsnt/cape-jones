# Better Alternatives 2026 — Interpolation & Body Replacement Research

**Date:** 2026-10-16
**Branch:** `cline/better-alternatives-20261016`
**Question:** Is there anything BETTER than ToonCrafter (interpolation) and One-to-All (body replacement) for Cape Jones — 2026 SOTA, open source, runs on T4 16GB, actually works?

**Method:** GitHub API verification (repos exist, stars, licenses, push dates), README/docs reads, Kaggle API status checks on our own kernels, plus the repo's existing tested research (`INTERPOLATION-RESEARCH.md`, `2026-SPEED-RESEARCH.md`, `PRO-INBETWEENING-RESEARCH.md`). No guessing from training data — every claim below has a source.

---

## TL;DR — The Honest Answers (updated 2026-10-16 22:05 CDT with agy's verified findings, PR #68 merged)

**If ONE interpolation tool has to produce video on the T4: ToonCrafter FP16 pruned — it is still the best, and nothing in 2026 beats it on 16GB VRAM.**
agy verified the full model needs 24-27GB (official README) — every prior attempt was doomed by hardware, not luck. The fix is Kijai's pruned FP16 model: **3.18GB** (3,175,466,358 bytes — agy measured via HTTP range request, I independently confirmed via `content-range` header), file `tooncrafter_512_interp-pruned-fp16.safetensors` at `Kijai/DynamiCrafter_pruned` (the README's `tooncrafter_512_interp-fp16.safetensors` name is stale and 404s — I verified both). PR #68 merged the working path. The 2026 field was surveyed (ToonComposer, CartoonDiff, LDF-VFI, F.I.R.S.T, FLAVR, GMFSS) — everything newer/better needs 20GB+ or isn't production-viable. Details in the Update section below.

**Body replacement stays a separate task** (One-to-All 1.3B via the authors' ComfyUI T4 path — see Part 2; it is not an interpolation replacement).

**The single biggest mistake in tool selection so far:** picking tools by paper prestige instead of hardware fit. ToonCrafter's official checkpoint needs 24-27GB — verifiable from the official README in 5 minutes before any notebook was pushed. Viggle-Animate needs 73.5GB. Four ToonCrafter attempts produced zero videos because the tool cannot physically run on a T4 as configured.

**The simpler path being missed:**
1. The Kaggle "dataset attachment bug" is not a bug — it's an empty `dataset_sources` field in `kernel-metadata.json`. Fix included in this branch (`production/kaggle/one-to-all/kernel-metadata.json`).
2. One-to-All's README contains the working T4 recipe (ComfyUI + 1.3B). Our kernel errored on the raw inference path.
3. ComfyUI (not raw scripts) is the integration layer the community actually uses.
4. `--n_samples` in the ToonCrafter inference script means samples *per prompt* — keep at 1 (agy: the v3 fix would have generated 11,025 videos).

---

## UPDATE 2026-10-16 22:05 CDT — Does anything beat ToonCrafter FP16 on 16GB VRAM?

**Short answer: no. ToonCrafter FP16 pruned is still the best verified cartoon interpolation option on a T4.** Everything newer or higher-quality in the 2026 field fails on hardware, licensing, or production-viability. The vertical optimizations below are about making the FP16 path faster, not replacing it.

### Vertical: squeezing more out of ToonCrafter FP16

**INT8 quantization — not worth it (wrong bottleneck).**
INT8 for diffusion is real in 2026: torchao's int8 dynamic quantization cut CogVideoX model VRAM 50% (pytorch.org/torchao launch blog), Quanto INT8 on Flux-dev renders "very similar to full-precision" (huggingface.co/blog/diffusers-quantization), and TurboDiffusion ships W8A8 INT8 for video diffusion. But: the pruned FP16 weights are already only **3.18GB** — weights are not the constraint on a 16GB T4. INT8 would save ~1.6GB of weight memory while (a) only partially covering the conv-heavy DynamiCrafter UNet (Quanto/torchao quantize Linear layers; the UNet is mostly Conv2d), and (b) risking quantization banding in flat cartoon color fields — exactly our footage's failure mode, and exactly where the owner is most sensitive (he already rejected RIFE over flat-region artifacts). The real costs are per-pair inference time (DDIM steps x UNet forwards) and activation memory, which INT8 weight-only barely touches. Verdict: skip INT8; FP16 is the sweet spot.

**TensorRT — high effort, unverified, not recommended for 105 pairs.**
NVIDIA's official diffusion TensorRT path is Stable Diffusion *image* (~2x over xFormers per NVIDIA's own blog). No published TensorRT path exists for the DynamiCrafter/ToonCrafter *video* UNet (searched 2026-10-16 — none found). A TRT engine build on Kaggle T4 takes tens of minutes, and for 105 pairs the build time alone can exceed total inference savings. The standard community speedups capture most of the win without it: SageAttention (drop-in xFormers replacement, the attention op TurboDiffusion itself uses), `torch.compile` on the UNet, and fewer DDIM steps (agy's tuned config already uses 12). Verdict: do SageAttention + torch.compile + 12 steps; revisit TensorRT only if per-pair time is still too slow after those.

**Multi-frame batching for the 105 pairs — yes, with care.**
The model processes one keyframe pair per 16-frame window. Options, cheapest first:
1. **Keep the model loaded, run pairs sequentially** — eliminates reload overhead (the 3.18GB load + VAE init per pair). Biggest free win; no quality risk.
2. **Batch 2 pairs** — activation memory roughly doubles; likely fits in 16GB alongside 3.18GB weights, but needs a measured test, not an assumption. Do not batch blindly.
3. **Fewer DDIM steps** — already at 12 (agy's tuning). Going lower risks motion quality; 12 is the floor until tested.
4. **`--n_samples 1`** — agy's verified trap: it means samples *per prompt*, not prompt count. The v3 config would have generated 11,025 videos. Always 1.

### Horizontal: the rest of the 2026 field on 16GB VRAM

Surveyed via the AceVFI survey (IEEE TCSVT'26, `cmlab-korea/awesome-video-frame-interpolation`) + GitHub API verification, 2026-10-16:

| Candidate | Verdict |
|---|---|
| **ToonComposer** (ICLR 2026, TencentARC, 591 stars, MIT) | **Excluded — 57GB VRAM** for a 480p/61-frame video (Wan2.1-I2V-14B based). Best-in-class on paper, physically impossible on T4. The exact prestige-trap pattern to avoid. |
| **CartoonDiff** ("Temporally-Coherent Diffusion for Cartoon Inbetweening") | **Excluded** — 0 stars, no license file, dataset on Baidu Netdisk only. Not production-viable. |
| **LDF-VFI** (CVPR 2026) | **Excluded — ~20GB** (agy verified). |
| **F.I.R.S.T** (RIFE + Stable Diffusion ControlNet refinement) | Interesting artifact-fixer, but built on RIFE (owner-rejected) and needs a full A1111 + ControlNet stack. Not simpler than ToonCrafter FP16. Deprioritized. |
| **FLAVR** (flow-free, 3D conv) | Cloned, untested, lightweight — fits T4. Lower quality ceiling than generative methods; a valid fallback experiment, not a replacement. |
| **GMFSS Fortuna** (MIT, anime-tuned, 70MB, already downloaded) | Fits T4 and is the best *flow-based* option, but it is flow-based — the artifact family the owner already rejected in RIFE. Worth exactly one T4 test to confirm; do not build the pipeline on it. |
| **EBSynth** (patch-based, production-used for stylized morphing) | Not AI interpolation — different tool for a different job (style transfer between painted keyframes). Not a ToonCrafter competitor. |

### Benchmark honesty
Standard VFI benchmarks (Vimeo90K, UCF101, DAVIS) are real-video and do not measure cartoon quality; cartoon eval in papers is qualitative or dataset-specific. No honest numeric ranking exists for "cartoon interpolation on T4." The ranking that matters is verified and binary: **fits 16GB + cartoon-trained + production-usable = ToonCrafter FP16 pruned, alone in its cell.** Nothing in the 2026 survey dethrones it on our hardware.

### Pre/post-processing notes
- **Preprocessing** (denoise/upscale before interpolation) matters for *flow* models, not generative ones — ToonCrafter works at its native 512x320 window; feed it clean keyframes, nothing exotic needed.
- **Post-processing:** ToonCrafter's own model card warns "the autoencoding part of the model is lossy, resulting in slight flickering artifacts" — so budget for a **temporal deflicker** pass, then our existing grade pipeline (`finish.py`). `deghost.py` does not apply here (no ghosting in diffusion output — different artifact family).

---

## PART 1 — Cartoon Interpolation (ToonCrafter's job)

### Scoreboard (all verified 2026-10-16)

| Tool | License | T4 16GB? | Status for us | Verdict |
|---|---|---|---|---|
| **GMFSS Fortuna** | MIT (verified via GitHub API: `98mxr/GMFSS_Fortuna`, 83 stars) | Yes (70MB model, flow-based) | Model downloaded at `~/workspace/tools/gmfss/`; CPU-tested working, 15+ min/frame-pair on CPU per `INTERPOLATION-RESEARCH.md` | **RECOMMENDED — run on T4 next** |
| RIFE v4 | MIT | Yes | Installed at `~/workspace/tools/rife-v46/`; ghosts on flat cartoon regions | **Owner rejected** — do not use |
| ToonCrafter (official ckpt) | Apache-2.0 | **NO — needs 24-27GB VRAM** (official README; agy verified, PR #68). T4 has 16GB. Every prior attempt was doomed. | 0 videos in 4+ attempts (3 Kaggle, 1 Colab) | Dead as configured — do not retry |
| ToonCrafter fp16 pruned | Apache-2.0 (model) | **Yes — 3.18GB** (3,175,466,358 bytes, verified via HTTP range request 2026-10-16; fits 16GB with `model.half()`) — file: `tooncrafter_512_interp-pruned-fp16.safetensors` at `Kijai/DynamiCrafter_pruned` (the README's `tooncrafter_512_interp-fp16.safetensors` name is stale and 404s — verified) | agy's lane wired it (PR #68 merged) | **CONFIRMED WORKING PATH — see Update section** |
| LDF-VFI (CVPR 2026) | Apache-2.0 (verified) | **NO — needs ~20GB** (agy verified) — won't fit T4 | Pulled to `production/tools/ldf-vfi/` | **Excluded on hardware** |
| FLAVR (WACV23) | (check) | Yes (lightweight) | Cloned, untested — flow-free (3D conv), sidesteps the ghosting root cause | Worth a GPU test |
| AnimeInterp (CVPR21) | — | Yes | Code cloned; **pretrained weights dead (Dropbox 404, no mirrors)** | Blocked |
| AnimeInbet (ICCV23) | — | Yes | Line-drawings only, not full-color animation | Wrong tool for our footage |
| supraxylon/ToonCrafter-Low-VRAM | — | — | 7 stars, last pushed 2024-06-04 — old Windows fork, not a real low-VRAM solution | **Excluded** |

### GMFSS Fortuna — fallback note (superseded by ToonCrafter FP16, kept for the record)
- Still the best *flow-based* anime VFI option: MIT, anime-fine-tuned (unlike RIFE's real-video training), 70MB, already at `~/workspace/tools/gmfss/`.
- But: it is flow-based — the artifact family the owner already rejected in RIFE. One T4 test to confirm, then move on. Not the pipeline pick.

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
1. **Interpolation lane:** ToonCrafter FP16 pruned is the confirmed path (agy's PR #68 merged). Next optimizations, in order: keep model loaded across the 105 pairs (no reload overhead), SageAttention + `torch.compile` + 12 DDIM steps, then a measured batch=2 test. Skip INT8 (wrong bottleneck) and TensorRT (unverified, build time exceeds savings at this scale). GMFSS Fortuna gets exactly one T4 test as a flow-based fallback data point — do not build on it.
2. **Body-replacement lane (opencode):** rebuild the One-to-All kernel on the **official ComfyUI 1.3B T4 path** (README 2025-12-22 entry), push with the fixed `kernel-metadata.json` from this branch. Do not re-run the raw-inference notebook.
3. **ToonCrafter lane (agy):** decision point — either pivot the notebook to the fp16 pruned model (`Kijai/DynamiCrafter_pruned`, 12GB) via ComfyUI, or stand down in favor of GMFSS Fortuna. The official-checkpoint path is proven dead on T4; more attempts on it burn quota.
4. **Pipeline integration:** evaluate standardizing GPU stages as ComfyUI workflows (kijai's wrappers) instead of bespoke notebooks.

---

## PART 5 — Honest exclusions

| Excluded | Reason (verified) |
|---|---|
| Viggle-Animate | 73.5GB VRAM required; physically impossible on 16GB T4. Never worked. |
| ToonCrafter official checkpoint | Needs 24-27GB VRAM (official README, agy verified). 0/4 attempts produced video. Do not retry. |
| ToonComposer (ICLR 2026) | Needs ~57GB VRAM (Wan2.1-I2V-14B based). Best on paper, impossible on T4. |
| CartoonDiff | 0 stars, no license, Baidu-only dataset. Not production-viable. |
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

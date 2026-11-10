# PULLIN-LOG — tools/inference (AI/ML inference on our hardware)

Standing log: every item pulled in by the 2026-10-16 inference research dispatch.
Format per item: what / why it beats what we had / license / install+test evidence /
where it landed.

## 2026-10-16

### city96/ComfyUI-GGUF (vendored)
- **What:** ComfyUI custom node that loads GGUF-quantized diffusion models
  (UnetLoaderGGUF, DualCLIPLoaderGGUF, ...). Lets FLUX.1-dev and Wan 2.1 14B run in
  16GB VRAM via Q4/Q5 GGUFs.
- **Why:** Without it there is no T4-viable FLUX path in ComfyUI (full bf16 FLUX.1-dev
  is ~24GB). The node the whole GGUF-diffusion community standardizes on.
- **License:** Apache-2.0 (verified via GitHub API + LICENSE file in tree).
- **Evidence:** cloned 2026-10-16, pinned commit `6ea2651e7df66d7585f6ffee804b20e92fb38b8a`;
  `.git` stripped; `python3 -m py_compile` passes on `__init__.py`, `nodes.py`,
  `loader.py`; node class names + `INPUT_TYPES` verified against ComfyUI core.
- **Landed:** `tools/inference/third-party/ComfyUI-GGUF/`
- **Docs:** `tools/inference/comfyui-t4-runbook.md`,
  `docs/research/AI-INFERENCE-HARDWARE-2026.md` §2.2

### kaggle-llm-server.sh
- **What:** One-command bootstrap: downloads prebuilt llama.cpp CUDA binary
  (release b11696, ggml-org/llama.cpp — MIT) + a GGUF, starts `llama-server`
  (OpenAI-compatible API) on a Kaggle T4.
- **Why:** Replaces "figure out serving from scratch" every session; no compile step;
  the binary release asset list was verified 2026-10-16
  (`llama-b11696-bin-ubuntu-cuda-12.8-x64.tar.gz` exists).
- **License:** our own script; llama.cpp is MIT.
- **Evidence:** `bash -n` syntax check passes; default model URL verified live on HF
  (`unsloth/Qwen3-30B-A3B-GGUF`, file `Qwen3-30B-A3B-UD-IQ3_XXS.gguf` present, 33 files).
- **Landed:** `tools/inference/kaggle-llm-server.sh`
- **Docs:** `docs/research/AI-INFERENCE-HARDWARE-2026.md` §1.1, §4

### inference_client.py
- **What:** stdlib-only (`urllib`) OpenAI-compatible chat client — the single way our
  pipelines call any LLM endpoint (llama-server, Ollama, vLLM, SGLang).
- **Why:** Zero-dependency, works from any pipeline without pip installs.
- **License:** ours.
- **Evidence:** tested 2026-10-16 against a mock OpenAI-compatible server
  (`/health` + `/v1/chat/completions`): `health()` → True, `chat()` round-trip OK,
  RC 0. Real `llama-server` e2e pending a full model download (see below).
- **Landed:** `tools/inference/inference_client.py`
- **Docs:** `docs/research/AI-INFERENCE-HARDWARE-2026.md` §4

### comfyui-t4-runbook.md
- **What:** Step-by-step: ComfyUI install on Kaggle/Colab T4, GGUF node install from the
  vendored copy, exact model download commands (aria2), VRAM notes, API sketch.
- **Why:** Turns the research into a runnable procedure anyone (or any agent) can follow.
- **Evidence:** every model URL HEAD/GET-checked 2026-10-16 —
  `flux1-dev-Q4_0.gguf` (city96/FLUX.1-dev-gguf, live),
  `t5xxl_fp8_e4m3fn.safetensors` + `clip_l.safetensors` (comfyanonymous/flux_text_encoders, live),
  `ae.safetensors` (black-forest-labs/FLUX.1-schnell, gated → login note added),
  `wan2.1-i2v-14b-480p-Q5_K_S.gguf` (city96/Wan2.1-I2V-14B-480P-gguf, live),
  `umt5_xxl_fp8_e4m3fn_scaled.safetensors` + `wan_2.1_vae.safetensors`
  (Comfy-Org/Wan_2.1_ComfyUI_repackaged, live).
- **Landed:** `tools/inference/comfyui-t4-runbook.md`

### workflows/flux1-dev-q4-t4.json, workflows/wan21-14b-i2v-t4.json
- **What:** Ready-to-POST ComfyUI API workflows: FLUX.1-dev Q4 text-to-image;
  Wan 2.1 14B Q5 image-to-video.
- **Why:** Pipelines can queue renders without hand-building graphs.
- **Evidence:** JSON parses; all node links resolve; every node class + input name
  verified against the vendored ComfyUI-GGUF `INPUT_TYPES` and ComfyUI core sources
  fetched 2026-10-16 (`UnetLoaderGGUF`, `DualCLIPLoaderGGUF`, `CLIPLoader` type `wan`,
  `WanImageToVideo`, `CreateVideo`, `SaveVideo`). First GPU run still to be done on a
  real T4 (needs browser/Kaggle lane — flagged for parent).
- **Landed:** `tools/inference/workflows/`

### qlora-t4-runbook.md
- **What:** Fine-tuning recipes for the T4: Unsloth QLoRA (Colab), Axolotl YAML,
  FLUX LoRA via Ostris ai-toolkit (MIT), RVC character voices, VRAM cheat-sheet.
- **Why:** Gives the voice/art-style lanes a concrete training path instead of
  "QLoRA works on T4" hand-waving.
- **License notes:** Unsloth Apache-2.0, Axolotl Apache-2.0, ai-toolkit MIT.
- **Evidence:** commands transcribed from current (2026) upstream docs; Unsloth
  install string and `FastLanguageModel` API match unslothai/unsloth current README.
- **Landed:** `tools/inference/qlora-t4-runbook.md`
- **Docs:** `docs/research/AI-INFERENCE-HARDWARE-2026.md` §5

### Research doc
- **What:** `docs/research/AI-INFERENCE-HARDWARE-2026.md` — all five research topics +
  voice addendum, T4 constraints, decision tables, license log, sources.
- **Evidence:** every factual claim traces to a source listed in §9, all accessed
  Oct 2026 (GitHub API, HF API, release asset lists, 2026 benchmarks/roundups).
- **Landed:** `docs/research/AI-INFERENCE-HARDWARE-2026.md`

## Explicitly excluded (documented, not pulled)
- FLUX.1-dev/schnell **weights** — BFL non-commercial license. Referenced by URL only.
- XTTS-v2 (CPML non-commercial), F5-TTS weights (CC-BY-NC), Fish-Speech (research license).
- Wan2GP — no license declared (NOASSERTION). Documented only.
- ComfyUI itself (GPL-3.0) — referenced, not vendored. Our workflows are our own.
- TensorRT-LLM — NVIDIA-proprietary, 1–2 week setup; not worth it at our scale.
- TGI — maintenance mode; HF recommends vLLM/SGLang.

## Test evidence still open
- [ ] `llama-server` end-to-end with a real GGUF (model download in progress at pull
      time; CPU smoke test on local VM next)
- [ ] First GPU run of both ComfyUI workflows on a Kaggle/Colab T4 (needs GPU lane)

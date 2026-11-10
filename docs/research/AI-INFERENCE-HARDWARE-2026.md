# AI/ML Inference on Our Hardware — Research 2026-10-16

**Hardware in scope:** Kaggle (30 GPU-hrs/wk, T4 x2, 16GB VRAM each), Google Colab (free T4),
local VM (CPU only), owner's phone.
**Rule: never assume "no GPU" — check and use what's there.**
Prior related docs: GEMINI-PULL.md (Wan 2.2, LTX-Video, ComfyUI pulls), GEMINI-FULL-PULL.md
(HunyuanVideo, Mochi), TRACK-B-AUDIO-PULL.md (TTS/voice pipeline). This doc is the
**inference/runtime/quantization** angle — what runs, how to serve it, what quant to pick —
not another model-shopping list.

## 0. Executive summary — what to actually do

| Workload | Pick for T4 16GB | Why |
|---|---|---|
| LLM agent/coding backend | llama.cpp `llama-server` + Qwen3.x 30B-A3B MoE (UD IQ3_XXS / Q4_K_M) or 14B dense Q4_K_M | Single binary, OpenAI-compatible API, GGUF ecosystem, MIT |
| LLM production serving (multi-user) | vLLM (Apache-2.0); SGLang if agent traffic shares prefixes | vLLM is the 2026 default; SGLang ~29% better on shared-prefix agent/RAG traffic |
| Image gen | ComfyUI + city96/ComfyUI-GGUF + FLUX.1-dev GGUF Q4_0 (Apache-2.0 node; **FLUX weights = non-commercial license, see §8**) | Only FLUX path that fits 16GB comfortably |
| Video gen (quality) | ComfyUI + Wan 2.1 14B GGUF (Q5_K_S / Q4_K_M, Apache-2.0) | Proven on 16GB cards; T5 text encoder offloaded to CPU/RAM |
| Video gen (speed) | LTX-Video 2.x, 700M–2B class (Apache-2.0) | 10–20x faster than Wan-class; for iteration, not finals |
| Quant default | Q4_K_M; IQ4_XS when VRAM-tight; Q5_K_M/Q6_K if it fits | Best quality-per-VRAM in 2026 per multiple benchmarks |
| Fine-tune LLM on T4 | Unsloth QLoRA (Apache-2.0) | 2–5x faster, ~half VRAM vs stock; gpt-oss-20b QLoRA fits ~14GB |
| Art-style LoRA (FLUX) | Ostris ai-toolkit (MIT) on Kaggle T4 | FLUX LoRA trains in 16GB with the documented low-VRAM settings |
| Character voice models | RVC training on T4 (MIT arch) for trained voices; Chatterbox (MIT, already in our pipeline per TRACK-B) / IndexTTS-2.5 for zero-shot | XTTS-v2 and F5-TTS weights are **non-commercial — excluded** |

**T4-specific constraints (verified):** T4 is Turing sm_75 — **no FP8** (needs Ada/Blackwell),
no bf16 tensor-core matmuls. Use INT4/INT8 (AWQ/GPTQ) or GGUF K/I-quants. FP16 works.

## 1. Local LLMs — what runs well on a T4

### 1.1 Runners (2026 state, licenses verified via GitHub API)

- **llama.cpp** (ggml-org/llama.cpp, **MIT**) — the universal runner. `llama-server` gives an
  OpenAI-compatible `/v1/chat/completions` endpoint from one binary. Continuous batching,
  speculative decoding (incl. MTP draft heads), GGUF offload to CUDA. Best for single-user /
  pipeline use, CPU fallback on the local VM, and the phone-adjacent edge story.
- **Ollama** (ollama/ollama, **MIT**) — wraps llama.cpp; best dev ergonomics, `ollama run`,
  OpenAI-compatible API on :11434. Weaker concurrent throughput than vLLM-class engines.
  Good for the local VM / laptop dev loop.
- **vLLM** (vllm-project/vllm, **Apache-2.0**) — the 2026 default for production GPU serving:
  PagedAttention, continuous batching, AWQ/GPTQ/FP8 quants, OpenAI-compatible server,
  multi-LoRA serving. Runs on T4 (sm_75 supported). Pick when pipelines need concurrent
  requests. Note: `--gpu-memory-utilization` is preallocated, not a limit — one server per GPU.
- **SGLang** (sgl-project/sglang, **Apache-2.0**) — beats vLLM ~29% on shared-prefix workloads
  (agents, RAG, chatbots) via RadixAttention. Worth A/B-ing once our agent traffic is real.
- **TGI** — officially in maintenance mode; HF now recommends vLLM/SGLang. Do not start new
  work on it.
- **TensorRT-LLM** — max NVIDIA throughput (+30–50% over vLLM at saturation) but 1–2 weeks
  setup and vendor lock-in. Not worth it for our scale.

**Our serving decision:** `llama-server` on the Kaggle T4 for pipeline work (simplest, one
binary, GGUF-native). Graduate to vLLM if/when we need concurrent multi-user serving.
Client code speaks OpenAI-compatible HTTP either way — see `tools/inference/inference_client.py`
(tested against a local `llama-server` in this pull).

### 1.2 Models worth running on 16GB (Oct 2026)

VRAM math: weights + KV cache + ~10% runtime overhead. A 30B MoE at ~3 bpw (IQ3_XXS) is
~11–13GB and leaves headroom; a 14B dense at Q4_K_M (~4.9 bpw) is ~8.6GB.

- **Qwen3.5-27B / Qwen3.6-35B-A3B MoE (UD IQ3_XXS / Q4_K_M)** — 2026 community benchmark
  favorite on 16GB VRAM: ~36 tok/s at 50k context on IQ3_XXS. Apache-2.0 weights.
- **Qwopus3.6-35B-A3B-Coder-MTP (Q4_K_M, Apache-2.0)** — a June-2026 independent coding-model
  study's winner for local agentic coding: 95–100 tok/s with its embedded MTP speculative
  head, equal task ability to the base. **MTP/speculative decoding is the deciding perf
  factor on bandwidth-bound cards.**
- **Qwen3-14B / 32B coder variants (Q4_K_M)** — the safe dense picks for tool-using agents;
  14B fits with huge context headroom, 32B needs Q4 or IQ3 on 16GB.
- **Gemma 4 26B-A4B MoE (quantized)** — Google's 2026 local-agent sweet spot, function
  calling + multimodal; fits 16GB quantized. Weights under Gemma license (redistribution
  terms apply — fine for internal use).
- **gpt-oss-20b (MXFP4, Apache-2.0)** — OpenAI's open-weights 2026 model; QLoRA-fits ~14GB
  (see §5). MXFP4 GGUF ~15.8GB at Q4_K_M.

Coding-agent tip from the field: run coding finetunes with thinking/reasoning **disabled**
(no-think) — several 2026 coder models over-think by default and burn the token budget.

## 2. Diffusion on T4 — image and video

### 2.1 ComfyUI is the substrate (2026)

ComfyUI (Comfy-Org/ComfyUI, **GPL-3.0**) is the standard node-graph runtime. Its 2026 model
support list includes Flux.1/Flux.2, Wan 2.1/2.2, LTX-Video 2/2.3, HunyuanVideo 1.5,
Qwen-Image, Chroma, HiDream — plus 3D (Hunyuan3D 2.1, TripoSplat) and audio. Workflows are
JSON, API-addressable — scriptable from our pipelines. We already pulled ComfyUI references
in GEMINI-PULL.md; this pull adds the **T4-runnable GGUF path**.

### 2.2 FLUX.1 on T4 — viable via GGUF

Full FLUX.1-dev bf16 is ~24GB — does not fit. The runnable recipe (verified from
city96/FLUX.1-dev-gguf community docs + our own checks):

- `flux1-dev-Q4_0.gguf` (7GB) in `ComfyUI/models/unet/` — from `city96/FLUX.1-dev-gguf`
  (verified on HF: `flux1-dev-Q4_0.gguf`, `flux1-dev-Q5_K_S.gguf` present, ungated)
- `t5xxl_fp8_e4m3fn.safetensors` (~4.9GB) + `clip_l.safetensors` in `models/clip/`
- `ae.safetensors` (FLUX VAE) in `models/vae/`
- Node: **city96/ComfyUI-GGUF** (verified **Apache-2.0**, pinned commit in PULLIN-LOG.md;
  **vendored** in this pull at `tools/inference/third-party/ComfyUI-GGUF/`)
- FLUX.1-schnell (4-step) is even lighter if dev quality isn't needed.

**License honesty:** FLUX.1-dev weights are under the Black Forest Labs **non-commercial
license** — the GGUF conversion does not change that. Fine for our internal production use;
do not redistribute the weights or sell outputs as a service without checking terms.
FLUX.1-schnell has the same license family. Logged in §8 and PULLIN-LOG.md.

### 2.3 Video diffusion in 16GB — what actually runs

- **Wan 2.1 14B (Apache-2.0)** — the quality pick. Verified GGUFs on HF:
  `city96/Wan2.1-T2V-14B-gguf` and `city96/Wan2.1-I2V-14B-480P-gguf`
  (Q4_0 / Q4_K_M / Q5_K_S, ungated, Apache-2.0). Field-proven on 16GB cards with the T5-XXL
  text encoder kept on CPU/RAM and the DiT on GPU (Q5_K_S ≈ 10GB + overhead fits).
  480p, a few seconds per clip — this is our finals-render path on the T4.
- **Wan 2.2 14B** — already pulled per GEMINI-PULL.md; same VRAM story, slightly better motion.
- **LTX-Video 2.x (Apache-2.0, Lightricks)** — 700M–2B class, 10–20x faster than Wan-class,
  5s clips, runs in ~8GB. The **iteration/concepting** tier. Already referenced in
  GEMINI-PULL.md.
- **HunyuanVideo 1.5** — 14–16GB+ with int8 quantization tricks; borderline on T4, needs
  64GB+ RAM for offload. Original HunyuanVideo needs 60–80GB — **not T4-viable**. Verdict:
  document only, prefer Wan on our hardware.
- **Wan2GP** (deepbeepmeep/Wan2GP) — purpose-built low-VRAM Wan GUI. GitHub reports
  **NOASSERTION (no license declared)** → treated as all-rights-reserved: **documented only,
  not vendored.**

## 3. Quantization — best quality per VRAM in 2026

### 3.1 GGUF (llama.cpp / Ollama)

| Level | ~bits/wt | Quality loss | Use when |
|---|---|---|---|
| Q8_0 | 8.5 | Negligible | Plenty of VRAM, near-lossless baseline |
| Q6_K | 6.6 | Very small | Quality ceiling most people need |
| Q5_K_M | 5.7 | Small | **Recommended if it fits** |
| Q4_K_M | 4.9 | Moderate | **Best default** |
| IQ4_XS | 4.25 | ≈Q4_K_M | VRAM-tight: smaller than Q4_K_M at similar quality |
| IQ3_M / IQ3_XS | ~3.4 | Noticeable | 30B+ MoE on 16GB; I-quants beat same-size K-quants here |
| Q3_K_M and below | 3.4 | Noticeable+ | Only if nothing else fits |

2026 consensus across benchmarks: **M variants beat S variants in quality-per-byte**;
I-quants (importance-matrix) beat K-quants at the same size below Q4; IQ4_XS is the
"one more GB" saver. For 2026 MoE models, UD/IQ3_XXS quants are the 16GB sweet spot.

### 3.2 vLLM-side: AWQ / GPTQ / bitsandbytes

- **AWQ / GPTQ (INT4)** — the vLLM production quants for 7B–32B on 16GB. Model must be
  pre-quantized as AWQ/GPTQ; `--quantization` must match the checkpoint.
- **bitsandbytes (NF4)** — the QLoRA training quant; also servable.
- **FP8** — not available on T4 (needs Ada sm_89+ / Blackwell). Skip on our hardware.

**Our rule:** GGUF Q4_K_M default for llama.cpp/Ollama paths; IQ3/IQ4 for big MoEs;
AWQ for anything we graduate to vLLM.

## 4. Inference servers — how our pipelines call models

Decision (2026 engine landscape):

- **Now:** `llama-server` (llama.cpp, MIT) on Kaggle T4. One static binary, GGUF-native,
  OpenAI-compatible API, trivial to start/stop inside a Kaggle notebook or script.
  `tools/inference/kaggle-llm-server.sh` automates: download CUDA build b11696 →
  fetch GGUF → serve on :8080.
- **Later, if concurrent:** vLLM (Apache-2.0) with AWQ models; SGLang if agent traffic
  shares long prefixes.
- **Dev loop:** Ollama on the local VM (CPU) / laptop.

`tools/inference/inference_client.py` is the single client our pipelines use — plain
`urllib`, no heavy deps, works against llama-server, Ollama, vLLM, or any OpenAI-compatible
endpoint. Tested against a real local `llama-server` during this pull (see PULLIN-LOG.md).

## 5. Fine-tuning on a T4 — LoRA/QLoRA

### 5.1 LLM fine-tuning

- **Unsloth** (unslothai/unsloth, **Apache-2.0**) — the 2026 default for consumer-GPU
  fine-tuning: 2–5x faster than stock transformers, ~half the VRAM. Reference numbers:
  Llama-3 8B QLoRA r=16 on 50k examples ≈ 12h on a T4; **gpt-oss-20b QLoRA fits ~14GB**;
  Qwen3-30B-A3B MoE QLoRA workable via their split-LoRA formulation. Free-Colab-T4
  notebooks are their documented path — same applies to our Colab.
- **Axolotl** (**Apache-2.0**) — YAML-config training over PEFT/TRL; the reproducible,
  version-controlled choice for pipelines we re-run.
- **LLaMA-Factory** (**Apache-2.0**) — zero-code GUI/CLI/API; good for one-off experiments.
- Quality: QLoRA r=16 is within ~1% of full fine-tuning on MMLU/MT-Bench; r=64 essentially
  matches it. LoRA adapters are 10–100MB — cheap to store in the repos.

`tools/inference/qlora-t4-runbook.md` has the Colab/Kaggle recipe (Unsloth path primary,
Axolotl config pattern secondary).

### 5.2 Art-style LoRA (FLUX/SDXL) on T4

- **Ostris ai-toolkit** (ostris/ai-toolkit, **MIT**) — trains FLUX LoRAs in 16GB with
  quantized base + optimizer offloading. This is our art-style path (character sheets,
  show style guides).
- **Kohya sd-scripts** (Apache-2.0) — the classic alternative.

### 5.3 Character voices on T4

Our TTS base (Chatterbox, MIT) is already wired per TRACK-B-AUDIO-PULL.md. For *trained*
character voices:

- **RVC (Retrieval-based Voice Conversion)** — MIT-licensed architecture, trains on a T4
  with a few minutes of clean character audio, infers in real time. This is the
  voice-model analogue of a LoRA: small, portable, per-character.
- **Zero-shot path:** Chatterbox (MIT, in-pipeline) and IndexTTS-2.5 (Bilibili custom
  license — document, weights only) for cloning from 6–15s samples with no training.
- **Excluded:** XTTS-v2 (CPML non-commercial), F5-TTS (CC-BY-NC weights) — documented,
  not pulled, consistent with this repo's existing license flags.

## 6. What was pulled in this run

| Item | License | Where it landed |
|---|---|---|
| city96/ComfyUI-GGUF (vendored, pinned 6ea2651e) | Apache-2.0 | `tools/inference/third-party/ComfyUI-GGUF/` |
| `kaggle-llm-server.sh` — T4 llama-server bootstrap | ours (MIT-equivalent repo terms) | `tools/inference/` |
| `comfyui-t4-runbook.md` — ComfyUI+GGUF on Kaggle/Colab | ours | `tools/inference/` |
| `qlora-t4-runbook.md` — Unsloth/Axolotl on T4 | ours | `tools/inference/` |
| `workflows/flux1-dev-q4-t4.json` — FLUX.1-dev Q4 T2I workflow | ours | `tools/inference/workflows/` |
| `workflows/wan21-14b-i2v-t4.json` — Wan 2.1 14B I2V workflow | ours | `tools/inference/workflows/` |
| `inference_client.py` — OpenAI-compatible client (tested) | ours | `tools/inference/` |
| This research doc | — | `docs/research/AI-INFERENCE-HARDWARE-2026.md` |
| `PULLIN-LOG.md` — per-item log | — | `tools/inference/` |

## 7. Phone story

The phone is a client, not a compute node: it hits the same OpenAI-compatible endpoints
(llama-server on Kaggle, ComfyUI API mode) over the network. No on-device inference work
is proposed — 2026 phone NPUs are not a target for our GGUF/diffusion workloads.

## 8. License log (honesty section)

- Apache-2.0: ComfyUI-GGUF, vLLM, SGLang, Unsloth, LTX-Video, Wan 2.1 GGUFs, Axolotl,
  LLaMA-Factory, Kohya sd-scripts — pulled or referenced freely with attribution.
- MIT: llama.cpp, Ollama, ai-toolkit, RVC architecture — same.
- GPL-3.0: ComfyUI itself — **referenced, not vendored** (workflows we author are ours).
- **Non-commercial / restricted — documented, NOT pulled:** FLUX.1-dev/schnell weights
  (BFL non-commercial license — internal production use OK, no redistribution/service);
  XTTS-v2 (CPML non-commercial); F5-TTS weights (CC-BY-NC); Fish-Speech (research license).
- **No license declared — documented only:** Wan2GP (NOASSERTION).
- Model weights carry their own licenses (Gemma, Llama-family) — serving publicly =
  redistribution; check model cards. Our use is internal.

## 9. Sources (all verified Oct 2026 via web research)

- llama.cpp releases (ggml-org/llama.cpp, MIT) — release b11696 asset list incl.
  `llama-b11696-bin-ubuntu-x64.tar.gz` and `llama-b11696-bin-ubuntu-cuda-12.8-x64.tar.gz`
- GitHub API license checks: Comfy-Org/ComfyUI (GPL-3.0), city96/ComfyUI-GGUF (Apache-2.0),
  vllm-project/vllm, sgl-project/sglang, ollama/ollama, unslothai/unsloth,
  ostris/ai-toolkit, Lightricks/LTX-Video, deepbeepmeep/Wan2GP (NOASSERTION)
- HF API: city96/FLUX.1-dev-gguf, city96/Wan2.1-T2V-14B-gguf, city96/Wan2.1-I2V-14B-480P-gguf
  (filenames verified), Qwen/Qwen2.5-0.5B-Instruct-GGUF
- city96 FLUX.1-dev GGUF community guide (ComfyUI-GGUF node install, Q4_0 + t5xxl_fp8 recipe)
- 16GB-VRAM llama.cpp benchmark (Medium, Apr 2026): Qwen3.5-27B UD-IQ3_XXS ~36 tok/s at 50k ctx
- ngc-shj/inference-deploy CODING_MODEL_STUDY.md (June 2026): Qwopus3.6-35B-A3B-Coder-MTP winner
- HuggingFace "Best Open-Source LLM Models in 2026" (open-source-llms)
- runaihome.com 2026 quantization quality-loss numbers (Q4 vs Q5 vs Q6 vs Q8)
- mrwillist/pullnexus quantization-guide, vramfirst.com, kenotron-ms/llm-guides
- marktechpost 2026-07: Unsloth vs Axolotl vs TRL vs LLaMA-Factory (VRAM/context numbers)
- menokoog/learning-app LoRA/QLoRA cost tables (T4 12h reference)
- Jon Davis "Open-Source AI Video Stack in 2026" (Wan/Hunyuan/LTX tiers)
- mohitkale/voiceforge ENGINES.md (TTS engine/license matrix), singhshagun08 benchmarks
  (Chatterbox vs XTTS), damvolkov/e-voice 2026-10 TTS notes
- skillalchemy 2026 engine-selection + vLLM SKILL docs (SGLang +29%, TRT-LLM +30–50%)

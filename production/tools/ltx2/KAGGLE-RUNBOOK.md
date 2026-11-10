# LTX-2 — Kaggle GPU Runbook (distilled smoke test)

> WIRING.md's usage section assumed a GPU lane existed somewhere — this doc is the
> "somewhere". It gets LTX-2's fast **DistilledPipeline** from zero to a first
> synced audio+video render on a Kaggle GPU notebook. Written 2026-10-23 by the
> overnight idle pipeline; **not executed yet** (no GPU on the VM) — the GPU lane
> that runs it should tick off the smoke-test checklist at the bottom and report back.

**License gate (read first):** LTX-2 code + weights are under the **LTX-2 Community
License** (see WIRING.md — free incl. commercial use under $10M annual revenue;
paid agreement required at/above $10M). Our indie operation is under the
threshold, so Kaggle runs are cleared. If the operation ever crosses $10M,
stop and re-license before further use.

**Weights:** `Lightricks/LTX-2.5` on HuggingFace is a **gated repo** — the
owner's HF account must accept its terms once, and the notebook needs a
**Read-scope `HF_TOKEN`** secret (Kaggle → notebook → Add-ons → Secrets →
`HF_TOKEN`). Quick-start weight set ≈ **66 GiB**.

## Accelerator choice

- **T4 (free tier):** 16GB VRAM — too small for the 22B distilled transformer at
  bf16. Use `--quantization fp8-cast --offload cpu` (expect slow) or treat as
  "does it even load" check only.
- **P100 (free tier):** same 16GB story as T4.
- **A100 / 2×T4 (paid):** the sane target. A100 40GB fits DistilledPipeline at
  1024×1536/121f without offload; 2×T4 is marginal — use fp8 + offload.
- **Checkpoint-friendly:** keep the notebook under the 30h/wk free quota
  (~owner's Kaggle budget) — download weights once, save them to a Kaggle
  Dataset for reuse across sessions.

## Setup (Kaggle notebook, fresh session)

```python
# Cell 1 — system deps + repo
!apt-get update -qq && apt-get install -y -qq git-lfs > /dev/null 2>&1
!git clone --depth 1 https://github.com/mhvnsnt/cape-jones.git
!pip install -q uv hf_transfer huggingface_hub  # hf_transfer speeds the 66GB pull
```

```python
# Cell 2 — secrets + weights (66 GiB, ~20-40 min first time)
from kaggle_secrets import UserSecretsClient
import os
os.environ["HF_TOKEN"] = UserSecretsClient().get_secret("HF_TOKEN")
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

from huggingface_hub import snapshot_download
for repo, allow in [
    ("Lightricks/LTX-2.5", ["diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors",
                             "text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors",
                             "vae/ltx-2.5-video-vae-bf16.safetensors",
                             "vae/ltx-2.5-audio-vae-bf16.safetensors",
                             "latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors"])]:
    snapshot_download(repo_id=repo, allow_patterns=allow, local_dir="/kaggle/working/models/ltx-2.5")
```

```python
# Cell 3 — install the ltx2 workspace (packages only, skip ltx-trainer)
!cd cape-jones/production/tools/ltx2 && uv sync --extra natten
# natten = fastest diffusion-VAE backend (Linux+CUDA). If it fails to build,
# rerun plain `uv sync` — it falls back to Triton/eager (slower, still works).
```

## Smoke test — DistilledPipeline (one synced A/V shot)

Prompting rule (from WIRING.md): describe BOTH picture and sound — who is on
screen, what they say, in what voice/tone, plus ambience/SFX. One prompt =
picture AND sound together.

```bash
cd cape-jones/production/tools/ltx2
uv run python -m ltx_pipelines.distilled \
    --transformer-path       /kaggle/working/models/ltx-2.5/diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors \
    --text-encoder-path      /kaggle/working/models/ltx-2.5/text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors \
    --video-vae-path         /kaggle/working/models/ltx-2.5/vae/ltx-2.5-video-vae-bf16.safetensors \
    --audio-vae-path         /kaggle/working/models/ltx-2.5/vae/ltx-2.5-audio-vae-bf16.safetensors \
    --spatial-upsampler-path /kaggle/working/models/ltx-2.5/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors \
    --num-frames 121 --seed 42 \
    --output-path /kaggle/working/ltx2-smoke.mp4 \
    --prompt "A medium close-up of a caped hero in a violet-lit living room. He speaks with a deep male voice saying, 'I think it is so good.' Room tone hums softly behind him."
```

**Defaults:** 1024×1536 @ 24fps, 121 frames ≈ 5s. UHD 4K only on A100+:
`--width 3840 --height 2176`.

**Low VRAM (T4/P100):** append `--quantization fp8-cast --offload cpu`.
Expect ~5–10× slower than A100; still valid as a smoke test.

## Show-pipeline follow-ons (after the smoke test passes)

1. **Dialogue scenes** — prompt spoken lines directly (Cape Jones / Wizard Gang
   beats); compare against the MuseTalk/LatentSync lane when a specific
   character face must be preserved.
2. **SFX/ambience beds** — pair LTX-2 audio with MMAudio
   (`production/tools/audio/mmaudio/`) for foley the pass didn't nail.
3. **Upscale** — Real-ESRGAN (`production/tools/realesrgan/`) for presentation renders.
4. **Production quality** — once DistilledPipeline is green, step up to
   `ltx_pipelines.dfr_pipeline` + the detailing IC-LoRA
   (`Lightricks/LTX-2.5-22b-IC-LoRA-Pixel-Spatial-Upscaler/ltx-2.5-22b-ic-lora-pixel-spatial-upscaler-x2-1.0.safetensors`).

## Smoke-test checklist (GPU lane: tick off + report back)

- [ ] Weights downloaded intact (5 files, ~66 GiB) + HF_TOKEN read-scope works
- [ ] `uv sync --extra natten` completed on the Kaggle image (or fallback noted)
- [ ] DistilledPipeline rendered `ltx2-smoke.mp4` (121f) — record GPU type + wall time
- [ ] Audio present and synced (voice + room tone) — OWN-EYES/ears check
- [ ] fp8-cast + offload path verified if run on T4/P100
- [ ] Result + weights saved to a Kaggle Dataset for session reuse

**Estimated first-session cost:** ~20–40 min download + install, one render
~5–15 min depending on GPU — well inside the 30h/wk quota.

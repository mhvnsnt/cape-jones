# ComfyUI on a T4 (Kaggle / Colab) — GGUF runbook

Tested pattern for 16GB VRAM. ComfyUI itself is GPL-3.0 (referenced, not vendored);
the GGUF loader node (city96/ComfyUI-GGUF, Apache-2.0) is vendored at
`tools/inference/third-party/ComfyUI-GGUF/` (pinned commit `6ea2651e`).

## 1. Install (Kaggle notebook cell)

```bash
# system deps
sudo apt-get update -qq && sudo apt-get install -y -qq aria2 > /dev/null

# ComfyUI (pinned commit; master moves fast)
git clone --filter=blob:none https://github.com/Comfy-Org/ComfyUI.git
cd ComfyUI && git checkout <PIN_A_WORKING_COMMIT> && cd ..

# venv + torch (cu124 has T4/sm_75 wheels)
python3 -m venv comfy-env && source comfy-env/bin/activate
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
pip install -r ComfyUI/requirements.txt

# GGUF node: copy the vendored copy from this repo
cp -r tools/inference/third-party/ComfyUI-GGUF ComfyUI/custom_nodes/
pip install -r ComfyUI/custom_nodes/ComfyUI-GGUF/requirements.txt
```

## 2. Models (aria2, resumable — T4 disk is small, fetch only what the job needs)

FLUX.1-dev image (T2I):
```bash
mkdir -p ComfyUI/models/{unet,clip,vae}
cd ComfyUI/models/unet && aria2 -x8 -s8 -o flux1-dev-Q4_0.gguf \
  https://huggingface.co/city96/FLUX.1-dev-gguf/resolve/main/flux1-dev-Q4_0.gguf && cd -
cd ComfyUI/models/clip && aria2 -x8 -s8 -o t5xxl_fp8_e4m3fn.safetensors \
  https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors
aria2 -x8 -s8 -o clip_l.safetensors \
  https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors && cd -
cd ComfyUI/models/vae && aria2 -x8 -s8 -o ae.safetensors \
  https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors && cd -
# NOTE: the BFL repos are gated — accept the license on the repo page and run
# `huggingface-cli login` once before downloading ae.safetensors.
```
**License:** FLUX.1-dev weights are BFL non-commercial — internal production use is fine,
do not redistribute the weights or sell generations as a service. See
`docs/research/AI-INFERENCE-HARDWARE-2026.md` §8.

Wan 2.1 14B image-to-video (Apache-2.0 weights):
```bash
cd ComfyUI/models/unet && aria2 -x8 -s8 -o wan2.1-i2v-14b-480p-Q5_K_S.gguf \
  https://huggingface.co/city96/Wan2.1-I2V-14B-480P-gguf/resolve/main/wan2.1-i2v-14b-480p-Q5_K_S.gguf && cd -
# Wan text encoder (umt5-xxl) — keep on CPU, it lives in RAM:
cd ComfyUI/models/clip && aria2 -x8 -s8 -o umt5_xxl_fp8_e4m3fn_scaled.safetensors \
  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors && cd -
cd ComfyUI/models/vae && aria2 -x8 -s8 -o wan_2.1_vae.safetensors \
  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors && cd -
```

## 3. Run

```bash
source comfy-env/bin/activate
python ComfyUI/main.py --listen 0.0.0.0 --port 8188 --disable-auto-launch
# API mode: POST workflows/ JSON to http://<host>:8188/prompt
```

Ready-made workflows: `tools/inference/workflows/flux1-dev-q4-t4.json` (T2I),
`tools/inference/workflows/wan21-14b-i2v-t4.json` (I2V). Node classes used were verified
against the vendored ComfyUI-GGUF (`UnetLoaderGGUF`, `DualCLIPLoaderGGUF`).

## 4. T4 VRAM notes

- T4 = sm_75: **no FP8 matmuls** — the `_fp8_e4m3fn` text encoders still load (they run
  dequantized); the DiT stays in GGUF quant. Do NOT expect FLUX.2-style FP8 DiT speedups.
- FLUX dev Q4_0 ≈ 7GB + T5-fp8 ≈ 5GB + CLIP-L/VAE ≈ 1GB → fits with headroom for 1024px.
- Wan 14B Q5_K_S ≈ 10GB on GPU + umt5 on CPU/RAM → fits; keep resolution at 480p and
  frames ≤ 81 on 16GB.

## 5. API sketch (from our pipelines)

```python
import json, urllib.request
wf = json.load(open("tools/inference/workflows/flux1-dev-q4-t4.json"))
# randomize seed: wf["<sampler-node-id>"]["inputs"]["seed"] = <int>
req = urllib.request.Request("http://<kaggle-host>:8188/prompt",
    data=json.dumps({"prompt": wf}).encode(),
    headers={"Content-Type": "application/json"})
print(json.loads(urllib.request.urlopen(req).read())["prompt_id"])
# poll /history/<prompt_id> for outputs
```

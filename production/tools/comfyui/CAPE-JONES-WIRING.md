# CAPE-JONES-WIRING.md — ComfyUI (AI image generation)

## What
**Comfy-Org/ComfyUI** @ `master` bc5f880dbdd43e426077f42ccec53bb577ffee9f (pulled 2026-10-23).
The node-based diffusion GUI + API + backend — the most powerful and modular diffusion interface (142k★).
**License: GPL-3.0** (own-eyes verified on `LICENSE` in the pulled tree — free + commercial, same bar as Glaxnimate/Flowblade/Audacity).

## Slot it fills
**AI IMAGE GENERATION** — the last empty rung of the AI-media ladder. The video-gen ladder
(Wan2.2 / LTX-Video / LTX-2 / Open-Sora) exists; nothing wired text-to-image orchestration for
concept art, background plates, and style frames until now. Krita AI Diffusion is a Krita plugin;
this is the repo's canonical standalone t2i/i2i engine.

## Show-pipeline uses
- **Concept art / style frames** — t2i for episode look-dev before any 3D is built.
- **Background plates** — t2i/i2i environments → Real-ESRGAN upscale → Natron composite → Flowblade timeline.
- **Character-consistent shots** — IPAdapter / FaceID-style reference nodes hold likeness across shots.
- **Pose-controlled frames** — ControlNet pose/depth nodes drive character poses from mocap or reference stills.
- **Plate repair** — inpainting/outpainting nodes fix backgrounds without re-rendering.
- **Headless farm mode** — save a workflow as JSON, POST it to `/prompt`; batch-render hundreds of plates
  deterministically (the image equivalent of `melt` for timelines).
- **Bridge to video** — AnimateDiff / Wan2.2 custom nodes feed the existing video-gen ladder (t2i → i2v).

## Setup
```bash
cd production/tools/comfyui
pip install -r requirements.txt        # torch per platform — needs a GPU
python main.py --listen --port 8188   # GUI at http://localhost:8188
# Headless: POST workflow JSON to http://localhost:8188/prompt
```
- **Models are NOT vendored.** Checkpoints/LoRAs/ControlNet/VAE live in `models/` and download at
  runtime (HuggingFace / Civitai) or Kaggle-side — same rule as every other weights-bearing tool here.
- **ComfyUI-Manager** (custom-node installer, Comfy-Org/ComfyUI-Manager) is a separate repo — not vendored;
  install it when you need one-click custom nodes.
- This VM has **no GPU**: run ComfyUI on the Kaggle/Colab lane, commit workflow JSONs back to the repo.

## Chain position
```
t2i concept/plates (ComfyUI) → upscale (Real-ESRGAN) → comp (Natron) → edit (Flowblade/melt)
                                        ↘ i2v (Wan2.2 / LTX-2 / Open-Sora)
                                        ↘ image-to-3D lab (reference plates)
```

## Pull notes (2026-10-23 overnight pipeline)
- Code-only depth-1 pull; upstream `.github/` CI trimmed (house convention).
- `agent_requirements.txt` kept — it's the documented dependency list for API/agent-driven use.
- 0 binaries >50MB; 0 model weights committed.
- Python files py_compile-clean (sampled); `python main.py --help` needs installed deps — documented, not run on this VM.

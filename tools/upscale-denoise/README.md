# upscale-denoise — free render cleanup for the pipeline

## Denoise — built into Blender, verified

- **Intel Open Image Denoise (OIDN)** — bundled with Blender, Apache-2.0,
  runs on CPU. Verified 2026-10-17 on Blender 4.5.12: rendered a Cycles still
  with `scene.cycles.use_denoising=True, denoiser='OPENIMAGEDENOISE'` — completed,
  PNG written. This is the default denoise for all our CPU/Colab renders.
- **OptiX denoiser** — ships with NVIDIA drivers, free. Use on the Kaggle T4
  lane (`--cycles-device OPTIX` renders already use it where enabled).
- OIDN on GPU needs Blender 4.2+ (`denoising_use_gpu`) — our pin is 4.5.12 LTS,
  fine.

Recipe (headless, any lane):
```python
scene.render.engine = 'CYCLES'
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'   # or 'OPTIX' on NVIDIA
```

## Upscale

- **Blender compositor Scale node** — verified headless: Image → Scale
  (RELATIVE 2.0) → Composite runs and outputs an upscaled composite. Good for
  quick 2x bumps of preview stills. Not AI — it's interpolation.
- **Upscayl** (upscayl/upscayl, GPL-3.0) — free, open-source, Real-ESRGAN,
  batch-capable, no watermark. **Needs a Vulkan GPU** — does NOT run on this
  CPU-only VM. Target: the Kaggle T4 lane (Vulkan-capable NVIDIA).
- **Real-ESRGAN** (xinntao/Real-ESRGAN, BSD-3-Clause) — the model Upscayl uses.
  CPU inference is possible via ONNX (`realesr-general-x4v3`, ~5 MB) — this lane
  installed onnxruntime but the model fetch failed; **not run, needs the GPU lane
  or a working model URL**.
- **nextgenUp** (riponcm/nextgenUp) — free open-source image+video upscaler,
  Real-ESRGAN + GFPGAN, local, no cloud. 2026 project; models are MIT/Apache-2.0.
  Ultra mode runs Real-ESRGAN via ONNX Runtime on CPU — candidate for a CPU
  upscale lane if the model fetch is sorted.

**Honest status:** denoise is DONE and in the pipeline. AI upscale is
documented with real 2026 sources but **not yet run** — it belongs on the GPU
lane (Kaggle T4), where Upscayl/Real-ESRGAN actually have a device to run on.

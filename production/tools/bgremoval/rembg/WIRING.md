# rembg — Wiring

**Source:** [danielgatis/rembg](https://github.com/danielgatis/rembg), master @ 2026-10-22
**License:** MIT (own-eyes verified 2026-10-22 on upstream `LICENSE.txt` — Copyright (c) 2020 Daniel Gatis). Commercial use OK.
**What:** AI background removal — feeds an image through a pre-trained ONNX segmentation model and outputs a foreground cutout with transparent background (or solid color, or alpha matte). Multiple built-in models: `u2net`, `isnet-general-use`, `birefnet-general`, `birefnet-general-lite`, `bria-rmbg`, and more. Runs on CPU (onnxruntime) or GPU (onnxruntime-gpu); the 24k-star standard for local offline bg removal.

**Use case (show pipeline):** Cutouts for compositing — isolate a character/actor from a plate to re-stage over new backgrounds, generate alpha mattes for AI-inpaint cleanup passes, extract foreground elements from reference photography. Complements `../realesrgan/` (upscale the cutout after) and `../rife/` (interpolate cutout plates). Anime-line `anime-girl` examples kept in `examples/` are closest to our drawn assets.

## IMPORTANT — model license caveat (research-verified 2026-10-22)

The **code** is MIT, but the **model weights** each carry their own license. The default model in rembg ≥2.0.85 is **BRIA RMBG-2.0**, whose weights are **CC-BY-NC 4.0 (non-commercial)** — do NOT use `bria-rmbg` for anything that ships in the show or product surfaces. Commercial-safe model choices:

```python
from rembg import new_session, remove
session = new_session("birefnet-general")   # weights MIT (commercial OK)
# or: session = new_session("u2net")       # classic, fast, small (176MB)
out = remove(Image.open("frame.png"), session=session, decontaminate=True)
```

Never commit downloaded `.onnx` weights to the repo — weights are never committed (weights rule).

## GPU-side setup (weights are NEVER committed)

```bash
pip install "rembg[cpu]"     # CLI + API; add [gpu] instead of [cpu] for CUDA
# models (~176MB–1GB depending on choice) download on first use into ~/.u2net/
```

## CLI

```bash
rembg i  plate.png cutout.png          # single image
rembg p  shots/ cutouts/               # whole folder
rembg i -m birefnet-general plate.png cutout.png   # pick a commercial-safe model
```

## Python API

```python
from rembg import remove, new_session
from PIL import Image

session = new_session("birefnet-general")
img = Image.open("plate.png")
cutout = remove(img, session=session)      # RGBA PIL image
cutout.save("cutout.png")
```

## Notes
- Code-only pull; trimmed from upstream: `.github` CI, `logo.png`/`onnxruntime-installation-matrix.png` doc art, and the heaviest demo images (`examples/food-1*`, `plants-1`, `animal-3.out.png` — ~15MB). Kept representative `examples/` (~3MB) and full `tests/`.
- `python3 -m py_compile` clean on all package files. Runtime import needs `onnxruntime`/`pymatting` (GPU-side pip install — import tested, deps absent locally as designed).
- Server mode: `rembg s` runs an HTTP server (`docker-compose.yml` included).

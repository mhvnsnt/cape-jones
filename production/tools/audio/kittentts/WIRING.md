# KittenTTS — wiring notes (cape-jones)

**What:** [KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) — open-source
text-to-speech, including ultra-lightweight models that run on plain CPU.
Pulled 2026-10-22 (depth-1, upstream main, upstream pushed 2026-10-22T17:18Z,
16k+ stars, not archived). Vendored code-only at `production/tools/audio/kittentts`
(3.6MB). No weights, no binaries, no CI in the vendored tree.

**License (own-eyes verified 2026-10-22):** the vendored CODE is Apache 2.0 —
upstream `LICENSE` reads "Apache License, Version 2.0" and the GitHub API
reports `license: apache-2.0`. Commercial use of the code is fine.

**Weight license caveat — read before shipping anything:**
The models are licensed SEPARATELY from the code (upstream README says so
explicitly). As of 2026-10-22:
- `kitten-tts-{nano,micro,mini}-0.8` (legacy ONNX path: 15M/40M/80M params,
  56/41/80MB, 8 voices — `KittenTTSOnnx`) — **Apache 2.0** weights. This is
  the commercial-safe default for shipped work.
- `KittenML/kitten-tts-2` (1.7B params, 506MB, 47 voices + voice cloning —
  `KittenTTS2`) — **Stellon Labs Community License**: research, non-commercial
  and *limited* commercial use are free; the commercial grant ends once you or
  your affiliates pass USD $1,000,000 in annual revenue or total cumulative
  funding, at which point a separate license from Stellon Labs is required, and
  distribution carries attribution requirements. Check the model's own license
  before relying on it — do not assume the code's Apache 2.0 extends to it.

Weights download GPU-side at runtime (Hugging Face), NEVER committed to the repo.

**Chain position:** this is the *draft-TTS* link in the audio chain:
text → **KittenTTS** (fast CPU TTS, dialogue drafts / narration / batch takes)
→ **RVC** (`production/tools/audio/rvc` — character voice conversion)
→ **MuseTalk / LatentSync** (lip-sync) → **rembg** (compositing cutouts).
OpenVoice (`production/tools/openvoice`) is the zero-shot *cloning* link;
`piper-tts` and `dia` are already vendored alternatives — KittenTTS Nano is
the lightest (15M params, CPU-only) and fastest-iterating of the set.

**Install (GPU-side, not on this VM):**
```bash
pip install -r requirements.txt        # CPU path
# or: pip install -r requirements_gpu.txt
```

**Usage:**
```python
from kittenml import KittenTTS

# v2 (needs torch; weights under Stellon Labs Community License — see caveat)
m = KittenTTS("KittenML/kitten-tts-2")
print(m.available_voices)
audio = m.generate("One day, a little girl named Lily found a needle in her room.", voice="Bruno")
import soundfile as sf
sf.write("output.wav", audio, m.sample_rate)

# legacy ONNX CPU path (Apache 2.0 weights — commercial-safe default)
from kittenml import KittenTTSOnnx
m = KittenTTSOnnx("KittenML/kitten-tts-nano-0.8-fp32")
audio = m.generate("Say it on a potato.", voice="Bella")
```

`example.py`, `example_advanced.py`, `example_expression.py`, `example_cloning.py`,
`example_streaming.py`, `example_onnx_0.8.py` cover the rest (gradio_demo.py
for an interactive demo; `tests/` for the suite).

**Verify this tool:** `python3 -m py_compile` on `kittenml/*.py` (clean 2026-10-22).

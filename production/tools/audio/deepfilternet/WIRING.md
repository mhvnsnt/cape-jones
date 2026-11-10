# deepfilternet — Wiring for the Cape Jones pipeline

**What:** `Rikorose/DeepFilterNet` — low-complexity real-time speech enhancement
via deep filtering (ICASSP 2022 / DeepFilterNet2 / DeepFilterNet3). Two-stage
model: ERB-domain envelope enhancement + deep filtering of the periodic component.
Full-band 48kHz. Single-threaded real-time factor ~0.19 on a notebook i5.

**License:** dual MIT / Apache-2.0 at your option ✅ (own-eyes verified 2026-10-22:
upstream README "## License" section + LICENSE-MIT on the pulled tree,
Copyright (c) 2021 Hendrik Schröter). Commercial-safe under either.

**Pulled:** 2026-10-22 (main, depth-1; upstream last push 2024-10-17).
Code-only 1.6MB (155 files). Trimmed per weights rule: `models/` (81MB of
DeepFilterNet/2/3 + ONNX weight bundles — upstream ships them on the releases
page) and the demo/test audio in `assets/` (22MB of .hdf5/.wav fixtures;
README.md + dataset.cfg kept). `demo/` (52K Rust example) kept.

## Where it sits in the audio chain

```
recorded take → deepfilternet (fast real-time noise suppression)
  → voicefixer (heavy restore, if the take is genuinely degraded)
  → demucs / audio-separator (stem split) → RVC (character voice)
  → MuseTalk/LatentSync (lip-sync)
```

- **deepfilternet** = first-pass hygiene: cheap, fast, real-time. Run on every
  take before anything else. 48kHz only — resample takes to 48kHz first.
- **voicefixer** (sibling pull) = the heavy restorer for takes that are still
  bad after this (reverb, clipping, low sample rate).

## Setup

Models download at runtime from the upstream releases page / HF, never committed:

```bash
# option A: pip package (pulls DeepFilterNet3 model on first run)
pip install deepfilternet

# option B: this tree (poetry) — console scripts: deepFilter / deep-filter-py
cd production/tools/audio/deepfilternet/DeepFilterNet
poetry install
```

## Usage

```bash
# pre-compiled binary (fastest path, no python deps) — from releases page
deep-filter noisy_take_48k.wav

# python CLI from this tree
deep-filter-py noisy_take_48k.wav --compensate-delay

# python API
from df.enhance import enhance, init_df, load_audio, save_audio
model, df_state, _ = init_df()
audio, _ = load_audio("noisy_take_48k.wav", sr=48000)
enhanced = enhance(model, df_state, audio)
save_audio("clean_take_48k.wav", enhanced, sr=48000)
```

## Pipeline uses for the show

1. **Take hygiene** — strip room tone / fan noise / hiss from every dialogue take
   before RVC training or lip-sync (fast enough to batch the whole session).
2. **Live / stream cleanup** — real-time factor allows a virtual-mic chain
   (LADSPA plugin in the tree) for recording sessions.
3. **Pre-voicefixer pass** — clean light noise first so voicefixer's vocoder
   spends its budget on the real damage (reverb/clipping).

## Notes

- **48kHz only** for the reference models. Resample to 48kHz before processing,
  back to the target rate after — do NOT run natively at 44.1kHz.
- `--compensate-delay` accounts for the model's look-ahead in streaming use.
- DeepFilterNet3 is the quality pick (slightly heavier); DeepFilterNet2 is the
  speed pick. Select with the model's runtime loader.
- The Rust core (`libdf/`) + LADSPA plugin are for the real-time/live path;
  the Python path above covers the batch pipeline.

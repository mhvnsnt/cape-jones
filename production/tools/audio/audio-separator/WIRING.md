# audio-separator — Wiring for the Cape Jones pipeline

**What:** `karaokenerds/python-audio-separator` (pip package `audio-separator`) — CLI + Python
package wrapping the MDX-Net separation models trained by Anjok07 for Ultimate Vocal Remover.
Separates any audio file into primary/secondary stems (typically instrumental + vocals).

**License:** MIT (upstream LICENSE, Copyright (c) 2023 karaokenerds) — own-eyes verified on the
pulled tree 2026-10-22. The UVR *models* (MDX-Net ONNX) ship with an MIT license requiring
credit to UVR and its developers (Anjok07 et al). Weights download at runtime; none are
committed here.

**Pulled:** 2026-10-22 (main, depth-1). Trimmed: `tests/inputs/` (129MB test audio fixtures)
and `.github/` (CI/deploy workflows) — code and test code kept intact.

## Where it sits in the audio chain

```
demucs (4-stem hybrid transformer) → audio-separator (MDX-Net karaoke/instrumental refiner)
  → RVC (voice conversion) → MuseTalk/LatentSync (lip-sync)
```

- **demucs** gives the broad 4-stem split (vocals/drums/bass/other).
- **audio-separator** is the specialist: its `UVR_MDXNET_KARA_2` and related MDX-Net ONNX models
  are the community standard for karaoke instrumental extraction and vocal-only isolation.
  Use it when demucs's vocal stem has too much bleed for lip-sync training data.
- **RVC** converts the isolated vocal into a character voice from ≤10 min of consented audio.

## Setup

Weights stay GPU-side, downloaded at runtime, never committed (weights rule).

```bash
# CPU
pip install "audio-separator[cpu]"
# NVIDIA GPU
pip install "audio-separator[gpu]"
# or install this tree in dev mode (poetry)
poetry install --extras cpu
```

## Usage

```bash
# CLI — separate into instrumental + vocals
audio-separator path/to/take.wav --model_name UVR_MDXNET_KARA_2 --output_dir stems/

# Python API
from audio_separator import Separator
sep = Separator('take.wav', model_name='UVR_MDXNET_KARA_2', output_dir='stems/')
primary, secondary = sep.separate()
```

## Pipeline uses for the show

1. **Backing-track prep** — strip vocals from a licensed track for a character-theme instrumental.
2. **Clean vocal stems for RVC** — feed only the isolated vocal to RVC character-voice training.
3. **Sample extraction** — pull drums/other stems from a track for remix or beat work.
4. **Dialogue cleanup** — separate dialogue from background music in recorded takes before lip-sync.

## Notes

- Model zoo (`audio_separator/models.json`) lists all supported UVR models; default is
  `UVR_MDXNET_KARA_2`. Ensemble presets in `ensemble_presets.json` combine models.
- Requires Python ≥ 3.9 (one dep is unhappy on 3.11+ in older releases — use the env in
  `environment.yml` if `pip install` fails).
- Batch usage in scripts: `audio-separator in.wav --batch_size 16` (GPU) per the upstream README.

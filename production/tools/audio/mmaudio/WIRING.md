# MMAudio — WIRING.md

**Slot:** SFX / Foley generation (NEW — first tool in this slot)
**Upstream:** hkchengrex/MMAudio @ 974010a026c731054592d8f777218bd9d85a6c24 (main, 2026-02-23)
**License:** MIT (Copyright (c) 2024 Sony Research Inc.) — own-eyes verified on upstream LICENSE 2026-10-22
**Code-only:** 136 files, 792KB. No weights committed — checkpoints download at runtime.
**Trimmed from upstream:** `sets/` (VGG dataset index TSVs, 7.2MB — re-downloadable upstream), `training/example_videos/` + `training/example_audios/` (7.2MB demo fixtures). Kept: all code, configs, docs, README, LICENSE, .gitignore.

## What it is

CVPR 2025 video-to-audio synthesis (UIUC + Sony AI). Multimodal joint training:
video-audio + text-audio → generates frame-synchronized sound effects and ambient
audio from video frames (and optional text prompts). Flow-matching, 157M params,
~1.23s to generate an 8s clip, 44.1kHz out. Also competitive at pure
text-to-audio.

## Chain position

```
episode scene video (silent cut)
  → mmaudio        # video-to-audio: footsteps, cloth, impacts, ambience, synced to frames
  → ACE-Step       # music bed (kept SEPARATE — mmaudio does SFX, not score)
  → deepfilternet → voicefixer → demucs/audio-separator → RVC → MuseTalk/LatentSync
```

MMAudio does NOT do dialogue (that stays higgs-audio/cosyvoice/qwen3-tts) and
does NOT do music (ACE-Step). It is the SFX/Foley stage: fight impacts, cloth,
footsteps, weather, room tone — synced to the actual animation frames.

## Setup

```bash
pip install -e .            # from this dir; needs Python 3.9+, torch 2.5.1+
# checkpoints auto-download from HF on first run (see docs/MODELS.md):
#   mmaudio_large_44k / medium_44k / small_44k / small_16k + VAE ckpts
```

Checkpoints are ~100–600MB each — GPU-side/Kaggle-side only, NEVER committed.

## Usage

```bash
python demo.py --video <clip.mp4> --prompt "footsteps on concrete, cloth rustle"
python batch_eval.py --cfg eval_config.yaml        # batch mode
python gradio_demo.py                              # interactive studio UI
```

API: `mmaudio/model/flow_matching.py` + `mmaudio/ext/` (CLIP video features,
SynchFormer motion features, T5 text). See README.md + docs/MODELS.md upstream.

## Notes

- Keep generated SFX on its own track — dialogue/music chains resample per
  stage; SFX stays 44.1kHz until the final mix.
- Weight license: MIT covers code; the released checkpoints are the authors'
  research models — re-verify the checkpoint's HF license card before any
  commercial episode ships.
- 8GB+ VRAM minimum for inference (per upstream).

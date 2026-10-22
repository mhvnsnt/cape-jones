# Demucs wiring — music source separation for the show pipeline

Source: facebookresearch/demucs @ main (depth-1), pulled 2026-10-22.
License: MIT (Copyright (c) Meta Platforms, Inc. and affiliates) — own-eyes
verified on the upstream LICENSE file. Free + commercial use OK.

## What it does

Hybrid transformer source separation (ICASSP 23 / ISMIR 21). Splits a song
into stems: vocals, drums, bass, other (4-stem mdx_extra_q default), or
vocals-only with `--two-stems vocals`. Quality benchmark: ~9.0 dB SDR on
MUSDB18-HQ (fine-tuned v4) — gold standard for open-source stems.

## Pipeline use cases

1. **Backing-track prep** — strip vocals from a reference track to build
   karaoke/instrumental backing for episode scoring.
2. **Stem re-balance** — re-mix drums/bass/vox for menu themes, character
   entrance themes (e.g. GMG JackBoy "Out My Body" stem work).
3. **Dialogue isolation** — htdemucs_ft on noisy field audio to pull clean
   vocal stems before lip-sync (feeds LatentSync/MuseTalk lanes).
4. **Sample extraction** — isolate vocal or drum hits for sound design.

## Weights (GPU-side only — never committed)

Demucs downloads model weights (~200–500MB per model) from Meta CDN on first
use, or via `demucs.utils.load_model` cache. On Kaggle/Colab run:

    pip install -U demucs
    python -m demucs.separate --mp3 --two-stems vocals -n mdx_extra track.mp3

Code in this repo is inference-ready; weights live GPU-side per the weights rule.

## Quick usage

    # 4-stem split, mp3 out
    python -m demucs.separate --mp3 -n mdx_extra track.mp3

    # Vocals-only stem
    python -m demucs.separate --mp3 --two-stems vocals -n mdx_extra track.mp3

    # Python API
    import demucs.separate
    demucs.separate.main(['--mp3', '--two-stems', 'vocals', '-n', 'mdx_extra', 'track.mp3'])

Output goes to `./separated/mdx_extra/<track>/{vocals,drums,bass,other}.mp3`.

## Conda envs

`environment-cpu.yml` / `environment-cuda.yml` pin the two runtimes. For the
GPU lanes use the CUDA env; local dev uses CPU (slow, fine for short stems).

## Pairs with

- `production/tools/stt/faster-whisper/` — transcribe isolated vocal stems for
  subtitles / dialogue alignment.
- `production/tools/lipsync/{latentsync,musetalk}/` — separated vocals feed
  cleaner lip-sync input.

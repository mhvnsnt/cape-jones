# Step-Audio2 — WIRING

Upstream: https://github.com/stepfun-ai/Step-Audio2 @ 76e272b56c3917a8d7188f18bbb5a65dfc8a0845 (main, verified 2026-10-23)
License: Apache-2.0 (own-eyes verified on upstream LICENSE; GitHub API spdx=Apache-2.0)
Pulled: 2026-10-23 via overnight-idle-pipeline (code-only, 57 files, 528KB; upstream `assets/` 12MB demo media trimmed; no model weights committed)

## What it is

Step-Audio 2 mini: fully open-source end-to-end speech-to-speech multimodal LLM
(StepFun, Aug 2025). Breaks the ASR→LLM→TTS pipeline — raw audio tokens in,
reasoning in a unified audio+text space, audio tokens out, preserving emotion,
accent, timbre, speed and background context. Three variants (all Apache-2.0,
same inference code, weights download GPU-side at runtime):

| Variant | HF repo | Use |
|---|---|---|
| Step-Audio 2 mini | `stepfun-ai/Step-Audio-2-mini` | speech conversation + audio understanding |
| Step-Audio 2 mini Base | `stepfun-ai/Step-Audio-2-mini-Base` | pre-trained base, fine-tuning |
| Step-Audio 2 mini Think | `stepfun-ai/Step-Audio-2-mini-Think` | reasoning / chain-of-thought |

Architecture: S3Tokenizer (50 Hz discrete audio codes) → Qwen2.5-7B-init LLM
backbone → diffusion vocoder (24 kHz real-time waveforms). Supports tool
calling (web search / audio search) and RAG to cut hallucination.

## Chain position

This fills the **real-time voice-conversation / in-character spoken agent** slot
in the audio chain, distinct from the TTS lanes:

- Scene video → mmaudio (SFX/ambience)
- Dialogue scripts → higgs-audio (multi-speaker dialogue) / cosyvoice (single)
  / qwen3-tts (fast single + instruction-directed)
- **Spoken interactive characters / voice agents → step-audio2 (speech-in, speech-out)**
- Cleanup/enhance: deepfilternet → voicefixer → demucs / audio-separator
- Voice clone: RVC; lipsync: MuseTalk / LatentSync; music: ACE-Step

If you need one-shot dialogue lines for an episode, use the TTS lanes. If you
need a character that holds an unscripted spoken conversation (fan experiences,
interactive NPCs, live voice booths), use Step-Audio2.

## Setup

Weights are NOT in this repo (per model-weights-off-disk law). On a GPU box
(Kaggle/Colab):

```
pip install -r <see upstream requirements / Dockerfile>
# weights auto-download from HF on first run:
#   stepfun-ai/Step-Audio-2-mini   (chat)
#   stepfun-ai/Step-Audio-2-mini-Base  (fine-tune)
#   stepfun-ai/Step-Audio-2-mini-Think (reasoning)
```

See upstream README.md for Docker images (ready-to-run) and vLLM serving
(`stepaudio2vllm.py`, `examples-vllm.py`, `examples-vllm-stream.py`).

## Usage

Local inference: `stepaudio2.py` + `examples.py` / `examples-base.py` /
`examples-think.py`. Vocoder path: `token2wav.py` (FlashCosyVoice +
CosyVoice2 code under `flashcosyvoice/`, `cosyvoice2/`). Web demo:
`web_demo.py` / `web_demo_vllm.py`.

## Notes

- Re-verify the weight license on the HF repo before commercial use of the
  CHECKPOINTS themselves; code is Apache-2.0 confirmed.
- ASR bench: 3.19 CER (CN) / 3.50 WER (EN), leading other open models by >15%
  (per StepFun, Sep 2025).

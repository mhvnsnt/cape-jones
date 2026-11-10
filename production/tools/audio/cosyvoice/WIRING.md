# CosyVoice 2 — Wiring for the Cape Jones pipeline

**What:** `FunAudioLLM/CosyVoice` — multilingual zero-shot voice cloning TTS
(CosyVoice 2.0: "Scalable Streaming Speech Synthesis with Large Language Models",
arXiv:2412.10117). LLM text→speech-token backbone + chunk-aware causal flow
matching + HiFi-GAN vocoder. 9 languages (EN/ZH/JA/KO/DE/ES/FR/IT/RU), 18+
Chinese dialects, cross-lingual zero-shot cloning, instruction control
(language / emotion / speed), bi-streaming with ~150ms first-packet latency.

**License:** Apache-2.0 ✅ (own-eyes verified 2026-10-22: upstream LICENSE on
main = Apache License Version 2.0, January 2004; GitHub API license key
Apache-2.0; upstream @ 074ca6dc, not archived). Commercial-safe.

**Pulled:** 2026-10-22 (main tarball @ 074ca6dc9e80a2f424f1f74b48bdd7d3fea531cc).
Code-only 3.4MB (156 files, +0/-0 — new slot). No weights committed: models
(CosyVoice2-0.5B ~1GB, CosyVoice-300M, Fun-CosyVoice3-0.5B) download from
HuggingFace/ModelScope at runtime. Demo prompts in `asset/` (two .wav +
one .png, ~1MB) kept — they are the canonical zero-shot/cross-lingual test
prompts, not weights. `third_party/Matcha-TTS` submodule intentionally NOT
initialized (empty dir); see Setup.

## Where it sits in the audio chain

```
script line → cosyvoice (character voice: zero-shot clone or instruct mode)
  → audio chain as before (deepfilternet → voicefixer → demucs/audio-separator
    → RVC → MuseTalk/LatentSync)
  → ACE-Step (music bed, sibling pull)
```

- **cosyvoice** = the ADVANCED VOICE slot the chain was missing: multilingual
  zero-shot cloning (clone any voice from ~seconds of prompt audio), streaming
  synthesis for interactive/dialogue iteration, and instruction-led delivery
  (emotion, speed) for directed line reads. Replaces/augments the older
  Kokoro/Chatterbox/Dia/OpenVoice/parler-tts/Bark set for hero dialogue.
- Output is **22050 Hz** — resample to 48kHz before deepfilternet/voicefixer,
  or to 16kHz for RVC input, per the stage's own rate rule.

## Setup (GPU box / Kaggle)

```bash
cd production/tools/audio/cosyvoice
pip install -r requirements.txt   # torch cu121, modelscope, etc.
# Matcha-TTS is a git submodule used by some training/eval scripts only;
# inference does not need it. If you want it:
git submodule update --init third_party/Matcha-TTS

# download the model once (never committed)
modelscope download --model iic/CosyVoice2-0.5B --local_dir ./pretrained_models/CosyVoice2-0.5B
# or: huggingface-cli download FunAudioLLM/CosyVoice2-0.5B
```

## Usage

```python
from cosyvoice.cli.cosyvoice import AutoModel
import torchaudio

cosyvoice = AutoModel(model_dir='./pretrained_models/CosyVoice2-0.5B')

# 1) zero-shot clone: prompt wav + its transcript -> new line in that voice
for i, j in enumerate(cosyvoice.inference_zero_shot(
        'He steps out of the smoke, cape snapping in the wind.',
        'The quick brown fox jumps over the lazy dog.',   # prompt text
        'asset/zero_shot_prompt.wav')):                   # prompt audio
    torchaudio.save(f'line_{i}.wav', j['tts_speech'], cosyvoice.sample_rate)

# 2) cross-lingual clone (prompt in one language, speak another)
for i, j in enumerate(cosyvoice.inference_cross_lingual(
        'Il sort de la fumée, la cape claquant au vent.',
        'asset/cross_lingual_prompt.wav')):
    torchaudio.save(f'line_xling_{i}.wav', j['tts_speech'], cosyvoice.sample_rate)

# 3) instruction mode: direct the delivery
for i, j in enumerate(cosyvoice.inference_instruct2(
        'You stay out of my town.', 'Speak in a low threatening growl', '')):
    torchaudio.save(f'line_dir_{i}.wav', j['tts_speech'], cosyvoice.sample_rate)

# 4) streaming (dialogue iteration / interactive): stream=True, first packet ~150ms
```

```bash
# Gradio studio UI
python3 webui.py --port 8080 --model_dir ./pretrained_models/CosyVoice2-0.5B
```

## Notes

- `example.py` = minimal end-to-end demo (sft / zero-shot / cross-lingual).
- `runtime/` = gRPC + Triton/TensorRT-LLM deployment scaffolding for
  production serving; `vllm_example.py` = vLLM-backed inference.
- VRAM: CosyVoice2-0.5B ~6–8GB; CosyVoice-300M ~4–6GB. CPU inference works,
  ~10–50x slower — GPU box only for episode work.
- Voice-clone ethics: clone only voices we own / have consent for
  (cast voices, our own TTS character voices). Same rule as RVC.

# Qwen3-TTS — Wiring for the Cape Jones pipeline

**What:** `QwenLM/Qwen3-TTS` — open-source TTS series from the Qwen team at
Alibaba Cloud (announced 2026-01-22). Discrete multi-codebook end-to-end
LM architecture (no LM+DiT cascade) on top of the self-developed
Qwen3-TTS-Tokenizer-12Hz. 10 languages (Chinese, English, Japanese,
Korean, German, French, Russian, Portuguese, Spanish, Italian) plus
dialectal voice profiles. Key features the chain was missing:
**natural-language instruction voice control** ("用特别愤怒的语气说" style
instruct params on timbre/emotion/prosody), **3-second rapid voice clone**
from user audio (`generate_voice_clone`),
and **97ms end-to-end streaming latency** (Dual-Track hybrid streaming
architecture — first audio packet after a single character of input).
vLLM day-0 support via vLLM-Omni (offline inference).

**License:** Apache-2.0 ✅ (own-eyes verified 2026-10-23: upstream LICENSE on
main = Apache License Version 2.0, January 2004; GitHub API license spdx
Apache-2.0; upstream @ 022e286b98fbec7e1e916cb940cdf532cd9f488e, main
branch, not archived). Commercial-safe for the code. Weights are NOT
committed here — they download from HuggingFace (`Qwen/Qwen3-TTS-*`) at
runtime. Re-verify the weight license on the HF model page before any
commercial deployment of the weights themselves.

**Pulled:** 2026-10-23 (main tarball @
022e286b98fbec7e1e916cb940cdf532cd9f488e, ls-remote HEAD agrees).
Code-only 29 files (qwen_tts package + examples + finetuning + README +
LICENSE + pyproject). Duplicate pre-check passed (recursive tree scan:
zero qwen3-tts code in tree — only mentions inside other tools'
docs/tests). No weights committed: binary scan clean (no
safetensors/pt/pth/bin/ckpt/onnx/wav). Upstream `assets/` (8MB media)
skipped; `.github/` skipped. `finetuning/` included: `sft_12hz.py`,
`prepare_data.py`, `dataset.py` let us fine-tune the Base model per
character voice from our own recordings.

**Model sizes (weights download GPU-side at runtime, NOT in this repo):**

| Model | Role | Streaming | Instruct |
|---|---|---|---|
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | voice design from NL description | ✅ | ✅ |
| Qwen3-TTS-12Hz-1.7B-CustomVoice | 9 premium timbres + style instruct | ✅ | ✅ |
| Qwen3-TTS-12Hz-1.7B-Base | 3-sec clone; base for fine-tuning | ✅ | |
| Qwen3-TTS-12Hz-0.6B-CustomVoice | same, lighter | ✅ | |
| Qwen3-TTS-12Hz-0.6B-Base | same, lighter | ✅ | |

## Where it sits in the audio chain

```
dialogue script / single line
  → higgs-audio   (multi-speaker dialogue scenes, [SPEAKER*] tags)
  → qwen3-tts     (single-speaker lines: 3-sec character clone, instruction
                    voice direction "angry / whispering", 97ms streaming)
  → cosyvoice     (backup single-speaker + streaming, instruction-led)
  → RVC           (character voice conversion)
  → MuseTalk / LatentSync (lip sync) + ACE-Step (music)
```

Qwen3-TTS is the fastest-turnaround single-speaker slot: pick it when a
line needs instruction-driven emotion ("say it angrier") or a 3-second
clone of a character/actor recording without RVC training. CosyVoice
remains the cross-lingual/dialect fallback; Higgs Audio remains the
dialogue-scene slot.

## Setup

```bash
# fresh isolated env recommended
pip install -U qwen-tts          # PyPI package (or pip install -e . here)
# weights auto-download from HuggingFace at first from_pretrained call;
# for offline runtimes pre-download: huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
```

## Usage

```python
import torch, soundfile as sf
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0", dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# 1) Custom voice + instruction direction
wavs, sr = model.generate_custom_voice(
    text="…",
    language="English",      # or "Auto"
    speaker="Ryan",          # 9 premium timbres (Vivian/Serena/Ryan/Aiden/…)
    instruct="Very happy.",  # omit if not needed
)

# 2) Voice design from description
wavs, sr = design_model.generate_voice_design(
    text="…", language="English",
    instruct="A raspy villain voice, middle-aged male.",
)

# 3) 3-second clone (Base model)
wavs, sr = clone_model.generate_voice_clone(
    text="…", language="English",
    ref_audio="actor_3s_ref.wav",     # or audio array / list; ref_text optional
)

# 4) Streaming: first packet after one character; end-to-end ~97ms
# (see Dual-Track streaming docs in upstream README)

sf.write("out.wav", wavs[0], sr)
```

CLI demo (Gradio): `python -m qwen_tts` → `qwen-tts-demo` (see `qwen_tts/cli/demo.py`).
Examples dir: `test_model_12hz_base.py`, `test_model_12hz_custom_voice.py`,
`test_model_12hz_voice_design.py`, `test_tokenizer_12hz.py`.
vLLM serving: vLLM-Omni offline inference (examples in vllm-project/vllm-omni).

## Voice-clone ethics

Clone only voices we have rights to (our cast, our actors' approved
references, synthetic designs). Same standing rule as the rest of the
chain: no cloning real people without consent. Fine-tuned Base-model
checkpoints derived from our recordings stay in the weight store, not in
git, alongside the model weights.

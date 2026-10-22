# Parler-TTS — wiring

**Upstream:** https://github.com/huggingface/parler-tts (HEAD d108732c, 2026-10-22)
**License:** Apache 2.0 — own-eyes verified on upstream LICENSE (2026-10-22).
Model checkpoints (parler-tts-mini/large, Mini v1.1, multilingual v1.1 on HF)
are ALSO permissively licensed (Apache 2.0 per their model cards) — fully
open release: datasets, training code, and weights. Code-only here; weights
download GPU-side at runtime, never committed.

## What it is

Lightweight text-to-speech where the VOICE IS DESCRIBED IN WORDS. Give it a
natural-language voice description ("A female speaker delivers a slightly
expressive and animated speech with a moderate speed and pitch. The recording
is of very high quality, with the speaker's voice sounding clear and very
close up.") plus the line to speak, and it synthesizes matching speech.
880M-param Mini and 2.3B-param Large checkpoints (trained on 45k hours of
audiobook data); SDPA / Flash Attention 2 / torch.compile support for fast
generation. Speaker consistency across generations in v1.1.

## Audio chain position (show pipeline)

```
text ──► KittenTTS (15–80M, cheap CPU draft TTS)
      ├──► parler-tts (description-controlled expressive TTS) ──► OpenVoice (zero-shot voice match)
      └────────────────────────────────────────────────────────► RVC (character voice clone, trained on ≤10min)
                                        │
                                        ▼
                                 demucs / audio-separator (clean vocal stems, karaoke backing tracks)
                                        │
                                        ▼
                                 MuseTalk / LatentSync (lip-sync to the face)
```

Use parler-tts when the SCRIPT dictates the voice style in words instead of
needing a cloned reference: narrator takes, monster voices ("deep, gravelly,
slow, threatening"), announcer energy, kid characters, accented readings.
Output flows to RVC for character-consistency conversion, then lip-sync lanes.

## Use

```bash
pip install git+https://github.com/huggingface/parler-tts.git
```

```python
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained(
    "parler-tts/parler-tts-mini-v1.1").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1.1")

description = "A gruff male speaker, slow and menacing, like a wrestling villain."
prompt = "You should have never stepped into MY ring."
input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
gen = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
sf.write("take.wav", gen.cpu().numpy().squeeze(), model.config.sampling_rate)
```

Random voice: omit the specific speaker and vary the description. For a named
character across many takes, lock the description text and/or feed the output
through RVC for a stable character voice.

## Notes

- No checkpoints, weights, datasets, or binaries are vendored here — code
  only, per the no-weights-on-disk rule. Checkpoints download from HF at
  runtime on GPU/Kaggle lanes.
- Consented-voice rule applies downstream: voice descriptions are fine for
  original characters; converting to a real person's voice needs their
  consent (see production/tools/audio/rvc/WIRING.md).

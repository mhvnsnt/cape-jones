# Higgs Audio (TTS 2 / v2) — Wiring for the Cape Jones pipeline

**What:** `boson-ai/higgs-audio` — text-audio foundation model from Boson AI.
Higgs TTS 2 (a.k.a. Higgs Audio v2 Generation): 3.6B LLM (Llama-3.2-3B base) +
2.2B audio DualFFN adapter, pretrained on 10M hours of audio (AudioVerse).
The slot the chain was missing: **conversational multi-speaker dialogue** —
zero-shot natural multi-speaker dialogues with `[SPEAKER*]` tags, automatic
prosody adaptation during narration, per-scene voice assignment, melodic
humming with a cloned voice, and simultaneous speech + background music.
EmergentTTS-Eval: 75.7% / 55.7% win-rate over gpt-4o-mini-tts (Emotions /
Questions). Multi-speaker eval beats MoonCast and Dia-1.6B on WER and
speaker similarity/dissimilarity.

**License:** Apache-2.0 ✅ (own-eyes verified 2026-10-22: upstream LICENSE on
main = Apache License Version 2.0, January 2004; GitHub API license key
Apache-2.0; upstream @ 05a145bb, not archived). Commercial-safe for the code.
Model-card page states "We are open-sourcing Higgs TTS 2"; weight files are
NOT committed here — they download from HuggingFace at runtime. Re-verify the
weight license on the HF model page before any commercial deployment of the
weights themselves.

**Pulled:** 2026-10-22 (main tarball @
05a145bb490501b534563bf51bf2f7aa2326b271, ls-remote HEAD agrees).
Code-only 2.2MB (~150 files, +0/-0 — new slot, no duplicates in tree;
`production/pipeline/tts_voices.py` already carried a `higgs-audio` stub
expecting this dir). No weights committed: binary scan clean (no
safetensors/pt/pth/bin/ckpt/onnx). Demo voice-prompt .wav files trimmed
(re-downloadable upstream); scripts + .txt/.yaml prompts kept. No git
submodules initialized (repo has a `.gitmodules`; not needed for inference).

**Rename note (upstream):** "Higgs Audio V2 / V2 Generation" has been renamed
"Higgs TTS 2". This repo also ships v3 pointers — v3 weights live on HF as
`bosonai/higgs-audio-v3-tts-4b` (4B multilingual). The v2 serve engine below
targets `bosonai/higgs-audio-v2-generation-3b-base` + `bosonai/higgs-audio-v2-tokenizer`.

## Where it sits in the audio chain

```
dialogue script (multi-speaker scene w/ [SPEAKER*] tags)
  → higgs-audio  (dialogue performance: voices, prosody, scene feel)
  → dialogue takes → deepfilternet → voicefixer → demucs/audio-separator
  → RVC (character voice lock) → MuseTalk/LatentSync (lip-sync)
  → ACE-Step (music bed, sibling slot)
```

- **higgs-audio** = the DIALOGUE SCENE slot: where CosyVoice 2 does
  single-character zero-shot cloning and ACE-Step does music, Higgs does the
  *scene* — two or more characters talking naturally in one pass, with the
  model picking appropriate voices and adapting prosody to the scene
  description. Ideal for episode dialogue scenes, trailer banter, and
  multi-character ADR where per-line single-speaker TTS would sound stitched.
- Output is **24 kHz** — resample to 48kHz before deepfilternet/voicefixer,
  or to 16kHz for RVC input, per the stage's own rate rule.

## Setup (GPU box / Kaggle)

```bash
cd production/tools/audio/higgs-audio
pip install -r requirements.txt   # torch, transformers>=4.45.1,<4.47.0, etc.
pip install -e .

# download weights once (never committed) — v2 generation + tokenizer
huggingface-cli download bosonai/higgs-audio-v2-generation-3b-base
huggingface-cli download bosonai/higgs-audio-v2-tokenizer
# v3 alternative: bosonai/higgs-audio-v3-tts-4b
```

transformers-native path also works (`HiggsAudioV2ForConditionalGeneration`
+ `AutoProcessor`, see upstream model card) with transformers>=5.3.0.

## Usage — serve engine (v2 code path)

```python
from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine, HiggsAudioResponse
from boson_multimodal.data_types import ChatMLSample, Message
import torchaudio, torch

MODEL_PATH = "bosonai/higgs-audio-v2-generation-3b-base"
AUDIO_TOKENIZER_PATH = "bosonai/higgs-audio-v2-tokenizer"
system_prompt = (
    "Generate audio following instruction.\n\n"
    "<|scene_desc_start|>\nAudio is recorded from a quiet room.\n<|scene_desc_end|>"
)
messages = [
    Message(role="system", content=system_prompt),
    Message(role="user", content=(
        "[SPEAKER0] You really think that cape is gonna save you?\n"
        "[SPEAKER1] It saved me last Tuesday. Tuesday counts.")),
]
device = "cuda" if torch.cuda.is_available() else "cpu"
engine = HiggsAudioServeEngine(MODEL_PATH, AUDIO_TOKENIZER_PATH, device=device)
out: HiggsAudioResponse = engine.generate(
    chat_ml_sample=ChatMLSample(messages=messages),
    max_new_tokens=1024, temperature=0.3, top_p=0.95, top_k=50,
    stop_strings=["<|end_of_text|>", "<|eot_id|>"],
)
torchaudio.save("scene_take.wav", torch.from_numpy(out.audio)[None, :], out.sampling_rate)
```

Speaker voices can be described in the `scene` role
("SPEAKER0: feminine", "SPEAKER1: masculine") or cloned zero-shot by placing
reference audio in the conversation history — see `examples/generation.py`
(single / multi-speaker / zero-shot cloning recipes) and the upstream
model card for the transformers-native equivalents.

## Pipeline fit notes

- **Emotion direction:** unlike CosyVoice's instruction control, Higgs takes
  emotion from scene description + dialogue text itself (EmergentTTS-Eval
  leader on "Emotions") — write the scene prompt, not per-line tags.
- **Voice consistency across takes:** pin voices with zero-shot reference
  clips in the scene role (or per-speaker reference audio in history);
  character-voice *lock* still goes through RVC downstream.
- **VRAM:** ~3.6B + 2.2B adapter ≈ Kaggle T4/P100 class at fp16; v3-4B is the
  heavier multilingual alternative.
- **tts_voices.py stub:** `production/pipeline/tts_voices.py` already lists a
  `higgs-audio` engine entry with `check: None` — flip `check` to a real
  import/CLI probe once the weights are on the GPU box.

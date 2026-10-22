# faster-whisper — Wiring

**Source:** [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper), master @ 2026-10-22
**License:** MIT (own-eyes verified 2026-10-22 on upstream `LICENSE` — Copyright (c) 2023 SYSTRAN). Commercial use OK.
**What:** Fast Whisper speech-to-text — a reimplementation of OpenAI's Whisper on the CTranslate2 inference engine. ~4x faster than the reference `openai-whisper` at the same accuracy, ~2x less VRAM. Supports word-level timestamps, Silero VAD filtering, batched inference, and hotwords. The transcription path for the dialogue pipeline.

**Use case (show pipeline):** Auto-transcribe dialogue audio → timed transcripts → subtitles for clips (wizard-gang/ashlane clips posted to the pages), dialogue alignment for lip-sync takes (`../lipsync/`), searchable dialogue logs. Word timestamps feed clip-cutting; Silero VAD skips silent stretches in raw VO takes. Whisper large-v3 handles the multilingual/named-slang dialogue; tiny/base models run on CPU for quick passes.

## GPU-side setup (weights are NEVER committed)

```bash
cd production/tools/stt/faster-whisper
pip install -r requirements.txt        # ctranslate2, tokenizers, onnxruntime, av
# Whisper model weights (~1-3GB depending on size) download on first use from HuggingFace — never committed
```

## Transcribe

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("vo_take.wav", word_timestamps=True, vad_filter=True)
for s in segments:
    print(f"[{s.start:.2f} -> {s.end:.2f}] {s.text}")
```

```bash
# quick CPU pass (tiny model, int8):
python -m faster_whisper --help   # CLI via benchmark/utils or scripts below
```

Batch transcribe a folder (GPU):

```python
from faster_whisper import BatchedInferencePipeline, WhisperModel
model = WhisperModel("large-v3", device="cuda", compute_type="float16")
batched = BatchedInferencePipeline(model=model)
for audio in files:
    segments, info = batched.transcribe(audio, batch_size=16, word_timestamps=True)
```

## Notes
- Code-only pull; Whisper model weights download GPU-side on first use (never committed).
- Bundled `faster_whisper/assets/silero_vad_v6.onnx` (1.2MB) ships inside the upstream package — kept; it's the tiny VAD model, not a generative weight.
- Trimmed from upstream (recorded per SAY THE DELETIONS): `.github` CI dir and the 13MB `benchmark/benchmark.m4a` benchmark audio. Benchmark scripts kept.
- `python3 -m py_compile` clean on all package/test/benchmark files.

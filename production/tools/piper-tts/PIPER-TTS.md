# piper-tts/ — Piper Neural TTS (rhasspy/piper v1.2.0)

Fast, local, offline neural text-to-speech. MIT licensed (commercial use OK).
Upstream archived 2026 (project complete/stable); pulled 2026-10-18 via
overnight-idle-pipeline. Upstream `.github/` workflows stripped per convention;
`.git` removed (landed as a plain subtree, not a submodule).

## What it is

- C++ inference binary (`piper`) + Python package (`src/python_run/piper/`)
  + HTTP server (`piper/http_server.py`) — serve TTS as a local API.
- Voices are small ONNX files (tens of MB); hundreds of free voices at
  `rhasspy/piper-voices` — download on demand, never commit voices to the repo.
- `etc/test_voice.onnx` (27MB) ships in-tree for smoke tests only.

## Build / run

Prebuilt binaries (Linux/macOS/Windows) are on the upstream releases page —
no build needed for narration use:

```bash
# one-shot synthesis
echo "Cape Jones saves the city." | piper \
  --model path/to/en_US-lessac-medium.onnx \
  --output_file line01.wav

# serve locally (pairs with cartoon-studio / animatic_builder.py)
python3 src/python_run/piper/http_server.py --model path/to/voice.onnx
```

Building from source needs CMake + onnxruntime (see upstream README);
the Python package needs only `onnxruntime` via pip for the HTTP server.

## Candidate uses in our pipeline

- Scratch dialogue / temp narration for animatics (`explainroo`-style flow)
  without API keys or per-character costs — pairs with `rhubarb-lip-sync/`
  (audio -> mouth-shape timelines) and `cartoon-studio/` (87-voice dialogue,
  piper can be a local-voice provider).
- Podcast/narration drafts for Wizard Gang / Cape Jones social cuts.
- Voice prototyping before committing to ElevenLabs / actor recordings.

## Notes

- Quality is single-speaker per voice file; not a voice-cloner.
  For cloning/reference voices use the ElevenLabs connector instead.
- Keep voice `.onnx` files OUT of git (model weights stay off the repo);
  document voice URLs in the lane, download to scratch at render time.

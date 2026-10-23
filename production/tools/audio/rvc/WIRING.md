# RVC (Retrieval-based Voice Conversion) — Wiring

**Upstream:** RVC-Project/Retrieval-based-Voice-Conversion-WebUI (38k stars), pulled 2026-10-22.
**License:** MIT (own-eyes verified on upstream LICENSE) — commercial OK.
**What:** train a voice model on ≤10 min of audio, then convert any voice INTO that voice. Code-only pull (3.2MB); no model weights in repo.

## Why it's in the show pipeline

- **Character voices:** convert a recorded dialogue take into a character's voice (e.g. apply a Static voice model to any temp dialogue recording). Works after demucs stem-splits and alongside faster-whisper transcripts.
- **Song covers / themes:** convert a vocal performance into a character voice for themes.
- **Dubbing/re-DP:** re-voice a line without re-recording the actor.
- Downstream: converted audio feeds MuseTalk/LatentSync lip-sync lanes.

## Entry points (scripted, batch-first)

Batch inference (no GUI — use this in pipelines):

```bash
cd production/tools/audio/rvc
# install deps first (GPU): pip install -r requirments_cu128_py312.txt
python infer/cli.py \
  --model assets/weights/<character>.pth \
  --input  dialogue/raw/wav/ \
  --output dialogue/converted/wav/ \
  --index-rate 0.75 --protect 0.33 --recursive
```

- `python webui.py` — full Gradio UI (training + inference, manual sessions).
- `python realtime_gui.py` — live voice changer (needs CUDA + low latency).
- `train/train.py` / `webui.py` train tab — train a new character model from ~10 min of clean voice audio (demucs vocals stem is a good source).
- `infer/modules/vc/pipeline.py` — the `VC` class for embedding in Python scripts.

## Weights / models (GPU-side only — NEVER committed)

- Character `.pth` models + `.index` files go in `assets/weights/` and `assets/indices/` (created at runtime, git-ignored — keep them off repos per the weights rule; they're large and often likeness-restricted).
- Pitch extractors (rmvpe, fcpe) download to `assets/rmvpe/` on first run.
- HubERT/content-vec base weights download at runtime.
- Train on Kaggle/Colab; download models there, copy `.pth`/`.index` into the GPU-side `assets/weights/` at run time.

## Notes

- `--protect` preserves breaths/unvoiced regions; `--index-rate` blends retrieval strength. Defaults (0.33 / 0.75) are the upstream sane baseline.
- `RVCRealtimeVST/` is the optional Windows VST plugin (needs iPlug2/vst3sdk/vst2sdk submodule fetches + C++ build) — not used by the show pipeline; kept upstream-intact.
- `assets/pymss_weights/` holds only YAML configs (mel-band roformer karaoke/dereverb); the actual separation weights download at runtime.
- Voice-cloning likeness rules still apply: only consented voice models (owner's confirmed character voices; licensed performers) get trained.

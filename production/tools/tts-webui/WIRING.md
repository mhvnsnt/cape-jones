# TTS-WebUI — Wiring

**Upstream:** [rsxdalv/TTS-WebUI](https://github.com/rsxdalv/TTS-WebUI)
**Pulled at upstream HEAD:** `2e5701387c423307d73972a45496bfdcb6a7d8e1` (main, 2026-09-07)
**License:** MIT — own-eyes verified on upstream `LICENSE` raw text
(sha256 `0f34ba386c174072c5e06eef5d112a7c19b03d84748b994816a6a1bbc55290e0`).
Free + commercial, no caveats. GitHub API: 3,291★, not archived.

## What it is

A unified Gradio + React web studio that brings together a large ecosystem of
text-to-speech, voice conversion, and audio generation models under one UI.
This fills the **TTS-WebUI studio slot** in the audio chain: instead of running
each TTS model in its own environment, every engine is managed as an extension
inside one interface.

## Chain position

```
step-audio2 (speech↔speech conversation)
    ↓
tts-webui  ← THIS  (studio UI + extension hub for every TTS engine below)
    ├─ higgs-audio (dialogue) / cosyvoice (single-clip clone) / qwen3-tts (fast/instruct)
    ├─ bark / parler-tts / kokoro / styletts2 / index-tts / fire-red-tts2 / openvoice v2
    ├─ piper-tts (local, fast narration)  ← overlaps our piper-tts pull (interchangeable)
    ├─ tortoise / f5-tts / chatterbox / kimi-audio / mimo-audio / mahatts / megatts3
    ├─ gpt-sovits / openvoice (uv) / mars5
    └─ xttsv2 / zylphra? (check extension catalog for current list)
    ↓
RVC (voice conversion)  ← already pulled
    ↓
latentsync / musetalk (lip-sync) + mmaudio (SFX) + ace-step (music)
```

Notes:
- TTS-WebUI has its own **Piper TTS** extension (uv-managed). Our standalone
  `production/tools/piper-tts` pull and the TTS-WebUI Piper extension are
  interchangeable — pick whichever is already set up in the running environment.
- **RVC extension** is built in; use our pulled RVC scripts for headless/batch
  work and the WebUI for interactive tuning.
- Some extensions ship via `uv` (isolated per-extension envs) — good for avoiding
  dependency clashes with our pinned environments.

## Extension catalog (69 entries at pull time)

Highlights: ACE-Step, Audio Separator, Bark, Chatterbox, CosyVoice [Unstable],
Demucs, DIA, F5-TTS, FireRedTTS2, GPT-SoVITS, Higgs V2 (Early Access),
Index TTS, Kimi Audio, Kitten TTS, Kokoro, MARS5, MegaTTS3, MiMo-Audio,
MiniMax Cloud TTS, MusicGen, OpenAI TTS API, OpenVoice (V2), Parler-TTS,
Piper TTS, RVC, Seamless M4T, Stable Audio, StyleTTS2, Tortoise, XTTSv2...

Extension manager (built-in GUI/CLI) installs community extensions from the
catalog; `extensions.json` lists what's available.

## Setup

```bash
cd production/tools/tts-webui
./start_tts_webui.sh          # Linux (installer path)
# or Docker:
docker-compose up
```

Gradio backend and the React frontend run on separate ports; see upstream
`README.md` for the port defaults and the Silly Tavern integration.

## GPU / Kaggle runbook

- Installer fetches CUDA toolkit + conda envs; on Kaggle/Colab use the upstream
  `documentation/notebooks/google_colab.ipynb` as the starting point.
- Weights are NOT committed (model weights stay OFF local disk / off-repo).
  Each extension downloads its own weights to the Huggingface cache on the
  GPU side. Note each engine's weight license before using it in the pipeline.

## Show-pipeline uses

1. **Dialogue batch generation** — audition many voices across engines in one UI
   instead of wiring each model separately.
2. **Voice conversion hub** — RVC built in; pair with our RVC scripts.
3. **SFX/music adjacency** — Audio Separator, Stable Audio, MusicGen extensions
   sit next to the TTS tab (overlaps our demucs/audio-separator + ACE-Step lanes;
   use whichever is provisioned).
4. **Extension catalog** — new community TTS models land here first; check the
   catalog before pulling any single-engine TTS repo.

## Pull provenance

- Pulled 2026-10-23 (overnight pipeline) via `~/workspace/tools/pull-to-repo.sh`
- Method: depth-1 clone of upstream main at verified HEAD, `.git` + upstream
  `.github` + `__pycache__` stripped. Code-only: 11MB, 0 files >50MB,
  0 weight binaries.
- `python3 -m py_compile`: clean. `bash -n` on shell scripts: clean.
- No duplicate on repo tree (production/tools has piper-tts but no tts-webui).

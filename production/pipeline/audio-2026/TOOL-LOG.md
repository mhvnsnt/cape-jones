# Pull log — audio/voice/music 2026 (2026-10-16)

Every entry: what it is, source URL, license (verified 2026-10-16), where it landed.
Owner rules: open source first; non-commercial/region-excluded = documented, NOT pulled.

## PULLED

### F5-TTS
- **What:** Flow-matching zero-shot TTS; fast inference for bulk ADR/dubbing. Complements Chatterbox (owner's character default, never replaced).
- **Source:** https://github.com/SWivid/F5-TTS (⭐ 15,414, pushed 2026-10-14)
- **License:** MIT (repo LICENSE; PyPI `f5-tts` 1.1.22 verified)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (install+smoke); `dialogue_pipeline.py` `f5tts` engine; western-heart CHARACTER-VOICE-2026 doc

### CosyVoice 3
- **What:** LLM TTS; cross-lingual voice cloning (9 langs incl EN↔JA), natural-language instruction emotion control, ~2GB models, GGUF quants for CPU.
- **Source:** https://github.com/FunAudioLLM/CosyVoice (⭐ 19,139, pushed 2026-05-25)
- **License:** Apache-2.0 (GitHub API verified)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (install notes); `dialogue_pipeline.py` `cosyvoice` engine

### audio.cpp
- **What:** Pure-C++ ggml audio engine: TTS, voice cloning (chatterbox GGUF), voice design, ASR, VAD, diarization, separation. Prebuilt v0.9.2.
- **Source:** https://github.com/0xShug0/audio.cpp (⭐ 3,586, pushed 2026-10-16)
- **License:** Apache-2.0 (LICENSE file, Copyright 2026 ShugoAI LLC). Per-model weights carry own licenses (chatterbox=MIT ok; fish_audio/index_tts2/higgs_audio=non-commercial, research only)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (binary+model table)

### DiffRhythm
- **What:** End-to-end lyrics+style → full-length song with vocals. DiffRhythm-base needs only 8GB VRAM with `--chunked`: fits Kaggle T4.
- **Source:** https://github.com/ASLP-lab/DiffRhythm (⭐ 2,347, pushed 2025-11-27)
- **License:** Apache-2.0 (GitHub API verified)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (T4 guide)

### voice-changer (w-okada)
- **What:** Real-time voice changer GUI + socket server (`server/MMVCServerSIO.py`). RVC/ONNX model slots. Western Heart create-a-fighter voice changer rig.
- **Source:** https://github.com/w-okada/voice-changer (⭐ 21,187, pushed 2026-09-26)
- **License:** MIT (LICENSE file: Copyright (c) 2022 Wataru Okada, verified)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (server notes); primary integration in western-heart

### python-audio-separator
- **What:** One CLI over UVR/MDX/HT-Demucs/Roformer models: vocals/drums/bass/other stems.
- **Source:** https://github.com/nomadkaraoke/python-audio-separator (⭐ 1,702, pushed 2026-09-01)
- **License:** MIT (GitHub API verified; PyPI `audio-separator` 0.47.0)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (install+smoke)

### DeepFilterNet
- **What:** Tiny real-time noise suppression + dereverberation. Stage 1 of phone-dialogue cleanup chain.
- **Source:** https://github.com/Rikorose/DeepFilterNet (⭐ 3,429, pushed 2026-08-21)
- **License:** Dual MIT / Apache-2.0 (README license section; gh metadata NOASSERTION, README governs)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (install+smoke); pairs with existing `production/pipeline/audio_restore.py`

### resemble-enhance
- **What:** Neural speech denoiser/enhancer. Stage 2 of phone-dialogue cleanup chain. Same org as Chatterbox (Resemble AI).
- **Source:** https://github.com/resemble-ai/resemble-enhance (⭐ 2,459)
- **License:** MIT (GitHub API verified; PyPI `resemble-enhance` 0.0.1)
- **Landed:** cape-jones `production/pipeline/audio-2026/` (install+smoke)

## DOCUMENTED, NOT PULLED
- **YuE2-3B** — best open song quality but weights CC-BY-NC-4.0 (HF API on `m-a-p/YuE2-3B`). Code repo Apache-2.0. Research/internal reference only.
- **TangoFlux** — best open text-to-SFX 2026 (ICLR 2026) but Stability AI Community License = non-commercial research-only. MMAudio (already pulled) covers production SFX.
- **Auffusion** — code Apache-2.0, checkpoints CC BY-NC-SA 4.0. Research only.
- **IndexTTS2** — weights under bilibili Model Use License Agreement.
- **XTTS** — no v3 exists (2026-10-16). CPML non-commercial; Coqui defunct 2024.
- **seed-vc** — GPL-3.0 copyleft; MIT voice-changer covers the slot.
- **Parler-TTS** — Apache-2.0 but stale since 2024-12-10; superseded by Chatterbox.
- **MusicGen (Meta)** — CC-BY-NC 4.0.
- **Stable Audio 3 / Magenta Realtime 2 / MiniMax Music 3.0** — previously documented, not pulled.
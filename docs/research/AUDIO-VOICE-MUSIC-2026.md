# Audio / Voice / Music 2026 — Research + Pull-in

**Date:** 2026-10-16 · **Researcher:** Ashes (subagent, parent orchestrator dispatch)
**Status:** Researched live (GitHub API, PyPI, HuggingFace API, web). Licenses verified per-repo.
**Rule:** Open source first, commercial-usable licenses only for pulls. Non-commercial / region-excluded = documented, NOT pulled.

Already in the stack (do not duplicate): Chatterbox (MIT — owner's BEST TTS, never replace for
characters, complements only), Kokoro, OpenVoice, Dia, StyleTTS2, LuxTTS, MMAudio.

---

## 1. Voice cloning / TTS 2026 (since Chatterbox)

### PULLED: F5-TTS — fast zero-shot TTS for bulk ADR/dubbing
- **Repo:** https://github.com/SWivid/F5-TTS · ⭐ 15,414 · pushed 2026-10-14 · **MIT**
- **PyPI:** `f5-tts` 1.1.22 (`pip install f5-tts`, CLI `f5-tts_infer-cli`)
- **What:** Flow-matching non-autoregressive TTS, strong zero-shot cloning from a short
  reference clip, fast inference (no slow AR loop). Excels at long-form/dubbing throughput.
- **Why it beats/complements what we have:** Chatterbox stays the character default (owner law).
  F5-TTS complements it for bulk work — episode ADR, scratch dialogue, multilingual dubs —
  where speed and zero-shot fidelity matter more than per-character tuning.
- **Wired:** `production/pipeline/audio-2026/kaggle_setup_audio2026.py` (install + smoke test);
  `production/pipeline/dialogue_pipeline.py` now lists `f5tts` as an engine option.

### PULLED: CosyVoice 3 — cross-lingual cloning + instruction emotion
- **Repo:** https://github.com/FunAudioLLM/CosyVoice · ⭐ 19,139 · pushed 2026-05-25 · **Apache-2.0**
- **What:** Alibaba/FunAudioLLM LLM-based TTS. CosyVoice 3 (`Fun-CosyVoice3-0.5B-2512`) adds:
  cross-lingual voice cloning across 9 languages (incl. EN ↔ JA — the exact design-in-JP-speak-EN
  workflow), natural-language *instruction* emotion control (`inference_instruct2`, e.g.
  "say it angry"), ~2GB models, bi-streaming at ~150ms latency, official Docker.
  GGUF quants exist (LLM Q4_K 384MB + flow Q8_0 361MB) — CPU-runnable. PyTorch-free ONNX
  inference also exists (community).
- **Why it complements Chatterbox:** Chatterbox has an `exaggeration` dial; CosyVoice 3 takes
  plain-English direction per line and clones a voice across languages — ideal for Japanese
  reference → English episode dialogue.
- **Wired:** `production/pipeline/audio-2026/` (install notes); `dialogue_pipeline.py`
  `cosyvoice` engine option (zero-shot + instruct paths).

### PULLED: audio.cpp — one GGUF engine for TTS/VC/separation/ASR
- **Repo:** https://github.com/0xShug0/audio.cpp · ⭐ 3,586 · pushed 2026-10-16 · **Apache-2.0**
  (LICENSE file, Copyright 2026 ShugoAI LLC). Prebuilt releases: v0.9.2.
- **What:** Pure C++ (ggml) all-in-one audio inference: TTS families (supertonic, vibevoice,
  voxcpm2, pocket_tts, omnivoice), voice cloning (chatterbox GGUF), voice design (qwen3_tts,
  irodori_tts), ASR, VAD, diarization, separation — one backend, CPU-friendly, GGUF quants.
  Prebuilt `audio-v0.9.2-bin-ubuntu-x64-cuda12.8-colab.tar.gz` fits Kaggle T4 directly.
- **Why:** Kills per-model Python env hell. The **chatterbox GGUF** family gives us the owner's
  best-TTS on CPU/quantized for the phone/laptop; VAD+diarization upgrades the edit pipeline.
- **License honesty:** engine is Apache-2.0; *individual model weights carry their own licenses*
  (chatterbox = MIT ✓; fish_audio / index_tts2 / higgs_audio weights = non-commercial — research
  only, never in production).
- **Wired:** `production/pipeline/audio-2026/` (release binary + model table).

### Documented, NOT pulled
| Tool | Verdict | Reason |
|---|---|---|
| **IndexTTS2** | ❌ excluded | Weights under bilibili "Model Use License Agreement" — commercial use needs written permission. (Chatterbox covers the quality slot anyway.) |
| **XTTS (v2)** | ❌ excluded | No v3 exists as of 2026-10-16. CPML = non-commercial, and Coqui shut down 2024 (no commercial license obtainable). |
| **Parler-TTS** | ❌ skipped (stale) | Apache-2.0 but untouched since 2024-12-10; superseded by Chatterbox for our use. |
| **Qwen3-TTS** | ❌ skipped | Upstream take-to-take instability confirmed unfixed (non-deterministic output, rate drift; maintainer unresponsive). |

---

## 2. SFX generation — best open text-to-SFX 2026

### Answer
- **Best open model: TangoFlux** ([ICLR 2026] flow-matching text→audio, super fast, faithful).
  https://github.com/declare-lab/TangoFlux · ⭐ 884 · pushed 2026-01-28.
  **BUT: non-commercial, research-only** — repo LICENSE section binds the model to the
  **Stability AI Community License** (+ WavCaps academic-only data terms). → **Documented, NOT pulled.**
- **Auffusion** (https://github.com/happylittlecat2333/Auffusion): code is Apache-2.0 but
  **checkpoints are CC BY-NC-SA 4.0** → **documented, NOT pulled.**
- **Production path that IS commercial-safe:** **MMAudio** (already pulled) does video→audio SFX/foley;
  pair it with Chatterbox/F5-TTS dialogue and DiffRhythm music. TangoFlux stays a research-only
  reference (fine for internal sound-design experiments, never ships in an episode).

---

## 3. Music generation — best open, runnable on Kaggle T4 / local CPU

### PULLED: DiffRhythm — blazing-fast full songs, T4-ready
- **Repo:** https://github.com/ASLP-lab/DiffRhythm · ⭐ 2,347 · pushed 2025-11-27 · **Apache-2.0**
- **What:** End-to-end full-length song generation from lyrics + style prompt. Diffusion-based,
  non-autoregressive — "blazingly fast and embarrassingly simple."
- **T4 fit:** **DiffRhythm-base needs only 8GB VRAM** (use `--chunked` flag) — fits Kaggle T4
  (16GB) with headroom. No 24GB card needed.
- **Why it wins the slot:** Only commercial-licensed open model that does *lyrics → full song
  with vocals* on a free T4. Ideal for episode soundtrack beds, menu music, parody songs.
- **Wired:** `production/pipeline/audio-2026/` (clone + `--chunked` inference notes).

### Documented, NOT pulled
| Tool | Verdict | Reason |
|---|---|---|
| **YuE2-3B** (multimodal-art-projection/YuE, code Apache-2.0, ⭐ 12,035) | ❌ weights excluded | Best open *quality* (48kHz stereo, editable score via YuE2-Studio/timoncool MIT) but **weights are CC-BY-NC-4.0** (verified via HF API on `m-a-p/YuE2-3B`). GGUF quants (Q8_0 ≈ 4.4GB) fit T4 — research/internal reference only, never in shipped tracks. |
| **MusicGen** (Meta) | ❌ excluded | CC-BY-NC 4.0. |
| **Stable Audio 3 / MiniMax Music 3.0 / Magenta Realtime 2** | already documented | Per prior index — not pulled. |
| **Riffusion** | ❌ skipped | Instrumental-only, 2022-era; DiffRhythm supersedes for songs. |

---

## 4. Voice conversion — real-time VC for create-a-fighter voice changer

### PULLED: w-okada/voice-changer — the real-time VC rig
- **Repo:** https://github.com/w-okada/voice-changer · ⭐ 21,187 · pushed 2026-09-26 ·
  **MIT** (LICENSE file: "Copyright (c) 2022 Wataru Okada", MIT text verified)
- **What:** The standard open real-time voice changer: GUI + `server/MMVCServerSIO.py`
  socket server, RVC/ONNX model slots, near-zero-latency conversion.
  Launch via repo start scripts (`start2.sh`, `start_docker.sh`).
- **Why:** Direct fit for the Western Heart create-a-fighter voice changer — player picks/creates
  a fighter, VC maps their mic (or a base voice) to the character voice in real time.
  Character-voice wiring lives in western-heart (`docs/research/CHARACTER-VOICE-2026.md`).
- **Wired:** cape-jones `production/pipeline/audio-2026/` (install + server notes);
  character integration in western-heart.

### Documented, NOT pulled
| Tool | Verdict | Reason |
|---|---|---|
| **seed-vc** (Plachtaa) | ❌ excluded | Strong quality, but **GPL-3.0** copyleft — MIT alternative (voice-changer) covers the slot without license friction. |
| **RVC official** (RVC-Project, MIT) | noted | MIT; voice-changer is the better *real-time rig* (RVC models load into its slots). |

---

## 5. Audio restoration — vocal separation, dialogue enhancement, de-reverb

### PULLED: python-audio-separator — vocal/instrument separation
- **Repo:** https://github.com/nomadkaraoke/python-audio-separator · ⭐ 1,702 ·
  pushed 2026-09-01 · **MIT** · **PyPI:** `audio-separator` 0.47.0
- **What:** One CLI (`audio-separator`) over UVR/MDX/HT-Demucs/Roformer models: vocals,
  drums, bass, other stems. CPU-runnable.
- **Why:** Stem-split finished mixes for remixes/parody edits; isolate vocals from reference
  tracks; clean dialogue beds.

### PULLED: DeepFilterNet — de-reverb/denoise for phone-recorded lines
- **Repo:** https://github.com/Rikorose/DeepFilterNet · ⭐ 3,429 · pushed 2026-08-21 ·
  **dual MIT / Apache-2.0** (README license section verified; gh metadata says NOASSERTION —
  README governs)
- **What:** Tiny real-time noise suppression + dereverberation. Built for exactly our pain:
  dialogue recorded on a phone in a room.
- **Why:** First stage of the phone-dialogue cleanup chain:
  `DeepFilterNet (de-reverb/denoise) → resemble-enhance (polish)`.

### PULLED: resemble-enhance — speech enhancement polish
- **Repo:** https://github.com/resemble-ai/resemble-enhance · ⭐ 2,459 · **MIT** ·
  **PyPI:** `resemble-enhance` 0.0.1 (`import resemble_enhance` verified from wheel)
- **What:** Denoiser + enhancer for speech; makes phone/field recordings sound studio-adjacent.
- **Why:** Second stage after DeepFilterNet. Same org as Chatterbox (Resemble AI), MIT — no
  license surprises.

---

## Wiring map

| Tool | License | Lands in cape-jones | Lands in western-heart |
|---|---|---|---|
| F5-TTS | MIT | `production/pipeline/audio-2026/` install+smoke; `dialogue_pipeline.py` engine | character ADR complement (doc) |
| CosyVoice 3 | Apache-2.0 | `production/pipeline/audio-2026/` install notes; `dialogue_pipeline.py` engine | cross-lingual character dubs (doc) |
| audio.cpp | Apache-2.0 | `production/pipeline/audio-2026/` binary+models | CPU chatterbox-GGUF fallback (doc) |
| DiffRhythm | Apache-2.0 | `production/pipeline/audio-2026/` T4 guide | menu/soundtrack music (doc) |
| voice-changer | MIT | `production/pipeline/audio-2026/` server notes | **create-a-fighter VC rig** (primary) |
| audio-separator | MIT | `production/pipeline/audio-2026/` install+smoke | stem splits for entrances (doc) |
| DeepFilterNet | MIT/Apache-2.0 | `production/pipeline/audio-2026/` install+smoke | phone-line cleanup chain (primary) |
| resemble-enhance | MIT | `production/pipeline/audio-2026/` install+smoke | phone-line cleanup chain (primary) |

Full install + T4 smoke-test script: `production/pipeline/audio-2026/kaggle_setup_audio2026.py`.
Kaggle notebook generator: `production/pipeline/audio-2026/gen_notebook_audio2026.py`
(pattern matches `production/kaggle/gen_notebook.py`).

**Chatterbox remains the character-voice default — owner law. Everything above complements, never replaces.**

## Verification evidence (2026-10-16)
- PyPI metadata verified: `audio-separator` 0.47.0, `deepfilternet` 0.5.6,
  `resemble-enhance` 0.0.1 (wheel inspected: `import resemble_enhance`), `f5-tts` 1.1.22.
- Licenses verified via GitHub API / README reads: F5-TTS MIT, CosyVoice Apache-2.0,
  audio.cpp Apache-2.0 (LICENSE file), DiffRhythm Apache-2.0, voice-changer MIT
  (LICENSE file), audio-separator MIT, DeepFilterNet MIT/Apache-2.0 (README),
  resemble-enhance MIT.
- Non-commercial exclusions verified: YuE2-3B weights CC-BY-NC-4.0 (HF API),
  TangoFlux Stability AI Community License (repo README), Auffusion checkpoints
  CC BY-NC-SA 4.0, IndexTTS2 bilibili model-use agreement, XTTS CPML, seed-vc GPL-3.0.
- `dialogue_pipeline.py` edit validated: `ast.parse` clean, `--list-engines` shows
  `f5tts`/`cosyvoice` with honest availability detection.
- audio.cpp v0.9.2 release asset verified: `audio-v0.9.2-bin-ubuntu-x64-cuda12.8-colab.tar.gz`.
- Local pip install smoke test: BLOCKED by disk (VM 99% full; deepfilternet needs a
  Rust build). Full install+smoke runs on Kaggle T4 via `kaggle_setup_audio2026.py`
  (queue currently on HOLD for Pantera render — runs when unheld).
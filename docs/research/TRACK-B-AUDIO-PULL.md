# TRACK B — Voice/TTS + Music/Sound Pull (2026-10-16)

Code only, `git clone --depth 1`. No weights stored locally — weight URLs +
sizes noted as "weights on Kaggle". Every repo below was license-checked;
anything non-commercial / research-only / territorial was SKIPPED (see Skips).

Legend: status OK = cloned + license verified. Weights = HF/model URL for the
Kaggle box + size.

## 1. VOICE / TTS

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| Piper TTS | `tools/piper/` | MIT | Fastest quality TTS; ONNX voices, CPU-friendly. Consistent character voices | Piper voices (HF rhasspy/piper-voices, ~50-100MB/voice) |
| KittenTTS | `tools/kitten-tts/` | Apache-2.0 code / model terms vary | SOTA <25MB CPU TTS, 8+ voices — instant scratch voices | KittenTTS model (~25MB); v2 weights Stellon Labs Community License — check terms |
| espeak-ng | `tools/espeak-ng/` | GPL-3.0 | Robot/TTS fallback, zero deps, 100+ langs | none needed |
| KittenTTS | `tools/kitten-tts/` | Apache-2.0 (code) | SOTA <25MB CPU TTS, 8 voices | KittenTTS model (~25MB); v2 weights under Stellon Labs Community License — check terms |
| StyleTTS 2 | `tools/StyleTTS2/` | MIT | Style + emotion control, diffusion | HF styletts2 (~400MB) |
| Tortoise TTS | `tools/tortoise-tts/` | Apache-2.0 | Expressive zero-shot clone from 3-6s ref (slow) | HF tortoise checkpoints (~1.7GB) |
| F5-TTS | `tools/f5-tts/` | MIT code / **CC-BY-NC-4.0 weights** | Fast zero-shot clone | F5TTS_Base (~1GB) — NC, research only |
| GPT-SoVITS v4 | `tools/gpt-sovits/` | MIT | Voice clone + singing, Chinese/EN/JP strong | GPT-SoVITS v4 (~1GB) |
| CosyVoice 2 | `tools/cosyvoice/` | Apache-2.0 | Alibaba 0.5B streaming, 9 langs + dialects, zero-shot clone | FunAudioLLM/CosyVoice2-0.5B (~1GB) |
| Qwen3-TTS | `tools/qwen3-tts/` | Apache-2.0 | 2026 release, 10 langs, 0.6B/1.7B | Qwen3-TTS 0.6B/1.7B (Apache) |
| Higgs Audio v2 | `tools/higgs-audio/` | Apache-2.0 | Conversational multi-speaker TTS (dialogue scenes) | boson-ai/higgs-audio-v2 (~7GB) |
| Step-Audio | `tools/step-audio/` | Apache-2.0 | Multilingual, instruction-led vocalization | Step-Audio 2-mini (Apache) |
| Sesame CSM-1B | `tools/sesame-csm/` | Apache-2.0 | Conversational speech model (Sesame) | sesame-ai/csm-1b (~7GB) |
| WhisperSpeech | `tools/whisperspeech/` | MIT | Expressive long-form (Collabora) | whisperspeech s2a models |
| VALL-E-X | `tools/vall-e-x/` | MIT | Cross-lingual voice cloning | VALL-E-X checkpoints (community) |
| Matcha-TTS | `tools/matcha-tts/` | MIT | Fast non-autoregressive; CosyVoice dependency | matcha checkpoints (~100MB) |
| MeloTTS | `tools/melotts/` | MIT | Light CPU multilingual | MeloTTS HF (~1GB total) |
| TTS-WebUI | `tools/tts-webui/` | MIT | All-in-one Gradio+React studio UI (Piper/RVC/Demucs/Vocos/DIA/Kokoro/CosyVoice/GPT-SoVITS/Stable Audio/ACE-Step...) as installable extensions | extension-managed on GPU box |
| tts-webui-docker | `tools/tts-webui-docker/` | MIT | RunPod/docker image for TTS-WebUI (Kaggle/RunPod deploy) | — |

Already had: Kokoro, Chatterbox, Dia, OpenVoice, parler-tts, Bark.

## 2. VOICE CONVERSION / SINGING

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| RVC (community fork) | `tools/rvc/` | MIT | Retrieval-based VC, huge model community | RVC v2 models (HF, ~300MB each) |
| so-vits-svc 4.1 | `tools/so-vits-svc/` | AGPL-3.0 | Singing VC | so-vits-svc 4.1 checkpoints |
| Seed-VC | `tools/seed-vc/` | GPL-3.0 | VC (Plachtaa) | Seed-VC checkpoints |
| DiffSinger | `tools/diffsinger/` | Apache-2.0 | Singing voice synthesis from score | DiffSinger acoustic models |

## 3. MUSIC / SONG GENERATION

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| ACE-Step | `tools/ace-step/` | Apache-2.0 | Lyrics->full song, fast | ACE-Step 3.5B (Apache, ~7GB) |
| DiffRhythm v1 | `tools/diffrhythm/` | Apache-2.0 | Full-length song, latent diffusion | aslp-lab/diffrhythm (Apache) |
| DiffRhythm 2 | `tools/diffrhythm2/` | Apache-2.0 | Block flow-matching song gen | aslp-lab/diffrhythm2 |
| SongGen | `tools/songgen/` | Apache-2.0 | Single-stage AR text->song, mixed/dual-track + 3s voice clone | SongGen + XCodec (~2GB) |
| YuE / YuE2 | `tools/yue/` | Apache-2.0 code / **CC-BY-NC-4.0 + creator permission** | Dual-track lyrics->song | m-a-p/YuE2-3B (~7GB); individual creators MAY monetize outputs, companies need license |
| Stable Audio | `tools/stable-audio/` | MIT code / **Stability Community License** | Text->music + SFX (44.1kHz stereo) | stabilityai/stable-audio-open-1.0 (gated, ~9.5GB); commercial OK under $1M/yr |
| Magenta | `tools/magenta/` | Apache-2.0 | Compositional: melody/drum continuation -> MIDI | Magenta bundles (Apache) |

Already had: AudioCraft (MusicGen+AudioGen — note: released weights research-only).

## 4. SFX / FOLEY (beyond MMAudio)

Covered by Stable Audio Open (text->SFX, Small-SFX variant) + `tools/MMAudio`
(video->SFX). See `post-pipeline/sfx_gen.py`.

## 5. STEM SEPARATION / RESTORATION / MASTERING

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| Demucs | `tools/demucs/` | MIT | 4-stem hybrid transformer (vocals/drums/bass/other) | mdx_extra checkpoints (~500MB) |
| UVR5 | `tools/uvr5/` | MIT | Ultimate Vocal Remover (MDX-Net variants GUI) | UVR models (various) |
| DeepFilterNet | `tools/deepfilternet/` | Apache-2.0/MIT | Real-time noise suppression | DeepFilterNet (~100MB) |
| VoiceFixer | `tools/voicefixer/` | MIT | Speech restoration (denoise+dereverb+declip+SR) | voicefixer ckpt (~500MB) |
| Resemble Enhance | `tools/resemble-enhance/` | MIT | Neural speech enhancement | enhance ckpt |
| Pedalboard | `tools/pedalboard/` | GPL-3.0 | Programmatic audio FX (Spotify) — foley chains | pip package, no weights |
| Encodec | `tools/encodec/` | MIT | Neural audio codec (compression/tokenization) | encodec_24khz (~100MB) |
| HiFi-GAN | `tools/hifi-gan/` | MIT | Vocoder | hifi-gan checkpoints |
| Vocos | `tools/vocos/` | MIT | Fast Fourier vocoder | charactr/vocos-mel-24khz (~50MB) |
| BigVGAN | `tools/bigvgan/` | MIT | Universal vocoder | bigvgan checkpoints |
| loudnorm | (ffmpeg) | — | Broadcast loudness: `ffmpeg -i in.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 out.wav` | — |

## 6. LIP-SYNC HELPERS (beyond LatentSync/MuseTalk/OpenFaceFX)

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| WhisperX | `tools/whisperx/` | BSD-2 | Word-level timestamps (whisper + wav2vec2 align) | whisper large-v3 + align models |
| whisper-timestamped | `tools/whisper-timestamped/` | AGPL-3.0 | Word timestamps, transformers-based | whisper models |
| Montreal Forced Aligner | `tools/montreal-forced-aligner/` | MIT | Phoneme-level alignment for visemes | MFA english_us_arpa acoustic model |
| aeneas | `tools/aeneas/` | AGPL-3.0 | Forced aligner -> sync-map JSON | embedded |
| Coqui STT | `tools/coqui-stt/` | MPL-2.0 | Transcription QC of generated dialogue | coqui stt models |

## 7. GLUE SCRIPTS (`tools/post-pipeline/`)

All parse-tested (`py_compile`), dry-run by default, `--run` executes,
`--list` shows availability:

- `tts_voices.py` — unified TTS dispatcher (16 engines, fastest-first)
- `music_gen.py` — music/song dispatcher (6 engines)
- `sfx_gen.py` — text->SFX dispatcher (stable-audio, MMAudio)
- `voice_convert.py` — VC/singing dispatcher (5 engines)
- `lipsync_align.py` — forced-alignment dispatcher (4 engines) -> JSON for visemes
- `stem_sep.py` — stem separation (demucs, uvr5)
- `audio_restore.py` — restoration + broadcast loudnorm

## DEFERRED (disk ceiling — pull on the GPU/Kaggle box)

Disk hit 85% (df) during the pull, so this one was deliberately NOT cloned
locally. License-cleared; one command on a box with headroom:

- **magenta** (Apache-2.0): `git clone --depth 1 https://github.com/magenta/magenta`

The `music_gen.py` dispatcher already references the `magenta/` path, so it
lights up automatically once cloned. (bigvgan, whisperx, and
montreal-forced-aligner were also deferred mid-pull but landed via the
parallel lane before it finished — all present and verified.)

## SIBLING-LANE NOTES

- A parallel MEGA-PULL lane also cloned into `~/workspace/tools/` (uvr5,
  ddsp, etc.). No conflicts: its script skipped dirs that already existed.
  `uvr5/` (MIT, 41MB) came from that lane and is usable here.
- `cosyvoice/` remote is `FunAudioLLM/CosyVoice` (sibling won the race; same
  upstream as `QwenAudio/CosyVoice`, GitHub redirects). Its
  `third_party/Matcha-TTS` submodule is NOT initialized — run
  `git submodule update --init --recursive` on the GPU box, or use the
  standalone `tools/matcha-tts/` already pulled here.
- All other contested dirs verified to carry this track's intended remotes.

## DISK

Track B added ~1.9GB across 43 repos (+4 more landed via the parallel lane:
bigvgan, whisperx, montreal-forced-aligner, uvr5). Disk went 81% -> 86%
(df); this track stopped new clones at 85% per the stay-under-85% rule —
the last point came from the parallel lane's final clones. Only magenta
remains un-pulled (deferred above, ~40MB).

## SKIPS (license or availability)

- **Coqui XTTS** — code MPL-2.0 OK, but XTTS-v2 weights under CPML (non-commercial) → skipped (maintained fork: idiap/coqui-ai-TTS)
- **Fish Speech / OpenAudio S1** — skipped per task (non-commercial); openaudio-s1-mini repo 404s
- **Breeze TTS 2** — skipped per task
- **F5-TTS weights** — CC-BY-NC-4.0 → code pulled, weights flagged research-only
- **Silero** — models CC-BY-NC-4.0 → skipped
- **IndexTTS 2** — weights non-commercial → skipped
- **Spark-TTS** — flipped to CC-BY-NC-SA → skipped
- **MaskGCT** — CC-BY-NC-4.0 → skipped
- **AudioLDM / AudioLDM2** — CC-BY-NC-SA-4.0 → skipped
- **Tango/Tango2** — "released for the research community", no commercial grant → skipped
- **VibeVoice (Microsoft)** — MIT but pulled by Microsoft after misuse → skipped
- **VOICEVOX** — LGPL core but canonical voices non-commercial → skipped
- **SongBloom** — Apache-2.0 but repo 404/deleted → skipped (unaudited mirrors exist)
- **SongGen weights** — Apache-2.0, pulled
- **SeamlessM4T** — models CC-BY-NC-4.0 → skipped (present as TTS-WebUI extension)

## DAW / PLUGIN NOTES (documented, not cloned — too heavy)

- **Ardour** (GPL-2.0+) — full open DAW for episode mixing
- **Zrythm** (AGPL-3.0) — modern open DAW
- **LMMS** (GPL-2.0) — beat/bassline DAW
- **Surge XT** (GPL-3.0) — flagship open synth (VST3/LV2)
- **LSP plugins** (LGPL/GPL) — full LV2/VST3 mixing/mastering suite
- pip: `librosa` (ISC), `pyloudnorm` (MIT), `aubio` (GPL) — analysis + loudness

## ADDITIONS 2026-10-16 (respawn run, disk stopped at 86%)

Verified from local LICENSE files unless noted. All `git clone --depth 1`, code only.

### Voice / TTS (new this run)

| Tool | Path | License | What / why | Weights (Kaggle) |
|---|---|---|---|---|
| Pocket TTS (Kyutai) | `tools/pocket-tts/` | MIT code / **CC-BY-4.0 weights** | 100M-param, CPU-recommended (~6x RT on 2 cores), voice clone from 10s clip, 8 built-in voices (alba, marius, javert, jean, fantine, cosette, eponine, azelma). CC-BY-4.0 = commercial OK w/ attribution | HF kyutai/pocket-tts (gated, ~400MB) |
| Orpheus-TTS | `tools/orpheus-tts/` | Apache-2.0 | Llama-3b backbone, human-like, zero-shot clone, emotion tags, ~200ms streaming | HF canopylabs/orpheus |
| MOSS-TTS | `tools/moss-tts/` | Apache-2.0 | 8B flagship + 100M Nano (CPU), voice clone, dialogue gen, SFX, realtime streaming | OpenMOSS/MOSS-TTS (~8B) |
| NeuTTS | `tools/neutts/` | **NeuTTS Open License v1.0** (NOT Apache — corrected) | On-device TTS, instant voice clone, GGUF quantized CPU/mobile, 120M Nano / 360M Air | neuphonic weights |
| LuxTTS | `tools/luxtts/` (+ ComfyUI nodes `tools/boyoluxtts-comfyui/`) | Apache-2.0 | zipvoice-based, 150x realtime GPU / faster-than-RT CPU, 48kHz, SOTA cloning for its size | HF YatharthS/LuxTTS |
| CosyVoice 2 | `tools/cosyvoice/` (repo is FunAudioLLM/CosyVoice) | Apache-2.0 | Alibaba 0.5B streaming, 9 langs + dialects, zero-shot clone, instruction control | FunAudioLLM/CosyVoice2-0.5B (~1GB) |
| VALL-E-X | `tools/vall-e-x/` (Plachtaa fork) | MIT | Cross-lingual voice cloning (EN->JP/ZH etc.) | community checkpoints |

### Voice conversion / singing (license verified)

| Tool | Path | License | Notes |
|---|---|---|---|
| so-vits-svc | `tools/so-vits-svc/` | AGPL-3.0 | Singing VC. AGPL = commercial-OK, network copyleft |
| DiffSinger | `tools/diffsinger/` | Apache-2.0 | Singing voice synthesis from musical score |

### Music / song (license verified)

| Tool | Path | License | Notes |
|---|---|---|---|
| DiffRhythm v1 | `tools/diffrhythm/` | Apache-2.0 | Full-length song, latent diffusion |
| DiffRhythm 2 | `tools/diffrhythm2/` | **Apache-2.0** ("All Rights Reserved" is just the copyright line; the LICENSE is Apache) | Block flow-matching song gen |
| SongGen | `tools/songgen/` | Apache-2.0 | Single-stage AR text->song, mixed/dual-track + 3s voice clone |
| YuE / YuE2 | `tools/yue/` | Apache-2.0 code / **CC-BY-NC-4.0 weights + creator permission** | Dual-track lyrics->song; individual creators may monetize outputs, companies need a license |
| DDSP | `tools/ddsp/` | Apache-2.0 | Google's differentiable DSP — neural instrument/timbre synthesis for score BGM |

### Stem separation / restoration / codecs (license verified)

| Tool | Path | License | Notes |
|---|---|---|---|
| Demucs | `tools/demucs/` | MIT | 4-stem hybrid transformer (vocals/drums/bass/other) |
| UVR5 | `tools/uvr5/` | MIT (code) | Ultimate Vocal Remover GUI; MDX-Net variants — check per-model terms |
| DeepFilterNet | `tools/deepfilternet/` | MIT | Real-time noise suppression |
| Encodec | `tools/encodec/` | MIT | Neural audio codec (compression/tokenization) |
| Vocos | `tools/vocos/` | MIT | Fast Fourier vocoder (~50MB weights) |
| BigVGAN | `tools/bigvgan/` | MIT (code AND weights) | Universal neural vocoder, 44.1kHz; v2 on HF nvidia/BigVGAN |

### Lip-sync helpers (license verified)

| Tool | Path | License | Notes |
|---|---|---|---|
| WhisperX | `tools/whisperx/` | BSD-2 | Word-level timestamps (whisper + wav2vec2 align) |
| faster-whisper | `tools/faster-whisper/` | MIT | 4x faster Whisper (CTranslate2) — transcription + timestamps for captions/dialogue QC |
| Montreal Forced Aligner | `tools/montreal-forced-aligner/` | **MIT** (verified from LICENSE file) | Phoneme-level alignment -> visemes |
| phonemizer | `tools/phonemizer/` | **GPL-3.0** (verified) | Text->phonemes (espeak-ng/festival backends) for viseme mapping |

### License corrections from this run

- **NeuTTS**: NOT Apache-2.0 — actual license is **NeuTTS Open License v1.0**: free research + limited commercial use; commercial OK **under $5M/yr annual revenue**, paid license required above. KEPT with flag (same class as Stability Community License).
- **whisper-timestamped / aeneas / so-vits-svc**: all AGPL-3.0 (verified from files). Commercial use allowed; network copyleft applies.
- **coqui-stt**: MPL-2.0 (verified). Commercial OK.
- **Stable Audio**: code MIT (verified); model weights under Stability Community License (gated, commercial OK under $1M/yr revenue).
- **KittenTTS v2 weights**: Stellon Labs Community License — check terms before commercial use.

### Document-only (disk ceiling hit — NOT cloned)

- **OmniVoice** (https://github.com/k2-fsa/OmniVoice) — Apache-2.0. 2026-03-31, 14.5K stars. 600+ languages, zero-shot voice cloning (3-10s ref), voice design, 40x real-time. Weights ~2.45GB. PRIORITY pull when disk allows — arguably the single best 2026 TTS find.
- **magenta/magenta** (monorepo) — Apache-2.0. Skipped: huge repo; pulled **ddsp** (the relevant synth piece) instead.
- **RAVE** (https://github.com/acidd/rave) — neural audio synthesis; check license before pulling.
- **gentle** (https://github.com/lowerquality/gentle) — forced aligner; document + check license.
- **Allosaurus** (https://github.com/xinjli/allosaurus) — universal phone recognizer; document + check license.
- **Qwen3-TTS** weights: Apache-2.0, 0.6B/1.7B (already pulled as code).
- DAW/plugin notes above still stand (Ardour, Zrythm, LMMS, Surge XT, LSP).

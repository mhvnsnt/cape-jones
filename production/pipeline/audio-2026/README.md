# audio-2026 — Audio / Voice / Music pull-in (2026-10-16)

Eight open-source tools, all commercial-usable licenses (verified 2026-10-16).
Research: `docs/research/AUDIO-VOICE-MUSIC-2026.md`.

**Owner law: Chatterbox stays the character-voice default. Everything here complements, never replaces.**

## The eight

| # | Tool | License | Slot | Install |
|---|---|---|---|---|
| 1 | [F5-TTS](https://github.com/SWivid/F5-TTS) | MIT | fast zero-shot TTS (bulk ADR/dubs) | `pip install f5-tts==1.1.22` |
| 2 | [CosyVoice 3](https://github.com/FunAudioLLM/CosyVoice) | Apache-2.0 | cross-lingual clone (EN↔JA) + instruction emotion | `pip install git+https://github.com/FunAudioLLM/CosyVoice.git` |
| 3 | [audio.cpp](https://github.com/0xShug0/audio.cpp) | Apache-2.0 | one GGUF engine: TTS/VC/ASR/VAD/diarize/separate | prebuilt release v0.9.2 |
| 4 | [DiffRhythm](https://github.com/ASLP-lab/DiffRhythm) | Apache-2.0 | lyrics→full song, **8GB VRAM min (`--chunked`)** | `git clone` + `pip install -e .` |
| 5 | [voice-changer](https://github.com/w-okada/voice-changer) | MIT | real-time VC (create-a-fighter rig) | clone, run `start2.sh` / `start_docker.sh` |
| 6 | [audio-separator](https://github.com/nomadkaraoke/python-audio-separator) | MIT | vocal/instrument stem separation | `pip install audio-separator==0.47.0` |
| 7 | [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | MIT/Apache-2.0 (dual) | de-reverb + denoise (phone lines) | `pip install deepfilternet==0.5.6` |
| 8 | [resemble-enhance](https://github.com/resemble-ai/resemble-enhance) | MIT | speech enhancement polish | `pip install resemble-enhance==0.0.1` |

## Files here

- `kaggle_setup_audio2026.py` — one-shot installer + smoke tests. Run on Kaggle T4
  (GPU, internet ON), Colab, or the VM. Installs all eight, then smoke-tests each
  (import / `--help` / CLI version — model weights download on first real use, not here).
- `gen_notebook_audio2026.py` — generates `cape_jones_audio2026_kaggle.ipynb`
  (pattern matches `production/kaggle/gen_notebook.py`: edit the generator, not the .ipynb).
- `TOOL-LOG.md` — pull log: what, source URL, license, where landed.

## Phone-dialogue cleanup chain (pairs with `../audio_restore.py`)

```
phone-recorded line.wav
  → deepfilternet   (de-reverb + denoise, real-time, tiny model)
  → resemble-enhance (neural polish)
  → ffmpeg loudnorm=I=-16:TP=-1.5:LRA=11   (broadcast loudness, see ../audio_restore.py)
```

## Dialogue pipeline

`../dialogue_pipeline.py` engine priority now lists F5-TTS (bulk/ADR) and CosyVoice 3
(cross-lingual + instruction emotion) as options. Chatterbox remains the character default.

## License traps avoided (documented, NOT pulled)

- **YuE2-3B** weights = CC-BY-NC-4.0 · **TangoFlux** = Stability AI Community License (non-commercial)
  · **Auffusion** checkpoints = CC BY-NC-SA 4.0 · **IndexTTS2** = bilibili model-use agreement
  · **XTTS** = CPML (no v3 exists; Coqui defunct) · **seed-vc** = GPL-3.0 (MIT alt pulled instead).
  See research doc for full table.
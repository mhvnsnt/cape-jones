# ACE-Step 1.5 — Wiring (cape-jones)

**Upstream:** ace-step/ACE-Step-1.5 @ main (depth-1), pulled 2026-10-22.
**License:** MIT (own-eyes verified on upstream LICENSE, Copyright (c) 2026 ACEStep).
Code AND model weights both MIT; generated music is explicitly cleared for
commercial use by the authors. No NC / geography / AGPL catches.
**Tree:** 1222 files, 22MB, code-only. Zero weights/binaries committed —
checkpoints download GPU-side from Hugging Face at runtime.

## What it is

ACE-Step 1.5 is an open-source music-generation foundation model (StepFun +
ACE Studio): text-to-music with optional multi-language lyrics, plus cover /
repaint / edit / music-editing operations. The 1.5 turbo variant generates in
8 diffusion steps; the XL series (4B DiT) is the top-quality line.

This fills the **music slot** in the show/game pipeline. Until now the audio
chain was speech-only (KittenTTS / parler-tts / OpenVoice / RVC -> lip-sync);
ACE-Step produces original scores, theme songs, stings, and battle music from
text prompts + optional lyrics.

## Chain position

```
text/lyrics -> ACE-Step (score, themes, stings)
                                        \
                                         -> audio-separator (stem-split music if needed)
speech chain: TTS/RVC/OpenVoice -> lip-sync (MuseTalk/LatentSync)
```

Use cases: episode underscore + title themes with lyrics, Western Heart
character/entrance themes (e.g. Bannon walkouts), menu music, menu/sting
library. Originality check on generated tracks before publishing (see
upstream license disclaimer re: stylistic similarity).

## Runtime usage (Kaggle/Colab GPU)

Weights are NOT in this tree — download GPU-side:

- `acestep-v15-turbo` (~10GB all-in-one, 8-step) — fastest, good default.
- `acestep-v15-sft` — higher fidelity, 50 steps.
- `acestep-v15-xl-turbo` — top quality, >=12GB VRAM (offload).

Install: `pip install -r requirements.txt` (or use the repo's uv/docker flow).
Generate via CLI:

```
python cli.py --configure        # wizard, saves TOML config
python cli.py -c config.toml     # run generation
```

The CLI auto-downloads model checkpoints from Hugging Face
(`ACE-Step/acestep-v15-turbo`, `ACE-Step/acestep-v15-sft`,
`ACE-Step/acestep-v15-xl-base`, ...). Gradio UI: `start_gradio_ui.sh`.
API server: `start_api_server.sh`.

## Verified this pull

- `python3 -m py_compile cli.py acestep/pipeline.py` clean (entry points).
- No `.safetensors/.pt/.pth/.bin/.ckpt/.onnx` in tree (binary scan clean).
- Upstream `AGENTS.md` left intact (upstream's own agent notes, not ours).

Pulled per one-store/disk-rules: code-only, weights live GPU-side only.

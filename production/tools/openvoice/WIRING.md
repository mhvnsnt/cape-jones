# OpenVoice — Wiring Guide (cape-jones show pipeline)

**What:** Instant voice cloning by MIT and MyShell AI (paper arXiv 2312.01479).
Clones a speaker's vocal tone color from a SHORT reference clip and speaks new
text in that voice — including cross-lingual (English/Spanish/French/Chinese/
Japanese/Korean V2; zero-shot on unseen languages). Flexible style control:
emotion, accent, rhythm, pacing, intonation adjustable independently of the
tone color.

**Repo:** https://github.com/myshell-ai/OpenVoice — vendored 2026-10-19
(PR #160 wave); wiring notes added 2026-10-22.

**License:** MIT — own-eyes verified on upstream LICENSE (Copyright 2024
MyShell.ai): code AND model weights free for commercial use, no royalty,
no attribution requirement. One of the cleanest licenses in the audio chain.

**Pipeline position — the fast voice-draft link:**
```
script text → OpenVoice (zero-shot clone from a short clip, INSTANT draft)
            → RVC (trained character voice, production takes; production/tools/audio/rvc/)
            → demucs/audio-separator (stems) + faster-whisper (timestamps)
            → MuseTalk / LatentSync (lip-sync rendered video)
```
OpenVoice is the INSTANT path: hear a character voice in seconds from a ~10s
reference clip before spending time training an RVC model. Also the fallback
when you only have one clean line of reference audio — RVC wants minutes of
audio, OpenVoice works from a single short clip.

## Setup (GPU-side, Kaggle/Colab — weights NEVER committed)

```bash
cd production/tools/openvoice
python3 -m venv venv && source venv/bin/activate   # or: conda create -n openvoice python=3.9
pip install -e .

# V1 checkpoints (code + weights free under MIT):
curl -L -o ckpts.zip https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip
mkdir -p checkpoints && unzip -q ckpts.zip -d checkpoints
# (V2 checkpoint link + V2 install notes live in docs/USAGE.md)
```

The `checkpoints/` dir is git-ignored here on purpose — weights stay OFF the
repo and OFF local disk (download on the GPU box only).

## Usage

```bash
# Minimal gradio demo (style control + cross-lingual):
python -m openvoice.openvoice_app --share

# Notebook flows:
#   demo_part1.ipynb — flexible voice style control
#   demo_part2.ipynb — cross-lingual cloning
#   demo_part3.ipynb — advanced usage
```

Programmatic pattern (see `openvoice/api.py`): `OpenVoiceBaseClass` loads a
base-speaker TTS checkpoint; `ToneColorConverter` (via `se_extractor.get_se`)
maps the base speaker to the reference clip's tone color. The base speaker
model can be swapped for any VITS/VITS2 model you prefer for naturalness.

## Rules

- **Consented voices only.** Clone a voice only with the subject's explicit
  consent, or voices you own outright (your own, licensed character voices,
  consented contributor voices — Onyx, Theory, Bill $aber references, etc.).
  No scraping someone else's voice. Same standing rule as the RVC lane.
- **Weights rule:** checkpoints live in `checkpoints/` at runtime only.
  Never commit them. This directory is code + docs + demo mp3s only.

## Known limitations (from upstream docs/QA)

- PyTorch 1.13.x-era code (conda recipe pins python=3.9); may need version
  pinning on modern toolchains. Check docs/QA.md first when the demo misbehaves.
- Requires CUDA for the stock path (api.py asserts cuda when device contains
  'cuda'); CPU inference is not the designed path — keep it on the GPU lane.

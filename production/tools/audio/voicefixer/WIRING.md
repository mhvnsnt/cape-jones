# voicefixer — Wiring for the Cape Jones pipeline

**What:** `haoheliu/voicefixer` (pip package `voicefixer`) — general speech restoration.
Analysis stage (ResUNet) + synthesis stage (44.1kHz neural vocoder). One model handles
noise, reverb, low resolution (2kHz–44.1kHz) and clipping (0.1–1.0 threshold) — plus
speech super-resolution (e.g. phone-quality 8kHz → 44.1kHz).

**License:** MIT ✅ (own-eyes verified on upstream LICENSE, 2026-10-22 — standard MIT
text; the header carries template placeholders `[year] [fullname]` in the upstream
file itself, but the license grant text is the stock MIT grant). Commercial-safe.

**Pulled:** 2026-10-22 (main @ aae2253c85f97a87b844b6832384de249c23ab37, depth-1,
GitHub API reports MIT, 1,391 stars, not archived, last push 2025-02-17).
Trimmed: `test/utterance/` (1.5MB of test .flac/.wav fixtures) — test code kept.
Code-only 1.0MB. No weights in tree.

## Where it sits in the audio chain

```
recorded take → voicefixer (restore/de-reverb/de-clip/super-resolve)
  → demucs / audio-separator (stem split) → RVC (character voice)
  → MuseTalk/LatentSync (lip-sync)
```

- **DeepFilterNet** (sibling pull, same chain) is the *lightweight real-time*
  noise suppressor — use it live or for clean-enough takes.
- **voicefixer** is the *heavy restorer*: use it when a take is genuinely degraded —
  noisy room, phone/intercom source, clipped peaks, or 8–16kHz source needing
  upsampling to full-band 44.1kHz before RVC training or lip-sync.
- Run voicefixer FIRST (it wants the raw degraded waveform), then stem-split.

## Setup

Weights stay GPU-side, downloaded at runtime into `~/.cache/voicefixer/`, never committed:

```bash
pip install voicefixer==0.1.2
# first run downloads: vf.ckpt (analysis) + model.ckpt-1490000_trimed.pt (vocoder)
```

## Usage

```bash
# CLI — restore one file (mode 0 = original model, default)
voicefixer --infile noisy_take.wav --outfile clean_take.wav

# folder batch
voicefixer --infolder takes/ --outfolder takes_restored/

# modes: 0 = original (default), 1 = preprocessing (strip high freq),
#        2 = train mode (sometimes helps on seriously degraded real speech)
voicefixer --infile bad.wav --outfile fixed.wav --mode 2
```

```python
# Python API
from voicefixer import VoiceFixer
vf = VoiceFixer()
vf.restore(input="noisy_take.wav", output="clean_take.wav",
           cuda=False, mode=0)
```

Output is 44.1kHz — resample to 48kHz for DeepFilterNet or keep 44.1k for RVC.

## Pipeline uses for the show

1. **Rescue bad dialogue takes** — de-reverb + denoise a take recorded in a live
   room so it doesn't need a re-record.
2. **Phone/intercom effect reversal** — super-resolve a deliberately-lo-fi source
   when the episode needs the clean version too.
3. **Declip hot takes** — recover dialogue recorded too hot (clipping 0.1–1.0).
4. **Pre-RVC cleanup** — restore before character-voice conversion so RVC trains
   on clean 44.1kHz audio.

## Notes

- Mode 2 ("train mode") is experimental upstream — spot-check output before
  batching it.
- The analysis checkpoint + vocoder (~1–2GB together) download on first use;
  on Kaggle/Colab lanes, pre-warm the cache before the lane starts.
- Upstream repo is quiet (last push 2025-02-17) but the released checkpoints are
  stable and widely used — pinned here via the pulled tree + pip pin above.

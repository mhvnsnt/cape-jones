# Wan2.2 — WIRING

**Upstream:** Wan-Video/Wan2.2 (main @ 1ea34ff4, 2026-10-22 — 18,108 stars, active, pushed 2026-09-21)
**What:** Alibaba Wan team's second-generation open video foundation suite — the successor to Wan2.1.
Biggest leaps over 2.1: **Mixture-of-Experts (MoE)** denoising architecture (experts split across
timesteps — bigger capacity, same compute), cinematic-level aesthetic training (lighting/composition/
contrast/color labels), +83.2% more training video for complex motion, and a **TI2V-5B** hybrid model
that does **720P@24fps** text+image-to-video on a consumer 4090.
**Pipeline slot:** VIDEO GENERATION. Sibling of `production/tools/ltx-video/` (PR #186, fast DiT),
`production/tools/ltx2/` (PR #199, synced audio+video) and `production/tools/wan2.1/` (PR #201,
unified editing/VACE). Wan2.2 is the **hero-shot + talking-head** lane: S2V (audio-driven cinematic
video) for dialogue scenes, Animate-14B (character animation/replacement) for rotoscope-style
character work.

## LICENSE — READ BEFORE USE (own-eyes verified 2026-10-22)

Upstream `LICENSE.txt` is the **Apache License 2.0** verbatim ("TERMS AND CONDITIONS FOR USE,
REPRODUCTION, AND DISTRIBUTION"; sha256 c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 —
identical text to the Wan2.1 LICENSE.txt pulled in PR #201), and the gh API license field reads
`Apache-2.0`. Free to use, modify, and distribute, **including commercial use**, with no revenue
threshold and no weight-license caveats. Not archived, default branch `main`.

## Layout

```
production/tools/wan2.2/
├── wan/                      # model code: text2video.py, image2video.py, text_image2video.py,
│                             # speech2video.py, animate/, modules/, configs/
├── generate.py               # main CLI inference entry (t2v / i2v / ti2v / s2v / animate)
├── gradio/                   # Gradio demos
├── examples/                 # sample inputs
├── assets/                   # README diagrams only (no weights)
├── tests/                    # test.sh + README
├── requirements.txt          # torch>=2.4.0, flash_attn, etc.
├── requirements_animate.txt  # Animate-14B extras
├── requirements_s2v.txt      # S2V extras (+ CosyVoice TTS support)
├── INSTALL.md / README.md    # upstream docs
├── LICENSE.txt               # Apache-2.0 (verified)
└── WIRING.md                 # this file
```

No `.github/` in upstream (nothing stripped on pull). No weights/binaries in tree (verified —
assets/examples are doc PNGs/JPGs only). `git lfs` carries nothing. Upstream `.git` removed by
pull-to-repo.sh.

## Tasks (what each module does)

| Task | Weight (HF `Wan-AI/`) | Use for the show pipeline |
|---|---|---|
| **Text-to-Video (T2V-A14B)** | `Wan2.2-T2V-A14B` (480P+720P, MoE) | Hero establishing shots, stylized plates; top-tier quality tier |
| **Image-to-Video (I2V-A14B)** | `Wan2.2-I2V-A14B` (480P+720P, MoE) | Animate keyframes / character art into motion |
| **Text-Image-to-Video (TI2V-5B)** | `Wan2.2-TI2V-5B` (720P@24fps) | Fast previz + rapid iteration on consumer GPU (4090 class); LightX2V/cache-dit distilled variants exist |
| **Speech-to-Video (S2V-14B)** | `Wan2.2-S2V-14B` (480P+720P) | **Audio-driven cinematic video** — drive a character's performance from dialogue audio; pairs with the TTS chain (Higgs Audio PR #196, CosyVoice PR chain, Qwen3-TTS PR #197); CosyVoice TTS support built in (`requirements_s2v.txt`) |
| **Animate-14B** | `Wan2.2-Animate-14B` (Diffusers integration PR #12526) | **Character animation + replacement** — holistic movement/expression replication from a driving video; the rotoscope lane. Try at wan.video / ModelScope Studio / HF Space `Wan-AI/Wan2.2-Animate` |
| **VACE** | `Wan2.1-VACE-*` (via sibling `wan2.1/`) | Wan2.2 repo focuses on generation; unified editing stays in the wan2.1 pull |

Diffusers integrations exist for T2V-A14B / I2V-A14B / TI2V-5B (HF `-Diffusers` repos); ComfyUI native
support (docs.comfy.org tutorial) + Kijai's ComfyUI-WanVideoWrapper cutting-edge optimizations.
Low-GPU-memory options: DiffSynth-Studio (layer-by-layer offload, FP8), LightX2V distillations.

## Weights — GPU/KAGGLE SIDE ONLY, NEVER COMMITTED

Download on the GPU lane:

```bash
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B
```

TI2V-5B is the Kaggle T4 starting point for 720P; A14B MoE models want pro-tier VRAM. ModelScope
mirrors exist for every weight (`Wan-AI/Wan2.2-*`).

## Show-pipeline uses (first ideas)

1. **Dialogue scenes:** S2V-14B driven by our TTS chain (dialogue → audio-driven cinematic video).
2. **Character acting:** Animate-14B to transfer motion/expression from reference footage onto our
   characters (rotoscope lane; pairs with `mesh2motion/` and mocap tools).
3. **Previz:** TI2V-5B at 720P@24fps for fast shot iteration before hero renders.
4. **Hero shots:** T2V/I2V-A14B MoE models for cinematic plates.

## Slot map

VIDEO GENERATION now: ltx-video (speed) → ltx2 (synced A/V) → wan2.1 (unified editing/directed
shots, cheapest VRAM) → **wan2.2 (MoE hero quality + S2V talking-heads + Animate rotoscope)**.
Wan2.2 vs Wan2.1: pick 2.2 for talking-head/dialogue and hero cinematic quality; pick 2.1 for VACE
unified editing and the 1.3B cheap tier.

# Wan2.1 — WIRING

**Upstream:** Wan-Video/Wan2.1 (main @ 2026-10-22, 17,281★, active — pushed 2026-03-05)
**What:** Alibaba Wan team's full open video-foundation-model suite — text-to-video, image-to-video, first-last-frame-to-video, unified video editing (VACE), text-to-image, and video-to-audio. Ranked #1 on VBench at release; the 1.3B variant runs on ~8.2 GB VRAM (consumer GPU / Kaggle T4-friendly).
**Pipeline slot:** VIDEO GENERATION. Sibling of `production/tools/ltx-video/` (LTX-Video v1, PR #186 — fast DiT video-only) and `production/tools/ltx2/` (LTX-2, PR #199 — synced audio+video). Wan2.1 is the **unified editing + reference-based generation** step up: VACE's Video Condition Unit takes text + images + video + masks in one interface (character/object replacement with references, pose-controlled animation, first↔last frame bridging), and the 1.3B tier is the cheapest to run locally of the whole slot.

## LICENSE — READ BEFORE USE (own-eyes verified 2026-10-22)

Upstream `LICENSE.txt` is the **Apache License 2.0** (verbatim, "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION"), and the gh API license field reads `Apache-2.0`. Free to use, modify, and distribute, **including commercial use**, with no revenue threshold. No caveats (unlike LTX-2's $10M Community-License gate — Wan2.1 is the unrestricted license in this slot).

## Layout

```
production/tools/wan2.1/
├── wan/                    # model code: text2video.py, image2video.py, first_last_frame2video.py,
│                           # vace.py, modules/, configs/, distributed/
├── generate.py             # main CLI inference entry
├── gradio/                 # Gradio demos: t2v (1.3B/14B), i2v, t2i, fl2v, vace
├── examples/               # sample input frames (snake.png, girl.png, FLF2V first/last frames)
├── assets/                 # README diagrams only
├── tests/                  # test.sh + README
├── requirements.txt        # torch, diffusers (T2V/I2V also in diffusers natively), etc.
├── INSTALL.md / README.md  # upstream docs
├── LICENSE.txt             # Apache-2.0 (verified)
└── WIRING.md               # this file
```

No `.github/` in upstream (nothing stripped on pull). No weights/binaries in tree (verified — assets/examples are doc PNGs/JPGs only). `git lfs` carries nothing. Upstream `.git` was removed by pull-to-repo.sh.

## Tasks (what each module does)

| Task | Entry | Use for the show pipeline |
|---|---|---|
| **Text-to-Video** | `wan/text2video.py`, `generate.py --task t2v` | Establishing shots, B-roll, stylized background plates from prompts |
| **Image-to-Video** | `wan/image2video.py`, `generate.py --task i2v` | Animate show stills / keyframes / character art into motion (the ToonCrafter-adjacent slot, but DiT-native) |
| **First-Last-Frame-to-Video** | `wan/first_last_frame2video.py` | Bridge two keyframes (inbetweening between drawn poses — pairs with AnimeInbet/ToonCrafter) |
| **VACE (unified editing)** | `wan/vace.py`, `gradio/vace.py` | The killer lane: one model for video creation AND editing — character/object replacement via reference images, pose-controlled animation, mask-guided inpainting. This is the closest open equivalent to a "direct the shot" tool for our characters |
| **Video-to-Audio** | V2A task | Generate matching SFX/ambience for a clip (pairs with the audio chain: MMAudio PR #198, ACE-Step #192) |

Gradio one-click demos exist for t2v (1.3B + 14B), i2v, t2i, fl2v, and vace — fastest way to eyeball a model on the GPU lane.

## Weights — GPU/KAGGLE SIDE ONLY, NEVER COMMITTED

All on HuggingFace `Wan-AI/` (ModelScope mirrors exist):

| Weight | Repo | Res | VRAM class |
|---|---|---|---|
| T2V-14B | `Wan-AI/Wan2.1-T2V-14B` | 480P + 720P | pro tier (multi-GPU ideal) |
| T2V-1.3B | `Wan-AI/Wan2.1-T2V-1.3B` | 480P | ~8.2 GB — Kaggle T4 / consumer GPU |
| I2V-14B-720P / -480P | `Wan-AI/Wan2.1-I2V-14B-720P` | 720P / 480P | mid–pro tier |
| FLF2V-14B-720P | `Wan-AI/Wan2.1-FLF2V-14B-720P` | 720P | mid–pro tier |
| VACE-14B / VACE-1.3B | `Wan-AI/Wan2.1-VACE-14B` | 480P+720P / 480P | mid–pro / ~8 GB class |

Download on the GPU lane:

```bash
pip install "huggingface_hub[cli]"
huggingface-cli download Wan-AI/Wan2.1-T2V-1.3B --local-dir ./Wan2.1-T2V-1.3B
```

Tip: T2V/I2V are also integrated into **diffusers** natively (`diffusers.WanPipeline`, `WanImageToVideoPipeline`) — the GPU lane can skip this tree's `wan/` code entirely and just use diffusers if it prefers.

## Show-pipeline uses (Cape Jones / Wizard Gang)

1. **Keyframe animation:** render a show keyframe (Blender), feed it to I2V → 5s motion shot. Cheaper than hand-animating secondary motion.
2. **First↔last bridging:** two drawn/extreme poses → FLF2V generates the inbetween — complements ToonCrafter (which is cartoon-trained) with DiT quality.
3. **VACE character direction:** reference image of Cape Jones / Pantera / Star + pose/mask control → directed shot variants without re-rendering in Blender.
4. **V2A:** generate matching SFX for a rendered clip, then layer the audio chain (MMAudio / ACE-Step / voicefixer) on top.
5. **720P 14B tier:** hero shots only (slow); 1.3B/480P for iteration, Real-ESRGAN (`production/tools/realesrgan/`) upscales to presentation.

## Verification (this pull, 2026-10-22)

- gh API: 17,281★, not archived, default `main`, pushed 2026-03-05, license `Apache-2.0`, ~10 MB.
- License own-eyes: `LICENSE.txt` raw text = Apache License 2.0 (sha256 c71d239d…), no commercial-use restriction.
- Tree: 11 MB code-only, 0 files >50 MB, 0 weight binaries, no `.github/`, no lfs blobs.
- **36/36 `.py` pass `py_compile`.**
- Slot duplicate pre-check: `production/tools/` had `ltx-video/` + `ltx2/` only — no wan* entry; pull doc (`docs/research/2026-PULL-SUMMARY.md`) carried only the LTX-Video row (LTX-2 row was never recorded — backfilled in this PR).

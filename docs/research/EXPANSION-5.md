# EXPANSION-5: Continuous Research — 2026 Bleeding Edge + Established Tools

Date: 2026-10-16
Two parallel research lanes. Raw findings recovered from child agent session logs.

---

## TRACK 1: 2026 Bleeding Edge — PULLED (4 repos, ~39MB, code only)

### 1. Kandinsky 6.0 (released 2026-10-06) ⭐ TOP FIND
- **Path:** `~/workspace/tools/kandinsky-6/` (29MB, code only)
- **URL:** https://github.com/kandinskylab/kandinsky-6
- **What:** Text-to-video + AUDIO in one pass (Lite 3B / Pro 29B). 5s clips at 44kHz with **lip-synced dialogue**, ships with ComfyUI integration (`comfyui/` dir), works in Diffusers/vLLM-omni/SGLang.
- **Why:** Biggest find — single-pass dialogue clips with mouth movement matching the spoken line. Potential dialogue-shot generator for the show.
- **License:** MIT (verified).
- **Weights:** NOT pulled (multi-GB). HF `kandinskylab/Kandinsky-6.0-Pro-5s-Diffusers` (MIT) — Kaggle candidate for the dialogue lane.
- **Paper:** huggingface.co/papers/2610.05608

### 2. LuxTTS
- **Path:** `~/workspace/tools/luxtts/` (1.1MB)
- **URL:** https://github.com/RazdorPaul/LuxTTS
- **What:** ZipVoice-based TTS with 3-second zero-shot voice cloning; 150× real-time on GPU, 48kHz output, fits in <1GB VRAM. Model + code both Apache-2.0.
- **Why:** Cartoon-voice generation for the cast at high quality with tiny compute footprint.
- **License:** Apache-2.0 (verified in LICENSE file).
- **Weights:** HF `YatharthS/LuxTTS` (Apache-2.0) — Kaggle candidate for voice lane.

### 3. BoyoLuxTTS-Comfyui
- **Path:** `~/workspace/tools/boyoluxtts-comfyui/` (1.6MB)
- **URL:** https://github.com/DragonDiffusionbyBoyo/BoyoLuxTTS-Comfyui
- **What:** ComfyUI custom nodes wrapping LuxTTS (voice cloning + speech in-graph).
- **Why:** Drops voice generation directly into the existing ComfyUI cartoon pipeline.
- **License:** Apache-2.0 (verified).

### 4. beatra-skills (curated subset)
- **Path:** `~/workspace/tools/beatra-skills/` (7.4MB)
- **URL:** https://github.com/beatra-ai/beatra-skills
- **What:** 21 animation/audio-relevant agent skill playbooks kept; ~124 unrelated ones pruned: `ai-storyboard-generator` (script → shot plan → key frames), `ip-character-consistency-studio`, `ai-multilingual-dubbing`, `voice-clone-series-studio`, `voice-cloning-studio`, `audio-drama-voice-studio`, `short-form-voiceover-audio`, `voiceover-narration-studio`, `ai-music-video-clip-maker`, `image-to-motion`, `talking-avatar-video`, `photo-singing-video`, `beatra-ai-video-studio`, `beatra-ai-voice-studio`, `beatra-ai-image-studio`, `ai-short-drama-shot-maker`, `ai-comic-drama-shot-maker`, `first-last-frame-video`, `assembly-one-step-clip`, `bilibili-video-storyboard`, `whiteboard-animation-maker`.
- **Why:** `ai-storyboard-generator` is a ready-made shot-planning skill for the storyboard lane.
- **License:** MIT-0 / MIT No Attribution (verified).
- **Caution:** The bundle ships a `minimax-h3-ai-video` skill — H3 is LICENSE-TOXIC for US production (see exclusions). Do not use.

### Documented, not pulled — license traps / out of scope
- **MangaNinja** (reference-based line-art colorization): CC-BY-NC 4.0 — non-commercial. Excluded.
- **Breeze TTS 2:** code Apache-2.0 but weights research/non-commercial. Excluded (already on traps list).
- **MiniMax H3:** territorial exclusion (excludes US/EU/UK/KR). Already on traps list.
- **sesly** (local voice studio, Sept 2026): AGPL-3.0 + default weights CC-BY-NC; large Electron app. Documented only.
- **YuE2-3B** music: CC-BY-NC 4.0 weights. Not pulled.
- **TangoFlux** (text→SFX, ICLR 2026): could not verify canonical repo + license. Not pulled — needs re-check.
- **Anime-layer-decomposition** (Mar 2026): outside 60-day window + repo 404s. Not pulled.
- **Foley-Omni** (MIT, June 2026, single-pass video→dialogue+SFX+music): outside 60-day window. Near-miss, documented.
- **weizhi999/cartoon-animator-pro-tools:** pirated software distribution (Reallusion Cartoon Animator). Excluded as illegitimate.

### Notable Apache-clean voice engines (for reference, Kaggle lane)
- **MOSS-TTS-Nano** (OpenMOSS, Apache-2.0, 0.1B CPU-realtime 48kHz cloning, 20 languages): HF `OpenMOSS-Team/MOSS-TTS-Nano-100M`
- **CosyVoice 3 / dots.tts / Confucius4-TTS:** all Apache-2.0 per vendor tables
- **Tether TranscribePsy** (2026-10-15, Apache-2.0): offline STT, 10min audio in 1.65s on iPhone

### Failures / non-finds
- No new sketch-inbetweening or character-animation papers in the last 60 days beyond what was already pulled.
- No new-in-60-days ComfyUI cartoon node packs with verified permissive licenses found.

---

## TRACK 2: Established Tools — PULLED (8 repos + 1 bonus, 4 custom scripts, ~69MB)

| # | Name | URL | What it does / why relevant | License | Size | Path |
|---|------|-----|------------------------------|---------|------|------|
| 1 | **lvsfunc** | https://github.com/Irrational-Encoding-Wizardry/lvsfunc | The standard VapourSynth function library of the anime-encoding scene — deblock, dedither, scaling, masking, detail/deband helpers. Proven deband/denoise chains for scanned hand-drawn art. | MIT | 7.4MB | `~/workspace/tools/lvsfunc/` |
| 2 | **kagefunc** | https://github.com/Irrational-Encoding-Wizardry/kagefunc | VapourSynth anime helpers: `adaptive_grain`, `retinex_edgemask` (line-art masking), `hybriddenoise`, `mask_descale`. Line-mask → line-darken is exactly what scanned ink cleanup needs. | MIT | 44KB | `~/workspace/tools/kagefunc/` |
| 3 | **GreaseWriter** | https://github.com/doakey3/GreaseWriter | Blender addon: auto-animates grease-pencil strokes with pauses to emulate hand-drawn writing/drawing, stipple redraw, stroke tracing. | GPL-3.0 | 6.8MB | `~/workspace/tools/greasewriter/` |
| 4 | **auto-caption** | https://github.com/sebetancurch/auto-caption | CapCut-style karaoke captions, fully local: faster-whisper word timestamps → grouped caption lines → animated `.ass` → FFmpeg burn-in (also emits DaVinci SRT). (Whisper model downloads separately on first use — not pulled.) | MIT | 580KB | `~/workspace/tools/auto-caption/` |
| 5 | **Palettator** | https://github.com/Franck-Demongin/Palettator | Python palette extractor: k-means palette from art → exports CSV/JSON/**GPL (Krita/GIMP)**/ACO. | GPL-3.0 | 1.1MB | `~/workspace/tools/palettator/` |
| 6 | **frei0r** | https://github.com/dyne/frei0r | Canonical cross-platform video plugin set, consumed natively by FFmpeg. Cartoon-relevant: `cartoon`, `squigglevision` (boiling-line wobble), `sobel`, `edgeglow`, `posterize`, `colorhalftone`, `filmgrain`, `gateweave`, `scanline0r`, `vignette`, plus `equaliz0r`/`curves`/`levels` for grading. Needs cmake build before FFmpeg can load it (`FREI0R_PATH`); `cartoon-fx.sh` assumes plugins installed. | GPL-2.0 | 20MB | `~/workspace/tools/frei0r/` |
| 7 | **krita-spritesheet-generator** | https://github.com/ShannonHG/krita-spritesheet-generator | Krita plugin exporting animations as spritesheets. Most recently maintained of the three spritesheet exporters found. | MIT | 92KB | `~/workspace/tools/krita-spritesheet-generator/` |
| 8 | **color-thief** | https://github.com/lokesh/color-thief | Dominant-color/palette extraction from images, browser + Node (13.6k stars, maintained 2026). Scriptable palette pulls for web tooling. | MIT | 524KB | `~/workspace/tools/color-thief/` |
| 9 | **SPAN (span-official)** | https://github.com/cszn/BSRGAN / NTIRE 2024 winner | Swift Parameter-free Attention Network for efficient super-resolution. Fast upscale for frames/art. | Apache-2.0 | 34MB | `~/workspace/tools/span-official/` |

### REMOVED — license trap caught post-pull
- **comfyui-rife-tensorrt:** license is **CC-BY-NC-SA-4.0** (non-commercial). NOT commercial-safe → deleted from `~/workspace/tools/`. Use our existing MIT RIFE nodes instead.

### Custom scripts built (all tested, in `~/workspace/tools/post-pipeline/`)
- **`vs-anime-cleanup.vpy`** — VapourSynth chain using kagefunc/lvsfunc: denoise → f3kdb deband → retinex line-mask line-darkening → adaptive grain, env-var driven. (Requires VapourSynth + ffms2; f3kdb degrades gracefully if missing.)
- **`cartoon-fx.sh`** — FFmpeg+frei0r recipe chains: `boil`, `ink`, `toon`, `halftone`, `grain`, `weave`, `scan`, `vig`, `sharp`; chainable with `+`.
- **`fx-particles.py`** — **deterministic** seeded particle FX (fire/smoke/sparkle/speedlines/explosion/magic) → PNG sequences. Same seed = byte-identical frames (verified via diff). Fills the 2D particle gap without AI.
- **`palette-enforce.py`** — seeded k-means palette extraction from key art → `.gpl`/`.json`/`.css`, then quantizes frames to the enforced palette.

### Skipped with reason
- **tiny-2d-rig-tools** (Blender 2D cutout rigging): **no license** → not commercial-safe, not pulled.
- **n3rdw1z4rd/particles:** **no license** → not pulled.
- **tsParticles** (MIT): no seeded-RNG support (grep found zero seed handling) → fails deterministic requirement; custom `fx-particles.py` covers it.
- **python-lottie:** AGPL-3.0 (copyleft risk) and redundant — Glaxnimate (already pulled) natively handles Lottie/animated SVG/Android Vector Drawables + FFmpeg render.
- **Production-tracking alternatives (Plane, Taiga, etc.):** large web apps, none cartoon-specific; Kitsu remains the animation-industry standard.
- **Storyboard/animatic beyond Storyboarder:** no *established* open alternative found (commercial, in-progress, or AI-pipeline toys). Storyboarder + Blender GP + Kdenlive remain the answer.
- **TupiTube, Enve, Wick Editor, Olive 0.2:** explicitly dead; not touched.

### Coverage check per gap
1. Krita animation plugins → ✅ spritesheet exporter
2. Blender 2D addons → ✅ GreaseWriter
3. FFmpeg cartoon filters → ✅ frei0r + cartoon-fx.sh
4. VapourSynth anime cleanup → ✅ lvsfunc + kagefunc + vs-anime-cleanup.vpy
5. Storyboard/animatic → ⚠️ no established tool found (open gap)
6. Subtitles/karaoke → ✅ auto-caption
7. Deterministic 2D particles → ✅ fx-particles.py (custom)
8. Palette management → ✅ Palettator + color-thief + palette-enforce.py
9. Production tracking → ⚠️ Kitsu stands (alternatives evaluated, too big)
10. Lottie/vector web export → ✅ already covered by Glaxnimate

---

## Wiring

New scripts wired into `production/pipeline/` (cape-jones repo):
- `vs-anime-cleanup.vpy`, `cartoon-fx.sh`, `fx-particles.py`, `palette-enforce.py`

Kaggle setup needed for GPU tools:
- Kandinsky 6.0: download `kandinskylab/Kandinsky-6.0-Pro-5s-Diffusers` from HF (MIT) — dialogue-shot experiments
- LuxTTS: download `YatharthS/LuxTTS` from HF (Apache-2.0) — voice lane
- SPAN: download weights from span-official repo releases — fast frame upscaling

Feed into lanes:
- `beatra-skills/skills/ai-storyboard-generator/SKILL.md` → storyboard lane design
- BoyoLuxTTS-Comfyui → copy to `ComfyUI/custom_nodes/`

## Disk Impact

Total new pulls this round: ~108MB (code only). All model weights stay on Kaggle.
Disk: 80% (was 83% at pull time, now 80% after NC-tool removal + earlier cleanup). Approaching 85% threshold — prioritize TeraBox offload.

## Repo Push

- 4 custom scripts → `mhvnsnt/cape-jones` `production/pipeline/` (branch → PR → merge)
- This doc → `docs/research/EXPANSION-5.md`

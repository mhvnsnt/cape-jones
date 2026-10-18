# CONTINUED PULL (2026-10-16) — Filling the Gaps

Owner: "keep pulling more stuff in that would be relevant." Aggressive gap-fill pass.

## Gap Analysis (from full tools inventory review)

| Gap | Status | Solution |
|-----|--------|----------|
| Storyboard → timed animatic (auto) | ❌ Missing | ✅ Built `animatic_builder.py` |
| Anime speed lines / impact frames | ❌ Missing | ✅ Built `anime_fx.py` |
| Screen shake for hits | ❌ Missing | ✅ Built into `anime_fx.py` |
| VHS / CRT / retro effects | ❌ Missing | ✅ Built `retro_fx.py` |
| Social delivery presets (TikTok/Shorts/IG) | ❌ Missing | ✅ Built `social_export.sh` |
| Anime-specific upscale/interpolate/restore | ❌ Missing | 🔄 Cloning TheAnimeScripter |
| Title cards / kinetic typography / bumpers | ❌ Missing | ✅ Cloned html-animation |
| Browser-based storyboard w/ audio timing | Partial (Storyboarder) | ✅ Cloned choxos/storyboard |
| Script → narrated video (auto animatic) | ❌ Missing | ✅ Cloned explainroo |
| Anime-style 3D rendering (cel shader) | ✅ Pulled | three-anime-style in production/tools/ (MIT, pulled 2026-10-16) |

## Custom-Built Pipeline Scripts

All in `post-pipeline/`, all CPU-only, all tested.

### `anime_fx.py` — Anime 2D effect overlays
- `--speed-lines`: Radial manga speed lines (surprise/speed). Transparent PNG sequence.
- `--impact`: White flash + starburst impact frames.
- `--speed-overlay INPUT`: Composite speed lines onto video at timestamp.
- `--shake-input INPUT`: Screen shake via animated crop (for hits/explosions).
- Tested: generates correct radial lines, verified visually.

### `retro_fx.py` — VHS/CRT retro effects
- `--vhs`: Tracking distortion + chromatic aberration + noise + soft blur.
- `--crt`: Scanlines + vignette + phosphor glow.
- `--chromatic` / `--noise` / `--scanlines`: Individual effects.
- `--intensity 0.1-2.0`: Strength control.
- For the trippy/Adult Swim vibe segments.

### `social_export.sh` — Social delivery presets
- `tiktok`/`shorts`/`reels`: 9:16 (1080x1920), smart center crop.
- `instagram-square`: 1:1 (1080x1080).
- `instagram-portrait`: 4:5 (1080x1350).
- `--focus-top` / `--focus-bottom`: Crop bias for character framing.
- All outputs: yuv420p + faststart (platform-compatible).

### `animatic_builder.py` — Storyboard → timed animatic
- Input: board images + CSV/JSON timing file.
- Optional: temp audio track, crossfade transitions.
- Output: 1080p MP4 animatic at 24fps.
- Closes the Storyboarder → animation gap.

## Cloned Tools

### `html-animation/` (acelera-agency, MIT, 14MB)
Motion graphics as code. Frame-exact animated logos, kinetic typography.
**Key feature**: exports MP4 in 1:1, 4:5, AND 9:16 from a single HTML file.
Use for: Adult Swim-style bumpers, title cards, "___ JONES" name gags.

### `storyboard/` (choxos, MIT, 1.1MB)
Browser + Tauri motion graphics editor. Storyboard → keyframes → audio timing → video export.
New (Sept 2026). Complements Storyboarder with web-based workflow.

### `explainroo/` (vincentsch, 6.4MB)
Script → narrated explainer video. Kokoro voice + Whisper timing + canvas renderer → MP4.
Use for: automated temp animatics with scratch dialogue.

### `TheAnimeScripter/` (NevermindNilas, ✅ core pulled, 7.5MB)
THE anime video toolkit. Updated 4 days ago. Core CLI + src/ modules intact.
Models download on-demand (by design).
- Upscale: 15+ anime-specific models (AnimeSR, AniScale 2, SPAN, etc.)
- Interpolate: RIFE 4.6–4.26, GMFSS Fortuna
- Restore: denoise, deblur, dehalo, deband (anime-tuned)
- Dedup, scene detection, depth maps, segmentation
- CLI + standalone + After Effects panel
This replaces/augments our generic RIFE pipeline with anime-specific models.

## Pipeline Integration

```
Storyboarder / storyboard/ → boards
  → animatic_builder.py → timed animatic (+ temp audio)
  → [owner draws keyframes]
  → ToonComposer / ToonCrafter → animation
  → anime_fx.py → speed lines / impact / shake
  → retro_fx.py → VHS/CRT grade (optional)
  → finish.py → color grade + audio mix
  → social_export.sh → TikTok / Shorts / IG versions
  → delivery
```

## Still To Pull (network blocked, retry later) — RESOLVED 2026-10-16
- `three-anime-style/` (xymeow, MIT): Cel-shaded anime rendering for Three.js 3D segments — ✅ PULLED 2026-10-16 into `production/tools/three-anime-style/` (22MB). NOTE: unblock-browser-items.json claimed a sibling agent had pulled it, but it was NOT on main — verified against the repo and pulled fresh.
- `video-gif-studio/` (miles990): Storyboard planning + music beat analysis — ✅ RECOVERED via PR #34 (126MB, on main).
- `AnimeEffects/` (AnimeEffectsDevs): 2D animation tool (GPL-3.0) — ✅ cloned (17MB).
- `hyperframes-effects-gallery/`: 255-effect catalog (transitions, captions) — ✅ correct URL found (genoooool/hyperframes-effects-gallery), PULLED 2026-10-16 into `production/tools/hyperframes-effects-gallery/` (427MB: 230MB previews, 1.5MB catalog JSON). License caveat: upstream effects keep original licenses per THIRD_PARTY_NOTICES.md.
- `cartoon-studio/` (Jellypod-Inc, **Apache-2.0 — commercial use OK**): 2D animated cartoon-show studio desktop app (Electron + Vite + TypeScript) — script in, MP4 out. Stage (drag SVG chars onto 1920x1080 canvas), Dialogue (87 voices across 8 TTS providers w/ word timestamps), Play (film-cabinet preview, render to MP4). Key pieces for our pipeline: `scripts/rig-svg.ts` CLI (SVG mouth auto-rig, 9-shape Preston Blair/Rhubarb mouth catalog, vowel-heuristic lip-sync cues), HyperFrames HTML→MP4 render path (pairs with our `hyperframes-effects-gallery/` pull), reproducible output from script+voices+characters (no LLM in the render loop). ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/cartoon-studio/` (6.4MB, source-only, no node_modules, commit e773568f). Note: runs on API keys (BYOK, encrypted in OS keyring); upstream TTS/LLM keys are owner-provided — render code itself is offline-capable. Candidate uses: Ashes mouth-pack SVG rigging workflow, episode animatic→MP4 render path evaluation.

### `AnimeEffects/` (AnimeEffectsDevs, ✅ cloned, 17MB)
2D modular animation tool. GPL-3.0. Updated Dec 2025. C++ based.

### `pencil2d/` (pencil2d, ✅ cloned, 20MB)
Hand-drawn 2D frame-by-frame animation app (Qt/C++). Bitmap + vector layers, onion skinning, camera layer, sound scrubbing. GPL-2.0 verified (LICENSE.TXT in-tree + GitHub API spdx_id=GPL-2.0, commercial use OK); upstream active (updated 2026-10-17). Upstream `.github/` workflows stripped per convention. ✅ PULLED 2026-10-18 (run: overnight-idle-pipeline) into `production/tools/pencil2d/` (610 files, shallow depth-1, no binaries >50MB). Candidate uses: hand-drawn 2D keyframes for Cape Jones shorts, EP01 gag-book sketches (fills the lightweight-frame-by-frame slot from FULL-PRODUCTION-STACK.md row 197).

## Disk Impact
Custom scripts: <50KB. Clones: ~42MB. Total pull: <45MB.

## Retry Status (2026-10-16 ~04:00 EDT) — updated ~16:30 EDT
- `three-anime-style/`: ✅ PULLED 2026-10-16 into production/tools/three-anime-style/ (MIT, 22MB).
- `video-gif-studio/`: ✅ recovered via PR #34 (on main).
- `hyperframes-effects-gallery/`: ✅ correct URL found (genoooool/hyperframes-effects-gallery). Status below.

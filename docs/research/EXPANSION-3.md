# EXPANSION-3 — Voice, Foley, 2D Rigging, Compositing

Pulled 2026-10-16. Focus: gaps the toolkit didn't cover yet.

## 1. AI Voice Acting / Dialogue

| Tool | Location | License | What | GPU |
|------|----------|---------|------|-----|
| **Dia2** (Nari Labs) | `tools/Dia/` | Apache-2.0 | Dialogue-first TTS. `[S1]`/`[S2]` multi-speaker tags, emotion tags `(laughs)` `(sighs)`, voice cloning. Built for character dialogue. | T4 (Kaggle) |
| **OpenVoice** (MyShell) | `tools/OpenVoice/` | MIT | Instant voice cloning + emotion/accent control. 30k stars. | T4 (Kaggle) |
| **Parler-TTS** (HF) | `tools/parler-tts/` | Apache-2.0 | Text-described voice control ("deep heroic voice, slightly bored"). No reference audio needed. | T4 (Kaggle) |
| **Bark** (Suno) | `tools/bark/` | MIT | Non-verbal sounds: laughs, sighs, gasps, music snippets. Perfect for cartoon acting. | T4 (Kaggle) |

Already had: Chatterbox (MIT, cloning+emotion), Kokoro (Apache-2.0, CPU-fast 82M).

**New pipeline script:** `post-pipeline/dialogue_pipeline.py`
- Takes a dialogue JSON script → per-line WAVs + `timing.json`
- Engine priority: dia2 → chatterbox → kokoro → bark → espeak-ng (fallback)
- Output feeds `tools/lipsync/` (Rhubarb/OpenFaceFX) for visemes
- Usage: `python3 dialogue_pipeline.py script.json out_dir/ --engine auto`

**License flags (documented, NOT pulled):**
- Fish Speech (28k stars, 15k emotion tags) — weights are CC-BY-NC. Non-commercial only. Skip for monetized shows.
- Breeze TTS 2 (beats ElevenLabs v3 on leaderboard) — weights non-commercial. Skip.

## 2. Music / Sound Design — AI Foley

| Tool | Location | License | What | GPU |
|------|----------|---------|------|-----|
| **MMAudio** (Sony AI/UIUC) | `tools/MMAudio/` | Open | **Video→audio Foley.** Watch a silent clip, generate synced SFX. CVPR 2025. 157M params, 8s audio in ~1.2s. The open SOTA for Foley. | T4 (Kaggle) |
| **TangoFlux** | Documented | Open (code+models) | **Text→SFX.** 515M params, ICLR 2026. "Heavy oak door slams in a stone corridor" → 30s 44.1kHz audio. Best open speed/fidelity. Pull on Kaggle. | T4 (Kaggle) |

Already had: AudioCraft (Meta, MIT — MusicGen + AudioGen), `tools/sfx/` categorized library (ambient/comedy/energy/impact/trippy/ui/whoosh).

**Workflow:** MMAudio watches the finished animation → generates synced foley → mix in `finish.py`. TangoFlux for one-shot SFX from text descriptions.

## 3. 2D Rigging (was a total gap)

| Tool | Location | License | What |
|------|----------|---------|------|
| **ChibiRigKit** | `tools/ChibiRigKit/` | Open | **PNG → animated 2D rig.** Semi-auto rigging from a single illustration: face parts, blinking, gaze, hair physics, camera face-tracking, mic lip-sync, browser player, OBS output. v1.0.0-beta.7. |
| **comfyui-autosplit-orchestrator** | `tools/comfyui-autosplit-orchestrator/` | Open | **Flat character → 26 riggable part PNGs** in ~33s via ComfyUI + SAM3. Exports to Spine JSON. Verified in Spine Pro. Pairs with our ComfyUI install. |
| **DragonBones** | Documented | Open | Free open-source Spine alternative. Skeletal 2D animation, mesh deformation. |

**For Cape Jones:** The owner's cutout workflow (model-sheet pieces layered like South Park) maps directly to ChibiRigKit's approach. The autosplit tool can take a finished character illustration and split it into animatable parts automatically — no more hand-cutting in rembg.

## 4. Compositing — 2D-specific

Natron research: Natron 2.5.0 is installed. The OpenFX plugin ecosystem covers the standard nodes. But for the headless pipeline, scriptable ffmpeg effects are more useful than GUI nodes.

**New pipeline script:** `post-pipeline/comp_glow.py` (CPU-only, ffmpeg)
- `--glow` — neon/bloom glow (energy blasts, LED strips, eyes)
- `--light-wrap` — background light spill on character edges
- `--atmosphere` — depth haze for backgrounds
- `--vignette` — focus vignette
- Presets: `energy-blast`, `neon-sign`, `dream`, `night-exterior`, `subtle`
- Palette-safe: uses screen/add blending so the white suit stays blown out
- Usage: `python3 comp_glow.py in.mp4 out.mp4 --preset energy-blast`

Also: `soda` (FrankFirsching) — Blender→Natron project generator for light-group compositing. Documented for the 3D segments.

## 5. Niche but Useful

**New pipeline script:** `post-pipeline/thumbnail_gen.py`
- Samples N frames across a finished episode, scores by color variance + edge density
- Picks the punchiest frame, crops to 16:9, sharpens, optional title burn-in
- Usage: `python3 thumbnail_gen.py episode.mp4 thumb.jpg --title "NUDE JONES"`
- `--list-frames` to preview scores without rendering

Already had: `ai-video-captions/` (Whisper animated captions), `animatic_builder.py`, `social_export.sh`, `explainroo/` (script→narrated video).

## 6. Update Check

| Repo | Status |
|------|--------|
| ToonCrafter | Code current (Kaggle notebook is the active path) |
| ToonComposer | Code current |
| Viggle-Animate | Code current (Kaggle notebook deployed to 6 repos) |
| Chatterbox | Code current |
| TheAnimeScripter | Updated 4 days ago per last pull |

## Pipeline Position

```
Dialogue script (JSON)
  → dialogue_pipeline.py → per-line WAVs + timing.json
  → tools/lipsync/ (Rhubarb/OpenFaceFX) → visemes
  → Tahoma2D/OpenToonz mouth shapes

Silent animation
  → MMAudio (Kaggle) → synced Foley track
  → finish.py → final mix

Character illustration (PNG)
  → comfyui-autosplit-orchestrator → 26 part PNGs → Spine/ChibiRigKit rig
  → OR ChibiRigKit directly → browser puppet with face-track + mic lip-sync

Finished episode
  → comp_glow.py → glow/light-wrap/atmosphere
  → thumbnail_gen.py → episode thumbnail
  → social_export.sh → platform delivery
```

## Disk

77%. All pulls are code-only (~130MB total). Model weights download on Kaggle, not locally.

# POST-INTERPOLATION.md — What Studios Do After Inbetweening

**The professional finishing process, adapted for the Cape Jones pipeline.**

After frames are interpolated (ToonCrafter/RIFE), real animation studios don't ship the raw output. There's a whole finishing pipeline. Here's what they do and what we've wired up.

---

## The Studio Pipeline (Post-Interpolation)

### 1. Cleanup / Tie-Down
**What studios do:** Assistant animators take the rough inbetweens and redraw them as clean, on-model line art. Every line is checked for consistency — no wobbling, no broken contours, no drifting proportions. This is the most labor-intensive step.

**What we do:** Our pipeline already handles the biggest cleanup problems automatically:
- `cleanup_lines.py` — OpenCV bilateral filtering, removes paper grain and scan noise while preserving ink lines
- `deghost.py` — snaps semi-transparent RIFE ghost pixels to solid (the #1 AI interpolation artifact on flat cartoon colors)
- De-ghosting is now automatic post-RIFE in `flipaclip_post.sh`

**AI-assisted cleanup (pulled, ready):**
- `~/workspace/tools/sketch-simplification/` — Simo-Serra SIGGRAPH 2016/2018 models for rough sketch → clean line art. Cloned, models downloadable via `download_models.sh`. Note: needs old PyTorch (0.4.1) — best run on Kaggle, documented for future wiring.

### 2. Ink and Paint (Color)
**What studios do:** Every drawing gets inked (final line art) and painted (flat colors, then shading). Traditionally the longest stage — every frame, by hand.

**What we do:** Cape Jones drawings come pre-colored from FlipaClip. The interpolation preserves colors. No re-painting needed. If a future scene needs AI colorization:
- `~/workspace/tools/basicpbc/` — AI paint-bucket colorization (CVPR 2024), already pulled

### 3. Color Grading (The "Look")
**What studios do:** A colorist applies a consistent grade across all shots — this is what makes a show look like *itself*. Every episode of Aqua Teen, every Adult Swim show has a signature grade.

**What we do — the Cape Jones signature grade:**
- `~/workspace/tools/post-pipeline/finish.py` — applies the grade + QC + audio + final encode
- Three grades, tuned for the locked palette:
  - `cape-jones` (default) — punchy cartoon: violet cowl saturated, whites protected, blacks deepened
  - `cape-jones-night` — darker variant for night/ghost-cave scenes
  - `cape-jones-trippy` — hyper-saturated for Wizard Gang-style trippy graffiti scenes
- **Palette protection:** the grade is designed around the locked colors — suit #FFFFFF stays blown out (never tinted), cowl #3E1473 gets punched, cape #000000 deepened not crushed
- Existing ffmpeg presets in `~/workspace/tools/color/presets.sh` (teal-orange, noir, vibrant-cartoon, etc.) for other moods

**AI LUT generation (pulled, ready):**
- `~/workspace/tools/color-grade-ai/` — generates .cube LUTs from reference frames. Useful when we want to match a specific look from a reference image.

### 4. Compositing ("Shooting")
**What studios do:** All layers are assembled — characters, backgrounds, effects, camera moves. Shadows, glows, atmosphere, depth. This is where flat drawings become a *scene*.

**What we do:**
- `~/workspace/tools/natron/` — Natron 2.5.0, open-source After Effects/Nuke alternative. Node-based compositing, rotoscoping, tracking.
- `~/workspace/tools/video-matte.py` — AI matting (rembg/RVM) for character separation
- For the trippy graffiti background: layer the matted character over animated backgrounds in Natron

### 5. Visual Effects
**What studios do:** Particles, energy effects, glows, screen shake, speed lines — anything that sells the action.

**What we do:**
- Gauntlet energy blasts: core #FFFFFF, corona yellow/cyan on Color Dodge (per locked palette spec)
- Natron for glow/composite effects
- `~/workspace/cape-jones-build/chowder-fx/` — animated texture fills (Chowder method)

### 6. Sound Design
**What studios do:** Dialogue, SFX, music — mixed and mastered. Sound is 50% of the experience.

**What we do:**
- `~/workspace/tools/audacity/` — Audacity 4.0.1 for editing and mixing
- `finish.py --audio` — mixes music/SFX under the video in the finishing stage
- Music: Ghost Surf Rock (outro/action), Nosferatu score (intro/theme)
- SFX sources: Zapsplat, Freesound, BBC Sound Effects (documented in FULL-PRODUCTION-STACK.md)

### 7. Final QC and Delivery
**What studios do:** Every shot is reviewed frame-by-frame. Continuity, sync, artifacts — nothing ships with errors.

**What we do:**
- `finish.py` runs automated QC: valid video stream, non-zero duration, sane resolution
- Delivery via Muse storage links (per video delivery law)

---

## The Full Pipeline (Updated)

```
FlipaClip drawings
  → flipaclip_post.sh (denoise → line cleanup → ToonCrafter/RIFE → deghost → upscale → sharpen)
  → finish.py (QC → Cape Jones grade → audio mix → final encode)
  → [optional] Natron (compositing, backgrounds, effects)
  → delivery
```

**One command for the finishing stage:**
```bash
python3 ~/workspace/tools/post-pipeline/finish.py input.mp4 output.mp4 \
  --grade cape-jones \
  --audio music.mp3 \
  --audio-volume 0.7
```

---

## What's New (2026-10-16)

| Tool | What | Status |
|------|------|--------|
| `finish.py` | Post-interp finishing: QC + grade + audio + encode | ✅ Built, tested on real footage |
| Cape Jones signature grade | 3 variants tuned for locked palette | ✅ Tested, visually verified |
| `sketch-simplification/` | AI rough→clean line art (SIGGRAPH) | ✅ Cloned, needs old PyTorch |
| `color-grade-ai/` | AI .cube LUT generator | ✅ Cloned |
| `basicpbc/` | AI paint-bucket colorization (CVPR 2024) | ✅ Already pulled |

## References
- Professional pipeline overview: businessofanimation.com 11-step and 13-step guides
- Cleanup process: Wikipedia "Cleanup (animation)" — Disney's traditional workflow
- TheAnimeScripter: already in pipeline (`~/workspace/tools/tas/`)
- Netflix VOID 2026: AI object removal (noted, not pulled — overkill for our needs)

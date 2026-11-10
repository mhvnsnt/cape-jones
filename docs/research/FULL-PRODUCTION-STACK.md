# CAPE JONES — Full Production Stack
**Studio-grade 2D animation pipeline. Written 2026-10-15. Think like a studio TD.**

This is the complete pipeline for making a REAL show — every stage, every tool, open-source vs commercial, what we have, what's missing.

---

## 1. PRE-PRODUCTION

### Storyboarding
| Tool | Type | Status |
|------|------|--------|
| **Storyboarder** (Wonder Unit) | Free, open-source | ❌ NOT INSTALLED — pull it |
| **Toon Boom Storyboard Pro** | Commercial ($67.50/mo) | ❌ Commercial — know it exists |
| **StudioBinder** (free tier) | Freemium | ❌ Web-based, no install needed |
| **Krita** (storyboard templates) | Free, open-source | ❌ NOT INSTALLED — pull it |
| **Boords** | Commercial ($19.99/mo) | ❌ Commercial |

**Recommendation:** Storyboarder (free, open-source, Photoshop integration). Pull it immediately.

### Animatics (timed storyboards)
- Build in any video editor: **DaVinci Resolve** (free), **Kdenlive** (free/open-source), or **Blender VSE**
- ❌ None installed yet — **DaVinci Resolve** is the pro pick (free tier is extremely capable)

### Character Design / Model Sheets
| Tool | Type | Status |
|------|------|--------|
| **Inkscape 1.4.4** (vector) | Free, open-source | ✅ INSTALLED (`~/workspace/tools/inkscape-1.4.4/`) |
| **Krita** (raster drawing) | Free, open-source | ❌ NOT INSTALLED — pull it |
| **Clip Studio Paint** | Commercial | ❌ Commercial — industry standard for drawing |

---

## 2. ANIMATION

### 2A. Frame-by-Frame (Hand-Drawn)
| Tool | Type | Status |
|------|------|--------|
| **FlipaClip** (phone) | Freemium | ✅ USER'S DRAWING TOOL |
| **Tahoma2D 1.5.4** | Free, open-source | ✅ INSTALLED (`~/workspace/tools/Tahoma2D/`) |
| **OpenToonz** | Free, open-source | ✅ Via Tahoma2D (fork) |
| **Krita** | Free, open-source | ❌ NOT INSTALLED — has excellent frame-by-frame |
| **Pencil2D** | Free, open-source | ❌ Simple, lightweight alternative |
| **Clip Studio Paint EX** | Commercial | ❌ Best drawing feel for 2D animation |
| **TVPaint** | Commercial | ❌ Studio standard for hand-drawn (used by Cartoon Saloon) |
| **Toon Boom Harmony** | Commercial ($28.50+/mo) | ❌ Industry standard (Rick and Morty, SpongeBob) |

### 2B. Cutout / Rig Animation (South Park Style)
| Tool | Type | Status |
|------|------|--------|
| **Tahoma2D** (bone rigs, mesh deform) | Free, open-source | ✅ INSTALLED — primary rig tool |
| **Moho** (formerly Anime Studio) | Commercial ($59.99 one-time) | ❌ Best bone rigging UX, affordable |
| **Adobe Animate** | Commercial ($22.99/mo) | ❌ Vector rigging |
| **Synfig Studio** | Free, open-source | ❌ Auto-tweening, vector-based |
| **Blender Grease Pencil** | Free, open-source | ✅ Blender installed (`~/workspace/tools/blender/`) |

### 2C. Auto-Inbetweening (THE HARD PROBLEM)
| Tool/Method | Type | Status |
|------|------|--------|
| **RIFE v4** (AI interpolation) | Free, open-source | ✅ INSTALLED — best general option, but ghosts on flat cartoon colors |
| **ffmpeg minterpolate** | Free, open-source | ✅ System — smoother motion than RIFE but blurrier, warps on outlines |
| **De-ghosting post-process** | Custom | ✅ PROTOTYPE (`~/workspace/tools/post-pipeline/deghost.py`) |
| **FLAVR** (flow-free AI) | Free, open-source | ⚠️ Code at `~/workspace/tools/flavr/` — NOT SET UP |
| **DAIN** (depth-aware) | Free, open-source | ❌ Older than RIFE, generally worse |
| **EMA-VFI** | Free, open-source | ❌ Benchmarks worse than RIFE |
| **GMFSS Fortuna** (anime-specific) | Free, open-source | ⚠️ At `~/workspace/tools/gmfss/` — works but 15+ min/frame on CPU, impractical |
| **AnimeInterp** (designed for cartoons) | Free, open-source | ⚠️ Code at `~/workspace/tools/animeinterp/` — **weights unavailable** (dead link) |
| **Cacani** (pro auto-inbetween) | Commercial | ❌ THE industry tool for this. No free version. |
| **Toon Boom Harmony AI inbetween** | Commercial | ❌ Built into Harmony |

**Root cause (verified):** RIFE was trained on real video. Flat cartoon colors (white suit, purple cape) have no texture for optical flow to track → defaults to blending → ghosting. The AnimeInterp paper (CVPR21) describes this exact problem.

**Current best stack:** RIFE + de-ghosting. Still better than ffmpeg alone.

### 2D. Lip Sync
| Tool | Type | Status |
|------|------|--------|
| **Rhubarb Lip Sync** | Free, open-source | ✅ At `~/workspace/tools/rhubarb/` |
| **Papagayo-NG** | Free, open-source | ✅ At `~/workspace/tools/lipsync/` (verify) |
| **Adobe Character Animator** | Commercial | ❌ Auto lip sync |

---

## 3. POST-PRODUCTION

### 3A. FlipaClip Cleanup Pipeline (CUSTOM BUILT)
**Script:** `~/workspace/tools/post-pipeline/flipaclip_post.sh`

| Stage | Tool | Status |
|-------|------|--------|
| 1. Denoise + deflicker | ffmpeg `hqdn3d` + `deflicker` | ✅ Working |
| 2. Line cleanup | Custom OpenCV (`cleanup_lines.py`) | ✅ Working |
| 3. Frame interpolation 12→24fps | RIFE (default) / ffmpeg (`--fast`) | ✅ Working |
| 4. Upscale 2x | Lanczos / ESPCN neural | ✅ Working |
| 5. Sharpen + color punch | ffmpeg `unsharp` + `eq` | ✅ Working |

**Doc:** `~/workspace/cape-jones-build/FLIPACLIP-POST-PIPELINE.md`

### 3B. Video Matting (Background Removal)
| Tool | Type | Status |
|------|------|--------|
| **Robust Video Matting (RVM)** | Free, open-source | ✅ At `~/workspace/tools/rvm/` |
| **rembg** (per-frame) | Free, open-source | ✅ At `~/workspace/tools/rembg-venv/` |
| **video-matte.py** (wrapper) | Custom | ✅ At `~/workspace/tools/video-matte.py` |

**LAW: NEVER use chroma key on main animation.** Matting only. Chroma key destroys white/colored characters.

### 3C. Compositing
| Tool | Type | Status |
|------|------|--------|
| **Natron 2.5.0** | Free, open-source | ⚠️ Downloaded (`~/workspace/tools/post-pipeline/natron.tar.xz`) — extract it |
| **Blender Compositor** | Free, open-source | ✅ Blender installed |
| **Friction** (motion graphics) | Free, open-source | ❌ Vector-first, worth pulling |
| **DaVinci Resolve Fusion** | Free tier | ❌ NOT INSTALLED — pro-grade, free |
| **Adobe After Effects** | Commercial | ❌ Industry standard |
| **Nuke** | Commercial | ❌ Film VFX standard |

### 3D. Color Grading
- **Natron:** Grade, HSVTool, Equalize nodes + LUT support
- **DaVinci Resolve:** Best free color grading on the planet (seriously)
- **Blender:** Color management via OpenColorIO

### 3E. Effects / VFX
| Need | Tool | Status |
|------|------|--------|
| Energy blasts, glows | Natron / Blender | ⚠️ Natron needs extracting |
| Chowder-style textures | `pattern_fill_v2.py` + ffmpeg track matte | ✅ Built (`~/workspace/cape-jones-build/chowder-fx/`) |
| Stroke reveal (write-on) | Natron / custom mask animation | ❌ NOT BUILT YET — user requested |
| Particle effects | Blender / Natron | ✅ Blender ready |

---

## 4. AUDIO

### Sound Design
| Tool | Type | Status |
|------|------|--------|
| **Audacity** | Free, open-source | ❌ NOT INSTALLED — pull it (basic editing) |
| **DaVinci Resolve Fairlight** | Free tier | ❌ Pro audio post, free |
| **Ardour** | Free, open-source | ❌ Full DAW |
| **Reaper** | Commercial ($60, generous trial) | ❌ Best value DAW |

### SFX Libraries (Free)
- **Zapsplat.com** — 100,000+ free SFX, updated daily
- **Freesound.org** — community SFX (Creative Commons)
- **BBC Sound Effects** — 33,000 free (RemArc license)
- **Soniss GDC Packs** — free annual game audio packs (great for cartoons)

### Cartoon-Specific SFX
- Classic cartoon sounds (boinks, zips, pops) are mostly in paid libraries (Sound Ideas)
- **DIY approach:** Foley recording + pitch-shifting + layering (the classic method)
- **AI SFX generation:** Emerging (ReelMind, etc.) — worth watching

### Voice
- **Local TTS:** espeak-ng (have it), Piper TTS (better quality, free)
- **ElevenLabs:** Commercial, best AI voices (have connector)

---

## 5. AI TOOLS FOR ANIMATION (2024-2026)

### Colorization (Sketch → Color)
| Tool | Type | Status |
|------|------|--------|
| **SketchColour** (DiT-based) | Research/open-source | ❌ Pull from GitHub |
| **AnimeColor** (diffusion transformer) | Research/open-source | ❌ Pull from GitHub |
| **DACoN** (reference-based) | Research/open-source | ❌ Pull from GitHub |

These auto-color line art. HUGE time saver for hand-drawn animation.

### Inbetweening
- **AnimeInterp:** Designed for cartoons, weights unavailable
- **MotionMaker** (Autodesk Maya, 2025): AI inbetweening for 3D, not 2D
- **Toon Boom Harmony AI:** Auto in-between generation (commercial)

### Backgrounds
| Tool | Type | Status |
|------|------|--------|
| **AI Horde** (free, crowdsourced) | Free | ✅ Have connector |
| **Stable Diffusion + AnimateDiff** | Free, open-source | ⚠️ Have some tooling |
| **Existing gen tools** | Custom | ✅ `~/workspace/trippedd-studio/tools/image-gen/` |

---

## 6. GAP ANALYSIS — What We're Missing

### PULL IMMEDIATELY (free, high impact)
1. **Krita** — best free drawing + frame-by-frame animation
2. **Storyboarder** (Wonder Unit) — free storyboarding
3. **DaVinci Resolve** — free pro editing, color grading, audio, Fusion VFX (replaces 4 tools)
4. **Audacity** — basic audio editing
5. **SketchColour / AnimeColor** — AI auto-coloring for line art
6. **Friction** — motion graphics

### NICE TO HAVE
7. **Synfig Studio** — auto-tweening vector animation
8. **Pencil2D** — lightweight frame-by-frame
9. **Blender** — already have it, learn Grease Pencil properly

### COMMERCIAL (know they exist, can't afford now)
- Toon Boom Harmony ($28.50+/mo) — industry standard
- Cacani (pro auto-inbetweening)
- TVPaint (hand-drawn standard)
- Adobe After Effects ($22.99/mo)
- Clip Studio Paint EX (best drawing feel)

### BUILD CUSTOM
- **Stroke reveal / write-on effect** — user specifically requested (neon scary face over real face)
- **Scene-aware interpolation** — detect cuts, interpolate within scenes only
- **De-ghosting refinement** — improve the RIFE post-process

---

## 7. RECOMMENDED PIPELINE (for Cape Jones)

```
PRE-PRODUCTION
  Storyboarder → script → boards → animatic (DaVinci Resolve)

ANIMATION
  FlipaClip (hand-drawn keys)
    → flipaclip_post.sh (cleanup → RIFE → upscale)
  Tahoma2D (rig/cutout animation)
  Inkscape (vector pieces from model sheets)

POST
  video-matte.py (RVM background removal)
  Natron (compositing, effects, stroke reveal)
  DaVinci Resolve (color grade, audio mix)

AUDIO
  Audacity (edit) → Zapsplat/Freesound (SFX) → DaVinci Fairlight (mix)
  Nosferatu 1922 score (intro theme — public domain)
```

**One-command rule:** Every stage should be runnable as a single script. No manual homework.

---

*This is a living document. Update as tools are pulled in or the pipeline changes.*

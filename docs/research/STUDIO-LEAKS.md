# STUDIO LEAKS & STUDIO-RELEASED OPEN SOURCE

**Pulled:** 2026-10-16
**Location:** `~/workspace/tools/studio-leaks/`
**Why:** The owner wants every production-grade tool that real animation studios use or have released.

---

## WHAT WE PULLED (on disk)

### 1. xSTUDIO — DNEG's Review Tool (AcademySoftwareFoundation/xstudio)
- **What:** DNEG's professional media playback and review application. Open-sourced 2023 via ASWF.
- **Why it matters:** This is what DNEG actually uses for dailies/review. Full Python API, C++ plugin framework, pipeline-agnostic.
- **Status:** ✅ Pulled (223MB, 2,681 files)
- **Use for Cape Jones:** Dailies review — play back animation shots, compare versions, annotate.
- **License:** Apache 2.0

### 2. AL_USDMaya — Animal Logic's USD Plugin (AnimalLogic/AL_USDMaya)
- **What:** Animal Logic's production USD integration for Maya. Used on Peter Rabbit and all their features.
- **Why it matters:** This is how a real studio bridges USD into their DCC. ProxyShape, live USD stage connection, multiproxyShape support.
- **Status:** ✅ Pulled (20MB)
- **Use for Cape Jones:** Reference for USD pipeline design. Our Blender USD workflow can mirror their architecture.
- **License:** Apache 2.0

### 3. Gazu — Kitsu Python SDK (cgwire/gazu)
- **What:** Python client for Kitsu (the open-source production tracker). Full API access to shots, assets, tasks, reviews.
- **Why it matters:** This is how you script a production pipeline — create shots, assign tasks, publish versions, all from Python.
- **Status:** ✅ Pulled (1.9MB)
- **Use for Cape Jones:** Automate the production pipeline. `gazu` can create shots for EP01, track animation tasks, publish renders.
- **License:** MIT
- **Install:** `pip install gazu`

### 4. Blender Studio Pipeline (bpype/blender-studio-pipeline)
- **What:** The COMPLETE Blender Studio production pipeline — docs, add-ons, scripts, tools. This is how Blender Studio makes their films.
- **Includes:**
  - `bbatch` — batch process .blend files from command line
  - Project Tools — shot/asset management scripts
  - Pipeline release packaging
  - Full TD guide and artist guide
- **Status:** ✅ Pulled (12MB)
- **Use for Cape Jones:** Model our pipeline on this. The bbatch tool is directly useful for batch-rendering shots.
- **License:** GPL

---

## DOCUMENTED (too heavy to pull, but tracked)

### Review & Playback
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **OpenRV** | Autodesk → ASWF (2022) | Documented | THE industry review tool. Sci-Tech award winner. Was commercial (ShotGrid), now open source. Needs VFX Platform build — use prebuilt binaries from GitHub releases. |
| **DJV** | grizzlypeak3d (maintained fork) | Documented | Lightweight EXR/sequence player. `pip install DJV_viewer` — runs immediately. A/B comparison, OTIO timeline, OCIO color. **This is the quick win for dailies.** |

### Render Management
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **OpenCue** | Sony Imageworks + Google | Documented | Sony's internal render manager (Cue 3), scaled to 150,000 cores. Needs Postgres + cluster setup. For when we need real render farm management. |
| **Flamenco** | Blender Foundation | Already have (documented) | Blender's own render manager. Lighter than OpenCue. |

### Production Tracking
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **Kitsu** (full stack) | CGWire | Documented | Open-source ShotGrid alternative. Trusted by 50+ countries. Needs Docker + Postgres. We pulled Gazu (the Python SDK) — that's the scripting interface. |
| **Ayon** | Ynput | Already have | Open ShotGrid alternative. Already documented in 2026-STUDIO-DEEP-DIVE.md. |

### Renderers
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **MoonRay** | DreamWorks Animation | Documented | DreamWorks' production path tracer. Used on every DW feature since 2019 (HTTYD3, Bad Guys, Wild Robot). Apache 2.0. Too heavy to build locally — needs full VFX platform. **For future 3D work.** |
| **OpenVDB** | DreamWorks → ASWF | Documented | Sparse volume data. Industry standard for smoke/fire/clouds. Already in Blender. |

### Scene Description & Rigging
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **OpenUSD** | Pixar → AOUSD | Documented | THE scene description standard. Already in Blender 4.x. We have Animal Logic's AL_USDMaya as reference implementation. |
| **OpenSubdiv** | Pixar | Documented | Subdivision surfaces library. Already in Blender. |
| **OpenExec** | Pixar | Documented | Execution/evaluation framework for rigging. Newer Pixar open source. |

### Color & Image
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **OpenColorIO** | Sony Imageworks → ASWF | Documented | Industry color management standard. Already in Blender, Natron, DJV. |
| **OpenEXR** | ILM → ASWF | Documented | HDR image format. Industry standard. Already everywhere. |
| **OpenImageIO** | Sony Imageworks → ASWF | Documented | Image I/O library. Already in Blender. |
| **MaterialX** | ILM → ASWF | Documented | PBR material standard. |
| **ACES** | Academy → ASWF (2025) | Documented | Academy Color Encoding System. The color science behind every major film. |

### Other Studio Open Source
| Tool | Studio | Status | Why |
|------|--------|--------|-----|
| **Open Shading Language** | Sony Imageworks → ASWF | Documented | Programmable shading language for renderers. |
| **Field3D** | Sony Imageworks | Documented | Voxel data storage (archived, superseded by OpenVDB). |
| **pystring** | Sony Imageworks | Documented | Python-like strings in C++. |
| **spReticle** | Sony Imageworks | Documented | Camera reticle plugin for Maya. |
| **ReviewPluginApi** | Sony Imageworks → ASWF | Documented | Plugin API for building review/playback tools. Part of Open Review Initiative. |

---

## OPEN REVIEW INITIATIVE (ASWF)

The Academy Software Foundation's umbrella project for unifying open-source review/playback. Members:
- **OpenRV** (Autodesk) — the reference application
- **xSTUDIO** (DNEG) — ✅ pulled
- **Itview** (Sony Imageworks) — their internal review platform (ReviewPluginApi is the open piece)
- **DJV** (community) — lightweight alternative

**For Cape Jones:** This is our dailies/review stack. DJV for quick playback, xSTUDIO for full review sessions.

---

## QUICK WINS (use immediately)

1. **DJV** — ✅ Installed (`/usr/local/bin/djv`, v3.7.5) — instant professional sequence player for reviewing animation
2. **Gazu** — ✅ Installed (`pip`, v1.3.1) — Kitsu production tracking from Python
3. **Blender Studio bbatch** — batch process .blend files from command line
4. **AL_USDMaya** — study their USD architecture for our pipeline design

---

## INTEGRATION WITH CAPE JONES PIPELINE

```
FlipaClip → flipaclip_post.sh → ToonCrafter (Kaggle) → finish.py
    → DJV (review) → xSTUDIO (dailies) → Kitsu/Gazu (track) → delivery
```

The studio tools slot into the **review and tracking** stages that our pipeline was missing.

---

## SOURCES

- ASWF: https://www.aswf.io/
- Open Review Initiative: https://www.aswf.io/projects/open-review-initiative/
- Awesome CG/VFX Pipeline: https://github.com/cgwire/awesome-cg-vfx-pipeline
- Sony Imageworks OSS: https://github.com/imageworks
- DreamWorks: https://github.com/dreamworksanimation
- Pixar: https://github.com/PixarAnimationStudios
- Animal Logic: https://github.com/AnimalLogic
- Blender Studio: https://studio.blender.org/
- CGWire/Kitsu: https://kitsu.cloud

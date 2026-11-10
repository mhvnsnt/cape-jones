# 2026 Studio Deep Dive — Production-Grade Animation Tools

Research completed 2026-10-16. Every tool below is free/open-source, pulled to `~/workspace/tools/`, and documented for the Cape Jones pipeline.

---

## 1. KRITA AI DIFFUSION (Owner Priority)

**Repo:** `~/workspace/tools/krita-ai-diffusion/` (Acly/krita-ai-diffusion)
**License:** GPL-3.0 | **Latest:** v1.53.0 (Aug 2026)
**Backend:** ComfyUI (local GPU or cloud via "Interstice")

### What it does
Generative AI directly inside Krita — inpainting, outpainting, live painting, upscaling to 4K/8K+. The owner already has Krita 6.0.4 extracted at `~/workspace/tools/krita-6.0.4/`.

### Key features for animation production
- **Inpainting/outpainting on selections** — fix backgrounds, extend scenes, remove artifacts
- **Live Painting** — AI interprets canvas in real-time as you draw
- **ControlNet layers** — scribble, line art, Canny edge, pose, depth, normals, segmentation (v1.53.0 added segmentation control)
- **IP-Adapter** — style/composition transfer from reference images, face swap
- **Regions** — assign separate prompts per layer (character vs background)
- **Model support** — Stable Diffusion 1.5/XL/Illustrious, partial Flux 2, Z-Image, SD3

### Animation-specific use cases
1. **Background generation** — paint rough background, AI refines to production quality
2. **Inbetweening assistance** — generate intermediate poses guided by line art control layers
3. **Style transfer** — apply consistent art style across frames via IP-Adapter
4. **Cleanup** — inpaint over animation artifacts, wire removal, gap filling
5. **Upscaling** — 4K/8K output without VRAM limits (tiled)

### Hardware
- NVIDIA GPU with 6GB+ VRAM recommended (CUDA)
- CPU supported but very slow
- **Kaggle T4 (16GB) is ideal** — run Krita + plugin via cloud backend

### Install
```bash
cd ~/workspace/tools/krita-ai-diffusion
# See install.py and docs/ for full setup
# Requires ComfyUI backend (already at ~/workspace/tools/comfyui/)
```

---

## 2. CASCADEUR DEEP DIVE

**Status:** Already at `~/workspace/tools/cascadeur/` (from earlier pull)
**License:** Free until $100K annual revenue, then paid tiers
**Website:** cascadeur.com

### What it is
AI-assisted 3D keyframe animation software. Block 2-3 key poses → AutoPhysics generates physically-plausible inbetweens with weight, momentum, and follow-through.

### Features relevant to Cape Jones

**AutoPosing** — Neural network generates natural full-body poses from a few control points. Set the hips and hands, AI positions everything else.

**AutoPhysics** — Physics simulation with adjustable sliders. Movements adhere to physical laws. Key for:
- **Cape dynamics** — simulate how the cape should billow, drape, follow-through on turns
- **Flight physics** — realistic banking, acceleration curves for flying scenes
- **Impact** — punch/kick follow-through with proper weight transfer

**Secondary Motion Controls** — Adjustable sliders for shake, bounce, jiggle on body parts. Perfect for:
- Cape flutter (secondary to body motion)
- Belly jiggle on Baked Jones
- Hair/cloth follow-through

**Animation Unbaking** — Converts baked simulations into editable keyframes. Simulate the cape in Cascadeur → unbaked keyframes → use as reference for 2D drawings.

**Video Mocap Integration** — Refine mocap data. Owner films himself → extract motion → clean up in Cascadeur → use as 2D reference.

**Export** — FBX, DAE, USD. Imports directly into Blender.

### 2D Animation Reference Workflow
```
1. Block key poses in Cascadeur (3-5 poses for a shot)
2. Run AutoPhysics for inbetweens
3. Add secondary motion (cape, cloth)
4. Export FBX → Import to Blender
5. Render turntable/reference views
6. Trace over renders in Krita for 2D frames
   OR use as timing/spacing reference for hand-drawn
```

### Why it matters for Cape Jones
The cape is the hardest thing to animate by hand — it's the most competent character on the show and it needs to move beautifully. Cascadeur's physics gives us real cape motion reference instead of guessing.

---

## 3. WHAT REAL STUDIOS USE IN 2026

### Titmouse (Metalocalypse, Big Mouth, Venture Bros)
- **Design/Animation:** Photoshop (frame-by-frame)
- **Compositing:** After Effects
- **Editing:** Premiere Pro
- **Takeaway:** Even top studios use "boring" tools well. Our Krita → Natron → finish.py pipeline mirrors this.

### Bento Box (Bob's Burgers)
- **Pipeline:** Toon Boom Storyboard Pro + Harmony (networked)
- **Takeaway:** Paperless digital pipeline. Our equivalent: Storyboarder → Tahoma2D/OpenToonz → Natron.

### DreamWorks (The Wild Robot)
- Painterly 2D aesthetics translated to 3D. Validates our approach of hand-drawn style with tech assist.

### SIGGRAPH 2025 Highlights
- AI in art/physical AI major theme
- DreamWorks "Wild Robot" painterly pipeline session
- Real-Time Live! — AI-powered motion tools demos
- Trend: studios adopting AI for inbetweening, lip-sync, coloring (not replacing artists)

### Open-Source Studio Tools (Academy Software Foundation)
| Tool | What | Status |
|------|------|--------|
| **OpenTimelineIO** | Editorial interchange format | ✅ Pulled to `~/workspace/tools/OpenTimelineIO/` |
| **OpenColorIO** | Color management | Available via ASWF |
| **OpenVDB** | Volumetric data | Available via ASWF |
| **OpenImageIO** | Image I/O | Available via ASWF |
| **USD** | Universal Scene Description | Via Pixar/ASWF |

---

## 4. 2026 AI ANIMATION PAPERS WITH WORKING CODE

**Index:** `~/workspace/tools/Awesome-Animation-Research/` (zhenglinpan/Awesome-Animation-Research)

### Pulled and Ready

| Model | Paper | What | Location |
|-------|-------|------|----------|
| **ToonComposer** | ICLR 2026 | Keyframe color + sketches → full animation. Based on Wan2.1. Gradio UI. | `~/workspace/tools/tooncomposer/` |
| **FlipSketch** | CVPR 2025 | Static drawing → text-guided sketch animation | `~/workspace/tools/flipsketch/` (cloning) |
| **AnimateAnything** | CVPR 2025 | Consistent controllable video generation | `~/workspace/tools/animateanything/` (cloning) |
| **ToonCrafter** | SIGGRAPH Asia 2024 | Generative cartoon interpolation | Already at `~/workspace/tools/tooncrafter/` |
| **AnimeInterp** | CVPR 2021 | Animation-specific interpolation (segment-guided matching) | Already at `~/workspace/tools/animeinterp/` |
| **Animating on Twos** | 2026 (Alvdansen) | Keyframe-animation adapters on pretrained video model | Cloning |

### Notable (documented, not pulled — check if needed)
- **FairyGen** (SIGGRAPH Asia 2025) — single child-drawn character → storied cartoon video
- **LayerAnimate** (ICCV 2025) — layer-level control for animation
- **PhysAnimator** (CVPR 2025) — physics-guided generative cartoon animation
- **AniSora** (IJCAI 2025) — animation video generation in the Sora era
- **Skeleton-Driven Inbetweening** (SIGGRAPH Asia 2024) — bitmap character inbetweening

### ToonComposer — The Big One
This is the most production-relevant find. Workflow:
1. Provide 1 keyframe color image (frame 0)
2. Add keyframe sketches at selected frames
3. Optional: black brush regions as motion masks
4. Set text prompt, output frames, resolution (480p/608p)
5. Generate → full cartoon animation

**This is "draw 2 frames, AI fills the shot."** Directly applicable to Cape Jones vibe segments and simple scenes.

---

## 5. PRODUCTION PIPELINE GLUE

### OpenTimelineIO (OTIO)
**Repo:** `~/workspace/tools/OpenTimelineIO/`
**What:** Open-source API for editorial timeline interchange. Created by Pixar, hosted by ASWF.
**Support:** Maya 2027, Blender VSE, DaVinci Resolve, Nuke, RV, Unreal Engine
**Use case:** Move episode timelines between Storyboarder → editing → compositing without lock-in.

### USD (Universal Scene Description)
**What:** Pixar's scene description format. Industry standard for 3D pipeline interchange.
**Use case:** 2D/3D hybrid scenes — Cape Jones 2D character in 3D environments, or vice versa.

### Pipeline Management
| Tool | What | License |
|------|------|---------|
| **Ynput Ayon 1.0** | Open-source VFX/animation pipeline (ShotGrid alternative) | Open source, production-ready |
| **Prism Pipeline** | VFX pipeline with USD, ComfyUI integration, AI agents | Free tier |
| **DJV 3** | Free VFX image viewer with OTIO + USD support | Open source |

### ComfyUI Integration
FMX 2026 showed Prism Pipeline integrating ComfyUI directly into studio workflows. Our `~/workspace/tools/comfyui/` can serve the same role — AI generation nodes wired into the production pipeline.

---

## 6. AUDIO PRODUCTION 2026

### AI Voice (Open-Source)

| Model | Params | License | Best For | Status |
|-------|--------|---------|----------|--------|
| **Kokoro** | 82M | Apache-2.0 | CPU TTS, 96x real-time, English | `pip install kokoro` |
| **Chatterbox** | 350M | MIT | Voice cloning (5 sec), emotion, 23 languages, [laugh]/[sigh] tags | Already at `~/workspace/tools/chatterbox/` |
| **Orpheus** | 150M-3B | Apache-2.0 | Expressive speech, scalable | HuggingFace |
| **Dia** | — | Apache-2.0 | Two-speaker dialogue with laughs/nonverbals | HuggingFace |
| **Qwen3-TTS** | 0.6B/1.7B | Apache-2.0 | 10 languages, 5M+ downloads | HuggingFace |
| **VoxCPM2** | 2B | Apache-2.0 | 30 languages, 48kHz, runs on CPU | HuggingFace |
| **Step Audio EditX** | — | Apache-2.0 | Emotion editing, best commercial-safe pick | Project page |

**Voicebox** (drgop/voicebox) — open-source AI voice studio, 7 TTS engines, voice cloning, 23 languages. Cloning.

### AI Music (Open-Source)

| Model | License | Best For | VRAM |
|-------|---------|----------|------|
| **MusicGen** (Meta) | MIT | Text-to-music + melody conditioning, 30-sec clips | 16GB recommended |
| **Stable Audio Open 3.0** | Open weights | High-fidelity ambient/textural, licensed training data | Varies |
| **ACE-Step** | Open | Full songs with lyrics/vocals (closest to Suno) | Varies |
| **AudioCraft** | MIT | Framework powering MusicGen + AudioGen + EnCodec | 12GB+ for Large |

**AudioCraft** (facebookresearch/audiocraft) — Meta's framework. Cloning.

### For Cape Jones
- **Dialogue:** Chatterbox (voice cloning for consistent character voices) + Dia (two-character conversations)
- **Narration:** Kokoro (fast, CPU-friendly)
- **Background music:** MusicGen (short loops for vibe segments) + Stable Audio (longer atmospheric)
- **SFX:** AudioGen (part of AudioCraft) + existing Zapsplat/Freesound/BBC libraries

---

## SUMMARY: What's New in ~/workspace/tools/

### Animation AI (New)
- `krita-ai-diffusion/` — AI inside Krita (inpaint, live paint, ControlNet)
- `tooncomposer/` — keyframe + sketch → animation (ICLR 2026)
- `flipsketch/` — drawing → text-guided animation (CVPR 2025)
- `animateanything/` — controllable video generation (CVPR 2025)
- `Awesome-Animation-Research/` — index of all 2026 papers

### Pipeline (New)
- `OpenTimelineIO/` — editorial interchange format
- `voicebox/` — AI voice studio (cloning)
- `audiocraft/` — Meta's audio generation framework (cloning)

### Already Had (Verified Working)
- `tooncrafter/` — cartoon interpolation
- `chatterbox/` — voice cloning
- `comfyui/` — AI video hub
- `cascadeur/` — physics-based 3D animation
- `krita-6.0.4/` — digital painting + animation

### GPU Strategy
All GPU-heavy tools target **Kaggle T4** (16GB). CPU-friendly tools (Kokoro, VoxCPM2) run locally.

---

## 7. 3D SEGMENT ASSETS (Cape Jones 3D Living Room)

**Requirement** (owner 2026-10-16): 15-second 3D segment — 3D Cape Jones sitting in chair in 3D living room, holding LED remote, room lights changing colors, ending on party light slowly fading. 3D segments are RARE (mainly for pipeline testing).

### Downloaded and Ready

**Kenney Furniture Kit v2.0** (CC0) — `~/workspace/tools/3d-assets/kenney-furniture/`
- 140 GLB models extracted and verified
- Key models: televisionModern.glb, loungeSofa.glb, tableCoffee.glb, lampRoundFloor.glb, cabinetTelevision.glb
- Source documented in `~/workspace/tools/3d-assets/SOURCE.md`

### Still Needed (Browser Download Required)
- **Quaternius Ultimate House Interior Pack** (123 models, CC0) — https://quaternius.com/packs/ultimatehomeinterior.html
- **Quaternius Ultimate Furniture Pack** (CC0) — https://quaternius.com/packs/ultimatefurniture.html
- Download buttons require browser interaction — parent should delegate a browser task

### 3D Pipeline for Segment
1. Import Kenney GLB models into Blender 4.0.2 (`~/workspace/tools/blender/`)
2. Build living room scene: sofa + coffee table + TV + floor lamp
3. Cape Jones character: use existing SVG/rig or build simple 3D proxy
4. LED lighting: animate Blender area/point light colors (matches LED presets from `led_controller.py`)
5. Render with Cycles (headless via `xvfb-run -a`)
6. Composite in Natron, grade with `finish.py`

### Blender Headless (verified working)
```bash
xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender -b --python-expr "..."
```

# TRACK A MEGA-PULL — Animation/interpolation + 2D rigging + Compositing/VFX
Date: 2026-10-16. All pulls stopped per disk-ceiling order (86%). Repos verified non-empty, licenses checked from LICENSE files.

## 1. ANIMATION / INTERPOLATION — `~/workspace/tools/trackA-interpolation/` (~494M)

| # | Name / URL | Path | What / Why | License | Status |
|---|---|---|---|---|---|
| 1 | **InterpAny-Clearer** — https://github.com/zzh-tech/interpany-clearer | `trackA-interpolation/interpany-clearer` | ECCV2024 Oral. Distance-indexed "anytime" VFI — sharper than RIFE on large motion, plus per-object re-timing. Entry: `inference_video.py` | MIT | Pulled, verified (291 files; deleted 18M webapp demo) |
| 2 | **JoSTC** — https://github.com/MarkMoHR/JoSTC | `trackA-interpolation/JoSTC` | SIGGRAPH 2024 (TOG). Joint stroke tracing + correspondence for 2D animation — rough line-art sequences → vector strokes with correspondence, SVG output for CACANi inbetweening. The vector-inbetweening backbone. Entry: `sketch_tracing_inference.py` | Apache-2.0 | Pulled, verified (145 files) |
| 3 | **5DVFI** — https://github.com/Feebami/5DVFI | `trackA-interpolation/5DVFI` | 3D denoising-diffusion VFI — diffusion inbetweening for stylized/hard-motion shots where flow methods smear | MIT | Pulled, verified (33 files) |
| 4 | **BMBC** — https://github.com/JunHeum/BMBC | `trackA-interpolation/BMBC` | Bilateral motion estimation + cost volume VFI — strong classical flow baseline. Entry: `run.py` | MIT | Pulled, verified (11 files) |
| 5 | **ABME** — https://github.com/JunHeum/ABME | `trackA-interpolation/ABME` | Asymmetric bilateral motion estimation — handles asymmetric/occluded motion well. Entry: `run.py` | MIT | Pulled, verified (29 files) |
| 6 | **IFRNet** — https://github.com/ltkong218/IFRNet | `trackA-interpolation/IFRNet` | Intermediate Feature Refine Network — efficient/light VFI, good for batch throughput. Entry: `demo.py` | MIT | Pulled, verified (39 files) |
| 7 | **ST-MFNet** — https://github.com/danielism97/ST-MFNet | `trackA-interpolation/ST-MFNet` | Spatio-temporal multi-flow VFI, small model, CPU-friendlier | MIT | Pulled, verified (33 files) |
| 8 | **FILM** — https://github.com/google-research/frame-interpolation | `trackA-interpolation/frame-interpolation` | Google's Frame Interpolation for Large Motion — complements RIFE on big displacements (deleted 21M demo gif) | Apache-2.0 | Pulled, verified (43 files) |
| 9 | **DistilDRBA** — https://github.com/routineLife1/DistilDRBA | `trackA-interpolation/DistilDRBA` | Distilled anime VFI tuned for real-time playback + scene-change detection. Weights deleted per CODE ONLY | MIT | Pulled, verified (10 files). Weights on Kaggle: re-obtain from full repo clone |
| 10 | **vs-gmfss_fortuna** — https://github.com/HolyWu/vs-gmfss_fortuna | `trackA-interpolation/vs-gmfss_fortuna` | VapourSynth wrapper for GMFSS Fortuna (anime VFI). Models deleted | MIT | Pulled, verified (24 files). Weights on Kaggle: pip package or full repo clone |
| 11 | **vs-mlrt** — https://github.com/AmusementClub/vs-mlrt | `trackA-interpolation/vs-mlrt` | VapourSynth ML runtime: ONNX RIFE, Real-CUGAN, waifu2x in VapourSynth scripts. Entry: `vsmlrt.py` | GPL-3.0 | Pulled, verified (59 files) |
| 12 | **RAFT** — https://github.com/princeton-vl/RAFT | `trackA-interpolation/RAFT` | SOTA optical flow — powers guided-tweening/warp pipelines. Entry: `demo.py` | BSD-3 | Pulled, verified (35 files) |
| 13 | **Sketch-Guided Inbetweening** — https://github.com/xiaoyu258/Inbetweening | `trackA-interpolation/Inbetweening` | Deep sketch-guided cartoon video inbetweening — keyframe + sketch → inbetweens | MIT | Pulled, verified (27 files) |
| 14 | **morpher91** — https://github.com/AndreFrelicot/morpher91 | `trackA-interpolation/morpher91` | WebGPU/WebCodecs 2D morphing studio: Delaunay mesh warp, thin-plate splines, Beier-Neely line fields, keyframable landmarks, MP4/WebM/PNG export | MIT | Pulled, verified (576 files) |
| 15 | **puppet-warp** — https://github.com/mikecokina/puppet-warp | `trackA-interpolation/puppet-warp` | Photoshop Puppet Warp as Python library (ARAP + graph warp) — scriptable mesh deformation/tweening | GPL-3.0 | Pulled, verified (69 files) |
| 16 | **ComfyUI-VideoColorGrading** — https://github.com/kijai/ComfyUI-VideoColorGrading | `trackA-interpolation/ComfyUI-VideoColorGrading` | ICCV 2025: 3D LUT from reference + video frames via diffusion — consistent show color grading in ComfyUI | No LICENSE file — reference until confirmed | Pulled (8 files), documented |
| 17 | **Awesome-AI4Animation** — https://github.com/yunlong10/Awesome-AI4Animation | `trackA-interpolation/Awesome-AI4Animation` | ICCVW 2025 curated index of every GenAI-for-cel-animation paper/code/dataset — future-pull shopping list | None (link list) | Pulled (14 files), documented |

Document-only (disk ceiling): **AdaCoF-pytorch** (https://github.com/HyeongminLEE/AdaCoF-pytorch, MIT) — adaptive collaboration of flows VFI; failed twice on network timeouts, retry in idle time.

## 2. 2D RIGGING — `~/workspace/tools/trackA-rigging/` (~466M)

| # | Name / URL | Path | What / Why | License | Status |
|---|---|---|---|---|---|
| 1 | **Stretchy Studio** — https://github.com/MangoLion/stretchystudio | `trackA-rigging/stretchystudio` | FOSS 2D animation tool: flat PSD → AI auto-rig (DWPose/heuristic), mesh deformation, shape keys, Spine 4.0 export. Closest open Live2D/Spine studio | MIT | Pulled, verified (210 files) |
| 2 | **tiny-2d-rig-tools** — https://github.com/sineadkearney/tiny-2d-rig-tools | `trackA-rigging/tiny-2d-rig-tools` | Blender addon: one-click 2D armature + IK/FK + drivers + Grease Pencil layer binding | No LICENSE — verify before redistributing | Pulled, verified (19 files) |
| 3 | **spine_anim_mcp** — https://github.com/K-ulucay/spine_anim_mcp | `trackA-rigging/spine_anim_mcp` | MCP server: layered PSD → Spine 4.2 rig + procedural idle/walk/run/jump/attack/hit generators with IK foot-lock. Agent-drivable | MIT | Pulled, verified (46 files) |
| 4 | **md_spine_tools** — https://github.com/SideswipeeZ/md_spine_tools | `trackA-rigging/md_spine_tools` | Blender addon: Spine 2D JSON/atlas → Blender meshes + armature + actions | MIT | Pulled, verified (8 files) |
| 5 | **FlowBoneEditor** — https://github.com/flowbone2d/FlowBoneEditor | documented | Free 2D bone editor (Spine 3.8 compatible). Repo is README-only — editor is web-hosted | Unclear | Documented |
| 6 | **Rigging-sketches** — https://github.com/mounika-v/Rigging-sketches-for-2D-character-animation | `trackA-rigging/Rigging-sketches-for-2D-character-animation` | Auto-rig from T-pose sketch: mesh-contraction skeletonization + pose-estimation. Entry: `rigit.py` GUI (deleted 203M build dirs + checkpoints) | No LICENSE — verify | Pulled, verified (1457 files) |
| 7 | **DUIK** — https://github.com/rxlaboratory/duik | `trackA-rigging/rxlaboratory-duik` | The open After Effects rigging suite + OCO open cut-out format + meta-rig library + auto-rig (trimmed 148M docs images) | GPL | Pulled, verified (3560 files) |
| 8 | **soda** — https://github.com/FrankFirsching/soda | `trackA-rigging/soda` | Blender addon generating a Natron comp from a Blender scene (per-light groups) — Blender→Natron comp bridge | GPL | Pulled, verified (23 files) |

## 3. COMPOSITING / VFX — `~/workspace/tools/trackA-vfx/` (~82M)

| # | Name / URL | Path | What / Why | License | Status |
|---|---|---|---|---|---|
| 1 | **frei0r** — https://github.com/dyne/frei0r | `trackA-vfx/frei0r` | 120+ scriptable video filter plugins — usable from FFmpeg (`-vf frei0r=filter_name=glow`) | GPL-2.0 | Pulled, verified (553 files) |
| 2 | **openfx-misc** — https://github.com/NatronGitHub/openfx-misc | `trackA-vfx/openfx-misc` | Natron's OFX plugin set incl. Shadertoy GLSL node, particles, glows, lens flares, keyers | GPL-2.0 | Pulled, verified (705 files) |
| 3 | **openfx-arena** — https://github.com/NatronGitHub/openfx-arena | `trackA-vfx/openfx-arena` | Second OFX plugin set (more transitions/effects for Natron) | GPL-2.0 | Pulled, verified (205 files) |
| 4 | **motion-canvas** — https://github.com/motion-canvas/motion-canvas | `trackA-vfx/motion-canvas` | MIT programmatic motion graphics (TypeScript/Canvas) — agent-writable titles/lower-thirds/transitions | MIT | Pulled, verified (1059 files) |
| 5 | **manim** — https://github.com/ManimCommunity/manim | `trackA-vfx/manim` | Programmatic math/title/data-driven animation — explainer segments | MIT | Pulled, verified (1398 files) |
| 6 | **Motion-Synthesizer** — https://github.com/ginonave/Motion-Synthesizer | `trackA-vfx/motion-canvas`… `trackA-vfx/Motion-Synthesizer` | Single-file web app: 10 animatable post-FX (glow, bloom, RGB split, CRT, glitch, radial blur…) + motion trails, MP4/WebM export | No LICENSE | Pulled (2 files), documented |
| 7 | **claude-motion-skills** — https://github.com/kevinbadi/claude-motion-skills | `trackA-vfx/claude-motion-skills` | MIT motion-design skill pack: principles, camera choreography, GSAP/SVG/Lottie/Remotion recipes | MIT | Pulled, verified (9 files) |

## 4. SKIPPED (license)
- **CDFI** — research use only → skipped
- **XVFI** — research and education only → skipped
- **VFIformer** — research use only → skipped
- **Remotion** — paid company license for teams >3 → skipped; motion-canvas (MIT) pulled instead

## 5. WIRED INTO `~/workspace/tools/post-pipeline/`
- **trackA-ffmpeg-fx-chains.sh** — 8 FFmpeg effect chains: `fx_glow`, `fx_speedlines`, `fx_impact`, `fx_xfade` (25 transitions), `fx_frei0r_glow`, `fx_filmlook`, `fx_keycomp`, `fx_shake`
- **trackA-wiring-guide.md** — tool-selection matrix + 5 pipeline wirings (JoSTC→CACANi→RIFE/InterpAny-Clearer→vs-mlrt; PSD→Stretchy Studio→spine_anim_mcp→Natron; Blender rig→soda→Natron; motion-canvas→xfade→ComfyUI-VideoColorGrading LUT pass)

## 6. Caveats
- 4 repos need license confirmation before redistribution (fine for internal use): ComfyUI-VideoColorGrading, tiny-2d-rig-tools, Rigging-sketches, Motion-Synthesizer
- GPU weights on Kaggle (code local, weights deleted per CODE ONLY): DistilDRBA, vs-gmfss_fortuna, plus runtime checkpoints for deployed models

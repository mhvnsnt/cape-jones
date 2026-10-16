# TRACK A wiring guide — animation/interpolation + 2D rigging + compositing/VFX

Everything under `~/workspace/tools/trackA-{interpolation,rigging,vfx}/`. License column must stay
commercial-ok for internal production tools (MIT/Apache-2.0/GPL allowed; research-only skipped).

## INTERPOLATION — which to use when

| Situation | Tool (path) | Entry point |
|---|---|---|
| General 24fps show footage, fast | RIFE v4.26 (already have) / FILM (already have) | comfui nodes / `film` CLI |
| Anime on-twos, large motion | **InterpAny-Clearer** `trackA-interpolation/interpany-clearer` — distance-indexed, per-object re-timing | `inference_video.py` |
| Diffusion-based inbetween (stylized) | **5DVFI** `trackA-interpolation/5DVFI` (MIT) | `base_model.train` / inference scripts |
| Flow-based classical, light | **BMBC** `trackA-interpolation/BMBC` (MIT) | `run.py` |
| Kernel-based adaptive | **AdaCoF** `trackA-interpolation/AdaCoF-pytorch` (MIT) | `run.py` / `AdaCoF_model` |
| Efficient light model | **IFRNet** `trackA-interpolation/IFRNet` (MIT) | `demo.py` |
| Small model, CPU-friendly | **ST-MFNet** `trackA-interpolation/ST-MFNet` (MIT) | `test.py` |
| Anime dedup + VFI scripts | **DistilDRBA** `trackA-interpolation/DistilDRBA` | README pipelines |
| VapourSynth anime VFI | **vs-gmfss_fortuna** `trackA-interpolation/vs-gmfss_fortuna` | `vs-gmfss_fortuna.py` |
| VapourSynth ML runtime (ONNX: RIFE, Real-CUGAN, waifu2x…) | **vs-mlrt** `trackA-interpolation/vs-mlrt` (MIT) | `vsmlrt.py` |
| Optical flow for guided tweening | **RAFT** `trackA-interpolation/RAFT` (BSD-3) | `demo.py` |
| **Line-art inbetweening (vector)** | **JoSTC** `trackA-interpolation/JoSTC` (SIGGRAPH 2024) — stroke tracing + correspondence, outputs SVG for CACANi inbetweening | `sketch_tracing_inference.py` |
| Sketch-guided cartoon inbetweening | **Inbetweening (xiaoyu258)** `trackA-interpolation/Inbetweening` | `demo_inbetweening.py`-style scripts |
| Paper/code index for future pulls | **Awesome-AI4Animation** `trackA-interpolation/Awesome-AI4Animation` | README tables |

Skipped (research-only license): CDFI, XVFI, VFIformer. Noted in report.

## RIGGING — which to use when

| Situation | Tool | Entry point |
|---|---|---|
| Flat PSD → rigged 2D character, AI-assisted | **Stretchy Studio** `trackA-rigging/stretchystudio` (MIT) — auto-rig (DWPose/heuristic), mesh deformation, Spine 4.0 export | `index.html` / editor.stretchy.studio |
| Cutout rig in Blender (Grease Pencil) | **tiny-2d-rig-tools** `trackA-rigging/tiny-2d-rig-tools` — auto armature + IK/FK, action tools | Blender addon: `tiny_2d_rig_tools/` |
| PSD → Spine 4.2 rig + procedural anims (agent-driven) | **spine_anim_mcp** `trackA-rigging/spine_anim_mcp` (MIT) — idle/walk/run/jump/attack/hit generators | `python -m spine_anim_mcp.server` / `tests/test_pipeline.py` |
| Import Spine 2D → Blender | **md_spine_tools** `trackA-rigging/md_spine_tools` (MIT) | Blender addon `__init__.py` |
| Free 2D bone editor (game-style) | **FlowBoneEditor** `trackA-rigging/FlowBoneEditor` — bones/timeline/skins, web + desktop | flowbone2d/FlowBoneEditor repo |
| Auto-rig from T-pose sketch (research) | **Rigging-sketches** `trackA-rigging/Rigging-sketches-for-2D-character-animation` — mesh contraction + pose-estimation skeleton | `rigit.py` (GUI) / `rundemo.sh` |
| Photoshop Puppet Warp in Python | **puppet-warp** `trackA-interpolation/puppet-warp` — ARAP/graph warp, scriptable mesh deformation | `from pwarp import graph_warp` / `Demo` |
| DUIK itself (cutout rigging in AE) | **rxlaboratory-duik** `trackA-rigging/rxlaboratory-duik` — OCO open cutout format, meta-rigs, auto-rig | Duik installer / ExtendScript |

Note: DUIK's own license — check LICENSE in repo; Duik is free and open-source (GPL-3.0 for the modern rewrite). Verify before redistributing; internal use is fine.

## COMPOSITING / VFX

| Situation | Tool | Entry point |
|---|---|---|
| Node compositing (AE/Nuke-like) | Natron (already have) + **openfx-misc / openfx-arena** source `trackA-vfx/openfx-{misc,arena}` — includes Shadertoy GLSL node, particles, glows, lens flares | C++ source; prebuilt plugins ship with Natron |
| 120+ video filters scriptable | **frei0r** `trackA-vfx/frei0r` (GPL-2.0) — glow, distort, colorgrade… | `ffmpeg -vf frei0r=filter_name=glow` (needs --enable-frei0r) |
| Programmatic motion graphics / titles | **motion-canvas** `trackA-vfx/motion-canvas` (MIT) — TypeScript, Canvas API, agent-writable | `npm create` project / `src/project.ts` |
| Math/title animation, data-driven | **manim** `trackA-vfx/manim` (MIT) | `manim -qm scene.py` |
| In-browser post-FX (glow/bloom/glitch/CRT) | **Motion-Synthesizer** `trackA-vfx/Motion-Synthesizer` — single-file HTML, WebGL, export MP4/WebM | `Motion-Synthesizer-v-07.html` in Chrome |
| Motion-design recipes for agents | **claude-motion-skills** `trackA-vfx/claude-motion-skills` (MIT) — principles + tool recipes | `README.md`, `tools/` |
| Natron comp from Blender render | **soda** `trackA-rigging/soda` (FrankFirsching) — Blender addon generates Natron light-group comp | Blender addon panel |
| FFmpeg effect chains (glow, speedlines, impact flash, xfade, key, shake, film look) | `trackA-ffmpeg-fx-chains.sh` (post-pipeline, built this run) | `source` the script, call `fx_*` |
| LUT-based video color grading (ICCV 2025, ComfyUI) | **ComfyUI-VideoColorGrading** `trackA-interpolation/ComfyUI-VideoColorGrading` (kijai) | ComfyUI custom nodes |

## Wiring (how they connect)

1. Keyframes/animatic → **JoSTC** (vector stroke correspondence) → CACANi inbetweening → **RIFE/InterpAny-Clearer** temporal smoothing → **vs-mlrt/RIFE-TensorRT** final rate.
2. Character art (PSD) → **Stretchy Studio** (auto-rig) → export Spine JSON → **spine_anim_mcp** procedural cycles → composite in Natron.
3. Blender 2D rig (**tiny-2d-rig-tools**) → render → **soda** generates Natron comp → per-light tweaks.
4. Titles/transitions → **motion-canvas/manim** → **ffmpeg xfade chains** → **Natron** final comp → **ComfyUI-VideoColorGrading** LUT pass.
5. Morph transitions between shots → **morpher91** (browser, Delaunay/TPS/Beier-Neely) or **puppet-warp** (scripted).

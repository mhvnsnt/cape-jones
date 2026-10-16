# MEGA-PULL — 2026-10-16
**Owner directive: "pull in like way way way more than you even think we need."**
6 parallel tracks, horizontal stacking + vertical stacking + branching. All license-checked for commercial use.

**Disk: 80% → 86% during pull.** Code-only rule enforced; model weights noted as "Kaggle" (download on GPU box, not local). Pulls halted at ceiling; remaining items documented-only.

**Per-track reports:** [TRACK-A-PULL.md](sandbox://workspace/tools/TRACK-A-PULL.md) · [TRACK-B-AUDIO-PULL.md](sandbox://workspace/tools/TRACK-B-AUDIO-PULL.md) · [TRACK-C-PULL-REPORT.md](sandbox://workspace/tools/TRACK-C-PULL-REPORT.md) · [TRACK-D-PULL.md](sandbox://workspace/tools/TRACK-D-PULL.md) · [TRACK-E-SUMMARY.md](sandbox://workspace/tools/TRACK-E-SUMMARY.md) · [track-f/README.md](sandbox://workspace/tools/track-f/README.md)

---

## TRACK A — Animation/interpolation + 2D rigging + Compositing/VFX
**Full report:** [TRACK-A-PULL.md](sandbox://workspace/tools/TRACK-A-PULL.md)

### Interpolation (17 tools, `tools/trackA-interpolation/`, ~494MB)
| Tool | License | Why it matters |
|---|---|---|
| **InterpAny-Clearer** (ECCV2024 Oral) | MIT | Anytime VFI sharper than RIFE on large motion + per-object re-timing |
| **JoSTC** (SIGGRAPH 2024) | Apache-2.0 | Joint stroke tracing + correspondence — rough line-art → vector strokes with correspondence, SVG for CACANi inbetweening. THE vector-inbetweening backbone |
| **5DVFI** | MIT | Diffusion-based VFI for stylized/hard-motion shots where flow smears |
| **BMBC / ABME** | MIT | Bilateral motion estimation baselines; ABME handles occluded motion |
| **IFRNet / ST-MFNet** | MIT | Efficient/light VFI — batch throughput, CPU-friendlier |
| **FILM** (Google) | Apache-2.0 | Large-motion interpolation, complements RIFE |
| **DistilDRBA** | MIT | Distilled anime VFI for real-time playback + scene-change detection (weights on Kaggle) |
| **vs-gmfss_fortuna** | MIT | VapourSynth GMFSS Fortuna wrapper (weights on Kaggle) |
| **vs-mlrt** | GPL-3.0 | VapourSynth ML runtime: ONNX RIFE, Real-CUGAN, waifu2x in scripts |
| **RAFT** | BSD-3 | SOTA optical flow — powers guided-tweening/warp pipelines |
| **Sketch-Guided Inbetweening** | MIT | Keyframe + sketch → cartoon inbetweens |
| **morpher91** | MIT | WebGPU 2D morphing studio (Delaunay warp, thin-plate splines, Beier-Neely) — shot-transition morphs |
| **puppet-warp** | GPL-3.0 | Photoshop Puppet Warp as Python lib — scriptable mesh tweening |
| **ComfyUI-VideoColorGrading** | ⚠️ no LICENSE — reference only | ICCV 2025: diffusion 3D LUT from reference — consistent show grading |
| **Awesome-AI4Animation** | link list | ICCVW 2025 index of every GenAI-for-cel-animation paper — future-pull shopping list |

Skipped (license): CDFI, XVFI, VFIformer (research-only); Remotion (paid team license → motion-canvas instead).

### 2D Rigging (8 tools, `tools/trackA-rigging/`, ~466MB)
| Tool | License | Why it matters |
|---|---|---|
| **Stretchy Studio** | MIT | FOSS 2D animation: flat PSD → AI auto-rig, mesh deform, Spine 4.0 export. Closest open Live2D/Spine studio |
| **spine_anim_mcp** | MIT | MCP server: PSD → Spine 4.2 rig + procedural idle/walk/run/jump/attack/hit generators. Agent-drivable |
| **DUIK** | GPL | THE open After Effects rigging suite + OCO open cut-out format + auto-rig |
| **Rigging-sketches** | ⚠️ no LICENSE — verify | Auto-rig from T-pose sketch via skeletonization |
| **md_spine_tools** | MIT | Blender addon: Spine JSON/atlas → Blender meshes + armature |
| **tiny-2d-rig-tools** | ⚠️ no LICENSE — verify | Blender addon: one-click 2D armature + IK/FK + Grease Pencil binding |
| **soda** | GPL | Blender addon generating Natron comp from Blender scene — the Blender→Natron bridge |

### Compositing/VFX (7 tools, `tools/trackA-vfx/`, ~82MB)
| Tool | License | Why it matters |
|---|---|---|
| **frei0r** (source) | GPL-2.0 | 120+ scriptable video filters, callable from FFmpeg |
| **openfx-misc / openfx-arena** | GPL-2.0 | Natron's OFX plugin sets: Shadertoy GLSL node, particles, glows, lens flares, transitions |
| **motion-canvas** | MIT | Programmatic motion graphics (TS/Canvas) — agent-writable titles/transitions |
| **manim** | MIT | Programmatic animation — explainer segments, animated diagrams |
| **claude-motion-skills** | MIT | Motion-design skill pack: camera choreography, GSAP/SVG/Lottie recipes |

### Wired (in `post-pipeline/`)
- **trackA-ffmpeg-fx-chains.sh** — 8 effect chains: glow, speedlines, impact-flash, 25-transition xfade, frei0r glow, film look, chroma-key comp, impact shake
- **trackA-wiring-guide.md** — tool-selection matrix + 5 pipeline wirings (vector inbetweening chain, PSD→Spine→Natron, Blender→Natron, motion-canvas→LUT grade)

---

## TRACK B — Voice/TTS + Music/sound
**Full report:** [TRACK-B-AUDIO-PULL.md](sandbox://workspace/tools/TRACK-B-AUDIO-PULL.md) — 45 repos, 7 glue scripts, all license-cleared.

### Voice/TTS (18 engines)
**New 2026:** Qwen3-TTS (Apache-2.0, 10 langs), Higgs Audio v2 (conversational multi-speaker), Step-Audio (instruction-led), Sesame CSM-1B. **Workhorses:** Piper TTS (fastest CPU, ONNX voices), KittenTTS (<25MB SOTA CPU), StyleTTS 2 (emotion), CosyVoice 2 (streaming, 9 langs), GPT-SoVITS v4 (clone + singing), Tortoise (expressive zero-shot), WhisperSpeech (long-form), Matcha-TTS (fast non-AR), MeloTTS (light multilingual). **Studio UI:** TTS-WebUI (Gradio+React, all engines as extensions). **Fallback:** espeak-ng (GPL-3.0, zero deps).

### Voice conversion / singing
RVC (MIT, huge model community), Seed-VC (GPL-3.0), so-vits-svc 4.1 (AGPL-3.0, singing), DiffSinger (Apache-2.0, synthesis from score).

### Music generation
ACE-Step (Apache-2.0, lyrics→full song), DiffRhythm v1/v2 (Apache-2.0), SongGen (Apache-2.0, +3s voice clone), Stable Audio Open (Stability Community License, commercial OK <$1M/yr), Magenta (Apache-2.0, compositional MIDI). YuE2 flagged: CC-BY-NC + creator permission — companies need license.

### SFX / restoration / mastering
Stable Audio Open (text→SFX) + MMAudio (video→SFX, already had). Demucs + UVR5 (stem separation), DeepFilterNet (noise), VoiceFixer + Resemble Enhance (restoration), Pedalboard (Spotify's programmatic FX), loudnorm via FFmpeg (broadcast loudness).

### Lip-sync helpers (beyond LatentSync/MuseTalk/OpenFaceFX)
Forced aligners + phoneme tools — see report.

### Wired (in `post-pipeline/`)
**tts_voices.py / tts_voices_2026.py** (multi-engine TTS router), **voice_convert.py**, **music_gen.py**, **sfx_gen.py**, **stem_sep.py**, **audio_restore.py**, **lipsync_align.py** — all py_compile clean.

### Skipped (license)
Fish Speech, Breeze TTS 2, F5-TTS weights (CC-BY-NC), Coqui XTTS (license changed — verify before use).

---

## TRACK C — 3D assets + Game dev + Comic/manga
**Full report:** [TRACK-C-PULL-REPORT.md](sandbox://workspace/tools/TRACK-C-PULL-REPORT.md)

### 3D assets pulled (all CC0)
- **Kenney Nature Kit** — 329 GLB: trees, rocks, plants, bridges (10.5MB) → `cape-jones-build/3d-assets/kenney-extra/nature-kit/`
- **Kenney Car Kit** — 50 GLB: cars, ambulance, cones, crash-debris (4.8MB) → `kenney-extra/car-kit/`
- **KayKit Halloween Bits 1.0** — 63 models: pumpkins, ghosts, witches, candy (1.15MB) → `kaykit/`
- **ambientCG** — Grass004 + Wood062 PBR sets @1K (21MB) → `ambientcg-additions/`

### Game dev overlap
**TIC-80 v1.3.1** pulled + verified (MIT) — fantasy console with sprite/map/sfx editors for retro 2D effects. Documented: LibreSprite, Pixelorama, Piskel, PixiEditor, free-tex-packer, Effekseer, DragonBones, Tiled 1.12.2 (May 2026 — new Properties view, Aseprite loading). **Spine runtimes EXCLUDED** — EULA requires paid Spine license.

### Comic/manga
6 OFL fonts pulled (Bangers, Comic Neue, Luckiest Guy, Permanent Marker, Zen Maru Gothic, DotGothic16). Documented: Krita comic panel/speech-bubble tools, Kumiko panel extractor, screentone via Krita/GIMP/David Revoy brushes, webtoon templates. Blambot fonts SKIPPED (non-commercial).

### Follow-ups
- Browser lane: OpenGameArt interior pack, itch.io rigged CC0 characters, BlendSwap/Sketchfab CC0
- **Owner call needed: Quaternius license changed CC0 → QAL v1.0** (commercial games OK, no standalone redistribution)
- Kenney `character-kit` slug 404s as of today

---

## TRACK D — Video editing + Motion graphics + Pre-production
**Full report:** [TRACK-D-PULL.md](sandbox://workspace/tools/TRACK-D-PULL.md)

### NLE recommendation: **Kdenlive primary**
Only open NLE with OpenTimelineIO I/O (round-trips with our OTIO lane), built-in proxies, keyframable effects, active dev. LosslessCut alongside for instant lossless trims. Olive 0.2 watch-list. Pulled source: Olive, Flowblade, Pitivi. Documented: Shotcut, Kdenlive/ LosslessCut AppImages, Shutter Encoder, HandBrake, FFqueue, MKVToolNix.

### Motion graphics
Motion Canvas (MIT, on disk — top pick, fully-open Remotion alternative), lottie-web + LottieConverter (on disk), HyperFrames (on disk), reveal.js (on disk — pitch decks + title cards). Documented: Manim, MoviePy, ReelForge, gl-transitions (200+ WebGL transitions).

### Pre-production
screenplain (Fountain→PDF/FDX, on disk), Trelby (desktop screenwriting, on disk), Manuskript (beat-board/corkboard, on disk), afterwriting (documented). Built: **fountain_to_beats.py** (Fountain → beat sheets JSON+MD). Already had: fountain_to_animatic.py, animatic_builder.py, storyboard_sheet.py.

### Wired (in `post-pipeline/`)
**kinetic_type.py** (typewriter/word-pop/cascade titles), **lower_thirds.py** (animated, ProRes 4444 alpha), **storyboard_sheet.py**, **fountain_to_animatic.py**, **fountain_to_beats.py** (new), **proxy_gen.py**.

---

## TRACK E — Production management + Distribution + Localization
**Full report:** [TRACK-E-SUMMARY.md](sandbox://workspace/tools/TRACK-E-SUMMARY.md)

### Production management
**Kitsu + Zou** (AGPL-3.0 ⚠️ — self-hosted shot/asset tracker, Blender Studio's), **OpenCue** (Apache-2.0, Sony Imageworks render-farm coordinator), **Flamenco** (GPLv3+, Blender's own render manager), **CGRU/Afanasy** (LGPL-3.0). **Recommended 2-person stack: Kitsu + Gazu + Flamenco.**

### Distribution
youtube-upload (resumable CLI), yt-dlp (Unlicense), TubeArchivist (self-hosted archive + analytics). Postiz documented (AGPL-3.0 ⚠️).

### Localization
Argos Translate (MIT, offline NMT), LibreTranslate (AGPL-3.0 ⚠️), Aegisub (BSD-3), Subtitle Edit (MIT — upstream relicensed), pysubs2 (MIT).

### Wired (in `post-pipeline/`)
**youtube_upload.py** (Data API v3, dry-run verified), **metadata_gen.py** (titles/descriptions/tags/chapters), **transcribe_translate.py** (faster-whisper → SRT → translated SRTs), **podcast_feed.py** (iTunes RSS). Deps in `post-pipeline/venv`.

**Note:** YouTube's built-in "Test & Compare" covers thumbnail A/B natively — no OSS tool needed.

---

## TRACK F — Merchandise + Community + Monetization + Live streaming
**Full report:** [track-f/README.md](sandbox://workspace/tools/track-f/README.md)

### Merchandise
printful-mcp (MIT — full POD API client + mockup generator), mockup-generator (batch tee mockups, scripts only), segno (BSD-3 — QR codes).

### Community
ForgeBot (MIT — Discord bot framework, drop in show-specific cogs), PaetreonLive (Patreon→Discord webhooks). Documented: Flarum/NodeBB/Discourse, Listmonk, Markette (AGPL ⚠️ — write-once-post-everywhere).

### Monetization
threefive (GPL-2.0 — SCTE-35 ad markers), tip-root (AGPL-3.0 ⚠️ — self-hosted tipping + OBS alerts, zero fees), creatoros (revenue dashboard, no license — reference).

### Live streaming
**OpenVT** (MIT — the open VTube Studio alternative, Godot + OpenSeeFace), **Fanfare** (MIT — self-hosted Streamlabs-style alerts/overlays), CriStream (MIT — bot + overlays), obsws-python (OBS WebSocket scripting), recbar (recording companion), burgertuber (tracking→web avatar reference).

### Wired (in `track-f/glue/`)
**merch_qr.py** (QR codes, tested), **obs_scene_json.py** (OBS scene import, tested).

**Practical picks (next 3 months):** Fanfare → ForgeBot → merch_qr.py → mockup-generator → printful-mcp → recbar.

---

## LICENSE FLAGS (do not use commercially until cleared)
- **MiniMax H3 / ComfyUI-H3-LongTake** — excludes US/EU/UK/KR. Unusable.
- **TalkingPose** — research-only. **Wav2Lip** — relicensed non-commercial. **CDFI/XVFI/VFIformer** — research-only.
- **Fish Speech / Breeze TTS 2 / F5-TTS weights / YuE2** — CC-BY-NC. Research only.
- **Spine runtimes** — require paid Spine license. Use DragonBones/Spriter.
- **Remotion** — paid team license >3 people. Use motion-canvas.
- **Blambot fonts** — non-commercial. Use OFL fonts pulled.
- **Quaternius** — license changed to QAL v1.0. Needs owner call.
- **AGPL** (Kitsu/Zou, LibreTranslate, tip-root, Postiz, Leantime, Markette) — fine self-hosted/internal; network clause if run as public service.
- **No-LICENSE repos** (verify before redistributing; fine for internal use): ComfyUI-VideoColorGrading, tiny-2d-rig-tools, Rigging-sketches, Motion-Synthesizer, mockup-generator, creatoros, PaetreonLive, burgertuber.

## KAGGLE QUEUE (code local, weights download on GPU box)
DistilDRBA, vs-gmfss_fortuna, all TTS/VC/music model checkpoints (see TRACK-B report), InterpAny-Clearer/FILM/RIFE checkpoints, Piper voices, Argos models (~1GB — pending, killed at disk ceiling; one-command install documented in transcribe_translate.py).

## NEW PIPELINE SCRIPTS (in `~/workspace/tools/post-pipeline/`, all tested/clean)
trackA-ffmpeg-fx-chains.sh, tts_voices.py, tts_voices_2026.py, voice_convert.py, music_gen.py, sfx_gen.py, stem_sep.py, audio_restore.py, lipsync_align.py, kinetic_type.py, lower_thirds.py, storyboard_sheet.py, fountain_to_animatic.py, fountain_to_beats.py, proxy_gen.py, youtube_upload.py, metadata_gen.py, transcribe_translate.py, podcast_feed.py (+ track-f/glue/: merch_qr.py, obs_scene_json.py)

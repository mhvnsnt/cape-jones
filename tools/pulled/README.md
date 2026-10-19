# Pulled Tools — Animation & Production

Third-party open-source tools vendored directly into this repo (PULL-STRAIGHT-TO-STORE law).
All licenses verified commercial-use OK. Weights/models stay OFF disk — code only.

## three-anime-style (xymeow/three-anime-style, MIT)
- **What:** TypeScript library giving Three.js r186+ WebGLRenderer scenes an anime look —
  three-tone character shading, painted scenery brushwork, pen outlines, anime
  shadows, film grain + acrylic frost finish, optional 12fps pose stepping.
- **Why:** cel-shaded rendering for 3D segments of the show (web preview + stage
  rendering). Browser playground included (`index.html` demo, 13 examples).
- **Use:** read its `README.md` + `skills/three-anime-style/SKILL.md` for integration;
  portable skill is designed for AI-agent integration.
- **License:** MIT — commercial OK.

## AnimeEffects (AnimeEffectsDevs/AnimeEffects, GPL-3.0)
- **What:** 2D animation tool (modular C++/CMake) — build & keyframe 2D animation
  without frame-by-frame drawing. Updated 2026-07.
- **Why:** 2D cutaway/gag animation alternative to Blender Grease Pencil.
- **Build:** CMake; see its `README.md`.
- **License:** GPL-3.0 — commercial use allowed (copyleft on derivative distribution).

## video-gif-studio (miles990/video-gif-studio, MIT)
- **What:** Storyboard planning + music beat analysis tool (SKILL.md included).
- **Why:** feeds the storyboard/animatic lane (Storyboarder → animatic_builder.py)
  and beat-synced gag timing.
- **Vendoring note:** the upstream `examples/` demo media (149MB of .mp4/.gif/.apng)
  was stripped from this vendored copy (demo media only — code, references,
  scripts, tests, and example READMEs/manifests retained).
- **License:** MIT — commercial OK.

## GNM (google/GNM, Apache-2.0)
- **What:** Google's parametric human head model (GNM Head, open-sourced July 2026):
  template mesh + 253 identity params + 383 expression params (100/eye, 150 lower
  face, 32 tongue, 1 iris) + 4-joint LBS, with semantic expression sampling
  (20 named expressions -> param vectors). Code vendored in `GNM/` (code only;
  model weights download on first use via the loader and were not pulled).
- **Why:** study reference for the CJ parametric face rig
  (`3d-assets/face-rig/cj_parametric_face.py`) — GNM-style grouped control vectors
  driving OUR cartoon face, not GNM's realistic head. Full study:
  `docs/research/GNM-HEAD.md`.
- **License:** Apache-2.0 — commercial OK (copyright notice retained; our changes
  documented in `GNM/PROVENANCE.md`).
- **Skipped sibling:** Nathan Dickson's free "GNM Head Importer" Blender add-on
  (Gumroad) — no stated license, requires checkout; documented, not vendored.

## Skipped (documented, not pulled)
- **genoooool/hyperframes-effects-gallery** — 255-effect catalog, but the repo
  declares NO license. Per license rules (document and skip): do not vendor until
  a license is declared. Revisit later.

## Scene wave pull-ins (2026-10-17, lane scene/fullstack-research-20261017)

### Light-Editor (riouxr/Light-Editor @ a4a08e9, GPL-3.0)
- **What:** Robert Rioux's spreadsheet-style light manager v2.4.6 — toggle,
  isolate, filter, and group every light in the scene; light linking manager.
- **Why:** the living room's light count is growing; this is the VFX-studio way
  to manage it.
- **Use:** `tools/light-editor/` (README + `install_light_editor.py`).
- **License:** GPL-3.0 — commercial OK.

### Render-Manager (riouxr/Render-Manager @ e827295, GPL-3.0)
- **What:** Robert Rioux's render-layer + render-pass manager v3.0.11 —
  per-layer 16-bit color + 32-bit data passes incl. Cryptomatte, precomp export.
- **Why:** the room is heading for compositing (god-ray glare, TV screen, LED
  glow passes).
- **Use:** `tools/render-manager/` (README + `install_render_manager.py`).
- **License:** GPL-3.0 — commercial OK.

### extra-lights (jlampel/extra-lights @ bb75dac, GPL-3.0)
- **What:** Jonathan Lampel / CG Cookie's photometric light presets v1.3.0 —
  21 `light.add_*` ops (lumens + Kelvin + IES profiles) in the Add menu.
- **Why:** physical lighting for the living room fixtures without guessing.
- **Use:** `tools/extra-lights/` (README + `install_extra_lights.py`).
- **License:** GPL-3.0 — commercial OK.

## Idle-pipeline tools wave (2026-10-19, overnight-idle-pipeline)
Five open-source tools that were sitting as local-only clones in ~/workspace/tools/
(untracked, unbacked-up) — now vendored into the repo (first store) per the
PULL-STRAIGHT-TO-STORE / CONTINUOUS-MIRROR laws. Additions only, 0 deletions.
All licenses verified commercial-use OK (see license notes). No model weights
vendored — weights download at run time per each tool's README. No binaries
>50MB, no node_modules, no .env.

### OpenTimelineIO (AcademySoftwareFoundation/OpenTimelineIO, Apache-2.0)
- **What:** Academy Software Foundation's open API + interchange format for
  editorial timeline data — read/write OTIO, EDL, FCP XML and more. C++ core
  with Python bindings.
- **Why:** timeline interchange for the EP/edit pipeline — move cuts between
  NLEs and our tooling without hand-rebuilding timelines.
- **Use:** `production/tools/opentimelineio/` — its README; Python package
  `opentimelineio`.
- **License:** Apache-2.0 — commercial OK.

### OpenVoice (myshell-ai/OpenVoice, MIT)
- **What:** instant voice-cloning text-to-speech — clone a voice from a short
  audio sample, multilingual, with tone/emotion/color control (MyShell.ai).
- **Why:** character voice generation and cloning for dialogue — complements
  Dia (below) and the existing voice lanes.
- **Use:** `production/tools/openvoice/` — see its README; checkpoints download
  at run time (kept OFF disk by policy).
- **License:** MIT — commercial OK.

### TheAnimeScripter (NevermindNilas/TheAnimeScripter, AGPL-3.0)
- **What:** AI anime video upscaling / frame interpolation / restoration toolkit
  (RIFE-class interpolation, Real-ESRGAN-class upscaling, scene-aware).
- **Why:** upscale + interpolate anime/2D segments, restore low-res reference
  footage for the show pipeline.
- **Use:** `production/tools/theanimescripter/` — see its README; model weights
  download at run time (kept OFF disk by policy).
- **License:** AGPL-3.0 — commercial use allowed; copyleft: if you run a
  modified version as a network service you must share the source. This repo is
  public, so the source is published.

### ChibiRigKit (milkc0de/ChibiRigKit, Apache-2.0)
- **What:** Blender one-click auto-rig kit for chibi-style characters, ships
  with a sample character.
- **Why:** fast rigs for chibi/cute character variants in gags and shorts —
  complements the full-body auto-riggers (blenrig6, afk-rig, ml-autorig,
  pinocchio, skintokens-autorig).
- **Use:** `production/tools/chibirigkit/` — `AUTO_RIG.sh` / README; sample
  character under `characters/`.
- **License:** Apache-2.0 — commercial OK.

### Dia (nari-labs/Dia, Apache-2.0)
- **What:** Nari Labs' 1.6B-parameter open text-to-speech model — natural
  dialogue synthesis, speaker-consistent, runs locally.
- **Why:** local TTS for dialogue/narration without cloud billing; pairs with
  OpenVoice for cloning.
- **Use:** `production/tools/dia/` — `cli.py` / `app.py`; model weights download
  at run time (kept OFF disk by policy).
- **License:** Apache-2.0 — commercial OK.

## Mocap + camera-match wave (2026-10-19, overnight-idle-pipeline)

### FreeMoCap (freemocap/freemocap @ main, AGPL-3.0)
- **What:** markerless motion capture from 2+ ordinary webcams/phones —
  calibration, recording, 3D skeleton triangulation (body + hands + face),
  Blender export (`freemocap/core/blender/export_to_blender.py`).
- **Why:** real human motion for the 3D animation automation directive — the
  direct answer to hand-posed sitting reading robotic. Capture real
  performances, retarget via the repo's mocap-retarget pipeline.
- **Use:** `production/tools/freemocap/` — wiring doc `CAPE-JONES-WIRING.md`;
  install at runtime with `pip install freemocap` (python 3.9–3.11, NVIDIA GPU
  recommended). Pairs with `production/tools/mocap-retarget/` and
  `production/tools/rhubarb-lip-sync/`.
- **Vendoring note:** sparse pull of essentials only — the `freemocap` Python
  package + README/LICENSE/CITATION.cff/pyproject.toml. The `freemocap-ui`
  frontend, docs site, and sample data were NOT pulled. Pose-estimation models
  download at runtime (kept OFF disk by policy).
- **License:** AGPL-3.0 — commercial use allowed; copyleft applies only if a
  *modified* version is distributed or run as a network service. This repo is
  public, so the source is published.

### fSpy-Blender (stuffmatic/fSpy-Blender v1.0.3, GPL-3.0)
- **What:** official fSpy camera-matching importer for Blender — imports
  `.fspy` projects as solved Blender cameras with the photo as background
  plate. Pure Python, zero dependencies.
- **Why:** matchmove for set building — solve real cameras from still photos,
  build environments to match, no eyeballed perspective.
- **Use:** `production/tools/fspy-blender/` — `install_fspy_blender.py
  --blender <dir>` installs into Blender's addons; wiring doc
  `CAPE-JONES-WIRING.md`. The fSpy app itself (Electron) is NOT vendored —
  fetch from fspy.io when a solve is needed.
- **License:** GPL-3.0 — commercial use allowed (copyleft on derivative
  distribution of the add-on itself).

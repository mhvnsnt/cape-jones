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

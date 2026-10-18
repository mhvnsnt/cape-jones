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

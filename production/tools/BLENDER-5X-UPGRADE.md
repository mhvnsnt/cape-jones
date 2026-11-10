# Blender 5.x Upgrade Path

**Current:** 4.0.2 at `~/workspace/tools/blender/blender-4.0.2-linux-x64/`
(headless note: run under `xvfb-run -a` + `env -u PYTHONPATH` — see TOOLS.md)
**Target:** 5.2.x LTS (latest: 5.2.2, released 2026-09-15; supported until July 2028)
**License:** GNU GPL (open source, free)

## Why upgrade

4.0.2 is two major versions behind. The 5.x line brings the capabilities that
matter for the Cape Jones 2D pipeline:

- **Grease Pencil overhaul** — new fill workflow with hole support, SVG import/export
  for fills, stroke/fill management tools (5.1+). 2D/3D hybrid shots get real.
- **Geometry Nodes drive Grease Pencil** — procedural effects on 2D drawings,
  Bone Info node for rig-driven setups. This is the closest open equivalent to
  Harmony-grade procedural 2D.
- **Compositor** — 2x faster nodes (Glare, Directional Blur, Lens Distortion):
  our bloom/glow post passes get cheaper.
- **Animation playback** — significantly improved for complex rigs; shape-key
  eval up to 4x faster on high-poly meshes.
- **LTS support** — 5.2 LTS is supported until July 2028 (4.2 LTS is EOL).

## Upgrade path (documented, NOT installed yet)

1. Download the Linux portable archive from https://www.blender.org/download/
   (pin: 5.2.x LTS — portable `.tar.xz`, no root needed).
2. Extract alongside the current install — do NOT replace 4.0.2 in place:
   ```
   ~/workspace/tools/blender/blender-5.2.x-linux-x64/blender
   ```
3. Re-verify the headless recipe on 5.x:
   `xvfb-run -a env -u PYTHONPATH <new-blender> -b --python-expr "..."`
   (libEGL requirement that forced xvfb on 4.0.2 may differ — test first.)
4. Run the existing rig/proof scripts against 5.x in a scratch dir; compare
   renders vs 4.0.2 before switching any pipeline default.
5. Only after proofs pass: update pipeline docs to point at 5.x, keep 4.0.2
   archived until the owner signs off.

## Blocker / caution

- Do NOT install until disk pressure is resolved — the archive is ~350MB and
  local disk is a cache, not storage (NO-LOCAL-CLUTTER LAW).
- The 4.0.2 headless workaround (`xvfb-run`) must be re-proven on 5.x; if 5.x
  needs different libs, document before migrating.

## Pipeline role (unchanged, faster)

Blender stays the 3D + final-compositing stage: Grease Pencil 2D/3D hybrid shots,
node compositor for bloom/glow passes, VSE for final assembly. 5.x makes each
of those faster and adds procedural 2D via Geometry Nodes.

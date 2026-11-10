# Harmony 27 — File Formats (public docs, 2026-11-01)
Sources: Toon Boom Help Centre "About saving options in Harmony" and
Harmony 27 Premium documentation "About Toon Boom Harmony Premium"
(docs.toonboom.com). No proprietary files were read, copied or redistributed
in this job; the installer was not executed on Linux.

## Scene
- `.xstage` — the Harmony scene file. It is NOT a single self-contained
  blob: it lives in a scene folder that contains all images, elements,
  sounds, palettes, etc. used by the scene. Open by double-clicking the
  .xstage icon, or File > Open / Welcome Screen. Created by File > New Scene
  / Create Scene.
- `.vbd` / Compact file (v25+) — compatible elements combined into a
  single `.vdb` (virtual database) inside the scene structure. Faster open
  for large scenes and Control Center import/export. WARNING in the docs:
  compact structures are NOT compatible with versions older than v25;
  uncompact before using with older versions. Default for this bridge:
  NON-compact .xstage, so the pack below is inspectable file-by-file.

## Drawings / vectors
- `.tvg` — Toon Boom Vector Graphic. Vector drawings created in Harmony
  are .tvg. A drawing layer's cells link to the drawing files in the
  layer's directory; a drawing cycle re-uses the same original files.
- Bitmap drawings — imported PNG/JPEG/PSD etc. stay as bitmap elements;
  they are NOT silently converted to .tvg unless you run vectorisation.
- `pix2vec` (utility, public docs) — converts scanned / bitmap line art to
  .tvg, line art in the line-art layer, colour zones in the colour-art
  layer. Syntax: `pix2vec -file INPUT [options]`, one file at a time;
  loop in shell for a series. Options include `-outfile`, `-rmv_holes`,
  `-rmv_dirt`, `-rmv_hairs`, `-output_version 0|604` (604 = current TVG).
  Use for our clean-cut pieces ONLY if we want a vector version; the
  default bridge keeps pieces as bitmap, whole, no re-vectorisation edit.
- `swf2tvg` (utility) — converts SWF to .tvg per frame; NOT used here
  (our .fla pieces are not SWF, and Flash .fla itself is not supported
  for direct import — export first, per docs).

## Palettes / templates / libraries
- Palette files (`.plt` in Harmony usage) — colour lists shared between
  scenes. The docs warn: sharing palettes between scenes can accidentally
  modify colours. Rule for this bridge: one Cape Jones palette per
  production, versioned, never edited in a scene without a new version.
  This job ships palette as CSV (see bridge doc) plus a Harmony import
  step; it does NOT fabricate a byte-exact .plt, because that format's
  exact bytes were not verified from a live Harmony install.
- Templates (`.tpl`) — saved rigs / node groups / drawings from the
  Library, reusable across scenes. Our sitting rig is shipped as a
  template SPEC (node CSV + pieces + palette), to be saved as .tpl inside
  Harmony after the first successful import — not faked here.
- Library — personal / shared libraries of templates, palettes, drawings.
  Keep Cape Jones templates in a personal library named `CapeJones`,
  not mixed with sample libraries.

## Scripting
- Qt Script, ECMAScript-based, very similar to JavaScript. Scripts are
  plain-text `.js` files (since Harmony 10.3, replacing .qsa).
- Three interfaces (docs): (1) Harmony Scripting — main interface,
  automate workflows, dialogs, batch operations; (2) Extended Scripting —
  modules for editing drawings, creating tools/toolbars, executing Python;
  (3) Script Node — a node that takes peg/image input, runs a custom
  script, outputs peg/image, e.g. the Maya Render Batch node is a Script
  Node. Plus Control Center scripting (command-line via Control Center)
  and a Python interface (Python representation of HarmonyGUI/project).
- Node attributes via script, documented pattern:
  `node.getAttr("Top/Drawing-P", 1, "position.x").doubleValue()`
  — i.e. full node path, frame, attribute name. Publish Attribute Mode /
  Show Attribute Information in Node View gives the exact attribute name
  for any node. Our stub uses exactly this pattern and nothing else
  proprietary.
- Action interface: `Action.perform("onAction…()", "responder")` and
  `Action.validate(...)` — used in the stub only as commented examples,
  not as executed calls, until tested in-app.

## Import / export (for TV production)
- Import: PNG, JPEG, PSD, PDF, AI (RGB only, no CMYK, no gradients/textures
  for AI/PDF per docs), MOV, audio. Export: MP4, MOV, AVI, image sequences,
  4K and higher (per Harmony product docs). Premium adds: full node-based
  compositing, 3D object integration, advanced particles, master
  controllers, hybrid 2D-3D — the only edition with full hybrid workflow.
- Storyboard Pro → Harmony: an animatic can be exported into separate
  Harmony scenes, so storyboard poses become scene layouts. That maps
  directly to our storyboards/animatic (30/30 panels, 1/1 animatic) —
  see REVERSE-ENGINEER-MAP.

## What is NOT in this doc, deliberately
No installer contents, no binary hashes beyond the installer filename/size
already reported by Mars, no license-key material, no cracked format
specs. If a format needs a live install to verify, it is marked UNVERIFIED
in the checklist, not guessed.

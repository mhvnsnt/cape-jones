# Pipeline landing — 2026-10-31 clean-100 + v2/v3 batches

This doc is the pipeline pointer for the landed batch. Content approval is Mars's
alone — repo landing is NOT content approval.

## Landed batches (branch feature/cape-jones-clean100-landing-20261031, PR-only)
- clean-100-20261031/ — exposure sheets 5/5, clips 23/23, painted backgrounds 4/4,
  layout passes 5/5, flex-opposition 4/4, shot specs 30/30, god-ray decisions 30/30,
  delivery spec 1/1, Blender proof render 1/1, ACES test 1/1, proof shot 1/1,
  JoJo demos 3/3, Pack 4 approval sheets 5/5, stack tests, additional standards.
  Excluded from this push (kept local, not landed): media-generation-*.json
  (generation-tool metadata with external CDN snapshot), *.blend1 backups,
  stack-tests/repo-main-tree.json (8.7 MB internal audit dump).
- device-prop-v2-20261031/ — hand-fit device, 148 px at lap vs v1 295 px, ~50% scale
  (Mars confirms exact scale). True two-hand grip pose still owed.
- forearm-fist-v3-20261031/ — front-facing fist, Arm2 clean redo. V2 upside-down
  diff-fist stays REJECTED, not approved.
- eyes-normal-superhero-v2-20261031/ — normal eyes 5/5, white angular, no pupils.
  V2 dark end is on the WRONG side (Mars: dark goes on Arm1 side) — v3 flip is
  still owed and is NOT in this batch.
- showcase/universe-color-v3-20261031/ + UNIVERSE-COLOR-LANGUAGE-V3-20261031.md —
  TRUE palette replacement, not a gain overlay. No v3 palette approved yet.
  Cape rule revised by Mars 16:35 CDT: cape changes to a different colour too,
  suit may stay white or change, choice is creator-feel / what looks cool.
- cape-styles-v2-20261031/ — 15 cape forms, 10 cloth methods.
- visemes-v2-20261031/ — mask-first visemes 14/14. Not approved yet.
- parts-catalogue-20261031/phone/ — 24 split catalogue chunks (the 14 MB single
  index.html is NOT in this push; it fails to load on phones as octet-stream).
- reposes-v7c-clean/full-final-flex-v7c-clean-20261031.png + before-after —
  full final flex: fists L -75 / R +75, forearms 135/-135, knees bent, body dipped
  28 px, feet planted. Pose only, not approved, flex clip retarget still owed.
- Rule docs: KNEE-FEET-RULE.md (knees and feet always point the same direction;
  kneecaps inward -> toes inward), ADDITIONAL-STANDARDS-20261031.md,
  DUAL-LIGHT-RIM-MIX-20261031.md (V4-level mixing = Level-3 trigger; a mix that
  only looks Level 2 is NOT Level 3).

## Pipeline wiring this landing enables
- Shot pipeline: clean-100-20261031/shots/shot-specs-30-20261031.json is the
  shot list (CJ-01–CJ-30) + god-ray-placement-30-20261031.json (9 Level-3
  placements, 21 explicit Level-2 no-god-ray decisions) + DELIVERY-SPECS-20261031.md.
  Delivery frame size + safe areas are still to be set by Mars.
- Blender pipeline: clean-100-20261031/blender-proof/ (proof shot, ACES test,
  compositor script). Blender 5.2.3 compositor output path is
  scene.compositing_node_group, NOT scene.node_tree; CompositorNodeComposite is
  undefined in 5.2 — use GroupOutput. Rim via SetAlpha + AlphaOver, never
  MixRGB Add with a small Factor image.
- Rig pipeline: v7c ball-centre pivots, pose-driven swaps (gauntlet cuff-only
  y62–180 per-row mirror; fist is NOT re-mirrored), knee-feet rule checked
  before any pose ships, alignment QC for Arm2 still owed (diagnosis running).
- Colour pipeline: LUTs 70/70 approved (base 30 + spectrum 24 + spectrum v2 16).
  Dialect 1 = LUT/rim/grade. Dialect 2 = JoJo palette replacement (v3 tables),
  NOT a .cube LUT. Rim follows key/LUT hue ±20°, or shifted key on shifted shots.
  Dual-light: cyan backlight god rays ONLY for cyan rim + gold LUT/overlay
  combined; gold rim alone gets NO cyan backlight.
- Chat-viewable rule (Mars, 16:25–16:29 CDT): visuals in chat as embedded
  images only. No download links, no file links for non-viewable types.
  Non-viewable files live in this repo, named in plain text only.
  New versions get NEW dated/versioned filenames, never the same name as a
  version Mars has seen, or the client shows the cached old image.

## Still owed, not landed here (kept local, reasons in parent report)
- STATUS-20261031-1428.md / TRACKER-20261031.md — moving targets, other lanes
  editing live; micro-push once appending stops.
- Eyes v3 (dark-end flip), god-ray Level-3 rebuild, light-wrap v2, knee-feet
  dance fix, JoJo cape/suit variation sheet, Arm2 alignment rebuild, device
  prop v3 scale confirmation, flex clip retarget — not delivered yet, so not
  pushed. Pushing them before delivery would land the wrong version.
- Comparison tests 0/7 — no their-side viewed files; needs legitimate
  Harmony/Animate trial install.

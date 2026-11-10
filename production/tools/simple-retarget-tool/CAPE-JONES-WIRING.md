# Simple Retarget Tool — Cape Jones Wiring

**Upstream:** https://github.com/cgvirus/Simple-Retarget-Tool-Blender @ 3adcfaf (main)
**License:** GPL-3.0 — own-eyes verified in-tree (`LICENSE`, 2026-10-18). Free AND
commercial-safe as a tool (same standing as afk-rig: used, not redistributed).
**What:** Single-file Blender addon that retargets mocap/armature animation onto
other armatures — Mixamo, BVH, iClone sources → Rigify, Daz3D (G3/G8), or custom
rigs. V2 added one-click "Set Rest Pose" + preset import/export; V3 added
blend-shape-safe rest pose. 144 stars / 19 forks / 3 releases.

## Why it matters for Cape Jones

This closes the one genuinely open gap on the AUTO-RIGGING PRIORITY law's
**auto-retargeting** axis: a free, open-source, commercial-safe BVH→rig
retargeter with no account gate, no paid tier, and no proprietary plugin.
Pairs with the already-pulled motion sources (afk-rig's 178 CC0 human clips,
Mixamo downloads, CMU BVH) and the pulled rigs (Rigify/CloudRig/BlenRig 6,
afk-rig-generated human skeleton, UniRig/TokenRig outputs).

## Install (artist machine)

1. Blender → Edit > Preferences > Add-ons > Install from Disk… select
   `production/tools/simple-retarget-tool/Simple_Retarget_Tool.py` (or the
   whole folder as a zip).
2. Enable "Simple Retarget Tool". It appears as a panel in the 3D Viewport
   sidebar (check README/video links in the folder for the exact tab name).

## Retarget workflow (per upstream V2 tutorial)

1. Import your source armature + animation (BVH via File > Import, Mixamo FBX,
   iClone FBX).
2. Select your target armature (Rigify / Daz3D / custom game rig).
3. In the tool panel: pick source ↔ target bone pairs ("characterization"),
   then hit **Set Rest Pose** so both rest poses match the mocap rest pose
   (this is the step most retarget failures come from).
4. Save the bone map as a **preset** (import/export — reuse per character
   generation, e.g. all G8 imports).
5. Run retarget → bake to action on the target rig → polish in Graph Editor.

## Tips from upstream Q&A (verified on the Blender Nation thread)

- Source and target MUST share the same rest pose; use the one-click
  "Set Rest Pose" script instead of doing it bone-by-bone in the modifier.
- Offsets (e.g. raising shoulder bones on Genesis characters) are persistent;
  corrections can also blend in/out (animation-layer style).
- To get animations back out to other apps/game engines: bake the action and
  export (FBX/GLB) — same as any Blender retarget.

## Cape Jones lane notes

- The hip-placement/limb-proportion technique note (from the "Good Good"
  research row) applies here too: before retargeting, scale the source
  armature to the target's proportions, line up hip bones first, then limbs.
- Foot-slide cleanup: pair with afk-rig's `weights`/`inspect` pass or do the
  standard IK-foot-pin polish after baking.
- Blender-version note: the addon is 2021-era code (V3). It is two small
  Python files with no external deps; `py_compile` passes on 3.12. If a
  `bl_info` or API deprecation surfaces on Blender 4.x/5.x, the fix surface
  is tiny — patch in-tree and note it here.

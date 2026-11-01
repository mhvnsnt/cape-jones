# Blender compositor Alpha Over fix — 100% Blender, no PIL composite (2026-10-31)

## Problem, plainly
In the Kaggle notebook, Blender 5.2.3 background-mode compositor Alpha Over
did NOT apply the 2D character plate — pixel checks showed 0 dark plate
pixels in both Alpha Over input orders — so the final frame was composited
with PIL in the notebook instead. That was NOT a Blender-compositor success.
Mars ordered it solved 100% with whatever industry-standard method fixes it.

## Root cause — three traps, all verified locally with Blender 5.2.3 LTS
1. **CompositorNodeComposite is UNDEFINED in Blender 5.2.** Probe result:
   `CompositorNodeComposite FAIL: Node type undefined` — same class of
   API break as the earlier Mix/Math nodes (CompositorNodeMixRGB and
   CompositorNodeMath are also undefined; the 5.2 types are
   ShaderNodeMixRGB / ShaderNodeMath). Any script that creates a
   "Composite" node fails or leaves the tree with no output, so the
   render that comes back is the empty 3D scene, with 0 plate pixels.
   The correct 5.2 output path is: create a CompositorNodeTree, assign
   it to `scene.compositing_node_group`, create an interface OUTPUT
   socket named "Image" (`tree.interface.new_socket(...)`), then link
   the final node to a `NodeGroupOutput` node. That IS the Composite
   output in 5.2.
2. **Building/saving the .blend alone produces NO image, and reading
   'Render Result' before a render produces NO plate.** The compositor
   only executes during a render, with `scene.render.use_compositing=True`
   and `bpy.ops.render.render(write_still=True)` with `filepath` set.
   The earlier stack script built the tree and saved the .blend and
   explicitly did NOT claim a render — that gap is where a Kaggle run
   that only built the tree would report 0 plate pixels.
3. **MixRGB Add with a small Factor image crops the output.** First
   final render here used MixRGB ADD for the cyan rim, with Factor =
   the transformed plate's rim mask (234x320 canvas). Result: black bars
   left/right, composite only in a central strip — verified by pixel
   profile (x<210 and x>440 black). The no-rim variant rendered full
   canvas (corners teal), isolating the Mix node as the culprit.
   Industry-standard fix: do the rim as an overlay layer via
   SetAlpha + AlphaOver, not Mix Add with a small Factor. AlphaOver
   keeps the background canvas.

Other checked, NOT the cause in the minimal test: AlphaOver input order
is Background=[0], Foreground=[1], Factor default 1.0 — swapping them
hides the plate behind an opaque background, but the Kaggle report said
both orders gave 0, so order alone was not it. Straight-alpha PNG plate
worked with the default AlphaOver settings in the minimal test.

## Industry-standard fix wired (method only, no proprietary code copied)
- Blender Manual compositor workflow: Render Layers / Image inputs ->
  AlphaOver -> GroupOutput, executed by a real render in background
  mode (`blender -b --python script.py`).
- After Effects / Nuke-style alpha handling as METHOD only: background
  plate, foreground plate with alpha, over operation, separate rim
  layer with its own alpha — rebuilt here with Blender nodes, not
  their code.
- Local route used: Blender 5.2.3 at
  `~/workspace/tools-industry/blender-5.2.3-linux-x64/blender`, Cycles
  CPU (no GPU needed for this fix; Kaggle T4 x2 ~17 hrs remaining and
  Colab free GPU remain the free fallback if a heavier render is ever
  needed — never present a roadblock, find a free way around).

## What was built and viewed
Final folder: `blender-composite-fix-20261031/`
- `cape-jones-dual-light-combined-blender-composite-20261031.png`
  — 640x360, viewed by the builder. Clean apose plate, centred, over a
  Blender Cycles volumetric cyan god-ray base, gold grade on background
  only, cyan back rim as a separate AlphaOver layer. NO PIL composite.
- `volumetric-base-cyan-godrays-20261031.png` — Cycles CPU, 32 samples,
  denoised, volume-scatter cube, cyan Spot back light, warm Point front
  key, dark pillar bars breaking the light into shafts. First render
  had the spot rotated 90° (cone opening upward) and pillars as walls;
  fixed to 180° (spot pointing to camera) and thin vertical bars.
  Denoiser warning `CUEW initialization failed` appears in the log but
  the output is smooth (noise gone, file size fell 476K -> 228K).
- `cape-jones-blender-composite-20261031.blend` — saved node tree.
- `blender_composite_final.py` — the exact script that rendered it.
- Minimal proof in `scratch/`: `minimal-out.png` (plate over a solid
  background through the same AlphaOver path) and `test-no-rim-20261031.png`
  (same composite without the rim layer, used for the rim proof).

## Pixel proof (not a claim, a count)
- Final frame: 640x360 RGBA. Near-white suit pixels: 7,229.
  Purple head pixels: 338. Plate+rim bbox (suit+head): x 257-387, y 61-288
  in the rim-difference test below (suit-only bbox y starts higher due
  to shaft highlights; the rim bbox is the cleaner silhouette measure).
- Rim layer proof: final vs no-rim version, pixels differing by
  Euclidean colour distance >20: **3,948 pixels**, bbox x 253-391,
  y 61-288 — exactly the character silhouette. The rim layer is real
  and present in the Blender output, not painted on afterwards.
- Full canvas: corners (76,122,103), (70,126,102), (55,93,82),
  (73,112,101) — teal volumetric background, no black bars in the
  final version (black bars were the Mix Add bug, fixed and re-rendered).
- PIL was NOT used for the final composite. PIL was used only for
  pixel counting / proof after the Blender render.

## DUAL-LIGHT CORRECTION (Mars, 2026-10-31 15:48 CDT) — logged here
Cyan backlighting / cyan god rays are for when he has **CYAN RIM
lighting combined with the GOLD LUT/overlay** — NOT when he has gold
rim lighting alone. Gold rim alone gets NO cyan backlight.
This final frame IS that combined case only: gold grade on the
background (gold LUT/overlay) + cyan volumetric backlight + cyan back
rim. The earlier dual-light demo image is still good, but it is that
combined case only, not a general rule. A gold-rim-alone version is a
separate shot spec (warm amber rim, no cyan backlight) and is NOT this
file. Do not use this file as proof that cyan backlight belongs on a
gold-rim shot.

## Still owed (not claimed done)
- Gold-rim-alone Blender composite (warm rim, no cyan backlight): 0/1.
- Arms-up reference pose through this same Blender compositor: 0/1
  (this fix used the clean apose plate; the arms-up pose is the next
  plate to run through it).
- Per-shot composites through this stack: 0/30.
- Repo push of this folder (parent's PR route; no commit made here).
- Kaggle/Colab re-run of this exact script on GPU for a higher-sample
  volumetric base is optional, not required — the CPU base already
  renders and composites correctly.

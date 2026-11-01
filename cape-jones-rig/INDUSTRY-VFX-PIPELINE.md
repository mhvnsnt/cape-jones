# Industry VFX pipeline — Cape Jones (2026-10-31, revised)

STOP RULE, from Mars 2026-10-31 13:40-13:43 CDT:
No more hand-drawn PIL shapes as VFX. The flat star / circle / cone sheets are
DRAFT ONLY, 10-20% of what production needs, not production VFX. They look
amateur / robot-made, not authored by a comic / anime / VFX artist.
Do NOT present another PIL-drawn VFX sheet as an upgrade.

## What is locked and good
- Rim light: OUTER ONLY, 2-4px, Add. User: "the rim lighting is way better."
- Inner outline: DO NOT USE. It makes the rim line too thick inside. Reverted
  2026-10-31, marked SUPERSEDED in rim-bleed-glow-library.json.

## What Mars confirmed 2026-10-31 13:43 CDT — internal line lighting
Environmental bleed and environmental lighting must change the LINES INSIDE
the character, not just the rim:
- muscle lines
- suit seams
- cape folds
- face lines
- shadows on / from those lines

That is the missing layer. Rim alone is not line work.

## How internal line lighting is actually done (industry method, not a new outline)
CORRECTION, Mars 2026-10-31 13:44 CDT: do NOT recolor the base art. The
lazy PIL recolor changed too much colour because it changed base pixels.
Industry compositing leaves the original rig untouched and adds lighting
as SEPARATE LAYERS ON TOP, with masks, so the original can be recovered
by turning the layers off:
1. KEEP the original rig untouched as the base layer. No base-pixel recolor.
2. LIGHT LAYER ON TOP: a light-direction gradient layer, Screen/Add, masked
   to the character, brighter on the lit side, fading to the shadow side.
   It sits over muscle lines, suit seams, cape folds and face lines, so
   those lines read lighter on the lit side without their base colour
   being repainted.
3. BLEED LAYER ON TOP: environment colour, Screen at low opacity (research
   recipe: reflected/bounce light Screen ~15-30%, colour sampled from the
   background/sky), masked to an edge band only (character alpha minus
   eroded alpha, blurred), fading inward with a lit-side gradient. Only
   fold/seam lines inside that band pick it up.
4. SHADOW LAYER ON TOP: Multiply layer in a hue-shifted shadow colour
   (cool blue-violet, not black at low opacity), masked to the shadow side,
   plus a separate hard contact shadow strip (few px, darkest at contact)
   on the floor layer under the feet.
Rim stays a separate layer: outer halo outside the silhouette (Add/Screen)
and, where the research calls it line replacement, one crisp line on the
lit-side contour at original weight — never a second thick line inside.
Research note: colour hold / colour trace IS a named paint-stage technique
for lines drawn in colour, but for a finished cutout rig the compositing
rule above is the production route Mars chose, and it is what Blender
will do here.

All four steps run as a node pass (Blender Compositor / Natron / Krita layer
stack), on the character's own lines, never as a newly drawn shape.

## VFX / powers / attacks — industry route, not PIL shapes
Production VFX comes from a real tool, in this order:
1. Blender 5.2.3 LTS (CORRECT production default, per repo
   production/tools/BLENDER-5X-UPGRADE.md, released 2026-10-22, supported
   until July 2028; previous 4.0.2 kept only as fallback) — local install in
   ~/workspace/tools-industry/, VERIFIED 2026-10-31 13:45 CDT:
   `blender --version` = Blender 5.2.3 LTS, build 2026-10-22.
   Blender 4.5.3 was downloaded in error and is NOT the production
   standard — do not use it for production passes.
   Compositor nodes to wire, not draw:
   Glare (fog glow + streaks, threshold-driven, not a drawn halo),
   Lens Distortion / chromatic edge, Color Balance / LUT, Vector Blur for
   smear, volumetric light shafts from a real light + fog volume, not a
   solid cone polygon.
2. Authored VFX reference already on the other branch, to EDIT from, not
   to redraw: characters/sheets/04-action-flight-vfx-reference.jpg —
   Gauntlet Blast Charge, lightning arcs, Energy Beam/Beams, Burst Effects,
   Impact, cape wind physics. Those are authored frames; new VFX frames are
   made by editing / compositing from that reference, via the image-edit
   pipeline (Qwen-Image-Edit / FLUX Kontext on Kaggle GPU, gated on Mars's
   approval for a specific run — no paid run without it).
3. Open-source particle / shader systems, not invented polygons:
   Blender particle / geometry-node sparks and debris, FFmpeg delivery
   (-14 LUFS audio, .cube LUT), RIFE for in-betweening. No other show's
   character / name / logo / dialogue pulled — systems only, per Mars's rule.
4. Deep research (agent 9abe4964, running) on top 2D show compositing,
   colour scripting, LUT/ACES, volumetric, wet surfaces, fog, hard/contact
   shadow, and JoJo non-canonical colour — findings wire into this pipeline
   when they land, they do not replace the tool above.

## Status, honestly, per the percentage rule
- Rim light (outer only): 100% as a spec, production compositing in Blender: 0%
- Internal line lighting: spec 100%, separated line layer + Blender pass: 0%
- Authored VFX (blast / lightning / beam / impact / god ray): draft PIL 10-20%,
  Blender / edited-authored production version: 0%
- Full production VFX to TV quality: NOT 100%. Do not claim it until a Blender
  compositor render, viewed by eye, beats the draft sheets.

## Blender 5.2.3 test — DONE 2026-10-31 13:53 CDT, first pass
File: showcase/blender5-comp-test-1.jpg (1168x784, 121 KB, viewed).
Nodes, Blender 5.2 API (different from 4.x, do not reuse 4.x socket order):
Background image + placed rig (495x675, centred) -> AlphaOver
(Background = inputs[0], Foreground = inputs[1]) -> MixRGB Screen with
light-version image, Fac = rig Alpha x 0.35 (ShaderNodeMath Multiply) ->
Glare Fog Glow, Threshold 0.85, Size 6, Strength 0.25 -> ColorBalance ->
Group Output. System note: headless Blender 5.2 needs libegl1 installed
(apt libegl1, EGL warnings do not stop the render).
Result is clean: rig on night skyline, not washed out. Light layer is
subtle in this first pass; rim/glare strength and per-shot grade are
still to tune. This is a pipeline proof, not a final production shot.
## Next steps, in order
1. Blender test done (above). Next: tune rim/glare, per-shot grade,
   and the layers-on-top line-lighting pass in the same Blender project.
2. Build the separated line layer + light-direction gradient pass in that
   same Blender project, view lit-side vs shadow-side lines.
3. Apply the deep-research findings to both passes, then re-render.
4. Only then push a production VFX batch to the repo, with the draft PIL
   sheets explicitly marked DRAFT, not production.

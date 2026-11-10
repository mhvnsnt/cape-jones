# Color and Lighting Compositing Research — logged 2026-10-31

Artifact page (delivered in chat 2026-10-31): "Color and Lighting Compositing Research"
Slug: color-and-lighting-compositing-research
Status: RESEARCH REFERENCE, not proof production VFX is finished.
This file logs the artifact into the repo record so it is saved and documented
in the same place as the rest of the rig work. The artifact page itself lives
in the chat artifact system; this doc is its repo-side record.

## What it covers (10 sections, from deep research 2026-10-31)
1. Colour script / colour keys: per condition, normal / highlight / shadow triples.
   Pixar-style: 2-3 keys per sequence, not one grade for everything.
2. Rim light: thin and bright on the lit side, colour sampled from the
   environment, Add / Screen / Overlay. On our rig: 2-4px, outer only.
   Thick inner outline is WRONG — it was tried, it thickened the rim, reverted.
3. Environment bleed: light wrap via a dilated-alpha edge band ONLY.
   It does NOT tint the whole suit. Suit stays white, per Mars's original key.
4. Internal line lighting: environmental light DOES change lines INSIDE —
   muscle lines, suit seams, cape folds, face lines — but as separate layers
   ON TOP of the untouched original (Screen/Add for light, Multiply for
   shadow, masked to lit side / edge band), never by recolouring the base art.
   Colour-hold / iro-toresu is a paint-stage line technique, not a reason
   to repaint a finished cutout.
5. Node tools: Nuke Merge, Blender Compositor Glare (Fog Glow / Streaks),
   Harmony Glow, etc. Production default here: Blender 5.2.3 LTS
   (released 2026-10-22, supported until July 2028). Blender 4.5.3 is NOT
   the production standard and must not be used for production passes.
6. LUTs: a 3D LUT is a 33x33x33 = 35,937-point colour remap. It changes
   colour only, no spatial effects. Delivery: Rec.709 gamma 2.4, sRGB 2.2,
   P3, Rec.2100 as applicable. ACES Input -> ACES/ACEScg -> Output.
7. God rays in 2D: painted shafts, Screen/Add ~20%, radial blur from
   crushed brights + fog / dust / occlusion — not flat PIL cones.
8. Wet floor reflection: flipped duplicate ~30% wet / ~50% mirror,
   gradient fade + progressive blur with distance.
9. Fog / aerial perspective: veiling per depth plane, not one flat wash.
10. Shadows: hard cel shadow = drawn hue-shifted shape (cool blue-violet,
    not black); contact shadow = separate few-px darkest Multiply band
    at the contact line, darkest at the feet.

## Standing rules saved from this research
- Never recolour the base art. Light and shadow go on separate layers on top.
- Rim is outer-only, 2-4px. Inner outline = DO NOT USE.
- Bleed is rim / edge-band only, never whole-suit tint.
- VFX hand-drawn in PIL is draft only (10-20% of production need).
  Production VFX is Blender compositor + edited authored VFX, on an
  approved GPU run — not new PIL sheets.
- Per-shot compositing (Natron / Blender, per scene) is still owed.
  This research page does not close that item.

## Related files in this repo batch
- COMPOSITING-LIGHTING-SPEC.md
- COLOR-KEY-VFX-STACK-10.md
- FREE-STACKS-INDUSTRY-STANDARDS.md
- INDUSTRY-VFX-PIPELINE.md
- rim-bleed-glow-library.json (inner outline marked DO NOT USE)
- showcase/luts-30/ (30 templates, 0 final approved — see LUT section)

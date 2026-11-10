# Gold split wire-100 — report, 2026-10-31

Folder: `gold-split-wire100-20261031/`, approval 0/1, no repo push, no existing file overwritten.
Plate: `dual-light-variants-20261031/base-arms-up-transparent-20261031.png`
(APPROVED arms-up plate, untouched). Full 1100x1500 canvas, plate bbox
x222-879 y239-1282, touches_edge=False — no crop window used, per the
no-crop-window rule (figure fits whole, never clipped to a box).

## What was built
Full V5 shot composite through an OPAQUE split in Blender 5.2.3 compositor
only (`build_gold_split.py`, `.blend` saved beside the PNG):
bg (god-ray v2 light) -> ground shadow -> cast shadow -> plate ->
seam-split bleed (gold left / cyan right) -> spill -> OPAQUE split rims
-> cyan-side-only Glare -> output. Seam x=550 (plate centre 550.5,
inside the G7 sweep range 550-650). Old left/right rim masks overlapped
x542-557 (15 px); new masks have ZERO left/right overlap on inner and
outer rings. Split rings alpha 1.0, zero semi-transparent pixels
(outer left 53,735 opaque px, inner left 75,410, outer right 51,627,
inner right 72,490). Gold is composited BEFORE cyan bloom, and the bloom
is masked to x>=550 after the gold rim, so cyan bloom cannot cross the
seam into gold.

## Measured colour (see color-tracking-gold-split-20261031.json)
- input_color gold (255,180,80); input_color cyan (0,200,255).
- NEW Standard: on_screen_color gold median (255,180,80) outer AND inner,
  delta (0,0,0), mean (254.9,180.0,80.0). PRESERVED, inside the ~5/channel
  gate. The 16.41% of gold pixels that are not byte-exact are +-1 channel
  sRGB round-trip rounding only: (255,181,81) 4,374 px, (254,179,79)
  4,258 px, rest <=113 px each. That is not a colour shift.
- Cyan on new Standard: median (3,204,255) outer / (6,204,255) inner vs
  input (0,200,255) — +3/+6 from the cyan-side-only bloom, expected;
  gold side is unaffected because bloom is masked off it.
- Seam check: x=549 median gold (255,180,80), x=550 median cyan
  (36,204,255) — a clean 1-px step at the seam, no mixed band.
- Old L3 V5 on the same opaque-mask regions: gold median (174,147,153)
  outer / (170,146,149) inner. Old gold-preserved V5: (194,148,158) /
  (187,146,152). Both still pinkish on this fair region basis.
- AgX control (same tree, no Glare, view AgX): gold median
  (204,160,107), delta (-51,-20,+27) — reproduces the old pinkish shift.
- ACES 1.3 control: gold median (211,161,69), delta (-44,-19,-11) —
  a creative look, not preservation.
- mix_cause (old): AgX tone mapping + semi-transparent split masks
  (max alpha 0.627) mixing gold over cyan/bg + unmasked Glare.
  mix_cause (new): none for gold; remaining cyan lift is the masked
  cyan-side Glare, by design.

## Honest trade-off, not hidden
Opaque binarised rings are HARDER and WIDER than the old soft blurred
bands. Preservation was bought with a harder rim edge. If Mars wants a
soft edge back, it must come from a soft halo UNDER the opaque ring
(L4 pattern), never from making the split ring itself semi-transparent
again — that re-opens the mix.

## Methods wired — 10 total
VERTICAL (colour pipeline, 6/6 real Blender runs or measurements):
1. OCIO colour management — Blender 5.2.3 default OCIO config, view
   transform set explicitly in the script (Standard / AgX / ACES 1.3),
   look None; sRGB PNG solids in, sRGB PNG out, no double conversion.
2. View-transform handling — Standard main + AgX control + ACES 1.3
   control, all real Blender renders of the same tree, measured above.
3. Bloom/glare separation — Glare branch (threshold 0.80, size 6,
   strength 0.20, L4 gentler settings) masked to the cyan side only,
   after the gold rim. Node names: BloomCyanSideOnly,
   BloomCyanSideOnly_masked, Over_BloomCyanSideOnly.
4. Premultiplied-alpha handling — solids are opaque, SetAlpha sets
   straight alpha from the mask, AlphaOver does the premultiplied
   composite; no mask alpha is multiplied twice (verified: split masks
   have zero semi pixels, so no double-premultiply path exists).
5. Layer order — gold before cyan bloom, in tree order, named in the
   script; cyan bloom is the last over, and only over x>=550.
6. Per-shot colour tracking — color-tracking JSON + shot spec below,
   input / on-screen / mix_cause / delta per region, preserved flag.

HORIZONTAL (adjacent colour tools/methods, 4: 1 real run, 3 mappings):
7. ACES vs Rec.709 finish — REAL Blender run: ACES 1.3 control measured
   above; finish choice for this shot is Rec.709/Standard (preservation),
   ACES is a creative look, not the preservation finish.
8. DaVinci Resolve-style split — METHOD MAPPING, not a Resolve run
   (Resolve not run here): serial node order split-mask -> gold grade
   node -> cyan grade node -> bloom node masked to cyan -> output,
   mapped node-for-node to the Blender tree in the script header.
9. After Effects-style split layers — METHOD EQUIVALENT, not an AE run:
   two precomp layers (gold-left, cyan-right) with seam track mattes =
   the two opaque rim branches + seam masks in this tree.
10. Natron / OpenColorIO split — METHOD MAPPING, not a Natron run:
    Natron OCIOColorSpace + Merge node graph equivalent; Blender uses
    the same OCIO library, which is why the view-transform controls
    above are the real evidence for this method.
Counts: real tool runs 7/10 (6 vertical + ACES), method mappings 3/10,
labelled as such. No vendor tool is claimed to have run when it did not.

## Still owed
- Mars approval 0/1 (this composite, the harder rim trade-off, and the
  seam through the face at x=550).
- Soft-halo-under-opaque-ring variant if Mars wants the soft edge back
  (not built; would be a new variant, not an edit of this file).
- Per-shot application to the other 29 shots (this is 1 shot, arms-up).
- No repo push made.

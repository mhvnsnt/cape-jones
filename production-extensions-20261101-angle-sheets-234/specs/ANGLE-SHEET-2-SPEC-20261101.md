# Angle Sheet 2 — Bird's-Eye (+45° down) — SPEC, 2026-11-01

Status: SPEC + DERIVED PARTS-LAYOUT ONLY. No native bird's-eye sheet exists.
The assembly `assemblies/Angle_Sheet_2_BirdsEye_DERIVED_ASSEMBLY.png`
(1200x1400, grey #808080) is an exploded parts-layout in figure order,
NOT a posed figure: gaps between parts are intentional so each part stays
readable, because the source slices are disconnected and no connecting
art (shoulders-to-torso seam, hip joints, cape top) was invented to join them.
A connected posed bird's-eye figure is still owed and needs new art.

## Camera / staging rule
- Camera 45° above, looking down. Near = head/shoulders (largest, 1.0x);
  far = feet (smallest, 0.7x). Vertical compression increases down the body:
  torso 1.05x wide, thighs 0.70x tall, shins 0.60x tall, soles 0.70x.
- Ground shadow ellipse under the feet (only invented element: a plain
  ellipse, no character art).
- Layer order top-to-bottom: Head, Torso, Pelvis, Arms, Legs, Soles.
  Nothing overlaps the head except nothing; the torso's neck disc sits
  below the head in the layout (it is the Torso_LeanForward donor's own disc).

## Piece table (donor -> sheet-2 use)
| Sheet-2 piece | Donor (existing slice) | Transform | Status |
|---|---|---|---|
| Head_BirdsEye | Head_Front | 0.85x | DERIVED-SCALE (layout only) |
| Torso_BirdsEye | Torso_LeanForward | 1.05x | DERIVED-SCALE — this donor already reads top-down (neck disc on top), the closest existing torso to a bird's-eye view |
| Pelvis_BirdsEye | Pelvis_Whole | 0.95x | DERIVED-SCALE |
| UpperArm_BirdsEye (L/R) | UpperArm_Z_Short (this job) | as built | DERIVED-WARP |
| Hand_BirdsEye (L/R) | Hand_Fist | 0.70x | DERIVED-SCALE |
| Thigh_BirdsEye (L/R) | Thigh_L, trapezoid 1.0->0.85, height 0.70, then 0.9x | DERIVED-WARP |
| Shin_BirdsEye (L/R) | Shin_L | x1.0 / y0.60 | DERIVED-WARP |
| Sole_BirdsEye (L/R) | Sole_Boot_Flat_L | 0.70x | DERIVED-SCALE |

## Still owed as native art (do not fake with warps)
- True top of cowl/head (crown, no face), top of shoulders/cape, foreshortened
  torso seen from above (chest plane hidden, back/shoulders dominant).
- Feet seen from above (toes pointing down-screen, not sole-flat). The sole
  pieces in the layout are sole-to-camera swaps, not top-of-foot art.
- Any cape: no cape-top drawing exists in the sheets at all.

## Approval
0/1. Mars approval required before any native sheet is drawn or any layout
is used as a posed figure.

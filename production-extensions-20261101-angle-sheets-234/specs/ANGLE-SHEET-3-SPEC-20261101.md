# Angle Sheet 3 — Worm's-Eye (-45° up, heroic) — SPEC, 2026-11-01

Status: SPEC + DERIVED PARTS-LAYOUT ONLY. No native worm's-eye sheet exists.
The assembly `assemblies/Angle_Sheet_3_WormsEye_DERIVED_ASSEMBLY.png`
(1200x1600, grey #808080) is an exploded parts-layout in figure order,
NOT a posed figure (see Sheet-2 spec for why gaps are intentional).
A connected posed worm's-eye figure is still owed and needs new art.

## Camera / staging rule
- Camera 45° below, looking up (heroic). Near = boots/legs (largest, 1.4x);
  far = head (smallest, 0.80x). Vertical stretch increases up the body:
  thighs y1.20, torso y1.25, to sell height.
- Layer order: boots foreground (drawn first in layout order, largest),
  then thighs, pelvis, torso, head last/smallest at top.
- Reaching arm rule (Sheet-1 spec, carried over): toward camera = Hand top,
  Forearm_Gauntlet_AimingAtLens under it — the near arm in the layout uses
  this job's aiming composite at 1.10x; the far arm is a plain 0.70x fist.

## Piece table (donor -> sheet-3 use)
| Sheet-3 piece | Donor (existing slice) | Transform | Status |
|---|---|---|---|
| Boot_WormsEye (L/R) | Boot | 1.40x | DERIVED-SCALE (foreground hero boots) |
| Thigh_WormsEye (L/R) | Thigh_L | x1.05 / y1.20 | DERIVED-STRETCH |
| Pelvis_WormsEye | Pelvis_Whole | 1.05x | DERIVED-SCALE |
| Torso_WormsEye | Torso_LeanBack | x1.0 / y1.25 | DERIVED-STRETCH (side-lean torso stretched tall) |
| Head_WormsEye | Head_Front | 0.80x | DERIVED-SCALE (small/far) |
| Arm_Near_WormsEye | Forearm_Gauntlet_AimingAtLens (this job) | 1.10x | DERIVED-COMPOSITE |
| Hand_Far_WormsEye | Hand_Fist | 0.70x | DERIVED-SCALE |

## Still owed as native art (do not fake with warps)
- True jaw underside / nostril / cowl-from-below head (this is Head_TiltUp_Z,
  also spec-only — see Sheet-1 Z status). Scaling Head_Front down is NOT a
  worm's-eye head; it keeps a frontal face.
- True boot soles from below at heroic scale (the Boot donor is a front boot,
  not a sole view; the sole swaps are flat/angled, not from-below hero soles).
- Groin/brief underside at heroic scale beyond Pelvis_UnderView (that piece
  is reissued as Pelvis_Whole_TiltBack; it is one static underside, not a
  worm's-eye pelvis in pose).
- Any cape from below.

## Approval
0/1. Mars approval required before any native sheet is drawn or any layout
is used as a posed figure.

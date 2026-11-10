# Angle Sheet 4 — 3/4 Diagonal Deep-Perspective Lunge — SPEC, 2026-11-01

Status: SPEC + DERIVED PARTS-LAYOUT ONLY. No native diagonal-lunge sheet exists.
The assembly `assemblies/Angle_Sheet_4_DiagonalLunge_DERIVED_ASSEMBLY.png`
(1400x1200, grey #808080) is an exploded parts-layout in near-to-far order,
NOT a posed figure (see Sheet-2 spec for why gaps are intentional).
A connected posed lunge is still owed and needs new art.

## Camera / staging rule
- Diagonal: figure runs top-left (far) to bottom-right (near). Depth scale:
  near limbs 1.20-1.30x, torso 1.05x, far limbs 0.70x.
- Rotation (2D only, no new perspective drawn): torso -14°, head -10°.
  Rotation of flat art is NOT true diagonal perspective; it only suggests it.
- Layer order (painter's order in the layout): far leg, torso, head, far hand,
  near thigh, near shin, near kick (foreground, largest, drawn last),
  near aiming arm (foreground-left, drawn last with the kick).
- Ground shadow ellipse under the lunge.

## Piece table (donor -> sheet-4 use)
| Sheet-4 piece | Donor (existing slice) | Transform | Status |
|---|---|---|---|
| Torso_Lunge | Torso_LeanForward | rotate -14°, 1.05x | DERIVED-ROTATE/SCALE |
| Head_Lunge | Head_Front | rotate -10°, 0.95x | DERIVED-ROTATE/SCALE |
| Leg_Far_Lunge (thigh+boot) | Thigh_L 0.70x, Boot 0.70x | DERIVED-SCALE |
| Thigh_Near_Lunge | Thigh_KneeForward_Z (this job) | 1.30x | DERIVED-WARP+SCALE |
| Shin_Near_Lunge | Shin_Boot_Z_Compressed (this job) | 1.20x | DERIVED-WARP+SCALE |
| Foot_Kick_Near_Lunge | Foot_Kick_Z (this job) | as built (1.5x sole) | DERIVED-SCALE, foreground |
| Arm_Near_Lunge | Forearm_Gauntlet_AimingAtLens (this job) | 1.20x | DERIVED-COMPOSITE, foreground-left |
| Hand_Far_Lunge | Hand_Fist | 0.70x | DERIVED-SCALE |

## Still owed as native art (do not fake with warps)
- True diagonal torso (twisted chest, one shoulder forward, cape diagonal):
  rotating Torso_LeanForward does not twist it.
- True diagonal lunge legs (one leg extended with foreshortened knee, one
  leg trailing with foot planted at an angle): the near leg here is a warp
  of a straight thigh + a sole swap, not a lunge drawing.
- True cape in diagonal motion, true lunge hands (one reaching, one back).
- A connected figure: joining far/near groups into one body needs new
  hip/shoulder/cape art.

## Approval
0/1. Mars approval required before any native sheet is drawn or any layout
is used as a posed figure.

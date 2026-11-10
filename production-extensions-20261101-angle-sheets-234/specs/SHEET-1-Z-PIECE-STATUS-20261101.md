# Sheet-1 Z pieces — final status per item, 2026-11-01

Source spec: `production-extensions-20261101/angle-sheet1/ANGLE-SHEET-1-SPEC-20261101.md`
plus its addendum. "Generated" below always means derived from existing art
by scale/warp/composite — never newly drawn character art. The distinction
matters: a derived piece is a usable swap; it is not evidence that a native
Z drawing exists.

## Generated in this job (pieces/)
| Piece | Output size | Method | Limit |
|---|---|---|---|
| Hand_Fist_Z_Close | 382x298 | Hand_Fist 1.5x | Same drawing, larger. No new knuckle/close detail. |
| Hand_Palm_Z_Close | 502x364 | Hand_OpenPalm 1.5x | Same drawing, larger. Spec's 1.5x requirement met exactly. |
| UpperArm_Z_Short | 170x128 | UpperArm_L x1.30/y0.55 | Squash only; no new spherical deltoid drawn. |
| Forearm_Gauntlet_AimingAtLens | 350x191 | Gauntlet_L x0.85/y1.40 + Hand_Fist 1.0x, 115px overlap, fist foreground | Composite; no new cuff ring or tapering pad drawn. Layer rule: Hand top, gauntlet under (reaching toward camera). |
| Thigh_KneeForward_Z | 234x208 | Thigh_L trapezoid warp hip 0.78x -> knee 1.38x, height 0.88x | Warp only; knee ball is the source art's, widened. Source thigh is diagonal, so the warp follows its orientation (knee end = bottom-left ball). |
| Shin_Boot_Z_Compressed | 538x167 | Shin_Boot_Cut_S1 x1.12/y0.62 | Squash only; V-trim is the source's, no new deep-U trim drawn. |
| Foot_Kick_Z | 531x436 | Boot_Angled_Sole_L 1.5x | Sole-to-camera swap (same drawing used for the 20261101 kick at 1.2x). NOT a native toe-first drawing. |

## Reissued / already existing (pieces/, byte-identical copies)
| Piece | Fact |
|---|---|
| Pelvis_Whole_TiltBack | Copy of Pelvis_UnderView (263x212). The underside pelvis (dome + two leg sockets) matches the spec's TiltBack description (groin arch, deep hip sockets). Alias note: parallel spec called this drawing Pelvis_Top_Dome — same drawing, two names. Reissue, not new art. |
| Torso_LeanBack | Copy of the existing Torso_LeanBack slice (325x328), verified visually: side-leaning torso with abs, distinct from Torso_LeanForward. CORRECTION to the Sheet-1 spec: this item was listed as owed, but the second slicing pass had already sliced it. The parallel spec's "Torso_Front" for the same bbox is a duplicate of Torso_LeanForward (visually identical drawing, grey vs black background removal), not this drawing. Mars adjudication on the naming is still open, but the drawing itself exists. |

## Spec-only — still owed, no PNG, and why no transform was used
| Piece | What new art must show | Why a transform was refused |
|---|---|---|
| Head_TiltDown_Z | Cowl dominating from above, jaw tucked, forward-charging glare | Squashing Head_Front cannot create a cowl top or a tucked jaw; it would mislabel a distortion as a new view. |
| Head_TiltUp_Z | Underside of jaw, cowl compressed from below | Head_ThreeQuarter is chin-raised with a still-frontal face — it is NOT an underside view and must not be relabelled. Stretching Head_Front cannot create a jaw underside. |

## Not done in this job (explicitly excluded by the task)
- No flex cutout still over the existing flex animation (Mars cancelled it).
- No 6-step spin v2 (the bust is final at 7 segments; the existing flex spin
  is a separate 3-step loop and was not touched).
- No repo PR, no deletions, original uploads untouched (hashes verified
  before and after: see REPORT).
- Layer-flip rule from the Sheet-1 spec is carried forward in the specs
  (toward camera: Hand > Gauntlet > UpperArm; away: reverse) but no Blender
  re-wire was done in this job.

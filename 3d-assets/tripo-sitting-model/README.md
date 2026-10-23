# Tripo Sitting Model Breakdown

Owner-made Tripo model of Cape Jones sitting in the chair ("superhero throne pose",
2026-10-18). Source: https://studio.tripo3d.ai/3d-model/22cdbc99-b2ba-4233-9da9-2ac4dc48d416
(18MB, pulled via tripo-pull.py — owner's lane only).

## The statue problem — SOLVED by separation, NOT by rigging

The model is ONE fused mesh (314,468 verts, 1 primitive). Separated into 6 pieces by
connected-component island assignment (v5: 2D white-suit mask voting + spatial refinement;
his mesh 100% intact, chair lost zero polys; all 314,468 verts accounted for).

**Rig verdict: POSE REFERENCE ONLY — do NOT rig the separated him.**
- Topology is triangle soup: 61k boundary edges (7% open holes/cracks), no edge loops at
  knees/elbows → poor deformation exactly where sitting bends.
- Pose is baked in (knees ~90°, head bowed); separation from the throne cuts contact patches.
- Proportions don't match canon (see below) — even a perfect rig wouldn't interchange.

## Scale check vs 0.925m canon — NOT at canon scale

Tripo's proportions are internally inconsistent; no single scale makes him 0.925m:

| Segment | Tripo | Canon 0.925m | Ratio |
|---|---|---|---|
| Head (chin→crown) | ~0.105 | 0.123 | 0.85 |
| Shin (knee→ankle) | ~0.23 | 0.228 | ~1.00 |
| Thigh (hip→knee) | ~0.15 | 0.227 | 0.66 |
| Foot | ~0.12 | 0.139 | 0.86 |
| Torso (butt→neck) | ~0.14 | ~0.28 | ~0.50 |
| Shoulder width | ~0.25 | ~0.23 | ~1.09 |

Best-fit uniform scale ≈ **1.15×** (standing-equivalent ~0.80–0.85m as modeled).
**Use as joint-angle/pose guide only** (overlay at 1.15× on the canon rig), not a dimensional template.

## Resize — owner's specs vs measured canon

Owner's eyeballed multipliers (from the perspective-warped Tripo preview) overshoot.
Both versions are delivered; **canon-matched is recommended**:

| Piece | Owner spec | Result | Canon-matched | Result |
|---|---|---|---|---|
| Lamp | ×10 | 1.82m, dips below ground | ×4.745 | 0.86m = canon floor lamp |
| Desk (side table) | ×5 | 2.70m monstrosity | ×1.02 | 0.55m = canon side table |
| Mug | ×5 | 0.86m novelty mug | ×0.58 | 0.10m = canon mug |

The Tripo pieces were never as small as they looked in the preview — the "desk" was
already 0.54m (canon: 0.55m) and the mug was already 0.17m (canon: 0.10m).

## Window placement

Window piece moved to the wall: glTF (3.5, 1.6, −1.5) = Blender (3.5, 1.5, 1.6),
the canon `window_unit` center on the right window wall. Piece is 0.40×0.33 (decorative;
canon opening is 1.4×1.1).

## Orientation / grounding

- Model arrived centered at origin (z −0.49..0.49), not grounded. Re-ground: +0.426 on
  glTF-Y (= +0.426 on Blender-Z after import).
- He faces +Z (glTF) = −Y (Blender) — matches the canon rig's −Y facing. No yaw fix needed.
- His feet sit ~10mm above ground after re-ground (minor pose artifact).

## Folders

- `pieces/` — the 6 separated originals + per-piece manifests (bbox, method, cut notes).
- `owner-spec/` — owner's literal ×10/×5 + grounded him/chair + window on wall.
- `canon-matched/` — measured versions matching locked room canon (recommended).
- `analysis/` — point-cloud projection renders + scale comparison (viewed, own-eyes).

## Open flags

- Bone-count discrepancy: this task's brief said 94-bone rig; the sitting-pose lane doc
  says 85-bone W5r rig. Resolve before overlay work.
- When `him.glb` is used as pose reference, re-verify the 1.15× suggestion against the
  separated mesh (analysis used numerical isolation, ±0.01–0.02 on landmarks).

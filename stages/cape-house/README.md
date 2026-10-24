# stages/cape-house — Cape's living room as a WH stage

## living-room.glb

Exported from `3d-assets/living_room.blend` (2026-10-23) via
`tools/show-retarget/export_stage.py` ( Blender headless; the .blend is never
saved). The .blend is the source of truth — this GLB is the working copy.

- Contents: the full room (furniture, CRT TV, LED strips with violet
  emission, lamps, rug, bookcase, mug) WITHOUT the Cape Jones character
  (CapeJones_Rig / Body / Cape are show objects, not stage geometry).
- Lights: exported (RoomLight violet point + Sun fill) — matches the canon
  look in `3d-assets/living-room/SCENE-CANON.md` (coral-pink furniture, warm
  oak, violet LED wash `#731AE5`).
- Scene canon (colors, palette, furniture) is LOCKED per SCENE-CANON.md —
  owner sign-off required for changes.

## Canon note

This is the test-ground copy. The canonical stage entry for the game lives
in western-heart (`stages/cape-house/STAGE-SPEC.md`); wiring it into the
game's stage select is a separate claimed lane — this repo does not touch
`game/` in western-heart.

Per SCENE-CANON.md: the recliner stays empty until the light-flicker gag rig
lands — proofs never place the character in the recliner.

# Sitting Fix — Full Canon Scene Pass (2026-10-19)

Owner's punch list from PR #159 review — all addressed:

## Fixed
1. **TOO HIGH OFF SEAT** — Root cause: mocap lane placed by bone, not mesh.
   Fixed by measuring the actual chair seat (center (2.990, 2.067), top z=0.370)
   and solving pelvis placement so the BUTT MESH (not the bone) contacts the seat.
   Butt min_z = 0.3700 verified numerically.
2. **WRONG ORIENTATION** — Root cause: retarget used -90° Z rotation (faced +X/wall).
   Fixed to +90° (faces -X/room, back toward +X wall). Verified visually.
3. **MESH DEFORMATION** — Applied PR #158 wave2 correctives (10 zones: shoulders,
   hips, knees, ankles, spine) via apply_wave2.py. Files copied from
   lane/deform-wave2-20261018 (not merged).
4. **TEXTURES + LIGHTING** — Rendered in the FULL living_room.blend (not a test scene).
   Full Tripo PBR textures (4K color/ORM/normal), canon violet LED lighting.
   Cycles, not Workbench. He has his colors.
5. **TRIANGULAR TEARING** — Investigated: geometry is CLEAN (verified via clay
   override render). The "tearing" was a texture artifact + over-rotated bones.
   Fixed 23 bones with >180° quaternion rotations (e.g. upperarm_fk_L at 289°)
   by flipping to shortest-path equivalents.

## Known issues (noted, not hidden)
- **Built-in cape**: The body mesh includes a black cape (canon) that bunches/spikes
  when posed. The separate CapeJones_Cape cloth object was removed from the working
  blend for this proof. The built-in cape needs a dedicated smoothing pass.
- **Feet dangle**: Chair seat (0.37m) is high for a 0.925m character; feet don't
  reach the floor in this mocap pose. Ergonomic, not a bug.
- **Upright pose**: Mocap frame 41 is a neutral seated pose; he's not leaning back
  against the backrest. The motion is natural human sitting.

## Files
- `final_front.png`, `final_threeq.png` — proof stills (viewed with own eyes)
- `sitcanon_retarget.py` — mocap retarget + measured placement pipeline
- `fix_twist_fast.py` — quaternion over-rotation fixer

## Verification
- Butt mesh min_z = 0.3700 (seat top) — numeric
- Root at seat center (2.990, 2.067) — numeric
- Facing -X (back to wall) — visual
- All stills viewed with own eyes before PR

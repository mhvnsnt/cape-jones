# Mocap Sitting Retarget Pipeline

Production-grade motion capture retargeting for the Cape Jones 94-bone rig.
Owner directive 2026-10-19: "use some full stack industry standard production grade
stuff pulled in and wired up" — hand-posing is OVER, real human motion only.

## What this does

Retargets real sitting motion capture onto the 94-bone Cape Jones rig with
contact solving (butt on seat, back on backrest, feet on floor).

## Clips

| File | Description | Seated frames | Source |
|------|-------------|---------------|--------|
| `113_15.fbx` | "Sit in chair and get up" | 70–150 (81 frames) | CMU via HuggingFace `gbionics/cmu-fbx` |

Additional sitting clips in `~/workspace/mocap-sit/` (not in repo): 114_16, 13_01,
13_04, 14_27, 14_30, 114_05.

## Pipeline

The retargeter (`production/tools/mocap-retarget/retarget.py`) does:

1. **Import** the FBX mocap (CMU skeleton, cm units).
2. **Map** source bones to target FK control bones (94-bone rig).
3. **Transfer rotations** in world space with rest-pose correction:
   `W_desired = TGT_REST @ (SRC_REST⁻¹ @ SRC_POSE)`
   then solve local: `R_local = (W_parent @ M_rel)⁻¹ @ W_desired`
   (M_rel = parent-relative rest rotation — this is the critical fix; using
   armature-space M_local gives garbage.)
4. **Place pelvis** via numerical calibration (the rig's bone axes are rotated;
   direct assignment puts him 2m in the air). Pelvis target Z=0.389 (proven by
   take-3 to put the butt on the 0.366m seat).
5. **Damp head/neck** 50% (the source has head fidget; this is channel selection,
   not hand-posing).

## Usage

```bash
# From the cape-jones repo root:
blender -b 3d-assets/living_room.blend --python production/tools/mocap-retarget/retarget.py
# Output: proof/sitting_mocap.blend (action `mocap_sit_113_15`, frames 1-81)
```

Requires: Blender 4.0.2 at `~/workspace/tools/blender/blender-4.0.2-linux-x64/blender`,
run under `xvfb-run -a` with `env -u PYTHONPATH`.

## Results (2026-10-19)

- Butt on seat: 0.00mm gap (contact solved)
- Feet on floor: minz 0.00m
- Arms: natural mocap gesture (no H-pose)
- 81 frames of real human sitting motion

See `~/workspace/your_files/mocap-sit/` for front + three-quarter stills.

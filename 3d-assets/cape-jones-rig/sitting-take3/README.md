# Sitting Redo — Take 3 (2026-10-18)

Owner rejected v5 (PR #156): "robot stance, H-stance — elbows bend but not
shoulders/fingers/wrists, no waist/hip bend, knees not bent enough, pelvis not
lowered." Take 3 addresses every point.

## What changed vs v5

1. **Action-clearing fix (the big one):** the living room scene has
   `pose_sit_normal` applied to the rig. An applied action OVERWRITES direct
   bone rotation sets on evaluation. v5's script set bones directly WITHOUT
   clearing the action — so the old stiff pose kept winning. Take 3 clears
   `rig.animation_data.action` before posing.

2. **FK spine controls:** the 94-bone rig's deform spine bones (spine_1..4,
   chest) are driven by COPY_ROTATION constraints from the FK controls
   (spine_fk_1..4, chest_fk). Posing the deform bones does nothing. Take 3
   poses the FK controls. Probe-verified: spine_fk -X = recline, +X = lean.

3. **Probe-verified arm axes:** numeric bone-position probes (no rendering)
   found the exact quaternions for the crossed arm:
   upperarm_fk_R x=-115° z=25° + forearm -55° = hand across lower chest.

4. **Bend everything:** shoulders (clavicles), elbows, wrists, fingers
   (relaxed curl on all joints), waist/hips (FK spine + pelvis tilt),
   knees (70-90°), ankles. Pelvis drops into the seat (pelvis_z=0.389).

## Poses (all own-eyes verified, front + three-quarter stills)

1. **lounge** (hero, Tripo reference match): leaning BACK into the chair,
   pelvis sunk, right arm CROSSED over torso, knees ~90°, feet forward,
   shoulders relaxed. Matches the owner's Tripo sitting model pose.
2. **leg_folded**: right knee out to the side, lower leg folded back under.
3. **lean_forward**: deep pensive forward pitch, head bowed, elbows on knees.
4. **shrug**: sitting back, both arms up/out, palms up.

## Files
- `pose_take3.py` — data-driven pose script (poses as bone-local quats)
- `*_front.png` / `*_threeq.png` — proof stills (480x270 iteration renders)

## Notes
- Iteration renders are 480x270 @ 4 samples with volumetrics off (memory).
  Final proofs should re-render at full quality.
- Cape hidden in proofs (cape lane owns drape).
- pelvis_z=0.389 vs seat ~0.36 — sunk in, not perching.

# Sitting Redo — him actually SITTING in the chair (2026-10-18)

**Replaces the rejected PR #138 turntables** (he was standing/floating in gray space).
Own-eyes verified: all 5 poses show him genuinely sitting IN the coral recliner,
in the living room scene.

## Poses (all rendered front + three-quarter, + turntable MP4s)
1. `pose_sit_normal` — upright sitting, hands on thighs. Matches the owner's
   Tripo sitting reference 1:1 (verified by automated geometric pose analysis —
   see TRIPO-POSE-ANALYSIS.md).
2. `pose_sit_leg_folded` — one leg folded under.
3. `pose_sit_lean_forward` — pensive lean forward, head bowed, hand on knee.
4. `pose_sit_recline` — leaning back relaxed.
5. `pose_sit_shrug` — sitting with arms up in a shrug gesture.

## Rig
- 94-bone rig (spine rebuild PR #127 took it from 85 → 94). The 85-bone "W5r"
  references in older docs are outdated.
- Built from measured sit-targets (butt at (3.12,2.067,0.368), seat top z~0.362).

## Tripo reference note
The owner's Tripo sitting model was scanned automatically (MiniBatchKMeans
clustering on the posed mesh). Its pose = `pose_sit_normal` above, so the
"100% replicate" is already achieved. The Tripo mesh itself is NOT rigged
(triangle soup, baked pose, 15-24% undersized, distorted proportions).

## Files
- `sitting_pose_library_fixed.blend` — the pose library
- `pose_sit_*_{front,threeq}.png` — proof stills (own-eyes verified)
- `pose_sit_*_turntable.mp4` — turntable videos
- `TRIPO-POSE-ANALYSIS.md` — automated pose-extraction analysis

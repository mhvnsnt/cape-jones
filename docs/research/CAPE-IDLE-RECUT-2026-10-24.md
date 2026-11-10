# Cape idle re-cut — diagnosis and fix (2026-10-24)

## What was wrong
The show idle (`anims/show/cape-jones/idle.glb`, baked 2026-10-23 from
CMU `140_06.bvh` frames 200–680) played as a deep lean/crouch, not a
neutral idle. The owner flagged it: the frame did not read as an idle.

## Measured evidence (Blender, plain/deform chain)
The body mesh is skinned ONLY to the plain chain (pelvis, spine_1–4,
chest, neck, head, arms, thigh/shin/foot). FK/IK chains carry no skin
weights; measuring them misleads.

Old clip, steady loop (frames 24–96):
- Torso pitch ~32–34° forward, plain knee flexion ~64–76°,
  pelvis height constant (in-place retarget, no root translation).

Source motion (`140_06.bvh`, labelled "Idle"):
- Frames 1–201: torso pitch 0.8–3.6°, knee 0–17°, hips steady → true
  neutral idle, upright.
- Frames 293–3563: torso pitch 21–31°, knees 48–80°, hips dropped →
  the subject crouches and NEVER stands back up for the rest of the
  trial. The trial is not a neutral idle beyond frame ~200.

Conclusion: the clip range was wrong. The retarget did not invent the
lean; it faithfully transferred a crouch. Retarget math
(`R_target_pose = (R_src_pose @ R_src_rest^-1) @ R_target_rest`), the
bone map, and the skeleton all check out clean. In-place retargeting
(no hips drop) makes the crouch read stranger (hips at full height
while torso pitches 33° and knees bend 70°+).

## Fix (re-cut, not re-rig)
Re-cut from the upright portion with the same retarget script
(`tools/show-retarget/retarget_idle_cape.py`, skip 0, step 4,
50 frames, source frames 1–197). Measured on the plain chain:
- Frame 1: torso pitch 2.0°, knee 20.6°
- Frame 25: torso pitch 2.5°, knee 18.7°
- Frame 50: torso pitch 3.5°, knee 19.4°
- Pelvis height constant; loop start/end within 1.5° pitch and 1.2°
  knee — minimal pop. The ~20° knee baseline is the plain chain's
  bind-pose offset, constant across frames, not motion.
Render proof: `anims/show/cape-jones/proof/upright-frame25.png`
(living-room, cycles_show, 1080p, frame 25 of the re-cut) — Cape stands
upright, torso vertical, legs straight, arms relaxed.

## Why UniRig is not the fix here
UniRig (MIT auto-rigger) generates a new skeleton + skinning weights;
it does not fix a baked clip by itself. Re-rigging and re-retargeting
the same crouching source range would reproduce the same crouch on a
new skeleton. UniRig remains an option for a genuinely untrustworthy
skeleton — that is a separate question from this clip, and it is being
pursued separately for the stance/rig work.

## Separate issue: old clip frame-1 crumple
The old clip's first rendered frame looked crumpled/twisted. The source
at frame 201 is upright, so that is not the loop lean: the old clip's
first chest/spine quaternion keys flip wildly between keys, so
per-component interpolation twists the torso at the very start. Fix by
starting a usable clip after the first keys or by fixing quaternion
continuity on bake. The re-cut starts from source frame 1 and does not
carry that artifact in its measured frames.

## Files changed in this PR
- `anims/show/cape-jones/idle.glb` — replaced (old 145,732 bytes,
  crouching cut) with the upright re-cut (116,956 bytes).
- `anims/show/cape-jones/SOURCES.md` — idle row + re-cut note updated.
- `anims/show/cape-jones/proof/upright-frame25.png` — render proof.

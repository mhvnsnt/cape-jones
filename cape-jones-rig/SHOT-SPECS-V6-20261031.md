# Shot specs — v6, 2026-10-31 (supersedes v5 shot-spec.yaml for rig version)

24 fps. Normal on 2s = 12 drawings/sec. Fast snaps on 1s = 24/sec. Holds 6-24 frames.
Rig: joint-locked v6 (Head 550,250 / Neck 550,360 / Torso 550,400 / Pelvis 550,680).
Labels: ARM 1 = our left, ARM 2 = our right, LEG 1 = our left, LEG 2 = our right.
QC: PENDING until Mars looks at the frames himself. No shot is called done before that.

## Per-shot specs (this is what "per-shot specs" means — one spec per shot, not just a clip list)
- Punch: windup F1 hold 6, extend-snap F7 hold 2, impact-hold F9 hold 12, recover F21 hold 6.
  Background: any, LUT: per scene key, Effects: impact energy + gauntlet glow, Audio: impact cue.
  BLOCKER: Arm 2 elbow bug in impact frame — joint fix required before this shot locks.
- Walk: contact LEG1 F1 hold 12, passing F13 hold 12, contact LEG2 F25 hold 12, passing F37 hold 12, loop.
  Background: street / town, LUT: per scene, Effects: none, Audio: footstep cue.
- Flex / power pose: apose F1 hold 6, flex-hold F7 hold 24, apose F31 hold 6.
  Background: any, LUT: per scene, Effects: none, Audio: none.
- Jump / landing: crouch F1 hold 6, takeoff F7 hold 2, tuck F13 hold 12, land F25 hold 6.
  Background: skyline / rooftop, LUT: per scene, Effects: cape wind, Audio: landing cue.
  BLOCKER: knee square-crop in tuck — joint fix required before this shot locks.
- Dance: dance-a F1 hold 12, dance-b F13 hold 12, dance-a repeat F25 hold 12, loop.
- Flying: hovering F1 hold 12, soaring-arms-out F13 hold 12, diving-arms-up F25 hold 12, hovering F37 hold 12.
  MISSING: forward-flight fists-toward-camera — needs a foreshortened forearm piece, not faked.
- Dialogue: NO shot yet — needs viseme pieces (0/14 sliced) + eye strips (0/8). Spec template only.
- Lounge / desk: seated pose, background: room / desk stand-in (see layout passes).
  Final painted desk background still owed.

## What a shot spec is NOT
It is not the clip JSON alone. Clip JSON = timing + angles. Shot spec = clip + camera +
background + LUT + effects + audio + QC status, per shot, so Animate / Blender can build it
without guessing. That is why the old list counted 0 per-shot specs even though clip JSONs existed.

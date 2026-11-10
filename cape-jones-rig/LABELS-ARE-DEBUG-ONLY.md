# LABELS ARE DEBUG ONLY — Mars, 2026-10-31 14:51 CDT

The little red numbered circles — ARM 1, ARM 2, LEG 1, LEG 2 — are DEBUG
TOOL pieces. They are NOT part of the scene, NOT part of the character,
and they are NEVER to be rim-lit, graded, composited, or given effects.

## The rule, going forward
- Final shots, lighting passes, LUT grades, effects, and composites use
  CLEAN builds only: joint_locked_rig_v7c.py with labels=False.
- Clean files live in reposes-v7c-clean/ (6/6 poses, 0 red label pixels,
  verified by pixel count) and rig-apose-v7c-clean-transparent.png.
- apply_lighting_levels.py REFUSES any plate with >100 pure-red label
  pixels. Proof: the old rig-apose-v6-transparent.png (8,425 red pixels)
  is refused with that exact message. No future pass can silently rim-light labels.
- Older labelled images (reposes-v7c/, clips-v7c/ with red circles, the
  earlier lighting-levels-0-5/ run on the labelled plate) are DEBUG ONLY.
  They are not final shots, and they are not to be used as shot plates.
- What stays: the white elbow/knee joint balls. Those are character joints
  (circle-masked caps from the rig pieces), not debug labels. Rim light
  follows the character silhouette, which includes those joints — it does
  NOT follow, circle, or highlight any red numbered label.
- Clean lighting re-run: showcase/lighting-levels-0-5-clean/ — 12 level
  images + 10 passes, 22/22 files, 0 red label pixels in every output.
  Rim in level-2-colored is on the silhouette only.

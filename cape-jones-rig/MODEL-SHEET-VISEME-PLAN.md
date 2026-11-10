# Clean model sheets + viseme chart — STARTED, spec first, 2026-10-31
Decision: yes, model sheets + viseme chart are priority 1 and 2, in that order.
Locked to: joint-locked v6 DEFAULT LOCK (not the old v8 T-pose-only lock).
That means every new angle must match v6 joints, proportions, and pieces — not a new drawing that drifts.

## 1. Clean multi-angle model sheets — status with percentages
Angles needed, 5 total:
- Front — HAVE, v6 rig, Head_Front + Torso_Chest + full limbs
- 3/4 — NEED TO MAKE, 0/1. Front pieces cannot be rotated into a true 3/4 — that needs a 3/4 torso/head/limb set, not a flat rotation.
- Side (Profile) — HAVE head only (Profile head from sheet, 1 of 2 head angles in v8 count), body side NEED TO MAKE, 0/1
- 3/4 back — NEED TO MAKE, 0/1
- Back — NEED TO MAKE, 0/1
Total angles: 2/5 = 40% (front full, profile head only — counted honestly, profile body is not done).
Lounge 3/4 packs on the other branch are NOT a substitute: those 11 files are byte-identical to the lounge/background files (see duplicate check below), not new 3/4 rig pieces.
Next build for this: one pack at a time, shown to Mars before the next pack — 3/4 torso/head first, then side body, then back angles. Do NOT generate a full 5-angle set in one unshown batch.

## 2. Viseme / mouth chart — status with percentages
Pack 4 spec (Mars, 2026-10-31): 14 visemes front + 3/4, 8 mask eye/brow strips, 5 neck cylinders, heads (5 blank + 1 furious).
Current:
- Mouth shapes on the heads sheet (AKqzs.jpg, flying folder): 8 shapes — neutral, smile, grin, open (talk), laugh, shout, surprised, clenched = 8/14 = 57% of the count, but NOT yet sliced as viseme pieces, and NOT mapped to phonemes.
- Eye strips: 0/8 = 0% sliced.
- Viseme phoneme mapping (to build, not yet approved): rest, EE, EH, AH, OH, OO, M/B/P (closed), F/V, L, S/Z, TH, R, W, G/K — 14 slots, mapping to be checked by Mars before slicing.
- Lip sync timing: on 2s normal, on 1s snaps, same as clips.
Next build for this: viseme chart doc + sliced mouth/eye pieces from the approved reference (Pack 1 head), one pack, shown before the next pack. Do NOT invent mouth shapes by regenerating the head — edit from the approved reference only.

## 3. Other priority gaps, in order after 1-2 (from the forwarded gap list, checked against what is actually in cape-jones)
- Exposure sheet / timing template — NOT yet built. Template: frame, pose, hold, mouth, camera — from clips/*.json format, next after visemes.
- Shot spec template + QC checklist — PARTLY: clips/shot-spec.yaml + frame-proof-manifest.json exist, QC pending until Mars looks. Template is next, not a new system.
- Background layout line art — NOT yet built. Painted backgrounds exist (37 images on branch), line-art versions do not.
- Color keys / color scripts — NOT yet built, per episode.
- Storyboards + animatics — scripts exist, boards do not.
- Compositing templates, grade LUTs, audio cue sheets, delivery specs — NOT yet built, post-production, after animation is locked.

## 4. Staged packs — verified counts, with the duplicate correction
Branch feature/character-parts-expansions-20261031, checked 2026-10-31 by API + local SHA:
- FLA packs: 87 files total (83 jpg + 2 md + 2 png references)
- Backgrounds: 38 files (37 jpg + README.md)
- Props: 19 jpg files
- File entries total: 144. Unique jpg images across FLA+backgrounds+props: 80/139 = 58%.
  Duplicate groups: 33. Examples, SHA-verified identical:
  dance-*.jpg = jojo-packs/recent-*.jpg = jojo-packs-2/recent-*.jpg (11 images tripled)
  lounge-*.jpg = lounge-3quarter/clean-*.jpg = backgrounds/bg-*.jpg (11 images tripled)
  props/prop-JmGUv, prop-bfSpz, prop-jPaPG, prop-xyug7 = backgrounds/batch-* (same files)
  So "87 + 38 + 19" is file entries, NOT 144 unique assets. Unique asset count is the number to use for production planning.
  Rejected sheets: cannot verify a rejection from the branch — absence is not a list. What I checked is what IS there.

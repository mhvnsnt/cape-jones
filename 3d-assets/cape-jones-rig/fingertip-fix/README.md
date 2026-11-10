# Fingertip Stretch Fix ("chameleon tongue fingers")

Owner canon (2026-10-18): "He does not have chameleon tongue fingers. His
fingers should not be stretching unless I say 'hey he has extendo fingers'."
Fingers NEVER stretch beyond normal joint articulation.

## Root cause (twofold)
1. Fingertip verts were weighted to WRONG bones — e.g. pinky-tip verts
   dominated by the ring finger's tip bone, index-tip verts bleeding into
   middle/index-2 bones. When fingers curled, tips got dragged by
   neighboring fingers (visible as elongation; in the extreme, verts
   exploded into spikes).
2. (Earlier, already fixed in this branch) finger bones were misplaced
   15-20mm outside the mesh digits; repositioned via `reposition_and_fix.py`.

## The fix — `fix_fingertips.py` (fully procedural, no hand-painting)
Re-weights all finger regions by rest-pose bone proximity:
- Pass 1: every vert assigned to its globally-nearest finger chain
- Pass 2: per chain, articulation-correct weights — 100% distal bone at
  tips, smooth joint falloff, knuckle blend to hand bone, ZERO forearm
  influence, zero cross-finger bleed.

Usage:
```
blender -b --python fix_fingertips.py -- <input.blend> <output.blend>
```

## Verification
- Numeric: 18,312 tip verts in the fixed blend, ZERO cross-finger weight
  bleed above 0.15 (script: `verify_tips.py` pattern).
- Visual (viewed with own eyes, OWN-EYES-BEFORE-DELIVERY LAW):
  - `fist_curl_BEFORE.png` — same fist-curl pose on the pre-fix blend:
    fingers EXPLODE into spikes/shards.
  - `fist_curl_AFTER.png` — same pose on the fixed blend: clean,
    natural fist curl, rounded fingertips, no elongation.
- The older `weightvis_*.png` pair shows the same story as vertex-color
  weight visualization (red = forearm bleed before, blue = correct tip
  weights after).

Fixed blend (working file, regenerable via the script above):
`~/workspace/fingertip-fix/cape_jones_fingertip_fixed.blend`

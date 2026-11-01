# Foreshortened forearm + 3/4 head V2 — report (Mars approved V1, 2026-10-31 16:02 CDT; V2 NOT approved yet)

## V1 base (approved as V1, good start)
- Forearm: from Arm_Front_Lower 153x289, compressed 0.5x length, fist enlarged 1.3x, wrist overlap kept. Output 199x232.
- Head: derived 3/4, front head squashed 0.82, far eye 0.7 — a STAND-IN, not a true 3/4.

## 10 industry-standard methods wired — 10/10 as methods, see honesty notes
1. Foreshortening — perspective shortening: forearm segment compressed to 0.42x (stronger than V1 0.5x), fist closest/largest.
2. 3/4 head construction — Loomis / comic-book head construction: centre line shifted to x=41 in a 100px-wide head (front centre 59/119), eye line / brow line / nose-mouth line marked on the REFERENCE sheet only, not baked into the clean piece.
3. Anatomy: forearm muscle — brachioradialis taper: row-wise width taper, 0.92x at elbow end to 1.10x at wrist (wider near wrist, narrower far).
4. Fist construction in perspective — box/wedge fist: fist enlarged 1.45x wide / 1.30x tall (V1 was 1.30x uniform), so the fist reads as a wedge facing camera, not a stretched oval.
5. Overlap + occlusion — fist OVER forearm (overlap 18px kept); far eye behind nose bridge: 3px bridge-occlusion shadow strip (x38-40, y65-95, 0.65 multiply) on the V2 head.
6. Volume preservation — wrist joint cap intact, cap placed BEHIND the fist (fixed after first V2 build, where the cap ring crossed the fist face). Gap scan at wrist: 0 gap rows for Arm1 and Arm2 (rows wrist-5 to wrist+15, wrist x +-10px all opaque).
7. Rim/light on foreshortened forms — rim variants saved separately: warm amber (255,180,80) screen blend on near edge (3px), cool multiply shadow on far edge (3px). Rim follows key; clean V2 pieces have NO baked rim.
8. Turnaround consistency — front -> 3/4: same features, same order. Front head 119 wide, centre 59; V2 head 100 wide, centre 41; far side compressed 0.70, near side 0.97; far eye extra 0.85 squeeze. Feature order (cowl, near eye, far eye, nose, mouth) unchanged.
9. Pose-driven substitution — Arm 2 different-angle fist: BUILT in this task, 1/1. Source Hand_2_FistBack (back view, 94x131, bbox crop, 1.15x), centred on the Arm2 fist centre (x181 at y110, not the original wrist pivot 147 — first build used 147 and misaligned, fixed), original fist cleared below the wrist, cap behind the new hand. This closes the previously owed Arm 2 different-angle fist 0/1 -> 1/1 as a piece (pose integration still owed separately).
10. Industry QC — silhouette readability: Arm1 V2 bbox 47-191 x 0-193, opaque 17,788; Arm2 V2 bbox 107-244 x 0-192, opaque 18,715; Arm2 diff-fist bbox 107-244 x 0-208, opaque (after rebuild, see manifest check); head V2 100x172, bbox 2-95 x 4-168, opaque 12,633. Joint-cap check: 0 gap rows (above). Scale check: forearm length V1 232px tall -> V2 216px tall (shorter, as foreshortening requires); fist width V1 ~? vs V2 fist 1.45x source — fist reads larger than forearm width, as required.

## Files (all new, in forearm-head34-v2-20261031/)
- forearm-v2-arm1-front-20261031.png (241x216, clean) + -rim variant
- forearm-v2-arm2-back-20261031.png (249x215, clean) + -rim variant
- forearm-v2-arm2-different-angle-fist-20261031.png (249x215, Hand_2 back view)
- head34-v2-construction-warp-20261031.png (100x172, clean, NO construction lines)
- head34-v2-construction-lines-reference-20261031.png (lines on reference only)
- proof-v1-vs-v2-20261031.png (V1 vs V2, viewed)

## Honesty — how close is V2 head to a true 3/4?
V2 head is a construction-guided ASYMMETRIC WARP of the front head (Loomis centre-line shift + far-side compression + far-eye squeeze + bridge occlusion). It is CLOSER to a true 3/4 than V1's uniform 0.82 squash, but it is NOT fully hand-drawn construction — the linework is warped original art, not redrawn. A true hand-drawn 3/4 head (and 3/4 torso, side body, back body) is still owed if Mars wants that level. Do NOT call V2 a true hand-drawn 3/4.

## Defects found and fixed during viewing
- First V2 build: wrist cap ring crossed the fist face (cap pasted after fist). Fixed: cap BEHIND fist, fist over it; only a small joint arc peeks at the wrist, as in v7c joints.
- First Arm2 diff-fist build: hand centred on original wrist pivot (147) misaligned with the Arm2 fist centre (181), and the original fist peeked behind the new hand. Fixed: original fist cleared below wrist, hand centred at 181, cap behind hand.

## Still owed (not claimed done)
- Mars approval of V2: 0/1.
- True hand-drawn 3/4 head / torso / side / back: still owed (see above).
- Pose integration of the Arm2 different-angle fist into a full punch pose: piece built, pose not built.
- Arm2 foreshortened forearm in a full pose, and V2 forearm rim on a real shot (rim variants are pieces, not shots).

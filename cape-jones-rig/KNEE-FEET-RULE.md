# KNEE-FEET RULE (Mars, 2026-10-31 16:09-16:10 CDT, standing)

Your knees and feet are always pointing in the same direction.
If his kneecaps start to go inward, his toes need to go inward as well.
Exception only: unless his legs get broken or something.

## Problem it names
Improved dance contact sheet, top row pose 2 (frame 15) and pose 4 (frame 42): knees go inward / legs cross, but feet/toes point OUTWARD. That reads as broken knees — like someone hit him in the knees with a baseball bat. All other dances look really good; this is the one small issue.

## Check before any pose ships
1. Knee direction (kneecap facing).
2. Foot/toe direction.
3. They must match. If knees go inward, toes go inward. If knees go outward, toes go outward.
4. Fix is foot rotation/substitution on its axis (like the forearm gauntlet/fist roll rule), ankle joint intact, no detached feet.

## Related rule
Perspective rule (arms): hand drives cuff/fist. Knee-feet rule (legs): knee drives foot. Both are rotation/substitution, not limb movement.

## Research — what the defect is called (2026-10-31, knee-feet fix)
- Proper name: **knee-foot misalignment / valgus tracking failure**. In anatomy terms: **genu valgum (knock-knee)** — knees collapse toward the midline — combined with **external tibial rotation**, where the shin twists outward so the foot points out while the knee points in. That combination is exactly the "broken knees" read: a hinge joint (the knee) being asked to bend in a direction it does not hinge, while the foot is planted the other way.
- Industry rule behind Mars's sentence: **the tibia tracks over the 2nd toe** (sports-therapy / gait literature: in a lunge/squat, the knee must track along the same line as the 2nd toe, or valgus collapse loads the joint). **Foot progression angle** is the angle of the foot relative to the direction of travel; the knee's hinge plane must match it. Long-axis rotation (LAR) of the tibia re-orients the foot: internal tibial rotation sends toes inward, external rotation sends toes outward — so a foot can only be "flipped on its axis" by rotating/substituting the lower leg, never by bending the knee sideways.
- Sources used (public web search, 2026-10-31): knee functional anatomy / tibial rotation and 2nd-toe tracking (Sports Therapy for the Knee, Vavetsis); foot progression angle and external tibial torsion (The Gait Guys); genu valgum / valgus vs varus definitions and Q-angle (anatomy references); "keep your knee and foot pointing in the same direction" / tibial internal rotation correction (PostureDirect, knee-valgus correction). No show material used.

## Fix method in a 2D cutout rig (2026-10-31, dance-kneefeet-fix)
- Same principle as the forearm rule: transverse rotation in 2D is **drawing substitution**, not limb movement. The shin/knee position does NOT move; the lower-leg piece is swapped for a mirrored piece (FootIn) whose toe points the other way, with the knee anchor re-mapped (Front lower: ball x 95 -> 59; Back lower: 100 -> 127). Ankle joint stays intact — no detached feet, no seam at the ankle, because the whole lower piece is mirrored, not a foot cut off and pasted.
- Honest trade: mirroring the whole lower piece also mirrors its calf shading side. That is the cost of a substitution drawing, and it is far smaller than the broken-knee read it fixes. A hand-drawn inward-foot lower (not a mirror) is still owed if Mars wants shading-perfect pieces.
- Swap points are keyframes, not hidden: FootIn is ON for frames 15-55 of the improved dance (groove + kick segments, knees inward) and OFF for frames 1-13 and 56-109 (knees outward, original toes outward = matching). The foot flip therefore happens on keyframe 15 and back on keyframe 56 — a visible substitution pop, like the gauntlet swap, stated here so it is not mistaken for a rendering bug.

## Check for future poses (walk, kick, flex, fight, dance)
- Before any pose ships: (1) knee direction, (2) foot/toe direction, (3) they match. Inward knees -> inward toes. Outward knees -> outward toes. Straight knees -> straight toes.
- Crossing legs (kick, dance) do NOT exempt the rule: if the legs cross and the knees end up pointing inward, the toes must be substituted inward, even though the legs have swapped sides.
- Exception only: a deliberately broken/injured leg, named as such in the shot spec. Never as an accident of the rig angles.

## Verification note (2026-10-31, dance-kneefeet-fix)
- f042 kick and f015 groove verified at FOOT LEVEL, not just full-figure
  scale: diagonal shins misread at small scale. f042: before toes splayed
  left/right, after both toes point down toward the midline. f015: before
  toes splayed, after feet together pointing down-left (crossover
  direction, no outward splay). Fix folder: dance-kneefeet-fix-20261031/.
- Combine dance: same defect in its groove pose, NOT fixed here — no
  builder script in its folder. See FIX-REPORT-20261031.md in the fix
  folder for the full still-owed list.

## CORRECTION 2026-10-31 16:58 CDT — BIDIRECTIONAL RULE, BLOCK RANGE WAS WRONG (Mars)
- Mars, reply to dance-kneefeet-contact-20261031.png, top row third frame: his knees are pointed OUTWARD in that frame, but the v1 fix pointed his feet INWARD. That frame is incorrect and must be fixed: feet back OUTWARD to match outward knees.
- The v1 mistake was a BLOCK range: FootIn ON for frames 15-55, as if every frame in that stretch had inward knees. It did not. Knee direction changes inside the stretch (stride -> groove -> kick), so a block flips outward-knee frames inward and misses inward-knee frames before frame 15.
- BIDIRECTIONAL RULE, standing, both directions, no exceptions except a deliberately broken leg named in the shot spec:
  * Knees pointed OUTWARD -> feet pointed OUTWARD (original lowers).
  * Knees pointed INWARD -> feet pointed INWARD (FootIn mirrored lowers).
  * Knees straight/forward -> feet straight/forward (original lowers; do not flip on a near-zero crossing).
- PIPELINE GATE (per frame, not per block, not per segment):
  * Read that frame's own leg_upper angles. FootIn = True ONLY if leg_upper L > 0 AND leg_upper R < 0 (both thighs angled toward the midline = both kneecaps inward).
  * Otherwise FootIn = False. This is the thigh-angle sign, NOT knee-x minus hip-x: at rest the thigh piece already sits slightly inboard of the hip, so x-offset alone misreads straight legs as inward.
  * Audit table must list every rendered frame (frame, L upper, R upper, knee direction, foot choice, changed vs previous) — a block range with no per-frame table FAILS the gate.
  * Contact-sheet keyframe check (8/8 must pass): f001 OUT/OUT, f015 IN/IN, f028 OUT/OUT (the corrected frame), f042 IN/IN, f056 OUT/OUT, f069 OUT/OUT, f083 OUT/OUT, f097 OUT/OUT.
- Anatomy study behind the correction (same sources as above, applied in both directions): the tibia tracks over the 2nd toe in EITHER direction — internal tibial rotation sends toes inward, external tibial rotation sends toes outward. Valgus (knee-in / toe-out) and varus (knee-out / toe-in) are BOTH misalignments: the knee is a hinge, it cannot bend sideways, so any knee/foot direction mismatch reads as a broken joint, whichever way it points. That is why the rule is bidirectional and why a one-way "always inward" fix creates the exact same broken read in reverse.
- Correction folder: dance-kneefeet-fix-correction-20261031/ (v1 fix folder untouched). See CORRECTION-REPORT-20261031.md there for the per-frame audit.

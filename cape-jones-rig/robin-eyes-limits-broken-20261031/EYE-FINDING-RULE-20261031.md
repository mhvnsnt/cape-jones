# EYE-FINDING RULE — standing, Mars 2026-10-31 19:40-19:41 CDT

Recorded exactly as Mars said it, in operational form. The Robin refit
(robin-eyes-refit-20261031/) is APPROVED PERFECT 1/1. This rule is how
character eyes are found and placed going forward, for every character.

## 1. FINDING character eyes — the refit extraction, always first
- Take the character's own white pixels in the eye band.
- Connected-component labelling of those pixels gives the EXACT interior
  of the black eye outline — Left 108px / Right 105px for Cape, front head.
- NEVER use an approximate box. A box is not an eye interior.
- If the white components in a piece are fragments (Cape's Face_Angry eyes
  are 14px / 6px fragments, not full interiors), say so plainly and do NOT
  call the fragment a full mask. Use the pulled shape's outline instead,
  labelled as such (see limits-broken L1).

## 2. WHOLE-EYE placement — the refit method
Use this when placing a whole eye, not a pupil:
1. Extract the target character's own eye interior (rule 1).
2. Scale the pulled shape anisotropically to that mask's bbox.
3. Clip to the mask — zero overflow past the black outline.
4. Complete the remaining mask pixels in the target's own measured white
   (Cape: (248,250,248)) so coverage is 100%.
5. Red debug ring on DEBUG proofs only, on pixels just outside the mask.
   NEVER in a clean proof. Clean proofs: 0 red pixels, by gate.

## 3. PUPIL placement — the FIRST method, different on purpose
Use this when placing a pupil, never the whole-eye method:
1. Height-fit the pulled pupil blob to the target eye height at 1x.
2. Centre it inside the eye.
3. Do NOT fill the whole eye with a pupil. A pupil is a blob inside an
   eye, not the eye itself.
4. If the pulled source has no pupil (all 25 Robin library eye files are
   solid white blobs, dark interior px = 0 in 23/25, grey shadow only in
   02-night), say so plainly and do NOT invent one. The pupil method is
   coded in build_limits.py (pupil_place) and gate-tested on a test-only
   disc (22px placed, 0 overflow), but no fake pupil eye is presented
   as pulled.

## 4. What counts as a break
A limit counts as broken only when a proof shows it broken by measurement:
coverage 100%, overflow 0, outline difference measured, gate PASS.
A method named but not run is a mapping, labelled as such, never a run.

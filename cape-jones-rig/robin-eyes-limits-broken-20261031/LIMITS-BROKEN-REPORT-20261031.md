# Robin Eyes LIMITS-BROKEN — all refit section-5 limits worked, wired 100%

Date: 2026-10-31. Folder: `robin-eyes-limits-broken-20261031/`.
Builder + gate: `build_limits.py`, `check_limits.py` — GATE 9/9 PASS.
No repo push. No file Mars has seen overwritten (new dated folder only).
The refit itself is APPROVED PERFECT 1/1 (Mars 2026-10-31 19:40-19:41 CDT).
Approval for THIS new broken-limit work: 0/1 — the refit approval does
not approve these new masks/variants.

## Standing rule recorded
See `EYE-FINDING-RULE-20261031.md` in this folder (whole-eye = refit
method, pupil = first height-fit method, finding = own-white connected
components). That doc is the rule going forward, not this report.

## Counts, with percentages (percentage rule)
- Limits fully BROKEN: 2/3 = 67% (L1 expression, L2 profile).
- Limits PARTIALLY BROKEN: 1/3 = 33% (L3 detail — shadow gradient
  preserved, pupil detail impossible from this library without inventing
  it, so it is NOT claimed broken).
- Expression masks: 10/10 sides differ from neutral = 100%.
- Profile near eye: 1/1 filled 100% = 100%.
- Detail: night gradient preserved, day control flat — see below.

## L1 — Expression silhouette: BROKEN
Old problem: every front entry shared Cape's neutral outline, because the
final fill was flat white over the neutral mask.
Break: per-expression target masks. Cape's Face_Angry piece was checked
first and is NOT usable as a full mask — its eye whites are 14px / 6px
fragments, not interiors — so, as the task allowed, each expression mask
is the pulled Robin expression shape's own outline, scaled anisotropically
to the neutral bbox, hole-filled, largest component kept. That is the
expression's outline, not Cape's neutral outline, and it is labelled as
Robin-outline, not as a Cape-drawn lid.
Measurements (full table in `measurements-20261031.json`):
- Angry (11): L 122px, symdiff 72px 66.7%, top-slope 0.041 vs neutral 0.317;
  R 121px, symdiff 36px 34.3%, slope -0.233 vs -0.316.
- Determined (12): L 100px, 30px 27.8%, slope 0.392; R 64px, 43px 41.0%, -0.377.
- Angry-point (13): L 91px, 37px 34.3%, 0.358; R 86px, 43px 41.0%, -0.372.
- Strain (14): L 118px, 20px 18.5%, 0.268; R 114px, 37px 35.2%, -0.274.
- Grit (15): L 75px, 33px 30.6%, 0.326; R 87px, 44px 41.9%, -0.219.
- Mean symdiff: 37.1%, range 18.5-66.7%. Every side differs: 10/10.
- Proofs: `expression/` (5 heads + neutral), `proofs/expression-contact-20261031.png`,
  `proofs/expression-outlines-20261031.png` (left masks stacked, 14x, labelled
  with symdiff + slope). Honest visual note: at head scale the differences
  are 1-3px and read subtly; the outline sheet is where they read clearly.
  That is why both contacts exist.
- Caveat, not hidden: an expression mask replaces the neutral mask, so it
  may cover a few black-outline pixels the neutral mask did not. In a final,
  the black outline would need redrawing around the new white shape. This
  set is a mask/white proof, not a redrawn black outline, and is not claimed
  as one. Overflow is 0 relative to the expression mask itself; overflow
  vs the neutral mask is exactly the symdiff above, by design.

## L2 — True profile / 3-4 placement: BROKEN (near eye), with scope stated
Old problem: single-eye entries were fitted to the front-left mask.
Break: a true profile target was extracted the SAME way as the front
masks — Cape's own profile head (`sliced/Head_Profile.png`), bright
components in the eye band. The near profile eye IS there, and is now used:
- Profile mask: 110px, bbox x74-96, y80-87, in Head_Profile.
- Robin 04 profile eye fitted to it by the refit method: coverage 100%,
  gate-verified as 1,760 Cape-white px in the profile bbox at 4x
  (= 110 x 16), exactly. Proof: `profile/profile-04-robin-profile-on-cape-profile.png`,
  debug ring version alongside it.
- The far-eye fragment in the profile head (41px, x124-133, y77-85) was
  LEFT as original art, not fitted — it is a fragment, not a full eye,
  and fitting it as if it were a full eye would be a false claim.
- 3/4 treatment, labelled NOT a profile: entry 22 on front masks, near eye
  108/108px full, far eye depth-shrunk to 0.85 about its centre = 78/105px
  (74%, vs 0.85^2 = 72.25% expected for area — close, shape-dependent).
  Proof: `profile/threequarter-22-depth.png`, in `proofs/profile-detail-contact-20261031.png`.
  A front fit with depth scaling is not a profile fit, and is not labelled one.

## L3 — Interior detail lost to flat recolour: PARTIALLY BROKEN
Old problem: flat recolour erased fine interior detail (and JPG speckle).
Honest audit first: the Robin library eye files contain NO pupil at all.
Dark interior px = 0 in 23/25 entries. The only interior variation in the
whole library is 02-night grey shadow: 338px (eye0) / 235px (eye1) in the
150-200 brightness band at original size, which resizes to a 201-227
gradient (resampling lifts it over 200, so a 100-200 threshold finds 0 —
that threshold bug was caught and fixed to a tone map, not hidden).
Break, for the detail that actually exists:
- Detail variant: source brightness gradient mapped onto the whole-eye
  mask as Cape-white tone (tone = Cape white x g/255), so the gradient
  shape is preserved in place, not flattened.
- Night: L tone mean 211.2, std 12.02, 99px darker than flat; R mean 213.0,
  std 13.71, 93px darker. Flat refit std = 0 by construction.
- Day control (solid blob): L mean 245.8, std 3.57, 0px darker than flat;
  R mean 246.2, std 3.16, 0px. That is the control proving the method does
  NOT invent detail where there is none: day detail variant ≈ flat.
- Proofs: `detail/02-night-front-neutral-detail-variant.png` (visibly
  grey-shadowed eyes vs day's clean white) and the day control, in the
  profile-detail contact.
- NOT broken, stated plainly: pupil detail. No pulled pupil exists in
  this library, so no pupil-in-white eye is delivered. The pupil method
  (height-fit to target height, centred, standing rule section 3) is coded
  in `build_limits.py` as `pupil_place` and gate-tested on a test-only disc
  (22px placed, 0 overflow), ready for a pupil-bearing source. Presenting
  a pupil eye from this library would be inventing detail, so it is not done.
- JPG speckle: erased by flat recolour in the approved refit, and that
  remains a benefit there, not a detail to restore — speckle is noise,
  not eye detail, and is not restored.

## Methods: 10 industry-standard + 10 experimental
RAN = actually executed in build_limits.py. MAPPING = named method, what it
would do here, NOT run as vendor software, no model downloaded, no run claimed.
Industry-standard (10):
1. Mask fitting / clipping — RAN (expression + profile fills clipped to mask).
2. Contour matching to target outline — RAN (masks are extracted contours).
3. Connected-component labelling — RAN (neutral + profile extraction).
4. Anisotropic scale to bbox — RAN (all masks).
5. Shape-to-mask warp (expression outline as mask) — RAN (L1).
6. Depth scaling for 3/4 (far eye 0.85) — RAN (L2, proxy for true depth).
7. Brightness / tone mapping — RAN (L3 night gradient).
8. Debug overlay, debug-only — RAN (profile debug ring).
9. Gate measurement (coverage, overflow, symdiff, slope) — RAN (check_limits.py 9/9).
10. Photoshop / Harmony / Animate clipping-mask principle — MAPPING
    (the principle the builder implements; no vendor software run).
Experimental (10):
1. SAM-style learned segmentation for eye masks — MAPPING (would replace
   threshold+components; no model run).
2. MediaPipe face-mesh eye landmarks — MAPPING (would give lid points;
   no model run).
3. Blendshape expression rig — MAPPING (expression masks are its manual
   equivalent; no rig built).
4. Gaze / eye-tracking pupil placement — MAPPING (pupil method is its
   static equivalent; no tracker run).
5. Anime2Sketch-style learned line extraction — MAPPING (no model run).
6. Depth Anything / MiDaS single-image depth for 3/4 — MAPPING (0.85
   depth scale is the proxy; no model run).
7. Optical-flow morph between expression masks — MAPPING (not run).
8. RIFE / FILM frame morph between expressions — MAPPING (not run).
9. 3D head-model normal-based eye placement — MAPPING (no 3D model built).
10. Generative inpainting for far-eye completion — MAPPING, REJECTED for
    use here (it would invent the far eye; the fragment was left original
    instead).

## Still owed
- New broken-limit work approval: 0/1 (refit itself is already approved perfect).
- Redrawn black outlines around expression masks, if Mars wants expression
  eyes as finals rather than mask proofs: 0/1.
- A pupil-bearing pulled source, if Mars wants a real pupil-in-white eye:
  0/1 — no such source in the current 25-entry library, and none was invented.
- Far profile eye as a full eye: not owed from this head piece — it is a
  41px fragment; a full far eye needs a different source piece, Mars's call.
- No repo push made (per task); landing is the parent's call, not claimed here.

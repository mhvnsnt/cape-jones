# Eyes v4 — PULLED Robin shapes, no hand-tooled eye shape, no black outline (Mars, 2026-10-31 16:47-16:54 CDT)
## Rules applied (all Mars, authoritative)
- Dark end on Arm1 side, image-LEFT (v3-confirmed correct) — NOT flipped back.
- Eye SHAPE itself is pulled, not drawn, not vector-polygoned, not hand-tooled in any degree.
  Only handling: fitting the pulled shape to his head (scale/position/affine transform of the
  pulled mask pixels), cowl purple (90,39,114), dark end Arm1 side, NO extra black outline.
- No black outline ring around the eyes when composited on his face; his cowl is the mask.
  No second mask layer. If a pulled shape carries its own thin line as part of the eye itself,
  only what belongs to the eye is kept — v4 strips contain 0 black pixels (verified).
- License is NOT a blocker (Mars 16:53). Sources recorded plainly below.
- V3 is FALLBACK / DRAFT / PLACEHOLDER / REFERENCE only (see v3 folder label file).
## Source — FOUND, used
- Mars's repo mhvnsnt/cn-gigaleak-teen-titans, release teen-titans-complete-v1
  (split ZIP TEEN_TITANS.zip.part-aa/ab, 970 entries, central directory read by range,
  no full 736 MB download). No file named Batman, no Space Ghost file in this archive.
- USED: "TEEN TITANS/TEEN TITANS MAIN MODEL PACK/Main Models/jpeg/ROBIN Day.jpg"
  (1648x1272, model sheet #385-900 ROBIN MAIN MODEL), head close-up white eye blobs
  extracted verbatim by pixel labelling (near-white, enclosed by black mask):
  near eye x805-901, y676-738 (96x62, 3,215 px), far eye x935-999, y685-734 (64x49, 1,525 px).
  Files: source-robin-near-eye-mask-20261031.png, source-robin-far-eye-mask-20261031.png.
  Night version checked: same shapes in shadow grey (thr ~180), not used (v4 eyes are white).
  Robin expression sheets RBEXPRES01-05 exist as EPS only; no Ghostscript/Inkscape on VM,
  so expressions are affine transforms of the pulled Day mask (below), not separate EPS pulls.
## Source — NOT found / NOT used as a shape
- Animated Batman pack: no Batman file by name in the Teen Titans archive (0 hits).
  Public search found only fan clipart / photo masks, not an animated Batman eye pack.
- Space Ghost: no file in the Teen Titans archive, no pullable public eye pack found
  (costume guides and generic ghost clipart only). Space Ghost remains a NAMED equivalent
  (Mars: Batman without the ears, same eye language) — NOT a file used in v4. Do not claim it was.
- Face-top secondary source: FreePNGimg "Batman Mask Free Png Image" (282x400, transparent,
  https://freepngimg.com/png/9765-batman-mask-free-png-image) — a PHOTO-style plastic mask,
  not animated. Used ONLY for the ears-off face-top proof (below). License note from Mars:
  license is not a blocker; recorded plainly here.
## V4 deliverables (new folder, v3 untouched except its fallback label file)
- 5 front expressions, 480x128 strips, white angular, NO pupils, dark left segment:
  01 neutral, 02 determined-focused, 03 angry-scowling, 04 surprised-alarmed, 05 concentrating.
  Transforms are affine transforms of the pulled mask only (scale Y / shear / rotation):
  neutral 1.00/1.00/0/0; determined 1.00/0.85/-0.10/-5; angry 1.00/0.65/-0.20/-12;
  surprised 1.00/1.20/0/0; concentrating 1.00/0.75/-0.14/-8. Black pixels per strip: 0/5.
- Angle sheet: FRONT pair (near eye + mirror) vs 3/4 pair (near + far AS PULLED, unmirrored).
- Proof on Head_Front, strip-overlay method (comparable to v3) — NOTE: the strip band itself
  reads as a second mask rectangle on his face even with no black outline. Final-face use
  should be the in-mask fit, not the band overlay.
- Proof eyes-in-own-mask: pulled eyes fitted to Head_Front's actual openings (height-fit,
  12px wide at 119px head, shape preserved, no clipping into blocks). Honest limit: at
  opening size the Robin shape reads very close to his original eye slits — the pulled
  shape is clearest at strip size; at slit size the difference is subtle.
- Face-top proof: ears cleared from the photo mask, recolored flat cowl purple, used as a
  backing cap. HONEST VERDICT: this photo mask's ears-off top is STEPPED, not a smooth
  rounded arc — it does NOT round off his head top as Mars asked. The ears-off + recolor
  method is proven, but a properly ROUNDED animated cowl top is still owed (not faked by
  drawing a curve, which would violate the no-hand-tooling rule).
## Still owed
- Mars approval of v4: 0/1. V4 is viewed, not approved.
- Comedic-set band composite with flipped dark end: 0/1 (unchanged from v3 report).
- Remaining normal expressions (intrigued, squinting/flight, straining, unconscious): not built,
  only if Mars wants them.
- Rounded animated cowl top (smooth arc, ears off): 0/1 — photo mask top does not achieve it.
- Robin expression EPS pulls (RBEXPRES01-05): 0/5 — needs a vector/EPS renderer, not drawn substitutes.
- No repo push in this task.

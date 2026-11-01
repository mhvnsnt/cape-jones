# Robin Eyes REFIT — fill the whole black, match Cape's white, red debug outline only
Date: 2026-10-31. Folder: `robin-eyes-refit-20261031/`. Builder/gate: `build_refit.py`.
No repo push. No file Mars has seen overwritten (new dated folder only).
Mars approval of the CORRECTED FITS: 0/1 — the library approval (2026-10-31 ~19:01 CDT)
does NOT approve these refits; these are the correction he just ordered.

## 1. The defect, measured (not guessed)
Cape's own eye interiors were extracted from `sliced/Head_Front.png` (119×172)
by connected-component labelling of his own white pixels in the eye band:
- Left interior: 108 px, bbox x25–45, y72–80 (21×9).
- Right interior: 105 px, bbox x73–92, y72–80 (20×9).
These are the exact insides of the black eye outlines, not the old approximate
boxes (25–44 / 73–92) and not a hand-drawn shape.

The old (v4-library) proof method height-fit each Robin blob to 8 px tall at 1x
and centred it. Measured against the true interiors, over 43 eye sides:
- Old coverage: mean 40.1%, range 0.9%–80.0%.
- Worst: 16-sg01-laugh-swirl left 0.9% (a thin curve, not a blob).
- Example: 01-day left 49.1%, right 38.1% — i.e. a pupil-sized blob sitting
  inside a much larger angular opening, exactly as Mars described.
Cape's eye-white, measured from his own art (213 white pixels in the eye band):
median (248,250,248), mean (244.5,244.8,244.2). Robin Day median was
(244,245,240) — close, but not Cape's white.

## 2. Industry-standard methods wired (methods, not software claims)
1. Mask fitting / shape-to-mask (Animate/Harmony mask-clip, Photoshop
   clipping-mask principle): scale the Robin shape anisotropically to the
   target mask's bounding box, then clip to the mask — zero overflow past
   the black outline.
2. Contour matching: the target is Cape's own extracted eye contour, so the
   fitted eye follows his angular eye shape, not a rectangle.
3. Colour matching to a reference white: every fitted pixel is set flat to
   Cape's measured white (248,250,248). Input Robin white vs output Cape
   white is recorded per side in `refit-table-20261031.json`.
4. Mask compositing / corner completion, stated plainly: a rounded Robin
   blob, even scaled to the bbox, covers only 79.4% of the angular mask on
   average (scaled-only column). The remaining mask pixels are completed in
   the SAME Cape white, so the eye reads as one solid white eye filling the
   whole interior. The Robin shape is the dominant core; the completion is
   invisible because it is the same flat colour. This is not hidden — the
   scaled-only coverage per side is in the table.
5. Debug overlay (labels-are-debug-only rule): a RED (255,0,0) ring is drawn
   around the fitted eye on the DEBUG proof only, on pixels just outside
   the mask (on the black outline). It is never in the clean proof.

## 3. Results — all 25 entries refit, clean + debug pair each
- New coverage: 100.0% of the target interior on all 43 sides (25 entries:
  18 two-eye + 7 single-eye, fitted to the left opening, as in the old proofs).
- Clean proofs: 0 red pixels across all 25 (gate PASS).
- Debug proofs: 30,384 red pixels total (the rings, gate PASS — red present).
- Overflow: 0 — fitted white exists only inside the target masks (verified:
  Cape-white pixel count in the 4x eye band = 3,408 = (108+105)×16 for
  every sampled proof).
- White: every fitted pixel is exactly (248,250,248) in the clean proofs.
- Contacts: `refit-contact-clean-20261031.png` and
  `refit-contact-debug-20261031.png` (25 proofs each, 4 columns).

## 4. Per-entry table (summary; full table in refit-table-20261031.json)
Old = old height-fit coverage; Scaled-only = bbox-scaled Robin shape alone;
New = final (with same-white completion). All values are % of that side's
target interior. Sides: L/R.
- 01-day-front-neutral: old L49.1/R38.1, scaled L88.9/R81.9, new 100/100
- 02-night-front-neutral: old L56.5/R44.8, scaled L91.7/R88.6, new 100/100
- 03-rbn01-front-neutral: old L38.9/R54.3, scaled L82.4/R90.5, new 100/100
- 04-rbn02-side-profile: old L43.5, scaled L88.0, new 100
- 05-ca01-action: old L23.1/R55.2, scaled L90.7/R93.3, new 100/100
- 06-ca02-action: old L14.8/R39.0, scaled L40.7/R67.6, new 100/100
- 07-ca03-action: old L55.6/R17.1, scaled L92.6/R81.9, new 100/100
- 08-rb01-action: old L29.6, scaled L93.5, new 100
- 09-rb02-action: old L21.3, scaled L69.4, new 100
- 10-rb03-action: old L47.2, scaled L85.2, new 100
- 11-expres01-angry: old L39.8/R80.0, scaled L73.1/R90.5, new 100/100
- 12-expres02-determined: old L31.5/R38.1, scaled L82.4/R60.0, new 100/100
- 13-expres03-angry-point: old L39.8/R33.3, scaled L75.0/R70.5, new 100/100
- 14-expres04-strain: old L46.3/R32.4, scaled L95.4/R86.7, new 100/100
- 15-expres05-grit: old L66.7/R66.7, scaled L69.4/R70.5, new 100/100
- 16-sg01-laugh-swirl: old L0.9/R21.0, scaled L3.7/R60.0, new 100/100
  (completion-dominant: the swirl is a thin curve, so most of this refit
  is the same-white completion — comedic reference only, as before)
- 17-dc-robin1-action: old L21.3, scaled L71.3, new 100
- 18-dc-robin2-action: old L28.7, scaled L93.5, new 100
- 19-dc-robin3-action: old L45.4, scaled L85.2, new 100
- 20-cc-front-neutral: old L45.4/R30.5, scaled L89.8/R69.5, new 100/100
- 21-robin1-neutral: old L43.5/R39.0, scaled L84.3/R83.8, new 100/100
- 22-robin2-34: old L32.4/R34.3, scaled L70.4/R77.1, new 100/100
- 23-headai-neutral: old L46.3/R44.8, scaled L92.6/R86.7, new 100/100
- 24-rbn01bw-front-neutral: old L44.4/R54.3, scaled L90.7/R90.5, new 100/100
- 25-place-front-neutral: old L52.8/R35.2, scaled L90.7/R72.4, new 100/100

## 5. Honest limits (and, per the 2026-10-31 19:02 standing rule, what breaks them next)
- Expression silhouette trade-off: because the final fill is one flat Cape
  white over the whole neutral Cape mask, front entries now share Cape's
  eye silhouette — Robin's expression slant is preserved only in the scaled
  core, which is the same colour as the completion, so it does not read as
  a different outline. If Mars wants angry/determined/grit outlines to stay
  visibly different, the next break is per-expression target masks (lid +
  brow shapes per expression), not the neutral mask — not built here, and
  not claimed.
- Single-eye entries (profile/3-4 views) are fitted to the front left
  opening only, as in the old proofs; a true profile eye placement is a
  separate fit, not claimed.
- The red debug ring sits on the black outline (pixels just outside the
  mask). It is debug-only and is absent from every clean proof by gate.
- JPG speckle in Day/CC source masks is erased by the flat recolour — a
  benefit here, but it also means fine Robin interior detail (none exists
  in a solid white blob) is not preserved; there was none to preserve.

# Mouth packs — clean pipeline, 2026-10-31

## Approval status, plainly
- PAH GO cleaned movement (`mouth-jaw-cleanup-5-methods-20261031/`, 30f @24fps) is
  APPROVED 100%, 1/1, Mars 2026-10-31 22:24 CDT. It is UNTOUCHED here.
- Everything in THIS folder is a NEW version / new pack. Approval 0/1 each:
  clean-line PAH GO, improved pipeline, FRONT-4 pack, THREEQUARTER-3 pack.
  No repo push.

## 1. Clean-line fix — no hand tool
Mars: the approved MBP bridge was a hand-drawn straight 6px stroke, visible
as a step at 3x zoom, not a clean SVG/rendered line; fix it back to normal,
industry-standard, cleaner.

Method, wired in `mouth_pipeline.py` (no hand-tool step anywhere):
- Centreline extracted from ORIGINAL tight fragments only (left 8–41, right
  67–75 at source scale, 86×10). The approved straight bridge was NOT used
  as input — it was excluded, so no hand-tool pixel survives.
- Smoothing cubic spline (scipy UnivariateSpline, s=5) through those
  centreline points. Median residual 0.203px, max 0.84px — the curve follows
  the original wavy line, it does not copy pixel steps.
- Sampled spline points → cubic Bezier segments (Catmull-Rom → Bezier),
  written as a real SVG: `packs/mbp-clean-line.svg` (18 path points, 17
  segments, stroke 5, round caps/joins).
- Rasterised at 8× supersample, LANCZOS downscale to 178×23, alpha
  threshold ≥128 (no fringe).
- Gate: dark columns 15–156, missing columns inside: none, max adjacent
  centre step 1.0px (approved: 2.0px). `gate_mouth.py` exit 0 PASS.
- Right-corner uptick IS preserved: centre median 15.0px at x130 → 2.0px
  at x154–156, same direction as approved. Honest trade-off: stroke is a
  constant 5px, clean/SVG-like by design; the approved diagonal thickened
  to 11px at the corner, that thickness variation is NOT preserved. That
  is what makes it look rendered rather than hand-tooled.
- Gap behaviour, stated: the spline sags in the gap (source y up to ~7.6,
  placed ~17.6) instead of the approved flat y14.0 bridge — it follows the
  original wave, it is not a straight line. At normal size it reads as one
  continuous wavy closed-mouth line; at 3× zoom there is no flat segment
  and no join step.
- Rebuilt movement: `pahgo-lineclean-20261031.gif`, 30f @24fps, same
  timeline/jaw as approved (MBP 0, AH 16, GK 8, GAP 10, REST 0), only the
  MBP patch swapped to the vector line. AH/GK patches are the approved
  cleaned patches, alpha-thresholded.

## 2. Improved pipeline (Mars 22:25 CDT pipeline update)
The pipeline itself, not just this one bridge, so future mouths never go
through a hand-tool step again. `mouth_pipeline.py` stages in order:
1. Colour decontamination (dark <90, orange tongue, white teeth only).
2. Component selection / garbage matte (mouth-body component only).
3. Vector line fit for thin-line mouths (spline → Bezier SVG → 8× raster).
4. Placement: alpha-bbox centre anchor, single target (231.5, 504.5).
5. Gates: `gate_mouth.py` — thin-line continuity, placement centre,
   no-crop. Exit 0 PASS / 1 FAIL.
Pipeline proof on a NEW mouth, not just MBP: EE smile vector-fit
(`packs/ee-clean-line-patch.png` + `.svg`, 200×113, stroke 3, 37 points,
36 segments, median residual 0.083px, max 0.414px, columns 12–191, missing
none, gate PASS). Every new pack below ran through stages 1, 2, 4, 5,
plus stage 3 for thin lines.

## 3. More mouth packs
Distinct drawings total: 7 Robin drawings (same 7 as v2) — NO new source
drawing was invented, morphed, or hand-tooled, and no new character mouth
was pulled. The "more packs" here is 3 new pack groupings through the new
pipeline, plus the clean-line version. All fitted at target (231.5, 504.5).
- LINECLEAN-PAHGO (new version): MBP vector 178×23, AH 196×67, GK 188×30.
- FRONT-4: MBP-v2 211×25 (short line — honest limit, clean continuous
  full-width front closed line does not exist in this set), AH-v2 211×70,
  GK-v2 211×32, EE-vector 200×113.
- THREEQUARTER-3, labelled 3/4-source, NEVER front: AH34 211×100,
  MBP34 211×36 (broken line — gap NOT bridged, gate continuity correctly
  does not apply to it as a continuous line), SMILE34 179×113 (face/shadow
  blocks attached, reference only).
Correction made during this run, not hidden: the first FRONT-4 fitted
contact placed patches at native size (GK 531px wide), overstating them.
It was regenerated at the true v2 fitted sizes above; the mouth-only
strips are native patches, the fitted strips are placed sizes.

## 4. Other Titans / Batman / Superman — BLOCKED, plainly
- Other Titans extractions: 0/5 (Cyborg, Starfire, Raven, Beast Boy, Slade
  are counts, not extractions). A fresh public web search this run found
  only clipart/gallery pages (Pikist, PNGWing, PNGEgg) and character pages
  — no pullable model-sheet mouth chart for any of them. Those clipart
  files were NOT pulled: they are not source mouth charts and would be
  the wrong drawings. The earlier local extraction route for the user's
  repo was flagged by a safety check in a prior session; I did not use
  it and did not use a replacement download route.
- Batman: 0 verified mouth files. Superman: 0 verified mouth files.
  Prior finding stands: Batman mouth guide exists only as a Heritage
  Auctions sale lot, Superman sheets only as sale/gallery pages — sales,
  not pullable files, not pulled.
- Multi-head expression-sheet segmentation: 0/1, still owed. The
  RBNEXPRES sheets were not located on local disk in this run (a full
  workspace find was started and killed as too slow; no sheet file was
  opened or segmented). Eligible route needed: Mars supplies the
  expression-sheet files, or the parent runs the pull through an eligible
  route — then this pipeline segments them automatically.
- Still owed elsewhere, unchanged: front AH shout with teeth 0/1,
  OH/OO 0, clean continuous front MBP line 0/1 (the vector line is
  continuous, but it is fitted from the same short/fragmented source —
  it does not create a new full-width drawing), audio-driven timing 0/1,
  AH corner spike removal 0/1 (in the approved version; the lineclean
  version does not touch AH).

## Files (all new, in this folder)
- `mouth_pipeline.py`, `gate_mouth.py`, `build_packs.py`
- `pahgo-lineclean-20261031.gif`, `frames_lineclean/` (30 frames)
- `lineclean-before-after-20261031.png` (approved vs vector, normal + 3×)
- `packs/mbp-clean-line-patch.png`, `packs/mbp-clean-line.svg`,
  `packs/ee-clean-line-patch.png`, `packs/ee-clean-line.svg`,
  `packs/*-pipeline-patch.png`
- `pack-LINECLEAN-PAHGO-{mouthonly,fitted}-20261031.png`,
  `pack-FRONT-4-{mouthonly,fitted}-20261031.png`,
  `pack-THREEQUARTER-3-{mouthonly,fitted}-20261031.png`
- `measurements-clean-pipeline-20261031.json`, this report

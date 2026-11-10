# Transparent Plates Sweep — 2026-10-31

Ordered by Mars 2026-10-31 21:23 CDT, replying to the ground-feet gate report.
Owned plainly: this blocker was known — clips-v7c flying frames were
full-canvas RGB, not transparent plates, so they could not be alpha-bbox
gated, and the airborne proof was only a lifted apose plate, labelled as
such — and it was not cleared. It is cleared here, for the plates below.

## Method (standing clean-cut rule, not invented)
`convert_plates.py` in this folder, method = `slice_clean.py` clean-cut
rule applied to the WHOLE figure as one silhouette (pieces are NOT
re-sliced; sliced/ and sliced-clean pieces already exist):
1. bg = median of four corners (flat grey 128 on v7c plates)
2. mask = distance from bg > 30 (keeps white art AND black outlines)
3. closing 3x3 x2 + hole fill, components area >= 800, union
4. 1px alpha feather + fringe decontamination; interior = original colour,
   never recoloured; light/shadow/bleed on separate layers (none in these plates)
5. NO-CROP: output keeps the ORIGINAL canvas size (1100x1500), never clipped.
rembg check: rembg is present in the rig venv but the check run stalled
on model load and was stopped; it was NOT used as the conversion, per the
slice_clean doc (on grey it eats white suit edges, on black it eats the
black cape). The scripted method is the standing default for flat sheets.

## Inventory — canonical plates/clips only, not proofs/contacts/GIFs
Proofs, contacts, before/after sheets and crops are display composites,
not plates, and were NOT converted (converting them would destroy the
proof). Superseded pose versions (reposes v3-v7, joint v7) were NOT
converted — superseded plates are not used, so they do not need transparency.

| Group | Total | Was transparent | Was opaque, converted here | Status |
|---|---|---|---|---|
| clips-v7c (current, incl. flying 4) | 23 | 0 | 23 | BLOCKER, now clear |
| clips-v7c-clean-20261031 (current clean, incl. flying 4) | 17 | 0 | 17 | BLOCKER, now clear |
| clips (legacy, incl. flying 4) | 25 | 0 | 25 | Converted |
| clips-v7 (legacy) | 5 | 0 | 5 | Converted |
| reposes-v7c-clean, single figures only | 23 | 0 | 23 | Converted |
| **Conversion set total** | **93** | **0 (0%)** | **93 (100%)** | **Done** |
| Already transparent, no conversion needed: sliced 31, cut-limbs 32, pack1 + pack1-clean 50, pose-dialects singles 8, ginyu singles 18 | 139 | 139 | 0 | Already clear |
| FLA pieces, sliced-clean D-xray-angle-ref (fla-front/back/3quarter + xray-fla) | 302 | 302 | 0 | Already clear — FLA was already transparent, despite the earlier order |
| NOT plates, not converted: reposes-v7c-clean before-after/crops 11, pose-dialect contact 1, ginyu contacts 9, all proof/contact/GIF outputs | — | — | — | Not plates |

After this sweep, plates needing transparency: 93 + 139 + 302 = 534 total,
534/534 = 100% transparent. (Proofs/contacts excluded by definition above.)

## Verification — every converted file, measured, not claimed
- All 93 outputs: mode RGBA, alpha min 0, alpha max 255, alpha>10 px
  >= 50,000, canvas size unchanged from source. BAD list: [] (empty).
- Full per-file record: `conversion-manifest.json` (source, output, bg,
  size, alpha_px, alpha min/max, bbox).

## Flying plates (the ground-gate blockers)
12 flying plates converted (4 v7c + 4 v7c-clean + 4 legacy clips):
- flying-01 hover: bbox x247-876, y252-1310, alpha 395,901 (v7c)
- flying-13 soar: bbox x1-1098, y252-1310, alpha 397,640 (v7c)
- flying-25 dive: bbox x182-896, y35-1310, alpha 405,622 (v7c)
- flying-37 hover: same as 01 (duplicate frame in source)
- v7c-clean and legacy versions: same bboxes, alpha 390,111-406,478.
- FLAG, honest: soar arms-out bbox starts at x=1 in the SOURCE plate
  itself — arms nearly touch the canvas edge before conversion.
  Conversion kept the full 1100px canvas and clipped nothing beyond
  the source; a wider re-render of the soar pose would need a new
  source plate, not a conversion fix.

## Re-gate — real flying pose, not a lifted apose plate
`ground_gate.py` (ground-feet-placement-wire100-20261031/) run on the
converted flying-13-soar plate:
- mode AIRBORNE, ground_y 1500, flight line "soar 190px above ground
  line, arms out"
- measured from alpha: bbox [1, 252, 1098, 1310], feet_y 1310,
  height 190, alpha 397,640
- verdict: PASS, exit 0.
- Scaled proof composite (550x750 pasted at 275,100, ground line
  y=1300): feet 755, height above ground 545, airborne PASS.
- First re-gate attempt measured the opaque grey canvas (feet 1499,
  false FAIL) — that was a measurement bug in my proof script, owned
  here, fixed by measuring plate alpha only, and confirmed by the
  real ground_gate.py PASS above.

## Files
- `plates/` — 93 transparent RGBA plates, flat names
  `sourcefolder__filename.png` (provenance in the name)
- `convert_plates.py` — converter
- `conversion-manifest.json` — per-file measurements
- `transparency-contact-20261031.png` — top row grey originals,
  bottom row converted on checkerboard (flying-01, flying-13, flying-25,
  walk-01, apose, punch impact; figure intact in all 6)
- `flying-regate-proof-20261031.png` — soar proof, red ground line y=1300

## Status
Approval 0/1 for the transparent-plate set. No repo push (landing is a
separate step). No original deleted, no existing file overwritten.
Overlap note: a separate ground-gate-complete workstream (ordered
21:24 CDT) was told to use this sweep's output rather than duplicate
the conversion — that overlap is noted plainly, not hidden.

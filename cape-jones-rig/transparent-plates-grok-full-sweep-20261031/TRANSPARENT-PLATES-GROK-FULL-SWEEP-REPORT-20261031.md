# Transparent Plates — Grok Full Sweep — 20261031

Mars order, 2026-10-31 23:01 CDT: cut the backgrounds out of all the sheets
made earlier with Grok and pushed to the repo, cleanly, including cape sheets.
The earlier transparent-plates sweep is SAVED PERFECT and was NOT touched.

## Scope, plainly — Mars's estimate vs the verified count

- Mars estimated "300 or 400 sheets". That is NOT the verified count.
- Verified repo sheet library, `characters/sheets/` in the study clone
  (`~/workspace/cape-jones-flying/`, read-only, tracked by git):
  **245 sheet images, all opaque before this sweep.**
- If Mars has Grok sheets somewhere else (uploads, another folder, another
  branch), they are NOT in this set — that is an open question, not a gap
  hidden in the numbers below. Nothing else on disc was counted as a "sheet".

## What was done here (new dated folder, no original touched, no push)

- Method: standing clean-cut rule only (`slice_clean.py` logic), applied to
  the WHOLE sheet as one plate, not re-sliced into pieces:
  bg = median of four corners, mask = distance from bg > 30,
  closing 3x3 x2 + hole fill, components >= 800px unioned,
  1px feather + fringe decontamination, interior = original colour,
  never recoloured, output keeps the ORIGINAL canvas size (no-crop).
- rembg was NOT used in this sweep. The clean-cut doc warns it eats white
  suit edges on grey and black cape on black; no rembg check beat the
  scripted cut on these sheets, so no rembg claim is made.
- One plate file came out 0 bytes in an interrupted first run
  (`fla-packs/fla-3quarter-front.png`); it was re-converted cleanly and
  re-verified. A second check found exactly one bad file in the whole set,
  that one, now fixed.

## Results — 208/208 converted, 0 failed

| Group | Sources | Converted here |
|---|---|---|
| root (main sheets 01–10) | 10 | 10 |
| backgrounds | 37 | 0 — EXCLUDED, see below |
| color-keys | 6 | 6 |
| exposure-sheets | 10 | 10 |
| fla-packs | 102 | 102 |
| layout-line-art | 5 | 5 |
| model-sheets | 7 | 7 |
| prop-scale-sheets | 2 | 2 |
| props | 19 | 19 |
| storyboards | 5 | 5 |
| variations | 40 | 40 |
| viseme-charts | 2 | 2 |
| **TOTAL** | **245** | **208** |

- Unique plate files: **197**, because 11 fla-packs sources are byte-identical
  duplicates in the repo (jojo-packs vs jojo-packs-2, same 11 stems:
  recent-2e9kj, D3pmc, MAHyh, UgepP, ZxEwS, a3jha, etaPY, mANuo, qIxLo,
  smAFI, w2Zh1). Each duplicate source is mapped to the same plate in the
  manifest — no content is missing, 208/208 sources are covered.
- Quality gate (alpha fraction): **204/208 PASS**, 4 CHECK-high, 0 CHECK-low,
  0 FAILED. All 208 outputs are RGBA, original canvas size, alpha min 0.
- CHECK-high 4 (alpha 98.2–99.6%): props prop-8LjQY, prop-oCpSw,
  prop-rY6iH, prop-xyug7. These are full-frame / full-bleed images, not
  objects on a background — prop-xyug7 viewed: a full-frame abstract
  pattern. There is almost no background to cut, so the plate is
  essentially the original. That is a property of the source, not a cut
  failure, but do not call those 4 "cleanly cut objects".
- Cape sheets, name-matched: 08-body-parts-limbs-capes (plate alpha 39.6%,
  viewed — clean, figures and all 5 cape forms intact, background gone),
  exposure-sheet-7-cape (53.7%), cape-jones-tpose-front.png (23.5%),
  cape-jones-tpose-front-alt.png (59.5%). All 4 converted.
- Weakest plate, stated plainly: 09-hero-shot-black (black hero on black
  background, alpha 27.6%). The cape shape is retained via hole-fill, but
  its edge shows colour fringe (blue/pink) at zoom — black-on-black edge
  decontamination, not a clean edge. Usable, not perfect. A better method
  for this one sheet is still owed if Mars wants it perfect; it was not
  hand-fixed here, because hand-fixing would break the clean-cut rule.

## Backgrounds — why 37 were NOT cut

The 37 `backgrounds/` images ARE backgrounds/rooms (e.g. batch-KKGuh).
Cutting their background out would destroy them. They are listed as
`excluded-background` in the manifest, kept as-is, not silently skipped.
If Mars wants a specific background cut anyway, that is a separate order
per background.

## Labelled / organised — the answer Mars does not know, plainly

Sheets:
- Organised by repo group folder: **245/245 = 100%**
- Organised into sliced-clean piece folders (pieces cut per sheet):
  **140/245 = 57.1%**
- NOT organised into piece folders: **105/245 = 42.9%**
  - Of those 105: 37 are backgrounds (excluded above), **68 are figure
    sheets (68/208 figure sheets = 32.7%)** that had no piece folder.
  - Those 68 now have a transparent whole-sheet plate in this sweep,
    organised by group folder — but they are STILL not sliced into
    individual pieces. A whole-sheet plate is not piece organisation.

Pieces (sliced-clean, 2,854 pieces from the 140 sliced sheets):
- Organised by sheet folder: **2,854/2,854 = 100%**
- Carrying a named provisional class (WHITE-SUIT / BLACK-CAPE / COWL /
  SKIN / XRAY): **1,794/2,854 = 62.9%**
- MIXED/UNCLASSIFIED (provisional label only, needs a human eye):
  **1,060/2,854 = 37.1%**

This sweep's own plates:
- Organised by group folder: **208/208 sources = 100%** (197 files, see
  duplicates above). Sheet-level label = source filename + group only.
- Piece-level semantic labels inside these plates: **0/208** — these are
  whole-sheet plates, not sliced pieces. Slicing the 68 unsliced figure
  sheets into labelled pieces is a separate job, not done here.

## Totals after this sweep (do not mix denominators)

- Prior saved-perfect sweep plates: 534/534 = 100% transparent (unchanged)
- This sweep, new unique plates: 197
- Unique transparent plates total: 534 + 197 = 731
- Sliced pieces already transparent: 2,854 (separate category, unchanged)
- Sheets still with no transparent plate: 0/208 figure sheets (37
  backgrounds excluded by definition, above)

## Files

- `plates/` — 197 RGBA plates, grouped by source group
  (root / color-keys / exposure-sheets / fla-packs / layout-line-art /
  model-sheets / prop-scale-sheets / props / storyboards / variations /
  viseme-charts)
- `conversion-manifest.json` — per-source record: source, group, status,
  output file, size, alpha px, alpha fraction, bbox, quality
- `transparency-contact-grok-full-sweep-20261031.png` — 35 samples across
  all groups: grey original on top, transparent plate on checkerboard
  below, per sample (cape sheets first, then up to 3 per group)
- `convert_grok_sheets.py`, `convert_shard.py`, `build_manifest.py`,
  `build_contact.py` — builders, kept in this folder
- Originals untouched: sources live in the read-only study clone; nothing
  in `~/workspace/cape-jones-rig/transparent-plates-sweep-20261031/`
  (saved perfect) was overwritten, and nothing was pushed to any repo.

## Approval

Approval **0/1** for this full Grok sweep. The earlier saved-perfect sweep
stands separately and is not re-approved or changed by this report.

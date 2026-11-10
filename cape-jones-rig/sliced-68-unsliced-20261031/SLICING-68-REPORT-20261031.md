# Slice the 68 unsliced figure sheets — REPORT 2026-10-31

Mars ordered 2026-10-31 23:26 CDT, replying to the Grok full sweep report.
He confirmed: it is just the 245 sheets in the repo, Grok sent/staged all
of them, and yes, he wants all 68 unsliced figure sheets sliced.

## Count correction — do not mix denominators
- Total sheets in repo: **245 = 208 figure sheets + 37 backgrounds**
- Already sliced into pieces before this job: **140 sheets**
- NOT sliced before this job: **68 figure sheets + 37 backgrounds**
  - Backgrounds are rooms. They are NOT sliced, by design. Cutting a
    room's background would destroy it. They stay excluded, with reason.
- This job: **68/68 figure sheets sliced = 100%**
- New total after this job: **208/208 figure sheets sliced = 100%**
- Backgrounds excluded: **37/37, with reason (rooms)**

## Method (standing clean-cut rule, slice_clean.py logic)
- Input = the transparent plate from the Grok full sweep (background
  already cut, interior = original colour, never recoloured).
  No original sheet was touched, no already-sliced sheet was touched,
  no background was sliced, 09-hero-shot-black was NOT hand-fixed here
  (that sheet is a separate question for Mars, per the task).
- Components = connected components of alpha > 10, area >= 800 px,
  8-connectivity. No hand-drawn rectangles.
- Pieces = component cropped to its own bbox, pixels copied exactly
  from the plate (RGBA unchanged).
- Naming = existing sliced-clean convention: rows clustered by
  component centre-y with a >150 px gap, left-to-right, Row{r}_{n}.png,
  plus a MANIFEST.json per sheet (with provisional_class per piece).
- Provisional class: ONLY where the sheet type makes it clear, never
  guessed as a body part:
  - storyboards -> storyboard_panel
  - layout-line-art -> layout_panel
  - color-keys (large figures) -> colour_variant_figure
  - viseme-charts (grid heads) -> viseme_head_cell (NOT a phoneme)
  - props (dominant object only) -> prop_main_object
  - variations tpose-front (single comp) / tpose-front-alt (largest)
    -> full_figure_tpose
  - everything else -> MIXED/UNCLASSIFIED (human eye needed)
  - Fla-pack pieces are therefore MIXED/UNCLASSIFIED: a pack component
    may be a torso, a limb, a hand, a cape, or a full pose, and
    position alone does not tell which. Labelling a 390x734 torso as
    a "full figure" would be a guessed label, and was NOT done.
    Body-part labelling for fla-packs is still owed as a human-eye pass.

## Exception, documented, not hidden: color-key-sheet-5
Its 5 figures touch at the fingertips and form ONE alpha component
(845,913 px). Component slicing alone would give 1 merged strip, not
5 individual figures. That strip was split at the 4 vertical midpoints
between the 5 figure centres (x = 360, 720, 1080, 1440 on the 1792-wide
sheet), giving 5 colour_variant_figure pieces. This is a grid split of
a merged row, NOT a hand-drawn body-part rectangle.
- Defect caught on viewing the first grid split: neighbour slivers at
  the touch points (a thin line beside the cyan figure, an orange bit
  beside the stormy figure). Fixed: each slab piece keeps ONLY its
  largest connected component, dropping neighbour slivers. Re-viewed:
  all 5 figures clean, no slivers.

## Duplicates — counted as sheets, flagged as content
22 of the 68 source entries are byte-identical repo duplicates:
11 jojo-packs vs jojo-packs-2, 11 lounge-packs vs lounge-3quarter clean.
Each duplicate source got its OWN sheet folder (suffix __dup2) with its
own pieces, so the count is 68/68 sheets, not 46 unique contents.
Duplicate pieces: 398. Unique-content pieces: 566.
Duplicate definition, clarified after a verification check: there are
22 plate-md5 duplicate pairs (11 jojo-packs vs jojo-packs-2, 215 second-
copy pieces, flagged by both duplicate_of and duplicate_md5_of; plus
11 lounge clean vs lounge pairs, 183 second-copy pieces, flagged by
duplicate_md5_of only, because their stems differ). Counting only the
duplicate_of field alone would give 11 sheets / 215 pieces and a
wrong unique total of 749 — that field alone is NOT the duplicate
count. The correct duplicate-content count is 22 sheets / 398 pieces,
unique-content pieces 566.

## Counts (this job)
- Sheets sliced: **68/68 = 100%**
  - fla-packs 44, color-keys 6, layout-line-art 5, storyboards 5,
    props 4, variations 2, viseme-charts 2
- Total new pieces: **964** (964 piece PNGs on disk, 0 missing)
  - Unique-content pieces: 566, duplicate-sheet pieces: 398
- Named (clear provisional class): **114/964 = 11.8%**
  - colour_variant_figure 30, storyboard_panel 30, viseme_head_cell 29,
    layout_panel 20, prop_main_object 3, full_figure_tpose 2
- MIXED/UNCLASSIFIED (human eye needed): **850/964 = 88.2%**
  - Almost all of this is fla-packs (796 pieces), where body-part
    identity is not clear from geometry alone.

## New combined totals
- Sliced sheets: **208/208 figure sheets = 100%** (140 old + 68 new)
- Sliced pieces: **3,818 total** (2,854 old + 964 new)
  - Named: **1,908/3,818 = 50.0%** (1,794 old + 114 new)
  - MIXED/UNCLASSIFIED: **1,910/3,818 = 50.0%** (1,060 old + 850 new)
  - Note: the old named rate was 62.9%; the new batch is mostly
    fla-pack pieces, which are honestly mostly MIXED, so the combined
    named rate falls to 50.0%. That is a labelling honesty result,
    not a slicing failure — the pieces themselves are cut.

## Still NOT done / owed after this job (not claimed)
- Body-part labelling for fla-pack pieces (human eye) — the 850 MIXED
  pieces here, plus the 1,060 MIXED pieces from before.
- 37 backgrounds: excluded, rooms, not sliced.
- 09-hero-shot-black: not hand-fixed here, separate Mars question.
- Approval 0/1 for this 68-sheet slicing set separately.
- No repo push by this job.

## Files (new folder, nothing overwritten)
- Slicer: sliced-68-unsliced-20261031/slice_68.py
- Per-sheet folders + MANIFEST.json: sliced-68-unsliced-20261031/sheets/<group>/<sheet>/
- Top manifest: sliced-68-unsliced-20261031/SLICING-MANIFEST-20261031.json
- This report: sliced-68-unsliced-20261031/SLICING-68-REPORT-20261031.md
- Contacts (viewed): contact-largest-piece-per-sheet-20261031.png
  (68 tiles, largest piece per sheet), contact-color-key-sheet-5-grid-split-20261031.png
  (5 figures, clean after sliver fix), contact-sample-<group>-20261031.png
  (first 6 pieces of the first sheet per group).

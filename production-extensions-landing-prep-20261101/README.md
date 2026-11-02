# Production Extensions — landing prep, 2026-11-01 (PROPOSAL ONLY — NOT LANDED)

Source folder `production-extensions-20261101/` was NOT modified: nothing renamed,
deleted, or force-pushed there. Approval 0/1 throughout. Original uploads untouched.

## BLOCKER — read first

This prep was supposed to live in a NEW folder
`~/workspace/cape-jones-rig/production-extensions-landing-prep-20261101/`.
That folder could NOT be created: every write under `~` fails with
`Disk quota exceeded` (Errno 122), even though the filesystem reports 39 GB free
— so this is a quota, not a full disk. No files were deleted to work around it
(the task forbids deletions). The complete prep is staged at
`/tmp/production-extensions-landing-prep-20261101/` (ephemeral — copy it to the
intended workspace folder once quota is cleared; the files below are identical
to what belongs there). All counts and verdicts in this report stand on their own
even if the staging folder is lost.

## 1. Inventory — what was actually in the folder

- 33-piece index: `piece-index-20261101.json` / `.csv` (33 entries, 22:45).
- 34-piece index: `slices/piece_index.json` / `.csv` (34 entries, 22:53).
- On disk in `slices/`: 58 PNGs = 55 piece PNGs + 3 non-piece PNGs
  (`piece_contact_sheet.png`, `sheet_flex_soles_limbs_bgremoved.png`,
  `sheet_heads_torsos_hands_boots_bgremoved.png`).
- Full per-file inventory (size, md5, dimensions, mode, mtime):
  `inventory.json` / `inventory.csv` (58 rows).
- Timestamps prove the overwrite: 33-pass piece files are dated 22:43–22:44,
  34-pass files 22:52–22:53. The 12 names shared by both indexes exist on disk
  ONLY as the later 34-pass re-crop — the 33-pass bytes for those 12 names are
  gone. Byte-identity between the two sets therefore CANNOT be verified for
  shared names and is NOT claimed anywhere here.

## 2. How the two sets relate (per piece)

- Byte-identical between sets: 0 pairs provable (see above — shared-name
  originals are overwritten; distinct-name files are re-crops with different
  sizes/padding, hence different md5s).
- Same drawing, different name (bbox match within 3 px, or pixel-verified):
  32 of the 33 index entries map onto a 34 entry. Every sheet-2 region exists
  in both sets; only the labels differ (L/R vs A/B, `Boot` vs `Boot_Front`,
  `Boot_Tread` vs `Boot_Sole_Tread`, sole names, and the crossed pairs below).
- Different drawings: the two torso drawings (X vs Y), the pelvis dome vs
  `Pelvis_Whole`, and every non-matching region pair (trivially).
- Sheet-1 cut difference: the 33 pass left the straight arm unsplit
  (`Arm_Gauntlet_Fist_Cut`, bbox 1525–1941); the 34 pass splits it at the
  elbow-ball valley x=1725 into `UpperArm_BentCut_S1` + `Gauntlet_Fist_Cut_S1`.
  The 34 pass also splits the leg at knee-ball valley x=478 with a 6 px overlap
  (`Thigh_Cut_S1` / `Shin_Boot_Cut_S1`); the 33 leg halves cut at x≈476/466.
- Two extra crossed-label errors in the 33 set (found by bbox + visual check,
  NOT part of Mars's two picks, resolved by content in the canonical set):
  33 `Neck_Ring` is actually the hooded head (34 `Head_ThreeQuarter`,
  bbox [579, 39, 742, 295]) and 33 `Head_ThreeQuarter` is actually the purple
  cowl ring (34 `Neck_Ring`, bbox [912, 95, 1061, 250]); 33 `Hand_Fist` is
  actually the open palm (34 `Hand_OpenPalm`, bbox [1349, 512, 1675, 746])
  and 33 `Hand_OpenPalm` is actually the fist (34 `Hand_Fist`,
  bbox [1065, 554, 1311, 744]). Visual check of the on-disk 34 files confirms
  the 34 labels: hooded head, purple ring, fist, open palm.
- Flex crops: 34 `Flex_Front` bbox [118, 32, 788, 509] and `Flex_ThreeQuarter`
  [843, 24, 1328, 502] are looser crops of the same drawings as the 33 entries
  (33: [118, 33, 782, 509] and [847, 34, 1312, 501]); on-disk sizes 679×486 /
  494×487 vs 33 index sizes 664×476 / 465×467.

## 3. The two named conflicts — verdicts with pixel evidence

Method: trim each PNG to its opaque bbox, search shifts ±4–6 px, report the
best alpha IoU and mean RGB difference on common opaque pixels. Same-drawing
pairs score RGB 0.00 (identical colour content); different drawings score ~95–104.
Blob overlap alone does NOT prove sameness (different drawings still overlap
at IoU ≈ 0.80) — RGB is the discriminator.

### Conflict 1 — Torso_LeanBack vs Torso_Front: GENUINELY DIFFERENT DRAWINGS
- Drawing X (wide torso, neck stump on top, purple V emblem):
  33 name `Torso_Front` (bbox [1144, 66, 1552, 304], file 420×250, survives),
  34 name `Torso_LeanForward` (bbox [1144, 67, 1550, 303], file 415×245).
  Pixel check X-vs-X: alpha IoU 0.9771, RGB diff 0.00 → same drawing.
- Drawing Y (tall torso, leaning to the side, abs visible):
  33 name `Torso_LeanForward` (bbox [1578, 48, 1895, 368]),
  34 name `Torso_LeanBack` (bbox [1578, 48, 1894, 367], file 325×328).
  Pixel check X-vs-Y (`Torso_Front` vs `Torso_LeanBack`): RGB diff 94.97;
  (`Torso_LeanForward` vs `Torso_LeanBack`): RGB diff 94.21 → different drawing.
- So `Torso_LeanBack` ≠ `Torso_Front`. The real collision is that BOTH passes
  used `Torso_LeanForward` — for X (34) and for Y (33). Mars is choosing a
  naming SCHEME for two pieces that both land, not deleting one.
- Correct name (evidence): Option A (`Torso_LeanForward` / `Torso_LeanBack`)
  is recommended: X leans forward with a neck stump (not a straight front —
  a straight front torso exists only inside `Flex_Front`), Y leans back/side,
  and the 34 scheme is content-correct on the two checkable crossed pairs above.

### Conflict 2 — Pelvis_UnderView vs Pelvis_Top_Dome: SAME DRAWING
- One dome with two black leg-socket openings, sheet-2 bbox [570, 332, 824, 535]
  in both indexes. Files: 33 `Pelvis_Top_Dome.png` 267×215 (survives, 22:44),
  34 `Pelvis_UnderView.png` 263×212 (22:53). Trimmed size identical 255×204,
  alpha IoU 0.9692, RGB diff 0.00 → same drawing, two names.
- Control: dome vs `Pelvis_Whole` (whole pelvis/brief): RGB diff 103.74 →
  different drawing; `Pelvis_Whole` lands regardless.
- Correct name (evidence): Option A (`Pelvis_UnderView`) recommended — the
  visible sockets are an underside view; `Top_Dome` describes only the outline.
  Either name is defensible; only one lands, the other becomes an alias.

## 4. Canonical set proposal (34 pieces)

Rule: canonical bytes are the 34-pass re-crops throughout (consistent
bg-removal method, documented split points, content-correct labels), with
33 names recorded as aliases. The 3 pending pieces carry provisional Option A
names; under Option B only their filenames change (bytes unchanged):
`Torso_LeanForward` → `Torso_Front`, `Torso_LeanBack` → `Torso_LeanForward`,
`Pelvis_UnderView` → `Pelvis_Top_Dome`.
Full table with bboxes, sizes, md5s: `canonical-index.json` / `.csv`.
Sheet 1 (12): Flex_Front, Flex_ThreeQuarter, Flex_Back, Sole_Boot_Flat_L,
Sole_Boot_Flat_R, Boot_Angled_Sole_L, Boot_Angled_Sole_R, Thigh_Cut_S1,
Shin_Boot_Cut_S1, UpperArm_BentCut_S1, Gauntlet_Fist_Cut_S1, Arm_Bent_Flex_S1.
Sheet 2 (22): Head_Front, Head_ThreeQuarter, Neck_Ring, Torso_LeanForward*,
Torso_LeanBack*, Pelvis_Whole, Pelvis_UnderView*, Belt_Block, UpperArm_L,
UpperArm_R, Gauntlet_L, Gauntlet_R, Hand_Fist, Hand_OpenPalm, Hand_Pointing,
Thigh_L, Thigh_R, Shin_L, Shin_R, Boot, Boot_Angled_S2, Boot_Tread.
(* = pending Mars pick.)

## 5. Rename / dedupe map (67 index rows = 33 + 34)

`rename-dedupe-map.json` / `.csv`, one row per index entry:
- CANONICAL: 31 (34-pass names already canonical, pick-independent).
- PENDING_MARS_PICK (provisional Option A): 3.
- SAME_DRAWING_RECROP_OVERWRITTEN: 12 (shared names; 33 bytes lost, 34 re-crop lands).
- DUPLICATE_SAME_DRAWING_DIFFERENT_NAME: 19 (surviving 33 re-crops; excluded).
- SAME_REGION_DIFFERENT_CUT_NOT_PIXEL_IDENTICAL: 1 (`Shin_Boot_Cut` →
  `Shin_Boot_Cut_S1`; best-shift RGB diff 30.36, IoU 0.9185 — same leg region,
  different cut edge + rendering; S1 version lands).
- SUPERSEDED_BY_SPLIT_PAIR: 1 (`Arm_Gauntlet_Fist_Cut` → `UpperArm_BentCut_S1` +
  `Gauntlet_Fist_Cut_S1`; excluded, not a separate piece).
- Thigh/Arm cut pairs ARE pixel-identical on overlap (Thigh RGB 0.00,
  IoU 0.9559; Arm RGB 0.00, IoU 0.9497) despite different cut edges/padding.

## 6. What would land once Mars picks — and what would NOT

See `landing-manifest.md` for the file-by-file list. Counts:
- WOULD LAND: 34 canonical piece PNGs + canonical index JSON + CSV = 36 files.
- WOULD NOT LAND (this pick): 21 duplicate on-disk piece PNGs (all 33-only
  filenames), 2 `.blend1` files, 269 `frames/` scratch files, 3 non-piece
  slices PNGs (contact sheet + 2 bg-removed sheets, QA reference only),
  and the still-unresolved parallel collisions — pose tables (long vs wide),
  flex spin vs camera-turnaround clips, sole-kick vs kick-sole-view clips —
  which need their own picks and are NOT decided here.
- NOTHING in `production-extensions-20261101/` was changed by this prep.

# Duplicates + Organization — 10 duplicate-finding + 5 organization methods
Mars ordered 2026-10-31 23:38 CDT, replying to the 68-sheet slicing contact.
NO DELETIONS AT ALL. Keep/delete below are SUGGESTIONS ONLY — Mars picks keep vs delete after seeing the organized list. No repo push.

## Scope actually run (verified on disk, not claimed totals)
- Sheets: 245 (cape-jones-flying/characters/sheets, images only)
- Plates: 290 in the two verified plate folders (197 Grok sweep + 93 old sweep). Parent summary quoted 731 plates total across all plate sets; this run covers the 290 in those two folders, NOT 731 — do not quote 731 as run here.
- Pieces: 3,818 (2,854 old sliced-clean + 964 new 68-sheet slices)
- Total records: 4,353. Candidate pairs via LSH bucketing (dHash/aHash 32-bit chunks, size, name, md5): 57,206.

## 10 duplicate-finding methods — ALL RUN
- D1 exact MD5 hash: 474 groups, 975 members, 501 extra copies
- D2 byte size + dimensions: 475 groups, 977 members, 502 extra
- D3 perceptual dHash, Hamming ≤5: 480 groups, 1,029 members, 549 extra
- D4 average hash, Hamming ≤10: 500 groups, 1,391 members, 891 extra
- D5 colour histogram, cosine >0.985: 388 groups, 2,440 members, 2,052 extra (LOOSE — see below)
- D6 alpha silhouette IoU >0.92: 575 groups, 2,120 members, 1,545 extra (LOOSE)
- D7 normalized name: raw 398 groups, 4,104 members — FLAWED for pieces (Row1_1 etc. repeat across sheets). Restricted, sheets+plates only, distinctive stems, not Row*: 201 groups, 413 members. Raw D7 is NOT used in the strict union.
- D8 metadata bucket (dims + aspect + alpha bucket + size log): 590 groups, 1,692 members, 1,102 extra (LOOSE)
- D9 downscaled 32×32 pixel MSE <150: 475 groups, 1,114 members, 639 extra
- D10 colour layout 4×4 grid: 534 groups, 2,697 members, 2,163 extra (LOOSE)

## Strict duplicate groups (the organized list) — D1+D2+D3+D4+D9 only, aspect guard ≤3× (except exact MD5)
- 498 groups, 1,420 members, 922 extra copies
- 1,420/4,353 = 32.6% of files sit in a strict duplicate group
- Unique content estimate: 4,353 − 922 = 3,431 files
- By category, members: pieces 1,152, plates 152, sheets 117 (note: one file can be in one group; categories are per member)
- Group sizes: 2×319, 3×124, 4×26, 5×4, 6×3, 7×5, 8×2, 9×4, 10×3, 11×1, 12×1, 14×2, 20×1, 25×1, 27×1, 29×1
- Largest: DUP-0001 same head piece ×29, DUP-0002 belt piece ×27, DUP-0003 plate figure ×25, DUP-0004 torso piece ×20 — Grok drift: the same head, belt, torso, cape art repeated across many different sheets.
- Cross-category proof: same art appears as sheet + plate + piece (e.g. prop-xyug7 pattern, tpose-front-alt, desert/park/kitchen backgrounds) — that is why the count looked like ~300: one piece of art staged in several folders/formats.

## Why loose methods are NOT in the strict union (owned plainly)
Transitive chaining through loose methods merges unrelated art: the all-method union gave 43 giant groups covering 4,286 files — useless. Colour histogram, silhouette IoU, colour layout and raw name matching are reported as candidate/similarity signals only, never as proof of duplication on their own. Same for D8 metadata buckets (same size ≠ same art).

## False positive caught on viewing, fixed in-run
First strict union included DUP-0013: a full city sheet grouped with 2-pixel-high strip pieces, because 32×32 downscaling crushes thin strips to the same grey. Fixed with the aspect-ratio guard (≤3×, except exact MD5): that sheet is now ungrouped, groups 498, members 1,420 (was 1,421). Lesson recorded: downscaled-pixel methods are unreliable for extreme aspect ratios.

## 5 organization methods — ALL RUN
- O1 Taxonomy: category (sheets/plates/pieces) → duplicate group → canonical name. Index: organized/ORGANIZED-INDEX-20261031.json, 498 groups.
- O2 Faceted index: organized/FACETED-INDEX-20261031.csv, all 4,353 files, columns path, category, duplicate group, duplicate status, keep/delete suggestion, canonical name, dimensions, bytes, alpha fraction, aspect, dominant colours, orientation, type tag.
- O3 Rule-based tagging (NOT a claimed AI model): dominant colours (quantized), orientation (portrait/landscape/square), type tag (full_figure if alpha>0.2 else part_or_sparse). True AI embedding (e.g. CLIP) is MAPPING ONLY — no torch/CLIP run on this VM, no AI label claimed.
- O4 Canonical naming: CJ-<category>-<stem>, e.g. CJ-pieces-row1-1, CJ-plates-prop-xyug7. One canonical name per duplicate group, in the index.
- O5 Keep/delete triage, suggestions only: KEEP CANDIDATE = highest resolution, then largest bytes, in each group; all other members = DELETE CANDIDATE. Counts: keep candidates 498 (one per group) + unique files 2,933 = 3,431 keep-side files; delete candidates 922. NOTHING DELETED. Mars decides per group.

## Proofs viewed
- contacts/duplicate-groups-largest-20261031.png (8 largest groups, first 4 members each)
- contacts/duplicate-groups-cross-category-20261031.png (8 cross-category groups)
- contacts/duplicate-groups-pieces-20261031.png (8 pieces-only groups)

## Still owed / not claimed
- Mars keep/delete picks per group (the whole point of the next step; a separate review UI workstream was spawned by the parent at 23:39 CDT — this job is the data for it, not the UI).
- Semantic body-part labelling of MIXED pieces (1,910 combined MIXED pieces) — duplicate grouping does not label body parts.
- True AI embedding tagging (CLIP etc.) — mapping only, needs a model run.
- Plates beyond the 290 verified here, if Mars wants the full 731-plate claim re-run over every plate folder.

## Status
- Duplicate-finding set: approval 0/1 separately.
- Organization set: approval 0/1 separately.
- Deletions: 0. Originals untouched. No repo push.

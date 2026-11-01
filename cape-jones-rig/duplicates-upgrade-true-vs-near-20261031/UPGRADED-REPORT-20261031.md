# Duplicate pipeline upgrade: TRUE vs NEAR-DUPLICATE — 2026-10-31

**Standing order obeyed: NO DELETIONS. 0 deletions in this job. Log only, organize only, learn only. No deletion list exported as approved.**

## The defect Mars named, in plain words
A couple of items were grouped in the same row / pattern row, but they are actually
two different items with slight differences. Example: DUP-0001, the head pieces.
Same row name (Row1_1 / Row1_10 / Row1_3), same head outline, but different
interior detail, different size, different file bytes. The old strict union
(D1+D2+D3+D4+D9) merged them because silhouette and hash were close.
That is a false merge, not a true duplicate.

## Result — re-scored all 498 old strict groups, 1,420 members, 0 files missing
- TRUE subgroups: **474 subgroups, 975 files = 68.7%** of old members
- NEAR-DUPLICATE files (similar pattern/row, different detail): **440 files = 31.0%**
- OTHER files (old grouping was a false merge, split out alone): **5 files = 0.4%**
- Groups fully true (no near, no other): **295 / 498 = 59.2%**
- Groups containing near files: **201 / 498 = 40.4%**
- Groups containing other files: **3 / 498 = 0.6%**
- Changed vs previous list: 445 of 1,420 old members (31.4%) are NOT true duplicates.
  The previous 498-group / 1,420-member count stays as the "similar" count;
  the new true count is 474 subgroups / 975 files. Do not quote 1,420 as true duplicates.

## Verdict rule (conservative, by design)
- TRUE = exact file MD5, OR same dimensions + pixel MSE == 0 + silhouette IoU >= 0.99
- NEAR = in an old group but not TRUE, with dHash <= 10 OR 64x64 grey MSE < 800
  OR silhouette IoU >= 0.85 — similar pattern/row, different detail/colour/piece
- OTHER = in an old group but below all NEAR thresholds — old merge was wrong

## Methods — all RUN (M1–M12), except mapping-only noted
- M1 exact MD5 (full file)
- M2 pixel-exact (same dims, RGBA MSE == 0)
- M3 dHash 64-bit, Hamming distance
- M4 aHash 64-bit, Hamming distance
- M5 downscaled 64x64 SSIM-proxy: MSE + correlation on grey
- M6 colour histogram cosine (16 bins x RGB)
- M7 alpha silhouette IoU (128x128, alpha > 10)
- M8 edge-map IoU (numpy gradient magnitude, 128x128) — NOT ORB
- M9 row/pattern-aware rule: same RowX_N name + same row position is NOT
  evidence by itself; it is a COLLISION FLAG when pixel scores disagree
- M10 difference map: mean/max abs RGB diff on common canvas
- M11 learning/feedback: Mars's DG-01 + DG-23 picks were exact-MD5 groups,
  so exact-MD5 weight goes UP, row-name weight goes to 0 (old D7 was flawed
  for pieces: Row1_1 repeats across sheets)
- M12 incremental index: new groups carry true/near label + score, so a later
  run re-scores only changed files (JSON index in organized/)
- MAPPING ONLY, not counted as run: ORB/SIFT feature matching, CLIP embedding
  — no cv2 / torch on this VM, no such run claimed

## Proof example — DUP-0001 head pieces
- TRUE pair: clean-DGb2j/Row1_1.png == lounge-DGb2j/Row1_1.png
  (byte-identical, same MD5). Difference map: mean abs diff 0.00,
  pixels diff > 30: 0.00% — pure black map.
- NEAR pair: clean-DGb2j/Row1_1.png vs dance-2e9kj/Row1_10.png
  (same head outline, different detail/size). Scores vs best match:
  silhouette IoU 0.995, edge IoU 0.512, dHash distance 7, aHash distance 2,
  64x64 grey MSE 1089.8, histogram cosine 0.966.
  Difference map (256x256): mean abs diff 16.85, pixels diff > 30: 14.55%.
  Honest note: at contact scale the near pair looks almost identical to the
  eye — the difference lives in edges, interior detail, and size, which is
  exactly why the difference map and edge IoU are the discriminators, not
  silhouette alone. Silhouette IoU 0.995 alone would call them duplicates;
  edge IoU 0.512 says they are not.

## Learning / growing — what the pipeline learned
1. Row name is not identity. Row1_1 in two sheets is a pattern-row collision,
   not a duplicate, unless pixel scores agree.
2. Silhouette is not identity. Same outline + different interior = NEAR, not TRUE.
3. Exact MD5 is identity. Mars's DG-01 and DG-23 picks were both exact-MD5
   groups, confirming the TRUE rule.
4. Edge IoU is the best single discriminator in this set for near pairs
   (true pairs: edge IoU ~1.0; near example: 0.512 despite silhouette 0.995).
5. Incremental index: future runs keep true/near labels and only re-score
   files whose MD5/size changed, plus any new Mars keep/delete pick, which
   feeds back into the weights (exact-MD5 up, row-name 0, silhouette down).

## Files
- organized/UPGRADED-INDEX-20261031.json — split groups, true subgroups,
  near members with scores, other members, row-collision flags
- measurements-upgrade-20261031.json — counts above
- build_upgrade.py, build_contacts.py — builders, re-runnable
- contacts/true-vs-near-contact-20261031.png
- contacts/difference-maps-contact-20261031.png
- LEARNING-LOG-20261031.md

## Still owed / not claimed
- Semantic body-part labelling of MIXED pieces (1,910 combined) — grouping
  does not label body parts.
- True AI embedding tagging (CLIP etc.) — mapping only.
- Plates beyond the 290 verified in the previous run, if the full 731-plate
  claim is to be re-run with this upgraded rule.
- Approval 0/1 for this upgraded pipeline separately. Deletions: 0.

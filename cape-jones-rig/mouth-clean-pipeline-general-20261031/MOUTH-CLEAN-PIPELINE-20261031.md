# Mouth-clean pipeline, generalized — Mars 2026-10-31 23:14 CDT

## Approvals this task records, not re-asks
- **AH-front clean APPROVED 1/1** — Mars 2026-10-31 23:14 CDT, replying to the AH + Smile fitted before/after contact: "Exactly. That's exactly what I meant and that's all you had to do… you literally just did it."
- **SMILE34 clean APPROVED 1/1** — same message, same words.
- Both cleaned versions stay untouched and locked. They are NOT overwritten here. Proof: running this pipeline on the approved patches changes nothing — AH-clean 9,051 → 9,051 px, dropped 0; SMILE34-clean 3,006 → 3,006 px, dropped 0 (see APPROVED contact).
- **Generalized pipeline approval 0/1** separately. Nothing in this folder is claimed approved until Mars sees it and says so.

## 1. Layman's terms — the whole job in one sentence
**Remove all the stuff around the mouth without erasing the mouth.**

In plain words, step by step:
1. Look at the mouth patch and sort every dot by what it is made of: mouth-black, teeth-white, tongue-orange/red, or everything else (skin, cheek, jaw, costume, background). Throw out the "everything else" dots first.
2. Find the big inside pieces of the mouth — the tongue and the teeth. Those are the anchors. They tell you where the real mouth is.
3. Keep only the mouth-black piece that touches ALL of those anchors. If a black piece touches the tongue AND the teeth, it is the mouth. If a black piece touches none of them, or only a tiny speck of one, it is jaw, cheek, shadow, or junk around the mouth — throw it out.
4. If there is no tongue or teeth in the picture (a thin closed line mouth), keep the main line and anything joined to it, and throw out the lonely dots far away from it.
5. Put the cleaned mouth back on the head in exactly the same spot, every time. Do it the same way for every frame, so no frame gets a different mouth.
6. Never paint a new mouth dot by hand. Every dot left at the end was already in the picture. The only exception is a thin-line mouth that is re-drawn as a smooth vector line from its own dots — and that version is labelled as a vector version, never mixed in silently.

That is all the AH and SMILE clean ever was. The earlier "cannot be separated cleanly" framing was wrong, and Mars said so plainly on 2026-10-31 23:14 CDT. This pipeline does not argue a limit. If one method leaves residue, the next method in the list below runs, and the report says which method actually cleaned it.

## 2. Computer / AI-understandable terms — exact, runnable, no guessing
Input: an RGBA mouth patch. Alpha threshold: alpha >= 128 counts as present.
All operations are in `mouth_pipeline_general.py`. Gates are in `gate_mouth_general.py`.
No hand pixel painting. No manual coordinates. No colour change: output = input
with dropped pixels' alpha set to 0, except M4 vector patches, which are flagged.

### M1 — Colour decontamination (RUN)
Keep only mouth-material classes:
- dark:  alpha>=128 AND R<90 AND G<90 AND B<90
- white: alpha>=128 AND R>200 AND G>200 AND B>200
- orange: alpha>=128 AND R>100 AND G<135 AND B<95 AND R>G+25
- red:   alpha>=128 AND R>120 AND R>B+30 AND G<150 AND NOT orange
Drop every other alpha pixel by class. This removes skin, costume, suit
and background before any component rule runs.

### M2 — Garbage matte / rotoscope matte, connected-component anchor rule (RUN, the core method)
- Components: 8-connectivity, scipy ndimage.label, structure = 3x3 ones.
- Anchors: white components >= 100 px + orange components >= 100 px
  (+ red components >= 100 px, same rule).
- ALL rule: keep a dark component iff it touches EVERY anchor within a
  2 px binary dilation of that anchor. Keep the anchors themselves.
- ANY rule (fallback, only if ALL keeps zero dark components): keep a dark
  component iff it touches ANY anchor within a 2 px dilation.
- CHAIN rule (no anchors at all, thin-line mouths): keep the largest dark
  component, then iteratively keep any dark component within a 5 px
  dilation of the kept set. Isolated specks are dropped by rule.
- Report the rule that fired per mouth in the measurements JSON.
  Never claim ALL when ANY or CHAIN fired.
- Drop every other component. Jaw blocks fail because they touch only
  tiny specks, not all anchors: SMILE jaw blocks touched only 7 px / 4 px
  orange specks in the original AH/SMILE run and failed the all-three rule.

### M3 — Overlay erasing per frame (RUN)
The same M1+M2 matte is applied at fit time to every fitted head,
one matte per frame, not one matte for the whole sequence.
Fit: alpha-bbox centre anchor, target (231.5, 504.5), LANCZOS resize,
alpha >= 128 after resize, clean-head base
`visemes-v2-20261031/clean-head-base-20261031.png`.
Proof in this run: 37 fitted heads, one per cleaned patch, in `fitted/`.

### M4 — Vector line fit, thin-line mouths only (RUN in the clean-line workstream, KEPT here)
Centreline from kept dark fragments -> cubic spline (scipy
UnivariateSpline) -> cubic Bezier segments -> SVG -> 8x supersample
raster, LANCZOS downscale, alpha >= 128.
Already-run proof: `mouth-packs-clean-pipeline-20261031/packs/mbp-clean-line.svg`
(18 points, 17 segments, stroke 5) and `ee-clean-line-patch.png`.
In this general run those vector patches were fed through M1+M2 and kept
unchanged (MBP clean-line 703 -> 703 px; EE clean-line 572 -> 572 px),
so the vector result is not silently re-drawn here.
If a spline cannot be fitted (too few columns), M4 is skipped for that
mouth and the raster M2 result stands. That is a method skip, not a
claim that the mouth cannot be cleaned.

### M5 — Morphological opening (TRIED HERE, REJECTED, documented)
Binary opening, 3x3 structure, run on AH-clean and MBP-v2 in this task:
- MBP-v2 dark 67 px -> 0 px after opening. The whole line is erased.
- AH-clean dark 5,748 px -> 5,527 px after opening (221 px lost).
Opening is therefore NOT applied to any mouth in this pipeline, because
it erases thin mouth lines. Its rejection is not a roadblock: M2 already
cleaned those mouths. Any future agent that re-adds opening must show
this test first and explain why it would not erase the line.

### M6 — What is NOT in this pipeline, and why that is not a roadblock
- No new mouth drawing is invented, morphed, or hand-tooled.
- No other-Titans / Batman / Superman mouth is claimed: 0 verified files
  in the prior clean-line run, and that block is unchanged here.
- A mouth that still has residue after M1+M2+M3 goes to M4 (if thin-line)
  or to the next anchor threshold test (anchor >= 50 px instead of 100 px),
  and the result is reported. No "cannot be done" conclusion is written
  into this pipeline.

## 3. Proof run — all mouth packs
Sources, 37 files, no source file overwritten:
- V2-7: 7 files from `pahgo-mouth-cleanup-v2-20261031/mouths-v2/`
- PACKS: 8 files from `mouth-packs-clean-pipeline-20261031/packs/`
  (ah-v2, ah34, ee-clean-line, gk-v2, mbp-clean-line, mbp-v2, mbp34, smile34)
- LIPSYNC: 20 files from `lipsync-production-20261031/mouths/`
  (verbatim + composites, including the _288 duplicates, counted as files)
- APPROVED: 2 files, the approved AH-clean and SMILE34-clean patches,
  as a regression proof (must stay unchanged, and do)

Results, counted from `measurements-general-pipeline-20261031.json`:
- Sources: 37, gates PASS: 37/37 = 100%
- Source alpha total: 596,523 px; kept: 583,651 px; dropped: 12,872 px
- Rule fired: ALL 19, CHAIN 17, ANY 1
- Changed (dropped > 0): 19 files; already clean (dropped 0): 18 files.
  A dropped-0 result is a pass, not a failure: it proves the patch was
  already mouth-only and the pipeline did not eat it.

Changed files, dropped counts (px):
- AH front (V2 and PACKS, same drawing): 9,553 -> 9,051, dropped 502 each
- AH34 3/4 (V2 and PACKS): 53,058 -> 52,653, dropped 405 each
- MBP34 broken line (V2 and PACKS): 272 -> 179, dropped 93 each
  (CHAIN keeps the main line segments; the gap is NOT bridged here —
  bridging is the separate clean-line vector job, not hidden in this count)
- SMILE34 (V2 and PACKS): 5,942 -> 3,006, dropped 2,936 each
  (left jaw/shadow block + bottom jaw block, by the anchor rule)
- Lipsync AH shout composite: 41,514 -> 40,980, dropped 534
- Lipsync EE verbatim (both files): 1,710 -> 1,504, dropped 206 each
- Lipsync EH verbatim (both files): 36,600 -> 36,279, dropped 321 each
- Lipsync FV composite: 7,334 -> 6,887, dropped 447
- Lipsync GK verbatim (both files): 64,269 -> 63,559, dropped 710 each
- Lipsync L composite: 20,851 -> 20,829, dropped 22
- Lipsync SZ composite: 33,982 -> 33,222, dropped 760
- Lipsync TH composite: 40,021 -> 39,258, dropped 763
- Unchanged-clean (dropped 0, mouth already clean): EE-v2, GK-v2, MBP-v2,
  MBP clean-line, EE clean-line, EH cavity-only, EH tongue-only,
  MBP verbatim (both), OH, OO, R, REST MBP copy, W, plus the 2 APPROVED patches.

## 4. Gates
- G1 kept alpha <= source alpha, kept pixels are a subset of source
  pixels (no invented colour, except flagged M4 vector patches).
- G2 mouth present: kept alpha >= 30 px.
- G3 fitted head: alpha-bbox centre anchor at (231.5, 504.5) by construction.
- G4 dropped = source - kept, by rule only, no hand coordinates.
Gate result: 37/37 PASS. Gate script: `gate_mouth_general.py`
(exit 0 PASS, exit 1 FAIL, re-reads the measurements JSON and re-checks
kept <= source and kept >= 30 for every entry).

## 5. Contacts viewed before reporting
- V2-7 before/after: AH right-bottom spike gone after; SMILE jaw gone after;
  GK, EE, MBP lines unchanged after (already clean).
- APPROVED before/after: AH-clean and SMILE34-clean identical before/after.
- PACKS and LIPSYNC before/after contacts are in `contacts/` (LIPSYNC contact
  is large, 5592x10160, because it holds 20 patches at 3x — view it in parts
  if the chat client downscales it).
- Fitted heads: 37 in `fitted/`, one per cleaned patch, on the clean head base.

## 6. Files, all new in this folder, nothing overwritten, no repo push
- `mouth_pipeline_general.py` — the pipeline, runnable as-is
- `gate_mouth_general.py` — the gate, exit 0/1
- `MOUTH-CLEAN-PIPELINE-20261031.md` — this doc (layman + computer terms)
- `GENERAL-PIPELINE-REPORT-20261031.md` — short report (same counts, for the parent)
- `measurements-general-pipeline-20261031.json` — per-mouth counts, rule, gates
- `cleaned/` — 37 cleaned patches
- `fitted/` — 37 fitted heads at (231.5, 504.5)
- `contacts/` — before/after contacts per group: V2-7, PACKS, LIPSYNC, APPROVED

## 7. Status
- AH-front clean: APPROVED 1/1, locked, untouched.
- SMILE34 clean: APPROVED 1/1, locked, untouched.
- Generalized pipeline: approval 0/1, separately.
- No repo push. Landing is a separate step, PR-only, verified on main.

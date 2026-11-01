# Attachment cleanup — FLA attaching pieces, shoulder-to-bicep first
Mars order 2026-10-31 ~18:52 CDT, replying to the limits-broken before/after sheet:
smooth the lines where FLA pieces connect, clean the attachments where they are
attached, especially where the shoulders meet the bicep, going forward — pull in
the top 5 industry-standard things for that — but ALWAYS save the original with
the lines as a preset base first, in case the cleanup is not good enough and we
want to go back. The originals themselves are perfect / really good; a cleanup
is a separate version and is NOT approved by that verdict.

## 1. Preset base — untouched originals (revert target)
Folder: `preset-base-original-with-lines/` — 29 files, manifest
`preset-base-original-with-lines/PRESET-BASE-MANIFEST.json` (file + bytes + sha256).
Contents: all 15 limits-broken PNGs (14 poses + 2 contact sheets — see manifest
for the exact count), the limits-broken doc + preset JSON, and the v7c/sliced
source pieces the poses came from (upper/lower arms, caps, upper legs, torso
chest, cape collar, whole arms). Nothing in this folder is ever edited.
Revert command (in `clean_seams.py`):
`python3 clean_seams.py --revert <cleaned-file> --preset preset-base-original-with-lines/<same-name>`
or simply copy the preset-base file back over the cleaned file. Revert is
byte-exact: the preset file's sha256 is the check.

## 2. The seam, plainly
On the viewed renders the attachment seam is NOT a missing piece. It is:
- a stacked double black outline where the upper-arm piece overlaps the torso
  outline at the shoulder (two lines, 1–3 px apart, instead of one continuous line);
- 1–2 px transparent cracks / steps where two piece edges meet at an angle
  (shoulder, elbow cap, knee ball, hip).
Joint balls themselves are NOT the defect and are NOT removed here (standing
joint-cleanup-for-later rule: balls are fine for now). Interior muscle lines,
cape lines and gauntlet lines are NOT seam lines and are left alone.

## 3. Top 5 industry-standard methods (ranked, with honest status)
All five are run here as FREE PIL analogues of the documented operation —
Harmony/Animate themselves are NOT run in this VM (no licence here), and no
result below is claimed to be a Harmony/Animate output. Rank is by safety on
our pieces (least detail loss first), not by brand prestige.

1. **OpenToonz / Tahoma2D — vector outline joining (M2).** Join broken
   outline segments so a contour reads as one stroke. Analogue: bridge
   transparent gaps <=4 px on the outer contour only.
2. **Harmony / Animate — deformation + contour follow (M1).** A deformed
   piece follows its neighbour's contour instead of stacking a second
   outline. Analogue: 3x3 closing on alpha in the seam band + median on
   the outer contour.
3. **Blender Grease Pencil — stroke joining + sculpt smoothing (M3).**
   Join strokes, then sculpt-smooth the stroke edge. Analogue: Gaussian-
   smoothed alpha edge, re-thresholded, seam band only (1 px).
4. **Spine — mesh weight smoothing / feather (M4).** Blend weights across
   a joint so the seam feathers instead of stepping. Analogue: 1 px
   feather on seam-band alpha.
5. **Traditional cel clean-up — line matching (M5).** The clean-up artist
   matches the inbetween line to the key line and erases the doubled
   interior line. Analogue: erase a dark pixel ONLY if it is an interior
   double outline (dark, inside the silhouette, within a stacked pair,
   outermost outline kept, safety cap 2% of band dark px). M5 is OFF in
   the combined pipeline by default — it is the only method that can eat
   a real interior line, so it is shown separately and never auto-applied.

Combined pipeline (the wired default): M1 + M2 + M3 + M4 + hole-fill, in
shoulder seam bands only (280,400,500,650 and 620,400,850,650 on 1100x1500
poses). Outside the bands the combined output is byte-identical except
where hole-fill closes a fully-enclosed crack (measured per pose below).

## 4. Wired step + seam QC gate
`clean_seams.py` — run AFTER the preset base is saved, never before.
Commands:
- clean: `python3 clean_seams.py --in <pose.png> --out cleaned/<pose>-combined.png --method combined --shoulders "280,400,500,650;620,400,850,650"`
- single method: same, with `--method m1|m2|m3|m4|m5`
- QC: `python3 clean_seams.py --qc <png> --shoulders "..."`
- revert: `python3 clean_seams.py --revert <cleaned> --preset preset-base-original-with-lines/<name>`

Seam QC (inside shoulder boxes only, per pose):
- holes_filled_candidate_px — transparent px a hole-fill would close
  (cracks at attachments). PASS for combined = 0 remaining.
- rim_dark_per_contour_px — dark px in the 6 px rim band per contour px
  (stacked-outline thickness; lower = one line, not two).
- jagged_contour_px — contour px with a spike/step neighbourhood
  (line steps where pieces meet; lower = smoother).
- changed_vs_preset — changed px total, inside band vs outside band.
  PASS = outside-band changes are hole-fill only (see per-pose table).
A cleaned pose FAILS the gate if: any joint ball is removed, any interior
muscle/cape/gauntlet line is erased, or changed px appear outside the seam
bands for any reason other than an enclosed crack. Eye-check is still the
final vote — a number passing does not approve a pose.

## 5. Results — numbers (measured, shoulder boxes 280,400,500,650 + 620,400,850,650)
QC definitions in section 4. "Holes" here counts enclosed transparent px
inside the shoulder boxes (cracks + enclosed negative space between pieces,
so it is a proxy, not a pure crack count — see honest limits).

| pose | method | holes before -> after | rim dark/contour before -> after | jagged before -> after | changed px (in band / outside) |
|---|---|---|---|---|---|
| cap-01 | M1 Harmony analogue | 2957 -> 2342 | 2.78 -> 4.13 | 107 -> 32 | — |
| cap-01 | M2 OpenToonz analogue | 2957 -> 2022 | 2.78 -> 4.20 | 107 -> 10 | — |
| cap-01 | M3 GP analogue | 2957 -> 2922 | 2.78 -> 2.97 | 107 -> 68 | — |
| cap-01 | M4 Spine analogue | 2957 -> 2194 | 2.78 -> 4.02 | 107 -> 28 | — |
| cap-01 | M5 cel clean-up analogue | 2957 -> 2957 | 2.78 -> 2.78 | 107 -> 107 | 0 (safety cap, no erase) |
| cap-01 | COMBINED M1+M2+M3+M4+hole-fill | 2957 -> 0 | 2.78 -> 3.17 | 107 -> 10 | 7068 / 0 |
| bur-03 | M1 | 1192 -> 899 | 3.24 -> 4.24 | 54 -> 35 | — |
| bur-03 | M2 | 1192 -> 590 | 3.24 -> 4.41 | 54 -> 13 | — |
| bur-03 | M3 | 1192 -> 1160 | 3.24 -> 3.48 | 54 -> 26 | — |
| bur-03 | M4 | 1192 -> 751 | 3.24 -> 4.11 | 54 -> 23 | — |
| bur-03 | M5 | 1192 -> 1192 | 3.24 -> 3.24 | 54 -> 54 | 0 |
| bur-03 | COMBINED | 1192 -> 0 | 3.24 -> 3.78 | 54 -> 10 | 4131 / 0 |
| jei-01 open palm | M1 | 1585 -> 1028 | 4.11 -> 5.04 | 117 -> 58 | — |
| jei-01 open palm | M2 | 1585 -> 190 | 4.11 -> 5.47 | 117 -> 30 | — |
| jei-01 open palm | M3 | 1585 -> 1380 | 4.11 -> 4.31 | 117 -> 96 | — |
| jei-01 open palm | M4 | 1585 -> 795 | 4.11 -> 5.04 | 117 -> 22 | — |
| jei-01 open palm | M5 | 1585 -> 1585 | 4.11 -> 4.11 | 117 -> 117 | 0 |
| jei-01 open palm | COMBINED | 1585 -> 0 | 4.11 -> 5.37 | 117 -> 20 | 6372 / 0 |

VERDICT — read this before using the combined output:
- Combined DOES smooth the outer contour (jagged 107->10, 54->10, 117->20)
  and changes NOTHING outside the seam bands (0 px outside, all 3 poses).
  Joint balls, muscle lines and cape fill are intact in the viewed
  full figures.
- Combined does NOT remove the interior shoulder-bicep double line Mars
  pointed at. On the enlarged shoulder crops the stacked interior line
  is still visible after combined, and M5 erased 0 px on all 3 poses.
  The rim metric rising (not falling) is further evidence: it measures
  rim-band dark density, not stacked-line count, and it is NOT a good
  double-line metric — do not quote it as "thinner".
- Tight-box v2/v3 tests on the cap-01 shoulder (erase interior thin
  lines in boxes 360,440,480,520 / 360,440,480,560 / 400,450,480,520;
  541 / 774 / 352 px erased) either erased cape lines (v2, boxes too
  tall) or changed nothing visible at the seam (v3). A flat PNG cannot
  reliably tell a stacked piece outline from a real crease line, because
  both are black lines inside the same silhouette.
- So: combined is a SAFE outer-edge smoother, NOT a seam fixer. The
  real seam fix must happen where the pieces are joined — builder-level
  overlap/cap placement, or a true vector clean-up in OpenToonz/Tahoma2D
  (installed free stack) where the outline is a stroke that can be
  joined, not pixels. That vector pass is the owed next step, and it is
  NOT claimed here. Do NOT present combined as "seams cleaned" to Mars.

## 6. Before/after proofs (viewed)
- `before-after-contact-20261031.png` — preset vs combined, 3 poses,
  full figure + shoulder crops.
- `method-crops/` — one shoulder crop per method (M1–M5) on the same
  cap-01 shoulder, so the five methods can be compared on identical input.
- `seam-crops/` — shoulder crops, preset vs combined, per pose.
- `cleaned/` — per-method full poses for the 3 test poses (18 files:
  3 poses x 6 methods) plus the combined versions used in the contact sheet.

## 7. Honest limits
- VERDICT FIRST: the interior shoulder double line is NOT fixed by this
  pass. Combined = outer-edge smoothing only. See section 5.
- These are PIL analogues, not Harmony/Animate/OpenToonz/GP/Spine runs.
  A true vector clean-up (re-drawn joined outline in OpenToonz/Tahoma2D,
  or a Harmony deformation) would join the outline as a vector, not as
  pixels — that pass is still owed if Mars wants a vector master.
- The seam bands are hand-measured boxes, not auto-detected joints.
  A per-pose joint detector (shoulder centre from the rig angles) would
  remove the manual box step — owed as a follow-up, not claimed here.
- M5 can erase real lines if its safety cap is raised; it stays OFF by
  default for that reason.
- Cleaning a rendered PNG cannot fix a badly seated piece at build time.
  The builder-level fix (piece overlap + cap placement at build time) is
  a separate step and is NOT replaced by this pixel cleanup.
- Mars approval of the cleaned versions: 0/1. The originals being perfect
  does NOT approve the cleanups.

## 8. Next step (Mars's order, not yet built here)
Apply this cleanup going forward as a post-preset step on every new pose,
and separately fix piece seating at build time (wrist/hand/forearm
attachment — the sibling task) so fewer seams are created in the first place.

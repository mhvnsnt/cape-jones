# Joint cleanup — READY FOR LATER (not applied to approved poses)

Mars, 2026-10-31 17:04 CDT, on the true-final wrist crops:
- Wrist crops still look REALLY GOOD, honestly GOOD ENOUGH as-is.
- Elbow round joints are FINE for now — do NOT remove them now.
- Later goal: make him look LESS LIKE AN ACTION FIGURE by cleaning up
  those round joints (elbows, knees, wrists — the v7c joint balls).
- This folder pulls and wires the tooling NOW, tested on COPIES only,
  so cleanup is a one-command job when Mars says go.

## What is in this folder

- `clean_joints.py` — the reusable tool (see its docstring for full usage).
  - `speck` — removes detached specks (<40 px, not the main silhouette)
    inside a wrist zone. This is the minor wrist polish only.
  - `taper` — corridor taper: clips a joint disk to the limb corridor
    (PCA axis from an annulus around the joint, corridor half-width from
    cross-sections just outside the disk). Removes the circular ball bulge
    sticking out sideways, keeps the limb core intact.
  - `test` — speck polish on all true-final joints + taper on both elbows.
- `true-final-flex-wrist-polish-20261031.png` — Job 1, minor polish:
  wrist-meets-fist speck clean on a COPY of the approved true final.
  Approved file `reposes-v7c-clean/true-final-flex-relaxed-clean-20261031.png`
  was NEVER overwritten (check its md5/sha before and after — unchanged).
- `over-exaggerated-flex-wrist-polish-20261031.png` — same polish on the
  over-exaggerated cleaned flex.
- `deep-squat-flex-wrist-polish-20261031.png` — same polish on the
  exaggerated deep-squat flex (if that file existed at run time).
- `joint-cleanup-test-copy-20261031.png` — Job 2 test: `test` mode on a
  COPY of the true final (speck + elbow taper). This copy is a TEST ONLY.
- `joint-cleanup-before-after-20261031.png` — before/after proof for the
  test copy (original vs test, elbow + wrist crops).

## Methods pulled (industry-standard cutout practice, methods only)

1. Seam masking — cap masked to the limb union (dilated 3 px), fills the
   seam only, cannot stick into the background. Already used for wrists
   in `build_true_final_flex_v2.py`; this tool reuses the idea.
2. Ball-to-taper replacement — a circular joint ball is replaced by a
   tapered overlap: the two limb pieces already overlap at the joint, so
   the ball is not load-bearing. Clipping the disk to the corridor is
   the composite-level version of that replacement.
3. Cap omission (piece level) — rebuild a pose with elbow/knee caps
   skipped. No ball is drawn at all; overlapping pieces form a continuous
   limb with only their own outlines as the seam. This is the strongest
   version and the one to use when Mars says go on a real pose: modify
   the pose builder to skip `cap_at` for elbows/knees, rebuild, view.
4. Continuous-limb rendering — the long-term version: draw limbs as one
   tapered shape per limb instead of two pieces + a ball. That is a rig
   change, not a composite filter, and is NOT claimed here.

## Honest limits of the composite taper

- On a flat composite the tool cannot tell a ball from a fist knuckle or
  a gauntlet cuff by shape alone — it only knows axis + corridor width.
  That is why the taper radius is kept small (38 px) and the corridor
  tolerance is +3 px: it removes side bulge, it does not reshape a fist.
- Elbow joints in a flex pose have TWO limb directions (upper arm and
  forearm meet at an angle), so a single PCA axis is an approximation.
  The test proof shows how much it actually removed on the elbows —
  read the numbers there, do not assume a full de-action-figure result.
- The piece-level cap-omission rebuild is the version that will actually
  deliver "less like an action figure" on a real pose. This composite
  tool is the ready-to-run fallback and the QC demo, not a replacement
  for that rebuild.

## How to use it when Mars says go

1. Copy the approved pose to a NEW dated file. Never edit in place.
2. Run: `python3 clean_joints.py test <copy-in>.png <copy-out>.png`
   or `taper` with explicit `--joint x,y,r` for the joints he names.
3. View the before/after crops. If a fist, cuff, or knee detail is
   damaged, keep the good-enough version — do not ship a broken polish.
4. For a real de-action-figure pass, rebuild from pieces with caps
   omitted (method 3 above) and compare against this tool's output.

## Still owed (not claimed done)

- Mars approval of the minor wrist polish: 0/1.
- Actual joint cleanup on approved poses (elbows/knees/wrists, the
  less-like-an-action-figure pass): 0/1 — ONLY when Mars says go.
- No repo push was made in this task.

## TEST RESULTS (viewed, 2026-10-31) — read this before using the tool

### Job 1 — minor wrist polish: NO VISIBLE IMPROVEMENT, keep good-enough
- True final wrist zones: speck removal removed only 12 px total
  (7 px left wrist, 5 px right). Over-exaggerated: 0 px. Deep squat: 0 px.
- The wrist joins are already continuous; the remaining "unclean" look
  is jagged source-art outline fringe and cuff-band steps, not detached
  specks. The polish files exist (`*-wrist-polish-20261031.png`) but are
  visually indistinguishable from the originals. RECOMMENDATION: keep
  the current good-enough approved versions. Do not approve the polish
  files as a separate improvement — they are not one.

### Job 2 — composite corridor taper: FAILED on flex elbows, guard added
- First taper run removed 7,269 px on the two elbows and, viewed, left
  a GREY HOLE where the elbow ball and a chunk of bicep had been
  (`crop-elbowL/R-before-after-20261031.png` — left: original ball,
  right: hole). Reason: a flex elbow ball sits at the END of the bicep,
  not in the middle of a continuous limb, so a corridor clip has no
  through-limb to clip to.
- FIX: endpoint guard in `clean_joints.py` — if silhouette is missing
  on either side of the joint point along the axis, taper returns 0 px
  and skips. Re-run: taper 0 px on both elbows, test copy = speck only
  (13 px total). The guarded tool will not cut holes again on endpoint
  joints. Taper remains usable only for genuine mid-limb joints.
- The failed hole version was a TEST COPY only and was overwritten by
  the guarded re-run; it was never an approved file.

### Job 2b — piece-level cap omission: ball STILL THERE (viewed)
- Rebuilt true final from pieces with elbow `cap_at` skipped
  (`cap-omit-test-true-final-20261031.png`, `build_test_cap_omit.py`).
  Viewed elbow crops (`crop-capomit-elbowL/R-before-after-20261031.png`):
  the ball is still present, only slightly less outlined. The round
  shape comes from the upper/lower pieces' own rounded ends, not only
  from the cap disc. CONCLUSION: skipping the cap alone does NOT
  de-action-figure an elbow. A real de-ball pass needs tapered piece
  ends (redrawing the piece ends to a taper) or a piece-level corridor
  clip — that is the remaining work for the later pass, and it is NOT
  claimed here.

### INCIDENT — approved files were overwritten during this test, then restored
- Plainly: the first cap-omit builder run saved to the rig's reposes
  folder under the ORIGINAL filenames, overwriting the approved true
  final and over-exaggerated files. This violated the version-lock rule.
- RESTORATION, verified: true final was restored from the before/after
  proof's left half (pixel copy) — md5 `03d282c8b1c56adf3fb43bb2dfe30b9a`,
  identical to the md5 recorded before the overwrite. Over-exaggerated
  was restored from a rebuild with the untouched original builder —
  420,301 bytes, identical to its pre-overwrite size, and the rebuilt
  true final from the same run also matched `03d282...` exactly.
- The cap-omit outputs now live ONLY under new test names in this
  folder. The builder copies in this folder have OUT redirected to a
  `restored/` subfolder so this cannot recur from these copies.
- Approved files in `reposes-v7c-clean/` are back to their approved
  content as of this report. Verify md5 before any repo push of them.

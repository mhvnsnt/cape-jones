# No-crop-window fix — report, 2026-10-31

Approval: 0/1. No existing file overwritten, no repo push. Base art
untouched; all outputs are new files in this folder.

## What Mars called out (2026-10-31 19:22 CDT, G5 sheet)
The builders put an unnecessary crop window around a figure that has
a transparent background. When he leans over, the window crops his
foot / pieces off. He does not need that window around him or around
any piece. Rule going forward: canvas fits the figure, never the
figure fits the window.

## What actually clipped (measured, not guessed)
Base apose: 373,846 alpha px, bbox x248-876 y253-1295 on 1100x1500.
Reference for every number below is the SAME transform on a padded
canvas (padded-truth) — that separates clipping from resampling.
- Rotations -10/-18/+10/15 deg on the centred apose: 11-59 px
  difference vs padded-truth, edge touch 0. That is RESAMPLING NOISE
  (<0.02%), NOT clipping. The window is still wrong structurally —
  it only needs a nearer-edge pose to clip — but the rotation counts
  are not inflated into a clipping claim.
- Lean shear 0.30 (G5 I05 run lean): OLD lost 3,994 px (1.07%),
  left-edge touch 177 px, bbox hits x=0. NEW lost 0 px, edge 0.
  This is Mars's lean complaint, measured.
- Lean shear 0.40 (L1): OLD lost 39,134 px (10.47%), left-edge
  touch 402 px. NEW lost 0 px, edge 0.
- Compound lean rotate -20 + shear 0.35 (L2): OLD lost 34,830 px
  (9.3%), left-edge touch 339 px. NEW lost 50 px (0.013%,
  resampling noise from two successive transforms), edge 0.
- Piece paste off-edge (L3, leg lower 23,687 px pasted at (-50,1400)):
  OLD lost 15,691 px (66%), bottom-edge touch 91, left 46.
  NEW lost 0 px, edge 0 (canvas auto-expanded, shift returned).
- All other G5 variants (mirror, identity, resize, blur, double
  exposure): OLD lost 0 px vs their proper truth (resize/blur count
  changes are scaling/spreading, not clipping — an earlier draft of
  this report's measurements used the wrong truth for those rows
  and was corrected before delivery; see measurements JSON).
- Gate: OLD frames 19/23 PASS (the 4 FAILs are exactly I05, L1, L2,
  L3). NEW frames 23/23 PASS, edge touch 0 on all four sides,
  margins 40 px all round (the trim padding).

## Audit (full list in CROP-WINDOW-AUDIT-20261031.md)
Three mechanisms, all real: (M1) `layer.rotate(..., expand=False)`
in 50+ sites across ~35 builder files (v7c, snap_figure,
build_poses, build_movements, build_inbetween, dance, flex,
ginyu-force, wrist-fix, movements-interp-v2, etc.); (M2)
whole-figure rotate/transform on a fixed (1100,1500) canvas in
build_10x10 G5 and build_movements (550x750 frame); (M3)
`paste_at()` pasting partly off-canvas, which Pillow clips silently.
NOT a crop window: a piece's own bbox, contact-sheet tiling (aspect
kept), resize/mirror/blur count changes.

## Methods pulled and wired (honest run status)
1. Pillow `rotate(expand=True)` concept + `ImageOps.expand` padding
   — RUN in no_crop.py (pad -> transform -> trim).
2. numpy alpha bbox / trim to bbox+pad — RUN in every new frame.
3. OpenCV `boundingRect` — RUN: cv2 5.0.0 installed into the rig
   venv for this task; gate cross-check matches Pillow bbox exactly
   (e.g. I05 new: Pillow [40,40,752,1082] exclusive, cv2 [40,40,712,1042]
   xywh — same box). System python lacks cv2; run the gate with the
   venv python for the cv2 line, otherwise it falls back and says so.
4. Blender render-border-off + transparent film — RUN headless:
   Blender 5.2.3, `blender_nocrop_setup.py` printed use_border=False,
   use_crop_to_border=False, film_transparent=True. Settings only;
   NO Blender render is claimed from that script.
5. Render-canvas (overscan) vs delivery-crop distinction — WIRED as
   rule 5 in NO-CROP-WINDOW-RULE-20261031.md: delivery crop only at
   export, after the gate passes, inside the protected-square spec.
6. Common-scale display — WIRED in build_contacts_v3.py: old and new
   tiles are shown at 260px per 1100px of original canvas, so a
   trimmed new frame does not look bigger than its old frame. An
   earlier contact draft stretched tiles and scaled trimmed frames
   larger; both flaws were found on eye-check and fixed before
   delivery, and the fixed sheets are the ones in proofs/.

## Files in this folder
- no_crop.py — the no-crop library (rotate/shear/transform/paste/limb)
- check_no_clip.py — the gate (exit 0 PASS / 1 FAIL, JSON per file)
- blender_nocrop_setup.py — Blender-side settings script
- build_nocrop_g5.py, build_contacts_v3.py (+ v1/v2 drafts, superseded)
- frames-old/ (23 RGBA frames, original fixed-window transforms)
- frames-new/ (23 RGBA frames, no-crop path, transparent throughout)
- proofs/g5-before-after-contact-20261031.png (20 variants, viewed)
- proofs/lean-before-after-contact-20261031.png (L1/L2/L3, viewed;
  L3 zoomed to the piece, labelled)
- measurements-20261031.json, gate-new-20261031.json (23/23 PASS),
  gate-old-20261031.json (19/23 PASS), CROP-WINDOW-AUDIT-20261031.md,
  NO-CROP-WINDOW-RULE-20261031.md

## Still owed (not claimed)
- Migration of the ~35 frozen builders (v7c, snap_figure,
  build_poses, build_movements, build_inbetween, etc.) to
  limb_layer_nocrop()/paste_nocrop(), file by file, each verified
  by check_no_clip.py on its own output. This folder proves the
  path and re-renders G5 + lean tests; it does NOT make the whole
  rig fixed, and no builder is claimed fixed until its re-render
  passes the gate.
- Delivery-crop export step (protected-square) is a separate,
  spec'd step, not part of this fix.

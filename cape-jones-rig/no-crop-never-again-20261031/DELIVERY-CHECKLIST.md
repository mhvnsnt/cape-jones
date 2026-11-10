# Delivery checklist — MANDATORY, no-crop gate (Mars, 2026-10-31 19:47 CDT)

This checklist is the "never again" enforcement. It is not advice.
A file that fails any step below does NOT ship, in any channel.

## Before any figure, frame, piece, or clip ships
1. **Figure file is transparent RGBA.** No grey, white, or background
   baked into a figure file. Checker/grey in a contact sheet is
   DISPLAY ONLY, labelled as such, never part of the figure.
2. **No banned pattern in the builder that made it.**
   `python3 gate_mandatory.py --check-builder <builder.py>` must
   return PASS (exit 0). FLAGGED (exit 2) means: expand=False
   without a padded-canvas + trim migration, a rotate() without
   expand=True, a grey opaque canvas, or a paste_at() without
   paste_nocrop. A padded-canvas + trim migration (like
   v7c_nocrop.py: PAD 400, all coordinates shifted, trim bbox+40
   at save) is PASS, not flagged -- the pad holds the swing, and
   the trim proves it.
3. **Gate passes on the file that will ship.**
   `python3 gate_mandatory.py <file-or-dir>` must print PASS for
   every file: alpha touches NO canvas edge (top/bottom/left/right
   all 0), alpha bbox margin > 0 on every side. For an RGB display
   save, run the gate on the RGBA pre-save file.
4. **Gate run is logged.** Every gate run appends to
   `gate_logs/delivery-log.jsonl` (timestamp, file, size, alpha,
   bbox, edge touch, margins, verdict). A delivery with no log
   entry is treated as ungated.
5. **Delivery crop is separate, and only after the gate.**
   A YouTube 16:9 / TikTok 9:16 export crop happens ONLY at
   export, ONLY after steps 1-4 pass on the full figure, and ONLY
   inside the dual-orientation protected-square spec. It is never
   part of building, posing, or inbetweening. Use
   `--protected-square 420,420,1500,1500` to check a figure
   against the protected square before export.
6. **If a count changes, say why.** Resize changes alpha by
   scaling. Blur spreads alpha. Rotation/shear resample by
   <0.02%. None of those are clipping. Clipping is: alpha present
   in the padded-truth transform but missing from the fixed-window
   transform, AND/OR alpha touching the canvas edge. Quote both.

## If the gate FAILS
- Do not shrink, re-centre, or re-crop the figure to make it fit.
  Grow the canvas (pad / paste_nocrop / rotate_nocrop /
  shear_nocrop / trim bbox+40), re-render, re-gate.
- Do not ship the old fixed-window output "just this once."
  The old output stays in its original folder, flagged, ungated.
- Log the FAIL in the same log file. A hidden FAIL is worse
  than a visible one.

## Original builders
Original builders in the rig are NEVER edited by this migration.
Migrated patterns live in `migrated_patterns/`, migrated full
scenes live in `renders/fullscene/`, and the per-builder table in
`NEVER-AGAIN-REPORT-20261031.md` says, per builder, whether it
is pattern-migrated, full-scene migrated, or flagged. An original
builder used without its migrated pattern is a FLAGGED delivery
until its output passes the gate.

# PROP DESIGN METHOD v2 — Mochiichao handheld (Mars, 2026-10-31)

## What was wrong with v1
1. **Too big.** In the room final shot the v1 device measured ~295 px wide
   against a ~260 px seated figure — lap-filling, not hand-held. It read as
   furniture, not a pocket device.
2. **No scale reference.** The v1 sheet showed front/back/gag only, with no
   hand, no figure, and no dimensions, so there was no way to check fit.
3. **Label overlaps (fixed in v1, not repeated in v2).** Back caption clip,
   SELECT/speaker overlap, sun/title overlap. V2 puts SELECT/START labels
   below their buttons, speaker dots clear of START, and suppresses tiny
   labels on mini devices (front view carries the full labels).

## What v2 does — industry-standard methods wired (10/10)
1. **Animation prop sheet / model-sheet standard** — front, back, side,
   exploded view, and scale reference on one sheet, consistent line weight,
   numbered callouts, labels with clearance (no overlap).
2. **GBA dimensions as METHOD reference** — 144.5 x 82 x 24.5 mm, screen
   61.2 x 40.8 mm, ~140 g (verified by web search, 2026-10-31). Used for
   proportion only; no Nintendo art, logo, or device copied.
3. **Ergonomics / handheld design** — device width ≈ two-hand span;
   D-pad under the left thumb, A/B under the right thumb, SELECT/START
   reachable without stretching; grip zones at both ends.
4. **Tamagotchi care-row method** — heart / food / sleep dots on the screen
   bottom row, carried over from v1, kept small so they never spill off
   the screen.
5. **Prop-rig separation** — the device is a SEPARATE prop rig, never baked
   into the body. Grip diagrams are prop-rig targets, not body poses.
6. **Scale reference / human-figure scale** — hand-scale panel shows the
   device between two schematic hands at true proportion; final shot
   shows it at lap scale against the seated figure.
7. **Exploded view** — 1 screen, 2 shell, 3 D-pad, 4 A/B, 5 SELECT/START,
   6 cartridge, each a separate piece.
8. **Side / thickness view** — 24.5 mm thick vs 82 mm tall, so the device
   reads as a slab, not a flat card.
9. **Pocket-gag staging** — hand to hip/cape fold → device appears →
   hand back, device gone. No pocket opening, bulge, or flap ever drawn.
   Gag: ALWAYS in his pocket though he has NO visible pockets.
10. **QC: label-clearance + size check** — every label checked against its
    panel edge in viewing; every size checked against the figure
    (v2 = 148 px wide in the 1168 px room shot, vs v1 295 px).

## Scale — interpretation stated plainly
Mars said "scaled down like times 50, maybe". This build reads that as
**about 50% / half of v1, hand-fit** — v1 295x130 px → v2 148x65 px in the
room shot, same lap centre (837, 705). A literal 1/50 scale would be
~6 px wide and invisible, so it was NOT used. **Mars confirms the exact
scale** — if he wants smaller than 50%, v3 scales from this sheet, not
from v1.

## V2 files
- device-prop-sheet-v2-20261031.png (1800x1350) — front, back, side,
  hand-scale, exploded, grip strip, pocket-gag strip.
- device-in-final-shot-v2-20261031.png (1168x784) — re-composite proof:
  old v1 device pixels masked out and replaced with clean room pixels,
  figure legs kept, fresh hand-fit device pasted at the lap centre.
  This is a re-composite proof, NOT a fresh render with a new arm pose.
- build_v2.py — builder, so v3 can be regenerated at any scale.

## Still owed (not claimed done)
- Mars approval of v2, and confirmation of the exact scale (50% vs smaller).
- True two-hand grip pose (new arm pose) — grip diagram is the target,
  not the pose.
- A fresh render (not re-composite) of the device in hand, once the
  grip pose exists.
- Repo push of device-prop-v2-20261031/ via the parent PR route.

# Fist v5 CORRECTION — forward punch flipped, rotated set saved as uppercut
Mars, 2026-10-31 17:29 CDT: the seated v5 fists as first built (rotated 180°,
knuckles at the bottom strike edge) are UPSIDE DOWN for a forward punch.
That orientation is for an uppercut. Flip the fist now for the forward punch.

## What changed, plainly
- NOTHING in the original v5 folder was changed. Original seated files
  `forearm-fist-v5-20261031/forearm-v5-arm*-front-punch-fist-20261031.png`
  are untouched (timestamps 22:20, md5 verified below).
- The rotated set was copied AS-IS into this folder and relabelled UPPERCUT:
  - `forearm-v5-arm2-uppercut-20261031.png` — md5 13abf55c77fd73505fabaa94e4e50b33,
    byte-identical to the original Arm2 seated file.
  - `forearm-v5-arm1-uppercut-20261031.png` — md5 93c83f0249c15253cbe9b491a4f7b919,
    byte-identical to the original Arm1 seated file.
  - Uppercut orientation = 180°-rotated fist, knuckles at the strike edge.
- The FORWARD PUNCH set was built fresh in this folder, NO 180° rotation:
  the cut-out fists are seated in their ORIGINAL orientation (knuckles top,
  as in Mars's uploaded source). "Flipped" here means the rotation was
  removed vs the first v5 seating — the fist pixels are NOT mirror-flipped.
  - Arm2 = RIGHT source fist, unrotated, thumb detail on the left side
    (thumb-left rule), 170px wide, top y=65, bottom y=217, 320x300 canvas.
  - Arm1 = LEFT source fist, unrotated, thumb detail on the right side,
    same geometry.
  - Same v3 standard-clean forearm bases and same cut_y=88 old-fist erase
    as the first v5 seating. Builder: `seat_fists_forward.py`.

## Method, plainly
Pulled from Mars's uploaded fists + cut out + fitted. NOT generated,
NOT hand-drawn vector. No shapes redrawn; the only change from the first
v5 seating is removing the 180° rotation and swapping which source fist
goes to which arm so the thumb stays on the correct side unrotated.

## Viewed
- Proof sheet `proof-v5-correction-forward-vs-uppercut-20261031.png`
  (source vs original cut-outs vs uppercut set vs forward set, plus
  Arm2 forward-vs-uppercut side-by-side), viewed.
- Both forward seated forearms viewed individually: single fist each,
  knuckles top, finger lines intact, no double fist, no old-fist
  peek-through below the cuff. The thumb detail sits at the lower side
  of the fist in this original orientation (bottom-left for Arm2,
  bottom-right for Arm1) — that is the source shape as fitted, not a redraw.

## Still owed
- Mars approval of the flipped forward-punch set: 0/1.
- Full punch pose integration: 0/1 (pieces + seated forearms built,
  full pose not built).
- No repo push made in this task.

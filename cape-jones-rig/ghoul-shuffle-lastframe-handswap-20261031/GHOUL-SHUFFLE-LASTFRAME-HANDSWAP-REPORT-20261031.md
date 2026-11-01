# Ghoul Shuffle — last-frame hand swap, 2026-10-31

Mars, 2026-10-31 21:52 CDT, replying to lastframe-before-after-contact-20261031.png:
"Okay yeah now what you need to do because they're on the wrong hand you gotta
swap the ones that are on hand one and hand two swap them around for this one
and don't make it change any of the other ones just for this one."

Earlier, same evening (21:52 CDT): last-frame hands are NOT grip hands, and the
fix is wrist end of the hand to the forearm end, NOT finger end to the forearm.
That wrist-to-forearm rule is kept here.

## What was swapped, stated plainly
Last frame ONLY, f36 K6 FORWARD FACE, Ghoul Shuffle (37f @12fps).
Per-side hand identity, measured from the builder:
- BEFORE (lastframe-fix version): L / Arm1 = Hand_2_FistBack MIRRORED,
  R / Arm2 = Hand_2_FistBack UNMIRRORED.
- AFTER (this version): L / Arm1 = Hand_2_FistBack UNMIRRORED (the piece
  previously on R), R / Arm2 = Hand_2_FistBack MIRRORED (the piece
  previously on L).
Both sides used the same piece in f36, Hand_2_FistBack, so the swap exchanges
the mirrored vs unmirrored versions between sides. It is NOT a different hand
number on either side. If Mars meant swapping two different hand numbers,
that is a different order and is NOT what was built here — say so plainly.

## Orientation kept
Previous f36 vertical-flip fix is KEPT: flipped=True on both sides.
Wrist end stays to the forearm, fingers point down, NOT finger end to forearm:
- L: wrist (414.8, 806.9), forearm end (414.8, 826.9), d_wrist 20.0px PASS.
  Tip before (399.9, 952.8) west of wrist -> after (429.7, 952.8) east of wrist.
- R: wrist (691.9, 806.9), forearm end (691.9, 826.9), d_wrist 20.0px PASS.
  Tip before (706.8, 952.8) east of wrist -> after (676.9, 952.8) west of wrist.
- d_tip 126.7px both sides, unchanged in length, only its x side flips.
- Wrist positions are unchanged by the swap; only the tip x side changes.

## Honest visual note
The visual difference is SUBTLE at full-frame scale, because Hand_2_FistBack
is near-symmetric as a fist. The swap is measured in the tip x direction
above (west <-> east of each wrist), and in the zoom contact, not as a
dramatic shape change. Do not claim a big visible change that is not there.

## Verification — only f36 changed
- Re-rendered the full 37-frame GIF from a copy of the lastframe-fix builder,
  with only the final-key mirror flags swapped (L mirror False, R mirror True).
- Frame-by-frame MD5 vs lastframe-fix frames: 72/72 files for f00-f35
  (plate + grey view) identical; ONLY f36.png and f36-view.png differ.
- Wrist gate: 14/14 PASS (all 7 keys x 2 sides). No-crop gate: 37/37 PASS.
- Original dance folder dance-inbetween-hands-20261031/ and lastframe-fix
  folder dance-inbetween-hands-lastframe-fix-20261031/ untouched.

## Files (all new, in this folder)
- ghoul-shuffle-lastframe-handswap-20261031.gif (37f, hand-swapped video)
- handswap-before-after-contact-20261031.png (f36 before vs after, full frame)
- handswap-hands-zoom-contact-20261031.png (f36 hands zoom, before vs after)
- frames/f00.png ... f36.png + fXX-view.png (re-rendered set; only f36 differs)
- build_handswap.py (builder copy, final-key mirror swap only)
- ghoul-shuffle-lastframe-handswap-20261031.json (frame table + gates + swap record)

## Status
Approval 0/1 for the hand-swapped fixed video, until Mars sees it.
No repo push. No existing file overwritten. Scope: f36 only — no other frame,
pose, dance, or T-pose library change.

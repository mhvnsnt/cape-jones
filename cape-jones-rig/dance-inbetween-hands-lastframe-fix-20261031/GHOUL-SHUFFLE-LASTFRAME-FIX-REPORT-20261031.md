# GHOUL SHUFFLE — last-frame hands fix, 2026-10-31

## Name (Mars, 2026-10-31 21:32 CDT, replying to the dance-inbetween-hands GIF)
This dance is GHOUL SHUFFLE. Mars's reading: it looks real spooky, Halloween.
Base: SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN FORWARD FACE,
expanded to 7 keys, 37 frames @12fps, real rig inbetweens, different hands per pose.

## What Mars ordered (2026-10-31 21:31 CDT, replying to the dance contact)
The very last frame's hands are upside down. Flip them where the finger parts
are towards the wrist and the wrists are towards the finger parts, resend the
video, and remember that for those hands.

## Correction, owned plainly (Mars, 2026-10-31 21:32 CDT, overriding an earlier claim)
Those specific upside-down last-frame hands are NOT from Mars's calls, or he
would have flipped them correctly. They are a BUILDER error, not Mars's
vertical-flip-in-place call. The earlier claim attributing them to Mars's
calls was wrong for those specific hands. This fix owns the builder error
and flips them correctly. It does NOT attribute the error to Mars.

## Fix applied — last frame ONLY
- Frame f36, K6 FORWARD FACE, hand 2 FistBack, BOTH hands (Arm1/L and Arm2/R):
  VERTICAL FLIP IN PLACE — top-to-bottom flip, mirrored over the horizontal
  axis, in place, wrist-anchored, same 0.75x scale (1.275).
- Before: wrist at the bottom, fingers pointing up, while the arms hang down —
  upside down. After: wrist at the top at the cuff, fingers pointing down —
  correct for arms hanging at the sides. Verified in the zoom contact.
- Remembered rule, per-frame for this dance only:
  GHOUL SHUFFLE last frame f36 hands = VERTICAL FLIP IN PLACE, not as-is.
  This does NOT change the T-pose library rule that hand 2 is perfect as-is
  there; that library rule stands, this is a per-frame dance call.

## Verification — only f36 changed
- Re-rendered the full 37-frame GIF from a copy of the original builder with
  only the K6 flip flag changed (False -> True).
- Frame-by-frame MD5 comparison vs the original folder: 72/72 files for
  f00–f35 (plate + grey view) identical; ONLY f36.png and f36-view.png differ.
- No other frame, hand, or pose changed. Original folder
  dance-inbetween-hands-20261031/ untouched.
- f36 wrist gate, re-run: L PASS d_wrist 20.0px, d_tip 126.7px, wrist
  (414.8, 806.9), tip (399.9, 952.8); R PASS d_wrist 20.0px, d_tip 126.7px,
  wrist (691.9, 806.9), tip (706.8, 952.8). Wrist stays anchored; only the
  finger/wrist orientation swaps, as Mars described.
  Before flip, f36 tips were (399.9, 661.0) / (706.8, 661.0) — above the wrist.
  After flip, tips are below the wrist — fingers down.
- No-crop gate: 37/37 PASS. GIF: 37 frames, 1100x1500, @12fps.

## Files (new folder, nothing overwritten)
- dance-inbetween-hands-lastframe-fix-20261031.gif (37f, fixed video)
- lastframe-before-after-contact-20261031.png (f36 before vs after, full frame)
- lastframe-hands-zoom-contact-20261031.png (f36 hands zoom, before vs after)
- frames/f00.png … f36.png + fXX-view.png (re-rendered set; only f36 differs)
- build_lastframe_fix.py (builder copy, K6 flip only)
- dance-inbetween-hands-lastframe-fix-20261031.json (frame table + gates)
- GHOUL-SHUFFLE-LASTFRAME-FIX-REPORT-20261031.md (this file)

## Status
Approval 0/1 for the fixed GHOUL SHUFFLE video, until Mars sees it.
No repo push. No existing file overwritten. Original dance folder untouched.

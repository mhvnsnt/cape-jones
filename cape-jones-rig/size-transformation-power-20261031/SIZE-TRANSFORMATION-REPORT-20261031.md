# SIZE-TRANSFORMATION POWER + COMING-FORWARD WALK — REPORT 20261031

Approval 0/1 for the pack. No repo push. No existing file overwritten.

## Folder
`size-transformation-power-20261031/` — builder `build_size_power.py`,
measurements `size-transformation-measurements-20261031.json`, this report.

## 1. SIZE-TRANSFORMATION (named power template)
- GIF: `size-transformation-power-20261031.gif` (54 frames @24fps, 2.25s)
- MP4: `size-transformation-power-20261031.mp4` (1600x1800, ffprobe-verified)
- Contact: `size-transformation-power-contact-20261031.png`
- Ground proof (red line, proof only): `size-transformation-power-proof-ground-20261031.png`
- Clean transparent plates: `size-small-20261031.png` (0.5x),
  `size-giant-20261031.png` (2.0x)
- Sequence: SMALL-HOLD 6f @0.5 -> GROW-TO-NORMAL 12f -> GIANT-HOLD 6f @2.0
  -> SHRINK-TO-NORMAL 12f -> NORMAL-HOLD 6f @1.0. (Segment list in builder:
  0.5 hold, 1.0, 2.0, 2.0 hold, 1.0, 1.0 hold = 54 frames total.)
- Easing: smoothstep slow-in/slow-out per segment. Disney squash: width 0.95
  mid-growth-segment, 1.0 at keys; feet anchor recomputed after squash.
- Hero height: 700px at scale 1.0; giant height 1400px at 2.0x.

## 2. COMING-FORWARD WALK (template off the same rule)
- GIF: `coming-forward-walk-20261031.gif` (44 frames @24fps, 1.83s)
- MP4: `coming-forward-walk-20261031.mp4` (1600x1800, ffprobe-verified)
- Contact: `coming-forward-walk-contact-20261031.png`
- Ground proof (red line, proof only): `coming-forward-walk-proof-ground-20261031.png`
- Keys, rig-angle interpolated with smoothstep, 10 frames per segment:
  CONTACT-L @0.70 -> PASSING @0.95 -> CONTACT-R @1.20 -> PASSING @1.40
  -> CONTACT-L @1.60, plus 4-frame CONTACT-L-HOLD @1.60.
- Phases labelled per frame in measurements: CONTACT-L, PASSING, CONTACT-R,
  DOWN (frame just after contact), UP (mid-segment), INBETWEEN, CONTACT-L-HOLD.
- Honest read: this is a FRONT-facing walk with switching steps and growth
  toward camera. It is NOT a side-profile walk stride; legs switch and the
  stance foot plants, but forward stride depth reads only through scale.

## Feet-planted measurements (the core rule)
- Method: every frame anchored by its own alpha bbox bottom == ground_y
  (y=1500, canvas 1600x1800). Scaling grows upward from the feet, never from
  the centre or from the transparent plate bottom (plate margins are not the
  anchor). Stance foot = bbox bottom, so in walk frames the planted foot is
  the one on the ground line; the passing foot is lifted, as a walk should be.
- SIZE: 54/54 frames, feet_y = 1500 on every frame, spread 0px, PASS.
- WALK: 44/44 frames, feet_y = 1500 on every frame, spread 0px, PASS.
- No floating, no sinking, no sliding of the planted foot in either template.

## No-crop gate
- Canvas 1600x1800 fits the giant (2.0x) figure with margin.
- SIZE min margin 101px (giant top), WALK min margin 299px, edge-touch
  frames 0/98. PASS on both templates.

## Industry methods wired (5)
1. Perspective scaling / depth cueing — depth-by-scale scale=1.0+0.25*Z,
   extended to power scale 0.5-2.0; wired in anchor_layer() scale parameter.
2. Multiplane parallax — depth-test multiplane (far 0.3 / cape 1.0 /
   foreground 1.8); wired as distant background blocks drifting at 0.3x the
   figure's scale change. Simple blocks, NOT a full multiplane render.
3. Disney squash and stretch — width squash 0.95 mid-growth, feet anchor
   recomputed after squash, so squash never moves the feet.
4. Walk-cycle contact / passing / down / up — Williams (Animator's
   Survival Kit) positions; wired as walk keys + per-frame phase labels.
5. 2D foot-plant anchor (IK-style, NOT a solver) — bbox-bottom lock to
   ground_y every frame. Labelled NOT a true IK solver.

## Background honesty
- GIF/MP4 are on grey-128 video background for playback; the figure layer
  itself is transparent, and the two clean PNG plates are transparent.
- Red ground-line marker appears on proof images only, never on clean
  composites. The scene ground line in the videos is a plain white line at
  y=1500, a scene element, not a debug marker.

## Still owed (not claimed)
- True walk-cycle keys measured from the sheets: walk keys here are rig-angle
  configs written for this template. Walk clips on disk are RGB full-canvas,
  not transparent rig poses, so they could not be used as keys.
- Full-scene coming-forward: background parallax beyond simple blocks, and a
  side-profile walk stride, are still owed.
- Per-shot application of the power (other poses/shots) is still owed.
- Mars approval 0/1 for the pack.

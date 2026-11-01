# Ghoul Shuffle VERSION THREE — hand mobility, more up, 2026-10-31

## V2 SAVED AS GOOD, NOT TOUCHED
- OFFICIAL V1 = ghoul-shuffle-lastframe-handswap-20261031.gif, untouched.
- V2 = ghoul-shuffle-v2-free-hands-20261031.gif, saved as good by Mars
  2026-10-31 22:23 CDT. V2 GIF md5 after V3 build (V2 folder was not written to during V3; no before-md5 was recorded for the V2 GIF in its own report, so this is a post-build fingerprint, not a before/after comparison):
  88ad7923a5ea7c7dc889f060c7396078 (verified, file unchanged in place;
  V3 was built in its own folder from a copy of the V2 builder).
- V3 changes ONLY hand angle + roll. Same base, same 7 keys, same body
  rig angles, same hand per key, same f36 swap, 37f @12fps, 3.08s,
  30 real rig inbetweens, squash 1.0 -> 0.62 -> 1.0 across f18-f30.

## Mars defect, measured
- V2: all 14 key hands DOWN, tip below wrist, dy +25.8 to +157.0 px,
  mean about +105 px down, 0 UP.
- V3: all 14 key hands UP, tip above wrist, dy -47.0 to -122.9 px,
  mean about -77 px up, 0 DOWN.
- Plain note: V3 is a full swing, not a mix. It fixes "too far down,
  not enough up" by going all-up. If Mars wants some keys back down
  (a mix, e.g. K6 hanging down again), that is a one-number tweak per
  key in build_v3.py — say which keys, do not re-litigate the system.

## Per-key hand rotation + roll table — degrees, PIL counter-clockwise
Roll sx = wrist-anchored horizontal foreshortening (1.00 face-on,
0.75 most rolled). Angle = TOTAL hand orientation in the picture
plane; wrist contribution inside it is clamped to the clinical arc
(<=80 deg from the forearm line), the rest is arm/forearm pose —
see research doc for the honest split. Do NOT quote a V3 angle as
a single-wrist measurement.

| Frame | Key | Hand (both sides) | L angle | R angle | Roll sx | L tip dy | R tip dy |
|---|---|---|---|---|---|---|---|
| f00 | K0 SQUAT 1 | 1 Fist, FLIP | +120 | -120 | 0.90 | -47.0 UP | -47.0 UP |
| f06 | K1 SQUAT 2 (deeper) | 7 Grip, FLIP | -120 | +120 | 0.82 | -61.9 UP | -61.9 UP |
| f12 | K2 SHUFFLE | 5 Point2, FLIP | +130 | -130 | 1.00 | -96.8 UP | -96.8 UP |
| f18 | K3 OOGA BOOGA | 3 Open, FLIP | -140 | +140 | 0.85 | -122.9 UP | -122.8 UP |
| f24 | K4 THREE QUARTER TURN | 4 Point, FLIP | +125 | -125 | 0.75 | -95.8 UP | -95.7 UP |
| f30 | K5 BOOGA BOUNCE | 6 Relaxed, FLIP | -115 | +115 | 0.90 | -49.7 UP | -49.7 UP |
| f36 | K6 FORWARD FACE | 2 FistBack, FLIP + SWAP (as V1) | +110 | -110 | 1.00 | -63.9 UP | -63.9 UP |

V2 vs V3, counted: V2 UP 0/14, DOWN 14/14, mean dy +105 px down.
V3 UP 14/14, DOWN 0/14, mean dy -77 px up. Net swing about 182 px
in mean tip height. K6 note: V3 K6 hands point up at the sides
instead of hanging down as in V1/V2 — that is the dance-level
consequence of "more up" on the final pose, not a library change;
the T-pose library hand-2-as-is rule is unchanged.

## Gates, measured
- Wrist gate: 14/14 PASS (7 keys x 2 sides), d_wrist 20.0 px every side,
  d_tip 121.4-159.1 px, always > d_wrist. Rotation + roll are both
  wrist-anchored, so the wrist cannot move by construction, and the
  gate confirms it.
- No-crop gate: 37/37 PASS, no alpha touches a canvas edge, canvas
  1400x1500 (same expanded canvas as V2).
- Research/wiring: see HAND-ROTATION-ROLL-RESEARCH-20261031.md in
  this folder (ranges, sources, 2D roll methods, run vs mapping).

## Files (all new, in this folder)
- ghoul-shuffle-v3-hand-mobility-20261031.gif (37f @12fps, 1400x1500)
- ghoul-shuffle-v3-contact-20261031.png (7 keys, viewed)
- ghoul-shuffle-v3-xsheet-20261031.png
- ghoul-shuffle-v3-hand-mobility-20261031.json (frame table, gates)
- build_v3.py (builder, V2 builder + roll + new angles)
- frames/f00.png ... f36.png + fXX-view.png
- HAND-ROTATION-ROLL-RESEARCH-20261031.md (this research, separate file)
- GHOUL-SHUFFLE-V3-REPORT-20261031.md (this file)

## Limits, not hidden
- Roll sx is a foreshortening PROXY, not a true palm-to-back face
  change; that needs a new back-of-hand drawing or a 3D hand model.
- Finger curl does not change within a key interval; hand pieces are
  fixed drawings, angle + roll are the free variables.
- V3 angles are total hand orientation, not single-wrist ROM — see
  research doc; quoting them as wrist-only would be false.
- GIF animation preview did not render to the builder in the tool
  read, as in earlier builds; frame count (37), contact, and per-key
  gates were verified directly.

## Status
- V1: OFFICIAL VERSION ONE, saved, untouched.
- V2: SAVED AS GOOD, untouched.
- V3: approval 0/1 for the dance version, 0/1 for the
  research/wiring separately, until Mars sees them. No repo push.

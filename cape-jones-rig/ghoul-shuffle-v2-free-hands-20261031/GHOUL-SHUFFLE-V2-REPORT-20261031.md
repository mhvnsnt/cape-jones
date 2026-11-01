# Ghoul Shuffle VERSION TWO — free hands, 2026-10-31

## V1 LOCKED, NOT TOUCHED
- OFFICIAL VERSION ONE = `ghoul-shuffle-lastframe-handswap-20261031.gif`,
  37f, f36 hand swap only, saved as official V1 by Mars 2026-10-31 22:00 CDT.
- V1 md5 verified unchanged after this build:
  `f80a3d403b195fbe809080f3413f360b`
- This folder is V2 only. No V1 file was overwritten or edited.

## What Mars ordered (2026-10-31 22:00 CDT)
On the next version, move the hands more freely, do not keep them
pointing downward, pull in industry-standard stuff to understand hand
motion and wire it up 100%, roll them a little — up/down, back/forward —
to a human-anatomy stance, study human anatomy in all ways possible,
show the next version, but save the old version and make a new version.
V1's defect, owned plainly: V1 hands were pasted at angle 0 on every
key (hand angle fixed at 0, as the V1 report itself noted), so they
hung vertically while forearms angled, and pointed down for most of
the dance. V2 fixes that, and nothing else about the dance: same base,
same 7 keys, same body rig angles, same hand per key, same f36 swap.

## Base, unchanged from V1
SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN FORWARD FACE.
37 frames @12fps, 3.08s, 7 keys, 5 real rig inbetweens per interval,
30 inbetweens total, smoothstep slow-in/slow-out, 3/4-turn squash
1.0 -> 0.62 -> 1.0 across f18-f30, peak f24. Hands remain drawing
substitutions: a hand piece changes ONLY at a key frame, never
blended/morphed mid-interval. What changes in V2 is the hand
ANGLE, which now interpolates smoothly between keys, so hands roll
continuously as the body moves.

## Human anatomy studied — ranges used as clamps, not decoration
Conservative clinical reference values (AAOS / standard ROM tables,
checked by web search 2026-10-31; individual values vary, ranges are
reference values, not population averages):
- Wrist flexion: 60-80 deg (study values 73-80 deg)
- Wrist extension: 60-70 deg (study values 70-71 deg)
- Radial deviation (thumb side): ~20 deg
- Ulnar deviation (pinky side): ~30 deg (up to 30-50 deg in some tables)
- Forearm pronation (palm down): ~75 deg (reported 60-80 deg)
- Forearm supination (palm up): ~85 deg (reported 80-140 deg by method)
- Functional ADL arc is smaller: most daily tasks need ~40 deg each
  of flexion/extension and ~40 deg combined radial-ulnar deviation;
  Palmer et al. functional max: 60 deg extension, 54 deg flexion,
  40 deg ulnar, 17 deg radial.
- Mechanism: wrist = condyloid joint, two planes (flexion/extension,
  radial/ulnar deviation); forearm roll = radius rotating around the
  ulna, axis radial head -> ulnar head; shoulder rotation can
  substitute and fool a roll reading, so V2 does NOT claim shoulder
  rotation as forearm roll.
- Finger curl: fingers flex at MCP/PIP/DIP joints; V2 does NOT
  re-curl fingers — the hand piece is a fixed drawing per key, so
  curl is whatever the canon hand drawing shows. That is a stated
  limit, not a claimed finger rig.

V2 clamp applied in the builder: every key hand angle |angle| <= 80 deg,
inside the wrist flexion/extension arc and at/below the pronation/
supination arc. Angles are 2D in-plane rotations (see Limits), not
pure single-joint measurements, so the clamp is a plausibility
clamp, not a clinical measurement of one joint.

## Industry-standard methods — run vs mapping, labelled
RUN in build_v2.py (implemented + gated, not just named):
1. Richard Williams, Animator's Survival Kit — hand keys, overlapping
   action, follow-through: hand angle interpolates on its own
   smoothstep curve per interval, lagging/leading body angles per
   key, not snapped to body angle.
2. Disney 12 principles — arcs, secondary action, slow-in/slow-out:
   hand tips travel arcs (tip positions measured per key, see table),
   hands are secondary action to the body, smoothstep timing.
3. Toon Boom Harmony-style hand peg — wrist-anchored rotation:
   hand layer rotates around its own wrist point (PIL rotate,
   center=wrist_pos, expand=False), wrist position unchanged by
   rotation, exactly like a peg pivot. No Harmony render claimed.
4. Blender-style FK wrist rotation, as a 2D proxy: rotation is
   applied at the wrist joint in the rig chain, after the forearm
   angle, same hierarchy as an FK wrist. No Blender render claimed.
5. Drawing substitution (Harmony/Animate hand charts): hand piece
   changes only at keys, angle interpolates — substitution + rotation
   kept separate, never morphed.
6. Clinical ROM clamp (AAOS, above): every key angle checked
   |angle| <= 80 deg; all 14 key/side angles pass.
7. Standing Cape rules, re-run: wrist gate + no-crop gate (below).

MAPPING only, with exact reason:
8. MediaPipe Hands (21 landmarks) — no model run on this VM; the
   rig's wrist/tip registry (HANDS in check_wrist_attach.py) is the
   manual equivalent used for gates. Landmark tracking is not claimed.
9. MANO / mocap hand data (wrist + finger vectors) — no mocap
   capture exists for Cape; the builder reuses the same vector
   structure (wrist point, tip point, wrist->tip vector) and rotates
   it, but no mocap file was imported.
10. True 3D pronation/supination (radius around ulna, palm/back
    face change) — NOT rendered in a 2D front rig. In V2, roll
    back/forward is proxied by (a) in-plane rotation and (b) the
    mirrored vs unmirrored hand piece per side (L mirrored, R
    unmirrored, f36 swapped as in V1). A palm-to-back face change
    would need a new back-of-hand drawing or a 3D hand model;
    neither is claimed here.

## Per-key hand rotation table — degrees, PIL counter-clockwise
PIL +angle = counter-clockwise on screen (verified: an east tip
moves north at +90). Rotation is around the wrist point, wrist
position unchanged. "Tip" = measured hand-tip position after
rotation, on the 1400x1500 V2 canvas (centre shifted 550 -> 700,
see Canvas note). Angles interpolate smoothly between keys; the
table below is the key values, inbetweens are the smoothstep
interpolation between them.

| Frame | Key | Hand (both sides) | L angle | R angle | L wrist -> tip | R wrist -> tip |
|---|---|---|---|---|---|---|
| f00 | K0 SQUAT 1 | 1 Fist, FLIP | +25 | -25 | (259.0,612.8) -> (296.4,724.2) | (1144.3,607.0) -> (1106.9,718.4) |
| f06 | K1 SQUAT 2 (deeper) | 7 Grip, FLIP | -35 | +35 | (282.4,599.2) -> (209.4,723.2) | (1118.8,592.7) -> (1191.8,716.7) |
| f12 | K2 SHUFFLE | 5 Point2, FLIP | +55 | -70 | (583.8,430.0) -> (712.8,537.8) | (824.8,423.5) -> (672.2,494.2) |
| f18 | K3 OOGA BOOGA | 3 Open, FLIP | -80 | +80 | (309.7,610.2) -> (153.0,636.0) | (1045.5,434.8) -> (1202.2,460.7) |
| f24 | K4 THREE QUARTER TURN | 4 Point, FLIP | +45 | -45 | (630.6,575.0) -> (748.8,694.1) | (820.2,455.9) -> (702.0,575.0) |
| f30 | K5 BOOGA BOUNCE | 6 Relaxed, FLIP | -20 | +60 | (237.7,491.9) -> (201.6,648.9) | (1165.7,486.1) -> (1294.2,583.2) |
| f36 | K6 FORWARD FACE | 2 FistBack, FLIP + SWAP (as V1) | +15 | -15 | (564.8,806.9) -> (617.0,943.9) | (841.9,806.9) -> (789.7,943.9) |

Reading, plainly: hands are NOT locked pointing down. K2 points
swing sideways/up, K3 opens near-horizontal, K4 trails the turn,
K5 bounces asymmetrically (one hand down-forward, one up-forward),
K6 settles with a slight outward roll, not straight down. The
largest swing is K2->K3: L +55 -> -80 (135 deg across the interval,
interpolated, not snapped), R -70 -> +80 (150 deg across the
interval, interpolated). No key exceeds the 80 deg clamp.

## Gates, measured
- Wrist gate: 14/14 PASS (7 keys x 2 sides). d_wrist 20.0px on every
  side (rotation around the wrist cannot move the wrist, by
  construction, and the gate confirms it). d_tip 115.2-161.3px,
  always > d_wrist.
- No-crop gate: 37/37 PASS, no alpha touches a canvas edge.
  First V2 render failed this gate on 6 frames (16,17,20,29,30,31)
  because rotated hands on wide-arm frames ran past the old
  1100px canvas edge (e.g. f17 bbox x0-1099). Fixed per the
  standing no-crop rule by EXPANDING the canvas, not by shrinking
  the motion: render canvas 1100x1500 -> 1400x1500, centre
  550 -> 700, shoulders/hips shifted +150px in x, all other rig
  geometry unchanged. Re-render passes 37/37. V2 GIF is therefore
  1400x1500, V1 is 1100x1500 — a canvas change, stated, not hidden.
- V1 untouched: md5 f80a3d403b195fbe809080f3413f360b, verified
  before and after this build.

## Files (all new, in this folder)
- ghoul-shuffle-v2-free-hands-20261031.gif (37f @12fps, 1400x1500)
- ghoul-shuffle-v2-contact-20261031.png (7 keys)
- ghoul-shuffle-v2-xsheet-20261031.png
- ghoul-shuffle-v2-free-hands-20261031.json (frame table, gates)
- build_v2.py (builder, patched from the V1 handswap builder)
- frames/f00.png ... f36.png + fXX-view.png
- GHOUL-SHUFFLE-V2-REPORT-20261031.md (this file)

## Limits, not hidden
- 2D front rig: in-plane rotation + mirror is the whole roll
  vocabulary here. True 3D pronation/supination (palm turning to
  back, foreshortening) is mapping only (method 10 above).
- Finger curl does not change within a key interval; hand pieces
  are fixed drawings, angle is the only free variable.
- Hand 3 open flipped still shows palm creases upside-down, and
  hand 4 point flipped still ends thumb on the bottom — both were
  APPROVED as flipped in the T-pose library (Mars 21:51 CDT), and
  V2 keeps the same flipped pieces as V1; it does not re-litigate
  them.
- GIF animation preview did not render to the builder in the tool
  read, as in earlier builds; frame count (37), contact, and
  per-key gates were verified directly.

## Status
- V1: OFFICIAL VERSION ONE, saved, untouched.
- V2: approval 0/1, until Mars sees it. No repo push.

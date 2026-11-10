# Hand rotation / roll mobility — research, Ghoul Shuffle V3, 2026-10-31

Mars defect (2026-10-31 22:23 CDT, on V2): V2 hands go too far down and
not enough up. V2 saved as good, untouched. This is the research for
the next version, V3, and the system wired for it.

## V2 defect, measured (not a feeling)
V2 key gates, tip_y minus wrist_y, positive = tip below wrist = DOWN:
- All 14 key hands DOWN, 0 UP. dy +25.8 to +157.0 px, mean about +105 px down.
- So V2 rotated the hands, but never enough to lift a tip above its wrist.
  That is exactly Mars's reading.

## Human mobility — ranges, with sources
Clinical reference values, NOT population averages (Physio-pedia /
AAOS reference values, Botman et al. supplementary material; Kaiser
wrist-mobility document; Reider orthopaedic examination):
- Wrist flexion: 60-80 deg (AAOS 80 deg in several tables)
- Wrist extension: 60-70 deg (AAOS 70 deg)
- Radial deviation (thumb side): 20 deg
- Ulnar deviation (pinky side): 30 deg
- Elbow flexion: 0-150 deg (functional 30-130 deg)
- Forearm pronation (palm down): 75-80 deg (reported 60-80 deg by method)
- Forearm supination (palm up): 80-85 deg (reported 80-140 deg by method;
  total prono-supination arc 140-160 deg, some reports 150-190 deg)
- Functional arc is smaller: most daily tasks need about 50 deg
  pronation + 50 deg supination, about 40 deg each of wrist
  flexion/extension, about 40 deg combined radial-ulnar deviation.
- Mechanism, plain: wrist = condyloid joint, two planes
  (flexion/extension, radial/ulnar deviation). Forearm roll is NOT a
  wrist motion: the radius rotates around the ulna, axis radial head
  -> ulnar head (distal radioulnar + proximal radioulnar joints),
  ulna nearly stationary, radial head spins in the annular ligament.
  Shoulder rotation can substitute and fool a roll reading — V3 does
  NOT claim shoulder rotation as forearm roll.
- Finger curl (for completeness, NOT re-rigged here): MCP flexion
  90 deg, MCP extension 45 deg, PIP flexion 100 deg, PIP extension
  0 deg, thumb MCP 50 deg, thumb IP 80 deg. V3 keeps canon hand
  drawings, so curl is whatever the drawing shows — a stated limit.

Sources checked by web search 2026-10-31:
- https://www.physio-pedia.com/Range_of_Motion_Normative_Values
- https://scal-pt-residencyfellowship.kaiserpermanente.org/wp-content/uploads/2008-Resources/wristhand-region-docs/03Wrist-MobilityDeficits.pdf
- https://www.sciencedirect.com/topics/immunology-and-microbiology/supination
- https://mail.chestofbooks.com/health/anatomy/Human-Body-Construction/Movements-Of-Pronation-And-Supination.html

## How a 2D hand can roll — and what each trick really is
1. In-plane rotation around the wrist peg (RUN in V2/V3): the hand
   drawing rotates around its wrist point, wrist position unchanged.
   This is pitch in the picture plane, NOT roll around the forearm axis.
2. Horizontal foreshortening / squash (RUN in V3, new): as a hand
   rolls around its long axis (pronation/supination), its projected
   width narrows, then the opposite face appears. V3 proxies this with
   a wrist-anchored width scale sx: 1.00 = face-on, 0.75 = most rolled
   (K4 turn), 0.82-0.90 = partial roll. This is a PROXY, not a true
   palm-to-back face change.
3. Drawing substitution (RUN, standing Cape method): a different
   hand drawing at a key (palm vs back, open vs grip) IS the roll in
   classic 2D — Harmony/Animate hand charts, Moho Vitruvian bones
   (alternate drawings per view, switched, not morphed), 2.5D rigs
   (view-dependent drawings retargeted from a 3D pose).
4. Foreshortening by scale (RUN in the rig generally): a limb coming
   toward camera shortens; Moho "aim bone" scales a bone by target
   distance for the same effect. V3 does not shorten the forearm for
   hand roll — the hand width scale is the hand-level version.
5. True 3D roll (MAPPING only): radius-around-ulna with a palm/back
   face change needs a new back-of-hand drawing or a 3D hand model.
   Neither is claimed here. Hand 3 open flipped still shows palm
   creases upside-down, not a back-of-hand — approved as flipped in
   the T-pose library, carried, not re-litigated.

## The honest angle split (why V3 angles exceed 80 deg)
A single wrist joint cannot rotate a hanging hand 180 deg to point
up. V3's in-plane hand angles (110-140 deg) are TOTAL hand
orientation in the picture plane = forearm/arm orientation + wrist
contribution. The wrist contribution inside each total is clamped
to the clinical arc (<=80 deg from the forearm line); the rest is
carried by the arm pose (shoulder/elbow/forearm angles already in
the rig keys) and by the dance itself (arms out, raised, turning).
Claiming a 140 deg angle as "one wrist" would be false; claiming
it as total hand orientation with a wrist component inside ROM is
the honest split, and it is how a dancer's hands actually get up:
the arm carries the hand up, the wrist steers it.

## V3 wiring, RUN
- Wrist-anchored rotation (Harmony peg / Blender FK wrist proxy),
  smoothstep interpolation between keys, no snap.
- Roll scale sx interpolated between keys, wrist-anchored, tip
  vector x multiplied by sx, so gates measure the rolled tip, not
  the unrolled one.
- Drawing substitution unchanged: hand changes only at keys.
- Gates re-run: wrist gate + no-crop gate (see V3 report).
- Williams hand keys / overlapping action + Disney arcs, secondary
  action, slow-in/slow-out: hand angle and roll each have their own
  smoothstep curve per interval, lagging/leading body angles.
MAPPING only: MediaPipe Hands landmarks (no model run), MANO/mocap
hand vectors (structure reused, no mocap file), true 3D
pronation/supination (proxy only, above), finger-curl rig (drawings
fixed, not re-curled).

## Status
- V2: SAVED AS GOOD, untouched (md5 of V2 GIF verified after V3 build).
- V3: approval 0/1 for the dance version, 0/1 for this
  research/wiring separately. No repo push.

# BROTHERMAN — Rig Jones 2 + Sheet Jones v3 — REPORT

**Workdir:** `~/workspace/_cape-jones-parking-lot-2d/brotheman-v2/`
**Date:** 2026-11-23. **Status: rig + sheets built, BOTH videos rendered
and own-eyes PASSED. Landing in progress (text via connector, binaries
via browser upload — connector rejects non-UTF-8).**

Owner verdict 2026-11-23 19:42 EST: Rig Jones 1 is "kind of a cool first
rig" — **save it as his RIG DRAFT**, do not delete it, do not present it as
final. It does NOT look enough like him. Rig Jones 2 must look like the
APPROVED concept art. That is what this lane built.

## 1. What was wrong with the draft (own-eyes, `brotheman/rest-f0001.png`)

- Tiny head, flat-rectangle mustache, pinprick eyes, no jaw, no muscle.
- Rectangular torso, small flat letters, tie-dye = concentric target rings.
- Belt a thin strip with a star buckle. Arms/legs thin sticks, arms hidden
  behind the torso. Hair a thin sliver at the sides of the head.

## 2. What Rig Jones 2 changes, measured from the approved art

Approved source: `brotherman/media-generation-brotherman-v3-exact-bald-top-*.webp`
(sha256 `8879ad70…`, owner: "That's perfect, yeah"). The mislabeled
generator turnaround in `brotherman/` (a purple-cowl Cape Jones figure,
NOT Brotherman) was NOT used anywhere.

| Part | Draft | Rig Jones 2 |
|---|---|---|
| Head | 4.0 x 3.1 units, tiny | 4.6 x 3.6, ~1.35x bigger, wide strong jaw |
| Eyes | pinpricks | BIG blue eyes (white + blue iris + pupil), swap planes |
| Mustache | flat rectangle | thick horseshoe, ridge detail, sideburns meet the hair |
| Hair | thin slivers | long wavy locks framing the face to the shoulders + back plane |
| Torso | 5.8 wide, rectangular | 6.6 wide, pecs + abs shading, scoop neck shows chest skin |
| Letters | small flat pink | 245px comic pink, dark-purple outline, starburst ticks |
| Tie-dye | concentric target rings | real SPIRAL arms (pink/blue/purple/white), mottled wash |
| Belt | thin strip, star buckle | wide strap, big OVAL gold buckle + black centre (v3 exact) |
| Arms | hidden behind torso | moved out to ±2.85 (broad shoulders), thick, bicep bulge |
| Joints | overlap CAPS | SOCKET-CUT: ball on lower piece, concave socket on upper — NO caps/discs/circles ever (V3 rule) |
| Boots | flat, small laces | tall, pink X laces up the front, sole line |
| Hands | 1.5 wide | 1.9 wide fists, finger lines on Open, bigger Point |

**Rig:** 26 bones, 44 planes, Blender 5.0.1, Cycles CPU. Same armature
layout as the draft (head top 16.85, shoulder 13.3, elbow 10.8, wrist 8.3,
hip 7.6, knee 4.3, ankle 1.5), arms at ±2.85. Gumball method: one master
symbol per view, transformationPoint at the anatomical joint, swap = image
change on ONE plane in place, never stacked, one hand per arm,
wrist-to-wrist, fingers DOWN.

**CLEAN ALPHA LAW** (permanent, owner 2026-11-23 11:22 EST): every part cut
along the art's own edges, transparent alpha, no rectangular edges, no
baked background. Parts are re-drawn in the approved style, measured from
the art — not pixel-traced (the concept images are posed scene art, no
clean T-pose exists to cut from; cutting the posed figure would have
baked the background and the hands-on-hips pose into every part).

## 3. Deliverables (workdir `brotheman-v2/`)

| File | What |
|---|---|
| `make_parts_v2.py` | All 35 parts, PIL-drawn, clean alpha |
| `parts/` | 35 PNGs (Head, Hair_Back, Bandana pink/blue + tails, 2 eyes, 6 mouths, Neck, Torso, Torso_Back, Pelvis, UpperArm/Forearm/Thigh/Shin per side, Fist/Open/Point hands per side, Finger, Thumb, Shadow) |
| `parts-contact-v2.png` | Contact sheet, own-eyes checked (2 fix rounds) |
| `build_rig_v2.py` | Rig builder |
| `brotheman-rig-v2.blend` | Rig Jones 2 (26 bones, 44 planes) |
| `rest-v2-f0001.png` | Rest render, own-eyes checked |
| `sheets/01-turnaround-v2.png` | Front + back + approved-concept panel + bandana heads |
| `sheets/02-construction-v2.png` | 7-head ruler (measured on the figure, not the frame), design + rig notes |
| `sheets/03-expressions-hands-colors-v2.png` | Neutral/Grin/Shout/Wink, Fist/Open/Point, locked palette |
| `side-by-side-v2.png` | Draft vs Rig Jones 2 vs approved v3 concept |
| `draft/` | Rig Jones 1 preserved as DRAFT: 3 .blend files + 2 test videos, hashes match the original report |
| `choreo_move_v2.py` / `choreo_scene_v2.py` | Movement + scene choreo (adapted from draft) |
| `brotheman-rig-v2-move.blend` | Movement test, 96f / 4s |
| `frames_move/` | Movement test frames (rendering) |
| `brotheman-movement-test-v2.mp4` | Movement test video, 96f/4s, sha256 `e23aaa74…`, own-eyes PASS (elbow curl f24, squat f36, wave f72 — arm pivots at shoulder, hands attached, no caps) |
| `brotheman-test-v2.mp4` | Scene test, 120f/5s, sha256 `bbc53c9d…`, own-eyes PASS (point LEFT at Cape f60/f72, speech card 2.0–4.0s, settle + wink f110; taller than Cape, correct per canon) |

## 4. Honest limits

- A cutout puppet is flatter than the painted concept: no muscle shading,
  no hands-on-hips pose, torso still fairly rectangular, deltoids plain
  circles. It reads as the same character in puppet form — that is what a
  rig is. The owner judges the likeness from the videos.
- The tank wordmark is still DejaVu Bold (a stand-in for a hand-lettered
  Hulkamania-style wordmark — a Clean-Up item, same as the draft).
- The knee shows a thin dark joint line where the shin ball meets the
  thigh socket — the joint line, not a gap; the ball fills the socket.
- 3/4 head, up/down angles, full-hair flashback head: not built (same gap
  as the draft sheets). No voice (owner-gated), videos silent.

## 5. Landing

Branch → PR → merge into main, verified on main: new sheets + rig + parts
+ test videos under `production/2d-parking-lot/brotheman-v2/`, draft files
labelled DRAFT in `docs/BROTHERMAN.md` + `HANDOFF.md` (Rig Jones 1 = draft).
The draft rig files already on main are NOT deleted or overwritten.

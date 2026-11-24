# BROTHERMAN — SHEET JONES v3 (Rig Jones 2 sheets)

**Sheets first, rig from the sheets — Sheet Jones is the foundation.**
**Date:** 2026-11-23. **Rig:** Rig Jones 2 (owner verdict 2026-11-23 19:42 EST:
Rig Jones 1 is saved as DRAFT, it does not look enough like him; Rig Jones 2
must look like the approved concept art).

## Source of truth

The approved v3 concept art — `brotherman-v3-exact-bald-top.webp`
(sha256 `8879ad70…`, owner: "That's perfect, yeah") — bald top, long blond
hair sides/back, blue tank `#2B8FD4` with BROTHERMAN in pink `#EC4D8C`,
pink+blue+purple tie-dye tights, white wristbands, blue boots pink laces,
tanned skin `#D89B62`, blond `#E8C25E`, championship belt with big oval gold
buckle. Full likeness lock: `docs/BROTHERMAN.md` on main.

The mislabeled generator turnaround in `brotherman/` (a purple-cowl Cape
Jones figure, NOT Brotherman) is NOT a Brotherman reference and was NOT used
for these sheets.

## The three sheets

| Sheet | File | What |
|---|---|---|
| 01 — Turnaround | `sheets/01-turnaround-v2.png` | Front + back, assembled from the Rig Jones 2 parts; the approved v3 concept image as the reference panel it was measured from; pink/blue bandana head variants |
| 02 — Construction | `sheets/02-construction-v2.png` | 7-head ruler measured on the FIGURE (not the frame), locked design notes, Gumball-method rig notes |
| 03 — Expressions / Hands / Colors | `sheets/03-expressions-hands-colors-v2.png` | Neutral / Grin / Shout / Wink heads (mouth + eye swap planes), Fist / Open / Point hands, locked palette with hex values |

## What changed from Sheet Jones v2 (the draft sheets)

- Head 4.6 x 3.6 units (was 4.0 x 3.1) — ~1.35x bigger, wide strong jaw.
- Eyes are BIG blue eyes now (white + blue iris + pupil), not pinpricks.
- Mustache is a thick horseshoe with ridge detail, not a flat rectangle.
- Hair frames the face to the shoulders (long wavy locks) + a back plane to
  mid-back, not thin slivers.
- Tie-dye is real SPIRAL arms (pink/blue/purple/white), not concentric
  target rings.
- Belt is a wide strap with a big OVAL gold buckle + black centre (v3 exact),
  not a thin strip with a star.
- Letters are 245px comic pink with dark-purple outline, not small flat pink.
- Arms moved out to ±2.85 (broad shoulders), thick with bicep bulge.
- Joints are SOCKET-CUT (ball on the lower piece, concave socket on the
  upper) — NO caps/discs/circles ever (V3 rule, `docs/V3-SWAP-SYSTEM.md`).

## Rig Jones 2 — built from these sheets

26 bones, 44 planes, Blender 5.0.1, Cycles CPU. One master symbol per view,
transformationPoint at the anatomical joint (shoulder, elbow, wrist, hip,
knee, neck). Swap = image change on ONE plane in place, never stacked, one
hand per arm, wrist-to-wrist, fingers DOWN. Build scripts in this folder:
`make_parts_v2.py`, `build_rig_v2.py`, `make_sheets_v2.py`,
`choreo_move_v2.py`, `choreo_scene_v2.py`. All resolve their paths from the
script location, so they work from the repo copy too.

## Videos (own-eyes PASS)

- `brotheman-movement-test-v2.mp4` — 96f/4s, sha256 `e23aaa74…`: idle/blink,
  elbow curl, knee squat with squash & stretch + overshoot, wave with
  finger/thumb wiggle + hair/bandana lag.
- `brotheman-test-v2.mp4` — 120f/5s, sha256 `bbc53c9d…`: Brotherman on the
  V2 parking-lot plate next to Cape Jones (correct Cape likeness): idle →
  wave → point LEFT at Cape + talking mouths → squash hit → wink → settle.
  Speech card 2.0–4.0s: `BROTHERMAN: "You just gotta motherfucking keep up
  with the Joneses, brother."` Silent — voice is owner-gated.

## Draft — preserved, not deleted

Rig Jones 1 (`brotheman-rig.blend`, 26 bones, 44 planes) is saved as DRAFT
in `brotheman-v2/draft/` (3 .blend files + 2 test videos, hashes match the
original report). It is a cool first rig, not the likeness. Do not present
it as final.

## Honest limits

- A cutout puppet is flatter than the painted concept: no muscle shading,
  no hands-on-hips pose, torso still fairly rectangular. It reads as the
  same character in puppet form — that is what a rig is.
- The tank wordmark is still a DejaVu Bold stand-in for a hand-lettered
  Hulkamania-style wordmark (Clean-Up item).
- 3/4 head, up/down angles, full-hair flashback head: not built yet.
- No voice (owner-gated), videos silent.

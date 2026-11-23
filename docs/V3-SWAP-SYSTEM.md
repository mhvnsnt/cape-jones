# V3 Swap System — Rig Jones 2 / Clean-Up Jones 1

Rig Jones 2 = Clean-Up Jones 1: the next version of Rig Jones, built to
Gumball level, 100% their method. Standard: if it is not at Gumball level,
it is not done.

## The corrected rule (owner, 2026-11-23 10:40–10:42 EST — the handswap rejection)

1. **NO joint caps/discs/circles — ever.** Parts must JOIN correctly at
   the joint: proper elbow/knee/shoulder cuts measured from the art, the
   two pieces meeting cleanly edge-to-edge at the anatomical pivot, tight
   and attached through the full range. If a gap shows, the CUT is wrong
   — fix the cut, never cover it. A disc stuck on a joint is not industry
   standard, not professional, not commercial standard. The handswap lane
   generated a literal white disc (`rig/parts/Cap_disc.png`, placed at
   every joint by `rig/build_rig_handswap.py`); that file is NOT in this
   build and never will be. The owner was right: the circles give him
   extra anatomy he does not need, and the cut probably would have been
   good if they were never added.
2. **Arms must be TIGHT.** The arm pivots AT the shoulder, attached to
   the body, no hanging, no float, no detach at any frame — without any
   cap hiding the join.
3. **Cape: one deforming piece, cleanly — or the V2 cape.** The one-piece
   skin-weighted mesh cape in this build IS clean (one subdivided mesh,
   graded vertex groups, no cover-up, no split), so it stays. If it
   cannot be clean, it reverts to the V2 cape and that is said plainly.
4. **Every delivery names EVERYTHING added**, especially anything that
   covers a join. Hiding an added piece and not talking about it is not
   acceptable.
5. **The hands were GOOD.** The hand system is kept exactly as it is —
   one hand per arm, swap the image in place, wrist-to-wrist, fingers
   down, thumbs medial, remote device-only. The ONLY thing fixed was the
   caps and the jumpiness of the swap (see below).

## What Gumball actually does (verified first-hand, not from notes)

GB200 (`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`, opened and parsed
2026-11-23 — see `v3-swap-system/GUMBALL-FIRSTHAND.md`):
- `.fla` = ZIP of XFL XML (`DOMDocument.xml` + `LIBRARY/*.xml`).
- L_ARM/R_ARM are ONE ARM layer of 24/26 keyframes, **every keyframe a
  single DOMShape** — the whole arm+hand re-drawn per pose; the elbow
  bend is DRAWN, not jointed.
- **There is NO symbol named *CAP*, *DISC*, *BALL*, *JOINT*, or *CIRCLE*
  anywhere in the whole GB200 library.** Gumball does NOT use caps.
- The ONLY limb split is at the SHOULDER, front/back, sharing ONE
  transformationPoint (L 30.05, 47.75; R 29.95, 47) — the arm's top
  tucks BEHIND the body. There is no elbow piece at all.
- Swapping = `loop="single frame"` + `firstFrame` on a frame-addressed
  comp. Mouth = ONE 124-frame MOUTHCOMP with viseme labels. Eyes = lid
  swaps + CLEAN_PUPILS as its own layer. Props ride a pose frame
  (SANDWICH on L_ARM f28).
- The earlier claim that Gumball uses an "overlap-cap" was WRONG and is
  struck. Never claim a method is Gumball's without opening the real
  `.fla` and showing it.

## How our rig does it (the cutout translation)

- **Socket cut, no caps.** Each joint is cut along the ball's OWN outline
  circle (RANSAC + Kasa fit on the ball's dark outline, RMS ~1.1px):
  the ball belongs entirely to the LOWER piece, the upper piece ends in
  a concave socket of the same circle. No pixel is in both pieces, none
  in neither — proven by pixel diff in `prep_art.py`. The cut follows
  the art's own contour; nothing is added. Ball circle fits: elbow R
  (58.9, 223.1) r=31.8; elbow L (109.4, 275.5) r=41.2; knee R (92.5,
  299.1) r=37.5; knee L (101.7, 297.2) r=38.9.
- **Measured pivots** (from the art, not guessed): elbow R (-1.767,
  8.681) / L (1.889, 8.183), wrist R (-1.724, 6.905) / L (1.928,
  6.905), knee R (-0.757, 5.109) / L (1.068, 5.127), shoulder
  (±1.6, 10.8), hip (±0.9, 7.47). The elbow ball centre is NOT on the
  limb's centre line and the wrist pinch is 0.12–0.33 units off it —
  that is why the hands did not sit cleanly on the wrists before.
- **Invisible swap.** ONE plane per hand/mouth slot, one common canvas
  (hands 132×144, cuff centre x=66, cuff top row 0; mouths 105×95,
  centred). Every variant is re-centred in the ART; swapping changes
  ONLY the image on that plane — same plane, same pivot, same position.
  The old 7-planes-per-side swap teleported the hand up to 0.24 units
  sideways at every swap (a literal scene cut). Eyes keep hide/show
  (two variants sharing objects — computed as a SET). Remote keeps
  hide/show, device only, no hand in the crop.
- **Parenting, verified.** `parent_keep()` builds the inverse from the
  bone TAIL — proven correct by experiment (`pivot_experiment.py`): it
  preserves the rest position AND rotates about the bone HEAD. The real
  bug was the bone heads (hand bone head sat at the fingertip 5.95, not
  the wrist 6.90) — now measured.
- **Cape: one piece, clean.** ONE subdivided mesh (6×12 grid) with
  Cape_Back_Main texture, graded vertex groups (torso/capeNeck/capeMid/
  capeTip, triangular falloff radius 2.6), armature modifier, parented
  to the TORSO chain only — never the arm. It hangs, trails the arm's
  motion (velocity-lag sway, capped ±1.5°, neck ×0.5 / mid ×1.0 / tip
  ×1.5), with lean compensation (neck 0 / mid 1/2 / tip full) so the
  tip hangs vertical when the torso leans. It NEVER lifts with the arm;
  the arm passes under it. No square crop edges, no split.

## Slots

| Slot | Kind | Variants |
|---|---|---|
| handR / handL | image (one plane) | Fist, FistBack, Open, Point, Point2, Relaxed, Grip (7 each, per-side sets) |
| mouth | image (one plane) | Closed, Open, Shout, Smile, Teeth |
| eyes | visibility | Normal (both white eyes), Pupils (white eyes + pupils) |
| forearmR / forearmL | visibility | Standard |
| remote | visibility | Device (device-only crop, Grip frames only) |

Interaction: click a part to make its slot active; scroll the mouse wheel
to roll through variants in order (scrolling back and forth plays like an
animation); ESC / RMB exits. Sidebar panel `CJ_PT_slots` with < > buttons.
Headless API: `cj_set_slot(arm, slot, index)` — index wraps.

## Files

`production/2d-parking-lot/v3/`:
- `prep_art.py` — socket cuts + hand/mouth re-centring + `art-geometry.json`
  (single source of truth: balls, wrists, plane centres, ball-local offsets,
  Grip finger centre). Copies only; `rig/` untouched.
- `cj_swap_addon.py` — slot system (image-swap + visibility slots).
- `build_v3.py` — rig build → `purple-lot-v3-rig.blend` (17 bones, 7 slots).
- `v3_keys.py` → `v3_keys.json` (240 keyframes, 480f) / `v3_test_keys.json`
  (60 keyframes, 120f short test).
- `dump_v3.py` — per-frame transforms + cape grid + per-frame `tex`.
- `pil_render_v3.py` — PIL rasteriser (cape warp per cell).
- `verify_v3.py` — the gate: 1 hand/side (single plane), 1 mouth,
  ball==socket, shoulder/wrist attached, cape hanging, remote on grip,
  swaps invisible (art centred). Exit 0 = pass.
- `assemble_v3.py` — full 480f cut (sodium → purple, hard cuts, black tail).
- `assemble_test_v3.py` — short-test assembler (sodium only).
- `GUMBALL-FIRSTHAND.md` — the GB200 evidence. `CN-IN-OUR-LANGUAGE.md` —
  every CN system in their language and what it becomes in ours.
- `pivot_experiment.py` — the parent_keep proof.

## Proof

- Short test (120f, 5s): `VERIFY PASS: 120 frames`, own-eyes at every
  beat and frame-by-frame around each swap (f31 Fist→Open, f37
  Open→Point, f43 Point→Grip) — swaps invisible, no caps, no gaps,
  wrist at forearm wrist, arm pivoting at shoulder attached to body,
  cape hanging one piece.
- Full cut (480f, 20s): `VERIFY PASS: 480 frames`, own-eyes at all 8
  beats (f1/f100/f150/f230/f313/f350/f440/f475).
- The V3 cut itself is NOT landed without the owner's call.
- The rejected handswap cut (`purple-lot-v2-handswap.mp4`) and the
  rejected V3 v1 cut (sha `83b740a4…`) are NOT landed. The handswap rule
  landing is HELD until the rule is rewritten to this corrected build —
  this document IS that rewrite.

## Next

- Crossover clip (authorized 2026-11-23 09:05 EST): 10s or 30s, Cape
  Jones walking through all of Gumball's settings, made exactly how they
  make their show. Needs: Gumball settings from the vault (school,
  house, town confirmed; pull order slice 74 backgrounds first, then
  school, house/town, then puppets).
- Rig Jones 3: per-frame drawn arm+hand set, full 124-frame viseme
  library, live Wiggle 2 cape sim, AnimLab peg/deformer proof.

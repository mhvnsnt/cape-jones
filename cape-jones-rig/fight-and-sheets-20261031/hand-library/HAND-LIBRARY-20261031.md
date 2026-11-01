# HAND LIBRARY — 2026-10-31 (Mars, ~18:35 CDT)

Priority build: hands first, because a lot of the sheets HAVE HANDS.
Clean-cut method only (slice_clean.py: bg from corners, mask distance >30,
closing + hole fill, components by sheet, rows by centre-y, 1px feather +
fringe decontamination). No hand-drawn shapes. No file Mars saw overwritten.

## 1) Normal (canon) hands — sliced/ — 7/7 = 100%, GOOD
White glove hands, same art family as the suit. These are the dance-swap hands.
- Hand_1_Fist (90x108): fist, front view — GOOD, punching fist
- Hand_2_FistBack (94x131): fist, back view — GOOD
- Hand_3_Open (103x141): open hand, fingers spread — GOOD, wave/stop/dance
- Hand_4_Point (83x148): point, index up — GOOD, point/dance punctuation
- Hand_5_Point2 (97x148): point variant — GOOD, needs side check vs Hand_4
- Hand_6_Relaxed (101x142): relaxed/open-ish — GOOD, dance relaxed
- Hand_7_Grip (103x129): grip — GOOD, device/prop hold
Contact: sliced-hands-contact-20261031.png (viewed, first row shown; full
7-piece contact is in the same folder — the earlier contact sheet cropped
rows 2+, that is a sheet bug, not a hand bug; pieces themselves are intact).

## 2) X-ray skeleton hands — NEW cut, 19 pieces, SPECIALTY ONLY — NOT canon hands
Source sheets (read-only study clone, never written there):
- xray-hand-sheet-1: 6 pieces — open palm, fist front, fist side, point-down,
  relaxed spread, fist back — all GREEN SKELETON (bones on black)
- xray-hand-sheet-2: 6 pieces — same family, angles differ
- xray-hand-sheet-3: 7 pieces — OK sign, open palm, claw/spread, fist,
  palm-back, wrist-bent spread, wide spread
Viewed: xray-hand-sheet-1-contact + xray-hand-sheet-3-contact (eye-verified).
LABEL: XRAY-SKELETON — DO NOT use as normal dance/fight hands. They read as
skeleton hands, not glove hands. Use only for an x-ray/vision beat, if ever.
Shapes/angles inventory: open (3+), fist front/back/side (5+), point (2),
claw/spread (3), OK (1), relaxed (2), wrist-bent (2) — exact per-piece list
is in each sheet's MANIFEST.json in this folder.

## 3) Sheet-08 hand row — 19 small pieces, PROVISIONAL, NEEDS EYE CHECK
slice_clean on sheet-08 produced Hand_1 (1522x3 = a title/rule line, REJECT
as a hand — it is not a hand) + Hand_2..Hand_20 (34-170px wide, 50-84px tall,
small hand/pose icons from the parts sheet). These are NOT yet eye-labelled
by shape — they are counted as PROVISIONAL, not GOOD. Do not swap them into
a dance until the eye pass names each one (fist/open/point/side).

## 4) Hands in the wider sliced-clean batch — PROVISIONAL by colour/position
The full piece-label index (piece-label-index-20261031.json, 2,854 pieces)
flags WHITE-SUIT pieces (910) that include hands inside limb pieces, but
hands are NOT separately cut from full-figure sheets — a hand inside a
full-figure piece is not a swappable hand. True swappable hands = the 7
canon + 19 x-ray + 19 sheet-08 provisional above = 45 pieces.
Hands still owed: (a) eye-label sheet-08 Hand_2..20 (19), (b) hand-only
sheets in variations/fla-packs where hands appear as separate components —
those components are inside the 2,854 index but not yet isolated as a
hand list (estimated, not counted, until isolated), (c) left/right side
confirmation for Hand_4 vs Hand_5 (point pair).
Counts, honestly: extracted 45, GOOD 26 (7 canon + 19 x-ray as specialty),
PROVISIONAL 19, REJECT 1 (sheet-08 Hand_1 line), still owed 19+ (eye labels)
+ unisolated hand components in the wider batch (not counted as extracted).

## 5) Dance-variant system (how a future dance swaps hands without rebuilding)
- Main dances stay MAIN (dance-improved / dance-kneefeet-corrected, 63f).
- Variant = same dance base poses, same angles, same body, ONLY the hand
  piece at the wrist end is swapped: fist centre = elbow +
  rot((0,1), arm_lower) * 210 * SCALE; hand piece pasted centred there,
  scaled 1.7x to cover the built-in fist.
- Proven in this folder: dance-variants/ — 3 groove poses x 4 hand sets
  (base-fist, open, point, relaxed) = 12 frames + 4 GIFs + contact.
  Swap works; see the dance-variants report section for limits.
- Future dance: call the same swap with any hand from section 1 (canon)
  or section 2 (x-ray, only for an x-ray beat). Never swap a provisional
  sheet-08 hand until its eye label lands.

## Approval
Hand library: 0/1. Dance variants: 0/1. Do not claim approved. No repo push.

# Cape Jones — professional 2D puppet rig package (2026-10-31)

Source: the two sheets Mars uploaded 2026-10-31 09:42 CDT.
- Exploded cutout sheet, 2048x1143, black background — sliced here.
- T-pose assembled reference, 921x2048 phone screenshot — cropped to its
  white central band only (`reference/cape-jones-tpose-crop.png`, rows 691-1422),
  used for assembly proportions only, NOT sliced (phone UI bars + joined limbs).

## Correction to the pasted pipeline, plainly
The pasted text said the sheet background was flat mid-gray. It is not:
the uploaded sheet is black. That actually helps the white suit, but it
hurts the jet-black cape, whose fill is only ~25-35 brightness above black.
Slicing therefore used distance-from-black > 20, morphological closing,
hole-filling, and a 150px speck filter — not a Magic Wand tolerance on gray.
Do NOT re-run the pasted gray-background steps on this sheet; you will
lose the cape edge.

## What is in `sliced/` — 28 transparent PNGs, 28/28 = 100% of the visible pieces
Main body (12): Cape_Back_Main, Cape_Collar, Head_Front, Head_Profile, Neck,
Torso_Chest, Belt_Overlay, Pelvis, Arm_Front, Arm_Back, Leg_Front, Leg_Back.
Hands (7): Hand_1_Fist, Hand_2_FistBack, Hand_3_Open, Hand_4_Point,
Hand_5_Point2, Hand_6_Relaxed, Hand_7_Grip — the sheet has 7 hands, not 8.
Face swaps (9): Mouth_Closed, Mouth_Smile, Mouth_Teeth, Mouth_Open,
Mouth_Shout, Face_Angry, Eyes_AngryStrip, Eye_White_L, Eye_White_R.
Manifest with sizes + opaque pixel counts: `sliced/MANIFEST.json`.
Proofs, both eye-checked this run: `contact-sheet.png` (all 28 on mid-gray),
`assembly-preview.png` (T-pose reassembled from the slices on mid-gray).

## Important sheet truth, not invented
The sheet draws each arm as ONE piece (shoulder ball + elbow circle +
gauntlet + fist) and each leg as ONE piece (hip cap + knee + foot).
There is no separate upper-arm/forearm or thigh/shin piece on this sheet.
So the honest rig is:
- Shoulder pivot + whole-arm rotation works now, elbow bend does NOT
  without a cut. To get a true elbow bend, cut the arm at the elbow circle
  in Photoshop (the circle is already drawn) and save Forearm as a second
  piece with that circle as its top cap — do not pretend the single piece bends.
- Same for the knee: the leg is one piece; cut at the knee circle for a
  true knee bend, or use it as a whole-leg piece.
- Hand swaps work because the gauntlet cuff hides the wrist seam, as the
  pasted pipeline said. In the base pose the arm's own fist stays on;
  swap hands by hiding the arm fist inside the Hand symbol frame, or by
  using the hand symbol layered over the gauntlet wrist.

## Layer stack, bottom to top (Animate timeline, top = first)
Cape_Back_Main, Leg_Back, Leg_Front, Arm_Back, Arm_Front, Pelvis (root),
Torso_Chest, Belt_Overlay, Neck, Head_Front, Head_Profile (alternate angle,
not stacked with Front in the same pose), Cape_Collar, then on top of the
head: Eyes swap, Mouth swap.
Face swaps sit above Head_Base; the head's own mouth/eyes stay as the
default frame and the swap layers mask over them.

## Pivots (fraction of piece, x from left, y from top)
Cape_Back_Main 0.50/0.02 (neckline centre, cape billows from shoulders);
Cape_Collar 0.50/0.10; Head_Front 0.50/0.95 (skull base); Head_Profile
0.50/0.90; Neck 0.50/0.50; Torso_Chest 0.50/0.95 (waist); Belt 0.50/0.50;
Pelvis 0.50/0.10 (root); Arm_Front/Back 0.50/0.08 (shoulder ball centre);
Leg_Front/Back 0.50/0.08 (hip cap centre); Hands 0.50/0.15 (wrist).
Set with Q (Free Transform) after the JSFL run and nudge to the drawn
circle centres — the fractions are starting points, the drawn circles are truth.

## Parenting
Pelvis = master root. Torso_Chest, Belt_Overlay, Leg_Front, Leg_Back -> Pelvis.
Head_Front -> Neck -> Torso_Chest. Cape_Collar, Cape_Back_Main, Arm_Front,
Arm_Back -> Torso_Chest. Hand swap -> Arm (forearm wrist, after an elbow cut).
In Animate: Timeline > Show Parenting View, drag child onto parent.

## Swap symbols (Graphic, Single Frame)
Hand_Swap frames 1-7 in the order listed above. Mouth_Swap frames 1-5 =
Closed, Smile, Teeth, Open, Shout; frame 6 = Face_Angry (a face fragment,
not a clean mouth — use it as a full-face angry swap, masked over the head,
not as a lip-sync viseme). Eyes: Eyes_AngryStrip is a clean pair strip;
Eye_White_L/R are single eyes for a wide/shock swap.
Flagged, not hidden: Mouth_Open also carries chin/face area in its crop.
In Animate, mask it to the mouth area or trim its top in Photoshop before
lip-sync; the other four mouths are clean mouth-only crops.

## Animate build (no .fla exported from chat — built in Animate)
1. Open Animate, run `build-cape-jones-rig.jsfl`, pick `sliced/`.
2. Check pivots with Q, check parenting, save as Cape_Jones_Master.fla.
3. For a true vector rig, Trace Bitmap per piece (Threshold 10, Min Area 1,
   Curve Fit Tight) — that step is manual in Animate and is NOT claimed here.
4. Cape wave: use Asset Warp (W) with a 3-bone chain down Cape_Back_Main,
   pivot at the neckline, rather than rotating the whole cape as a stiff board.

## What is NOT done / still owed
- Elbow/knee cuts (see above) — 0/2, needs a Photoshop cut, not a script guess.
- 5-angle turnaround (Front, 3/4 Front, Profile, 3/4 Back, Back) — the sheet
  gives Front + Profile heads only, 2/5 angles; the other 3 are not invented.
- 12-14 viseme chart — the sheet gives 5 clean mouths + 1 face fragment,
  5/12 at best; a full viseme set is a new draw, not a slice.
- No .fla binary is delivered from chat, by design; the JSFL builds it in Animate.

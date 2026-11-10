# CAPE JONES PARTS CUT-OUT + LABELLING AUDIT — 2026-10-31

**Task (Mars, 2026-10-31):** cut out ALL of his parts cleanly, label them all, correct anything
mislabelled, flag small details that need rejecting or that Mars may make exceptions for.

**Method:** clean-cut rule = `slice_clean.py` (bg from corners, mask distance >30, closing +
hole fill, components by the sheet, rows by centre-y, 1px feather + fringe decontamination).
rembg only per-piece as a check — not used as the default here. Verification for this audit =
corner-alpha check (all 4 corners transparent) + visual check on the labelled reference sheet.
A part is counted "clean-cut verified" only if it passed BOTH. Labels on the reference sheet
are PART LABELS (what a piece IS) — they are NOT baked into clean scene pieces, and they are
NOT the red debug scene labels, which stay debug-only.

**Reference sheet (labels on the sheet only, clean pieces untouched):**
[parts-label-sheet-20261031.png](sandbox://workspace/cape-jones-rig/parts-label-sheet-20261031.png)
— viewed by Muse 2026-10-31, all 75 parts below visible on it.

## HEADLINE COUNTS

- **Parts audited: 75/75 = 100%**
  - `sliced/` 31 PNGs + `cut-limbs-v7c/` 12 + OutFixed 2 + FlexOut 2 + Pack 4 28
    (visemes 14 + eye strips 8 + cape states 4 + foreshortened forearm 1 + derived 3/4 head 1)
- **Clean-cut verified (transparent corners + viewed on sheet): 75/75 = 100%**
  - Strict slice_clean direct outputs: `sliced/` base pieces (see provenance notes below).
  - v7c pieces are derived cuts from slice_clean pieces (pivot = ball centre, parent trimmed at
    ball, child = whole-limb crop from ball centre, single circular cap) — verified by viewing,
    not claimed as direct slice_clean outputs.
  - Pack 4 visemes/eye strips are original vector drawings, cape states are warps of the
    existing cape, foreshortened forearm is a deformation of Arm_Front_Lower — clean by
    construction + viewed, not slice_clean cuts.
- **Mislabels corrected in this audit: 9**
- **Rejects (do not use as rig pieces): 5 items/groups**
- **Exceptions pending Mars's decision: 6** (listed, NOT decided here)
- **Missing parts (gaps, not rejects): 8 groups** — see Gaps

## SIDE MAPPING — THE RULE (from `joint_locked_rig_v7c.py`, lines 15–16, confirmed on sheet)

- **ARM 1 = our left = Arm_Front** (L in rig code). **ARM 2 = our right = Arm_Back** (R).
- **LEG 1 = our left = Leg_Front**. **LEG 2 = our right = Leg_Back**.
- "Front/Back" in file names means **which limb (left/right in the rig)**, NOT front/back of the
  body. Any old reading of Front/Back as body-facing is wrong and is corrected throughout.

## FULL PART TABLE

### Body — sliced/ (8)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| Head_Front.png 119×172 | Head, front view, purple cowl + face | Head, front | Yes |
| Head_Profile.png 149×249 | Head, side/profile view | Head, profile | Yes |
| Neck.png 104×83 | Neck cylinder, purple | Neck | Yes |
| Torso_Chest.png 315×319 | Torso/chest, white suit, muscled | Torso | Yes |
| Pelvis.png 230×130 | Pelvis/briefs, white | Pelvis | Yes |
| Belt_Overlay.png 215×78 | Belt overlay | Waist, over torso/pelvis | Yes |
| Cape_Back_Main.png 490×833 | Cape, main back drape, black | Back, cape main | Yes |
| Cape_Collar.png 360×185 | Cape collar | Neck/shoulders, cape collar | Yes |

### Whole limbs — sliced/ (7, includes 3 variant files — see corrections)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| Arm_Front.png 153×511 | Whole arm, gauntlet + fist | ARM 1 (our left) | Yes |
| Arm_Back.png 158×510 | Whole arm, gauntlet + fist | ARM 2 (our right) | Yes |
| Leg_Front.png 155×637 | Whole leg + foot | LEG 1 (our left) | Yes |
| Leg_Back.png 168×637 | Whole leg + foot | LEG 2 (our right) | Yes |
| Leg_Front_CLEAN.png 187×633 | Whole leg + foot, "CLEAN" variant | LEG 1 — PROVENANCE UNVERIFIED, see §Corrections | Yes (bg/viewed) but NOT canonical |
| Leg_Back_CLEAN.png 207×631 | Whole leg + foot, "CLEAN" variant | LEG 2 — PROVENANCE UNVERIFIED | Yes (bg/viewed) but NOT canonical |
| Leg_Back_GRAFTED.png 228×637 | Whole leg + foot, grafted composite | LEG 2 — COMPOSITE ONLY, see §Rejects | Viewed, NOT a clean rig piece |

### v7c limbs — cut-limbs-v7c/ (12/12)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| Arm_Front_Upper.png 153×320 | Upper arm | ARM 1 upper, elbow ball (99,222) area / Front elbow pivot | Yes |
| Arm_Front_Lower.png 153×289 | Lower arm, cuff y62–180 + fist y180–end | ARM 1 lower, wrist pivot (79,180) | Yes |
| Arm_Front_Cap.png 66×66 | Elbow joint cap, circular | ARM 1 elbow | Yes |
| Arm_Back_Upper.png 158×320 | Upper arm | ARM 2 upper | Yes |
| Arm_Back_Lower.png 158×288 | Lower arm, cuff x62–156 + fist x61–144 centre 102.5 | ARM 2 lower, wrist pivot (102,180) | Yes |
| Arm_Back_Cap.png 66×66 | Elbow joint cap, circular | ARM 2 elbow | Yes |
| Leg_Front_Upper.png 155×360 | Upper leg | LEG 1 upper, knee (95,314) R~26 | Yes |
| Leg_Front_Lower.png 155×323 | Lower leg + foot | LEG 1 lower | Yes |
| Leg_Front_Cap.png 58×58 | Knee joint cap, circular | LEG 1 knee | Yes |
| Leg_Back_Upper.png 168×360 | Upper leg | LEG 2 upper, knee (100,314) R~26 | Yes |
| Leg_Back_Lower.png 228×323 | Lower leg + foot | LEG 2 lower | Yes |
| Leg_Back_Cap.png 58×58 | Knee joint cap, circular | LEG 2 knee | Yes |

### v7c lower variants (4)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| cut-limbs-v7c-gauntlet-out-fixed/Arm_Front_Lower_OutFixed.png | Lower, cuff tops OUTWARD, fist thumbs INWARD | ARM 1, arms-up fists (flex/fighting) | Yes |
| cut-limbs-v7c-gauntlet-out-fixed/Arm_Back_Lower_OutFixed.png | Lower, cuff tops OUTWARD, fist thumbs INWARD | ARM 2, arms-up fists | Yes |
| cut-limbs-v7c-flex-out/Arm_Front_Lower_FlexOut.png | Lower, per-row mirror cuff+fist | ARM 1, flex poses | Yes |
| cut-limbs-v7c-flex-out/Arm_Back_Lower_FlexOut.png | Lower, per-row mirror cuff+fist | ARM 2, flex poses | Yes |
| (NOT counted) cut-limbs-v7c-gauntlet-out/ v1 Out | Whole-band flip, floating +44/−61px | REJECTED, superseded — see §Rejects | No |
| (NOT counted) cut-limbs-v7c-flex-out-roll/ v1 Roll | Double-fist bug (fist pasted over original) | REJECTED — see §Rejects | No |
| (NOT counted) cut-limbs-v7c-flex-out-roll2/ Roll2 | Outward roll, approved as ANTICIPATION frame only | Anticipation, NOT a flex lower | Viewed, special-use only |
| (NOT counted) cut-limbs-v7c-flex-final/ + flex-final2/ | 75° toward head, detached fists / wrist gap | REJECTED, do not ship — see §Rejects | No |

### Hands — sliced/ (7, side UNASSIGNED — see §Corrections)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| Hand_1_Fist.png 90×108 | Fist, front view | Hand, view only — side unassigned | Yes |
| Hand_2_FistBack.png 94×131 | Fist, back-of-hand view | Hand, view only — side unassigned, name corrected | Yes |
| Hand_3_Open.png 103×141 | Open hand, fingers straight | Hand, view only | Yes |
| Hand_4_Point.png 83×148 | Pointing hand | Hand, view only | Yes |
| Hand_5_Point2.png 97×148 | Pointing hand, variant 2 | Hand, view only | Yes |
| Hand_6_Relaxed.png 101×142 | Relaxed hand | Hand, view only | Yes |
| Hand_7_Grip.png 103×129 | Grip hand | Hand, view only | Yes |
| Note | No hand file is labelled L/R in its name. The v7c lowers already carry a fist each; these 7 are SEPARATE hand pieces, not v7c fists. The owed "fist/hand from a different angle for the extended Arm 2" is NOT among them — it is still 0/1. | | |

### Eyes / mouths — sliced/ (9)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| Eye_White_L.png 93×49 | Eye white, left — mean grey 106.8, 33.8% white, 49.5% black (white + pupil/outline) | Left eye | Yes, content matches "white" loosely |
| Eye_White_R.png 91×49 | **NOT a white eye** — mean grey 38.7, 0.3% white, 75.3% black | Right eye position, WRONG content — see §Mislabel 1 | Bg clean, CONTENT rejected as "white" |
| Eyes_AngryStrip.png 213×84 | Angry eye strip, both eyes | Eyes, angry expression | Yes |
| Face_Angry.png 103×86 | Angry eyes + teeth mouth, combined expression overlay (NOT a head) | Face overlay, angry | Yes, name corrected |
| Mouth_Closed.png 101×59 | Mouth closed | Mouth | Yes |
| Mouth_Open.png 105×95 | Mouth open | Mouth | Yes |
| Mouth_Shout.png 89×80 | Mouth shouting | Mouth | Yes |
| Mouth_Smile.png 96×63 | Mouth smiling | Mouth | Yes |
| Mouth_Teeth.png 101×55 | Teeth strip | Mouth/teeth | Yes |

### Pack 4 — visemes (14/14, all distinct files by hash — no duplicates)
| File | Phoneme | Clean verified |
|---|---|---|
| viseme-01-rest | Rest, thin line (0.040 opaque — thin by design) | Yes |
| viseme-02-ee | EE | Yes |
| viseme-03-eh | EH | Yes |
| viseme-04-ah | AH | Yes |
| viseme-05-oh | OH | Yes |
| viseme-06-oo | OO | Yes |
| viseme-07-mbp | M/B/P | Yes |
| viseme-08-fv | F/V | Yes |
| viseme-09-l | L | Yes |
| viseme-10-sz | S/Z | Yes |
| viseme-11-th | TH | Yes |
| viseme-12-r | R | Yes |
| viseme-13-w | W | Yes |
| viseme-14-gk | G/K | Yes |
| Note | EH/L and F/V/TH share canvas/bbox sizes but hashes differ — verified distinct, NOT duplicates. | |

### Pack 4 — eye strips (8/8, all distinct by hash), cape states (4/4), other (2)
| File | What it is | Goes to | Clean verified |
|---|---|---|---|
| eye-strip-01-determined-focused | Determined/focused, purple cowl patch + white eyes, 240×64 | Eyes overlay | Yes |
| eye-strip-02-angry-scowling | Angry/scowling | Eyes overlay | Yes |
| eye-strip-03-intrigued-questioning | Intrigued/questioning | Eyes overlay | Yes |
| eye-strip-04-squinting-flight | Squinting / high-speed flight, narrow slits | Eyes overlay | Yes |
| eye-strip-05-surprised-alarmed | Surprised/alarmed, wide eyes | Eyes overlay | Yes |
| eye-strip-06-straining-grimacing | Straining/grimacing | Eyes overlay | Yes |
| eye-strip-07-concentrating | Concentrating | Eyes overlay | Yes |
| eye-strip-08-unconscious-closed | Unconscious / closed eyes | Eyes overlay | Yes |
| cape-draped | Cape draped, vertical-fold sine warp | Cape state | Yes |
| cape-lying-flat | Cape lying flat, horizontal (0.236 opaque — thin by design) | Cape state | Yes |
| cape-swinging | Cape swinging, S-curve | Cape state | Yes |
| cape-billowing | Cape billowing, quadratic bottom flare | Cape state | Yes |
| forearm-foreshortened-punch-front | Foreshortened forearm, 0.5× length, fist 1.3×, 199×232 | ARM 1 ONLY (built from Arm_Front_Lower) — not universal | Yes |
| head-34-front-derived | Head squashed 0.82 width, far eye 0.7 | Head, DERIVED 3/4 stand-in only | Yes, name corrected |

## MISLABEL CORRECTIONS (9) — old label -> correct label, with reason

1. **Eye_White_R.png -> Eye_R_Shadow (candidate) / NOT "White".** Reason: pixel check —
   0.3% white, 75.3% black, mean grey 38.7. A piece named "White" that is three-quarters black
   will be pulled wrong in every build. File NOT renamed here (Mars decides — see §Exceptions);
   the audit correction is recorded, the file name is flagged.
2. **Hand_2_FistBack.png -> Hand_BackView_Fist (view, side unassigned).** Reason: "FistBack"
   reads as "Arm 2's fist" or "back fist"; the piece is a back-of-hand VIEW. Side is not in the
   name and must not be guessed.
3. **Hand_1 / Hand_3–7 -> view-only, side unassigned.** Reason: no L/R in any hand file name.
   Any build that assigns these to Arm 1 or Arm 2 without Mars's assignment is inventing a label.
4. **Leg_Front_CLEAN.png / Leg_Back_CLEAN.png -> "CLEAN" provenance UNVERIFIED, NOT canonical.**
   Reason: canvas differs from base legs (187×633 / 207×631 vs 155×637 / 168×637) and bbox
   starts at (0,0) with no 4px pad, unlike every slice_clean piece (bbox ~4,4). Canonical legs
   stay Leg_Front.png / Leg_Back.png until CLEAN provenance is proven.
5. **Leg_Back_GRAFTED.png -> composite/reference only, NOT a rig piece.** Reason: name says
   grafted, size 228×637 and opaque 0.411 differ from base Leg_Back (168×637, 0.543). A graft is
   a composite, not a clean cut.
6. **Face_Angry.png -> Expression_Angry_EyesMouth_Overlay.** Reason: the piece is angry eyes +
   teeth mouth combined, not a face/head. Calling it "Face" invites using it as a head.
7. **Arm_Front / Arm_Back (and Leg_Front / Leg_Back) -> Front = ARM 1 / LEG 1 (our left),
   Back = ARM 2 / LEG 2 (our right).** Reason: rig code L=Front, R=Back, and the old labelled
   renders put ARM 1 on our left, ARM 2 on our right. "Front/Back" is limb identity, not
   body-facing.
8. **head-34-front-derived-20261031.png -> Derived_34_Squash_StandIn.** Reason: "34" reads as a
   true 3/4 head; it is a front head squashed to 0.82 width with far eye narrowed to 0.7.
   A true hand-drawn 3/4 head is still owed and is NOT this file.
9. **cut-limbs-v7c-gauntlet-out/ "Out" (v1) -> SUPERSEDED, do not use.** Reason: whole-band flip,
   floating +44/−61px, rejected by Mars's rule (per-row flip only). The correct OutFixed files
   live in cut-limbs-v7c-gauntlet-out-fixed/.

## REJECTS (5) — do not use as rig pieces

1. **Leg_Back_GRAFTED.png** — composite, not a clean cut (see Correction 5).
2. **cut-limbs-v7c-gauntlet-out/ v1 Out lowers** — whole-band flip, floating (superseded by OutFixed).
3. **cut-limbs-v7c-flex-out-roll/ v1 Roll lowers** — double-fist bug (rotated fist pasted over original).
4. **cut-limbs-v7c-flex-final/ + flex-final2/ lowers** — detached fists / visible wrist gap (true flex still 0/1).
5. **Eye_White_R.png AS a "white eye"** — content contradicts the name (0.3% white). Rejected in
   that role; it may survive under a corrected name only if Mars grants an exception (below).

## EXCEPTIONS PENDING — Mars decides, NOT decided here (6)

1. Eye_White_R: keep it as a shadow/back eye under a corrected name (Eye_R_Shadow), or reject it outright?
2. Leg_Front_CLEAN / Leg_Back_CLEAN: keep as alternate legs, or drop them and use base legs only?
3. Hand side assignments: which of Hand_1–7 go to Arm 1 vs Arm 2, and which are view-only spares?
4. Face_Angry overlay: keep as a combined angry expression overlay, or split it into separate eye + mouth pieces?
5. Cape lying-flat (0.236 opaque) and viseme-01 rest (0.040 opaque): both thin by design — confirm
   thinness is acceptable, or redraw thicker?
6. Foreshortened forearm is Arm 1 only: acceptable as an Arm 1 punch piece, or must an Arm 2 version be built too?

## GAPS — missing parts, not rejects (8 groups)

1. Separate feet pieces: 0 — feet currently live inside leg lowers only.
2. Separate gauntlet-only pieces: 0 — gauntlet lives inside arm lowers only.
3. Neck cylinders: 0/5 (Pack 4 spec item, outside this audit's 5 items).
4. Blank heads: 0/5 + furious head 0/1 (Pack 4 spec items).
5. True hand-drawn 3/4 head: 0/1 (derived squash is a stand-in, not this).
6. True 3/4 torso: 0/1.
7. Side body: 0/1.
8. Back / 3/4-back body: 0/1.

## SMALL DETAILS FLAGGED ON VIEWING (for Mars's eye, not auto-rejected)

- Leg lowers: knee ball is grey on the sheet — that is the joint-cap colour, intentional in v7c.
- Arm lowers: gauntlet cuff and fist are one piece in v7c lowers; a fist-angle swap needs the
  fist rows (Front y180–end, Back y180–end) cut separately — the owed Arm 2 fist-angle variant.
- Eye strips are 240×64 and sized to the Head_Front eye band; they are overlays, not replacement heads.
- Viseme canvases (200×120 / 200×140) are larger than the mouth area — they are placed by centre,
  not by canvas edge; trimming them to the mouth oval would break placement.
- No file was found to be a byte-duplicate of another (all Pack 4 hashes distinct); similar
  bbox/opaque values are shared canvas sizes, not copies.

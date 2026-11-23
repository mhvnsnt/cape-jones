# CN Systems in Our Language — V3 / Clean-Up Jones 1

Owner direction 2026-11-23 09:54 EST: figure out how to make ALL that CN
stuff work for our show, and make everything in our show work just like the
professional industry-standard Cartoon Network commercial-grade files — all
their systems and mechanics and everything — but in OUR show's languages.

This V3 / Rig Jones 2 (Clean-Up Jones 1) build is the first piece of that.
For each CN system/mechanic used, this record says what it is in THEIR
language and what it becomes in OURS. Source: GB200 first-hand
(`GUMBALL-FIRSTHAND.md`) — the `.fla` was opened and read, not guessed from
the earlier dissection. Study only: method travels, CN/Gumball characters
and artwork NEVER go into show files.

## The translation table

| # | CN system — their language | Cape Jones — our language |
|---|---|---|
| 1 | **`.fla` = ZIP of XFL XML** — `DOMDocument.xml` + `LIBRARY/*.xml`, ns `http://ns.adobe.com/xfl/2008/` | **`.blend` + slots JSON** — one rig file (`purple-lot-v3-rig.blend`), one armature, slots stored as a JSON property on the armature (`cj_slots`). The `.blend` IS our `.fla`; the JSON IS our library. |
| 2 | **One master graphic symbol per view** — `GB200_GUMBALL_PUPPET_001`, `FRONTVIEW`, `BACKVIEW`, `FLOPPED` masters; main timeline 25 fps, 2730x1625, four view layers | **One armature, cameras as views** — wide ortho 71 (0, 10.08), medium 34 (±0.5, 8.6), close 26 (0, 9.6). Our "views" are the V2 camera cuts, kept verbatim. Our frame rate stays 24 fps, not their 25. |
| 3 | **Swap = `loop="single frame"` + `firstFrame`** — changing which frame of a comp shows replaces the part in place. Master: L_ARM 27 placements ff 1,2,3,…,54,55; R_ARM 29; BODYCOMP ff 1–10; HEADCOMP ff 17,32,33,85–95 | **Slot index** — `cj_set_slot(arm, slot, index)` (headless API) + `cj.slot_wheel` (click a part, scroll the mouse wheel, roll through variants in order; scrolling back and forth plays like an animation) + sidebar panel `CJ_PT_slots` with < > buttons. Index IS `firstFrame`; the variant list IS the comp's frames. **v2: image-swap slots** (handR/handL/mouth) — ONE plane per slot; swapping changes ONLY the image on that plane. The old 7-planes-per-side swap teleported the hand up to 0.24 units sideways at every swap (a literal scene cut); the single-plane swap is invisible. |
| 4 | **MOUTHCOMP = ONE frame-addressed library** — 124 keyframes, sections HAPPY_LIPSYNCH f0–16, SAD_LIPSYNCH f17–36, MOUTH_HOLD_POSE f37–78, STD_EXTRA_MOUTH_FOR_LIPSYNCH f79–104, STD_LIPSYNCH_BIG_MOUTH_HAPPY f105–121; viseme labels (HAPPY_REST/B/P,M/N,S/F/O_01-03/O,U,W/L_01-02/A_01-03-05/A,I/CH,S, SAD_* set, TEETH_SMILE_01, OPEN_SMILE_02, …). Mouth placed in HEADCOMP with the SAME transformationPoint (40.2, 9) at every keyframe | **Mouth slot, 5 variants, ONE plane** — Closed / Open / Shout / Smile / Teeth, all re-centred on one common 105×95 canvas, anchored at (0, 11.31), swapped by changing the image on the single mouth plane. Same addressing, smaller library: their 124-frame viseme set is a Rig Jones 3 step, not a V3 blocker. |
| 5 | **EYESCOMP = lid swaps + separate pupils** — sections STD_EYES f0–8, CLOSED_EYES f9–25, STD_SPECIAL_EXPRESSIONS f26–85, EXT_SPECIAL_EXPRESSION f86–104, BIG_CHEEK_STD_EYES_001 f105–124, SPECIAL_POSE_WHISTELING f125–159; layers WHITE_MASK_01/02, CLEAN_EYES_LINES, EYEBROWS, and CLEAN_PUPILS as its OWN layer (56 keyframes, 36 shapes) | **Eyes slot, 2 variants** — Normal (both white eyes) / Pupils (white eyes + pupils). Pupils are their own planes, toggled WITH the variant, exactly like CLEAN_PUPILS is its own layer. Eye whites sized to the DRAWN eyes (0.18 units — the 0.56-unit first try was caught own-eyes); pupils kept at V2's proven 0.34 (the f440 gag look). |
| 6 | **`transformationPoint` at the anatomical joint** — legs EXACTLY one pivot each (L_LEG (10.55,3.35) ×29; R_LEG (25.5,4.25) ×16); BODYCOMP 3 distinct (two within 0.05); L_ARM 3 distinct (two within 0.05); HEAD 2 within 0.05. BUT HEADCOMP 8, R_ARM 6, TAIL 8, EAR1 7 — extremes DELIBERATELY re-register. Rule as built: pivots stable for standard poses; extremes may re-register | **Bone heads measured from the art itself (v2, fitted circles)** — shoulder (±1.6, 10.8), elbow R (-1.767, 8.681) / L (1.889, 8.183), wrist R (-1.724, 6.905) / L (1.928, 6.905), hip (±0.9, 7.47), knee R (-0.757, 5.109) / L (1.068, 5.127), ankle 1.90. The v1 pivots (elbow R 8.51 / L 8.09, wrist on the limb centre line) were approximations — the elbow ball centre is NOT on the limb's centre line and the wrist pinch is 0.12–0.33 units off it, which is why the hands did not sit cleanly on the wrists. `parent_keep()` tail form VERIFIED by experiment (not the bug — the bug was the hand bone head sitting at the fingertip 5.95 instead of the wrist 6.90). The verifier (`verify_v3.py`) ENFORCES the pivot rule numerically at every frame: ball == socket at every joint, shoulder gap 0 against the MOVING shoulder point (the torso breathes/leans ±3.5° — a fixed-point check failed 422 good frames before it was fixed), wrist pinch == hand cuff. |
| 7 | **Arm = ONE drawn symbol, hand poses as LABELED arm frames** — L_ARM 12 labeled frames (f25 EXPLAINING, f26 SHRUG_SHOULDER, f27 POINTING_FINGER, f28 EATING_ARM, …, f54 FIST_CLOSED_EXTREME_POSE, f55 HAPPY_FIST); R_ARM 14 (f24 FIST_CLOSED_PERS, f26 SHRUG, …). The two sides' frame maps DIFFER — per-side sets, not mirror copies. Elbow bend is DRAWN, not jointed. **NO caps/discs anywhere in GB200** — verified first-hand 2026-11-23: L_ARM/R_ARM are 24/26 keyframes of ALL DOMShape (zero symbol instances, zero discs); there is NO symbol named *CAP*, *DISC*, *BALL*, *JOINT* or *CIRCLE* anywhere in the library; the ONLY limb split is shoulder front/back sharing ONE transformationPoint, the arm's top tucking BEHIND the body. The earlier "overlap-cap" claim was WRONG and is struck | **Cutout split at measured joints, same addressing — SOCKET CUT, no caps** — upper arm + forearm + hand are separate planes, jointed at the elbow/wrist; hand variants (Fist, FistBack, Open, Point, Point2, Relaxed, Grip — 7 per side, per-side sets, not mirrors) swap on ONE hand plane by changing the image. The joint is cut along the ball's OWN outline circle (RANSAC+Kasa fit, RMS ~1.1px): the ball belongs entirely to the lower piece, the upper piece ends in a concave socket of the same circle — no pixel in both, none in neither (pixel-diff proven in `prep_art.py`), no added piece, no cover-up. That is the cutout translation of their method: the split must be invisible, the two pieces reading as the one drawn limb. HONEST DELTA: their way (redraw arm+hand per frame) is Rig Jones 3 for us — our art is sliced, so jointed swap is the correct cutout translation. One hand per arm, ever; forearm ends at the cuff, no drawn fist. |
| 8 | **PROPS layer — a prop rides a pose frame** — SANDWICH attaches to a specific arm frame (L_ARM f28) with a full rotation/scale matrix | **Remote slot** — device-only crop (no hand inside it), visible on Grip frames only, grip point landed on the Grip hand's finger centre (verifier: within 0.20). The remote rides the Grip pose exactly the way their sandwich rides EATING_ARM. |
| 9 | **LABEL_01 / LABEL_02 named frames** — POSES_LABELS, viseme labels, expression labels on the timeline | **Variant names + keyframe labels** — Fist/Open/Point/Grip, Closed/Open/Shout/Smile/Teeth, Normal/Pupils; `v3_keys.json` carries the slot schedule per keyframe. A named pose library (their POSES_LABELS) is Rig Jones 3. |
| 10 | **Scene places the puppet with `firstFrame` + `loop` + matrix** — GB202REMOTE_Sc094: Mom puppet `firstFrame="17" loop="loop"` scale 0.53; "Mom angry run rough" steps firstFrame 6,7,8,9,10,11… with `loop="play once"` — stepping firstFrame IS how a cycle plays | **Dump keys: bone targets + slot schedule** — `v3_keys.json` (240 keyframes, 480f, on twos) → Blender evaluates the armature → `dump_v3.py` writes per-frame plane transforms + cape grid → `pil_render_v3.py` rasterises → `assemble_v3.py` cuts. The dump IS the scene placement; the keys ARE the firstFrame steps. |
| 11 | **TAIL re-registers per pose; no cape on this puppet** — the closest analogue to a cape is the TAIL, which deliberately shifts registration for extreme poses | **One-piece skin-weighted cape (our own system, built to the owner's rule)** — ONE subdivided mesh (6×12 grid) with Cape_Back_Main texture, graded vertex groups (torso/capeNeck/capeMid/capeTip, triangular falloff radius 2.6), armature modifier. It hangs from the torso and trails the arm's MOTION only (velocity-proportional sway, capped ±1.5°, neck ×0.5 / mid ×1.0 / tip ×1.5), with progressive lean compensation (neck 0 / mid 1/2 / tip full) so the tip hangs vertical when the torso leans. It NEVER lifts with the arm; the arm passes under it. No square crop edges, no split. Live Wiggle 2 sim is Rig Jones 3 — the mesh is weight-ready for it. |
| 12 | **File-making: library folders per view** — `FRONTVIEW/BACKVIEW/FLOPPED/V001`, `REF`, `PROPS`, `GB200_GB_MOUTH`, `GB200_GB_EYES` as named comps | **File-making: `v3-swap-system/`** — `prep_art.py` (derived art, copies only, `rig/` untouched), `cj_swap_addon.py` (slot system), `build_v3.py` (rig), `v3_keys.py` (choreography), `dump_v3.py` (transforms), `pil_render_v3.py` (raster), `verify_v3.py` (gate), `assemble_v3.py` (cut), `GUMBALL-FIRSTHAND.md` (the evidence), `CN-IN-OUR-LANGUAGE.md` (this file). Docs land in `docs/V3-SWAP-SYSTEM.md`. |

## What we did NOT take (yet) — next pieces of the same job

- **Chowder systems — CORRECTED 2026-11-23:** the CN vault catalogue
  (PR #441, merged `c6178384`) settled it: **Chowder is zero — no Chowder
  archive in the vault, any repo, or any release.** The 350 GB Documents
  zip holds 79,772 entries; Gumball is 1,893 files / 65.89 GB. So Chowder
  lighting/clothing/material/texture systems can NOT come from the vault —
  any Chowder work needs another source found first, or it stays unwired.
  Do not claim a vault Chowder pull. First concrete Chowder idea planned
  (pattern-lock: pattern fills anchored to screen/world space while the
  character moves, as a switchable layer in a short test, NOT baked into
  the V3 cut) still stands as a design, but its material is NOT in hand.
- **Gumball backgrounds / settings** — the vault catalogue confirms the
  school, house and town settings ARE in the vault (Gumball 1,893 files /
  65.89 GB; `.fla` count settled at 138 including the GB200 original
  puppet). Pull order is slice 74 backgrounds first, then school,
  house/town, then the puppets. Settings work waits on that pull.
- **Full viseme library** (124-frame MOUTHCOMP → our 5) and **drawn
  arm+hand per frame** — Rig Jones 3 steps.
- **Crossover clip** — AUTHORIZED 2026-11-23 09:05 EST (CORRECTION of the
  earlier no-crossover reading, recorded in MEMORY.md): a 10s or 30s clip
  of Cape Jones walking through all of Gumball's settings, made exactly
  how they make their show, so he feels IN their world. V3 cut first,
  crossover clip next. The rule now reads: use CN systems/mechanics
  wholesale, adapted for OUR show; use their characters/backgrounds only
  to make our own stuff and learn how real-network files are made. The
  settings it needs are confirmed in the vault (school, house, town —
  Gumball 1,893 files / 65.89 GB; pull order slice 74 backgrounds first,
  then school, house/town, then the puppets).

## Gotchas recorded (do not re-learn)

- **Blender `hide_viewport` vs `hide_render`:** setting `hide_viewport`
  excludes the object from the depsgraph, so its `hide_render` F-Curve is
  never evaluated on `frame_set` and reads back stale. Never set
  `hide_viewport` on objects whose `hide_render` you keyframe and read
  back. (`cj_set_slot(..., set_viewport=False)` for headless callers.)
- **Shoulder point moves with the torso.** Any attachment check must derive
  the joint point from the parent plane's actual transform, not a fixed
  rest coordinate.
- **A hanging cape does not rotate rigidly with the torso.** Lean
  compensation must grow down the chain (neck 0 / mid 1/2 / tip full).
- **Slot variants that share objects** (eyes: both variants contain Eye_L/R)
  must be computed as a SET — an object shows iff it belongs to the active
  variant — or the last variant's hide wins and the whites vanish.
- **Eye art is not head art scale.** Eye_L.png renders 3× the drawn eye at
  the generic 0.95 scale. Size every slot plane against the DRAWN feature
  it covers, measured from the pixels.
- **The wrist pinch is NOT on the limb's centre line.** The forearm plane's
  bottom midpoint is not the wrist — the wrist pinch sits 0.12–0.33 units
  off the plane centre. Measure attachment against the art's actual pinch
  point (wrist_local in the geometry file), never against plane midpoints,
  or you will report a constant "gap" that is not a gap at all.
- **Swap continuity is an ART property, not a per-frame one.** A
  single-plane swap cannot move the plane (its transform is bone-driven);
  what can jump is the drawn art. Every variant's cuff must be centred
  on the common canvas (cuff centre x=66, cuff top row 0 for hands;
  opaque bbox centred for mouths) — `verify_v3.py` re-measures this from
  the PNGs. Two earlier verifier versions compared per-frame plane
  centres and failed good frames: they were measuring the arm's swing,
  not the swap.
- **NO caps, ever — verified against the real .fla, not the notes.** The
  handswap lane's claim that caps were "the Gumball method" was wrong,
  and the delivery hid the caps. Never add unasked anatomy; never claim
  a method is Gumball's without opening the real `.fla` and showing it.
  If a gap shows, the CUT is wrong — fix the cut, do not cover it.

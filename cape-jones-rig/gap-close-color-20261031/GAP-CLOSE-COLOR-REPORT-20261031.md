# Gap-close chunk C — COLOUR / BLENDER / LIGHTING — report 2026-10-31

New folder only; nothing Mars has seen was overwritten or deleted; no repo push.
No show character art/name/dialogue/logo copied — original Cape Jones only.
Labels live on sheets only, never baked into clean pieces. Every image output
below was viewed by the builder; defects found in viewing are listed at the end.

## 1. ACES 1.3 comparison — REAL BLENDER RENDERS (Cycles CPU)
- aces13-standard-20261031.png + .blend — Standard view, Cycles CPU 16 samples, 660x900
- aces13-aces13-20261031.png + .blend — ACES 1.3 view, same plate/node tree/display (sRGB)
- aces13-comparison-20261031.png — side-by-side sheet + measured deltas
- Same clean fighting pose, same 34-node/43-link tree (clean-100 proof stack);
  ONLY the view transform changed. EEVEE was NOT needed: Cycles CPU rendered
  fine (EGL console warnings are harmless noise; both renders saved/verified).
- Measured (full 660x900 frame): mean absolute delta 25.34, max 49,
  per-channel R 26.31 / G 25.61 / B 24.10.
  Samples: bg corner (129,129,129)->(104,104,104); suit torso
  (255,249,218)->(211,205,191); cowl (95,38,97)->(59,9,64);
  shadow zone (107,107,117)->(79,79,89).
- Verdict: ACES 1.3 darker/greyer; Standard remains the strict Rec.709 gamma 2.4
  finishing view. Prior ACES 2.0 (EEVEE, Rec.1886: grey 129->107, mean 24.0,
  max 73) is NOT like-for-like with this run (different engine + display),
  so no 1.3-vs-2.0 ranking is claimed. OCIO note is on the sheet.

## 2. Room-at-2.5x Blender proof — REAL BLENDER RENDER (Cycles CPU, textured planes)
- room-2.5x-blender-proof-20261031.png + .blend (1168x1060, Cycles CPU 32 samples)
- Clean apose plate over a painted room background, orthographic camera.
- SUBSTITUTION (stated, not hidden): batch-KKGuh.jpg was NOT found on disk
  (searched the whole workspace), and the locked 2.5x sheet / layout-pass-room.jpg
  both contain a LABELLED character, so neither can serve as a clean background.
  The background used is the clean-100 desk painting (no character, no labels)
  extended below with its own average floor colour (95,63,43) to reach the
  1060px locked-sheet frame height. Prep files: room-proof-bg-canvas-20261031.png,
  room-proof-char-alpha-20261031.png (grey-keyed apose alpha; prep, not a deliverable).
- Scale check: character 950px tall BY CONSTRUCTION (plane scaled 950/1041).
  Strict-threshold measurement: cowl top y=44, white-boot bottom y=974 ->
  931px; the 19px gap is feather/anti-aliasing edge loss at strict thresholds
  (feet bottom including feather lands at the designed y=985). Feet stand on
  the floor band; full body in frame. Chair-back-at-waist check is NOT
  replicable on the desk substitute (no chair in that painting) — it holds
  only against the original room painting in the locked sheet, and is not
  claimed here.

## 3. JoJo pose shifts — PIL palette replacement (NOT a gain)
- jojo-pose-shifts-fighting-20261031.png — clean fighting pose in BASE +
  TENSION, POWER, DREAM, BRIGHT PINK, with the palette table on the sheet.
- Method: v3 nearest-base classification + delta remap, clamped; black outline
  never reassigned; fringe pixels >90 from any base left untouched.
- Addendum compliance: cape is a FULL colour in all four (TENSION magenta
  (255,20,120); POWER scarlet (220,30,50); DREAM magenta-pink (255,60,180)
  per the addendum; BRIGHT PINK hot pink (255,80,200)). Suit: CHANGED in
  TENSION (rose) and POWER (red-orange); WHITE in DREAM (addendum Variant A)
  and BRIGHT PINK (pink-hour variant). DREAM cowl turquoise / skin pink-tint
  follow the addendum exactly.

## 4. JoJo sequence colour script — sheet + JSON
- jojo-sequence-colour-script-20261031.png / .json
- 5 beats at 24fps, total 216f (9.0s): 1 BASE 48f, 2 TENSION 36f, 3 POWER 48f,
  4 UNCERTAINTY 36f, 5 RETURN TO BASE 48f. Each beat: trigger, palette, scope
  (both), duration, key, rim under the SHIFTED key, return rule.
  Return rule: hard palette cut on the decision beat, never a grade fade.

## 5. Level-3 proof composites — PIL COMPOSITES (labelled as such, NOT Blender)
- level3-CJ11-spotlight-finale-PIL-20261031.png (dance pose, violet-magenta stage key)
- level3-CJ19-dual-light-PIL-20261031.png (fighting pose, gold front + cyan back)
- level3-CJ28-rooftop-sunset-PIL-20261031.png (apose, sunset key, character BASE)
- level3-proof-composites-sheet-20261031.png — combined labelled sheet
- Each: character + bright god-ray shafts + layered rim + bleed band +
  ground shadow + cast shadow + spill on character + haze + dust.
  CJ-19: BACK rim cyan (0,200,255) + FRONT inner rim amber (255,180,80).
  CJ-28: rim follows the sunset LUT, character stays BASE (ATMOSPHERE env-only).
  Masks were regenerated per pose because godray-level3 layers are not
  pose-aligned for dance/fighting; layer colours/density follow the L3 spec.
  Rooftop painting reused unchanged for CJ-28. NOT Mars-approved as L3.

## 6. Painted-background versions (partial close) — PIL
- painted-bg-room-TENSION-shifted-20261031.png
- painted-bg-room-POWER-shifted-20261031.png
- painted-bg-environment-shift-sheet-20261031.png (base bg + base char control
  vs shifted bg + base char, with the distinction spelled out)
- Method on painted art is a palette-family grade + tint overlay, LABELLED as
  a grade (a painted bg has no flat parts to reassign, so this is not the v3
  flat replacement): TENSION (1.15,0.75,1.20)+rose 0.12; POWER
  (1.20,0.80,0.65)+scarlet 0.12. Character held at BASE in both, vs the task-3
  sheet where the character is also repainted — that pairing IS the
  environment-only vs full-shift distinction. Room painting = desk painting
  (KKGuh substitute, stated in §2).

## 7. Background colour scripts (4 scenes) — sheet + JSON
- background-colour-scripts-20261031.png / .json
- Room: warm-interior (1.10,0.95,0.70), warm lamp front-left, amber rim,
  no shift, room-only 2.5x rule.
- Street: golden-hour (1.10,0.95,0.70), low sun front-right, TENSION-family
  rim only under shift; NO clean painted street art on disk, so a swatch
  panel only (labelled layout-pass-street.jpg NOT embedded).
- Rooftop: sunset-rooftop (1.15,0.80,0.70), sun low behind, rim (255,155,75),
  ATMOSPHERE environment-only.
- Alley: neon-alley-pink-cyan (0.95,0.85,1.05), dual pink front + cyan back,
  each rim named to its source, no JoJo shift. LUT gains taken from the
  CJ shot-spec family; street batch-Auzjk was likewise not found on disk.

## Defects found in viewing and fixed
- Pose-shift sheet v1: panel labels overlapped the palette-table header and
  table columns overlapped (suit strings too long). Fixed: label gap raised,
  suit cells shortened to RGB + WHITE/CHANGED tag. Re-viewed clean.
- Sequence sheet v1: file was cut off mid-save by a tool timeout (corrupt PNG).
  Rebuilt with cached classification; verified decodable; also fixed the beat-5
  table palette label (now BASE, matching the JSON).
- ACES sheet v1: title, subtitle and stats lines truncated at the right edge
  (canvas too narrow). Rebuilt wider (1444px, panels 700x954). Re-viewed clean.
- L3 sheet v1: panel captions ran into neighbouring panels. Captions shortened
  to fit panel width. Re-viewed clean.
- Part-2 build timed out twice on slow full-res mask filters; remaining pieces
  were built individually and every file was verified decodable afterwards.

## Still owed (not claimed)
- Mars approval: 0 for every artefact here (all sheets state this).
- Production (Blender) renders of the 4 pose-shift palettes and of the
  sequence beats (these are PIL palette proofs).
- Painted-background versions for the other palettes (only TENSION, POWER done).
- Full-colour cape versions of the other v3 palettes on a pose (only the 4 here).
- A clean painted street background (batch-Auzjk not on disk) and the true
  KKGuh room background (not on disk); chair-back-at-waist re-check against it.
- Blender (not PIL) Level-3 composites for CJ-11/19/28.
- ACES 1.3 vs 2.0 like-for-like ranking (needs same engine + display).

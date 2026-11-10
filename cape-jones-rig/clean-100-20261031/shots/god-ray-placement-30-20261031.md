# God-ray placement 30/30 — clean-100, 2026-10-31

**Decisions recorded: 30/30. God-ray shots: 9. Explicit Level-2 no-god-rays decisions: 21. This is NOT 30 god-ray shots forced.**

Rule: god rays first appear at Level 3. God rays are NEVER in Level 2 (Mars correction, standing). Production god rays are Blender volumetric passes (separate back volume + front volume passes), not PIL wedges. Wedge counts/angles/opacity/blur below are DRAFT preview numbers (following the viewed dual-light demo) so a shot can be previewed without guessing; the Blender volume pass is the production deliverable, and a PIL wedge preview must be labelled DRAFT if shown.

Dual-light rim ownership is recorded per shot: a back rim belongs to the back source, a front rim belongs to the front key — never swapped, never a single unnamed source wearing the other source's colour.


## Table — all 30 decisions

| Shot | Decision | Source direction | Wedges / fan | Colour | Intensity (draft) | Rim belongs to |
|---|---|---|---|---|---|---|
| CJ-01 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-02 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-03 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-04 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-05 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-06 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-07 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-08 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-09 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-10 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-11 | GOD RAYS (Level 3) | spotlight from front-top, above stage | 6 / fan 30 deg centred on stage front-top | warm spotlight white 255,220,170 | opacity 70/255, blur 25px (draft preview) | rim 220,150,255 belongs to the violet-magenta stage key (single family); spotlight shafts are the same warm-white volume, not a second rim colour |
| CJ-12 | GOD RAYS (Level 3) | sun behind, upper-right | 8 / fan 50 deg centred upper-right | warm gold 255,180,80 | opacity 70/255, blur 25px (draft preview) | rim warm amber 255,180,80 belongs to the sun-behind source (single family) |
| CJ-13 | GOD RAYS (Level 3) | sun directly behind character | 12 / radial fan 12 x 30 deg (full halo fan) | warm gold 255,200,110 | opacity 80/255, blur 20px (draft preview) | rim 255,200,110 belongs to the sun-behind source (single family) |
| CJ-14 | GOD RAYS (Level 3) | sun high behind character | 10 / fan 60 deg centred high-behind | warm sunset 255,155,75 | opacity 75/255, blur 22px (draft preview) | rim 255,155,75 belongs to the sun-high-behind source (single family) |
| CJ-15 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-16 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-17 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-18 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-19 | GOD RAYS (Level 3 dual-light) | cyan back source behind character + warm gold front beams | cyan back 12 x 30 deg; warm front diagonal beams (count per Blender volume pass, not fixed in PIL draft) / cyan radial fan behind; warm beams diagonal from front | back cyan 0,200,255; front warm gold 255,180,80 | cyan opacity 90/255 blur 18px, centre (560,802) in the viewed dual-light demo; warm opacity 70/255 blur 25px layered over back rays, under character (draft preview numbers from showcase/dual-light-cyan-back-godrays-warm-front-v2-20261031.png) | BACK rim cyan 0,200,255 belongs to back cyan source; FRONT rim warm amber 255,180,80 belongs to front warm gold key - recorded separately, never swapped |
| CJ-20 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-21 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-22 | GOD RAYS (Level 3) | sun low behind skyline | 8 / fan 45 deg centred low-behind | warm gold 255,180,80 | opacity 70/255, blur 25px (draft preview) | rim warm amber 255,180,80 belongs to the sun-low-behind source (single family) |
| CJ-23 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-24 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-25 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-26 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-27 | none, Level 2 | — | — | — | — | rim is the shot's single key/LUT rim (see shot spec) |
| CJ-28 | GOD RAYS (Level 3) | sun low behind rooftop horizon | 10 / fan 55 deg centred low-behind | warm sunset gold 255,155,75 | opacity 75/255, blur 22px (draft preview) | character rim 255,155,75 belongs to sunset LUT key; JOJO-ATMOSPHERE background shift does NOT create a second character rim |
| CJ-29 | GOD RAYS (Level 3) | city glow behind rooftop, low-behind | 8 / fan 50 deg centred low-behind | cool city blue 160,185,255 | opacity 65/255, blur 25px (draft preview) | rim 160,185,255 belongs to the back city-glow source (single cool family) |
| CJ-30 | GOD RAYS (Level 3 dual-light) | cyan back source behind character in alley + pink/magenta front neon | cyan back 12 x 30 deg; pink front beams diagonal (count per Blender volume pass) / cyan radial fan behind; pink beams diagonal from front | back cyan 0,200,255; front pink/magenta 255,178,229 | cyan opacity 90/255 blur 18px; pink opacity 70/255 blur 25px (draft preview, following the CJ-19 dual-light demo pattern - alley centre to be set on the alley plate, NOT copied from CJ-19's (560,802)) | BACK rim cyan 0,200,255 belongs to back cyan source; FRONT rim magenta-rose 255,178,229 belongs to front pink source - recorded separately, never swapped |

## Per-shot detail

### CJ-01 — punch-windup

- Decision: NONE — Level 2. Reason: No volumetric source in shot; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-02 — punch-extend-snap

- Decision: NONE — Level 2. Reason: No volumetric source in shot; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-03 — punch-impact-locked

- Decision: NONE — Level 2. Reason: Impact energy/glow are FX passes, not god rays; no volumetric source named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-04 — punch-recover

- Decision: NONE — Level 2. Reason: Recover beat, interior street grade only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-05 — punch-across-down-placement

- Decision: NONE — Level 2. Reason: Daylight placement frame; no back volumetric source named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-06 — walk-street-contact

- Decision: NONE — Level 2. Reason: Daylight street walk; no volumetric source named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-07 — walk-town-passing

- Decision: NONE — Level 2. Reason: Evening town walk; no volumetric source named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-08 — walk-alley-night

- Decision: NONE — Level 2. Reason: Night alley walk is Level 2 by design; neon volume is CJ-30, not this shot.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-09 — dance-a

- Decision: NONE — Level 2. Reason: Dance-a stage grade only; spotlight volume is CJ-11 finale, not this shot.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-10 — dance-b

- Decision: NONE — Level 2. Reason: Dance-b stage grade only; no volumetric source named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-11 — dance-combined-finale

- Decision: GOD RAYS, Level 3. Source direction: spotlight from front-top, above stage.
- Wedges/fan: 6, fan 30 deg centred on stage front-top. Colour: warm spotlight white 255,220,170. Intensity (draft preview): opacity 70/255, blur 25px (draft preview).
- Rim ownership: rim 220,150,255 belongs to the violet-magenta stage key (single family); spotlight shafts are the same warm-white volume, not a second rim colour.
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-12 — flying-hover

- Decision: GOD RAYS, Level 3. Source direction: sun behind, upper-right.
- Wedges/fan: 8, fan 50 deg centred upper-right. Colour: warm gold 255,180,80. Intensity (draft preview): opacity 70/255, blur 25px (draft preview).
- Rim ownership: rim warm amber 255,180,80 belongs to the sun-behind source (single family).
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-13 — flying-soar

- Decision: GOD RAYS, Level 3. Source direction: sun directly behind character.
- Wedges/fan: 12, radial fan 12 x 30 deg (full halo fan). Colour: warm gold 255,200,110. Intensity (draft preview): opacity 80/255, blur 20px (draft preview).
- Rim ownership: rim 255,200,110 belongs to the sun-behind source (single family).
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-14 — flying-dive

- Decision: GOD RAYS, Level 3. Source direction: sun high behind character.
- Wedges/fan: 10, fan 60 deg centred high-behind. Colour: warm sunset 255,155,75. Intensity (draft preview): opacity 75/255, blur 22px (draft preview).
- Rim ownership: rim 255,155,75 belongs to the sun-high-behind source (single family).
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-15 — flying-forward-foreshortened

- Decision: NONE — Level 2. Reason: Spec only (foreshortened piece owed); no god rays until the piece exists and a volumetric source is named.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-16 — flex-anticipation-before-tighten

- Decision: NONE — Level 2. Reason: Anticipation frame, grade only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-17 — arms-up-reference

- Decision: NONE — Level 2. Reason: Reference pose, grade only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-18 — true-flex-double-bicep

- Decision: NONE — Level 2. Reason: Spec only (seam fix owed); no god rays until a final flex exists.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-19 — fighting-pose-forward-bicep-curl

- Decision: GOD RAYS, Level 3 dual-light. Source direction: cyan back source behind character + warm gold front beams.
- Wedges/fan: cyan back 12 x 30 deg; warm front diagonal beams (count per Blender volume pass, not fixed in PIL draft), cyan radial fan behind; warm beams diagonal from front. Colour: back cyan 0,200,255; front warm gold 255,180,80. Intensity (draft preview): cyan opacity 90/255 blur 18px, centre (560,802) in the viewed dual-light demo; warm opacity 70/255 blur 25px layered over back rays, under character (draft preview numbers from showcase/dual-light-cyan-back-godrays-warm-front-v2-20261031.png).
- Rim ownership: BACK rim cyan 0,200,255 belongs to back cyan source; FRONT rim warm amber 255,180,80 belongs to front warm gold key - recorded separately, never swapped.
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-20 — fighting-stance-arms-up-high

- Decision: NONE — Level 2. Reason: Stance frame, grade only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-21 — jump-crouch-takeoff

- Decision: NONE — Level 2. Reason: Crouch/takeoff, grade only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-22 — jump-tuck-landing

- Decision: GOD RAYS, Level 3. Source direction: sun low behind skyline.
- Wedges/fan: 8, fan 45 deg centred low-behind. Colour: warm gold 255,180,80. Intensity (draft preview): opacity 70/255, blur 25px (draft preview).
- Rim ownership: rim warm amber 255,180,80 belongs to the sun-low-behind source (single family).
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-23 — lounge-seated-room

- Decision: NONE — Level 2. Reason: Interior room, lamp key only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-24 — desk-seated

- Decision: NONE — Level 2. Reason: Interior desk, lamp key only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-25 — room-standing-device-gag

- Decision: NONE — Level 2. Reason: Interior room, lamp key only; god rays NEVER in Level 2.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-26 — dialogue-neutral-unsure

- Decision: NONE — Level 2. Reason: Spec only (visemes owed); interior dialogue, no volumetric source.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-27 — dialogue-shout-angry

- Decision: NONE — Level 2. Reason: Spec only (visemes owed); interior dialogue, no volumetric source.
- A god-ray layer added to this shot without re-levelling it to Level 3 and re-recording the source + rim ownership would fail the gate.

### CJ-28 — rooftop-sunset

- Decision: GOD RAYS, Level 3. Source direction: sun low behind rooftop horizon.
- Wedges/fan: 10, fan 55 deg centred low-behind. Colour: warm sunset gold 255,155,75. Intensity (draft preview): opacity 75/255, blur 22px (draft preview).
- Rim ownership: character rim 255,155,75 belongs to sunset LUT key; JOJO-ATMOSPHERE background shift does NOT create a second character rim.
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.
- Atmosphere note: Environment-only: background gain recorded separately (sky warm/purple shift); character gain 1,1,1, character palette unchanged.

### CJ-29 — rooftop-night-city

- Decision: GOD RAYS, Level 3. Source direction: city glow behind rooftop, low-behind.
- Wedges/fan: 8, fan 50 deg centred low-behind. Colour: cool city blue 160,185,255. Intensity (draft preview): opacity 65/255, blur 25px (draft preview).
- Rim ownership: rim 160,185,255 belongs to the back city-glow source (single cool family).
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

### CJ-30 — alley-neon-dual-light

- Decision: GOD RAYS, Level 3 dual-light. Source direction: cyan back source behind character in alley + pink/magenta front neon.
- Wedges/fan: cyan back 12 x 30 deg; pink front beams diagonal (count per Blender volume pass), cyan radial fan behind; pink beams diagonal from front. Colour: back cyan 0,200,255; front pink/magenta 255,178,229. Intensity (draft preview): cyan opacity 90/255 blur 18px; pink opacity 70/255 blur 25px (draft preview, following the CJ-19 dual-light demo pattern - alley centre to be set on the alley plate, NOT copied from CJ-19's (560,802)).
- Rim ownership: BACK rim cyan 0,200,255 belongs to back cyan source; FRONT rim magenta-rose 255,178,229 belongs to front pink source - recorded separately, never swapped.
- Production: Blender volumetric passes (separate back volume + front volume passes). PIL wedge numbers below are DRAFT preview only, not production god rays.

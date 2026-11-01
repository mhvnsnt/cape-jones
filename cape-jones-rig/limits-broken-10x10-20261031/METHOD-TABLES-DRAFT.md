# 10+10 method tables — DRAFT, proofs pending script completion

Grouping is stated plainly: methods genuinely overlap inside a group, so 10 industry +
10 experimental are named PER GROUP, not 20 per single limit. A group proof does not
claim a vendor tool ran; all image proofs in this task are PIL proxies, labelled as such.

## G1 — Drawing masters: L01 (3/4, side, back) + L14 (torso twist master)
Industry (10): 1 foreshortening by width scale, 2 layer flip for back view, 3 far-side
darkening, 4 perspective quad turn, 5 shear turn, 6 segment counter-rotation
(chest vs pelvis), 7 silhouette reference sheet, 8 model-sheet turn-around, 9 profile-head
substitution (Head_Profile exists in sliced/), 10 orthographic turn chart.
Experimental (10): 1 depth-by-scale turn, 2 scale+dark combined, 3 negative shear turn,
4 learned lineart extraction (Anime2Sketch method, proxy), 5 posterize turn test,
6 contrast turn test, 7 solarize turn test, 8 blur+sharpen turn test, 9 flip+dark back,
10 quad-back turn.
Verdict target: PARTIALLY BROKEN — derived views usable as turn approximations, NOT
hand-drawn masters. Unblocker for full break: a redrawn master (Mars decision / artist pass).

## G2 — True 3D shading: L02
Industry (10): Lambert left/right, top/bottom light, distance-transform normal,
side-weighted relight, soft normal (blur), hard normal (sharpen), rim-only, dual-light
split, gradient mesh, high-contrast relight.
Experimental (10): pseudo-depth, edge-aware smoothing, posterized faceting test,
inverted depth, blur relight, warm/cool split, scale+shade, contrast relight,
silhouette-distance shading, no-shade control.
Verdict target: PARTIALLY BROKEN — side-weighting measurable, faceting remains,
NOT a true 3D normal pass. Unblocker: a 3D model, or a true normal pass from one.

## G3 — Volumetric / GPU: L03 remainder + L20
Industry (10): sharp 0px shafts, blur 1/3/6, tiled render, low-res upscale, 16-sample,
64-sample, EEVEE-like, Cycles-like, fan shafts, parallel shafts.
Experimental (10): neon shafts, soft shafts, crisp+bloom, cross shafts, dust shafts,
god-ray PIL, volumetric fake, speed-line shafts, no-shaft control, fan+cross combined.
Verdict target: BROKEN for 2D shafts, PARTIAL for true volumetric — PIL shafts are not
Cycles volume. Unblocker for full volumetric sequence: GPU-first run (Kaggle/Colab free tier).

## G4 — Gates / tooling: L04 cowl gate, L06 comparison, L07 Ruffle, L17 JSFL, L18 Grease Pencil
Industry (10): overlap px, edge interruption, angle delta, axis delta, fist offset,
alpha bbox, red-label px, knee angle, foot angle, collar overlap.
Experimental (10): edge continuity, silhouette symmetry, limb-length ratio,
joint-ball radius, layer-order check, temporal smoothness, flow magnitude, depth order,
mask coverage, confidence vote.
Verdict target: PARTIALLY BROKEN — gate methods wired and computed on real apose alpha;
vendor runs NOT claimed. Unblockers: Ruffle binary run (official release), Animate
sign-in (Mars secure entry) for JSFL, Grease Pencil workstream report for the .blend rig,
Harmony/Animate trial installs for a true their-side comparison.

## G5 — Motion / pose keys: L09 remainder, L13 Arm1, L15 device grip
Industry (10): pivot-corrected rotation (Arm2 method applied to Arm1), lean shear,
run lean, fly tilt, grip placement L/R, 6-frame cycle, 12-frame cycle, squash,
stretch, bounce.
Experimental (10): mirrored run, double-exposure blend, speed lines, device-at-lap,
device-grip kitbash, shear run, afterglow trail, cycle resize, rotation sweep,
no-motion control.
Verdict target: PARTIALLY BROKEN — Arm1 method is gate-ready but no Arm1-fixed proof
frame was built in the original task; this task's rotation variants are proxies, and a
true forward kick / new key drawings remain owed. Unblocker: a fixed Arm1 frame built
through the v7c builder (not a PIL rotate) + a foreshortened kick piece.

## G6 — Source / decision-blocked: L10 Bonyu, L11 per-shot finals, L12 recorded audio, L16 eye pass
These are NOT broken by any method below, and none is claimed broken.
Industry (10, preparation only): source-citation intake, Mars-call intake form,
frame-size/safe-area spec template, per-shot render queue, recording session sheet,
cue sheet, eye-pass batch sheets, correction workflow, approval ledger, spec archive.
Experimental (10, preparation only): dual-orientation spec (YouTube/TikTok workstream),
track-swap audio slot, batch contact-sheet eye pass, confidence-banded labelling,
sub-template matching, synthetic test sheets, intake photo matching (canonical room),
song search in repo, dual-frame proof, automated batch QC (numeric only, never eye).
Exact unblockers: L10 source or Mars's own call; L11 Mars frame size + safe areas
(research workstream running); L12 a final recording session; L16 human eye-pass
batches, sheet by sheet. What is pulled next: the running workstreams for each.

## G7 — Gold split: L19
Industry (10): hard matte split, opaque seam 2px, gold median check, seam at 10
measured x positions, no semi-transparent overlap, bloom-isolated split, rim-only split,
wrap-only split, full-composite split, control (no split).
Experimental (10): split x sweep, gold/red band test, gradient seam test, fan seam,
cross seam, dust seam, bloom-overlap test, posterized seam, contrast seam, no-seam control.
Verdict target: PARTIALLY BROKEN — synthetic split proof holds gold exactly; a full-shot
opaque-split composite is still owed. Unblocker: a full V5 shot composite through the
opaque split.

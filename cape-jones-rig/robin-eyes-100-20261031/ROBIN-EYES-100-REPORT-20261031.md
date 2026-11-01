# Robin eyes 100% + cape check (Mars, 2026-10-31 17:33 CDT)
## Source
Repo mhvnsnt/cn-gigaleak-teen-titans, release teen-titans-complete-v1,
split ZIP TEEN_TITANS.zip.part-aa/ab (970 entries), central directory read by
authenticated range reads, 63 Robin files extracted individually (no full download).
## Count
- Archive entries: 970. Robin files found: 63 (61 with "robin" in name + 2 SG01 RBNEXPRES).
- Of 63: 10 empty Icon placeholders (0 bytes) + 6 byte-identical SG01/SG02 duplicates
  = 47 unique Robin content files.
- Unique files: 40 vector (EPS/AI, ALL rendered) + 5 raster JPG + 2 PSD.
- Eye library delivered: 25 entries (see library/manifest.json).
  Front neutral 8 (Day, Night-grey, RBN01, CC, Robin 1.ai, Head.ai, place.jpg,
  RBN01 B&W duplicate art) + side profile 1 + action 9 (CA01-03, RB01-03, DC ref 1-3)
  + expressions 01-05 (5) + laughing swirl comedic 1 + Robin 2.ai 3/4 (1) = 25.
- Zero-eye sources, checked not skipped: RBN03 back view (no eyes), swt.jpg
  (swatches only), Icons (empty), PSDs (same art as Day/Night JPGs — thumbnail
  mean abs diff 0.34 / 0.30, duplicates, 0 new shapes), CC.jpg (same sheet as CC.ai),
  SG02 model sheets (byte-identical to SG01), other B&W model sheets (eye shapes
  covered by their color versions; RBN01 B&W front DID separate and is entry #24).
## Method (no hand-drawing)
- Vector rendering: free Ghostscript 10.02.1 — Ubuntu .debs extracted locally
  (system apt was locked by OS replay and lost its Ubuntu candidates, so direct
  .deb extraction was used instead of apt install) + 10.02.1 init/Resource/ICC
  files from Artifex ghostpdl tag gs10.02.1. Fix found in the run: GenericResourceDir
  MUST end with a trailing slash or gs fails at gs_res.ps; the PNG device also
  needs the iccprofiles/ set. Toolchain kept at gsroot/ (local tooling, not a
  deliverable, not for push).
- Eye masks = verbatim white-component pixels from the renders (pixel labelling),
  never redrawn, never vector-polygoned. Strips 480x128 carry the v4 convention
  dark cowl segment image-LEFT (52,22,66) — that segment is a strip convention,
  the eye shapes themselves are pulled.
- In-mask proofs: each pair fitted to Cape Jones Head_Front openings
  (119x172 head; left x25-44, right x73-92, y72-80), height-fit, no extra black
  outline, his cowl is the mask — the approved v4 method.
- Honest limits: Day masks carry JPG compression speckle; CC masks are small
  (upscaled, speckled); swirl entry #16 is a thin-curve comedic eye, partial as
  a blob pair, kept as comedic reference only; singles (#04, #08, #09, #10,
  #17, #18, #19) are profile/3-4 views with one visible eye.
## CAPE — measured, pull TRIGGERED (outer is black)
- Production color callout (Cartoon Network, 02/25/2003, Robin CC sheet):
  "Hair, Mask, Outs. Cape, Insignia, Boots." = PMS BLACK.
  "Ins. Cape, Insignia, Laces, Belt." = PMS 115c yellow, swatch (255,225,82).
  "Eyes" = WHITE. Green PMS 336c = Shirt, Gloves, Pants — NOT the cape.
  Mars's "might be green" guess is not what the callout says.
- Back-view cape pixels measured (0,0,0) pure black.
- PULLED (transform-only reference/prop rig pieces, same method as eyes):
  library/robin-cape-black-outer.png (387x1050, back-view cape-dominant black
  region — honest: cape merges with the black suit fill in that view, this is
  NOT a cleanly separated cape-only cut) and
  library/robin-cape-yellow-lining.png (780x569, flat (205,184,125) as rendered
  in Robin 2.ai — darker gold than the PMS 115c callout swatch; both values
  recorded, neither is green).
- No green cape was pulled, because no green cape exists in the callout.
## Files
- library/ — 25 strips + eye masks + manifest.json
- proofs/ — 25 in-mask proofs on Head_Front
- library-contact-sheet.png — all 25 strips, viewed
- render/ — all 40 unique vector renders (Ghostscript)
- raw/ — all 63 extracted Robin files; manifest.json; tt-entries.json
## Still owed
- Mars approval of the library: 0/1 (v4 Day in-mask was already approved; this
  extends it to 25 entries).
- No repo push made in this task.

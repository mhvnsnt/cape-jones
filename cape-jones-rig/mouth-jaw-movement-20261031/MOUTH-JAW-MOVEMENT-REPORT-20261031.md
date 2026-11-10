# Mouth / lip / jaw movement system — Cape Jones — 2026-10-31

Status: DELIVERED, approval 0/1 for the movement system. No repo push.
No existing file overwritten. Base art untouched (mouths are pasted on the
clean masked head base, never drawn over the base plate).

## 0. What Mars ordered, and what this is not
Mars, 2026-10-31 20:35 CDT, after approving all Robin expression eyes
(especially top row number two, express01-angry, expressive, open):
get the mouths down — mouth wrinkle corners / movements, lip and mouth
movements, and some jaw movements, industry-standard stuff pulled in and
wired up 100%. Eye approval is NOT re-asked here.

This system is a movement system, not a new mouth library. It takes mouths
as input and moves mouth + lips + jaw together. It does NOT invent mouths,
does NOT use PIL vector mouths for production proofs (visemes v2 are
DRAFT BASE DEFAULT only, production rejected), does NOT duplicate EH to
paper over missing OH (OH = GAP, clean head, jaw still drops), and does
NOT use Batman/Superman mouths (0 in Teen Titans complete-v1).

## 1. Input dependency — changed during this build, stated plainly
At build start, the separate tight-cut re-cut agent's folder was EMPTY, so
the first version of this builder used the old pulled patches with a tight
bbox crop. That version is SUPERSEDED and its frames were deleted from
the phrase folder (stale EE/REST frames caused a contact-indexing bug,
see §6). The final version below uses the re-cut agent's DELIVERED output
(pahgo-mouth-fix-20261031/, approval 0/1 for that fixed version):
- MBP-front = NEW 09 model-sheet closed, FRONT. Tight patch 68x7 alpha
  bbox (source canvas 86x10). Placed 178x23.
- AH-front = 03 open smile, FRONT, used as AH. Tight patch 271x90
  (source canvas 296x98, top 8 rows + x>270 jaw fragments dropped).
  Placed 196x67. Shape cost, from the fixed agent, carried here: this is
  an open smile, NOT a shout — no upper teeth, reads smaller/softer than
  01 shout. 01 shout is 3/4 and was rejected for a front head. A front AH
  shout WITH teeth does NOT exist in this front Robin set.
- GK-front = 05 grit, FRONT, tight. Tight patch 467x69 (rows y>=69 chin/
  jaw curve dropped, 342 alpha px). Placed 188x30.
- Corner wrinkles kept by the re-cut: 0. Cape's own cheek lines are
  already in the clean head base. So this movement system ADDS 0 wrinkles.
  If Mars wants a corner wrinkle for a specific viseme, it is a labelled
  layer still owed, not silently carried. The "wrinkle" numbers in the
  measurements JSON are corner-linework presence (dark pixels in the
  patch's own corner zones, which include the mouth outline), NOT
  isolated wrinkle strokes separated from the outline. Do not quote them
  as wrinkle counts.
- Placement, fixed agent's numbers: old zone centre (251.5, 484.5).
  Mars gave direction + 0.75x, NOT pixel offsets. The fixed agent's
  interpretation, used here verbatim: LEFT -20px, DOWN +20px, scale 0.75x.
  New target centre, every viseme: (231.5, 504.5). One target for every
  viseme, so the mouth does not jump between frames (the old builder's
  17.5px x-jump is gone by construction; measured centres are the same
  target in every frame).
- Defects carried from the input, not hidden: MBP-front is FRAGMENTED,
  not a clean continuous closed line (86px source upscaled 2.45x, right
  segment slanted, merges with jaw outline at its right end). A clean,
  continuous, front, closed Robin line at usable resolution does NOT
  exist in this set. OH/OO round = 0. FV, L/SZ/TH/R/W = 0 true shapes.
  Other Titans mouths extracted = 0 (counts only: Cyborg 65, Starfire 61,
  Raven 63, Beast Boy 65, Slade 16). Batman 0, Superman 0.

## 2. How mouth, lips, and jaw move together
Builder: build_movement.py. Head base: visemes-v2 clean-head-base
(476x688, mouth zone already blanked with a feathered skin mask, so no
old mouth line bleeds through).
- Mouth chart substitution: one mouth layer, swapped per frame, exactly
  the Toon Boom Harmony mouth-chart idea (see §4). The mouth is NOT
  pasted over an old mouth.
- Lip movement is parameterised, not just swapped: per key, mouth width,
  mouth height, and jaw drop are numbers, and between keys they
  interpolate with smoothstep over 3 frames (in-between frames, not hard
  cuts). Width = lip spreading/rounding, height = lip opening/closing,
  jaw = chin drop.
- Jaw movement, honest proxy: the jaw is NOT a true rotated mandible
  mesh. The chin region below y=560 (4x head) is shifted down by
  jaw_drop, the gap is filled with the hinge row's own pixels stretched
  down (first version used a flat mean skin colour and left a visible
  hinge seam; the hinge-row fill is the fix, and the remaining faint
  hinge line on close inspection is stated in §6), and the mouth patch
  height stretches from its top — upper lip fixed, lower lip follows the
  jaw, mouth centre follows the jaw by 1/4 of jaw_drop. That reads as
  jaw drop in 2D and is labelled a proxy everywhere it is used.
- Jaw drop per key (px, 4x head): MBP 0, AH 16, GK 8, GAP 10, REST 0.
  GAP matters: on the OH gap frame there is no mouth patch, but the jaw
  still drops to 10 and the chin still shifts — the jaw is not a static
  jaw with a swapping mouth.
- Lip parameters per key (placed px): MBP 178x23, AH 196x67, GK 188x30,
  GAP 0x0. AH is the widest and tallest (open), GK is wide but short
  (spread teeth, AU12 corner pull, mapping), MBP is short (closed).

## 3. What was built and measured
- PAH GO movement: keys MBP -> AH -> GK -> GAP -> REST, 30 frames @24fps,
  1.25s. Keys every 6 frames, 3-frame smoothstep in-betweens.
  Files: pahgo-movement.gif, pahgo-movement-contact.png (key frames
  f3, f9, f15, f21, f27), frames_pahgo/ (30 PNGs),
  pahgo-movement-measurements.json (per-frame: viseme, timeline label,
  mouth_w, mouth_h, jaw_drop, mouth_cx, mouth_top, wrinkle_l/r corner
  linework counts).
- Longer phrase movement: PAH GO AH — keys MBP -> AH -> GK -> GAP -> AH
  -> REST, 36 frames @24fps, 1.5s. No invented OH/OO, no EH duplication,
  no EE (04 is front but was not re-cut tight in the fixed set, so it is
  NOT used as a movement key here). Files: phrase-movement.gif,
  phrase-movement-contact.png (key frames f3, f9, f15, f21, f27, f33),
  frames_phrase/ (36 PNGs), phrase-movement-measurements.json.
- Measured, both sequences: jaw range 0 to 16px. Max mouth height 67px
  (AH). Max mouth width 196px (AH). Sampled PAH GO key frames:
  f3 MBP 178x23 jaw 0; f9 AH 196x67 jaw 16; f15 GK 188x30 jaw 8;
  f21 GAP 0x0 jaw 10; f27 REST 178x23 jaw 0. Sampled phrase key frames:
  f3 MBP 178x23 jaw 0; f9 AH 196x67 jaw 16; f15 GK 188x30 jaw 8;
  f21 GAP 0x0 jaw 10; f27 AH 196x67 jaw 16; f33 REST 178x23 jaw 0.
  Transition frames move between those numbers (e.g. PAH GO f6
  MBP->AH 183x34 jaw 4; f12 AH->GK 194x57 jaw 14) — that is the movement,
  not a hard swap. Corner-linework counts (NOT wrinkle counts, see §1):
  MBP 265/247, AH 1224/404, GK 188/147, GAP 0/0 — AH has the most corner
  linework because it is the widest open patch, not because wrinkles
  were added.
- GIFs and contacts were viewed before reporting. The GIF preview in
  chat shows the first frame (MBP); the movement is in the full GIF and
  in the key-frame contacts.

## 4. Industry-standard methods — run vs mapping, labelled
RUN as PIL/numpy proxies in build_movement.py (vendor tools not run):
1. Toon Boom Harmony mouth chart + drawing substitution — mouth on its
   own layer, swapped per frame, masked base with no mouth bleeding
   through. Run as the substitution system itself.
2. Adobe Character Animator viseme set structure — 14-shape idea reduced
   here to the honestly covered pulled shapes (MBP, AH, GK, GAP, REST);
   the other shapes are gaps, not invented.
3. Preston Blair / Disney squash-and-stretch + slow-in/slow-out —
   smoothstep in-betweens, mouth height stretch from the top (upper lip
   fixed), jaw ease. Run as interpolation.
4. FACS parameter mapping — AU24 lip press (MBP), AU25 lips part + AU26
   jaw drop (AH), AU12 lip corner puller (GK spread), AU27 mouth stretch
   (AH height). Names are mappings to FACS; no FACS coder ran.
5. Facial-landmark anchor — single target centre (231.5, 504.5) for every
   viseme, alpha-bbox centre anchor. Run as the placement rule.
6. Mouth ROI tight cut — the fixed agent's connected-component +
   lip-contour bbox cut, reused verbatim as input. Run by that agent.
7. Mandible hinge proxy — chin shift below a hinge line, hinge-row fill.
   Run as a 2D proxy, NOT a true mandible rotation.
MAPPINGS only, with reason not run:
- MediaPipe Face Mesh mouth ROI (landmarks 61-68 lip contour) — no model
  run on this VM; the tight cut is its manual equivalent.
- Rhubarb Lip Sync / audio-driven phoneme timing — timing here is fixed
  6f/viseme; audio-driven timing still owed (recorded audio 0%).
- Toon Boom Harmony bone jaw rig, Adobe Character Animator jaw
  behaviour, Blender shape-key jaw — vendor rigs, not run; the chin-shift
  proxy is the local equivalent.
- ARKit blendshapes (jawOpen, mouthSmile, etc.) — taxonomy only, no
  ARKit run; the per-key numbers above are the local equivalent.
- True 3D mandible rotation / muscle simulation — not run; needs a true
  3D head model, which does not exist for Cape.

## 5. What this does not do yet
- Audio-driven timing 0/1. Timing is fixed 6f/viseme.
- Corner wrinkle as a separate labelled layer 0/1 (kept 0 in the input;
  add only if Mars names a viseme for it).
- Clean continuous front MBP line 0/1. Front AH shout with teeth 0/1.
- OH/OO round, FV, L/SZ/TH/R/W true shapes 0 each.
- Other Titans mouth extractions 0/5 characters. Batman mouth 0.
  Superman mouth 0.
- Full-body talking shot (head only here) 0/1. Per-shot lip-sync 0/30.
- True 3D jaw 0/1.

## 6. Corrections made during this build, not hidden
1. First version used the old pulled patches (old MBP/AH were 3/4) and
   provisional placement -12/+10. Superseded: final version uses the
   front-only tight re-cut and the fixed agent's -20/+20, (231.5, 504.5).
   Old frames were deleted, not left as a second version.
2. First jaw fill used a flat mean skin colour and leaked a full-width
   skin stripe outside the head (the first phrase contact showed it).
   Fixed: gap fill masked to the head silhouette, then filled with the
   hinge row's own pixels stretched down. A faint hinge line can still
   be seen on close inspection on high-jaw frames; that is the proxy's
   seam, stated here, not claimed away.
3. First contacts picked transition frames (f0, f6, …) and, in the phrase
   folder, stale EE/REST frames from the superseded build shifted the
   sorted-glob index, so two tiles were old frames. Fixed: contacts pick
   key frames (offset 3 in each 6-frame block) by frame-number prefix,
   stale frames deleted, and the builder now clears its frame folder at
   build start and picks contacts by frame number, so this cannot recur.
4. First wrinkle metric was described loosely; corrected in §1 and in the
   JSON notes: it is corner-linework presence, not isolated wrinkles.

## 7. Files
- build_movement.py (builder, jaw proxy, interpolation, measurement)
- pahgo-movement.gif / pahgo-movement-contact.png /
  pahgo-movement-measurements.json / frames_pahgo/ (30)
- phrase-movement.gif / phrase-movement-contact.png /
  phrase-movement-measurements.json / frames_phrase/ (36)
- MOUTH-JAW-MOVEMENT-REPORT-20261031.md (this file)

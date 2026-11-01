# METHODS INDEX — industry-standard methods pulled in, wired, proven

Wiring = a real viewed Cape Jones output, or a file verified by
re-parse where the output is a file. "Documented only" is listed as
such in the Wire-100 Sweep — it is not counted as wired.

| # | Method | Source | Wired into | Proof |
|---|---|---|---|---|
| 1 | Harmony Z-depth + drawing substitution | Toon Boom docs (Rig a Cut-out Character; Ordering Layers; Ordering in Z-Depth) | Snap gate + audit CSV as Z-keyframe table; face/cowl snap | Gate output + fixed poses, viewed |
| 2 | Animate layer parenting / reparenting at any time | Adobe blog + Learn | Snap = temporary reparent of flagged chain for one pose | snap_figure.py renders + JoJo 02 L counter-proof |
| 3 | Godot Z property + RemoteTransform2D | docs.godotengine.org (cutout animation) | Builder computes transforms from skeleton, draws chains in gate-decided passes | Ginyu 03 render matches upper-only fix within 36 px (elbow cap, correctly normal) |
| 4 | Spine keyable draw order + asset cutting | Esoteric blog | Audit CSV as draw-order table; whole-limb crops + circular caps; cowl-upper split rule | Ginyu 03 / jump fixes, viewed, no elbow gap |
| 5 | Traditional cel stacking | Traditional cutout practice | Default stack never changed; snap = documented override with gate number | 43/62 no-snap sides untouched |
| 6 | Blender Grease Pencil layer tree | Blender 5.2 manual | Mapping table: FaceSnapArm > Head > CowlUpperArm > Neck > ChestSnapArm > Torso > Collar > NormalArm > Legs > CapeBack | MAPPING ONLY in wire-100; actual GP .blend rig is a separate workstream (see Gaps) — do not claim a GP file |
| 7 | OpenToonz/Tahoma2D SO stacking-order value | OpenToonz 1.7.1 + Tahoma2D 1.6 docs | Snap = animated SO value per side per pose/frame; dance per-frame audit = frame-level SO table | Dance-arm-snap 63-frame audit |
| 8 | Knee tracking over 2nd toe / tibial rotation / foot progression angle | Sports therapy / gait literature | Knee-feet rule + per-frame gate | Correction 8/8 keyframes, 63 frames, APPROVED |
| 9 | Scapular protraction / serratus anterior (overhead arm) | Standard anatomy references | Face/cowl snap anatomy basis | JoJo 03 / Ginyu 01 fixes, viewed |
| 10 | Contrapposto / S/Z silhouette | Renaissance sculpture; Araki / SPUR 2018 (as reported) | JoJo + Ginyu Force posing | Pose dialects + Force contact sheets, viewed |
| 11 | Sentai roll-call timing (announce 12f -> snap 2f -> hold 12f+) | Sentai/tokusatsu parody origin (Toriyama, as reported) | Ginyu roll-call sequence | Roll-call contact + GIF, APPROVED |
| 12 | Silhouette test | Animation staging practice | Every pose must read in silhouette alone | Contact sheets (grey-128 viewing bg only) |
| 13 | Inbetweening: keys -> breakdowns -> inbetweens, easing, arcs, timing charts | Animation principles | Inbetween workstream (dialects + roll-call + dance) | Timing JSONs, onion-skin, easing graph (inbetween-20261031/) |
| 14 | FPS standards: 12 fps on twos vs 24 fps on ones | TV/film animation practice | Inbetween target 24 fps, >=3 inbetweens per key pair | Dance inbetweened meta: 63 -> 125 frames, 24 fps (image interpolation, LABELLED — not rig inbetweening) |
| 15 | Multiplane camera / parallax / depth-by-scale / depth-by-blur | Disney multiplane; 2.5D practice | 2.5D depth workstream (separate, see Gaps) | Not in this package as proven — workstream report pending |
| 16 | Blender compositor (SetAlpha + AlphaOver, Glare, volumetric) | Blender 5.2.3 (verified behaviour, see R13) | Wrap v2/v3/v4, god-ray L3/L4/L5, afterglow Blender renders | Viewed frames 1100x1500; punch video 24/24 Blender frames |
| 17 | Cycles volumetric (Principled Volume, Track-To spots, emission dust) | Blender Cycles practice | God-ray v2/v4, L3/L4/L5 shafts, true dust motes | Shaft layer mean RGB, px >200 counts; 120 emission motes in v4 scene |
| 18 | Intrinsic-image / 2D relighting (normal-from-depth) | Neural LightRig / GeoRelight / PIXLRelight (implementable core) | Wrap v4 normal-from-depth relight | Relit chest proof, 85,734 px differ >20 inside apose alpha |
| 19 | ACES vs Standard view transform (colour tracking) | Blender colour management | Colour-shift study; Standard remains strict L5 Rec.709 gamma 2.4 finish; ACES 1.3 = creative look | ACES 1.3 comparison: mean diff 25.34, max 49 |
| 20 | Rim follows key hue (+/-20 deg), rim lighter/brighter, bleed darker/more saturated, shadow stays cool | Colour theory + rim-color rule | All lighting / wrap / god-ray work | L2 v2 warm-rim APPROVED; gold-preserved variants measured |
| 21 | JoJo palette replacement (flat reassignment, shading as deltas, outline never reassigned) | Colour theory; Araki / David Production research (public) | JoJo v3 shifts | V3 palettes/sheets APPROVED |
| 22 | FLA/XFL parsing (DOMDocument + LIBRARY, JSFL) | Adobe Animate | Top-5 FLA labelling tool 4 | Tool script in fla-piece-labelling-top5-20261031/ |
| 23 | SWF rendering / inspection (Ruffle, free/open) | Ruffle project | Top-5 FLA labelling tool 5 | Tool script + ruffle bundle in same folder |
| 24 | OpenCV shape matching (contours, Hu moments, template matching) | OpenCV | Top-5 FLA labelling tool 1 | Tool script in same folder |
| 25 | Vision-embedding / KNN classification with confidence | CLIP-style embeddings; local classifier on labelled parts | Top-5 FLA labelling tool 2 | Tool script in same folder |
| 26 | Animation naming schema (character_part_view_angle, peg/hierarchy) | Harmony / Animate naming conventions | Top-5 FLA labelling tool 3 + labelling workflow | Tool script + correction-file workflow in same folder |
| 27 | Clean-cut segmentation (bg from corners, mask distance, closing, hole fill, feather, fringe decontamination) | slice_clean.py method (rig root) | All clean slices | 140/184 sheets = 76%, 2,854 pieces; eye pass owed on 129 sheets |
| 28 | 12 principles of animation (checklist) | Disney 12 principles | 12-PRINCIPLES-CHECKLIST-20261031.md, principles matrix 30/30 (visual proof CJ-01 only) | Matrix doc; per-shot visual proof still owed |
| 29 | TV production pipeline (storyboard -> animatic -> EDL -> edit -> titles/credits -> delivery) | TV production practice | TV-PRODUCTION-STACK-20261031.md; shot specs 30/30; EDL 30/30 (17 assumed 12f holds, flagged) | Docs; boards 21/30 poses, 9 POSE PENDING |
| 30 | ADR — architecture decision records + onboarding README + living documentation | ADR practice; documentation patterns | THIS PACKAGE (ADR-20261031.md + README order + "docs updated in the same task" rule) | This package itself; check_package.py proof |

**Not applicable, with reasons (wire-100 report, still standing unless
the 2.5D / blocker-breaking workstream proves otherwise):**
- True 3D camera depth (Maya/3D rigs) — no camera-depth axis in 2D
  cutout. Mars 18:42 CDT rejected this as final — 2.5D workstream is
  the experimental replacement, labelled EXPERIMENTAL until proven.
- Auto lip-sync layer switching for LIMB stacking — it changes which
  mouth drawing is exposed, not limb stacking. It DOES apply to mouth
  layer order (visemes v2) — wire it there, not as a limb method.

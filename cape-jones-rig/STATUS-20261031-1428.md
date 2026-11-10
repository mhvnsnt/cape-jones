# Status 2026-10-31 14:28 CDT — items built/shown in this batch, not yet PR'd

- V6 poses contact sheet: showcase/v6-poses-contact-20261031.jpg (6 poses)
- Layout passes single-scene, new: layout-pass-flying-single-20261031.jpg,
  layout-pass-rooftop-single-20261031.jpg, layout-pass-alley-single-20261031.jpg,
  layout-pass-desk-single-20261031.jpg — all at layout scale ~0.35, same as room/street/etc.
  Backgrounds are STAND-IN batch backgrounds; final painted flying/rooftop/alley/desk backgrounds still owed.
  Room scale change is ROOM-ONLY, not applied to these passes, per Mars 2026-10-31 14:20 CDT.
- Exposure sheets, new: exposure-walk-variant, exposure-dance, exposure-power-pose,
  exposure-landing, exposure-wave (wave-1/2/3 new v6 rig poses, clips/wave-*.png).
  Wave and power/landing sheets show the elbow/knee bug — they are NOT locked as final.
- Shot specs v6: SHOT-SPECS-V6-20261031.md (per-shot: punch, walk, flex, jump, dance, flying, dialogue, lounge)
- Research artifact repo log: COLOR-LIGHTING-COMPOSITING-RESEARCH-20261031.md
- Joint diagnosis (measured, not yet implemented as v7):
  Elbow ball Arm_Back (99,222) radius ~30, Arm_Front (~62,222); Knee ball Leg_Front (95,314) radius ~26, Leg_Back (100,314).
  Builder v6 elbow pivot was at upper y285 / lower y20 — that is forearm/gauntlet, NOT the ball centre.
  That is why forearm looks detached at the elbow and the bend looks square.
  Fix (industry standard, to implement as v7): pivot at ball centre for every joint,
  trim parent segment at the joint so it does not carry the child's segment,
  draw a single circular ball cap (cropped from original art, circle-masked, not square)
  centred on the pivot, over the seam, after the child segment. Same for knees.
  Do NOT just tweak punch angles. Do NOT square-crop.
- Clean-slice-all: NOT finished. Sliceable inventory includes branch sheets (251 files, 184 unique),
  viseme charts (2), model sheets (7), props (19). Clean method is slice_clean.py (component-based,
  no hand rectangles, 1px feather + fringe decontamination). Full batch is a separate gate-checked PR,
  not claimed done here.
- Room: scale 1.5x vs 2x decision still open, canonical room palette not yet identified,
  room-only scale rule recorded: when he is in batch-KKGuh room, use that room's locked scale only.

## UPDATE 2026-10-31 14:37 CDT — elbow fix v7b, user-confirmed diagnosis
User, 5 times: bend was from mid-forearm, not from elbow. Correct. v6 pivot was at
upper y285 / lower y20, which is forearm/gauntlet, not the ball. v6 upper carried a
forearm stub below the ball, so a bent arm showed TWO forearms: stub + real forearm.
v7b fix, implemented and viewed:
- Pivot = ball centre, measured: Arm_Back (99,222) R30, Arm_Front (60,222) R30,
  Leg_Front (95,314) R26, Leg_Back (100,314) R26.
- Lower piece = whole limb crop from ball centre, anchor = ball centre, so its top
  edge is inside the cap, never a square cut in mid-forearm.
- Upper trimmed at ball bottom, no child stub.
- Single circular ball cap, circle-masked from original art, drawn at pivot after lower.
- Vector pivot: elbow/knee = shoulder/hip + rotated (ball - anchor) vector, not just length.
Files: cut-limbs-v7/, joint_locked_rig_v7b.py, reposes-v7/ (6 poses),
clips-v7/punch/ (windup, extend, impact, recover), clips-v7/flex/ (flex-hold).
v6 is DO NOT USE for bent arms/legs. Other clips (walk, jump, dance, flying) still
need v7 re-render — poses are fixed, clips are not yet all re-rendered.

## UPDATE 2026-10-31 14:38 CDT — Mars approval
Mars, on punch pose v7 (reposes-v7/joint-punch-v7-20261031.png): "This one looks good. This one actually looks good."
LOCKED: v7 punch pose is approved as current. v6 punch pose is superseded, DO NOT USE.
This approval is for the punch pose image shown, not for all v7 clips, not for LUTs,
not for room scale — those still need their own looks.

## UPDATE 2026-10-31 14:44-14:49 CDT — fighting pose rename, spectrum sheet 4, lighting approval, universal pipeline
- FIGHTING POSE RENAMED (Mars, 14:44 CDT, on flex-07-flex-hold-v7c): "perfect square fighting pose, elbows clean, both arms up, squaring up, getting ready to punch" — NOT a flex. Renamed, original kept as checkpoint, to: clips-v7c/flex/fighting-pose-forward-bicep-curl-v7c.png + reposes-v7c/fighting-pose-forward-bicep-curl-v7c.png. Old name flex-hold is SUPERSEDED for this pose. OWED: a separate true flex (different pose, not this one).
- SPECTRUM SHEET 4 APPROVED (Mars, 14:46 CDT, on lut-spectrum-sheet-4): all 6 on that sheet approved — magenta-normal, magenta-deep, pink-normal, pink-deep, lime-normal, lime-deep. Spectrum approved now 6/24, sheets 1-3 (18) NOT approved. Base 30/30 still approved. Approved LUT total now 36/70 after v2 expansion below.
- LIGHTING LEVELS APPROVED (Mars, 14:47 CDT, colored + non-colored demos): both sets approved. Industry 0-5 extension written in LIGHTING-LEVELS-0-5.md (Mars wording beside industry term, 10 graded levels + shared Level 0 = 11 rows, 12 if Level 0 counted per type). Pass script: apply_lighting_levels.py (levels 0-5 x colored/noncolored, passes shadow/rim/bleed/volume/emission separate, 22 files in showcase/lighting-levels-0-5/). LIMIT: PIL script's Level 1 grade is not a .cube LUT — real LUT step is ffmpeg lut3d with the .cube files; do not present PIL L1 as the LUT grade.
- FREE-FIRST WIRING (Mars, 14:47-14:48 CDT, corrected "wiring, not watering"): wire everything in the freest way possible; anything not free, reverse-engineer the METHOD and rebuild it free — methods/systems/passes/node order, never proprietary characters/logos/assets/copied code. Doc: FREE-FIRST-WIRING.md. Free stack wired: Blender 5.2.3 LTS, FFmpeg lut3d, PIL passes, OCIO bundled with Blender. ACES transform in PIL still NOT wired — owed, not claimed.
- SPECTRUM v2 EXPANSION (built, NOT approved): 16 new 33^3 .cube files in showcase/luts-spectrum-v2/ — 8 intermediate hues (red-orange, orange-yellow, yellow-green, green-cyan, cyan-blue, blue-violet, violet-magenta, magenta-rose) x normal+deep, graded images + 2 sheets (lut-spectrum-v2-sheet-1/2-20261031.jpg), checklist lut-spectrum-v2-checklist.json.
- AUDIO CUE SHEET v2 (large print, industry fields): showcase/audio-cue-sheet-v2-20261031.jpg + audio/audio-cue-sheet-v2.csv/.json, 5 cues, -14 LUFS target, total demo 6.0s. DEMO ONLY: synthesized tones, no recorded audio claimed. Audio delivered as LINK in chat, never in-chat audio, per Mars 2026-10-31. Link expires 2026-11-02T19:49:54Z (48h Muse storage).
- UNIVERSAL PIPELINE (Mars, 14:49 CDT): UNIVERSAL-PIPELINE.md — same 11 stages for every show/character, wired here, no outsourcing to other chatbots/tools. GATE ORDER: prove good shots with Cape Jones alone first, THEN other shows, THEN more characters after a little while. A full end-to-end proof shot with him alone (effects on fist, final audio, repo-verified merge) is NOT yet claimed done.
- STILL OPEN, not dropped: punch Arm2 pick (variants in clips-v7c/punch-arm2-variants/), v7c approval for impact/flex (now fighting pose renamed — flex approval is for the fighting pose, true flex still owed), room scale 2x vs 2.5x pick, spectrum sheets 1-3 picks, spectrum v2 picks, effects anchored to fist, cleanup v2, clean-slice batch 0/184, JSFL run in real Animate, final painted backgrounds for flying/rooftop/alley/desk.

## UPDATE 2026-10-31 14:51 CDT — LABELS ARE DEBUG ONLY (Mars correction)
- Red numbered ARM 1 / ARM 2 / LEG 1 / LEG 2 circles are DEBUG tool pieces, NOT scene, NOT character. They must never get rim light or effects.
- FIXED in code, not just in words: joint_locked_rig_v7c.py now takes labels=False (clean mode); apply_lighting_levels.py refuses any plate with >100 pure-red label pixels (old v6 plate: 8,425 red pixels, refused).
- Clean re-render: reposes-v7c-clean/ 6/6 poses, 0 red label pixels each; rig-apose-v7c-clean-transparent.png, 0 red; showcase/lighting-levels-0-5-clean/ 22/22 files, 0 red in every output. Rim in clean level-2 is silhouette-only.
- Older labelled images are now marked DEBUG ONLY, not final shots. White elbow/knee joint balls stay — those are character joints, not debug labels.
- Doc: LABELS-ARE-DEBUG-ONLY.md. Push batch updated to include the clean files + updated builder/script.

## UPDATE 2026-10-31 14:54-14:55 CDT — gauntlet flip, clean Level 2 approved, v2 sheet 1, room vs LUT
- GAUNTLET FLIP (Mars, 14:53-14:54 CDT): gauntlet side panels were facing INWARD (toward chest) in the fighting pose. FIXED, only the gauntlet band: lower pieces cut at y62-180 (cuff top to bottom, measured from grid), that band flipped left-right, forearm/elbow above y62 and fist below y180 kept pixel-identical in the source piece. Builder angles/positions unchanged (arm_upper -25/25, arm_lower 160/-160, legs same), so bicep, forearm angle/direction, and fist position are unchanged. New file: reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-v7c-clean.png + comparison sheet. Pixel check before vs after: differing pixels 28,582/1,650,000 = 1.7%, all inside the gauntlet zone (bbox x285-833, y412-566 in this pose), nothing else changed. This flip is fighting-pose-specific for now; default lower pieces for other poses NOT changed until Mars approves it globally.
- CLEAN LEVEL 2 APPROVED (Mars, 14:55 CDT, on lighting-levels-0-5-clean/level-2-colored.png): "that looks great, that looks clean, that's clean as fuck." Clean Level 2 is approved. Earlier labelled Level 2 is debug-only, superseded.
- SPECTRUM v2 SHEET 1 APPROVED (Mars, 14:54 CDT): all 8 on sheet 1 — blue-violet-normal/deep, cyan-blue-normal/deep, green-cyan-normal/deep, magenta-rose-normal/deep. v2 approved now 8/16, sheet 2 (red-orange, orange-yellow, yellow-green, violet-magenta) NOT approved. Total LUTs approved now 44/70 = 63% (base 30 + spectrum 6 + v2 8).
- ROOM vs LUT (Mars, 14:54 CDT): he could not tell if room colours were affecting the LUT overlay. ANSWER, measured: a LUT MULTIPLIES what is already there, it does not paint over it. Room wall original (118,111,59) — warm brown — x magenta-rose gain (1.25,0.70,0.90) = (147,77,53) redder; x green-cyan gain (0.70,1.15,1.05) = (82,127,61) greenish, because the wall had little blue to start with. White suit (255,255,255) shows the pure LUT: magenta-rose -> (255,178,229), green-cyan -> (178,255,255). So the room always shifts the result; to judge a LUT alone you look at character-on-grey, to judge a shot you look at character-on-room. Diagnostic sheet: showcase/lut-room-vs-lut-diagnostic-20261031.jpg (room alone graded / char on grey graded / char on room graded clean, no labels). RULE going forward: every LUT approval sheet must include a grey-128 control, so room colour is never mistaken for LUT colour.

## NOTE 2026-10-31 14:56 CDT — old compositor subagent report arrived, superseded in two counts
- The 2026-10-31 ~14:31 compositor wiring subagent completed: spec + PIL stack + Blender 5.2.3 tree + 6 condition composites viewed. Its report is NOT re-surfaced as new, because two of its "still owed" items have since closed: (1) clean label-free plate now exists (rig-apose-v7c-clean-transparent.png, 0 red pixels) — its composites use the labelled v6 apose and are therefore DEBUG ONLY, not final shots; (2) LUT approvals in its report (0/30) are out of date — approved LUTs are now 44/70 (base 30 + spectrum 6 + v2 sheet 1 8). Its other owed items stand: 0/30 shots run through the stack, per-shot tuning, ACES in PIL, viewed Blender render.

## UPDATE 2026-10-31 14:58 CDT — gauntlet fixed in place, arms-up-only scope, Level 2 v2, full tracker
- GAUNTLET FIXED (Mars, 14:58 CDT): v1 gauntlet-out was flipped correctly but FLOATING — whole-band flip shifted Front cuff +44px / Back cuff -61px off its forearm/fist centre. FIX: per-row flip within each row's own alpha span (cuff band y62-180), so every row's x-range is exactly as inward, cuff sits in the exact world spot, connected to arm, panels outward. New file: reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png. v1 floating version is SUPERSEDED, do not use. Diff fixed vs inward: 17,082 pixels, bbox x323-775 y433-565 (gauntlet zone only, narrower than v1's 285-833). NOT yet approved — Mars said "then I'll approve" on this fixed version.
- SCOPE RULE (Mars, 14:58 CDT): gauntlet flip applies ONLY when arms are up / in front like this pose. Then panels must be on the outside / facing toward camera, NEVER facing inward toward each other. Other poses keep the original gauntlets until an arms-up pose is built.
- LEVEL 2 v2 (Mars, 14:57 CDT: upgrade it, cleaner, nothing stubbed, name all tools + percentages in every message): built in apply_lighting_level2_v2.py — LUT grade first, directional rim 3px lit-side fade, falloff bleed tightened 8px/0.25 -> 5px/0.20 after viewing, clean shadow (ellipse + foot pads, no blob), internal line light 12px inner band, 1px feather. Output: showcase/lighting-level2-v2/ (2 levels + 8 passes, 0 red pixels). v2 is NOT approved yet; v1 clean Level 2 remains the approved Level 2.
- TRACKER: TRACKER-20261031.md — every tool named with its wired count, every work item as completed / started / unfinished with percentages. This tracker is to be updated in every message going forward.

## UPDATE 2026-10-31 15:00 CDT — gauntlet fixed APPROVED, pose-driven swap rule locked
- APPROVED (Mars, 15:00 CDT): fixed gauntlet pose, "that one's perfect." File: reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png is now the locked reference for arms-up-in-front poses.
- RULE LOGGED INDUSTRY-STYLE (GAUNTLET-FLIP-RULE.md + pose_driven_swaps.json): pose-driven piece swap = pose space deformation / driven-key corrective (corrective tied to joint angle, Maya Pose Deformer / Blender Corrective Shape Keys) + cutout drawing substitution (extremities on separate layers, swapped per pose, Toon Boom multi-pose rig method). Driver: |arm_lower| >= 120 + forearm in front of torso. Driven: lower piece -> OutFixed at 100% when condition met, 0% otherwise, per frame, never global. Method: cuff band y62-180, per-row mirror within each row's own span, row x-ranges preserved exactly, everything else untouched.
- REGRESSION TEST: check_gauntlet_flip.py, 5/5 checks PASS. Run it before any arms-up clip ships and before any lower piece changes, so this never regresses or reverts.

## UPDATE 2026-10-31 15:02 CDT — rim-colour rule + gauntlet approval re-confirmed
- GAUNTLET: Mars re-confirmed approval 15:02 CDT ("Yeah, I approve of that") for the fixed gauntlet pose. No change — it was already locked at 15:00 CDT. Locked reference stands.
- RIM-COLOUR BUG (Mars, 15:02 CDT): v2 colored rim was cyan under a warm golden-hour grade — hue mismatch, rim must go with the colour. FIXED + VIEWED: apply_lighting_level2_v2.py now sets rim per grade — colored warm amber (255,180,80), bleed orange (255,120,0), same family; non-colored neutral white. Internal line light uses the same rim_col, so lines/rim/bleed move together. Output: showcase/lighting-level2-v2/level-2-v2-colored.png (rebuilt, viewed) + level-2-v2-colors.json with power_override field (null — no power named yet).
- RULE LOGGED: RIM-COLOR-RULE.md (industry: three-point rim colour temperature matches key/fill; gels bring fixtures to same temperature; warm ~3500K rim for warm key), AGENTS.md standing rule appended, MEMORY.md appended, tracker updated. EXCEPTION: a specific power's rim overrides grade rim for that shot only, recorded by power name in shot spec, never carried over, never changing the default. Wired: --power-rim R,G,B --power-name NAME.
- Rebuilt v2 as a whole is NOT yet approved — awaiting Mars on this warm-rim version.

## UPDATE 2026-10-31 15:04 CDT — image cache fix
- Mars caught it: rebuilt warm-rim v2 was re-shown under the SAME filename (level-2-v2-colored.png), so the client showed the cached cyan version. FIX: new file level-2-v2-colored-warm-rim-20261031.png (606,536 bytes, sha256 615a2069...), viewed, warm amber rim confirmed. Non-colored also copied dated. RULE: every changed image gets a new dated/versioned filename, never overwrite a shown file — logged in AGENTS.md standing rules + MEMORY.md.

## UPDATE 2026-10-31 15:11-15:13 CDT — warm-rim APPROVED, universe color language, dual-light god rays
- APPROVED (Mars, 15:11 CDT): Level 2 v2 warm-rim, "perfect exactly". File level-2-v2-colored-warm-rim-20261031.png is now the approved Level 2 colored version. Default rim rule stands unless (a) Mars says a power calls for it, or (b) a JoJo shift / dual-light setup is recorded.
- UNIVERSE COLOR LANGUAGE (Mars, 15:11 CDT): doc UNIVERSE-COLOR-LANGUAGE.md — Dialect 1 lighting-motivated (LUT/grade/rim follows key), Dialect 2 JoJo non-canon shifts (not from lighting, for vibe/atmosphere/tension/power/uncertainty, alone or combined, approved palettes only, trigger + return to canon base recorded). Demo sheet showcase/jojo-color-shift-demo-20261031.jpg viewed: base / tension (1.20,0.70,1.30) / power (1.30,0.60,0.60) / uncertainty near-B&W. Repo search honest note: no JoJo research doc found in Mars's repos searched (48 mhvnsnt repos, code search JoJo/Araki/non-canon, memory, local docs — only dance pose filenames + INDUSTRY-VFX-PIPELINE placeholder); research used is public Araki/David Production. If Mars names the exact repo ("emoji child repose" matches no repo name), it will be pulled in.
- DUAL-LIGHT TERTIARY (Mars, 15:13 CDT): cyan rim is valid in dual-light: warm gold front key + cyan back light radiating god rays + warm gold rays from front. Demo showcase/dual-light-cyan-back-godrays-warm-front-v2-20261031.png viewed (cyan 12 wedges + warm diagonal beams, both read). PIL version is DRAFT proof only; production = Blender volumetric passes. Rule logged in RIM-COLOR-RULE.md, UNIVERSE-COLOR-LANGUAGE.md, AGENTS.md, MEMORY.md. Shot spec must name both sources and which rim belongs to which.

## UPDATE 2026-10-31 15:17 CDT — ALL LUTs APPROVED 70/70 = 100%
- Mars approved ALL remaining LUTs: spectrum batch 1 sheets 1-3 (18) + spectrum v2 sheet 2 (8) = 26, on top of base 30/30 + spectrum sheet 4 6/6 + v2 sheet 1 8/8 = 44. Total LUTs approved 70/70 = 100%. Checklists updated (lut-spectrum-checklist.json 24/24, lut-spectrum-v2-checklist.json 16/16).
- Note: approval is of the LUTs as shown on the old labelled/room sheets. Clean grey-128 re-grades of these 26 are NOT yet built — if Mars wants them, that is a separate rebuild, not a new approval.

## UPDATE 2026-10-31 15:18 CDT — true flex built, repo pull confirmed, scope confirmed by Mars
- SCOPE CONFIRMED (Mars, 15:18 CDT): pull anything from those repos EXCEPT literal character images, character names, literal dialogue, logos. Union with standing forbidden list (also: Pokemon/Sonic cries, town names straight from their games). Allowed and wired: systems, movements, dances, rig structures, timing, poses, beat grids. No character art, no names, no dialogue, no logos were copied into this pose.
- REPO SEARCH (confirmed, by name): GitHub code search user:mhvnsnt — gumball 25 hits, Watterson 0 hits, cartoon-network 101 hits, nickelodeon 3 hits, disney 30 hits, dance 1364 hits, flex 1140 hits (most are tool/vendor noise, filtered). Real finds: cape-jones production/dance-choreo/README+INVENTORY (Darwin dance, Gumball "The Words" GB214 Sc057 198f + Sc059 twist, beat ~14f @25fps ~107 BPM, keyframed on twos, twist layer 32 keyframes f43-97); TRIPPEDD-Production-studios- production/wizard-gang-fla/docs/gumball-dissection.md (XFL parsed puppet/scene structure); docs/wizard-gang/RIG-DISSECTION.md (Smiling Friends Charlie/Pim master-symbol layer stacks, pose-swap libraries); animation-study fosters-home + grim-adventures CATALOGs (CN pipeline, Illustrator/Flash/AE — searched, NOT wired into this pose, pipeline reference only). CORRECTION: NO Richard dance exists in holdings — Richard puppet is pose libraries + model-sheet turnarounds only (1 main frame, 147 shapes, 0 sprites); the 145f export is a model-sheet presentation. Darwin is the only rig dance extracted.
- TRUE FLEX BUILT (not yet approved): reposes-v7c-clean/true-flex-double-bicep-v7c-clean.png — classic double-bicep flex, DISTINCT from fighting pose: upper arms out wide (L -70 / R 70, elbows at (253,493)/(849,487)), forearms up beside head (lower L 150 / R -150), fists above head height, legs planted wider (leg_upper -15/15). Fighting pose, by contrast: upper -25/25, lower 160/-160, fists in front of chest, elbows down at sides. Gauntlet flip NOT applied here — arms are out to sides, not up-in-front, so original lowers are correct per the gauntlet rule. Alt variant true-flex-double-bicep-alt-v7c-clean.png (upper -60/60, lower 140/-140) also built, not shown.
- WIRED, HONESTLY: this pose uses our v7c rig + double-bicep pose geometry + the repo movement principles (beat grid, on-twos keyframing) as the timing spec for the upcoming flex clip. Darwin's dance choreography itself is NOT yet retargeted to Cape Jones — that retarget is the next step, not claimed here.

## UPDATE 2026-10-31 15:22-15:24 CDT — perspective rule, flex roll, color batch done, scope final
- PERSPECTIVE (Mars 15:22 CDT, logged): arms-up inward gauntlet tops are correct ONLY if hands are pointed outward — flat/straightened hands, perpendicular to shoulders, away from head (snake-hands example). Research: forearm pronation/supination = roll around forearm long axis, radius around ulna, up to ~180 deg, palm flips without elbow/shoulder moving; 2D handling = drawing substitution, not limb movement. Rule + checklist added to GAUNTLET-FLIP-RULE.md.
- FLEX ROLL BUILT + VIEWED: reposes-v7c-clean/true-flex-double-bicep-gauntlet-out-fist-in-roll-v7c-clean.png — gauntlet tops outward, fist thumbs inward, fists rolled down/in toward neck/shoulders, biceps/forearms unchanged (upper -70/70, lower 150/-150, elbows (253,493)/(849,487)). NOT yet approved by Mars.
- SCOPE FINAL (Mars 15:23 CDT): not just dances — ANY type of move, ANYTHING helpful, barred ONLY: exact character likeness image, using their character literally, name, dialogue literally from script, brand image/logo. Everything else pull + wire.
- CHARACTER IMAGE EXCEPTION (Mars 15:24 CDT): a character image may be brought over ONLY as production reference if edited/modified during production into a parody character or a whole different character before release — never shipped as their character. Flagged transform-only in audit scope.
- COLOR BATCH DONE 2026-10-31: combined golden-hour + JOJO-TENSION (showcase/combined-golden-hour-jojo-tension-20261031.png, viewed, pink tension grade, rim in tension family); JOJO-ATMOSPHERE environment shift (showcase/jojo-atmosphere-yellow-sky-20261031.jpg, viewed, background shifted warm/purple, character base palette unchanged); shot-spec template (color-shot-spec-template.json, fields lut/rim/bleed/shift/power/dual-light, incomplete spec must not render as final); script wiring (--rim added to apply_lighting_level2_v2.py, tested to /tmp/test-l2v2, colors json records rim-override (255,178,229)).
- STILL NOT DONE: flex roll approval (Mars), deep show audit (running, subagent), repo push verification (worker pending), Blender volumetric god rays 0/1, canon approval of JoJo demo palettes, opposition pair demo (needs antagonist plate), punch Arm2 pick, room scale pick.

## UPDATE 2026-10-31 15:26 CDT — Roll2 = before-flex frame, final flex NOT done, full list requested
- Mars: Roll2 (fists outward) is a BEFORE-FLEX / anticipation frame, good in-between interpolation frame before tightening the flex. Renamed copy: reposes-v7c-clean/flex-anticipation-before-tighten-v7c-clean.png. Final flex = fists toward head + down toward shoulders.
- FINAL FLEX ATTEMPT FAILED VISUALLY: true-flex-double-bicep-final-fists-in-v7c-clean.png has detached fists (gap between gauntlet and fist, fist floating) because a 75-deg piece-space fist rotation around the wrist top edge pulls the fist base away from the gauntlet. NOT presented as done. Fix owed: rotate fist in pose space around wrist with a wrist cap/overlap to hide the seam, or rotate around a pivot inside the fist overlap zone — do not ship the detached version.
- Mars 15:26 CDT: wire up all audit pulls + all other undone wiring, get everything 100%, and list EVERYTHING (todo + completion + percentages). Top-5 wiring delegated to a subagent (Cartoon Vault FLAs, Frankie rig, Nick/Disney/PPG listings). Full list is in the reply and in TRACKER-20261031.md — nothing is claimed 100% that is blocked (Blender volumetric, JSFL/Animate, Toon Boom, RAR5 full-leak walk are blocked/unknown, listed as such).

## UPDATE 2026-10-31 15:33 CDT — PUNCH IMPACT LOCKED + TOOL PASS LOG
- PUNCH IMPACT LOCKED (Mars, 15:33 CDT, "perfect, lock that in"): clips-v7c/punch-arm2-variants/punch-impact-a2l-minus110-across-up-v7c.png — Arm2 forearm diagonal UP across upper chest, fist near centre upper chest. Locked copy: clips-v7c/punch-impact-locked-v7c.png. Punch pick now 1/1 = 100%.
- PUNCH SEQUENCE FRAME APPROVED (Mars, 15:33 CDT): -70 across-down variant — Arm2 forearm diagonal DOWN across lower chest/belly, fist lower centre. Approved as a scene placement during / before / after the punch, NOT the impact frame. File: punch-impact-a2l-minus70-across-down-v7c.png.
- ARM2 FIST-UP RULE (Mars, 15:33 CDT, reply to current-160 variant): if Arm2 fist is ever UP like that, the TOP part of the arm pad (gauntlet) must be FLIPPED, arm stays in the SAME spot, and a fist/hand from a DIFFERENT ANGLE is owed for the extended arm — fist-angle variant 0/1, not yet built. This extends the gauntlet perspective rule (hand orientation drives cuff/fist).
- TOOL PASS LOG (Mars, 15:32 CDT, standing): every pass shown must name ALL tools/resources used for that pass, in chat AND in repo. Doc: TOOL-PASS-LOG.md. First logged pass: demo-pass-flex-level2 (v7c rig + FlexOut + Level 2 v2 + golden-hour LUT, viewed, not approved as final).
- BROWSER TASKS (15:33 CDT status): Wick Editor/Animate task running, Kaggle GPU task running, Toon Boom task completed (result not yet delivered as a handoff — do NOT report its findings until that handoff arrives).

## UPDATE 2026-10-31 15:34 CDT — ROOM SCALE LOCKED 2.5x + SEATED SCALE RULE
- ROOM SCALE LOCKED (Mars, 15:34 CDT, "perfect size for the room"): 2.5x, rig 950px tall, feet on floor, chair back at his waist. Room scale pick now 1/1 = 100%. File: showcase/layout-pass-room-scaled-25x-20261031.jpg. Room-only rule unchanged: other backgrounds NOT changed.
- SEATED SCALE RULE (Mars, 15:34 CDT, approximate, to be verified visually on the seated pose): when he sits in the chair, he scales down by about 0.2 from standing — i.e. 2.5x standing -> 2.3x seated (subtract 0.2 from the scale factor, following Mars's earlier "0.5 bigger" usage which meant +0.5 to the factor). If the seated visual shows that reading as a 20% reduction instead (2.5x -> 2.0x), that is a correction to log, not a silent change.

## UPDATE 2026-10-31 15:36 CDT — JOJO-ATMOSPHERE APPROVED + MOCHIICHAO COMBINE (Mars)
- JOJO-ATMOSPHERE APPROVED (Mars, 15:36 CDT, reply to jojo-atmosphere-yellow-sky-20261031.jpg, "this is good"): environment-only shift, background warm/purple, character base palette unchanged. Atmosphere palette now 1/1 approved. Tension / power / uncertainty palettes still demo-only, NOT approved yet.
- BACKGROUND LIFE (Mars, 15:36 CDT): once animating starts, backgrounds need LIFE in them. Pull background-life systems from the Mochiichao repo + show side to help.
- CANON DISTINCTION (Mars, 15:36 CDT): Cape Jones / Space Jones has a DIFFERENT canon and a DIFFERENT show language than Mochiichao. Bring only a little Mochiichao aspect/soul into Cape Jones, like a little Western Heart aspect was brought into its soul. Do NOT merge canons.
- SPACE JONES ACTIVITIES (Mars, 15:36 CDT): not just chilling in his house, flipping lights, watching TV, bullshitting, playing video games — Mochiichao is also one of the things Space Jones does.
- HANDHELD GAG DEVICE (Mars, 15:36 CDT): Mochiichao inside Cape Jones's universe as a little handheld pocket video game — Game Boy Advance + Tamagotchi mix. GAG: it is ALWAYS in his pocket even though he has NO visible pockets.
- KAWAII / DIGICORE DANCE SOURCE (Mars, 15:36 CDT): the kawaii Tamagotchi vibe / Digicore is where a lot of the dance-scene energy comes from. Combine Mochiichao dance work (good start there) + Cape Jones dance work (Darwin beat grid, etc.) + all other pulls — combined dance scenes will be even better.
- WORK KICKED OFF: Mochiichao-combine subagent (background life systems, dance combine spec, handheld gag device design) -> MOCHIICHAO-COMBINE-20261031.md, spec/design only, not a final shot.

## UPDATE 2026-10-31 15:37 CDT — TOON BOOM TRIAL AUTHORIZED + REVERSE-ENGINEER (Mars)
- Mars authorized starting the Toon Boom Harmony 27 14-day free trial on ANY account accessible, free trial only, no purchase yet. He may still buy a subscription later.
- REVERSE-ENGINEER RULE (Mars, 15:37 CDT): reverse-engineer Harmony WHILE on the trial/subscription and build OUR OWN version. NOT cracking, NOT bypassing subscription, NOT copying Harmony code — study methods (node view, bone rigging, deformations, timeline/xsheet, symbol/instance structure) and rebuild equivalents in OpenToonz / v7c rig. Browser task started for trial signup/download + method study.

## UPDATE 2026-10-31 15:38 CDT — INDUSTRY STANDARDS PULL (Mars)
- Mars: pull in ANY industry-standard stuff that helps build all of this, from his other repos AND outside his repos, wire it up, keep working on everything else.
- Work kicked off: industry-standards subagent (12 principles checklist, studio pipeline template, colour management ACES/Rec.709, rigging standards map, audio standards, repo tools scan across 161 repos) -> INDUSTRY-STANDARDS-PULL-20261031.md, wired into rig docs, not just listed.
- Other workstreams continue in parallel: top-5 pulls wiring, clean-slice/clips, visemes/eyes/cape (pack4 done), backgrounds/Blender/ACES, free stack install, Mochiichao combine, Toon Boom trial, Wick/Kaggle browser tasks, repo push verification.

## UPDATE 2026-10-31 15:39 CDT — COMPARISON TESTS (Mars, standing)
- While building our own version: keep USING theirs, keep LEARNING as we use it, keep REVERSE-ENGINEERING, keep WIRING our own version as we use theirs, then COMPARISON TESTS to see if ours is just as good or better. Doc: COMPARISON-TESTS.md, 7 tests (rig pose, timeline/xsheet, deformation, drawing substitution, export, colour, audio sync). Tests run 0/7 — Harmony trial pending, our side ready for tests 1/3/4/6.

## UPDATE 2026-10-31 15:40 CDT — COMPARISON LOOP UNIVERSAL (Mars, standing)
- The use + learn + reverse-engineer + wire + comparison-test loop applies to ANY tool we reverse engineer and ANYTHING ELSE we reverse engineer, not just Harmony. Tools in scope: Harmony, Animate, After Effects, Maya, OpenToonz/Tahoma2D, Blender, Wick/Brinimate, any future tool in FREE-FIRST-WIRING.md. A tool is not "done" until its comparison tests are run.

## UPDATE 2026-10-31 15:41 CDT — ANIMATE ALL THREE APPROVED + MOCHIICHAO COMBINE ALL APPROVED (Mars)
- Animate: Mars approved options 1, 2, AND 3, with NO user takeover — use Google/GitHub sign-in, make an account if needed, reverse-engineer the rest. Browser task updated with that approval, including 7-day trial enrollment ($22.99/mo after, cancellation date to be reported).
- Mochiichao combine: Mars approved ALL of it ("get all of that done") — spec approval, dance clip, device prop sheet, device in final shot, background-life animation pass. Implementation subagent kicked off, in that order, canon rule intact.

## UPDATE 2026-10-31 15:43 CDT — DEMO-PASS POSE RECLASSIFIED: ARMS-UP / PRE-FLEX, NOT FLEX (Mars)
- Demo-pass pose (showcase/demo-pass-flex-level2-20261031/level-2-v2-colored.png, FlexOut lowers, upper -70/70, lower 150/-150): APPROVED as an ARMS-UP POSE, NOT as a flex. Mars 15:43 CDT: "good for our arms up pose, but it's not exactly a flex yet. That's really good though."
- USES FOR THIS POSE (Mars, 15:43 CDT): (1) a weird fighting stance with his arms up really high, OR (2) right before a flex — either one. (3) Reference for body movement / understanding how he moves his body. Good positioning for all of that.
- TRUE FLEX RULE, restated (Mars, 15:43 CDT): to make an actual true flex from this pose, roll the fists TOWARD HIS HEAD about 75 more degrees. True flex still 0/1 — earlier 75-degree-toward-head attempts detached at the wrist, so the seam fix (pose-space rotation + wrist cap) is still owed before a true flex ships.
- This pose is therefore renamed in intent: arms-up reference pose, not flex. Do NOT call this image a flex in future lists.

## UPDATE 2026-10-31 15:44 CDT — EFFECTS DESIGN UPGRADE (Mars, standing criticism)
- Mars: effects design was lacking, sent back / needs upgrading multiple times. Fix: pull 10+ more industry-standard VFX things (VFX, not SFX) + designing effects + existing lighting, so effects look REAL, affect the world, create lighting, and bring something to the atmosphere — NOT flat coloured pieces of lines and circles.
- Work kicked off: effects-design-v2 subagent, 12 target systems (volumetric god rays, bloom/spill, atmospheric scattering, particles, impact shockwave+flash, fire/energy aura, water/reflection, smoke/steam, motion blur, DOF/lens, electricity, effect shadows), each with Blender/compositor node setup + world/atmosphere effect + shot-spec fields -> EFFECTS-DESIGN-V2-20261031.md, plus one viewed proof (production if Blender, else labelled DRAFT).
- Toon Boom account mismatch resolved: Mars previously authorized ANY account, so browser task answered to proceed with the saved filled account marquiswhitacre@gmail.com, not wait for fmmg.mars@gmail.com, trial only, no purchase.

## UPDATE 2026-10-31 15:45 CDT — GET EVERYTHING TO 100% + SHOW AS DONE (Mars, standing)
- Mars: get ALL of the owed list done and wired up 100%, then find anything else industry-standard that can add to the stack and wire it up 100% too.
- SHOW-AS-DONE RULE (Mars, 15:45 CDT, standing): show anything that needs to be shown, show ALL of it that can be shown visually or audio-wise, show it AS IT GETS DONE — not batched at the end. Visuals attached in chat, audio as LINKS (never audio in chat).
- Work kicked off: 100%-drive coordinator (exposure sheets, layouts, clean-up batch, clips, effects v2 coordination, shot specs 30/30, Blender render, delivery spec, flex/fist/opposition, JoJo demos, free stack, comparison tests, repo push, proof shot, plus additional industry standards beyond the 6 groups already pulled).

## UPDATE 2026-10-31 15:48-15:52 CDT — CORRECTIONS + APPROVALS (Mars, all logged)
- DUAL-LIGHT CORRECTION (Mars, 15:48 CDT, reply to dual-light demo): cyan backlight god rays are for when he has CYAN RIM lighting combined with the GOLD LUT/overlay. Gold rim lighting ALONE gets NO cyan backlighting. Dual-light demo is still good, really good, but it is that combined case only. God rays/lighting still need more industry-standard upgrades to be even more realistic — in the effects-v2 work.
- JOJO COLOUR SHIFT DEMO APPROVED (Mars, 15:49 CDT): "I approve on these, these are all really good" — JoJo demo sheet approved, all palettes on it as shown.
- COMBINED APPROVED + RENAMED (Mars, 15:49-15:50 CDT): combined golden-hour + JOJO-TENSION approved, really good, name underneath does say JoJo tension. RENAMED: it is bright pink, NOT golden hour — call it BRIGHT PINK JOJO TENSION, or PINK HOUR JOJO TENSION, not golden hour. Old "golden-hour" name for that file is SUPERSEDED for this image.
- ARMS-UP POSE APPROVED (Mars, 15:50 CDT): approved, good pose, as arms-up. As a COMPLETE FLEX it is NOT done: roll his fists DOWN toward his head and shoulders about 75 more degrees, NOT outward away from his head. Outward roll was the wrong direction for flex. No new complete flex was shown yet — the image shown is the arms-up pose, not a complete flex. True flex still 0/1, seam fix still owed.
- PUNCH IMPACT APPROVED (Mars, 15:51 CDT): approved, really good, liked.
- ROOM SCALE 2.5x APPROVED (Mars, 15:51 CDT): approved.
- FREE-WAY-AROUND RULE (Mars, 15:51 CDT, standing, in AGENTS.md + SOUL.md + MEMORY.md): if GPU runs out, use Colab + every other free GPU source; if we run into ANY roadblock, find a FREE way around it or REVERSE-ENGINEER one and create our own way. NEVER just present a roadblock. GPU-first stays, Kaggle ~17 hrs remaining, Colab is next free route.
- COMPOSITOR FIX RULE (Mars, 15:51-15:52 CDT, standing): whatever the Kaggle limitation was, pull in and wire up whatever helps; if nothing free/open-source fixes it, reverse-engineer the paid top-level industry-standard method and get it solved 100%. Whatever gets the Blender composite wired up 100%, industry-standard way, do that. Fix subagent kicked off (Alpha Over background-mode diagnosis, local Blender 5.2.3 test, Kaggle/Colab fallback, viewed Cape Jones composite through Blender compositor itself, no PIL fallback claimed as success).
- WORKSTREAMS ALREADY RUNNING (Mars, 15:47 CDT): TV production stack 10 more standards, show/network templates for world interactions, improved dance scene, parts cut-out + labelling audit — all four kicked off, show-as-done as each lands.

## UPDATE 2026-10-31 15:53 CDT — DUAL-LIGHT RIM-MIX NUANCE (Mars)
- When cyan lights come from BEHIND him, there can ALSO be a mix at the front: gold rim lighting WITH cyan rim lighting AROUND the gold rim, layered. Need to SEE it in different ways, pull industry-standard dual-lighting methods, solve it, wire it up.
- Variants owed: (1) gold rim only, no cyan backlight; (2) cyan rim + gold LUT/overlay with cyan backlight god rays; (3) gold rim with cyan rim around it; (4) cyan rim with gold rim around it; (5) gold front key + cyan back god rays, rims mixed along silhouette. Subagent spawn for this failed once (database pool timeout) — retry pending, do NOT claim variants are built.

## UPDATE 2026-10-31 15:56 CDT — JOJO DEEP RESEARCH + PUSH LANDED 99.3%
- JoJo deep research kicked off (Mars, 15:56 CDT): deepen JoJo colour shift language/dialect, pull research already collected in Mochi repo first, then even more public research, wire anything that helps that universe language/dialect, 100% industry standard -> UNIVERSE-COLOR-LANGUAGE-V2-20261031.md + presentation sheets.
- PUSH LANDED (push worker, completed 15:49 CDT): PR #286 merge 5677d2fdd9d0f1b96bc85dafbb7909e37d96b3aa (278/279 at that time, apply_lighting_level2_v2.py newer locally), PR #287 follow-up merge 02694af9d149e57d619402c8ecf154ed2be87f13 (current main head). Verified on main: 292/294 = 99.3%. NOT 100%: STATUS-20261031-1428.md (local 34,814 vs main 24,733) and TRACKER-20261031.md (local 8,763 vs main 8,412) still owed — both kept growing while push ran, micro-push owed once appending stops. No local work deleted. PR bodies note LUT approval as 44/70 at push time (base 30/30, spectrum sheet 4 6/6, spectrum v2 sheet 1 8/8) — that is STALE vs Mars's later 70/70 approval in chat, do NOT quote 44/70 as current.

## UPDATE 2026-10-31 15:57 CDT — TOON BOOM ACCOUNT CREATION (Mars)
- If no login form / no saved account, CREATE an account: Gmail login or GitHub login if offered; if neither has an account, create one with the credential card Mars already gave. Browser task updated with that instruction, trial only, no purchase.

## UPDATE 2026-10-31 15:59 CDT — VISEMES V1 REJECTED AS HAND-TOOLED (Mars)
- Visemes v1 (pack4): Mars says too hand-tooled, good start, NOT good enough to approve. Need a better industry-standard method for Cape Jones.
- O/OO/W FIX (Mars): circular mouths (woo, ooh) — previous mouth must be MORE covered with skin colour first, mouth line AND cheek lines covered where new mouth sits, little mouth line covered, then new circular mouth drawn. V1 pasted over old lines; v2 masks first.
- GOODVILLE NOTE (Mars): the current hand-tooled way may go in his Goodville repo, but Cape Jones needs the better one. Goodville repo name NOT confirmed yet — do NOT push to a guessed repo; identify it first.
- Work kicked off: visemes v2 subagent, mask-first swap-library method (Toon Boom/Character Animator/OpenToonz mouth-chart standards), 14/14 rebuilt, OO/W before/after proof, no repo push in that task.

## UPDATE 2026-10-31 16:00 CDT — EYES RECLASSIFIED: V1 = COMEDIC, NORMAL = SUPERHERO (Mars)
- Eye strips v1 (pack4, proof-eyes-on-head): NOT accurate enough for normal eyes. RECLASSIFIED as COMEDIC RELIEF EYES — the ones with pupils, which he only sometimes has, for comedic effect only. Save as that set.
- NORMAL EYES (Mars): way more Batman-like / Teen Titans-like, superhero / comic-book / anime style — white angular eyes, normally NO pupils. Pull superhero eye methods (style only, not copied art) and build normal set v2.
- COWL EDGE FIX (Mars): little purple side edge goes a little too far out on the darker edge, on the Arm 1 edge. Fix: pull edge back on that side, make it a little DARKER on that little side of the rim, just right on the side where the darkness is.
- Work kicked off: normal superhero eyes v2 subagent (core expressions, white angular eyes, cowl edge corrected, proof on Head_Front).

## UPDATE 2026-10-31 16:01 CDT — CAPE STYLES V2 (Mars)
- Cape states v1 (4: draped, lying-flat, swinging, billowing): good start, NOT enough. Need a bunch of different cape styles, lot of movement, lot of forms/shapes, going all different ways/angles, like a real cape, real fabric aspect in 2D.
- Work kicked off: cape styles v2 subagent, 12+ forms (wind left/right, lifted, heavy hang, twisted, folded over shoulder, wrapped front, trailing run, flying spread, sitting pooled, etc.), cloth methods (Blender cloth, nCloth method, verlet/bone-chain secondary motion), cape as separate prop rig, folds follow gravity+wind, hem weight, no flat strips.

## UPDATE 2026-10-31 (JoJo V2 subagent) — UNIVERSE COLOR LANGUAGE V2
- V2 doc: UNIVERSE-COLOR-LANGUAGE-V2-20261031.md (new file, v1 untouched). Palettes 8 + base + opposition pair. Sheets 2/2 viewed, defects fixed.
- Mochi repo correction: JoJo material there is representation-canon.md (cool-first, show-first, never diagnosed in dialogue), NOT colour research. No Araki/palette doc found in Mochi repo (local clone verified; GitHub code search 0 items, incomplete_results=true).
- Approved: base, atmosphere, Bright Pink JoJo Tension image+name. Demo-only: tension, power, uncertainty, dream, dread, resolve, opposition — Mars approves each separately.

## UPDATE 2026-10-31 16:02 CDT — FOREARM/HEAD V1 APPROVED + PARTS CATALOGUE (Mars)
- Forearm + derived 3/4 head proof APPROVED as V1 so far, good start. V2 owed: pull/wire 10 more industry-standard things (foreshortening, 3/4 construction, anatomy, fist perspective, overlap, volume, rim/light, turnaround, pose substitution, QC), wire 100%, show V2. V2 subagent kicked off.
- Parts label sheet: good so far, but Mars needs ALL parts — every pack, every part, every name, every piece individually, not just sheets. Need sheets AND individual pieces. Catalogue subagent kicked off (HTML gallery, grouped by pack/body part, rejects separate DO NOT USE, exceptions PENDING, missing parts listed as missing).

## UPDATE 2026-10-31 16:03 CDT — CAPE V1 USE CASE CLARIFIED (Mars)
- Cape states v1 (draped, lying-flat, swinging, billowing): NOT fully rejected. Good for NOT moving too much / very light movement / standing still. That is their use case. V2 (12+ styles, fabric, wind, dynamic angles) is for real movement, not a replacement for the standing-still set.

## UPDATE 2026-10-31 16:06 CDT — MOCHIICHAO DEPTH SCOPE (Mars)
- Mochiichao universe gets that DEEP only in: (1) an episode/scene expressing how he plays it, (2) an episode where he's playing it, (3) shorts/scenes where they appear and dance around with him. Otherwise it stays as the handheld device / aspect / soul only.
- Full Mochiichao rigs, full FLAs, cut-out pieces for them: LATER, AFTER placeholder characters from other shows + all the pulls/wiring Mars ordered. Placeholder-first order confirmed. Pull/wire more industry-standard stuff for all of that, wired 100%.
- FILE VIEWABLE FIX (Mars, 16:06 CDT): dance GIF was not viewable on phone — converted to MP4 (phone-playable) + Muse file links for the combine build, expires 2026-11-02.

## UPDATE 2026-10-31 16:09-16:10 CDT — KNEE-FEET RULE + DANCE VIEWABLE (Mars)
- Improved dance: very, very good, really close, perfect apart from ONE issue. All dances look really good except toes pointing outward when knees go inward.
- KNEE-FEET RULE (Mars, standing, KNEE-FEET-RULE.md): knees and feet always pointing same direction; kneecaps inward -> toes inward; exception only if legs broken. Current dance reads as broken knees (baseball bat to knees) — defect, not style.
- Problem frames: improved dance contact sheet top row pose 2 (frame 15) and pose 4 (frame 42). Fix kicked off: research (knee tracking over second toe, tibial rotation, valgus), rebuild those frames + any other inward-knee frames in both dances, foot substitution/rotation, ankle intact, before/after proof.
- Improved dance made phone-viewable: GIF -> MP4 + Muse links, expires 2026-11-02.

## UPDATE 2026-10-31 16:12 CDT — DEVICE PROP UPGRADE V2 (Mars)
- Device prop v1: needs REALLY HEAVY upgrade, pull industry-standard prop stuff, AND way too big. Scale down to hand-fit device — "times 50, maybe" read as about 50% / half current size, hand-fit, to be confirmed visually (literal 1/50 would be invisible, so hand-fit version is built for approval, not a microscopic device).
- Work kicked off: device prop v2 subagent (prop sheet standards, ergonomics, GBA/Tamagotchi dimensions as method, scale reference with hand, separate prop rig, true two-hand grip, v1 defects not repeated).

## UPDATE 2026-10-31 16:14 CDT — JOJO DIALECT V3 CORRECTION (Mars)
- JoJo dialect/language does NOT just alter lighting. It BREAKS canon, it is NON-CANON: world colors change AND character colors change.
- Mars correction: he cannot look like he stayed base same color with just an overlay on top. His colors must ALSO alter, with JoJo color theory (research creators' method).
- V2 was PIL gain overlay, base hues preserved — WRONG for Dialect 2, reference only. V3 kicked off: true palette replacement tables (character part-by-part + world), side-by-side base vs shifted sheets, another application so far, still to be perfected, not claimed perfect.

## UPDATE 2026-10-31 16:15 CDT — FULL FINAL FLEX SPEC (Mars)
- 30° pose-space flex: definitely more of a flex, good, 75% done to a flex scene. NOT final.
- Full final flex = fists L -75° / R +75° (+45° beyond current), forearms tightened/rolled L -15° more / R +15° more, PLUS knees bent a little + head/torso/pelvis/thighs dipped to complete the pose.
- Full final flex build kicked off, new dated file, before/after proof, viewed before showing.

## UPDATE 2026-10-31 16:21-16:25 CDT — ARMS-UP APPROVED + LEVEL-3 THRESHOLD + CHAT-VIEWABLE RULE (Mars)
- ARMS-UP APPROVED (Mars, 16:21 CDT): dual-light base arms-up pose is a good base starting point. Approved as arms-up / pre-flex only, NOT a flex.
- LEVEL-3 THRESHOLD RULE (Mars, 16:21 CDT, standing): when mixing reaches V4 level, it starts to get to LEVEL 3. V4/V5 mix is good, but still kind of looking LEVEL 2 — upgrade it so it IS level 3. L3 requires: upgraded god rays (bright, not v1 dark bands), light bleed / light-effect bleed, light affecting shadows on him, more effects + more lighting effects, all wired 100%. A mix that only looks L2 is NOT L3, even if it uses V4 rim order.
- GOD-RAY UPGRADE (Mars, 16:21 CDT): god rays are at a really low level right now, need to be up and improved a bunch, pull 10 industry-standard things, wired 100%. Repeated 16:21:39 CDT: pull 10 things that upgrade god rays, wire 100%.
- CHAT-VIEWABLE RULE (Mars, 16:25 CDT, standing, do not make him repeat it): STOP sending file types that cannot be previewed in chat. Put those files in the repo, then send in chat ONLY the ones that can be viewed here. Non-viewable types (blend, json, md, html, scripts, docs, folders) go to the repo / workspace path in plain text, NEVER as a chat file link. Chat shows: viewable images (PNG/JPG via phone-openable links) and audio as links only.
- FOREARM/FIST CRITICISM (Mars, 16:25 CDT): everything else in forearm-head34 v2 is good and APPROVED on that, EXCEPT the last fist — the Arm2 different-angle fist is UPSIDE DOWN, not a good fist, other two fists were right. Arm1 is done a bit better, Arm2 is done really bad, not clean. Fix: find Mars's better fist in the repo if it exists (he may have a front-facing fist image from an animated thing / saturation reference), otherwise generate a proper front-facing fist to put over that. Pull industry-standard fist construction, wired 100%, get it solved.

## UPDATE 2026-10-31 16:27 CDT — EYES DARK SIDE FLIP (Mars, repeated)
- V2 darkened the WRONG end segment. Mars specified Arm1 side; v2 put dark on Arm2 side. FIX: flip it — dark on Arm1 side, normal color on the side v2 made dark. V2 dark-side claim is NOT approved.
- Eyes v3 kicked off: flipped dark end + pull Batman / Teen Titans eye packs (repo first, then public transparent-background packs) as TRANSFORM-ONLY reference, adapted to his head/cowl/palette, never shipped as-is.
- Eyes are really close but look hand-tooled — v3 must not read hand-tooled.

## UPDATE 2026-10-31 16:29 CDT — CHAT-VIEWABLE = EMBEDDED IMAGES ONLY + LIGHT-WRAP UPGRADE (Mars)
- CHAT-VIEWABLE RULE CORRECTED: remote-storage http links are DOWNLOAD links, not viewable links. In chat, send visuals as EMBEDDED image attachments that show right in the chat, not as file links and not as download links. Non-viewable files go in the repo, mentioned in plain text only, never as chat file links.
- BLENDER COMPOSITE V2 (Mars): good, upgrade even more, more industry-standard stuff. Light must NOT just upgrade behind him — it must look like it is coming AROUND him in a realistic way. Light-wrap upgrade kicked off (wrap falloff, spill/bounce, volumetric wrap, realistic falloff, apose + arms-up base).

## UPDATE 2026-10-31 16:27 CDT — NORMAL EYES V3, DARK END FLIPPED (Mars, repeated 16:27:31)
- CORRECTION: v2 dark segment was on the WRONG end (image-RIGHT x385-426). V3 flips it:
  dark segment image-LEFT x41-79 (52,22,66), normal purple on image-RIGHT. Dark = Arm1 side
  as Mars sees it in the proof. V2 dark side NOT approved; v2 mapping claim superseded.
- V3: 5 normal expressions, white angular NO pupils, floating brow bars removed, brow in lid slant.
  Proof on Head_Front + before/after v2 vs v3 viewed. V3 NOT approved — Mars approves.
- Eye packs: no verified Teen Titans eye-pack file in Mars's repos (that repo is Rig UNKNOWN,
  parts not listed — next pull, not a source used); public Batman mask PNGs are fan clipart,
  transform-only reference, NOT a clean open-licensed eye-only pack — no such pack claimed.
- Comedic v1 strips have no band end segment, so no flip applies to those files; flipped band
  composite for comedic eyes is still owed 0/1.

## UPDATE 2026-10-31 16:30 CDT — REALISM = LIGHTING/EFFECTS/GOD RAYS, NOT BACKGROUND (Mars)
- Correction: "more realistic" means lighting + effects + god rays look more realistic, NOT the background itself. Background painting stays as-is; light/effects/rays get realistic (industry-standard methods wired for light, not background repaint).
- Correction sent to god-ray L3 and light-wrap workstreams.

## UPDATE 2026-10-31 16:30 CDT — RE-SENDS WERE NOT IMPROVEMENTS + CACHE RULE RE-CONFIRMED (Mars)
- The images re-sent in the 16:29 chat message were the SAME existing files (V1-V5, composite, forearm, eyes) re-sent for viewability, NOT improved versions. Mars correctly spotted they look the same — they ARE the same.
- Improved versions (god-ray L3, light-wrap v2, fist v3, eyes v3, JoJo v3, flex final, prop v2, knee-feet fix) are still running and have NOT been shown yet. Do NOT present a re-send as an improvement.
- IMAGE-CACHE RULE re-confirmed: every improved version gets a NEW dated/versioned filename, never the same filename as a version Mars has seen, or the client shows the cached old image.

## UPDATE 2026-10-31 16:31 CDT — ARM2 ALIGNMENT (Mars)
- Forearm V2 Arm2 back: NOT correct, NOT lined up correctly. Mars cannot explain it in words — diagnosis must come from industry-standard measurement, not from Mars explaining.
- Arm2 alignment diagnosis + pipeline QC fix kicked off: measure wrist/elbow/fist/cuff centres + axes vs Arm1 + v7c geometry, name misalignment in numbers, rebuild correctly aligned Arm2 with new filename, wire alignment QC script into pipeline 100%.

## UPDATE 2026-10-31 16:35 CDT — JOJO CREATOR-FEEL RULE (Mars)
- V3 first non-canon color change: good first one. Blue helm / different colorway is exactly the type of non-canon shift.
- Cape rule REVISED (supersedes v3 dark-tint proposal): cape would probably change from black to a DIFFERENT COLOR also, not stay black, not just dark tint.
- Suit rule: might stay white, or might change to a different color sometimes — both valid per beat.
- Creator rule: JoJo creators do palette shifts based on how they feel / what would look cool — cool-first creative choice per beat, recorded in shot spec, not a rigid formula.
- Variation sheet kicked off: blue helm example, cape full color, suit white vs suit changed.
- SYNFIG RED CIRCLE EXPLAINED: Synfig test was a tool tween test only (red circle left->right, 24 frames) to prove Synfig can move/render — NOT a Cape Jones story element. Next Synfig test must use Cape Jones pieces, not a circle, so test outputs are not mistaken for character work.

## UPDATE 2026-10-31 16:35 CDT — JOJO DREAM VARIATION (subagent task)
- DREAM variation built: helm turquoise, cape FULL magenta-pink (255,60,180) in both shifts, suit white in A / gold in B. Base panel for comparison.
- Addendum filed (new file, v3 doc untouched): cape = full colour change (supersedes v3 dark-tint proposal), suit = stay white OR change, choice = creator-feel / what looks cool per beat, recorded in shot spec.
- Mars approval 0/1, pick A vs B pending.

## UPDATE 2026-10-31 16:39-16:42 CDT — JOJO APPROVALS + FLEX + FIST CORRECTIONS (Mars)
- JOJO V3 APPROVED: tension, hot pink, pink violet, world differences, ALL v3 palettes/sheets — "that's exactly how we should do it, that's just how Jojo does it, take it even further, those all look really cool." Keep building on language/dialects as the show builds and as the language is used.
- JOJO LANGUAGE RULE (Mars 16:39): a JoJo shift is its OWN language/dialect, separate from lighting language — but it CAN go hand-in-hand with lighting segments and CAN mix with lighting + effects (color bleed, rim lights, god rays). When it mixes, it turns all of it UP and mixes crazy — a different mix, not just a shift or just lighting alone. Record mix vs shift-alone in the shot spec.
- FLEX VERDICT (16:40): full-final-flex is REALLY GOOD / REALLY CLOSE, but NOT the true final flex as-is. Keep it as OVER-EXAGGERATED flex frame (when he over-flexes, it goes this far). TRUE final flex = a little more relaxed in the arms + cleaned up around wrists. Changes: biceps angle up toward head ~15 deg more; wrists clenched up at forearm connection; forearm-wrist angle opened ~5 deg (more space); wrist cleanup on BOTH versions. Refinement running.
- FIST CORRECTION (16:41, authoritative): v3 "front-facing" fist is actually UPWARD-facing / PALM-facing — a front-facing fist shows KNUCKLES to the front, no palm. Save v3 as palm-facing fist, NOT a punching fist. V4 running: generate an actual front-facing punching fist, knuckles at top facing viewer, no palm visible.
- CRITIQUE-LEARNING RULE (16:40): learn from every critique, research why in anatomy/animation + industry standards as we go, log it all in the repo so Mars does not have to repeat himself. Critique-learning log + gap audit running.
- FACEBOOK SEND (16:36): Mars asked for JoJo v3 sheets sent individually on Facebook. BLOCKER, plain: Facebook post tool is TEXT ONLY (no image attach), and Messenger is NOT connected (check returned not connected). Cannot send images as Facebook posts via connector as-is. Needs Mars's choice: connect Messenger, or browser post to his profile with an audience he picks — do NOT post publicly without him picking that. Asked, not sent, not claimed sent.
- WIRE-UP 100% (16:36, 16:40, 16:42): all of it + any other industry-standard things missing, wired into repo + pipeline and landed 100%. Gap audit running; repo-push workstream already running.

## CORRECTION 2026-10-31 16:46 CDT — "CLENT UP" = CLEANED UP, NOT CLENCHED (Mars)
- Flex wrist instruction corrected: clean up around the wrists where they connect to the forearm (clean seams/join), NOT roll fists more, NOT clench wrists more. Speech-to-text misheard "cleaned up" as "clenched up".
- Correction sent to the flex refinement workstream; other flex numbers unchanged (biceps +15 toward head, forearm-wrist angle +5 open, true final flex more relaxed than over-exaggerated frame).

## UPDATE 2026-10-31 16:47 CDT — EYES V4: USE REAL BATMAN-SHAPE EYES (Mars)
- V3 dark side CONFIRMED correct (Arm1 side, image-left in proof) — do NOT flip back.
- V3 eye SHAPE still rejected: still hand-tooled. Mars: nothing wrong with taking small pieces from another character; Batman's eyes are universal to any hero with all-white eyes.
- V4 running: pull animated Batman eye pack; search Teen Titans pack first (Batman + any Teen Titans characters with Batman-shaped eyes); search other public open-source superhero/comic-book resources; Space Ghost counts (Batman without the ears). Eye shapes only, fitted to his head openings + purple cowl, dark end Arm1 side, no Batman ears/mask/logo/character shipped.

## UPDATE 2026-10-31 16:48-16:49 CDT — HAND-TOOLED EYES = FALLBACK DRAFT ONLY (Mars)
- V3 eyes: good for a start, NOT fully approved. Save as FALLBACK / DRAFT / PLACEHOLDER / REFERENCE eyes only in repo, never as approved normal eyes.
- V4 rule, explicit: NO rebuilt vector polygons, NO hand-tooled eyes. V4 = pulled Batman-style / comic-book superhero eye shapes only (animated Batman pack, Teen Titans, Space Ghost, public open-source superhero resources), fitted to his head, dark end Arm1 side.
- If no real pulled shape is found, report that plainly — do NOT substitute another hand-tooled set as v4.

## CORRECTION 2026-10-31 16:50-16:51 CDT — EYES: NO HAND-TOOLING AT ALL + NO EXTRA OUTLINE (Mars)
- Black outline critique: hand-tooled eyes have an unnecessary black outline — sat on his face it looks like an extra mask on top of his mask. V4: NO extra black outline around eyes; pulled shape sits IN his own mask openings, his cowl is the mask.
- "Less hand-tooled" is NOT what Mars said and is not acceptable phrasing. Rule: NOT hand-tooled AT ALL. Only handle things where necessary (fit to head openings, cowl color, dark end Arm1 side). If a step would require hand-drawing a shape, report it blocked instead of hand-tooling around it.
- V3 = fallback/draft/reference only, NOT approved, and the pulled v4 eyes are what will actually be used.

## CORRECTION 2026-10-31 16:58 CDT — KNEE-FEET RULE IS BIDIRECTIONAL (Mars)
- Previous knee-feet fix over-applied FootIn (frames 15-55 block) and broke top-row third contact-sheet frame: knees OUTWARD there, but feet were flipped INWARD. Wrong.
- Standing rule, both directions: knees OUTWARD → feet OUTWARD; knees INWARD → feet INWARD. Per-frame decision from knee direction, never a block range.
- Correction running: re-audit all keyframes/frames, fix third top frame + any other outward-knee frames flipped wrong, keep correct inward fixes, anatomy study into KNEE-FEET-RULE.md, new dated rebuild.
- Otherwise the fix is all good (Mars).

## UPDATE 2026-10-31 17:01 CDT — WRAP V3: INTERNAL LIGHT + BACKGROUND UPGRADE (Mars)
- Wrap v2 verdict: getting pretty good, looks like real superpower effects.
- V3 direction (explicit new request, supersedes 16:30 background-stays rule for v3 only): upgrade the BACKGROUND itself + upgrade how light affects HIM.
- Light must affect color ON him and put shadows on him around his outlines, not just a color band around him.
- Inner outlines OF HIM (not lighting outlines): pec shadows, clothing folds/creases — light must hit those realistically (lit side brighter, shadow side darker, direction-consistent).
- Pull open-source relighting/interior-shading methods to reach that level; upgrade other things around this too.
- V3 workstream running.

## RIM LAYERING RULE 2026-10-31 17:02 CDT (Mars, standing)
- Hard rim line outline (v1 3px style) is KEPT, not eliminated by the soft rim.
- Soft rim is really good, kept too. Differentiation hard vs soft must stay visible.
- Full stack, bottom to top: HARD rim halo, then SOFT halo, then SOFT rim on top. Rim-light halo layering.
- Variants: full stack together; soft rim WITHOUT hard rim sometimes; hard rim alone as control.
- Added to wrap v3 workstream.

## APPROVAL + NEW VERSION 2026-10-31 17:02 CDT — TRUE FINAL FLEX PERFECT (Mars)
- TRUE FINAL FLEX relaxed-cleaned: PERFECT, approved as the true final flex. Do NOT change that file.
- OVER-EXAGGERATED FLEX new version running: deeper squat, legs bent deeper, exaggerated a little more than normal flex. Feet planted, knee-feet same direction, wrist cleanup kept, fists toward head.
- Save both as really good: true final (perfect/approved) + exaggerated deeper-squat version (new file, approval 0/1 until Mars sees it).

## UPDATE 2026-10-31 17:04 CDT — WRIST GOOD ENOUGH + JOINT CLEANUP FOR LATER (Mars)
- True final wrist crops: still really good, honestly good enough. Minor extra clean at wrist-meets-fist only if it helps, never breaking the perfect pose.
- Elbow/knee round joints: FINE for now, do NOT remove now. They help understand the rig.
- LATER GOAL (logged, not done now): make him look LESS LIKE AN ACTION FIGURE by cleaning up those round joints later.
- Tooling job running: pull + wire up joint-cleanup methods/tools NOW, tested on copies, targeted at elbow/knee/wrist, ready to use when Mars says go — so cleanup is easy later, not a new research job then.

## CORRECTION 2026-10-31 17:05 CDT — SOFT RIM = SOFT HALO, SAME THING (Mars)
- Mars was using "soft rim" and "soft halo" interchangeably — he thought they were the SAME, not two layers.
- ORIGINAL intent (corrected): hard rim + ONE soft layer (soft rim = soft halo), together, or soft alone sometimes, or hard alone as control. NOT a three-layer stack by default.
- EXPERIMENTAL VARIANT ONLY: show what soft rim on top of soft halo looks like as two separate layers; Mars will then say if he wants that or not. It is a test, not what he originally meant.
- Logged here + sent to wrap v3 workstream to correct the stack doc.

## CORRECTION + RULE 2026-10-31 17:05 CDT — DO NOT LIE ABOUT "GENERATED" (Mars)
- Fist v4 verdict: NOT good.
- Plain ownership: v4 was PIL vector shapes drawn by code — that IS hand-tooled in effect, NOT a generated/pulled fist image. Calling it "generated" was wrong. Never claim generated when a piece is vector-drawn; call it exactly what it is.
- Fist v5 reference (Mars's own example): SmackDown fist, 2001-2005 era (SmackDown vs Raw era), saturation taken DOWN to near white to match his white glove. Fist shape only, no WWE logo/character/branding shipped.
- V5 workstream running.

## UPDATE 2026-10-31 17:11 CDT — L3 AWESOME + LEVEL 4/5 RULE + GOLD-TO-RED SHIFT (Mars)
- L3 proof verdict: AWESOME. Keep improving, keep pulling industry-standard stuff into lighting/effects pipeline, keep logging upgrades.
- LEVEL RULE (standing): three levels exist; anything created ABOVE third level = LEVEL 4; above that = LEVEL 5; levels keep going up as pipeline upgrades, never capped at L3.
- GOLD-TO-RED SHIFT (noticed, NOT a complaint — looks great/beautiful/amazing): after Blender comp, gold rim reads as RED, not gold. Pay attention to that shift, measure + log cause, build gold-preserved variant for comparison, do NOT destroy the beautiful version.
- L4/L5 + gold-shift workstream running.

## MAPPING 2026-10-31 17:12 CDT — LEVELS vs V5 BEFORE/AFTER (Mars)
- L1 / L2 lighting+overlays may still LOOK like V5 BEFORE (the L2-looking before image).
- L3 and beyond L3 looks like V5 AFTER.
- L4 will be BEYOND that (beyond the V5 after).
- Use before/after pair as visual anchor: L1/L2 = before look, L3 = after look, L4 = beyond after.

## PRESET PACKS + LEVELS + COLOR-SHIFT STUDY 2026-10-31 17:12-17:15 CDT (Mars, standing)
- MAPPING CONFIRMED: L1/L2 lighting+overlays may look like V5 BEFORE (L2-looking); L3 and beyond looks like V5 AFTER; L4 will be beyond that.
- PRESET PACKS (separate axis from levels, levels still stand):
  * LIGHTING PACK VERSION 5 = V4/V5 BEFORE stack (pre-L3, L2-looking stack) as a saved lighting style/preset.
  * LIGHTING PACK VERSION 6 = V4/V5 AFTER stack (L3 stack) as a saved lighting style/preset.
  * Naming EXACTLY "lighting pack version five/six" — NOT "lighting pack level five/six".
  * Mars calls: "go to level 0/1/2/3 in the lighting" = levels axis; "pull up lighting pack version five/six" = preset axis, to set that preset onto a scene.
- COLOR-SHIFT STUDY (standing): study + log WHY layering/Blender comp changed gold to red, so we understand how overlays/environments affect color. NEVER call a color the wrong color after overlay/change: record input color + on-screen color + mix cause (e.g. used yellow/gold, on screen looks red/green because of how the mix affects this room/environment). Shot specs must carry all three when they differ.

## CORRECTIONS 2026-10-31 17:28-17:30 CDT (Mars)
- HIP LOWER (both exaggerated flexes, both sides): hip joints up too high on pelvis; lower them a little, slightly, with the pelvis when crouching, tilted lower like bending on the knee, still attached to pelvis, knees and feet EXACTLY where they are (planted, y1299). Anatomy research owed with the fix. True final flex PERFECT file untouched. Both versions already very close to perfect; hip-lower should make them perfect. Approval 0/1 each.
- FIST V5 ORIENTATION: seated v5 (180-degree rotated, knuckles at bottom) is UPSIDE DOWN for a forward punch — SAVE that orientation as UPPERCUT fists, FLIP the fist now (original knuckles-top orientation) for the forward punch. Forward-punch approval 0/1.
- EYES V4 IN-MASK: APPROVED — proof eyes in own mask on Head_Front is PERFECT (Robin eyes, as fitted in his own mask openings). Strip reshape (before/after V3-V4) is CLOSE/COOL/STRAIGHT but reads a little like Ninja Turtles — NOT the perfect version, do not present strips as the approved face. Approved = in-mask fit only.

## FACETOP + GENERIC EYES 2026-10-31 17:31-17:32 CDT (Mars)
- FACETOP EARS-OFF: NO as a face top. That mask is 3D Batman, NOT 2D animated Batman. Purple recolored version not good enough, not enough like animated Batman, and behind the head it crops out weird. KEEP the image ONLY as a parody prop / joke gag (Halloween gag, put over his face as if wearing a Batman costume, parody joke). Rounded ANIMATED cowl top still owed 0/1.
- GENERIC SUPERHERO EYES RULE: confirmed — generic superhero eyes, almost any superhero with eyes like that would fit; Robin fitted perfectly. Approved = Robin eyes in own mask (1/1).

## SHOW-REPO ANIMATION AUDIT 2026-10-31 17:34 CDT (Mars, running)
- Get Teen Titans rigs/motions/animations over: comic-book anime superhero like, helps build our universe. Don't need their characters; pieces may be placeholders for now; main goal: animate, get rigs moving, learn what we can do with characters in our show.
- Same audit for ALL show repos: do they actually have saved animation files, or build animations by dragging pieces with no saved file? Gumball, Teen Titans, ETC, all of them. 100%.

## AFTERGLOW EFFECT 2026-10-31 17:36 CDT (Mars)
- Loose light-shadow floating away from outline in wrap v3 fighting = SOFT RIM layer (cyan, dilate 6, blur 5, 0.60), NOT hard rim. Soft rim = soft halo, one layer.
- NEW USE: motion AFTERGLOW, not a still thing. Glow trails behind him as he moves (glow-stick-in-dark), fades; standing still = no afterglow visible. Animated test running, approval 0/1.

## SOFT RIM = LIGHT TRAIL, NOT STATIC 2026-10-31 17:38 CDT (Mars, standing)
- Soft rim must move when he moves, like a light trail. Static soft rim looks ugly, makes him look like he is not standing on the ground — like a shadow in the wrong place if just sat there static. Afterglow rule: trail in motion only, fade at rest, never a static glow.
- WRAP V4 running: pull industry-standard normal/depth + Cycles volumetric + dust tools, wire 100%, eliminate all v3 honest limits (true normal relight, full-height render, Cycles shafts, side-weighted wrap, true dust motes, rim-only proof).

## EFFECTS SUNBEAM PRESET 2026-10-31 17:47 CDT (Mars)
- Effects v2 proof: REALLY GOOD light, REALLY GOOD sunbeams. Arms-up reads like two double yellow spirit bombs (energy orbs at raised fists) — goes hard.
- SAVE v2 stack as a versioned preset (Effects Sunbeam Preset v1, preset system alongside Lighting Pack v5/v6) so it can always be gotten back to, then UPGRADE it with additional industry-standard methods wired 100% (orb snap to fists, denoise, shaft masking, etc.). Approval 0/1 for upgraded version.

## APPROVAL 2026-10-31 17:48 CDT (Mars)
- Fist v5 FLIPPED forward-punch set: APPROVED 1/1 — good enough right now, good for a straightforward punch, better. Uppercut set saved separately, not the approved forward punch. Full punch pose integration still 0/1.

## APPROVALS 2026-10-31 17:48-17:49 CDT (Mars)
- Fist v5 flipped forward punch: APPROVED 1/1 (good enough right now, straightforward punch, better). Uppercut set separate.
- AFTERGLOW: APPROVED 1/1, really nice. Save as DEFAULT AFTERGLOW PRESET. Current glide version also saved as TELEPORTATION variant (idle+ moving read = teleportation). Add afterglow to RUNNING animation and to FLYING — that is his base afterglow color; different powers/variations built off it later. Running/flying applications 0/1 each.

## APPROVALS 2026-10-31 17:50-17:51 CDT (Mars)
- KNEE-FEET CORRECTION: APPROVED 1/1, 100% PERFECT — corrected GIF, foot crops f028, before/after, contact sheet all perfect. Fixed. Only thing from here is go up and upgrade the whole pipeline.
- SPEC ARCHIVE RULE (standing): save ALL specs + information of everything done to the repo so it can always be revisited or recreated. Keep pulling/working, get still-owed 100% done, pull new industry standards and wire 100% to help anything built so far.

## ARM FRONT SNAP RULE 2026-10-31 17:58 CDT (Mars, standing)
- When arms cross the torso/chest threshold (ribs/pecs start), forearms+fists must SNAP to the layer ABOVE, momentarily, so they are NOT eaten by torso/pecs. Arms out to side = no snap; arms in front = snap to front. More realistic in those moments.
- Research anatomy/animation layering (back vs front vs above layer, momentary snap) + industry-standard methods wired 100% + rule doc in repo. Snapped dance version running, approval 0/1.

## APPROVALS + SEQUENCE 2026-10-31 17:59-18:01 CDT (Mars)
- HIP-LOWER: APPROVED 1/1 both — over-exaggerated hip-lower + deep-squat hip-lower, all of those. Could be a little better, but counted as perfect for right now, go ahead with that.
- FLEX SEQUENCE: over-exaggerated flex + deep squat are TWO SEPARATE frames/poses: frame 1 = over-exaggerated flex, frame 2 = over-exaggerated flex + deep squat.
- RE-PRESENTATION RULE: anything that is Mars's pick or needs Mars approval must be SHOWN AGAIN in chat (embedded) — Mars does not know where they are otherwise. All picks + approvals get re-shown in the approval pack.
- ANIMATE: restart the Animate sign-in step (previous browser task errored, no enrollment).

## VERDICTS 2026-10-31 18:03 CDT (Mars)
- Gold-preserved V5: GOOD, really good, accepted — still pinkish/still red, that is FINE, looks good/cool. Same for gold-preserved V4 above it. God-ray v2 / L3 V4 look good.
- L4 candidate: CRAZY, wild, a DIFFERENT level — reads as L4, approved as an L4 level.
- NAMING RULE: name ALL presets/levels clearly with visual differences explained, because some levels cannot be told apart otherwise.
- L5 SHOT OWED: build first L5 shot and show it.

## JOJO/STAND/GINYU POSES 2026-10-31 18:04 CDT (Mars, running)
- Study JoJo poses + Stand poses + Stand-user poses; Cape Jones does JoJo pose stuff sometimes.
- Ginyu Force type poses: funny, almost comedic, pose/dance stuff, different gags.
- Wire as universe language dialects/gags, industry-standard methods, 100%, show poses.

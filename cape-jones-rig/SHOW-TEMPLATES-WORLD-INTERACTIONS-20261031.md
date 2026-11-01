# Show / Network Templates — World Interactions for Cape Jones
Date: 2026-10-31. Status: TEMPLATE / PLACEHOLDER ONLY — none of these is a final Cape Jones scene.

## Rules this pack follows (Mars, 2026-10-31)
- Barred ONLY: (1) exact character likeness shipped as-is, (2) using their character literally, (3) character name, (4) dialogue literally from their script, (5) brand image / logo.
- Character images are TRANSFORM-ONLY production reference (parody or wholly different character before release, never ship-as-is). This pack uses NO character art at all — only interaction patterns, staging, timing, prop use, and background interaction.
- Cape Jones canon stays his own. These are interaction templates to be reskinned to him, not donor scenes copied over.
- Sources are cited by FILE IDENTIFIER only (repo + release + filename), not by character. Where the audit's network label is only a repo name, this pack says so — it is not a verified broadcast claim.
- Standing Cape Jones rules carried in: room scale locked 2.5x (950px, chair back at waist), seated scale = standing − 0.2 → 2.3x (approximate, verify visually); labels are debug only, never in finals; base art never recoloured (light/shadow/bleed on separate layers); rim follows key/LUT hue ±20°, dual-light only when both sources are named in the shot spec; version-lock (new dated files, never overwrite a version Mars has seen).

## Sources used
- `SHOW-REPO-DEEP-AUDIT-20261031.md` (41 rows, content-verified rig/dance 3/41, extractable rig files 4/41, verified dance 1/41).
- `WIRED-PULLS-20261031.md` (6 wired systems: multi-view part-swap puppet + pose-library sheet; build vs reference layers + variant-as-layer-set; turnaround-page rig + chin + mouth pair; prop-rig separation + noodle deformer + baked-cache pipeline; shot-code filename pattern; frame-addressed pose-swap libraries).
- `MOCHIICHAO-COMBINE-20261031.md` (background-life 10 systems, dance spec ~107 BPM, handheld device gag).
- Cape Jones's own locked items: punch impact −110 across-up, arms-up reference pose (NOT a flex — true flex = roll fists toward head ~75° more, still 0/1), Level 2 v2 warm rim, LUTs 70/70, JOJO-ATMOSPHERE approved.

## Templates presented: 7/7 (task asked for 5+, delivered 7)
Presentation folder: `show-templates-world-interactions-20261031/`

| # | Template | Source (file identifier only) | Interaction | Timing | Cape Jones setting | Placeholder-only vs ready to apply |
|---|---|---|---|---|---|---|
| 01 | Dance groove: stride → groove → kick → split → twist | cape-jones/production/dance-choreo/dance-gumball-darwin-words-sc057-sc059.json (GB214 Sc057 + Sc059) | Dance / beat interaction | ~108f loop, 13–14f/beat @24fps, keys on twos, snaps on ones, holds 6/12/24 | Room rug / street sidewalk | READY as timing/staging template; final dance clip 0/1 still owed |
| 02 | Walk through a room and sit | ch_max.fla pose-library sheet (46f hold, guide layers) + room scale lock | Walk, plant, turn, sit | ~72f (walk 24f, plant+turn 12f, sit 12f, hold 24f) | Room, chair | READY as staging template; seated pose visual verification 0/1 still owed |
| 03 | Flip lights, watch TV, react | Cape Jones house activities + L0–L3 / LUT / rim system | Light-driven world interaction | ~55f + 24f idle loop, 6f light crossfade | Room (standing 2.5x / seated 2.3x) | READY as interaction + lighting template; final lights/TV shot 0/30 per-shot specs |
| 04 | Open door, enter/exit, handle prop | pds3hx.fla (6 pages, 430 comps) + Nick ZIP RIGS/ listing (prop rigs separate) | Prop handling, door | ~54f, 6f minimum hand-contact hold | Room door / street shop door | READY as prop-rig template; final door shot 0/1 still owed |
| 05 | Handheld device gag (always in pocket, no visible pockets) | MOCHIICHAO-COMBINE-20261031.md device design | Pocket gag, play loop | ~42f + 24f play loop, beep as metronome | Room (chair / rug) | READY as gag template; device prop sheet 0/1, device in final shot 0/1 still owed |
| 06 | React: expression swap (chin + mouth pair, eye library) | tv-gigaleak-fla-v1 assets (25f mouth library, 9/5-layer heads) + pds3hx.fla chin + mouth pair | Reaction / expression | Snap 2f, hold 12f, blink 2f+2f | Room / street (reacting to TV, door, device) | READY as swap template; final expression shots 0/30 per-shot specs |
| 07 | Street walk + background life | 2024_Nick_Gigaleak.zip listing (RIGS/ listed only) + combine background-life 10 systems + ch_ruby.fla night variant | World moves around him | 48f tiling loop, walkbob 2f+2f, door glow 24f loop | Street / forest atmosphere / room | READY as background-life template; background-life animation pass 0/1 still owed |

## Interactions covered (count)
- Movement interactions: 3 (dance, walk-and-sit, street walk)
- World/prop interactions: 3 (lights/TV, door/prop, handheld device)
- Reaction interactions: 1 (expression swap)
- Total interaction patterns presented: 7
- Body-part coverage: arms (both, incl. grip/fist swaps), legs (both, walk + split + kick), torso, head (chin/mouth/eyes/brows/lids as separate symbols), cape as separate prop rig in 5/7 templates.
- Props covered as separate rigs: chair, door + handle, TV / switch / remote, handheld device, background door/glow/grass/path.

## What is placeholder-only (NOT final, NOT claimed as a scene)
- Every template sheet above: staging, timing, and parts lists only. No final Cape Jones scene, clip, or shot has been built from them in this task.
- All donor material: systems/timing/structure only. No donor character, scene, art, dialogue, or logo is reproduced or reskinned here — reskinning a donor character into a Cape Jones scene is a later, separately-viewed build step.
- Nick Maya rigs, Disney FLA (`ww226_26s_016_final.fla`, filename only), and nick.7z contents: listed only / unknown — no values, timing, or art claimed from them.

## What is ready to apply right now
- Templates 01–07 as staging/timing/parts checklists for the next build step (dance clip, seated pose, lights/TV shot, door shot, device shot, expression shots, background-life pass).
- The pose-library sheet method (Template 02) and the swap-library method (Template 06) plug directly into pack4 (visemes 14/14, eye strips 8/8, cape states 4/4 — approval of those sets still owed, 0/5).
- The shot-code naming pattern (`show_scene_shot_final`, never overwrite a shown version) applies to every file the next build step produces.

## Still owed (after this pack)
1. Final dance clip from Template 01 (+ combine spec): 0/1
2. Seated pose visual verification (2.3x): 0/1
3. Device prop sheet drawing: 0/1; device in a final shot: 0/1
4. Background-life animation pass (Template 07): 0/1
5. Per-shot specs filled: 0/30; per-shot god-ray placement: 0/30
6. True flex (fists toward head ~75° more, pose-space + wrist cap): 0/1; fist-angle variant for extended Arm 2: 0/1
7. Disney FLA data parse (`ww226_26s_016_final.fla`): 0/1, if Mars wants it
8. nick.7z listing (needs a 7z tool + full download): 0/1, unknown contents
9. Mars approval of this template pack itself: 0/1
10. Any template turned into a final scene: 0/7 — that is the next build step, not this pack

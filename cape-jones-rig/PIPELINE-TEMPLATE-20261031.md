# Pipeline template — Cape Jones shot pipeline (wired 2026-10-31)

Public industry-standard stage order (story → boards → animatic → layout → keys →
breakdowns/in-betweens → clean-up → colour → compositing → audio mix → final output),
mapped to the tools actually wired for Cape Jones. Template status: wired as a template
10/10 stages = 100%. Shots run end-to-end through all 10 stages: 0/30 — that is a
separate pass, not claimed here. Gate order for shows is unchanged: Cape Jones alone
first, then other shows, then more characters.

| Stage | Tool (wired) | File / output | Gate — do not pass without it |
|---|---|---|---|
| 1. Story / script | Written shot spec (color-shot-spec-template.json fields) | shot spec JSON: LUT/grade, key, rim, bleed, shift, power, dual-light sources | Spec names every colour source; a spec missing a rim or a named second source is incomplete and must not render as final |
| 2. Storyboard | Board frames from v7c poses (joint_locked_rig_v7c.py, labels=False clean mode) | reposes-v7c-clean/*.png | Board reads in silhouette; debug labels are DEBUG ONLY, never in a board that ships |
| 3. Animatic | production/pipeline/animatic_builder.py (cape-jones repo, verified 2026-10-31: storyboard images + timing + temp audio → timed animatic) | timed animatic video | Timing in frames on the exposure sheet; temp audio is labelled DEMO ONLY until recorded |
| 4. Layout | Room scale locked 2.5x (room only); other backgrounds at their approved scale; layout passes in showcase/layout-pass-* | layout-pass-room-scaled-25x-20261031.jpg | Character feet on floor, full body in frame (room: chair back at waist at 2.5x); seated = standing − 0.2 (2.5x → 2.3x, approximate, verify visually) |
| 5. Key poses | v7c rig (pivots 4/4, ball-centre joints, per-row gauntlet/fist swaps, pose_driven_swaps.json, check_gauntlet_flip.py 5/5) | reposes-v7c-clean/, clips-v7c/ | Joint caps attached, no detached fists, gauntlet/fist orientation checked against the hand-orientation table (GAUNTLET-FLIP-RULE.md) before building |
| 6. Breakdowns / in-betweens | On-twos keyframing (Darwin beat grid ~14f @ 25fps precedent); flex anticipation frame as the before-flex in-between | exposure sheet, in-between frames | Anticipation frame exists before every big move; arcs checked (Principle 7) |
| 7. Clean-up | slice_clean.py ONLY (bg from corners, mask distance >30, closing + hole fill, components by sheet, rows by centre-y, 1px feather + fringe decontamination); rembg only per-piece as a check | sliced/, pack1-clean/, pack4-20261031/ | No hand-tooled square crops; no hand-drawn PIL VFX presented as production |
| 8. Colour | 70 approved LUTs (.cube, 33³), colour-shot-spec-template.json, apply_lighting_level2_v2.py (--rim wiring tested), LIGHTING-LEVELS-0-5.md | showcase/luts-*/, showcase/lighting-level2-v2/ | LUT approval sheet includes a grey-128 control; rim follows key/LUT hue family (±20°) or the shifted key under a JoJo shift |
| 9. Compositing | Blender 5.2.3 LTS compositor stack (compositor-stack-spec.json, 18 nodes / 22 links, node types 6/6; Blender render viewed 0/1 = 0% — spec only until a rendered frame is viewed) + PIL compositor stack (10/12 layers wired = 83%) + FFmpeg lut3d (70/70 LUTs = 100%) | blender-compositor-stack.py, apply_compositor.py | Production VFX = Blender compositor + edited authored VFX; flat PIL VFX is draft only (10–20% of production need) |
| 10. Audio mix + final output | Audio cue sheet v2 (CSV/JSON, 5 cues at 24fps, delivery target −14 LUFS); FFmpeg delivery encoding | showcase/audio/audio-cue-sheet-v2.csv/.json | Demo tones labelled DEMO ONLY; recorded final audio is a separate deliverable (0% recorded); final output is checked by remote API size+SHA after repo merge, never by local commit alone |

## Colour management (stage 8, detail)
- Already wired: 70 LUTs in 33³ .cube, FFmpeg lut3d 70/70, L5 finishing (grain, vignette, halation, DOF, Rec.709 gamma 2.4 output) as a spec in LIGHTING-LEVELS-0-5.md, OpenColorIO present on the VM.
- Still missing: ACES transform in a colour-managed tool 0/1 (PIL ACES 0/1 — PIL is not colour-managed, so this must land in Blender/OCIO, not in PIL); viewed Blender render 0/1; per-shot god-ray placement 0/30.
- Rule: base art is never recoloured; light/shadow/bleed go on as separate layers on top (Screen/Add for light, Multiply hue-shifted for shadow), masked to the lit side / edge band.

## Audio standards (stage 10, detail)
- Cue sheets with frame-accurate sync at 24fps (Cape Jones) and 25fps (Darwin dance source — convert, do not mix frame rates in one timeline).
- Delivery target −14 LUFS (already in the cue sheet). LUFS is checked with FFmpeg, not by ear alone.
- Recorded audio 0% — demo tones are not a substitute and must stay labelled DEMO ONLY.

## Rigging standards (stage 5, detail)
- Bone rigs → v7c joint-locked rig (ball-centre pivots, upper/lower/cap per limb).
- Node view → Blender compositor node tree + Toon Boom method study (trial started 2026-10-31, Harmony NOT installed — do not claim it is).
- Deformation → pose libraries / drawing substitution: gauntlet-out, fist-in, flex-out, flex-roll pieces are drawing swaps driven by hand orientation (pronation/supination roll), not by moving the limb.
- Pose libraries → Richard-style pose libraries are a valid pattern (pose library ≠ dance); Cape Jones pose library = reposes-v7c-clean/ + clips-v7c/.
- Xsheet / beat grids → Darwin beat grid (~14f @ 25fps, on twos) + Cape Jones exposure sheets; OpenToonz/Tahoma2D xsheet and Brinimate timeline are the free/browser equivalents for new rig work.

# Universal pipeline — for all shows, all characters, wired here first

Mars, 2026-10-31 14:49 CDT: everything done today for Cape Jones becomes a
universal pipeline, wired up here, so no show and no character has to go
outside for it — no outsourcing, no other chatbot/tool as a dependency.
Prove it here first, with Cape Jones alone, with good shots of him alone.
Only after those shots are proven do we start other shows, and only after
a little while do we start making more characters.

## Gate order (this order is the rule, not a suggestion)

1. PROVE HERE, CAPE JONES ALONE: good shots with him alone — punch, walk,
   fighting pose / forward bicep curl, jump, dance, flying — through the
   full pipeline below, viewed, approved, in the repo.
2. THEN other shows: same pipeline, new show folder, same stage names,
   same gates, same percentage accounting.
3. THEN more characters: after a little while, after step 1 is proven.
   A new character does NOT skip stages, does NOT get a hand-tooled shortcut.

## The pipeline, character-agnostic (same stages for every character/show)

0. INGEST — character pieces in, clean-cut only. slice_clean.py:
   component-based cuts, 1px feather + fringe decontamination, no hand
   rectangles, no square crops. Joint cuts go around the ball, never through
   mid-forearm / mid-shin. Likeness rule holds for every character: reference
   image first, visible attributes only, never a character name in a prompt.
1. RIG — joint locks, ball-centre pivots, round-masked caps, vector pivot
   math (joint = parent joint + rotated (ball - anchor)). Builder script per
   character, locked-joints JSON, T-pose/A-pose lock doc. v6-style square
   pivots are DO NOT USE for bent limbs, for any character.
2. POSES — pose library from the rig, not from flat sheets. Every pose gets
   its own dated checkpoint file, never overwrites a version Mars saw.
   Rename rule, proven today: if Mars says a pose reads as something else
   (flex-hold -> fighting pose / forward bicep curl), the file is renamed
   AND the old name is logged as superseded, and the true version of the
   old name becomes its own owed item.
3. CLIPS — timing standard: TV 24fps, normal on 2s, fast on 1s, holds 6–24f.
   Exposure sheet per clip (drawings + frame numbers + loop), shot spec per
   shot (clip + camera + background + LUT + effects + audio + QC status).
4. BACKGROUNDS / LAYOUTS — layout pass per scene, safe boxes (5% / 10%),
   scale locked PER background (room scale is room-only — that rule
   generalises: a scale lock names its background, it never leaks to others).
   Stand-in backgrounds are labelled STAND-IN until the final painted one lands.
5. COLOUR / LIGHTING — colour keys first, then LUTs, then lighting levels
   0–5 (LIGHTING-LEVELS-0-5.md). LUTs are 33^3 .cube, ffmpeg lut3d compatible,
   approved in checklists with counts. Mixes are Level 1 only, ratio in the
   shot spec. Never recolour base art; rim outer-only 2–4px; bleed edge-band only.
6. COMPOSITE — pass/AOV stack, free-first: Blender 5.2.3 LTS node tree +
   PIL apply_compositor.py / apply_lighting_levels.py, same order, passes
   saved separately (shadow, rim, bleed, volume, emission, finishing).
   ACES transform gap is still owed (see WIRED-COMPOSITOR-STATUS.md).
7. EFFECTS — anchored to the thing they hit (fist, foot, impact point),
   layered falloff / gradient / streak, Blender Glare route for production.
   Flat PIL shapes are drafts only, 10–20% of production need.
8. AUDIO — cue sheet v2 format (timecode, shot, cue, in/out, duration,
   level dB, LUFS target -14, fade, status) + machine CSV/JSON for a DAW.
   Audio is delivered as LINKS in chat, never as in-chat audio. Demo tones
   are labelled DEMO ONLY; no recorded audio is ever claimed that is not recorded.
9. CLEANUP / QC — stray-pixel, hole, and line-weight metrics, large readable
   before/after, viewed before showing. Own-eyes-before-delivery: no image
   ships until Muse has viewed it.
10. REPO — PR-only, additions only, 0 deletions unless Mars approved that
    exact deletion, no force-push, merge gate, verify on main by size+SHA
    after merge. A local file, a push receipt, or a PR number alone is NOT
    confirmation. Percentages with counts on every unfinished list.

## Per-show / per-character folders (when step 2/3 opens)

- shows/<show>/characters/<character>/ — pieces, rig, poses, clips, layouts,
  luts, audio, shots, all under the same stage names above.
- A character folder without a rig lock, without a pose library, or without
  a shot spec is 0% at that stage, even if it has pictures in it.

## What is proven here so far, honestly

- Cape Jones rig v7c, fighting pose renamed and approved as a pose, punch
  pose approved, LUTs approved 36/70, lighting levels 0–5 documented and
  scripted, audio cue v2 + demo link built.
- NOT yet proven: a full good shot of him alone end-to-end through stages
  3–9 with effects on the fist, final audio, and a repo-verified merge.
  That proof shot is the next gate — it is not claimed done in this doc.

# Industry standards pull + wire-up — Cape Jones and Mars's shows (2026-10-31)

Mars, 2026-10-31: pull in ANY industry-standard stuff that helps build all of this, from
his other repos and from outside his repos, and wire it up. Barred ONLY: exact character
likeness shipped as-is, character literally, name, script dialogue, logo. Everything else
is pullable; character images are transform-only (parody / wholly different character
before release). No show character art, names, dialogue, or logos are listed as pulls
below — only tools, systems, and methods.

## Standards pulled — 6/6 groups = 100% as documents (wiring status per group below)

| # | Standard (public source, by name) | Wired into Cape Jones docs | Still missing (honest) |
|---|---|---|---|
| 1 | 12 Principles of Animation — Disney, *The Illusion of Life* (Thomas & Johnston): squash & stretch, anticipation, staging, straight-ahead vs pose-to-pose, follow-through/overlap, slow in/out, arcs, secondary action, timing, exaggeration, solid drawing, appeal | YES — 12-PRINCIPLES-CHECKLIST-20261031.md, 12/12 principles with a Cape Jones example + gate each. Checklist wired 12/12 = 100% | Per-shot application 0/30 shots |
| 2 | Studio pipeline stages — story/script → storyboard → animatic → layout → key poses → breakdowns/in-betweens → clean-up → colour → compositing → audio mix → final output | YES — PIPELINE-TEMPLATE-20261031.md, 10/10 stages with tool, file, and gate each. Template wired 10/10 = 100% | Shots run end-to-end 0/30 |
| 3 | Colour management — ACES / OpenColorIO, Rec.709 gamma 2.4 output, LUT .cube workflow | PARTIAL — 70 LUTs (33³ .cube) approved 70/70, FFmpeg lut3d 70/70, L5 finishing spec (Rec.709 gamma 2.4) in LIGHTING-LEVELS-0-5.md, OpenColorIO present. Wired 3/5 items = 60% | ACES in a colour-managed tool 0/1; viewed Blender render 0/1 |
| 4 | Rigging standards — bone rigs, node view, deformation, pose libraries / drawing substitution, xsheet / beat grids | YES as mapping — PIPELINE-TEMPLATE stage 5: v7c rig = bone rig, Blender node tree = node view, gauntlet/fist swaps = drawing substitution driven by forearm roll, Darwin beat grid (~14f @ 25fps, on twos) = xsheet. Toon Boom method study: trial started 2026-10-31, Harmony NOT installed — do not claim it is | Harmony trial install + method study report (browser task running, result pending) |
| 5 | Audio standards — cue sheets, LUFS loudness, frame-accurate sync | YES — cue sheet v2 (CSV/JSON, 5 cues at 24fps), delivery target −14 LUFS, FFmpeg LUFS check. Wired as spec 3/3 = 100% | Recorded final audio 0% (demo tones only, labelled DEMO ONLY); 25fps source conversion for Darwin material |
| 6 | Free / industry tool stack — OpenToonz/Tahoma2D, Synfig, Blender Grease Pencil, Krita, FFmpeg, Rigby2D/Spine JSON, DaVinci Resolve (free), Brinimate (browser) | YES — FREE-STACKS-INDUSTRY-STANDARDS.md already wired this stack (sibling work, not duplicated here); free-stack install/test workstream running separately | Free-stack install verification + per-tool tests (separate workstream, results pending) |

Standards pulled as documents: 6/6 = 100%. Standards fully wired end-to-end (not just documented):
3/6 = 50% (principles checklist, pipeline template, audio spec). Colour 60%, rigging mapping
documented but Harmony study pending, free-stack verification pending.

## Repo tools found — Mars's other repos (code search via gh_api.py, 2026-10-31)

Searches run: pipeline (2,140 hits), builder (874), tool (5,968), template (3,568) — most hits
are vendored upstream source code inside production/tools/, filtered out below. Only
Mars's own pipeline docs, builders, and pulled-tool entries are counted. Show character
material was NOT counted and is NOT listed.

| # | Repo + path | What it is | Wired yet? |
|---|---|---|---|
| 1 | mhvnsnt/cape-jones docs/COMPLETE-PIPELINE.md (19,742 chars, verified via API) | "Studio in a Box" — FlipaClip drawings in, finished animation out | YES — cited in pipeline template stage order |
| 2 | mhvnsnt/cape-jones docs/pipeline/EP1-RENDER-PIPELINE.md (16,214 chars, verified) | EP1 render pipeline, Track D report 2026-10-24 | YES — cited in pipeline template |
| 3 | mhvnsnt/cape-jones cape-jones-rig/UNIVERSAL-PIPELINE.md (5,062 chars, verified) | Universal pipeline for all shows/characters, Cape Jones first | YES — gate order in pipeline template |
| 4 | mhvnsnt/cape-jones cape-jones-rig/cleanup-pipeline.md (509 chars, verified) | Clean-up pipeline TEMPLATE (its own words: "not yet a built pipeline") — slice_clean.py steps | PARTIAL — template cited; built pipeline = slice_clean.py, already wired |
| 5 | mhvnsnt/cape-jones production/pipeline/animatic_builder.py (3,767 chars, verified) | Storyboard images + timing + temp audio → timed animatic | YES — pipeline template stage 3 |
| 6 | mhvnsnt/cape-jones 3d-assets/cape-jones-rig/tools/sit_pose_builder.py | Sit-pose builder for the rig | PARTIAL — listed; sit pose integration not verified in this pass |
| 7 | mhvnsnt/cape-jones production/tools/simple-retarget-tool/README.md | Simple retarget tool | PARTIAL — listed; retarget wiring is the Darwin dance spec, not this tool's output |
| 8 | mhvnsnt/cape-jones production/tools/opentimelineio/ (OTIO docs/tutorials) | OpenTimelineIO — industry-standard timeline interchange format | YES as format — cited in rigging mapping (xsheet/timeline interchange) |
| 9 | mhvnsnt/cape-jones production/tools/glaxnimate/ (source) | Glaxnimate — free 2D animation tool (vendored source) | YES as free equivalent — already in FREE-STACKS doc |
| 10 | mhvnsnt/cape-jones production/tools/natron/ (source) | Natron — free compositing (vendored source) | YES as free equivalent — Blender compositor is the production default, Natron is the free alt |
| 11 | mhvnsnt/cape-jones production/tools/coa_tools2/ | Cutout animation tools (Blender) | PARTIAL — listed; not verified as wired into v7c rig in this pass |
| 12 | mhvnsnt/cape-jones tools/pulled/three-anime-style/, AnimeEffects/ | Pulled 2D animation tools (three.js anime style, AnimeEffects) | PARTIAL — listed as pulled tools; no output from them verified in this pass |
| 13 | mhvnsnt/cape-jones production/tools/audio/audacity/, musescore/ | Audacity (audio edit), MuseScore (notation) — free audio tools | PARTIAL — listed; Cape Jones audio cue sheet is the wired audio spec, not these tools' output yet |
| 14 | mhvnsnt/cape-jones production/tools/audio/rvc/, tts-webui/, kittentts/, ace-step/, deepfilternet/ | Voice/TTS/audio-ML pipelines (RVC voice, TTS, KittenTTS, ACE-Step, DeepFilterNet) | NO — listed only; not wired into Cape Jones audio (cue sheet is tones + spec, not voice) |
| 15 | mhvnsnt/cape-jones production/tools/blendertools/ (send2ue, ue2rigify) | Blender → Unreal rig tools | NO — listed only; Cape Jones is not an Unreal pipeline in this pass |
| 16 | mhvnsnt/cape-jones production/tools/comfyui/, ltx2/ | ComfyUI / LTX video generation tools | NO — listed only; generative video is not a Cape Jones final-shot source |
| 17 | mhvnsnt/cape-jones production/tools/anime-upscaling/ | Anime upscaling web app | NO — listed only |
| 18 | mhvnsnt/Bannon tools/statue-to-game/PIPELINE.md | Statue-to-game pipeline (game lane, not show lane) | NO — reference only; game pipeline, not wired into Cape Jones show pipeline |
| 19 | mhvnsnt/Bannon tools/model_diag/CHARACTER_PIPELINE.md | Character pipeline (game lane) | NO — reference only |
| 20 | mhvnsnt/Bannon tools/generative/GENERATIVE_PIPELINE.md | Generative pipeline (game lane) | NO — reference only |
| 21 | mhvnsnt/Bannon tools/rigging/TOOLS_RIGGING.md | Rigging tools list (game lane) | NO — reference only |
| 22 | mhvnsnt/Bannon tools/video/TOOLS_VIDEO.md | Video tools list (game lane) | NO — reference only |
| 23 | mhvnsnt/Bannon docs/production-bible/RIG_REPAIR_PIPELINE.md | Rig repair pipeline (game lane) | NO — reference only |
| 24 | mhvnsnt/cape-jones docs/research/AUTO-RIGGING-TOOLS-2026.md, FREE-3D-TOOLS.md | Auto-rigging + free 3D tools research | PARTIAL — research cited; auto-rigging not wired into v7c rig in this pass |

Repo tools found (curated, own docs + pulled tools, vendored upstream code filtered out):
24 entries. Wired (YES): 6/24 = 25%. Partial: 9/24 = 38%. Not wired / reference only:
9/24 = 38%. "Wired" here means cited in the pipeline template or already in a Cape Jones
script/doc — it does NOT mean the tool's output is in a final shot.

## What was wired in this pass (files, not just lists)
- [12-PRINCIPLES-CHECKLIST-20261031.md](sandbox://workspace/cape-jones-rig/12-PRINCIPLES-CHECKLIST-20261031.md) — new file, 12/12 principles with Cape Jones example + gate.
- [PIPELINE-TEMPLATE-20261031.md](sandbox://workspace/cape-jones-rig/PIPELINE-TEMPLATE-20261031.md) — new file, 10/10 stages with tool, file, and gate.
- [INDUSTRY-STANDARDS-PULL-20261031.md](sandbox://workspace/cape-jones-rig/INDUSTRY-STANDARDS-PULL-20261031.md) — this file.
- No version Mars has seen was overwritten. No show character art, name, dialogue, or logo
  was copied. Toon Boom Harmony is NOT claimed as installed (trial started, browser task
  running, result pending).

## Still owed
- Per-shot 12-principles checks: 0/30 shots.
- Shots run end-to-end through the 10-stage pipeline: 0/30.
- ACES in a colour-managed tool: 0/1. Viewed Blender render: 0/1. Per-shot god-ray placement: 0/30.
- Recorded final audio: 0% (demo tones only).
- Harmony trial install + method study report (browser task pending).
- Free-stack install verification + per-tool tests (separate workstream pending).
- Repo tools marked PARTIAL/NO above: 18/24 not fully wired — each needs its own wiring
  pass (voice tools, Unreal tools, generative tools, and Bannon game pipelines are reference
  only until Mars says otherwise for a specific one).
- Flex clip retarget, punch/room/JoJo picks, and repo push verification are separate
  workstreams and are NOT claimed here.

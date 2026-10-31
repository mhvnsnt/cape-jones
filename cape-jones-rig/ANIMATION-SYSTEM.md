# Cape Jones animation system — wired from our repos' methods, not their characters
Mars, 2026-10-31 11:53 CDT: get all their systems 100% wired up.
No characters, names, logos, or literal dialogue from other shows.
Methods and systems only, with Cape Jones's own pieces on them.

## Systems, counted
- Rig hierarchy + joint locks — WIRED, v4. Torso -> shoulder -> upper
  arm -> elbow -> lower arm; pelvis -> hip -> upper leg -> knee ->
  lower leg. Shoulders (430,445)/(670,445), hips (495,760)/(585,760).
  Builder: joint_locked_rig_v4.py, registry locked-joints-v4.json.
- Clean cuts — WIRED. slice_clean.py, mask by sheet, no square crops.
- Pose library — WIRED, v4. A-pose, flex, punch, dance, seated, jump
  (tuck-in, whole-arm raise). Files in reposes/joint-*-v4-20261031.png.
- Timeline / keyframes — WIRED as format, clips/ below. A clip is a
  JSON list of keyframes: pose angles per joint, frame number, hold.
  24 fps, normal on 2s (12 drawings/sec), snaps on 1s, holds 6-24 frames.
  Renderer: render_clip.py reads a clip JSON and renders each keyframe
  with the v4 rig, so a clip is angles, not new drawings.
- Symbol library + JSFL FLA — PARTLY WIRED. Static symbols + JSFL
  exist (build-cape-jones-rig-v8.jsfl). Timeline JSFL (build a .fla
  timeline from clip JSON, layers named, pivots at joints) is next,
  not yet built — do not claim it done.
- Shot spec + manifest + SHA + proof — PARTLY WIRED. Repo pushes
  already verify by size + blob SHA on main (PRs #276-279, 98/98).
  Shot spec YAML + frame proof (reopen, count frames, SHA) is next,
  following the TRIPPEDD pipeline pattern.
- Technique library — WIRED as index, not as copied art.
  Stages: script -> boards -> animatic -> model sheet -> rig ->
  scene -> final. Shot types indexed: punch, take, walk, lip sync,
  cutout rig, smear, jump tuck, flex, dance. Sources are methods
  docs in our own repos (see below), plus public-domain / open-movie
  technique references, never another show's character art.

Total wired: 4/7 systems fully wired = 57%, 2 partly wired, 1 format
only. The remaining work is named above, not hidden.

## Source repos used for methods (checked 2026-10-31)
- cn-gigaleak-chowder: KIT-INDEX.md, RESEARCH.md — kit structure.
- samurai-jack-repo: method/tartakovsky-method.md,
  craft-for-our-shows/CRAFT-EP01.md — staging / method.
- disney-tva-bbb-pulls: ANIMATION-REFERENCE.md — technique index,
  points to animation-research-library (PD cartoons, Blender open
  movies, Pepper&Carrot).
- TRIPPEDD-Animation-Studio: PIPELINE.md — manifest+SHA, shot spec,
  Blender headless, frames + proof + QC.
- Grok-Animation-Project: pipeline/, docs/ — pipeline structure.
- game-reverse-engineering: PLAYBOOK.md, PULL-LOG.md — extraction
  structure, not game assets.
- cape-jones itself: v8 T-pose lock, v3/v4 joint locks, clean cuts,
  Pack1, cut limbs.
- Flying sheets: branch feature/character-parts-expansions-20261031,
  characters/sheets/variations/ = NOTE.md + README.md only, 0/5
  images landed. Flying poses are built from this rig until those
  images land, not waited on.

## Cutout rig, first priority — Spine / Rigby2D / Synfig wiring
Checked 2026-10-31: production/pipeline/ANIMATION-PIPELINE-2026.md
and production/tools/BLENDER-5X-UPGRADE.md DO exist on branch
feature/character-parts-expansions-20261031 in cape-jones.
Pipeline there is Tahoma2D -> Synfig (bone rigs + tweening) ->
RIFE -> OpenToonz, plus Blender 5.2.3 LTS as production default
(docs wired, binary not in the sandbox — install block in that doc).
Our rig wires into that pipeline as:
- Pieces: cape-jones-rig/pieces/ + pack1/ + cut-limbs/ (already on main).
- Rig: cape-jones-rig-spine.json — bones parented as above, slots
  = piece attachments, animations = apose + jump-tuck angles from v4.
  This is the format Rigby2D / Spine-compatible tools read. Synfig
  bone rigs use the same parent/length/pivot idea, with pivots at
  the v4 joints, not at piece centres.
- Tools to pull/document next, open-source only: Synfig (bone rigs,
  tweening, already in the pipeline plan), Rigby2D (skeletal editor,
  AutoRig, IK, Spine JSON out), Stretchy Studio (mesh deform, Spine
  out), Flare/OpenToonz fork (partial FLA/XFL import), fla-decoder
  and JPEXS (study/convert old .fla/.swf structure, not characters).
  Do NOT vendor any other show's .fla/.swf art into cape-jones.
- FLA path: JSFL builds .fla symbols from the same pieces, with
  pivots at v4 joints. Timeline JSFL from clip JSON is still the
  remaining FLA piece, after the Spine/Synfig rig template above.

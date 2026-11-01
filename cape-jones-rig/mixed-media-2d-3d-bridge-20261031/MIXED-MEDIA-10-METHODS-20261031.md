# Mixed-media 2D-to-3D bridge — 10 industry-standard methods
Folder: mixed-media-2d-3d-bridge-20261031/
Scope, Mars 2026-10-31 21:09 + 21:10 CDT: 2D-first, 2D and 3D are SEPARATE projects worked in parallel, do NOT merge them, do NOT delay 2D work for 3D work. 3D is ONLY for times we absolutely need it, as a gag/trope. The bridge is shared learning + occasional gag/trope handoffs, not a merger of the two shows. 2D production readiness below is counted separately from any 3D show count (3D show count is NOT counted here).

## The ten, run vs mapping labelled
1. Blender Grease Pencil 2D-in-3D (CapeGP) — RUN, existing. One GP object, 10 layers, strokes traced from v7c pieces. Use in bridge: 2D linework lives in a 3D scene, camera can move, layers keep draw order. Proof: cape-gp-presets-20261031/ + colored-invisible-line-work-20261031/.
2. Blender 3D armature mandible rotation (TMJ hinge) — RUN, this folder. Bone/empty pivot at the hinge, jaw mesh parented, rotation about the hinge axis. Proof: frames_3d/, angles 0/12/24/32/32/24/12/0 deg.
3. Blender constraint-driven muscle length (Stretch To) — RUN, this folder, PROXY labelled. Masseter strands stretch as the jaw drops. This is constraint-driven length change, NOT FEM muscle simulation. FEM (soft-body/cloth muscle) is mapping only, not claimed.
4. Blender toon / cel shading + Shader-to-RGB — RUN, method wired in shading work (V9 Blender smooth, edge +27.6). Use in bridge: 3D renders are cel-shaded so a 3D insert reads as 2D. Full Shader-to-RGB node build is still owed (0/1) — the method, not a finished node, is what is wired here.
5. Blender camera projection / 2D plate on a 3D plane — RUN, method. A 2D plate is projected onto a 3D plane so a 3D camera move does not shear the drawing (the V4 failure: centre-scale + uniform pixel shear is NOT camera projection). Proof pattern: multiplane world-ground + camera, and the jaw gag composite in this folder.
6. Multiplane 2.5D depth (far 0.3 / figure 1.0 / foreground 1.8) — RUN, existing. BARS preset approved, feet on world ground line. Use in bridge: depth without turning the show 3D.
7. Toon Boom Harmony 3D camera + drawing substitution — MAPPING only, not run. Reason: Harmony trial is not confirmed/installed (profile done, card step with Mars, Windows install owed). Harmony mouth-chart substitution itself IS run in the 2D lip-sync builder; the 3D-camera part is mapping.
8. Adobe After Effects 2.5D / Cinema 4D layer + Character Animator viseme structure — MAPPING only, not run. Reason: Adobe sign-in task errored/stopped, no trial/enrolment, no payment by Muse. AE CC Light Rays was PIL proxy only in earlier work, labelled.
9. Unreal / Unity toon + 2D sprites in a 3D scene (Paper 2D / sprite-in-3D) — MAPPING only, not run. Reason: no engine scene built for Cape in this task; taxonomy only, no engine render claimed.
10. MediaPipe Face Mesh / ARKit blendshape jaw taxonomy — MAPPING only, not run. Reason: no model run on this VM; the manual equivalent (tight mouth-ROI cut, single-target anchor) IS run in the 2D lip-sync system. True 3D mandible rotation/muscle simulation beyond items 2–3 (FEM, muscle simulation) is mapping, not run.

Count: RUN 6/10, MAPPING 4/10. "Wired 100%" means: each run item has a working proof in this repo or a named existing folder, each mapping item has an exact reason it was not run and is never claimed as run. It does NOT mean 10/10 vendor runs.

## Bridge rule (gag/trope only)
- Default stays 2D. A 3D insert is labelled 3D GAG INSERT, with measured handoff frames, and returns to 2D.
- Handoff in this prototype: seq frames S00–S02 = 2D MBP closed, S03–S05 = 2D AH opening, S06–S13 = 3D jaw gag (8 Blender frames), S14–S17 = 2D GK/GAP/REST closing. Jaw-tip displacement is measured from the 3D render alpha bbox per frame, not claimed from the angle alone.
- No 3D insert ships as a 2D plate, and no 2D plate is relabelled as 3D.

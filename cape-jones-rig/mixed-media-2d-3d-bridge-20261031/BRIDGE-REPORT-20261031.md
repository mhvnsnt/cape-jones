# 2D-to-3D bridge — report
Folder: mixed-media-2d-3d-bridge-20261031/
Mars orders: 2026-10-31 21:09 CDT (build the bridge, 10 industry-standard mixed-media things, TV production readiness, then build it) + 21:10 CDT clarification (2D and 3D are SEPARATE projects, worked in parallel, do NOT merge, do NOT delay 2D for 3D; bridge = shared learning + occasional gag/trope handoffs, not a merger; keep 2D readiness separate from any 3D show count).

## What was built
- Blender 5.2.3 LTS, Cycles CPU (Eevee failed headless: libEGL.so.1 missing; Cycles was the free way around, not a claim of GPU).
- True 3D mandible rotation: TMJ_Hinge empty at (0,-0.35,0), Mandible mesh parented to it, keyframed rotation X: 0/12/24/32/32/24/12/0 degrees, 8 frames, 476x688, transparent.
- Constraint-driven muscle length: Masseter_L/R cylinders with Stretch To constraints to jaw attaches. This is constraint-driven length change, NOT FEM muscle simulation — FEM is mapping only.
- Jaw gag sequence, 18 frames @24fps (GIF 100ms/frame): S00–S02 2D MBP closed, S03–S05 2D AH opening, S06–S13 3D jaw gag, S14–S15 2D GK, S16–S17 2D REST. Handoffs: 2D→3D at S05→S06, 3D→2D at S13→S14. All frames 476x688. Grey in GIF/contact is display-only; 3D masters in frames_3d/ are transparent RGBA.

## Measured handoffs (not claimed)
- 3D alpha bbox, all 8 frames: x 58–418, top 91, bottom 555–560px, alpha 132,629–133,122px.
- Bottom range is only 5px (555 at 32deg, 560 at 12deg, 558 at 0deg) — NOT a big vertical drop. Reason, stated plainly: hinge rotation is about the X axis, seen front-on in ortho, so the jaw moves forward in depth (Z), not down on screen (Y). The gag reads as a style-switch insert (2D head → stylised 3D head → 2D head), not as a large on-screen jaw drop. A side-view 3D jaw would show the drop clearly; that is a next build, not claimed here.
- 3D head is a stylised proxy (sphere head, purple cap, white eyes, bevelled jaw box), NOT Cape's actual face/likeness. Do not present it as the 3D show's head.
- V1 blocky head (cube skull + sphere cowl overlapping) was superseded by V2 and its frames deleted/replaced; V1 is not delivered.

## 10 industry-standard mixed-media methods (full table in MIXED-MEDIA-10-METHODS-20261031.md)
RUN 6/10: Blender Grease Pencil (CapeGP), Blender armature mandible rotation, Blender Stretch-To muscle length (proxy), Blender toon/Shader-to-RGB method, Blender camera projection / 2D plate on 3D plane, multiplane 2.5D depth.
MAPPING 4/10, with reasons: Toon Boom Harmony 3D camera (trial not confirmed/installed), After Effects 2.5D/Cinema 4D + Character Animator (Adobe sign-in task errored, no trial/payment by Muse), Unreal/Unity toon + sprites-in-3D (no engine scene built), MediaPipe/ARKit jaw taxonomy (no model run on this VM).
"Wired 100%" here means each run item has a working proof and each mapping item has an exact non-run reason — it does NOT mean 10/10 vendor runs.

## TV production readiness — 2D only (full counts in TV-PRODUCTION-READINESS-2D-20261031.md)
Computed average of 7 gating components: (0+0+0+0+0+70+90)/7 = 22.9% ≈ 23%.
- Shots end-to-end 0/30 = 0% (gating fact: no finished episode exists yet)
- Per-shot proofs 0/30 = 0% (shading, multiplane, shafts/effects, lip-sync, Invisible V1, Colored Line Work all 0/30 per-shot)
- Recorded final audio 0% (demo -16.27 LUFS, not -14; song tempo 152 vs ~107 BPM open)
- True masters 0/4 = 0% (3/4, side, back, torso-twist)
- Lip-sync production 0% (movement system exists, approval 0/1; audio-driven timing 0/1; OH/OO + other visemes gaps)
- Storyboards 21/30 = 70% (pending CJ-01,02,04,11,15,17,18,20,27)
- QC 27/30 PASS = 90% (fails CJ-05,06,26, hues unstated, Mars ruling owed)
Supporting, not in the average: clean sliced 140/184 = 76%, wired inventory 24/41 = 59%, no-crop pattern 46/46 = 100% but full-scene 1/46 = 2%.
Blockers vs additives: blockers = shots end-to-end, storyboard/QC closes, recorded audio, true masters, per-shot applications, Mars-only gating decisions. Additives/extras = everything after 100% production-ready, including new shading presets (STOPPED per Mars 20:53 CDT).

## Approvals owed, no push
Bridge approval 0/1. 3D jaw gag approval 0/1. No repo push made; landing is a separate step.

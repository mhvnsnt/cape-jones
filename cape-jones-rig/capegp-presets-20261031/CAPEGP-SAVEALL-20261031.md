# CapeGP save-all package list — nothing in the GP set is lost or left unstaged

**Rule:** save ALL GP stuff. This list covers (A) the original depth
package GP files and (B) this preset pack. Sizes below are as listed at
build time; the landing workstream verifies by size+SHA on main after
merge — a size here is not a landing verification. No file in either
list was overwritten by this task, and no file was pushed by this task.

## A. Original depth package — depth-25d-blockers-broken-20261031/
GP core (the set Mars said to save):
- cape-gp-rig-experimental-20261031.blend (119,753 bytes) — original
  CapeGP .blend, frames 1 apose, 2 mid, 3 true-final, 4 hold, 10 JoJo 03.
- gp_frames.json (58,591 bytes) — traced stroke frames for that .blend.
- trace_gp_frames.py (8,008 bytes) — cv2 tracing builder, v7c joint math.
- build_gp_blend.py (3,212 bytes) — original Blender builder + render.
- EXPERIMENTAL-GP-PIPELINE-USE-20261031.md (4,228 bytes) — original
  pipeline rule doc (PIL/v7c default, GP for proofs/motion/layer trees).
- gp-jojo03-face-snap-experimental-20261031.png (296,634 bytes) — frame 10
  face-snap proof, R arm in FaceSnapArm above Head.
- gp-motion-0001.png … gp-motion-0004.png (~290–295 KB each) — motion
  frames apose → mid → true-final → hold.
- gp-motion-experimental-20261031.gif (19,001 bytes) + .mp4 (35,086 bytes)
  — the motion Mars praised in the follow-up: apose to true-final flex.
- gp-true-final-before-after-experimental-20261031.png (359,620 bytes) —
  approved coloured original vs GP outline version, same pose.

Rest of that folder (kept, not GP core, listed so nothing is dropped):
- EXPERIMENTAL-BLOCKERS-BROKEN-REPORT-20261031.md, EXPERIMENTAL-3D-SIDE-
  READY-TOOLS-20261031.md, angle-configs-gate-20261031.csv,
  angle-configs-recovered-20261031.json, build_25d_and_tests.py,
  cowl_gate_v2.py/.csv, cowl_gate_v2b.py/.csv,
  experimental-depth-by-scale-20261031.gif/.mp4/contact + spec JSON,
  experimental-lipsync-layer-20261031.gif/.mp4/contact,
  experimental-multiplane-camera-20261031.gif/.mp4/contact,
  experimental-pseudo-turn-20261031.gif/.mp4/contact.

## B. This preset pack — capegp-presets-20261031/ (NEW, this task)
- README-CAPEGP-20261031.md — formal name, layers, presets, pipeline rule,
  new-character use, no-crop gate, staging/prototype/test plan.
- METHODS-CAPEGP-20261031.md — 11 industry methods, run vs mapping vs owed.
- JOINT-SMOOTHING-20261031.md — JOINT_SMOOTH method + measurements.
- build_capegp_presets.py — trace builder for the 6 presets + Chaikin.
- capegp_presets_frames.json (104,805 bytes) — 6 preset stroke frames.
- build_capegp.py — Blender builder, all-presets or single-preset .blend.
- capegp_all_presets.blend (135,935 bytes) — CapeGP, frames 1–6 = the 6 presets.
  INSPECTION ONLY: do not render proofs from this file (GP layer holdover,
  see README). Proof renders come from the single-preset blends below.
- single-NORMAL.blend, single-APOSE_FLEX.blend, single-FACE_SNAP.blend,
  single-COWL_SNAP.blend, single-CHEST_SNAP.blend, single-JOINT_SMOOTH.blend
  — one preset each, one frame each, no holdover.
- render_single_presets.sh — builds the single blends and renders the proofs.
- preset-0001.png … preset-0006.png — proof renders FROM the single blends,
  one per preset, in preset order NORMAL, APOSE_FLEX, FACE_SNAP, COWL_SNAP, CHEST_SNAP, JOINT_SMOOTH.
- capegp-preset-contact-20261031.png — 6-preset contact sheet (built from
  the six proof renders, labels on sheet only).
- CAPEGP-SAVEALL-20261031.md — this file.

## C. What is NOT in this save-all (stated, not hidden)
- GP colour fills, interior linework, line-weight-by-depth: owed, no files.
- A smoothed motion sequence (all 4 motion frames through Chaikin): owed.
- A new-character dry run through the CapeGP builder: owed (test T5).
- CapeGP in any other repo: NOT staged there yet, testing here first.
- Any repo push: none by this task; landing is a separate workstream.

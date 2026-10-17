# Pinocchio — headless CPU auto-rigger

**What:** Pinocchio (Baran & Popović, SIGGRAPH 2007, MIT CSAIL) — the classic
automatic rigging system. Given a static character mesh + a skeleton template,
it (1) embeds the skeleton into the mesh via medial-surface sphere packing +
discrete graph matching + continuous refinement, and (2) computes smooth
skinning weights (heat-diffusion-style) per vertex per joint. No GPU, no
account, no upload — pure C++, runs on a laptop CPU in about a minute for a
~80k-vert mesh.

**Why here:** It is the only genuinely *local + headless + free-for-commercial*
auto-rigger that runs on CPU. Every other 2026 option is either GPU-bound
(UniRig, Puppeteer, MagicArticulate, HumanRig, RigAnything), web-only
(Mixamo, Cinevva, Tripo, Meshy, DeepMotion), or Windows-GUI-only (AccuRIG).

**Version / provenance:**
- Upstream: Ilya Baran's original source release (MIT project page, now
  offline) via mirror `jingma-git/Pinocchio` (git, 2026-10-17).
- Library: `../pinocchio-src/Pinocchio/` — **GNU LGPL-2.1** (commercial use
  OK; we use it as an unmodified compiled library, no code copied).
- This lane's additions: `rig.cpp` (headless CLI driver), `proof/` scripts.
- Build fix for g++ ≥ 11 (two one-line friend-declaration scope fixes in
  `vector.h` / `rect.h`) — documented in `pinocchio-src/BUILD-NOTES.md`.

**Install / build (Linux):**
```bash
cd production/tools/pinocchio-src/Pinocchio && make        # libpinocchio.a
cd ../pinocchio && g++ -O3 -w -I../pinocchio-src/Pinocchio rig.cpp \
    -o rig -L../pinocchio-src/Pinocchio -lpinocchio -lm
```

**Run:**
```bash
# mesh -> rigged skeleton + weights (model is NEVER rescaled;
# joints are mapped back into the original mesh units)
./rig work/cj_dec.obj work/cj_pinocchio --skel human
# outputs: work/cj_pinocchio_skeleton.json, work/cj_pinocchio_weights.bin
```

`weights.bin` format: `int32 nverts, int32 njoints`, then
`float32[nverts*njoints]` row-major (weight row *i* = input-mesh vertex *i*).

**Blender import + pose proof:**
```bash
blender -b --python proof/blender_proof.py -- \
    work/cj_dec.obj work/cj_pinocchio_skeleton.json \
    work/cj_pinocchio_weights.bin proof/
# renders proof/pinocchio_pose_front.png, _side.png, _rest_front.png
```

**Transfer weights to the full-res mesh** (nearest-vertex, scipy):
```bash
python3 proof/transfer_weights_full.py work/cj_full.obj work/cj_dec.obj \
    work/cj_pinocchio_weights.bin work/cj_pinocchio_weights_full.bin
```

**Known limits (vs BlenRig 6 / ML riggers):**
- Template-based: human/horse/quad/centaur skeletons. Great for Cape Jones
  (humanoid), wrong tool for creatures with extra limbs.
- No face rig, no IK/FK controls, no muscle system — it produces a plain
  joint skeleton + weights. Pair it with Rigify/BlenRig controls, or use it
  as the *bone-placement + skinning* stage and build controls on top.
- Wants a single closed mesh in a neutral pose; multi-part meshes keep
  only the largest component (logged).
- On Tripo's 1M-vert meshes, decimate to ~50–100k first, then transfer
  weights back (script above) — minutes instead of hours.

**Cape Jones proof (2026-10-17):** `proof/pinocchio_pose_front.png` (+ side,
rest) — 18-joint human skeleton auto-embedded in the 84k decimated mesh,
elbows/knees/shoulders posed. Read with own eyes before claiming.

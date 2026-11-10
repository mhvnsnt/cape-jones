# 2D-to-3D jaw gag — REBUILT with Cape Jones's ACTUAL 3D model

Mars, 2026-10-31 22:46 CDT, replying to the proxy jaw gag GIF:
save the proxy as 3D draft one, it is hilariously bad/ugly, go get his actual
3D model from the repo and use that instead. Done here. Parent owns the
explanation in chat; this file is the build record.

## 1. Draft One saved, locked
- Proxy version saved as **3D DRAFT ONE** in `draft-one/` (GIF + contact copies,
  plus `DRAFT-ONE-20261031.md`). Original bridge folder untouched, no file
  overwritten or deleted there.
- Draft = stylised proxy only: sphere head, purple cap, white eyes, bevelled
  jaw box. NOT canon, NOT the real model. Draft approval 0/1 separately.

## 2. Actual model found and verified
Repo: `mhvnsnt/cape-jones`, branch main, tree listing (52,999 entries, truncated
flag true, but the 3d-assets hits below are exact paths from that listing).

- **Main rigged model:** `3d-assets/cape-jones-rig/cape_jones_rigged.blend`
  (92 MB, downloaded to `model/cape_jones_rigged.blend` in this folder)
- Also downloaded: `3d-assets/face-rig/cj_face_parametric.blend` (2.2 MB)
- Other exact repo candidates, NOT used for this gag:
  `3d-assets/cape-jones-rig/cape_jones_rigged_w5r.blend`,
  `cape_jones_rigged_w5r_clean.blend`, `cape_jones_rigged_w5r_idle.blend`,
  `3d-assets/face-rig/cj_mouth_kit.blend`,
  `3d-assets/tripo-sitting-model/pieces/him.glb` (sitting model, not the hero rig),
  `anims/show/cape-jones/*.glb` (episode animations, not the base rig).

Verified in Blender 5.2.3 LTS, headless, from the downloaded file:
- Objects (4): `CapeJones_Body` MESH 910,374 verts, `CapeJones_Cape` MESH
  82,213 verts, `BlenRigMdefCage` MESH 1,057 verts (hidden from render),
  `CapeJones_Rig` ARMATURE.
- Armature bones include `head` and `jaw` (jaw parent = head, rotation mode XYZ,
  jaw head (0, -0.068, 0.845), tail (0, -0.098, 0.825)).
- Body vertex group `jaw`: 29,313 verts, max weight 0.999. No shape keys on
  the body. Armature modifier on the body points at `CapeJones_Rig`.
- Model-alone proof: `model-alone-front.png` (full body, default pose) and
  `frames_3d/final_f01_0deg.png` (head close-up, jaw 0deg) — purple cowl,
  white eyes, white suit, purple chest emblem, black cape. That is Cape Jones,
  not a generic proxy.

## 3. Rebuilt gag
New dated folder only, no existing file overwritten, no repo push.
- Sequence, 18 sequence positions @150ms each (2,700ms total), 476x688,
  same structure as the original:
  S00-S02 2D MBP closed, S03-S05 2D AH opening, S06-S13 3D jaw gag,
  S14-S15 2D GK, S16-S17 2D REST.
  Stored GIF frames: 12, because PIL merges consecutive identical frames
  and sums their durations (e.g. MBP x3 = 450ms, 32deg x2 = 300ms) —
  playback timing is unchanged, distinct stored frames are 12, sequence
  positions are 18. This is stated here so the frame count is not misread.
  2D frames reused unchanged from the original bridge `frames_seq/`.
- 3D section: actual model, Blender 5.2.3 Cycles CPU, 32 samples, denoising,
  transparent film, ortho head camera (scale 0.30, head centre (0, -0.02, 0.82)),
  Sun + area lights. Cage and armature hidden from render.
- True mandible rotation: pose bone `jaw`, rotation X (local) at
  0 / 12 / 24 / 32 / 32 / 24 / 12 / 0 degrees. No FEM muscle simulation
  claimed (that was mapping-only in the original bridge work).
- Transparent 3D masters: `frames_3d/final_f01..f08_*.png` (RGBA).
  GIF/contact display composites use grey (128) background, matching the
  original 2D display; masters stay transparent.

## 4. Measured proof (not just claimed)
- Front head close-up, pixel diff vs jaw 0deg (RGB+alpha diff >30):
  12deg = 25,654 px, 24deg = 43,310 px, 32deg = 51,811 px, return to 0deg = 0 px
  exactly (loop closes). Diff grows monotonically with jaw angle.
- Side-view proof: `jaw-gag-actual-model-side-drop-20261031.png`
  (side 0deg vs 32deg, full + head-crop zoom). Honest limit: a numeric
  chin-drop in pixels is NOT quoted from the side view, because the
  model's default raised arm/shoulder fills the head-zone bbox in both
  side frames (lowest y 399 in both), contaminating a simple bbox metric.
  The side frames are visual proof only; the front diff above is the
  measured proof. The model's default pose (arms out/raised) was NOT
  changed — only the jaw bone was rotated.
- No-crop: 3D masters are 476x688, alpha bbox (0, 102, 476, 688) on all
  8 front frames — no edge clipping of the head/chest framing, and the
  frame size matches the 2D sequence frames exactly.
- First attempt notes, owned: the first full-body render framed the head
  too small and the jaw change was invisible at that scale; the first
  side camera pointed the wrong way and rendered empty frames. Both were
  fixed (ortho head close-up; tracked side camera) and the bad side
  frames were overwritten only inside this new folder, never in the
  original bridge folder.

## 5. Files
- `jaw-gag-actual-model-20261031.gif` (18 sequence positions, 12 stored
  frames, durations summed — see report §3)
- `jaw-gag-actual-model-contact-20261031.png` (2D MBP, 2D AH, 3D 0deg,
  3D 32deg peak, 2D GK, 2D REST)
- `jaw-gag-actual-model-side-drop-20261031.png` (side 0deg vs 32deg + crops)
- `model-alone-front.png` (actual model alone, full body, jaw 0deg)
- `frames_3d/final_f01..f08_*.png` (transparent 3D masters)
- `frames_3d/final_side0.png`, `frames_3d/final_side32.png`
- `frames_seq/seq_actual_00..17.png` (assembled sequence frames)
- `model/cape_jones_rigged.blend`, `model/cj_face_parametric.blend`
- `draft-one/` (Draft One copies + DRAFT-ONE-20261031.md)
- This report: `ACTUAL-MODEL-JAW-GAG-REPORT-20261031.md`

## 6. Status / still owed
- Actual-model jaw gag approval: 0/1. Draft One approval: 0/1 separately.
- No repo push by this task (landing is separate, PR-only, verify on main).
- Side-view chin-drop numeric metric: owed only if a clean head-only
  side render (arm moved out of the head zone) is ordered — that would
  change the model pose, so it was not done silently here.
- Face-rig parametric / mouth-kit integration (cj_face_parametric,
  cj_mouth_kit): not used in this gag; the rig `jaw` bone was sufficient.

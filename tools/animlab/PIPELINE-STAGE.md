# AnimLab pipeline stage — cape-jones

Updated 2026-11-22 on branch `tools/animlab-v0.2.27-wireup` (v0.2.27 binary
LANDED — see `tools/animlab/README.md`). Supersedes the 2026-11-20 staging
note (binaries UNFETCHED, itch 429).

## Where AnimLab slots in

Cape Jones is Adult Swim limited animation (arms-down natural idle, feet planted, scene-by-scene building). This repo holds production/ rigs, toon-boom-linux tooling and Blender rig work. AnimLab slots in as Draw -> Rig/Tween -> Composite -> Finish for limited-animation cuts: vector drawing and Bone/Game Bone rigging for cut-out style movement, node-graph compositing, multi-camera timeline, MP4/PNG export. It sits alongside the existing Toon Boom / Blender rig work as an experiments stage — it does not replace the locked idle/arm rules or the scene-by-scene method, and it does not replace Blender Grease Pencil, which stays the animation CORE.

## Stages AnimLab covers (for this show)

1. **Draw** — vector drawing, pegs.
2. **Rig/Tween** — Bone / Game Bone / Curve / Envelope rigging, tweening.
3. **Composite** — node-graph compositing, multi-camera timeline, audio mixer.
4. **Finish** — MP4 / PNG export.

## What AnimLab does NOT do here

- It does not replace this show's existing core pipeline or its locked rules.
- It does not ship unproofed: AnimLab output goes through the same own-eyes / proof
  gate as every other stage before it reaches the owner.
- No synthesized voice ever — Cape Jones dialogue is the owner's recorded voice only.

## Binary status — LANDED (2026-11-22)

v0.2.27 Linux .deb on Release `production-stack-free-20261120` (mhvnsnt/dream-girl),
79,278,566 B, sha256 `46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf`.
Install: `sudo dpkg -i AnimLab-Linux-v0.2.27-x86_64.deb` (+ `apt-get install -f`
for libwebkit2gtk-4.1-0 / libgtk-3-0), launch `animlab-desktop`.

## Smoke test — PROVEN (placement + export) (2026-11-22, updated; kernels v4–v15)

Smoke test ran on a Kaggle kernel (`marsfmmg/animlab-smoke-test-v0-2-27`,
versions 4–15; local install blocked by a VM disk-write wall — child-process
file writes fail "Operation not permitted"). The bar was a real Cape Jones
board open in AnimLab, vector drawing exercised, a rig/deformer applied, and
a PNG sequence or MP4 exported — each step own-eyes verified. Verdict:
**PROVEN for placement + export. Grease Pencil stays the animation core
until the rig/deformer is fully proven.**

Proven (own-eyes, screenshots/frames in the kernel logs):
- Install + launch: .deb sha-verified, deps install, GUI runs under
  openbox + Xvfb (v0.2.27, 79,278,566 B).
- First-run "Choose Workspace Folder" chooser UNSTUCK — mouse drive works
  (11 reproductions, v5–v15); workspace `.recovery/` created.
- Board `cj-pl-05.png` imported as a scan level (name + Black/White Point,
  Gamma, TONE TO ALPHA controls; v7–v15).
- **Board PLACED on canvas + timeline (v14, reproduced v15): the placement
  mechanism is the scan dialog's footer button "Import sequence"** — found in
  AnimLab's own web-demo frontend bundle + in-app Help ("Place the queued
  images on one timeline layer as consecutive exposures"). Batch Import, then
  click "Import sequence" at (1055,920) — the button right of Cancel. The
  board fills the canvas at 100% zoom and a "Scanned Drawings" layer appears
  on the timeline (Frame 1, Start 1, Stop 60, Length 60). v7–v12 never clicked
  it; v13 clicked the dialog title instead. No HTML5 drag-from-library to
  timeline exists (explains the failed v9/v10/v12 drags); the timeline-cell
  right-click menu ("Import Image Here") never appears on empty cells.
- Vector stroke draws (3.4%–21% screen diffs per drag, v8–v13). In v14/v15
  the stroke is hidden under the opaque placed board (it draws on the default
  Drawing layer underneath) — layer order, not a brush failure.
- Export pipeline WORKS **with board content**: real h264 MP4, 2.5 s
  (60 frames @ 24 fps), 1920×1080, destination honored — v15
  `purple-lot-test.mp4`, 89,712 B, sha256
  `81b079681101c9f56ca15ba941ff65022bf6cc9587d237496866d23d7d3675d9`, frame 1
  IS the board (1920×1080, mean (133,90,182), 1,223 colors; proof in
  `tools/animlab/proof/`). v9–v12 exports were byte-identical 6,869 B blank
  files because nothing was placed yet.
- ANIMATION menu CAN open (5 of 11 attempts; opens at x=135 with a slow
  click) and contains Add Peg; Add Peg was CLICKED four times (v11, v13,
  v14, v15).

Not yet fully proven:
- Rig/deformer (Peg): Add Peg now shows a first observable effect — after the
  click the layer row renames to "Scanned Drawings-P" and gains an expand
  chevron (v14, reproduced byte-identical in v15), which reads as a peg
  attached to the layer. But no peg node/pivot has been seen on the canvas,
  so creation is still only PARTIALLY evidenced, not fully proven.
- Vector stroke ON TOP of a placed board: untested (stroke draws under the
  opaque board layer; the active-layer behavior needs one more check).

Workdir + kernel logs: `~/workspace/_animlab-wireup-20261120/`
(CHECKPOINT.md is the authoritative record); kernel
https://www.kaggle.com/code/marsfmmg/animlab-smoke-test-v0-2-27.

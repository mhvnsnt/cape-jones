# AnimLab pipeline — Cape Jones runbook

AnimLab v0.2.27 is wired into Cape Jones as a rigging/compositing **experiment
candidate**. It is NOT the core: Blender Grease Pencil stays the animation core,
Tahoma2D 1.6.3 stays the proven headless renderer/compositor for the PURPLE LOT
short. AnimLab earns a bigger role only by proving itself on real shots, through
the same own-eyes gate as every other stage.

## What it is

Free animation studio by KevesDev (itch.io). Vector drawing, pegs, rigging (Bone /
Game Bone / Curve / Envelope deformers), node-graph compositing, multi-camera
timeline, audio mixer, 3D primitives, MP4 + PNG-sequence export. $0 freeware, NOT
open-source. Live version v0.2.27 (landed 2026-11-22).

## Install + verify (Linux workstation)

```sh
curl -L -o AnimLab-Linux-v0.2.27-x86_64.deb \
  https://github.com/mhvnsnt/dream-girl/releases/download/production-stack-free-20261120/AnimLab-Linux-v0.2.27-x86_64.deb
sha256sum AnimLab-Linux-v0.2.27-x86_64.deb
# expect: 46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf
sudo dpkg -i AnimLab-Linux-v0.2.27-x86_64.deb
sudo apt-get install -f   # libwebkit2gtk-4.1-0 + libgtk-3-0
animlab-desktop           # headless: xvfb-run -a animlab-desktop
```

Binary: `/usr/bin/animlab-desktop`. Package contents verified: .NET/GTK app,
bundled ffmpeg, NAPS2 scanner component. Full file list + fetch method:
`tools/animlab/README.md`.

## Running a Cape Jones cut through AnimLab

Inputs (real assets in this repo — never placeholders):

- Storyboard keys: `production/2d-parking-lot/boards/cj-pl-01.png` … `cj-pl-07.png`
- Poses: `production/2d-parking-lot/poses/pose-01-idle.png` … `pose-06-nod.png`,
  plus `cape-01-billow.png` / `cape-02-settle.png`
- Locked palette: suit #FFFFFF, cowl #3E1473, skin #E5B28C, cape #000000; white
  eyes default; pupils only for a specific sensation/expression the beat
  requires (see SHOW-BIBLE.md pupil canon + the glove gag: bare hand ONLY
  inside the gag beat, gloves on in every normal/wide shot).

Steps:

1. **Import** the board/pose PNG as a reference layer.
2. **Draw** the vector pass on top (pegged layers, locked palette).
3. **Rig** with Bone / Game Bone deformers — cape-first movement for the lift
   (the cape moves before the arm, per the PURPLE LOT boards).
4. **Tween** on twos at 24fps — drawn changes, NOT holds, NOT stills-with-pans.
5. **Composite** in the node graph: purple-streetlight lighting shift
   (dim sodium orange → broken-streetlight purple), rim light, purple glow.
6. **Export** PNG sequence (or MP4) and hand it to Tahoma2D for the final
   composite, or straight to the `production/2d-parking-lot/` proof gate.

## Gates (non-negotiable)

- Own-eyes verify every AnimLab output against the board/pose reference before
  it reaches the owner: palette exact, arms down / feet planted on idles,
  lighting shift big and visible, hard-cut ending.
- "ah, that's better" stays a GAP for the owner's recorded voice — NO
  synthesized/temp voice ever, in AnimLab or anywhere else.
- Music: check the repo for an existing original track first; otherwise the
  visual cut ships silent and the audio gap is flagged.
- Nothing AnimLab produces replaces a Grease Pencil / Tahoma2D proof until the
  owner eye-judges it frame by frame.

## Smoke-test status — PROVEN (placement + export) (2026-11-22, updated; kernels v4–v15)

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


## Companion tools

See `docs/2D-PARKING-LOT-PRODUCTION.md` (Tahoma2D setup), the free-anim-stack
(Pencil2D, Rigby2D, Olive, Kdenlive), and the companion-tool catalog in
`tools/production-stack-free/` (dream-girl): Synfig, Glaxnimate, Storyboarder
(pulled 2026-11-22 — see the companion wire-up note in this repo's
`tools/animlab/` history). Grease Pencil stays core; every new tool is a
candidate for cleanup / rigging / compositing experiments, never a core
replacement until proven on real shots.
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

## Smoke test — PARTIAL (2026-11-22, final; kernels v4–v12)

Smoke test ran on a Kaggle kernel (`marsfmmg/animlab-smoke-test-v0-2-27`,
versions 4–12; local install blocked by a VM disk-write wall — child-process
file writes fail "Operation not permitted"). The bar was a real Cape Jones
board open in AnimLab, vector drawing exercised, a rig/deformer applied, and
a PNG sequence or MP4 exported — each step own-eyes verified. Verdict:
**PARTIAL — the bar is NOT met. Grease Pencil stays the animation core.**

Proven (own-eyes, screenshots/frames in the kernel logs):
- Install + launch: .deb sha-verified, deps install, GUI runs under
  openbox + Xvfb (v0.2.27, 79,278,566 B).
- First-run "Choose Workspace Folder" chooser UNSTUCK — mouse drive works
  (8 reproductions, v5–v12); workspace `.recovery/` created.
- Board `cj-pl-05.png` imported as a scan level (name + Black/White Point,
  Gamma, TONE TO ALPHA controls; v7–v12).
- Vector stroke draws (3.4%–21% screen diffs per drag).
- Export pipeline WORKS: real h264 MP4, 2.5 s (60 frames @ 24 fps),
  1920×1080, destination honored (v9, v10, v11, v12 — four byte-identical
  6,869 B files, `purple-lot-test.mp4`).
- ANIMATION menu CAN open (2 of 8 attempts; opens at x=135 with a slow
  click) and contains Add Peg; Add Peg was CLICKED once (v11).

Not proven (exact failures):
- Board placed on canvas/timeline: NEVER. Tried — canvas double-click
  (0.3% change), canvas drag (0.0%), timeline drag to (250,960) (moved the
  level label only), timeline-track drag to (300,985) (3.6% view shift),
  right-click (no context menu — 0.0% in v11, 3.6% in v12), 'insert'
  timeline control click (0.0%). Every export's frame 1 is pure white —
  the timeline is empty.
- Rig/deformer (Peg): Add Peg was clicked once but no peg node/pivot was
  ever observed after the click; creation is unconfirmed.
- The MP4 export's CONTENT is blank white in all four runs, because nothing
  was ever placed on the timeline.

Workdir + kernel logs: `~/workspace/_animlab-wireup-20261120/`
(CHECKPOINT.md is the authoritative record); kernel
https://www.kaggle.com/code/marsfmmg/animlab-smoke-test-v0-2-27.
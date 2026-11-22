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

## Smoke test — RUNNING (2026-11-22)

Local install is blocked by a VM disk-write wall (child-process file writes fail
"Operation not permitted" since ~13:07 EST); the install + launch smoke test runs
on a Kaggle kernel instead (slug `marsfmmg/animlab-smoke-test`). The stage is
docs + verified binary until the smoke verdict lands — then this file records
exactly what works on a real Cape Jones asset.
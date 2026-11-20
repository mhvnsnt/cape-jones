# AnimLab pipeline stage — cape-jones

Staged 2026-11-20 on branch `tools/animlab-wireup-20261120` (AnimLab wire-up, binaries UNFETCHED — see
`tools/animlab/README.md`).

## Where AnimLab slots in

Cape Jones is Adult Swim limited animation (arms-down natural idle, feet planted, scene-by-scene building). This repo holds production/ rigs, toon-boom-linux tooling and Blender rig work. AnimLab slots in as Draw -> Rig/Tween -> Composite -> Finish for limited-animation cuts: vector drawing and Bone/Game Bone rigging for cut-out style movement, node-graph compositing, multi-camera timeline, MP4/PNG export. It sits alongside the existing Toon Boom / Blender rig work as an experiments stage — it does not replace the locked idle/arm rules or the scene-by-scene method.

## Stages AnimLab covers (for this show)

1. **Draw** — vector drawing, pegs.
2. **Rig/Tween** — Bone / Game Bone / Curve / Envelope rigging, tweening.
3. **Composite** — node-graph compositing, multi-camera timeline, audio mixer.
4. **Finish** — MP4 / PNG export.

## What AnimLab does NOT do here

- It does not replace this show's existing core pipeline or its locked rules.
- It does not ship unproofed: AnimLab output goes through the same own-eyes / proof
  gate as every other stage before it reaches the owner.
- Binaries are UNFETCHED as of 2026-11-20 (itch 429). Until `fetch-animlab.sh` lands
  them on Release `animlab-v0.2.26`, this stage is docs + fetch route only.

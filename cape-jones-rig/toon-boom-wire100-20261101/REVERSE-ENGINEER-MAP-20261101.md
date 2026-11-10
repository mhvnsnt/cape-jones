# Reverse-Engineer While Using It — Harmony Feature → Our Pipeline
Method: use the owned app, observe behaviour, document the interface,
write an interoperable bridge. No bypass, no key extraction, no code copy.
Each row: what Harmony does, what it maps to in our work, what to test
first after activation, and what it replaces.

| # | Harmony feature | Maps to our pipeline | Test first after activation | Replaces |
|---|---|---|---|---|
| 1 | Node View (node graph, pegs, drawings, composites) | Our z-order / DEFS-stable layer order; cape z0 … hands z13 | Import sitting pack, check node order = z order, no reversed tie at z=4 | PIL layer-paste order guesses |
| 2 | Peg (position / rotation / scale / pivot) | Our pivot_xy = x + ox·w, y + oy·h; top-centre (0.5,0) for torso/arms/thighs/shins, (0.39,0.11)/(0.63,0.11) for forearms, centre for knees/caps/hands | Set a peg pivot, rotate 15°, check bicep is NOT square-cropped (large-canvas rotate lesson) | In-place PIL rotate that clipped 25.7% of Arm 2 bicep |
| 3 | Drawing substitution (swap drawings on a layer) | Our hands (open / fist), mouths (MBP/AH/GK/GAP/REST), eyes (Robin library, 25/25), hands 1–7 flips | Swap handL open↔fist on one key, check wrist stays attached | Layering a spare hand over a fused hand (the double-hand bug) |
| 4 | Deformer: Bone / Game Bone / Curve / Envelope | Our FK chains: shoulder→elbow→wrist, hip→knee→ankle; knee-feet rule; joint locks together, not frozen in space | Bone chain on arm, bend elbow, check forearm follows, hand stays on wrist | Manual per-frame paste offsets |
| 5 | Kinematic Output node | Rig a hand under a deformation chain without deforming the hand itself | Hand under arm deformer, check hand shape stays whole | Hand deforming with the forearm |
| 6 | Master Controller (widgets → pegs / deformers) | Our pose dials: sitting pose, lean-forward, shimmy, Ghoul Shuffle keys; envelope deformers are reversible, bone chains with "Apply Parent Transformation" are not (docs) | One widget driving head-tilt + torso-bob for sit-idle | Re-typing numbers per frame |
| 7 | Onion skin + Timeline / Xsheet (.xsheet) | Our inbetweening rule: real intermediate rig poses, keys/breakdowns/inbetweens, timing chart; crossfade is NOT inbetweening | 3-key sit-idle, check inbetweens are rig poses, not blends | PIL crossfade / whole-picture blend |
| 8 | Camera + 3D space / multiplane | Our multiplane, room scale, ground gate (Gy=1475 in widget, 1180 in room shots, 1000 in ground-gate) | Camera move over canonical room, check feet stay on ground line | Flat PIL composites with no camera |
| 9 | Effects / compositing (node-based, Premium) | Our L0–L5 lighting, rim-colour rule (±20° hue), dual-light, shadows, god rays, crystal, dream colourways | Apply rim + bleed as separate effect layers, never recolour base art | PIL VFX as production (draft only) |
| 10 | Lip-sync / exposure sheet, Storyboard Pro → Harmony | Our lip-sync chart 14/14, mouth-jaw movement, PAH GO, temp songs 107 BPM, Space Ghost Phases 0–7 (picture lock, then dialogue fill) | Import 107 BPM temp, map MBP/AH/GK/GAP to exposure, check jaw drops (MBP 0, AH 16, GK 8, GAP 10) | Manual mouth paste per frame |
| 11 | Batch render / Control Center scripting | Our wire_tv_100.py runner, landing batches, render queue | Batch-render sit-idle + shimmy, check -14 LUFS audio pass separately | One-off ffmpeg calls with no queue |
| 12 | Templates (.tpl) + Libraries | Our rig registry RIG-00 … RIG-06, locked versions, checkpoint rule | Save sitting rig as .tpl, open in a new scene, check it is identical | Rebuilding a rig from scratch per scene |

## Reverse-engineering log (to fill in-app, after activation)
For each feature above, record in-app: exact menu path, exact node
attribute name (via Show Attribute Information), what value changed,
what rendered, and what broke. That log IS the reverse-engineering
output — behaviour, not binaries. Do not paste license, key, or
proprietary code into it.

## What it can help us with, concretely
- TV production: one app for rig → animate → composite → export, instead
  of 20+ PIL builders each re-implementing rotation, layering and timing.
- Sitting show: the canonical room + sitting rig + dance moves (Ghoul
  Shuffle V1/V2/V3, Shimmy Number One) become Harmony scenes, not PNGs.
- QC: onion skin, timing chart and camera make the defects we kept
  finding (floating feet, cropped biceps, double hands, arm-over-face
  layering) visible before render, not after.
- 2D/3D bridge: Premium's hybrid 2D-3D lets the 3D jaw gag / actual-model
  work live in the same scene family, without merging the 2D and 3D
  projects (locked separation rule stands).

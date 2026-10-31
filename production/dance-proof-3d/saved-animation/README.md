# Saved animation — Cape Jones 3D dance v3 (the literal animation)

Saved 2026-10-31 on the owner's order: keep the actual dance animation, not
just the rendered video, so it can be reopened, built on, and reused later.
This is the v3 dance — the version of record ("3D v3"). It stays frozen here;
v4 is a separate new build and never overwrites this.

Source: PR #272 (branch `feature/cj-dance-proof-3d-v3-20261030`), built by
`production/dance-proof-3d/build_dance.py`. Rendered video:
`cj-dance-proof-3d-v3.mp4` (75.79 s, English v2 song mix).

## Files

| File | What it is |
|---|---|
| `cj-dance-3d-v3.blend` | The full v3 scene exactly as rendered, with the dance inside it (see below). 20,423,101 bytes. |
| `cj-dance-3d-v3.bvh` | Portable motion export of the dance, frames 1–1824 at 24 fps. Retarget onto any rig. 9,297,190 bytes. |

## What's inside the .blend

- **`CapeJones_Rig`** (88 bones, BlenRig-style FK/IK rig) carries the original
  dance action, renamed **`CJ_Dance_3D_V3`** (63 fcurves). It keys 20 control
  bones: pelvis, spine_2, chest, neck_2, head, the FK arm chains
  (upperarm/forearm/hand, L+R), the FK leg chains (thigh/shin/foot, L+R) and
  the cape bones cape_1–3. The deform bones follow through the rig's
  Copy-Transforms/IK constraint stack (28 constraints), exactly as rendered.
- **`CapeJones_Rig_BAKED`** (collection `SAVED_ANIMATION_BAKED`) carries
  **`CJ_Dance_3D_V3_BAKED`** (792 fcurves): the same dance visual-baked onto
  all 88 bones with constraints cleared, so the motion plays back with no rig
  logic — grab this one to build on. Verified after saving: baked poses match
  the original rig's poses (deform-bone world matrices across sample frames,
  including a post-save reopen spot-check at frame 900).

## Timeline / loop structure

- 1,824 frames at 24 fps on the timeline; the final video trims to 1,819
  frames = the full 75.79 s song.
- The dance itself is a 48-frame step-touch loop, tiled underneath the whole
  song (8 loops per 384-frame section).
- The five lighting sections are **render-side world state**, not part of the
  character's motion: 1–384 day · 385–768 LED magenta · 769–1152 LED cyan ·
  1153–1536 night · 1537–1819 day return. Sections 2 and 4 were mirrored
  (hflip) at assembly time, on loop boundaries — an edit-side flip, also not
  part of the dance action. **The dance action is the character motion.**

## Reuse

- Open the .blend and use `CapeJones_Rig_BAKED` / `CJ_Dance_3D_V3_BAKED` to
  extend or re-stage the dance with zero constraint setup, or use
  `CapeJones_Rig` / `CJ_Dance_3D_V3` to adjust the original FK keys.
- Import `cj-dance-3d-v3.bvh` in any tool to retarget the raw motion.
- Known character (owner's verdict on v3): the motion is FK-keyed, so it is
  stiff outside the forearms — that is what the v4 auto-IK build answers. This
  save preserves v3 exactly as it is, stiffness included; it is the record.

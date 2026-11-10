# Synfig Studio — Vector Tweening & Bone Rigs (Auto-Inbetweening)

**Pinned version:** 1.5.5 (latest dev, released 2026-03-16, verified 2026-10-19) ·
stable fallback 1.4.5
**License:** GPLv2+ (open source, free)
**Upstream:** https://www.synfig.org/ · https://github.com/synfig/synfig

## What it is

Free vector 2D animation with **automatic tweening** — define keyframes, it generates
the in-betweens. 50+ layer types (gradients, distortions, filters), bone/skeleton
system for cut-out rigs, shape morphing, inverse kinematics. This is the tool that
answers the "interpolation" ask **at the authoring level**: instead of interpolating
rendered video frames after the fact (RIFE), Synfig interpolates the vector artwork
itself between poses.

## Why this tool (pipeline role)

Two kinds of interpolation in this pipeline — do not confuse them:

| | Synfig (authoring) | RIFE (post) |
|---|---|---|
| Input | Vector keyframes you pose | Rendered video frames |
| Output | Smooth vector motion, resolution-independent | Smooth video, fixed resolution |
| Use when | Building new animated shots from drawings/rigs | Smoothing existing footage (Viggle clips, expressions) |

For new Cape Jones animation built from our own drawings: rig in Synfig, pose keys,
let the tweener do the in-betweens. For existing choppy footage: RIFE.

## Linux install

```bash
# AppImage from synfig.org (recommended)
chmod +x SynfigStudio-*.AppImage
./SynfigStudio-*.AppImage
# or distro package: apt install synfigstudio  (may lag upstream — prefer AppImage for 1.5.5)
```

## Bone-rig + tween workflow

1. **Build** — vector character parts as layers; attach Skeleton layers, link bones.
2. **Pose** — set keyframes on the timeline for extremes (contact, passing, extremes).
3. **Tween** — Synfig interpolates automatically; adjust easing per-waypoint
   (clamped/linear/ease) for cartoon snap vs smooth.
4. **Render** — export PNG sequence or video; hand to OpenToonz/Blender for compositing.

## Caveats (from reviews — plan around them)

- Stability issues on complex projects: keep scenes modular, save incrementally.
- Confusing UI for beginners: the README + a short eval lane before production use.
- Thinner docs than commercial tools: budget learning time.

## Evaluation lane (before production use)

Prove it on one Cape Jones shot: rig the character, pose 3 keys, render the tween,
compare against hand-drawn frames. If the tween quality holds, it becomes the
default for new 2D shots. Document the eval result here.

## License

GPLv2+. Repo integration is legal — document version pin on upgrade.

# crt-tv — procedural CRT screen shader (in-house)

Our own `crt_tv.py` — a procedural CRT *look* stack for the living room's
`crt_tv`, built as node group `CJ_CRT_Screen`. No add-on, no compositing pass:
native Cycles nodes, so it renders on the Kaggle/Colab lanes as-is.

## How real studios do TV screens

They don't simulate a CRT — they shade an emission plane with the video
content plus a CRT look stack: **scanlines + phosphor mask + rolling refresh
band + flicker + vignette**. (Paid Blender add-ons like CRT Monitor Generator
and Phosphor do exactly this in a compositor wrapper; we built the shader
directly so it's free and dependency-free.)

## The stack

| Stage | Nodes | Control |
|---|---|---|
| Content | Image Texture (image or **movie**) inside the group | `crt_tv.set_content(path)` |
| Scanlines | Wave Texture bands (Y), default **240 lines** | `set_scanline_count(n)` |
| Aperture grille | Brick Texture → vertical RGB stripes | fixed |
| Rolling refresh band | Y + `crt_refresh` → fract → narrow bright band | animate `crt_refresh` 0→1 |
| Flicker | `crt_flicker` 0..1 scales emission | the flicker gag drives this |
| Power | `crt_power` 0/1 | off = dark glass |
| Vignette | radial gradient | fixed |

## Use

```python
import crt_tv
crt_tv.apply_to_screen("crt_screen")          # assigns CJ_CRT_Mat
crt_tv.set_content("/path/to/static.mp4")     # image or movie
crt_tv.set_scanline_count(240)
```

Keyframe the group inputs on the material's group node (`crt_power`,
`crt_brightness`, `crt_flicker`, `crt_refresh`) for the gag — e.g. the remote
press sets `crt_flicker=1` for 6 frames then back to 0.

**Verified 2026-10-17 by this lane (real run, Blender 4.5.3 LTS):**
group builds with all 5 inputs + Shader output, assigns to a mesh,
32px Cycles render compiles and writes PNG.

For the `scene/tv-functional-20261017` lane: call `apply_to_screen("crt_screen")`
on the canon blend, then `set_content()` with the episode/static clip.

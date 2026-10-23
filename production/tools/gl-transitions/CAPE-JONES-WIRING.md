# gl-transitions — 125 GPU transition shaders for show editing (wiring doc)

**Upstream:** https://github.com/gl-transitions/gl-transitions (MIT;
123 MIT + 1 BSD-2-Clause + 1 BSD-3-Clause across the 125 shaders — all
permissive, commercial use OK).
**Vendored:** `transitions/` (125 `.glsl` shaders), `LICENSE`, `README.md`
(upstream). Dev tooling (`crates/`, `packages/`, `examples/`, `scripts/`,
`skills/`) NOT pulled — the shaders are the asset.
**New here:** `render_transition.py` — headless renderer: Playwright +
Chromium (SwiftShader WebGL) renders each frame, ffmpeg encodes H.264 MP4.
**License:** MIT — free, commercial use allowed.

## Why

The show pipeline (EP01/EP02 finishing, bump cards, promos) had no
transition system — cuts were hard cuts or hand-built fades. This is the
industry-standard open transition collection (the same shaders behind dozens
of editors), rendered deterministically headless. Pick any of 125
transitions (fade, wipes, burns, 3D flips, glitch, kaleidoscope...) and bake
it between two clips/stills with one command. No hand-tooling, no NLE
needed for transition work.

## Install

```bash
python3 production/tools/gl-transitions/render_transition.py --help
python3 production/tools/gl-transitions/render_transition.py --list   # 125 names
```

Requires: `pip install playwright` + `playwright install chromium`,
ffmpeg with libx264. (Both already on the VM.)

## Use

```bash
# Basic: 2s crossfade between two stills -> MP4
python3 production/tools/gl-transitions/render_transition.py \
    --from scene_a.png --to scene_b.png --transition fade \
    --duration 2 --fps 24 --out transition.mp4

# A fancy one with default shader params
python3 production/tools/gl-transitions/render_transition.py \
    --from scene_a.png --to scene_b.png --transition undulatingBurnOut \
    --width 1920 --height 1080 --out burn.mp4

# Override a shader uniform (defaults come from the .glsl header comments)
python3 production/tools/gl-transitions/render_transition.py \
    --from a.png --to b.png --transition directionalwipe \
    --param smoothness=0.2 --out wipe.mp4

# Keep the PNG frames too
python3 production/tools/gl-transitions/render_transition.py \
    --from a.png --to b.png --transition BookFlip \
    --keep-frames ./frames --out flip.mp4
```

Transition-to-transition chains (A->B->C): render each leg, concat with
ffmpeg (`-f concat`). For clip-to-clip (not still-to-still): extract the
last frame of clip A and first frame of clip B, render the transition
between them, then concat `A + transition + B`.

## Verified

- `python3 -m py_compile` clean; `--help` and `--list` (125) work.
- Rendered 4 transitions headless and viewed frames with own eyes:
  `fade` (endpoints = exact input images, mid-frame = true crossfade),
  `undulatingBurnOut` (burnt char edge eating across, backtick-in-comment
  GLSL compiled fine), `displacement` + `luma` (extra-sampler path —
  smooth generated displacement/luma fields, not white noise).
- Outputs probed: H.264, yuv420p, +faststart, correct frame counts.
- Uniform parser covers every declaration style in the collection
  (float/int/bool/vec2/vec3/vec4 + `// = default` comments); the 2
  transitions needing extra samplers (`displacementMap`, `luma`) get a
  generated smooth noise texture.

## Cape Jones uses

- Episode finishing: transitions between scenes/stills in EP01/EP02,
  LOTI, Goodville, TRIPPEDD cuts.
- Bump cards / promos: `BookFlip`, `circleopen`, burns for card reveals.
- Menu/UI: short transitions for select-screen and Creation Suite
  panel changes (render once, ship the MP4/WebM).

## Limits

- Still-to-still (or still-frame-to-still-frame). Full clip warping
  (moving video through the shader) is not implemented — extract
  boundary frames for clip work.
- Headless SwiftShader render: ~1-2s/frame at 640x360, slower at 1080p.
  Fine for transitions (seconds long), not for full-episode rendering.
- Audio is not touched — mux your audio track with ffmpeg after.
- Shader compile happens in Chromium; a malformed custom .glsl fails
  loudly with the compiler log (no silent black frames).

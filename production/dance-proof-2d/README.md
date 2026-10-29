# Cape Jones Dance Proof — 2D version (v1)

The owner's example scene from `docs/SHOW-BIBLE-SEED.md`, built as the 2D lane
of the 2D-vs-3D race (2026-10-29): Cape Jones outside, doing the weird
Charlie Brown dance in one spot — the same simple loop, facing one way then
the other — while the lighting cycles daytime → LED colors → natural dusk →
night → back to day, and the environment changes around him. Tamagotchi-style
chiptune plays. The world changes; the dance does not.

## What it is
- `cj-dance-proof-2d-v1.mp4` — 21 s, 1920×1080, 24 fps timeline.
- 7 hard-cut sections of 3 s: DAY (yard) → LED MAGENTA (yard) → LED CYAN
  (mesa) → LED GREEN (mesa) → DUSK (evening yard, flipped) → NIGHT (evening
  yard, flipped) → DAY again (yard, flipped).
- Contact sheet: `cj-dance-proof-2d-sheet.png` (one frame per lighting state).

## How it was built (production model, PR #265)
- **Character = the show's own stock, extracted, never redrawn.**
  `characters/sheets/01-tpose-turnaround.jpg` was roto-cut (HSV candidate
  flood from the border; the white suit survives because its black outlines
  wall it off) and segmented into a 7-layer cutout puppet: cape, legs L/R,
  torso, arms L/R, head. No chroma key.
- **One dance loop of 4 drawings** (lean-left / crouch / lean-right / crouch-B),
  each held 3 frames (animation on threes), built by rotating the puppet
  layers at shoulder/hip/neck pivots. Sections 5–7 reuse the same drawings
  mirrored — facing the other way costs zero new drawings.
- **Lighting = grades, not new art.** Each section is a color grade
  (multiply + tint) over the same plates, the 2D equivalent of the LED gag
  engine: day / magenta / cyan / green / dusk / night. Grades are linear, so
  layers were pre-graded and composited.
- **Backgrounds** are three flat plates (yard + picket fence, mesa, evening
  yard) with matching foreground silhouette strips, swapped between sections.
  The Space Ghost gigaleak background EPS files could not be rendered in this
  lane (no working EPS rasterizer on the box), so the plates are simple flat
  scene dressing in that style; the character art is 100% repo stock.
- **Music**: the Tamagotchi-style loop pulled from the Mochiichao repo music
  stash by the music lane (`tamagotchi-loop-from-mochi-repo.mp3`, muxed in).
  An alternate in-lane synth chiptune is kept as `chiptune-alt.wav`.

## Scripts
- `build_dance.py` — extraction + puppet segmentation + the 4 dance drawings.
- `stage2_render.py` — plates, grades, sections, frame render, contact sheet.
- `make_music.py` — the alternate chiptune synthesizer (numpy).

## Known limits (honest)
- Cutout-puppet movement: pieces rotate at joints; there are no in-betweens
  and no drawn pose swaps beyond the 4 loop drawings. That is the Adult Swim
  limited model working as designed, but arm swings pass through the T-pose
  line on two drawings.
- The mesa plate is very flat. A real SGC2C background (EPS) pass would lift
  sections 3–4 once an EPS rasterizer is wired.

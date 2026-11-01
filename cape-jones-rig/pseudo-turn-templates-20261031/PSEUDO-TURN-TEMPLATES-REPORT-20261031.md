# PSEUDO-TURN TEMPLATE PACK — 2026-10-31

Approval 0/1 for the pack. No repo push. No existing file overwritten.
Builder: build_templates.py (parameterised, re-runnable on any pose via
snap.figure angle sets). Masters: transparent RGBA PNGs in frames/<name>/.
GIF/MP4 are view copies on a neutral grey canvas sized as the UNION of
that template's frames, feet-anchored — that is NOT a crop window, no
frame is clipped. No-clip gate: 7/7 templates, 0 alpha pixels on any
union-canvas edge.

## What the original was (keep straight)
Original: depth-25d-blockers-broken-20261031/experimental-pseudo-turn-20261031.gif,
13 frames @12fps, width squash 1.0 -> 0.62 -> 1.0 (sine), head tilt to -10,
arm layer-order flip at t>=0.5, angles APOSE -> TURNED. It is NOT a true
side view. No true side torso/head piece exists; a true hand-drawn turn
master is still owed separately and is NOT claimed by anything here.

## Templates (all 12fps)
| Template | Kind | Frames | Parameters |
|---|---|---|---|
| pseudo-turn | BASE TEMPLATE (cheat, not a true turn) | 13 | squash sine 1.0->0.62->1.0, head 0->-10, layer flip at midpoint, angles APOSE->TURNED, smoothstep easing. Ends at TURNED pose, full width — NOT "front again" (an early contact label said that; corrected). |
| stretch-power | POWER | 13 | height 1.0->1.40->1.0, width 1.0->0.90->1.0, feet-anchored |
| thin-power | POWER | 13 | width 1.0->0.45->1.0 (thinner than pseudo midpoint), height 1.0->1.05->1.0 |
| invisible-power | POWER | 17 | body width 1.0->0.02 over f00-f07, outline-only hold f08-f11, return f12-f16. Outline = FROZEN unsquashed silhouette, hard ring (180,245,255) + one soft halo (0,200,255) — frozen on purpose, or it would vanish with the body. Hold outline pulses 100%/94% so GIF writers keep all 17 frames (an early GIF dropped 3 identical hold frames to 14; fixed, MP4 was always 17). Measured: visible body alpha 337,389 px, outline-only hold 104,787 px. |
| cheat-turn-a-depth-dark | CHEAT | 13 | pseudo squash + layer flip + scale 1.0->0.80 at midpoint + far-side darken to 0.75 |
| cheat-turn-b-bend-mirror | CHEAT | 13 | pseudo squash + height-varying bend warp (lattice/plastic-equivalent, max 30px) + horizontal mirror at t>=0.5. Ends MIRRORED front, labelled as such — a mirror is not a back view. |
| sheet-animated-turn-attempt | SHEET ATTEMPT, NOT a true turn | 15 | Keys are real rig poses built from sheet pieces (snap.figure, no new art drawn): front -> turned -> mirrored -> front, 5 frames per key pair, squash at midpoints. Gaps named: no side torso, no side head, no back piece — the midpoint is squash, not a side drawing. |

## Industry-standard methods wired (7)
1. Disney 12 principles squash & stretch — STRETCH/THIN/PSEUDO parameters.
2. Toon Boom Harmony deformers (bone + curve) — parameterised squash/stretch
   as the deformer-equivalent, method proxy only; no Harmony run (trial is
   blocked at the card step in the parent chat, not claimed).
3. Spine mesh warp — horizontal squash with vertical compensation, method
   proxy via PIL resize, not a Spine run.
4. Moho bone warp — bone-angle interpolation via snap.figure + layer flip,
   method proxy, not a Moho run.
5. Blender lattice — bend warp in CHEAT-TURN-B, a real warp implementation
   (height-varying shift), lattice-equivalent in PIL, not a Blender run.
6. OpenToonz/Tahoma2D plastic tool — same mesh-deformation idea as (5),
   method proxy, not an OpenToonz run.
7. Model-sheet turn construction — SHEET-ANIMATED key order
   front -> twist -> mirrored -> front, with a turn chart in the builder;
   honest about the missing side/back drawings.

Real runs: snap.figure rig builds, PIL transforms, ffmpeg encodes, gate
measurements. Proxies are labelled proxies above; no vendor tool is
claimed to have run when it did not.

## Still owed
- Pack approval 0/1.
- True side torso/head piece 0/1, true hand-drawn turn master 0/1.
- Per-pose application: templates are parameterised for any snap angle
  set, but only the apose base was rendered in this pack.
- No repo push made; landing is the parent's landing workstream's job.

## Correction logged (Mars, 2026-10-31 19:48 CDT)
- PSEUDO-TURN base template is logged as THREE-QUARTER PSEUDO TURN, not just pseudo-turn: he turns three quarters and then turns back. It is more than an actual turn in that sense — a 3/4 out-and-back cheat, not a full turn, not a true side view. This label applies to the base template; the other templates (stretch, thin, invisible, cheat A/B, sheet attempt) keep their own labels.

# EXPERIMENTAL — 3D camera depth in 2D + breaking the "not applicable / blocker" list

Mars, 2026-10-31 ~18:42 CDT: "we can find ways to use 3D camera depth in a
2D way… and any of that other stuff that you said is unusable or blockers
we can find experimental or new ways to use them… wire up any industry
standard stuff 100%." Priority update ~18:44 CDT: Grease Pencil 100% is the
priority deliverable; 2D focus until Mars says otherwise; 2.5D/3D only
where it makes the 2D feel perspective-bending; 3D-side tools documented
separately, not turning current Cape work into a 3D project.
All outputs in this folder. No repo push in this task. Mars approval of
each new system: 0/1 each. Every method here is labelled EXPERIMENTAL
unless it says otherwise — experimental means it works in this test, it
does not mean production-proven.

## 1. 3D depth in 2D — BROKEN (experimental, working tests)
Industry methods pulled: Disney multiplane camera (1937, layers at
different distances moving at different rates), parallax, depth-by-scale,
atmospheric perspective (far = blurred/darker), Z-order as a depth axis,
After Effects 3D camera on 2D layers, Spine/Moho mesh-warp pseudo-turn.

### (a) Multiplane camera move — WORKING, viewed
`experimental-multiplane-camera-20261031.gif/.mp4` (24 frames @12fps) +
contact sheet. Layers: far rooftop bg parallax 0.3 (blurred 1.2, -40px
total), Cape parallax 1.0 (-120px), foreground railing bars parallax 1.8
(-216px). The moon/bg moves slowest, the bars fastest — the depth read
is real, not faked by scaling alone.
Honest limit: the foreground bars are heavy (55px wide, alpha 210, every
180px) and occlude Cape for stretches. They are a TEST foreground, not a
final shot foreground — a final needs thinner/sparser foreground elements.

### (b) Depth-by-scale — WORKING, viewed (after a framing fix)
`experimental-depth-by-scale-20261031.gif/.mp4` + contact sheet + spec
`experimental-depth-spec-20261031.json`. Z table: Z=-2 scale 0.60
parallax 0.3 blur 2.0 (far); Z=-1 0.80 / 0.6 / 1.0 (mid-far); Z=0 1.00 /
1.0 / 0 (hero plane); Z=1 1.25 / 1.4 / 0 (near); Z=2 1.50 / 1.8 / 0
(closest). Rule: scale = 1.0 + 0.25*Z; feet stay on the ground line;
scaling grows upward from the feet, never from the centre.
Defect caught and fixed in this pass: the first Z-table render used a
750px-tall frame, so Z=1/Z=2 cropped Cape's head off. Re-rendered at
full 1500px height with feet at y=1400 — all five Z planes now read
clean. The crop was a framing bug in the test, not a depth rule.

### (c) Pseudo-3D turn — WORKING as an approximation, labelled as such
`experimental-pseudo-turn-20261031.gif/.mp4` (13 frames) + contact.
Method: snap_figure angle interpolation apose -> turned pose, width
squash 1.0 -> 0.62 at midpoint -> 1.0, head tilt to -10°, and a layer-order
flip at the midpoint (before: L arm chest-pass in front; after: R arm
chest-pass in front). Honest limit: this is NOT a true side view — no
true side torso/head piece exists, so the turn reads as a squash +
counter-pose, not a profile. It proves the layer-flip-at-midpoint rule
works; a true turn still needs a side piece (same owed item as the
dance twist).

## 2. Grease Pencil — BROKEN, priority deliverable, WORKING rig
Was: mapping table only. Now: a real Blender 5.2.3 GP rig.
- File: `cape-gp-rig-experimental-20261031.blend`, builders
  `trace_gp_frames.py` + `build_gp_blend.py`, stroke data `gp_frames.json`.
- 10 layers, front to back: FaceSnapArm, Head, CowlUpperArm, Neck,
  ChestSnapArm, Torso, Collar, NormalArm, Legs, CapeBack; one colour-coded
  material per layer; `use_lights=False` for flat 2D colour.
- Every stroke is a traced outline of an existing v7c piece (cv2 largest
  external contour, approxPolyDP, max 140 points), placed by the v7c
  joint/anchor/rotation math. No new art.
- Rendered, viewed: GP motion apose -> mid -> true-final -> hold, 4
  frames (`gp-motion-experimental-20261031.gif/.mp4`, raw frames
  `gp-motion-0001..0004.png`); GP JoJo 03 face-snap frame 10
  (`gp-jojo03-face-snap-experimental-20261031.png`, R arm in FaceSnapArm
  above Head); GP true-final vs original before/after
  (`gp-true-final-before-after-experimental-20261031.png`).
- Pipeline use: see `EXPERIMENTAL-GP-PIPELINE-USE-20261031.md` — GP is
  the layer-order proof + Blender-motion path; PIL/v7c remains the
  DEFAULT for approved poses and clean plates. GP is NOT a replacement
  for any approved file (approved true-final untouched).
- GP API note (saves a wasted run): `gpencil_add` does NOT exist in
  Blender 5.2 — build via `bpy.data.grease_pencils.new()` +
  `drawing.add_strokes([sizes])` + `points[].position` / `radius`.
  Eevee under xvfb-run; bare headless aborts on missing libEGL.
- Honest GP limits: outlines ONLY (no fills, no interior linework, no
  colour fills); fixed stroke radius 0.035; cape outline dominates the
  line drawing because Cape_Back_Main's contour is the whole cape;
  rendering is slow on this VM (~60-90s/frame in probes) — GPU is the
  free route for longer GP sequences. Filled GP art is the next pass.

## 3. Rendered-only clips: angle configs — BROKEN for 3 poses, rest standing
Recovered configs: `angle-configs-recovered-20261031.json` + gate CSV
`angle-configs-gate-20261031.csv`. Gate results (check_pose_snap.py):
- Fighting pose: PASS, NO SNAP both sides (measured-estimate ±15°:
  uppers -65/+65, lowers 140/-140).
- True-final flex: PASS, NO SNAP both sides (DOCUMENTED angles:
  uppers -85/+85, lowers 145/-145, legs -22/22, lower 10/-10).
- Punch impact: PASS (L COWL-CANDIDATE with eye-check recorded —
  eye-check says FALSE POSITIVE, upper out to the side, not cut;
  R CHEST-SNAP warning only, forearm already in front).
  Measured-estimates ±15° (uppers -110/20, lowers 10/-110).
  Punch render carries red ARM/LEG circles — DEBUG labels only, never
  part of a clean scene.
- Standing gap: other clips-v7c families (walk/dance/flying/jump) still
  have no configs on disk and remain eye-checked only. Do NOT claim the
  whole clips set is gated.

## 4. Auto lip-sync layer switching — BROKEN as a layer system (not as limb stacking)
The wire-100 report was right that lip-sync switching does not change
limb stacking — but it DOES apply as a layer system, and that is what is
wired here: `experimental-lipsync-layer-20261031.gif/.mp4` + contact,
timeline MBP -> AH -> GK -> OH ("PAH GO" test phrase, visemes v2 heads).
Rule proven: the mouth patch lives INSIDE the head layer (visemes v2
heads are full-head images with the mouth patched in), so the mouth
never rises above the head/cowl and the cowl never covers the mouth.
The switching is driven by the phoneme timeline, one viseme head per
phoneme, held 2 frames each in the test. Full dialogue sync to a real
recording is still owed (recorded audio is 0%).

## 5. Cowl-gate automation — NOT BROKEN; two signals tried, both measured, neither deploys
This is the one former blocker that stays standing, with evidence, not
with a shrug. Eye-check remains the final vote.
- Signal v2a (collar-band diff, normal vs cowl-upper renders):
  `cowl_gate_v2.py` + results CSV. Ratios vs apose baseline (10,221px):
  JoJo 02 false positive 1.01, Ginyu 03 true 0.67, jump true 0.74,
  Ginyu 01 true 0.87, JoJo 03 control 0.85. True notches score LOWER
  than the false positive — the signal does not separate at all.
- Signal v2b (collar splits the bicep into components):
  `cowl_gate_v2b.py` + results CSV. Bite fractions (upper area eaten by
  collar): apose baseline 0.276/0.288, JoJo 02 false positive 0.190,
  true notches 0.208-0.249, normal Ginyu 01 R 0.246. It separates true
  vs JoJo 02 (4/4 above 0.20 vs 0/1) but ALSO flags baseline apose and
  normal shoulders — so as a standalone auto-decision it would flag
  every normal shoulder. Component counts are noise (1-108px specks
  from piece alpha fringe).
- Verdict: neither signal is deployable as an automatic gate. The
  working system remains: existing gate (elbow >50px above shoulder +
  upper-vs-collar >1000 = candidate) + eye-check as final vote, plus
  the GP layer stack as a visual check. What would break this: a
  learned classifier trained on labelled notch vs attachment examples
  (the top-5 labelling workstream's vision model is the candidate for
  that — not built here, not claimed).

## 6. Scope: 2D focus + 3D-side-ready tools
Per Mars ~18:44 CDT: 2D focus until he says otherwise; 2.5D/3D only
where it makes the 2D feel perspective-bending (the multiplane, Z-scale,
and pseudo-turn tests above are exactly that — 2D tests, not a 3D
project). 3D-side tools are documented separately in
`EXPERIMENTAL-3D-SIDE-READY-TOOLS-20261031.md` (Blender 5.2.3, GP in 3D
space, real camera multiplane, Z + DOF, Spine/Moho warp, .abc caches,
Cycles volumetrics). No 3D Cape model was built in this pass.

## Push-ready package (for the landing workstream, do NOT push from here)
This whole folder: GP .blend + gp_frames.json + both builders, GP motion
GIF/MP4 + raw frames, GP before/after + JoJo 03 frame, 2.5D GIFs/MP4s +
contacts + depth spec, lipsync GIF/MP4 + contact, angle configs +
gate CSV, cowl v2 scripts + result CSVs, all three docs. Landing
verifies by size+SHA on main. Nothing was deleted locally.
Mars approval: every new system in this folder 0/1 each.

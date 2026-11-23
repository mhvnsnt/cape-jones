# PURPLE LOT V2-MIXED — Mixed Cut Report (2D)

**Status:** MIXED CUT VERIFIED own-eyes 2026-11-22. **NOT landed** — no commit,
push, or PR from this lane; landing is the owner/parent call.
**Deliverable:** `v2/purple-lot-v2-mixed.mp4` — 480f, 20.000s, 1280x720,
24fps, h264, silent, 6,822,132 B,
sha256 `604e49030bd316e55b18953022cd11ec57cb37094e91c544b0d90183ee297777`.
ffprobe: 480 frames, 20.000s, 24/1 fps, 1280x720.

## 1. The hand bug — cause and fix (owner spotted 2026-11-22 21:27 EST)

**What the owner saw:** in the V2 cut, the SECOND / TOP layer of hands —
the overlay pair used during hand motions — was UPSIDE DOWN. The wrist was
attached where the fingers should be, and the fingers where the wrist
should be. The FIRST pair of hands (the arm's own drawn fist) was correct.

**Cause (verified by reading the art and the renders):** the hand PNGs in
`cape-jones-rig/cape-jones-sliced.zip` are authored fingers-UP / cuff-down
in image space (fingers at the top of the PNG, cuff band at the bottom).
The Blender plane maps image-top to rig +Y (up), while the hand bone
points DOWN at rest (head at the wrist, tail below it). So the overlay
glove rendered fingers-up toward the elbow, 180° opposite the arm's own
fist (cuff at top, fingers down). The plane placement, pivot and bone
parenting were all correct — the IMAGE orientation was wrong. Visible in
the V2 check frames: f150 hanging hand, fingers up, cuff at the bottom.

**Fix (images only, no rig transform touched):**
- L hand: vertical flip (`rig/parts/Hand_*_flip.png`) — fingers down,
  thumb stays on the medial side, matching Arm_Back's own fist (thumb-left).
- R hand: 180° rotation (`rig/parts/Hand_*_rot180.png`) — fingers down,
  thumb on the medial side, matching Arm_Front's own fist (thumb-right).
- A single transform for both sides would put one hand's thumb on the
  wrong (lateral) side. The interrupted mixed-cut lane's
  `rig/parts/sliced_fixed_hands/` (180° for BOTH sides) was NOT used
  as-is, for that reason.
- Remote prop moved with the fix: it sat ABOVE the wrist (y 6.35) because
  the buggy fingers pointed up into it; it now sits IN the fingers
  (y 5.65, overlapping the finger zone 5.34–5.95).
- New rig file: `rig/purple-lot-v2-mixed-rig.blend` (the interrupted lane
  had already renamed the save path; the original V2 rig
  `rig/purple-lot-v2-rig.blend` is untouched, pre-fix copy saved as
  `.pre-handfix`). Originals in `rig/parts/sliced/` untouched.
- **Verified own-eyes (probe, `v2/probe-hands/`, 3 frames):** rest f1 —
  both hands fingers-down, cuffs at wrists, thumbs medial; raise f151 —
  Grip hand wraps the remote, fingers over it, thumb below, cuff at the
  wrist; lower f351 — lowered hand fingers-down with the remote in grip.
- Known pre-existing artifact (NOT from this fix): the remote crop carries
  a light-grey rectangular background visible on close zoom — it was
  already in the V2 cut.

## 2. The mix — what came from V1 vs V2

Owner direction 2026-11-22 21:24 EST: the real show is a MIX of V1 and V2,
not one over the other; use V2 rig stuff to fill the in-between parts that
made V1 a slideshow; all of it could be better, even V2.

**From V1 (the anchors):** V1's beat structure, all 7 boards, all 10
in-between drawings. Each V1 drawing fades in over 3–6f, holds 2–6f, fades
out over 3–6f at the COMP stage (before grading, so the drawing gets the
same sodium/purple grade as the rig frame it sits in). 148/480 frames
carry a V1 anchor blend. Anchors: f1 board 01, f25 ib-01a, f49 ib-01b,
f73 board 02, f97 ib-02a, f121 ib-03a, f137 ib-03b, f153 board 03,
f206 board 05, f313 ib-06a, f337 board 06, f361 ib-06b, f380 ib-07a,
f404 board 06, f428 ib-07b, f452 board 07. The gag beat f169–205 is pure
V1 plates (board 04 + ib-04b click), as in V2. Script:
`rig/assemble_mixed.py` (anchor design from the interrupted lane,
repointed at this lane's frames).

**From V2 (the motion):** the fixed-hand cutout rig (12 bones, 28 sliced
parts, cape 2-bone spring), 240 pose keys on twos, computer tweening
between them — breathing, hand drift, raise, hero sway, lower, nod. The
rig fills every gap between V1 anchors, so no beat is a static hold any
more. Verified numerically: frame-to-frame motion is non-zero everywhere
checked (f210→220 diff 34.10, f250→260 3.66, f300→310 0.53 — hero hold
breathing, f400→410 33.55). V1 held board 05 for 107f with ZERO motion;
the mixed cut's hero beat moves throughout.

**Improvements over V2:** hands fixed (the bug); V1 drawings woven in
(148 frames + 37 pure-V1 gag frames); no other choreography change — the
proven V2 motion is untouched.

## 3. How the frames were rendered — the PIL path (honest)

The Blender Cycles render kept dying on this VM (killed twice: once after
18 frames, once after 49 frames of a chunk; VM load averaged 20–50 from
other lanes' jobs, memory down to 146 MB free) and ran ~15–35 s/frame.
A second agent lane was also rendering the same frames into the same
folder at the same time — its two Blender processes were stopped (frames
are identical in content: same rig, same keys, same outdir; nothing was
lost, the frames on disk are shared).

So the puppet frames were produced a different, verified way:
`rig/dump_transforms.py` loads the fixed-hand rig in Blender and dumps
every part plane's per-frame world transform (centre, rotation, size,
visibility) for all 480 frames — Blender does ALL the bone math.
`rig/pil_render.py` then reproduces each frame as 2D rotate+paste of the
same part art, in the same z-order, through the same ortho camera mapping.
Validation vs the Blender renders that DID complete (f1, f30, f82):
mean abs diff 0.46–2.10 / 255, p99 ≤ 6 at f1/f30 (f82: p99 58, edge AA
only) — visually identical side-by-side, hands correct in both. The PIL
frames are NOT a re-implementation of the rig; they are a rasterisation
of Blender's own transforms. 480 frames in ~7 minutes. The mixed rig was
rendered at 8 samples (was 32 — verified identical: mean abs diff
0.049/255 vs the 32-sample probe frame; emission art is nearly
noise-free). All 480 PIL frames: `v2/pil-frames/`.

## 4. Verification (own-eyes, this lane)

- ffprobe: 480f, 20.000s, 1280×720, 24fps, h264, silent. ✓
- Check frames at all 27 beat/weave points (`v2/mixed-check/`,
  `sheet.png`): f1 wide sodium, f13/f25/f37/f49 breathing anchors,
  f73 medium, f97 drift, f121/f137/f153/f157 raise + remote in grip,
  f180/f200 gag close-up (V1 plates), f206 hero purple, f230 crossfade
  mid-blend, f253 crossfade end, f300 hero, f313/f337/f361 lower,
  f380/f404 nod, f428/f440 pupils (pupils visible, head unmoved),
  f452 board 07, f468 wide, f475 pure black (mean RGB 0, 0, 0.01).
- Hands: fingers-down, cuffs at wrists, thumbs medial at rest, raise,
  grip and lower — in the final cut (f157 raise, f313 lower, f440 nod).
- No long static holds (motion diffs above, all non-zero).
- The remote's grey-box background (pre-existing, §1) is visible on
  close zoom in the raise; it was already in the V2 cut.

## 5. Still not as good as it could be (owner: all of it could be better)

- Elbow/knee cuts: still owed — arms/legs are one piece each in the
  28-part slice set. The PR #430 lane's 44 re-sliced parts have them, but
  their delivered cut is broken (forearms+hands don't render); merging
  their parts onto this pipeline is the next rig step, not done here.
- Cape: still the 2-bone spring, not Wiggle 2 / cloth.
- No COA Tools 2 build, no EEVEE (Cycles CPU only, via the PIL path here).
- Remote prop: grey-box background (see §1) — needs a clean re-crop.
- The V1 anchor dissolves morph between the drawn Jones (bulkier) and
  the rig Jones (slimmer) for 6 frames at each anchor — it reads as the
  drawing coming alive, which is the intent, but the two Joneses are not
  the same drawing.
- Voice ("ah, that's better") and original track remain owner-gated;
  the cut is silent. AnimLab peg/deformer (step 2) and boards/in-betweens
  (step 3) were NOT started in this lane, per the work order.

## 6. Files

- `v2/purple-lot-v2-mixed.mp4` — the deliverable (this report §0).
- `v2/pil-frames/` — 480 puppet frames (PIL, from Blender transforms).
- `v2/mixed/` — assembly intermediates (comp, na/pu streams, final).
- `v2/mixed-check/` — 27 check frames + contact sheet.
- `v2/probe-hands/` — 3-frame hand-fix probe (Blender).
- `rig/purple-lot-v2-mixed-rig.blend` — fixed-hand rig (8 samples).
- `rig/transforms.json`, `rig/dump_transforms.py`, `rig/pil_render.py`,
  `rig/assemble_mixed.py`, `rig/mixed_keys.json`, `rig/render_chunk.py`,
  `rig/render_mixed_loop.sh` (chunked Blender loop — superseded by PIL,
  kept for the record).
- `CHECKPOINT.md` (updated), `RIG-REPORT.md` (V2, unchanged),
  `MIXED-REPORT.md` (this file).
- NOT landed: no commit, push, or PR. Main's `purple-lot-v2.mp4`
  (PR #430, broken forearms/hands) is untouched.

# Cape Jones 3D dance proof v5 — the standing-rig fix

Answers the owner's verdict on v4 (2026-11-02): the dance would work if
his rig was completely fixed with industry-standard tools; instead the
rig and movement still read broken and stiff. His correction stands at
the top of this build: **the sitting rig was the wrong base for standing
work. The sitting rig and sitting pose library are canon and are NOT
modified by this PR** (blob hashes before/after in the PR body — zero
changes). This PR builds a **new, separate STANDING rig** and dances on
that.

Full inventory + v4 diagnosis:
`docs/production/RIG-INVENTORY-AND-V4-DIAGNOSIS-V5.md` (in this PR).

## The standing rig — `cape_jones_standing_v5.blend`

Built by `production/dance-proof-3d-v5/build_v5.py` from the repo's own
3D family (`cape_jones_rigged_w5r.blend` — the bake-off-validated file),
copied out to a new file. Nothing was hand-keyed and no substitute was
fabricated. One more repair the measurement forced: the base rig's
**hands, fingers and toes were never skinned** (most finger groups at
exactly 0.0 total weight, toes at exactly 0.0 — full census in the build
report). The toes get a distance-falloff completion (two-bone chain).
The hands get a **fan-axis completion**: the sculpt's fingers are one
fused mitten, so each distal vert's finger weight is split across the
five finger chains by lateral proximity to each finger's own axis,
and along the chain by projection — the mitten curls as one fist.
The completion's weight fields are then **smoothed over the mesh**
(Laplacian, 10 iterations — the smoothness term every production
skinning solver carries), and the wrist crease is rebuilt as a clean
two-bone forearm↔hand blend: the base bake had scattered finger-bone
weight into the wrist (one pinky segment held 663 weight units at the
wrist crease while the hand bone itself held 111 of 8,788 zone verts).

- Weights remain the bake-off-winning **Surface Heat Diffuse** solution
  (in-repo MIT solver) — the only solver that ever produced usable
  full-mesh weights on this model (Blender Bone Heat fails 100% on it,
  documented in `docs/research/WEIGHT-BAKEOFF-2026.md`).
- **Preserve Volume restored ON** (the v3 scene had it OFF; v4 inherited
  OFF — volume collapsed at every bend).
- **Twist bones** (upperarm/forearm/thigh) built by the bake-off's own
  `add_twist_bones()` construction — half the downstream twist is
  absorbed mid-segment instead of candy-wrapping the biceps.
- **Shoulder/deltoid repair** (the owner's named defect; bake-off defect
  zone 1): chest+clavicle vs upperarm weights re-blended across the
  shoulder joint by a smooth distance falloff, identical construction
  on both sides — the documented R/L solver asymmetry (~688k vs ~300k
  claimed verts) is removed by construction. Measured before/after
  group counts: `build_v5_report.json` in this PR.
- **Ankle transition tightened** the same way (bake-off defect zone 2).
- Influences capped at 4, totals renormalized (repo standard).
- Corrective Smooth at the winning 0.5 / 3 iterations.

## Pose-test gate (hard gate — ran BEFORE the dance)

`production/dance-proof-3d-v5/gate_v5.py` — scripted extreme bends at
shoulder, elbow, wrist, fingers, spine, neck, head, hip, knee, ankle and
the cape chain, rendered full-body + zoomed (shoulders, elbows, hips,
knees, cape hem, between legs), with cross-section volume ratios
(posed vs rest) per limb segment. Gate sheet:
`cj-dance-proof-3d-v5-gate-sheet.png` (in this PR and delivered with the
video). Numbers: `gate_v5_report.json`.

**Gate verdict: PASS** (own-eyes reads of the zoomed crops; volume =
cross-section radius, posed vs rest):

- **Shoulder → bicep → elbow (the owner's named defect): PASS.**
  Arm down: upperarm 0.996 / 0.995, deltoid smooth. Arm overhead:
  0.985 / 0.984, deltoid flows into the raised arm, natural armpit
  fold, no pinch crater (the base rig FAILED this pose in the bake-off).
  Forward raise + elbow bent 115°: upperarm 0.985 / 0.983,
  forearm 1.001 — the whole arm moves from the shoulder, nothing is
  elbow-only.
- **Crouch: PASS.** Thigh 1.001, shin 1.006; the cape's back panels
  hang as two solid unbroken sheets (before the panel-unification fix
  they fringed into strips — the panels' verts were split between
  pelvis and thigh weight; now unified to the pelvis).
- **Spine + head: PASS.** Distributed bend, head turn reads clearly.
- **Fingers: PASS (mitten curl).** The sculpt's fingers are one fused
  mitten; the fan-axis completion makes the whole mitten curl as one
  hooked fist for the first time (base: fingers could not move at all).
- **Cape: PASS.** One solid piece in every full-body gate render.
- **Documented flaw (pre-existing, not caused by this build):** at the
  extreme 115° elbow bend, an edge-on zoom shows a small gap at the
  palm heel — the sculpt is built from unwelded surface islands, and
  two islands that merely touch at rest separate by a few millimetres
  at that angle. Reproduced IDENTICALLY on the untouched base file in
  the same harness (bisected across three builds); face-on views at
  70° and 115° read whole. It is a sculpt-geometry property, not a
  weight defect, and sits far beyond the dance's elbow range.

## The dance

`production/dance-proof-3d-v5/solve_v5.py` — CMU 15_04 loop (the same
front-facing, in-one-spot window v4 selected by facing scan) retargeted
onto the standing rig's own FK layer with the repo's world-space delta
method (`mocap_retarget.py` lineage): torso orientation deltas
distributed over the spine chain, two-bone analytic limb placement from
the captured joint positions with normalized reach, fingers by the
master-coupling distribution, cape by lagged chest deltas. 96-frame
loop tiled ×19 = 1,824 frames, full 75.79 s song, **EN v2 mix**
(v4 used JP; the approved mixes rotate). World cycle day → LED → night
reuses the v3 set and its actions. Rendered 960×540 / 24 fps.

Two retarget bugs were caught by numeric probes and fixed in this
solver — both are the class of error that reads as "broken, stiff
movement" while joint numbers look fine:

1. **Delta compounding across frames.** The first solve premultiplied
   each frame's orientation delta onto a bone matrix that already
   contained earlier frames' keyed deltas (the action was attached
   during solving). The pelvis wound through a full 360° revolution
   over the loop (measured, probe13). Fix: solve with the action
   detached, reset every bone each frame, record the bases, write the
   keys afterwards (v4's solver set absolute matrices for the same
   reason).
2. **Delta compounding down chains.** Applying a joint's full world
   delta at every bone of a parented chain adds it once per bone:
   spine folded shut on the deep-crouch frames, cape whipped to 2.1×.
   Fix: every delta is parent-relative (child delta composed with the
   inverse parent delta) and split evenly across the bones sharing it
   — the same treatment for spine, neck, clavicles, fingers and cape.

Deliverables: `cj-dance-proof-3d-v5.mp4` + `cj-dance-proof-3d-v5-sheet.png`
(delivered in chat with the gate sheet; the standing .blend is
delivered alongside them — at ~93 MB it exceeds the Git Data API blob
limit, so like v4's rig it is not inside this PR; it is fully
reproducible from main by running `build_v5.py` on the repo's
`cape_jones_rigged_w5r.blend`, and its SHA-256 is in the PR body).

## Honest shortfalls

- **Palm-heel island gap at extreme elbow bend.** At the gate's 115°
  elbow pose, an edge-on zoom shows a small black gap at the palm heel
  and a slightly displaced surface chunk. Exhaustively bisected: the
  identical gap renders from the untouched base rig under the same
  harness, and no weight surgery at the wrist changes it — the sculpt
  is unwelded surface islands that merely touch at rest and separate a
  few millimeters at extreme flexion. Face-on views at 70° and 115°
  read whole; in the dance's elbow range it does not appear. Fixing it
  means re-welding the hand sculpt, not rig work.
- **Mitten fingers.** The sculpt's hand is fused; the completed finger
  skinning curls it as one hooked fist. The index chain carries little
  direct weight (its fan direction overlaps the middle finger's). A
  faint hard step crosses the knuckle line in the curl zoom — another
  sculpt-island boundary.
- **Render samples.** The dance is rendered in EEVEE at TAA 8 samples
  (software GL on this machine; the full-res body at the default 64
  samples measured ~100 s/frame would take ~50 h). The flat cartoon
  look is unaffected; edges may shimmer very slightly in motion.
- **Same dance window as v4.** CMU 15_04 @12625 was independently
  re-chosen by facing scan in this lane (the source was verified
  upright and innocent of the v1 solve bug by probe). It is a
  bounce/squat groove in one spot, per the scene spec.

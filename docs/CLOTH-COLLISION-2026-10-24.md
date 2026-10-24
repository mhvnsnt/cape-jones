# Cloth collision + clipping audit — Cape Jones show (2026-10-24)

> Reproduce note: the scripts in tools/show-cloth/ are the exact procedure record. They reference absolute paths under the lane's scratch dir (~/workspace/scratch/cj-cloth-20261024/) plus the release-hosted cape-jones-show.glb and the repo's living_room.blend — adapt the SRC/OUT constants to rerun. Working blends (19–292 MB) and the 118 MB GLB are NEVER committed; the scripts + this doc + the proof PNGs are the committed record.


## What the cape actually is (measured, not assumed)
- The standalone `CapeJones_Cape` is a SHORT shoulder mantle (peaked top,
  0.42 m wide, 0.32 m tall; 82,213 shared verts / 157,262 polys), NOT the
  full-length cape. The full cape visible in renders is part of the BODY
  mesh (skinned drape).
- As shipped, the mantle sits EMBEDDED inside the body: 3,890 BVH overlap
  pairs at rest, 1,821–2,923 across idle frames, min distance ~0 mm.
  It must be placed on the shoulders before any cloth work makes sense.
- Placement (idle, measured from rest-pose bones): location
  (0.01, 0.04, 0.377) puts the top band at neck_1 head (z 0.779) and ~15 mm
  proud of the drape back surface. VIEWED at frame 0: mantle across the
  shoulders, peaks at the neck, hanging to mid-back.

## Collision setup (stage2 pattern, sitting-saga proven)
- NO body duplication: duplicating the body OOM-killed this VM twice
  (sitting saga) and again in this lane.
- Primitive colliders skinned to the rig: back shell (measured p99 back
  profile, 10 mm inset + 15 mm collision thickness) + arm/thigh capsules
  + REAL chair (308 verts) + floor.
- Cloth: stage2 settings; proxy quality 5 (12 OOMs here at full res).
- Pin: local-z ramp, full pin across the top band (1,846 full-pin verts
  on the 82k mesh).

## The OOM story (honest)
- Full-res cloth (224k AND 82k capes) dies at solver init on this VM
  (SIGKILL ~30–60 s, 3 attempts), even with the body stripped.
- Mini test proved the path: decimated proxy (~5k verts) bakes fine
  (10 frames / 72 s, is_baked=True).
- => PROXY WORKFLOW: decimate 0.05 (~4.1k sim verts), bake, full cape
  follows via Surface Deform for proof renders. Clearances measured on
  the proxy (representative) + spot-checked on the full cape.
- A 0.08/quality-8 proxy bake ALSO died mid-run (frame 50 of 96) under
  system-wide memory pressure; the 0.05/quality-5 bake completed
  (599.4 s, 96 frames, is_baked=True).

## Idle bake (Scene A: cape-vs-body) — v2 vs v3
- V2 (world-fixed pins) COMPLETED but PENETRATED: proxy-vs-real-body at
  frame 48 = 1,286 overlap pairs; min 0.01–0.06 mm at frames 24–96
  (touching); frame 0 clean (6.84 mm). Arm capsules: L clears 19.6 mm,
  R touches (0.02 mm, 0 penetration). Floor: 489 mm clear.
- ROOT CAUSE of v2: the cape object was UNPARENTED, so cloth pins were
  fixed in WORLD space while the body moved under them during the idle.
  A mantle pinned in world space on a moving character MUST penetrate.
  (Static sitting bakes don't hit this; moving idle does.)
- V3 FIX: cape parented to the chest BONE (world matrix verified
  preserved at frame 0) + neck capsule collider; proxy 0.05/q5; 96 frames.
  Frame-48 cape shape differs from v2 completely (mean vert delta
  206 mm, all 6,903 verts moved >10 mm) — parenting DID change the sim.
  Median cape-body distance halved (57 mm -> 25 mm): cape rides the torso.
- V3 RESIDUAL (honest, NOT zero-penetration): frame 48 still 1,286
  overlap pairs, but only 181 cape faces / 215 verts involved (~3% of
  proxy verts), mostly FREE cloth (165 free, 32 ramp, 18 pinned),
  world z 0.52–0.805 (mid-back to shoulders). Cause: the back-shell proxy
  doesn't track the true back surface exactly during idle motion
  (skinned z-band weights vs real deformation) + shell edges + proxy
  triangle chord error vs the dense body. Pair count is inflated (one
  cape face x dozens of tiny body triangles).
- V3 PROOF RENDERED + VIEWED (baked_idle_v3_f0/f48/f96_back.png): mantle
  sits on shoulders, peaks at neck, hangs to mid-back, follows body
  through idle. No visible mantle-body penetration from back views
  (measured contact is sub-surface, hidden by the mantle itself).
  Pre-existing observations (NOT cloth-caused): body's skinned drape
  folds raggedly in crouch poses; thin line artifact at ankle height.
- DESIGN NOTE: the mantle overlays the body's built-in drape, and they
  share the back volume — the residual contact is a design overlap, not
  a sim failure. Zero-penetration needs either hiding the body's drape
  when the mantle is worn (show decision) or a real-body collider bake
  (bigger machine / longer bake). See sitting section for the proof
  that the seated pose has the same overlap structurally.

## Sitting bake (Scene B: cape-vs-chair)
- Setup: room rig in pose_sit_normal, mantle rotated Rz(-90) onto seated
  shoulders, real chair collision + static shell (rebuilt in room coords
  after the first shell double-transformed to y~4.1) + thigh capsules,
  60-frame settle.
- V1 SIT BAKE INVALIDATED (quaternion bug): the room-blend cape uses
  QUATERNION rotation_mode, so setting rotation_euler was ignored — v1
  "mantle" was an unrotated plank (wide in x, thin in y) at x 3.444–3.867,
  BEHIND THE WALL (3.425), invisible in renders. V1 sit numbers
  (chair 118 mm, shell 2.25 mm) describe the plank, NOT the mantle, and
  are DISCARDED (kept in logs as a cautionary record).
- V2 SIT BAKE COMPLETED (rotation_mode XYZ forced; bbox verified thin
  in x [3.444, 3.472], wide in y [1.847, 2.270], z [0.469, 0.790]; 60
  frames, 0.05/q5). Measurements (measure_sit2b.log, all 60 frames,
  static settle, frames 1 and 60 identical): chair min 116.22 mm, 0
  overlaps (sampled 1/12/24/36/48/60); shell min 0.05 mm (contact, 0
  overlaps; shell is inset 10 mm inside the body surface, so ~10 mm
  from the true body); thighs 271.53/383.95 mm, 0 overlaps. Floor number
  (3,237 mm) is a wrong-Floor-object mismatch, not claimed.
- SIT RENDER PROBLEM (honest): the v2 mantle sits at x 3.444–3.472,
  BEHIND THE WALL plane (3.425), because its top band was anchored to
  the neck-height back surface (3.432), which is the leaning head/hood,
  not the torso. From the front camera the wall occludes it; renders
  show an empty chair. The placement is not show-valid as baked.
- WHY NO THIRD SIT BAKE: seated-body histogram proves no full-height
  shoulder mantle fits with the drape present. At z 0.65–0.75 (shoulder/
  head height) the body fills x 3.00–3.55 CONTINUOUSLY (every 50 mm bin
  11k–20k verts; torso band z 0.55–0.65 by contrast ends cleanly at
  3.25). The bulk is predominantly the body's billowing drape (by vert
  count) + hood. Any x in that band intersects body mesh; x > 3.55 is
  inside the wall. So a torso-anchored re-bake would intersect the drape
  bulk just as the wall-anchored one does, at a different x. The fix is
  a SHOW DECISION: hide the body's drape in seated shots (mantle
  REPLACES drape) or accept drape-bulk contact — not another sim tweak.
  This also answers the lane's open question (replace vs overlay):
  overlay is geometrically impossible at shoulder height in the seated
  pose; replace is the consistent option, pending owner approval.
- Sitting proof renders: sit_f60_front/side (v2 placement, viewed):
  empty chair — the mantle is behind the wall from the front camera.
  Reported as a placement failure, not as proof of success.
- Sitting proof WITH BODY (sitbody_f60_front/side, viewed): figure
  seated in the chair, arms out, wearing his full drape. Front view:
  mantle NOT visible (occluded by wall). Side view: mantle visible as
  a black slab behind the chair back — it IS there, hanging behind the
  chair, but behind the wall plane, so it reads as "empty chair back"
  from the front. Not show-valid from the front.

## Intersection audit (all show animations)
- anims/show/ holds ONE clip: cape-jones/idle.glb. Pre-cloth overlap
  (unplaced mantle): 1,821–3,890 pairs. Post-cloth (v3): 1,286 pairs at
  frame 48 but only 181 faces / 215 verts (see above).
- Sitting poses (5, from sitting_pose_library.blend; placed mantle,
  rigid, not baked; audit.log). Mantle-vs-body overlap computed only
  for pose_sit_normal (bounded cost); other poses report distances only.
  | pose | body_vs_chair_overlap | pelvis_z | mantle_vs_chair_min_mm | mantle_vs_chair_overlap | mantle_vs_body_min_mm | mantle_vs_body_overlap | applies? |
  | pose_sit_normal | 5,694 | 0.389 | 115.96 | 0 | 0.04 | 0 | yes |
  | pose_sit_leg_folded | 5,694 | 0.389 | 3,061.03 | 0 | 3,087.98 | — | NO (mantle 3 m away) |
  | pose_sit_lean_forward | 4,289 | 0.387 | 27.87 | 0 | 0.04 | — | weak (pelvis +2 mm, body dist identical to normal) |
  | pose_sit_recline | 6,736 | 0.320 | 3,022.64 | 0 | 3,017.37 | — | partial (pelvis moves, mantle 3 m away) |
  | pose_sit_shrug | 5,694 | 0.389 | 71.11 | 0 | 0.10 | — | yes |
  Findings: (1) normal + shrug apply cleanly and give sensible mantle
  clearances (chair 116/71 mm, 0 overlaps; body contact 0.04/0.10 mm,
  normal 0 overlaps). (2) leg_folded + recline placements FAIL — the
  mantle lands ~3 m from chair/body, so those poses are NOT validated;
  the library actions do not apply cleanly to the room rig for those
  poses (likely action/rig compatibility — needs investigation, not
  assumed). lean_forward barely applies (pelvis +2 mm). (3)
  body_vs_chair_overlap is NONZERO in all poses (4,289–6,736 pairs) —
  shallow back-vs-chair-back contact (~10 mm depth; thousands of pairs
  because both meshes are dense), CONTRADICTING the sitting saga's zero
  gate. Method difference: the audit applies raw library actions without
  place_sitter's root lift (ankles at 0.064); the saga used place_sitter.
  The zero-gate needs re-verification with the place_sitter method, not
  silent acceptance of either number.
- Body self-intersection: NOT gated (BVH self-overlap on a skinned mesh
  is dominated by adjacent-face pairs; cross-object gates above are the
  meaningful ones). Body-vs-chair gate re-verified via place_sitter method.
- Pre-existing (not this lane): body's drape penetrates the wall plane
  in the seated pose (drape bulk to x 3.55 vs wall at 3.425); thin ankle
  line artifact in renders; body's drape folds raggedly in crouch poses.

## Out of scope / follow-ups
- SHOW DECISION NEEDED (blocks show-valid sitting mantle): hide the
  body's built-in drape when the standalone mantle is worn (mantle
  REPLACES drape), or accept mantle-vs-drape contact in seated shots.
  Same decision resolves the idle residual contact.
- Recline-motion (0→1) cloth bake: needs scene_recliner_mech.blend
  (release recliner-mech-20261023, 165 MB, not in repo tree) AND bone
  parenting (idle lesson: world-fixed pins fail on moving bodies). The
  settle bake covers the seated state; the recline sweep is the next bake.
- Real-body collider bake (alternative to shell proxy) for
  zero-penetration idle: needs bigger machine or longer bake budget.
- SITTING-POSE-LIBRARY.md "Cape drape validation: PENDING" — this lane
  addresses it for the show-rig mantle; the W5r-library drape question
  remains open if the show adopts the W5r poses directly.

## Reproduce
- tools/show-cloth/build_cloth_idle.py, build_cloth_idle82.py,
  slim_scene.py, build_proxy_bake.py, bake_proxy.py,
  build_cloth_idle_v3.py, bake_v3.py, measure_body.py,
  measure_body_v3.py, compare_v2_v3.py, diag_penetration.py,
  render_proxy_v3.py, build_cloth_sit.py, fix_sit_shell.py,
  check_sit_shell.py, build_proxy_sit.py, bake_proxy_sit.py,
  measure_clearance.py, measure_sit2.py, audit_sitting.py,
  render_sit.py, measure_seated_geo.py
- NEVER commit the 118 MB cape-jones-show.glb (release asset) or the
  19–292 MB working blends (scratch only).

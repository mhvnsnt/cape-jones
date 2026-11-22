# Cape Jones PURPLE LOT V2 — Cutout Puppet Rig Report
**Track: 2D. Lane: RIG-BUILD. Date: 2026-11-22. Blender 5.2.4 LTS + COA Tools 2 (Aodaruma fork v2.3.0) + Wiggle 2 RTX.**
**Status: RIG BUILT AND PROVEN STRUCTURALLY + NUMERICALLY. Visual proofs rendered (compositor); parent own-eyes pass still owed. `.blend` NOT saved (disk-write wall — see §9).**

Targets (owner 2026-11-22): Metalocalypse + Amazing World of Gumball + $UPEREGO + Aqua Teen Hunger Force. Method: the Metalocalypse/ATHF way — puppet rigs, not hundreds of drawings. Bar: 24fps, twos density (a new rig pose every 2 frames, computer tweening between poses).

## 1. Pieces (44 part PNGs, 4,315,237 bytes total)
All on branch `v2-rig-parts`, `production/2d-parking-lot/v2/rig-parts/<name>.png`, with `MANIFEST.json` (name, source box, method, w×h, bytes, fg px, sha256). Sliced from the real source art (flood-fill from the border / colour-key), never hand-drawn. Every part verified on the branch (44/44 listed, head.png re-downloaded and sha256-verified byte-identical).

| Group | Parts |
|---|---|
| Body (sheet 01 T-pose) | head, torso, pelvis, upper_arm_R/L, forearm_R/L, hand_glove_open_R/L, thigh_R/L, shin_foot_R/L |
| Cape (sheet 08 + poses) | cape_hang, cape_sweep, cape_billow, cape_diag, cape_settle, cape_billow_pose |
| Hands (sheet 08) | fist_glove_h, fist_glove_v, hand_glove_point, hand_glove_open_08, belt_front |
| Props (poses) | remote_small (pose-02), remote_gag + hand_bare_gag (pose-03 close-up gag) |
| Eyes (sheet 05, grey-keyed) | white_default, look_left, look_up_b, look_down, look_up_c, sideeye_a, closed, angry, smug_sideeye |
| Pupils (derived) | pupil_center, pupil_audience (black discs on the white-default pair) |
| Mouths | neutral (sheet 05 head #1), halfsmile (pose-05) |
| Dance variants (derived) | forearm_R_out, forearm_L_out (gauntlet-flip), shin_foot_R_in, shin_foot_L_in (FootIn) |

R = viewer-left / his right = the remote arm. Palette locked: suit #FFFFFF, cowl & logo #3E1473, skin #E5B28C, cape & shadows #000000, 2–4px rim light, white eyes default. White gloves everywhere except the gag beat (bare hand ONLY in the PL-04 close-up, gloved again on the cut to wide).

## 2. Bones + hierarchy (19 deform bones + 8 IK/pole = 27 in the armature)
Sprite object `CJ_SpriteRig` (COA-flagged armature). Puppet plane = XZ, up = +Z, right = +X; scale 0.01 (1 sheet px = 0.01u); figure origin sheet-01 (1024,580).

```
Root
├── Spine → Chest → Neck → Head
├── Thigh.R → Shin.R        (hips 180 apart, LEG-CONNECTION-v8: x 934/1114)
├── Thigh.L → Shin.L        (thighs parented to Root: hips drop WITH the pelvis, HIP-LOWER-ANATOMY)
├── UpperArm.R → Forearm.R → Hand.R      (Chest)
├── UpperArm.L → Forearm.L → Hand.L      (Chest)
└── Cape1 → Cape2 → Cape3 → Cape4        (Chest; Cape1 use_connect=False)
IK: IK_Hand.R/L, IK_Foot.R/L, Pole_Elbow.R/L, Pole_Knee.R/L (all use_deform=False)
```
Binds (P9 method: sprite ACTIVE, `temp_override(selected_bones=…)`, `bind_mesh_to_bones(ob_name=…)`): **42/42 bound, 0 failures.** Cape (all 6 variants) → Cape1–4; torso → Spine+Chest; pelvis/belt → Root; limbs → their single bone; head/eyes/mouth → Head; remote_small → Hand.R; hand_bare_gag + remote_gag are unbound close-up props.

## 3. IK setup
Plain Blender IK (not COA's): forearms + shins, chain_count 2, pole targets (elbows +90°, knees +90°). IK targets sit at the hand/foot rest positions; pole targets at the elbows/knees. Arms raised = whole arm from the shoulder, forearm follows (JOINT-LOCKED-v4). Jump legs tuck toward each other (never split).

## 4. Range of motion (demonstrated by the proof poses, degrees, screen-clockwise-positive)
| Joint | Demonstrated range |
|---|---|
| Shoulder (UpperArm) | −80 (hang) … +180 (across chest); raise +135; flex ±150 |
| Elbow (Forearm, relative) | −125 (flex) … +30 (twist); raise −20 |
| Hip (Thigh) | −15 … +35 (groove kick) |
| Knee (Shin, relative) | −40 (groove) … +10 |
| Neck/Head | −8 … +8 (nod/tilt) |
| Chest/Spine | 0 … +12 (twist) |
| Root (pelvis drop) | 0 demonstrated; squat drop is wired (thighs parented to Root) but no squat pose rendered yet — owed |
| Cape chain | Wiggle live sim (below); sway angles demonstrated 0–12° |

These are the ranges the poses prove, not hard joint locks — COA has no angle limits set; the animation lane keys whatever the boards need and the gates below catch bad poses.

## 5. Wiggle 2 RTX cape (live sim, per the cape proof recipe)
Cape1 `wiggle_head=True`, Cape4 `wiggle_tail=True`; stiff/damp 25/1.0, 18/0.8, 14/0.7, 10/0.6; mass 1.0, gravity 1.0; `scene.wiggle_enable=True` (defaults FALSE — set explicitly). `build_list()` ran, cape chain registered. **Bake NOT relied on** (partial in the cape proof — Cape2/Cape3 never bake; bake replaces the active action). Live sim is stepped per frame (`frame_set` + `view_layer.update()`); an animation render does NOT step it. Cape follow-through: the cape lags the body by 1–2 frames and settles after it (12-principles #5).

## 6. WHAT MOVES
- Every bone (FK pose + IK targets), all 11 eye swaps, 2 mouth swaps, 7 hand swaps, 6 cape swaps, remote prop.
- Cape follows through on the Wiggle live sim (bend concentrates in the bottom quarter — the cape proof's finding).
- Sprite swapping is wired by visibility (COA `hide_viewport`/`hide_render` per part, default-visible set per LAYOUT).

## 7. What the rig CAN'T do (gaps for Grease Pencil hand in-betweens / later work)
- **No 3/4 back-arm layer.** Both arms render in front of the torso (z 0.02/0.03 > torso 0.01). The CJ docs' Arm_Back/Arm_Front split is not built; a 3/4 view needs a behind-body arm piece. Acceptable for the board framings (front/medium); a gap for later.
- **Pieces don't deform within themselves.** Joints bend BETWEEN pieces (forearm rotates about the elbow, shin about the knee). A forearm/torso never curves — only the cape (6×20 grid) and torso (8×8 grid) have deformable meshes; all other pieces are rigid quads (correct for a cutout puppet; COA automesh is unusable here — it needs cv2 + the image FILE on disk, both wall-blocked, so I built my own grid meshes).
- **No squash & stretch on the head/body** (12-principles #1 beyond rigid rotation). Flex biceps bulge, impact squash — Grease Pencil in-betweens, owed.
- **No finger articulation.** Hands are single pieces (open / fist / point / bare). Finger-level motion is a swap or a Grease Pencil pass.
- **Mouth library is 2 shapes** (neutral, half-smile). The sheet-05 heads hold more mouths; cutting them into swaps is owed. No phoneme set (the Gumball mouth library is the model for this when dialogue comes).
- **Cape scale is unresolved.** Sheet-08 cape_hang spans z 3.1 to −1.05 (mid-shin); the bone chain runs to −4.7 (below the feet). It needs ~1.9× scale (or the sheet-01 cape) to reach the feet. Set from the first visual pass.
- **Fist/point/08-hand wrist anchors are estimates** (wrist at the crop edge; verified numerically at d=0 for the open hands, but the fist/point/08-hand offsets are eyeballed from the sheet-08 row and need the visual pass).
- **No walk cycle yet.** Legs are proven in strut/groove poses; a looped walk is the animation lane's job on this rig.

## 8. Dance articulation + DANCE TEST
Dance requirement (owner 2026-11-22 ~09:00 EST): full-body articulation — hips, shoulders, knees, elbows that hit dance poses (strut, twist, flex, knee/feet, wrist attach) — cape as follow-through. Built on the Gumball S2 rig study (pose-library masters, pivots AT the joint, HIDE_NECK occluder = the head piece's cowl, pupils always a separate layer, FLOPPED = separately drawn, never −1 scale) and the CJ rig docs (arm-alignment, arm-front-snap, arm-flip/leg-gap, joint-locked-v4, knee-feet per-frame gate, leg-connection-v8, hip-lower-anatomy, head-neck-v6, gauntlet-flip, wrist-attach-fix, 12-principles checklist).

### Dance test — what it proves FIRST, before the next cut
Poses rendered by the 2D cutout compositor (`rig/proof_composite.py`, same pivots/z-order/placement/swaps as the Blender rig): strut, twist, flex, groove + the 6 board poses (rest, idle, raise, press_gag, lower_smug, pupil_end) + a 6-frame motion proof (raise → press → lower on twos). Per-frame gates, all computed from the rig math:
- **Wrist gate** (d_wrist ≤ 30 sheet-px AND d_wrist < d_tip): **PASS on all 10 poses + all 6 motion frames — d_wrist = 0.0 everywhere** (the wrist pixel sits exactly on the forearm end through every rotation; verified numerically from the build log too).
- **Knee-feet gate** (FootIn swap ONLY when both thighs angle toward the midline; per-frame, never a block range): **PASS everywhere.** Strut (thigh +20/−15, FootIn true, _in active), groove (+35/−5, true), twist (+10/−10, true, _in active).
- **Arm-front-snap gate** (forearm-vs-torso alpha overlap > 1430 px @2048×1152; a declared snap must show overlap + the arm layered above the torso): **PASS everywhere.** Twist: overlap 3,107 px, snapped, arm above torso. Idle overlap 0 (arms hang just outside the torso edge — correct, the pre-fix 2,145 was the warp bug).
- **Gauntlet-flip** (|forearm| ≥ 120 AND forearm in front of torso → _out variant): flex uses the _out condition via relative angles ±125°; twist does NOT meet it (relative +15) and correctly uses the normal forearm.
- **Timing**: poses are keyframes; the motion proof interpolates raise → lower_smug over 6 frames (t=0…1) with the snap overlap falling smoothly 2,251 → 1,192 → 171 → 0 → 0 → 0 — clean continuous motion, no jumps, no detached limbs by any gate.
- **Cape follow-through**: Wiggle live sim wired (see §5); the compositor stills show the cape as a rigid follow-through (sway angle) — the live-sim bend is proven by the cape proof lane's sim, not re-proven here.

### Proof files (branch v2-rig-parts, `production/2d-parking-lot/v2/proof/`)
| File | Size | Gates |
|---|---|---|
| pose-rest.png | 1,742,104 B | all pass; bbox (545,158,1503,1046) vs rig-math prediction (536,158,1512,1052) — within 9 px |
| pose-idle.png | 1,826,175 B | all pass |
| pose-raise.png | 2,485,156 B | all pass |
| pose-press_gag.png | 1,784,714 B | all pass |
| pose-lower_smug.png | 3,324,441 B | all pass |
| pose-pupil_end.png | 2,380,523 B | all pass |
| pose-flex.png | 2,359,124 B | all pass |
| pose-groove.png | 2,648,199 B | all pass |
| pose-strut.png / pose-twist.png | NOT ON BRANCH — rendered, all gates pass, uploads died on the GitHub rate limit (see §9) | gates pass (strut knee-feet +20/−15; twist snap 3,107 px) |
| motion frames f0–f5 | rendered + analyzed in-process (not uploaded); all gates pass on all 6 frames | see §8 |

**Own-eyes visual pass: NOT DONE in this lane.** I could not see the proof pixels in this sandbox (Blender's render result stays empty — see §9; the widget image fetcher fails on the 1.7–3.3 MB proofs; browser.open returns references, not viewable pixels to me). The parent (or a browser-capable lane) must open the 8 proof URLs above and do the visual pass — especially: cape length/scale, the fist/point wrist anchors, the gag close-up framing, and the flex/groove poses — before the animation lane treats them as approved. Programmatic analysis stands in until then: rest bbox matches the rig math within 9 px; the sodium proofs' red pixels are the background plate's own red lights (8,050 in the plate); the purple proofs carry ~2,400–5,900 faint red speckles from the compositor's warp (an artifact of the proof tool, NOT the rig — the part PNGs are verified 0 red pixels).

## 9. Environment notes (what blocked what, and the workarounds)
- **Disk-write wall (80% quota, 119G/150G):** child-process writes land 0 bytes or EPERM — Python, printf, cp, Blender saves, /tmp, /dev/shm, all of it. Local `rig/parts/*.png` are all 0 bytes (never claim otherwise). **Workaround that held:** compute in memory → `gh api` PUT (network writes) for all 44 parts + MANIFEST + 8 proofs; Blender reads parts from `raw.githubusercontent.com` into memory (pure-Python PNG decoder, byte-identical to cv2 on all 4 test parts); proof renders go out the same way.
- **GitHub API rate limit (user 197314870): HARD STOP.** After the part/proof uploads, `gh api` returns 429/401/stream errors. No more GitHub calls in this lane. Strut/twist proof uploads + RIG-REPORT.md upload are owed after the hourly reset (`proof_composite.py --jpg strut twist`; report is at `rig/RIG-REPORT.md` locally).
- **Blender render readback is broken in this sandbox.** Cycles COMPUTES pixels (debug log: 8 samples in 0.15s, "Saved") but `bpy.data.images['Render Result']` stays (0,0)/has_data=False — in every mode tried (write_still, double render, frame_set, compositor Viewer Node which crashes Blender). Workbench aborts (no libEGL.so.1 on the box). Hence the Python compositor as the visual-proof engine. The 65-byte `rest_tpose.png` on the branch is an EMPTY render — NOT a proof; ignore it.
- **COA automesh is dead here** (needs cv2 + the image FILE on disk). Replaced by my own grid meshes (capes 6×20, torso 8×8). P9's "automesh OK" only meant the op didn't raise.
- **Placement sign bug (found + fixed):** COA puts the image top at obj.location.z with the image extending DOWN, so placement must derive from the box TOP-LEFT, not the centre — the first build run mirrored the figure in Z. Fixed in `placement()`.
- **Warp bug (found + fixed):** the compositor passed the FORWARD transform to `cv2.warpAffine`, which expects the INVERSE — rotated parts went the wrong way about the wrong centre. Fixed (`[R^T | −R^T t]`); idle's top-edge red band cleared.
- **gh auth flickers** (transient 401s, stream errors) — `gh_put` retries 3×; the rate limit, not the flicker, is what stopped uploads.

## 10. How to rebuild / use the rig (animation lane)
1. Parts are on branch `v2-rig-parts` (`production/2d-parking-lot/v2/rig-parts/`, MANIFEST.json alongside).
2. Run `rig/build_rig_remote.py` in Blender 5.2.4: `xvfb-run -a env -u PYTHONPATH <blender> -b --factory-startup --python build_rig_remote.py`. It downloads the parts, builds the sprite object + 19 bones + IK + Wiggle, and attempts the `.blend` save (lands when the wall clears).
3. Pose by keyframing bone rotations (FK) or the IK targets; swap eyes/mouth/hands/capes by visibility; check the gates per frame (wrist d≤30, knee-feet FootIn, snap overlap). Timing: on twos at 24fps; cape lags the body 1–2 frames (Wiggle live sim, stepped per frame).
4. Proof with `rig/proof_composite.py` (`--analyze` for gates+bbox without uploading; `--view` for small base64 previews). `rig/motion_proof.py` renders interpolated frame sequences the same way.

## 11. Open items (owed, in order)
1. Parent own-eyes visual pass on the 8 proof URLs (§8) — cape scale, fist/point wrists, gag framing, flex/groove.
2. Upload pose-strut + pose-twist + this report to the branch after the GitHub rate-limit reset.
3. Save `rig/cj-cutout-rig.blend` when the disk-write wall clears (disk < 80%); until then the rig is the builder script + the repo parts.
4. Cape scale (~1.9×) or the sheet-01 cape, set from the visual pass.
5. Squat pose (Root drop with feet planted) to prove the hip-lower wiring.
6. Mouth library expansion from the sheet-05 heads; back-arm layer for 3/4 views.
7. Blender render readback: re-test when the sandbox changes (Cycles computes; the result never materializes) — the compositor is the proof engine until then.

---
*Files (local, `~/workspace/_cape-jones-parking-lot-2d/rig/`): `build_rig_remote.py` (builder), `build_rig.py` (local-disk edition, superseded by the remote edition while the wall is up), `proof_composite.py` (proof engine), `motion_proof.py`, `analyze_proofs.py`, `upload_part.py` / `upload_all.sh`, `make_part.py`, `probe_coa.py`, `PROGRESS.md`, `parts/MANIFEST.json` (local copy; canonical copy on the branch).*

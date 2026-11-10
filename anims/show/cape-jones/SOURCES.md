# SOURCES — anims/show/cape-jones/ (show clips for Cape Jones)

Show-context clips ONLY. Never fight movesets — the anim-gate law holds:
show clips play in SHOW / CUTSCENE / INTRO_OUTRO contexts, never FIGHT.

## Rig target (IMPORTANT — differs from western-heart's cape-jones clips)

These clips target the **CapeJones_Rig** (94 bones, 0.925 m native, cape-jones
repo canon — `3d-assets/cape-jones-rig/RIG-DOCS.md`), the owner's actual Cape
Jones show mesh. They do NOT target western-heart's `cyborg-x.glb`
(160-joint T7 Alisa port) — that rig has its own clip set in western-heart
`anims/show/cape-jones/` (PR wh#849, open). Bone names differ; clips are not
interchangeable. This directory is the show test-ground copy.

## Clips

| Slot | File | Source motion | Frames @ fps | Baked |
|---|---|---|---|---|
| idle | `idle.glb` | CMU `140_06.bvh` ("Idle", 3563f @120fps; used f1–197, skip 0 step 4) | 50 @ 30 | 2026-10-24 |

### Idle re-cut (2026-10-24)

Previous idle cut (source f200–680, 121 frames, baked 2026-10-23) played as a crouch-lean hold (torso ~33°, knees 64–76°), because the source subject crouches from ~frame 200 onward and never stands back up. Re-cut from the upright portion (source f1–197, skip 0 step 4, 50 frames @ 30, baked 2026-10-24): measured torso pitch 2.0–3.5°, knees ~19–21°, loop start/end within 1.5° pitch. Render proof: `anims/show/cape-jones/proof/upright-frame25.png`. Full diagnosis: `docs/research/CAPE-IDLE-RECUT-2026-10-24.md`. The fix is a re-cut, not a re-rig; the skeleton, bone map, and retarget method verified sound.

## Motion source

- **CMU Graphics Lab Motion Capture Database** (`mocap.cs.cmu.edu`), via the
  BVH conversion mirror `una-dinosauria/cmu-mocap` (GitHub).
  File in-repo: `3d-assets/animation/mocap-cmu/140_06.bvh`
  (see `3d-assets/animation/mocap-cmu/MANIFEST.md`).
- License (verbatim CMU): "Use this data! This data is free for use in
  research and commercial projects worldwide." Attribution: "The data used in
  this project was obtained from mocap.cs.cmu.edu. The database was created
  with funding from NSF EIA-0196217."
- No hand-made or procedural animation. No fight movesets.

## Retarget method

- `tools/show-retarget/retarget_idle_cape.py` (committed) + bone map
  `tools/show-retarget/bonemap_cmu_to_capejones.json`.
- Rotation-delta retarget, parent-first, scale-safe (adapted from
  western-heart `tools/anim-retarget/retarget_rot.py`, proven on the
  cyborgx wave clip):
  `R_target_pose = (R_src_pose @ R_src_rest^-1) @ R_target_rest`
- Baked DIRECTLY onto deform bones (pelvis, spine_1/3, chest, neck_1/2,
  head, upperarm/forearm/hand, thigh/shin/foot/toe, thumb+index fingers) —
  the mesh is skinned to deform bones and FK→deform constraints do not
  survive GLB export, so the FK layer is bypassed for the baked clip.
- In-place (no root translation — idle). Source faces −Y, rig faces −Y
  (measured yaw 1.2°, negligible).
- Exported from a clean Blender session (factory settings): single armature
  + single action → one `show_idle` animation, 282 channels.
- Bind check on reimport against `3d-assets/cape-jones-rig/cape-jones-show.glb`:
  **940/940 fcurves bound** to the 94-bone rig.

## Model QA (2026-10-23)

- Weight audit (`tools/show-retarget/qa_weights.py` logic): 117,637
  head-region verts — dominant bones are head/jaw/neck/clavicle/chest;
  **0 verts dominated by spine/pelvis/lower** → PASS, no face-stretch bug.
- T-pose front/side renders: `shared/cast/proof/cape_tpose_front.png`,
  `shared/cast/proof/cape_tpose_side.png` (viewed).
- Moving proof: `shared/cast/proof/cape_idle_in_cape_room_v1.mp4`
  (Cape idling in the living room, Eevee) + checkframes PNG (viewed).
- Known exporter artifact: the model GLB carries a stray 24-vert `Cube`
  node at origin (same family as the documented Icosphere stray). Harmless:
  auto-hidden by the proof render script; does not affect skinning.

## Model export

- `3d-assets/cape-jones-rig/cape-jones-show.glb` — CapeJones_Rig (94) +
  CapeJones_Body + CapeJones_Cape, rest pose, skins, materials/textures.
  Exported from `3d-assets/living_room.blend` (never saved). The .blend is
  the source of truth; this GLB is the show pipeline's working copy.
## Episode 1 "Immortal Qombat" clips (2026-10-24, Track B)

Placement note (read first): the clips below depict the Episode 1 fight
scene AS IT APPEARS IN THE SHOW. They are show-scene clips, not game
movesets: they never drive gameplay, and they do not go into
western-heart. The show-anim law on this page ("show clips play in SHOW /
CUTSCENE / INTRO_OUTRO contexts, never FIGHT") is about game fights; the
Ep 1 fight scene is a show context (a scene inside the episode). If the
coordinator wants fight-scene clips housed elsewhere (e.g. a future
`anims/fight/` directory), these files move with no content change.

### Fight-scene clips (Cape) — T3 fallback, labeled

Source motion: decoded Tekken 3 motion (owner's disc teardown), gunjack
bank, `game/assets/anim/t3/` in western-heart (decoder
`teardown/tekken3/tools/local/pose_assemble.py + usa_motion.py`). Tekken
3 is the LOGGED FALLBACK ONLY: source priority is Tekken 5/6/7/TTT2, and
every clip below is on the T7 swap list (see below). Baked with the
world-space extrinsic retarget (`bake_cape_t3.py`, Track B work files):
`Wdes = (QG @ W @ QG^-1) @ RESTW`, pelvis location converted from
armature space to root-parent space. Exported armature-only, 30fps, one
animation per GLB, 282 channels (94 bones x 3), same convention as
`idle.glb`. Set scene fps to 30 BEFORE importing a clip GLB.

| Slot | File | Source motion | Frames @ fps | Baked |
| ---- | ---- | ------------- | ------------ | ----- |
| stance | `ep1_cape_stance.glb` | gunjack `t3_stance_b.json` (near-static held guard, NOT a bounce; re-baked 2026-10-24, direction-IK — see note below) | 108 @ 30 | 2026-10-24 |
| strike_light | `ep1_cape_strike_light.glb` | gunjack `t3_light.json` (move_row 119) — a 180-degree SPINNING strike, NOT a jab; ends turned 180 deg away | 22 @ 30 | 2026-10-24 |
| strike_heavy | `ep1_cape_strike_heavy.glb` | gunjack `t3_heavy.json` (move_row 370) — overhead/hook swing | 34 @ 30 | 2026-10-24 |
| hit | `ep1_cape_hit.glb` | gunjack `t3_hit.json` (stagger) | 21 @ 30 | 2026-10-24 |
| hit_launch | `ep1_cape_hit_launch.glb` | gunjack `t3_hit_launch.json` (airborne tumble; frames 15+ drive the pelvis below ground — the paired choreography uses frames 0-14 only) | 25 @ 30 | 2026-10-24 |
| ko | `ep1_cape_ko.glb` | gunjack `t3_ko.json` (flat on back/side, on the ground plane, no sinking) | 40 @ 30 | 2026-10-24 |

### Stance re-bake (2026-10-24)

The first bake of `ep1_cape_stance.glb` (orientation retarget, `tools/show/bake_cape_t3.py`) played one arm down and one arm up (L upper 17–31° from down, R upper 130–144°), while the source guard has both arms raised. Re-baked with direction-IK (`tools/show/bake_stance_ik.py`): arm segment directions taken from motion-chain FK of the source, torso/legs kept on the orientation bake (which already matched source tilt/roll). Verified by measurement: the new clip matches source FK to ~1° on sampled frames (L upper ~45–49°, L fore ~149–156°, R upper ~57–67°, R fore ~111–125°; torso ~25°, shoulders rolled left-low). A segment-correct orientation map was also tested and did NOT fix it, so it was not shipped.

Fingers, clavicles, and FK/IK layers stay at rest in these bakes (the T3
source has no finger channels). Fingers stay open during grabs: a
fist-curl pass is future polish, not blocking.

### Living-room clips (Cape)

| Slot | File | Source motion | Frames @ fps | Baked |
| ---- | ---- | ------------- | ------------ | ----- |
| channel_flip | `ep1_cape_channel_flip.glb` | CMU `13_05.bvh` (sit, hands against chin, fidget), source frames 600-1200 @120fps -> 151 @ 30, same CMU retarget as idle (pelvis parent-space conversion fixed) + procedural overlay: right-arm remote point (f10-25 ease-in, held, f135-150 release), head turns + right-hand thumb wags at beats f45/f85/f120 | 151 @ 30 | 2026-10-24 |
| portal_flight | `ep1_cape_portal_flight.glb` | Seated hold sampled from `ep1_cape_channel_flip` frame 0 + procedural stand (slerp to stance, f15-34) + procedural flight (pelvis accelerates -Y 3.2 m + rises 0.35 m, body pitches to 70 deg superman, arms swept back, f35-94) + procedural land (pitch back to 0, crouch: thighs Rx-55 deg, shins vertical, feet flat, f95-114) + crouch hold (f115-124). No mocap source exists for being pulled through a TV. Cape streaming is the cloth lane's job — this clip moves the BODY only. | 125 @ 30 | 2026-10-24 |

Known staging note (channel_flip / portal_flight): the CMU sit comes from
a stepstool sit, so the feet dangle (toes z ~0.24-0.28) past the
recliner's extended footrest instead of resting on it. The seat itself
(pelvis at butt_target) is correct; footrest contact is a polish item
for the sit pass.

### LED gag (production script, not a skeletal clip)

`tools/show/led_gag.py` keys `LEDStripMat`'s Principled Emission Color
(canon violet `#731AE5`) and Emission Strength @30fps: steady 1.0
(f0-29), flicker 1.0/0.1/1.0/0.2/1.0/0.1/1.0 (f30-41), slow pulse
0.7-1.0 sine (f42-89), dropout 0.05 (f90-104 — he notices, does NOT fix
it), steady 1.0 (f105+). The material previously had NO emission
channel (dark gray Principled only); the gag script ADDS the emission.
Single shared material, so all three strips animate together.

### T7 swap list (these T3-fallback clips get replaced, not kept)

- Cape: hand-cannon strike `.bin`s (especially a true jab to replace or
  supplement the spinning `t3_light` if the owner wants a non-spin
  strike), via TKMovesets2 extraction -> BlenderTekkenAnimationImporter
  triage -> bake -> GLB (same convention, fps 30 before import).
- General: any T7 animation that supersedes a T3 fallback clip.
- Pull lane: T7/DepotDownloader (Grok's box). The importer addon has NO
  license file (all rights reserved by default) — do NOT vendor it into
  the repo; use it as a tool only.

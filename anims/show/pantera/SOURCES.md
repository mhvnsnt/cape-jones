# SOURCES — anims/show/pantera/ (show clips for Pantera)

Show-context clips ONLY. Never game movesets — the same show-anim law as
`anims/show/cape-jones/SOURCES.md` holds: show clips play in SHOW /
CUTSCENE / INTRO_OUTRO contexts, never in game fights. The Episode 1
fight-scene clips below depict the fight AS IT APPEARS IN THE SHOW; they
do not drive gameplay and do not go into western-heart. (Placement
tension, flagged for the coordinator: if fight-scene clips belong in a
future `anims/fight/` directory instead of `anims/show/`, these files
move with no content change.)

## Rig target

- Pantera show rig: 53 joints + `Character` root node, from
  `pantera-leopard-king.glb` (Tripo model, best on roster). Joints:
  Hips, Spine, Spine1, Spine2, Neck, Head, Left/Right Shoulder/Arm/
  ForeArm/Hand, fingers (thumb 2 segments left / 3 right — asymmetric:
  RightHandThumb3 present, LeftHandThumb3 missing), Left/Right UpLeg/
  Leg/Foot/ToeBase, Tail1-4.
- Orientation (measured): the GLB imports lying along -Y (file Z-up
  baked; Blender import conversion is (x,y,z)_file -> (x,-z,y)_Blender).
  Up = -Y, forward = -Z (toe direction). Standing fix: rotate the
  armature object by Rx(-90 deg) -> up becomes +Z, forward becomes -Y
  (matching Cape). Then shift feet to z=0 and scale to 1.8 m for proof
  framing.
- Audit notes (2026-10-23): 964,668 verts, 0 not-normalized, 0
  influences >4. Suspicious weights: leg weighted to TAIL 366, core
  weighted to TAIL 799, tail weighted to CORE 35. Stray `Cube` /
  `Icosphere` meshes (same family as Cape's documented stray).
- NOT the game runtime rig: `pantera_rigged.glb` (13 joints) is a
  simplified game rig, not the show rig. Do not use it for show clips.

## Clips

| Slot | File | Source motion | Frames @ fps | Baked |
| ---- | ---- | ------------- | ------------ | ----- |
| stance | `ep1_pantera_stance.glb` | `T3Stance` action extracted EXACTLY from `pantera-leopard-king.glb` (frames 0-74). Frame 0 is a deep crouch (hips -0.53); frames 30+ are a standing guard. | 75 @ 30 | 2026-10-24 |
| grab | `ep1_pantera_grab.glb` | `T3Grab` action extracted EXACTLY from `pantera-leopard-king.glb` (frames 0-34). Suplex/backdrop-style throw: crouch-in, lift (hips to ~1.46 m, ~1 m forward travel), slam, ends WITH the victim on the ground (attacker goes down too). | 35 @ 30 | 2026-10-24 |

Method: exact GLB action extraction (one clean Blender session per
clip), NO re-derivation. An earlier attempt to re-derive Pantera clips
from T3 JSON motion (world-space fit over all 24 cube rotations) FAILED
for all candidates (best mean error 0.656 m) and was abandoned: the prior
game-side GLB bake used a different (local-copy/hybrid) method that was
not reverse-engineered. Do not retry the JSON fit as-is.
Exported armature-only, 30fps, one animation per GLB, 159 channels.
Internal GLB action names remain `T3Stance` / `T3Grab` (cosmetic only;
file names carry the show convention and document the source).
Set scene fps to 30 BEFORE importing a clip GLB.

Fingers stay open during grabs (the T3 source has no finger channels).
A fist-curl pass is future polish, not blocking.

## What is NOT in hand (T7 swap list)

- Pantera: strike clips (light/heavy), hit-reaction clips, win-pose
  clips, per-stage chain-throw `.bin`s (the full multi-stage chain, not
  just the single T3 grab). King JSON `t3_win_lk/lp/rk/rp` exist but were
  NOT converted (mirrored-frame risk, unvalidated) — they belong on the
  swap list, not as silent T3 conversions.
- Pantera's comeback "one hit from death" is a health/edit state, not an
  animation clip. Staging conveys it by order (Cape strikes first,
  Pantera still standing, then Pantera's grab wins). A Pantera stagger
  can only be staged at edit level (scene-level recoil/translation)
  unless a future clip is made — no stagger clip is invented here.
- Pull lane: T7/DepotDownloader (Grok's box), TKMovesets2 extraction ->
  BlenderTekkenAnimationImporter triage (no-license addon: tool use
  only, do NOT vendor into the repo) -> bake -> GLB, same convention.

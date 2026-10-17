# DONOR ANIMATION LIBRARY — Cape Jones retarget sources

**Owner directive 2026-10-17:** pull fighting-game animations from the Western Heart
repo (`mhvnsnt/western-heart`) into cape-jones as **donor** animations for
retargeting to Cape Jones's 85-bone rig. **Steal-like-an-artist law applies:**
study and adapt the technique — these are motion donors, never shipped as-is.

## What's here

### `king-t3/` — King (Tekken 3), REAL decoded motion
31 clips in `wh-anim/1` JSON format: per-bone quaternion rotations
(`rot_xyzw`), 23-bone skeleton (Root/Hips/Spine/Chest/Neck/Head/arms/legs),
30fps, decoded from the owner's Tekken 3 disc teardown
(`teardown/tekken3/animations/divmot03_king.bin`, slot 0xd06) via
`teardown/tekken3/tools/local/pose_assemble.py + usa_motion.py`.

Clips: stances (a/b/c), walks (fwd/back, a/b), backdash, dash_fwd, sidesteps
(a–d), crouch (+hold), block (a/b), light/medium/heavy strikes, grab,
hit, hit_launch, jumps (fwd/back/up), ko, win poses (lk/lp/rk/rp).

**Retarget status:** proven path — `teardown/wwf-no-mercy/aki_to_tekken3.py`
retargets AKI clips to Tekken skeletons (proven on King).

### `gunjack-t3/` — Gun Jack (Tekken 3)
- `t3_gunjack.glb` — model + **11 embedded animations**: idle, walk_fwd,
  walk_back, light, medium, heavy, grab, hit, block, ko (+1). 20 nodes,
  1 skin.
- `moveset_gunjack.json` — full 391-move frame-data set from the T3 teardown
  (startup/active/recovery/damage per move).
- `gunjack_moves.json` — game-ready move summary (damage scaled T3 170HP → 100HP).

**Note:** the raw `divmot16_gunjack.bin` motion bank exists in Western Heart
but is not yet decoded to `wh-anim/1` JSON like King's. The same
`t3_motion_bake.py` pipeline that decoded King applies — flagged as
follow-up decode work.

### `cmu-mocap-fighting/` — CMU mocap, fighting set
16 `.bvh` clips (standard BVH, directly importable in Blender):
135_04, 135_07, 135_09, 135_11, 13_17, 143_23, 143_24, 144_05, 144_07,
144_09, 144_13, 144_20, 144_26, 14_01, 17_10, 86_06.

### `no-mercy-donor/` — WWF No Mercy (AKI engine), curated donor subset
NPY int16 clips, shape `(nframes, 26, 3)`, AKI 26-joint layout.
Format doc: `FORMAT.md` (copied from
`teardown/wwf-no-mercy/animations/FORMAT.md`).
Clip manifest: `moveset-library/animations/ANIMATION-INDEX.json` in
Western Heart (13 categories, 5,932 clips total).

Pulled so far (695 npy clips — strikes 476/734, stances 107/193,
walks 21/193, taunts 11/194, weapons 80/735):
- `clips/anim_*.npy` — No Mercy clips

Still pending (blobs unavailable from the local partial clone; needs a
follow-up pull): remaining ~1,354 npy clips, the 56 WMXIX JSON clips
(`teardown/wmxix/animations/*.json`, 70-bone Yukes skeleton), and
`teardown/wwf-no-mercy/animations/FORMAT.md` (read it in Western Heart
in the meantime).

**Retarget status:** AKI→Tekken3 proven via `aki_to_tekken3.py`.

## HONEST GAPS — what the owner asked for that is NOT here

1. **ALISA (Tekken robot): NOT IN WESTERN HEART.** Only
   `docs/t7t8-reference/frame-data/alisa.json` (frame data, no motion).
   Tekken 7 was never fully acquired ("Full game never acquired. Individual
   model rips have no animation data."). Her weapon-arm/weapon-hand
   animations do not exist in the repo. **Needs a new acquisition lane.**
2. **Gun Jack ARM-BLAST:** no dedicated arm-cannon blast animation found.
   The 11 GLB anims cover strikes but none is the blast motion. The raw
   divmot16 bank (391 moves in the moveset JSON) likely contains it —
   needs the decode pass.
3. **Urban Reign:** `teardown/urban-reign/ppks/` holds raw PPK motion pools
   (`general_normal/30frame/weapon.gyu` + `gyuindex.bin`) — "Inner Namco
   chunk decode needs binary RE." Not usable yet.
4. **Def Jam FFNY:** motion bank `MOTION/WRES_ALL.VIV` (64MB, wres001–wres141)
   was never extracted into the repo — only findings docs
   (`ANIMATION-FINDINGS.md`, `EAGL-FORMAT-ANALYSIS.md`) and the move
   database `MAIN_ALL.DAT`. Needs an extraction lane.
5. **Tekken 6:** animation data locked behind PSP encryption (46 ending
   cinematics extracted, not moves).
6. **No Mercy remainder:** this pull is the curated subset (strikes, stances,
   walks, taunts, weapons). The full 5,787-clip library (grapples,
   submissions, high-flying, etc.) stays in Western Heart.

## Provenance
All files pulled from `mhvnsnt/western-heart` `origin/main`
(post PR #231 full restore, merged 2026-10-17). Original paths recorded
per folder above. Donor use only.

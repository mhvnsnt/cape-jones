# Functional Recliner — `recliner_rigged.blend`

Living Room Scene Wave, Lane 2 (owner directive 2026-10-17 ~20:51 CDT):
"The chair needs to actually be functional — to open up and close and all of that."

## What this is

A standalone library blend containing the living-room recliner (`loungeChairRelax`)
rebuilt as an articulated, animated mechanism. It is **not** a modified
`living_room.blend` — an integration lane will link/append this into the scene later.

## Source mesh analysis

`loungeChairRelax(Clone)` in `3d-assets/living_room.blend` is **one merged mesh**
(308 verts / 188 faces, three materials). It is not made of clean part islands —
it separates into ~60 loose single-quad panels — so parts were classified
geometrically (chair-local frame: x = width 0..0.49, y = depth 0..0.675,
z = height 0..0.63; front = −Y side, back = +Y side):

| Part | Object | Islands | Verts | Contents |
|---|---|---|---|---|
| Seat base | `recliner_base` | 8 | 66 | seat body, front/back/bottom faces, cushion, trim ledge |
| Backrest | `recliner_backrest` | 9 | 38 | backrest slab (y 0.525..0.675, z 0.37..0.63) |
| Footrest shank | `recliner_footrest_link` | 4 | 24 | folded shank panels under seat front |
| Footrest pad | `recliner_footrest_pad` | 11 | 56 | foot box (5 carpet islands) + metal linkage brackets (6) |
| Armrest L/R | `recliner_armrest_L/R` | 4+4 | 22+22 | side armrest panels (static) |
| Legs | `recliner_legs` | 20 | 80 | 4 wooden legs (static) |

Totals: 308 verts / 188 faces — **byte-identical geometry to the source mesh**,
zero shape change. Parts were joined from the separated islands, never remodeled.

## Mechanism (armature `recliner_rig`)

Bones lie **along** their hinge axes (chair-local X), so articulation is a pure
rotation about each bone's local Y:

| Bone | Hinge (chair-local) | Motion at `recline`=1 |
|---|---|---|
| `root` | — | static (base, legs, armrests parented here) |
| `backrest` | (y 0.56, z 0.38) | −26° (top tips backward) |
| `footrest` (shank) | (y 0.205, z 0.23) | −50° (swings forward/out) |
| `footrest_pad` (child of shank) | (y 0.20, z 0.12, at the fold) | +50° counter-rotation → pad stays **level** while deploying, like a real recliner parallel linkage |

**Single control:** custom property `recline` on the armature, 0 = closed, 1 = fully
open. Three scripted drivers map it to the bone rotations above.

**Animation:** action `ReclinerOpen`, frames 1–24: `recline` 0 → 1 (BEZIER ease).
Scrub the timeline or the property to pose; the mechanism is live.

## Canon guarantees

- **Placement:** armature carries the exact source transform —
  location (2.653, 2.312, 0), rotation Z 270° (4.7124 rad). Closed-state world
  bbox matches the original chair bbox exactly. The chair never moves.
- **Colorway LOCKED:** the original material datablocks are reused unchanged —
  `carpet` coral pink #F15E57 (0.943, 0.367, 0.343), `metal`, `wood`. Zero color edits.
- **Footprint:** base, legs, armrests are static; only backrest + footrest articulate.
- **No interpenetration:** moving parts were swept through recline 0→1; the
  footrest deploys forward of the seat front face and the reclined backrest
  clears the armrests (verified in renders, `renders/`).

## Verification

Own-eyes Cycles renders (640×480) of closed / half-open / fully-open from two
angles (front 3/4, side): `renders/recliner_{closed,half,open}_{front34,side}.png`.

Driver evaluation (frame → recline → bone angles, radians):

| frame | recline | backrest | shank | pad |
|---|---|---|---|---|
| 1 | 0.0 | 0.0 | 0.0 | 0.0 |
| 12 | 0.467 | −0.212 | −0.408 | +0.408 |
| 24 | 1.0 | −0.454 | −0.873 | +0.873 |

## Use

In the integration lane: File → Link → `recliner_rigged.blend` → Collection →
`Recliner`. It drops in at canon placement. Animate `recline` (or play 1–24).

Build script (reproducible): `/tmp/build_recliner_rig.py` was the working copy;
the final parameters are recorded in this doc. To rebuild from scratch, separate
`loungeChairRelax(Clone)` by loose parts, classify per the table above, join,
create the armature per the bone table, add the `recline` property + drivers +
24-frame action, bone-parent the parts, and save.

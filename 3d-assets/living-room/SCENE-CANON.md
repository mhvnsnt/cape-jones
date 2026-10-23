# Cape Jones — Living Room SCENE CANON
**Owner-approved 2026-10-16.** This document is the single source of truth for the 3D living room scene
(`3d-assets/living_room.blend`, from `3d-assets/living-room/`). Every color, material, and furniture piece
below is LOCKED. Future builds must match this colorway exactly — change requires owner sign-off.

Visual anchors:
- `colorway-reference.png` — owner-approved preview (front view).
- `scene-overview.png` — second viewpoint (3/4 view from the open front side).

> NOTE (owner 2026-10-16): furniture placement will be re-staged against his 2D layout reference in a
> later lane. The COLORS below are canon regardless of placement. Do NOT place the Cape Jones character
> in the room yet — the recliner stays empty until the light-flicker gag rig lands.

## 1. Palette (hex from Principled BSDF Base Color)

| Material | Hex | Used on |
|---|---|---|
| `carpet` (chair upholstery) | `#F15E57` | lounge chair (coral pink) |
| `carpet.001` (rug field) | `#F15E57` | round rug |
| `carpetBlue` | `#5B84DD` | sofa upholstery |
| `carpetDarker` | `#9B4C49` | rug ring trim |
| `wood` / `wood.001` / `wood.002` / `wood.003` | `#E59964` | chair frame, coffee table, TV cabinet, bookcase (warm oak) |
| `metal` / `metal.001` / `metal.002` / `metal.003` | `#BDD2D6` | chair base, sofa frame, lamp poles (cool silver) |
| `WallMat` | `#D1C7B8` | all three walls (warm bone) |
| `FloorMat` | `#735238` | floor (dark warm brown) |
| `lamp` / `lamp.001` | `#FFE996` | lamp shades (warm amber) |
| `RemoteMat` | `#0D0D0D` | LED remote body |
| `LEDStripMat` base | `#1A1A1A` | LED strip housings |

### Emission accents (the signature glow)

| Material | Emission hex | Strength | Used on |
|---|---|---|---|
| `LEDStripMat` | `#731AE5` (violet-purple) | 4.0 | LED_Back / LED_Left / LED_Right strips — this casts the purple wash over the whole room |
| `BtnMat_0` | `#FF0000` | 1.5 | remote button |
| `BtnMat_1` | `#00FF00` | 1.5 | remote button |
| `BtnMat_2` | `#0000FF` | 1.5 | remote button |
| `BtnMat_3` | `#FFFF00` | 1.5 | remote button |
| `BtnMat_4` | `#FF00FF` | 1.5 | remote button |
| `BtnMat_5` | `#00FFFF` | 1.5 | remote button |

### Lighting
- `RoomLight` — POINT light, energy 300, color `#731AE5` (matches the LED violet), shadows ON. This is the
  dominant light: everything in the room reads pink/purple because of it.
- `Sun` — SUN light, energy 1.5, color `#FFFFFF`, shadows ON. Fill only.
- World background: `#0D0D0D` (near-black; seen through no openings — room is enclosed on 3 sides).

**The look in one line:** coral-pink furniture + warm oak wood on a dark floor, all soaked in violet
LED glow (`#731AE5`). That's the canon. Protect it.

## 2. Furniture inventory (positions = post-relayout 2026-10-16, branch build/living-room-relayout)

Room shell: floor 7.0 × 6.0 m; walls 3.0 m high (back wall at y=3.0, left/right at x=±3.5).
Layout contract: `3d-assets/living_room_layout.json` (validated with
`tools/layout-rules/validate_layout.py` — 8 items, all checks passed).
Positions below are Blender coords (x right, y depth, z up).

| Object | Type | Size W×D×H (m) | Position (x, y, z) | Material(s) |
|---|---|---|---|---|
| `loungeChairRelax(Clone)` | recliner chair | 0.49 × 0.675 × 0.63 | REV2: (3.14, 1.5, 0), rot 90° facing -x into room, back against window wall | metal, carpet, wood |
| `loungeDesignSofa(Clone)` | sofa | 1.12 × 0.41 × 0.4 | (-2.9, -0.6, 0), rot -90° facing +x | carpetBlue, metal.001 |
| `tableCoffee(Clone)` | coffee table | 0.661 × 0.4 × 0.23 | (-0.2, 0.4, 0) | wood.001 |
| `rugRound(Clone)` | round rug | 1.472 × 0.016 | REV2: (2.7, 1.5, 0.01), under recliner at window wall | carpet.001, carpetDarker |
| `cabinetTelevision(Clone)` | TV stand, open-shelf console (rebuilt 2026-10-16) | 0.8 × 0.3 × 0.75 | (-0.9, 2.6, 0) | wood.002 |
| `crt_tv` + `crt_screen` + `antenna_0/1` | CRT TV, violet screen, rabbit ears | 0.62 × 0.42 × 0.52 | (-0.9, 2.6, 1.01) | RemoteMat, tvScreenMat, metal |
| `vcr_dvd` | VCR/DVD player (middle shelf) | 0.42 × 0.24 × 0.09 | (-1.02, 2.6, 0.51) | RemoteMat |
| `box_a` … `box_d` | storage boxes (shelves) | various | on stand shelves | wood.002 |
| `monster_body` + eyes + feet | monster toy, canon-blue (bottom shelf) | ~0.14 tall | (-0.92, 2.58, 0.22) | carpetBlue, lamp |
| `side_table` + 3 legs | round side table | r 0.175, h 0.55 | REV2: (2.9, 0.95, 0.55), left of recliner at window wall | carpetBlue |
| `okayest_hero_mug` + handle + `mug_text` | WORLD'S OKAYEST HERO mug | r 0.045, h 0.1 | REV2: world (2.9, 0.95, 0.618), centered + fully supported on tabletop (close-up verified) | WallMat, RemoteMat |
| `bookcaseClosed(Clone)` | bookcase | 0.4 × 0.25 × 0.85 | (-2.95, -1.8, 0) | wood.003 |
| `lampRoundFloor(Clone)` | floor lamp | 0.152 × 0.176 × 0.86 | (3.0, 2.5, 0) | metal.002, lamp |
| `lampSquareTable(Clone)` | table lamp (re-seated on coffee table) | 0.12³ | (-0.02, 0.4, 0.23) | lamp.001, metal.003 |
| `LEDRemote` + `RemoteBtn_0..5` | LED remote (re-seated on coffee table) | tiny | (-0.32, 0.45, 0.245) | RemoteMat, BtnMat_* |
| `door_jamb_L/R` + `door_lintel` | doorway frame, back wall | opening 0.9 × 2.1 | (-2.6, 3.0, ~1.05) | wood.002 |
| `hallway` (floor / walls / end / door) | hallway stub behind doorway | 1.3 × 2.6 | (-2.6, 4.3, 0) | FloorMat, WallMat, RemoteMat |
| `HallLight` | POINT light, energy 60, `#FFE996` | — | (-2.6, 4.4, 2.2) | — |
| `window_unit` (jambs / head / sill / mullions) | window, right wall | opening 1.4 × 1.1 | (3.5, 1.5, 1.6) | wood.002 |
| `exterior` (sky / sun / trees / baffles) | exterior diorama | — | x 4.4–5.4 | skyMat, lamp, FloorMat, canopyMat |
| `wall_decor` → `poster_*` | FRY EM UP poster | 0.5 × 0.66 | (-1.7, 2.92, 1.9) | WallMat, wood.002, carpet |
| `wall_decor` → `squid_*` | squid wall hanging | ~0.2 tall | (-0.9, 2.87, 2.02) | carpetBlue, lamp |
| `wall_decor` → `ghost_*` | framed ghost picture | 0.5 × 0.6 | (0.5, 2.92, 1.9) | wood.002, lamp, carpet |
| `LED_Back` / `LED_Left` / `LED_Right` | LED strips | — | unchanged | LEDStripMat |
| `Floor` / `WallBack` / `WallLeft` / `WallRight` | room shell (door+window holes cut) | — | — | FloorMat / WallMat |
| `Ceiling` | roof/ceiling (REV2) | 7.0 × 6.0 plane at z=3.0, normal down | (0, 0, 3.0) | WallMat |
| `CapeJones_ScaleCheck` | Cape Jones, STANDING (REV2, temporary scale check) | 0.925 tall | (-0.5, -1.0, 0.462), facing MainCam | tripo PBR (as-generated, NOT recolored) |

### Cape Jones character canon (owner 2026-10-16)
- Official 3D model: https://studio.tripo3d.ai/3d-model/67a6f309-0ac2-4c56-92b8-a4ea3e72bf46
  (Tripo 3D, 17MB, full PBR textures). Local recovery: `~/workspace/tripo-recovery/cape_jones.glb`
  (meshopt-compressed; Blender 4.0.2 can't read EXT_meshopt_compression — transcode to plain
  GLB with gltf-transform before import).
- Who he is: a Space Ghost/Batman-type fighter who does NOT want to fight or be a hero — he only
  does it because everyone thinks he looks like a superhero and either wants his help or wants
  to fight him. Hand cannons like Mega Man and Android 16. The model fits his bio/vibe/moveset.
- Render direction for scale checks: standing in the room FACING THE CAMERA.
- Native model height: 0.925 m (stylized). Do NOT rescale without owner sign-off.

Recliner stays EMPTY — no character placed (light-flicker gag rig lands later).

### New materials (all reuse locked canon hexes — no new colors)
- `tvScreenMat`: emission `#731AE5` strength 1.5 (same violet as the LED strips)
- `skyMat`: base + emission `#5B84DD` strength 0.5 (same blue as the sofa)
- `canopyMat`: base + emission `#F15E57` strength 0.45 (same coral as the chair)

### Documented color substitutions (palette had no match — owner judges the render)
- Side table: canon blue `#5B84DD` (no purple surface in palette; violet LED wash reads it purple)
- Monster toy: canon blue `#5B84DD` (no green in palette)
- Flowering-tree canopies: canon coral `#F15E57` (no green in palette)

Mesh count: 22 meshes + 2 lights + `MainCam` + `Camera.001` (scene cameras) + `CamTarget`.

## 3. Render settings (as shipped)
- Engine: Cycles (CPU), 64 samples
- Resolution: 960 × 540
- Frames: 1–360 (15 s @ 24 fps)
- Film transparent: OFF; color mode RGBA

## 4. Change log
- 2026-10-16: Revision 3 (branch build/living-room-rev3-20261016, owner-directed fixes).
  (1) Table lamp: moved away from the window, fully onto the coffee tabletop — lamp bbox
  x -0.35–-0.23 vs tabletop x -0.661–0.0 (no overhang; was overhanging +x edge by 0.10m).
  Close-up render-checked (`scene-rev3-lamp-closeup.png`). (2) Chair rotation: the recliner
  was facing +x (INTO the wall) at 90deg yaw — CAUGHT the quaternion trap (rotation_mode was
  QUATERNION, euler edits silently ignored), set rotation_mode='XYZ', rotated to 225deg
  yaw (-45deg from straight-into-room) so it faces (-0.707, +0.707): into the room, angled
  toward the TV/conversation zone, backrest toward the wall. (3) Wall clipping fixed with
  real bounds math: chair bbox xmax 3.341 vs WallRight inner face 3.425 (8.4cm clear; was
  3.63, THROUGH the wall); rug re-centered, bbox xmax 3.286 (13.9cm clear; was 4.172,
  THROUGH the wall). Layout re-validated: 8 items, all checks passed. Verified by eye:
  `scene-rev3-window-wall.png`. Zero color changes. Cape Jones model untouched (separate
  rigging lane owns him; native 0.925m scale locked per owner).
- 2026-10-16: Revision 2 (branch build/living-room-rev2-20261016, owner-directed). (1) Moved pink
  recliner + round rug + side table + mug to the RIGHT WINDOW WALL — chair back against the wall
  under the window, facing into the room; recliner now an accent seat (secondary: true in
  living_room_layout.json; validator's side-table rule widened to measure against any seat).
  Layout re-validated: 8 items, all checks passed. (2) Mug fix: mug was parented to the side
  table with keep-transform — moving both double-moved the mug/legs. Reverted children to
  original local coords; mug now verified centered and fully supported on the tabletop
  (world z 0.568 = tabletop 0.567), close-up render-checked. (3) Added Ceiling: 7x6m plane at
  z=3.0, WallMat, normal facing down. (4) Cape Jones scale check: imported cape_jones.glb
  (Tripo3D project 67a6f309, owner's model; transcoded meshopt->plain via gltf-transform since
  Blender 4.0.2 can't read EXT_meshopt_compression) as `CapeJones_ScaleCheck`, standing at
  (-0.5, -1.0), feet on floor, facing MainCam. Native height 0.925m (stylized). STAYS STANDING —
  chair sit comes later with the light-flicker gag. Zero color changes.
- 2026-10-16: Canon locked from `living_room.blend` (PR: canon/living-room-colorway-20261016).
  Colors extracted headless from Principled BSDF nodes, owner-approved preview saved as
  `colorway-reference.png`, second angle saved as `scene-overview.png`. No scene geometry changed.
- 2026-10-16: Full re-layout (branch build/living-room-relayout-20261016). Furniture placed per
  `living_room_layout.json` (validated: 8 items, all layout-rules checks passed). Added: CRT TV +
  rabbit ears, open-shelf TV console (rebuilt), VCR/DVD, boxes, blue monster toy, round side table,
  WORLD'S OKAYEST HERO mug, doorway + hallway stub, window + exterior diorama (sky/sun/flowering
  trees), wall decor (FRY EM UP poster, squid, ghost picture). Re-seated table lamp + LED remote on
  coffee table. Zero color changes — 3 new materials reuse locked hexes only. Render:
  `scene-relayout-v2.png` (960×540, 64 samples, verified by eye).

## DEFAULT LIGHTING & SETUP (owner-locked 2026-10-16 — this is the default look)

Extracted headless from `living_room.blend` on main. This lighting is CANON — do not change
it without owner approval.

| Light | Type | Color | Energy | Location |
|---|---|---|---|---|
| RoomLight | Point | violet (0.45, 0.10, 0.90) ≈ #731AE5 | 300 | (0.0, 0.0, 2.4) |
| Sun | Sun | white (1.0, 1.0, 1.0) | 1.5 | (2.0, -4.0, 5.0) |
| HallLight | Point | warm (1.0, 0.914, 0.588) | 60 | (-2.6, 4.4, 2.2) — hallway stub |

- LED strips (LED_Back / LED_Left / LED_Right): violet #731AE5 emission, strength 4.0 —
  the signature purple wash soaking the room. Ceiling carries the strip treatment too.
- World: dark background (0.051, 0.051, 0.051).
- Render: Cycles, 960×540 @ 50%, 24 samples, film transparent OFF, frames 1–360.
- The violet RoomLight + LED wash is what makes the pink furniture read the way it does —
  changing light color or energy changes the whole colorway. Hands off.

## 5. Furniture positions (owner 2026-10-18 ~10:10 CDT)

Two saved TV/shelf layouts. Both restorable via
`3d-assets/living-room/apply_furniture_position.py`
(transforms in `3d-assets/living-room/furniture_positions.json`).
The chair NEVER moves (canon placement locked per sit-targets).

- **POSITION 1 — backs against the wall (DEFAULT).** TV console un-rotated
  (screen faces -Y/south into the room), back flush to WallBack.
  Bookcase back flush to WallBack, west of the TV. Owner: "the back of the TV
  and the back of the shelf was against the wall I liked that better."
- **POSITION 2 — TV and shelf facing the chair (walkthrough video layout).**
  TV console yaw 84.5 deg (screen faces +X/east toward the chair); bookcase
  in the southwest at (-2.95, -1.8). Exact 2026-10-18 walkthrough video
  layout. Usable alternate — "we can always go back to [it]."

**TV-PARALLEL GAG (owner 2026-10-18):** the TV plays where WE (camera/audience)
can see it, but he sits off to the side not really watching it — "TV parallel."
He looks toward the TV/table direction of the room, but the TV is not facing
him. That is the joke.

**CHARACTER SITTING CORRECTION (owner 2026-10-18 ~10:11 CDT):** he caught the
walkthrough video with the character STANDING IN T-POSE INSIDE the chair
(clipped through geometry). He must be SITTING in the chair (on it, not inside
it), facing toward the TV/table direction (not the camera), out of T-pose,
breathing. Fixed via `3d-assets/living-room/render_sitting_preview.py`
(sitting pose library + 48-frame breathing layered in NLA).

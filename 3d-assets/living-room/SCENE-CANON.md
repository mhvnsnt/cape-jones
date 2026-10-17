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

## 2. Furniture inventory (positions = pre-rerelayout, recorded for reference)

Room shell: floor 7.0 × 6.0 m; walls 3.0 m high (back wall at y=3.0, left/right at x=±3.5).

| Object | Type | Size W×D×H (m) | Position (x, y, z) | Material(s) |
|---|---|---|---|---|
| `loungeChairRelax(Clone)` | recliner chair | 0.49 × 0.675 × 0.63 | (-1.1, 0.4, 0) | metal, carpet, wood |
| `loungeDesignSofa(Clone)` | sofa | 1.12 × 0.41 × 0.4 | (1.9, 0.4, 0) | carpetBlue, metal.001 |
| `tableCoffee(Clone)` | coffee table | 0.661 × 0.4 × 0.23 | (0.4, 1.3, 0) | wood.001 |
| `rugRound(Clone)` | round rug | 1.472 × 1.472 × 0.016 | (0.4, 0.9, 0.01) | carpet.001, carpetDarker |
| `cabinetTelevision(Clone)` | TV cabinet | 0.8 × 0.25 × 0.31 | (0.4, 2.55, 0) | wood.002 |
| `bookcaseClosed(Clone)` | bookcase | 0.4 × 0.25 × 0.85 | (-2.9, 2.5, 0) | wood.003 |
| `lampRoundFloor(Clone)` | floor lamp | 0.152 × 0.176 × 0.86 | (2.9, 2.5, 0) | metal.002, lamp |
| `lampSquareTable(Clone)` | table lamp | 0.12 × 0.12 × 0.29 | (0.9, 1.3, 0.42) | lamp.001, metal.003 |
| `LEDRemote` | remote | 0.035 × 0.11 × 0.02 | (0.15, 1.15, 0.5) | RemoteMat |
| `RemoteBtn_0..5` | 6 remote buttons | tiny | (0.155, 1.28, 0.51) | BtnMat_0..5 |
| `LED_Back` | LED strip | 3.4 × 0.04 × 0.04 | (0, 2.9, 2.75) | LEDStripMat |
| `LED_Left` | LED strip | 0.04 × 2.9 × 0.04 | (-3.4, 0, 2.75) | LEDStripMat |
| `LED_Right` | LED strip | 0.04 × 2.9 × 0.04 | (3.4, 0, 2.75) | LEDStripMat |
| `Floor` / `WallBack` / `WallLeft` / `WallRight` | room shell | — | — | FloorMat / WallMat |

Mesh count: 22 meshes + 2 lights + `MainCam` + `Camera.001` (scene cameras) + `CamTarget`.

## 3. Render settings (as shipped)
- Engine: Cycles (CPU), 64 samples
- Resolution: 960 × 540
- Frames: 1–360 (15 s @ 24 fps)
- Film transparent: OFF; color mode RGBA

## 4. Change log
- 2026-10-16: Canon locked from `living_room.blend` (PR: canon/living-room-colorway-20261016).
  Colors extracted headless from Principled BSDF nodes, owner-approved preview saved as
  `colorway-reference.png`, second angle saved as `scene-overview.png`. No scene geometry changed.

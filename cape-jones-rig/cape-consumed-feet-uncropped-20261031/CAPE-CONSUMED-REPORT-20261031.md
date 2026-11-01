# CAPE CONSUMED — feet uncropped + Feet Front Facing Engulfed variant
2026-10-31. Mars ordered 2026-10-31 21:26 CDT, replying to
future-symbiote-contact-20261031.png.

## Name lock
- The all-black variant is **CAPE CONSUMED**. That name is locked here.
- The cropped version Mars saw is saved separately as
  **FEET FRONT FACING ENGULFED** — a variant name, NOT the main version.
- FUTURE ONLY, NOT V2, NOT canon. Body (18,18,22), symbol WHITE diamond only,
  capeless, white outline where body crosses itself.

## What Mars flagged, and the measured cause (not hidden)
Mars: a weird square crop thing down at the feet, cropping his feet off;
the feet look front-facing now, so that version can be used for that, but
make one where the feet are not cropped off, and save the cropped one as
Feet Front Facing Engulfed.

Measured: the version Mars saw (crystal-builder NO-cape plate) does NOT touch
any canvas edge — bottom margin 207 px, edge alpha 0 on all four sides.
Its feet READ as cut off because the old crude cape erase (alpha y>=600
outside x380-720, removed 85,752 px) left a black slab behind the legs, and
the feet are engulfed in that black slab:
- Engulfed, lowest 45 px band: 2,727 px, x380-720 only.
- Engulfed, band above that: 3,708 px, x380-720 only.
No toes spread outward. That engulfment, not a canvas-edge crop, is why the
feet read as cropped off in the contact. The contact tiles themselves were
full-aspect (400 px wide, 545 px tall), not square-cropped — the crop read
comes from the plate, and this build fixes the plate, not just the tile.

## 1. CAPE CONSUMED — UNCROPPED (main version)
- [cape-consumed-uncropped-20261031.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/cape-consumed-uncropped-20261031.png) (transparent, 1300x1700)
- [cape-consumed-uncropped-20261031-on-grey.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/cape-consumed-uncropped-20261031-on-grey.png)
- Source: the later true piece-removal capeless plate
  (future-symbiote-capeless-white-outline-20261031/symbiote-apose-CAPELESS-20261031.png),
  cape pieces Cape_Back_Main + Cape_Collar omitted, NO rectangle erase.
- No-crop rule: canvas padded 100 px on every side (1100x1500 -> 1300x1700).
- Measured: alpha 247,825 px; bbox x348-975, y354-1394;
  margins top 354, bottom 305, left 348, right 324; edge alpha 0 on all
  four sides. Body (18,18,22): 246,301 px. White: 1,524 px (diamond only).
- Feet, full and front-facing, toes forward:
  lowest 45 px band 8,691 px, x404-931; band above 6,354 px, x431-918.
  Compare engulfed above: 2,727 px / x380-720. The feet are no longer
  engulfed, and nothing is clipped at the canvas edge.

## 2. CAPE CONSUMED — crossed, white outline, uncropped
- [cape-consumed-crossed-white-outline-uncropped-20261031.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/cape-consumed-crossed-white-outline-uncropped-20261031.png) (transparent, 1300x1700)
- [cape-consumed-crossed-white-outline-uncropped-20261031-on-grey.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/cape-consumed-crossed-white-outline-uncropped-20261031-on-grey.png)
- Source: the earlier crossed white-outline plate, padded 100 px all sides.
- Measured: alpha 202,694 px; bbox x404-931, y354-1394; bottom margin 305;
  edge alpha 0 all sides. White 4,959 px = symbol diamond 1,524 px +
  white crossing ring 3,458 px (width 4, from that builder) + outline detail.
  Same feet as the apose (lowest band 8,691 px, x404-931).

## 3. FEET FRONT FACING ENGULFED — variant, kept as-is
- [feet-front-facing-engulfed-20261031.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/feet-front-facing-engulfed-20261031.png) (transparent, 1100x1500)
- [feet-front-facing-engulfed-20261031-on-grey.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/feet-front-facing-engulfed-20261031-on-grey.png)
- BYTE-IDENTICAL copy of
  crystal-cape-jones-v2-transformation-upgrade-20261031/future-symbiote-black-white-symbol-NO-cape-20261031.png,
  md5 d133260530769632791fb0f5a3616b57 (matches the original exactly).
  NOT re-padded, NOT fixed over, NOT recoloured. Its feet stay engulfed
  (lowest band 2,727 px, x380-720), exactly as Mars saw it.
- This variant is usable for the front-facing-feet read Mars noted, but it
  is NOT the main Cape Consumed version.

## Contact (viewed before reporting)
- [cape-consumed-contact-20261031.png](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/cape-consumed-contact-20261031.png)
  Tile 1 = uncropped apose, tile 2 = crossed + white outline,
  tile 3 = engulfed variant as-is. Tiles are full-aspect, never
  square-cropped. Bottom row is a labelled feet-detail magnifier only
  (left = uncropped full feet, right = engulfed narrow slab); the full
  figures above it are the uncropped deliverables.
- Contact defect fixed during this build, not hidden: the first contact
  draft's feet-detail crops overlapped each other and the tile labels ran
  together. Labels were shortened and detail crops were scaled to one tile
  width each; the plates themselves were not changed by that fix.

## Files
- Builder: [build_cape_consumed.py](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/build_cape_consumed.py)
- Measurements: [measurements-20261031.json](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/measurements-20261031.json)
- Folder: [cape-consumed-feet-uncropped-20261031/](sandbox://workspace/cape-jones-rig/cape-consumed-feet-uncropped-20261031/)

## Status
- Approval 0/1 for UNCROPPED Cape Consumed.
- Approval 0/1 for FEET FRONT FACING ENGULFED variant, separately.
- No repo push. No existing file overwritten, no original deleted.
- Known carry-over, not hidden: the crossed pose's elbow cap reads as a
  dark disc centre-chest (from the earlier builder, caps excluded from the
  front mask); outlining/removing caps in the all-black form is still owed
  if Mars wants it.

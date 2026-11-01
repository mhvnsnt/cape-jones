# Changelog and deprecation — Shading Preset Library SHD-20261031-v1 (2026-10-31)

## Superseded — kept, labelled, never deleted
- Set One (20 entries, BARELY WORKS) SUPERSEDED by Set Two (DEFINITELY WORKS) as the production shading source. Set One stays as ARCHIVE, reference only.
- V9 Blender first run, sRGB normal map, edge +25.7, SUPERSEDED by V9 second run, Non-Color normal map, edge +27.6. The +27.6 figure is the one to quote.
- Old G2 whole-canvas gradient (V1) kept only as a flaw record (half -13.3, edge +0.5, FAIL).
- First shading-upgrade normal-field attempt from normalized depth (gradient ~0.02/px, near-uniform) SUPERSEDED by raw distance-transform normals (EDT ~1 px/px, sigma 2, z-scale 1.5) — recorded in the upgrade report, not re-run here.

## Deprecated for production use (not deleted)
- All ARCHIVE entries: do not use for production.
- X10 inverse: TEST ONLY, do not ship.
- V2/V4/V3/V6 on apose: faceted warning — method works, apose plate facets; do not ship as clean apose relight.
- N05, N10, X08, X01: proxy warnings (see index) — quote the proxy note with the preset.

## Versioning rule for this library
- Library version SHD-YYYYMMDD-vN, monotonic, never reused. A new preset gets a new ID and a changelog line; an old preset is never overwritten or silently replaced.
- A preset that is superseded keeps its ID, its file, and its status line, so anything built on it can still be found.

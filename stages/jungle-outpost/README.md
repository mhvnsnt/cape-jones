# stages/jungle-outpost — Jungle Outpost arena for Episode 1, Scene 6

Show asset for the Episode 1 fight scene (Cape lands in the arena and
fights Pantera). Production/technical references live in this file only —
never in in-universe writing.

## Status: RECREATION VERSION (preserved) — not extracted game geometry

This asset is the RECREATION VERSION of the Jungle Outpost arena. It is
PRESERVED permanently: it is never replaced or deleted, even after a true
extraction lands (see the replacement note below).

This GLB is original geometry built to the publicly documented layout of
the stage the owner picked (technical stage code `stg02` in the source
game's own modding tables). It is **not** a rip of the game's stage mesh:
no stage geometry, textures, or layout data for this stage existed in
either repo when this was built (survey 2026-10-24 — see below), and a
direct pull was not possible from this box (no Steam session here; the
saved Steam session lives on a collaborator's box, and no credentials
were requested, copied, or used). When a true `stg02` extraction lands,
it is added as the ACTUAL version (a separate file) and this recreation is
NOT replaced or deleted — both versions are kept. This README should
then be updated to point at the actual version for final renders, while
this recreation stays as reference and fallback.

## Sourced vs. approximated

| Element | Status | Source |
|---|---|---|
| Upper fight floor 23 x 13 m, lower floor 26 x 11.5 m, wall-break expansion to 26 x 26 m | SOURCED (dimensions) | Public stage-size tables (TekkenMods stage modding reference; community stage-number table lists `stg02` for this stage) |
| Two tiers: fight starts upstairs, balcony break drops fighters to the lower court | SOURCED (layout) | Public stage descriptions (Tekken Wiki / Tekkenpedia) |
| Breakable balcony rail on one side; breakable vine wall on the lower court | SOURCED (mechanic), geometry original | Same stage descriptions |
| Bahay kubo hut in the distance, temple ruin, tiki statues, crashed-plane wreckage around the lower court | SOURCED (dressing elements), geometry original | Same stage descriptions |
| Daytime lighting | SOURCED (version) | Original version of the stage is daytime; the sunset version is a later variant and was NOT used |
| Exact mesh shapes, textures, colours, prop positions, foliage | APPROXIMATED / ORIGINAL | No extracted reference was available; all meshes are original primitives built for this show asset |
| Animated wildlife (birds, snake), waterfall | NOT MODELLED | Described in stage references but out of scope for this static stage asset; add as animated dressing only if a later lane claims it |
| No crowd characters | INTENTIONAL | The episode script specifies no crowd; the arena's own dressing carries the space |

## Files

- `jungle-outpost.glb` — the stage (GLB, same convention as
  `stages/cape-house/living-room.glb`). Static, no character, no
  animation. Lights exported (day sun + canopy fill, via
  `KHR_lights_punctual`). Verified structure: 209 nodes, 203 meshes,
  15 materials, 1,669,744 bytes; spawn empties and both fight floors
  present with the dimensions in §Scale below.
- `jungle-outpost-recreation.glb` — byte-identical preserved copy of
  the recreation, saved 2026-10-24 (same bytes as `jungle-outpost.glb`).
  The recreation version, kept permanently; the actual version, when it
  lands, lives alongside it, never over it.
- `build_jungle_outpost.py` — the source of truth for this asset.
  Rebuild + re-render with Blender 4.2 headless:
  `blender -b --python build_jungle_outpost.py -- jungle-outpost.glb proof`
  (renders the hero and wide proof frames into `proof/`).
- `render_lower.py` — re-renders `proof/lower_court.png` from the
  exported GLB (west-slot view under the upper platform), so the lower
  court can be checked against the shipped file itself, not just the
  build scene: `blender -b --python render_lower.py --
  jungle-outpost.glb proof/lower_court.png`.
- `proof/hero_upper.png`, `proof/lower_court.png`,
  `proof/wide_tiers.png` — frames actually rendered and viewed before
  the PR was opened. `hero_upper` shows the upper fight floor;
  `lower_court` shows the lower court, carved stone, vine wall, tiki
  statues, and plane wreckage; `wide_tiers` is a side elevation of the
  two-tier stack (canopy foliage crosses the frame edge — the canopy
  sits above and around the platform, not in the fight space).

## Scale, origin, and use in the episode

- Units are metres. Origin = centre of the upper fight floor.
- Upper floor top is at z = 0 in Blender (Z-up); the glTF export
  converts to Y-up, the same convention as `living-room.glb`.
- Lower floor top is 4.2 m below the upper floor (the balcony-break
  drop level).
- Spawn empties (exported as nodes, on the x-axis so the Blender→glTF
  axis conversion leaves them unchanged):
  - `Spawn_Cape` at (-2, 0, 0) on the upper floor
  - `Spawn_Pantera` at (2, 0, 0) on the upper floor
  - `FightCentre_Upper` (0, 0, 0), `FightCentre_Lower` (0, 0, -4.2)
- Breakable objects are in their PRE-BREAK state: `BalconyRail_*`
  (south edge) and `VineWall_*` (north edge of the lower court). The
  animation lane triggers the breaks; this asset does not animate them.
- Scene 6 use: Cape arrives (`portal_03_arrival`) on the upper floor,
  Pantera waits on the same floor, and the fight plays out there first;
  the lower court is the post-break floor.

## Survey notes (2026-10-24, before building)

- cape-jones `stages/` contained only `stages/cape-house/` (living room).
- western-heart `teardown/tekken7/arenas/` contained only a Mishima Dojo
  map archive — no geometry for this stage.
- western-heart teardown docs record only a 34-stage ID table for the
  source game; stage geometry was documented as pending full-game
  acquisition. No other stage geometry for this stage was found in
  either repo.

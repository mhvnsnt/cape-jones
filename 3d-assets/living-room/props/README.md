# props/ — AI/procedural prop handoff to the build lane

This folder is the **handoff point** between prop-making lanes (AI 3D, procedural,
fSpy, whatever) and the living-room **build lane**.

## The pattern

1. A prop lane drops a finished prop here as **GLB** (preferred) or FBX/OBJ,
   already recolored to the canon palette
   (`3d-assets/living-room/SCENE-CANON.md` — coral `#F15E57`, blue `#5B84DD`,
   oak `#E59964`, violet `#731AE5` emission, amber `#FFE996`, trim `#9B4C49`,
   silver `#BDD2D6`, bone `#D1C7B8`, floor `#735238`).
2. Next to it, a `NOTE-TO-BUILD-LANE.md` (see template below) with: what it is,
   its real-world scale, the anchor it belongs to ("on the TV stand, middle
   shelf"), its source + license, and a preview render PNG.
3. The build lane imports it, runs the layout validator, places it, renders —
   owner judges. Nothing else changes.

## Naming

`<prop>_<variant>.glb` — e.g. `vcr_dvd_player_v1.glb`, `monster_toy_v1.glb`,
`mug_okayest_hero_v1.glb`. Preview: `<prop>_<variant>_preview.png`.

## NOTE-TO-BUILD-LANE.md template

```markdown
# NOTE TO BUILD LANE — <prop name> v<n> (date)

- **File:** props/<prop>_<variant>.glb (+ _preview.png)
- **What:** one-line description
- **Scale:** real-world size in meters (e.g. VCR = 0.42 × 0.30 × 0.09 m)
- **Anchor:** where it goes, in the owner's words
  (e.g. "TV stand, middle shelf, left of the boxes")
- **Palette check:** base colors are exactly the canon hexes (list them)
- **Source + license:** e.g. "TripoSR self-hosted, MIT" / "Poly Pizza, CC-BY
  (attribution line below)"
- **Attribution (if CC-BY):** <required credit line>
- **Known issues:** anything the build lane should know
```

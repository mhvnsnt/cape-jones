# GB202 "The Remote" — Sc144: kids burst in, Richard tackles them for the remote

**Cast (named, from the file):** Gumball, Darwin, Richard, Nicole — the whole family except Anais, who has no puppet or placement anywhere in this file.
**Shape:** 262 frames @ 25 fps · stage 1920×1080 · source `GB202REMOTE_Sc144_KeyAnim_V050_clean_MS.fla`

## Construction
- Only 3 working scene layers: `animation`, `white`, `background` (plus audio/framecounter/fieldguide/layout-mov production layers).
- The entire family performance is nested inside ONE master `animation` symbol (1,413 keyframes) placed over white + background, instead of one scene layer per character.
- Library assets dropped into the nest: a nested `gb run cycle` (375 kf) and Nicole's mouth comp (349 kf) — cycles and face comps are shared assets, not scene drawings.
- Gumball and Darwin have no master puppet file in this FLA — they are assembled from comp parts (BODYCOMP/HEADCOMP part symbols) inside the nest; Richard and Nicole do have master puppet symbols. Both construction styles coexist in one scene.
- Highest motion sum of wave 1 (136,609) — the most physical scene in the set.

## Techniques (evidence in scene-anatomy.json)
- nested-master-symbol — the `animation` nest holds all four characters.
- run-cycle-library — `gb run cycle` reused inside the nest.
- layout-mov-reference — guide layer ships in the file.

## What Cape Jones steals
Stage multi-character physical comedy inside one master symbol so entrances, runs and the tackle can be timed against each other in a single timeline, over a dumb-simple white + BG base. Face comps and cycles come from the shared library, never redrawn per scene.

## Media status
Contact sheet: landed in wave 1. Video: attempted in the library build-out (native render); see media_status / CATALOG.

## Honesty
The companion SWF embeds a reference video on its layout-mov layer; renders use a tag-stripped copy (the reference movie is a layout guide, not scene content). Anatomy comes from the untouched FLA.

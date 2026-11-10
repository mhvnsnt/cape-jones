# GB211 "The Treasure" — Sc105: the whole family in one bed, the duvet layer sandwich

**Cast (named, from the file):** Nicole, Gumball, Richard — Nicole reads the bedtime story, Gumball lies between his parents faking sleep, Richard is already out.
**Shape:** 123 frames @ 25 fps · stage 1920×1080 · source `GB211TREASURE_Sc105_V013_clean_GD.fla`

## Construction
- 23 scene timeline entries incl. folders: Roughs, DAD, MOM, MOM R ARM FRONT, DAD OVERLAY HANDS, DUVET, DUVET GUMBALL, dark stripe, MAIN, DUVET MOM MASK, DUVET MOM SIDE, DUVET DAD MASK, DUVET DAD SIDE, GUMBALL, duvet, background…
- Three heads, one blanket: Nicole left, Gumball centre, Richard right. Masks, not redraws, solve the occlusion — DUVET MOM MASK / DUVET DAD MASK clip each body to its place under the shared duvet; Gumball gets his own duvet piece; DAD OVERLAY HANDS rides on top so hands rest on the covers.
- The performances are tiny (mouths, eyelids, one eye popping open) — Gumball's one-eye-open beat (around frames 62–93) is the gag: he's faking sleep during the story. The construction is the show.
- Costume-variant puppets again: GB211_PYJAMAS_DAD_PUPPET and GB211_PYJAMAS_MOM_PUPPET — pyjama versions of the stock puppets built for this episode.
- `DAD ANIMATION copy` (452 kf) and `MOM ANIMATION copy` (370 kf): scene-specific copies are edited in place; library originals stay clean.
- A Roughs layer ships inside the clean file.

## Techniques (evidence in scene-anatomy.json)
- per-character-mask — one duvet mask per character.
- overlay-hands — DAD OVERLAY HANDS layer.
- costume-variant-puppet — pyjama puppets.
- rough-layer-shipped — Roughs layer in the clean file.
- face-comp-driven — the acting is eyelids and mouths.

## What Cape Jones steals
Shared-occlusion staging (three bodies, one blanket; a group under one tablecloth; a crowd behind one counter) is a layering problem, not a drawing problem: per-character masks + one overlay layer for whatever must read on top.

## Media status
Contact sheet: landed in wave 1. Video: attempted in the library build-out (native render); see CATALOG.

## Honesty
In the production SWF export the bedroom background renders white — the visible architecture is the duvet sandwich itself; frame-counter and field-guide overlays are part of the export.

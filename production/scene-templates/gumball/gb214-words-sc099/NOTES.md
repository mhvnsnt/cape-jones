# GB214 "The Words" — Sc099: Darwin's about-to-explode rant (two-shot on white)

**Cast (named, from the file):** Gumball, Darwin — the only two puppets in the file; the classroom is background art, no other character is placed or puppeted in this scene.
**Shape:** 284 frames @ 25 fps · stage 1920×1080 · source `GB214WORDS_Sc099_V006_CLEAN_HS_FR_157.fla`

## Construction
- Scene layers are literally named per character: GUMBALL, DARWIN, WHITE, background — one scene layer per character over a WHITE layer and the background, so each performance can be retimed independently.
- The story beat gets its own asset: an episode-specific costume head comp, `DRWAboutToExplode` (628 keyframes), swapped onto the standard Darwin puppet instead of redrawing the stock head.
- Lip sync is its own pass: mouth comps for both characters run 304–433 keyframes on their own timelines.
- The face system (eye/mouth/head comps) holds more keyframes than the bodies — in dialogue, the comps ARE the animation.

## Techniques (evidence in scene-anatomy.json)
- head-comp-swap — the AboutToExplode comp replaces the stock head for one beat.
- costume-variant-puppet — the exploding-head Darwin is a variant build.
- face-comp-driven — comp keyframes outweigh body keyframes.
- layout-mov-reference — guide layer ships in the file.

## What Cape Jones steals
Dialogue two-shots: one layer per character over white + BG, retime each performance separately, and when a character hits a special state (about to explode), build a variant head comp and swap it on — never bend the stock puppet into the gag.

## Media status
Contact sheet: pending in wave 1 (write-guard window), re-attempted in the library build-out. Video: same. See CATALOG for current status.

## Honesty
This SWF embeds a reference video on its 'layout mov' layer (video character 1). Sheets/videos are rendered from a copy with that reference-video tag stripped — the reference movie is a layout guide, not scene content; all character and background art is untouched. Anatomy comes from the untouched FLA.

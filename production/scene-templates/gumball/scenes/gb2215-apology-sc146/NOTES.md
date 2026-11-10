# The Apology — Sc146: Darwin bursts out of a locker — hop-in, face-off, make-up

**Episode:** GB2215 "The Apology" (Season 2) · **Scene:** Sc146 · **Frames:** 86 @ 25fps · **Source:** GB2215APOLOGY_Sc146_V004_CLEAN_MO.fla / .swf

## Story / beat
One locked shot of a school locker bank, a complete arc with no cuts. Empty lockers (f1). Gumball hops in from frame-right with his ankles strapped together, teeth gritted (f12–22). A locker door pops open and Darwin emerges from inside the locker (f33). Shock turns into a mutual shouting face-off (f43–65 — both still hopping), then cools into a calm standing make-up by the open locker (f75–86).

## Cast
- **Gumball** — GB200_GUMBALL_PUPPET_001 (801 kf) on the GB scene layer. Ankles strapped for the entire scene; every move is a hop.
- **Darwin** — GB200_DRW_ORIGINAL_PUPPET_v001 (359 kf) on the DWN scene layer. Enters from inside the locker.

## Construction
- One locked background: GB215_Apology_SC146_LO_BG.jpg (bitmap plate, frames 0–86) — photographic locker bank with the corridor receding right; the open locker door is the only set element that changes state, between f22 and f33.
- Separate GB / DWN layers carry the offset reactions; a second video layer ('Layer 1', DOMVideoInstance) sits alongside the standard 'layout mov' reference layer.
- The library carries a 'head_WITHOUT_Ears' face comp (363 kf) — an earless Gumball head variant for poses where the ears would tangle.

## Techniques (tags + evidence)
- **photo-plate** — contact sheet shows the photographic hallway plate (glossy red lockers with specular reflections, reflective tiled floor) under the vector puppets — same plate family as GB218 Sc002 (manual, sheet).
- **dialogue-two-shot** — from f33 to f86 both characters are staged together in the one locked shot on separate layers (GB / DWN) over the shared background, playing shock / shouting / reconciliation (manual, layers + sheet).
- **face-comp-driven** — face comps 3,954 kf vs body puppets 1,160 kf (auto).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).

## What Cape Jones steals from this scene
- A physical constraint as the comedy engine: strap the character's ankles and every entrance, argument and apology has to be hopped — staging does the joking.
- The locker entrance: a background-state change (one door opens) is a character entrance with zero new set — keep one movable panel in hallway sets.
- Full arc, one plate: entrance → reveal → fight → make-up in 86 frames without a cut. If the layers are per-character, the timing can carry the whole story.

## Media status
- Contact sheet: done (86 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 86/86.
- Render history: the first render process died silently at launch (VM restart window); the relaunch completed 86/86 on its first attempt.

## Gaps / honesty
- The background filename carries a GB215 prefix inside a GB2215 episode file (GB215_Apology_SC146_LO_BG.jpg) — production naming drift, recorded so archive searches don't miss it.

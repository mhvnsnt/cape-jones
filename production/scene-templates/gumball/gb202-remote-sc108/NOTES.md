# GB202 "The Remote" — Sc108: forced-perspective run (giant Darwin FG, small Gumball BG)

**Cast (named, from the file):** Darwin, Gumball.
**Shape:** 40 frames @ 25 fps · stage 1920×1080 · source `GB202REMOTE_Sc108_Clean_V001_STN.fla`

## Construction
- Both characters run library cycles (`gb run cycle` 410 kf, `dar run cycle` 223 kf) — the staging does the work, not new drawings.
- Darwin's cycle is placed HUGE in the foreground, cropped by the frame edge, one giant leg swinging across the shot; Gumball runs the same kind of cycle small in the background, clutching the remote.
- The background is reduced to a horizontal speed smear: no location detail at all. At full run, location is deleted on purpose.
- Darwin's foreground leg overlaps Gumball's space on the swing (~frame 23, near-collision): FG/BG characters share the frame's depth, staged by layer order.
- 40 frames total: just enough loops for the cut; the cycles do the rest.

## Techniques (evidence in scene-anatomy.json)
- run-cycle-library — both performances are library cycle symbols.
- forced-perspective — the same asset class reads at ~0.3x (background) vs ~3x cropped (foreground).
- speed-smear — the background layer is a speed-line smear.
- layout-mov-reference — guide layer ships in the file.

## What Cape Jones steals
Travel and scale comedy come from placement scale: build ONE good run cycle per character, then direct with size and crop. A foreground limb sweeping past a background character sells depth cheaper than any new art.

## Media status
Contact sheet: landed in wave 1. Video: attempted in the library build-out (native render); see CATALOG.

# GB202 "The Remote" — Sc103: Richard hogs the remote (three run cycles, one garage)

**Cast (named, from the file):** Richard (scene layer/symbol `dad_run`; face comps `GB200_RICHARD_EYECOMP`, `GB200_RICHARD_MOUTH`), Gumball (layer "gumball", symbol `gb run cycle`), Darwin (layer "darwin", symbol `dar run cycle`).
**Shape:** 141 frames @ 25 fps · source `GB202REMOTE_Sc103_V0024_cleanup_LW.fla` (34 MB — the largest FLA in this batch)
**Media:** contact sheet done + video done (production audio muxed from the SWF sound asset) — see media_status.json.

## Story / beat (from the contact sheet)
- Frame 1: Richard sits cross-legged at centre frame in a parking garage, both hands clamped on the remote, grinning with his mouth wide open.
- Frames 19–36: Gumball and Darwin run in from frame-left on their run cycles, furious; Richard hovers cross-legged, still clutching the remote.
- Frame 53: Darwin stretches out horizontal at full run; Gumball snarls beside him. Richard's grin is gone — he is shouting, remote still in both hands.
- ~Frame 71: the kids are gone (Gumball last seen small, looking up). Richard rants alone for the remaining ~70 frames: seated splits, bounces, mouth wide, remote never released (frames 89–123).
- Frame 141: Richard is upside down mid-fall, soles to camera, gritted teeth, the remote up by his foot; a black rectangular outline (a doorway-like shape) appears at frame-left.

## Construction
- One background for all 141 frames: bitmap plate `GB202_REMOTE_SC103_LO_BG.jpg` on the "background" layer (brick wall, red-banded "1" pillars, dark floor, ceiling lights). It reads as a painted/layout plate in the render — unlike Sc094's clearly photographic garage — so it is NOT tagged photo-plate.
- Each character gets his own scene layer with his own library cycle: `gb run cycle` (1,533 kf), `dad_run` (1,038 kf), `dar run cycle` (727 kf), plus shared `Run_1`/`Run_2` sub-cycles.
- Performance weight is in the faces: face comps hold 1,720 kf vs 294 kf of body-puppet keyframes (anatomy census). Richard's body stays in one seated pose family while grin → fury → scream is all comp work.

## Techniques (tags + evidence)
- run-cycle-library (auto) — three named library cycles placed as the scene's locomotion/energy.
- face-comp-driven (auto) — 1,720 face kf vs 294 body kf.
- layout-mov-reference (auto) — 'layout mov' reference layer ships in the file.
- multi-character-staging (manual) — sheet frames 19–53 stage all three characters in one shot on separate layers.

## What Cape Jones steals from this scene
A run cycle is not locomotion until staging says so. Put the cycle on a seated, centred, unmoving character and it reads as manic possession — perfect for a character guarding a coveted object. Cape Jones can stage a "mine!" beat with zero new animation: stock cycle + static plate + face-comp rant + one single-frame flip at the end as punctuation.

## Gaps / honesty
- The builder also emits one unmapped cast entry, 'GB200_ORIGINAL_PUPPET_FRONTVIEW_v001' (a front-view puppet symbol it could not attribute to a named character); the named cast above is the three characters evidenced by layers, cycles and comps and visible in the render.
- The last frame's black rectangular outline is unexplained by the layer census (no new symbol enters in the seams data) — described as seen, not interpreted.
- Whether Richard's rant is dialogue or wordless screaming cannot be told from the sheet; the SWF carries production audio (muxed into the video) but no transcript was made.

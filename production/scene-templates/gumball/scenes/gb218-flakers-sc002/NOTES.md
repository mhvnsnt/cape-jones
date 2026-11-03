# The Flakers — Sc002: panic run straight at the camera down the school hallway

**Episode:** GB218 "The Flakers" (Season 2) · **Scene:** Sc002 · **Frames:** 42 @ 25fps · **Source:** GB218Flakers_Sc002_KeyAnim_V004.fla / .swf

## Story / beat
An empty school hallway. Darwin appears tiny at the far end, then Gumball — both panic-run straight down the corridor at the camera, growing from specks to frame-filling faces in 42 frames. Darwin's gritted-teeth face fills the foreground at f32, Gumball's shape exits past the top of frame at f37, and the shot ends exactly as it began: empty hallway (f42).

## Cast
- **Darwin** — 'Darwin Panic Run' placement / GB200_DRW_ORIGINAL_PUPPET_v001 (238 kf). Runs the lead line, closest to camera.
- **Gumball** — GB200_GUMBALL_PUPPET_001 (153 + 256 kf entries). Runs the same beat smaller and behind Darwin.

## Construction
- One locked background for all 42 frames: GB218_FLAKERS_SC002_LO_BG.jpg (bitmap plate, frames 0–42) — a photographic school hallway with red lockers and a glossy reflective floor.
- Scene layers: DRW (10 kf) and GB (10 kf) over background, plus the production furniture: audio, framecounter, fieldguide, and a guide layer. A 'layout mov' guide layer carries a DOMVideoInstance reference.
- The run is a library asset: 'Panic Run Cycle' key symbol (318 kf).

## Techniques (tags + evidence)
- **forced-perspective** — 'Darwin Panic Run' placed at scales 0.33–3.89 in the same scene (auto, placement matrices).
- **run-cycle-library** — library cycle symbol 'Panic Run Cycle' (318 kf) (auto).
- **cycle-multi-scale** — the same cycle placed from 0.33x at the hallway far end (f1–16) to 3.89x as Darwin's face fills the frame (f32) (manual, sheet + matrices).
- **photo-plate** — contact sheet shows a photographic hallway plate (glossy floor mirroring the lockers, realistic fluorescent fixtures) under the vector puppets (manual, sheet).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).
- **face-comp-driven** — face comps 3,105 kf vs body puppets 647 kf (auto).

## What Cape Jones steals from this scene
- A run AT the camera is a scale ramp, not a new animation: one cycle, one locked plate, 12x of placement scale does the whole gag. Directly reusable for hallway rush shots.
- Open and close on the empty set: the 1-frame empty hallway at both ends makes the intrusion feel like an event.
- KeyAnim honesty: the red timing charts drawn over f11–f27 and Darwin's red rough legs (f21–f32) show where the animator's timing notes live — keep annotation layers in template files, they teach the timing.

## Media status
- Contact sheet: done (42 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 42/42.

## Gaps / honesty
- This is a KeyAnim file, not a clean final: rough red legs and on-frame timing annotations are part of the export and are documented, not hidden.

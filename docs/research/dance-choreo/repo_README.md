# Dance Choreography — pulled from pro show rigs

Owner's concept (2026-10-31): the pro cartoon holdings contain rigs performing
dances. Pull the rigs' dance animation as choreography, then swap Cape Jones
onto the motion once his 2D FLAs exist. This folder is the first extraction.

## What landed here

**Darwin's dance — "The Words" (Gumball S2, ep. GB214), scenes Sc057 + Sc059.**

- `dance-gumball-darwin-words-sc057-sc059.json` — the choreography file (v1).
- Proof sheet (rendered from the source SWF with JPEXS FFDec):
  `~/workspace/your_files/dance-choreo/dance-gumball-darwin-sheet-v1.png`
  (9 frames across Sc057: wide strides, kicked leg, split stances, twist finish.)

Sc057 is the wide shot: Darwin dance-struts down the school hallway toward
camera for the full 198 frames (7.9 s at 25 fps), full body in frame, while
classmates (Tobias, Carmen, Masami, Ocho, Carrie, Tina) watch from the sides.
Sc059 is the companion close-up of the same sequence — Darwin waist-up,
performing the beat-timed **twist**: his puppet timeline in that file contains
layers literally named `twist` (32 keyframes, active frames 43–97) and `beat`.

## How we know it's a dance (production evidence, not vibes)

- A `beat` layer grids the performance: spans of ~14 frames at 25 fps
  (~107 BPM) across the whole shot.
- Arms, legs and the `twist` layer are keyframed every 2 frames (on twos)
  through the dance — classic dance-cycle keyframing.
- `BEAT` layers also exist in the onlooker puppets (Masami, Tobias, Carmen,
  Carrie comps) in Sc057 — the crowd is animated on the same beat.
- A library symbol in Sc059 is named `darwin twist` (rough fragment of the move).
- The renders show the progression: stride → groove step → leg kick →
  split stance → backview twist. See the proof sheet.

## Source

- Archive: `CN-Leaks-001-gumball.zip` (876 entries, 1,709,550,213 bytes) —
  GitHub `mhvnsnt/cn-gigaleak-gumball`, draft release
  `untagged-1676e192ae8c72e95791`, asset id 640772406.
- Files: `GB214WORDS_Sc057_V036_clean_MUI.fla` / `GB214WORDS_Sc059_V001_clean_RR.fla`
  (+ their companion .swf exports in the same archive).
- Extraction: the FLAs are XFL zips. These 2012 Flash zips have a malformed
  central directory (Info-ZIP compensates; Python zipfile rejects them), so
  they were read with a sequential local-header parser, then `DOMDocument.xml`
  and the `LIBRARY/` symbol XMLs were parsed directly. Nothing was redrawn,
  generated, or approximated — every number in the JSON is from the files.

## JSON format

- `fps`: 25. All frame numbers are 0-based XFL frame indices.
- `scene_057` / `scene_059`:
  - `placements` — the scene timeline: per layer, per keyframe, the placed
    symbol (`item`), its `first_frame`, `loop` mode, affine `matrix`
    (a, b, c, d, tx, ty) and `pivot` (transformationPoint) where stored.
  - `darwin_puppet_timeline` — the scene's own copy of the Darwin puppet
    timeline (the performance). Per layer: `keyframes` exactly as authored,
    plus `sampled_frames`: the per-frame expansion (keyMode 9728 =
    pose-to-pose, so each keyframe's elements hold to the next keyframe —
    the same way the SWF plays it).
  - Onlooker puppet timelines (Masami, Ocho in Sc057) in keyframe form.
  - `darwin_twist_symbol` (Sc059) — the named rough fragment.
- A part pose is `(item, first_frame, matrix, pivot)`: the puppet's slots are
  head comp, L/R fin (arm), L/R leg, body layers. Negative `a` = the
  animators flipped the puppet in-scene.
- Honest scope: layers named `rough*` and some `Layer N` tracks mix symbol
  placements with hand-drawn `DOMShape` keyframes (the animators' drawn pass).
  Shape keyframes are recorded as elements of type `DOMShape` (count and
  timing are real; the vector geometry itself stays in the source FLA).
  Transform-driven tracks (head comp ~80 keyframes, arms/legs/fins, the
  twist layer) carry full matrices and are the retargetable spine.

## How a Cape Jones FLA consumes this

1. Build Cape Jones's puppet with the same slot structure (head comp,
   L/R arm, L/R leg, body) — the Gumball slot layout is the reference.
2. For each part slot, play the JSON's per-frame `(first_frame → CJ pose
   equivalent, matrix, pivot)` sequence at 25 fps. The Darwin pose-library
   indices map to CJ poses by slot and body position, not by number.
3. The root placement comes from `placements` (Darwin's scene instance);
   the hallway perspective scale ramp in Sc057 is in that matrix track.
4. Keep the beat: phrase CJ's version on the same ~14-frame beat grid.

## What is NOT in here (honest gaps)

- **No Richard dance exists in the held Gumball production files.** All 71
  FLAs in CN-Leaks-001 were extracted and scanned (symbol names, layer
  names, keyframe structure). Richard's scenes (The Job Sc019/Sc119,
  The Phone Sc154, The Treasure Sc105/117/122, The Remote Sc144) are
  dialogue/action — no dance layers, symbols, or beat structure anywhere.
  The only dance-structured files in the archive are Sc057 + Sc059.
- The 43.5 GB full Gumball leak (`mhvnsnt/cn-gigaleak-gumball` draft
  `gumball-leak-v1`, 86 split parts) is a **RAR5** archive — more episodes
  (S1/S3+) are likely inside, but listing it needs a sequential RAR header
  walk across the parts. That is the next pull if a Richard dance is hunted.
- Scooby-Doo holdings contain **zero** FLA/animation rigs: Mystery Inc is
  model packs, production art, scripts and storyboards only (its one song
  item, ep. 607 act D, is a baked .mov animatic — not extractable).
- Foster's CN dot-com Flash animations (7 character reels, 1,618–2,190
  frames each) are real animated performances, but their FLAs are pre-CS5
  binary and the SWFs are main-timeline shape animation — a heavier
  SWF-tag extraction, not yet done. Secondary pool.
- In Sc057's SWF export, Tina/Carrie/Masami render as line art (their
  colour pass is not in this V036 file); Darwin, Carmen and Tobias render
  in full colour. Choreography data is unaffected.

Full holdings inventory: `INVENTORY.md` in this folder.

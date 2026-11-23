# GUMBALL BACKGROUNDS — HOW THEY ARE USED

Study, not guessing. Every claim below comes from opening the actual files:
the three production PSDs (layer by layer, with `psd_tools`, free and open
source) and one real Gumball scene `.fla` (`GB202REMOTE_Sc094_Clean_V023_STN.fla`,
opened first-hand by streaming its local file headers — its central
directory is damaged, so normal unzip fails). Where a file does not show
something, this doc says so instead of guessing it.

Source: `Documents/Gumball/Gumball/NEW GUMBALL BACKGROUNDS.zip` (479,874,527
bytes, sha256 `5c50207c…ccb3de`, CRCs all OK), pulled from slice 74 of
`documents-zip-slices-v1`, catalogued in `docs/GUMBALL-BACKGROUNDS.md`
(PR #442). Full PSDs live in the workdir
(`torbox-pulls/backgrounds-extracted/NEW GUMBALL BACKGROUNDS/`) — they are
160–246 MB each and cannot go in the repo tree (see §9).

## The three backgrounds, labelled

### 1. Alley — photo plate

- Exact file: `Gumball_Stock_Backgtround_Model_Sheet_Alley_GB238TAPE_Sc046.psd`
- Type: PSD (Photoshop layered image file), 16-bit, RGB
- Size: 160,086,576 bytes. Canvas 4752 x 3168. Layers: **2**.
- sha256 `95c2ca54…8763c0`. Scene code in the name: GB238TAPE, scene 046.
- Layers, as the file itself lists them:
  - `BG` — the alley itself. A real photograph (brick walls, a "9" wall,
    trash, a drain grate), 4760 x 3172 — 8 pixels larger than the canvas
    on each side. Mean alpha 247/255, 14,644,998 opaque pixels.
  - `sc 046` — a red frame/border layer. Own-eyes check of this layer
    alone: red border, transparent middle (mean alpha 49.5/255). The red
    border seen in the preview is IN the file — it is the model-sheet
    frame, not a rendering artefact.
- How Gumball uses it: the name says it — "Stock Background Model
  Sheet". This is a stock plate of a real place, kept as a photo and
  framed as a model sheet for scene 046. The setting IS the photograph;
  nothing in this file is drawn over it.

### 2. School Corridor 6k — painted, with a working locker

- Exact file: `Gumball_Stock_Backgtround_Model_Sheet_School_Corridor_6k_GB110FIGHT_SC133.psd`
- Type: PSD, 16-bit, RGB. Size: 242,602,784 bytes. Canvas 6000 x 3375.
  Layers: **7** (5 visible, 2 hidden). sha256 `97798ebf…ea580ba`.
  Scene code: GB110FIGHT, scene 133.
- Layers, as the file itself lists them:
  - `bty` ("beauty") — the whole painted corridor, 6000 x 3375, fully
    opaque. Red lockers, stickers and graffiti, checkered floor. This is
    the painting everything else sits on.
  - `locker hole` — 280 x 641, the dark inside of an open locker.
  - `locker shadow` — 422 x 890, blend MULTIPLY. The shadow the open
    locker casts, on its own layer.
  - `locker door` — 319 x 761, the locker door itself, separable.
  - `vigniette` (their spelling) — full frame, blend OVERLAY, opacity
    77/255 (30%). Darkens the edges.
  - `Layer 1` — hidden. Measured: 0 opaque pixels, mean alpha 0. An
    empty layer. Nothing in it.
  - `label` — hidden. Measured: 0 opaque pixels, mean alpha 0. An empty
    layer. Nothing in it.
- How Gumball uses it: the locker is three layers on purpose — door,
  hole, shadow. Hide the door and you see the hole; the shadow stays
  put. A prop that opens and closes without redrawing the corridor.
  This is THE school setting for the crossover clip (owner direction
  2026-11-23 09:05 EST).

### 3. Wattersons House, New Living Room v04 — the method, in full

- Exact file: `Gumball_Stock_Backgtround_Model_Sheet_WattersonsHouse_NewLivingroom_v04_GB100KEYCAM_SCF1.psd`
- Type: PSD, 8-bit, RGB, 4 channels. Size: 246,242,573 bytes.
  Canvas 6000 x 3667. Layers: **80 total (70 visible)**, in 17 top-level
  entries. sha256 `550b6608…be537875`. Scene code: GB100KEYCAM, scene F1,
  version 04.
- Groups, as the file itself lists them (top level first):
  - `granny photo` — a framed photo on the wall, its own layer.
  - `HIDE PHONE` — hidden layer, 110 x 590. A phone that is hidden in
    this version of the room.
  - `shadows` — 13 layers. `shadow base` and `sofa shadow` (MULTIPLY);
    `around window` at 40% and 50% opacity; `inside kitchen` at 20%;
    `stairs railing` at 55%; `door` at 30%; `curtain transparency`;
    `shading adjustment` (MULTIPLY, 36%); `standing light cover`;
    `standing light cast shadow` at 20%; `color` (SCREEN); `warm color
    bounce` (COLOR, 35%).
  - `props` — 9 layers. `magazines`, `shoe 1` (hidden), `small desk`,
    `handle`, and shadows (`shadow`, `sha`, `shad` — all MULTIPLY).
  - `Door open` — a HIDDEN group, 9 layers: three alternate door
    states (`Door Open 1`, `Door Open 2`, `Door Open 3`), `door shad`
    (MULTIPLY), `sun light` (COLOR_DODGE), two `Color Fill` layers
    (MULTIPLY). The room with the door open is built and kept, just
    switched off.
  - `Door closed` — the visible group: `door`, `door handle`, and a
    `letterbox` subgroup (mail slot, with its own MULTIPLY shadow).
  - `Couch` — `Couch_SHA` (its shadow, MULTIPLY), `Couch_BTY` (the
    couch itself), and a `cushions` subgroup whose cushions have their
    own shadow layer (`sha`, MULTIPLY).
  - `Carpet` — `blurred` carpet plus a full-frame `table shadow`
    (MULTIPLY).
  - `Table` — `Table_BTY` plus `glass 1` (the glass top, its own layer).
  - `reading lamp` — `base` (COLOR_DODGE), `reading lamp`, `glow`
    (SCREEN, 2141 x 2141), `lens flare` (SCREEN, 1003 x 1015).
  - `glow sunlight` — full frame, LINEAR_DODGE.
  - `TV center` — visible. `TV left` — hidden (the TV in another spot).
  - `SHORTEN DOOR` — hidden.
  - `compositing grade` — 13 layers: `recolor whites` (MULTIPLY, 30%),
    `light contrast`, `red glow` (SCREEN), `grad`, `color`, `dusty air`
    (SCREEN), `window glow` (LINEAR_DODGE) plus a second `window glow`
    (NORMAL, 40%), `Color Balance 1` (50%), `vignette 1` (OVERLAY),
    `vignette 2` (COLOR_DODGE), `vignette 3` (COLOR_BURN), `grain`
    (OVERLAY).
  - `ADD CEILING` — a ceiling strip added on top, 6000 x 233.
  - `labels` — hidden.
- How Gumball uses it: this is the house setting for the crossover
  clip, and it is also the template for how every setting should be
  built. The room is not one drawing. It is 80 pieces: furniture on
  its own layers, every shadow on its own layer, every light on its
  own layer, alternate states (door open / door closed, TV center /
  TV left, phone hidden) built and kept in the same file. The room can
  be re-lit, re-dressed, and re-shot without redrawing it.

## How Gumball uses a background inside a scene — from a real .fla

Opened first-hand: `GB202REMOTE_Sc094_Clean_V023_STN.fla`
(22,851,853 bytes, from `Gumball_S2_Rigs.zip`). Its central directory
is damaged (unzip reports 54 bytes missing), so it was read by
streaming its local file headers — 79 entries recovered, including
`DOMDocument.xml` (291,907 bytes).

- Timeline layers, in order: `Folder 1`, `audio`, `framecounter`,
  `fieldguide`, `Mom Angry run Cycle`, `mom`, `CAR`, `background`
  (locked), `layout mov` (guide, hidden).
- The `background` layer holds ONE instance: a graphic symbol called
  `bg`, 56 frames long, scale 0.848, placed at (948, 188), alpha
  0.34, looping. Characters (the Mom puppet) and the CAR sit on layers
  ABOVE it.
- Library folders: `Scene atributes/BACKGROUNDS`, `CHARACTERS`, `FX`,
  `PROPS`, `VIDEO AND SOUNDS`. The BACKGROUNDS folder holds one file:
  `GB202REMOTE_SC094_LO_BG.JPEG` — the background in the scene is a
  JPEG plate.
- The hidden `layout mov` guide layer holds the low-res video
  reference (`GB202REMOTE_SC094_LO_QT.flv`) underneath the scene — the
  animatic/video the scene was timed against.
- What is NOT in this scene file: the `bg` instance does not move
  across its 56 frames — no keyframes sliding it, no parallax. The
  depth in the shot comes from the painted background itself
  (overlapping furniture, shadows, perspective) and from the grade,
  not from background layers moving at different rates in the .fla.
  This is one scene file (Sc094). Other scenes may differ; do not
  generalise beyond what this file shows.

## How Gumball gives a place lighting and LIFE — by study

Owner question 2026-11-23 10:44 EST. Answer from the files only.

### Separate shadow layers — the shadows are not painted in

Living room `shadows` group, 13 layers: `shadow base` and `sofa
shadow` (MULTIPLY), `around window` (40% and 50%), `inside kitchen`
(20%), `stairs railing` (55%), `door` (30%), `standing light cast
shadow` (20%), plus `warm color bounce` (COLOR, 35%). Every shadow is
its own layer, separated from the furniture that casts it. Move the
light, move the shadow — the sofa stays put. The corridor does the
same thing smaller: `locker shadow` (MULTIPLY) is separate from
`locker door` and `locker hole`.

### Separate light layers — light is added, not painted

Living room: `glow sunlight` (LINEAR_DODGE, full frame), `window
glow` (LINEAR_DODGE, plus a second one at 40% NORMAL), `red glow`
(SCREEN), reading-lamp `glow` and `lens flare` (both SCREEN), `sun
light` (COLOR_DODGE) inside the hidden Door-open group, `warm color
bounce` (COLOR). Light is built as ADDITIVE layers (SCREEN /
LINEAR_DODGE / COLOR_DODGE) over the painted base. That is how a room
gets re-lit without repainting: change the light layers, the painting
stays.

### Photo plates vs drawn art — both, on purpose

The Alley `BG` is a real photograph. The Corridor `bty` and the whole
living room are painted. Gumball mixes the two: a photo plate where a
real place is needed, painted art where the world is drawn. The
living room gets its photographic feel from `grain` (OVERLAY) and
`dusty air` (SCREEN) — texture layers, not paint.

### Layered depth — in the painting, not in the .fla

Foreground, midground and background are separate painted pieces
(couch in front, table in the middle, window at the back; lockers
against the back wall, checkered floor in front). But in the Sc094
scene file the background is ONE locked plate that never moves — no
multiplane parallax keyframes were found in that file. The depth
feeling comes from overlapping pieces, shadows, and perspective in
the painting, plus the grade. Do not claim Gumball slides background
layers at different rates: the file we opened does not do that.

### Animated elements inside the background — none found

The three PSDs are still images. There is no flicker layer, no
dust-motion layer, no light-shift animation layer in any of them.
`dusty air` and `grain` are STATIC screen/overlay layers. Movement in
the finished show comes from the characters, the camera, and the
edit — not from the background file itself. If some other scene .fla
animates a background element, it is not in Sc094 and not in these
three PSDs, and this doc does not claim it.

### How the lighting is built — the stack, in order

Bottom to top, as the living-room layer order shows it: painted base
(NORMAL) → shadows (MULTIPLY, separate) → light (SCREEN /
LINEAR_DODGE / COLOR_DODGE, separate) → colour grade (COLOR /
Color Balance / `recolor whites` MULTIPLY) → atmosphere (`dusty
air` SCREEN, `grain` OVERLAY, three vignettes OVERLAY / COLOR_DODGE /
COLOR_BURN). That stack is the method. Copy the stack, not just the
look.

## How WE should use each one — in Cape Jones

- **Alley.** Use it as the reference for how a photo plate can BE a
  setting, and for crossover-clip alley shots. Lesson to copy: a real
  place, kept as a plate, framed as a model sheet — the setting does
  not need to be drawn to feel real.
- **School Corridor 6k.** THE school setting for the crossover clip.
  Lesson to copy: the locker — door, hole, shadow on three layers.
  That is the pattern for every movable prop in our own backgrounds:
  the thing, the hole it leaves, and its shadow, all separate.
- **Wattersons House living room.** THE method template, and the
  standard for every setting in our show (owner 2026-11-23 10:46
  EST). Lesson to copy: the whole stack — base, shadows, light,
  grade, atmosphere — and the alternate states kept in the same file
  (door open / door closed, TV center / TV left, phone hidden).

## Honest audit — how WE do backgrounds NOW

Owner asked 2026-11-23 10:47 EST. Answered by opening our actual
files (`rig/pil_render.py`, `rig/composite.py`, `rig/make_plates.py`,
`rig/assemble_handswap.py`, `rig/transforms.json`). No guessing, no
defending. The real answer is: we mostly do not do it at all yet.

### What the background IS right now

One flat plate. `rig/plate-sodium.png`, 2048 x 1152, rebuilt from
board 01 (`production/2d-parking-lot/boards/cj-pl-01.png`) by
inpainting Jones out of it (`rig/make_plates.py`): the fence band is
horizontal interpolation between the pixels either side of the hole,
the asphalt band is mirrored asphalt from the left at 70% plus
interpolation at 30%, feathered 25 px at the edges. It has a known
faint vertical seam at the camera-window edge and a half-clipped blue
car at the edge — both visible in the plate itself.

### How Jones is composited onto it

`rig/pil_render.py` renders the puppet parts as transparent PNG
frames (each part rotated and pasted in z-order from
`rig/transforms.json`), and `rig/composite.py` pastes each frame over
a crop of the plate: the camera window (ortho, centre x/y) maps to a
plate crop via `plate_window()` — rig (0, 1.9) [Jones's feet] maps to
plate pixel (1020, 810), 30.2 px per rig unit — the crop is resized
to 1280 x 720, and the puppet frame is pasted on top by its alpha
channel (`bg.paste(pup, (0, 0), pup)`). That is the whole composite.
There is no colour keying anywhere in our pipeline — nothing is
chroma-keyed; Jones's art is RGBA PNG pasted by alpha. That is not
the same thing as keying, and this doc does not call it keying.

### What makes him feel IN the setting — the honest list

Only four things, and three of them are thin:

1. The plate is a real drawing of the lot with correct perspective,
   and the feet mapping above puts Jones on the ground at the right
   scale.
2. One shadow: the puppet has a `P_Shadow` part in
   `rig/transforms.json` — a ground shadow that moves with him. It is
   a puppet part, not a background shadow layer, and it is the ONLY
   shadow in the whole pipeline.
3. The camera crops match the puppet scale (ortho 71 wide down to 34
   close-up), so the framing stays consistent.
4. The whole-frame grade (below) unifies puppet and plate colour, so
   they read as one image.

That is it. There is no light layer, no shadow layer in the
background, no depth, no foreground, no atmosphere layer, and
nothing in the background moves. Jones looks IN FRONT OF the picture
rather than IN the setting, because that is literally what the
pipeline does: a flat picture with a puppet pasted on top of it.

### Where the sodium → purple shift actually happens

Two mechanisms, stacked, neither of them a light layer:

1. **Plate swap.** Two plates exist: `plate-sodium.png` and
   `plate-purple.png`. The purple plate is NOT separately painted —
   `make_plates.py` says so in plain text: "Purple plate = sodium
   plate through the repo purple-streetlight grade." The assemble
   scripts (`assemble_fixed.py`, `assemble_fixed2.py`,
   `assemble_handswap.py`) composite the puppet over the sodium plate
   for f1–253 and the purple plate for f206–480, with a per-frame PIL
   crossfade between them at f206–253.
2. **Whole-frame ffmpeg grade.** Each stream is graded AFTER the
   puppet is composited in, with the repo's verbatim chains
   (`production/pipeline/grades.py`): sodium gets `BULB_ORANGE_DIM`
   (a `colorchannelmixer` pushing red, plus dimming), purple gets
   `PURPLE_STREETLIGHT` (a `colorchannelmixer` pushing blue/purple).
   The grade hits Jones and the plate together — which is why they
   match, and also why the light cannot move, change, or be aimed:
   there is no light in the scene, only a colour wash over the
   finished frame.

So the canon lock — sodium orange → broken-streetlight purple — is
currently a plate dissolve plus a whole-frame colour wash. It works
as a mood change. It is not a lighting system.

### The gap to Gumball, honestly

| Gumball has | We have |
|---|---|
| 80 layers, shadows / light / furniture separate | 1 flat plate |
| Shadows as MULTIPLY layers, separate from furniture | 1 puppet shadow part (`P_Shadow`) |
| Light as SCREEN / LINEAR_DODGE / COLOR_DODGE layers | None — whole-frame colour wash after compositing |
| Props that open/close (locker door / hole / shadow) | None — props are baked into the plate |
| Alternate states in the same file (door open/closed, TV spots) | None — a second whole plate, made by grading the first |
| Photo plates AND painted art, mixed on purpose | One painted plate, inpainted from a board |
| Grade as a layer stack inside the file | Grade as an ffmpeg chain on the finished video |
| Background as a locked JPEG plate in the scene, characters above it | Same idea, cruder: plate crop + puppet paste |

### Exact steps to close it

1. **Layered PURPLE LOT rebuild (this lane, done — §7 below).** The
   proof that our plate can become a movable real space.
2. **Use the layered file in the next cut.** Composite Jones BETWEEN
   background layers (behind the foreground, in front of the back
   wall) instead of on top of one flat plate — that alone is what
   makes a character feel IN a place.
3. **Light as layers.** The sodium → purple shift becomes a light
   toggle (proven in §7), not a plate swap plus a grade.
4. **Re-slice the source art.** The flat plate can only be split by
   region (bands and boxes). True per-prop separation — every car, the
   stop sign, the fence, the lamps as separate drawn pieces — needs
   the board art re-sliced like the rig parts were. That is the next
   job after this proof.
5. **Same method for every other setting** (owner 2026-11-23 10:46
   EST). One flat picture at a time: keep the art, add the Gumball
   structure underneath it.

## The layered-background standard — for ALL our settings

Owner direction 2026-11-23 10:46 EST. This is now the standard for
every setting and every place in the show, not just the parking lot:

Build every background like the Gumball living room — 80 separate
layers, shadows on their own layers, lighting on its own layers,
furniture on its own layers. Light can be moved, furniture can be
moved, ALL of it can be moved without redrawing the room. That
creates a MOVABLE, reusable REAL SPACE we can use over and over and
move stuff around in.

Proof case first: the PURPLE LOT parking lot (§7). Then the same
method applies to every other setting after it.

## PURPLE LOT rebuild — the proof

### What it is

`torbox-pulls/free-proof/purple-lot-layered.psd` — 31,160,642 bytes
(under the 100 MB repo-tree limit), 2048 x 1152, 8-bit RGB, 5 groups,
20 layers. Built by `torbox-pulls/free-proof/build_purple_lot_layered.py`
with `psd_tools` (free, open source) — no Photoshop, no paid tool.

It is NOT a redraw and NOT a new style (owner 2026-11-23 10:47 EST).
It starts from the existing V2 plate art (`rig/plate-sodium.png`),
the exact look and atmosphere the owner already likes, and splits
THAT art into the Gumball method. Same colours, same atmosphere,
same plate — now layered and alive.

### The layers (mirroring the living-room structure)

- `base` — `sky` (top band), `skyline and fence` (middle band),
  `asphalt` (bottom band). Each is an exact crop of the plate with
  the rest transparent.
- `props` — `cars left row`, `blue car mid`, `cars right row`,
  `stop sign`. Each is an exact box cut from the plate.
- `light` — `street lamp right` and `street lamp far` (box cuts from
  the plate, at the lamps' measured positions: right lamp head
  (1745, 205), far lamp head (625, 395)); `lamp glow sodium` and
  `lamp glow purple` (radial gradients, SCREEN); `light pool sodium`
  and `light pool purple` (radial pools on the asphalt, SCREEN).
- `shadows` — `ground shadow jones` (soft ellipse, MULTIPLY, at the
  feet mapping (1020, 810) from `rig/composite.py`); `asphalt shade`
  (MULTIPLY, 30%).
- `grade` — `light sodium` (solid orange, COLOR) and `light purple`
  (solid purple, COLOR), one on and one off; `dusty air` (SCREEN),
  `vignette` (OVERLAY, 50%), `grain` (OVERLAY).

### Proof — side by side, measured, own-eyes

- **Base-only composite vs flat plate: mean absolute difference
  0.0, max 0.0.** With the light/shadow/grade groups hidden, the
  layered file composites to the flat plate pixel-for-pixel. The
  split loses nothing.
- **Full sodium composite vs flat plate: mean absolute difference
  8.3 / 255** (red +12.5, green +7.1, blue +5.2). Own-eyes on the
  side-by-side: the same look and atmosphere, the lamp area a touch
  warmer and brighter — the added glow layers doubling light the
  plate already has baked in. The atmosphere layers were tuned down
  twice to get here (glow peak 230 → 110, light alpha 70 → 28).
  Honest note: the faint vertical seam in the middle of the frame is
  pre-existing in the flat plate itself (from the inpainting in
  `make_plates.py`), not introduced by the layering.
- **The lighting shift is a light toggle, not a redraw.** Sodium →
  purple means switching three layers off (`light sodium`, `lamp
  glow sodium`, `light pool sodium`) and three on (the purple
  versions). Rendered and checked: the purple composite reads as the
  broken-streetlight purple lot, same art, no repainting.
- Previews (1920-wide renders of the composites):
  `torbox-pulls/free-proof/purple-lot-sodium.png`,
  `torbox-pulls/free-proof/purple-lot-purple.png`, and the
  side-by-side
  `torbox-pulls/free-proof/purple-lot-side-by-side.png`.
- The PSD re-opens in `psd_tools` with all 5 groups and 20 layers,
  blend modes, opacities and visibility intact (verified by re-read).
  Each layer is also exported as a PNG in
  `torbox-pulls/free-proof/purple-lot-layers/` (20 files, 16 MB
  total — the two noise layers are 6.7 MB each and can be regenerated
  by the build script instead of stored).
- **Limit, stated plainly:** the split is by region (bands and
  boxes) because the source is one flat plate. The cars, lamps and
  sign are box cuts, not cleanly re-sliced art — their edges are the
  plate's own pixels, and a car moved far from its box would show a
  rectangular edge. True per-prop separation needs the board art
  re-sliced (step 4 above). The rebuild proves the STRUCTURE and the
  light toggle; it does not magically un-bake the plate.

## Keep the look — the rule for every flat picture

Owner direction 2026-11-23 10:47 EST. Take the FLAT PICTURES we
already have and make them the Gumball way — BUT keep them looking
and feeling just like the flat pictures we used, because those were
really good, they had a real good atmosphere to them. The rebuild is
NOT a redraw and NOT a new style: start from the existing plate art,
split/convert THAT art into layers, same colours, same atmosphere,
now movable and alive. **If the layered version looks different from
the flat plate, it is wrong — compare them side by side and match
it.** Same rule for every other flat picture after the parking lot:
keep the art, add the Gumball structure underneath it.

## Big files, in plain words — and the free way to handle them

Owner asked 2026-11-23 10:43 EST what PSDs and LFS mean. Plain
words:

- **A PSD is a Photoshop layered image file.** One file that holds a
  picture as many separate layers — the painting, the shadows, the
  light, the props — instead of one flat image. Photoshop makes them;
  that is the format Gumball's backgrounds arrive in.
- **LFS is Git Large File Storage.** A way to store big files outside
  the repo's own tree, so the repo stays small and GitHub does not
  refuse them. It has a free tier. This repo does NOT have LFS set
  up, and GitHub still refuses any single file over 100 MB in the
  repo tree, LFS or not, unless the file is stored through LFS.
- **The problem:** the three Gumball PSDs are 160–246 MB each. They
  cannot go in the repo tree. The PURPLE LOT layered PSD is
  31,160,642 bytes — under 100 MB, so it CAN go in the tree.

### The free route that actually works (proven on this VM)

1. **Previews and exported layers go in the repo tree.** JPG
   previews (300–425 KB each) and per-layer PNGs (all under 100 MB)
   live in `production/2d-parking-lot/` like any other art file.
2. **Full files over 100 MB go to GitHub Releases as slices.**
   Exactly how `Documents.zip` already works: cut the file into 2 GB
   slices with a MANIFEST and a sha256 file per slice, upload the
   slices as release assets, reassemble by concatenating in order
   and verifying each slice first. Proven by the whole CN vault
   pipeline (PR #441).
3. **Free tools that read and write PSD layers — proven here, not
   just listed:**
   - `psd_tools` (free, open source, Python, already on this VM):
     opens all three Gumball PSDs, reads every layer name, blend
     mode, opacity and bounding box; exports each layer as a PNG;
     and BUILDS a new layered PSD — the PURPLE LOT rebuild above
     was made and verified with it (create group, create pixel
     layer, set blend mode and opacity, save, re-open and check).
   - `Pillow` (free, open source, already on this VM): image
     crops, gradients, compositing, previews.
   - GIMP and Krita (free, open source) open and edit PSDs with a
     real interface — they are the free GUI for this work. They are
     NOT installed on this VM and were not proven here; `psd_tools`
     is the proven path on this machine, GIMP/Krita is the proven
     path on a desktop.
4. **Exact steps to reproduce the rebuild:** run
   `torbox-pulls/free-proof/build_purple_lot_layered.py` from the
   workdir. It reads `rig/plate-sodium.png`, builds the 5 groups and
   20 layers, saves `purple-lot-layered.psd`, exports every layer as
   a PNG, renders the sodium and purple composites, and prints the
   side-by-side difference numbers. No Photoshop, no paid tool, no
   account.

## What is NOT landed yet — parent jobs (browser upload)

The GitHub connector cannot carry binary files, so these need a
browser upload, signed in as mhvnsnt — this lane cannot run it:

1. The 3 Gumball JPG previews into
   `production/2d-parking-lot/gumball-backgrounds/`:
   `torbox-pulls/backgrounds-previews/Gumball_Stock_Backgtround_Model_Sheet_Alley_GB238TAPE_Sc046.jpg`
   (424,500 B), `..._School_Corridor_6k_GB110FIGHT_SC133.jpg`
   (322,465 B), `..._WattersonsHouse_NewLivingroom_v04_GB100KEYCAM_SCF1.jpg`
   (337,957 B).
2. The PURPLE LOT layered PSD (31,160,642 B) and its 20 layer PNGs
   (16 MB) into `production/2d-parking-lot/purple-lot-layered/`,
   plus the two composite previews and the side-by-side sheet.
3. Pull 2 school slices are downloading separately (browser job
   already running) — classroom, stadium, corridor, playground,
   exterior, gym. Their backgrounds get the same treatment: labelled,
   studied by their layers, rebuilt the same way.

## Sources

- PSD layer dumps: `psd_tools` 1.27.0, run on this VM 2026-11-23
  against the three extracted PSDs (layer names, blend modes,
  opacities, bounding boxes, per-layer alpha statistics — including
  the two empty hidden layers in the Corridor file, 0 opaque pixels
  each, and the Alley `sc 046` red frame, own-eyes checked).
- Scene file: `GB202REMOTE_Sc094_Clean_V023_STN.fla`, streamed
  local-header parse, 79 entries, `DOMDocument.xml` 291,907 bytes.
- Our pipeline: `rig/pil_render.py`, `rig/composite.py`,
  `rig/make_plates.py`, `rig/assemble_handswap.py`,
  `rig/transforms.json` (30 parts, including `P_Shadow`),
  `production/pipeline/grades.py` — all read on this VM 2026-11-23.
- Catalogue: `docs/GUMBALL-BACKGROUNDS.md` (PR #442),
  `docs/DOCUMENTS-CATALOGUE.md` (PR #441).

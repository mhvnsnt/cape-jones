# Gumball School Settings — Pull 2 (TorBox)

Source: `Documents.zip` (TorBox torrent 119449922, "Cartoon Network documents"),
slices 85 / 88 / 89 / 90 / 91 of release `documents-zip-slices-v1`
(`mhvnsnt/cn-gigaleak-documents-archive`). Extracted by byte range only —
never the whole zip. All 5 slices sha256-verified against their `.sha256.txt`
before use; every entry CRC32-verified against the catalogue
(`torbox-pulls/catalogue.json`).

These are the Elmore Junior High settings for the crossover clip
(Cape Jones walking through Gumball's school). Study only — no CN art
goes into any show file except the explicitly authorized crossover clip.

## The six settings

| File | Type | Size | Dimensions | Layers | Slice | sha256 (first 16) |
|---|---|---|---|---|---|---|
| `GB36_sc33_School_Classroom_Final_upressed_v4.psd` | PSD 8-bit | 970,797,439 B | 7654 × 4895 | 57 (incl. groups) | 85 | `1226f539d2e229d3` |
| `GB04_sc120_School_Stadium_Final_4_upressed.psd` | PSD 8-bit | 303,782,283 B | 8820 × 4961 | 24 (incl. groups) | 88 | `9cd38fa45927e0c8` |
| `GB21_sc18_School_Corridor.tif` | TIFF flat | 165,428,140 B | 7000 × 3938 | 1 (flat) | 89 | `23c0969543c658f2` |
| `GB17_SchoolPlayground_sc024_FINAL.tif` | TIFF flat | 82,778,208 B | 7000 × 3940 | 1 (flat) | 90 | `c4e57776bbb9b3a0` |
| `GB00_Schoolexterior_BM_final.tif` | TIFF flat | 98,044,884 B | 7000 × 4667 | 1 (flat) | 90 | `d4e3b353b8d4d25f` |
| `GB37_sc018_SchoolGym_final.tif` | TIFF flat | 183,761,598 B | 7000 × 4374 | 1 (flat) | 91 | `1bbae8c4a68f88db` |

Full sha256 values are in `torbox-pulls/school-previews/school-catalogue.json`.
Full PSDs/TIFs (83–971 MB) stay OUT of the repo tree (GitHub 100 MB tree
limit, 25 MB web-upload limit) — previews (1920-wide JPGs, 2.0 MB total)
and the catalogue go in the tree; full files are re-derivable any time
from the verified slices + `torbox-pulls/zipcat.py` + `extract_school.py`.

## What each one is (own-eyes, from rendered composites)

### 1. Classroom — `GB36_sc33_School_Classroom_Final_upressed_v4.psd`
Real photograph of a classroom: rows of wooden desks, blackboard with four
posters pinned on it (Times Table, "The World's Largest Trees", a water-cycle
diagram, an eye diagram), tall windows right with trees outside, ceiling
fluorescent lights. Layered, not flat: `posters` group (each poster its own
layer with its own MULTIPLY/OVERLAY colour fill, so a poster can be swapped
without redrawing the board), `chair group` (chair + its own light
COLOR_DODGE + reflection group), `reflection group` (floor reflections as
separate MULTIPLY/COLOR layers), `post` group (COLOR_DODGE light, SCREEN
grade, Levels/Hue-Saturation/Vibrance adjustments). Two hidden layers
(`dessk mask`, `mask chairs`, `animatic`) — the animatic is a hidden
reference frame. **In-file artifacts, not added by us:** a magenta bar
across the top of the blackboard and a small red triangle at the top-left
corner — both are in the PSD itself.

### 2. Stadium — `GB04_sc120_School_Stadium_Final_4_upressed.psd`
Honest note: the composite is dominated by a white cartoon character
(Penny, backlit, arms out) against a blue sky — the character IS in this
PSD (`penny` group), and the background layer (`bg`) is sky + a floodlight
tower + the edge of a stand. This file is a character-over-sky shot, not
an empty stadium plate. Layered: `penny` group (character + MULTIPLY
colour fill + COLOR_DODGE light), `post` group (SCREEN glare ×2,
LINEAR_DODGE, five Levels copies, Hue/Saturation, red glow SCREEN,
blue flare SCREEN), `vignette` OVERLAY 41. The lighting stack is the
same Gumball method as the living room (PR #443): base → MULTIPLY
shadow/colour → COLOR_DODGE light → SCREEN glare/flare → OVERLAY vignette.

### 3. Corridor — `GB21_sc18_School_Corridor.tif` (flat)
Photograph: red lockers both sides, a water fountain in a tiled alcove,
a wooden door with a mesh window, a framed "Fantasy Club" poster,
checkered floor with a purple strip. Flat TIFF — one layer, no separable
pieces. This is the corridor's *look* reference; the separable-locker
version is the 6k corridor PSD from Pull 1
(`..._School_Corridor_6k_GB110FIGHT_SC133.psd`, 7 layers).

### 4. Playground — `GB17_SchoolPlayground_sc024_FINAL.tif` (flat)
Photograph of the school basketball court: red/blue painted court lines,
two hoops, trees, houses behind the fence, climbing frame. Cartoon
white clouds are pasted into the sky (the Gumball photo-plus-cartoon mix),
and a red wall clock is pasted on the building edge at right.

### 5. School exterior — `GB00_Schoolexterior_BM_final.tif` (flat)
Photograph of Elmore Junior High itself: yellow building, pink/blue/orange
entrance doors, tall central windows, "ELMORE JUNIOR HIGH SCHOOL" sign
over the steps, "ELMORE J HIGH" bunting, graffiti. Cartoon additions
pasted on: a flat green tree left of the doors. This is the establishing
shot for the crossover clip.

### 6. Gym — `GB37_sc018_SchoolGym_final.tif` (flat)
Photograph of the gym: wooden floor with pink/blue court lines, bleachers
both sides, basketball hoop hanging from the roof trusses, "FITNESS CENTER"
doors, purple exit doors. Cartoon props pasted in: a pommel horse and a
green mat at left. **Black letterbox bars top and bottom are in the file
itself** — the image is framed, not full-bleed.

## How Gumball uses them (by study, PR #443 method)

- Interiors that need to change (classroom, stadium) are layered PSDs:
  posters, chairs, characters, reflections, light and grade are all
  separable, so a scene can re-light, swap a poster, or move a chair
  without redrawing the room.
- Exteriors and one-off plates (corridor, playground, exterior, gym)
  are flat TIFF photographs with cartoon elements pasted on — the
  photographic feel IS the setting, and the cartoon paste-ins are the
  Gumball signature.
- The lighting stack, wherever it exists: painted/photo base (NORMAL) →
  shadows/colour (MULTIPLY) → light (COLOR_DODGE / SCREEN) → grade
  (Levels / Hue-Saturation / Vibrance) → atmosphere (vignette OVERLAY).

## For our show

Same rule as Pull 1: keep the art, add the structure. When we rebuild
our own school settings, they get built the Gumball way — layered,
separable, re-lightable — and any prop we cut gets **clean alpha, no
rectangular edges, never a square/box crop** (owner rule, 2026-11-23).
The flat TIFFs are look references only; a movable version of one
needs to be rebuilt from separable layers, not box-cut from the flat.

## Pull 3 — next download (house / town)

Slices 78, 81, 87, 88, 90, 98 of `documents-zip-slices-v1`.
**Slices 88 and 90 are already on disk** (verified for Pull 2) — only
four need downloading:

| Slice | File to download | Contents (verified in catalogue) |
|---|---|---|
| 78 | `slice-156000000000-2000000000.bin` | Town reference JPGs: `GB_Town_L_Final.jpg` (1.0 MB), `GB_Town_P_Final.jpg` (3.3 MB) |
| 81 | `slice-162000000000-2000000000.bin` | `06_Page_08-09_The_Wattersons.psd` (156.2 MB) |
| 87 | `slice-174000000000-2000000000.bin` | `GB30_sc53_WatersonsHouse_Kitchen_final.tif` (177.5 MB) |
| 98 | `slice-196000000000-2000000000.bin` | Gumball style-guide packaging layered art (AWG_PKG PSDs, incl. `AWG_TI_4C_001-green.psd` 203.4 MB) |
| 88 | already on disk | `05_Page_06-07_Elmore.psd` (99.1 MB), Wattersons AI files |
| 90 | already on disk | `Page_08_The_Wattersons_FINAL.ai`, `PAGE_05_The_Wattersons_FINAL.ai` |

Each file + its `.sha256.txt` companion; verify sha256 before use.
After Pull 3: Pull 4 = slices 105, 106, 107 — all 138 Gumball `.fla`.

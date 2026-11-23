# Gumball House / Town Settings — Pull 3 (TorBox)

Source: `Documents.zip` (TorBox torrent 119449922, "Cartoon Network documents"),
slices 78 / 81 / 87 / 88 / 90 / 98 of release `documents-zip-slices-v1`
(`mhvnsnt/cn-gigaleak-documents-archive`). Extracted by byte range only —
never the whole zip. All 6 slices sha256-verified against their `.sha256.txt`
before use; every entry CRC32-verified against the catalogue
(`torbox-pulls/catalogue.json`).

- Slice 78 `a34ecd83ff5c4667b5e13e786c28c86c83d603cfe00e2f8d5c30727e4a4bfb1c`
- Slice 81 `f3a14c1b40f342f232d84a305da941f201d5b11486938f62abde78be42fc5ac9`
- Slice 87 `0cbae9d0f011f3aabced309d0927e2a744d087eb1fcbed8d3d6723e098a90273`
- Slice 88 `2f7180b1…` (verified for Pull 2)
- Slice 90 `bac4de98…` (verified for Pull 2)
- Slice 98 `e5ca8d3378309dac19ed0ecc40aab622e678775084414ec0264a9ddec88499a7`

These are the Watterson house and Elmore town settings for the crossover clip
(Cape Jones walking through Gumball's house and town), plus the style-guide
packaging layered art that came in on slice 98. Study only — no CN art
goes into any show file except the explicitly authorized crossover clip.

CLEAN ALPHA RULE (owner, 2026-11-23): every cut/slice/prop has clean alpha,
no rectangular edges, never a square/box crop. Previews here are whole-image
flat composites for viewing only; no props were cut from these files.

## The nine house / town files

| File | Type | Size | Dimensions | Layers | sha256 (first 16) |
|---|---|---|---|---|---|---|
| `05_Page_06-07_Elmore.psd` | PSD 8-bit | 99,066,479 B | 9921 × 2790 | 6 | `3953fafdfb8a91fb` |
| `06_Page_08-09_The_Wattersons.psd` | PSD 8-bit | 156,176,564 B | 9921 × 2790 | 23 | `851d2dd8d2668916` |
| `07_Page_10_The_Wattersons_B_APPROVED_FINAL_CS4.ai` | AI (PDF 1.5) | 6,692,530 B | 1191 × 341* | — | `0bb78fb57616319d` |
| `07_Page_11_The_Wattersons_B_APPROVED_FINAL_CS4.ai` | AI (PDF 1.5) | 6,245,038 B | 1191 × 341* | — | `776b283ea30e7f1d` |
| `GB30_sc53_WatersonsHouse_Kitchen_final.tif` | TIFF flat | 177,534,280 B | 7000 × 4226 | 1 (flat) | `858970946e40c95f` |
| `GB_Town_L_Final.jpg` | JPEG | 1,016,805 B | 1244 × 886 | — | `cad83e5ee8e41d6b` |
| `GB_Town_P_Final.jpg` | JPEG | 3,309,094 B | 886 × 1244 | — | `ba9864312959684a` |
| `PAGE_05_The_Wattersons_FINAL.ai` | AI (PDF 1.5) | 4,989,800 B | 1191 × 341* | — | `f5e223d325c78d8a` |
| `Page_08_The_Wattersons_FINAL.ai` | AI (PDF 1.5) | 7,646,891 B | 1191 × 341* | — | `7fd65d35fb74af64` |

\* AI dimensions are the 72-dpi first-page render size (pdftoppm), not the
vector page size — the .ai files are PDF 1.5 vectors, rendered for preview.

Full sha256 values are in `torbox-pulls/house-previews/house-catalogue.json`.
Full PSDs/TIFs/AIs (1–178 MB) stay OUT of the repo tree (GitHub 100 MB tree
limit, 25 MB web-upload limit) — previews (1920-wide JPGs, 1.6 MB total)
and the catalogue go in the tree; full files are re-derivable any time
from the verified slices + `torbox-pulls/zipcat.py` + `extract_pull3.py`.

## What each house / town file is (own-eyes, from rendered composites)

### 1. Elmore — `05_Page_06-07_Elmore.psd`
A show-art book spread, 9921 × 2790, 6 layers (`LEFT_PAGE` / `RIGHT_PAGE`
groups). Left page: a real photo street — houses, white picket fence,
brown car, traffic light, fire hydrant — with cartoon characters standing
in it (furry slug feet, balloon, potato, ghost at the bus stop). Right page:
solid red panel, "ELMORE" in the Gumball bubble font, text "Elmore, USA –
POP. 20,000" and the "Welcome to The Amazing World of Gumball" intro.
**This is a book spread, not a clean background plate** — the usable
setting is the left-page photo; the text panel is book layout. The `DISTORTION`
layer name is in the file itself.

### 2. The Wattersons — `06_Page_08-09_The_Wattersons.psd`
A show-art book spread, 9921 × 2790, 23 layers. Left page: the whole
Watterson family (Gumball, Darwin, Anais, Richard, Nicole) grouped over
the house and the yellow car, pink cloud shapes, `family` group with
MULTIPLY shadow layers per character. Right page: solid blue panel,
"THE WATTERSONS" and the family intro text. Same caveat as Elmore: a
book spread, not a clean plate. The four `.ai` files are the vector
versions of the same spreads (same art, same text) — `Page_08` renders
identically to this PSD's spread; `PAGE_05` is the Elmore spread.

### 3. Kitchen — `GB30_sc53_WatersonsHouse_Kitchen_final.tif`
**A real setting, flat.** 7000 × 4226, one layer. A photo-modelled kitchen:
wood cabinets, white tile, checkered black-and-white floor, window left
with green polka-dot curtains and trees outside, orange stove, white
fridge with magnets and cereal boxes ("DIZZYFLAKES"), arched doorway
right to a blue-carpet room. This is the Watterson house interior for
the crossover clip — the kitchen Jones walks through. Flat, so it is a
look/plate reference, not separable layers.

### 4. Town posters — `GB_Town_L_Final.jpg` / `GB_Town_P_Final.jpg`
Landscape (1244 × 886) and portrait (886 × 1244) versions of the same
promo poster: "JUST YOUR AVERAGE TOWN!" banner over the Elmore street
photo (same street as the Elmore spread), Gumball and Darwin in front,
rainbow + "The AMAZING WORLD OF GUMBALL" logo, "BRAND NEW, EVERY DAY 5PM",
CN bug, social icons. **Promo posters, not clean backgrounds** — logo,
banner, and characters are baked in. The street photo underneath is the
usable town reference.

## The 32 style-guide packaging files (slice 98)

All 32 start in slice 98 and end inside it; every CRC32 OK. One more
packaging file, `AWG_PKG_HANGTAG-DIE CUT.ai` (234,318,327 B), starts in
slice 98 but ends in slice 99 — **NOT extracted** (slice 99 is not on
disk). It needs slice 99 for a later pull.

| File | Type | Size | Dimensions | Layers | sha256 (first 16) |
|---|---|---|---|---|---|
| `AWG_AL_4C_002.psd` | PSD | 10,856,710 B | 5000 × 3750 | 3 | `046aaef61e4be415` |
| `AWG_AL_4C_002-outlined.psd` | PSD | 10,856,258 B | 5000 × 3750 | 3 | `f90e7df6663a3b98` |
| `AWG_AT_4C_001.psd` | PSD | 36,123,871 B | 5000 × 3750 | 3 | `6ea37c2730303d14` |
| `AWG_AT_4C_001-outlined.psd` | PSD | 36,119,784 B | 5000 × 3750 | 3 | `77fc7130626df4cf` |
| `AWG_BA_4C_001-outlined.psd` | PSD | 73,540,896 B | 5000 × 3750 | 2 | `2ba030649eaa7577` |
| `AWG_BO_4C_001-outlined.psd` | PSD | 36,675,471 B | 5000 × 3750 | 2 | `7d64c13aecf57994` |
| `AWG_CL_4C_001.psd` | PSD | 46,418,655 B | 5000 × 3750 | 2 | `6edb637226f91268` |
| `AWG_CL_4C_001-outlined.psd` | PSD | 53,875,201 B | 5000 × 3750 | 2 | `c11cf91960395bf9` |
| `AWG_ID_4C_001.psd` | PSD | 18,943,326 B | 5000 × 3750 | 2 | `ef91652a62faabf8` |
| `AWG_ID_4C_001-outlined.psd` | PSD | 27,716,488 B | 5000 × 3750 | 2 | `a5f2f4b7debc4f01` |
| `AWG_LE_4C_001.psd` | PSD | 4,731,385 B | 2291 × 3378 | 1 | `eef4707d67636da0` |
| `AWG_MA_4C_001.psd` | PSD | 1,018,893 B | 806 × 602 | 1 | `61f81a2f0118751c` |
| `AWG_PE_4C_002.psd` | PSD | 3,111,489 B | 3229 × 2469 | 1 | `a356494c7cf39508` |
| `AWG_PKG_BADGES.ai` | AI (PDF 1.5) | 1,973,665 B | 997 × 707* | — | `6909a4be124e40bb` |
| `AWG_PKG_BADGES_BW.ai` | AI (PDF 1.5) | 1,941,824 B | 997 × 707* | — | `16c9df7d7bcc511f` |
| `AWG_PKG_BK.eps` | EPS (binary DOS EPS) | 5,211,574 B | — | — | `9f6d946fe3a80602` |
| `AWG_PKG_BKG_home.jpg` | JPEG | 22,163,360 B | 5616 × 5906 | — | `e16df805a78d8d9c` |
| `AWG_PKG_BKG_house.jpg` | JPEG | 33,778,820 B | 5616 × 5906 | — | `ad1cf687602e3358` |
| `AWG_PKG_BKG_school.jpg` | JPEG | 6,201,287 B | 2666 × 3543 | — | `32a791f1d5359079` |
| `AWG_PKG_ELEMENTS.ai` | AI (PDF 1.5) | 24,494,916 B | 842 × 596* | — | `f611e5a6c66ba8e9` |
| `AWG_PKG_HANGTAG-BW.jpg` | JPEG | 1,000,454 B | 2236 × 1214 | — | `6a26335098c1eecb` |
| `AWG_PKG_HANGTAG-DIE CUT-BW.jpg` | JPEG | 935,566 B | 2246 × 1214 | — | `01cae51e8fbe1d96` |
| `AWG_PKG_HANGTAG-DIE CUT.jpg` | JPEG | 1,098,773 B | 2248 × 1214 | — | `1fb5adf9cf8e1d5d` |
| `AWG_PKG_HANGTAG.jpg` | JPEG | 1,232,162 B | 2238 × 1214 | — | `d52286a36a5884a2` |
| `AWG_PKG_HANGTAG_DIECUT-BW.ai` | AI (PDF 1.5) | 234,272,206 B | 842 × 596* | — | `6eb37d7b5ee33290` |
| `AWG_PKG_back.jpg` | JPEG | 8,367,935 B | 4010 × 2677 | — | `af41c33716202849` |
| `AWG_PKG_back-BW.jpg` | JPEG | 3,861,850 B | 4010 × 2677 | — | `be1df2cca235bbcc` |
| `AWG_TI_4C_001-green.psd` | PSD | 203,355,491 B | 3119 × 5033 | 1 | `1b742cdf61eff857` |
| `AWG_TI_4C_001-outlined.psd` | PSD | 75,572,469 B | 5000 × 3750 | 2 | `8a04c018495e91cb` |
| `AWG_TO_4C_001.psd` | PSD | 3,598,590 B | 2444 × 2046 | 1 | `b7b65c13b4965cc5` |
| `AWG_WI_4C_001-outlined.psd` | PSD | 14,684,366 B | 5000 × 3750 | 2 | `8445bd4c94804cc8` |
| `Corridor_Shot-ceiling extended-cmyk.psd` | PSD 16-bit CMYK | 776,856,474 B | 4010 × 2677 | 47 | `8d46416e580c42b6` |

Full sha256 values are in `torbox-pulls/styleguide-previews/styleguide-catalogue.json`.

## What the style-guide files are (own-eyes)

- **Blank show backgrounds (the crossover plates):** `AWG_PKG_BKG_house.jpg`
  (5616 × 5906) is a CLEAN blank photo plate of the Watterson house exterior
  — blue house centre, green house left, purple house right, white picket
  fence, mailbox, lawn, sidewalk, no characters, no text. `AWG_PKG_BKG_home.jpg`
  is the same size, the home interior plate. `AWG_PKG_BKG_school.jpg`
  (2666 × 3543) is the blank school plate. These three are the clean
  plates the crossover clip can actually stand a character in.
- **Corridor hero shot — `Corridor_Shot-ceiling extended-cmyk.psd` (776 MB,
  16-bit CMYK, 47 layers):** the full school corridor photo plate with the
  whole cast composited in it (Gumball, Darwin, T-Rex Tina, Bobert, Penny,
  Leslie, Tobias, Carmen, Jamie, Anton, Ms. Simian, Alan, the flower, the
  eyeball). The layer list is the Gumball lighting method in the open:
  per-character floor reflections (`*REFLECT` layers), a `FULL AO` group
  with a MULTIPLY ambient-occlusion layer per character (`jamieAo`,
  `tinaAo`, `DARWINAO`, `GBAO`…), flat character layers, and a `Vignette`
  OVERLAY. Same stack as the classroom and living room (PR #443): photo
  base → MULTIPLY shadow/AO → character flats → OVERLAY vignette.
  Characters are baked into this file — it is a packaging hero shot,
  not a clean corridor plate (the clean corridor is Pull 1 / Pull 2).
  `AWG_PKG_back.jpg` / `AWG_PKG_back-BW.jpg` are the flattened colour and
  black-and-white versions of the same shot.
- **Character art PSDs (4C):** Alan, Anton, Banana Joe, Bobert, Clare,
  Idaho, Leslie, Masami, Penny, Tina, Tobias, William — each 5000 × 3750
  (except Leslie 2291 × 3378, Masami 806 × 602, Penny 3229 × 2469, Tobias
  2444 × 2046), layers are `BG` + character + face/shadow (e.g. Tina
  `Tina_Shadow`, Idaho `Idaho_Shadow`). The `-outlined` twin of each is
  the same art with an outline variant. `AWG_TI_4C_001-green.psd` is a
  single-layer green Tina T-Rex cutout with clean alpha — the preview
  shows black where the layer is transparent (JPEG has no alpha), which
  is the file's transparency, not a black background in the art.
- **Packaging:** hangtag JPGs/AI (die-cut shapes), badges AI, elements AI,
  `AWG_PKG_BK.eps` (binary DOS EPS — no renderer on this VM, recorded by
  header only, no preview). These are retail packaging art, not settings.

## How to use this for the crossover clip

- **House exterior:** `AWG_PKG_BKG_house.jpg` (clean, no characters).
- **House interior:** kitchen TIF (flat plate) + living room PSD (Pull 1,
  80 layers) + `AWG_PKG_BKG_home.jpg`.
- **Town:** the Elmore street photo inside the Elmore spread / Town
  posters — the cleanest town plate is the street itself; the posters
  and spreads carry baked-in characters and text that must be left out.
- **School:** Pull 1 corridor PSD + Pull 2 classroom/stadium/corridor/
  playground/exterior/gym + this pull's corridor hero shot (characters
  baked in — reference only, not a plate).

## Pull 4 — next download (all 138 Gumball .fla)

Slices 105, 106, 107 of `documents-zip-slices-v1`. Verified in the
catalogue: **138 Gumball `.fla`, 2,559,808,643 B total** — 44 start in
slice 105, 93 in slice 106, 1 in slice 107
(`GB227Lesson_Sc014_V004_Clean_JA.fla`). Includes
`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` (1,740,533 B, slice 106,
offset 212,099,960,644) and the full LATEST_PUPPETS set (Anais / Dad /
Darwin / Gumball / Mom — present twice in the vault, same sizes).
Each file + its `.sha256.txt` companion; verify sha256 before use.

| Slice | File to download |
|---|---|
| 105 | `slice-210000000000-2000000000.bin` |
| 106 | `slice-212000000000-2000000000.bin` |
| 107 | `slice-214000000000-2000000000.bin` |

Download URLs are in `torbox-pulls/documents-slices-release.json`
(release `documents-zip-slices-v1`). After Pull 4: the `.fla` are
opened first-hand (XFL `DOMDocument.xml` / library) — the V3 lane's
swap/pivot findings get checked against the real files.

## Workdir

- Slices: `torbox-pulls/slices/` (78, 81, 87, 88, 90, 98 verified)
- Extracted: `torbox-pulls/house-extracted/` (9 files, 462 MB),
  `torbox-pulls/styleguide-extracted/` (32 files, 1.7 GB)
- Previews + machine catalogues: `torbox-pulls/house-previews/`
  (9 JPGs, 1.6 MB + `house-catalogue.json`),
  `torbox-pulls/styleguide-previews/` (31 JPGs, 7.0 MB +
  `styleguide-catalogue.json`; EPS has no preview)
- Tools: `torbox-pulls/extract_pull3.py` (exact-name byte-range
  extraction; picks the catalogue copy whose range is covered by
  slices on disk — duplicate basenames exist in the vault),
  `torbox-pulls/catalogue_pull3.py` (PSD/TIFF/JPG/AI cataloguer;
  AI rendered with `pdftoppm`, EPS header-only)

# Gumball .fla — Pull 4 (TorBox)

Source: `Documents.zip` (TorBox torrent 119449922, "Cartoon Network documents"),
slices 105 / 106 / 107 of release `documents-zip-slices-v1`
(`mhvnsnt/cn-gigaleak-documents-archive`). Extracted by byte range only —
never the whole zip. All 3 slices sha256-verified against their `.sha256.txt`
before use; every entry CRC32-verified against the catalogue
(`torbox-pulls/catalogue.json`).

This is the complete Gumball Flash set from the vault: **every `.fla` under
`Documents/Gumball/` — 138 entries, and zero Gumball `.fla` live outside
slices 105–107** (checked against the full catalogue). Study only — no CN
art goes into any show file except the explicitly authorized crossover clip.

## What was pulled

| | |
|---|---|
| Entries | **138** `.fla` (2,559,808,643 B total) |
| Slices | 105: 44 entries · 106: 93 · 107: 1 |
| Slice sha256 | 105 `318e9bc5…`, 106 `6af1c408…`, 107 `e19a7acd…` (full values in `fla-catalogue.json`) |
| CRC32 | **138 / 138 OK**, zero failures |
| XFL (ZIP of XML) | 129 files, 2,501,220,995 B |
| OLE binary (CS3-era) | 9 files, 58,587,648 B — see § Binary `.fla` |
| Unique contents | **79 distinct sha256** — 57 groups have 2+ copies (59 extra copies) |
| Symbols (XFL) | **9,291** total across the 129 XFL files |

Full per-file record (vault path, rel path, bytes, crc32, sha256, slice,
offset, kind, stage, fps, symbol count): `torbox-pulls/fla-catalogue.json`.
Full per-symbol timelines: `torbox-pulls/fla-parse-results.json`.
Extractor: `torbox-pulls/extract_pull4.py`. Parser:
`torbox-pulls/parse_fla.py` + `parse_all_fla.py`.

The vault holds the same tree (nearly) twice: `GUMBALL_CHARACTERS_ART_Flash/`
(53 files) mirrors `2d/GUMBALL_CHARACTERS_ART/` (part of the 69 under `2d/`),
and `Family Puppets 03.04.12/` mirrors `Gumball Flash Files/` — same bytes,
different vault paths. The 138 count is vault entries, not unique puppets.
Largest file: `GB222Bumpkin_Sc035_KeyAnim_V007.fla` (MOM sat down,
84,777,585 B). Smallest: `Ocho_Spider.fla` (50,176 B, binary).

### The files at a glance

- **Scene files (84):** 1920 × 1080 @ 25 fps, main timelines 17–444 frames —
  cleaned key animation / cleanup shots (GB202–GB227), e.g. Darwin dancing,
  the family fighting, Richard running/crying/asleep. Flash CS5.5 throughout.
- **Puppet files (43):** 2730 × 1625/1630 @ 25 fps (Dad 2880 × 1630) — the
  `GB200_ORIGINAL_PUPPET_*` family sets plus `Family Puppets 03.04.12`,
  `TurnerCreated_Models`, `Gumball Flash Files`, `NEW GUMBALL CHARACTER ART
  041515` poses. (The other two non-1920 files are both copies of one
  2300 × 1080 scene, `GB214WORDS_Sc061_V012_Clean_MB.fla` — Darwin dancing.)
- **Created with:** Flash Professional CS5.5 (119 files), Animate CC (5),
  CS6 (4), Animate (1). **6 files (3 unique × 2 copies) carry no frameRate**
  in their `DOMDocument`: the three GB209 scene files
  (`BANANA_GB+D_BILBOQUET_SC162`, `DESTROYED_FACE_GUMBALL`,
  `GB+DRW_CRASHED_TOP_SHOT`).

Full `.fla` files (up to 84.8 MB each, 2.56 GB total) stay OUT of the repo
tree (GitHub 100 MB tree limit) — catalogue + doc go in the tree; full files
are re-derivable any time from the verified slices + `extract_pull4.py`.

## GB200 deep dive — `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`

The canonical Gumball puppet, `GUMBALL_CHARACTERS_ART_Flash/LATEST_PUPPETS/`
(slice 106, offset 212099960644, 1,740,533 B,
sha256 `fb30f003a3ce9192…`). Stage **2730 × 1625 @ 25 fps**, Flash CS5.5,
**61 symbols**, main timeline 162 frames / 7 layers. The main timeline
places **4 view assemblies** — V001 (3/4 view), FRONTVIEW, BACKVIEW,
FLOPPED — but only the V001 rig is animated: every FRONTVIEW / BACKVIEW /
FLOPPED symbol is a 1-frame placeholder. The real rig is V001.

### V001 timelines (measured first-hand)

| Symbol | Frames | Named labels | Layers | Notes |
|---|---|---|---|---|
| `GB200_GUMBALL_PUPPET_001` (assembly) | 95 | 0 | 15 | places BODYCOMP / HEADCOMP / arms / legs / tail |
| `GB200_GB_BODYCOMP` | 11 | 0 | 2 | body art, 11 poses |
| `GB200_GB_HEADCOMP` | 309 | 15 | 13 | head poses incl. `GB200_EATING_CYCLE_WIP` f175–308 |
| `GB200_GB_HEAD` | 5 | 5 | 3 | STANDARD / BIG_CHEEK ×2 / SQUASH / Eating |
| `GB200_GB_MOUTH` | **280** | **133** | 6 | see below |
| `GB200_GB_EYESCOMP` | **445** | **37** | 3 | see below |
| `GB200_GB_EYESCOMP_SYMBOL` | 445 | 38 | 7 | same span, fuller layer set |
| `GB200_GB_L_ARM` | 90 | 12 | 4 | labelled poses f25–55 |
| `GB200_GB_R_ARM` | 89 | 14 | 4 | labelled poses f24–55 |
| `GB200_GB_L_LEG` / `GB200_GB_R_LEG` | 10 / 10 | 0 / 0 | 2 / 2 | 10 walk poses each, unlabelled |
| `GB200_GB_TAIL` | — | — | — | tail art |

### Pivots (`transformationPoint`, dominant value in the assembly timeline)

Pivots are per-placement, not per-symbol — animators nudged them. The
dominant value is the rig's pivot; legs never move, arms/head vary.

| Part | Pivot (dominant) | Placements at that value |
|---|---|---|
| L_LEG | **(10.55, 3.35)** | 29 — exactly one pivot, never shifts |
| R_LEG | **(25.5, 4.25)** | 16 — exactly one pivot, never shifts |
| L_ARM | **(13, 8.25)** | 23 of 27 |
| R_ARM | **(9.5, 0.55)** | 22 of 29 |
| MOUTH (in HEADCOMP) | **(40.2, 9)** | most placements; big-cheek variants (41.1, −1.3) |
| BODYCOMP | (37.5, 125.15) | 12 of 16 |
| HEADCOMP | (127.7, 224.45) | 13 of 21 |

### MOUTH — 280 frames, 133 labels

`GB200_GB_MOUTH`, 6 layers. LABEL_01 (guide) carries 10 section labels:

| Section | Frames |
|---|---|
| HAPPY_LIPSYNCH | f0–16 |
| SAD_LIPSYNCH | f17–36 |
| MOUTH_HOLD_POSE | f37–78 |
| STD_EXTRA_MOUTH_FOR_LIPSYNCH | f79–104 |
| STD_LIPSYNCH_BIG_MOUTH_HAPPY | f105–121 |
| STD_LIPSYNCH_BIG_MOUTH_SAD | f124–140 |
| STD_LIPSYNCH_BIG_MOUTH_SAD (same name again) | f141–149 |
| BIG_CHEEK_LIPSYNCH_HAPPY | f150–166 |
| BIG_CHEEK_LIPSYNCH_SAD_ANGRY | f167–229 |
| CHEWING_CYCLE_(to use with eating head shape) | f230–279 |

LABEL_02 (guide) carries 123 named per-frame visemes (HAPPY_REST/B/P,M/N,S/
F/O_01–03/O,U,W/L_01–02/A_01–03–05/A,I/CH,S, the SAD_* set, TEETH_SMILE_01,
OPEN_SMILE_02, …) — 124 `DOMFrame` elements, one of which is a blank `" "`
at f108. **10 + 123 = 133 named labels, 280-frame span.** See § Correction
for why the V3 doc said 124.

### EYESCOMP — 445 frames, 37 labels

`GB200_GB_EYESCOMP`, 3 layers. LABEL_01 carries 10 section labels — and the
timeline **continues 285 frames past f159**:

| Section | Frames |
|---|---|
| STD_EYES | f0–8 |
| CLOSED_EYES | f9–25 |
| STD_SPECIAL_EXPRESSIONS | f26–85 |
| EXT_SPECIAL_EXPRESSION | f86–104 |
| BIG_CHEEK_STD_EYES_001 | f105–124 |
| SPECIAL_POSE_WHISTELING | f125–159 |
| SPECIAL_POSE_EATING_CYCLE | f160–229 |
| STD_HEAD_ANIMATED_BLINK_EXAMPLE_001 | f230–264 |
| STD_HEAD_BIG_CHEEKANIMATED_STD_BLINK_EXAMPLE_002 | f265–299 |
| EXT_HEAD_ANIMATED_BLINK_SUPRISED/SCARED | f300–443 |

LABEL_02 carries 27 per-frame labels (f0–104 only: STANDARD_EYES_01–04,
BLINK_01/02, SNEEKY/SCARED/CRYING/ANGRY/CUTE eyes, …). **10 + 27 = 37
named labels, 445-frame span.** Layers: WHITE_MASK_01/02, CLEAN_EYES_LINES,
EYEBROWS, CLEAN_PUPILS as its own layer — pupils live apart from the lids.

### No joint caps, discs, or circles — confirmed

Searched all **9,291 symbols** (2,261 distinct names) for
joint / knuckle / pivot / hinge / socket / disc / circle: **zero hits**.
The only `CAP` token in any symbol name is `GB200_BLUE_PANTS_GUY_CAP`
(the Blue Pants Guy character's cap); the only `BALL` token is the
`GB208TheColossus_Props_Spitball_PAPER BALL` prop. There is no joint-cap /
joint-disc rigging in this set — limbs are swapped whole by `firstFrame`,
not rotated on joint discs.

## LATEST_PUPPETS — the family, measured first-hand

Canonical copies in `GUMBALL_CHARACTERS_ART_Flash/LATEST_PUPPETS/`
(identical bytes also under `2d/GUMBALL_CHARACTERS_ART/LATEST_PUPPETS/`).
All 2730 × 1630 @ 25 fps except Dad (2880 × 1630) and Gumball (2730 × 1625).
Naming varies by character: Darwin/Mom/Dad use `EYECOMP`, not `EYESCOMP`;
Darwin's mouth is `GB200_DRW_Mouth`.

| Puppet | File | Symbols | MOUTH (frames / labels) | EYES (frames / labels) |
|---|---|---|---|---|
| Anais | `GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002.fla` | 48 | **605 / 122** | **709 / 26** |
| Darwin | `GB200_ORIGINAL_PUPPET_DARWIN_Version002.fla` | 34 | **517 / 138** | **586 / 29** |
| Mom (Nicole) | `GB200_ORIGINAL_PUPPET_MOM_VERSION_002.fla` | 38 | **448 / 118** | **525 / 31** |
| Dad (Richard) | `GB200_ORIGINAL_PUPPET_DAD_VERSION_004.fla` | 46 | **300 / 87** | **280 / 20** |
| Gumball | `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` | 61 | **280 / 133** | **445 / 37** |

Notes: Anais has the biggest mouth/eyes libraries in the family (605/709).
Dad is the only one whose eyes (280f) are shorter than his mouth (300f).
Darwin's HEADCOMP alone is 1,472 frames; his legs carry long cycles
(L_LEG 176f, R_LEG 313f) and his fins are labelled (L_FIN 124f/3,
R_FIN 125f/3). Mom's arms are the most posed in the family (L_ARM 100f/18,
R_ARM 109f/18). As with Gumball, each file's FRONTVIEW / BACKVIEW / FLOPPED
variants are 1-frame placeholders — the V001 rig is the real one.

Older puppet versions also in the pull, for reference: V004 Gumball +
V002 Anais/Darwin/Mom + V003 Dad in `Family Puppets 03.04.12/` (same bytes
again under `Gumball Flash Files/`), V006 Gumball, Darwin V002 CS5 for
Turner, and the CS3 originals (binary, below). `RECOVER_GB200_ORIGINAL_PUPPET_DARWIN_Version002.fla`
is the biggest puppet file by symbol count (312 symbols).

## Binary `.fla` — 9 files, OLE compound, need a JPEXS FFDec job

These nine are pre-XFL Flash (OLE compound documents, `D0 CF 11 E0`),
CRC-verified but **not parseable as XFL** — the ZIP/XML parser does not
apply. They need opening in JPEXS Free Flash Decompiler (FFDec) or
equivalent; do not hand-edit them.

| File | Bytes | Notes |
|---|---|---|
| `2d/TurnerCreated_Models/PrincipalBrown.fla` | 46,516,736 | biggest binary in the pull |
| `2d/TurnerCreated_Models/GumballFamily and HectorLegs-V07.fla` | 3,260,416 | |
| `2d/Flash models - Gumball, Richard, Nicole, Anais and Hector/Gumball-em_V06.fla` | 3,259,904 | |
| `2d/TurnerCreated_Models/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_001_CS3.fla` | 2,736,640 | CS3 original Gumball puppet |
| `2d/TurnerCreated_Models/GB200_HECTOR_ORIGINAL_PUPPET_V001_CS3.fla` | 1,512,448 | CS3 Hector puppet |
| `2d/TurnerCreated_Models/Carrie_Ghost.fla` | 968,704 | |
| `2d/TurnerCreated_Models/Tobias_SportyPuff.fla` | 146,432 | |
| `2d/TurnerCreated_Models/Penny_PeanutAntlers.fla` | 136,192 | |
| `2d/TurnerCreated_Models/Ocho_Spider.fla` | 50,176 | smallest file in the pull |

## The vault `.fla` EOCD quirk — read this before opening one

**Stock Python `zipfile` refuses all 129 XFL files** with the identical
error: `BadZipFile: Bad magic number for central directory`
(0 of 129 open; the 9 binary files are not ZIPs at all). The files are
not corrupt — their central directories are miscounted by one entry.

Measured on `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`: the EOCD
declares 89 entries and `cd_size` 9,639, but the central-directory stream
is only 9,585 bytes holding 89 records — 54 bytes short, exactly one
46+8-byte `mimetype` central-directory record. The file carries a second
local-header copy of `mimetype` (90 local entries vs 89 central-directory
records) that has no central-directory record at all. Across the set:
127 files are off by exactly that one 54-byte record; the two copies of
`RECOVER_GB202REMOTE_Sc103_V0024_cleanup_LW.fla` are off by two records
(184 local vs 182 central, `cd_size` delta 146).

Fix: walk the **local headers** (`PK\x03\x04` records) and decompress each
entry directly — that is what `torbox-pulls/parse_fla.py` does, and it
reads all 129 files cleanly (9,291 symbols, zero parse errors). Do not
"repair" the files by re-zipping them; the quirk is in the vault copy and
re-zipping would change the bytes (and the sha256 in the catalogue).

## Correction to the V3 doc — MOUTH is 280 frames / 133 labels, not 124

The V3 swap-system docs undercount the Gumball mouth and cut the eyes
short. Measured first-hand from the same file the V3 doc was built on
(`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`):

- **MOUTH is 280 frames / 133 named labels, not "124 keyframes".**
  Where 124 came from: the LABEL_02 viseme layer has 124 `DOMFrame`
  elements (123 named + one blank `" "` at f108), and the `GB200_MOUTH`
  art layer also has 124 frames. That is one layer's keyframe count, not
  the timeline — the timeline spans 280 frames and LABEL_01 adds 10
  section labels the old count missed (the last five sections run
  f124–279: BIG_MOUTH_SAD ×2, BIG_CHEEK HAPPY, BIG_CHEEK SAD_ANGRY,
  CHEWING_CYCLE).
- **EYESCOMP continues past f159.** The old section list stopped at
  `SPECIAL_POSE_WHISTELING f125–159`; four more sections follow, to
  f443: `SPECIAL_POSE_EATING_CYCLE` f160–229, `STD_HEAD_ANIMATED_BLINK_EXAMPLE_001`
  f230–264, `STD_HEAD_BIG_CHEEKANIMATED_STD_BLINK_EXAMPLE_002` f265–299,
  `EXT_HEAD_ANIMATED_BLINK_SUPRISED/SCARED` f300–443. Total 445 frames /
  37 labels, not a 160-frame comp.

Files to correct (recorded here; not edited in this lane):
`v3-swap-system/GUMBALL-FIRSTHAND.md` §3 ("124 keyframes", sections ending
f105–121) and §4 (EYESCOMP sections ending f125–159);
`v3-swap-system/CN-IN-OUR-LANGUAGE.md` rows 4–5;
`v3-swap-system/V3-SWAP-SYSTEM.md` ("124-frame MOUTHCOMP").
The V3 design conclusion stands — a 5-variant mouth slot is still the
right simplification — but the source library it simplifies is 280 frames,
not 124, and the eating-cycle mouth/eyes (f230–279 / f160–229) are part of
it.

## Next pull — slice 99, the AWG hangtag set

Slice 99 is `slice-198000000000-2000000000.bin` of
`documents-zip-slices-v1` (+ its `.sha256.txt`; verify before use).
It completes the AWG packaging hangtag set left unfinished by Pull 3:

| Entry | Bytes | Note |
|---|---|---|
| `AWG_PKG_HANGTAG-DIE CUT.ai` | 234,318,327 | starts in slice 98, ends in slice 99 — the straddler |
| `AWG_PKG_HANGTAG.ai` / `.pdf` | 353,623,694 each | fully in slice 99 |
| `AWG_PKG_HANGTAG-DIE CUT.pdf` | 234,318,327 | fully in slice 99 |
| `AWG_PKG_HANGTAG_DIECUT-BW.pdf` | 234,272,206 | fully in slice 99 |
| `AWG_PKG_HANGTAG-BW.ai` / `.pdf` | 234,222,542 each | fully in slice 99 |

Slice 99 also starts the shoebox trio (`AWG_PKG_SHOEBOX.jpg` 9,305,397 B,
`.pdf` / `.ai` 263,229,647 B each). Same route as Pulls 1–4: browser
download, sha256-verify, extract by byte range, CRC32-verify, catalogue,
land the doc. After that, the Gumball `.fla` set is done — Pull 4 was all
of it.

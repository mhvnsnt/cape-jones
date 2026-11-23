# Documents.zip — full catalogue

Catalogued 2026-11-23 from the tail slice of the GitHub slices release
(`documents-zip-slices-v1`, `mhvnsnt/cn-gigaleak-documents-archive`).
Parser: `torbox-pulls/zipcat.py` (EOCD + ZIP64 central directory).
Full 79,772-entry machine catalogue (23 MB JSON) lives in the workdir at
`torbox-pulls/catalogue.json` — this doc is the human summary + pull list.

## What it is

- **79,772 entries: 72,369 files + 7,403 directories**, all under `Documents/`.
- **349.99 GB total, stored (method 0, no compression)** — every byte of the
  zip is payload. ZIP64: 79,772 entries, central directory 13,817,072 bytes.
- EOCD entry count matches the parsed count exactly (79,772 = 79,772).
- Zip served size 350,016,069,416 bytes; TorBox lists 350,016,069,428 —
  12 bytes more. Unsettled; per-slice sha256 verification will settle it.
- File types: 31,128 EPS, 8,795 PSD, 7,907 TIF, 6,552 JPG, 5,049 AI,
  2,412 PDF, 595 MP3, 374 PNG, **168 .fla**, 126 SWF, 124 MOV, 98 nested .zip.

## Per-show breakdown (files, uncompressed)

| Show | Files | Size |
| --- | --- | --- |
| Adventure Time | 13,484 | 95.63 GB |
| HB Classics Boomerang | 11,569 | 10.87 GB |
| Powerpuff Girls Original | 7,931 | 2.65 GB |
| Camp Lazlo | 5,796 | 6.66 GB |
| Regular Show | 2,999 | 29.78 GB |
| Kids Next Door | 2,700 | 5.61 GB |
| LOONEY TUNES (Classic) | 2,654 | 0.89 GB |
| Looney Tunes Classic | 2,654 | 0.89 GB |
| BAKUGAN | 2,478 | 32.79 GB |
| Dexter's Lab | 2,298 | 0.45 GB |
| **Gumball** | **1,893** | **65.89 GB** |
| Ed Edd N Eddy | 1,746 | 6.35 GB |
| Fosters | 1,707 | 7.05 GB |
| Grim Adventures of Billy & Mandy | 1,620 | 5.73 GB |
| THE LOONEY TUNES SHOW | 1,225 | 3.72 GB |
| Cow & Chicken | 1,213 | 0.28 GB |
| Johnny Bravo | 1,104 | 0.65 GB |
| TEEN TITANS | 970 | 1.10 GB |
| Johnny Test | 863 | 1.98 GB |
| Scooby-Doo! Mystery Inc | 845 | 12.16 GB |
| Powerpuff Girls 10th Anniversary | 655 | 0.12 GB |
| MGM Shorts | 635 | 7.65 GB |
| I Am Weasel | 502 | 0.12 GB |
| Space Ghost C2C | 474 | 0.85 GB |
| Gym Partner | 435 | 5.43 GB |
| OK KO | 428 | 12.05 GB |
| DUCK DODGERS | 393 | 0.70 GB |
| Garfield | 257 | 2.07 GB |
| Powerpuff Girls Special | 182 | 3.71 GB |
| Robot Chicken | 147 | 0.43 GB |
| New Looney Tunes | 104 | 0.10 GB |
| Wabbit | 76 | 2.37 GB |
| The Pink Panther | 76 | 0.03 GB |
| PDFs (HB model sheets) | 63 | 0.42 GB |
| Transfer(1) | 48 | 0.03 GB |
| BONUS (nested zips, see below) | 47 | 21.89 GB |
| Juniper Lee | 38 | 0.15 GB |
| PPGZ | 29 | 0.26 GB |
| Jimmy Two Shoes (`j2s-…`) | 13 | 0.28 GB |
| Looney Tunes Cartoons | 12 | 0.09 GB |
| Foster's Home | 1 | 0.03 GB |

Notes: the two Looney Tunes Classic folders are duplicates of each other
(2,654 files / 0.89 GB each). Gumball is the third-biggest show by size
after Adventure Time and BAKUGAN, despite fewer files — its PSDs are huge.

## Gumball — what is actually here (1,893 files, 65.89 GB)

- `NEW GUMBALL STYLE GUIDE 071415` — 802 files, 20.20 GB.
- `Show Art - Original Delivery` — 418 files, 24.99 GB. This is where the
  settings live: school classroom, corridor, gym, playground, stadium,
  school exterior, Watterson house kitchen, Elmore town pages.
- `Gumball Asset Pack (USE)` — 324 files, 10.14 GB.
- `2d` — 182 files, 1.11 GB (includes duplicate puppet sets).
- `GUMBALL_CHARACTERS_ART_Flash` — 154 files, 1.09 GB.
- `NEW GUMBALL CHARACTER ART 041515` — 107 files, 0.25 GB.
- `Gumball Flash Files` — 24 files, 1.06 GB.
- `Gumball_s2_EMEA_Print` — 5 files, 5.76 GB (two 4.3 GB .psb posters).
- `NEW GUMBALL BACKGROUNDS.zip` — **one nested zip, 479.9 MB**,
  the whole background pack in one entry (slice 74).
- `Gumball Back to School Stunt`, stills, logos, fonts, sales deck.

### Crossover clip settings — confirmed in the vault

School: 129 entries, 4.79 GB, including:
- `GB36_sc33_School_Classroom_Final_upressed_v4.psd` — 970.8 MB (slice 85)
- `GB04_sc120_School_Stadium_Final_4_upressed.psd` — 303.8 MB (slice 88)
- `GB21_sc18_School_Corridor.tif` — 165.4 MB (slice 89)
- `GB37_sc018_SchoolGym_final.tif` — 183.8 MB (slice 91)
- `GB17_SchoolPlayground_sc024_FINAL.tif` — 82.8 MB (slice 90)
- `GB00_Schoolexterior_BM_final.tif` — 98.0 MB (slice 90)

Watterson house / Elmore town:
- `GB30_sc53_WatersonsHouse_Kitchen_final.tif` — 177.5 MB (slices 87–88)
- `06_Page_08-09_The_Wattersons.psd` — 156.2 MB (slice 81)
- `05_Page_06-07_Elmore.psd` — 99.1 MB (slice 88)
- `GB_Town_L_Final.jpg` / `GB_Town_P_Final.jpg` (slice 78)
- `AWG_PKG_BKG_house.jpg` — 33.8 MB (slice 98)

### .fla files — 138 Gumball, and the count is now settled

- **138 Gumball .fla, 2.56 GB total** (slices 105–107). This settles the
  unreconciled count from the inventory (9 vs 71 vs 138): **138 is the
  real number inside the vault.**
- Includes `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` (1.7 MB,
  slice 106) and the full `LATEST_PUPPETS` set: Anais v002, Dad v004,
  Darwin v002, Gumball v008, Mom v002 — plus v001–v006 variants, Turner
  CS3/CS5 builds, and 130+ scene KeyAnim .fla files.
- Also in the vault: 20 Fosters .fla, 10 Jimmy Two Shoes .fla.

## CHOWDER — NOT IN THE VAULT

**Zero entries match "chowder" anywhere in Documents.zip.** The owner's
#2 priority has no source in this archive. Chowder material must come from
elsewhere: it is not in any of the 38 cn-gigaleak repos either (research
docs only). Do not claim a Chowder pull until a real source is found.

## BONUS — 47 files, 21.89 GB, contents unknown

Nested zips by year (`2000.zip`–`2020.zip`, 200–868 MB each) plus
hash-named zips (`88pd8l.zip`, `1fama1.zip`, …). Contents cannot be
catalogued without extracting them — a later pull.

## Pull list — exact slices (GitHub slices release, verify sha256 first)

Slice size is 2,000,000,000 bytes; slice N covers zip bytes
[N·2,000,000,000, (N+1)·2,000,000,000).

### Pull 1 — Gumball backgrounds pack (do first)

| Slice | File | sha256 |
| --- | --- | --- |
| 74 | `slice-148000000000-2000000000.bin` | `c05c0f277bb8604501243da9335f71ecd306591b860181030ba7fa0cb0ac06e8` |

Contains `NEW GUMBALL BACKGROUNDS.zip` (479.9 MB) whole. Extract it,
catalogue its contents, land the backgrounds.

### Pull 2 — School settings (crossover clip)

| Slice | File | sha256 |
| --- | --- | --- |
| 85 | `slice-170000000000-2000000000.bin` | `d7da7afbfe348bcd86cbdaff82a34815218b2b08d6cb3703ff52de64b06ad9d7` |
| 88 | `slice-176000000000-2000000000.bin` | `2f7180b1dd396c89c0dd03d03a3d2a4930f9db0dea64c1df47ecb5ff53383e6d` |
| 89 | `slice-178000000000-2000000000.bin` | `420af58f3e1b72c6dbcb777e5aaba109cb2c3260b4acc9a266e11bda0f9f1ee6` |
| 90 | `slice-180000000000-2000000000.bin` | `bac4de98458472a75ba6c1bf06448e8598eb2acb0bf75360ea59cc3f60a2698f` |
| 91 | `slice-182000000000-2000000000.bin` | `8af75dde3cead400949ef6eba3860555802d50fe6a748735d19e89a8de1a75c8` |

Classroom, stadium, corridor, playground, school exterior, gym.

### Pull 3 — Watterson house + Elmore town (crossover clip)

| Slice | File | sha256 |
| --- | --- | --- |
| 78 | `slice-156000000000-2000000000.bin` | `a34ecd83ff5c4667b5e13e786c28c86c83d603cfe00e2f8d5c30727e4a4bfb1c` |
| 81 | `slice-162000000000-2000000000.bin` | `f3a14c1b40f342f232d84a305da941f201d5b11486938f62abde78be42fc5ac9` |
| 87 | `slice-174000000000-2000000000.bin` | `0cbae9d0f011f3aabced309d0927e2a744d087eb1fcbed8d3d6723e098a90273` |
| 88 | (same as Pull 2) | — |
| 90 | (same as Pull 2) | — |
| 98 | `slice-196000000000-2000000000.bin` | `e5ca8d3378309dac19ed0ecc40aab622e678775084414ec0264a9ddec88499a7` |

Kitchen, Wattersons pages, Elmore page, town posters, house background.

### Pull 4 — Gumball puppet .fla files (Clean-Up Jones 1 / V3)

| Slice | File | sha256 |
| --- | --- | --- |
| 105 | `slice-210000000000-2000000000.bin` | `318e9bc5b35e2c7033d22fae5400a7dba45fb5ef7e4045a35ab69db2a47bc800` |
| 106 | `slice-212000000000-2000000000.bin` | `6af1c408066068ec072a16c19a40efb25a915117bbf2637ae038324b17d310c7` |
| 107 | `slice-214000000000-2000000000.bin` | `e19a7acdeadc4d740d4aefceb4373f586eba269712f9117848943d633549f756` |

All 138 Gumball .fla (2.56 GB), including the GB200 puppet set.

### Later pulls

- BONUS nested zips: locate per-zip slices with `zipcat.py locate`
  after Pulls 1–4, extract one at a time.
- Adventure Time / Regular Show / BAKUGAN / the rest: pull by the
  inventory priority, one show at a time, same method.

## How to pull (the rule)

GitHub Slices is always how we deal with big files. Download ONLY the
slices in the pull list, verify each slice sha256 against MANIFEST.txt
before use, extract only the wanted entries with `zipcat.py locate`
(byte ranges are in `catalogue.json`), verify each entry, land it in the
repo branch → PR → merge, clear the slice. Never the whole 350 GB.
Disk on this VM is ~74 GB free: a few 2 GB slices at a time, no more.

TorBox direct download stays blocked: `requestdl` needs the token as a
query parameter (stored credential is Bearer-only) and the Essential
plan caps a file at 200 GiB vs the 326 GiB zip.

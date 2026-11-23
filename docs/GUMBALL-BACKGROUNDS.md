# NEW GUMBALL BACKGROUNDS — Pull 1 (2026-11-23)

TorBox Pull 1, from the Documents.zip vault. Catalogue: `docs/DOCUMENTS-CATALOGUE.md`
(PR #441). This doc is the catalogue of the pulled pack. Study-only source
material, per the owner's rule: use it to make OUR files like theirs, and to
build the authorized crossover clip (Cape Jones walking through Gumball's
settings, owner 2026-11-23 09:05 EST). No CN art goes into a show file except
through the crossover clip the owner names.

## Source — verified, multi-source

- Vault entry: `Documents/Gumball/Gumball/NEW GUMBALL BACKGROUNDS.zip`
- In Documents.zip at local header offset 148,992,580,854, method 0 (stored),
  479,874,527 bytes, CRC32 2802978339.
- Pulled from GitHub slice 74 (`slice-148000000000-2000000000.bin`,
  2,000,000,000 bytes, sha256
  `c05c0f277bb8604501243da9335f71ecd306591b860181030ba7fa0cb0ac06e8` —
  matches its `.sha256.txt`), release `documents-zip-slices-v1` on
  `mhvnsnt/cn-gigaleak-documents-archive`. Extraction read only the entry's
  own byte range out of the slice (no whole-zip download, no TorBox direct
  download — that route is blocked: query-token placement + Essential
  200 GiB/file cap vs the 326 GiB zip).
- Extracted nested zip: `NEW-GUMBALL-BACKGROUNDS.zip`, 479,874,527 bytes,
  sha256 `5c50207c12ed13076bc2ddecfd730776b9f1ac92b6a259cbad62573509ccb3de`,
  CRC32 2802978339 — matches the catalogue entry. `zipfile.testzip()` = None
  (all CRCs OK). Workdir copy:
  `~/workspace/_cape-jones-parking-lot-2d/torbox-pulls/NEW-GUMBALL-BACKGROUNDS.zip`
  (parser: `torbox-pulls/zipcat.py`).

## What is inside — 3 production PSDs, 648,938,201 bytes uncompressed

The "whole background pack" is three stock background model sheets. Nothing
else: two `.DS_Store` files (junk, 6,148 bytes + 120 bytes) and a `__MACOSX`
folder. Own-eyes verified from rendered composites (1920-wide JPG previews
in the workdir at `torbox-pulls/backgrounds-previews/`).

### 1. Alley — `Gumball_Stock_Backgtround_Model_Sheet_Alley_GB238TAPE_Sc046.psd`

- 160,086,576 bytes, sha256
  `95c2ca54be9173f971c61fd19cfe4a05a03938fc24026721514c928a4d8763c0`
- 4752 x 3168, RGB, 16-bit, 3 channels, 2 layers: `BG`, `sc 046`.
- What it is, own-eyes: a real photo plate of a back alley — brick walls,
  cracked render, a wall marked "9", graffiti, trash bags and cardboard
  piled at the right, drain grate foreground. The `BG` layer is 4760 x 3172,
  8 px larger than the canvas, so the composite carries a red border on all
  four sides — that red frame is IN the file, not a render artifact.
- Use: Elmore town / alley setting for the crossover clip; the photo-plate
  method (real photo as background, drawn characters on top) is the Gumball
  house style to study.

### 2. School Corridor — `Gumball_Stock_Backgtround_Model_Sheet_School_Corridor_6k_GB110FIGHT_SC133.psd`

- 242,602,784 bytes, sha256
  `97798ebff162dd1160d2c22551547670b206b9a371feacfe902cde55aea580ba`
- 6000 x 3375, RGB, 16-bit, 3 channels, 7 layers: `bty`, `locker hole`,
  `locker shadow`, `locker door`, `vigniette`, `Layer 1` (hidden), `label`
  (hidden).
- What it is, own-eyes: Elmore Junior High corridor — a full wall of red
  lockers, one locker open (the `locker door` / `locker hole` / `locker
  shadow` layers are that open locker, separable), stickers and graffiti
  ("BOMB", "HELP ME!"), checkered tile floor with a red mat, purple
  skirting, pale yellow upper wall.
- Use: THE school setting for the crossover clip — Cape Jones walking the
  corridor. The open locker is a separate layered element, not baked in.

### 3. Wattersons House, New Living Room — `Gumball_Stock_Backgtround_Model_Sheet_WattersonsHouse_NewLivingroom_v04_GB100KEYCAM_SCF1.psd`

- 246,242,573 bytes, sha256
  `550b6608f2655df9fbed9517edaef2a92cc9c7137529840b58c91050be537875`
- 6000 x 3667, RGB, 8-bit, 4 channels, 80 layers.
- What it is, own-eyes: the Watterson living room — plaid sofa, coffee
  table, stairs with wooden balustrade, family portrait (Richard, Nicole,
  Gumball, Darwin, Anais) on the wall, unicorn poster, floor lamp, window
  light. Layers include `granny photo`, `shadows`, `shadow base`,
  `sofa shadow`, `around window`, `inside kitchen`, `stairs railing`,
  `door`, `curtain transparency`, `shading adjustment`, and a hidden
  `HIDE PHONE` layer.
- Use: THE house setting for the crossover clip. 80 layers means the room
  is built to be re-lit and re-dressed per shot — study how the shadow
  layers are separated from the furniture.

## What is NOT in this pack

No classroom, no school exterior, no gym, no stadium, no playground, no
Elmore town street, no kitchen — those are separate Documents.zip entries,
in Pull 2 (school slices 85, 88, 89, 90, 91) and Pull 3 (house/town slices
78, 81, 87, 88, 90, 98) in `docs/DOCUMENTS-CATALOGUE.md`. Do not claim this
pack covers them.

## Where the full PSDs live — and why they are not in the tree

Each PSD is 160–246 MB. GitHub refuses files over 100 MB in a repo tree,
and this repo has no Git LFS. So the full PSDs are NOT in this repo. They
live in the workdir at
`~/workspace/_cape-jones-parking-lot-2d/torbox-pulls/backgrounds-extracted/NEW GUMBALL BACKGROUNDS/`,
and they are re-derivable at any time from slice 74 + `zipcat.py` (see
Source above). The 1920-wide JPG previews (424,500 + 322,465 + 337,957
bytes) are in the workdir at `torbox-pulls/backgrounds-previews/` and are
the files to browser-upload into
`production/2d-parking-lot/gumball-backgrounds/` — the connector cannot
carry binary files, so that upload is a parent job, not this PR.

## Next pulls

- Pull 2 (school): slices 85, 88, 89, 90, 91 — classroom, stadium,
  corridor, playground, exterior, gym. Needs a browser download first.
- Pull 3 (house/town): slices 78, 81, 87, 88, 90, 98.
- Pull 4 (puppets): slices 105, 106, 107 — all 138 Gumball .fla, for
  Clean-Up Jones 1 / V3.
- Exact slice filenames and sha256 prefixes are in
  `docs/DOCUMENTS-CATALOGUE.md`. Disk on the work VM is ~71 GB free —
  a few 2 GB slices at a time, never the whole zip.

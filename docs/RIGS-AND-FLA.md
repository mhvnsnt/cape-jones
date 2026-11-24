# RIGS AND .FLA — full inventory

Owner rule: nothing held hostage. Every rig and every .fla we have worked on is inventoried here, landed in the repo (tree or Release), and merged into main. Rejected cuts are NOT landed as videos; their rigs ARE landed as rigs.

## Our own rigs (Blender .blend)

| Rig | Size (B) | SHA-256 | Status on main |
|---|---|---|---|
| `brotheman-rig-animated.blend` | 140613 | `2bfea968b1c8329ad0d81f8523d410b71bab5ed7d276e31baf0d29b8e16cd057` | ALREADY ON MAIN |

BROTHERMAN animated-scene rig — already on main.

| `brotheman-rig-move.blend` | 141075 | `bf831a17fb812091b390c276d7ce170cec5ad6f9d93fb2ecb6a6f56479d9f48b` | ALREADY ON MAIN |

BROTHERMAN movement-test rig — already on main.

| `brotheman-rig.blend` | 135471 | `a7f4a8d3870c8b65e0e07b58bbbb0318a70d761fa29738c0b7196ea648d724d7` | ALREADY ON MAIN |

BROTHERMAN Rig Jones 1, 26 bones, 44 planes — already on main.

| `purple-lot-v2-handswap-rig.blend` | 121525 | `f33d3d6406b10cd0393b92bbb738a02bd1640fd814a3e1a4c38f91fb8f84bc53` | STAGED — browser upload to tree |

Handswap rig, 16 bones, one hand plane per side — REJECTED cut, rig landed as a rig (joint caps present in this rig; see no-caps rule).

| `purple-lot-v2-mixed-rig.blend` | 119987 | `9bf7c074e3e538f83712fc4412f7681297f89f986aa29e937d2a50f44b271382` | STAGED — browser upload to tree |

Mixed-cut rig — REJECTED cut, rig landed as a rig.

| `purple-lot-v2-rig.blend` | 119896 | `d0c39a59efcc49773231a1fb8d016c436966b79bc1a51c561764d470628eb70f` | STAGED — browser upload to tree |

Rig Jones 1 — official V2 rig, 12 bones, native Blender cutout puppet from the 28 sliced parts (T-pose v8).

| `purple-lot-v3-rig.blend` | 125004 | `ffce3535c8756bcd3cdb9d12bce1290c8f28d9abcc92604f54d5d286b63058cd` | STAGED — browser upload to tree |

Rig Jones 2 / Clean-Up Jones 1 — 17 bones, 7 slots, socket-cut joins, invisible swap, measured pivots (PR #448 docs).

Tree paths (staged): `production/2d-parking-lot/rig/` for the V2 rigs, `production/2d-parking-lot/v3/` for the V3 rig. BROTHERMAN rigs already live at `production/2d-parking-lot/brotheman/`. `.blend1` backups are NOT landed.

## Gumball S2 rig zips (downloaded releases)

| File | Size (B) | SHA-256 | Route |
|---|---|---|---|
| `Gumball_S2_Rigs.zip` | 685,983,662 | `b0fc20ccdf20e1db5733a13ad0fe231c10b62988d9f5464459ad4d41c8648809` | GitHub Release asset (under 2 GB) |
| `CN-Leaks-001-gumball.zip` | 1,709,550,213 | `f33dc420f08a5b137adecac3915e049b14d66e70adb7b2527847bd90b9cdce58` | GitHub Release asset (under 2 GB; 876 files, 71 .fla) |

Source: private release `untagged-1676e192ae8c72e95791` on `mhvnsnt/cn-gigaleak-gumball`, downloaded 2026-11-23. Local copies in `~/workspace/browser_downloads/`.

## Gumball .fla from the vault (Pull 4)

- **138 vault files, 2,559,808,643 B total, CRC32 138/138 OK**, extracted from verified slices 105/106/107 of `documents-zip-slices-v1`.
- **79 unique contents by SHA-256, 1,588,578,257 B** — 57 duplicate groups (56 pairs + 1 group of 4). The `GUMBALL_CHARACTERS_ART_Flash/` (53 files) and `2d/GUMBALL_CHARACTERS_ART/` (69 files) trees are near-mirrors.
- By kind: **102 scenes, 25 puppet rigs, 11 character models/poses**. By slice: 105: 44, 106: 93, 107: 1.
- Largest: `GB222Bumpkin_Sc035_KeyAnim_V007.fla` 84,777,585 B (x2). Smallest: `Ocho_Spider.fla` 50,176 B.
- 9 binary .fla files (OLE compound, CS3-era) were CRC-verified but NOT parsed — they need a JPEXS FFDec job.
- Quirk: the vault .fla EOCD is off by one 54-byte entry, so stock `zipfile` refuses them; the catalogue was built with a local-header walker.
- Full 138-row table: [`docs/FLA-INVENTORY.md`](FLA-INVENTORY.md) (name, vault path, size, full SHA-256, slice + offset, unique/duplicate, what it is). Machine data: `fla-inventory-data.json` (workdir).

### GB200 v008 deep dive (first-hand)
- 61 symbols, 4 views (V001/FRONTVIEW/BACKVIEW/FLOPPED), 2730x1625 @ 25fps.
- **MOUTH spans 280 frames / 133 named labels** (correction to the V3 doc's 124 — it continues past f159: BIG_MOUTH_SAD, BIG_CHEEK, CHEWING_CYCLE f230-279).
- **EYESCOMP spans 445 frames / 37 labels** (EATING_CYCLE, animated blink examples).
- L_ARM 90-frame span / 12 labeled poses, R_ARM 89 / 14 — per-side sets, not mirrors.
- Pivot rule CONFIRMED exactly (L_LEG (10.55, 3.35), R_LEG (25.5, 4.25), L_ARM (13, 8.25), mouth at (40.2, 9)).
- **No-caps rule CONFIRMED at vault scale:** token search across all 9,291 symbols returns only a baseball cap and a spitball PAPER BALL — zero joint caps/discs/circles.
- LATEST_PUPPETS family: Anais MOUTH 605f / EYES 709f, Darwin 517/586, Mom 448/525, Dad 300/280, Gumball 280/445. Anais/Darwin/Mom LATEST copies differ from the Family Puppets copies under the same version number.

### Gumball-study .fla files (24)
Only 2 are real files, both byte-identical duplicates of vault files: `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` (1,740,533 B) and `GB202REMOTE_Sc094_Clean_V023_STN.fla` (22,851,853 B). The other 22 are 0-byte stubs from the XFL unpack — the real content is in the `gb202-xfl/` XFL tree. The study adds 0 unique .fla contents; combined unique total stays 79.

## Release package — 79 unique .fla files

| File | Size (B) | SHA-256 |
|---|---|---|
| `gumball-fla-unique-79.zip` | 1588625861 | `2f2cd00d5eabf50af4affc69628651718ae2ae3f3bfe313334225cc54858d74d` |

Contents: the 79 unique .fla files (flat, under `fla-unique/`, 3 same-basename collisions renamed with a `-family-puppets` suffix) + `fla-unique-MANIFEST.json` (name, size, full SHA-256, vault path, kind per file). ZIP_STORED, 80 entries, `testzip()` clean. Staged at `torbox-pulls/rigs-fla-release/gumball-fla-unique-79.zip`. Goes up as a GitHub Release asset (under the 2 GB per-asset limit).

## What is NOT in the repo (and why)

- The full 138-file / 2.56 GB vault extraction stays on disk (re-derivable from verified slices 105/106/107); only the 79 unique contents ship in the Release zip. Duplicates are recorded, not shipped twice.
- The rejected mixed cut and handswap cut videos are NOT landed as videos. Their rigs ARE landed as rigs (see table above).
- `.blend1` backups, 0-byte .fla stubs, and the local Blender install are NOT landed.
- No CN art goes into show files.

## Next pull

Slice 99 — the AWG hangtag set (`AWG_PKG_HANGTAG-DIE CUT.ai` straddles slices 98-99, plus HANGTAG .ai/.pdf, DIECUT-BW .pdf, BW .ai/.pdf).

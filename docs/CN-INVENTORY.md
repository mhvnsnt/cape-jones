# CN-INVENTORY — All the Cartoon Network stuff we have

**Date:** 2026-11-23
**Owner direction:** 2026-11-23 09:03 EST (inventory), 09:04 EST (Chowder priority), 09:05 EST (systems/mechanics correction + crossover authorized), 09:06 EST (Clean-Up Jones V1 standard), 09:07 EST (TorBox sign-in — get everything helpful piece by piece).
**Verified by:** reading the GitHub repos live on 2026-11-23 — root listing of all 38 `cn-gigaleak-*` repos, plus HANDOFF/README/RESEARCH/KIT-INDEX/PULL-TRACKER docs where they exist. No torrent download was done in this lane. No CN art went into any show file.

## 0. The corrected rule (owner, 2026-11-23 09:05 EST)

The earlier rule in this doc's first draft was backwards. The corrected rule is:

- **We DO want their systems and mechanics wholesale — adapted so they work for OUR show.** Not making Gumball the show. Making HIS show — Cape Jones — but using their stuff, wholesale, to make his show.
- **We CAN use their characters, backgrounds, and stuff — ONLY to make our own stuff:** to learn how industry-standard / real-network / commercial-grade files are made, and to make OUR files like theirs.
- **Crossover is AUTHORIZED, explicitly:** a 10-second or 30-second clip of Cape Jones walking through all of Gumball's settings, made exactly how they make their show — how they use their stuff, how they make their show — so he feels like he is IN their world, in the Gumball world. Order: **V3 cut first, crossover clip next after it.** The clip itself is a separate build lane — scoped in §7 here, not built in this lane.
- **Clean-Up Jones V1 (owner, 2026-11-23 09:06 EST):** this is the chance to start Clean-Up Jones V1 — the next version of Rig Jones (Rig Jones 2 = Clean-Up Jones 1). Getting the next version of Rig Jones onto the level of the Gumball rigs, **100% how they do theirs**. That is the standard for the V3 cut.
- Study-only on the leaked material itself: method travels, CN/Gumball characters and artwork never go into Cape Jones show files except in the explicitly authorized crossover clip, where Cape Jones walks through Gumball's settings on purpose, by name.

## 1. The big picture — the TorBox torrent

- **The torrent is ~172.84 GB / 42,549 files across 22 repos**, per `cn-gigaleak-ok-ko/PULL-TRACKER.md` (the full-pull tracker). The owner calls it "almost 200 GB" — same torrent, rounded.
- **Pipeline (per the tracker):** TorBox cached torrent → range-extract → verify → GitHub repo + TeraBox home → clear local. "Reference files are never modified; Cape Jones builds live only in mhvnsnt/cape-jones."
- **Status: almost everything is still PENDING, 0 landed.** Per the tracker table, every repo except OK KO is `pending / 0 landed`. OK KO was `extracting (TorBox) / 208 of 428` at tracker time and has since completed (see §3).
- **TorBox gap (what only lives in the torrent, not in any repo tree):** the per-show totals in the tracker table, §2. Biggest: Bakugan 2,228 files / 32.61 GB, Adventure Time 5,546 files / 28.82 GB, Regular Show 2,280 files / 25.20 GB, Gumball 855 files / 24.59 GB, Camp Lazlo 5,190 files / 6.02 GB, Powerpuff Girls 4,904 files / 4.54 GB, Teen Titans 7,167 files / 4.52 GB, Looney Tunes 3,821 files / 3.44 GB, Billy & Mandy 1,418 files / 5.15 GB, Scooby-Doo 498 files / 8.66 GB.
- **TorBox sign-in (owner, 2026-11-23 09:07 EST):** sign into TorBox to reach the big almost-200 GB thing, get everything needed piece by piece into the repo that would help build this show — everything helpful, even slightly helpful, or possibly helpful in the future. A browser sign-in job is running (09:07 EST, Google/GitHub sign-in, owner approves; report archive contents first, do NOT download the whole 200 GB). This inventory does not depend on that job — it records what is already in the repos.

## 2. The 38 repos — what is actually in each

Root listings read live 2026-11-23. "In tree" = files in the repo itself. "Release" = only in a GitHub Release, not in the tree. "On disk here" = on this VM — for the CN material, that is **0 .fla files and 0 production files** unless stated otherwise; the repos were read over the GitHub API, not downloaded.

| Repo | In the tree | Release / notes | Usable for Cape Jones |
|---|---|---|---|
| cn-gigaleak-gumball (private) | Gumball Bible (11.4 MB), 2012 Guide (5.5 MB), Character Comp Guide (2.2 MB), Colour Palettes, HANDOFF, docs/NO-DATA-LOSS-RULES.md | **gumball-leak-v1 — full 43.52 GB; gumball-gap-fill-v1; untagged-1676e192ae8c72e95791 — S2 Rigs pull v1** (Gumball_S2_Rigs.zip 686 MB, CN-Leaks-001-gumball.zip 1.7 GB, 71 .fla). HANDOFF: ~46 GB in draft releases. | **#1 priority.** Swap system, pivots, rig method. See §4. |
| cn-gigaleak-documents-archive (private) | ~0 KB — HANDOFF + README + WORKING-METHOD only | **documents-zip-slices-v1** — Documents.zip raw slices (2 GB assets) from the TorBox cached torrent. **Reassembly UNVERIFIED** — no verified reassembly recorded anywhere. | Source of the Documents.zip trees (j2s, Juniper Lee, I Am Weasel). Reassembly is the open job. |
| cn-gigaleak-ok-ko (private) | README, PULL-TRACKER.md, ok-ko-manifest.txt, pull-tracker.json, build_release_archives.py | **ok-ko-complete-v1** (16 parts, OK KO.zip 7.91 GB, MD5 6c276bef…, 428 files, 100% of torrent dir) + **okko-v1** (10 tars: okko-out 6.0 GiB / 211 files — character art, brand guides, fonts, backgrounds, episodes; extracted/ 2.2 GiB / 1,355 files — HB Classics, Teen Titans, Johnny Bravo). Second copy staged for TeraBox at /CN-Gigaleak/OK-KO/. | **Most complete landed repo.** Backgrounds, brand guides, fonts, character art — study how a complete pull is packed and verified. |
| cn-gigaleak-chowder (private) | HANDOFF, README, RESEARCH.md, KIT-INDEX.md — **research docs only, NO Chowder files** | **No releases. No archive pulled yet.** HANDOFF states this plainly. | Pattern-fill / texture / colour systems. See §5. |
| cn-gigaleak-dexters-lab (private) | DEXTER MAIN MODELS (model pack PDF 1.2 MB), DEXTER BACKGROUNDS (11 EPS files), DEXTER CHARACTER SHEETS (Dee Dee + Dexter EPS), DEXTER CHARACTER ART (4C/BW/PMS), DEXTER CAP 09, LOG LINES, LOGOS, MAIN TITLE THEMES, SGs, 3D, ON SERVER | Tree material, no release noted | Model-pack + background EPS system — how a lab set is built and reused. |
| cn-gigaleak-ed-edd-n-eddy (private) | EEE MAIN MODEL PACK.pdf (8.7 MB), character-sheets (Ed/Edd/Eddy EPS + JPG), bible (10.8 MB), 3d-turns, cap-update, docs, eds-are-coming, gap-fill, loglines, logos, pr, style-guide-old | Tree material | Model-pack + bible + 3D turns — character construction and turnarounds. |
| cn-gigaleak-duck-dodgers (private) | Main Model Pack PDF (9.5 MB), Backgrounds (PSD + VECTOR), Character Art (CN + WBCP), Color Call Outs, Docs, Log Lines, Logos, PR, Style Guide, Theme MP3 | Tree material | BG PSD/vector system + colour call-outs — backgrounds as layered production files. |
| cn-gigaleak-grim-adventures (private) | GBM BACKGROUNDS, CHARACTER ART PACK FULL, CHARACTER SHEETS, CONSTRUCTION NOTES, DESIGN GUIDE, MAIN MODEL PACK 2006, RANDOM MODELS, SIZE CHART, SPIDER QUEEN, THEME SONG, TURNS, LOGLINES, LOGOS, PR | Tree material (folder names only — contents not enumerated in this pass) | Construction notes + size chart + turns — rig construction method. |
| cn-gigaleak-scooby-doo-mystery-inc (private) | SDMI Main Model Pack (Color + low res), Production Art (614-626 line art/size comps, monsters, cover art), Storyboards (345-601 … 345-613), Scripts, Vector Art, Villains, Presentation, Docs, Logos | Tree material | **Storyboard + model-pack pipeline** — full episode pipeline in one repo. |
| cn-gigaleak-camp-lazlo (private) | Camp Lazlo Bible Long PDF (43.3 MB) + EPUB (17.3 MB), production-docs (CL_Bible_Early.pdf) | Tree material | Bible as production source — how a show bible drives everything. |
| cn-gigaleak-cow-and-chicken (private) | CowChicken_RedGuy.pdf (17.8 MB), docs | Tree material | Single-character model study. |
| cn-gigaleak-robot-chicken (private) | RBC STYLEGUIDE.pdf (27.3 MB), CHARACTER ART, DESIGN ELEMENTS, LOGO, PRODUCT SAMPLES, PROPS | Tree material | Style guide as system — props and design elements as a kit. |
| cn-gigaleak-looney-tunes (private) | props/ — 6 prop sets, each JPG + PSD (anvils, Bugs mailbox, carrot, dynamite ×2, mallet; PSDs 4.9–24 MB) | Tree material | Prop PSDs — how a prop is built as layered art. |
| cn-gigaleak-pink-panther (private) | character-art/ — 38 EPS files (PPE_CA_01–30 + Head 01–08), color-palette, fonts, icons, logo, mgm-logo | Tree material | Character art as vector EPS — clean vector construction. |
| cn-gigaleak-johnny-bravo (private) | model-sheets (s2 main model pack, 29 pp, 3.0 MB), show-bible | Tree material | Model sheets — the Sheet Jones reference. |
| cn-gigaleak-my-gym-partner (private) | bibles, model-sheets (Gym Partner), misc | Tree material (folder names only) | Bibles + model sheets. |
| cn-gigaleak-space-ghost (private) | Space Ghost C2C folder | Tree material (folder name only) | **Cape Jones's own origin** — Space Ghost is what Cape Jones was renamed from. Study the C2C material. |
| cn-gigaleak-regular-show (private) | production-docs (RS_SIZE4C01_CASC_CAP.pdf 2.9 MB) | Tree material; tracker: 2,280 files / 25.20 GB pending, 0 landed | Size/cap sheets. |
| cn-gigaleak-johnny-test (private) | docs only at root | Tracker not listed separately | Docs only — material still in torrent. |
| cn-gigaleak-kids-next-door (private) | docs only at root | Tracker: 1,171 files / 3.28 GB pending | Docs only. |
| cn-gigaleak-teen-titans (private) | docs only at root | Tracker: 7,167 files / 4.52 GB pending | Docs only. |
| cn-gigaleak-fosters-home (private) | docs only at root | Tracker (fosters): 999 files / 3.70 GB pending | Docs only. |
| cn-gigaleak-powerpuff-girls (private) | ppgz folder + docs | Tracker: 4,904 files / 4.54 GB pending | ppgz folder — contents not enumerated. |
| cn-gigaleak-powerpuff-girls-special (private) | Docs only (AGENTS/HANDOFF/WORKING-METHOD) | — | Empty/pointer repo. |
| cn-gigaleak-adventure-time (private) | Docs only (AGENTS/HANDOFF/README/WORKING-METHOD) | Tracker: 5,546 files / 28.82 GB pending, 0 landed | **Empty in tree — all material still in torrent.** |
| cn-gigaleak-bakugan (private) | Docs only | Tracker: 2,228 files / 32.61 GB pending | Empty in tree. |
| cn-gigaleak-billy-mandy (private) | Docs only | Tracker: 1,418 files / 5.15 GB pending | Empty in tree. |
| cn-gigaleak-fosters (private) | Docs only | Tracker: 999 files / 3.70 GB pending | Empty in tree (dup of fosters-home). |
| cn-gigaleak-cow-chicken (private) | Docs only | Tracker: 974 files / 0.15 GB pending | Empty in tree (dup of cow-and-chicken). |
| cn-gigaleak-gym-partner (private) | Docs only | Tracker: 379 files / 5.33 GB pending | Empty in tree (dup of my-gym-partner). |
| cn-gigaleak-scooby-doo (private) | Docs only | Tracker: 498 files / 8.66 GB pending | Empty in tree (material is in scooby-doo-mystery-inc). |
| cn-gigaleak-wabbit (private) | Docs only | Tracker: 73 files / 2.36 GB pending | Empty in tree. |
| cn-gigaleak-mgm-shorts (private) | Docs only | — | Empty in tree. |
| cn-gigaleak-cartoon-vault (private) | misc-pdfs (khsqgj.pdf 7.8 MB), smiling-friends folder | Tracker: 696 files / 0.77 GB pending | Misc PDFs — contents not enumerated. |
| cn-gigaleak-bonus-non-cn (public) | HANDOFF + README + WORKING-METHOD | Nickelodeon, Disney, Club Penguin, Care Bears, Rick & Morty (owner-approved) | Non-CN study material — same study-only rule. |
| cn-gigaleak-jimmy-two-shoes (private) | README only | Release jimmy-two-shoes-complete-v1 — 13 files / 278,480,586 B from Documents.zip (prefix Documents/j2s-20261010T163554Z-1-001/j2s/), single tar + manifests | Small complete pull — the pattern for the Documents.zip extractions. |
| cn-gigaleak-juniper-lee (private) | README only | 38 files from the Documents.zip tree — release not verified in this pass | Same pattern as j2s, unverified. |
| cn-gigaleak-i-am-weasel (private) | HANDOFF + WORKING-METHOD only (pointer repo) | Release i-am-weasel-torbox-v1 — TorBox Documents.zip extraction; contents not re-verified in this pass | Timing/cutting study — fast setup, fast payoff, straight-man / chaos-agent duo. |

**Count check:** 15 repos hold real production material in the tree; 2 more (Gumball, OK KO) hold their material in releases; 3 more (Chowder, documents-archive, i-am-weasel) are research/pointer repos; the rest are docs-only at root with their material still in the torrent. Folder contents were not enumerated below root level except where listed — "folder present" means the folder name was read, not its files.

## 3. What is usable for Cape Jones — wholesale systems, adapted

Per the corrected rule (§0): take their systems and mechanics wholesale, adapt them so they work for OUR show. Not Gumball the show — Cape Jones the show, built the way they build theirs.

| Their system | Where it lives | Cape Jones adaptation |
|---|---|---|
| Frame-addressed part swap (MOUTHCOMP / EYESCOMP, `loop="single frame"` + `firstFrame`) — click a part, scroll, swap in place, never stack | Gumball .fla rigs (S2 Rigs release; dissected in TRIPPEDD-Production-studios- docs/wizard-gang/FLA-PRODUCTION-STANDARD.md from GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla) | **The V3 swap system** — one slot per part, exactly one variant visible, swap replaces in place. Hands, mouths, eyes, forearm plates. |
| Anatomical pivots (`transformationPoint` at neck/shoulder/elbow/wrist/hip/knee, identical across keyframes) | Same Gumball .fla dissection | **Parenting and pivoting fix** — arm pivots AT the shoulder, attached to the body; every joint pivots at its real point. Prime suspect in our rig: `parent_keep()` builds `matrix_parent_inverse` from the bone TAIL. |
| One master symbol per view; head = nested HEADCOMP; hands per-side matched to the arm set | Same | Rig Jones 2 / Clean-Up Jones 1 structure — one master rig per view, nested head, per-side hand sets. |
| Model-pack + bible as production source | Dexter, Ed Edd n Eddy, Duck Dodgers, Johnny Bravo, Camp Lazlo, Gumball Bible/Guides | **Sheet Jones done right** — the model pack IS the bible for the rig; Rig Jones must match Sheet Jones, converging to one guy by V10. |
| Backgrounds as layered production files (PSD / VECTOR / EPS) | Duck Dodgers Backgrounds, Dexter Backgrounds (EPS), Looney props (PSD) | Parking-lot plates as layered files, not flat crops — so the cape, the plates, and the props stop splitting into square crops. |
| Storyboard → model-pack → production-art pipeline | Scooby-Doo Mystery Inc (storyboards 345-601…613, scripts, vector art, production art) | CJ-01..CJ-30 episode stage — boards and in-betweens wired as a pipeline, not a pile of files. |
| Style guide as a kit (design elements, props, logos) | Robot Chicken style guide (27 MB), Pink Panther vector art, OK KO brand guides | Cape Jones identity kit — palette, logo, props as a reusable kit, not one-offs. |
| Colour families per location | Chowder (district colour families) + Gumball colour palettes | Sodium orange → broken-streetlight purple lighting shift, keyed per location/beat. |
| Static pattern-fill (fill locked to screen, shape moves through it) | Chowder RESEARCH.md / KIT-INDEX.md | See §5 — suit/cape texture system. |

## 4. Gumball deep dive — the #1 priority

- **In the tree:** Bible, 2012 Guide, Character Comp Guide, Colour Palettes, HANDOFF, docs/NO-DATA-LOSS-RULES.md. No .fla in the tree.
- **In releases:** `gumball-leak-v1` (full 43.52 GB), `gumball-gap-fill-v1`, `untagged-1676e192ae8c72e95791` (S2 Rigs pull v1: Gumball_S2_Rigs.zip 686 MB; CN-Leaks-001-gumball.zip 1.7 GB, 876 files, 71 .fla).
- **.fla count — three different numbers, all from the repos, not reconciled:** the Gumball HANDOFF says the Cape Jones rig program studies "the S2 .fla rigs (9 files)"; the S2 release zip holds 71 .fla; the earlier audit counted 138 .fla listed remotely (43.5 GB, headers only). The tracker says Gumball is 855 files / 24.59 GB, pending, 0 landed. **Do not quote one number as the total until the release is opened and counted.**
- **On disk here: 0 .fla.** A browser download job started 2026-11-23 08:59 EST to download both S2 zips signed in as mhvnsnt. A prior lane dissected GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla (1,740,533 B) and scene GB202REMOTE_Sc094_Clean_V023_STN.fla (22,851,853 B) from XFL XML — that dissection is the source of the swap/pivot findings in §3.
- **What Gumball gives Cape Jones, in order:** (1) the swap system, (2) the anatomical pivots, (3) the one-master-symbol-per-view rig structure, (4) the colour palettes and comp guide as a production standard.

## 5. CHOWDER — priority section (owner, 2026-11-23 09:04 EST)

**What we actually have:** the Chowder repo holds **research docs only** — `RESEARCH.md`, `KIT-INDEX.md`, `README.md`, `HANDOFF.md`. **No Chowder archive has been pulled here yet — no releases, no production files.** The HANDOFF states this plainly, and the bar for done there is (1) a Chowder archive pulled and verified in a Release, and (2) a kit study the show can build from. Neither is owed yet — the pull has not been ordered. The TorBox torrent is the source for that pull when the owner orders it.

**What is in the research (from published sources — Greenblatt's own production writing and interviews, not from Chowder production files):**

- **Static pattern-fill (the signature technique):** characters and props are filled with rich patterns/textures that stay FIXED to the screen while the shape moves through them. The pattern does not travel with the character. It reads as fabric/collage and makes simple movement feel handmade and tactile. Production-wise it is a **compositing rule, not a drawing rule**: the fill layer is locked; the character is a moving matte over it.
- **Food-logic worldbuilding:** Marzipan City is a food-built world — architecture, vehicles, landscape all derive from food forms and kitchen logic. The world system IS the menu. Environments carry the show's jokes before any character speaks.
- **Backgrounds:** flat colour shapes mixed with photographic/collage texture and visible pattern; depth comes from texture contrast more than realistic perspective. Layouts favour clear stage-like compositions with strong foreground framing (market stalls, counters, hanging food) — the frame is dressed like a shop window.
- **Colour:** high-saturation, clashing-on-purpose palette, organised by location; each district/shop keeps its own colour family so cuts read instantly. Patterns are colour-keyed per character per episode.
- **Format craft:** apprentice/master workday engine (a task → chaos → small earned lesson); food gags are mechanisms (recipes that fight back), not decoration. Fourth-wall and puppet/credits gags exist — noted as format awareness only, not a transfer item.

**The 4 kit items (from KIT-INDEX.md, written for Mochiichao — the same construction-kit rule applies for Cape Jones):**

| # | Kit item | Cape Jones form |
|---|---|---|
| 1 | Static pattern-fill | Garden-texture fills → **parking-lot texture fills**: pattern sheets painted natively from lot motifs (asphalt, sodium light, purple night) |
| 2 | Food-logic worldbuilding | **Lot-logic environments:** every structure derives from lot forms — the parking lot is the world system, the way the kitchen is Chowder's |
| 3 | District colour families | **One colour family per location** — sodium orange lot, broken-streetlight purple, extending the Persona-5 one-dominant-colour rule already in use |
| 4 | Shop-window foreground framing | **Foreground dressing layer standard** for lot scenes (parked cars, fence lines, hanging signs) — the frame is dressed, not empty |

**Owner addendum (09:04 EST) — lighting, clothing, material/texture effects as SYSTEMS and MECHANICS and UNIVERSE LANGUAGES, not just a look:**

| Effect area | What Chowder did | First system to build for Cape Jones |
|---|---|---|
| **Lighting effects** | Colour-keyed patterns per character per episode; depth from texture contrast, not perspective; location colour families so cuts read instantly | **Location colour-family lighting system** — one dominant colour + keyed pattern per location/beat; the sodium → purple shift as a system, not a one-off grade |
| **Clothing effects** | Static pattern-fill on characters — the fill stays fixed to screen while the shape moves, reading as fabric/collage | **Pattern-fill suit/cape system** — Cape Jones's white suit and black cape filled with a screen-locked pattern/texture; the suit reads as fabric, the cape as one deforming piece, not two cropped planes |
| **Material and texture effects** | Flat colour + photographic/collage texture + visible pattern in backgrounds; texture contrast = depth | **Texture-contrast background system** — parking-lot plates built from flat colour + collage texture, depth from texture contrast; replaces flat cropped plates |
| **Universe language** | Food-logic worldbuilding — the world system IS the menu; environments carry jokes before dialogue | **Lot-logic universe language** — the parking lot as a world system: every prop, sign, and structure derives from lot forms; the lot carries the show before Jones speaks |

**Honest limit:** all of the above is from published research, not from Chowder production files — because no Chowder files are in the repo yet. The first real Chowder build step is the archive pull (TorBox → release → verify), when the owner orders it. Do not claim a Chowder file was studied until it is in hand.

## 6. The TorBox gap — what is NOT in any repo

- **The torrent as a whole:** 42,549 files / 172.84 GB across 22 repos (PULL-TRACKER.md). Only OK KO is complete in a repo. Everything else is pending, 0 landed, per the tracker.
- **By show (tracker table):** Adventure Time 5,546 files / 28.82 GB; Regular Show 2,280 / 25.20 GB; Gumball 855 / 24.59 GB (plus the separate 43.52 GB leak release); Bakugan 2,228 / 32.61 GB; Camp Lazlo 5,190 / 6.02 GB; Powerpuff Girls 4,904 / 4.54 GB; Teen Titans 7,167 / 4.52 GB; Looney Tunes 3,821 / 3.44 GB; Billy & Mandy 1,418 / 5.15 GB; Scooby-Doo 498 / 8.66 GB; Fosters 999 / 3.70 GB; Kids Next Door 1,171 / 3.28 GB; Ed Edd n Eddy 978 / 2.03 GB; Wabbit 73 / 2.36 GB; Gym Partner 379 / 5.33 GB; Duck Dodgers 338 / 0.69 GB; Dexter 1,943 / 0.37 GB; Cow & Chicken 974 / 0.15 GB; Space Ghost 252 / 0.07 GB; Johnny Bravo 548 / 0.06 GB; Cartoon Vault 696 / 0.77 GB.
- **Documents.zip:** the 2 GB slices in `cn-gigaleak-documents-archive` (release `documents-zip-slices-v1`) are **unverified** — no hash-verified reassembly is recorded. Jimmy Two Shoes (13 files / 278 MB) and Juniper Lee (38 files) are the two completed Documents.zip extractions; I Am Weasel's release contents were not re-verified in this pass.
- **What the TorBox job (running 09:07 EST) must report first:** the archive's contents — what is actually in the ~200 GB — before any piece-by-piece pull. Do not download the whole 200 GB.

## 7. Crossover practice piece — SCOPED, not built (owner authorized 2026-11-23 09:05 EST)

**The clip:** 10 seconds (240f) or 30 seconds (720f) at 24fps, silent. Cape Jones walking through **all of Gumball's settings** — Elmore Junior High (the school), the Watterson house, and Elmore town — made exactly how they make their show, so he feels like he is IN their world, in the Gumball world.

**What we actually have for it, verified:**
- Gumball rig method (swap system, pivots) — dissected from the .fla, §4.
- Gumball Bible, 2012 Guide, Character Comp Guide, Colour Palettes — in the tree.
- **No verified background files for the school, the house, or the town in the repo tree.** Those backgrounds would come from `gumball-leak-v1` (43.52 GB) or the TorBox torrent — they have not been downloaded, catalogued, or verified in this pass. Do not claim a specific school/town/house file exists until it is opened.

**What the clip needs (build lane, separate — V3 cut first):**
1. Download + catalogue the Gumball backgrounds: school exterior/interior, Watterson house exterior/interior, town streets — exact file names, sizes, hashes.
2. Jones walk cycle built Gumball-style: one hand per arm, slot-swapped hands, anatomical pivots, one-piece deforming cape, walk on twos, hard cuts between settings.
3. Lighting/colour per setting from the Gumball palettes — each location its own colour family, the way Gumball does it.
4. Cuts, not dissolves: school → house → town, each setting a clean hard cut, Jones walking through the frame in each.
5. Prove small first: one setting, one walk, own-eyes — then the full 10s/30s clip.

**What it proves:** that Cape Jones can be built and shot exactly the way a real network show is built and shot — and that our files are made like theirs.

## 8. Order of work

1. **V3 cut first** — Clean-Up Jones V1 (Rig Jones 2), Gumball-level 100%: swap system, parenting/pivoting, one-piece cape. That lane is running.
2. **Gumball .fla download + first-hand dissection** — browser job running 08:59 EST.
3. **TorBox contents report** — browser job running 09:07 EST; piece-by-piece pulls after that, everything helpful, even slightly helpful, or possibly helpful in the future.
4. **Chowder archive pull** — when the owner orders it; then the 4 Chowder systems in §5 as working systems.
5. **Crossover clip (10s/30s)** — after V3, per §7.
6. **Documents.zip verified reassembly** — open job in cn-gigaleak-documents-archive; until it verifies, the vault is parts, not a store.

## 9. What was NOT verified in this pass

- Subdirectory contents below root level, except where listed in §2 — most folders were named, not enumerated.
- Release contents for most repos — only Gumball, OK KO, documents-archive, I Am Weasel, and Jimmy Two Shoes have release details stated in their own docs; the rest were not opened.
- The exact .fla count for Gumball (9 vs 71 vs 138 — §4).
- Any file inside the TorBox torrent — that is the 09:07 EST browser job's report, not this inventory.
- No file on this VM was downloaded, extracted, or opened from any CN archive in this lane.

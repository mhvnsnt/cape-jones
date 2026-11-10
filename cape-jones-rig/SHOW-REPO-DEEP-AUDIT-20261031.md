# Show-Repo Deep Audit — pullable material for Cape Jones
Date: 2026-10-31. Auditor: subagent deep-audit task. This is an AUDIT ONLY.
Nothing in this file claims material is wired into Cape Jones. Wiring is a
separate step, and it must follow the scope below.

## Scope (confirmed by Mars, 2026-10-31; UPDATED 2026-10-31 15:24 CDT)
Audit ANY type of move and ANYTHING helpful, not just dances: walks,
runs, jumps, fights, flexes, dances, gestures, expressions, holds,
camera moves, timing, squash-and-stretch, pose libraries, gait swaps,
production methods, bible/pipeline architecture, colour/texture
systems. A move is a move — the audit does not limit itself to dance.
BARRED LIST — ONLY these five (Mars, 2026-10-31 15:24 CDT, supersedes
any narrower framing used earlier in this audit):
1. Exact character likeness image shipped as-is.
2. Using their character literally.
3. Character name.
4. Dialogue literally from their script.
5. Brand image / logo.
Everything else is pullable.
EXCEPTION (Mars, 2026-10-31 15:24 CDT): a character image may be used
as a PRODUCTION REFERENCE ONLY if it is edited/modified during
production into a parody character or a whole different character
before release. It must NOT ship as their character. All
reference-image material in this audit is therefore flagged
TRANSFORM-ONLY, never ship-as-is. Where the table below previously
said "art NOT pullable", read it as: not shippable as-is; usable as
transform-only production reference, and only the systems/movement
in it (pose, timing, structure) carry into Cape Jones, never the
likeness, name, dialogue, or logo.
An audit inventory may name shows/repos/files as source identifiers.
That is documentation, not game content. No dialogue, character art,
or logos are reproduced in this file.
Note on earlier scope items: Pokemon/Sonic cries and town names
straight from their games were in the standing scope for the game
lanes; they are not part of this show audit's five-item barred list,
and no such material is recorded as pullable here.

## How this audit was done
- Listed every repo reachable via the GitHub API helper
  (`~/workspace/cape-jones-rig-repo-batch/gh_api.py`, `req("GET", …)`):
  161 unique repos total (48 public + 113 private/authenticated).
- For each show archive: read the repo root listing and the release
  list (asset names + counts). Small docs were read in full
  (READMEs, catalogs, inventories). Large split archives were NOT
  downloaded — their contents are therefore "unknown", not "empty".
- Code search was used sparingly and deduplicated (gumball, Watterson,
  cartoon-network, nickelodeon, disney, dance, flex). Most dance/flex
  hits are tool/vendor noise and were filtered out.
- A show is only marked "dance: YES" if a file proves it. A show is
  only marked "rig: YES" if a rig file (`.fla` XFL, or a named rig
  asset) was seen. Everything else is NO or UNKNOWN, with the reason.

## Counts (audited entries = 41 rows in the table below)
- Audited show/collection entries: 41
- Content-verified rig/dance material: 3/41 = 7%
  (Gumball, Smiling Friends, Foster's Home)
- Rig files present, content unexamined (format-level only): 1/41 = 2%
  (Cartoon Vault unsorted `.fla` set)
- Total with extractable rig files (verified + format-level): 4/41 = 10%
- Verified dance (a performed dance, not a pose library): 1/41 = 2%
  (Gumball — Darwin, "The Words")
- Verified MOVEMENT material, any move type (scope update 15:24 CDT —
  not dance-only): 3/41 = 7% content-verified (Gumball dance + scenes,
  Smiling Friends gait/pose swaps, Foster's character reels + Frankie
  rig) + 1/41 format-level (Cartoon Vault unsorted .fla set) = 4/41
  = 10% with extractable movement files. Video timing references
  (movement study, not rigs) additionally: Scooby-Doo! Mystery Inc.
  ep. 607 song animatic, Adventure Time animatic, Disney TVA pilot
  MP4s (catalogued, not pulled), public-domain films.
- Reference-image material: flagged TRANSFORM-ONLY throughout (see
  Scope). Model packs, art dirs, and stills in rows 6, 7, 14, 17, 19,
  20, 23, 24, 37 are usable as production reference for pose/timing/
  structure ONLY if edited into a parody or wholly different
  character before release; they must never ship as the source
  character, and their names/dialogue/logos are still barred.
- Archive exists, content unlisted / unknown (split parts or zip not
  listed — rig presence neither proved nor disproved): 21/41 = 51%
- Format present but not usable here (Toon Boom, no Toon Boom on VM): 1/41 = 2%
- Empty / placeholder repo (no show material in repo): 2/41 = 5%
  (Bakugan, I Am Weasel)
- Method / bible / art / video reference only, no rig: 13/41 = 32%
- Check: 3 + 1 + 21 + 2 + 1 + 13 = 41. 100%.
- Repos checked but NOT counted in the 41 (own shows, hubs, games):
  cape-jones itself, Goodville-Show, God-Molecule-Show-Studio,
  mystery-coast-ghosted, johnny-test-parody, TRIPPEDD-Production-studios-
  (hub), Bannon (game, not a show archive), Mochiichao repos (game).
  Duplicate/empty variant repos are folded into their show row, not
  counted twice: cn-gigaleak-cow-chicken (empty variant of Cow &
  Chicken), cn-gigaleak-fosters (empty variant of Foster's Home),
  cn-gigaleak-my-gym-partner (variant of My Gym Partner),
  cn-gigaleak-scooby-doo (variant of Scooby-Doo! Mystery Inc.),
  cn-gigaleak-billy-mandy (empty variant of Grim Adventures of
  Billy & Mandy), cn-gigaleak-wabbit (empty, folded into Looney Tunes).

## Table — one row per show/collection
Network column: "CN gigaleak repo label" means the repo name/description
labels it a CN gigaleak archive; it is NOT a verified broadcast-network
claim unless the row says "stated in source". "Not stated" means the
source files checked do not state a network.

| # | Show / collection | Network (source-stated only) | Repo + key path | Format | Rig / dance / movement present | Extractable here? | Pullable under scope (systems only, never art/names/dialogue/logos) |
|---|---|---|---|---|---|---|---|
| 1 | Adventure Time | CN gigaleak repo label | mhvnsnt/cn-gigaleak-adventure-time — releases at-2015-v1, at-cnzip-20261015, adventure-time-loose-v1 | Split parts (500 MB chunks) + animatic .mov/.mp4 + notes PDF | Rig: UNKNOWN. Dance: UNKNOWN. Animatic + notes seen. | NO for rig/dance — archive content unlisted; split parts reassemblable but contents unknown | Animatic timing (if the .mov is examined frame by frame); notes structure. Nothing else until the zip is listed. |
| 2 | Bakugan | CN gigaleak repo label | mhvnsnt/cn-gigaleak-bakugan — root only AGENTS.md + WORKING-METHOD.md, 0 releases | None in repo | Rig: NO. Dance: NO. | N/A — nothing held | Nothing. Placeholder repo. |
| 3 | Camp Lazlo | CN gigaleak repo label | mhvnsnt/cn-gigaleak-camp-lazlo — Camp Lazlo Bible PDF/EPUB in repo + production-docs, release camp-lazlo-bible-v1 | Bible PDF/EPUB | Rig: NO. Dance: NO. | NO for rig/dance — bible only | Bible architecture: world/episode structure, production-doc format. |
| 4 | Chowder | CN gigaleak repo label (donor repo for Mochiichao) | mhvnsnt/cn-gigaleak-chowder — RESEARCH.md + KIT-INDEX.md, 0 releases | Research/kit docs only, no source files | Rig: NO. Dance: NO. | NO — no source files held | Already extracted as a kit: static pattern-fill (fill locked to screen, shape moves through it), food-logic worldbuilding, district colour families, shop-window foreground framing. Rebuilt natively, no show art. |
| 5 | Cow & Chicken | CN gigaleak repo label | mhvnsnt/cn-gigaleak-cow-and-chicken — docs + CowChicken_RedGuy.pdf, release cow-and-chicken-v1 (Cow.Chicken.zip, 1 asset) | Zip (single asset) + PDF | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — zip not listed | Nothing verified yet. Zip listing is a next pull. |
| 6 | Dexter's Laboratory | CN gigaleak repo label | mhvnsnt/cn-gigaleak-dexters-lab — in-repo dirs: character art/sheets, backgrounds, main models, title themes, SGs; release dexters-lab-complete-v1 (Dexter.s.Lab.zip) | Art/model dirs + zip | Rig: NO evidence. Dance: NO. | NO for rig — art/model packs only, as listed | Model-sheet structure, background systems, title-theme structure. Art itself is NOT pullable. |
| 7 | Duck Dodgers | CN gigaleak repo label | mhvnsnt/cn-gigaleak-duck-dodgers — in-repo dirs: backgrounds, character art, colour call-outs, main model pack, style guide; releases duck-dodgers-*.zip (draft) | Art/model/style dirs + zip | Rig: NO evidence. Dance: NO. | NO for rig — art/style only, as listed | Colour call-out system, style-guide structure, background systems. Art/logos NOT pullable. |
| 8 | Ed, Edd n Eddy | CN gigaleak repo label | mhvnsnt/cn-gigaleak-ed-edd-n-eddy — in-repo dirs: 3d-turns, bible, character-art/sheets, main-model-pack, style-guide; releases eenee-cnleaks-v1 (9 parts), een-gap-fill, ed-edd-n-eddy-complete-v1 (20 chunks) | Art/bible dirs + split parts | Rig: UNKNOWN (parts unlisted). Dance: NO evidence. | UNKNOWN for rig — parts not listed | Bible + model-pack + style-guide structure (in-repo dirs). Rig only if a part listing proves it. |
| 9 | Foster's Home for Imaginary Friends | Cartoon Network Studios — stated in TRIPPEDD animation-study catalog (Burbank + Boulder Media, Illustrator/Flash/After Effects pipeline) | mhvnsnt/cn-gigaleak-fosters-home — release frankie-rig-fla-v1 (pds3hx.fla, 1 asset), fosters-flash-v1 (default.tmp-fosters-flash.zip), fosters-complete-v1 (8 parts), fosters-cnleaks-007/006/002; TRIPPEDD animation-study/fosters-home/CATALOG.md | XFL .fla (Frankie rig) + Flash zip + split parts; CN dot-com Flash reels (Berry, Bloo, Cheese, Coco, Ivan, Uncle Pockets, Wilt) per dance-choreo INVENTORY | Rig: YES (Frankie .fla, single asset). Dance: NOT VERIFIED — long character reels, no dance identified yet. | YES for the Frankie rig file (single-asset download, XFL parseable by the same method as Gumball). Reels: heavier route (SWF PlaceObject parsing, 1,618–2,190 f @24 fps, pre-CS5 binary FLA). | Master-symbol layer stack + pose-swap structure from the Frankie rig; Adobe vector pipeline method (Illustrator → Flash → After Effects); character-first development method. No character art. |
| 10 | The Grim Adventures of Billy & Mandy | Cartoon Network Studios — stated in TRIPPEDD animation-study catalog | mhvnsnt/cn-gigaleak-grim-adventures — in-repo dir "Grim Adventures of Billy & Mandy", release grim-complete-v1 (GRIM.zip, 8 parts); TRIPPEDD animation-study/grim-adventures/CATALOG.md | Split zip + catalog (public production material) | Rig: NO evidence. Dance: NO. | UNKNOWN for rig — parts not listed | Tone/production method from the catalog: creator-documented production, 7-min vs 11-min episode-structure lesson, student-film-to-series path. No rig/dance verified. |
| 11 | The Amazing World of Gumball | CN gigaleak repo label | mhvnsnt/cn-gigaleak-gumball — releases: untagged-1676e192ae8c72e95791 (CN-Leaks-001-gumball.zip 1.71 GB, 876 entries, 71 .fla; Gumball_S2_Rigs.zip 686 MB, 132 entries, 62 .fla), gumball-leak-v1 (86 RAR5 parts, unlisted), gumball-flash-v1 (4 parts); cape-jones/production/dance-choreo/ (README, INVENTORY, dance-gumball-darwin-words-sc057-sc059.json) | XFL .fla (25 fps) + SWF exports + guides/bibles in repo root | Rig: YES (11 puppets + 61 scene FLAs). Dance: YES — Darwin, "The Words" GB214, Sc057 wide (198 f) + Sc059 close-up twist (105 f). | YES — already extracted to JSON. Method proven: sequential local-header parse of malformed 2012 XFL zips, DOMDocument + LIBRARY XML parse, FFDec SWF rendering for proof. | Beat grid ~14 f @25 fps (~107 BPM), keyframing on twos, twist layer (32 keyframes, f43–97), beat layers in onlooker puppets, stride → groove → kick → split stance → twist progression, puppet slot structure (head comp, L/R fin, L/R leg, body layers), negative-a flip-in-scene. This is the ONLY verified dance in the whole audit. |
| 12 | My Gym Partner's a Monkey | CN gigaleak repo label | mhvnsnt/cn-gigaleak-my-gym-partner + cn-gigaleak-gym-partner — bibles, model-sheets, misc dirs; releases gym-partner-batches-v1, gym-partner-gaps-torbox-v1, gp-cowchicken-v1 (29 parts) | Bibles/model sheets + split parts/tarballs | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN for rig — batches not listed in detail | Bible + model-sheet structure (in-repo dirs). Nothing else verified. |
| 13 | I Am Weasel | CN gigaleak repo label | mhvnsnt/cn-gigaleak-i-am-weasel — root only WORKING-METHOD.md; release i-am-weasel-torbox-v1 (0 assets) | None in repo | Rig: NO. Dance: NO. | N/A — nothing held | Nothing. Empty release. |
| 14 | Johnny Bravo | CN gigaleak repo label | mhvnsnt/cn-gigaleak-johnny-bravo — in-repo dirs: model-sheets, show-bible; release johnny-bravo-cowchicken-v1 (10 assets incl. johnny-bravo.zip + .eps files) | Model sheets/bible + zip + EPS | Rig: NO evidence. Dance: NO. | UNKNOWN for rig — zip not listed | Model-sheet + show-bible structure. Nothing else verified. |
| 15 | Johnny Test | CN gigaleak repo label (parody repo is Mars's own, see appendix) | mhvnsnt/cn-gigaleak-johnny-test — docs dir; releases johnny-test-cowchicken-v1 (14 parts), johnny-test-extracted-v1 (0 assets) | Split parts | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — parts not listed; extracted release is empty | Nothing verified yet. Part listing is a next pull. |
| 16 | Codename: Kids Next Door | CN gigaleak repo label | mhvnsnt/cn-gigaleak-kids-next-door — docs dir; releases knd-cnleaks-v1 (6 parts), knd-complete-v1 (5 parts) | Split parts | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — parts not listed | Nothing verified yet. Part listing is a next pull. |
| 17 | Looney Tunes (incl. Wabbit placeholder, New Looney Tunes, LT Classic) | CN gigaleak repo label | mhvnsnt/cn-gigaleak-looney-tunes — in-repo dirs: props, stills; releases ltc/lts-cnleaks parts, new-looney-tunes-complete-v1, lt-classic-complete-v1, looney-tunes-complete-v1 (single zips) | Props/stills + split parts + single zips | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN for rig — parts/zips not listed | Prop/still structure (in-repo dirs). Classic squash-and-stretch timing is a candidate ONLY if a part listing proves rig/film material — not claimed here. |
| 18 | MGM Shorts | CN gigaleak repo label | mhvnsnt/cn-gigaleak-mgm-shorts — docs dir; release mgm-shorts-complete-v1 (12 parts) | Split parts | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — parts not listed | Nothing verified yet. |
| 19 | OK K.O.! Let's Be Heroes | CN gigaleak repo label | mhvnsnt/cn-gigaleak-ok-ko — PULL-TRACKER.md, ok-ko-manifest.txt, pull-tracker.json in repo; releases okko-cnleaks-v1 (76 parts), okko-extract-20261016 (123 assets: .psd/.jpg production art), ok-ko-complete-v1 (2 parts) | PSD/JPG production art + split parts | Rig: NO evidence (art only in the extract). Dance: NO. | NO for rig — extract is art | Production-art pipeline (PSD layering, shot numbering in asset names like B005S004_650_v02). Art itself NOT pullable. |
| 20 | The Pink Panther | CN gigaleak repo label | mhvnsnt/cn-gigaleak-pink-panther — in-repo dirs: character-art, color-palette, fonts, icons; release pink-panther-complete-v1 (The.Pink.Panther.zip, 1 asset) | Art/palette dirs + zip | Rig: NO evidence. Dance: NO. | NO for rig — art/palette only, as listed | Colour-palette system structure. Art/icons/logos NOT pullable. |
| 21 | The Powerpuff Girls | CN gigaleak repo label | mhvnsnt/cn-gigaleak-powerpuff-girls + -special — docs, ppgz dirs; releases ppg-original-cowchicken-v1 (3 parts), ppg-10th-anniversary.zip, PPG_flas.rar (backup release), ppgs100m parts (special, 19 parts) | Split parts + RAR | Rig: UNKNOWN (PPG_flas.rar name suggests FLAs, contents not listed). Dance: NO evidence. | UNKNOWN — RAR/parts not listed | Nothing verified yet. Listing PPG_flas.rar is a next pull (it is the only PPG asset whose name promises rig files). |
| 22 | Regular Show | CN gigaleak repo label | mhvnsnt/cn-gigaleak-regular-show — production-docs dir (1 PDF seen: RS_SIZE4C01_CASC_CAP.pdf); release regular-show-cnleaks-v1 (71 assets, ~180 × 100 MB parts per dance-choreo INVENTORY, 18.9 GB) | Split zip parts + 1 production PDF | Rig: UNKNOWN. Dance: UNKNOWN. | UNKNOWN — parts not listed | Production-doc format (the 1 PDF). Nothing else until the parts are listed. |
| 23 | Robot Chicken | CN gigaleak repo label | mhvnsnt/cn-gigaleak-robot-chicken — in-repo dirs: CHARACTER ART, DESIGN ELEMENTS, PROPS, RBC STYLEGUIDE.pdf; release robot-chicken-complete-v1 (Robot.Chicken.zip + poster .tif) | Art/design/style dirs + zip | Rig: NO evidence (stop-motion show; rig here would mean puppets/sets, not .fla). Dance: NO. | NO for .fla rig — none listed | Style-guide structure, prop/design-element organisation. Art NOT pullable. |
| 24 | Scooby-Doo! Mystery Incorporated | CN gigaleak repo label | mhvnsnt/cn-gigaleak-scooby-doo-mystery-inc + cn-gigaleak-scooby-doo — in-repo dirs: Main Model Pack, Production Art, Storyboards, Scripts, Vector Art; releases scooby-complete-v1 (95 assets incl. 607_ActDsong-old.mov animatic), scooby-mystery-inc-cowchicken-v1 (79 parts) | Model packs/art/storyboards/scripts + animatic .mov + split parts | Rig: NO (.fla count = 0, per dance-choreo INVENTORY). Dance: NO — chase-song material exists only as ep. 607 act D song animatic (baked video). | NO for rig — baked pixels only | Storyboard + model-pack structure; animatic timing (baked video, frame-by-frame timing only). Scripts/art NOT pullable as content. |
| 25 | Space Ghost (Coast to Coast) | CN gigaleak repo label | mhvnsnt/cn-gigaleak-space-ghost — in-repo dir "Space Ghost C2C"; releases space-ghost-c2c-cowchicken-v1 (Space.Ghost.C2C.zip), space-ghost-complete-v1 (Space.Ghost.tab) | Zip + .tab | Rig: NO evidence. Dance: NO. | UNKNOWN — zip/tab not listed | Nothing verified yet. Note: Cape Jones is already the renamed successor to this line — do not re-pull its identity material. |
| 26 | Teen Titans | CN gigaleak repo label | mhvnsnt/cn-gigaleak-teen-titans — docs dir; releases teen-titans-cnleaks-v1 (10 parts), teen-titans-cowchicken-v1 (8 parts), teen-titans-complete-v1 (2 parts) | Split parts | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — parts not listed | Nothing verified yet. Part listing is a next pull. |
| 27 | Cartoon Vault (catch-all collection) | CN gigaleak repo label | mhvnsnt/cn-gigaleak-cartoon-vault — README: catch-all for smaller finds; releases tv-gigaleak-years-*, tv-gigaleak-pdfs-v1 (62 PDFs), tv-gigaleak-lts-v1, tv-gigaleak-hbrefs-v1, tv-gigaleak-garfield-v1 (39 assets), randy-cunningham-v1, animaniacs-complete-v1, tv-gigaleak-fla-v1 | Mixed: PDFs, model packs, zips, .fla set | Rig: YES at format level (see row 28 for the .fla set). Dance: UNKNOWN for the vault as a whole. | YES for the .fla set (single-asset downloads, see row 28). PDFs/model packs: reference only. | Guide/model-pack PDF structure; year-bucketed archive organisation. See row 28 for the rig set. |
| 28 | Smiling Friends (inside Cartoon Vault) | Not stated in source files checked | mhvnsnt/cn-gigaleak-cartoon-vault — release tv-gigaleak-fla-v1 assets SmileFriends.Charlie.fla (82,390 B) + SmileFriends.PimRigUpdate.fla (296,483 B); TRIPPEDD docs/wizard-gang/RIG-DISSECTION.md §1–2 | XFL .fla, Animate 22.0, stage 1920×1080 | Rig: YES, content-verified by dissection. Dance: NO — rigs only, scene timelines empty. | YES — single-asset .fla downloads, XFL parseable | Master-symbol layer stacks (Charlie 9 layers, Pim 5 layers), head sub-symbols, separate pupil/brow/lid symbols, mouth as frame-addressed drawing library (Charlie mouth 25 frames), pose-swap libraries (legs 10, arms 2–3, brows/lids 3 each), mask layers, pupil PARENT wrapper. No character art. |
| 29 | Cartoon Vault unsorted .fla set (show(s) not identified in asset names) | Not stated in source files checked | mhvnsnt/cn-gigaleak-cartoon-vault — release tv-gigaleak-fla-v1, remaining 10 assets: Unsorted.AB112-LINE-UP.alien.1.fla, .earth.1.1.fla, BOSS_101A_BG_079.fla, BOSS_113A_CH_021.fla, BOSS_113A_CH_065.fla, BOSS_113C_BG_001.fla, DIME01_ENG_POSTER_01.1.fla, ch_max.fla, ch_ruby.fla, yyo_spl_act_flipflopfoo.fla | XFL .fla (sizes 9.4 MB–57.4 MB) | Rig/scene: FILES PRESENT, content unexamined. Dance: UNKNOWN. | YES at format level — single-asset downloads, same XFL parse method applies; content (character/scene vs background vs poster) is NOT yet known | Nothing yet until one file is parsed. Priority pull: ch_max.fla / ch_ruby.fla (largest, likely character rigs) and yyo_spl_act_flipflopfoo.fla (name suggests a split/action). Do not assume a show from a filename prefix. |
| 30 | Randy Cunningham: 9th Grade Ninja | Not stated in source files checked | mhvnsnt/cn-gigaleak-cartoon-vault — release randy-cunningham-v1 (randycunning.ham.t.zip, 142.5 MB, per vault README) | Zip (.ham.t?) | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — zip not listed | Nothing verified yet. |
| 31 | Animaniacs | Not stated in source files checked | mhvnsnt/cn-gigaleak-cartoon-vault — release animaniacs-complete-v1 (animaniacs-leak-20261015.zip, 1 asset) | Zip | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — zip not listed | Nothing verified yet. |
| 32 | Rick and Morty (Toon Boom files) | Not stated in source files checked (bonus repo labels it non-CN) | mhvnsnt/cn-gigaleak-bonus-non-cn — release bonus-non-cn-v1 includes rick-and-morty-toonboom-files.zip (17.7 MB, single asset); mhvnsnt/cn-gigaleak-cartoon-vault — release tv-gigaleak-rickandmorty-v1 (rick-and-morty-toonboom-files.zip, same file) | Toon Boom .tpl/.tvg (thumbnails only on this VM, per dance-choreo INVENTORY) | Rig: FILES PRESENT, but format only. Dance: UNKNOWN. | NO here — no Toon Boom on the VM, so the files cannot be opened/parsed here | Nothing yet. If Toon Boom becomes available, re-audit: pose libraries and scene structure would be the pull, never character art. |
| 33 | Nickelodeon (2024 Nick Gigaleak + nick.7z, shows unlisted) | Non-CN — stated in bonus repo description (Nickelodeon) | mhvnsnt/cn-gigaleak-bonus-non-cn — release bonus-non-cn-v1: 2024_Nick_Gigaleak.zip (4.33 GB, parts 0000–0041) + nick.7z (7.21 GB, parts 0000–0068) | Split zip / 7z, contents unlisted | Rig: UNKNOWN. Dance: UNKNOWN. | UNKNOWN — neither archive has been listed | Nothing verified yet. This is the largest unknown in the audit (11.5 GB combined). Listing nick.7z / 2024_Nick_Gigaleak.zip central directories is the highest-value unknown pull. |
| 34 | Disney pitch bibles + Disney FLA rar (incl. Wow! Wow! Wubbzy! FLA) | Non-CN — stated in bonus repo description (Disney) | mhvnsnt/cn-gigaleak-bonus-non-cn — release bonus-non-cn-v1: A.TON.OF.DISNEY.PITCH.BIBLES.AND.CLUB.PENGUIN.PDFS.rar (2.48 GB, parts 0000–0023) + DISNEY.LEAKS.and.wow.wow.wubbsy.fla.rar (757 MB, parts 0000–0007) | RAR parts (pitch-bible PDFs + .fla) | Rig: UNKNOWN (FLA rar contents unlisted). Dance: NO evidence. | UNKNOWN — RAR parts not listed | Bible architecture (once listed). The .fla rar is the only Disney-side rig lead in the audit — listing it is a next pull. |
| 35 | Club Penguin | Non-CN — stated in bonus repo description | mhvnsnt/cn-gigaleak-bonus-non-cn — release bonus-non-cn-v1: ClubPenguin.zip (436 MB, parts 0000–0004) | Split zip | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — zip not listed | Nothing verified yet. |
| 36 | Care Bears | Non-CN — stated in bonus repo description | mhvnsnt/cn-gigaleak-bonus-non-cn — release bonus-non-cn-v1: Care.Bears.-.Random.7z (266 MB, parts 0000–0002) | Split 7z | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN for rig — archive not listed; "Random" in the name suggests mixed material, not a rig set | Nothing verified yet. |
| 37 | Garfield + Looney Tunes Show model packs | Not stated in source files checked (bonus repo, "smalls") | mhvnsnt/cn-gigaleak-bonus-non-cn — release tv-gigaleak-smalls-v1: garfield-model-sheets.zip (14.2 MB, single asset) + LTS_MainModelPack_120909.pdf (250 MB, 3 parts); mhvnsnt/cn-gigaleak-cartoon-vault — release tv-gigaleak-lts-v1 (same LTS PDF) | Model sheets + model-pack PDF | Rig: NO. Dance: NO. | NO for rig — model packs only | Model-sheet structure, size-chart method (HB character size chart .ai in hbrefs release). Art NOT pullable. |
| 38 | Disney TVA collection (44 pitch/show bibles pulled 2026-10-12 + 36 pilot MP4s catalogued, not pulled) | Disney TVA — stated in DISNEY-TVA-CATALOG.md (Internet Archive sources, 4chan /co/ leak 2023–2025, DMCA-risk note in source: catalogued for study, never redistributed) | mhvnsnt/disney-tva-bbb-pulls — release v1.0.0 (disney-tva-new-bibles-2026-10-12.zip + bbb-production-files parts); DISNEY-TVA-CATALOG.md, ANIMATION-REFERENCE.md, BBB-PRODUCTION-CATALOG.md | Pitch/show-bible PDFs + pilot MP4s (catalogued, ~11 GB, not bulk-pulled) + Big Buck Bunny (CC-BY) production files | Rig: NO. Dance: NO. | NO for rig/dance — bibles + pilots only | Pitch-bible architecture (logline/world/springboards/art), show-bible depth (series bible vs pitch bible), pilot-stage template. Big Buck Bunny files are CC-BY and are the only openly licensed production files in this row. |
| 39 | Samurai Jack | Not stated in source files checked (repo is a study archive) | mhvnsnt/samurai-jack-repo — dirs: samurai-jack/episode-files, series-structure-index.md, transcripts; craft-for-our-shows/CRAFT-EP01.md; 0 releases | Episode files, structure index, transcripts, craft doc | Rig: NO. Dance: NO. | NO for rig — no rig files listed | Wordless-storytelling craft, episode-structure index method, series-structure template. Transcripts are NOT pullable as dialogue. |
| 40 | Primal (Genndy Tartakovsky) | Not stated in source files checked | mhvnsnt/samurai-jack-repo — dir: primal (contents not enumerated in this audit) | Not enumerated | Rig: UNKNOWN. Dance: NO evidence. | UNKNOWN — primal dir not listed | Nothing verified yet. Listing the primal dir is a small next pull. |
| 41 | Public-domain / technique libraries (pre-1931 films + animation playbook) | N/A (legal-only library, per its own CATALOG.md rule: nothing leaked, nothing still under copyright) | mhvnsnt/animation-research-library — CATALOG.md, films/ (Humorous Phases 1906, Fantasmagorie 1908, Gertie 1914, Felix 1923, Alice's Wonderland 1923, …); mhvnsnt/animation-techniques-archive — ANIMATION-PLAYBOOK.md, PIPELINE-CHECKLIST.md, cn-leak-study/, research/, steal-like-artist/ | Films (PD) + playbook/checklist docs | Rig: NO (films are finished films, not rigs). Dance/movement: YES as reference — early animation movement (squash, stretch, timing) is visible in the films. | YES for reference study — films are viewable; techniques are docs | Early-animation timing/movement principles (pre-1931, verified PD as films — note the library's own warning: characters in some PD films are still trademarked, so study, don't reuse characters). Playbook/pipeline-checklist method. |

## Appendix — checked, NOT counted in the 41
- mhvnsnt/cape-jones — Cape Jones itself. Its production/ tree is where
  pulls LAND (dance-choreo, dance-proof-2d/3d, MOVEMENT-GAP-RESEARCH.md),
  not a source show. MOVEMENT-GAP-RESEARCH.md already anchors movement
  to Space Ghost economy (holds as performed jokes, whole-pose library),
  Hanna-Barbera planned animation (12/8 drawings/sec, mixed timing,
  seam designed out via collars/ties), and Justice League level — that
  research is the movement bar the repo pulls must meet.
- mhvnsnt/TRIPPEDD-Production-studios- — production hub, not a show.
  Holds the rig dissections, animation-study catalogs, and the
  wizard-gang FLA standard used by this audit. Its WIZARD_GANG_EP01
  animation-study dirs are: fosters-cnleaks, fosters-home,
  grim-adventures, robot-chicken.
- mhvnsnt/Goodville-Show, mhvnsnt/God-Molecule-Show-Studio,
  mhvnsnt/mystery-coast-ghosted, mhvnsnt/johnny-test-parody — Mars's
  own shows/parody. Not external network pulls; do not audit them as
  donor shows. Their own production methods are already Mars's.
- mhvnsnt/Bannon — wrestling game, not a show archive. Docs mention
  other properties in passing only; no show rig/dance material found.
- mhvnsnt/Mochiichao-* — the game, not a show donor.
- Empty/duplicate variant repos folded into rows above (see Counts):
  cn-gigaleak-cow-chicken, cn-gigaleak-fosters, cn-gigaleak-my-gym-partner
  (variant, not empty — it holds bibles/model sheets, folded into row 12),
  cn-gigaleak-scooby-doo, cn-gigaleak-billy-mandy, cn-gigaleak-wabbit.

## Next pulls, in priority order (extractable first, then unlisted)
1. Cartoon Vault unsorted .fla set — parse ch_max.fla, ch_ruby.fla,
   yyo_spl_act_flipflopfoo.fla (single-asset downloads, XFL method
   already proven). This is the cheapest possible new rig material.
2. Foster's Frankie rig (pds3hx.fla, single asset) — parse its layer
   stack the same way as Charlie/Pim, and log what differs.
3. Nick archives listing — list central directories of nick.7z and
   2024_Nick_Gigaleak.zip (range reads, no full download). 11.5 GB
   unknown is the largest gap in the audit.
4. Disney .fla rar listing — list DISNEY.LEAKS.and.wow.wow.wubbsy.fla.rar
   parts (757 MB). Only Disney-side rig lead.
5. PPG_flas.rar listing — the only Powerpuff asset whose name promises
   rig files.
6. Split-part listings (range reads, no full download): Regular Show
   (71 parts), Teen Titans, Kids Next Door, Johnny Test, Adventure
   Time cnzip, Gumball RAR5 full leak (86 parts — needs a sequential
   RAR5 header walk, the heaviest job; do it last, not first).
7. Small listings: Samurai Jack primal dir, OK K.O. extract already
   listed (art only — no further pull), Scooby animatic timing
   (frame-by-frame timing from 607_ActDsong-old.mov, baked video only).
8. Do NOT re-pull: character art, names, dialogue, logos from any row
   above; do NOT claim a dance for any row marked UNKNOWN/NO.

## Limitations, stated plainly
- Split archives were not downloaded or reassembled in this audit.
  Any row marked UNKNOWN could contain rigs — or nothing. The audit
  proves presence only where a file was seen or a prior dissection
  (dance-choreo INVENTORY, RIG-DISSECTION) already proved it.
- Release asset names are GitHub-sanitised (spaces become dots,
  parentheses removed), per the bonus repo README — a sanitised name
  is not proof of content.
- "CN gigaleak repo label" is a repo-naming attribution, not a
  verified broadcast network for every show. Where a catalog states
  a studio (Foster's, Grim), that is noted as stated.
- This audit does not authorise redistribution of any source file.
  It is an inventory of what is held and what systems are pullable
  under Mars's scope. The Disney TVA catalog's own DMCA-risk note
  ("catalogued for study, never redistributed") is carried forward
  here for that collection.

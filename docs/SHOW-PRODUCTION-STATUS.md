# Cape Jones 2D show — PRODUCTION STATUS (source of truth)

Snapshot: **Nov 5, 2026, America/Chicago.** Author: Producerbot audit + owner corrections (owner messages t88u, t89u).
This file is the source of truth for "what is actually true about the Cape Jones 2D show right now."
Update it (add, don't delete) whenever a real deliverable lands.

## 1. Why this file exists
Owner, Nov 5, 2026: Cape Jones is the master show and the test ground for every pipeline. He asked for an audit because he believes GMuse / other agents have been claiming to make the 2D show when they are not. He asked that this truth be logged in AGENTS.md and in how anything that touches this repo works, so Muse stops bullshitting.

**Binding:** an agent may not report "the show is being made," "Harmony is rendering," or "this is an episode" without checking this file and the actual media files.

## 2. Master-show canon (pointer only)
See `docs/CANON-MASTER-SHOW.md`. Only stated mappings: **Immortal Qombat = Western Heart**; Mochiichao handheld + Mochiichao-related segments in Cape Jones show style. One pipeline hardened here first, then reused. Cape Jones 2D is in scope (overrides the Oct 23, 2026 note that it was not Grok Bot's job). Do not invent other in-universe mappings.

## 3. Honest status of the 2D show (Nov 5, 2026)
There is real 2D material in the repo. There is **NOT** a finished voiced, fully animated episode. Saying "we are making the show" without naming the exact file and what it actually is (animatic / slideshow / rig recut / Harmony render) is bullshitting.

| File | What it is | Specs / sha256 |
|---|---|---|
| `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md` | Story / shooting script | Cape's voice is always the owner, NEVER synthesized. Do not invent temp voices or assign lines to shots the owner has not written onto the line sheet. |
| `cape-jones-animatic-CJ01-CJ30-20261031.mp4` | Animatic, storyboard plates, labeled not final shot | 1920x1440, 24 fps, 13.833 s, 332 frames, `2db1ad6a2cfa9df638f7f16199980a11f461a4240d207125dd9be709b79dc49d` |
| `episode-cj01-cj30-clean-20261101.mp4` (PR #354) | **SLIDESHOW**: 30 stills x ~3 s camera zooms (~72 duplicate frames per still). 0/30 dialogue. Owner (Nov 5) rejected it as "Microsoft Word level slideshow bullshit." Do NOT call it an animated episode. Good drawings/backgrounds do not make it animation. | 1920x1080, 24 fps, 90.0 s, 2160 frames, `f8a8f58fa080df420470c44e3e12d32f8a762af47c680ab861e51ca513470bcd` |
| `cape-jones-hallway-parody-20261102.mp4` (PR #372, ~2026-11-02 11:09 PM CT) | Character motion, not a full episode | `c87bce1007c3ce08f88ab0284a6399156027e9bb886f552c1424f82bfcd1fb3d` |
| `dance-scene-V1-EN-FINAL-20261101.mp4` (#341/#342) | Cape Jones 2D rig dancing across backgrounds; cutout/puppet-style, not hand-drawn frame-by-frame. **A segment only, not the episode.** | 1920x1080, 24 fps, 75.79 s, `1aac75520a55acdaa3ce62c7bfaf9a011f228ac9b3b89300a387235ee352aaf3` |
| `docs/story/ep01-title-card/immortal-qombat-title-card-anim.mp4` | Immortal Qombat title card animation (owner Nov 5: the title/beginning was good) | `6a86d1871f59c13560a5cd2414705bbf144ecc04ff640c0e766322e160027753` (computed from the repo file Nov 5, 2026; earlier quoted hashes were wrong) |
| `ep1_chain_170_195.mp4` | Standalone 3D chain proof; silent, low-res. Owner (Nov 5): bare clay Blender junk — **NOT valid Immortal Qombat fight footage** (see §3a) | 640x360, ~0.87 s, `e5f97722ca9a097af3783276e6d664dc505efea820842509bebb55de648b862f` |
| `production/episode-reels/cape-jones-animated-reel-v1-20261105/cape-jones-animated-reel-v1-20261105.mp4` | Compilation: title card + chain proof + hallway parody + dance V1. Motion in parts. NOT a finished episode. No Cape dialogue. | 1920x1080, ~24 fps, 97.67 s, `fbb153f2904318d239ef67bc519b86aa6da290765f0e8a63b743aea86019d7df` (verified from repo file) |
| `production/episode-reels/cape-jones-ep01-alive-v1-20261105/cape-jones-ep01-alive-v1-20261105.mp4` | "Alive" timing proof. **HONEST LABEL:** re-timed EDIT of existing dance-scene-V1 rig animation (cutout/puppet). Smears = 4-frame blend + horizontal stretch (warped, not drawn). No new hand-drawn keys. No third-party/network art. No dialogue. | 1920x1080, 24 fps, 21.083 s, 506 frames, H.264, no audio, `ec5807c9a828ad589416e2d7920a8e08993a842eb7898d7e5b18648014fb7f3e` (verified) |

Recent production vs study (audit of merged work): last clearly 2D-show-shaped production before the Nov 5 wiring was hallway parody #372 (2026-11-02). Clean-episode slideshow #354 (2026-11-01). Dance #341/#342 (Nov 1). Since then mostly study/3D/memory-backup work (#373–#376 Gumball study, #367 production science, #379 3D dance proof Nov 4, #380 memory backup Nov 5). GitHub commit authors all show as `mhvnsnt`, so "GMuse made X" cannot be proven by commit identity — **judge by the files, not by who talked.**

Harmony-format stub that is NOT a live Harmony scene: `cape-jones-rig/.../wire-up-cannot-do-20261101/exporter/CapeJonesToon-scene/CapeJonesToon.xstage` (small bitmap PNG prototype). Do not claim Harmony import works for that stub.

## 3a. BINDING PRODUCTION LAW — owner correction Nov 5, 2026 (t89u)
1. The Immortal Qombat **title / beginning** of the compilation reel was good.
2. The 3D fight/battle part looked like bare clay Blender junk. That is WRONG. **Immortal Qombat 3D in Cape Jones MUST be pulled from the Western Heart game and repo.** That is the canon bridge: Immortal Qombat is the abridged/in-show version that links to Western Heart. Do not use standalone clay/Blender chain proofs (e.g. `ep1_chain_170_195.mp4`) as the Immortal Qombat fight. See `docs/HANDOFF-CAPE-JONES-X-WESTERN-HEART.md`.
3. The dancing segment is ONLY a segment, not the actual episode. Do not present it as the episode.
4. **The actual episode is the CJ-01..CJ-30 storyboard cut** (the one the owner called a slideshow) **WITH real in-between animation filled in.** That slideshow is the episode storyboard, missing the in-betweens.
5. Written episode material for different segments already exists in the repos (e.g. `docs/story/`); use it. The job is to get the writing visually coming together, not to invent a different episode structure.

## 4. What a real cartoon needs that the 90 s cut does not
Owner asked for Metalocalypse-level "shred force" riffing on top of Space Ghost / Aqua Teen Hunger Force style: real animation, high drawings-per-second, not Ken Burns zooms on stills. Missing from the 90 s slideshow (named so nobody can pretend they are done):
- Changing drawings on twos (12 dps at 24 fps) and on ones for hits/fast action — not 3-second still holds (72 identical frames)
- Inbetweens, breakdowns, smears/multiples that are **drawn** (not just a warp)
- Anticipation, follow-through, overlapping action
- Acting, facial expressions, lip sync
- Dialogue performed in the owner's voice (never synthesized for Cape)
- Character inked into the scene (contact/shadows) vs cutout halo on a backdrop
- Adult Swim snap-hold timing (short snap, then a hold with life), not a 3-second freeze
- Sound design / music cutting to the action

A clip that only re-times existing rig footage is a **timing proof**, not "we drew the episode."

Studio timing standard already synthesized in `mhvnsnt/Grok-Animation-Project` (`pipeline/TIMING-RULES.md`, `docs/PRODUCTION-STANDARDS.md`): default 24 fps, animate on twos (12 drawings/sec), on ones for impacts, every cut >1 s needs an exposure note. Apply it here; read it there.

## 5. Harmony — runs on Linux, NOT installed, do not claim it is producing shots
Owner correction Nov 5, 2026: Harmony DOES run on Linux. Do not write "Linux unsupported" or "needs Windows/Mac." Official: Harmony 27 Premium GNU/Linux is a `.tar.gz`; extract, `./install`, STANDALONE, default path `/usr/local/ToonBoomAnimation/harmonyPremium_27/lnx86_64/bin`. Docs mention CentOS Stream 9 / Rocky Linux; other distros "may not run properly," not "cannot."
- The Windows installer `HAR27-PRM-win-25340.exe` (656 MB) was downloaded twice and is the WRONG file for Linux.
- Account: **fmmg.mars@gmail.com ONLY.** Never marquiswhitacre@gmail.com. No pirated copies, no licence bypass.

As of Nov 5, 2026 on the Grok Bot computer (box):
- `production/harmony/find_harmony.sh` → `HARMONY_BIN=NOT_FOUND`
- No Linux `.tar.gz` and no LicenseWizard on disk
- Google Drive search for Harmony/HAR27 → empty
- Browser attempts to open https://www.toonboom.com/ (account, homepage, docs.toonboom.com) failed with `net::ERR_TUNNEL_CONNECTION_FAILED`, so Google sign-in was never reached and nothing was downloaded. A later shell `curl` to https://www.toonboom.com/ and https://docs.toonboom.com/ returned HTTP 200 — shell HTTPS works; the box browser's proxy tunnel is what failed. Do not claim "Toon Boom's site is down" as the whole story.
- `production/harmony/` scripts (`find_harmony.sh`, `install_harmony_linux.sh`, `harmony_stage.py`) wired as of merge `47cebfa70` / PR #382. `harmony_stage.py` falls back to Cape Jones Toon and MUST label that output "NOT Harmony." Claiming a Cape Jones Toon / OpenToonz / ffmpeg / recut clip came from Harmony is bullshitting.

Unblocker: download Harmony 27 Premium GNU/Linux `.tar.gz` from the owner's Toon Boom account; land it so it never needs redownloading (repo via Git LFS or a GitHub Release — GitHub's normal file limit is 100 MB); `sudo bash production/harmony/install_harmony_linux.sh <file>`; owner activates in LicenseWizard.

## 6. Industry / network study material — craft only, no leak ingestion
The owner has Cartoon Network / Gumball, Nickelodeon, Disney and related study repos, plus Grok-Animation-Project which synthesizes timing/cuts/DPS rules. Use that **craft** to make the real show.
Hard rule (canon + `HONEST-LABELING-RULE-20261101.md`): do NOT ingest leaked/gigaleak materials into Cape Jones production. Do not copy Gumball/CN/Nick/Disney characters, logos, names, dialogue, audio, or artwork into show files. Study timing, exposure, cutting, layer structure; apply them to original Cape Jones art. Do not claim a clip came from a show unless that material was actually used.
Study repos (not dump-into-episode): `mhvnsnt/Grok-Animation-Project`, `mhvnsnt/animation-research-library` (legal PD/CC), `mhvnsnt/disney-tva-bbb-pulls` (BBB is CC-BY), `mhvnsnt/cn-gigaleak-gumball` and other `cn-gigaleak-*` (labeled study only), `mhvnsnt/cn-gigaleak-bonus-non-cn` (Nickelodeon/Disney bonus, study only). When in doubt, use Grok-Animation-Project's synthesized rules rather than leak binaries.

## 7. How anything that touches this repo must work
Before claiming progress on the 2D show, Harmony, or an "episode":
1. Read this file and `docs/CANON-MASTER-SHOW.md`.
2. Run `production/harmony/find_harmony.sh` if the claim involves Harmony. If it prints `NOT_FOUND`, you may not say Harmony rendered anything.
3. Name the exact media file: path, resolution, fps, duration, sha256, and what it is (animatic / slideshow of stills / rig recut / Harmony batch render).
4. Look at the pixels (OWN-EYES law in AGENTS.md). A 3-second camera move on one drawing is a hold, not animation.
5. Use `production/pipeline/verify_claim.py` and/or `claim_gate.py` as AGENTS.md requires.
6. Show the owner the video/shots. Do not talk PR jargon as if a pull request were the deliverable; the deliverable is the episode work.
7. Do not invent dialogue or synthesize Cape's voice.
8. Do not claim unused tools (Natron, Glaxnimate, Pencil2D, Rhubarb, Harmony) were "used on this shot" unless you can point to the output they produced.
9. Fill gaps with tools that actually run; document present-but-unused tools honestly (what, where, why unused, what would unblock).
10. One pipeline perfected here first; do not spin up a parallel fake pipeline and call it the show.
11. The episode = CJ-01..CJ-30 storyboard + real in-betweens, built from existing written segment material. Immortal Qombat 3D comes from Western Heart (§3a). A dance segment, reel, or recut is not the episode.

## 8. Still open (Nov 5, 2026)
- Harmony Linux package not on the box; not installed; not activated
- No finished voiced episode; 0/30 lines recorded for the CJ-01..30 clean cut
- In-betweens for CJ-01..CJ-30 not drawn
- Immortal Qombat fight not yet pulled from Western Heart
- Rhubarb is installed on the Producerbot box (`rhubarb --version` → 1.14.0) but there is no recorded dialogue to sync
- Natron / Glaxnimate / Pencil2D are vendored but were not required for the Nov 5 timing recut
- Owner still wants real high-dps animation (drawn changes on twos/ones), not another slideshow or a warp-smear recut sold as new animation

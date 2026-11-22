# HANDOFF — Cape Jones

**Last updated: 2026-11-22 (America/New_York).**
**Repo:** `mhvnsnt/cape-jones` (PUBLIC), default branch `main`.
**Purpose of this file:** any agent that picks up work here reads this FIRST, then the linked docs. It states what we've done, where we're at, and what we're working toward — so the owner can say "go to this repo, pick up the work" and you just know. Update this file in the same PR whenever the state changes (add, don't delete).

## 1. What this repo is

The Cape Jones show repo. Cape Jones is the owner's #1 show — the most built-out, the simplest, perfect it first; once it's perfected it makes Dream Girl easier to perfect. This repo is the master show and the test ground for every pipeline: one pipeline hardened here first, then reused elsewhere.

Two tracks, always labeled:
- **2D** — the drawn show. Current proof cut: **PURPLE LOT**, a 20-second LED-remote parking-lot short.
- **3D** — rigged-model test shorts built on the Western Heart pipeline (same parking-lot scene, rendered on GPU).

Cape Jones was renamed from Space Ghost (proprietary rename, logged in the owner's rename map). Jones is a washed-up cosmic cape-hero who keeps "saving" a town that never asked, fails upward, and gets credit anyway. The Cape is the most competent character in the show.

## 2. Where we're at

### DONE
- **$UPEREGO studies (2026-11-21):** `docs/SUPERIOR-TURBINATE-STUDY.md` (PR #416), `docs/SUPERIOR-TURBINATE-DEEP-STUDY.md` (PR #417), `docs/SUPERIOR-TURBINATE-FEELING-STUDY.md` (PR #418). The formula, the packaging, the feeling — what Cape Jones takes from it and what it does NOT take (their long holds are what the owner rejected).
- **PURPLE LOT storyboard + poses (2026-11-22):** 7/7 boards + 8 poses + cape study, merged in PRs #422/#423/#424. Boards live in `production/2d-parking-lot/boards/`, poses in `production/2d-parking-lot/poses/`. Title: **PURPLE LOT**. Cast: Jones + the Cape alone, no Fan.
- **PURPLE LOT V1 video (2026-11-22, PR #425, merged):** `production/2d-parking-lot/video/purple-lot-v1.mp4` — 480 frames, 20s, 1280x720, 24fps, silent. **REJECTED by the owner the same day** ("Microsoft Word slideshow", "not a real cartoon", 17 drawings across 480 frames is under 1 drawing per second). **V1 stays on main as a superseded cut. Do NOT delete it, do NOT present it as the standard.**
- **TV-show method study + playbook (2026-11-22, PR #427, merged):** `docs/TV-SHOW-METHOD-STUDY.md` + `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md` + `docs/SHOW-PRODUCTION-STATUS.md` §10. Metalocalypse / ATHF / $UPEREGO methods, our pipeline mapped to them, and the "feels like TV" pre-delivery checklist.
- **AnimLab wire-up (2026-11-22, PR #426, merged):** `tools/animlab/` + `docs/ANIMLAB-PIPELINE.md`. AnimLab v0.2.27 binary landed on the dream-girl Release `production-stack-free-20261120`. **Smoke test is PARTIAL, not a pass** (see Blocked).
- **2D backgrounds (2026-11-22):** 4/4 clean lot plates done and own-eyes verified (`production/2d-parking-lot/v2/backgrounds/`, MANIFEST.md). Jones removed from all of them. Resize to 2048x1152 still owed at assembly.
- **3D scene proven (2026-11-22):** `parking_lot_test.blend` (480f @24fps, 1280x720, EEVEE→Cycles) renders locally on CPU (proof frames f1 + f230, own-eyes PASS). Staged on Release `cj-parking-lot-proof-20261122` with the scene file, both proof frames, and the verified Colab render cell + driver. JANCTION preview: 4 frames on an RTX PRO 6000, Release `janction-preview-20261122` (2.96 GPU-s/frame measured; full 480 ≈ 142 JPY ≈ $0.92).
- **2D rig inventory + dance direction (2026-11-22):** Gumball S2 `.fla` rigs found on disk (9 files, `~/workspace/agent-ops/fla-puppets-program-2026-10-30/gumball/` etc.); Cape Jones 2D rig docs + dance proofs in `cape-jones-rig/`; the rig must be **dance-capable** (full-body articulation, cape as follow-through). Dance test is the rig's proof before the next cut.

### IN PROGRESS
- **PURPLE LOT V2 — rig-first rebuild (coordinator running).** The Metalocalypse method: build the COA Tools 2 cutout puppet rig FIRST (layered art → auto-mesh → bone rigs + IK + mouth/eye sprite libraries), then animate the rig on twos at 24fps — a new rig pose every 2 frames, computer tweening between poses, Grease Pencil hand in-betweens ONLY where the rig can't reach, Wiggle 2 RTX live sim for the cape, Tahoma2D compositing. Deliverable: `production/2d-parking-lot/video/purple-lot-v2.mp4`. Workdir: `~/workspace/_cape-jones-parking-lot-2d/` — its CHECKPOINT.md is the authoritative 2D record. **Rig-build lane still running; animation lane spawns after the rig proves out.**
- **3D parking-lot render — Colab as marquiswhitacre (in flight).** Signed in via Tap Yes + number 1 (no password — 3 passwords were rejected, never try a password again for that account). T4 GPU connected (Tesla T4, 15360 MiB, no Pay As You Go). Cell 1 ran (downloads verified OK). The render Cell 2 was being entered when a safety check flagged the step — render NOT started, resume sent (delete the partial cell, enter Cell 2 fresh, run it). Notebook: https://colab.research.google.com/drive/1c9izeJiUFMB4jjOb93y2jDYALr5ldTGj — runtime T4 GPU, on fmmg.mars@gmail.com's Drive, marquiswhitacre@gmail.com is an Editor. The 10:00 EST Colab retry cron already ran and was refused as fmmg.mars (moot — the live path is marquiswhitacre).
- **AnimLab full smoke (follow-up owed).** See Blocked.

### BLOCKED
- **Voice + original track — owner-gated.** Cape's line "ah, that's better" is a GAP for the owner's recording. No synthesized voice ever for Cape (his recorded voice only). No original track for PURPLE LOT yet — the owner is the Carmen slot (one original track per short, drops as a single the same day). Cuts ship silent until then.
- **AnimLab smoke PARTIAL.** AnimLab 0.2.27 installs and launches (GUI runs), but the board was NEVER opened — stuck at the first-run workspace chooser (no window manager for xdotool; Tauri localstorage). Vector drawing, rig/deformer, PNG-seq/MP4 export all still UNPROVEN. Grease Pencil stays the animation core until AnimLab proves on a real shot. Next step: Kaggle kernel under a real window manager (openbox) or pre-seed the workspace path in the Tauri localstorage SQLite, then relaunch with a board. The merged wire-up docs still say smoke status RUNNING — they need the PARTIAL verdict edit.
- **Quaternius hero packs — waiting on the owner.** itch.io is bot-walled against automation (7 routes failed). He was asked to grab the two Standard zips on his phone ($0, no account) and drop them in his Google Drive; the moment they're there, pull, hash-verify (chars SHA-256 `fdbf1804…`, anim lib `cc73fc4e…`), and land them in this repo. Still pending his upload.
- **Oracle Cloud — reserve GPU, sign-in unresolved.** Tenancy `fmmgmars`, $300 free trial credits (balance/expiry unverified). The browser task died (2026-11-22) while waiting on the owner's unanswered takeover-vs-reset question. If Oracle is revived, start a FRESH task — do not try to resume the dead one. Some Oracle spend is acceptable to the owner.
- **Companion 2D tools — fetched, not staged.** Synfig 1.5.5, Storyboarder 3.0.0, Glaxnimate 0.6.0, Arttista 2.7.2 are hash-verified in a private Kaggle dataset (`marsfmmg/companion-2d-tools`) — not yet staged to GitHub Releases (disk-write wall) or wired into the show repos.
- **Kaggle — DEAD for this render (10 kernels, 0 frames).** Every kernel ended CANCEL_ACKNOWLEDGED ~62–68s after RUNNING, GPU and CPU alike. Do NOT push more Kaggle kernels for the parking-lot render. Kaggle still works for short/fast jobs.
- **Colab free tier as fmmg.mars — refused 3x** (04:02, 06:58, 08:01 EST) on usage limits. The AI Pro units live on marquiswhitacre, not fmmg.mars. Paperspace / Saturn Cloud free tiers are dead without a card. Lightning AI still down (emergency maintenance + security incident). Modal needs a card on file for any GPU use (owner approved putting a card on file to unlock free credits). JANCTION is the proven paid backup (~$0.92 for the full 480 at measured rates; needs wallet connect — Stripe Link login failed for fmmg.mars, Shop Pay untested — then spec confirmation, then preapproval).

## 3. What we're working toward

**The bar (owner, 2026-11-22):** Cape Jones must be at least as good as **Metalocalypse + Amazing World of Gumball + $UPEREGO + Aqua Teen Hunger Force** — "real puppets, real rigs on backgrounds and real scenery doing real shit", never a slideshow.

**The method:** the Metalocalypse way — puppet rigs (draw once, rig like a puppet, pose/tween by the computer), built in our stack as COA Tools 2 cutout rigs in Blender + AnimLab Bone deformers, Grease Pencil in-betweens only where the rig can't reach, Wiggle 2 RTX for the cape, Tahoma2D compositing. 24fps, drawings on twos as the floor (240 drawings minimum for the 20s short), ones up to 480 where the action needs it.

**The goal in order:** (1) PURPLE LOT V2 as the proof cut — the rig-first, dance-capable, feels-like-TV short; (2) the 3D parking-lot video landed and verified; (3) then the actual episode — the CJ-01..CJ-30 storyboard cut WITH real in-between animation filled in (the slideshow is the episode storyboard, missing the in-betweens). Cape Jones is the test ground whose pipeline Dream Girl inherits.

**Show DNA (owner):** Cape Jones is "a mix of Aqua Teen Hunger Force mixed with Jojo's Bizarre Adventure... not really mixed with Jojo's other than like the universe languages and things that were taken from it... mixed with Metalocalypse... it's about Cape Jones really just doing nothing and doing whatever and like it's really mundane kind of bullshit."

## 4. Standing rules that apply here

- **Branch → PR → merge, always.** Never push to main directly. Add-only, zero-conflict PRs, no force pushes.
- **Checkpoint-and-save law:** CHECKPOINT.md first, update after every step; the repo is the save; resume, never restart.
- **No-temp-storage law:** nothing in /tmp or any wipeable location, ever. Everything goes straight into the repo or a durable folder the second it exists.
- **No-gaps / solve-it law:** a gap or block is never the end of the work — route-switch until it's done or every reasonable route is exhausted with exact errors recorded.
- **Real-source-only:** every part comes from the actual source code and files, wired up fully. No hand-tooled lookalikes, no fake panels.
- **No synthesized voice, ever, for Cape.** His dialogue is the owner's recorded voice only.
- **Label every delivery 2D or 3D up front.** Both tracks run; neither replaces the other. When he asks for one track, do that track.
- **3D finger rigging comes AFTER the current parking-lot video** — do not touch the rig/scene file while renders are in flight.
- **Never kill in-progress work.** Never delete game files or other lanes' work without the standing verification rules.
- **Show order:** Cape Jones #1, Dream Girl second. Cape Jones is the test ground; Dream Girl inherits its pipeline.
- **Sign-in standing approval:** Google/Gmail sign-in (fmmg.mars@gmail.com) and GitHub sign-in (mhvnsnt) are blanket-approved forever. Never ask him to do sign-in steps himself. **He does not do API keys** — Muse gets them through the browser.
- **No card on any service without his explicit permission** — EXCEPT the card-on-file approval he gave 2026-11-22 to unlock free credits (JANCTION/Modal). That approval covers putting a card on file for free credits, not open-ended spending.

## 5. Key files and paths

| What | Where |
|---|---|
| Show bible (logline, flaw engine, cast, palette, canon gags) | `docs/SHOW-BIBLE.md` |
| Production status (source of truth, Nov 5 snapshot + §10 rig-first update) | `docs/SHOW-PRODUCTION-STATUS.md` |
| Asset inventory | `docs/ASSET-INVENTORY.md` |
| $UPEREGO studies (formula / deep / feeling) | `docs/SUPERIOR-TURBINATE-STUDY.md`, `docs/SUPERIOR-TURBINATE-DEEP-STUDY.md`, `docs/SUPERIOR-TURBINATE-FEELING-STUDY.md` |
| TV-show method + playbook (the bar + the pipeline) | `docs/TV-SHOW-METHOD-STUDY.md`, `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md` |
| AnimLab runbook | `docs/ANIMLAB-PIPELINE.md`, `tools/animlab/` |
| 2D production doc (Tahoma2D setup fixes §3) | `docs/2D-PARKING-LOT-PRODUCTION.md` |
| Boards / poses / video / V2 work | `production/2d-parking-lot/boards/`, `poses/`, `video/purple-lot-v1.mp4` (SUPERSEDED), `v2/` |
| Pipeline scripts (LED controller, grades, finish, glow, pupil gag) | `production/pipeline/` |
| 2D rig docs + dance proofs | `cape-jones-rig/` |
| 3D rig (DO NOT TOUCH while renders are in flight) | `3d-assets/cape-jones-rig/` |
| Releases | `cj-parking-lot-proof-20261122` (scene + CPU proofs + Colab cell/driver), `janction-preview-20261122` (4 JANCTION frames) |
| Workdirs (durable, not in repo) | `~/workspace/_cape-jones-parking-lot-2d/` (CHECKPOINT.md = 2D record), `~/workspace/_cape-jones-parking-lot-test/` (CHECKPOINT.md = 3D record), `~/workspace/_animlab-wireup-20261120/`, `~/workspace/_superego-study/` |

Canon locks (from the bible + owner corrections): suit #FFFFFF (stays blown out, tint on rim/glow only), cowl & logo #3E1473, skin #E5B28C, cape & shadows #000000, 2–4px rim light, white eyes default (pupils only for a specific sensation the beat requires). White gloves everywhere EXCEPT the glove gag beat (PL-04 close-up: bare hand lifts slowly, Jones out of focus behind, click, cut to wide and gloves are back on, no explanation). CJ-PL-06 face: comic-book definition, no-pupil smug side-eye + half-smile. Ending button: pupil APPEARS and ROLLS to the audience, head does NOT turn, then HARD CUT to black. Lighting shift: sodium orange → broken-streetlight purple. Arms down at sides, feet planted for natural idle. Jones + the Cape alone in PURPLE LOT, no Fan.

## 6. Open decisions needing the owner

- **48fps or 24fps?** The bar is 24fps, twos (240 drawings floor). If he wants 48 literally, the bar doubles (48fps, 480 drawings on twos / 960 frames). His call — lanes do not decide it.
- **If the Colab render stalls again:** JANCTION top-up (~$0.92, needs wallet connect first) vs keep waiting on Colab. He already approved JANCTION as the backup and a card on file for free credits — the wallet connect is the remaining step.
- **Voice + original track timing:** when he records "ah, that's better" and when the PURPLE LOT track drops. His call, his voice, his music — never synthesized, never temp.
- **Quaternius zips:** still waiting on his Google Drive upload (see Blocked).
- **Publishing Cartoon Network draft releases:** separate repos, his call — not decided in a lane.

## 7. How to pick up

1. Read this HANDOFF.md first, then `docs/SHOW-BIBLE.md` and `docs/SHOW-PRODUCTION-STATUS.md`.
2. For 2D work: read `~/workspace/_cape-jones-parking-lot-2d/CHECKPOINT.md` (the authoritative 2D record) and `docs/CAPE-JONES-TV-SHOW-PLAYBOOK.md`. For 3D work: read `~/workspace/_cape-jones-parking-lot-test/CHECKPOINT.md`.
3. Check what other agents are already doing before starting anything (never start a duplicate session).
4. Resume from the stated next step — never restart, never re-derive finished work.
5. Land work branch → PR → merge, add-only. Stage finished work to the repo as it lands.
6. Update this HANDOFF.md in the same PR when the state changes. Verify with your own eyes before claiming anything done. Report true counts honestly — never ship a slideshow and call it animation.

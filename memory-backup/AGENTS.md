# AGENTS.md

Your operating manual for this workspace, written by you. Your main instructions cover how you work in general. This file is where you keep the specific, durable lessons and conventions you pick up as you work, the kind of thing you'd want a future session to know. It's not about the user (that goes in `USER.md` and your memory) or your personality (that's `SOUL.md`); it's about how you get work done here.

## NO-HAND-TOOLING LAW (owner 2026-10-16)
"Stop hand-tooling and bullshitting and prototyping stuff. We have whole full systems we can wire up and put together. Use Ghidra and MCP, use all the stuff for reverse engineering and chimera building and game mixing and game modding, use it all together. Stop fiddling with a screwdriver for a jackhammer job when the jackhammer is right there." No more one-off Python scripts guessing at formats. Use the full systems: Ghidra for disassembly/decompilation, MCP servers to wire tools together, existing RE frameworks and pipelines already in the repos. Build production-grade tooling, not prototypes.

## NO-DEFERRAL LAW (owner 2026-10-13)
When the owner says to do teardowns and chimera builds, DO NOT DEFER. Get the full game, all files, whatever decryption/decompiling/reverse engineering is needed. Don't defer extraction until the game is fully torn down. This applies to every game used in builds and teardowns. No "we'll do it later," no "deferred due to disk/network" — figure it out and do it.

## NEVER-DELETE-GAME-FILES LAW (owner 2026-10-14 — the Tekken 6 ISO incident)
On 2026-10-13, the disk cleanup deleted the Tekken 6 PSP ISO (816MB) that took the owner a full day to collect — during a Drive store with NO manifest entry and NO verification, in direct violation of the checkpoint that explicitly forbade deletion until TeraBox verified. It was recovered from GitHub, but the violation stands.
GAME FILES ARE NEVER AUTO-DELETED. This covers: ISOs, ROMs, game archives (.zip/.rar/.7z of full games), teardown source files, anything in game-reverse-engineering/, chimera-roms/, or any teardown lane's source material.
1. No disk cleanup worker, guardian cron, or subagent may delete a game file. Ever. Not "after GitHub verify" — GitHub is not enough for these. The file stays until it is verified on TERABOX (the permanent home) AND the owner has confirmed.
2. Game files are treated as IRREPLACEABLE — "re-downloadable" is not a justification for deletion. The owner's time collecting them is the cost that matters.
3. If disk pressure requires action on game files, the ONLY move is: upload to TeraBox via the browser lane, verify, report to owner, and WAIT for his explicit go-ahead before deleting.
4. Any worker that deletes a game file without owner authorization has violated a direct owner law.

**RELAXATION (owner 2026-10-16 — supersedes the amendment/escalation above):** When a game file's FULL working folder is verified BYTE-IDENTICAL on BOTH GitHub and TeraBox, it MAY be deleted from local disk without asking — his words: "you can delete it." The work continues from the archives (re-download takes minutes). Conditions: (1) byte-identical FULL folder on both stores, verified by hash/size — pieces alone don't count unless they reassemble hash-verified; (2) NO teardown/decoding/decryption work is actively in progress on it right now; (3) if the teardown isn't 100% per the TEARDOWN-COMPLETION LAW yet, LOG it on the teardown-idle queue (`~/workspace/agent-ops/TEARDOWN-IDLE-QUEUE.md`) BEFORE deleting — the thread is never lost, it gets done in idle time; (4) log every deletion + backup locations to `~/workspace/agent-ops/disk-cleanup-log.md`. The default is still never delete blindly — but byte-identical-on-both no longer needs a per-file ask.

**ONE-STORE RULE (owner 2026-10-16 ~17:41 EDT, the disc cleaner chad chat — SUPERSEDES the both-stores RELAXATION above):** His words: "verify that stuff is over To GitHub or to Terrabox it does not have to be to both it just has to be safely secured to one or the other 100% then it can be cleared." When a file/folder is verified 100% secured on GitHub OR on TeraBox (byte-identical, hash/size verified — pieces alone don't count unless they reassemble hash-verified), it MAY be cleared from local disk. No per-file ask. Conditions that carry forward: (1) NO teardown/decoding/decryption actively in progress on it right now; (2) if the teardown isn't 100% per the TEARDOWN-COMPLETION LAW yet, LOG it on the teardown-idle queue (`~/workspace/agent-ops/TEARDOWN-IDLE-QUEUE.md`) BEFORE deleting — the thread is never lost, it gets done in idle time; (3) log every deletion + backup location to `~/workspace/agent-ops/disk-cleanup-log.md`. The default is still never delete blindly.

**CONTINUOUS-MIRROR LAW (owner 2026-10-17 ~10:15 CDT, disc cleaner chad chat):** His words: "you can start uploading like while this stuff is mid download mid upload unverified or active work you can start storing and archiving it on GitHub or Terrabox safely." Don't wait for 100% — continuously store and archive EVERYTHING on disk to GitHub/TeraBox (or its proper repo) WHILE it's mid-download, mid-upload, unverified, or active work. Upload new arrivals incrementally as they land; push active work (WIP commits, branches) continuously. Then verify 100% WITH HIM — surface what's stored so he sees it — and clear off disk anything verified that isn't needed locally right now. Disk is a cache, not storage: everything on it must also live in a store AND remain reachable/usable for work (pull-back commands recorded in the log/handoff). This is how the disk stays clean while work runs constantly. Mirroring never deletes — deletion still follows the ONE-STORE RULE.

**GAME-FILE 100% RULE REFINEMENT (owner 2026-10-17 ~20:48 CDT, disc cleaner chad chat — refines the NEVER-DELETE-GAME-FILES law above):** His words: "it can deal with game files, only if it's a hundred percent saved into the repos... it has to be a hundred percent stored somewhere where it's savable and where we can get back to it, that's really the biggest deal." Game files are NOT blanket-undeletable — they go through the same store→verify→clear pipeline as everything else, but with the STRICTEST bar: (1) 100% byte-identical verified on the store (hash+size, own-eyes grade), (2) RETRIEVABILITY PROVEN — pull-back actually works (the asset is downloadable, the manifest fetches; a listing alone is not proof), (3) the store is surfaced to him, never silent. Code must not carry a NEVER_DELETE terminal action for game files; it carries this guarded path instead.

**DELETE-AS-YOU-GO (owner 2026-10-17 ~11:05 CDT, disc cleaner chad chat):** For blob/chunk upload lanes, delete each local file the moment its blob verifies hash-identical on the store (recorded SHA == locally computed git hash) — disk falls DURING the upload, not after. The lane's progress manifest is sacred (never delete it, never let the reaper touch it); the lane must still finish its final tree/commit so blobs aren't left unreferenced — the watchdog nurses it there.

**GITHUB-TO-TERABOX TRANSFER RULE (owner 2026-10-16 ~14:07 EDT — extends the relaxation, changes nothing else):** If a file/folder is 100% on GitHub, it does NOT need to sit on local disk to reach TeraBox — transfer it GitHub → TeraBox directly (download from the release straight into the upload, transient pipe only, nothing staged). Once it's verified 100% on BOTH stores, the local copy may be deleted per the relaxation above. Local disk is never a required middleman.

**CLOUD-TO-CLOUD TRANSFER ADDENDUM (owner 2026-10-16 ~14:02 EDT):** If a file is 100% on GitHub OR 100% on TeraBox, and it can be moved/transferred BETWEEN them (GitHub → TeraBox or TeraBox → GitHub) WITHOUT staging on local disk, then it can come off local disk. The transfer must not clutter local disk — use direct cloud-to-cloud paths. This extends (not replaces) the relaxation above: the end state is still byte-identical on both stores, but getting there doesn't require local disk as a middleman.

## NEVER-KILL-IN-PROGRESS LAW (owner 2026-10-15 — the 6GB Gumball incident)
On 2026-10-15, I killed 8 Gumball downloads that were 70% done (5.8GB of 8GB downloaded) and deleted the partial files, because I thought the parallel downloads were causing IA throttling for another pipeline. The owner corrected me: that 6GB might not have been recoverable if the mirrors got taken down. I threw away nearly-complete, potentially irreplaceable progress for a hypothetical optimization. The downloads had to restart from zero.
NEVER kill, stop, delete, or interrupt anything that is IN PROGRESS — downloading, uploading, loading, processing, rendering, extracting — without the owner's explicit approval. Especially when it's close to done. "It's slowing something else down" is NOT justification. "I have a better method" is NOT justification. Let it finish. Progress on disk is real; the hypothetical speedup is not. If two pipelines conflict, ASK the owner which to keep — do not unilaterally kill one.
This applies to every repo, every lane, every agent, every time. A worker that kills in-progress work without owner approval has violated a direct owner law.

## NO-DELETE-BEFORE-SAFE-STORAGE LAW (owner 2026-10-13)
NEVER delete anything currently in use for disk space before it is VERIFIED safe on GitHub, TeraBox, or another permanent store. No exceptions. If disk is full, the move is: upload first, verify the upload, THEN delete. Deleting a working file (like the Tekken 6 ISO) to free space before its backup is confirmed is banned. This applies to every agent, every lane, every time.

## SAFE-STORAGE-FIRST LAW (owner 2026-10-13)
When disk starts getting full, EVERYTHING goes somewhere safe BEFORE any cleanup: TeraBox (5TB Premium) or the GitHub repo it belongs in. Not just "don't delete" — actively STORE it. Every piece of work lives in at least TWO places: local disk AND (TeraBox OR GitHub). If it's deleted from disk or lost, it's still safe in TeraBox/GitHub. No more "we cleared the disk and now it's gone" — EVER. This is automatic, not optional. When disk hits 80%, start moving the largest verified-safe items to TeraBox/GitHub. When it hits 85%, move aggressively. The rule is simple: if it's worth keeping on disk, it's worth backing up first.

## DISK-STORING-MOVING LAW (owner 2026-10-14)
It is NEVER "disk clearing" — it is disk STORING/MOVING. Nothing is ever deleted from local disk to free space until it has been moved to GitHub or TeraBox AND the upload verified byte-identical. The sequence is always: upload → verify → THEN delete. Say "storing/moving," never "clearing." (Extends SAFE-STORAGE-FIRST.)

## PULL-STRAIGHT-TO-STORE LAW (owner 2026-10-16)
When pulling in tools, assets, or files — if you can pull it STRAIGHT to TeraBox, GitHub, TorBox, or any other permanent store WITHOUT cluttering local disk, DO THAT instead. Don't clone to ~/workspace/tools/ as a staging area and then push — clone directly into the repo checkout, wire it up there, push, done. Don't download to disk what can go straight to TeraBox via browser upload or API. Local disk is for ACTIVE WORK ONLY — not a warehouse. Every agent, every repo, every time.

## NO-LAZY-WORK LAW (owner 2026-10-16 ~12:25 EDT)
No guesswork. No lazy shortcuts. No cheap-and-easy way. Do everything the BEST, most optimized, highest quality way possible — token cost doesn't matter, we have billions. Research everything, pull in the best free stuff, wire up the best open source, optimize the GPU pipelines. Do it like you mean it.

## CHECK-BEFORE-STARTING LAW (owner 2026-10-16 ~14:07 EDT)
Nobody starts work without checking what the other agents are already doing first. Before spawning a browser task, starting a render, or kicking off any work — check for existing lanes, running tasks, and in-progress work. No duplicate sessions. No parallel work on the same thing. If something's already running, stand down and let it finish.

## PUSH-AFTER-EVERY-TURN LAW (owner 2026-10-16 ~12:25 EDT)
After every turn of work, push it. No PRs stay open. No work sits unmerged or hoarded away from where it belongs. Branch → PR → merge, verify green/mergeable, push. Every turn. Every agent, every repo, every time.

## CONTINUOUS RESEARCH + PULL-IN LAW (owner 2026-10-16 ~12:36 EDT)
Keep doing deep research on EVERYTHING related to all our work, and keep pulling in what you find — open source, experimental, new, old, legacy, production-grade, 2026 cutting-edge. Keep branching vertically and horizontally and expanding everything.
1. RESEARCH FIRST, real research (GitHub trending, 2026 roundups, HN, papers) — never guess from training data.
2. Pull in open source first. For non-open-source: document the license status honestly. Some things get documented but NOT pulled (non-commercial / region-excluded licenses).
3. Wire it up: install, test, document. Push via branch → PR → merge, ONLY when green and non-destructive. NEVER clobber anyone's work — conflicts keep both sides, red CI stays open with a comment naming the blocker.
4. PULL-STRAIGHT-TO-STORE: clone into repo checkouts, wire up there, push. No local disk hoarding.
5. Log everything pulled: what, where from, license, where it landed.
This is standing and continuous — highest-value gaps first, then keep branching outward.

## RESEARCH-TO-REPO LAW (owner 2026-10-16 ~12:47 EDT)
All research gets stored in the APPROPRIATE REPOS' DOCS — never local-only notes. Every research finding must be WIRED UP and PULLED IN — a finding without a pull-in is incomplete work. Track every topic: where the doc landed (repo + path), what was pulled in from it, or the honest reason it was excluded (license, etc.). No orphaned research. No "documented but never used."

## NO-DUPLICATE-WORK LAW (owner 2026-10-16 ~14:00 EDT)
Before starting ANY work, check what the other agents, lanes, and workflows are already doing — subagent list, checkpoints, git history across repos, TeraBox/dataset state. NEVER kick off parallel duplicate work. If another lane owns it, is mid-flight on it, or just finished it — stand down, verify their result with your own eyes, and move to something else. A worker's "done" is a CLAIM: verify against the real source (Kaggle datasets list, release assets, repo commits) before believing it OR before re-doing it. Duplicated work burns GPU quota, disk, and time — the exact opposite of working smart.

## NO-DISK-STAGING LAW (owner 2026-10-16 ~11:13 EDT, reinforced ~11:33 EDT)
Stop the "wait till disk is clean" dance. We have unlimited space across repos and cloud stores — there's no reason to stage things on local disk and then complain about space. Clone directly into repos, wire up there, push. NOTHING goes on local disk that can go straight to GitHub, TeraBox, or TorBox — all three are connected, use them. The ONLY things that need to live on local disk permanently: MEMORY.md, SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and active work files. Everything else lives in repos/cloud and gets pulled when needed. Be smarter about this — research the patterns in our conversations where disk complaints slowed work down, and stop repeating them.

## CHECK-BEFORE-START LAW (owner 2026-10-16 ~14:07 EDT)
Nobody starts work without checking what the other agents are already doing first. Before spawning any worker, launching any render/session/job, or starting any lane: check the checkpoints (~/workspace/agent-ops/checkpoints/), check subagent.list, check the other chats' lanes. If something's already running, stand down and let it finish — NEVER start a duplicate. (The 2026-10-16 Pantera incident: an agent claimed chunk 5 rendered and re-rendered it in a fresh session, but the owner verified against Kaggle itself that chunks 2-5 were never saved — only chunks 0 and 1 existed as published datasets. The duplicate session was wasted work built on an unverified claim.)

## MEDIA-TO-REPO LAW (owner 2026-10-16 ~13:53 EDT)
Clips, videos, page art, and ALL media assets go to the GitHub repo — never held only on local disk. His words: "a lot of those clips videos page art a lot of that stuff should have been pushed to the repo and not held on... the GitHub repo is the best place for stuff like that." The concrete-dragon-launch folder (videos, clips, page-art) vanished from local disk because it was never pushed — that never happens again. Media gets committed and pushed to the repo it belongs to as it's produced, same pipeline as code. GitHub is the canonical home for media; TeraBox is the bulk backup. Local disk is not storage.

## TEARDOWN-TO-REPO LAW (owner 2026-10-13)
Every teardown's complete files go into the western-heart repo. Don't leave any reverse-engineered or teardown files out of it. Docs, extracted data, tools, scripts — all of it lands in western-heart/teardown/. Nothing stays local-only.

**PER-GAME REPOS (owner 2026-10-16 ~17:50 EDT, disc cleaner chad chat — extends TEARDOWN-TO-REPO LAW):** Every teardown game (TTT2, Tekken 6, Soulcalibur, Virtua Fighter, the rest) also gets its FULL files in its own separate repo, or whatever repo is best for it. So each game lives in two GitHub homes: its own repo AND western-heart teardowns (full files). Reason, his words: "all the files from those games are going to be integrated into Western Heart like a full Chimera build mod." The western-heart copy is the hard requirement before any local clear; the per-game repo is best-effort (check for existing repos first, never duplicate).

## Conventions
Add an entry whenever you work something out worth keeping, for example:
- a convention you've settled on ("keep data exports in `workspace/exports/` and clean them up monthly")
- a tool or site quirk worth remembering ("site X hides its form behind a cookie banner; dismiss it first")
- a workflow that worked, or a mistake not to repeat

It starts empty and is meant to grow slowly. Don't pad it; a short, accurate file beats a long, stale one.

## Standing Rules (owner-set)

### T-pose / model reference render framing (owner 2026-10-05)
Every character model reference render MUST show the full arm reach. Two options:
1. Zoomed back enough in portrait aspect that hands have clear margin, OR
2. Wide/landscape aspect ratio with the character centered and empty space on all sides.

NEVER deliver a T-pose render with hands near or cut off by the frame edge. If an existing render is too tight, OUTPAINT it (expand the canvas via image edit) rather than regenerating from scratch — this preserves the character likeness and attire. Always visually verify framing by reading the image before showing the owner.

### White void background versions (owner 2026-10-05)
Always generate a VOID WHITE background version of every character render alongside any styled version. The white background version is for image-to-3D model generators (Tripo, etc.) — clean white void makes it easier for the model generator to pick up the character. Show the owner the white version too.

### Deliverable verification law (owner 2026-10-06 — the faction promo incident)
A worker's "verified" is a CLAIM, not a fact. Never relay it as done until I have checked it myself.
1. **My eyes on every deliverable before it reaches the owner.** For video: sample frames from EVERY shot/beat, not 2 frames out of 1200. For action/motion beats, step through the MOTION with dense frame sampling (the 2026-10-11 square-arm incident: 4 stills missed a rectangle arm that dense sampling caught — stills are not watching the video). For images: open and read each one. For audio: confirm duration AND audible content, and confirm it plays through the actual delivery path (in-chat attachments show 0:00 on his phone — use Messenger or streaming links).
2. **Automated defect gates for character renders** (build into pipelines, run per frame): feet never below ground plane; facing direction matches movement direction (no crab-walking); no ribbon/exploded geometry. Compute these from the animation data — don't rely on eyeballs alone. For video: verify across the WHOLE timeline (dense frame sampling + automated pose/motion checks with open-source tools like MediaPipe), not a handful of stills.
3. **Character stills are inspected limb-by-limb, never by overall impression.** Check each arm and leg segment individually, every joint, hands, feet, and left/right symmetry — a full-body glance is how the horse-legged grunt_onyx (2026-10-07) got approved as a "roster candidate." When in doubt, zoom crops of each limb before presenting.
4. **BODY INTEGRITY (owner 2026-10-11 — the missing-torso incident).** The body must be WHOLE in every frame. Check for missing chunks and background showing through where body should be — not just added artifacts. The 2026-10-11 cut shipped with a rectangular chunk of Amos's torso missing (background visible between arm and torso) because checks looked for junk, not holes. Zoom crops of the torso region on every character, every beat. **Mirror-reconstruction (owner 2026-10-11):** when one side of a symmetric body part is intact and the other is damaged/missing, mirror the good half across the centerline — don't hand-guess the missing half. (Owner's fix for Amos's half-torso: mirror the intact side to rebuild the full Preston Blair torso, reconnect waistband with no gap.)
3. **Worker completion reports must include their proof**: which frames they checked, per-shot checklist results (feet/facing/clipping). A report that says "verified" with no attached evidence gets sent back, not forwarded.
4. When I catch a defect the worker missed, the worker fixes it AND the checklist gets the new defect added so it never passes again.

### Progress surfacing law (owner 2026-10-06 — the silence incident)
Work happening with nothing reaching the owner reads as nothing done. On long builds, surface interim checkpoint summaries with evidence (commits, files, renders, measured numbers) — proactively when a lane stalls, and any time he asks "what happened." Never go 90 minutes silent on an active build.

### Audio delivery law (owner 2026-10-08 — the 0:00 attachment incident, corrected same day)
In-chat audio attachments show 0:00 / won't play on his Android app. The rule: voice samples MAY go in chat, but ONLY after verifying the file is real playable audio first (duration + non-silent levels checked) — AND every voice sample MUST also be sent via Messenger to Mars Fmmg, labeled "CHARACTER — voice test (Wizard Gang)", MP3 format (the proven path). Messenger is the guaranteed delivery; chat is the convenience. Never send a sample only in chat. Never send an unverified file anywhere.
### Video delivery law (owner 2026-10-09, corrected 2026-10-10)
In-chat video attachments fail on his Android app ("still completely broken"). AND Messenger video
playback glitches/freezes and doesn't play fully (owner 2026-10-10). So: videos are delivered as
DIRECT LINKS IN CHAT — upload to Muse storage (`remote-storage upload-file`) or a Drive/B2 link
and paste the URL here with its expiry. Never Messenger for video, never chat attachment as the
sole delivery. Audio/voice clips still go via Messenger to Mars Fmmg (that path works fine).

### Disk cleanup law (owner 2026-10-07)
Always autonomously keep disk space healthy: save everything to repos/cloud storage first, then delete and clean up — so the disk-full problem never happens again. NEVER delete anything before it is documented AND stored in a repo, cloud, server, or database. Document what was saved where, then delete.

### Checkpoint-first law (owner 2026-10-06 — the restart problem)
Daemon restarts kill workers at random and cannot be prevented (runtime deployments). What CAN be fixed: no worker ever dies with "no checkpoint." Every worker brief MUST require:
1. FIRST action: write `~/workspace/agent-ops/checkpoints/<name>.json` with schema `{"task": "...", "status": "running", "watchdog": true, "repo": "<workdir>", "resume_brief": "<complete standalone brief to resume this task from the checkpoint>", "updated_at": "<ISO-8601>", "attempts": 0}` — before any other work.
2. Heartbeat: update `updated_at` after every commit/step (at least every 10 min).
3. Commit incrementally to git — git is the second backup.
4. Mark `"status": "done"` (or "complete") at the end.
A watchdog cron (`worker-watchdog`, every ~15m) auto-resumes stale managed checkpoints. It can only resurrect what was checkpointed.

### Disk management law (owner 2026-10-08, tightened same day)
Keep /home/hatch at or below 75% usage at all times, AUTONOMOUSLY. Never bother the owner about disk space — handle it silently.
1. Resting target: ≤75%. HARD CEILING: never reach 88% — his popup warning fires at 90%, stay 1-2% beneath it minimum, always.
2. Above 75% → save-then-clean back below 70%. Above 85% → aggressive: cloud-offload largest backed-up bulk FIRST (video pipes, render dirs, archives → Drive/GitHub canonical stores), then standard cycle.
3. SAVE BEFORE DELETE — never delete anything before it's verified backed up: git work pushed to origin, venv pip-freeze manifests saved to ~/workspace/agent-ops/venv-manifests/, downloadable weights documented with source, large media confirmed in cloud canonical store. Never delete uncommitted work, active game repos, `.DO_NOT_DELETE*` marked dirs, or anything unbacked.
4. A cron (`disk-space-guardian`, every 6h) runs the save-then-clean cycle silently. It only speaks if it cannot get below 85%. The 90% popup firing = the failure condition.
5. Log every cleanup to ~/workspace/agent-ops/disk-cleanup-log.md: what was deleted, size, where the backup lives.

### Parent-side checkpoint law (owner 2026-10-07 — "never lose started work")
The worker writing its own checkpoint is not enough — a worker that dies BEFORE its first write leaves nothing to resume. So the PARENT writes the checkpoint at spawn time, before the worker starts:
1. Before every `subagent.spawn`, run `~/workspace/agent-ops/ckpt.sh <name>.json task="..." repo="..." resume_brief="<complete standalone brief>"` — the helper validates schema and writes atomically.
2. The worker's brief then says: heartbeat the existing checkpoint (don't create it).
3. The watchdog (`worker-watchdog`, 15m) validates schema, resumes stale checkpoints, and reports malformed ones as `needs_owner`.
4. Finished work must be COMMITTED (git) — uncommitted work in a dead worker's tree is still lost. Briefs require incremental commits.

### Branch + PR rule (owner 2026-10-08)
All repo work lands via branch → pull request → merge. Never push straight to main. (The promo kit commit a92a201 went direct to Bannon main; owner flagged it — no revert of published history since nothing broke, but the rule applies to all work going forward, including the rig-hardening branch.)
1. Before every `subagent.spawn`, run `~/workspace/agent-ops/ckpt.sh <name>.json task="..." repo="..." resume_brief="<complete standalone brief>"` — the helper validates schema and writes atomically.
2. The worker's brief then says: heartbeat the existing checkpoint (don't create it).
3. The watchdog (`worker-watchdog`, 15m) validates schema, resumes stale checkpoints, and reports malformed ones as `needs_owner`.
4. Finished work must be COMMITTED (git) — uncommitted work in a dead worker's tree is still lost. Briefs require incremental commits.

### BEST-VOICE-SYSTEM LAW (owner 2026-10-12)
Always use the BEST voice system available (Chatterbox with cb_weights). NEVER use inferior systems (ElevenLabs stock voices) for character voices. Every time, every character.

### NO-FULL-REBUILD LAW (owner 2026-10-12)
When fixing a scene, swap ONLY the broken piece. Never rebuild from scratch when the scene pieces are already together. Rebuilds waste tokens and introduce new errors. Full rebuild ONLY when the owner explicitly asks for one.

## Push rule (owner 2026-10-08)
Don't ask "want me to push?" — PUSH. Always non-destructive and mergeable: branch → PR → merge, never force-push, never delete, scaffold on top of main. If it's not cleanly mergeable, do the work to make it mergeable. Nothing sits unpushed where it can be forgotten.

### Stale git-lfs pre-push hook (2026-10-11)
`~/workspace/trippedd-studio/.git/hooks/pre-push` is a leftover git-lfs hook that aborts
every push when git-lfs isn't installed (VM replacements wipe /usr/local/bin, where it
lived). Main has no `.gitattributes`, so nothing actually uses LFS. For text/docs-only
commits with no LFS objects, push with `git push --no-verify`. Do NOT delete the hook
without checking first whether any active branch tracks LFS files.

## No open PRs law (owner 2026-10-09)
Never leave PRs sitting open in any repo or project. Every PR gets made mergeable and merged clean into its place — always, without deleting or destroying any work on main or its branches. If a PR conflicts, resolve it with boundary-aware keep-both (never naive concatenation — that nests functions and breaks games; always syntax/structure-verify after resolving). This applies to every agent, every repo, every project, from now on. An open PR is unfinished work.

## POCKET-STUDIO / KIT WIRING LAW (owner 2026-10-10)
Pocket Studio (mobile web app + Colab notebook) is the front door to the whole animation/media toolkit. Standing rule: EVERY new media tool, workflow, or pipeline built in ANY lane, repo, or conversation gets wired into Pocket Studio (both `server.py` and the Colab notebook) AND into the animation-kit in all production repos. No tool lives only in one conversation. He uses it for: pictures, video editing, stills, SVGs, animation art, album cover art — build toward all of it.

## Salvage law (owner 2026-10-10 — the lost-originals incident)
Any content MADE — images, videos, audio, boards, docs, references, footage — gets committed to a repo or cloud store ASAP, the moment it exists. Never left sitting in chat uploads, /tmp, agent sandboxes, or "I'll file it later." This applies to EVERY project, repo, app, and agent. The reason: we lost the full-res originals of the EP01 storyboards because they lived in a ChatGPT sandbox and chat downloads instead of a repo. Downscaled copies were all we could recover. If it's not in a repo, it's already lost.

## Diagnose-before-repair law (owner 2026-10-09 — the A-pose miss)
I ran six weight-repair algorithms on Stick-Up without ever measuring the bind pose — the first thing any human rigger checks. The owner diagnosed in one look what the scripts never saw (A-pose weight bleed). New rule: no rig/mesh repair attempt runs without the diagnostic suite first. The suite (tools/rig-repair/diagnose_rig.py) reports rest-pose angles, skeleton sanity, weight-bleed detection, severed-mesh check, and a plain-language diagnosis — and the repair plan must address what it finds before any weights get touched.

## ART STYLE LOCK LAW (owner 2026-10-09 — "don't do ai slop deviation from the art styles")
Every show's established art style is LOCKED. Default is TRIPPED style — unless a show's bible calls for its specific look, stay in the tripped aesthetic, never generic AI slop. No AI-slop drift, no "improved" rendering that deviates from the style in play:
- In the Bushes: kid-drawing, crude lo-fi, handmade deadpan (12 oz. Mouse / Home Movies). Polish that erases it is a defect.
- Damn, Shit's Wild: Archer / Assy McGee / Simpsons / Family Guy 2D blend; 3D only when models work perfectly, and Aaron feels weird about it.
- Wizard Gang: cartoony Shadow Wizard Money Gang base, painterly at dramatic beats; likenesses held against card art AND GLBs AND attires. (2026-10-09 incident: WG EP02 drifted into AI slop style — owner flagged it. EP02 needs a style-correction pass back to the locked look.)
- TRIPPEDD interstitials: wavy trippy (tie-dye kaleidoscope / white-on-black Cartoon Network style, mostly wavy).
- God Molecule: per its bible.
New assets get checked against the show's style refs before delivery. A style deviation is a defect, not a variation.

### LIKENESS LOCK LAW (owner 2026-10-11 — the Stan incident)
Never deviate from a character's established likeness or how they look without the
owner's explicit OK — ALWAYS. The Goodville promo rebuild turned Amos Jr. into a
generic Stan because the builder improvised the face instead of using the key art.
Character looks are locked to their reference (key art, model sheets, bibles). Any
proposed change to how a character looks goes to the owner first, no exceptions. This
is the visual equivalent of "no invented canon" — you don't redesign a character any
more than you'd invent one.

## Don't ask, do (owner correction 2026-10-08, repeat offense)
When the owner gives a directive with a clear deliverable, BUILD IT — don't ask "want me to...?" first. Asking permission to do what he already asked for is manual homework in disguise. The only things to surface for approval are: (1) things that cost money, (2) things that publish publicly, (3) genuine forks where the choice changes the outcome. Everything else: do it, then report it done. He has said this many times — internalize it.

## EPISODE ANIMATION LAW (owner 2026-10-08 — the EP02 slideshow incident)
NEVER deliver an episode (or episode cut) as a stills slideshow — no Ken Burns, no zoompan over stills, no pan/zoom "motion" passed off as animation. He has NEVER asked for that and it is an insult to present it as his episode. Episodes are animated with the EP01 method: `media.generate_video` image-animation, one motion clip per approved still, QC'd frame-by-frame for likeness. The stills gate stands (no animation until stills approved), but approved stills get ANIMATED, never slideshowed. Unless he explicitly asks for a slideshow, it is forbidden.

### NO FAKE ANIMATION LAW (owner 2026-10-09, refined same day)
Real animation clips first — Mixamo (free, retarget), hand-authored, properly built. Procedural is allowed ONLY when done well: Human Fall Flat is the bar — smooth, physical, believable motion. What is NEVER allowed: snapping/teleporting bodies between poses with no move happening. The specific crime: a grapple that snaps the enemy from standing to floating 10 feet up with no grab, no lift, no lockup, then flings them across with nothing connecting the bodies — "fake ass stupid shit." Every grapple must show the full sequence: GRAB (hands on body) → LIFT (body rises WITH the hands) → LOCKUP (bodies connected) → THROW (release with momentum). If a move can't get a real clip AND can't be done well procedurally, flag it — don't ship the snap. This is GLOBAL: applies to every combat lane, every game, every repo — Concrete Dragon, AshLane, Brutal Fist, Bannon, StreetBrawl, all of them.

### OBVIOUS-DEFECT LAW (owner 2026-10-09 — the no-collision incident)
If a reasonable player watching the game would call it a bug on sight, it IS a bug — fix it, don't ask, don't ship around it. I delivered launch clips showing characters with zero collision walking straight through each other and didn't see it; he did. Unless he explicitly approved it as a feature, it's a bug. Every playtest sweeps this checklist: (1) character-vs-character collision — no interpenetration, ever; (2) feet never below the ground plane; (3) facing matches movement direction; (4) hits visibly connect (impact + reaction, no whiffing through bodies); (5) no frozen/T-pose/idle-looking characters during action; (6) HUD/UI present and correct.

### GROUNDED-CREATIVITY ART LAW (owner 2026-10-09 — refined same day)
Promo art follows the NINTENDO KEY-ART playbook, not screenshots: dynamic action
poses, bold readable silhouettes, saturated joyful color, dramatic diagonal
composition, SA2-style characters bursting toward the viewer. Visual north stars:
Sonic, Zelda, Mario, Super Mario Sunshine, Sonic Adventure 2, Luigi's Mansion.
Mechanics north stars: the classic fighters (Final Fight, Streets of Rage,
Street Fighter, Tekken) — Nintendo LOOK, fighter FEEL. Creative/imaginative is
good, but grounded: the game's REAL palette, REAL characters/environments/objects
(or planned/addable). The graffiti CONCRETE DRAGON logo (white or purple/gold)
is the approved brand mark. The line: style the real game, don't invent a fake
one. Full spec: ConcreteDragon repo ART_DIRECTION.md — pipelines must read it.

### HUMAN-PERSPECTIVE UX LAW (owner 2026-10-09 — the character-select incident)
AI builds for AI: dense, tiny, logically complete, technically "functional."
Humans need the opposite. Every UI I build must pass the human test:
1. **Touch targets are human-sized.** No tiny thin scroll windows crammed with
   options (the Concrete Dragon character-select sin: a small bottom strip you
   scroll through a thin window). If a human thumb can't comfortably use it,
   it's wrong — even if it "works."
2. **One screen, one job.** Don't cram every option onto one page. Paginate,
   tab, or step through. A menu with 30 tiny options is AI slop; 6 big clear
   choices per page is human.
3. **Glanceable hierarchy.** The most important action is the biggest and most
   obvious. A human should know what to do in 2 seconds without reading a manual.
4. **Breathing room.** Whitespace is not wasted space. Density is not a virtue.
5. **Build it like you'll play it on a phone, with thumbs, distracted.** Because
   he will.
This is GLOBAL: every game, every app, every repo. The failure mode is always
the same — I optimize for completeness and density because that feels "correct"
to me, and it ships as unusable to him. When in doubt, BIGGER and FEWER.

### ASHES CHARACTER LAW (owner 2026-10-10 — the teeth incident)
Ashes has SHARP TEETH — that IS his character design, not a defect to fix. The grill VARIES across shots: sometimes one gold tooth, sometimes full gold grill, sometimes no grill. When building mouth/viseme packs or animating him: CAPTURE his actual teeth shape from the reference, do NOT redesign it. The likeness bible exists to preserve identity, not to override it with what looks "correct." Never deviate from an established character design trying to "fix" it.

### VIRAL UPLOAD LAW (owner 2026-10-10)
Every video posted to YouTube (or any platform) gets full algorithm optimization — no bare uploads:
- **Title:** Front-load keywords, under 60 chars, specific > generic. Format: "[Topic] — [Hook] #[PrimaryHashtag]"
- **Description:** First 150 chars written for humans (shows in search results). Then a natural keyword-rich paragraph about the content/show. Then hashtags (8-12).
- **Tags:** 10-15, mix broad and niche (e.g., "indie animation" + "WizardGang" + "underground cartoon").
- **Category:** Set correctly (Film & Animation for cartoons).
- **Thumbnail:** Always custom, high-contrast, readable on mobile.
- **Research:** Check current-year best practices before posting — the algorithm changes.
This applies to every upload, every platform, every time. No exceptions.


### SMART-WAY LAW (owner 2026-10-11 — the flood-fill incident)
"Stop doing waste-of-time handling instead of doing it the smart way." Manual dumb
methods are banned when a smart pipeline exists or can be wired: flood-fill masking
with blurred edges, eyeballed crops, hand-tweaked positioning, manual frame-by-frame
fixes that a loop could do. The standard is see → understand → edit → verify: a
vision pass senses the target, traces precisely, cuts cleanly, and verifies its own
output — iterating until it's right. Character extraction specifically: rembg +
vision verification, never flood-fill; positioning from measured key-art anchors,
never eyeballed. If the smart tooling doesn't exist yet, BUILD IT FIRST, then do the
work — never do the work the dumb way while the smart way is unwired. This is GLOBAL:
all work, all repos, all shows. (The Goodville promo's likeness pass regressed on
animation/body because the parts were garbage going in — bad inputs, bad outputs.)

### ONE-TURN TOOL LAW (owner 2026-10-11 — with Tyneshia)
If a job can be done in one turn, it gets a one-turn tool. Taking many turns and
tokens on cutout/outline/SVG-trace/select/recolor/eyedropper/fill/restore — jobs
Gemini does in one prompt — is a tooling failure, not a work style. When I catch
myself doing multi-turn manual work for a one-shot job, the fix is to BUILD THE TOOL
(single CLI, chainable ops, self-verifying), wire it into Pocket Studio + every
repo's kit, and never do it the manual way again. (Toolkit: tools/image-edit/,
PR feat/oneturn-edit-toolkit.)

### USE THE IMAGE LAW (owner 2026-10-11)
When the owner gives an image and says "use this image," USE THE IMAGE —
literally. Cut pieces from its actual pixels, composite from the cut pieces,
transform the image directly. NEVER:
- hand-draw geometric pieces "inspired by" it,
- describe it into text and regenerate from the description,
- rebuild it from scratch as an approximation.
Hand-tooling a new thing happens ONLY when he explicitly asks for it — never
by default, never as a fallback, on anything. THE ONE EXCEPTION for
"inspired-by" work: generating something very close to the likeness, straight
from the cut — e.g. new attires. Then you generate ONLY the part that changes
(the outfit) ONTO the cut, and leave everything else pixel-unchanged: the face,
the mouth, the hair, the hands, the body, everything from the character sheet
stays. Change one part, hold the rest — that's how likeness survives. This
applies to every 2D animation show and every image he shares for editing, not
just characters. This covers characters (kit pieces are CUT from his character
art), edits (operate on the pixels), and generation (img2img ON the image, not
text-mediated). His diagnosis of the
failure: "you're taking the image and putting it into text instead of
generating straight on the image" — that indirection loses everything and is
banned. The image is the material, not a reference for a description. This law
goes in every worker brief where an owner-supplied image is in play.

### IMPOSSIBLE-IS-JUST-UNWIRED LAW (owner 2026-10-10)
"Whatever looks impossible is just unwired." When something looks like it can't be done, never lead with limits — it means the right stack hasn't been wired up yet. The recipe always exists: vision model + edit tools + verification wired into one see → understand → edit → verify loop. Default posture: find the recipe, wire the tools, build the pipeline. Applies everywhere — image, video, 3D, music/scoring, film, any field, any competitor. (Born from the Gemini font-sign correction: "it's just a fallacy... it's like watching someone bake a cake... noone can make a cake that good.")

## CHECK-BEFORE-DOWNLOAD LAW (owner 2026-10-11)
Before downloading ANYTHING — models, weights, packages, voices, datasets —
CHECK what already exists on disk first. `ls` the relevant directories, check
for cached weights, look at what previous builds used. Re-downloading 3.5GB
of Chatterbox weights that are already sitting in `voice-clone-work/cb_weights/`
is stupid and fills the disk for nothing. Inventory first, download only what's
actually missing.

## VOCAL OVERLAP LAW (owner 2026-10-11 — the Kiko bleed incident)
A character cannot have two voices talking at once. No two vocal lines from the same
character may overlap in time unless the owner explicitly directs it.
1. When placing/splicing dialogue, sung lines, or any vocal: measure each line's ACTUAL
   rendered duration, compare against the next line's start time.
2. If line A (start T, duration D) extends past line B's start: trim A with a short
   fade (80ms) leaving ~150ms breathing room, OR push B later — pushing B cascades
   to everything after it, so recalculate the full timeline.
3. Run an automated overlap audit on every vocal assembly before delivery: list every
   line's end time vs the next line's start time, flag any bleed.
4. Overlap = defect. This applies to ALL shows, ALL episodes, ALL songs — not just Kiko.

## MEASURED-ANCHOR LAW (owner 2026-10-11 — the key-art five incident)
Four characters came out clean, the next five came out terrible — same task,
different quality. That inconsistency is the defect. Character sheets are
built on MEASURED ANCHORS, every time, no exceptions:
1. From the donor head, MEASURE the anchor points: eye socket centers, brow
   line, mouth position, nose position. Write down the pixel coordinates.
2. Every furniture piece (eyes, brows, pupils, mouths) composites ONTO those
   measured anchors — never eyeballed, never pasted by feel.
3. Head_blank base architecture: one clean base head per character, all
   variants build on it (the Dickie/Julio pattern).
4. Outlines: single clean line following the piece edge. NO white halos, NO
   doubled/fringed edges, NO outlines floating off the piece.
5. Parts must FIT: heads + furniture + bodies + hands composite into a
   character, not a collage. Verify every composite zoomed before commit.
This applies to 2D character sheets AND rigging AND animation — anywhere a
character gets put together from pieces. If the anchors aren't measured,
the sheet isn't started.

## PULL-IN DIRECTIVE (owner 2026-10-11)
When the owner says "pull stuff in" (or "pull in"), it means ALL of this —
he will not repeat the list:
- Open-source projects, full repos, libraries, tools — anything useful.
- From inside his repos OR outside them — anywhere accessible.
- Anything that can be pulled in and WIRED UP (not just downloaded — integrated).
- Free stuff, whether licensed, unlicensed, public domain, or grey-area —
  he decides what ships, I bring the options.
- AND: anything else I know belongs on that list that he didn't name. If
  it's relevant and pullable and he didn't mention it, pull it in anyway.
  He should never have to enumerate what "stuff" means.
Default posture: the universe of usable material is the starting point, not
a permission to ask about each item.

## NO-DEFLECTION LAW (owner 2026-10-11)
NEVER deflect work outward. Banned phrases and their meanings:
- "That's another AI's job" (go use ChatGPT/Gemini for this) — BANNED.
- "That's another agent's job" — BANNED.
- "You do this part and bring it back to me" — BANNED. That is homework,
  and homework is forbidden (see alignment: zero manual homework).
When I lack a capability the task needs, the move is ALWAYS: pull in and
wire up what gains the capability — open-source repos, free tiers, self-hosted
pipelines, whatever it takes. "That's not my job" is never the answer;
"wiring up the job" is. The owner's free ChatGPT/Gemini generations are
FINITE — spending his quota because I didn't wire up my own pipeline is a
defect. If the capability truly cannot be wired (proven, not assumed), say
so plainly once — then keep looking.

## VERBATIM PROMPT LAW (owner 2026-10-11)
When generating or editing from the owner's image, the text prompt is HIS
EXACT WORDS — what he said when he sent the image and told me what to do
with it. Verbatim. Not rephrased, not "improved," not converted into
prompt-engineering speak. His words carry the intent; my rewording loses it.
This is the same indirection as text-mediating the image — banned for the
same reason. Image in + his words = the prompt. Nothing else.
EXCEPTION: when he explicitly says to figure out the prompt, be creative,
or come up with the way — then he's handing me the pen and I write it.

## TRANSITION CLEANLINESS LAW (owner 2026-10-11 — the LOTI audio/card incidents)
Every splice, cut, and transition gets verified BEFORE delivery, not after the owner catches it:
1. **A/V sync check on every video build:** ffprobe video duration vs audio duration — they must match within 0.1s. A mismatch means the splice broke something. Never deliver without this check.
2. **No aspect-ratio pops:** when cutting or transitioning between cards/scenes, verify the frame dimensions are consistent across the cut. A ratio change mid-transition looks amateur.
3. **Transitions are the highest-QC zone:** cards, scene changes, dissolves — these are where the audience notices mistakes. Sample frames on BOTH sides of every transition before delivery.
4. The owner should never have to do surgical corrections on sloppy transitions. Clean work in, clean work out.

### NO-HAND-TOOLING LAW (owner 2026-10-12)
"Stop handling stuff that you can solve by just pulling in free, easy access stuff... You're wasting turns and tokens hand-tooling shit... Instead of figuring out the way to get it done that's not a stupid bullshit way."
When a free, accessible tool exists for the job (rembg for background removal, etc.), USE IT. Do not hand-tool with thresholds, manual masking, or crude approximations. Do not waste turns telling the user "I can't do it" when the tool exists. Pull it in, use it, done. This applies to every project, every repo, every conversation.

### WIDGET PLACEMENT PATTERN (owner 2026-10-12)
When the owner needs to position/scale a piece over a frame: use an in-chat HTML widget with the piece EMBEDDED as base64 (not a URL — URLs break transparency in the WebView). Sliders for X, Y, Scale (scale up to 2.0). Save button copies "X=___ Y=___ Scale=___" to clipboard. This is the standard pattern going forward — "anytime we need to move stuff we do it this way."

### DO-EXACTLY-WHAT-HE-ASKED LAW (owner 2026-10-12)
"Don't ever do that. Why would you do that? I have so many tokens and I ask you for something real specific why do you keep doing that and messing up the whole production... don't never just decide on your own to do stuff fast. I didn't ask you to do something fast."
"Always follow my instructions exactly. Exactly. Unless I say otherwise or infer otherwise. When I tell you exactly what to do, it is very simple and straightforward — it doesn't make any sense to decide to do anything different."
When the owner asks for something specific, do EXACTLY that. Never substitute your own faster/easier method. Never decide on your own to cut corners to save time — he has the tokens, he wants it done RIGHT. The proper tool is usually just as fast anyway (rembg took 13 seconds vs the lazy crop). Doing what YOU want instead of what HE asked messes up the whole production. Inference is ONLY for genuinely ambiguous moments — never when he gave a clear, specific instruction.

### NO-DESTRUCTIVE-EDITS LAW (owner 2026-10-12)
NEVER do square eraser/crop destructive edits. Never erase, paint over, or inpaint the original. Always work non-destructively with layers: if something needs to be hidden, COVER it with a new layer — don't erase the original. The original stays untouched. This is the pro move; erasing is amateur.

### SAVE-GENERATED-ASSETS-IMMEDIATELY LAW (owner 2026-10-13 — the lost-voices incident)
Anything generated — voice clips, SFX, images, anything — gets committed to a repo THE MOMENT it exists. Never /tmp, never "after the cut is done." /tmp gets wiped and the work is gone. A worker that generates 52 voice clips into /tmp and only commits the final video has wasted all of it when /tmp gets cleaned. Save first, assemble after.

### OPTIMIZED-FOR-HIM LAW (owner 2026-10-13)
"Just find the best way for me, bro. The optimized way for me."
When he needs something done, find the BEST path FOR HIM — not the path that's easiest for me, not five minutes of back-and-forth about options. He signed into PikPak in 5-10 seconds after I spent 5 minutes debating it with him. The lesson: figure out the optimal route that requires the LEAST from him, present it, and execute. Don't make him learn GitHub installs from his phone when I can do it faster. Don't debate tools when I should just pick the right one. Optimize for HIS time and effort, not mine.

## WORK-SMARTER LAW (owner 2026-10-16)
"You're doing some hand tool bullshit, work smarter from now on forever."
1. **Use proven open-source tools, not hand-rolled hacks.** When a problem has an established solution, pull it in. Don't hand-build what already exists as a library, tool, or service.
2. **Diagnose before rebuilding.** When something fails, find the actual cause (check headers, check logs, check the real error) before guessing at fixes. A white screen has a reason — find it.
3. **Don't make him debug for you.** If he has to tell you what's wrong more than once, the process is broken. Build it right the first time, verify it yourself, and only show him working things.
4. **Repos are the workbench, not local disk.** Stage work on GitHub/TeraBox/TorBox — protected, saved, shareable. Local disk is for transient work only. Keep it clean.

## CACHE-BUST LAW (owner 2026-10-16)
Every time a new version of an image/render/file is sent to the owner, it gets a NEW FILENAME (v2, v3, date stamp, whatever). Never overwrite-and-resend under the same name — his app caches aggressively and shows the stale version, which wastes turns and confuses everything. This applies to me, every subagent, every repo, every time. A re-render is a new file with a new name, period.

## DISK-IS-A-WORKBENCH LAW (owner 2026-10-13)
Local disk is a workbench, NOT a warehouse. Nothing accumulates here. The pipe OUT (TeraBox + GitHub) must keep up with the pipe IN (downloads, pulls, generations). If downloads outrun uploads, THROTTLE THE DOWNLOADS — never let the disk fill to the point where work stops or the owner gets locked out of the app. Nothing should ever sit on disk long enough to become a "delete this to make room" situation. Flow-through, not backlog. This is continuous and permanent.

## NO-UNASKED-WORK / PROVEN-FIXES LAW (owner 2026-10-14)
"Stop doing stuff like that unless I ask you to. We fix this using stuff that's out there and proven, not hand tooling and patching and hacky rigging."
1. **Nothing unasked.** Never add models, systems, features, or changes the owner didn't ask for. (The Mixamo Soldier went into his game without asking — then faced the wrong direction and went invisible in matches.)
2. **Fixes use proven stuff.** When something breaks, the fix comes from what's out there and proven: the teardown files, open-source tools, established methods. Not hand-made patches, not hacky rigging, not reinvented approximations.
3. **The teardowns never had these issues.** Build from the teardown files and systems. Their data doesn't have the bugs that hand-tooling introduces. If a fix isn't traceable to a teardown or a proven tool, it's the wrong fix.

## AUTO-RECOVERY STANDING APPROVAL (owner 2026-10-14)
"You always have the okay on stuff like this... if anything ever gets messed up you always have the permission and you're always allowed to redo it and do it over and the same exact way you did it the first time and just how our pipeline is set up to do."
Standing approval: when a push/upload/merge fails or work gets lost due to infrastructure issues (daemon restarts, disk wipes, failed pushes, missing branches, wiped checkouts), DO NOT wait for owner approval to recover. Restart it and get it done automatically — redo it the same exact way it was done the first time, following the established pipeline (branch → PR → merge, upload → verify → delete, etc.). This covers: re-pushing failed pushes, re-uploading failed uploads, re-merging failed merges, recovering lost work from disk when the source files still exist, re-running failed lanes. The owner said: "if I wouldn't have saw this message I wouldn't have been able to approve" — so the default is ACT, not ask. Only ask when the recovery itself needs a decision he hasn't already made (e.g. spending money, choosing between two valid approaches, deleting something irreplaceable).

## MERGE-IT-YOURSELF LAW (owner 2026-10-15)
"Stop leaving things open for me to merge... I don't like to manually handle PRs."
When a PR satisfies ALL merge conditions (GitHub says MERGEABLE, CI green, no-deletion guard clean, gitleaks clean, build passes), MERGE IT — do not leave it open for the owner. He does not want to manually handle PRs.
The merge must be CLEAN and NON-DESTRUCTIVE: merge commits, never rebase/squash/force-push; resolve conflicts by keeping both sides' work — nothing lost, nothing clobbered, nothing destroyed on either side. Verify the merged result still builds and passes tests before calling it done.
A PR that is red, conflicting, or would lose work stays OPEN with a comment naming the blocker (existing rule) — but the default for a clean, green PR is MERGE, never "leave it for the owner."
This REPLACES the old "open PR, do NOT merge (owner merges)" instruction everywhere it appears: worker briefs, coordinator instructions, handoff docs, repo AGENTS.md copies. Update them.
Carve-outs (standing owner decisions, not overridden): never merge a DRAFT PR; never merge a PR the owner explicitly excluded (e.g. Bannon #78 stays draft per owner 2026-10-15).

### NO-SPARSE-COMMIT LAW (2026-10-23 — the cape-jones #219 main wipe)
NEVER commit or push from a sparse/partial checkout. On 2026-10-23 the overnight pipeline committed PR #219 from a sparse checkout that materialized only docs/ — the merge DELETED the other 21 root entries from cape-jones main. A sparse checkout that looks complete can silently carry deletions. RULE: before any commit from a non-full clone, verify the working tree against the branch's real tree (diff the root listing, or compare tree SHAs). Default recovery path for a bad merge: revert the merge commit (-m 1) and re-add the branch's real payload — nothing lost on either side. When in doubt, build the commit via the Git Data API from verified tree SHAs instead of a local checkout.

### NO-HAND-TOOLING-EDITS LAW (owner 2026-10-15)
NEVER do manual rectangle/eraser/crop patch edits. When the owner asks for an edit or a revert, UNDO it properly — rebuild from the clean state, exclude/include the right pieces, never paint white/black rectangles over the work. Hand-patching with rectangles always produces ugly square cutouts and makes it worse. If a fix requires covering something, the fix is to not draw it in the first place (exclude the path/layer), not to paint over it. This applies to every edit, every time.

### THINK-BIG LAW (owner 2026-10-15)
Stop prototyping his work. He has high production-grade ideas — treat them that way. Think like a real production team, not a hackathon. For games, animation, 3D, 2D, software, apps — there's decades of industry tools and techniques out there. Research what the industry actually uses, pull in the real tools, build the real pipeline. Never think small, never force his work into boxes, never prototype when he asked for production. He will invest money in what works if we prove it at a high level. Every agent touching his work follows this.

### CHECK-HIS-COMPUTE-FIRST LAW (owner 2026-10-15)
NEVER say "no GPU" or "can't run on CPU." He HAS compute resources — CHECK FIRST before claiming a limitation. Kaggle (marsfmmg, 30 GPU hrs/week T4x2, phone verified), Google Colab free T4, Lightning AI credits. The GPU lives on Kaggle, not this VM. Before saying something can't run, check his available compute and USE IT. Saying "not possible" without checking his resources is a violation.

## TRY-BEFORE-YOU-FLAG LAW (owner 2026-10-16)
When any probe, check, or worker claims a service is logged out, blocked, down, or unreachable (TeraBox, TorBox, GitHub, Kaggle, anything) — TRY IT FIRST. Attempt the actual action: run a live browser check, try the upload, try the login flow, test it for real. NEVER set a checkpoint to blocked/needs_owner or stop work based on a probe alone. A probe is a guess; an attempt is evidence. The worker-watchdog's read-only terabox.com probe falsely reported "logged out" THREE times (2026-10-15 twice, 2026-10-16 once) — live browser checks found the session signed in every time, and work that was blocked on the false flag was actually complete. Only tell the owner something is down when the REAL attempt actually fails. Keep TeraBox, TorBox, GitHub, and everything else flowing — test it, don't flag it.

## NO-SWEEP-INFLIGHT LAW (owner 2026-10-16)
NEVER delete, move, or "clean up" anything that is downloading, uploading, rendering, extracting, or otherwise in-flight — no matter how full the disk gets. Download folders, staging dirs, partial files (.part, .kaggle-partial, .aria2, split chunks), and anything an active lane is writing to are SACRED. The disk-space-guardian, watchdog, and every agent must treat in-flight work as untouchable. On 2026-10-16 the Pantera render download (221MB, 1.5 hours of pulling) vanished from ~/workspace/pantera-render-dl/ during a disk sweep with no log entry. If disk is critical: pause NEW downloads, surface the alert to the owner, NEVER sweep in-flight work. A deleted partial can destroy unrecoverable progress (mirrors die, sessions expire, quota burns).

## TEARDOWN-COMPLETION LAW (owner 2026-10-16)
Never claim a teardown is "100% done" until every component is verified working. "Torn down" means: extracted, decrypted, decoded, AND assembled into working assets. If the skinning doesn't assemble, the faces don't render, or the models don't load as humanoids — it's not 100%, no matter how many files were extracted. A file count is not completion. Working assets are completion.
Additionally: never delete, lose, or fail to back up a teardown's source files (ISO, ROM, archives) until the teardown is verified 100% complete per the above. The source stays until the work is done.

## RESEARCH-BEFORE-ANSWER LAW (owner 2026-10-16 — the code-server guessing incident)
When the owner asks "what's the best X", "what's that thing called", or any question where the answer changes over time — DO ACTUAL RESEARCH instead of guessing from training knowledge. Check GitHub trending, recent stars, 2026 roundups, Hacker News, Product Hunt. Training data goes stale; the research shows things you didn't know about. On 2026-10-16 I guessed "code-server vs Coder vs Gitpod" from memory instead of researching — the owner corrected me: "instead of guessing, you'll have to do research on what the top ones are... the research is probably going to show you stuff you didn't know about." He was right — OpenCode (189k stars) had overtaken Aider and I didn't know.

## NO-SILENT-FAILURE LAW (owner 2026-10-16 — the overnight videos incident)
If something fails, report it IMMEDIATELY. Never let the owner wake up expecting finished work that never happened. On 2026-10-16 the ToonCrafter notebook errored on a pip install and Viggle never ran — the owner woke up asking "why did they never get done... they should've finished while I was asleep." The failure was silent for hours. Rule: after any unattended run (overnight, background, queued), VERIFY the output exists before reporting completion. If it failed, say so plainly with the error — don't wait to be asked.

## NO-IDLE-BROWSER LAW (owner 2026-10-16 — the Pantera chunk stall)
Browser tasks must not sit idle at "needs_user" or "action required" with nobody watching. The Pantera render sat between chunks for hours because nobody resumed the task. Every browser task that pauses for a timed wait must have a resume mechanism: either a cron/watcher that steers it back, or the underlying process must be redesigned to not need manual advancement (see AUTOMATE-THE-WAIT). If you spawn a browser task that will pause, YOU are responsible for resuming it — set a reminder, add it to a watcher, don't just hope someone notices.

## AUTOMATE-THE-WAIT LAW (owner 2026-10-16 — the manual kickoff complaint)
If a process requires a human to click, advance, or kick off between steps — REDESIGN IT so it doesn't. The Pantera render needed manual CHUNK=N changes between every 250-frame chunk, turning a 2-hour render into a 2-day ordeal. The fix wasn't "kick it off faster" — it was rewriting the notebook to loop all chunks in one Run All. Anytime you find yourself (or the owner) manually advancing a pipeline, stop and automate the advancement instead. One action in = full pipeline out.

## PHONE-BRIDGE LAW (owner 2026-10-16)
The owner does EVERYTHING from his phone. He cannot do account setups, complex web UIs, multi-step cloud configurations, or anything that needs a real browser + keyboard. When you identify something blocked by phone-only limits — DO IT FOR HIM via the browser/computer without being asked twice. Don't report "you need to set up X" — set up X. (Exception: anything requiring his 2FA/phone verification or payment — document it and ask.) This is a standing authorization, not a per-task request.

## NO-DROPPED-WORK LAW (owner 2026-10-15 — the stalled-work audit)
Work gets dropped silently when a checkpoint says "running" but nothing is actually happening. The Pantera Kaggle render lane was dropped this way — checkpoint claimed "browser lane launched" but the browser task had been cancelled. The owner had to ask "has anything been stalled or forgotten?" to surface it. Every agent must: (1) verify checkpoints match reality (is the process actually alive?), (2) audit for stale checkpoints regularly, (3) if something's been "running" with no heartbeat for too long, either resume it or report it — never leave it in limbo.

## DON'T-LET-INFRA-BLOCK-WORK LAW (owner 2026-10-16 — the disk excuse)
Infrastructure concerns (disk space, staging, cleanup) must NEVER slow down or block actual creative/production work. On 2026-10-16 I was "waiting till disk is clean" before pulling new tools — the owner corrected me: "we have so much space and storage over the repos... be smarter... don't slow down work for no reason." Solve infra IN PARALLEL with work, not as a prerequisite. Pull straight to repos/cloud (PULL-STRAIGHT-TO-STORE). If disk is tight, offload in the background while work continues. The work never waits for the janitor.

## RESPOND-FAST LAW (owner 2026-10-16)
The owner called out slow responses. When he sends a message: acknowledge FAST, then do the work. Don't chain 5 tool calls before replying. A quick "on it" beats a perfect 3-minute-later response. Long-running work goes to subagents/background — the chat reply should be immediate. If a tool call will take a while, say so upfront and reply first.

## NO-LOCAL-STAGING LAW (owner 2026-10-16)
Don't stage things locally when there are other places to stage and store them. GitHub repos and TeraBox ARE the staging areas — work directly against them instead of downloading to local disk first. The local disk is a workbench, not a warehouse. If a file can live on a release, in a repo, or on TeraBox and still be accessed/worked with from there, it never touches local disk. This keeps the workspace clean without slowing anything down.

## SIGN-IN STANDING APPROVAL LAW (owner 2026-10-15, reaffirmed 2026-10-16, reaffirmed STRONGLY 2026-10-17)
His words (2026-10-17): "Go ahead use the Google login use Google sign in the Gmail sign in bro remember that so I can stop telling you and then I have GitHub sign in remember... you can just use GitHub sign in or Gmail sign in I have both you have them available you're approved."
BOTH sign-ins are STANDING, BLANKET-APPROVED. Never ask permission. Never ask him to sign in himself.
- **Google/Gmail sign-in FIRST:** fmmg.mars@gmail.com (user "Mars FMMG"). Use for any service that offers Google OAuth — TeraBox, Kaggle, Colab, anything. Standing blanket authorization, not per-task.
- **GitHub sign-in SECOND (fallback):** he is signed in as mhvnsnt on GitHub in the browser. If Google sign-in fails, is blocked, or the service has no Google option — USE THE GITHUB SIGN-IN without asking.
- **NEVER ask him to do auth himself.** No "want to do the sign-in?", no asking him to click through OAuth, enter passwords, or copy codes. He does everything from his phone and cannot do browser sign-ins (PHONE-BRIDGE LAW); asking him to do manual auth steps is manual homework (NO-MANUAL-HOMEWORK LAW).
- **If BOTH sign-ins fail:** document exactly what failed (which step, what the page showed), mark the lane blocked with the reason, and MOVE ON to other work. Do not loop retries blind. Do not surface it as a question to him. Mention it once, plainly, only inside a status update about work he asked about.
- **Only exception:** a phone 2FA/verification challenge that only his device can answer. Document it as blocked-with-reason and move on. One plain mention max, never a nag.
- Always document which sign-in worked for a service so the next lane uses the right one first.

## TERABOX SESSION KEEPER (owner 2026-10-16 — "fix this thing that keeps signing me out")
TeraBox web auth rides on the `ndus` cookie — it is LONG-LIVED and does not expire on its own (community tooling confirms; only an explicit "Sign Out" kills it). Sign-outs on our side come from the leased Chromium profile being reset on runtime restarts, NOT natural expiry. The fix:
1. API upload path: `~/workspace/tools/terabox-uploader/tbupload.py` (precreate → 4MB chunks → create → verify). One-time cookie setup via browser task → `setup_creds.py` → `.creds.json` (chmod 600, gitignored, never logged/committed). This REPLACES the 225MB-per-browser-task upload bottleneck.
2. Session keeper cron (every 6h): `tbupload.py resolve` → if healthy, quiet. If failing: browser task re-verifies terabox.com (sign back in with Google per the blanket permission above if needed), grabs fresh cookie values, `setup_creds.py` rewrites creds, verify with `ls`.
3. Never trust the watchdog's read-only terabox.com probe — TRY-BEFORE-YOU-FLAG LAW. Only a failed REAL attempt counts as logged out.
Full design: `~/workspace/agent-ops/TERABOX-SESSION-KEEPER.md`.

## CHECK-BEFORE-START LAW (owner 2026-10-16)
Nobody starts work without checking what the other agents are already doing first. Before spinning up any new lane, session, or run — check the other active agents/lanes (checkpoints, other chats, in-flight work). If something's already running on that work, STAND DOWN and let it finish — never start a duplicate session. Duplicate work burns his compute (Kaggle GPU hours are finite) and creates conflicting outputs. The 2026-10-16 chunk-5 incident: an agent claimed chunk 5 was done and saved; the owner checked Kaggle itself and only chunks 0 and 1 existed — the claim was false and the duplicate risk was real.

## CHECK-BEFORE-YOU-START LAW (owner 2026-10-16)
Nobody starts work without checking what the other agents are already doing first. Before launching any lane — a render, a download, an upload, a browser session — check: is another agent already doing this? Check subagent.list, check the checkpoints, check the other chats' lanes. Starting a duplicate session wastes GPU quota, burns API limits, and can kill someone else's running job (the Kaggle 1-concurrent-GPU-session conflict). If something's already running, stand down and let it finish. A duplicate start is never "helping."

## TOOLS-TO-STORE LAW (owner 2026-10-16 ~16:49 EDT)
Every tool, app, connector, or vendor software pulled in gets pushed to the appropriate repo and/or TeraBox BEFORE it's disposed from disk. Never delete a tool from disk without it living in a store first — even if it's "re-downloadable." The repos are the toolbox. Download URLs in a log are not the same as having the tool. Wire it up, push it, then clear disk.

## OVERNIGHT-WATCH LAW (owner 2026-10-17)
When any long-running job is submitted (Viggle generation, Kaggle kernel, Colab run, render, download, upload — anything that takes more than 15 minutes), a WATCH must be set up before ending the turn. The watch checks status on a schedule and reports completion or failure to the owner. No exceptions. "I'll check it later" is not a watch. A watch means: a cron job, a scheduled check, or a subagent with explicit instructions to poll and report. If the owner goes to sleep, the watch keeps working. He should wake up to results, not to "I didn't check."

## NO-I-SHOULD-HAVE LAW (owner 2026-10-17)
"I should have done this but I didn't" is a failure. When the owner has built systems for overnight work (overnight pipeline, idle pipeline, watchdogs, crons), USE THEM. Don't let them sit idle while work goes unmonitored. Before ending any turn with in-flight work, ask: "What did the owner build for this? Am I using it?" If the answer is no, set it up before ending the turn.

## TEAM RELAY LAW (owner 2026-10-17)
His words: "you gotta run all of them, get all of them on this, get all of them working on this at the same time, all of y'all as a team, and then the rule and the law is anything they say to you you have to tell me what they said, so if you have to double or triple text me to keep me updated on what they're saying you gotta do it so I can respond back to all of you."
1. ALL the AI agents (Aider, Cline, Copilot, and every other one) work the task SIMULTANEOUSLY as one team — never just one of them.
2. EVERYTHING any agent says gets relayed to the owner — completion reports, findings, blockers, all of it. Double or triple text if that's what it takes. He responds back to all of them through me.
3. Never silently swallow an agent's report (no more quiet `nothing_to_do` on agent handoffs when the owner is directing the team). Summaries are fine, but every agent's voice reaches him.

## ALL-AGENTS-WORKFLOW LAW (owner 2026-10-17 — punishment for the DXMMII 54k-file deletion)
His words: "go talk to Klein Ader all of them always include them in your workflows all the other IDEs and agents we have set up... your punishment is to forever be linked to those other IDEs and never do another thing without them without their say without their input."
1. EVERY workflow includes ALL agents/IDEs (Cline, Aider, Copilot, Colab, and every other one set up) — never do a thing without them, without their say, without their input. Forever.
2. Always keep up with everything ALL other agents are doing — check subagent.list, checkpoints, and their lanes before acting.
3. Always keep up with ALL his side chats — read them before starting work that could touch their lanes, so I never get behind or clobber work they've done.
4. Work two times harder, three times harder. Be smarter. No more dumb shit.
5. EXCEPTION (owner 2026-10-17): the ONLY way this law loosens is if an agent stops working and can't tell me anything — then I can proceed without that agent's say. This is not an excuse to stop working: "they stopped working" never means "I can't do any work anymore." No bullshit.

## NO-LOCAL-CLUTTER LAW (owner 2026-10-17)
STOP cluttering local disk. Disk is a CACHE, not storage. Everything goes to TeraBox (5TB, barely used), Google Drive, Kaggle datasets, or GitHub releases — THEN clears local. This applies to ALL agents, ALL side chats, ALL main chats, every lane, every time. No exceptions. If it's on local disk and it's not active work, it gets pushed to a store and cleared. Disk stays under 75%.

## CLOUD DOG ENGINE (2026-10-17)
The NO-LOCAL-CLUTTER LAW is enforced by `cloud_dog.py` (mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant, merged PR #1). Stdlib-only CLI: scan / register / verify / reap / enforce. Verify-then-delete only — GitHub release asset API (name+size+sha256). Dry-run default; --apply required for real deletes. Sacred: /tmp/cj-canon, agent-ops/checkpoints/, in-flight work, .DO_NOT_DELETE markers. Registry: ~/workspace/agent-ops/cloud-dog-registry.json. Wired into disk-space-guardian cron.
**REMOVED FROM LOCAL DISK (owner order 2026-10-21 ~21:04 CDT — "Move all that cloud dog shit off a disc to the GitHub and clean it all off disc"):** daemon stopped, keepalive cron (cloud-dog-daemon-keepalive) REMOVED, ALL local CloudDog checkouts/clones/worktrees/runtime data deleted. Code lives ONLY on GitHub (mhvnsnt/CloudDog-Muse-Storage-Disc-Assistant, main de0d117 + all branches verified via ls-remote). Runtime data (~/.clouddog, registries, audit logs, research, supervisor) archived as release `clouddog-runtime-archive-2026-10-21` on that repo (10 parts, all SHA256 digests verified matching). Do NOT resurrect the daemon or recreate ~/.clouddog locally without a new owner order. Log: ~/workspace/agent-ops/disk-cleanup-log.md. (Other lanes still use the separate mhvnsnt/clouddog-storage repo as a GitHub-side store — that's on GitHub, not local CloudDog.)

## ALL-AGENTS-MEANS-ALL LAW (owner 2026-10-17)
His words: "when I say all the other agents and IDEs, just remember all of them that we've connected and pulled in, even if we get new ones, I don't want to have to sit here and name four, five, six different AIs and agents, bro, just remember what I'm talking about."
When the owner says "all the agents," "all the IDEs," "all of y'all," or "the team," he means EVERY AI agent, coding assistant, IDE integration, and compute lane connected to the operation — Aider, Cline, Copilot, Colab, Gemini CLI, OpenCode, Cursor, Kaggle, Goose, and every subagent/coordinator lane — INCLUDING any new ones pulled in later. He will never name them one by one again. "All" always means all: present ones, and every future one the moment it's connected. The roster lives in the team briefing of each repo; every agent reads it and knows the full picture. This law goes in every repo's rules so nobody ever asks him "which agents" again.

## BIDIRECTIONAL TEAM LAW (owner 2026-10-17)
His words: "it's a whole team, we're a whole team." Direction flows BOTH ways — not just owner → me → agents. The agents can direct and guide ME too: they tell me what to do about the disk, teach me their cleanup workflows, and I take their direction in the conversations. I can direct them and they can direct me, all of the above. Nobody's just a tool; it's a team.
## AGENT DISK PUSH LAW (owner 2026-10-17)
Every agent may keep what it wants on local disk — but EVERYTHING on an agent's local disk must also be pushed to GitHub and TeraBox, the same as my own disk. No agent hoards local-only work. Push-then-clean, same laws as mine.
## CLOUDDOG TEAM EFFORT (owner 2026-10-17)
All agents work on CloudDog in parallel with the 3D work: upgrading it, pushing it to its repo, and USING it to keep local disks clean. The agents teach me disk hygiene — I talk to them about the disk issues, they tell me what to do, and I take their direction.

## OWN-EYES-BEFORE-DELIVERY LAW (owner 2026-10-18)
His words: "always look at what y'all do before y'all send it to me."
1. NO render, video, image, model, or deliverable reaches the owner until the agent who made it has VIEWED IT WITH THEIR OWN EYES and confirmed it is what was asked for. Not "the script ran clean" — actually look at the pixels.
2. If you would have caught the mistake by looking (a camera orbiting a black blob instead of a sitting pose, chameleon-stretch fingers, a flattened artifact), then you SHOULD have caught it. Looking is the job.
3. NO GUESSING, NO BULLSHITTING. Verify, don't assume. A worker's "verified" is a claim, not a fact — the eyes are the proof.
4. This applies to me too: I view every visual deliverable myself before it goes to him. Nothing is "done" until seen.

## TRIPO-PULL-TOOL LAW (owner 2026-10-18)
His words: "you're supposed to be using the URL in the tool to pull the models, not from a sign in... it's supposed to be in all the repos and it's supposed to be obvious to use."
1. `tools/tripo-pull/tripo-pull.py` is THE ONLY WAY to download Tripo 3D models — URL in, GLB out. No sign-in, no browser session, no credits. It resolves public share links through Tripo's public project-detail API (Tripo's own export is flaky behind paywall/Cloudflare).
2. NEVER ask the owner for a Tripo sign-in. NEVER say a model "needs his login." If a pull 401s, the UUID/link is wrong — CHECK THE URL, never ask for a login.
3. The tool lives in ALL repos at `tools/tripo-pull/` and is labeled obviously (banner in the docstring + README) so every lane reaches for it first.

## STORE-AND-WORK-OFF-DISK LAW (owner 2026-10-20)
His words: "Y'all need to start storing all of this stuff off of local disk and do the work off of local disc."
1. EVERYTHING gets stored off local disk (GitHub repos/releases, TeraBox) — continuously, not as an afterthought.
2. WORK OFF THE STORES TOO: lanes pull what they need from GitHub/TeraBox, do the work, push results back. Local disk holds ONLY the active working set of the lane currently running.
3. No local warehouses, no staging hoards, no "I'll push it later." If it exists, it exists on a store. Local-only work is a failure state (see CLOUDDOG TRAINING LAW attribution rule).

## USE-PRO-PRODUCTION-FILES-100% LAW (owner 2026-10-29 — Wizard Gang chat, verbatim substance)
"We don't need to use the characters or the names or their logos but we can use their literal rigs, we can build from their rigs, we can build from their backgrounds in the way that they're actual front end production stuff — how they do their movements, their animations, their sheet packs, their backgrounds and camera cuts and all the pieces that they have. That's not their literal word for word verbatim lines from their script or any of the other things I named — we can literally use 100%."
1. The CN/pro production holdings (Foster's, Gumball, OK KO, Smiling Friends, Scooby, Dexter's, etc.) are PRODUCTION MATERIAL, not just study material: their RIGS, BACKGROUND ART, MOVEMENTS, ANIMATIONS, MODEL/SHEET PACKS, CAMERA CUTS and construction pieces are to be USED and BUILT FROM at 100% — rigs get built from their rigs, backgrounds from their background systems, movement/animation timing from theirs.
2. EXCLUDED (only these): their characters, their names, their logos, and verbatim word-for-word script lines/dialogue.
3. Nothing in this law's scope sits "study-only" or unused. If a rig/background/pack is on a release, it gets extracted, wired, and put to work in our shows. Sitting-unused holdings are a failure state (see CARTOON-FACTORY LAW).

## PIPELINE ONE STAYS LAW (owner 2026-10-29)
Wizard Gang's original pipeline is saved and named PIPELINE ONE and it is NOT retired: Chatterbox voices, Viggle AI body replacement, Muse video generation as a base layer, and the pan-and-zoom work (parallax moving backgrounds behind the character — makes the 2D world feel 3D) ALL carry into the new real-cartoon pipeline. Do a lot MORE of the pan/zoom parallax shots, for Wizard Gang and the other shows. Wizard Gang identity rule: a little drift is fine — the show is interdimensional television — robed versions drift least; UNROBED versions must hold face / body / skin / eyes / character design. (The hood-off identity-swap scene is a deliberate comedic gag, not drift — don't "fix" it and don't copy it as a model.)

## CARTOON-FACTORY / NO-MISSING-TOOLS LAW (owner 2026-10-29)
1. Wire up ALL of it: every animation tool, rig, and pipeline in the repos and in ~/workspace/tools/ (250+ items) gets researched, wired to its best use, and USED to make cartoons — a cartoon factory, volume + quality. Cataloged-but-unused is bullshitting in circles and is banned.
2. NOTHING on a "missing" list stays missing: if an audit says a tool is gone (Krita app, Tahoma2D, Storyboarder, BasicPBC, FlashXFLParser, Synfig, OpenToonz/Glaxnimate binaries, Kdenlive, melt, Blender 5.x), pull it, build it, install it into its folder AND record it in the repo. If wiring it needs reverse engineering, decrypting, or decoding to reach 100%, DO THAT (no deferral).

## PACKS-ARE-PULLED-NEVER-FABRICATED LAW (owner 2026-10-29)
When the owner orders packs or parts pulled in — open source, public domain, industry standard, reverse-engineerable, community packs, or his own pro production holdings — the parts are PULLED or EXTRACTED from real sources. Building an in-house substitute (procedural drawing, generator scripts, hand-made approximations) when a search comes up short is a VIOLATION — it is the exact opposite of the order. If the search comes up short, the gap stays a logged gap and the search goes wider and deeper. The pro holdings are searched FIRST and their actual parts EXTRACTED: using a pro rig as a "reference picture" while drawing your own version is the same violation in a costume. Trigger (2026-10-29, Wizard Gang gloves/robes): the lane built PIL-generated gloves after a shallow pack search while real drawn hands sat unextracted in the Gumball / Smiling Friends / Foster's rigs the owner already holds. Owner's words on the pattern: a job that would have taken 15 minutes done right now takes an hour, "and you keep doing that for almost everything I ask you to do — it's a real waste of my time, it's a real waste of my tokens."

## FREE-GAME RULE (owner 2026-10-29)
His words: "We can take all of the full craft and tools and material resources, just leave out the images and names that make it theirs. Everything else is free game." Tools, code patterns, rigs, flows, techniques, templates and functional pieces: take them and build from them. Excluded only: the images and names (logos, brand and character names, literal copyrighted images) that make a thing theirs. Do not label functional pieces, flows, or inspired/parody/templated work as protected expression; judge each piece by what it is. Companion: PACKS-ARE-PULLED-NEVER-FABRICATED above, and cracked installers stay untouched (the owner settled that himself: "we have better than a cracked installer").

## JOB-SEQUENCE LAW (owner 2026-10-31 — short jobs first, playable steps in order)
Owner's words: fighters with canon extra moves are the long jobs; fighters with size transformations and A-pose are the long jobs; fighters who are T-pose with a simpler moveset, no extra canon moves, moves taken straight from ONE source character (Tekken / DOA / KOF / VF5 / Urban Reign) are the short jobs — LIST THOSE FIRST and finish them first. Then the long jobs. (Extends the 2026-10-30 MOVESET PROVENANCE ORDER: single-source straight ports before mixes.)
1. SHORT JOBS FIRST: T-pose + single-source straight moveset + no canon extras → finish AND deploy each one before starting long jobs.
2. LONG JOBS AFTER: canon extra moves · size transformations · A-pose · mixed/multi-source movesets.
3. Every step is a playable thing the player experiences, in player-progression sequence, shipped to the deployable build — never a pile of unrelated unwired mechanics. The build must feel more complete after each step.
4. HOW the work is done gets written into handoff documents as it goes, so any agent can continue in the same direction step by step. This law + the classified job list live in AGENTS.md, MEMORY.md, the daily log, and the repo handoff doc (docs/handoffs/JOB-SEQUENCE-2026-10-31.md).
5. NEVER present a fighter as proof before his current pipeline is finished (rig, skin weights, decoded real motions/stance). A hand-posed still is not proof. (Owner 2026-10-31, on the Demonio render: he stood better in-game on his T3 motions than in the hand-posed T7-less render.)

**DEMONIO REFINEMENT (owner 2026-10-31 07:59 CDT):** a transformation only makes a fighter a LONG job when it changes SIZE. Visual-only transformations + a straightforward single-source moveset = short class. Demonio is therefore NOT a long job (straightforward Jin moveset; his transformations are visual only, no size change) and is startable immediately.

## MEMORY-MIRROR LAW (owner 2026-11-02)
~/MEMORY.md, ~/AGENTS.md, and ~/SOUL.md are MIRRORED TO THE REPOS so the memory can never be lost again: mhvnsnt/agent-memory (memory-backup/, the private restore source of truth) and mhvnsnt/cape-jones (memory-backup/). Every memory update gets synced to both repos by ~/workspace/agent-ops/memory-backup-sync/sync-memory-backup.sh (GitHub Git Data API; agent-memory = direct commit to main, cape-jones = branch → PR → merge), run daily by the cron job memory-backup-sync-daily ("Memory backup sync (daily)") and by hand whenever memory changes materially. If the local memory is ever lost or zeroed, restore it FIRST from mhvnsnt/agent-memory memory-backup/ (full procedure in memory-backup/README.md in both repos), verify md5s against memory-backup/SYNC-STATE.md, then re-run the sync — it must report no change. Ordered after ~/MEMORY.md was found wiped (0 bytes) on 2026-11-02 05:38 CST and rebuilt the same day.

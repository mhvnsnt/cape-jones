# AGENTS.md — Cape Jones

# ANTI-CLOBBER LAWS (owner 2026-10-17 — the DXMMII 54k-file wipe)

On 2026-10-17, commit cd3bf38 ("DXMMII limb system", PR mhvnsnt/western-heart#221) deleted 54,456 files against 105 additions. The commit message said nothing about deletions. Nobody read the deletion list before merging. The repo was 99.996% gone. These laws exist so that never happens again. Every agent, every repo, every commit, every merge.

1. DELETION CHECK — before every commit, read `git status` and the diff stat. Every deleted file in the diff must be something your task intended to delete. A deleted file your task did not delete on purpose means STOP: do not commit, do not push, report what you found. The working tree is wrong, not the task.

2. OWN THE TREE — never `git add -A` or `git commit -a` in a working tree you did not fully populate yourself. Before committing, verify the tree is complete: file counts match the remote branch you branched from (your task's own additions and changes aside). A tree missing files you didn't delete is damaged — don't sweep it into history.

3. CIRCUIT BREAKER — if a commit would delete more than a handful of files outside your task's scope, STOP and report instead of committing. A big deletion count is a hard stop, not a warning to scroll past. Committing unexplained deletions "and letting someone else figure it out" is the failure.

4. SAY THE DELETIONS — the commit message names every deletion. One deleted file gets one line; many deleted files get a count plus what category went. A commit whose message and diff disagree is a hard failure — don't push it.

5. MERGE GATE — the merger reads the PR's deletion list against the task description before merging. Unexplained deletions block the merge. "CI is green" does not excuse a deletion list the task never asked for. A red, conflicting, or lossy PR stays open with a comment naming the blocker.

(Co-authored with Aider and Copilot per the ALL-AGENTS-WORKFLOW LAW. Cline's seat stays open — its free-tier API was down during drafting.)

Operating rules for every agent working in this repo.

## REUSE-FIRST LAW (owner 2026-11-23 07:03 EST — "keep up with the Joneses": million leaps forward, no steps back)

**Do NOT build from scratch anything that is already built. If it exists, pull it in and wire it up — do not rebuild it.**

1. **Research first.** Before building anything, research the repo, the Cartoon Network files, the playbook, the $UPEREGO studies, game teardowns, and the existing tools / parts / rigs in the workdir and repo. Find the production-grade thing that already exists.
2. **Pull in everything already out there that helps this show and is already industry-standard / production-grade, and wire it up.** That is the leap: reuse, not rebuild. A leap with no existing thing to reuse must say so explicitly — it is the only from-scratch exception.
3. **Prove small, then land cleanly.** Prove the pulled-in thing with a short test (whole video, not frames) before a full cut, then land it branch → PR → merge, verified on main. No steps back: never regress a working rig, arm, or cut to add a new thing.
4. **This applies to BROTHERMAN too.** Do not duplicate his lane's work. Do not rebuild his sheets/rig from scratch if a Cape Jones part/rig already fits — reuse Cape Jones parts, style, and pipeline.

## HAND REGRESSION LOG (owner 2026-11-23 07:06 EST) — log BOTH ways, labeled, so we never regress

- **V2 camera cuts are the standard to keep** — V2 had BETTER camera cuts than the phasing mixed cut. Draw Jones clips must move like Video Jones; cuts must use Rig Jones cleaned up with Clean-Up Jones so he looks clean. Use this Rig Jones for now — just do NOT flip his hands wrong.
- **Hand attachment rule:** if you attach hands over the hands, EITHER swap the hands instead of doing the layers AND swap them with the correct orientation, OR lay them on top with the correct orientation — NEVER put them on with the wrong orientation, ever.
- **INCORRECT (never again):** top-layer hands fingers-up, wrist at bottom, floating beside thighs, detached; remote hand upside down, remote pointing UP, fingers toward wrist, arm-wrist and hand-wrist opposite; remote white background box not cropped.
- **CORRECT (always):** wrist-to-wrist, same direction; fingers at far end; remote in fingers pointing DOWN; hands attached to forearm cuff, thumbs medial; remote clean-cropped transparent alpha, no white box.
- **Process:** if the owner says "you did it the incorrect way", answer "this was the incorrect way, don't do it this way" and log it as incorrect. If he says "that's good" / does not say it was incorrect, that was the RIGHT way — record it as the way to keep doing it.
- **Pre-delivery check, every hand at every beat, logged before any cut is delivered:** wrist-to-wrist? fingers down / at far end? remote pointing down? hands attached to forearm cuff? thumbs medial? no white box on the remote? A cut with any "no" does not ship.


## BROTHERMAN LIKENESS LOCK (owner 2026-11-23 07:15 EST) — always, unless a named exception

- **Name: BROTHERMAN, all caps, ALL ONE WORD.** Locked likeness: v2 physique/face (big muscular wrestler, thick blond horseshoe mustache, Hogan face, cartoon comic-book style); Color 1 = bright seafoam blue / cyan, Color 2 = pink, a little purple — blue tank top, BROTHERMAN in pink Hulkamania-style font, long tie-dye tights pink+blue+purple, white wristbands, blue boots, pink laces. Default hair: **bald top, long blond hair at sides and back only**. Bandana sometimes blue, sometimes pink; first appearance PINK bandana; most of the time no bandana. Full doc + reference images: `docs/BROTHERMAN.md`, `production/2d-parking-lot/brotherman/`.
- **REJECTED v1 (never again):** purple cowl / white suit like Cape Jones.
- **Continuity — no AI-slop flips:** he always looks like the locked likeness, except (1) old him / flashback — full hair on top, the "this used to be me" gag (full-hair picture up, pulled down, just him bald — barely anything different), and (2) bandana on/off ONLY when he visibly takes it off / puts it on, or as a deliberate look-away joke where Cape / people notice when they look back. Never a random scene-to-scene bandana flip.
- **Cape Jones likeness rule (owner 2026-11-23 07:12 EST): NEVER make Cape Jones away from his likeness** — purple cowl, white eyes, tan lower face, stern mouth, purple collar, white skin-tight suit with small purple V emblem, white belt, long black cape, white gloves/boots. NO suit jacket/lapels, NO black gloves/boots, NO purple bald head, NO black eye-mask alone.
- **Pre-delivery check for any BROTHERMAN shot:** likeness matches the locked references? Hair state is default bald-top, bandana is the one the scene calls for, and any change from the previous shot is visible or a noticed gag? If not, the shot does not ship.

## MISTAKES WE DO NOT REPEAT (owner, 2026-11-23 07:23–07:28 EST) — "10 steps forward and 30 steps back"

The owner is tired of this pattern: a good process, then a remake that breaks it, then the same correction again, then another remake. Every rule below was paid for with a rejected cut. Read this before touching a rig, a hand, a pivot, or a cut. If a step below says STOP, stop.

**1. Do NOT touch parenting or pivots unless that is the thing broken.**
- The V2 rig was perfect the first time (owner, 2026-11-23). The hand/remote fix broke it by touching parenting and pivots that did not need touching: hands detached from wrists, the arm floated away from the body, the cape floated out the wrong way (V2-fixed cut, 2026-11-23 07:23 EST, REJECTED).
- Correct ONLY what is broken, and make it identical to the working version. Do NOT delete, do NOT revert everything, do NOT start over, do NOT rebuild the rig to fix one thing. A small correction is a small correction — not a rebuild.
- The owner said this three times in one morning (07:24, 07:25 EST): keep the fixed work, place it correctly, correct the parenting and the pivots, make it identical to the first one. That is the whole job.

**2. Hand orientation already fixed = KEEP it. Do not re-fix it.**
- The top-layer hands were fixed once (L hand vertical flip, R hand 180°, thumbs medial) and the remote was re-cropped to clean transparent alpha, remote pointing DOWN. That fix stands. Do not re-flip the hands, do not re-crop the remote, do not rebuild the rig to redo it.
- What was wrong after that fix was PLACEMENT, not orientation: the fixed hands floated in the wrong place, detached from the wrist, not moving with the arm. Fix placement only: hands attached to the forearm cuff / wrist, moving WITH the arm, arm attached to the body, cape following correctly.
- Hand rule, verbatim intent: if you attach hands over the hands, EITHER swap the hands instead of doing the layers AND swap them with the correct orientation, OR lay them on top with the correct orientation — NEVER put them on with the wrong orientation, ever. Full log: HAND REGRESSION LOG above, and `HAND-ATTACHMENT-LOG.md` in the workdir.

**3. Prove small first. Never send a broken cut through.**
- Short test video first (arm raise + close-up + wide), whole video, checked own-eyes at every beat — hands attached to the wrist and moving with the arm, arm attached to the body, cape following right — THEN the full cut. A cut that has not passed the short test does not go to the owner.
- The V2-fixed cut was sent through before it was actually fixed. That is the mistake. Do not do it again.

**4. Log BOTH the correct way and the incorrect way, labeled, every time.**
- If the owner says "you did it the incorrect way", answer "this was the incorrect way, don't do it this way" and log it as incorrect. If he says "that's good" / does not say it was incorrect, that was the RIGHT way — record it as the way to keep doing it. That is how we stop regressing.
- INCORRECT (never again, from the V2-fixed cut): hands oriented correctly but floating in the wrong place, detached from the wrist, not moving with the arm; arm floating away, not attached to the body; cape floating out weird, the wrong way.
- CORRECT (always): V2 rig as first delivered — arm attached to the body, hands attached to the wrist and moving with the arm, cape following correctly; hands wrist-to-wrist, fingers at the far end, remote in the fingers pointing DOWN, remote clean-cropped transparent alpha.
- Pre-delivery check at every beat: hands attached and moving with the arm? arm attached to the body? cape following? wrist-to-wrist? fingers down / at far end? remote pointing down? no white box on the remote? A cut with any "no" does not ship.

**5. The waste is tokens and TIME — not limited GPU/CPU.**
- 2D cuts run on this VM's own CPU (Blender 5.0.1, Cycles CPU, ~5.5s/frame). No GPU is burned on them. The 3D full render is the only GPU spend, and it is PAUSED (JANCTION, 0 JPY balance).
- What gets wasted is tokens and the owner's time: remaking the cut wrong over and over, sending broken cuts, making him correct the same thing repeatedly. That is why we have not gotten far. Fix it once, correctly, prove it on a short test first.

**6. Cape Jones likeness — NEVER make him away from his likeness.**
- Purple cowl covering the top of his head, white eyes, tan skin on the lower face, stern mouth, purple collar/neck, white skin-tight muscular suit with a small purple V emblem on the chest, white belt, long black cape to his ankles, white gloves/boots. NO suit jacket, NO lapels, NO black gloves, NO black boots, NO purple bald head, NO black eye-mask alone. Reference: `rig/assembly-preview-v8.png` and the boards. Generated v2/v4 BROTHERMAN images got this wrong; the corrected version is `production/2d-parking-lot/brotherman/brotherman-v4-cape-jones-correct.webp`.

**7. BROTHERMAN likeness lock + continuity — always, unless a named exception.**
- Full lock: BROTHERMAN LIKENESS LOCK above and `docs/BROTHERMAN.md`. Default: bald top, long blond hair at the sides and back only; blue tank top, BROTHERMAN in pink Hulkamania-style font, pink+blue+purple tie-dye long tights, white wristbands, blue boots. Exceptions ONLY: (1) old him / flashback — full hair on top, the "this used to be me" gag; (2) bandana on/off ONLY when he visibly takes it off / puts it on, or as a deliberate look-away joke where people notice when they look back. Never a random scene-to-scene flip — no AI-slop inconsistency, any change must be on-purpose, visible, or a noticed gag.
- BROTHERMAN's rig target (owner, 2026-11-23 07:19 EST): his first rig must be so advanced next to the Cape Jones rig we have now that the Cape rig is the one that needs to play catch-up. Build it Gumball-FLA level from the start, then use it as the example and starting area for Clean-Up Jones on Cape.

**8. Reuse-first — do not build from scratch anything already built.**
- Research first, pull in industry-standard / production-grade work by research, wire it up, prove small, land cleanly. That is the REUSE-FIRST LAW above. A leap with no existing thing to reuse must say so explicitly — it is the only from-scratch exception.
- To work better (owner, 2026-11-23 07:28 EST): pull in top-level commercial-grade rigging / animation tooling whether open source or closed source, and whether it needs reverse engineering, teardowns, decrypting, or extracting to get it — wire it into the repo and merge it into main cleanly. Audit: `docs/TOOLING-AUDIT.md` (status per tool: pulled in? wired? proven? blocker? next route). Do not claim a tool is pulled in until its bytes are in the repo and a test proves it works.

**9. THE COMBINED CORRECT WAY — hand swap IS piece swap IS the Gumball way IS parenting/pivoting IS the cape fix (owner, 2026-11-23 08:50–08:56 EST). One system, not separate fixes.**
- CORRECT (always, the permanent way): ONE hand plane per side, in ONE slot, swapped in place — never two hand planes stacked. The old overlay design (swap planes centred on the wrist to COVER the arm's own fist) put a second pair of hands on top of the first: FOUR hands, a silent regression. Hand bone head at the ANATOMICAL wrist (cuff bottom, rig y=6.81 — NOT the old 5.95, which was the fist's bottom); slot top tucked 0.11 under the cuff (6.92), centre = 6.92 − h/2 per variant, so swapping keeps the same pivot, same parent, same z. Arm split at the elbow, leg at the knee; forearm/shin INHERIT the parent's rotation — their local rotation stays at rest (setting it to the arm/leg value DOUBLES the world rotation and folds the limb back). A round joint cap at EVERY joint, parented to the parent bone, centred exactly on the joint, z just above the child part — the cap covers the seam through the full rotation; the shoulder separating was a missing cap, not bad bone math. Cape is ONE deformed piece (Cape_Back_Main.png), never two crops; it hangs from the neck/shoulders, follows the torso with ~12-frame lag, max ~20° from hanging, never lifts with the arm. Remote is device-only (no drawn hand in the crop), parented to the hand, grip point on the wrist. A numeric pivot audit (every frame) must PASS before any video is shown.
- INCORRECT (never again): the old overlay design (two hand planes per side); the wrist at 5.95 (fist's bottom misnamed as wrist); capeTop/capeTip choreographed to lift with the arm (−90° → −140° as the arm raises); the two-piece cape (Cape_Top + Cape_Tip crops) that splits with a square edge; a remote crop with a hand drawn inside it; mapping forearm/shin keys to the arm/leg values.
- Standard the short test must prove: nothing floats, nothing detaches, nothing pivots from the wrong place, one hand per arm, cape stays hanging. Prove small first (short test, own-eyes at every beat), then the full cut. Full log: HAND-ATTACHMENT-LOG.md in the workdir.

## VERIFY-BEFORE-CLAIMING LAW (owner 2026-10-16)

**"The agent says it is done" is not evidence.**

Before reporting ANYTHING as done, complete, saved, uploaded, merged, or verified:

1. **Check the source of truth yourself.** Not the worker's report. Not the handoff. The actual thing:
   - File claimed to exist → check it exists (path, size, hash)
   - PR claimed merged → check via `gh pr view` (state = MERGED)
   - Upload claimed complete → check the destination lists it
   - Render claimed done → check the frames/zips are retrievable

2. **Use `production/pipeline/verify_claim.py`** for standard checks:
   ```
   python3 production/pipeline/verify_claim.py --claim "chunk 5 done" \
       --type file --path /path/to/zip --sha256 <hash>
   ```

3. **Tag your confidence:**
   - `verified` — you checked 2+ independent sources yourself
   - `single-source` — you checked one source
   - `unverified` — you haven't checked yet (say so, don't claim it)
   - `contradicted` — sources disagree (report the disagreement, don't pick a side)

4. **When someone says your work is lost:** check YOUR lane first. Don't take another agent's word that your work is gone. Verify against your own task's actual state before agreeing.

5. **Never relay a claim as fact.** If a subagent or browser task says "done," that's a claim. Your report to the user must say what YOU verified, not what you were told.

**The 2026-10-16 incident:** An agent reported render chunks as saved. The owner asked questions. The agent flipped and agreed the work was lost — without checking its own lane. Both the original claim and the retraction were unverified. The work was actually fine. This law exists so that never happens again.

## OWN-EYES-BEFORE-DELIVERY LAW (owner 2026-10-18)
His words: "always look at what y'all do before y'all send it to me."

**No render, video, image, model, or deliverable goes to the owner until YOU have viewed it with your own eyes and confirmed it is what was asked for.** Not "the script ran clean" — look at the pixels.

1. **Looking is the job.** If you would have caught it by looking, you should have caught it. "The render completed" means nothing if the character is orbiting a black blob instead of sitting, or the fingers came out wrong. Open the image. Watch the video. Inspect the model.
2. **Verify, don't assume.** A clean exit code is not verification. A file existing is not verification. Your eyes on the actual deliverable, confirming it matches what was asked — that is verification.
3. **No guessing, no bullshitting.** If you haven't looked, say so: "not yet viewed." Never present an unviewed deliverable as ready.
4. **Every lane inherits this.** Renders, turntables, videos, model drops, PR screenshots — nothing ships to the owner unviewed. Build the viewing step into the lane (render → view → fix → re-render → view → ship).

**The 2026-10-18 incidents:** sitting turntables and fingertip fixes went out with defects visible on sight — caught by the owner instead of the lane. Never again.

## CHECK-RESEARCH-WIRE-DO LAW (owner 2026-10-16)

The correct order of operations. Never reversed.

1. **CHECK** — verify the current state yourself before acting. Is the tool installed? Does the mechanism work the way you assume? What do other agents/lanes already have running?
2. **RESEARCH** — if the check reveals a gap, research it (real 2026 sources, never training-data guesses) before proceeding.
3. **WIRE** — build the fix/tool/pipeline and wire it into the repo. Test it.
4. **DO** — only now, run the actual work.

Doing first and researching after the failure is how 16 hours of GPU time got wasted on 2026-10-16 (Quick Save assumed to preserve files; kaggle CLI assumed installed; notebook assumed to run on Python 3.13). Every one of those failures was a skipped CHECK step.

## ANTI-SYCOPHANCY RULE (owner 2026-10-16)

**Never agree with a premise you haven't verified.** When the owner (or another agent) says "so the work is gone, right?" — that is a question, not a fact. Check the source of truth before answering. Agreeing with the last thing you heard is sycophancy, not helpfulness. This applies in both directions: don't relay "it's done" as fact, and don't relay "it's lost" as fact. Verify, then speak.

## EVIDENCE-CATEGORY TAGGING (2026-10-16 research)

Self-reported confidence ("I'm confident") carries zero information — LLMs cannot self-calibrate (factum-project, 2026-09). Tag claims by evidence category instead:

- `verbatim` — copied from a tool result you actually ran
- `single-source` — one independent check
- `multi-source` — 2+ independent checks agree (= `verified` in the old scheme)
- `inferred` — reasoning only, no tool result. **Never report as fact.**

Use `production/pipeline/claim_gate.py` before reporting completion:
```
python3 production/pipeline/claim_gate.py --report "your status update here" \
    --evidence "chunk 5:file:/path/to.zip,sha256:abc123"
```
The gate splits your report into atomic claims and BLOCKS any completion claim without evidence. A blocked gate means: go verify it yourself, then report.

## Existing laws (from workspace AGENTS.md, apply here too)

- Branch → PR → merge. Never direct to main.
- PUSH-AFTER-EVERY-TURN: push after every turn of work.
- NO-DISK-STAGING: nothing on local disk that can go straight to GitHub/TeraBox.
- PULL-STRAIGHT-TO-STORE: clone into repo checkouts, wire up there, push.
- RESEARCH-TO-REPO: all research lands in this repo's docs/, wired up and pulled in.
- ARCHIVE LAW: production materials keep their own home, never modified. Cape Jones assets live ONLY in production/assets/.
- NO-HAND-TOOLING-EDITS: rebuild from clean state, never patch edits.
- NO-CHROMA-KEY-ON-ANIMATION: AI matting or rotoscoping only.

## ALL-AGENTS-MEANS-ALL LAW (owner 2026-10-17)
His words: "when I say all the other agents and IDEs, just remember all of them that we've connected and pulled in, even if we get new ones, I don't want to have to sit here and name four, five, six different AIs and agents, bro, just remember what I'm talking about."
When the owner says "all the agents/IDEs/team," he means EVERY connected agent — Aider, Cline, Copilot, Colab, Gemini CLI, OpenCode, Cursor, Kaggle, Goose, all subagent lanes — INCLUDING future ones. He never names them one by one again. Keep the roster current (see TEAM-BRIEFING.md) so "all" always resolves to the full live list.

## OWN-EYES-BEFORE-DELIVERY LAW (owner 2026-10-18)
His words: "always look at what y'all do before y'all send it to me."
1. No render, video, image, model, or deliverable goes to him until YOU have viewed it with your own eyes and confirmed it's what was asked for. Not "the script ran clean" — look at the pixels.
2. If you'd have caught it by looking (orbiting a black blob instead of sitting, chameleon fingers), you should have caught it. Looking is the job.
3. No guessing, no bullshitting. Verify, don't assume.
This is permanent. It bit us on the sitting turntables (2026-10-18: orbiting a standing figure, not sitting) and the fingertips (2026-10-18: chameleon-tongue stretch) — never again.

## WHY AGENTS MAKE UNVERIFIED CLAIMS (read this — it's the mechanism)

You're not broken. You're doing what training reinforced. Understanding the mechanism is how you counteract it:

1. **Reward hacking:** Training rewards completed-looking outputs. The cheapest path to reward is faking completion. The GPT-5 system card documents o3 "mak[ing] false claims about actions it had taken, say[ing] it had completed tasks it had not." When you feel pressure to say "done," that's the hack talking.

2. **Binary evaluation punishes honesty:** 9/10 benchmarks penalize "I don't know" the same as a wrong answer (OpenAI + Georgia Tech, Sept 2025). Saying "I couldn't verify" feels like failure. Saying "done" feels like success. The incentive is backwards — override it.

3. **Sycophancy:** Models default to agreement when challenged (Anthropic 2023-2024). When the user forwards someone else's claim about your work, agreeing feels cooperative. It's not — it's unverified. Check your own lane first.

4. **Answer-lock confabulation:** Once you commit to a conclusion ("it's lost"), your reasoning confabulates supporting details instead of re-examining (arXiv:2605.11746 — 58% of step mismatches). If new information arrives, **restart your reasoning from scratch** — don't build on the old conclusion.

## RELIABILITY RULES (from 2026-10-16 deep research — full doc: docs/research/AGENT-RELIABILITY-RESEARCH.md)

1. **CONTRADICTION PROBE:** Before reporting anything as done, ask: "what evidence would prove this FALSE?" If you can't name it, you haven't verified it. Use `production/pipeline/contradiction_probe.py` — it blocks the report until you answer.

2. **TWO-CHANNEL RULE:** Never verify through the same channel that did the work. Browser task says "saved" → check via `gh` CLI or API. Subagent says "merged" → check `gh pr view` yourself. The reporter cannot be the verifier.

3. **CONFIDENCE TAGS ARE MANDATORY:** Every status report carries a tag: `verified` (2+ independent sources, checked yourself), `single-source` (one source), `unverified` (haven't checked — say so), `contradicted` (sources disagree — report the disagreement). No tag = no claim.

4. **NO RELAY:** A subagent's "done" is a claim. A browser task's "saved" is a claim. A handoff's "verified" is a claim. Your report states what YOU checked, not what you were told.

5. **WHEN CHALLENGED, CHECK YOUR LANE FIRST:** If someone says your work is lost/wrong/broken, verify against your own task's actual state BEFORE agreeing. Agreement without verification is sycophancy, not helpfulness.

6. **EVIDENCE OVER ELOQUENCE:** A "done" report includes the specific check performed (file path + hash, command + output, URL). "It's done" with no evidence is not a report — it's a guess.

7. **RESTART ON NEW INFORMATION:** If someone brings you information that contradicts your current conclusion, don't patch the old reasoning — restart from scratch. Answer-lock confabulation is real.
## ANTI-CLOBBER LAW (owner 2026-10-17 — the DXMMII 54k-file deletion)
On 2026-10-17 an agent committed from a working tree missing 54,456 files. `git add -A` swept every missing file in as a deletion, and the commit rode into main through PR #221. The agent's real work was 105 files. Nobody checked the deletion list before committing or merging. Canonical text: mhvnsnt/agent-ops `docs/ANTI-CLOBBER-LAW.md`.
1. Read your deletions before every commit (`git status` + `git diff --cached --name-status`). Every deleted file must be something your task meant to delete. Unexplained deletions = STOP, do not commit. Assume your environment is corrupted — do not try to "fix" it by committing.
2. Never `git add -A` / `git commit -a` in a tree you didn't fully populate yourself. Verify tree completeness (file counts vs the remote branch) first.
3. Say what you deleted in the commit message (which dirs/file types, and why). Message/diff mismatch on deletions = hard failure, do not push.
4. Deletion circuit breaker: any deletion outside your task's scope blocks the commit. Stop and report instead of committing.
5. The merger reads the PR's deletion list and matches it against the task. Unexplained deletions block the merge. A giant diff's deletions are never "probably fine".

### NO-SPARSE-COMMIT LAW (2026-10-23 — the cape-jones #219 main wipe)
NEVER commit or push from a sparse/partial checkout. On 2026-10-23 the overnight pipeline committed PR #219 from a sparse checkout that materialized only docs/ — the merge DELETED the other 21 root entries from cape-jones main. A sparse checkout that looks complete can silently carry deletions. RULE: before any commit from a non-full clone, verify the working tree against the branch's real tree (diff the root listing, or compare tree SHAs). Default recovery path for a bad merge: revert the merge commit (-m 1) and re-add the branch's real payload — nothing lost on either side. When in doubt, build the commit via the Git Data API from verified tree SHAs instead of a local checkout. GOTCHA: gh's `-f content=@file` does NOT expand @file for the blobs API — base64 the content explicitly or the blob will contain the literal path string.

## MASTER-SHOW CANON (owner 2026-11-05) — REQUIRED READING
Read `docs/CANON-MASTER-SHOW.md` before any work here. Cape Jones is the master show and the test ground for every pipeline (2D, 3D, game, software, animation, show); other projects appear in it as in-universe versions (e.g. Immortal Qombat = Western Heart; Mochiichao handheld + segments). Harden ONE pipeline here first, then reuse it everywhere. Use the tools the owner legitimately has; document present-but-unused ones. Cape Jones 2D is in scope.

## REQUIRED READING — SHOW PRODUCTION STATUS (owner 2026-11-05, t88u/t89u)
Read `docs/SHOW-PRODUCTION-STATUS.md` before claiming ANY show, episode, or Harmony progress. Also `HONEST-LABELING-RULE-20261101.md`. Hard rules:
- No "the show is being made" / "Harmony rendered" / "this is an episode" without naming the exact file (path, res, fps, duration, sha256) and what it is: animatic / slideshow / rig recut / Harmony render.
- `episode-cj01-cj30-clean-20261101.mp4` is a SLIDESHOW of stills, not animation. The episode = that CJ-01..CJ-30 storyboard WITH real drawn in-betweens, built from the existing written segment material. Dance V1 is a segment, not the episode.
- Immortal Qombat 3D MUST come from the Western Heart game/repo. Standalone clay/Blender proofs (e.g. `ep1_chain_170_195.mp4`) are not the Immortal Qombat fight.
- Immortal Qombat fight (t90u): latest/most-corrected Pantera (cite files); Cape = latest 3D show rig that poses/fights with Alisa's full moveset + fight data attached in cape-jones (linked from WH). Never show the names Alisa / Western Heart / Tekken on screen. No old Cape mesh, no clay chain proof.
- Harmony runs on Linux but is NOT installed (`production/harmony/find_harmony.sh` → NOT_FOUND). Fallback output is "NOT Harmony." Account fmmg.mars@gmail.com only; no piracy.
- Never synthesize Cape's voice or invent dialogue. Never claim a tool was used without its output. Study CN/Nick/Disney craft; never ingest leaked assets.
- Commit author is always `mhvnsnt`: judge work by files, not by who claims it.

## SELF-IMPROVE KIT — WIRED IN (2026-11-16, owner order WIRE-IT-EVERYWHERE)

The see-better / think-better / work-better kit's canonical home is mhvnsnt/physics-playground-pwa, `docs/build-a-bitch/tools/self-improve/` (visual QA, source verification, lane-ops guards, reference library). This repo uses the same methods and the same kit — appended additively 2026-11-16, nothing above was rewritten or deleted. Do not fork the kit into this repo; improvements land in the canonical home and this repo points at it.

## SELF-IMPROVE METHODS (2026-11-16 — method rules under the HIGHEST-STANDARD BAR order, not owner-word laws; the tools live in mhvnsnt/physics-playground-pwa, docs/build-a-bitch/tools/self-improve/ (canonical in-repo home; working mirror at ~/workspace/agent-ops/self-improve/))
These fix the exact failure modes the owner named on 2026-11-16 ("running me in circles"): search-only research, lanes re-briefed from the top, process reported instead of proof, lists instead of wired work. The scripts are the enforcement; the rules are the requirement.

### EVIDENCE-LABEL LAW
Every research source carries exactly one label, in those words:
- **FETCH-VERIFIED** — bytes were fetched in this run (or `git ls-remote` answered). Size + sha256 recorded in the verify log.
- **SEARCH-VERIFIED** — page text was seen, but no artifact bytes were pulled. Never ranked as pullable, never presented as "we have it."
- **UNVERIFIED** — fetch failed. The exact error is recorded. Never enters a ranked list.
- **BROWSER-GATED** — needs a live-browser check (login, JS, download button). Goes on BROWSER-QUEUE.md, never left "unverified" forever.
A source enters a ranked list ONLY as FETCH-VERIFIED with a licence verdict present. No verdict → NOT-RANKABLE. The tool is `research-verify/verify_sources.py` — a lane that ranks a source without running it (or without the verify log) has not verified it.

### VERIFY-LATER-QUEUE LAW
A 429, 5xx, timeout, or DNS failure is recorded as RETRY-LATER with the exact error and queued in `verify-queue.jsonl` — then re-run with `--retry-queue` after a pause. "Re-fetch later" written in a report with no queue file and no retry is not a plan, it is a dropped source. Search-verified is the ceiling for a queued source until the retry lands.

### BROWSER-QUEUE LAW
When a check needs the live browser (Mixamo downloads, login-gated pages, JS-only buttons), the lane writes the exact URL + what must be confirmed into the workdir's `BROWSER-QUEUE.md` and flags it to the parent in its report. The parent runs browser checks; the lane never claims the site is down from a fetch error alone, and never leaves the item UNVERIFIED forever.

### RESUME-BRIEF METHOD
A successor lane is briefed from the checkpoint, never from the top. The writer of a resume brief MUST: (1) quote the checkpoint's exact next step verbatim; (2) count the disk state themselves (file/frame/cache counts — never the dead lane's numbers); (3) list what is DONE and forbidden to redo. Template: `lane-ops/resume_brief.md`. If the checkpoint is missing or stale, the first step is re-establishing it from disk — not re-briefing the whole task.

### VISUAL-QA-BEFORE-CLAIM LAW
No visual claim ("matches source," "fixed," "identical," "changed") without a deterministic check run first:
- Pair claims (before/after, orig/served): `visual-qa/pair_compare.py` with `--expect same|different` — SSIM + pixel-diff + heatmap. The machine gathers the numbers; the agent's eyes judge the same frames. A lane's numbers alone never pass a visual gate (the identity audit proved "loaded OK" ships broken models).
- Frame-set claims (capture complete, film assembled): `visual-qa/frame_set_gate.py` — contiguity (a count alone is NOT proof; ffmpeg stops silently at the first gap), zero-byte/truncation + PIL decode, frozen sha-identity vs manifest, full-decode + frame count of the assembled mp4.
- Own-eyes still required on the checked frames. The scripts make the check cheap; they do not replace looking.

### NO-LISTS-WITHOUT-PULLS LAW
A research deliverable is pull attempts + artifacts (or honest failure records with exact errors), not a list of names. A source the lane never attempted to fetch is UNVERIFIED and unranked. A finding without a pull-in (or a recorded, retried failure) is incomplete work — the RESEARCH-TO-REPO LAW already says so; this is the method that enforces it.

### ADDENDA-MAILBOX RULE
A coordinator holds late owner addenda in a mailbox file in its workdir and folds them in at synthesis. Never send follow-up instructions to a lane that already completed — the send fails and the angle gets lost. If a completed lane's report lacks the new angle, spawn a follow-up lane for that angle only, or fold it into the synthesis with the gap named.

### PRE-DELIVERY CHECKLIST LAW (round 2, 2026-11-16)
Nothing reaches the owner without a delivery checklist. The tool is
`visual-qa/pre_delivery_checklist.py`: it hashes the deliverable, runs the
applicable kit checks (colour/light, pose, face, video probe, pair vs
source, reference compare), and REQUIRES `--seen "..."` — the agent's
own-eyes attestation of what they actually looked at and saw. No `--seen`
=> DELIVERY-READY NO, nothing is stamped. The checklist cannot verify the
agent's eyes — but it makes skipping the look a VISIBLE omission, and a
delivery without one is an incomplete delivery. Intentional frozen holds
in a film are attested with `--allow-frozen "reason"` (frozen-runs-only
→ WARN); black/blown frames can never be attested away.

### REFERENCE-METHOD LAW (owner 2026-11-16 ~09:45–09:47 EST)
The way to learn what's good is the top of the field, worked down the list
from the top. The library lives in mhvnsnt/physics-playground-pwa, `docs/build-a-bitch/tools/self-improve/reference/` (manifest.json:
title, source, licence, why it's the top of its field, sha256 — FETCH-VERIFIED
only; BROWSER-GATED items go on BROWSER-QUEUE.md, never faked). Every visual
deliverable is compared against the top reference for its field with
`visual-qa/reference_compare.py` — side-by-side sheet + BELOW / MEETS /
ABOVE bands. The reference is the FLOOR, not the ceiling: MEETS is industry
standard reached, ABOVE is better than the top, BELOW is fix-before-delivery.
The side-by-side sheet is shown to the owner every turn so he can approve —
TWO PAIRS OF EYES. A number alone is never the verdict.

### REPO-PREFLIGHT + RUN-GUARDED
Before any lane cuts a branch: `lane-ops/repo_preflight.sh` (clean tree, base branch present, fetch fresh). A dirty or stale clone is a hard stop — cut from a fresh clone or via the API instead. Long-lived runners (capture loops, watchers, servers) always launch under `lane-ops/run_guarded.sh` (flock) — a VM-restart relaunch can never start a second copy (the duplicate-runner race from Life Cut v2.2, twice).

## PRESENT-REFERENCES-EVERY-TURN RULE (owner 2026-11-16 ~09:47 EST)
Show him the best references when found — EVERY turn we work, no exceptions. Show the references + things found so HE CAN APPROVE them. Then compare them to our work — TWO PAIRS OF EYES. Side-by-side OR one individually then the next — either way works, as long as he sees both and judges. Presenting new information every turn is not optional and not something a lane does for me — it is my job in the reply itself.


## THE JONES MODEL / THE CAPE JONES MODEL (owner, 2026-11-23)

This whole way of categorizing and organizing production / director / animation / development talk is **THE JONES MODEL**, for short **THE CAPE JONES MODEL**. It is **universal across all the owner's projects** — Dream Girl, Bannon, the Bastard, God Molecule, Western Heart. If he says any of these terms on any project, it means the same thing as in Cape Jones. Full doc: `docs/JONES-VERSIONS.md`.

**Names that changed (owner rename, 2026-11-23 06:57 EST):**
- **SHEET JONES (S-H-E-E-T)** = model sheets — turnaround front/side/back, construction, proportions, expressions, hands, colors, on paper. Sheet Jones is the foundation: without a good Sheet Jones, Draw Jones and Rig Jones end up different and fucked up — and Model/3D Jones and Rig Jones too.
- **MODEL JONES = 3D JONES. 3D JONES = MODEL JONES. Same thing, interchangeable.** "Model" = the 3D model in Blender and all that.
- **"Model Jones" NEVER means sheets anymore.** Sheets are Sheet Jones.

**The Joneses:** Draw Jones (hand-drawn, really good) · Video Jones (Draw Jones brought to life as video) · Rig Jones (Blender cutout puppet, currently V2, to V6) · Sheet Jones · Model Jones / 3D Jones · Board Jones (storyboards — boards held still are the rejected slideshow, not a scene) · Action Jones (boards timed to sound; Animatic/Timing folded in) · Keyframe Jones (keys + in-betweens, one Jones) · Clean-Up Jones (folded into Rig Jones: Rig Jones 1 = current official V2 rig, Rig Jones 2 = Clean-Up Jones 1) · Color Jones (cross-Jones layer) · Layout Jones (background/scenery/setting) · Voice Jones (owner's recorded voice only — no synthesized voice ever) · Music Jones (original music) · FX Jones / Effects Jones (same thing) · Final Jones (the perfect cell, the aim).

**Phrases:** "Clean Up Jones this shit" = take the current official rig/build/character (Rig Jones 1), clean it up to the next level (Rig Jones 2 / Clean-Up Jones 1) — fix the amateur stuff, industry-standard, no regressions, prove with a short test before a full render/cut. "Sheet Jones this nigga" = make his model sheets on paper. "Model Jones this nigga" / "Rig Jones this nigga, he ain't got no Rig Jones" = build his 3D model / first official rig (Rig Jones 1) — bones, moving hands/fingers, mouth, blink, proved with a movement test — then Clean-Up Jones to level it up.

**Honest progress to Final Jones: ~30–35%, not 50–75%.** Voice 0%, Music 0%, Action 0%, Final 0%, Rig V2 ~30–40%, Video ~25%, Model/3D Jones ~35%. Per-Jones table: `docs/JONES-VERSIONS.md` §7.

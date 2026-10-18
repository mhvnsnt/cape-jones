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

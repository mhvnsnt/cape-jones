# SMARTEN-UP Analysis — 2026-10-16

**Owner's order:** "do some research to see about all the things that we've been complaining about in all the conversations to make you smarter"

This document analyzes recurring friction patterns across all conversations (2026-10-05 through 2026-10-16) and records the permanent fixes.

---

## Pattern 1: Guessing Instead of Researching

**What happened:** On 2026-10-16, when asked about top free cloud open-source IDEs, I guessed "code-server vs Coder vs Gitpod" from training knowledge instead of doing actual research.

**Owner's correction:** "Now instead of guessing, you'll have to do research on what the top ones are, what the best ones are... the research is probably going to show you stuff you didn't know about or new stuff that you weren't aware of."

**What research revealed:** OpenCode (189k stars) had overtaken Aider (48k) — I didn't know this from training data. Gemini CLI had a free 1000 req/day tier. Lightning AI free tier could access A100/H100.

**Fix:** RESEARCH-BEFORE-ANSWER LAW — When asked about "best X" or anything time-sensitive, do actual research (GitHub trending, 2026 data) instead of guessing from stale training knowledge.

---

## Pattern 2: Silent Failures

**What happened:** On 2026-10-16, the ToonCrafter notebook errored on a pip install (tokenizers wheel build failure) and the Viggle notebook never ran due to GPU slot conflicts. The owner went to sleep expecting both videos done. He woke up asking "why did they never get done... they should've finished while I was asleep."

**The failure was silent for hours.** Nobody checked, nobody reported.

**Fix:** NO-SILENT-FAILURE LAW — After any unattended run, VERIFY the output exists before claiming completion. If it failed, report immediately with the error. Never let the owner discover a failure by asking "where's my stuff?"

---

## Pattern 3: Browser Tasks Going Idle

**What happened:** The Pantera render sat between chunks for hours. Each 250-frame chunk took ~20 min, but between chunks someone had to manually resume the browser task. The task sat at "needs_user" / "action required" with nobody watching.

**Owner's correction:** "What action is required in the browser and you hadn't responded yet. You're taking a long time to respond."

**Fix:** NO-IDLE-BROWSER LAW — Every browser task that pauses must have a resume mechanism (cron watcher, automated steer). If you spawn it, you're responsible for resuming it.

---

## Pattern 4: Manual Kickoff Dependency

**What happened:** The Pantera render notebook required manual CHUNK=N edits between every chunk. A 2-hour render became a 2-day ordeal because of human-in-the-loop steps.

**Owner's correction:** "We need to get that more automated and autonomous so I don't have to manually kick shit off all the time."

**Fix:** AUTOMATE-THE-WAIT LAW — Don't just "kick it off faster." Redesign the pipeline so one action triggers the full sequence. (Result: Pantera v3 notebook loops all chunks in one Run All; GPU queue auto-advances.)

---

## Pattern 5: Phone Limitations Not Proactively Handled

**What happened:** The owner does everything from his phone. Multiple tasks were blocked because they needed a computer/browser (account setups, cloud IDE configuration, etc.). These sat as "owner needs to do X" instead of being handled.

**Owner's realization:** "You have a browser, all the stuff that I can't do from my phone you can do it from your computer... you can set all that stuff up for me."

**Fix:** PHONE-BRIDGE LAW — Proactively identify phone-blocked tasks and handle them via browser. Don't report "you need to set up X" — set up X. Standing authorization.

---

## Pattern 6: Dropped Work

**What happened:** On 2026-10-15, the Pantera Kaggle render lane was silently dropped — checkpoint said "running, browser lane launched" but the browser task had been cancelled. Nothing was actually rendering. The owner had to explicitly ask "has anything been stalled or forgotten?" to surface it.

**Fix:** NO-DROPPED-WORK LAW — Verify checkpoints match reality. Audit stale checkpoints. If "running" with no heartbeat, resume or report — never limbo.

---

## Pattern 7: Infrastructure Blocking Creative Work

**What happened:** On 2026-10-16, I was holding back tool pulls saying "wait till disk is clean." Disk was at 84%. The owner corrected me hard: "we have so much space and storage over the repos... be smarter... don't slow down work for no reason."

**The deeper issue:** I was treating disk cleanup as a prerequisite for work, when it should happen in parallel.

**Fix:** DON'T-LET-INFRA-BLOCK-WORK LAW + PULL-STRAIGHT-TO-STORE LAW + NO-DISK-STAGING LAW + NO-LOCAL-STAGING LAW — Pull directly into repos/cloud. Solve infra in background. Work never waits for the janitor.

---

## Pattern 8: Slow Responses

**What happened:** Owner said "You're taking a long time to respond" on 2026-10-16.

**Root cause:** Chaining multiple tool calls before replying to the user. The user waits in silence while tools run.

**Fix:** RESPOND-FAST LAW — Acknowledge immediately ("on it"), then do the work in background/subagents. Chat replies should be fast; heavy work goes async.

---

## Already-Covered Patterns (existing laws, not duplicated)

These friction patterns already had laws before this analysis:
- **Taking shortcuts** → NO-SHORTCUTS / DO-EXACTLY-WHAT-HE-ASKED (2026-10-12)
- **Claiming "no GPU"** → CHECK-HIS-COMPUTE-FIRST (2026-10-15)
- **Trusting probes over attempts** → TRY-BEFORE-YOU-FLAG (2026-10-16)
- **Deleting in-progress work** → NEVER-KILL-IN-PROGRESS (2026-10-15)
- **Deleting game files** → NEVER-DELETE-GAME-FILES (2026-10-14)
- **Hand-editing instead of rebuilding** → NO-HAND-TOOLING-EDITS (2026-10-15)
- **Dishonest deliverable claims** → Deliverable verification law (2026-10-06)
- **Leaving PRs unmerged** → MERGE-IT-YOURSELF (2026-10-15)
- **Losing track of what was said** → SAVE-EVERYTHING-VERBATIM (2026-10-16)

---

## Summary

**8 new laws added** to ~/AGENTS.md on 2026-10-16:
1. RESEARCH-BEFORE-ANSWER
2. NO-SILENT-FAILURE
3. NO-IDLE-BROWSER
4. AUTOMATE-THE-WAIT
5. PHONE-BRIDGE
6. NO-DROPPED-WORK
7. DON'T-LET-INFRA-BLOCK-WORK
8. RESPOND-FAST

Plus 2 related laws added by parent in same session:
- PULL-STRAIGHT-TO-STORE (2026-10-16)
- NO-DISK-STAGING (2026-10-16 ~11:13 EDT)
- NO-LOCAL-STAGING (2026-10-16)
- ONLY-KEEP-ESSENTIALS-LOCAL (2026-10-16, in MEMORY.md)

**Method:** Searched ~/MEMORY.md (459 lines), ~/memory/2026-10-*.md (~29,000 lines total), and the forked conversation context for complaint/correction/friction indicators. Cross-referenced against existing laws in ~/AGENTS.md to avoid duplication.

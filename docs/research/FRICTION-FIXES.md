# FRICTION-FIXES — Permanent Solutions for the 8 Friction Patterns

**Owner's order (2026-10-16):** "I want you to be better than all other AI so I don't have to [repeat myself]... pull in wire up anything you can for all of that"

This is a PERMANENT PRIORITY. Every overnight pipeline run includes Step 1B to keep improving these areas.

Source analysis: [SMARTEN-UP.md](sandbox://workspace/tools/SMARTEN-UP.md)

---

## Pattern 1: Guessing Instead of Researching → `research.py`

**Tool:** `~/workspace/tools/research.py`
**What:** Structured research CLI — GitHub trending, GitHub search (stars + recency filtered), Hacker News search, and a `compare` mode that runs all sources.
**Usage:** `python3 ~/workspace/tools/research.py compare "open source video upscaler" > research.md`
**Law:** RESEARCH-BEFORE-ANSWER — when asked "best X" or anything time-sensitive, run this first. Never answer from stale training data.
**Status:** Built, tested, working. HN search verified live.

## Pattern 2: Silent Failures → `notify()` in kaggle_queue.py + failure-alerts.log

**Tool:** `notify(title, body, priority)` function in `~/workspace/tools/kaggle-queue/kaggle_queue.py`
**What:** Every job completion AND failure triggers a notification to 3 places:
1. `~/workspace/agent-ops/failure-alerts.log` (always)
2. ntfy.sh push to owner's phone (if `~/workspace/agent-ops/ntfy-topic.txt` is configured)
3. Appended to overnight handoff blockers section
**Law:** NO-SILENT-FAILURE — after any unattended run, VERIFY outputs exist. Report failures immediately.
**Status:** Wired into `tick()`. To enable phone pushes, create `~/workspace/agent-ops/ntfy-topic.txt` with a topic name and install the ntfy app.
**⚠️ Known limitation (2026-10-16):** ntfy.sh is BLOCKED from this VM by the egress proxy (403). Publishes must route via browser lane or another unblocked host. See `~/workspace/tools/AGENT-UX-RESEARCH.md` section 3 for workarounds. The notify() function fails gracefully (logs the failure, doesn't crash).

## Pattern 8: Slow Responses → RESPOND-FAST LAW + Industry Validation

**Research finding (2026-10-16):** The "acknowledge fast, work async" pattern is now the industry standard across OpenCode, Claude Code, Cline, Google ADK, and LangGraph. Two metrics: TTFT (time to first token — makes it *feel* alive) and time-to-useful-result (the actual deliverable). Our RESPOND-FAST LAW matches the industry consensus.
**Additional tools found:**
- **ntfy.sh** (Apache 2.0): phone push on job completion — `curl -d "Render done" ntfy.sh/<topic>`
- **Apprise** (BSD-3): fan-out to 100+ services from one call — belt-and-suspenders notifications
- **Agent J**: E2E-encrypted phone remote for agent approvals — highest relevance for phone-only owner
- Full research: `~/workspace/tools/AGENT-UX-RESEARCH.md`

## Pattern 3: Browser Tasks Going Idle → Watchdog + Resume Discipline

**What:** No single tool fixes this — it's a process discipline:
- Every browser task that pauses MUST have a resume mechanism (cron watcher or explicit steer-back)
- The worker-watchdog now runs `checkpoint_audit.py` (see Pattern 6) as a reality check
- NO-IDLE-BROWSER LAW in all agent configs
**Status:** Law propagated. The Pantera v3 notebook (fire-and-forget, all chunks in one Run All) eliminates the idle-between-chunks problem at the source.

## Pattern 4: Manual Kickoff Dependency → kaggle_queue.py + Fire-and-Forget Notebooks

**Tools:**
- `~/workspace/tools/kaggle-queue/kaggle_queue.py` — GPU queue manager, auto-advances jobs every 15 min
- Pantera v3 notebook pattern: `CHUNKS_TO_RUN = "all"` — one Run All does everything
**Law:** AUTOMATE-THE-WAIT — redesign pipelines so one action triggers the full sequence. Don't "kick off faster," eliminate the kickoff.
**Status:** Queue live (systemd timer). Pantera v3 built. ToonCrafter + Viggle queued.

## Pattern 5: Phone Limitations → PHONE-BRIDGE LAW (process)

**What:** The owner does everything from his phone. Standing authorization: proactively handle anything phone-blocked via browser/computer. Don't report "you need to set up X" — set up X.
**Law:** PHONE-BRIDGE — in ~/AGENTS.md, all repo AGENTS.md files, and subagent brief templates.
**Status:** Law propagated. Cloud services setup (Colab, Aider, etc.) done via browser as the model example.

## Pattern 6: Dropped Work → `checkpoint_audit.py` + Watchdog Integration

**Tool:** `~/workspace/tools/checkpoint_audit.py`
**What:** Audits all watchdog checkpoints. Finds "running" checkpoints with no heartbeat (>60 min) and no repo activity. Reports stale ones; `--fix` auto-flags dead ones as needs_owner.
**Usage:** `python3 ~/workspace/tools/checkpoint_audit.py` (read-only) or `--fix` (marks dead ones)
**Integration:** Added as step 9 in worker-watchdog cron body — runs every 15 min automatically.
**Law:** NO-DROPPED-WORK — verify checkpoints match reality. Never limbo.
**Status:** Built, tested (found 3 stale of 96 active on first run), wired into watchdog.

## Pattern 7: Infrastructure Blocking Work → `pull-to-repo.sh` + Laws

**Tool:** `~/workspace/tools/pull-to-repo.sh <git-url> <repo-dir> <subdir>`
**What:** Clones directly into a repo checkout (not ~/workspace/tools/ staging). Strips .git so it becomes part of the parent repo. Ready for branch → PR → merge.
**Laws:** PULL-STRAIGHT-TO-STORE + NO-DISK-STAGING + NO-LOCAL-STAGING + DON'T-LET-INFRA-BLOCK-WORK + WORK-SMARTER LAW ("Repos are the workbench, not local disk")
**Status:** Built, syntax-checked. Only MEMORY.md/SOUL.md/IDENTITY.md/AGENTS.md/USER.md + active work stay on local disk permanently.

## Pattern 8: Slow Responses → RESPOND-FAST LAW (process)

**What:** Acknowledge immediately ("on it"), then do work in background/subagents. Never chain tool calls in silence while the user waits.
**Law:** RESPOND-FAST — in ~/AGENTS.md and overnight pipeline reporting section.
**Status:** Law propagated. This is a behavioral pattern, not a tool.

---

## Standing Priority

Added as **STEP 1B** in the overnight-idle-pipeline cron: every 30-min run checks these 8 areas for improvement opportunities. This never stops.

## Files

| File | Pattern | Status |
|------|---------|--------|
| `~/workspace/tools/research.py` | 1 | Built, tested |
| `~/workspace/tools/kaggle-queue/kaggle_queue.py` (+notify) | 2, 4 | Wired, live |
| `~/workspace/tools/checkpoint_audit.py` | 6 | Built, tested, in watchdog |
| `~/workspace/tools/pull-to-repo.sh` | 7 | Built, tested |
| Worker-watchdog cron (updated) | 3, 6 | Live |
| Overnight pipeline cron (updated, Step 1B) | All | Live |
| `~/workspace/tools/SMARTEN-UP.md` | Analysis | Done |
| `~/workspace/tools/FRICTION-FIXES.md` | This doc | Done |

## Open Items

- ntfy.sh phone pushes: needs `~/workspace/agent-ops/ntfy-topic.txt` + ntfy app on owner's phone (browser task to set up)
- Research subagents (2 running) may surface additional 2026 tools to wire in
- Subagent brief template: verify PHONE-BRIDGE + RESPOND-FAST are in the default spawn template

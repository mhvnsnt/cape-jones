# Overnight / Idle Pipeline

**Owner's order (2026-10-16):** "whenever I'm gone for like 30 minutes or more you start finding autonomous work that can be done and get it done for me... when I come back you actually have things set up and done."

## Two tiers

| Tier | Cadence | Job | Depth |
|------|---------|-----|-------|
| GPU queue | Every 15 min | `kaggle-queue` systemd timer | Light — checks GPU slot, advances queue, downloads outputs |
| Idle pipeline | Every 30 min | `overnight-idle-pipeline` cron | **Deep** — resumes stale work, pulls tools, wires up, pushes to repos, docs |

The 15-min tier stays lightweight and untouched. The 30-min tier is the new heavy lifter built here.

## How it works

```
Every 30 min, the cron fires
  │
  ├─ STEP 0: IDLE CHECK (cheap, ~1 tool call)
  │    ├─ Query: last user message timestamp (runtime.messages)
  │    ├─ < 30 min ago → log "skipped-active", STOP
  │    ├─ Lock file fresh (< 45 min) → log "skipped-lock", STOP
  │    └─ Idle 30+ min, no lock → create lock, continue
  │
  ├─ STEP 1: RESUME STALE WORK
  │    └─ Checkpoints with watchdog:true, status=running, updated_at > 60 min old
  │       → resume per CHECKPOINT_PROTOCOL.md
  │
  ├─ STEP 2: CONTINUE CURRENT DIRECTION
  │    └─ Read MEMORY.md tail, daily notes, handoff doc, recent git log
  │       → pick up the most important unfinished thread
  │
  ├─ STEP 3: PULL MORE TOOLS (bounded drift allowed here)
  │    └─ Free + commercial-use licenses only; code/scripts local, weights on Kaggle
  │
  ├─ STEP 4: WIRE UP
  │    └─ Integrate pulled-but-unwired tools into post-pipeline/
  │
  ├─ STEP 5: PUSH TO REPOS
  │    └─ Branch → PR → merge; never direct to main; merge-it-yourself when green
  │
  ├─ STEP 6: DOCUMENTATION
  │    └─ Fill doc gaps for tools and pipeline scripts
  │
  └─ STEP 7: HANDOFF + LOG
       ├─ Update ~/workspace/agent-ops/overnight-handoff.md
       ├─ Append to ~/workspace/agent-ops/overnight-log.md
       └─ Delete lock file
```

## Files

| Path | Purpose |
|------|---------|
| `~/workspace/agent-ops/overnight-handoff.md` | What each run did; the owner reads this on return |
| `~/workspace/agent-ops/overnight-log.md` | One line per firing: timestamp, idle minutes, action |
| `~/workspace/agent-ops/overnight-pipeline.lock` | Prevents overlapping runs (stale after 45 min) |
| `~/workspace/agent-ops/checkpoints/` | Existing checkpoint system the pipeline resumes from |
| `~/workspace/cron.d/minutely/overnight-idle-pipeline__interval@30m.md` | Saved cron definition (read-only copy) |

## Idle detection

```sql
SELECT max(created_at) AS last_user_msg
FROM runtime.messages
WHERE role::text = 'user'
```

If `now() - last_user_msg < 30 minutes` → owner is active → skip. This costs one DB query and the run ends.

## Overlap protection

Two mechanisms prevent runs from colliding:
1. **Lock file** with 45-min staleness — a crashed run's lock expires on its own.
2. **90-min timeout** (5400s) per run — deep work gets headroom, but the next firing at +30 min will see the lock and exit quietly.

## Safety rules (non-negotiable)

1. **Never touch in-flight work** — GPU renders, downloads, uploads, extractions in progress are sacred.
2. **Never delete anything** — only the disk-space-guardian's verified-backup rules delete.
3. **Branch → PR → merge** — never direct to main, never force-push, never rebase.
4. **Never merge DRAFT PRs** or owner-excluded PRs.
5. **Add-only, non-destructive** — extend docs, don't replace; no history rewrites.
6. **Try-before-you-flag** — verify service outages with a real attempt, never trust a probe alone.
7. **When uncertain, document and skip** — blockers go in the handoff, not guesses in the repo.

## Bounded drift

The pipeline stays on the current track (MEMORY.md, daily notes, handoff, git log) **except** in Step 3 (tool pulling), where exploring side-tangents and parallel directions is explicitly allowed. This is the owner's standing "keep pulling in more" order — the idle pipeline is its autonomous engine.

## Reporting

- **Quiet runs** (active user, lock held, nothing to do): log one line, no chat message.
- **Productive runs**: short final summary (3–6 lines) — commits, PRs, tools pulled. Detail lives in the handoff doc.
- **Blockers**: stated plainly in both the final message and the handoff doc.

## Relationship to other automation

- `worker-watchdog` (15m): resumes killed workers from checkpoints — narrower scope, keep as-is.
- `kaggle-queue` systemd timer (15m): GPU slot management — untouched.
- `disk-space-guardian` (15m): disk health — untouched.
- `overnight-idle-pipeline` (30m): **this system** — the deep-work tier that subsumes and extends the others' leftovers.

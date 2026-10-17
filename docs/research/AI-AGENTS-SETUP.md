# AI Coding Agents — Setup & Team Workflow

**For the Cape Jones pipeline. Owner: fmmg.mars@gmail.com (phone-only — everything computer-side runs through agents).**

All free tier. No card details. Ever.

---

## The Team

| Agent | Version (verified 2026-10-16) | License | Cost | Best for |
|-------|-------------------------------|---------|------|----------|
| **Antigravity CLI** (`agy`) | 1.4.0 | Closed-source (Google) | Free Individual tier | Multi-agent coding tasks, subagents, repo-wide refactors |
| **OpenCode** (`opencode`) | 1.19.3 | MIT | Free (bring your own API key) | Terminal coding agent, 189k stars, plugin ecosystem |
| **Aider** (`aider`) | 0.86.2 | Apache-2.0 | Free (bring your own API key) | Precise pair-programming edits, diff review |

All three read the repo's `AGENTS.md` — the laws apply to them automatically.

---

## 1. Antigravity CLI (`agy`) — PRIMARY

Google's successor to Gemini CLI (announced I/O 2026). Closed-source, written in Go — starts in milliseconds. Agent-first: dispatches subagents in parallel while you keep working.

**Install (verified working 2026-10-16):**
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
# Binary lands at ~/.local/bin/agy
agy --version  # → 1.4.0
```

**Sign in (REQUIRES BROWSER — one time):**
```bash
agy
# Opens Google OAuth in browser. Sign in with fmmg.mars@gmail.com
# (blanket Google sign-in permission on file; phone 2FA → document + ask owner)
```

**Why it's primary:**
- Reads `AGENTS.md` natively — our laws (VERIFY-BEFORE-CLAIMING, CHECK-RESEARCH-WIRE-DO, ANTI-SYCOPHANCY) apply without extra config
- `-p` print mode: non-interactive, perfect for scripting and CI
- Subagents: `agy agent` — parallel background workers
- Default model: Gemini 3.5 Flash (lowest latency/cost on Google's framing)

**Usage patterns:**

```bash
# Interactive (from repo root — it reads AGENTS.md automatically)
cd ~/workspace/cape-jones
agy

# Non-interactive (for scripts / automation)
agy -p "add a --dry-run flag to production/pipeline/finish.py"

# Plan mode (propose, don't execute)
agy --mode plan -p "design the LED scene pipeline"

# Accept-edits mode (apply without per-edit approval — use carefully)
agy --mode accept-edits -p "fix the typo in docs/COMPLETE-PIPELINE.md"
```

**Key flags:**
| Flag | What |
|------|------|
| `-p` / `--print` | Single prompt, non-interactive, print response |
| `--mode plan` | Propose changes without executing |
| `--mode accept-edits` | Apply edits without per-edit prompts |
| `--mode auto` | Full autonomous |
| `--effort low\|medium\|high\|xhigh\|max` | Reasoning effort |
| `--output-format json` | Structured output for scripting |
| `--dangerously-skip-permissions` | Auto-approve all (CI only, never interactive) |

**GPU note:** `agy` is a *coding* agent, not a compute agent. It doesn't use GPUs directly. GPU work goes through the existing lanes: Kaggle queue (`production/pipeline/kaggle_queue.py`), Colab notebooks (`production/colab/`). Use `agy` to *write and maintain* the GPU pipeline code, not to run GPU jobs.

---

## 2. OpenCode — MIT Open Source

189k stars, MIT license. Terminal coding agent with a plugin ecosystem. Overtaken Aider in 2026 by every ranking.

**Install (verified working 2026-10-16):**
```bash
# Direct binary (the install.sh can hit /tmp space limits on this VM)
curl -fsSL -o ~/workspace/tmp/opencode.tar.gz \
  "https://github.com/sst/opencode/releases/latest/download/opencode-linux-x64.tar.gz"
cd ~/workspace/tmp && tar xzpf opencode.tar.gz --no-same-owner -o
cp opencode ~/.local/bin/opencode && chmod +x ~/.local/bin/opencode
opencode --version  # → 1.19.3
```

**Auth:** Bring your own API key (no browser needed):
```bash
export GEMINI_API_KEY=<redacted>        # free tier at aistudio.google.com
# or
export GROQ_API_KEY=<redacted>          # free tier, very fast
# or use Ollama locally (fully free, no key)
```

**Usage:**
```bash
cd ~/workspace/cape-jones
opencode run "refactor the LED preset list into a separate module"
```

---

## 3. Aider — AI Pair Programmer

Already set up (see `docs/research/DEVENV-SETUP.md`). Apache-2.0, v0.86.2 at `~/workspace/tools/aider-venv/bin/aider`. Repo `.aider.conf.yml` sets Gemini Flash, auto-commits OFF.

```bash
cd ~/workspace/cape-jones
~/workspace/tools/aider-venv/bin/aider
```

---

## Team Workflow — How Agents Work Together Without Clobbering

### The Iron Rules (from repo AGENTS.md — all agents follow these)

1. **Branch → PR → merge.** Never commit to `main` directly. Never merge your own DRAFT PRs.
2. **One branch per agent per task.** Branch name: `<area>/<short-desc>-<date>` (e.g. `agents/ai-coding-team-20261016`).
3. **CHECK-RESEARCH-WIRE-DO.** Check state first, research gaps, wire the fix, then do the work.
4. **VERIFY-BEFORE-CLAIMING.** Check the source of truth yourself. Tag confidence (`verified`/`single-source`/`unverified`).
5. **PUSH-AFTER-EVERY-TURN.** No open PRs sitting, no hoarded work.

### Coordination Pattern

```
Owner / lead agent assigns task
    → Agent A: branch agents/task-a-20261016, works, PR, merge
    → Agent B: branch agents/task-b-20261016, works, PR, merge
    → If B depends on A: B branches from A's PR branch (not main)
    → Conflicts: keep BOTH sides, never delete the other agent's work
```

### Before Starting Any Work

Every agent (human or AI) checks:
1. `git log --oneline -5` — what's landed recently?
2. `gh pr list --state open` — any open PRs in my area? Don't duplicate.
3. Checkpoints: `~/workspace/agent-ops/checkpoints/` — is another lane on this?

This is the **CHECK-BEFORE-STARTING LAW**. No duplicate sessions. If something's running, stand down.

### AGENTS.md Is the Contract

`agy` reads `AGENTS.md` natively. Aider reads it via repo context. OpenCode picks it up too. The laws live in **one place** (`~/workspace/cape-jones/AGENTS.md`) — every agent sees the same rules. When the owner adds a law, it propagates to all agents automatically. No per-tool config duplication.

### What Each Agent Is For

| Task | Use |
|------|-----|
| Multi-file refactor, research + code | `agy` (subagents work in parallel) |
| Quick terminal edit with plugin support | `opencode` |
| Surgical single-file edit with diff review | `aider` |
| GPU render / interpolation / body replacement | Kaggle queue or Colab (NOT coding agents) |
| Verifying a claim | `production/pipeline/verify_claim.py` (not an agent's word) |

### Anti-Patterns (Don't Do These)

- ❌ Two agents editing the same files on different branches → merge conflicts. Coordinate first.
- ❌ Agent reports "done" without verifying → use `verify_claim.py`, tag confidence honestly.
- ❌ Agent agrees "it's lost" without checking its own lane → ANTI-SYCOPHANCY RULE.
- ❌ Pushing directly to `main` → always branch → PR → merge.
- ❌ Using a coding agent for GPU compute → they write pipeline code; Kaggle/Colab run it.

---

## Auth Status (2026-10-16)

| Agent | Installed | Authenticated | Blocker |
|-------|-----------|---------------|---------|
| `agy` 1.4.0 | ✅ `~/.local/bin/agy` | ❌ Needs Google OAuth | **Browser task needed**: run `agy`, sign in with fmmg.mars@gmail.com |
| `opencode` 1.19.3 | ✅ `~/.local/bin/opencode` | ⚠️ Needs API key | Set `GEMINI_API_KEY` or `GROQ_API_KEY` (free tiers, no browser needed) |
| `aider` 0.86.2 | ✅ `~/workspace/tools/aider-venv/` | ⚠️ Needs API key | Same as opencode — `GEMINI_API_KEY` |

---

## Quick Start (After Auth)

```bash
cd ~/workspace/cape-jones

# agy: full task with subagents
agy -p "research 2026 cartoon upscalers and wire the best one into production/pipeline/"

# opencode: quick edit
export GEMINI_API_KEY=<redacted>
opencode run "add input validation to led_scene_assembler.py"

# aider: surgical edit
export GEMINI_API_KEY=<redacted>
~/workspace/tools/aider-venv/bin/aider
# > fix the off-by-one in grades.py
```

All three respect the repo's branch → PR → merge flow. All three read AGENTS.md.

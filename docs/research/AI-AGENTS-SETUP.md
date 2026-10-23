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
| **Cline** (`cline`) | 3.0.72 CLI / 4.1.25 ext | Apache-2.0 | Free (bring your own API key) | Autonomous multi-file tasks, Plan/Act modes, MCP, headless CI |

All four read the repo's `AGENTS.md` — the laws apply to them automatically.

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

## 4. Cline — Autonomous Coding Agent (CLI + VS Code/code-server extension)

**Owner-requested (2026-10-16):** "get in that... Klein C L I N E... hook up... get that on the work also."

Apache 2.0, ~66k GitHub stars, 8M+ installs. Autonomous agent: reads the whole project, plans multi-file changes, runs terminal commands, iterates — with human-in-the-loop approval gates. Supports 15+ providers (Anthropic, OpenAI, OpenRouter, **Google Gemini**, **Groq**, AWS Bedrock, Cerebras, Ollama local) — bring your own free-tier key.

**Two installs (both verified working 2026-10-16):**

CLI (headless — scripts, CI, terminal):
```bash
npm i -g cline        # → 3.0.72 at /usr/bin/cline (Bun binary)
cline --version
```

VS Code extension (inside code-server — browser/phone IDE):
```bash
# Extension ID is still the original marketplace slug:
code-server --install-extension saoudrizwan.claude-dev   # → v4.1.25
```
Then in code-server's Cline sidebar: pick provider (Gemini or Groq), paste the free-tier key, choose model. The owner can drive Cline from his phone through code-server.

**Auth (pick one):**
```bash
# One-time interactive (persists to ~/.cline):
cline auth gemini        # paste Gemini key when prompted

# Or per-run, no persistence (good for scripts):
cline -P gemini -k "$GEMINI_API_KEY" -m "gemini-2.5-flash" "your task here"
cline -P groq   -k "$GROQ_API_KEY"   -m "llama-3.3-70b-versatile" "your task here"
```

**Why it's different from the other three:**
- **Plan/Act dual mode**: `-p` drafts a strategy before touching code. Best of the four for big refactors you want to review first.
- **Checkpoints**: every edit is undoable. Safer than `agy --mode accept-edits`.
- **`--worktree`**: auto-creates a detached git worktree per task — matches our branch-per-task law natively. The agent works isolated; you merge via PR.
- **MCP + Skills marketplace**: install MCP servers / Skills from inside Cline (DBs, APIs, CI).
- **Kanban**: `cline --kanban` tracks agent tasks across a session.
- **ACP mode** (`--acp`): editor-integration protocol.

**Usage:**
```bash
cd ~/workspace/cape-jones

# Plan first (review before it touches anything)
cline -p "design the One-to-All body-replacement pipeline wiring"

# Act (auto-approve on — use for sandboxed/trusted runs only)
cline "wire the One-to-All notebook outputs into finish.py"

# Isolated worktree (no clobber risk — separate checkout)
cline --worktree "add retry logic to kaggle_queue.py"

# JSON output for scripting
cline --json "list all TODO comments in production/pipeline/"
```

**Key flags:**
| Flag | What |
|------|------|
| `-p` / `--plan` | Plan mode — propose, don't execute |
| `-y` / `--yolo` | Auto-approve limited toolset (benchmarks/CI only — DANGEROUS, sandboxed envs only) |
| `--auto-approve <bool>` | Tool auto-approval (default true on CLI — set false for review) |
| `-P` / `--provider` | Provider id (`gemini`, `groq`, `openrouter`, `anthropic`, ...) |
| `-k` / `--key` | API key for this run (also saved as provider's key) |
| `-m` / `--model` | Model id |
| `-c` / `--cwd` | Working directory |
| `--worktree` | Detached git worktree per task |
| `--json` | JSON output for scripting |
| `-i` / `--tui` | Interactive terminal UI |

**GPU note (same as the others):** coding agent, not compute. Writes pipeline code; Kaggle/Colab run the GPUs.

**Safety note:** CLI defaults `--auto-approve` to **true**. For repo work under our laws, prefer `cline -p` (plan) or `--auto-approve false` so every file edit goes through review before landing — matches VERIFY-BEFORE-CLAIMING.

**Laws wiring:** Cline reads `.clinerules` at the repo root (committed in this PR) — it points at `AGENTS.md` as the law book and restates the non-negotiables (branch → PR → merge, verify-before-claiming, check-before-starting). One contract, all agents.

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
| Autonomous multi-file task, plan-then-act, isolated worktree | `cline` (Plan mode for review, `--worktree` for isolation) |
| GPU render / interpolation / body replacement | Kaggle queue or Colab (NOT coding agents) |
| Verifying a claim | `production/pipeline/verify_claim.py` (not an agent's word) |

### Anti-Patterns (Don't Do These)

- ❌ Two agents editing the same files on different branches → merge conflicts. Coordinate first.
- ❌ Agent reports "done" without verifying → use `verify_claim.py`, tag confidence honestly.
- ❌ Agent agrees "it's lost" without checking its own lane → ANTI-SYCOPHANCY RULE.
- ❌ Pushing directly to `main` → always branch → PR → merge.
- ❌ Using a coding agent for GPU compute → they write pipeline code; Kaggle/Colab run it.
- ❌ Running `cline` CLI with default auto-approve on repo work → use `-p` plan mode or `--auto-approve false`; every edit reviewed before it lands (VERIFY-BEFORE-CLAIMING).

---

## Auth Status (2026-10-16)

| Agent | Installed | Authenticated | Blocker |
|-------|-----------|---------------|---------|
| `agy` 1.4.0 | ✅ `~/.local/bin/agy` | ❌ Needs Google OAuth | **Browser task needed**: run `agy`, sign in with fmmg.mars@gmail.com |
| `opencode` 1.19.3 | ✅ `~/.local/bin/opencode` | ⚠️ Needs API key | Set `GEMINI_API_KEY` or `GROQ_API_KEY` (free tiers, no browser needed) |
| `aider` 0.86.2 | ✅ `~/workspace/tools/aider-venv/` | ⚠️ Needs API key | Same as opencode — `GEMINI_API_KEY` |
| `cline` 3.0.72 / ext 4.1.25 | ✅ `/usr/bin/cline` + code-server ext | ⚠️ Needs API key | `cline auth gemini` once, or per-run `-P gemini -k "$GEMINI_API_KEY"` |

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

# cline: plan first, then act
export GEMINI_API_KEY=<redacted>
cline -p "design the LED scene assembler refactor"   # review the plan
cline "implement the approved refactor"              # act (review each edit)
```

All four respect the repo's branch → PR → merge flow. All four read AGENTS.md.

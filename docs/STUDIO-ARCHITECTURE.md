# Cape Jones Studio Architecture — "Studio in a Box"

**One repo. Every tool wired together. No manual homework.**

This doc is the map of how all studio components connect: GPU lanes, the queue,
the reliability layer, the research layer, and the dev tools. For the
frame-by-frame animation pipeline itself, see `docs/COMPLETE-PIPELINE.md`.
For dev-environment setup details (Colab sign-in, Aider, code-server), see
`docs/research/DEVENV-SETUP.md`.

Owner constraint that shapes everything: **he is phone-only**. Every component
here must be operable by agents without him touching a computer — except the
two things that genuinely need him (Google phone 2FA, payment). That's the
PHONE-BRIDGE law, and it's why the queue is autonomous and the IDE is in a browser.

---

## Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                              │
│  agents (main + subagents) → claim_gate.py → status reports    │
│  research.py → docs/research/ → pull-in → PR → main            │
└──────────────┬──────────────────────────────────────────────────┘
               │ jobs in
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│  kaggle_queue.py (systemd timer, every 15 min)                  │
│    validate_job() → push → monitor → download → claim gate     │
│    → second copies (GitHub release / TeraBox)                   │
│  checkpoint_audit.py (stale-work watchdog, every 15 min)        │
└──────┬──────────────────────────────┬───────────────────────────┘
       │ primary GPU lane             │ fallback GPU lane
       ▼                              ▼
┌──────────────────┐          ┌──────────────────┐
│  KAGGLE (T4 x2)  │          │  COLAB (T4)      │
│  30h/week free   │          │  ~4h/session     │
│  queue-automated │          │  manual Run All  │
│  dataset cache   │          │  HF re-download  │
│  save_outputs.py │          │  files.download()│
│  in-kernel       │          │  immediately     │
└──────────────────┘          └──────────────────┘
       ▲                              ▲
       │   notebook generators        │
       │   production/kaggle/*/gen_*.py│
       │   production/colab/gen_*.py  │
       └──────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     DEV TOOLS LAYER                             │
│  Aider (terminal pair programmer, repo-native)                  │
│  code-server (browser VS Code — phone-accessible)               │
│  OpenCode / Gemini CLI (documented alternatives)               │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                   RELIABILITY LAYER (always on)                 │
│  claim_gate.py ......... blocks unverified "done" reports      │
│  verify_claim.py ........ checks files / PRs / releases / cmds │
│  contradiction_probe.py . "what would prove this false?"      │
│  checkpoint_audit.py .... finds stale "running" checkpoints   │
│  save_outputs.py ........ in-kernel dataset publishing        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. GPU Lanes

| Lane | GPU | Free quota | Automation | Model cache | Output safety |
|------|-----|-----------|------------|-------------|---------------|
| **Kaggle** (primary) | T4 x2 | 30h/week | Full — `kaggle_queue.py` | Kaggle datasets (persistent) | `save_outputs.py` → dataset versions |
| **Colab** (backup/parallel) | T4 | ~4h/session | Manual — upload + Run All | Re-download per session (or Drive) | `files.download()` immediately |
| **Lightning AI** (tertiary) | T4/A100/H100 | 15 credits/mo | Manual | — | Manual download |

**Routing rule:** Kaggle first, always. Colab when Kaggle quota is low, Kaggle
is erroring, or two jobs need to run in parallel. Lightning AI for overflow
(signup via Google is a browser task — see DEVENV-SETUP.md).

**Colab notebooks** (`production/colab/`, generators `gen_*_colab.py`):
- `cape_jones_tooncrafter_colab.ipynb` — ToonCrafter interpolation
- `cape_jones_viggle_colab.ipynb` — Viggle-Animate body replacement
- `cape_jones_lighting_reel_colab.ipynb` — Blender lighting reel

**Kaggle → Colab handoff:** the Colab notebooks are ports of the Kaggle
generators (`production/kaggle/*/gen_notebook.py`). Same inputs, same expected
outputs. If a Kaggle job keeps failing, the fallback is: upload the matching
`production/colab/*.ipynb` to Colab, Runtime → T4 GPU → Run All, download the
output immediately. No code changes needed — the handoff is notebook-for-notebook.

---

## 2. Orchestration — `kaggle_queue.py`

The queue is the studio's foreman. Systemd timer runs `tick` every 15 min:

1. **CHECK** — `validate_job()` on every pending job before push: notebook
   exists, all code cells compile, title resolves to the kernel slug
   (Kaggle API 400s otherwise), dataset slugs well-formed. Invalid jobs fail
   fast with a clear error — never a wasted GPU run.
2. **PUSH** — `kaggle kernels push` with `save_outputs.py` shipped in the
   kernel dir, saver-setup cell injected after the leading markdown, and a
   final-checkpoint cell appended as the last cell.
3. **MONITOR** — poll job status via Kaggle API each tick.
4. **DOWNLOAD** — on completion, pull expected outputs to the VM.
5. **VERIFY** — completion report runs through `claim_gate.py`. Evidence =
   the downloaded files. Blocked gates set `verification_warning` on the job.
6. **SECOND COPIES** — push outputs to GitHub release (`--gh-repo`,
   `--gh-release-tag`) and/or TeraBox (`--terabox-dir`). Credentials live on
   the VM, never in the kernel.

Queue state: `~/workspace/agent-ops/kaggle-queue.json` (VM-local, active work
file). Log: `~/workspace/agent-ops/kaggle-queue.log`.

**Aider → queue handoff:** when a job fails, the fix loop is: read the error
→ fix the generator with Aider (or by hand) → regenerate the notebook →
`kaggle_queue.py retry <job-id>`. The generator is the source of truth
(`gen_*.py`), never the `.ipynb` — always regenerate, never hand-edit.

---

## 3. Reliability Layer — always on, never optional

These run on every job, every report, every turn. They are the reason the
2026-10-16 failure class (unverified claims, lost renders) doesn't repeat.

| Tool | Where it runs | What it enforces |
|------|---------------|------------------|
| `save_outputs.py` | Inside every Kaggle kernel | Dataset version published after EVERY checkpoint. Survives session death. **NEVER-QUICK-SAVE**: Quick Save preserves 0 output files — only commits do. |
| `claim_gate.py` | Queue completion + agent reports | Splits reports into atomic claims; blocks any "done" without evidence. Exit 0 = pass, 1 = blocked. |
| `verify_claim.py` | Agent verification step | Checks files (exist/size/sha256), GitHub PRs (merged?), releases (published?), shell commands. Exit 0 = VERIFIED, 1 = UNVERIFIED, 2 = CONTRADICTED. |
| `contradiction_probe.py` | Before "done" reports | "What evidence would prove this FALSE?" Blocks until answered. |
| `checkpoint_audit.py` | Worker-watchdog cron (15 min) | Finds checkpoints claiming "running" with no live process/heartbeat. Marks stale ones `needs_owner`. |

**The order of operations (CHECK-RESEARCH-WIRE-DO law):** check the real
state → research the gap → wire the fix into the repo → then do the work.
Doing first and researching after the failure is what burned 16 GPU hours on
2026-10-16. The queue's `validate_job()` is this law in code.

---

## 4. Research Layer — `research.py`

**RESEARCH-BEFORE-ANSWER law:** never guess from training data on
time-sensitive or "best X" questions. `production/pipeline/research.py`
queries GitHub trending, GitHub search, and HN, then ranks.

```
python3 production/pipeline/research.py compare "cartoon interpolation 2026"
```

**RESEARCH-TO-REPO law:** every finding lands in `docs/research/` AND gets
wired up or honestly excluded (license, etc.). A finding without a pull-in is
incomplete work. The master index is `docs/research/RESEARCH-INDEX.md`.

**Research → pipeline handoff:** research doc → candidate tool →
license check → pull into `production/tools/` or `production/pipeline/` →
wire up → test → branch → PR → merge. The 2026 pulls that built this studio
(LDF-VFI, One-to-All Animation, anime-upscaling, Kandinsky 6.0, LuxTTS,
LatentSync, OpenColorIO candidates) all followed this path.

---

## 5. Dev Tools Layer

| Tool | What | Where | Status |
|------|------|-------|--------|
| **Aider** | Terminal AI pair programmer, repo-native | `~/workspace/tools/aider-venv/bin/aider` (v0.86.2) | Installed + verified |
| **code-server** | Full VS Code in browser (phone-accessible) | `~/.local/bin/code-server` | Installed |
| **OpenCode** | Aider successor (189k stars, MIT) | `production/devtools/opencode/` | Source pulled, evaluate |
| **Gemini CLI** | 1000 free req/day on Google login | documented | Not installed |

**Aider config** (`.aider.conf.yml`, repo root): model `gemini/gemini-2.0-flash`
(free tier), `auto-commits: false` (human reviews everything), `watch-files:
true`, `show-diffs: true`. Needs `GEMINI_API_KEY` (free at aistudio.google.com)
— **browser task**: generate the key, owner pastes it once.

**Aider → PR handoff:** Aider edits code in the repo checkout → agent reviews
the diff → `git checkout -b` → commit → `gh pr create` → merge when green.
Aider never pushes directly (auto-commits off). This is the PUSH-AFTER-EVERY-TURN
law with a human-or-agent review gate.

**code-server → repo handoff:** serves `~/workspace/cape-jones` in the
browser. The owner can view code from his phone. Not a replacement for agent
work — it's his window into the studio.

---

## 6. Config Inventory — everything lives in the repo

| Component | Config location | Notes |
|-----------|----------------|-------|
| Queue behavior | `production/pipeline/kaggle_queue.py` (args) | State is VM-local by design (active work) |
| Aider | `.aider.conf.yml` (repo root) | Model, no-auto-commit, diff review |
| In-kernel saver | `production/pipeline/save_outputs.py` | Shipped into every kernel by the queue |
| Claim gate | `production/pipeline/claim_gate.py` | Hooked into queue completion |
| Colab notebooks | `production/colab/gen_*_colab.py` | Generators = source of truth |
| Kaggle notebooks | `production/kaggle/*/gen_*.py` | Generators = source of truth |
| Model weight cache | Kaggle datasets (`marsfmmg/tooncrafter-weights`, `marsfmmg/viggle-animate-weights`) | Seeded once, attached to every run — see `docs/research/MODEL-WEIGHT-CACHING.md` |
| GPU routing | This doc (§1) + `docs/research/DEVENV-SETUP.md` | Kaggle → Colab → Lightning AI |
| Laws | `AGENTS.md` (repo root) | VERIFY-BEFORE-CLAIMING, CHECK-RESEARCH-WIRE-DO, ANTI-SYCOPHANCY, + workspace laws |

**Nothing is configured only on local disk.** If a setting matters, it's in
the repo or in a repo doc pointing at it. (Queue *state* — which jobs are
pending — is the one VM-local exception: it's live operational state, not
configuration.)

---

## 7. Failure-Recovery Map

| Failure | Detected by | Recovery |
|---------|-------------|----------|
| Kaggle job errors | Queue tick (API status) | Read error → fix generator (Aider ok) → regenerate → `retry` |
| Kaggle quota exhausted | Queue tick (quota API) | `hold` queue → route next job to Colab lane |
| Kernel session dies mid-run | Next tick (no heartbeat) | Resume from `save_outputs.py` dataset versions — attach dataset, `restore_from_input()` |
| Output lost (no dataset version) | `claim_gate.py` (no evidence) | Job flagged `verification_warning`, NOT reported done. Re-run. |
| Stale checkpoint ("running" forever) | `checkpoint_audit.py` (15-min cron) | Marked `needs_owner`, surfaced in handoff |
| Agent reports "done" unverified | `claim_gate.py` / `contradiction_probe.py` | Blocked until evidence provided |
| Colab session times out | Human/agent watching | Re-run; outputs must be `files.download()`ed immediately — Colab has no saver |
| Model weights missing on Colab | Notebook cell fails | Drive-cache lines (in notebook, commented) or re-download from HF |

---

## 8. What Still Needs a Browser (parent-agent delegation)

Subagents can't operate the live browser. These items need parent-side
browser tasks (all covered by the Google sign-in blanket permission;
phone 2FA → document and ask the owner):

1. **Colab first-run** — upload `production/colab/*.ipynb`, set T4 GPU runtime, Run All (one-time per notebook; validates the lane works).
2. **Gemini API key** — aistudio.google.com → Get API key → owner pastes once → `export GEMINI_API_KEY` for Aider.
3. **Lightning AI signup** — Google sign-in, free tier (tertiary GPU lane).
4. **code-server exposure** — if the owner wants phone access outside the VM network, needs tunnel/reverse-proxy setup (browser task to verify reachability).

---

## 9. The Laws That Hold This Together

From `AGENTS.md` (repo root) — the non-negotiables:

- **VERIFY-BEFORE-CLAIMING** — check the source of truth yourself; tag confidence.
- **CHECK-RESEARCH-WIRE-DO** — never do first and research after.
- **ANTI-SYCOPHANCY** — never agree with an unverified premise.
- **NEVER-QUICK-SAVE** — Quick Save preserves 0 files; the in-kernel saver is the only save.
- **PUSH-AFTER-EVERY-TURN** — branch → PR → merge, every turn.
- **NO-DISK-STAGING / PULL-STRAIGHT-TO-STORE** — repos and cloud are the warehouse; disk is the workbench.
- **RESEARCH-TO-REPO** — findings land in `docs/research/` AND get wired up.
- **PHONE-BRIDGE** — the owner is phone-only; agents do the computer work.

---

*Last updated: 2026-10-16. Complements `docs/COMPLETE-PIPELINE.md` (the
frame pipeline) and `docs/research/DEVENV-SETUP.md` (the setup guide).*

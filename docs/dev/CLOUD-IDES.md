# Cloud IDEs for cape-jones Blender work

Verified 2026-10-16. Real free-tier numbers, not marketing copy.
Scope: which free cloud IDEs/workstations genuinely help Blender/3D iteration.

The Blender pin for this repo is **4.5.12 LTS** (see
`docs/research/RENDER-2026-OPTIMAL.md` - LTS until July 2027,
`denoising_use_gpu` needs 4.2+). The `.devcontainer/` in this repo bakes that
exact build in.

## TL;DR

- (a) Quick Blender script iteration: **GitHub Codespaces** - free, no new
  sign-in, one click from this repo's `.devcontainer/`. CPU-only on the free
  tier, so script/logic work, not final GPU renders.
- (b) GPU test runs: **Lightning AI Studio** (~75 T4-hr/mo free, persistent,
  web VS Code) - NEEDS-PARENT-BROWSER for signup. Daytona $200 credits as a
  burst fallback. Kaggle/Colab stay the batch lanes.
- (c) Full workstation sessions: **Oracle Always Free VM + VS Code tunnel or
  code-server** - permanent, your root, no monthly hour cap. Needs parent
  browser signup (account + card identity verification is the owner's call).

## Options, verified

### GitHub Codespaces - USE (primary, no new sign-in)

- Free: **120 core-hours/month + 15 GB-month storage**, personal GitHub Free
  accounts (official billing docs). Billed in core-hours: 120 = 60 h on a
  2-core machine or 30 h on a 4-core. Spending limit can be set to $0, and
  with no payment method on file usage simply blocks at quota - no surprise
  charges. Idle auto-stop after 30 min.
- Blender: installable via this repo's `.devcontainer/` (official 4.5.12
  tarball, URL verified live 2026-10-16). Headless `-b` renders work.
- GPU: **none on the free tier.** Standard machine types are CPU-only; GPU
  machine types are paid/org paths only. Do not plan GPU renders here.
- Sign-in: GitHub - already authed (mhvnsnt), nothing new needed.
- Best for (a).

### Lightning AI Studio - USE (GPU IDE), NEEDS-PARENT-BROWSER

- Free: **~15 credits/month**. T4 GPU burns ~0.19-0.2 credits/hr, so roughly
  **~75 T4 GPU hours/month**. Persistent environment (files and env survive
  between sessions) plus a web VS Code IDE. Full Studio keeps running on CPU
  for free; switch to GPU only for render/test time.
- Blender: installable (download official tarball, apt deps); real GPU for
  Cycles test renders (CUDA/OptiX).
- Sign-in: web sign-up with email, then phone verification. Multiple reports
  of a 2-3 business-day verification wait before GPU unlocks. No credit card
  required for the free tier.
- NEEDS-PARENT-BROWSER: create the account and complete verification.
  Account to use: fmmg.mars@gmail.com (standing permission).
- Best for (b).

### Oracle Cloud Always Free - USE (permanent CPU workstation), NEEDS-PARENT-BROWSER

- Free, **permanent** (not a trial): **2 OCPU / 12 GB RAM ARM** (cut from
  4 OCPU / 24 GB on 2026-06-15, enforced Aug 2026 - most tutorials still say
  4/24, they are stale), 200 GB block storage, 10 TB egress/month.
- Traps: credit card required for identity verification (temporary hold; no
  charge while staying within Always Free limits - **owner decides**);
  instances idle 7 days can be reclaimed; "out of host capacity" is routine
  for the ARM shape; home region is fixed at signup.
- Blender: run CPU-only headless renders, or host code-server / VS Code
  tunnel for a real IDE you reach from the phone.
- NEEDS-PARENT-BROWSER: account creation + card verification. Account to
  use: fmmg.mars@gmail.com.
- Best for (c).

### VS Code Remote Tunnels - USE (free, built-in)

- Free forever, built into VS Code. Turns any VM (e.g. the Oracle box above)
  into a cloud IDE at vscode.dev. Sign in with GitHub or Microsoft account.
- One-time per host: install `code` CLI, run `code tunnel` once for device
  approval, then `code tunnel service install` for persistence across reboots.
- Pairs with code-server (already wired by the aider lane, see below) - tunnel
  for VS Code client access, code-server for pure-browser access.
- NEEDS-PARENT-BROWSER: first device approval with the GitHub account.

### Daytona - USE for burst GPU runs only

- Free: **$200 one-time compute credit on signup**, no credit card. GPU
  sandboxes available (H100 on-demand ~$2.27/hr on the live pricing page).
- But: agent-sandbox oriented, ephemeral, 15-minute default auto-stop, and
  credits burn fast at GPU rates. Not a persistent workstation. Good for
  scripted burst runs (e.g. fire a render, pull results), not daily IDE use.
- Sign-in: email/GitHub. NEEDS-PARENT-BROWSER for first account signup.
  Account: fmmg.mars@gmail.com. Watch the credit burn; no auto-spend.

### code-server - already wired (aider lane)

- `docs/research/DEVENV-SETUP.md` (PR #56) has code-server v4.141.0 verified
  with install steps. Self-hosted VS Code in a browser tab. Run it on the
  Oracle Always Free VM for a permanent browser IDE. No new sign-in beyond
  your own password.

### Google Colab - already in pipeline

- Notebooks live in `production/colab/` (aider lane). Free T4 ~10-15 h/week
  dynamic, no persistence, notebook-only editor. Keep as the prototyping GPU
  lane. Not an IDE.

### Kaggle Code as an IDE - SKIP as IDE

- Free GPU is real (30 GPU-hr/week + 20 TPU-hr/week, T4x2/P100 - owner
  already uses this) but it is a notebook editor only: no real IDE, no
  devcontainer, no persistent workstation. Stays the batch GPU lane
  (`production/kaggle/`, setup/kaggle-gpu-render worktree). Not an IDE
  candidate.

### Gitpod (now Ona) - SKIP

- Acquired by OpenAI, rebranded to Ona (ona.com), pivoted to agentic AI
  orchestration ("task in, pull request out"). Free offering is ~$10 in
  one-time starter credits, not a monthly allowance. Not a Blender
  workstation anymore.

### Replit - DO NOT USE

- Owner was burned $200 here before. No GPU on free. Not evaluated further.

### Modal - honorable mention (burst GPU, not an IDE)

- Starter tier: $30/month in free compute credits, GPU-concurrent slots.
  Serverless execution, not an IDE - but it can run burst headless Blender
  renders via CLI. Optional, not primary.

## What landed in this repo (this lane)

- `.devcontainer/Dockerfile` + `devcontainer.json` - Python 3.11,
  Blender 4.5.12 LTS pinned (URL verified live), Python + Blender Development
  + Jupyter extensions. One-click Codespaces.
- `.vscode/settings.json` - Blender-aware Python (Blender's bundled python
  path documented, fake-bpy autocomplete enabled), editor defaults.
- `.vscode/extensions.json` - Python, Blender Development, Jupyter.
- `.vscode/launch.json` - run current script inside Blender headless, plus
  plain-python config for repo tooling.
- `.editorconfig` - matches existing repo style (4-space Python, 2-space
  YAML/JSON/Markdown, LF).
- `.vscode/` is owned by this lane; the aider lane was told not to touch it.

## NEEDS-PARENT-BROWSER checklist

1. Lightning AI Studio - account + phone verification (2-3 day wait reported).
2. Daytona - first account signup.
3. Oracle Cloud - account creation + card identity verification (owner call).
4. VS Code tunnel - first device approval (during Oracle VM setup).

All under fmmg.mars@gmail.com per the standing Google sign-in permission.
Free tiers only - nothing here costs money; where a credit card appears
(Oracle), it is flagged, not used.

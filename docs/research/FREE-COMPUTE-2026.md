# FREE-COMPUTE-2026.md — Solving Our Compute Problem (2026-10-18)

**Why this doc exists:** We keep hitting the same wall — Kaggle kernels cancelled in minutes, Colab browser automation failed, our VM has no GPU, and daemon restarts kill long renders. The owner ordered: "pull in some shit for the compute issue and wire it up into the repo and into the workflow... research on the best 2026 stuff — new stuff or legacy stuff."

**Builds on:** `CLOUD-RESEARCH.md` (2026-10-16, free IDEs/GPUs) and `RENDER-2026-OPTIMAL.md` (2026-10-16, fastest free Blender pipeline). This doc is the *reliability* companion: how we stop losing renders.

---

## 1. THE PROBLEMS (all real, all recent)

| # | Problem | What happened |
|---|---------|---------------|
| 1 | **Kaggle scheduler cancels kernels** | v8–v11 went RUNNING → CANCEL_ACKNOWLEDGED in minutes, zero output, quota fine (17min/6h used). Started after rapid version pushes. v7 proved the pipeline runs on 2×T4. |
| 2 | **Colab browser automation failed** | Browser infra couldn't open any tab — no way to drive Colab's interactive UI as a subagent. |
| 3 | **VM has no GPU** | 2 CPUs, 8GB RAM. Local Blender = CPU-only, slow. |
| 4 | **Daemon restarts kill renders** | 7 kills on one turntable job. Any render longer than the daemon's mood dies. |

**Design principle from here on:** every render job must be *resume-safe* (per-frame checkpointing, skip-done) and *queue-driven* (a manager hands out chunks; dead workers just re-queue). No more fire-and-forget 3-hour runs.

---

## 2. FREE GPU LANDSCAPE — 2026 VERIFIED RANKING

Ranked for OUR use case: Blender Cycles GPU renders, cloth bakes, ML deformation, automation-friendly.

### Tier 1 — Wire up NOW

| Service | Free GPU | Allowance | No-card? | Automation | Verdict |
|---------|----------|-----------|----------|------------|---------|
| **Kaggle** | 2× T4 (16GB each) | ~30 GPU-hrs/week, 12h max/run | ✅ | ✅ CLI/API | **WORKHORSE.** Already wired. Fix = operational discipline (see `kaggle-ops.md`). |
| **Lightning AI Studio** | T4 / L4 / A10G / L40S | ~15 credits/mo ≈ 22 T4-hrs; up to ~80 free GPU-hrs after phone verify; 5 credits on signup + 25 with card | ✅ base | ✅ API + VS Code | **BEST NEW WIRE-UP.** Persistent disk (unlike Colab/Kaggle reset), 4h restarts on free plan, 50–100GB storage. Signup: lightning.ai/sign-up. Phone verify = GPU hours. **Owner action needed: sign up + phone verify** (open signup item). |
| **SheepIt** | Community (CPU+GPU, CUDA/OptiX) | Free, point system — earn ~4× what you contribute; starter points for new users | ✅ | ✅ client CLI | **BEST FREE RENDER FARM.** Run the headless client on OUR VM to earn points 24/7 (CPU), spend on GPU renders. No NDA-sensitive work (volunteers see thumbnails). **Owner action needed: create account** (open signup item). |

### Tier 2 — Worth having

| Service | Free GPU | Allowance | Notes |
|---------|----------|-----------|-------|
| **Google Colab free** | T4 (unnamed, users report T4) | Opaque quota, 12h max, idle timeouts | Interactive-only; our browser automation failed. Keep as manual fallback via owner's browser. |
| **Paperspace Gradient free** | M4000 (weak, Kepler-era) | 5GB storage, 6h auto-shutdown | GPU too old for OptiX; CPU fallback only. Weak. |
| **Modal starter** | Various (serverless) | $30/mo free compute, per-second | Code-first serverless, not notebooks. Good for render *functions* — a render job as a Modal function with checkpointing is a real option. Needs signup. |

### Tier 3 — Dead ends for us (documented so nobody retries)

| Service | Why not |
|---------|---------|
| HF ZeroGPU | 5 min/day, Gradio Spaces only. Not a render target. |
| SageMaker Studio Lab | Closed to new users (July 2026). |
| Oracle Always Free | No GPU. Card verification = owner's call, not done. |
| Cerebras / DeepInfra | Need cards. Stopped per owner. |
| RunPod / Vast.ai / Lambda / Thunder | No free tier (paid only). Documented for the day there's budget. |

---

## 3. THE KAGGLE CANCELLATION PROBLEM — what we know

**Symptoms:** kernels pushed via rapid version succession (v8–v11) cancelled within minutes with CANCEL_ACKNOWLEDGED, zero log output, quota untouched.

**No public root-cause found** (searched 2026-10-18 — no matching reports; Kaggle doesn't document this status).

**Working theory:** anti-abuse/session limiter tripped by many pushes in quick succession, or an external cancellation. v7 (pushed normally) ran fine.

**Mitigations (wired into `kaggle-ops.md`):**
1. **Space pushes ≥30 min apart.** Never push v+1 while v is still initializing.
2. **One active kernel per task.** Cancel the old one explicitly before pushing the new.
3. **Prefer the Kaggle API/CLI over web pushes** — `kaggle kernels push` is the same path every time.
4. **Checkpoint to datasets** — every kernel writes frames to `/kaggle/working` AND uploads incrementally; a cancelled run loses nothing already checkpointed.
5. **Resume-safe scripts** — the kernel skips frames already in the output dataset (see `cj-render.py` pattern).
6. **If cancellations persist >24h:** stop pushing, switch to Lightning AI / SheepIt, retry Kaggle after a cooldown.

---

## 4. RENDER QUEUE TECH — stop losing work to restarts

### Flamenco (Blender's own, OSS) — the answer for queue-driven rendering
- **What:** Blender Studio's official render manager. Manager (queue, web dashboard, chunking) + Worker (polls for work, runs Blender, reports progress). Single Go binaries, no DB, no K8s.
- **Why it solves our problem:** jobs split into frame-chunks; a dead worker's chunk **retries on another worker**; 3 failures → worker blocklisted for that job. Daemon restarts just re-queue chunks.
- **Fits us:** manager runs on our VM; workers run on our VM (CPU) + any cloud GPU we wire up (Lightning/Kaggle/Colab each run a Flamenco worker against our manager via the existing Tailscale network).
- **Setup:** `production/pipeline/compute/flamenco-setup.md`.
- **Upstream:** https://flamenco.blender.org (official), https://projects.blender.org/studio/flamenco-orchestra (Blender Studio's cloud deployment reference).

### `cj-render.py` — resume-safe render CLI (wired, in this repo)
Generalizes the proven `~/workspace/turntable_render.py` pattern:
- Renders a frame range with **per-frame checkpointing** (done-frames manifest; skips existing on restart).
- Targets: `local` (xvfb-run CPU), `flamenco` (submit chunks to the manager), `kaggle` (generates the kernel payload).
- Survives daemon restarts by design: re-run the same command, it picks up where it died.
- Location: `production/pipeline/compute/cj-render.py`.

### Checkpoint discipline (law for all render lanes)
1. Every render writes frames to a **persistent dir** (never /tmp).
2. Every render keeps a **done-manifest** (`frames_done.json`).
3. Every render script **skips done frames** on start.
4. Long jobs go through **Flamenco or cj-render**, never bare `blender -b` in a 3-hour exec.

---

## 5. WHAT GOT WIRED (this PR)

```
production/pipeline/compute/
├── COMPUTE-README.md        # index: what to use when
├── cj-render.py             # resume-safe render queue CLI (local/flamenco/kaggle)
├── kaggle-ops.md            # Kaggle cancellation mitigations + push discipline
├── lightning-ai-setup.md    # signup guide + Studio bootstrap for renders
├── sheepit-setup.md         # signup + headless client + job packaging
└── flamenco-setup.md        # pull + configure Flamenco manager/worker
docs/research/FREE-COMPUTE-2026.md  # this file
```

## 6. OWNER ACTIONS NEEDED (the two open signups)

1. **Lightning AI** — sign up at lightning.ai, verify phone → up to ~80 free GPU hours + 15 credits/mo. This is our best new GPU wire-up.
2. **SheepIt** — create account at sheepit-renderfarm.com → we run the headless client on our VM earning points 24/7, spend on GPU renders.

Both are no-card, free, and take minutes. Everything else is already wired and waiting.

---

*Research: web, 2026-10-18. Cross-checked across gpuperhour.com (Sep 2026), thundercompute.com (Oct 2026), opsnexusai.com, freetokens.custats.info (Sep 2026), superrendersfarm.com, dev.to render-cost benchmarks (Oct 2026).*

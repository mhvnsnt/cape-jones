# Cloud Research — Free Cloud Open-Source IDEs, GPUs, and Services (2026)

Deep research conducted 2026-10-16. Sources: GitHub trending, Product Hunt, Hacker News,
2026 roundup articles, dev.to, Medium, spheron.network GPU comparison (Oct 2026).

---

## 1. FREE CLOUD OPEN-SOURCE IDEs — Ranked

### Tier 1: Pull These First

| Rank | Tool | Stars | License | What | Browser? | Setup |
|------|------|-------|---------|------|----------|-------|
| 1 | **code-server** | ~70k+ | MIT | Full VS Code in any browser. Self-host on any Linux box. Password auth built in. Lower RAM than alternatives. | Yes | `curl -fsSL https://code-server.dev/install.sh \| sh` |
| 2 | **OpenVSCode Server** | — | MIT | Gitpod's maintained VS Code server. Better extension compat than code-server. Higher RAM (~500MB-1GB). | Yes | `docker run -p 3000:3000 gitpod/openvscode-server` |
| 3 | **Coder** | ~25k+ | AGPL-3.0 | Self-hosted cloud dev environments via Terraform. Secure tunnels, idle shutdown, AI agent integration. | Yes | Self-host (2-4 day setup) or coder.com cloud |

### Tier 2: Worth Knowing

| Tool | License | What |
|------|---------|------|
| **Eclipse Theia** | EPL-2.0 | Framework behind Gitpod. Build custom browser IDEs. |
| **DevPod** | Apache-2.0 | Client-only, launches devcontainers on any cloud/K8s/Docker. No vendor lock-in. |
| **Daytona** | AGPL-3.0 | AI agent sandboxes, sub-90ms creation. Built for agent workloads. |
| **Eclipse Che** | EPL-2.0 | Kubernetes-native, Red Hat backed. Free self-hosted. |

### Cloud-Hosted (Free Tier, Not Self-Hosted)

| Tool | Free Tier | Notes |
|------|-----------|-------|
| **Gitpod/Ona** | 3 parallel envs, 4vCPU/16GB/80GB | Zero setup, 30-60s startup. Prebuilds. |
| **CodeSandbox** | Unlimited public sandboxes, 40hr VM/month | Great for web projects. |
| **Daytona** | $10 free credits/month (~200 core-hours) | Best free compute for dev envs. |
| **GitHub Codespaces** | Free tier for personal accounts | 60hrs/month on 2-core. GitHub login. |

**Recommendation for us:** code-server on our VM = instant browser IDE for the owner.
Gitpod for zero-setup cloud workspaces. Daytona's $10/mo free credits for agent sandboxes.

---

## 2. OPEN-SOURCE AI CODING ASSISTANTS — Ranked by Stars (July 2026 data)

| Rank | Tool | Stars | License | Type | Why It Matters |
|------|------|-------|---------|------|----------------|
| 1 | **OpenCode** | 189k | MIT | Terminal agent | MOST-STARRED. 75+ LLM providers, no git required. The Aider successor. |
| 2 | **Gemini CLI** | 105k | Apache-2.0 | Terminal | FREE daily quota (60 req/min, 1000/day) on Google account. No API key needed. |
| 3 | **Cline** | 65k | Apache-2.0 | VS Code/JetBrains agent | Most actively maintained. MCP support. Autonomous edits. |
| 4 | **Goose** | 52k | Apache-2.0 | CLI + Desktop | Block (ex-Twitter) backed. 70+ MCP extensions. |
| 5 | **Aider** | 48k | Apache-2.0 | Terminal pair programmer | Git-native. Last release Feb 2026 — slowing down. |
| 6 | **Kilo Code** | 20k | MIT | IDE + CLI | 500+ models, BYOK at provider rates. |
| 7 | **Roo Code** | 24k | Apache-2.0 | VS Code agent | Configurable agent modes. |

**Key insight:** OpenCode (189k stars) has overtaken Aider. Gemini CLI gives free daily AI coding
with just a Google login — no API key. Cline is the most actively maintained IDE agent.

**Recommendation:** Pull OpenCode + Gemini CLI. OpenCode for terminal work, Gemini CLI for free
daily AI coding on the owner's Google account.

---

## 3. FREE CLOUD GPU SERVICES — Beyond Kaggle/Colab (2026)

| Service | Free GPU | Free Hours | Card? | Best For |
|---------|----------|------------|-------|----------|
| **Kaggle** | T4 x2 (16GB) | 30 hrs/week | No | Our main GPU. Notebooks. |
| **Google Colab** | T4 | ~4 hrs/session | No | Quick experiments. Unreliable for long runs. |
| **Lightning AI** | T4 (free), A100/H100 (credits) | 15 credits/mo (~22 T4 hrs) | No | **Closest to "Colab with A100".** Real terminal, persistent. |
| **Hugging Face ZeroGPU** | RTX PRO 6000 Blackwell (48GB) | Limited daily quota | No | Gradio demos on high-end GPUs. |
| **Paperspace Gradient** | M4000 (8GB) | Limited | Yes | MLOps pipelines. |
| **Saturn Cloud** | T4 | 30 hrs/month | Yes | Dask + ML. |
| **SageMaker Studio Lab** | T4 | 4hr/session | No | **Closing to new signups July 2026.** Skip. |

**Key insight:** Lightning AI free tier is the best "third GPU" — real Linux terminal
(unlike Colab/Kaggle's managed kernels), persistent storage, and the free credits can
access A100/H100 (not just T4).

**Recommendation:** Set up Lightning AI as our third GPU source. Use for Blender renders
and long-running jobs that need a real terminal.

---

## 4. FREE BLENDER RENDER FARMS

| Service | Model | What You Get |
|---------|-------|--------------|
| **SheepIt** | Community (free forever) | Contribute idle CPU → earn points → spend on your renders. 600+ volunteer machines. Cycles/Eevee/Workbench. Best for non-urgent personal projects. |
| **GarageFarm.NET** | Free trial credits (~$25) | Commercial hardware, predictable times. One-shot trial. |
| **RenderStreet** | Free trial | Test before committing. Cycles/Eevee support. |
| **Fox Render Farm** | $25 free credits (new users) | Commercial, for evaluation. |

**Key insight:** SheepIt is the ONLY truly free ongoing option. You earn by contributing.
For our animation pipeline: SheepIt for overflow/background renders, Kaggle/Colab for urgent.

**Recommendation:** Sign up for SheepIt. Run the client on our VM during idle hours to
bank points, spend them on Cape Jones renders.

---

## 5. BROWSER-BASED 3D SOFTWARE (Free)

| Tool | License | What | Relevance |
|------|---------|------|-----------|
| **KoKraft** | Open source | Browser-based 3D modeling, real-time. GitHub: sengchor/kokraf | Quick 3D edits without Blender install. |
| **Spline** | Freemium | "Figma of 3D." Modeling, materials, animation, web embeds. | Landing pages, portfolio pieces. |
| **Clara.io** | Freemium | Full browser 3D: modeling, animation, rendering. Free tier. | Full 3D in browser. |
| **Tinkercad** | Free | Absolute beginner, drag-and-drop. | Too simple for our needs. Skip. |
| **SketchUp Free** | Free (Trimble ID) | Architecture/interiors, browser-based. | Set design reference. |

**Recommendation:** KoKraft is the open-source pick. Spline for quick web 3D.

---

## 6. BROWSER-BASED VIDEO EDITING (Open Source, 2026)

This is where the research really paid off — several NEW 2026 projects:

| Tool | License | What | Status |
|------|---------|------|--------|
| **OpenReel Video** | MIT | "Open-source CapCut." 100% browser, WebGPU+WebCodecs, 4K export, AI subtitles (90+ languages), DaVinci-style color grading, chroma key. | Live at openreel.video |
| **Opencut** | MIT | Browser timeline editor, Rust+WASM core, 4K scrubbing. No watermarks, no limits. | Alpha live at opencut.fun |
| **video-ware** | Open source | Browser editor + **CLI designed for AI agents** (`vw timeline doctor`). Speech-to-text search, proxy generation. Docker deploy. | Active |
| **ESCAPE Suite** | MIT | Recorder + editor, single HTML file, air-gapped capable. | Live at escapesuite.io |

**Key insight:** OpenReel Video is the standout — MIT licensed, 4K, GPU-accelerated, runs
entirely in browser. video-ware is unique for having a CLI built for AI agent interaction.

**Recommendation:** Pull OpenReel Video. It could replace a lot of our FFmpeg pipeline
for quick edits.

---

## 7. NEW 2025-2026 FINDS (Less Well-Known)

| Tool | What | Why It's Interesting |
|------|------|---------------------|
| **Daytona** | AI agent sandboxes ($10/mo free) | Built specifically for AI agent workloads. Sub-90ms sandbox creation. |
| **ECC** | 71 agents + 311 skills framework | Trending #3 on GitHub today. Agent orchestration. |
| **XERJ** | Local search for coding agents | Hands agent exact passages instead of whole files. $1.58 vs $11.18. |
| **Context Mode** | MCP server, sandboxed tool output | 315KB → 5.4KB (98% context reduction). |
| **KoKraft** | Open-source browser 3D modeling | New, real-time, GitHub-hosted. |

---

## PULLED (This Research Round)

- [x] **OpenReel Video** — ~/workspace/tools/openreel-video/ (MIT, 58MB) — verified, README + apps dir present
- [x] **video-ware** — ~/workspace/tools/video-ware/ (open source, 17MB) — verified, CLI README present
- [ ] **OpenCode** — FAILED (network too flaky, clone timed out 2x). Retry when stable. Repo: github.com/sst/opencode (redirects to anomalyco/opencode). MIT, 189k stars.
- [ ] **code-server** — documented, install on demand (MIT). Install: `curl -fsSL https://code-server.dev/install.sh | sh`

## SETUP NEEDED (Browser/Account)

- [ ] Lightning AI — sign up with fmmg.mars@gmail.com, verify free tier
- [ ] SheepIt — sign up, install client, start earning points
- [ ] Gitpod — connect GitHub, test workspace
- [ ] Daytona — claim $10/mo free credits

## SOURCES

- GitHub trending (Oct 16, 2026)
- spheron.network GPU comparison (Oct 2026)
- morphllm.com AI coding assistant rankings (July 2026)
- devventa.com (Aug 2026)
- olud.ai (2026)
- ishandutta2007/awesome-cloud-ide-platform
- dev.to render farm guides (Oct 2026)

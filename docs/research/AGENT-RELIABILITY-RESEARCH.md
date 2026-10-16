# Agent Reliability Research — Open-Source Tools, 2026

Researched 2026-10-16. Star counts and activity verified via GitHub API on that date.
Licenses verified via GitHub API + LICENSE files where marked **verified**; others noted as reported.

Focus: practical, usable, commercially-usable tools for making autonomous AI agents
more reliable — failure detection/alerting, research automation, checkpointing,
and browser reliability. Directly supports the standing laws: NO-SILENT-FAILURE,
TRY-BEFORE-YOU-FLAG, NO-DROPPED-WORK, RESEARCH-BEFORE-ANSWER, WORK-SMARTER.

Legend: ✅ permissive/commercial-safe · ⚠️ copyleft or non-OSI — read before adopting ·
❓ license not machine-verified — check repo before commercial use.

---

## 1. Failure Detection & Alerting for Autonomous Agents

### 1a. Notification plumbing (ntfy.sh alternatives)

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **Apprise** `caronc/apprise` | One Python library + CLI that sends notifications to 100+ services (ntfy, Telegram, Discord, Slack, email, Matrix, Pushover, webhooks…) via URL config | ✅ **BSD-2-Clause (verified)** | 17,595 · pushed 2026-10-14 | **INSTALLED** — `pip install apprise`; CLI: `apprise -t "Title" -b "Body" ntfy://topic` ; Python API one-liner | The single best "agent yells for help" primitive. One call fans out to phone + Discord + email. Direct answer to NO-SILENT-FAILURE: wrap every unattended run so failures page the owner instead of dying quiet |
| **ntfy** `binwiederhier/ntfy` (self-hosted) | Self-hostable push server; publish via simple PUT/POST, subscribe via app | ✅ **Apache-2.0 (verified)** | 34,859 · pushed 2026-10-16 | `docker run -p 80:80 binwiederhier/ntfy serve` or distro package; `curl -d "build failed" ntfy.sh/mytopic` | Already in use on this setup. Self-hosting removes the ntfy.sh free-tier rate limits. Pairs with Apprise (`ntfy://` URLs) |
| **Gotify** `gotify/server` | Self-hosted push server, WebSocket delivery, Android app | ✅ **MIT (verified)** | 16,080 · pushed 2026-10-15 | Docker image `gotify/server`; POST to `/message` with app token | Simpler than ntfy if you only need phone push; no polling, no FCM dependency |
| **Shoutrrr** `containrrr/shoutrrr` | Go notification library + CLI, URL-based config, 20+ services (Slack, Discord, Telegram, ntfy, Gotify, SMTP, Teams…) | ✅ **MIT (verified)** | 1,696 · pushed 2026-07-01 | `go install github.com/containrrr/shoutrrr@latest`; `shoutrrr send discord://webhookid/token "done"` | Go-native equivalent of Apprise for Go lanes; used by Watchtower/Kured. Note: nicholas-fedor/shoutrrr fork is the more actively maintained line |

**Recommendation for this setup:** Apprise (installed) is the standard alerting layer —
cron/watchdog scripts call `apprise` on failure, and it fans out to ntfy + Messenger/Discord.
That is exactly the NO-SILENT-FAILURE wiring.

### 1b. Dead-man's-switch / job monitoring (did the job actually run?)

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **Healthchecks** `healthchecks/healthchecks` | Cron-job monitoring on the dead-man's-switch principle: job pings a URL on success; missed ping → alert. Start/fail signals, grace periods, ping logs | ✅ **BSD-3-Clause (verified)** | 10,424 · pushed 2026-10-16 | `pip install healthchecks` or Docker; add `curl -m 10 https://hc.example.com/<uuid>` to end of each cron job | Purpose-built for the dropped-work problem: a cron that dies silently (the NO-DROPPED-WORK / NO-SILENT-FAILURE cases) pages you within minutes. The TRY-BEFORE-YOU-FLAG workflow can also ping Healthchecks so the watchdog itself is monitored |
| **Gatus** `TwiN/gatus` | Lightweight health dashboard + alerting; YAML config-as-code, conditions on status/body/JSONPath/cert expiry, badges | ✅ **Apache-2.0 (verified)** | 12,325 · pushed 2026-10-07 | Single Go binary: download release, write `config.yaml`, run | Cheap always-on dashboard for "are my services/lanes alive" with alerting baked in. Very low resource use |
| **OneUptime** `OneUptime/oneuptime` | Full observability platform: uptime, status pages, on-call, incidents, logs, traces, APM | ✅ Apache-2.0 (reported in 2026 awesome lists) | 7,740 · pushed 2026-10-16 | Docker Compose from repo | If you outgrow single-purpose tools: one self-hosted platform replacing uptime + status page + on-call |
| **Keep** `keephq/keep` | Open-core AIOps alert manager: sits in front of existing monitoring, correlates/dedupes/routes alerts; AI correlation from past incidents; rules in Python/YAML | ✅ Apache-2.0 core (verified LICENSE; `ee/` dir proprietary) | 12,414 · pushed 2026-09-28 | Docker Compose | Alert-storm control: when one underlying failure fires dozens of alerts (common with agent fleets), Keep groups them so the owner gets one incident, not 40 pings |
| **HyperDX** `hyperdxio/hyperdx` | Open-source observability on ClickHouse + OpenTelemetry: logs, metrics, traces, errors, session replay | ✅ **MIT (verified)** | 9,949 · pushed 2026-10-16 | Docker Compose; OTEL-native so existing instrumentation flows in | Self-hostable Datadog alternative; MIT license. Good if agent lanes start emitting OTEL traces |
| Cachet `cachethq/cachet` | Classic self-hosted status page | ❓ (could not machine-verify; historically open source) | 15,259 · pushed 2026-10-16 | PHP/Laravel app | Public status communication; heavier than needed for internal agent monitoring |
| ⚠️ Checkmate `bluewave-labs/checkmate` | Modern monitoring UI + status pages | ⚠️ **AGPL-3.0 (verified)** | 10,951 · pushed 2026-10-15 | Docker | Capable, but AGPL copyleft — self-hosting is fine, embedding/redistributing is not |
| ⚠️ OpenStatus `openstatusHQ/openstatus` | Status page + multi-region uptime monitoring-as-code | ⚠️ **AGPL-3.0 (verified)** | 9,190 · pushed 2026-10-16 | Docker/self-host | Same AGPL caveat; Gatus covers the same ground permissively |

### 1c. Agent-specific reliability (the 2026 wave)

2026 produced a cluster of tools built specifically for *agent* failure modes, not just
server uptime. These are the most on-point finds of this research:

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **agent-audit** `HeadyZhang/agent-audit` — **PULLED** → `~/workspace/tools/agent-audit/` | Static security scanner for LLM agent code: prompt-injection rules, MCP config auditing, taint analysis; maps to OWASP Agentic Top 10 (2026) | ✅ **MIT (verified)** | 238 · pushed 2026-09-13 | `pip install agent-audit` then scan a project; ships as GitHub Action (`action.yml`) | Pre-deploy gate: scan agent code/configs for injection and tool-abuse risks before they run unattended. Small, fast, CI-friendly |
| **aegis** `Justin0504/aegis` | Runtime policy enforcement for AI agents: cryptographic audit trail, human-in-the-loop approvals, kill switch | ✅ **MIT (verified)** | 542 · pushed 2026-10-09 | TypeScript; see repo README | Runtime guardrails layer — the "never let an agent go rogue" counterpart to pre-deploy scanning |
| **auditable** `yzhao062/auditable` (USC-FORTIS lab) | SDK capturing a *signed* record of each agent decision; audits across past/present/future on one typed graph | ✅ **Apache-2.0 (verified)** | 28 · pushed 2026-09-08 | Python SDK | Verifiability primitive: every agent decision gets a tamper-evident record — matches the "verifiable work" requirement |
| ❓ agent-reliability-toolkit `tylerdh12/agent-reliability-toolkit` | Testing framework for 7 agent failure modes (hallucination, edge cases, prompt injection, tool failures, context loss, governance); audit scripts + report generator | ❓ **NO LICENSE FILE (verified)** — do not redistribute without asking author | 2 · pushed 2026-09-25 | `git clone …; pip install -r requirements.txt; ./scripts/run-audit.sh --endpoint http://localhost:8000` | Conceptually excellent checklist (the 7 failure modes map directly to real incidents), but **no license = cannot safely adopt commercially** until the author adds one |
| **Observability platforms** (tracing/evals/cost) | Langfuse `langfuse/langfuse` (✅ MIT core, 35,918★) · Opik `comet-ml/opik` (✅ Apache-2.0, 22,654★) · Helicone `Helicone/helicone` (✅ Apache-2.0, 6,226★) · OpenLIT `openlit/openlit` (✅ Apache-2.0, 2,852★) · LangWatch `langwatch/langwatch` (✅ Apache-2.0, 4,959★) · Laminar `lmnr-ai/lmnr` (✅ Apache-2.0, 3,394★) | mixed, see row | all active Oct 2026 | Docker Compose or `pip install` SDKs | When agent spend/debugging matters: trace every LLM call, eval outputs, track cost/latency. **Opik** is the sweet spot for Python agent shops (Apache-2.0, evals built in). ⚠️ Arize Phoenix is source-available under **Elastic License 2.0 (not OSI)** — fine to use, not fully open |

**What's new in 2026 (this category):** the shift from *server* monitoring to *agent*
monitoring — pre-deploy failure-mode test suites, runtime policy enforcement with
kill switches, and signed decision audit trails. The OWASP Agentic Top 10 (2026)
gave these tools a common threat model to build against.

---

## 2. Web Research Automation

Tools that do *structured* research for agents — not one-off search, but standing
pipelines: trending analysis, HN tracking, paper monitoring, release tracking.
Supports RESEARCH-BEFORE-ANSWER (research, don't guess) as an automated lane.

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **trending-repos** `m2dumpling/trending-repos` — **PULLED** → `~/workspace/tools/trending-repos/` | Bilingual GitHub trend tracker: discovers repos via GitHub Search + HN Algolia API + HuggingFace + npm/PyPI/Docker signals; deterministic AI-category classification (Agents, MCP, Coding Agents, RAG…); daily snapshots → 7/28-day velocity; builds a static GitHub-Pages site | ✅ **Apache-2.0 (verified)** | new (Oct 2026) · pushed 2026-10-16 | `GITHUB_TOKEN=… npm run fetch` → `npm run build` → serve static site. Node ≥20 | The exact pipeline the RESEARCH law wants: multi-signal trend discovery with *velocity* (star growth over time), not just snapshots. The `scripts/sources/` modules (github, hacker-news, huggingface, npm, pypi, docker) are reusable building blocks for any research lane |
| **Breakout** `chinesepowered/hack-long` | "Live AI news desk": watches the GitHub public event firehose, spots breakout repos, researches *why* on the live web, publishes cited bulletins; designed to resume exactly where it left off after a crash | ❓ (could not machine-verify) | new (2026) | See repo README | Two ideas worth stealing even without adopting it: (1) breakout detection on the event firehose (velocity, not totals), (2) crash-resumable agent loop as a design requirement |
| **Autarch Pollard hunters** `mistakeknot/autarch` (`docs/pollard/HUNTERS.md`) | Agent research pipeline with per-source "hunters": `github-scout` (GitHub Search API → README fetch → synthesize → score), `hackernews` (Algolia API, points-filtered), `arxiv` (papers), `competitor-tracker`, plus OpenAlex/PubMed/Wikipedia hunters; writes YAML source files per query per day | ✅ **MIT (verified)** | 2026 | Configure hunters in YAML, run the pipeline | Best *pattern* found for structured agent research: one hunter per source, scored/synthesized output to dated files. Directly adaptable to a standing research cron |
| **changedetection.io** `dgtlmoon/changedetection.io` | Website change detection + notifications: watch any page (or REST/JSON endpoint), diff on change, alert via 90+ notifiers incl. ntfy/Apprise | ✅ **Apache-2.0 (verified)** | 35,060 · pushed 2026-10-16 | Docker: `dgtlmoon/changedetection.io` | Release/changelog tracking without writing scrapers: point it at release pages, changelogs, pricing pages; it diffs and alerts. Integrates with ntfy so it plugs into the alerting layer above |
| ⚠️ **RSSHub** `DIYgod/RSSHub` | Turns almost any site into an RSS feed (GitHub trending, HN, release feeds, social) — 1000s of route "recipes" | ⚠️ **AGPL-3.0 (verified)** | 46,548 · pushed 2026-10-16 | Docker | Enormous coverage, but AGPL — fine to *self-host and consume*, do not embed in commercial products |
| **Miniflux** `miniflux/v2` | Minimalist feed reader, Fever/Google-Reader APIs | ✅ **Apache-2.0 (verified)** | 9,803 · pushed 2026-10-14 | Single Go binary or Docker | The inbox for the research pipeline: RSSHub/changedetection/arXiv feeds land here; agents poll its API |
| **Free keyless APIs (no install)** | HN Algolia API (`hn.algolia.com/api` — stories/comments search, no auth) · arXiv API + `export.arxiv.org/rss/cs.AI` (papers) · GitHub Search API (10 req/min anon, 30/min with token) · GitHub release Atom feeds (`github.com/<o>/<r>/releases.atom`) | n/a (public APIs) | — | `curl` | The raw material every tool above is built on. For a lightweight research lane, these four endpoints + a scoring script *are* the pipeline — no framework needed |

**What's new in 2026:** multi-signal trend trackers (GitHub+HN+package registries fused
into one attention score), and research pipelines designed as *resumable agent loops*
rather than one-shot scripts.

---

## 3. Checkpoint / State Management for Long-Running Agent Tasks

State of the art in 2026: **durable execution** — work that survives crashes and resumes
mid-step instead of restarting. Two tiers: heavyweight engines and lightweight patterns.

### 3a. Durable execution engines

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **LangGraph** `langchain-ai/langgraph` | Stateful agent orchestration: cyclic graphs, **checkpointing to SQLite/Postgres/Redis after every step**, time-travel debugging, `interrupt()` for human-in-the-loop approvals that can resume days later | ✅ **MIT (verified)** | 43,367 · pushed 2026-10-16 | `pip install langgraph`; `graph.compile(checkpointer=SqliteSaver.from_conn_string("./checkpoints.db"))` | The state of the art for *agent-shaped* durable work. Checkpointing is a framework primitive, not bolted on. If agents get rebuilt as code (not prompts), this is the chassis |
| **Temporal** `temporalio/temporal` | Durable workflow engine: workflow state survives process death, retries/timers/signals as primitives, polyglot SDKs. Raised $300M (Feb 2026); ~9.1T lifetime executions | ✅ **MIT (verified)** | 23,749 · pushed 2026-10-16 | Self-hosted cluster or Temporal Cloud | The industrial standard for long-running workflows. Heaviest ops of the list — worth it only at real scale |
| **Hatchet** `hatchet-dev/hatchet` | Task queue + DAG orchestrator + durable execution engine; **Postgres as the durability layer**; per-step retries, fan-out/fan-in, HITL; Go/Python/TS SDKs | ✅ **MIT (verified)** | 8,127 · pushed 2026-10-16 | Docker Compose (engine) + worker SDK | Best balance found in 2026 comparisons: durable execution without operating a Temporal cluster. Postgres-backed = fits a Postgres-first stack. Free cloud tier to 100k runs/mo |
| **DBOS Transact** `dbos-inc/dbos-transact-py` | Durable execution as a *library*: annotate ordinary functions as workflows/steps with decorators; Postgres-backed; no server to run | ✅ **MIT (verified)** | 1,635 · pushed 2026-10-16 | `pip install dbos` | Lowest-friction durable execution: add decorators to existing Python code, get crash-recovery for free |
| **Inngest** `inngest/inngest` | Event-driven step functions (cron/events/webhooks → memoized steps) + AgentKit for AI agents; excellent DX | ✅ Apache-2.0 (reported; verify in repo) | 5,949 · pushed 2026-10-16 | `npx inngest-cli dev` or cloud | Fastest path for serverless/TS teams; AgentKit is purpose-built for agent step durability |
| ⚠️ **Restate** `restatedev/restate` | Durable handlers, virtual objects (per-key state), durable RPC | ⚠️ **Business Source License 1.1 (verified)** — converts to Apache-2.0 after 4 years, but not OSI-open today | 4,564 · pushed 2026-10-16 | — | Architecturally interesting, but BUSL fails the commercial-use bar for now — skip |

### 3b. The lightweight pattern (what actually works for prompt-driven agent fleets)

For agents driven by prompts/subagents rather than code, the 2026 consensus pattern is:

1. **JSON checkpoint first** — worker writes `checkpoints/<name>.json` with
   `{task, status, watchdog, resume_brief, updated_at}` *before* doing anything else.
2. **Heartbeat** — `updated_at` refreshed every step (≥ every 10 min); a stale
   heartbeat = dead worker, not a running one.
3. **Resume brief** — the checkpoint contains a *complete standalone brief* so any
   fresh agent can pick up the work cold.
4. **Git as second backup** — commit incrementally; checkpoints are pointers, git is truth.
5. **External liveness probe** — a watchdog cron checks heartbeats and pages via the
   alerting layer (§1) when one goes stale. The watchdog's own claims get verified
   by attempt, not by probe (TRY-BEFORE-YOU-FLAG).

This is already the standing convention in `~/workspace/agent-ops/` — the engines above
are for when a lane graduates from prompt-driven to code-driven.

**What's new in 2026:** durable execution went mainstream for AI workloads — Hatchet and
DBOS lowered the entry cost to "just Postgres" / "just decorators," and Temporal's
$300M raise validated the category. For agents specifically, LangGraph's checkpoint +
interrupt model is the reference design.

---

## 4. Browser Automation Reliability

2026 state: the war is **stealth** (not getting blocked) + **session durability** (not
losing logins) + **self-testing** (proving you're not leaking automation signals).

| Tool | What it does | License | Stars / activity | Install / use | Why it matters |
|---|---|---|---|---|---|
| **Camoufox** `daijro/camoufox` | Anti-detect Firefox: fingerprint spoofing done **in the C++ engine** (WebGL, AudioContext, WebRTC, canvas) before any JS can observe the patching; Playwright-compatible API; virtual-display mode | ✅ **MPL-2.0 (verified)** — file-level copyleft, commercial-safe | 12,583 · pushed 2026-10-15 | `pip install camoufox && camoufox fetch` | 2026's #1 OSS anti-detect. Engine-level = pages can't see the patching the way they can see JS-injected stealth scripts. 0% headless detection on CreepJS in independent tests |
| **Patchright** `Kaliiiiiiiiii-Vinyzu/patchright` | Patched Playwright driver: same API, best-known Playwright tells removed at the source level | ✅ **Apache-2.0 (verified)** | 4,882 · pushed 2026-10-15 | `pip install patchright` (drop-in for `playwright`) | Smallest adoption cost — existing Playwright code keeps working, just harder to detect. Good first upgrade for the browser lane |
| **Pydoll** `autoscrape-labs/pydoll` | Python browser automation over raw CDP — **zero WebDrivers** (no driver-version breakage); async-first; human-like interaction engine (mouse paths, typing cadence); Cloudflare/Turnstile handling | ✅ **MIT (verified)** | 7,116 · pushed 2026-10-09 | `pip install pydoll-python` | Kills the #1 flakiness source (chromedriver mismatches) and the #2 (bot-shaped input) in one library. MCP server available (`pydoll-mcp`) for agent use |
| **browser-use** `browser-use/browser-use` | AI browser-agent framework: LLM drives the browser via structured DOM actions; built-in retry/step limits | ✅ **MIT (verified)** | 118,183 · pushed 2026-10-16 | `pip install browser-use` | The dominant open-source "agent uses a browser" framework in 2026. Its action/observation loop is the reference design for reliable agent browsing |
| **wraith** `yogevkr/wraith` — **PULLED** → `~/workspace/tools/wraith/` | Stealth browser **built for autonomous agents**: Camoufox primary + Patchright fallback; session/cookie harvesting from real profiles; `wraith selftest` runs a leak suite and exits non-zero (CI gate); challenge solving (Turnstile/hCaptcha/reCAPTCHA via CapSolver/2Captcha); MCP server included; WAAP fingerprinting (DataDome/Akamai/Kasada…) | ✅ **MIT (verified)** | new (Sep 2026) | `pip install wraith`; `camoufox fetch …`; `wraith selftest` | Purpose-built for exactly our problem (unattended agent browsing that must not stall on challenges). The selftest-as-CI-gate idea is directly reusable |
| **invisible_playwright_mcp** `feder-cr/invisible_playwright_mcp` | MCP server wrapping a C++-patched Firefox (identity derived from a seed → reproducible fingerprints) | ✅ **MIT (verified)** | 2026 | MCP config | Reproducible stealth: same seed = same browser identity across runs — useful for session consistency |
| **SeleniumBase (UC mode)** `seleniumbase/SeleniumBase` | Selenium with undetected-chromedriver mode; `uc_gui_click_captcha()` solves Cloudflare Turnstile via real GUI mouse events | ✅ **MIT (verified)** | 13,080 · pushed 2026-10-13 | `pip install seleniumbase` | The escape hatch for the hardest challenges (real OS-level clicks). Heavier than CDP tools, but solves what headless can't |
| ⚠️ nodriver `ultrafunkamsterdam/nodriver` / zendriver `cdpdriver/zendriver` | CDP-based undetected Chrome automation | ⚠️ **AGPL-3.0 (verified, both)** | 4,848 / 1,458 | `pip install` | Technically strong, but AGPL — and nodriver's last push was May 2026 with rising failure reports. Prefer MIT alternatives above |

### Reliability patterns (engine-agnostic, worth adopting)

- **Session persistence:** Playwright `storageState` / cookie export-import — log in once, reuse the session file across runs (wraith and zendriver-mcp both implement this).
- **Tiered escalation:** cheap no-browser TLS fetch (`curl_cffi` with browser impersonation) → stealth browser only when challenged. Saves enormous time/compute.
- **Self-test gates:** run a leak/detection suite (`wraith selftest`) in CI before trusting a browser change.
- **Fail fast on hard blocks:** detect WAAP blocks and abort the run with a clear signal instead of burning timeouts (feeds the alerting layer in §1).
- **Human-like input:** bezier mouse paths, per-keystroke typing jitter — Pydoll and several 2026 skills ship this as a library, not hand-rolled code.

**What's new in 2026:** Camoufox pulled ahead as the OSS anti-detect standard (engine-level
patches); Patchright made Playwright stealth a drop-in upgrade; agent-specific wrappers
(wraith, invisible_playwright_mcp) added MCP interfaces, session harvesting, and
self-test gates aimed at unattended agents rather than human-driven scraping.

---

## Pulled into ~/workspace/tools/ (this research)

| Path | What | License | Note |
|---|---|---|---|
| `~/workspace/tools/trending-repos/` | Multi-signal GitHub trend tracker (GitHub+HN+HF+npm/PyPI/Docker) | Apache-2.0 | `GITHUB_TOKEN=… npm run fetch` — research lane building block |
| `~/workspace/tools/wraith/` | Stealth browser for autonomous agents (Camoufox+MCP+selftest) | MIT | `pip install wraith` + `camoufox fetch` to activate |
| `~/workspace/tools/agent-audit/` | Static security scanner for agent code (OWASP Agentic Top 10) | MIT | `pip install agent-audit` — pre-deploy gate |
| apprise (pip, system-wide) | 100+ service notification fan-out | BSD-2-Clause | `apprise -t "T" -b "B" <url>` — the alerting primitive for all crons |

Not pulled (bigger frameworks / pip-installable when needed): LangGraph, Hatchet, DBOS,
Temporal, Opik, Gatus, Healthchecks, changedetection.io, Miniflux, Camoufox, Patchright,
Pydoll, browser-use.

## Suggested wiring for this operation

1. **Failure alerts:** every cron/watchdog failure path calls `apprise` (ntfy + owner-visible channel) — this is the NO-SILENT-FAILURE enforcement mechanism.
2. **Dead-man's-switch:** register long-running crons with Healthchecks; the watchdog's stale-checkpoint audit becomes a ping check instead of a guess.
3. **Research lane:** adapt `trending-repos/scripts/sources/` + the Autarch hunter pattern into a standing research cron (feeds RESEARCH-BEFORE-ANSWER with velocity data, not guesses).
4. **Pre-deploy gate:** run `agent-audit` on agent code/configs before they go unattended.
5. **Browser lane:** evaluate Patchright as a drop-in Playwright replacement first (cheapest win), Camoufox where DataDome-grade stealth is needed; adopt `wraith selftest` as the leak gate.

---
*Research method: GitHub API verification (licenses, stars, push dates) + 2026 roundups,
awesome-lists (awesome-auditable-ai, awesome-agent-observability, awesome-agent-harness,
awesome-ai-sre), and project docs. Per RESEARCH-BEFORE-ANSWER: no training-data guesses —
every tool above was checked live.*

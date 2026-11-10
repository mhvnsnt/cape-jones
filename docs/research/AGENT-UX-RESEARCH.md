# Agent UX Research — Faster Responses, Progress Surfacing, Notifications, Mobile Control
*Researched 2026-10-16 by Muse (Ashes). Scope: 2026 open-source tools.*

## TL;DR for Real
- **Respond-fast pattern**: the industry converged on *acknowledge instantly, stream tokens, work async* — "time to first token" matters for feeling fast, "time to useful result" matters for actually being done. OpenCode/Claude Code/Cline all do this via streaming + hooks.
- **Progress surfacing**: Claude Code status lines (context %, cost, elapsed), OpenPets (desktop pet showing agent state), agent-kanban (local-first task board with MCP for Claude Code/Cline + REST for OpenCode).
- **Phone notifications**: **ntfy.sh is the winner** — free, open source (Apache 2.0), one `curl` sends a push to an Android app, UnifiedPush support, priorities (urgent bypasses Do Not Disturb). **Caveat found in testing: this VM's egress proxy blocks ntfy.sh (403)** — so pushes must originate from an unblocked host or the live browser. Gotify (MIT) is the runner-up. Apprise (BSD-3) fans one message out to 100+ services at once.
- **Mobile control of agents**: Agent J (E2E-encrypted phone remote for Claude Code/Codex/OpenCode, permission-approval cards on phone), Buddy (Android app running Claude Code/Codex/OpenCode on-phone via proot, Apache 2.0), opencode-android fork (Android APK bundling OpenCode server + WebView UI).
- **Test result**: self-hosted ntfy server binary (v2.31.0) ran fine on this VM; publish→read-back loop verified. Public ntfy.sh test from this VM was blocked by the sandbox egress proxy, NOT by ntfy.

---

## 1. Fast acknowledgment patterns — "respond fast, work async"

### The consensus pattern (2026)
Across frameworks the winning pattern is the same four beats:
1. **Acknowledge immediately** — reply with a 202/ack the instant input is validated, before any heavy work. (From webhook/agent trigger guides: "Acknowledge fast, process separately" — GitHub-style providers expect a response in seconds and retry on slow handlers.)
2. **Stream the work** — token-by-token streaming (SSE, e.g. Google ADK's SSE flow) gives "zero perceived latency": the user sees words appear in milliseconds even if total work takes minutes.
3. **Queue + background workers** — enqueue the event, return, process async; retries with backoff and a dead-letter queue after ~5–10 attempts.
4. **Mid-task steering** — 2026 architectures accept follow-up input *while* a task runs ("steering"), batching rapid messages into one turn, and prioritize direct-user messages over background/routine ones.

Two metrics to keep separate (from a 2026 latency-infrastructure analysis):
- **TTFT (time to first token)** — first visible sign of life; makes the product *feel* alive.
- **Time to useful result** — the usable patch/answer/action; the commercial metric. A product can nail one and miss the other.

Voice-agent vendors converge on the same trick: spoken acknowledgments during long tool calls ("I'm checking the payment status") so necessary pauses feel intentional — PolyAI's 2026 guidance. Same idea applies in text: a fast "on it — pulling the render now" beat the silence.

### Frameworks / examples to borrow from
| Tool | License | What it does for speed | Relevance |
|---|---|---|---|
| **OpenCode** (sst/opencode) | MIT | Streams everything by default; TUI shows tool calls live; subagents run async | The reference architecture — this is how Real's lanes should behave: instant ack, then async worker |
| **Claude Code hooks** | (Anthropic product, Apache-2.0 examples) | `PreToolUse`/`PostToolUse`/`Stop`/`Notification` hooks fire on agent events — can push a progress note or ntfy ping on each milestone | notify-cli-public repo (suzega) wires these hooks to ntfy.sh so the *phone* buzzes when Claude finishes |
| **Google ADK (Agent Development Kit)** | Apache 2.0 | SSE streaming reference implementation; orchestrator → specialists → consolidator with token-by-token front-end delivery | Pattern to copy for any custom dashboard: SSE tunnel, render tokens as they arrive |
| **LangGraph + FastAPI** | MIT | Async-first agent graphs: "async for waiting (LLM calls, tools, I/O), sync for logic" — the golden rule from 2026 best-practices guides | Scales concurrent lanes; matches the VM's multi-lane workload |

### Practical takeaways for this operation
- **Ack in the chat reply FIRST, then delegate.** Exactly the RESPOND-FAST LAW Real already set — research confirms it's the industry default, not a quirk.
- **Wire Claude Code/OpenCode `Stop` hooks to ntfy** → phone buzzes when any long job (render, upload, teardown) finishes. See section 3.
- **Checkpoint summaries = streaming milestones.** The existing PROGRESS-SURFACING LAW (interim checkpoint summaries with evidence) is the "streaming" equivalent for long builds.

---

## 2. Progress surfacing — show work-in-progress without spamming

### Tools
| Tool | License | What it does | Relevance |
|---|---|---|---|
| **Claude Code status line** (built-in + community scripts: kcchien/claude-code-statusline, lucasilverentand/claudeline) | MIT (community scripts) | Persistent bar pinned to bottom of terminal: model, context % with progress bar (▓▓▓░░░), session cost, elapsed time, lines changed, git branch. Zero API cost — runs locally. | Cheap, proven pattern: a one-line live summary beats a paragraph of status. The `ctx:bar` component is directly reusable in any TUI. |
| **OpenPets** (alterhq/openpets) | Open source | Native macOS desktop pet that shows *visible agent progress*: task state, review prompts, completion states, lightweight animations. Exposes MCP server (`http://127.0.0.1:3001/mcp`) — Claude Code, Cline, OpenCode, Cursor report work through one visible companion | Ambitious/fun idea: agents report state to one shared visual surface. macOS-only; would need an Android/web port for Real. |
| **agent-kanban** (boian-ivanov/agent-kanban) | Check repo LICENSE | Local-first kanban for AI-agent workflows: Backlog → Approved → Analyst → In progress → Testing → UAT → Done. MCP server (28 tools) for Claude Code & Cline; REST/OpenAPI for OpenCode/any function-calling LLM. Outbound webhooks on task_created/task_moved/task_updated → Slack/Telegram/HTTP. Milestone→epic→story→task with roadmap view. | Strong fit: drag a task to Approved and the agent picks it up itself; webhook → ntfy → phone pings on lane state changes. No polling the chat. |
| **Novu** (novuhq/novu) | MIT (open core) | Full notification *infrastructure*: unified API for push/email/SMS/in-app with workflows, templates, **digests**, subscriber preferences | If notification needs ever outgrow ntfy: digest mode batches many lane events into one summary — the anti-spam answer. |
| **Apprise** (caronc/apprise) | BSD 3-Clause | One API fans out to **100+ services** (Slack, Discord, Telegram, email, SMS, push…) | Relay/fan-out layer: one call from a lane → Discord + ntfy + email simultaneously. |

### The anti-spam pattern (digest > stream)
The research consensus: stream *in the chat UI* (tokens, spinners, collapsible tool-call groups), but **push to the phone only on milestones**. Concrete rules that work:
- Phone buzz: job started, job finished (success/fail), blocked-on-owner, milestone hit. Nothing else.
- Chat stream: token streaming + collapsible per-tool progress (OpenCode TUI model).
- Digest: Novu-style digest batches N lane events into one summary per hour/day for the Feed or a cron summary.

---

## 3. Notification systems — Linux VM → Android phone

### Winner: ntfy.sh
| | |
|---|---|
| **What** | Dead-simple HTTP pub/sub push notifications. `curl -d "Render done" ntfy.sh/<topic>` → instant push on the phone. Topics are the only addressing — no accounts, no API keys needed on the public server. Priorities (`urgent` bypasses Android Do Not Disturb), tags/emoji, markdown, click actions, attachments, action buttons. |
| **License** | Apache 2.0 (server); Android/iOS apps also open source |
| **Setup (public server, 2 minutes)** | 1. Install ntfy app on Android (Play Store `io.heckel.ntfy`, or F-Droid). 2. Subscribe to a topic name — pick something unguessable, e.g. `fmmg-render-alerts-9f3k2`. 3. Publish from anywhere: `curl -H "Title: Render done" -H "Priority: high" -H "Tags: clapper" -d "wizard-gang-ep01 cut finished" https://ntfy.sh/fmmg-render-alerts-9f3k2` |
| **Setup (self-hosted)** | Single Go binary or Docker: `docker run -p 80:80 binwiederhier/ntfy serve`. Then in the ntfy app: Settings → Default server → your URL. Optional auth: `NTFY_AUTH_DEFAULT_ACCESS=deny-all` + per-topic tokens. |
| **Relevance** | Highest. Zero-cost, zero-account, works from any shell/cron/hook. Perfect for "render finished at 3 AM" pings. UnifiedPush support = no Google dependency required. |
| **⚠️ Tested 2026-10-16** | Public **ntfy.sh is BLOCKED from this VM** — the sandbox egress proxy returns `403 Forbidden` on CONNECT to ntfy.sh:443 (domain-specific policy; github.com and gotify.net both reachable from the same VM). **Not an ntfy outage.** Workarounds: (a) publish from the live-browser lane or any unblocked host; (b) self-host ntfy on a reachable VPS (documented above); (c) use Apprise relay from here to a service that isn't blocked. |
| **Self-host test** | ✅ Downloaded ntfy v2.31.0 (linux_amd64) from GitHub releases onto this VM, ran `ntfy serve` on 127.0.0.1:8899, published and read back a message successfully. Setup is genuinely a single binary + one command. |

### Runner-up: Gotify
| | |
|---|---|
| **What** | Self-hosted push/messaging server: create "apps" in a web UI, each gets a token, POST messages via REST; messages persist in SQLite; WebSocket real-time; Android app. |
| **License** | MIT |
| **Setup** | Docker: `docker run -p 80:80 gotify/server`; create app in web UI → token; `curl -X POST -H "X-Gotify-Key: <token>" -F "title=Done" -F "message=Render finished" https://gotify.example.com/message`. Android app → add server URL. |
| **Trade-offs vs ntfy** | More structured (per-app tokens, web dashboard, plugin system, persistent history) but: Android-only (no iOS app), no UnifiedPush, no public free instance — must self-host, needs a reachable server for the phone anyway. |
| **Relevance** | Good if a private, authenticated dashboard is wanted. For Real's use (fire-and-forget phone pings from lanes), ntfy is simpler. |

### Fan-out layer: Apprise
| | |
|---|---|
| **What** | Python library/CLI: one call → 100+ notification targets (Discord, Telegram, Slack, email, SMS gateways, ntfy, Gotify…). |
| **License** | BSD 3-Clause |
| **Setup** | `pip install apprise`; `apprise -t "Render done" -b "ep01 cut finished" discord://webhook_id/webhook_token ntfy://ntfy.sh/topic mailto://user:pass@gmail.com` |
| **Relevance** | Best "belt and suspenders" option: lanes call Apprise once → hits ntfy AND Discord AND email. If one channel is blocked, others still land. |

### 2026 newcomers / adjacent
- **Agent J** (preangelleo/agentj) — not a notifier per se, but its phone-approval cards *are* push notifications for agent permission requests (see section 4).
- **Novu** (novuhq/novu, MIT open-core) — full notification infrastructure with **digest workflows**: batch "47 lane events" into one summary push instead of 47 buzzes. Worth it if lane count grows.
- **awesome-push-notifications** (ishandutta2007/awesome-push-notifications) — curated list, kept current; the fastest way to survey this space later.

### Recommended wiring for Real's lanes
1. **Android**: install ntfy app → subscribe to private topic (e.g. `fmmg-agent-ops-<random>`).
2. **Every long lane** (render, upload, teardown): publish on completion — one `curl` line at the end of the script, or a Claude Code/OpenCode `Stop` hook:
   ```bash
   curl -s -H "Title: ✅ Render done" -H "Priority: high" -H "Tags: clapper" \
     -d "wizard-gang-ep01-16x9-dialogue-v11.mp4 finished" \
     https://ntfy.sh/fmmg-agent-ops-<random>
   ```
   Priority levels: `urgent` = bypasses Do Not Disturb (failures), `high` = completions, `default` = FYI.
3. **Claude Code hooks** (notify-cli-public pattern): `Stop` → ntfy publish, `PermissionRequest` → ntfy publish with `urgent`. The phone becomes the approval/completion surface.
4. **From this VM**: route publishes through an unblocked path (browser lane, or Apprise to Discord/Telegram which aren't blocked).

---

## 4. Mobile-friendly agent interfaces

| Tool | License | What it does | Relevance |
|---|---|---|---|
| **Agent J** (preangelleo/agentj) | Check repo (open source, beta) | Control your own Claude Code / Codex / OpenCode from your phone. Host program runs next to the agent; phone pairs via QR + 6-digit code + passphrase; **E2E-encrypted (Noise protocol)** through a blind relay. Agent permission requests arrive as phone cards — approve/deny with a tap (120s timeout = deny); every decision signed + logged. | **Highest relevance for Real** (phone-only operator). Approval cards on phone = no more "waiting on permission" stalls. Sandbox isolation via bubblewrap on Linux. |
| **Buddy** (netmag.pk coverage; GitHub, v2.1) | Apache 2.0 | Android app that runs Claude Code, Codex, OpenCode **on the phone itself** via proot Alpine Linux env. Floating chat bubble UI; can read screen content, tap buttons, enter text, navigate other apps. No computer/root/ADB/API key needed; uses existing Claude Pro/Max or ChatGPT plan. | For on-the-go agent work from the phone directly. Early stage (tested mainly on OnePlus 12, Android 16); battery/perf vary. |
| **opencode-android** (hi77x/opencode-android) | Check repo LICENSE | Independent OpenCode fork as an **Android APK**: bundles the real OpenCode server + WebView UI; server data under `/sdcard/OpenCode/home` with all-files access. Also ships desktop builds. | Full OpenCode TUI experience on Android. Beta. |
| **agmux** (neelsatyavolu/agmux) | MIT + Commons Clause (source-available) | macOS app running agents side-by-side (Claude Code, Codex, Cline, OpenCode…); has `remote-relay` + `remote-mobile` (PWA + iOS shell) for phone remote control | macOS-only desktop; the phone-remote piece is the relevant pattern. |
| **rwanbt/opencode** (fork) | Check repo | Bundles an Android app with on-device inference (llama.cpp), terminal/PTY, voice STT/TTS, REST task API, DAG orchestration | All-in-one but a fork; evaluate stability before depending on it. |

### Recommended pick for Real
**Agent J** — it solves his exact bottleneck (phone-only, needs to approve agent actions and see completions) without moving the compute: agents keep running on the VM/Kaggle, the phone is just the secure remote. Pair with **ntfy** for passive completion pings (no app to open) — Agent J for interactive approvals, ntfy for fire-and-forget alerts.

---

## Test log
- `curl https://ntfy.sh/agent-ux-test-topic` → **HTTP 000 / 403 from egress proxy** — domain blocked by sandbox policy, not an ntfy problem. Direct (no-proxy) also fails (no route). github.com + gotify.net reachable from same VM.
- Self-hosted ntfy v2.31.0 on 127.0.0.1:8899 → publish returned message JSON with id, and the topic's JSON stream read the message back **(full loop verified)**. Single binary, one command. Test server shut down after verification.
- Binary kept at `/tmp/ntfy_2.31.0_linux_amd64/ntfy` (ephemeral /tmp); re-download from `https://github.com/binwiederhier/ntfy/releases/latest` when needed.

## Open questions for the owner
1. Install the **ntfy Android app** and pick a private topic name → then lanes can ping his phone on completions (publishes route via browser lane until VM egress allows ntfy.sh).
2. Try **Agent J** for phone-based agent approvals — biggest mobile-UX unlock for a phone-only operator.
3. Digest preference: instant buzz per event, or Novu-style hourly digest? Recommend instant for completions/failures, digest for routine lane heartbeats.

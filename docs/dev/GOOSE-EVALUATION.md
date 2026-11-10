# GOOSE — evaluation verdict: NOT pulled in (2026-10-17)

**Verdict: PASS.** Goose does not earn a slot on this team today. This doc
preserves the research so nobody redoes it.

## What it is

Goose is an open-source AI agent (Apache 2.0), originally built by Block,
now stewarded by the Agentic AI Foundation at the Linux Foundation. CLI +
desktop app, MCP-native extension model (70+ extensions), multi-provider
(BYO key), recipes for reusable workflows, foundation-backed neutral
governance. BYO-API pricing: free software, you pay your LLM provider.

Sources (checked 2026-10-17):
- https://mcp.directory/blog/goose-vs-cline-vs-aider-vs-claude-code-vs-opencode-2026
- https://blog.marcnuri.com/goose-on-machine-ai-agent-cli-introduction
- https://dev.to/pickuma/goose-cli-review-blocks-open-source-agent-after-the-linux-foundation-handoff-4ail

## Why it doesn't earn a slot

Our roster (2026-10-17, all live and wired in this repo's docs/dev/):

| Slot | Holder | Goose's overlap |
|---|---|---|
| Free-volume coding CLI | **Gemini CLI** (60 RPM / 1,000 RPD, 1M context) | full overlap |
| Free-model overflow agent | **OpenCode** (MIT, OpenRouter `:free` models) | full overlap — OpenCode is Goose's closest philosophical cousin per the reviews |
| Repo surgery / precise edits | **Aider** | overlap |
| Build/test/fix loops | **Cline** | overlap |
| GitHub-native work | **Copilot CLI** | partial overlap |
| Zero-key free gateway | **Codex CLI + Kilo Code** (200 req/hr/IP) | overlap |

Goose's genuine differentiators — desktop UI polish, the MCP extension
catalog, recipes, foundation-backed neutrality — serve **interactive,
desktop-driven workflows**, not our headless VM lanes. On this VM every run
is headless (`-p`, `run`, cron), where Goose is a seventh agent with a
seventh quota surface and nothing to do the other six can't already do.

## What would change the verdict

- A lane needs **portable YAML session recipes** running in CI (Goose's
  recipe model is genuinely stronger than ad-hoc shell for this).
- A lane needs the **MCP extension catalog** (70+) without hand-wiring MCP
  servers per tool.
- The team outgrows OpenCode or needs **foundation-neutral governance** for
  a long-term commitment (Goose's neutrality is the feature you'd buy).

If any of those fire, install is one `curl` away and the wiring pattern is
identical to OpenCode's (BYO key in the key file, config in repo). Re-eval
then — not before.

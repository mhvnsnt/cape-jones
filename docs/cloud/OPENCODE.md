# OpenCode — AI Coding Agent (Terminal)

**Status:** Source pulled into this repo at `production/devtools/opencode/` (shallow clone).
**License:** MIT. **Stars:** ~189k (most-starred open-source AI coding assistant as of July 2026).
**Repo:** https://github.com/sst/opencode

## What it is

Terminal-based AI coding agent. The Aider successor — 75+ LLM providers, no git
required, works in any terminal. This is the #1 pick from our 2026 cloud research
(`docs/research/` → CLOUD-RESEARCH.md).

## Install (one command, no repo needed)

```bash
curl -fsSL https://opencode.ai/install | bash
```

Or via npm/bun:

```bash
npm i -g opencode-ai
```

## Quick start

```bash
cd ~/workspace/cape-jones-build/cape-jones
opencode
```

Then type what you want. It reads the repo, makes edits, runs commands.

## Providers

75+ supported (Anthropic, OpenAI, Google, local Ollama, etc.). Configure via
`opencode.json` in the project root or `~/.config/opencode/`.

Free option: point it at Ollama for fully local, or use any provider free tier.

## Why it's here

The owner's workflow is phone-first; agents do the computer work. OpenCode gives
every agent a terminal coding assistant with no API key required for local models.
Source is vendored in-repo so the exact version we evaluated is preserved.

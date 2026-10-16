# Gemini CLI — Free Daily AI Coding (Google Login)

**Status:** Install-on-demand (documented here, not vendored).
**License:** Apache-2.0. **Stars:** ~105k.
**Repo:** https://github.com/google-gemini/gemini-cli

## What it is

Google's terminal AI coding assistant. The killer feature: **FREE daily quota
(60 req/min, 1000 req/day) on just a Google login — no API key needed.**

## Install (one command)

```bash
npm install -g @google/gemini-cli
```

Then:

```bash
gemini
```

Sign in with the Google account when prompted. That's it — 1000 free AI coding
requests per day.

## Why install-on-demand

Same reasoning as code-server: the npm install IS the pull. Vendoring the
source repo would add bulk for zero benefit. The command lives here in the
permanent store.

## Use with our repos

```bash
cd ~/workspace/cape-jones-build/cape-jones
gemini "explain the LED controller presets"
```

Free tier resets daily. For heavier work, OpenCode (`OPENCODE.md`) with a
paid provider key or local Ollama.

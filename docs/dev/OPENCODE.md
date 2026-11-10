# OpenCode in cape-jones — setup & usage

OpenCode is the open-source terminal coding agent (MIT, 75+ providers).
Lane role: **overflow/parallel coding work on free models** — the agent you
throw the small, boring, numerous jobs at while the big CLIs do the heavy
lifting.

## Install (per opencode.ai, checked 2026-10-17)

```bash
npm install -g opencode-ai   # 1.19.3 live on the VM as of 2026-10-17
opencode --version
```

No binary to commit — the VM's global npm install is the single install
every lane shares. (npm install took ~9 min on 2026-10-17; it's a big
package. Don't re-install, it's already there.)

## Point it at a key (free only)

OpenRouter is a **native provider** — no custom config needed, just the key:

```bash
set -a && . ~/.config/cape-jones/api-keys.env && set +a   # chmod 600, gitignored
# provides OPENROUTER_API_KEY — never paste a value anywhere
```

The repo's `opencode.json` (project root) pins the default model so every
lane runs the same free model without thinking:

```json
{"$schema":"https://opencode.ai/config.json",
 "model":"openrouter/cohere/north-mini-code:free",
 "small_model":"openrouter/cohere/north-mini-code:free"}
```

Why this model: `cohere/north-mini-code:free` is the model Cline proved
working on this VM (2026-10-17). OpenRouter `:free` models are **50
requests/day** (no card — do NOT buy the $10 credit that raises the cap).
That's the whole lane budget: small tasks, one shot each.

## Usage

```bash
set -a && . ~/.config/cape-jones/api-keys.env && set +a
opencode run "Fix the typo in docs/dev/OPENCODE.md"   # headless, one shot
opencode                                              # interactive TUI
opencode run --model openrouter/other-free-model "..."  # override per run
```

Project config is picked up automatically from the repo root; user-wide
settings would go in `~/.config/opencode/opencode.jsonc` (not used — the
repo file is the shared lane config). Keys added via `/connect` land in
`~/.local/share/opencode/auth.json` — we don't use that path; env var only.

## Live-AI proof (2026-10-17)

`opencode run "Reply with exactly this string and nothing else:
OPENCODE-LIVE-OK"` — see probe log. Model: openrouter/cohere/north-mini-code:free.

## When NOT to use it

- The 50 req/day budget is spent → **Gemini CLI** (1,000 req/day free tier).
- Precision file edits / repo surgery → **Aider**.
- Build/test/fix loops with step approval → **Cline**.
- Whole-repo reads / research synthesis → **Gemini CLI**.

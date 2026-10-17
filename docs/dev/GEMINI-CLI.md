# Gemini CLI in cape-jones — setup & usage

Google's official AI coding CLI (Apache 2.0). Lane role: **massive-context
reads** — whole-repo analysis, research synthesis, large refactors. Runs
entirely off the free API tier: **60 req/min, 1,000 req/day, 1M-token
context**, no credit card.

## Install (per geminicli.com, checked 2026-10-17)

```bash
npm install -g @google/gemini-cli   # needs Node >= 18
gemini --version                     # 0.64.0 live on the VM as of 2026-10-17
```

No binary to commit — the VM's global npm install is the single install
every lane shares.

## Point it at a key (free only)

The Gemini API key is live on the VM in `~/.config/cape-jones/api-keys.env`
(chmod 600, gitignored). Source it — never paste a value anywhere:

```bash
set -a && . ~/.config/cape-jones/api-keys.env && set +a
```

Two headless gotchas, both learned the hard way on 2026-10-17:

1. **Auth type must be pre-selected.** In a non-TTY run the CLI stalls on the
   interactive auth-method prompt. Pre-seed once per VM:
   ```bash
   mkdir -p ~/.gemini
   printf '{"selectedAuthType":"gemini-api-key"}' > ~/.gemini/settings.json
   ```
2. **Untrusted working folders block headless runs.** Either trust the dir in
   interactive mode once, or pass `--skip-trust` on headless calls (headless
   agents working out of git worktrees will hit this).

## Headless usage (the lane pattern)

```bash
set -a && . ~/.config/cape-jones/api-keys.env && set +a
gemini -p "Explain the architecture of this codebase" --skip-trust
```

- `-p / --prompt` runs once and exits; stdout is the answer.
- Pipes work: `cat error.log | gemini -p "Explain why this failed"`.
- `--output-format json` for script consumption; `stream-json` for progress.
- Interactive TUI: just `gemini` (needs the auth pre-seed above only for
  headless/CI; the TUI picks the persisted auth type itself).
- `/memory` and `GEMINI.md` give per-project memory layers; this repo's
  canon docs (SCENE-CANON.md, AGENTS.md, TEAM-WORKFLOW.md) are the context
  you point it at before any large refactor.

## Models, limits, caveats

- Free-tier model selection follows the CLI default at install time
  (Gemini 3 family in 0.64.x; check with `-m` if you need to pin).
- Limits on the free API tier: 60 RPM / 1,000 RPD. Generous for volume work —
  this is the CLI to absorb big batch jobs.
- **Free-tier prompts may be used to train Google models.** Same tradeoff as
  the aider Gemini default; don't feed it anything the owner wouldn't want
  Google to see.
- Free-tier quota is shared with aider's Gemini usage — the same key hit
  aider's quota wall earlier on 2026-10-17, so if a run 429s, fall back to
  OpenRouter/Groq lanes rather than hammering retries.

## Live-AI proof (2026-10-17, verbatim)

`gemini -p "Reply with exactly this string and nothing else:
GEMINI-CLI-LIVE-OK" --skip-trust` returned exactly `GEMINI-CLI-LIVE-OK`
via the shared `GEMINI_API_KEY`. Not a fallback — real Gemini API response.

## When NOT to use it

- Precision file edits and repo surgery → **Aider** (best git integration).
- Build/test/fix loops → **Cline**.
- GitHub-native work → **Copilot CLI**.
- Tiny overflow tasks on free models → **OpenCode** (docs/dev/OPENCODE.md).

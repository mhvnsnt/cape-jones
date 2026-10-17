# Cline in cape-jones — setup & usage

Verified 2026-10-16 (install paths actually executed on this VM — see
"Verification log" at the bottom). Cline is the autonomous agent lane;
Aider (`docs/dev/AIDER.md`) is the pair-programmer lane.

## Cline vs Aider — when to use which

| | Cline | Aider |
|---|---|---|
| Shape | Autonomous agent: plans, edits, runs commands, iterates with checkpoints | Pair programmer: you drive, it edits |
| Interface | VS Code sidebar, terminal CLI (`cline`), headless JSON mode | Terminal TUI |
| Best for | Multi-step scene iteration loops (edit script → run Blender → render → check frames → fix → repeat) without babysitting | Targeted code edits where you want to review each diff immediately |
| Model key | BYOK per provider via `cline auth`, or Cline account sign-in | `GEMINI_API_KEY` env var (free tier default) |

Rule of thumb: Aider when you want hands on the wheel, Cline when you want
to hand it a task card and check back. Both obey `.clinerules` (repo rules)
and `AGENTS.md` (verify-before-claiming laws). Cline's extra mode for scene
work is `.roomodes` → `scene-iterate`.

## Install

Two independent installs, both verified on this VM:

```bash
# 1. CLI — the headless-capable agent (verified: installs cline 3.0.72)
npm i -g cline
cline --version        # expect 3.0.72+
cline doctor           # headless-safe; reports hub/daemon state

# 2. VS Code extension — for code-server / VS Code / Codespaces (verified: 4.1.25)
code-server --install-extension saoudrizwan.claude-dev
code-server --list-extensions | grep cline
```

The extension is the official Cline listing (publisher `saoudrizwan`,
package `claude-dev`, display name "Cline"). It pulls from Open VSX on
code-server — no Microsoft account needed. Docs: https://docs.cline.bot

## Connecting the API key (the one blocked step)

Cline ships with no key. Three paths (all free-tier compatible; the owner
spends nothing):

1. **Cline account (usage-billing, free models included)** — sign in with
   Google/GitHub/email inside the extension or `cline auth`. No key to
   manage. **Needs a browser OAuth flow → NEEDS-PARENT-BROWSER**
   (subagents cannot do this).
2. **BYOK via CLI (non-interactive, verified from `cline auth --help`)** —
   once the secure-vault lane delivers a raw key, one command wires it:
   ```bash
   # OpenRouter free models
   cline auth --provider openrouter --apikey "$OPENROUTER_API_KEY" --modelid <model-id>
   # Gemini free tier
   cline auth --provider gemini --apikey "$GEMINI_API_KEY" --modelid <model-id>
   # Any OpenAI-compatible endpoint (e.g. Groq free tier)
   cline auth --provider openai-native --apikey "$GROQ_API_KEY" \
       --baseurl https://api.groq.com/openai/v1 --modelid <model-id>
   ```
   Per-run override without storing anything:
   `cline -P openrouter -m <model-id> -k <key> "task"`.
   Config lands in `~/.cline` (or an isolated dir via `--data-dir`).
3. **BYOK in the extension** — open Cline settings → API Configuration →
   pick provider, paste key. VS Code secret storage holds it (never a file).

Hard boundaries, established 2026-10-16:
- The stored `custom.legacy-gemini` connector credential is surrogate-only
  and is NOT retrievable as a raw key. It cannot feed Cline. Do not try.
- Getting a Gemini free-tier key needs a Google sign-in at
  https://aistudio.google.com → NEEDS-PARENT-BROWSER.
- A separate lane is collecting keys through the secure vault flow. Until
  a key lands, everything below is wired and waiting — nothing here takes
  a key as an argument, logs one, or commits one.

## First-run smoke test (once a key lands)

```bash
# 1. Doctor passes, auth stored
cline doctor

# 2. Headless one-shot, JSON output (this is also the lane-automation shape)
cline --json "list the files in tools/layout-rules and say nothing else" \
  | python3 -c "import json,sys; [print(json.loads(l).get('event',{}).get('text','')[:200]) for l in sys.stdin if l.strip()]"

# 3. Interactive: type one task, watch it plan → act → checkpoint
cline
# > In scene-iterate terms: "check validate_layout.py for bugs, do not edit anything"

# 4. Extension: open Cline sidebar → mode dropdown should list "Scene Iterate"
#    (from .roomodes) alongside Code / Architect / Ask.
```

## Repo wiring (this lane)

| File | Purpose |
|---|---|
| `.clinerules` | Always-on repo rules: git discipline, locked colorway palette, Blender headless invocation, verify-before-claiming |
| `.roomodes` | One custom mode: `scene-iterate` (read/edit/command, full scene-workflow discipline baked in). Modes earn their keep or they don't ship — this one does. |
| `docs/dev/CLINE.md` | This file |

`.clinerules` loads automatically per the current Cline docs
(`.clinerules/` dir, `.cline/rules/`, or single `.clinerules` file —
this repo uses the single-file form). Cline also reads `AGENTS.md`
cross-tool.

## VM quirks (this machine)

- `cline auth` and `cline config` need a TTY/browser — they hang or error
  headless. All scripting uses the flag forms (`--provider`, `--apikey`,
  `-P`, `-m`, `-k`, `--json`, `--data-dir`).
- `npm i -g cline` installs into `/usr/lib/node_modules` on this image
  (outside `~`, ephemeral on VM replacement). Reinstall is one command —
  this doc is the persistent record, not the install.
- The `no_proxy` IPv6-literal crash documented for aider
  (`docs/dev/AIDER.md`) is a Python httpx bug. The Cline CLI is Node —
  not observed to be affected; if you see proxy weirdness, check
  `no_proxy`/`NO_PROXY` first.

## Verification log (2026-10-16, this VM)

- `npm i -g cline` → 331 packages, `cline --version` → **3.0.72** ✅
- `cline doctor` headless → runs, reports hub down (expected) ✅
- `cline auth --help` → confirms non-interactive `--provider/--apikey/--modelid/--baseurl` ✅
- `cline auth` without TTY/browser → hangs waiting on OAuth (killed) — expected, this is the key boundary ✅
- `code-server --install-extension saoudrizwan.claude-dev` → v4.1.25 present, listed ✅
- Extension manifest check → publisher `saoudrizwan`, name `claude-dev`, display `Cline`, `./dist/extension.js` present, 19 `cline.*` commands ✅
- `.roomodes` → `python3 -c json.load` parses; shape matches the
  `customModes[]` schema (`slug`/`name`/`roleDefinition`/`groups`/`customInstructions`) ❓ — parse-verified; UI pickup (mode dropdown) needs the key + a running IDE, still unverified
- **Precise boundary: everything installs, loads, and parses. The agent
  cannot act until a provider key (or Cline account sign-in) lands.**

## NEEDS-PARENT-BROWSER checklist

1. Cline account sign-in (free usage-billing path) — Google/GitHub/email OAuth.
2. Gemini free-tier key — Google sign-in at aistudio.google.com.
   Account for both: fmmg.mars@gmail.com (standing permission).

# Aider in cape-jones — setup & usage

Aider is the AI pair programmer for code/docs iteration in this repo.
Repo defaults live in `.aider.conf.yml` (root) and `.aiderignore`.
Lane conventions: `docs/dev/AIDER-CONVENTIONS.md`.

## Install (per aider.chat/docs/install.html, checked 2026-10-16)

```bash
# recommended: uv tool install (isolated venv, own python 3.12 if needed)
python3 -m pip install --break-system-packages uv
uv tool install --force --python python3.12 --with pip aider-chat@latest

# verify
aider --version
aider --help
```

Alternatives from the same page: `python -m pip install aider-install && aider-install`,
`pipx install aider-chat`, or the `curl https://aider.chat/install.sh | sh` one-liner.

## Point it at a key (free only)

Free tier default in `.aider.conf.yml` is `gemini-exp`
(Gemini 2.5 Pro Exp, free with usage limits — aider.chat/docs/llms/gemini.html).

```bash
export GEMINI_API_KEY=<key>     # never commit, never log
```

Get the key at https://aistudio.google.com — requires a Google sign-in in a
browser (a subagent cannot do this; flag NEEDS-PARENT-BROWSER if you need one).
The repo's stored Gemini connector (`custom.legacy-gemini`) is a surrogate-only
credential for one-turn image edits — it is NOT retrievable as a raw API key
and cannot feed aider. Paid higher-limit alternative: `aider --model gemini`.
OpenRouter also offers free models with daily usage limits (`OPENROUTER_API_KEY`).

Aider looks for keys in env vars, `--api-key gemini=<key>`,
or a `.env` file (env vars override; `AIDER_xxx` overrides config file).

## Common jobs (exact commands)

Run from the repo root of your worktree. All non-interactive runs add
`--yes-always` (never rely on it for the first run — watch the first diff).

```bash
# 1. Iterate on the layout applier (code + read-only context)
cd ~/workspace/cape-jones-setup-aider   # or your lane's worktree
aider tools/layout-rules/apply_layout_blend.py \
      --read tools/layout-rules/README.md \
      --message "Add a --dry-run flag that prints object moves without touching bpy" \
      --yes-always
# then: git diff (eyes on it), python3 -m py_compile, run the validator

# 2. Draft docs
aider --message "Draft docs/dev/LAYOUT-ANCHORS.md: document the layout contract fields \
  (name, x, z, rotation_deg, anchor) with one example each. Source: tools/layout-rules/README.md" \
  --read tools/layout-rules/README.md --yes-always
# then read the file it created and fix it up yourself

# 3. Review a branch diff (read-only: --read adds files WITHOUT letting aider edit them)
aider --read tools/layout-rules/validate_layout.py \
      --message "Review this file for bugs. Do not edit anything." --yes-always

# 4. Explore / sanity check (loads config, detects git, exits — no LLM needed)
aider --exit

# 5. List models aider knows for a provider
aider --list-models gemini/
```

## Config files

| file | purpose |
|---|---|
| `.aider.conf.yml` | repo defaults: free model (`gemini-exp`), auto-commits OFF, watch-files, no analytics |
| `.aiderignore` | keeps the repo map off binaries: `*.blend`, `*.fbx`, `*.glb`, media, node_modules |
| `.aider.model.settings.yml` | not needed — `gemini`/`gemini-exp` are known aliases with built-in settings |

Per-file overrides on the command line always win over the config file.

## Notes

- `.blend` scene files are binary — aider works on code/docs/JSON, never blends
  (the applier scripts are the interface to scenes).
- `watch-files: true` — aider notices edits you make outside it mid-session.
- Never paste an API key into chat, logs, or repo files.

## VM quirks (this machine)

- **httpx/no_proxy crash:** aider's HTTP stack (httpx via litellm) crashes on this
  VM's `no_proxy`/`NO_PROXY` values, which contain IPv6 literals (`::1`, `[::1]`):
  `httpx.InvalidURL: Invalid port: ':1]'`. Strip them before running aider:
  ```bash
  for v in no_proxy NO_PROXY; do
    export "$v=$(echo "${!v}" | tr ',' '\n' | grep -v '::' | paste -sd, -)"
  done
  ```
- **Big-repo first scan:** the initial repo-map scan over ~12k files is very slow
  here (10+ minutes). For targeted work, run aider from the subdirectory with
  `--subtree-only` — the scan finishes in under a minute:
  ```bash
  cd tools/layout-rules && aider --subtree-only apply_layout_blend.py --read README.md --message "..."
  ```
- **Aider wants to edit `.gitignore`:** on first run it offers to add `.aider*`.
  Answer no (or pass `--no-gitignore`) — `.aider.conf.yml` and `.aiderignore`
  are tracked repo files; only the session junk (`.aider.chat.history.md`,
  `.aider.tags.cache.v4/`) is ignored.

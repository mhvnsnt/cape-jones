# code-server — VS Code in the Browser

**Status:** Install-on-demand (documented here, not vendored — install script is the pull).
**License:** MIT. **Stars:** ~70k+.
**Repo:** https://github.com/coder/code-server

## What it is

Full VS Code running in any browser. Self-host on any Linux box. This is the
tool the owner was trying to remember — the top free cloud open-source IDE by
every 2026 ranking (`docs/research/` → CLOUD-RESEARCH.md).

## Install (one command)

```bash
curl -fsSL https://code-server.dev/install.sh | sh
```

Then:

```bash
code-server --bind-addr 0.0.0.0:8080
```

Open `http://<host>:8080` in any browser — including a phone browser.
Password auth is built in (set via `~/.config/code-server/config.yaml`).

## Why install-on-demand

code-server is a system service, not repo content. The install script above IS
the pull — no need to vendor 100MB+ of TypeScript into the repo. Per the
PULL-STRAIGHT-TO-STORE law: the install command lives here in the permanent
store (this repo), and gets run when needed.

## Phone workflow

The owner works from Android. code-server in a phone browser = full VS Code
with terminal, extensions, and file editing — no laptop needed.

## Alternatives (also documented, not vendored)

- **OpenVSCode Server** (MIT, Gitpod-maintained): `docker run -p 3000:3000 gitpod/openvscode-server`
- **Coder** (AGPL-3.0): self-hosted cloud dev environments with AI agent integration

# AniCraft — Clean-Room Adobe Animate Reimplementation (Rust)

**Version:** 0.2.1 (release tag `v0.2.1`) · **Licence:** Apache-2.0 (free, open source)
**Upstream:** https://github.com/storytold/anicraft
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`).
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/anicraft/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `anicraft-0.2.1-linux-x86_64.AppImage` |
| Size | 19,024,376 B (matches published release asset size exactly) |
| SHA-256 | `352456384d1e82f373d836dcbcd9f1473b1603c5c9c7b185d763218470091b31` — **OK vs the project's published `SHA256SUMS.txt`** |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, 44M extracted):
`AppRun`, `ai.storyteller.anicraft.desktop`, `usr/bin/anicraft`,
`usr/bin/anicraft-cli`.

## What it is

A clean-room, open-source 2D animation editor written from scratch in pure
Rust, file-compatible with Adobe Animate (XFL/FLA, SWF) per the project
description. The closest thing in the sweep to a free reimplementation of a
paid animation tool — real, released, and runnable on Linux. Shape tweens,
Bone tool, camera layer.

Note: a second repo of the same name, `soof-golan/anicraft`, describes
itself as "file-compatible with Adobe Animate (XFL/FLA, SWF)" but has NO
releases; the `storytold/anicraft` repo is the one shipping builds.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'anicraft-0.2.1-linux-x86_64.AppImage'
chmod +x anicraft-0.2.1-linux-x86_64.AppImage
./anicraft-0.2.1-linux-x86_64.AppImage
# No FUSE on this VM: extract instead of mounting:
./anicraft-0.2.1-linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## Smoke test (2026-11-20, this Linux VM)

**RAN.** `--version` exit 0; `anicraft-cli render --sample` exit 0 — real
PNG 1280x720, 74,871 B. GUI blocked: `libxkbcommon-x11.so` missing
(apt broken) — the CLI is the usable path here.

## Stage it serves

2D vector/raster animation authoring — the Adobe Animate slot. Candidate
for Animate-format (XFL/FLA) interchange. **Not a Grease Pencil core
replacement** — Grease Pencil stays the rig/animation core; AniCraft is the
interchange/experiment seat. See `tools/free-stack/PIPELINE-STAGE.md` for
this show's exact slot.

## Honest limits

- v0.2.1 is early (0.x). No production history on our shots yet.
- FLA compatibility is claimed by the sibling fork's description, not yet
  proven by us against a real .fla — a follow-up lane must test it.
- No Windows/macOS testing done here (Linux AppImage only).

## Licence

Apache-2.0. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

# Kdenlive — Primary Free Video Editor (NLE)

**Version:** 26.08.3 (released 2026-11-07; maintenance release of the 26.08
series, includes an important security fix for manipulated `.kdenlive`
project files — upgrade advised by the project) · **Licence:** GPL-3.0
(KDE project; GPL per the project's own pages and every independent
listing checked)
**Upstream:** https://kdenlive.org/ — downloads at
https://download.kde.org/stable/kdenlive/26.08/linux/
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`) —
the **PRIMARY free video editor for the stack**: stable, actively
maintained, current release. Olive is the secondary/alpha editor only.
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/kdenlive/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `kdenlive-26.08.3-x86_64.AppImage` |
| Size | 214,346,232 B (confirmed by Content-Length from the KDE mirror and by the completed download) |
| SHA-256 | `2c8322edfc86605e4c98a78a019310d9b4fc46bb8e94e6fe313dc7dd987e7671` (published by KDE alongside the AppImage; verified locally with `sha256sum -c`) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0):
`AppRun`, `org.kde.kdenlive.desktop`, `usr/bin/kdenlive`,
`usr/bin/kdenlive_render`, plus bundled `ffmpeg`/`ffplay`/`ffprobe`.

## What it is

Multi-track non-linear editing, nested sequences, multicam, 3-point
editing, markers, automatic backups, proxy editing, motion tracking,
colour correction, video scopes (histogram, vectorscope, RGB parade,
waveform), subtitling, speech-to-subtitles. Linux (AppImage / Flatpak —
the only two Linux formats the Kdenlive team supports), Windows, macOS,
BSD.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'kdenlive-26.08.3-x86_64.AppImage'
chmod +x kdenlive-26.08.3-x86_64.AppImage
./kdenlive-26.08.3-x86_64.AppImage
# No FUSE on this VM: extract instead of mounting:
./kdenlive-26.08.3-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## Smoke test (2026-11-20, this Linux VM)

**RAN, only with host shims.** Stock fails exit 127 (`libOpenGL.so.0`
missing); works with symlink shim (→ `libGL.so.1`) + vendored libEGL;
GUI under dbus-run-session + xvfb reaches welcome/splash.

## GPU route (owner law: no-GPU is never an excuse)

Kdenlive's OpenGL preview path needs a working GPU context. GPU-dependent
smoke tests run on a working GPU source — **Kaggle GPU first** (validated
live 2026-11-20: `kaggle kernels list --mine` returns marsfmmg's kernels;
T4/P100 free tier, 30 hrs/wk), **Colab second** (free-tier T4 notebook via
browser). Lightning AI is down until its watch reports recovery; Oracle
Cloud free tier is CPU-only and is not a GPU route. Never report Kdenlive
as blocked for lack of a GPU on this box — route the test to Kaggle.

## Stage it serves

Video editing — the primary editor: cutting episodes, assembling renders,
subtitles, colour. This is the editing slot's real answer. See
`tools/free-stack/PIPELINE-STAGE.md` for this show's exact slot.

## Honest limits

- Needs proxies for smooth playback of heavy footage on low-end systems
  (the project's own guidance).
- The 26.08.3 AppImage is ~200 MB; Flatpak is the project's other
  supported Linux route.

## Licence

GPL-3.0. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

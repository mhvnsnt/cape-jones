# Rigby2D — 2D Skeletal Animation (Spine / Moho Slot)

**Version:** 0.5.1 (release tag `v0.5.1`) · **Licence:** Apache-2.0 (free, open source)
**Upstream:** https://github.com/jaisurya-dev-art/rigby2d — docs: rigby2d.com/docs
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`).
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/rigby2d/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `Rigby2D_0.5.1_amd64.AppImage` |
| Size | 96,979,448 B (matches published release asset size exactly) |
| SHA-256 | `27afa7de71a43e2fe45f27e605176a62b9a559db4b7f5f00f3a105870bdbd6ee` — **OK vs the project's published `SHA256SUMS.txt`** |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, 280M extracted):
`AppRun`, `AppRun.wrapped`, `Rigby2D.desktop`, `usr/bin/rigby2d`.

Also published upstream (not pulled): `.deb`, Godot/Unity/Phaser/Pixi
runtimes, `SHA256SUMS.txt`.

## What it is

The strongest live Spine/Moho cover found in the sweep: a real, actively
developed open-source 2D skeletal animation editor with a Linux AppImage —
the role DragonBones' dead editor used to hold. AutoRig layered PSDs,
animate with meshes, IK and physics, lip-sync from audio, render video,
export JSON/.skel. JavaScript, Rust, Godot and Unity runtimes. Built-in
MCP server for AI assistants.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'Rigby2D_0.5.1_amd64.AppImage'
chmod +x Rigby2D_0.5.1_amd64.AppImage
./Rigby2D_0.5.1_amd64.AppImage
# No FUSE on this VM: extract instead of mounting:
./Rigby2D_0.5.1_amd64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## GPU route (owner law: no-GPU is never an excuse)

Rigby2D needs EGL/GPU to run its GUI (it looks for `libEGL.so.1` and a
working EGL context). GPU-dependent smoke tests run on a working GPU
source — **Kaggle GPU first** (validated live 2026-11-20: `kaggle kernels
list --mine` returns marsfmmg's kernels; T4/P100 free tier, 30 hrs/wk),
**Colab second** (free-tier T4 notebook via browser). Lightning AI is down
until its watch reports recovery; Oracle Cloud free tier is CPU-only and
is not a GPU route. Never report Rigby2D as blocked for lack of a GPU on
this box — route the test to Kaggle.

## Stage it serves

2D skeletal/bone rig + mesh animation with game-engine runtimes — the
Spine slot (replacing the dead DragonBones editor) and the Moho slot
(vector/mesh rig + IK + physics). Exports JSON/.skel, so it can feed
engines directly. See `tools/free-stack/PIPELINE-STAGE.md` for this
show's exact slot.

## Honest limits

- v0.5.1 is young and moving fast (0.x); API/format stability is not
  Spine-grade yet. No production history on our shots.
- No headless/CLI proof run done here; GUI-only probing so far. The
  built-in MCP server is a later-lane integration candidate, not tested here.
- Grease Pencil stays the rig/animation core. Rigby2D is the
  skeletal/game-runtime complement, not a core replacement.

## Licence

Apache-2.0. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

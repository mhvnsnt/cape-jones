# Pencil2D — Hand-Drawn Frame-by-Frame (TVPaint Slot)

**Version:** 0.7.2 (release tag `v0.7.2`) · **Licence:** GPL-2.0 (free, open source)
**Upstream:** https://github.com/pencil2d/pencil — https://www.pencil2d.org/
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`).
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/pencil2d/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `pencil2d-linux-amd64-v0.7.2.AppImage` |
| Size | 60,471,800 B (matches published release asset size exactly) |
| SHA-256 | `4034b036258b6a13d4540911ebce085f31ee18a9dacf438845ac71998d42ff91` (size-exact + GitHub release provenance; the project publishes no SHA256SUMS file for this release) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, 154M extracted):
`AppRun`, `org.pencil2d.Pencil2D.desktop`, `usr/bin/pencil2d`, `qt.conf`.

## What it is

Free, open-source, raster+vector hand-drawn animation — the closest free
pen-first frame-by-frame tool not already in the stack. Raster + vector
layers in one timeline, bitmap/vector/camera/sound layers, onion skinning,
direct export to MP4, AVI, animated GIF, PNG sequences. No automatic
tweening, no skeletal bones — every in-between is drawn by hand (by design).

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'pencil2d-linux-amd64-v0.7.2.AppImage'
chmod +x pencil2d-linux-amd64-v0.7.2.AppImage
./pencil2d-linux-amd64-v0.7.2.AppImage
# No FUSE on this VM: extract instead of mounting:
./pencil2d-linux-amd64-v0.7.2.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## Smoke test (2026-11-20, this Linux VM)

**RAN.** `--version` exit 0 under xvfb; GUI alive at 25s.

## Stage it serves

Hand-drawn frame-by-frame / cel animation — the TVPaint slot for roughs,
timing tests, and simple hand-drawn cuts. Lightweight complement to
Tahoma2D/OpenToonz, not a replacement for either. See
`tools/free-stack/PIPELINE-STAGE.md` for this show's exact slot.

## Honest limits

- No bones, no tweening, no mesh deformation — pure traditional
  frame-by-frame. Anything rigged still goes through Blender Grease
  Pencil / Rigby2D / DragonBones.
- Small volunteer project; 0.7.2 is the current stable, not a
  studio-scale pipeline.
- Grease Pencil stays the rig/animation core.

## Licence

GPL-2.0. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

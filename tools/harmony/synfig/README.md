# Synfig Studio — Vector Tweening & Bone Rigs

**Version:** 1.5.5 (dev release, 2026-03-16) · **Licence:** GPLv2+ (free, open source)
**Upstream:** https://www.synfig.org/ · https://github.com/synfig/synfig
**Status in this repo:** BINARY LANDED — this fills the gap left by cape-jones PR #165,
which carried docs only (`production/tools/synfig/README.md`, pins 1.5.5, no binary).

## Landed binary (verified)

| | |
|---|---|
| Release | `harmony-equivalents-20261120` on mhvnsnt/dream-girl |
| Asset | `SynfigStudio-1.5.5-linux64.appimage` (upstream name `SynfigStudio-1.5.5-2026.03.15-linux64-79bf7.appimage`) |
| Size | 115,539,968 B (matches upstream asset size exactly) |
| SHA-256 | `b85aabc26f690a0c150d2143c656c17f358b73abbedf8d01007f15a7a95740e9` — **matches upstream `checksum-sha256.txt` exactly** |
| Format | AppImage, Type 1 (ISO9660 payload) |

Contents verified by ISO9660 parse (1,638 entries: 472 dirs, 1,166 files):
`AppRun`, `synfigstudio.desktop` (Name=Synfig Studio, Exec=launch.sh,
MimeType=application/x-sif), `usr/bin/synfigstudio` (3,014,361 B),
`usr/bin/synfig`, `usr/bin/synfigplayer`, bundled ffmpeg/ffprobe, melt,
sox, ImageMagick, GTK3 stack.

## What it is

Free vector 2D animation with **automatic tweening** — define keyframes, it
generates the in-betweens. 50+ layer types (gradients, distortions, filters),
bone/skeleton system for cut-out rigs, shape morphing, inverse kinematics.
This is the tool that answers the "interpolation" ask **at the authoring
level**: instead of interpolating rendered video frames after the fact, Synfig
interpolates the vector artwork itself between poses.

## Install / run

```bash
# From our release (recommended — verified copy, no upstream dependency):
gh release download harmony-equivalents-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'SynfigStudio-1.5.5-linux64.appimage'
chmod +x SynfigStudio-1.5.5-linux64.appimage
./SynfigStudio-1.5.5-linux64.appimage
# No FUSE on this VM: extract instead of mounting:
./SynfigStudio-1.5.5-linux64.appimage --appimage-extract
./squashfs-root/AppRun
```

Note: this AppImage's runtime needs `libfuse.so.2` to start — this VM has
none. The `--appimage-extract` route works once `libfuse.so.2` is present
(e.g. from the Ubuntu `libfuse2` package, `LD_LIBRARY_PATH` pointed at it).
The contents listing above was done with a read-only ISO9660 parse, no
runtime needed.

## Harmony comparison

| Harmony does | Synfig covers | Gap |
|---|---|---|
| Vector drawing + rigging (deformers, bones) | Bone/skeleton rigs + IK, shape morphing, 50+ layers | No bitmap frame-by-frame drawing strength — pair with Tahoma2D / Pencil2D for that |
| Auto in-betweening (tweening) | Native: keyframes + automatic tweens with per-waypoint easing | — |
| Node compositing | No node schematic | Compositing stays in Tahoma2D / OpenToonz (node schematic) |
| Camera, multiplane | Basic camera/pan | No multiplane camera — Tahoma2D covers it |
| Lip sync, audio | Audio import; no built-in lip sync | Rhubarb (bundled in Tahoma2D) covers lip sync |
| Stability on big scenes | Keep scenes modular, save incrementally | Known stability issues on complex projects; confusing UI for beginners |

**Verdict:** the closest free Harmony-class **rigging/tweening** tool in the
stack — the best new pull of this lane for cut-out character rigs. It does
not replace Tahoma2D (drawing/Xsheet/camera/compositing); it complements it.

## Licence

GPLv2+. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

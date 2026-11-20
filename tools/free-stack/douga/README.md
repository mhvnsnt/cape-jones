# Douga — Pen-First Cel Animation with a Real Dope Sheet (Windows-only)

**Version:** build 1116 (updated 2026-11-17 13:18 UTC) · **Licence:** free
(beta, one person's program; see watermark note below)
**Upstream:** https://douga.app — https://keihoag.itch.io/douga (author: keihoag)
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`) —
browser-downloaded Windows zip, contents verified. **Windows 10 / 11,
64-bit ONLY** — `douga.exe`, Direct3D 11; Wacom / XP-Pen / Huion /
Surface Pen. No Linux build, no macOS build.
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/douga/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `browser-download-20261120T160026.367892390Z-0-douga-windows.zip` |
| Size | 3,766,009 B |
| SHA-256 | `bf3bd41c5593736caf4b7d74ebcf4c00c52766691c3596f3d3c7b34a9ea0b774` |
| Format | Windows zip |

Contents verified (zip extracts clean, 16 entries): `Douga/douga.exe`
(6,263,648 B), `EULA.txt`, `lang/en.ini` + `ja.ini`, plugins (effects
blur/levels/mosaic/noise/sample_invert/smooth, ffmpeg exporter).

Related plugins NOT pulled: douga-rig-import.zip 190 kB, brush_convert
279 kB, video_import 83 kB, update_check 85 kB, poses 13 MB.

## Watermark (honest — do not present Douga as watermark-free)

**Exports from an unlicensed copy carry a small "made with douga.app"
line in the bottom-right corner**; a licence key from douga.app/buy
removes it. The tool itself is free; the watermark-free export is paid.
Log it honestly.

## What it is

Pen-first cel animation with a real dope sheet. Tagline: "Pen-first cel
animation with a real dope sheet." Pressure-sensitive brush engine (ink,
pencil, splatter, marker, airbrush; custom `.dbrush` files), stabilizer,
perspective/grid/symmetry guides, drop a GLB/GLTF/OBJ to trace over, real
dope sheet (keys, holds, loops, exposure on ones/twos, warm/cool onion
skin), scenes > cuts > layers, managed palettes (`.dpal`), one `.dga`
file per project. Export: PNG sequence, GIF, APNG, H.264 MP4 with sound,
built in. "It draws, it times, it saves, it exports." Vector layers +
more of the shooting stage (glow, focus, motion blur) are next, not
shipped.

## Install / run

```bash
# From our release (Windows only — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'browser-download-20261120T160026.367892390Z-0-douga-windows.zip'
# Unzip on Windows 10/11 64-bit and run Douga/douga.exe. No installer, no account.
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## Smoke test (2026-11-20)

**VERIFIED, CANNOT RUN HERE.** Windows-only; zip extracts clean (16
entries, douga.exe 6,263,648 B). No Linux run possible — staged for
Windows only.

## Stage it serves

Pen-first cel animation with a real dope sheet — the TVPaint-adjacent
slot for hand-drawn timing work. Complements Pencil2D (Linux, pulled)
and Tahoma2D (in stack). See `tools/free-stack/PIPELINE-STAGE.md` for
this show's exact slot.

## Honest limits

- Windows-only. Beta, single author. Watermark on free exports (see above).
- Grease Pencil stays the rig/animation core.

## Licence

Free (beta). No purchase, no account, no card. The watermark-free export
key is a paid licence — never a purchase list; the free export with its
small watermark is what is staged here.

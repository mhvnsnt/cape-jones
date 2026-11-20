# Olive Video Editor — Secondary / Alpha NLE (Node-Based)

**Version:** 0.2.0-nightly (build `8ac191ce`, rebuild of master from
2024-12-04; last code change 2023-09-24) · **Licence:** GPL-3.0 (free, open source)
**Upstream:** https://github.com/olive-editor/olive
**Status in this repo:** BINARY LANDED (release `production-stack-free-20261120`) —
as the **SECONDARY / ALPHA editor, not the primary**. Kdenlive is the primary
free editor: stable, maintained, current.
**Staged:** branch `tools/free-stack-wireup-20261120`, 2026-11-20 (Harmony + free-stack wire-up, lane A).
**Source doc:** sweep doc `tools/production-stack-free/sweep/olive/README.md` on dream-girl branch `tools/production-stack-free`.

## Landed binary (verified)

| | |
|---|---|
| Release | `production-stack-free-20261120` on mhvnsnt/dream-girl |
| Asset | `Olive-8ac191ce-Linux-x86_64.AppImage` |
| Size | 154,107,880 B (matches published release asset size exactly) |
| SHA-256 | `30a6c0d18dfb4ff77addd06984348656fd69d153cfa913eb3cde56a60aa14160` (computed locally 2026-11-20; no published sums to check against) |
| Format | AppImage |

Contents verified by `--appimage-extract` (exit 0, 353M extracted):
`AppRun`, `org.olivevideoeditor.Olive.desktop`, `usr/bin/olive-editor`,
plus `crashpad_handler` and `olive-crashhandler` (it ships its own crash
handler — consistent with the alpha/unstable status).

## What it is

Free, node-based, non-linear editor; billed by the project as a
fully-featured alternative to high-end professional editors. The README
itself calls Olive alpha software and highly unstable. The project is
PAUSED, not dead: the official site now serves an "Olive will return"
placeholder; the 0.1.0 alpha and this 0.2.0-nightly are the only GitHub
binaries. Repo last push: 2024-12-05.

## Install / run

```bash
# From our release (recommended — verified copy):
gh release download production-stack-free-20261120 --repo mhvnsnt/dream-girl \
  --pattern 'Olive-8ac191ce-Linux-x86_64.AppImage'
chmod +x Olive-8ac191ce-Linux-x86_64.AppImage
./Olive-8ac191ce-Linux-x86_64.AppImage
# No FUSE on this VM: extract instead of mounting:
./Olive-8ac191ce-Linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
# Or use the shared fetcher (verifies size + sha256, skips already-verified):
bash tools/free-stack/fetch-verify.sh
```

## Smoke test (2026-11-20, this Linux VM)

**RAN.** `--help` / `--version` exit 0 with no display; has `-x` / `--export`
headless mode; GUI under xvfb alive at 25s.

## Stage it serves

Video editing — node-based timeline/compositing experiments, and a fallback
if Kdenlive ever blocks. **NOT the primary editor.** See
`tools/free-stack/PIPELINE-STAGE.md` for this show's exact slot.

## Honest limits

- Alpha, unstable by its own README; community reports freezes several
  times per hour on the stock AppImage. No releases since Dec 2024; no
  code changes since Sep 2023.
- **Do NOT cut anything deadline-critical in Olive. Kdenlive is the editor
  for real work.**

## Licence

GPL-3.0. Repo integration is legal — document the version pin on upgrade.
Source + licence logged honestly next to the item, per lane rule; licence
never gated the pull.

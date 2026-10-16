# Retry Pulls — Failed Clones Recovered (2026-10-16)

These tools failed to clone during the original pulls (network issues) and were
recovered on 2026-10-16.

## LDF-VFI (xypeng9903/LDF-VFI)
- **What:** LDF-VFI — CVPR 2026 generative video frame interpolation
- **URL:** https://github.com/xypeng9903/LDF-VFI
- **Size:** ~73MB (code only, no weights)
- **License:** Check repo LICENSE before commercial use
- **Weights:** Download separately (not included)

## SCAIL-2 (zai-org/SCAIL-2)
- **What:** SCAIL-2 — skeleton-free character animation
- **URL:** https://github.com/zai-org/SCAIL-2
- **Size:** ~47MB (code only)
- **License:** Check repo LICENSE before commercial use

## coa_tools2 (hcqmaker/coa_tools2)
- **What:** COA Tools 2 — Blender 2D cutout rigging tools
- **URL:** https://github.com/hcqmaker/coa_tools2
- **Size:** ~19MB
- **License:** GPL (per repo)

## Notes
- All cloned with `--depth 1` (shallow), `.git` stripped, committed as regular files
- `three-anime-style` (xymeow) and `video-gif-studio` (miles990) were also on the
  retry list; three-anime-style was already pulled by a sibling agent.
- `video-gif-studio` repeatedly timed out on clone (network) — still pending,
  retry when network is stable.
- `layerinbetween` and `InstanceAnimator` were on the original failed list but
  verified already present in ~/workspace/tools/ — no re-pull needed.

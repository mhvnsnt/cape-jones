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
- `three-anime-style` (xymeow, MIT): the retry-list note claiming "already pulled by a sibling agent" was verified FALSE on 2026-10-16 — it was NOT on main. Pulled fresh (22MB) via PR #38.
- `video-gif-studio` (miles990): RECOVERED via PR #34 (126MB, `--filter=blob:none` after 6 attempts). On main.

## hyperframes-effects-gallery (genoooool)
- **What:** 445-effect catalog (transitions 184, captions 58, camera motion 25, emphasis 24, asset presentation 36, rhythm/mood 37, info cues 67, texture/finish 14) — HyperFrames/Remotion/WebGL/GLSL, with pinned sources, license notes per effect, and copyable AI integration briefs
- **URL:** https://github.com/genoooool/hyperframes-effects-gallery
- **Size:** ~427MB (230MB preview MP4s/posters in assets/; catalog JSON 1.5MB; llms-full.txt 431KB)
- **License:** no top-level license file — upstream sources keep their original licenses/authors' terms per THIRD_PARTY_NOTICES.md. Check per effect before reuse.
- **Live gallery:** https://77654321.xyz
- `layerinbetween` and `InstanceAnimator` were on the original failed list but
  verified already present in ~/workspace/tools/ — no re-pull needed.

# tools/ — commercial-grade rigging / animation tooling (vendored 2026-11-23)

Owner direction 2026-11-23 07:28 EST: pull in top-level commercial-grade tooling, wire it into the repo. Full audit: `docs/TOOLING-AUDIT.md`.

## What is here

| Path | What | Licence | Proven |
|---|---|---|---|
| `tools/coa-tools2-aodaruma/coa_tools2/` | COA Tools 2 v2.3.0 (Aodaruma), source text files. Release zip sha256 `5719aa99d7257ddd931979371459a6221cb9e651dc434f7863b833a31deae66d`. | GPL-3.0-or-later | ENABLE-OK on Blender 5.0.1 (this VM, headless). Operators `coa_operator` / `coa_tools2` present. |
| `tools/wiggle_2.py` | Wiggle 2 v2.2.3 (shteeve3d), single file. sha256 `570ae0a1a17800ba13f38f8bfdae4068d4c0b88dad237f4a0f32237d6b9ab21e`. | GPL-3.0 | ENABLE-OK on Blender 5.0.1. `bpy.ops.wiggle` present. |
| `tools/wiggle-bones/wiggle_bones/` | Wiggle Bones v1.1.2 (Hans-xwh), the maintained Blender-5 successor of Wiggle 2. Zip sha256 `75789f3186db47778e04dea93b3c500bc6f2f79a46a1611daa4b26a07cac3167`. | GPL-3.0-or-later | ENABLE-OK on Blender 5.0.1 (twice). Prefer this one for new cape work. |

## Install (Blender 5.0.1)

Put each addon path under Blender's scripts `addons/` directory, then enable
`coa_tools2`, `wiggle_2`, and `wiggle_bones` in Edit → Preferences → Add-ons.

- **Wiggle 2 filename matters:** the release file is named `wiggle_2-v2.2.3.py`.
  That name does NOT load — Blender cannot import a module name with hyphens
  and dots. It must be installed as `wiggle_2.py`, which is how it is vendored
  here. If you re-download it, rename it before installing.
- **COA Tools 2 icons are missing here on purpose:** `icons/*.png` and
  `icons/*.dat` are binary and cannot be carried by the GitHub connector.
  The addon enables and works without them. For the full release (with icons),
  run `tools/fetch-tooling.sh` — it downloads the three release zips and
  verifies their sha256 hashes.
- **Do NOT use the repo's other COA copy for this VM:**
  `production/tools/coa_tools2/` is the hcqmaker fork v2.3.1 for Blender 5.1.2
  and FAILS to enable on Blender 5.0.1 (PEP 701 f-string, Python 3.12+ only).
  Use the Aodaruma v2.3.0 vendored here until the VM moves to Blender 5.1.2+.

## What is NOT here (and why)

- **AnimLab** — freeware, not open source; its binary stays external. Only its
  docs/proof belong in the repo (see PR #429, open). Peg/deformer still partial.
- **EEVEE** — no repo file; it is a VM package gap. `libegl1` is now installed,
  but headless EEVEE still fails (`EGL_BAD_MATCH`) on this VM. Cycles (CPU)
  stays the working headless renderer.
- **Gumball `.fla` rigs** — 0 on disk; the 9 files sit in an unverified draft
  release on `mhvnsnt/cn-gigaleak-gumball`. Study-only when fetched; never
  ingest leaked art into show files.

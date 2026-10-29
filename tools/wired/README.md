# Wired tools — Cape Jones show process (wired 2026-10-28 21:32-21:33 CDT)

Location: `~/workspace/ep1-farm/tools/wired/` — all four surveyed tools, copied from their source repos (originals untouched). These tools VERIFY and GUARD; they never edit a `.blend` file. The locked approved files were verified untouched after wiring (sit timestamp 2026-10-28 21:18:51, guard timestamp 2026-10-28 21:21:11).

## 1. verify_proof.py (Mochiichao `show/production/tooling/proof-gate/verify_proof.py`, 37,464 bytes, sha 511f3007f7ff)
- Use: `python3 verify_proof.py <clip.mp4> [--json-out result.json] [--likeness canon-reference.png]`
- Measures a proof clip without trusting the producing lane: ffprobe spec, frame-to-frame difference, near-identical fraction (held/still footage), hold profile, sha256. It MEASURES only — verdict is owner viewing, by design.
- Tested 2026-10-28: on a 2s solid-colour test clip it correctly reported near_identical_frac 1.0 and "MEASURED — owner viewing decides".
- Note: no `--help` flag — usage is positional (passing `--help` is treated as a clip path and asserts). Use the usage line above.

## 2. disk_guard.py (Mochiichao `show/production/tooling/disk-guard/disk_guard.py`, 30,619 bytes, sha 70bba1efc31a)
- Use: `python3 disk_guard.py preflight --expect-bytes <bytes> --path <dir>` (exit 0 GO / 3 NO-GO); also `check`, `inventory`, `reap` (dry-run unless `--apply`), `publish-evict`.
- Tested 2026-10-28: preflight on `~/workspace/ep1-farm` for 100 MB → GO, 50.7 GB free, canary write ok, quota not blocked.
- Rule going forward: run preflight before any 150+ MB `.blend` save/render job.

## 3. an.mjs (game-reverse-engineering `toolkit/scripts/gltfx/an.mjs`, 3,958 bytes, sha 5ce4e69a1452)
- Use: `node an.mjs <file.glb>` — GLB skin/weight audit: verts, skinned prims, bones, bones used, unweighted verts, weight-sum deviations >0.05, bbox.
- Deps (installed in `tools/wired/node_modules/`): `@gltf-transform/core`, `@gltf-transform/extensions`, `meshoptimizer`, plus `@gltf-transform/functions` (needed by whp, installed 2026-10-28).
- Tested 2026-10-28: on `alisa-own-rig.glb` → 51,133 verts, 160 bones, 125 used, unweighted 0, badNorm 0 — clean.

## 4. whp.mjs (game-reverse-engineering `toolkit/scripts/gltfx/whp.mjs`, 6,503 bytes, sha c5b4ba86616c)
- Use: `node whp.mjs IN.glb [OUT.glb] [--report report.json]` — lossless-to-the-eye GLB pipeline (dedup, quantize, meshopt/webp) with a no-cut gate: fails if any count changes.
- Tested 2026-10-28: on `alisa-own-rig.glb` → 41.35 MB to 4.66 MB, "no-cut OK", cuts []. Note on its report: after-counts for skins/joints are summed per skin (18 skins × 160 joints = 2,880 joint references) vs before-counts per file — that is a counting-basis difference, not a cut; the gate's own verdict (cuts []) is the signal.
- Caution: on pose-only GLBs with no meshes, its prune step removes unused skins/joints and reports CUT — that is the gate working (flagging, not silently passing). Use it on mesh GLBs for the no-cut guarantee.

## Still missing (not in either repo, still owed)
One small new Blender script that runs INSIDE a `.blend`: lock all actions (fake_user), bake deform→FK for constrained rigs, check body-to-rig alignment before render, and verify action/bone/bbox/weights after. The four tools above gate everything around it (proof, disk, GLB stage) but do not replace it.

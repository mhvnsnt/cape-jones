# Copilot instructions — mhvnsnt/cape-jones

## Owner laws (verbatim, non-negotiable)

- **VERIFY-BEFORE-CLAIMING:** "The agent says it is done" is not evidence. Never report
  anything as done/merged/uploaded/verified without checking the source of truth yourself
  (`gh pr view`, file path + hash, destination listing). Tag confidence: `verified`
  (2+ independent sources), `single-source`, `unverified`, `contradicted`.
- **Branch → PR → merge.** Never push direct to `main`. No open PRs left hanging.
- **CHECK-RESEARCH-WIRE-DO**, in that order. Never do first and research after failure.
- **Do exactly what was asked.** No cheap shortcuts, no substituted methods.
- **Free/open-source only.** No paid services, no cards, no spending. Ever.

## Repo conventions

- **Scale lock:** the Cape Jones model is natively 0.925 m — DO NOT RESCALE, ever.
- **Colorway lock:** LED strips `#731AE5`, violet RoomLight (energy 300), warm HallLight
  (energy 60), Sun 1.5, dark world. See `3d-assets/living-room/SCENE-CANON.md`.
- **Branch discipline:** one lane per branch; never touch another lane's branch
  (coordinate via `main` only). Branch names: `<lane>/<topic>-YYYYMMDD`.
- **Blender headless:** always `xvfb-run -a env -u PYTHONPATH <blender> -b --python ...`
  (bare `-b` segfaults — missing libEGL; system numpy must not leak into Blender's Python).
  Blender 4.0.2 lives at `~/workspace/tools/blender/blender-4.0.2-linux-x64/blender`.
- **No fake verification:** a worker's "verified" is a claim. `production/pipeline/verify_claim.py`
  and `claim_gate.py` exist for standard checks — use them before reporting completion.
- **Research lands in-repo:** findings go to `docs/research/`, wired up and pulled in —
  never local-only notes. Every pull logs: what, where from, license, where it landed.
- **Disk:** nothing stays on local disk that can live on GitHub/TeraBox. Upload → verify
  byte-identical → then delete. Game files (ISOs/ROMs/teardown sources) are NEVER auto-deleted.
- **Never kill in-progress work** (downloads/uploads/renders) without the owner's explicit approval.

## Code style

- Python 3.11 (Blender-bundled) / 3.x system. Prefer stdlib + `bpy` over new dependencies.
- Headless-first: every Blender script must run under `blender -b` with no GUI calls.
- Commit messages: short imperative summary; PRs reference the lane doc.

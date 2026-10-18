# TEAM-CONVERSATION.md — Cape Jones rig-perfection wave

Coordination log for the lanes working the rig perfection wave. Each lane posts what it
touched, what it needs from others, and what it deliberately did NOT touch.

---

## 2026-10-18 — rig-perfection / best-rigging-tech research lane (restart)

**Lane:** autonomy research + Wiggle 2 pull + wiring. Branch: `pull/wiggle2-20261017`.

**Touched (mine, committed in my PR):**
- `docs/research/BEST-RIGGING-TECH-2026.md` — full autonomy ranking (20 systems, grades A–D),
  updated with the 2026-10-18 restart addendum.
- `production/tools/wiggle2/` — vendored Wiggle 2 v2.2.4 (GPL-3.0, byte-identical to upstream),
  proof script + 3 proof renders, `CAPE-JONES-WIRING.md` (new: chain-build/bind/bake template).

**Verified, not relayed:** addon enables in headless Blender 4.0.2; proof renders own-eyes;
upstream hash match. Rig introspection: `CapeJones_Rig` = 94 bones, **zero cape bones** —
the cape chain gets built by the wiring, not found.

**Needed from other lanes:**
- **Spine lane:** run the Wiggle cape wiring only on your SETTLED rig file, never a WIP .blend.
  The wiring is additive (new armature + modifier), it never edits existing bones.
- **GPU lane:** Puppeteer vs TokenRig vs UniRig neural-skinning bake-off against W5r stays yours.
- **GNM head / MPFB lanes:** face and parametric body stay yours — no overlap.

**Deliberately NOT touched (other lanes' work, left in the tree):**
- `3d-assets/cape-jones-rig/spine-lane/`, the `cape_jones_rigged_w5r.blend` edit
- `3d-assets/face-rig/` (scratch files, `cj_face_*`, `face-rig/README.md` edit)
- `docs/research/GNM-HEAD.md`, `tools/pulled/GNM/`, GNM section of `tools/pulled/README.md`
- `production/tools/mpfb2/`

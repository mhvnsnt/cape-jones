# TEAM-WORKFLOW — one team, one room

**Purpose:** every agent, IDE, and CLI working on the Cape Jones living room
works as ONE team. This doc says what each piece is for, when to use which,
and the discipline that keeps lanes from clobbering each other.

**Standing laws (not repeated, just named):** VERIFY-BEFORE-CLAIMING,
CHECK-RESEARCH-WIRE-DO, PUSH-AFTER-EVERY-TURN, CHECK-BEFORE-START,
RESEARCH-TO-REPO — see `AGENTS.md`.

---

## 1. The pieces and when to use which

| Piece | What it is | Use it when… | Don't use it for… |
|---|---|---|---|
| **Local Blender CLI** (4.5.12 LTS, `tools/` scripts) | Headless Blender on this VM (`-b` + `xvfb-run`). CPU only. | Layout applier, validators, quick logic tests, addon smoke tests, compositor work. | Final-quality GPU renders (no GPU here). |
| **Kaggle GPU lane** (`docs/research/FREE-3D-TOOLS.md` §1a) | 2× T4, 30 GPU-h/week, headless via Kaggle API (already authed). | Batch Cycles renders, TripoSR/TRELLIS prop gen, Upscayl/Real-ESRGAN upscales — anything needing CUDA. | Interactive iteration (12 h session cap; quota is shared — CHECK-BEFORE-START, another chat runs a render lane). |
| **Colab notebook** (`notebooks/colab/`, `docs/pipeline/COLAB.md`) | Interactive T4, human presses Run-all. | Visual smoke tests, quick look-dev, owner-run renders. | Unattended batch (idle timeout ~90 min kills it). |
| **Aider** (`docs/dev/AIDER.md`, `.aider.conf.yml`) | AI pair programmer for code/docs. Free model: `gemini-exp`. | Iterating `tools/` scripts, drafting docs, reviewing diffs. `--subtree-only` for speed. | `.blend` files (binary — work through the applier scripts). API keys never in chat/files. |
| **Cline** (`setup/cline-20261016`, `.clinerules`) | Autonomous coding agent in VS Code. | Multi-step repo tasks inside the editor. | Anything outside its lane's files without checking. |
| **VS Code / Codespaces** (`.vscode/`, `.devcontainer/`) | One-click cloud IDE (Blender 4.5.12 pinned). CPU-only free tier. | Script iteration with a real editor + debugger. | GPU renders (no GPU on free Codespaces). |
| **blender-mcp** (`tools/blender-mcp/`) | MCP server: scene info, screenshots, `execute_blender_code`, export. 9 tools, MIT. | Screenshot→move→re-render micro-adjustments with any MCP client (Cline, Claude Code). | Re-layout from scratch — the JSON contract stays source of truth; write MCP moves back into it. |
| **Layout engine** (`tools/layout-rules/`) | JSON contract + headless validator + Blender applier. | EVERY furniture move. Validate first (seconds, no GPU), then apply. | — |
| **Lighting** (`tools/lighting/`) | Light It Up 4.0.0 (free, GPL): 17 editable studio rigs. | Look-dev lighting moods; bake the winner into the scene. | Final look without owner eyes on a render. |
| **Scatter** (`tools/scatter/`) | GScatter (free, GPL): geometry-nodes scattering. | Clutter/detail passes (rug fibers, shelf items). | Hero furniture (that's the layout engine's job). |
| **Camera match** (`tools/camera-match/`) | fSpy + importer (GPL): solve a camera from the 2D reference. | Aligning 3D renders against the owner's drawing. | — |
| **HDRI/textures** (`tools/hdri-textures/`) | Poly Haven + ambientCG fetchers (CC0). | IBL, wall/floor PBR. 1k is enough for interiors. | Pulling 8k "just in case". |
| **Proc textures** (`tools/textures-proc/`) | procedural-pbr (MIT, runs now), Material Maker (MIT, GPU lane). | Tiling surfaces, canon-tinted materials. | AI-service textures for shipping (terms unverified — look-dev only). |
| **Denoise/upscale** (`tools/upscale-denoise/`) | OIDN in-Blender (done), compositor upscale (done), Upscayl/Real-ESRGAN (GPU lane). | Render cleanup. | Claiming AI upscale ran on the CPU VM (it needs Vulkan/CUDA). |

**Decision shortcut:**
- Moving furniture? → layout engine (JSON → validate → apply).
- Making a prop? → Kaggle (TripoSR/TRELLIS) → recolor to canon → drop in `3d-assets/living-room/props/` + NOTE-TO-BUILD-LANE.md.
- Lighting mood? → Light It Up preset → render → owner judges.
- Need it fast and headless? → local Blender CLI. Need GPU? → Kaggle (check quota first) or Colab (interactive).

---

## 2. Branch discipline — how lanes share the repo

- **Worktrees off `origin/main`.** Every lane: `git worktree add -b <lane>/<name>-<date> ~/workspace/<dir> origin/main`. Never clone into `/tmp` (512M tmpfs).
- **One branch per lane.** This lane: `setup/more-3d-tools-20261016`. The build lane owns `build/living-room-relayout-20261016` (and `build/living-room-rev2-20261016`). **Never push into another lane's branch.**
- **Owned files are off-limits:** `.vscode/` + `.devcontainer/` (cloud-ides lane), `.aider*` (aider lane), `.clinerules` (cline lane), `notebooks/colab/` (colab lane). Touch them only if the owning lane asks.
- **PR → green → merge.** Branch → PR → verify checks green → merge. No direct pushes to `main`. No open PRs left sitting.
- **CHECK-BEFORE-START, every time:** before a render, a GPU burn, or touching the `.blend`, check the other lanes (worktrees, checkpoints, other chats). The Kaggle quota and the living-room `.blend` are shared resources.

## 3. COLORWAY LOCK

Nothing ships unless its base colors are exactly these hexes (from
`3d-assets/living-room/SCENE-CANON.md`). Verify in the material panel, not by eye.

| Hex | Name | Used on |
|---|---|---|
| `#F15E57` | coral pink | chair upholstery, rug field |
| `#5B84DD` | blue | sofa upholstery, mug |
| `#E59964` | warm oak | chair frame, coffee table, TV cabinet |
| `#731AE5` | violet LED | LED strips (emission ~4.0), RoomLight |
| `#FFE996` | amber | lamp shades |
| `#9B4C49` | rug trim | rug ring |
| `#BDD2D6` | silver | chair base, lamp poles, VCR body |
| `#D1C7B8` | warm bone | walls |
| `#735238` | dark warm brown | floor |

AI/procedural outputs NEVER match canon out of the box — strip their textures
and apply canon materials (recipe in `docs/research/FREE-3D-TOOLS.md` §2b).

## 4. Handoff pattern

- **Props:** `3d-assets/living-room/props/` — GLB + preview PNG + `NOTE-TO-BUILD-LANE.md`
  (template in `props/README.md`). The build lane imports, validates, places, renders.
- **Layout changes:** edit `3d-assets/living_room_layout.json`, run the validator,
  then the applier. The JSON is the reviewable contract — never "just move it in Blender."
- **Findings:** research lands in `docs/research/`, wiring lands in `tools/` with a
  README. A finding without a pull-in is incomplete (RESEARCH-TO-REPO).
- **Status claims:** tag every claim (`verified` / `single-source` / `unverified` /
  `contradicted`) and check the thing yourself — never relay another agent's
  "done" as fact (AGENTS.md).

## 5. The loop (normal week)

```
owner direction / drawing (ground truth)
  → layout JSON → validate → apply → render (Kaggle/Colab)
  → owner-eyes check → adjust JSON → …
props: AI/procedural/CC0 source → canon recolor → props/ + note → build lane places
```

Furniture FIRST (owner staging law), then window + doorway (Archimesh),
then wall decor, then the rest. The chair stays EMPTY until the character
rig lands (light-flicker gag).

# afk-rig — Cape Jones wiring

**What:** afk-rig 0.1.2 (afk.ai) — free, local auto-rigging for 3D models,
**built to be driven by an AI agent**. Deterministic auto-fit skeleton +
AI-in-the-loop joint correction + skin-weight rules + export, all through a
CLI or an MCP server on stdio. MIT license, assets CC0.

Pulled 2026-10-17 by the overnight idle pipeline (npm tarball vendored —
no public GitHub repo; tarball at
https://registry.npmjs.org/afk-rig/-/afk-rig-0.1.2.tgz, 17MB total,
largest single file 5.0MB — under the 50MB repo-binary rule).

**Why here:** it slots into THREE standing lanes at once:
1. **"Auto-rig Tripo models perfectly"** (owner, 2026-10-17) — one-shot
   `auto` command: skeleton fit + bind + export in a single call. Complements
   TokenRig (ML single-pass, needs GPU) and BlenRig 6 (artist control rig):
   afk-rig is the **CPU/local deterministic pass** — no GPU needed, no
   weights download, runs on the VM or anywhere Node runs.
2. **Weight-painting pipeline sweep** (owner, 2026-10-17) — the W5r
   bake-off winner has defect zones at shoulders/feet needing manual
   cleanup. afk-rig's `weights` rules (`--add '{"mode":"only"|"never",...}'`
   by bone/box/sphere/mesh/`piece_at`) plus `render --weights`,
   `slice --axis`, and `ray` give exactly the surgical weight-inspection and
   weight-fixing workflow that sweep was missing. Use it to repair the W5r
   defect zones and to re-skin the cape attachment zone.
3. **Animation lanes** — 178 animation clips ship on the human skeleton
   (10 walk variants, idles, mocap set, addon set). Free CC0 test-drive
   library for EP01 animation blocking before final animation is authored.

**Verified this lane (2026-10-17, own-eyes):**
- `package.json` license = MIT; `LICENSE` (MIT) and
  `assets/LICENSE-CC0.md` (CC0 1.0 Universal — "even for commercial
  purposes") verified on disk. License gate PASSED for code AND assets.
- `npm install --omit=dev` → `afk-rig --help` prints the full command
  list cleanly; `skeletons` returns 9 rigs (human: 66 bones incl. fingers);
  `animations human --search walk` returns 10 walk clips. CLI works.
- `node_modules/` was removed before commit — never committed per law.
  (Setup step below re-installs it; it is NOT in the repo.)

## Setup

```bash
cd production/tools/afk-rig
npm install --omit=dev   # ~121 packages; NOT committed to the repo
node dist/cli.js --help
# or: npx afk-rig ... (if linked: npm link)
```

MCP (for AI-agent drivers — Claude Code, Cursor, Windsurf, Claude Desktop):

```bash
node dist/cli.js mcp     # MCP server on stdio
```

## Contents

| Path | What |
|---|---|
| `dist/cli.js` | CLI (`afk-rig`) |
| `dist/index.js` | Programmatic API |
| `assets/rigs/rig-*.glb` | 9 template skeletons: human (66 bones, fingers, 178 anims), fox, horse, bird, dragon, kaiju, spider, snake, fish |
| `assets/animations/*.glb` | 250+ CC0 clips (human-base, human-addon, human-mocap, + per-creature packs) |
| `assets/animations/catalog.json` | Animation catalog with names/seconds/root_motion |

## Usage — one-shot auto-rig (Tripo / any GLB)

```bash
node dist/cli.js auto model.glb --skeleton human --out rigged.glb --animations all
# GLB + glTF input (incl. Draco/meshopt). Convert FBX/OBJ → GLB first.
# No T-pose required: T-pose, A-pose, arms-down all handled; animations adapt to arm angle.
```

## Usage — AI correction loop (when auto-fit gets it wrong)

This is the tool's actual design: the agent inspects renders and adjusts.

```bash
node dist/cli.js start model.glb --skeleton human --hands all-fingers   # creates model.afk-rig.json project
node dist/cli.js render model.glb --joints all --labels --out check.png # skeleton drawn on the mesh, rulers in model units
node dist/cli.js inspect model.glb --issues        # lists joints that look off
node dist/cli.js slice model.glb --axis y --at 0.9 # cross-section at height
node dist/cli.js ray model.glb --from x,y,z --dir x,y,z
node dist/cli.js set model.glb elbow_l=x,y,z --mirror        # move + mirror
node dist/cli.js aim model.glb --joint upperarm_l --at x,y,z # point a limb at a spot
node dist/cli.js fit model.glb --joints elbow_l,elbow_r       # re-fit selected joints
```

## Usage — skin weights (W5r defect-zone repair)

```bash
# Cape Jones weights come from the W5r bake-off winner (see weight-bakeoff docs).
# Use these rules to pin down the shoulder/feet bleed zones:
node dist/cli.js weights model.glb --add '{"mode":"never","bones":["thigh_l*","thigh_r*"],"piece_at":[0.1,0.55,0.0]}'
node dist/cli.js weights model.glb --add '{"mode":"only","bones":["shoulder_l","upperarm_l"],"box":{"min":[-0.2,1.2,-0.1],"max":[0.0,1.5,0.1]}}'
node dist/cli.js render model.glb --weights --bone shoulder_l --out weights-check.png
node dist/cli.js undo model.glb --steps 1
node dist/cli.js bind model.glb --rest limbs
node dist/cli.js export model.glb --out cj-afk-rigged.glb --animations Walk,Idle_A
```

Rules apply in order, broad first; `"thigh_l*"` = thigh_l and below;
`piece_at` selects the connected mesh piece nearest a point (use for the
cape attachment). `meshes --exclude` keeps props/floors out of fitting
and skinning.

## Usage — animation library (EP01 blocking)

```bash
node dist/cli.js animations human              # full human clip list (178)
node dist/cli.js export model.glb --out cj-animated.glb --animations all
# Export with --arm-spread / --ground / --head-correction as needed.
```

## Cape-specific notes

- Cape Jones is native 0.925m — the human skeleton auto-fit measures the
  mesh, so no rescale is needed (scale stays locked per owner law).
- The cape is a separate cloth-sim piece: exclude it from fitting/skinning
  (`meshes --exclude <cape-mesh-id>`) so auto-fit never treats it as legs,
  then skin it in its own pass. The afk.ai docs flag "long coats / capes"
  as the exact case where the AI correction loop pays off.
- Fingers: use `--hands all-fingers` on `start` (Cape Jones's hands are
  visible in dialogue scenes).

## Compared with the other rig lanes in this repo

| | afk-rig (here) | TokenRig (`skintokens-autorig/`) | BlenRig 6 (`blenrig6/`) | Pinocchio |
|---|---|---|---|---|
| Method | Deterministic fit + agent loop | ML single-pass (skeleton+weights) | Artist control rig | CPU skeletonization |
| GPU | No | Yes (≥14GB VRAM, Kaggle) | No | No |
| Weights download | None | ~GBs, Kaggle-side | None | None |
| Best for | Fast local pass, weight surgery, anim library | Best single-shot quality | Film-quality control | Quick skeleton |
| Output | GLB, CC0 anims | GLB | Blender rig | JSON skeleton+weights |

Recommended order for a new Tripo model: afk-rig `auto` (seconds, local)
→ inspect; if joint placement is solid, done. If the mesh is unusual,
TokenRig on Kaggle for the ML pass, then BlenRig for the final control rig.

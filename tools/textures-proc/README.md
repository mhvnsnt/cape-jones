# textures-proc — procedural + AI texture generation, free tiers

## RUNNING TODAY (verified 2026-10-17)

### procedural-pbr — MIT, numpy/PIL, zero GPU

`whappens/procedural-pbr` (also `forcequady/procedural-pbr`) — tiny Python CLIs
that generate seamless tileable PBR sets (albedo, normal, packed ORM,
displacement) for water and clouds. **MIT license.**

Verified run: `python3 generate_water_pbr.py 1k` → 4 PNGs at 1024×1024 in ~15 s,
all real image bytes (viewed the albedo — seamless blue water).
```bash
pip install numpy pillow
python3 generate_water_pbr.py 1k   # or generate_clouds_pbr.py 1k
```
Use for: stylized water, sky/cloud planes, any tiling surface that needs to be
canon-tinted (recolor the albedo to a canon hex after generation).

### Material Maker — MIT, the free Substance Designer

`RodZill4/material-maker` — node-based procedural PBR authoring (Godot-based),
exports metallic/roughness PBR PNG sets. **MIT license**, ~6k stars.
There's also a 2026 MCP server for it (`graysonchalmers/Tool-MaterialMaker-MCP`,
MIT) that authors node graphs from natural language and renders them.

Status: **documented, not run on this VM** — headless export needs the desktop
app under a real GL context (`--export-material` flag; do NOT pass `--headless`;
needs `steam_appid.txt` containing `4110830`). Run it on the Lightning/GPU lane
under xvfb, or any desktop. Recipe for that lane:
```bash
# under xvfb on a GPU box:
./MaterialMaker.x86_64 --export-material /path/to/material.ptex --output-dir ./out
```

## Free-tier AI texture services (documented, terms NOT fully verified)

| Service | Free tier | License on free outputs | Verdict |
|---|---|---|---|
| **Poly** (withpoly.com) | Free version exists; paid from $5.99/mo | Unverified | ⚠️ Do not depend on it until a browser lane confirms the free tier's commercial terms. |
| **Meshy** | 100 credits/mo, no card | CC BY 4.0 (attribution) | ⚠️ Runner-up per `docs/research/FREE-3D-TOOLS.md` §2c — textures via the same account. |
| **Layer / Scenario** | Trials/credits | Varies, mostly commercial-hostile | ❌ Skip. |

**Lane rule:** for anything that ships, prefer the two verified-MIT paths above
or CC0 sources (`tools/hdri-textures/`). AI-service textures are for look-dev
only until their free-tier commercial terms are confirmed in writing.

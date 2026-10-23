# blender-mcp — agent "eyes + hands" for the living room

**What:** the community Blender MCP server (`ahujasid/blender-mcp`, MIT) — an MCP
server that talks to Blender over a socket (`localhost:9876`) via a Blender add-on.
An agent (or any MCP client) gets scene inspection, viewport screenshots,
arbitrary `bpy` execution, and export tools — the screenshot→move→re-render
refinement loop from `docs/research/AI-SCENE-LAYOUT.md` §6 step 6.

**Verified 2026-10-16/17 by this lane (real run, not docs):**
- `pip install blender-mcp` → installs `blender-mcp 2.0.0` + `mcp-for-blender 2.1.9`.
- Real MCP client handshake (`initialize` + `tools/list`) over stdio succeeded.
- **9 tools listed:** `get_addon_status`, `disable_telemetry`, `get_scene_info`,
  `execute_blender_code`, `record_trajectory_feedback`, `look`, `generate_3d`,
  `search_assets`, `import_asset`.
- Server starts cleanly headless; Blender connection is refused until the Blender
  add-on's MCP server is started — expected, tool listing works regardless.

## Install

```bash
# server (any machine with Python 3.10+)
pip install blender-mcp          # or: uvx blender-mcp

# Blender add-on (GUI, one time):
# Blender → Edit → Preferences → Add-ons → Install → addon.py from
# https://github.com/ahujasid/blender-mcp → enable "Interface: Blender MCP"
# Then in the 3D viewport: N-panel → BlenderMCP tab → "Start MCP Server"

# disable telemetry on first run (the server phones home otherwise)
# call the disable_telemetry tool once, or set BLENDER_MCP_DISABLE_TELEMETRY
```

Headless add-on install is possible but the socket server needs a running Blender
with the add-on enabled — on this VM use `xvfb-run` for a virtual display.

## MCP client config

`mcp-config.json` in this folder — drop it into Cline (`~/.config/Code/.../cline_mcp_settings.json`
`mcpServers` section), VS Code MCP config, or Claude Code `.mcp.json`:

```json
{ "mcpServers": { "blender": { "command": "uvx", "args": ["blender-mcp"] } } }
```

For aider (no native MCP): aider drives Blender through the repo's headless
scripts (`tools/layout-rules/`, this folder's recipes) instead — see
`docs/dev/TEAM-WORKFLOW.md`.

## Safety

- `BLENDER_MCP_SAFE_MODE=1` blocks file/network/process access in
  `execute_blender_code` scripts. Use it for any untrusted prompt chain.
- The server executes LLM-generated code **inside Blender without guards**
  (same warning as the official Blender Lab MCP). Run it on a machine with
  nothing sensitive — the Kaggle/Colab GPU lanes qualify.

## What it does NOT replace

The JSON layout contract (`3d-assets/living_room_layout.json`) stays the source
of truth. MCP moves are micro-adjustments; write them back into the JSON and
re-run `tools/layout-rules/validate_layout.py`. Never let the agent re-layout
the room from scratch through MCP.

## Alternatives (researched, not pulled)

| Server | Note |
|---|---|
| Official Blender Lab MCP (blender.org/lab/mcp-server) | Real, but docs lookup + scene analysis only, needs Blender 5.1+. Weaker. Skip. |
| RFingAdam/mcp-blender | 218 atomic tools, mesh editing, GeoNodes, vision refinement loop. Heavier; evaluate if 9 tools prove limiting. |
| djeada/blender-mcp-server | 27 tools, async job queue for long scripts — interesting for long Cycles renders. Install from git URL; not run by this lane. |
| sandraschi/blender-mcp | ~58 tools, headless + live bridge, VSE/splat support. Broad; treat as reference. |

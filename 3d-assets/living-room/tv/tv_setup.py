"""Functional TV setup for the Cape Jones living room scene.

Applies to 3d-assets/living_room.blend (run by the integration lane — this
script is NOT committed alongside a modified .blend):

  1. Screen content: wires the 48-frame original loop in frames/ onto
     crt_screen's tvScreenMat as a cyclic image sequence.
  2. Power control: custom property tv_power (0.0..1.0) on crt_tv.
     0 = off (dark glass), 1 = on (emissive screen content).
     Drives the material mix AND the TV glow light.
  3. TV_Glow: a cool point light in front of the screen that fades in with
     power, so the TV throws light on the room when on.

Usage (headless):
    blender -b 3d-assets/living_room.blend \
        --python 3d-assets/living-room/tv/tv_setup.py

Toggle power afterwards (or animate it):
    bpy.data.objects["crt_tv"]["tv_power"] = 1.0  # on  (0.0 = off)
    # then render — the cj_tv_apply_power frame-change handler installed by
    # this script reads tv_power fresh at every frame change and switches the
    # screen + glow light. Keyframing tv_power works too (standard workflow).

  NOTE (Blender 4.0 headless): drivers alone do NOT reach bpy.ops.render.render()
  in this environment (verified: neither update_tag() nor keyframes propagate
  them) — the handler is what makes headless renders honor the switch. Drivers
  are still installed for live interactive use. Handlers don't persist in the
  .blend, so re-run this script in any fresh session before headless renders.

Idempotent: safe to re-run; it rebuilds the screen node tree and reuses the
existing image datablock / light if present.
"""

import os
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME_1 = os.path.join(HERE, "frames", "tv_show_0001.png")
SEQ_NAME = "tv_show_seq"
SEQ_FRAMES = 48
GLOW_NAME = "TV_Glow"

# ---------------------------------------------------------------- screen image
img = bpy.data.images.get(SEQ_NAME)
if img is None:
    img = bpy.data.images.load(FRAME_1)
    img.name = SEQ_NAME
else:
    img.filepath = FRAME_1
    img.reload()
img.source = "SEQUENCE"

# ---------------------------------------------------------------- power property
tv = bpy.data.objects.get("crt_tv")
if tv is None:
    raise RuntimeError("crt_tv not found in this .blend")
tv["tv_power"] = float(tv.get("tv_power", 0.0))
try:  # nice slider in the UI; harmless if the API shifts
    ui = tv.id_properties_ui("tv_power")
    ui.update(min=0.0, max=1.0, description="TV power: 0 = off (dark glass), 1 = on")
except Exception:
    pass


def power_driver(target, data_path, expression="p"):
    """Add/replace a driver reading crt_tv['tv_power'] as variable p."""
    drv = target.driver_add(data_path).driver
    while drv.variables:
        drv.variables.remove(drv.variables[0])
    var = drv.variables.new()
    var.name = "p"
    var.type = "SINGLE_PROP"
    var.targets[0].id = tv
    var.targets[0].data_path = '["tv_power"]'
    drv.type = "SCRIPTED"
    drv.expression = expression
    return drv


# ---------------------------------------------------------------- screen material
mat = bpy.data.materials.get("tvScreenMat")
if mat is None:
    raise RuntimeError("tvScreenMat not found in this .blend")
mat.use_nodes = True
nt = mat.node_tree
nt.nodes.clear()

out = nt.nodes.new("ShaderNodeOutputMaterial")
mix = nt.nodes.new("ShaderNodeMixShader")
glass = nt.nodes.new("ShaderNodeBsdfPrincipled")
emis = nt.nodes.new("ShaderNodeEmission")
tex = nt.nodes.new("ShaderNodeTexImage")
coord = nt.nodes.new("ShaderNodeTexCoord")
mapping = nt.nodes.new("ShaderNodeMapping")

tex.image = img
tex.image_user.frame_duration = SEQ_FRAMES
tex.image_user.frame_start = 1
tex.image_user.use_cyclic = True
tex.image_user.use_auto_refresh = True

# OFF state: dark glass (canon-adjacent near-black, NOT a color change to the room)
glass.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
glass.inputs["Roughness"].default_value = 0.25
glass.inputs["Specular IOR Level"].default_value = 0.5

# ON state: emissive screen content
emis.inputs["Strength"].default_value = 2.2

nt.links.new(coord.outputs["UV"], mapping.inputs["Vector"])
nt.links.new(mapping.outputs["Vector"], tex.inputs["Vector"])
nt.links.new(tex.outputs["Color"], emis.inputs["Color"])
nt.links.new(glass.outputs["BSDF"], mix.inputs[1])
nt.links.new(emis.outputs["Emission"], mix.inputs[2])
nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])

for n, (x, y) in ((coord, (-600, 200)), (mapping, (-420, 200)),
                  (tex, (-200, 200)), (emis, (0, 300)), (glass, (0, 0)),
                  (mix, (220, 150)), (out, (420, 150))):
    n.location = (x, y)

power_driver(mix.inputs[0], "default_value")  # 0 -> glass, 1 -> emission

# ---------------------------------------------------------------- TV glow light
glow = bpy.data.objects.get(GLOW_NAME)
if glow is None:
    bpy.ops.object.light_add(type="POINT", location=(-0.9, 2.02, 1.05))
    glow = bpy.context.active_object
    glow.name = GLOW_NAME
glow.location = (-0.9, 2.02, 1.05)
glow.data.color = (1.0, 0.97, 0.92)   # cool TV spill
glow.data.cutoff_distance = 4.5
glow.data.use_shadow = False             # cheap; room lights own the shadows
power_driver(glow.data, "energy", "p * 14.0")

# ------------------------------------------- render-time power application
# Blender 4.0 headless quirk (verified 2026-10-17): drivers on the screen mix
# and the glow light evaluate in the viewport depsgraph but do NOT propagate
# into bpy.ops.render.render() — neither update_tag() after writing tv_power
# nor keyframing the property changes that. This frame-change handler reads
# tv_power fresh and writes the driven values directly, so renders always
# honor the power switch. The drivers above stay installed for interactive
# use (they work live in the viewport); both write the same values.
def cj_tv_apply_power(scene):
    tv_obj = bpy.data.objects.get("crt_tv")
    p = float(tv_obj.get("tv_power", 0.0)) if tv_obj else 0.0
    p = max(0.0, min(1.0, p))
    mat2 = bpy.data.materials.get("tvScreenMat")
    if mat2 and mat2.node_tree:
        for n in mat2.node_tree.nodes:
            if n.type == "MIX_SHADER":
                n.inputs[0].default_value = p
    glow_obj = bpy.data.objects.get(GLOW_NAME)
    if glow_obj:
        glow_obj.data.energy = p * 14.0


_handlers = bpy.app.handlers.frame_change_pre
for _f in [_f for _f in _handlers if getattr(_f, "__name__", "") == "cj_tv_apply_power"]:
    _handlers.remove(_f)
_handlers.append(cj_tv_apply_power)

print(f"[tv_setup] screen sequence wired ({SEQ_FRAMES} frames), "
      f"tv_power={tv['tv_power']}, glow light '{GLOW_NAME}' ready, "
      f"render handler installed")

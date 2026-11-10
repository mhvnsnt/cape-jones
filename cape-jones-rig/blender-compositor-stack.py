"""
blender-compositor-stack.py — Blender 5.2.3 LTS compositor node tree
for the Cape Jones stack (same order and names as apply_compositor.py
and compositor-stack-spec.json).

Run headless with Blender 5.2.3 LTS ONLY (NOT 4.5.3):
  ~/workspace/tools-industry/blender-5.2.3-linux-x64/blender \
    --background --python blender-compositor-stack.py \
    -- <condition> <background.jpg> <rig.png> <output.blend>

Blender 5.2 API, verified by probe in this project (do NOT use older API):
 - Compositor tree is scene.compositing_node_group: create a
   CompositorNodeTree group and assign it (use_nodes deprecation warning ok).
 - Mix node type is ShaderNodeMixRGB (CompositorNodeMixRGB is UNDEFINED in 5.2).
   Its inputs are Factor (VALUE), Color1 (RGBA), Color2 (RGBA), in that order.
   blend_type is an attribute: MIX / ADD / SCREEN / MULTIPLY all settable.
 - Math node type is ShaderNodeMath (CompositorNodeMath is UNDEFINED in 5.2).
   operation is an attribute: ADD / SUBTRACT / MULTIPLY all settable.
 - AlphaOver inputs are Background = inputs[0], Foreground = inputs[1].
   Getting this wrong washes the composite to white/grey.
 - DilateErode inputs are Mask, Size (INT), Type, Falloff Size, Falloff.
   Size positive = dilate. Type default 'Steps' is left alone.
   There is NO .mode / .distance attribute in 5.2.
 - ColorBalance lift/gain are INPUT SOCKETS in 5.2, not attributes.
   This script does not use ColorBalance at all: the colour-key tint
   is a MixRGB MULTIPLY by the spec multiplier, which is exactly what
   the tint is.
 - Glare Type is the string 'Fog Glow' (not 'FOG_GLOW').
   Glare Threshold / Size / Strength are SOCKETS. Size in 5.2 is
   normalised (default 0.5), not pixels, so it is set to 0.5 here.
 - Group output: tree.interface.new_socket(name='Image',
   in_out='OUTPUT', socket_type='NodeSocketColor'), then link to
   NodeGroupOutput inputs['Image'].

This script builds the node tree and saves a .blend. It does NOT claim a
render unless the caller also renders and views the output image.
Per-shot refinements still owed (see WIRED-COMPOSITOR-STATUS.md):
 - per-plane fog (this build has no fog node; fog is in the PIL stack),
 - per-side internal-light mask (this build uses scalar factors),
 - god-ray shafts (must come from a light-shaft render or a painted
   shaft layer supplied per shot; no fake cone is built here),
 - LUT: the .cube path is recorded in a text block 'LUT_PATH'.
   Blender 5.2's compositor has no native .cube node, so claiming one
   would be false. Load the .cube in Natron/Resolve or Blender VSE
   colour management.
"""
import sys, os, json

try:
    import bpy
except ImportError:
    raise SystemExit("This script must run inside Blender 5.2.3: blender --background --python blender-compositor-stack.py -- <args>")

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_PATH = os.path.join(HERE, "compositor-stack-spec.json")


def hex_rgba(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)


def build(condition, bg_path, rig_path, out_blend):
    with open(SPEC_PATH) as f:
        spec = json.load(f)
    if condition not in spec["conditions"]:
        raise SystemExit(f"unknown condition {condition}; known: {sorted(spec['conditions'])}")
    c = spec["conditions"][condition]

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = bpy.data.node_groups.new("CapeJonesCompositorStack", "CompositorNodeTree")
    scene.compositing_node_group = tree
    nodes = tree.nodes
    links = tree.links
    nodes.clear()

    def node(ntype, name, x, y):
        n = nodes.new(ntype)
        n.name = name
        n.label = name
        n.location = (x, y)
        return n

    def mix(blend, name, x, y, fac, col1_link=None, col2_rgb=None):
        n = node("ShaderNodeMixRGB", name, x, y)
        n.blend_type = blend
        n.inputs["Factor"].default_value = fac
        if col1_link is not None:
            links.new(col1_link, n.inputs["Color1"])
        if col2_rgb is not None:
            n.inputs["Color2"].default_value = col2_rgb
        return n

    # Inputs
    bg = node("CompositorNodeImage", "Background", -1000, 300)
    if os.path.exists(bg_path):
        bg.image = bpy.data.images.load(bg_path)
    rig = node("CompositorNodeImage", "Character_untouched", -1000, -300)
    if os.path.exists(rig_path):
        rig.image = bpy.data.images.load(rig_path)

    # 2_color_key_tint_background_only: MixRGB MULTIPLY by spec multiplier.
    mult = c["lut_multiplier"]
    tint = mix("MULTIPLY", "ColorKeyTint_bg_only", -750, 300, 1.0,
               col1_link=bg.outputs["Image"],
               col2_rgb=(mult[0], mult[1], mult[2], 1.0))

    # 5_hard_shadow: rig alpha -> Blur -> MixRGB MULTIPLY by shadow hue.
    shadow_blur = node("CompositorNodeBlur", "HardShadow_Blur", -750, -450)
    shadow_blur.inputs[1].default_value = (3.0, 3.0)
    links.new(rig.outputs["Alpha"], shadow_blur.inputs["Image"])
    shadow = mix("MULTIPLY", "HardShadow_Colour", -500, -450,
                 float(c["shadow_opacity"]),
                 col1_link=shadow_blur.outputs["Image"],
                 col2_rgb=hex_rgba(c["shadow_hue"]))
    # Note: MixRGB MULTIPLY with Factor=opacity blends colour*alpha toward
    # the input; the ground-flattening transform for the shadow is a
    # per-shot placement (see PIL stack), not faked here.

    # Shadow under character: AlphaOver(bg_tint, shadow), then character over that.
    over_shadow = node("CompositorNodeAlphaOver", "AlphaOver_shadow_under", -500, 100)
    links.new(tint.outputs["Color"], over_shadow.inputs["Background"])
    links.new(shadow.outputs["Color"], over_shadow.inputs["Foreground"])
    over_bg = node("CompositorNodeAlphaOver", "AlphaOver_bg_character", -250, 100)
    links.new(over_shadow.outputs["Image"], over_bg.inputs["Background"])
    links.new(rig.outputs["Image"], over_bg.inputs["Foreground"])
    last = over_bg
    last_out = "Image"

    # 9_rim_outer_only_Add: Dilate(rim_px) - original alpha, MixRGB ADD,
    # Factor = rim mask (per-pixel), Color1 = composite, Color2 = rim colour.
    dilate = node("CompositorNodeDilateErode", "Rim_Dilate", -250, 450)
    dilate.inputs["Size"].default_value = int(c["rim_px"])
    links.new(rig.outputs["Alpha"], dilate.inputs["Mask"])
    sub = node("ShaderNodeMath", "Rim_SubtractOriginal", 0, 450)
    sub.operation = "SUBTRACT"
    links.new(dilate.outputs["Mask"], sub.inputs[0])
    links.new(rig.outputs["Alpha"], sub.inputs[1])
    rim = node("ShaderNodeMixRGB", "Rim_Add", 250, 450)
    rim.blend_type = "ADD"
    links.new(sub.outputs["Value"], rim.inputs["Factor"])
    links.new(last.outputs[last_out], rim.inputs["Color1"])
    rim.inputs["Color2"].default_value = hex_rgba(c["rim_color"])
    last, last_out = rim, "Color"

    # 10_bleed_edge_band_Screen: Dilate(rim+5) - Dilate(rim), * opacity, MixRGB SCREEN.
    dilate_b = node("CompositorNodeDilateErode", "Bleed_Dilate", -250, 650)
    dilate_b.inputs["Size"].default_value = int(c["rim_px"]) + 5
    links.new(rig.outputs["Alpha"], dilate_b.inputs["Mask"])
    sub_b = node("ShaderNodeMath", "Bleed_SubtractRim", 0, 650)
    sub_b.operation = "SUBTRACT"
    links.new(dilate_b.outputs["Mask"], sub_b.inputs[0])
    links.new(dilate.outputs["Mask"], sub_b.inputs[1])
    mul_b = node("ShaderNodeMath", "Bleed_Opacity", 250, 650)
    mul_b.operation = "MULTIPLY"
    links.new(sub_b.outputs["Value"], mul_b.inputs[0])
    mul_b.inputs[1].default_value = float(c["bleed_opacity"])
    bleed = node("ShaderNodeMixRGB", "Bleed_Screen", 500, 650)
    bleed.blend_type = "SCREEN"
    links.new(mul_b.outputs["Value"], bleed.inputs["Factor"])
    links.new(last.outputs[last_out], bleed.inputs["Color1"])
    bleed.inputs["Color2"].default_value = hex_rgba(c["bleed_color"])
    last, last_out = bleed, "Color"

    # 7_internal_light_Screen (scalar factor; per-side mask is per-shot).
    light = mix("SCREEN", "InternalLight_Screen", 750, 450,
                float(c["light_opacity"]),
                col1_link=last.outputs[last_out],
                col2_rgb=hex_rgba(c["light_color"]))
    last, last_out = light, "Color"

    # 8_internal_shadow_Multiply (scalar factor; per-side mask is per-shot).
    shadow2 = mix("MULTIPLY", "InternalShadow_Multiply", 1000, 450,
                  float(c["shadow_opacity"]) * 0.6,
                  col1_link=last.outputs[last_out],
                  col2_rgb=hex_rgba(c["shadow_hue"]))
    last, last_out = shadow2, "Color"

    # 11_bloom_glow: Glare, Fog Glow, parameters via sockets.
    glare = node("CompositorNodeGlare", "Bloom_GlareFogGlow", 1250, 450)
    glare.inputs["Type"].default_value = "Fog Glow"
    glare.inputs["Threshold"].default_value = 0.85
    glare.inputs["Size"].default_value = 0.5
    glare.inputs["Strength"].default_value = 0.25
    links.new(last.outputs[last_out], glare.inputs["Image"])
    last, last_out = glare, "Image"

    # Output
    # Fresh tree: no output socket yet. new_socket creates it; the
    # probe verified out.inputs then shows [('Image', 'RGBA'), ...].
    tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    out = nodes.new("NodeGroupOutput")
    out.name = "Output"
    out.location = (1500, 450)
    links.new(last.outputs[last_out], out.inputs["Image"])

    txt_name = "LUT_PATH"
    if txt_name in bpy.data.texts:
        txt = bpy.data.texts[txt_name]
        txt.clear()
    else:
        txt = bpy.data.texts.new(txt_name)
    txt.write(f"Condition: {condition}\nLUT (template, not final approved): {c['lut']}\n"
              f"Load this .cube in Natron/Resolve or Blender VSE colour management.\n"
              f"Blender 5.2 compositor has no native .cube node; do not claim one.\n"
              f"Rim: {c['rim_px']}px {c['rim_color']} Add, outer only.\n"
              f"Bleed: {c['bleed_color']} Screen {c['bleed_opacity']}, edge band only.\n")

    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print(f"Blender node tree saved: {out_blend}")
    print(f"Nodes: {[n.name for n in nodes]}")
    return out_blend


def main():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    if len(argv) < 4:
        print("Usage: blender --background --python blender-compositor-stack.py -- <condition> <background.jpg> <rig.png> <output.blend>")
        raise SystemExit(2)
    build(argv[0], argv[1], argv[2], argv[3])


if __name__ == "__main__":
    main()

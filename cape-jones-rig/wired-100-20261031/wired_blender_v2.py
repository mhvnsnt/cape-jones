#!/usr/bin/env python3
"""Wired Blender v2 — full-height Level 2 with the previously-owed pieces,
all as FULL-SIZE nodes (small-image placement failed in 5.2, proven in the
proof report, so masks are 1100x1500 images, never small strips):
  * shadow = PIL ellipse + two foot pads mask (not a squashed blob)
  * internal line light = PIL inner-edge mask, warm, lit side only
  * lit-side rim/bleed fade = PIL left(1.0)->right(0.3) gradient mask
  * full height 1100x1500 (not 660x900), view transform passed in
Run: blender --background --python wired_blender_v2.py -- <pose> <view> <display> <out.png> <out.blend>
Base art is never modified in place; grade/rim/bleed/shadow/line are layers.
"""
import sys, os, time
try:
    import bpy
except ImportError:
    raise SystemExit("run inside Blender 5.2.3")
GREY_CENTRE = 0.216
GREY_TOL = 0.044
RED_LIMIT = 100

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lin_rgb(r, g, b):
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), 1.0)

GAIN = (1.10, 0.95, 0.70, 1.0)
RIM_LIN = lin_rgb(255, 180, 80)
BLEED_LIN = lin_rgb(255, 120, 0)
SHADOW_LIN = lin_rgb(40, 40, 90)

def count_pure_red(img):
    px = img.pixels[:]
    return sum(1 for i in range(0, len(px), 4) if px[i] > 0.99 and px[i+1] < 0.01 and px[i+2] < 0.01)

def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    pose_path, view_transform, display_device, out_png, out_blend = argv[:5]
    pose_path, out_png, out_blend = map(os.path.abspath, (pose_path, out_png, out_blend))
    rig = os.path.dirname(os.path.dirname(out_png))
    # masks live in the same wired folder as the outputs
    wdir = os.path.dirname(out_png)
    shadow_mask_p = os.path.join(wdir, "wired-blender-shadow-ellipse-pads-mask-20261031.png")
    line_mask_p = os.path.join(wdir, "wired-blender-linellight-mask-20261031.png")
    fade_mask_p = os.path.join(wdir, "wired-blender-fade-mask-20261031.png")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    probe = bpy.data.images.load(pose_path)
    red = count_pure_red(probe)
    print(f"LABEL GATE pure-red={red} limit={RED_LIMIT}")
    if red > RED_LIMIT:
        raise SystemExit("REFUSED: labelled plate")
    W, H = probe.size
    print(f"PLATE {W}x{H}")
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x, scene.render.resolution_y = W, H
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.filepath = out_png
    scene.view_settings.view_transform = view_transform
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.display_settings.display_device = display_device
    scene.use_nodes = True
    tree = bpy.data.node_groups.new("WiredBlenderV2", "CompositorNodeTree")
    scene.compositing_node_group = tree
    nodes, links = tree.nodes, tree.links
    nodes.clear()

    def node(ntype, name, x, y):
        n = nodes.new(ntype); n.name = name; n.label = name; n.location = (x, y); return n

    def math(op, name, x, y, v0=None, v1=None, l0=None, l1=None):
        n = node("ShaderNodeMath", name, x, y); n.operation = op
        if v0 is not None: n.inputs[0].default_value = v0
        if v1 is not None: n.inputs[1].default_value = v1
        if l0 is not None: links.new(l0, n.inputs[0])
        if l1 is not None: links.new(l1, n.inputs[1])
        return n

    def mix(blend, name, x, y, fac, c1_link=None, c2_rgb=None):
        n = node("ShaderNodeMixRGB", name, x, y); n.blend_type = blend
        n.inputs["Factor"].default_value = fac
        if c1_link is not None: links.new(c1_link, n.inputs["Color1"])
        if c2_rgb is not None: n.inputs["Color2"].default_value = c2_rgb
        return n

    def img_node(path, name, x, y):
        n = node("CompositorNodeImage", name, x, y)
        n.image = bpy.data.images.load(path)
        return n

    def mask_value(imgnode, name, x, y):
        """Image -> SeparateColor -> Red channel = grayscale mask value."""
        s = node("CompositorNodeSeparateColor", name, x, y)
        links.new(imgnode.outputs["Image"], s.inputs["Image"])
        return s.outputs["Red"]

    char = node("CompositorNodeImage", "Character_untouched", -1200, 0); char.image = probe
    sep = node("CompositorNodeSeparateColor", "Separate_R_G_B", -950, 0)
    links.new(char.outputs["Image"], sep.inputs["Image"])
    diffs = []
    for ch in ("Red", "Green", "Blue"):
        sub = math("SUBTRACT", f"KeyDiff_{ch}_sub", -700, 200, l0=sep.outputs[ch], v1=GREY_CENTRE)
        ab = math("ABSOLUTE", f"KeyDiff_{ch}_abs", -550, 200, l0=sub.outputs["Value"])
        diffs.append(ab)
    max_rg = math("MAXIMUM", "KeyMax_RG", -400, 200, l0=diffs[0].outputs["Value"], l1=diffs[1].outputs["Value"])
    max_rgb = math("MAXIMUM", "KeyMax_RGB", -250, 200, l0=max_rg.outputs["Value"], l1=diffs[2].outputs["Value"])
    key_mask = math("GREATER_THAN", "KeyMask_grey128", -100, 200, l0=max_rgb.outputs["Value"], v1=GREY_TOL)
    blur = node("CompositorNodeBlur", "KeyMask_Blur", 50, 200); blur.inputs[1].default_value = (1.5, 1.5)
    links.new(key_mask.outputs["Value"], blur.inputs["Image"])
    sep_blur = node("CompositorNodeSeparateColor", "KeyMask_Blurred_R", 200, 200)
    links.new(blur.outputs["Image"], sep_blur.inputs["Image"])
    feathered = sep_blur.outputs["Red"]
    char_keyed = node("CompositorNodeSetAlpha", "Character_keyed", 350, 200)
    links.new(char.outputs["Image"], char_keyed.inputs["Image"]); links.new(feathered, char_keyed.inputs["Alpha"])

    # --- Shadow: full-size ellipse+pads mask, blurred, blue-violet x0.35 ---
    sh_img = img_node(shadow_mask_p, "ShadowMask_EllipsePads", 500, -500)
    sh_val = mask_value(sh_img, "ShadowMask_R", 650, -500)
    sh_blur = node("CompositorNodeBlur", "ShadowMask_Blur", 800, -500); sh_blur.inputs[1].default_value = (8.0, 8.0)
    links.new(sh_val, sh_blur.inputs["Image"])
    sh_sep = node("CompositorNodeSeparateColor", "ShadowMask_Blurred_R", 950, -500)
    links.new(sh_blur.outputs["Image"], sh_sep.inputs["Image"])
    sh_op = math("MULTIPLY", "Shadow_Opacity035", 1100, -500, l0=sh_sep.outputs["Red"], v1=0.35)
    solid = mix("MIX", "Shadow_SolidHue", 500, -700, 1.0, c2_rgb=SHADOW_LIN)
    solid.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)
    shadow = node("CompositorNodeSetAlpha", "Shadow_EllipsePads", 1250, -500)
    links.new(solid.outputs["Color"], shadow.inputs["Image"]); links.new(sh_op.outputs["Value"], shadow.inputs["Alpha"])
    over_shadow = node("CompositorNodeAlphaOver", "AlphaOver_shadow_under", 1400, 0)
    links.new(char.outputs["Image"], over_shadow.inputs["Background"]); links.new(shadow.outputs["Image"], over_shadow.inputs["Foreground"])

    # --- Graded character ---
    graded = mix("MULTIPLY", "Grade_Gain_110_095_070", 1550, 200, 1.0, c1_link=char_keyed.outputs["Image"], c2_rgb=GAIN)
    over_char = node("CompositorNodeAlphaOver", "AlphaOver_graded_character", 1700, 0)
    links.new(over_shadow.outputs["Image"], over_char.inputs["Background"]); links.new(graded.outputs["Color"], over_char.inputs["Foreground"])
    last, last_out = over_char, "Image"

    # --- Fade mask (lit side 1.0 -> opposite 0.3) ---
    fade_img = img_node(fade_mask_p, "FadeMask_LitSide", 500, 900)
    fade = mask_value(fade_img, "FadeMask_R", 650, 900)

    # --- Rim outer-only ADD, factor = rim band x fade ---
    dil3 = node("CompositorNodeDilateErode", "Rim_Dilate3", 1850, 400); dil3.inputs["Size"].default_value = 3
    links.new(key_mask.outputs["Value"], dil3.inputs["Mask"])
    rim_sub = math("SUBTRACT", "Rim_SubtractOriginal", 2000, 400, l0=dil3.outputs["Mask"], l1=key_mask.outputs["Value"])
    rim_fac = math("MULTIPLY", "Rim_Factor_x_Fade", 2150, 400, l0=rim_sub.outputs["Value"], l1=fade)
    rim = node("ShaderNodeMixRGB", "Rim_Add_warm_amber_faded", 2300, 400); rim.blend_type = "ADD"
    links.new(rim_fac.outputs["Value"], rim.inputs["Factor"]); links.new(last.outputs[last_out], rim.inputs["Color1"])
    rim.inputs["Color2"].default_value = RIM_LIN
    last, last_out = rim, "Color"

    # --- Bleed band 3..8px SCREEN, factor = band x fade x 0.20 ---
    dil8 = node("CompositorNodeDilateErode", "Bleed_Dilate8", 1850, 650); dil8.inputs["Size"].default_value = 8
    links.new(key_mask.outputs["Value"], dil8.inputs["Mask"])
    bleed_sub = math("SUBTRACT", "Bleed_SubtractRim", 2000, 650, l0=dil8.outputs["Mask"], l1=dil3.outputs["Mask"])
    bleed_f = math("MULTIPLY", "Bleed_Factor_x_Fade", 2150, 650, l0=bleed_sub.outputs["Value"], l1=fade)
    bleed_op = math("MULTIPLY", "Bleed_Opacity020", 2300, 650, l0=bleed_f.outputs["Value"], v1=0.20)
    bleed = node("ShaderNodeMixRGB", "Bleed_Screen_orange_faded", 2450, 650); bleed.blend_type = "SCREEN"
    links.new(bleed_op.outputs["Value"], bleed.inputs["Factor"]); links.new(last.outputs[last_out], bleed.inputs["Color1"])
    bleed.inputs["Color2"].default_value = BLEED_LIN
    last, last_out = bleed, "Color"

    # --- Internal line light: line mask x keyed alpha, SCREEN warm x 0.5 ---
    line_img = img_node(line_mask_p, "LineLightMask", 500, 1150)
    line_val = mask_value(line_img, "LineLightMask_R", 650, 1150)
    line_in = math("MULTIPLY", "LineLight_Inside", 800, 1150, l0=line_val, l1=feathered)
    line_op = math("MULTIPLY", "LineLight_Opacity050", 950, 1150, l0=line_in.outputs["Value"], v1=0.50)
    linelight = node("ShaderNodeMixRGB", "LineLight_Screen_warm", 2600, 650); linelight.blend_type = "SCREEN"
    links.new(line_op.outputs["Value"], linelight.inputs["Factor"]); links.new(last.outputs[last_out], linelight.inputs["Color1"])
    linelight.inputs["Color2"].default_value = RIM_LIN
    last, last_out = linelight, "Color"

    tree.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    out = nodes.new("NodeGroupOutput"); out.name = "Output"; out.location = (2800, 200)
    links.new(last.outputs[last_out], out.inputs["Image"])
    txt = bpy.data.texts.new("SHOT_SPEC") if "SHOT_SPEC" not in bpy.data.texts else bpy.data.texts["SHOT_SPEC"]
    txt.clear(); txt.write(f"Wired Blender v2 full-height {W}x{H}, view {view_transform}/{display_device}\nShadow: full-size ellipse+pads mask (not squashed blob). Line light: inner-edge mask SCREEN warm x0.5. Rim/bleed: lit-side fade mask 1.0->0.3.\nBase art untouched. PROOF ONLY - not Mars-approved.\n")
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    t0 = time.time()
    print(f"NODES {len(nodes)} LINKS {len(links)}")
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {out_png} exists={os.path.exists(out_png)} size={os.path.getsize(out_png) if os.path.exists(out_png) else 0}")

if __name__ == "__main__":
    main()

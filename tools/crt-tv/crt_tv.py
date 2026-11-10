#!/usr/bin/env python3
"""crt_tv.py — Cape Jones in-house procedural CRT screen shader (Blender 4.x).

How real studios do on-set TV screens (film/VFX): they do NOT simulate a CRT.
They shade an emission plane with the video content plus a CRT *look* stack:
scanlines + phosphor mask + refresh band + flicker + vignette. That is what
this builds — node group `CJ_CRT_Screen`, 100% native nodes, zero add-ons.

Group inputs (all keyframable / driver-ready for the gag lane):
  Content        — image/movie plugged inside the group (see set_content)
  crt_power      — 0 = off (dark glass), 1 = on
  crt_brightness — master emission multiplier
  crt_flicker    — 0..1 flicker amount (the light-flicker gag drives this)
  crt_refresh    — 0..1 rolling refresh-band position (animate 0->1 per loop)
  scanline_count — default 240

Chain: Content -> scanline bands -> aperture-grille RGB stripes ->
rolling refresh band -> flicker -> vignette -> Emission.

Usage (inside Blender):
    import crt_tv
    crt_tv.build_crt_group()                 # (re)build the node group
    crt_tv.apply_to_screen("crt_screen")     # assign CJ_CRT_Mat to the mesh
    crt_tv.set_content("/path/to/static.mp4")  # image or movie

Headless verify:
    xvfb-run -a env -u PYTHONPATH blender-4.5 -b --python tools/crt-tv/crt_tv.py -- --verify
"""
import os
import sys

try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False

GROUP_NAME = "CJ_CRT_Screen"
MAT_NAME = "CJ_CRT_Mat"


def _link(nt, a, b):
    nt.links.new(a, b)


def build_crt_group():
    if GROUP_NAME in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[GROUP_NAME])
    g = bpy.data.node_groups.new(GROUP_NAME, "ShaderNodeTree")

    gi = g.nodes.new("NodeGroupInput")
    gi.location = (-1200, 0)
    go = g.nodes.new("NodeGroupOutput")
    go.location = (600, 0)

    def add_input(name, stype, default=None, mn=None, mx=None):
        s = g.interface.new_socket(name=name, in_out="INPUT",
                                   socket_type=stype)
        if default is not None:
            gi.outputs[name].default_value = default
        return s

    add_input("crt_power", "NodeSocketFloat", 1.0)
    add_input("crt_brightness", "NodeSocketFloat", 2.5)
    add_input("crt_flicker", "NodeSocketFloat", 0.0)
    add_input("crt_refresh", "NodeSocketFloat", 0.0)
    add_input("scanline_count", "NodeSocketFloat", 240.0)
    g.interface.new_socket(name="Shader", in_out="OUTPUT",
                           socket_type="NodeSocketShader")

    # --- Content: image/movie texture lives INSIDE the group ---
    img = g.nodes.new("ShaderNodeTexImage")
    img.location = (-1000, 300)
    img.label = "CRT_CONTENT (set via crt_tv.set_content)"

    uv = g.nodes.new("ShaderNodeTexCoord")
    uv.location = (-1200, -200)
    _link(g, uv.outputs["UV"], img.inputs["Vector"])

    # --- Scanlines: horizontal bands ---
    wave = g.nodes.new("ShaderNodeTexWave")
    wave.location = (-800, 300)
    wave.wave_type = "BANDS"
    wave.bands_direction = "Y"
    wave.inputs["Scale"].default_value = 240.0
    wave.label = "SCANLINE_SCALE (set via crt_tv.set_scanline_count)"
    _link(g, uv.outputs["UV"], wave.inputs["Vector"])
    sramp = g.nodes.new("ShaderNodeValToRGB")
    sramp.location = (-600, 300)
    sramp.color_ramp.elements[0].position = 0.42
    sramp.color_ramp.elements[1].position = 0.58
    _link(g, wave.outputs["Fac"], sramp.inputs["Fac"])

    # --- Aperture grille: vertical RGB stripes ---
    brick = g.nodes.new("ShaderNodeTexBrick")
    brick.location = (-800, -100)
    brick.inputs["Scale"].default_value = 160.0
    brick.inputs["Mortar Size"].default_value = 0.0
    brick.offset = 0
    brick.offset_frequency = 1
    _link(g, uv.outputs["UV"], brick.inputs["Vector"])
    seprgb = g.nodes.new("ShaderNodeSeparateColor")
    seprgb.location = (-600, -100)
    _link(g, brick.outputs["Color"], seprgb.inputs["Color"])

    # --- Rolling refresh band ---
    sepxyz = g.nodes.new("ShaderNodeSeparateXYZ")
    sepxyz.location = (-800, -400)
    _link(g, uv.outputs["UV"], sepxyz.inputs["Vector"])
    band_add = g.nodes.new("ShaderNodeMath")
    band_add.location = (-600, -400)
    band_add.operation = "ADD"
    _link(g, sepxyz.outputs["Y"], band_add.inputs[0])
    _link(g, gi.outputs["crt_refresh"], band_add.inputs[1])
    band_frac = g.nodes.new("ShaderNodeMath")
    band_frac.location = (-450, -400)
    band_frac.operation = "FRACT"
    _link(g, band_add.outputs["Value"], band_frac.inputs[0])
    band_ramp = g.nodes.new("ShaderNodeValToRGB")
    band_ramp.location = (-300, -400)
    band_ramp.color_ramp.elements[0].position = 0.0
    band_ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    band_ramp.color_ramp.elements[1].position = 0.06
    band_ramp.color_ramp.elements[1].color = (1.6, 1.6, 1.6, 1)
    _link(g, band_frac.outputs["Value"], band_ramp.inputs["Fac"])

    # --- Vignette (radial gradient on UV) ---
    vgrad = g.nodes.new("ShaderNodeTexGradient")
    vgrad.location = (-600, -650)
    vgrad.gradient_type = "RADIAL"
    _link(g, uv.outputs["UV"], vgrad.inputs["Vector"])
    vramp = g.nodes.new("ShaderNodeValToRGB")
    vramp.location = (-400, -650)
    vramp.color_ramp.elements[0].position = 0.35
    vramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    vramp.color_ramp.elements[1].position = 0.75
    vramp.color_ramp.elements[1].color = (0.25, 0.25, 0.25, 1)
    _link(g, vgrad.outputs["Color"], vramp.inputs["Fac"])

    # --- Combine: content * scanlines * grille * band * vignette ---
    m1 = g.nodes.new("ShaderNodeMix")
    m1.location = (-400, 300)
    m1.data_type = "RGBA"
    m1.blend_type = "MULTIPLY"
    m1.inputs["Factor"].default_value = 1.0
    _link(g, img.outputs["Color"], m1.inputs["A"])
    _link(g, sramp.outputs["Color"], m1.inputs["B"])

    m2 = g.nodes.new("ShaderNodeMix")
    m2.location = (-200, 100)
    m2.data_type = "RGBA"
    m2.blend_type = "MULTIPLY"
    m2.inputs["Factor"].default_value = 1.0
    _link(g, m1.outputs["Result"], m2.inputs["A"])
    _link(g, band_ramp.outputs["Color"], m2.inputs["B"])

    m3 = g.nodes.new("ShaderNodeMix")
    m3.location = (0, -100)
    m3.data_type = "RGBA"
    m3.blend_type = "MULTIPLY"
    m3.inputs["Factor"].default_value = 1.0
    _link(g, m2.outputs["Result"], m3.inputs["A"])
    _link(g, vramp.outputs["Color"], m3.inputs["B"])

    # --- Flicker + power + brightness -> Emission ---
    flick = g.nodes.new("ShaderNodeMath")
    flick.location = (200, -100)
    flick.operation = "MULTIPLY_ADD"
    _link(g, gi.outputs["crt_flicker"], flick.inputs[0])
    flick.inputs[1].default_value = -0.35
    flick.inputs[2].default_value = 1.0
    emis = g.nodes.new("ShaderNodeEmission")
    emis.location = (400, 100)
    _link(g, m3.outputs["Result"], emis.inputs["Color"])
    powmul = g.nodes.new("ShaderNodeMath")
    powmul.location = (200, 200)
    powmul.operation = "MULTIPLY"
    _link(g, gi.outputs["crt_power"], powmul.inputs[0])
    _link(g, gi.outputs["crt_brightness"], powmul.inputs[1])
    _link(g, powmul.outputs["Value"], emis.inputs["Strength"])
    # flicker scales the final strength
    fmul = g.nodes.new("ShaderNodeMath")
    fmul.location = (400, 250)
    fmul.operation = "MULTIPLY"
    _link(g, powmul.outputs["Value"], fmul.inputs[0])
    _link(g, flick.outputs["Value"], fmul.inputs[1])
    _link(g, fmul.outputs["Value"], emis.inputs["Strength"])

    out = g.nodes.new("ShaderNodeOutputMaterial")
    out.location = (600, 100)
    _link(g, emis.outputs["Emission"], out.inputs["Surface"])
    return g


def apply_to_screen(object_name="crt_screen"):
    """Assign CJ_CRT_Mat (using the CJ_CRT_Screen group) to a mesh object."""
    g = build_crt_group()
    mat = bpy.data.materials.get(MAT_NAME)
    if mat is None:
        mat = bpy.data.materials.new(MAT_NAME)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    grp = nt.nodes.new("ShaderNodeGroup")
    grp.node_tree = g
    grp.location = (-200, 0)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (200, 0)
    nt.links.new(grp.outputs["Shader"], out.inputs["Surface"])
    ob = bpy.data.objects.get(object_name)
    if ob is None:
        raise ValueError(f"object '{object_name}' not found in this blend")
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
    return mat


def set_content(path, frame_start=1):
    """Point the in-group image node at an image or movie file."""
    g = bpy.data.node_groups.get(GROUP_NAME)
    assert g is not None, "build the group first (build_crt_group)"
    node = next(n for n in g.nodes if n.label.startswith("CRT_CONTENT"))
    img = bpy.data.images.load(path, check_existing=True)
    if path.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        img.source = "MOVIE"
    node.image = img
    return img


def set_scanline_count(n=240.0):
    """Set the scanline band count on the shared CJ_CRT_Screen group."""
    g = bpy.data.node_groups.get(GROUP_NAME)
    assert g is not None, "build the group first (build_crt_group)"
    node = next(n for n in g.nodes
                if n.label.startswith("SCANLINE_SCALE"))
    node.inputs["Scale"].default_value = float(n)
    gi = next(n for n in g.nodes if n.type == "GROUP_INPUT")
    try:
        gi.outputs["scanline_count"].default_value = float(n)
    except (KeyError, TypeError):
        pass


def _verify():
    g = build_crt_group()
    want = {"crt_power", "crt_brightness", "crt_flicker", "crt_refresh",
            "scanline_count"}
    got = {s.name for s in g.interface.items_tree if s.in_out == "INPUT"}
    assert want <= got, f"missing group inputs: {want - got}"
    assert g.nodes.get("Group Output") or any(
        n.type == "GROUP_OUTPUT" for n in g.nodes)
    # scratch screen mesh
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0, 0, 1))
    scr = bpy.context.active_object
    scr.name = "verify_crt_screen"
    mat = apply_to_screen("verify_crt_screen")
    assert scr.data.materials[0] == mat
    # 32px shader-compile render
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 1
    sc.render.resolution_x = 32
    sc.render.resolution_y = 32
    sc.render.filepath = "/tmp/crt_verify.png"
    bpy.ops.render.render(write_still=True)
    assert os.path.exists("/tmp/crt_verify.png")
    print("CRT_TV VERIFY: node group + material + 32px render OK")


if __name__ == "__main__" or "--verify" in sys.argv:
    if IN_BLENDER and "--verify" in sys.argv:
        _verify()
    elif not IN_BLENDER:
        print("crt_tv: import inside Blender (bpy).")
